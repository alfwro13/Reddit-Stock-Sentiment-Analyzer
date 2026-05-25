import os
import re
import logging
from datetime import datetime
from typing import Dict, Any, List

import numpy as np
import pandas as pd
import praw
from dotenv import load_dotenv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure VADER lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

load_dotenv()

# Configure module-level logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - REDDIT_SENTIMENT - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RedditSentimentAnalyzer:
    """
    Analyzes Reddit sentiment for specific stock tickers by querying top finance 
    subreddits, extracting posts, and traversing top-level comments using VADER.
    """
    def __init__(self) -> None:
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'Quantamental-Sentiment-Engine/1.0')
        )
        self.sia = SentimentIntensityAnalyzer()

    def clean_text(self, text: str) -> str:
        """
        Strips URLs, markdown links, and disruptive special characters.
        Crucially preserves punctuation (!, ?, .) that VADER uses for intensity scoring.
        """
        if not isinstance(text, str):
            return ""
            
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove Reddit-style markdown links: [text](link) -> text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove special characters but KEEP punctuation needed by VADER
        text = re.sub(r'[^\w\s\?\!\.,]', '', text)
        
        return text.strip()

    def get_sentiment_score(self, text: str) -> float:
        """Calculates the VADER compound score (-1.0 to 1.0) for a given text."""
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return 0.0
            
        return self.sia.polarity_scores(cleaned_text)['compound']

    def analyze_submission_and_comments(self, submission, max_comments: int = 15) -> float:
        """
        Calculates the aggregate sentiment of a post AND its highest-voted comments.
        Prevents 'neutral' titles with highly opinionated comments from being misclassified.
        """
        scores: List[float] = []
        
        # 1. Score the main post (Title + Body)
        post_text = f"{submission.title}. {submission.selftext}"
        post_score = self.get_sentiment_score(post_text)
        
        # We append the main post score twice to give it a slightly higher base weight 
        # than an individual comment
        scores.extend([post_score, post_score])

        # 2. Traverse and score the comment forest
        try:
            # Flatten the comment tree, limit expansion to save API limits and time
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()
            
            # Sort by upvotes (score) to capture the accepted community narrative
            top_comments = sorted(comments, key=lambda c: c.score, reverse=True)[:max_comments]
            
            for comment in top_comments:
                comment_score = self.get_sentiment_score(comment.body)
                if comment_score != 0.0:  # Ignore perfectly neutral/empty comments
                    scores.append(comment_score)
                    
        except Exception as e:
            logger.warning(f"Failed to traverse comments for submission {submission.id}: {e}")

        if not scores:
            return 0.0
            
        # Return the unweighted average of the post + top comments
        return sum(scores) / len(scores)

    def get_reddit_posts(self, stock_symbol: str, limit: int = 50) -> pd.DataFrame:
        """
        Queries targeted financial subreddits for a ticker, extracts posts, 
        traverses comments, and compiles the DataFrame.
        """
        posts = []
        subreddits = 'stocks+investing+wallstreetbets'
        
        # Use exact match quotes around the ticker to prevent false positives 
        # (e.g., searching ALL without quotes matches the word "all")
        search_query = f'"{stock_symbol}"'
        
        logger.info(f"Querying Reddit API for {search_query} across {subreddits}...")
        
        try:
            for post in self.reddit.subreddit(subreddits).search(search_query, limit=limit, time_filter='month'):
                aggregate_sentiment = self.analyze_submission_and_comments(post, max_comments=15)
                
                posts.append({
                    'title': post.title,
                    'text': post.selftext,
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'sentiment': aggregate_sentiment,
                    'created_utc': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f'https://reddit.com{post.permalink}',
                    'subreddit': post.subreddit.display_name
                })
        except Exception as e:
            logger.error(f"Error fetching Reddit posts for {stock_symbol}: {e}")
            
        return pd.DataFrame(posts)

    def analyze_sentiment(self, stock_symbol: str) -> Dict[str, Any]:
        """
        Master method called by the Flask application. 
        Compiles the full weighted sentiment report.
        """
        posts_df = self.get_reddit_posts(stock_symbol)
        
        if posts_df.empty:
            return {
                'success': False,
                'error': f'No Reddit posts found for {stock_symbol}'
            }
        
        # Calculate an UPVOTE-WEIGHTED average sentiment.
        # This prevents a highly upvoted megathread from being diluted by 0-upvote spam posts.
        total_score = posts_df['score'].sum()
        if total_score > 0:
            weighted_avg_sentiment = np.average(posts_df['sentiment'], weights=posts_df['score'])
        else:
            weighted_avg_sentiment = posts_df['sentiment'].mean()
        
        # Categorize the sentiment for the frontend pie-chart/distribution
        posts_df['sentiment_category'] = posts_df['sentiment'].apply(
            lambda x: 'positive' if x > 0.05 else ('negative' if x < -0.05 else 'neutral')
        )
        
        sentiment_counts = posts_df['sentiment_category'].value_counts().to_dict()
        
        # Extract the top 5 most popular posts to display in the UI
        top_posts = posts_df.nlargest(5, 'score').to_dict('records')
        
        return {
            'success': True,
            'average_sentiment': float(weighted_avg_sentiment),
            'post_count': len(posts_df),
            'sentiment_distribution': sentiment_counts,
            'top_posts': top_posts
        }
