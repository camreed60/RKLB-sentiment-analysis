import requests
import pandas as pd
from datetime import datetime
import os

# API Details (Delete before publishing)
API_KEY = "eecdfdfa23a8427b91a157a0edc779c8"
BASE_URL = "https://newsapi.org/v2/everything"

params = {
    "q": "Rocket Lab", # Search query
    "from": "2024-11-21", # Start date
    "to": "2024-12-20", # end date
    "language": "en", # language
    "sortBy": "relevancy", # Sorting param
    "pageSize": 100, # Max articles per page
    "apiKey": API_KEY
}

# Function to collect data
def fetch_articles(params):
    all_articles = []
    for page in range(1, 2):
        params["page"] = page
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Error: {response.json()}")  # Log the error
            return []  # Return an empty list to avoid TypeError
        data = response.json()
        articles = data.get("articles", [])
        all_articles.extend(articles)
        if len(articles) < params["pageSize"]:
            break  # No more articles to fetch
    return all_articles

    
articles = fetch_articles(params)

# Save to CSV in the correct directory
if articles:
    df = pd.DataFrame(articles)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(current_directory, "..", "data", "raw_data", "newsapi_data")
    os.makedirs(data_directory, exist_ok=True)
    file_path = os.path.join(data_directory, "rklb_newsapi_articles.csv")
    df.to_csv(file_path, index=False)
    print(f"Collected {len(articles)} articles and saved to {file_path}")
else:
    print("No articles were collected.")

# Saves as source, author, title, description, url, urlToImage, publishedAt, content