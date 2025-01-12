from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import pandas as pd

# Load the dataset
df = pd.read_csv('data/clean_data/twitter_data/rklb_cleaned_tweets.csv')

# Extract columns
date_tweeted_col = df['Title']  # Date tweeted
sentence_col = df['Cleaned_Text']  # The cleaned tweet text

### VADER Sentiment Analysis ###
# Initialize VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Function to calculate sentiment using VADER
def vader_sentiment_score(sentence):
    sentiment_map = vader_analyzer.polarity_scores(sentence)
    return sentiment_map  # Returns a dictionary with sentiment scores

# Lists to store VADER sentiment data
vader_titles = []
vadar_entry_length = []
compound_scores = []
positive_scores = []
neutral_scores = []
negative_scores = []
vader_overall_rated = []

# Iterate through tweets and calculate VADER sentiment
for title, text in zip(date_tweeted_col, sentence_col):
    sentiment_data = vader_sentiment_score(text)
    vader_titles.append(title)
    vadar_entry_length.append(len(text))
    compound_scores.append(sentiment_data['compound'])
    positive_scores.append(sentiment_data['pos'])
    neutral_scores.append(sentiment_data['neu'])
    negative_scores.append(sentiment_data['neg'])

    # Determine overall sentiment rating
    if sentiment_data['compound'] >= 0.05:
        vader_overall_rated.append('Positive')
    elif sentiment_data['compound'] <= -0.05:
        vader_overall_rated.append('Negative')
    else:
        vader_overall_rated.append('Neutral')

# Create a new DataFrame for VADER results
vader_sentiment_df = pd.DataFrame({
    'Title': vader_titles,
    'Tweet_Length': vadar_entry_length,
    'Compound_Score': compound_scores,
    'Positive_Score': positive_scores,
    'Neutral_Score': neutral_scores,
    'Negative_Score': negative_scores,
    'Overall_Rated': vader_overall_rated
})

# Save VADER results to a CSV
vader_sentiment_df.to_csv('twitter_vader_sentiment.csv', index=False)
print('VADER sentiment analysis completed successfully.')

### FinBERT Sentiment Analysis ###
# Load FinBERT model and tokenizer
finbert = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
finbert_analyzer = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

# Function to calculate sentiment using FinBERT
def finbert_sentiment_score(sentence):
    result = finbert_analyzer(sentence)[0]  # Get the first result
    return result  # Returns a dictionary with label and score

# Lists to store FinBERT sentiment data
finbert_titles = []
finbert_tweet_length = []
finbert_overall_rated = []
finbert_scores = []

# Iterate through tweets and calculate FinBERT sentiment
for title, text in zip(date_tweeted_col, sentence_col):
    sentiment_data = finbert_sentiment_score(text)
    finbert_titles.append(title)
    finbert_tweet_length.append(len(text))
    finbert_overall_rated.append(sentiment_data['label'])  # Sentiment label
    finbert_scores.append(sentiment_data['score'])  # Confidence score

# Create a new DataFrame for FinBERT results
finbert_sentiment_df = pd.DataFrame({
    'Title': finbert_titles,
    'Tweet_Length': finbert_tweet_length,
    'Overall_Rated': finbert_overall_rated,
    'Confidence_Score': finbert_scores
})

# Save FinBERT results to a CSV
finbert_sentiment_df.to_csv('twitter_finbert_sentiment.csv', index=False)
print('FinBERT sentiment analysis completed successfully.')
