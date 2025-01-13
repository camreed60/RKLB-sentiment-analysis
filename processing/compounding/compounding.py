import pandas as pd
import os

# File paths for VADER and FinBERT sentiment data
finbert_paths = [
    'data/sentiment_scores/yfinance_finbert_sentiment.csv',
    'data/sentiment_scores/twitter_finbert_sentiment.csv',
    'data/sentiment_scores/reddit_finbert_sentiment.csv',
    'data/sentiment_scores/newsapi_finbert_sentiment.csv'
]

vader_paths = [
    'data/sentiment_scores/yfinance_vader_sentiment.csv',
    'data/sentiment_scores/twitter_vader_sentiment.csv',
    'data/sentiment_scores/reddit_vader_sentiment.csv',
    'data/sentiment_scores/newsapi_vader_sentiment.csv'
]

# Sentiment columns for each model
vader_sentiment_columns = ['compound', 'positive', 'neutral', 'negative']
finbert_sentiment_columns = ['score']

# Function to load CSV file
def load_file(file_path):
    return pd.read_csv(file_path)

# Function to calculate weighted averages
def calculate_weighted_averages(df, sentiment_columns, weight_column='length'):
    weighted_results = {}
    for column in sentiment_columns:
        # Weighted average for each sentiment column
        weighted_results[column] = (df[column] * df[weight_column]).sum() / df[weight_column].sum()
    return weighted_results

# DataFrame to store all compounded VADER scores
vader_compounded_list = []

# Process VADER files
for path in vader_paths:
    if not os.path.exists(path):
        print(f"Path {path} does not exist.")
        continue

    # Extract media title from file name
    media_title = os.path.basename(path).replace('_vader_sentiment.csv', '').replace('_', ' ').title()

    # Load file and calculate compounded scores
    vader_df = load_file(path)
    vader_compounded = calculate_weighted_averages(vader_df, vader_sentiment_columns)
    vader_compounded = {'Media_Title': media_title, **vader_compounded}  # Add Media_Title as the first column

    # Append to the list
    vader_compounded_list.append(vader_compounded)

# Combine all VADER results into a single DataFrame
vader_compounded_df = pd.DataFrame(vader_compounded_list)
vader_output_path = 'data/sentiment_scores/compounded_vader_all.csv'
vader_compounded_df.to_csv(vader_output_path, index=False)
print(f"VADER compounded scores saved to {vader_output_path}")

# DataFrame to store all compounded FinBERT scores
finbert_compounded_list = []

# Process FinBERT files
for path in finbert_paths:
    if not os.path.exists(path):
        print(f"Path {path} does not exist.")
        continue

    # Extract media title from file name
    media_title = os.path.basename(path).replace('_finbert_sentiment.csv', '').replace('_', ' ').title()

    # Load file and calculate compounded scores
    finbert_df = load_file(path)
    finbert_compounded = calculate_weighted_averages(finbert_df, finbert_sentiment_columns)
    finbert_compounded = {'Media_Title': media_title, **finbert_compounded}  # Add Media_Title as the first column

    # Append to the list
    finbert_compounded_list.append(finbert_compounded)

# Combine all FinBERT results into a single DataFrame
finbert_compounded_df = pd.DataFrame(finbert_compounded_list)
finbert_output_path = 'data/sentiment_scores/compounded_finbert_all.csv'
finbert_compounded_df.to_csv(finbert_output_path, index=False)
print(f"FinBERT compounded scores saved to {finbert_output_path}")
