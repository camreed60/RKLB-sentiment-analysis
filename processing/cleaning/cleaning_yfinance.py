import pandas as pd
import re
from transformers import AutoTokenizer

# Load the dataset
df = pd.read_csv('data/raw_data/yfinance_data/articles_with_titles.csv')

# Load FinBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

# Define the preprocessing function for FinBERT compatibility
def preprocess_text(text, max_tokens=512):
    if pd.isnull(text):
        return None  # Skip processing if the text is null
    
    # Convert text to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove special characters and punctuation (keep alphanumeric and spaces)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenize and truncate to max_tokens
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    
    # Decode back into a string
    truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)
    
    return truncated_text

# Preprocess Title and Article_Text columns
df['Cleaned_Title'] = df['Title'].apply(lambda x: preprocess_text(x, max_tokens=512))
df['Cleaned_Text'] = df['Article_Text'].apply(lambda x: preprocess_text(x, max_tokens=512))

# Remove rows where Cleaned_Title or Cleaned_Text is null
df = df.dropna(subset=['Cleaned_Title', 'Cleaned_Text'])

# Save the preprocessed data to a new CSV
df[['Cleaned_Title', 'Cleaned_Text']].to_csv('cleaned_yfinance_data.csv', index=False)

print(f"Preprocessing complete. Saved {len(df)} entries to 'cleaned_yfinance_data.csv'.")
