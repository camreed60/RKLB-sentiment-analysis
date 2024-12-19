import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_yahoo_finance_news(ticker):
    """
    Scrape news articles for a given ticker from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'RKLB')
    
    Returns:
        list: List of dictionaries containing news article data
    """

    url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        news_data = []

        time.sleep(100)
        
        # Find all news content divs
        articles = soup.find_all("div", class_="content yf-18q3fnf")
        print(f"Found {len(articles)} articles.")
        
        for article in articles:
            try:
                # Get the article link element
                link_element = article.find("a", class_="subtle-link")
                if not link_element:
                    continue
                
                # Extract title from h3
                title_element = link_element.find("h3", class_="clamp")
                title = title_element.get_text(strip=True) if title_element else "No title"
                
                # Extract description from p tag if it exists
                description_element = link_element.find("p", class_="clamp")
                description = description_element.get_text(strip=True) if description_element else ""
                
                # Extract link
                link = link_element.get('href', '')
                if link and not link.startswith('http'):
                    link = f"https://finance.yahoo.com{link}"
                
                # Extract source and publication time
                publishing_div = article.find("div", class_="publishing")
                if publishing_div:
                    # Split text on the bullet character
                    source_time = publishing_div.get_text(strip=True).split('•')
                    source = source_time[0].strip()
                    time_ago = source_time[1].strip() if len(source_time) > 1 else "Unknown"
                else:
                    source = "Unknown"
                    time_ago = "Unknown"
                
                # Extract stock info if available
                stock_info = {}
                ticker_container = article.find("a", class_="ticker")
                if ticker_container:
                    symbol_element = ticker_container.find("span", class_="symbol")
                    percent_change_element = ticker_container.find("fin-streamer", class_="percentChange")
                    
                    stock_info = {
                        "symbol": symbol_element.get_text(strip=True) if symbol_element else "",
                        "percent_change": percent_change_element.get_text(strip=True) if percent_change_element else ""
                    }
                
                news_data.append({
                    "Title": title,
                    "Description": description,
                    "Link": link,
                    "Source": source,
                    "Published": time_ago,
                    "Stock_Symbol": stock_info.get("symbol", ""),
                    "Stock_Change": stock_info.get("percent_change", "")
                })
                
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
                
        return news_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def save_to_csv(data, ticker):
    """
    Save the scraped news data to a CSV file.
    
    Args:
        data (list): List of dictionaries containing news article data
        ticker (str): Stock ticker symbol used in filename
    """
    if data:
        df = pd.DataFrame(data)
        filename = f"{ticker}_news.csv"
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"News data saved to {filename}")
        print("\nFirst few rows of scraped data:")
        print(df.head().to_string())
    else:
        print("No articles found to save.")

def main():
    ticker = "RKLB"
    news_data = scrape_yahoo_finance_news(ticker)
    save_to_csv(news_data, ticker)

if __name__ == "__main__":
    main()