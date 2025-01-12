# compounding scored entries by the model finBERT.
# Scoring is weighed based off the length of an entry

import pandas as pd

paths = ['data/sentiment_scores/yfinance_finbert_sentiment.csv', 
         'data/sentiment_scores/twitter_finbert_sentiment.csv',
         'data/sentiment_scores/reddit_finbert_sentiment.csv',
         'data/sentiment_scores/newsapi_finbert_sentiment.csv']

