import pandas as pd
import re
import os

# Define the relative file paths based on the root directory
input_file_path = os.path.join('data', 'raw_data', 'newsapi_data', 'rklb_newsapi_articles_scraped.csv')
output_file_path = os.path.join('data', 'clean_data', 'news_api_data', 'cleaned_rklb_newsapi_articles.csv')

# Define a function to check and create directories if they don't exist
def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        print(f"Directory does not exist. Creating: {directory}")
        os.makedirs(directory, exist_ok=True)

# Debugging: Check if input file exists
if not os.path.exists(input_file_path):
    print(f"Input file does not exist: {input_file_path}")
else:
    print(f"Input file found: {input_file_path}")

# Load the data if the file exists
if os.path.exists(input_file_path):
    df = pd.read_csv(input_file_path)

    # Function to clean text content
    def clean_text(text):
        if isinstance(text, str):
            # Remove URLs
            text = re.sub(r'http\S+', '', text)

            # Remove special characters, punctuation, and extra spaces
            text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
            text = re.sub(r'\s+', ' ', text)     # Replace multiple spaces with a single space

            # Remove numbers if they are not relevant
            text = re.sub(r'\d+', '', text)  # Remove digits

            # Convert to lowercase
            text = text.lower()

            # Strip leading and trailing spaces
            text = text.strip()

            # Remove short, irrelevant text (e.g., "None", "Not Available")
            if len(text) < 5 or text in ["none", "not available", "n/a"]:
                return ''
            return text
        return ''

    # Clean the content and title columns
    df['cleaned_content'] = df['content'].apply(clean_text)
    df['cleaned_title'] = df['title'].apply(clean_text)

    # Clean the engagement if it exists (if the column is numeric, we'll keep it)
    df['cleaned_engagement'] = df['engagement'].apply(lambda x: x if isinstance(x, (int, float)) else None)

    # Ensure the output directory exists
    ensure_directory_exists(output_file_path)

    # Save the cleaned data to a new CSV file
    df.to_csv(output_file_path, index=False)

    print(f"Data cleaned and saved to {output_file_path}")
else:
    print("Exiting due to missing input file.")
