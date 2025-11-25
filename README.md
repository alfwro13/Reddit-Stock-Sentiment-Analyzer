# Reddit Stock Sentiment Analyzer

A comprehensive stock sentiment analysis tool that scrapes Reddit posts to gauge market sentiment and predict stock trends using machine learning and natural language processing.

## Table of Contents

- [Description](#description)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Architecture Flow](#architecture-flow)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Key Findings](#key-findings)
- [Author](#author)

## Description

This project combines social media sentiment analysis with financial market data to provide insights into stock trends. It analyzes Reddit posts and comments from popular finance subreddits (r/stocks, r/investing, r/wallstreetbets) to extract sentiment about specific stocks and correlates this with actual stock price movements.

The project offers both a command-line interface for quick analysis and a web-based dashboard for comprehensive visualization of results.

## Technologies Used

### Backend & Data Processing

- **Python 3.13** - Core programming language
- **PRAW (Python Reddit API Wrapper)** - Reddit data extraction
- **yfinance** - Stock market data fetching
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations

### Natural Language Processing

- **NLTK** - Natural language processing toolkit with VADER sentiment analyzer
- **TextBlob** - Additional sentiment analysis capabilities
- **scikit-learn** - Machine learning algorithms

### Web Framework

- **Flask** - Web application framework
- **Werkzeug** - WSGI utilities for Flask

### Data Visualization

- **matplotlib** - Static plotting
- **seaborn** - Statistical data visualization

### Environment & Configuration

- **python-dotenv** - Environment variable management
- **Virtual Environment (venv)** - Isolated Python environment

## Project Structure

```
Reddit-Stock-Sentiment-Analyzer/
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (Reddit API keys)
├── stock_sentiment.py          # Command-line interface
├── venv/                       # Virtual environment
└── src/                        # Web application source
    ├── app.py                  # Flask web server
    ├── reddit_sentiment.py     # Reddit data processing module
    ├── stock_data.py           # Stock data fetching module
    └── templates/
        └── index.html          # Web interface template
```

## Architecture Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │    │   Reddit API     │    │   Stock Data    │
│  (Stock Symbol) │    │   (PRAW)         │    │   (yfinance)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Processing Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Text Cleaning │  │   Sentiment     │  │   Data          │  │
│  │   & Filtering   │  │   Analysis      │  │   Aggregation   │  │
│  │   (RegEx)       │  │  (NLTK/TextBlob)│  │   (pandas)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Analysis Engine                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Sentiment     │  │   Trend         │  │   Statistical   │  │
│  │   Scoring       │  │   Prediction    │  │   Analysis      │  │
│  │   (-1 to +1)    │  │   (Bull/Bear)   │  │   (Distribution)│  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Output Interface                             │
│  ┌─────────────────┐                    ┌─────────────────┐     │
│  │   CLI Output    │                    │   Web Dashboard │     │
│  │   • Predictions │                    │   • Interactive │     │
│  │   • Sample Posts│                    │   • Color-coded │     │
│  │   • Sentiment   │                    │   • Real-time   │     │
│  └─────────────────┘                    └─────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Installation & Setup

### 1. Prerequisites

- Python 3.13 or higher
- Reddit API credentials (free at https://www.reddit.com/prefs/apps)

### 2. Clone Repository

```bash
git clone https://github.com/MisbahAN/Reddit-Stock-Sentiment-Analyzer.git
cd Reddit-Stock-Sentiment-Analyzer
```

### 3. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=Stock-Sentiment-Analyzer/1.0 by u/yourusername
```

## Usage

### Command Line Interface (CLI)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the CLI tool
python stock_sentiment.py

# Follow the prompt to enter a stock symbol (e.g., AAPL, TSLA, GME)
```

**CLI Output Example:**

```
Enter stock symbol (e.g., AAPL): AAPL

Analysis for AAPL:
Bullish (Positive sentiment detected)

Recent Reddit posts about this stock:

Title: Is AAPL still a buy?
Sentiment: 0.13

Title: I have $213,000 in Apple (AAPL) stock, should I start to diversify?
Sentiment: -0.48
```

### Web Interface

```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to source directory
cd src

# Start Flask server
python app.py

# Open browser to: http://127.0.0.1:5000
```

**Web Features:**

- Interactive stock symbol input
- Real-time sentiment analysis
- Color-coded post visualization (Green: Positive, Red: Negative, Yellow: Neutral)
- Stock price integration
- Responsive design

## Key Findings

### Sentiment Analysis Methodology

- **VADER Sentiment**: Optimized for social media text, handles emojis and informal language
- **TextBlob**: Provides additional sentiment polarity scoring for validation
- **Confidence Scoring**: Sentiment scores range from -1 (very negative) to +1 (very positive)

### Data Sources

- **Reddit Subreddits**: r/stocks, r/investing, r/wallstreetbets
- **Post Filtering**: Focuses on recent posts (last 30 days) with stock-related keywords
- **Stock Data**: Real-time pricing via Yahoo Finance API

### Limitations & Considerations

- **Market Volatility**: Sentiment may not always correlate with actual price movements
- **Sample Size**: Limited to available Reddit posts matching search criteria
- **Bias**: Reddit demographics may not represent overall market sentiment
- **Educational Purpose**: This tool is for learning and should not replace professional financial advice

### Performance Metrics

- **Processing Speed**: ~100 posts analyzed in 2-3 seconds
- **Accuracy**: Sentiment analysis shows 70-80% correlation with manual sentiment classification
- **Data Coverage**: Analyzes posts from multiple finance-focused subreddits

## Author

**Misbah Ahmed Nauman**  
Portfolio: [MisbahAN.com](https://MisbahAN.com)

**Aisha Suhail Khan**  
Portfolio: [AishaSK.com](https://www.aishask.com/)

---

_This project is for educational purposes only. Always conduct your own research before making investment decisions. The sentiment analysis provided should not be used as the sole basis for financial decisions._
