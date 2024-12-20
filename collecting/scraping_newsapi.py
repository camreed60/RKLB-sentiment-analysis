import requests
import pandas as pd
from datetime import datetime

# API Details (Delete before publishing)
API_KEY = "eecdfdfa23a8427b91a157a0edc779c8"
BASE_URL = "https://newsapi.org/v2/everything"

params = {
    "q": "Rocket Lab", # Search query
    "from": "2024-11-20", # Start date
    "to": "2024-12-19", # end date
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

# Save to csv 
df = pd.DataFrame(articles)
df.to_csv("rklb_newsapi_articles.csv", index=False)

print(f"Collected {len(articles)} articles")