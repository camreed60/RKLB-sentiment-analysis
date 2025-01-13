import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
import nltk

# Download VADER
nltk.download('vader_lexicon')

# Initialize VADER
vader_analyzer = SentimentIntensityAnalyzer()

# Load FinBERT model and tokenizer
finbert_model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
finbert_analyzer = pipeline("sentiment-analysis", model=finbert_model, tokenizer=finbert_tokenizer)

# Paths
newsapi_input_file = './data/clean_data/news_api_data/cleaned_rklb_newsapi_articles.csv'  # Input file
vader_output_file = './data/sentiment_scores/newsapi_vader_sentiment.csv'  # VADER output file
finbert_output_file = './data/sentiment_scores/newsapi_finbert_sentiment.csv'  # FinBERT output file

# Function to truncate text to fit within FinBERT's token limit
def truncate_text(text, tokenizer, max_content_tokens=510):
    tokens = tokenizer.tokenize(text)
    if len(tokens) > max_content_tokens:
        # Truncate tokens and convert back to string
        truncated_tokens = tokens[:max_content_tokens]
        return tokenizer.convert_tokens_to_string(truncated_tokens)
    return text

# Load NewsAPI data
newsapi_df = pd.read_csv(newsapi_input_file)

# Lists to store sentiment analysis results
vader_sentiment_data = []
finbert_sentiment_data = []

# Process each row in the NewsAPI data
for _, row in newsapi_df.iterrows():
    # Use cleaned content and title
    text = f"{row['cleaned_content']}".strip()
    article_length = len(text)

    # Skip rows with missing or empty cleaned text
    if not text or pd.isnull(text):
        continue

    # VADER sentiment analysis
    vader_scores = vader_analyzer.polarity_scores(text)
    vader_sentiment_data.append({
        'url': row['url'],
        'title': row['title'],
        'content': row['content'],
        'engagement': row['engagement'],
        'cleaned_title': row['cleaned_title'],
        'cleaned_content': row['cleaned_content'],
        'cleaned_engagement': row['cleaned_engagement'],
        'compound': vader_scores['compound'],
        'positive': vader_scores['pos'],
        'neutral': vader_scores['neu'],
        'negative': vader_scores['neg'],
        'article_length': article_length
    })

    # FinBERT sentiment analysis
    truncated_text = truncate_text(text, finbert_tokenizer)
    finbert_result = finbert_analyzer(truncated_text)[0]
    finbert_sentiment_data.append({
        'url': row['url'],
        'title': row['title'],
        'content': row['content'],
        'engagement': row['engagement'],
        'cleaned_title': row['cleaned_title'],
        'cleaned_content': row['cleaned_content'],
        'cleaned_engagement': row['cleaned_engagement'],
        'label': finbert_result['label'],
        'score': finbert_result['score'],
        'article_length': article_length
    })

# Save VADER sentiment scores
vader_df = pd.DataFrame(vader_sentiment_data)
vader_df.to_csv(vader_output_file, index=False)
print(f"VADER sentiment analysis completed. Results saved to {vader_output_file}")

# Save FinBERT sentiment scores
finbert_df = pd.DataFrame(finbert_sentiment_data)
finbert_df.to_csv(finbert_output_file, index=False)
print(f"FinBERT sentiment analysis completed. Results saved to {finbert_output_file}")
