"""
Script is intended for preparing text data for sentiment analysis
using VADAR (Valence Aware Dictionary for Sentiment Reasoning)
"""

import pandas as pd
import re

# Path to CSV file to read
df = pd.read_csv('data/raw_data/twitter_data/rklb_raw_tweets_v2.csv')

# Selecting and accessing the specific column as a Series
col_name = 'text'
col_series = df[col_name]

# List to store cleaned tweets
cleaned_tweets = []

# Iterating through the Series
for text in col_series:
    new_text = str(text) # casting just to assert text is a string for regex use
    
    # Handle any excessive characters
    new_text = re.sub(r'(.)\1{2,}', r'\1\1', new_text)  # Convert "soooo" to "soo"
    
    # Remove tagged people
    new_text = re.sub(r'@[A-Za-z0-9_]+', '', new_text)
    
    # Remove URLs
    new_text = re.sub(r'http\S+|www\S+|https\S+', '', new_text, flags=re.MULTILINE)
    
    # Remove extra spaces
    new_text = re.sub(r'\s+', ' ', new_text).strip()
    
    # Add cleaned tweet to the list
    cleaned_tweets.append(new_text)


# Assert that no duplicates are contained
unique_cleaned_tweets = list(set(cleaned_tweets))

# Save to a new csv
cleaned_df = pd.DataFrame(unique_cleaned_tweets, columns=['cleaned_text'])
cleaned_df.to_csv('rklb_cleaned_tweets.csv', index=False)