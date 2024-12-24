"""
Script is intended for preparing text data for sentiment analysis
using VADAR (Valence Aware Dictionary for Sentiment Reasoning)
"""

import pandas as pd
import re

# Path to CSV file to read
df = pd.read_csv('data/raw_data/twitter_data/rklb_raw_tweets_v2.csv')

# Selecting and accessing the specific columns as Series
col_text = 'text'
col_created_at = 'created_at'
tweets = df[col_text]
timestamps = df[col_created_at]

# Lists to store cleaned tweets and associated timestamps
cleaned_tweets = []
tweet_titles = []

# Iterating through the Series
for text, timestamp in zip(tweets, timestamps):
    new_text = str(text)  # Ensure text is a string for regex use
    
    # Handle any excessive characters
    new_text = re.sub(r'(.)\1{2,}', r'\1\1', new_text)  # Convert "soooo" to "soo"
    
    # Remove tagged people
    new_text = re.sub(r'@[A-Za-z0-9_]+', '', new_text)
    
    # Remove URLs
    new_text = re.sub(r'http\S+|www\S+|https\S+', '', new_text, flags=re.MULTILINE)
    
    # Remove extra spaces
    new_text = re.sub(r'\s+', ' ', new_text).strip()
    
    # Append the cleaned tweet and its creation timestamp to respective lists
    cleaned_tweets.append(new_text)
    tweet_titles.append(timestamp)  # Use `created_at` as the title

# Combine cleaned tweets and titles into a DataFrame
cleaned_df = pd.DataFrame({
    'Title': tweet_titles,  # Timestamp as the title
    'Cleaned_Text': cleaned_tweets
})

# Assert that no duplicates are contained
cleaned_df = cleaned_df.drop_duplicates(subset=['Cleaned_Text'])

# Save to a new CSV
cleaned_df.to_csv('rklb_cleaned_tweets.csv', index=False)

print(f"Successfully cleaned {len(cleaned_df)} tweets.")
