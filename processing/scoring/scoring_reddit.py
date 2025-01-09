import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# Initialize VADER
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# Path to the cleaned Reddit data directory
reddit_data_dir = './data/clean_data/reddit_data'
output_file = './data/sentiment_scores/reddit_vader_sentiment.csv'

# Initialize a list to store sentiment scores
sentiment_data = []

# Process each subreddit CSV
for file_name in os.listdir(reddit_data_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(reddit_data_dir, file_name)
        # Read the subreddit CSV
        df = pd.read_csv(file_path)

        # Apply VADER 
        for _, row in df.iterrows():
            title = row['cleaned_title'] if pd.notnull(row['cleaned_title']) else ''
            selftext = row['cleaned_selftext'] if pd.notnull(row['cleaned_selftext']) else ''

            # Combine title and selftext for sentiment analysis
            text = f"{title} {selftext}"

            # Get sentiment scores
            sentiment = sid.polarity_scores(text)

            # Append results with additional metadata
            sentiment_data.append({
                'subreddit_file': file_name,
                'title': row['title'],
                'selftext': row['selftext'],
                'score': row['score'],
                'num_comments': row['num_comments'],
                'url': row['url'],
                'compound': sentiment['compound'],
                'positive': sentiment['pos'],
                'neutral': sentiment['neu'],
                'negative': sentiment['neg']
            })

# Save sentiment scores to a CSV
sentiment_df = pd.DataFrame(sentiment_data)
sentiment_df.to_csv(output_file, index=False)

print(f"Sentiment analysis completed. Results saved to {output_file}")
