import os
import pandas as pd
import re

# Define specific directory
reddit_data_dir = '/home/cam/Desktop/personal-projects/RKLB-sentiment-analysis/data/raw_data/reddit_data'
clean_data_dir = '/home/cam/Desktop/personal-projects/RKLB-sentiment-analysis/data/clean_data/reddit_data'


def clean_text(text):
    try:
        if not isinstance(text, str) or text.strip() == '':
            return ''
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return ''


def clean_reddit_data(file_path, output_dir):
    try:
        # Load the data
        df = pd.read_csv(file_path)
        
        # Perform cleaning (update with actual cleaning logic)
        if 'title' in df.columns and 'selftext' in df.columns:
            df['cleaned_title'] = df['title'].apply(clean_text)
            df['cleaned_selftext'] = df['selftext'].apply(clean_text)

            # Save cleaned data
            output_file = os.path.join(output_dir, os.path.basename(file_path))
            df.to_csv(output_file, index=False)
            print(f"Saved cleaned data to {output_file}")
        else:
            print(f"Missing required columns in {file_path}. Skipping...")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process only files in reddit_data_dir
for file_name in os.listdir(reddit_data_dir):
    file_path = os.path.join(reddit_data_dir, file_name)
    if os.path.isfile(file_path):  # Ensure it's a file
        clean_reddit_data(file_path, clean_data_dir)
