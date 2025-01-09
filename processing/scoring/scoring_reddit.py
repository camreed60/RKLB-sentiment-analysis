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
reddit_data_dir = './data/clean_data/reddit_data'
vader_output_file = './data/sentiment_scores/reddit_vader_sentiment.csv'
finbert_output_file = './data/sentiment_scores/reddit_finbert_sentiment.csv'

# Function to truncate text to fit within FinBERT's 512-token limit
def truncate_text(text, tokenizer, max_length=510):
    tokens = tokenizer.tokenize(text)
    if len(tokens) > max_length:
        # Truncate tokens and convert back to string
        truncated_tokens = tokens[:max_length]
        return tokenizer.convert_tokens_to_string(truncated_tokens)
    return text

# Process VADER and FinBERT Sentiment Analysis
vader_sentiment_data = []
finbert_sentiment_data = []

for file_name in os.listdir(reddit_data_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(reddit_data_dir, file_name)
        # Read the subreddit CSV
        df = pd.read_csv(file_path)

        # Apply sentiment analysis on each row
        for _, row in df.iterrows():
            # Use cleaned text directly and truncate if necessary
            text = f"{row['cleaned_title']} {row['cleaned_selftext']}".strip()
            truncated_text = truncate_text(text, finbert_tokenizer)

            # VADER sentiment analysis
            vader_scores = vader_analyzer.polarity_scores(text)
            vader_sentiment_data.append({
                'subreddit_file': file_name,
                'title': row['title'],
                'selftext': row['selftext'],
                'score': row['score'],
                'num_comments': row['num_comments'],
                'url': row['url'],
                'compound': vader_scores['compound'],
                'positive': vader_scores['pos'],
                'neutral': vader_scores['neu'],
                'negative': vader_scores['neg']
            })

            # FinBERT sentiment analysis
            finbert_result = finbert_analyzer(truncated_text)[0]
            finbert_sentiment_data.append({
                'subreddit_file': file_name,
                'title': row['title'],
                'selftext': row['selftext'],
                'score': row['score'],
                'num_comments': row['num_comments'],
                'url': row['url'],
                'label': finbert_result['label'],
                'score': finbert_result['score']
            })

# Save VADER sentiment scores
vader_df = pd.DataFrame(vader_sentiment_data)
vader_df.to_csv(vader_output_file, index=False)
print(f"VADER sentiment analysis completed. Results saved to {vader_output_file}")

# Save FinBERT sentiment scores
finbert_df = pd.DataFrame(finbert_sentiment_data)
finbert_df.to_csv(finbert_output_file, index=False)
print(f"FinBERT sentiment analysis completed. Results saved to {finbert_output_file}")
