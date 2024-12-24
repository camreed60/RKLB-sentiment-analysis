"""
Iterating through scraped links of yahoofinance articles, 
and scraping all text from these articles. Each articles text
is saved as a new entry. Delays are a must when making a request
to the same server multiple times otherwise prone to bad status codes
like 404 or 503.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Path to CSV file to read
df = pd.read_csv('data/raw_data/yfinance_data/RKLB_news_links.csv')

# Selecting and accessing Series with all article links
col_name = 'Link'
article_links = df[col_name]

# Lists to store raw text data and titles from articles
output_article_text = []
output_article_titles = []

# Constants
P_CLASS = "yf-1pe5jgt"
TITLE_CLASS = "cover-title yf-1at0uqp"
MAX_RETRIES = 3
DELAY = 2  # Delay in seconds between retries

# Counter for successful scrapes
success_counter = 0

# Headers for mimicking browser behavior
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for link in article_links:
    article_text = None
    article_title = None
    for attempt in range(MAX_RETRIES):
        try:
            # Ensuring we get status 200 for a link
            response = requests.get(link, headers=headers, timeout=10)
            response.raise_for_status()  # Raise error if not status 200

            # For parsing HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Finding all paragraph tags with the specified class
            paragraphs = soup.find_all('p', class_=P_CLASS)

            # Extract and join the text from all paragraphs in article
            article_text = ' '.join(p.get_text(strip=True) for p in paragraphs)

            # Finding the title using the specified class
            title_div = soup.find('div', class_=TITLE_CLASS)
            article_title = title_div.get_text(strip=True) if title_div else None

            # Increment success counter and exit retry loop
            success_counter += 1
            print(f"Success scraping: {link}")
            break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {link}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY * (attempt + 1))  # Exponential backoff delay

    # Append scraped text and title (or None if failed)
    output_article_text.append(article_text)
    output_article_titles.append(article_title)

# Save the scraped data to a new CSV
output_df = pd.DataFrame({
    "Link": article_links,
    "Title": output_article_titles,
    "Article_Text": output_article_text
})
output_df.to_csv('articles_with_titles.csv', index=False)

# Print the number of successful scrapes
print(f"Scraping complete. Total successful scrapes: {success_counter}/{len(article_links)}")
