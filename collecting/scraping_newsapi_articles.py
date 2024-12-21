import requests
import pandas as pd
import time
from random import randint
import csv
from bs4 import BeautifulSoup

# Define the headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Define the URL to the CSV file
input_csv_path = 'data/raw_data/newsapi_data/rklb_newsapi_articles.csv'
output_csv_path = 'data/raw_data/newsapi_data/rklb_newsapi_articles_scraped.csv'

def scrape_article(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx, 5xx)
        
        # Check for specific response codes
        if response.status_code == 403:
            print(f"403 Forbidden for {url}, skipping.")
            return None
        if response.status_code == 404:
            print(f"404 Not Found for {url}, skipping.")
            return None
        if response.status_code == 429:
            print(f"429 Too Many Requests for {url}, waiting to retry.")
            time.sleep(randint(5, 15))  # Random delay to avoid detection
            return scrape_article(url)  # Retry after delay
        if response.status_code == 503:
            print(f"503 Service Unavailable for {url}, retrying.")
            time.sleep(randint(10, 20))  # Longer delay for server issues
            return scrape_article(url)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title = soup.title.string if soup.title else 'No title found'

        # Extract the article content (this may need to be customized for different sites)
        content = ''
        article = soup.find('div', {'class': 'article-content'})  # This is just an example, adjust for the site
        if article:
            content = article.get_text(strip=True)
        if not content:
            content = soup.get_text(strip=True)  # Fallback if no article div is found

        # Extract engagement data (if available, like comments or shares)
        engagement = ''
        engagement_data = soup.find('div', {'class': 'engagement'})  # Customize based on website structure
        if engagement_data:
            engagement = engagement_data.get_text(strip=True)
        
        return title, content, engagement
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

# Read URLs, scrape articles, save results
def main():
    # Read the CSV file containing article links
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"CSV file {input_csv_path} not found.")
        return
    
    # Prepare list to store the scraped content
    scraped_data = []

    # Loop over each URL and scrape it
    for index, row in df.iterrows():
        url = row['url']  # Adjust if the column name is different in your CSV
        print(f"Scraping {url}...")
        result = scrape_article(url)
        
        if result:
            title, content, engagement = result
            scraped_data.append({'url': url, 'title': title, 'content': content, 'engagement': engagement})
        else:
            scraped_data.append({'url': url, 'title': 'Error scraping title', 'content': 'Error scraping content', 'engagement': 'N/A'})

        # Delay between requests to avoid overwhelming the server
        time.sleep(randint(1, 5))  # Random delay between 1 to 5 seconds

    # Save the results to a new CSV file
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'title', 'content', 'engagement']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
        
        print(f"Scraped data saved to {output_csv_path}")
    
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == '__main__':
    main()
