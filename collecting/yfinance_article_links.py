from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_yahoo_finance_news(ticker, driver_path):
    """
    Scrape dynamically loaded news articles for a given ticker from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'RKLB')
        driver_path (str): Path to the WebDriver executable
    
    Returns:
        list: List of dictionaries containing news article data
    """
    # Correct WebDriver initialization
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(f"https://finance.yahoo.com/quote/{ticker}/news/")
    wait = WebDriverWait(driver, 10)

    # Scroll and load content
    news_data = []
    scroll_pause_time = 5  # Seconds to wait for new content to load
    last_height = driver.execute_script("return document.body.scrollHeight")

    try:
        while True:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

            # Wait for new articles to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Parse loaded content with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.find_all("li", class_="stream-item story-item yf-1usaaz9")
        print(f"Found {len(articles)} articles.")

        for article in articles:
            try:
                # Extract the article link
                link_element = article.find("a", class_="subtle-link")
                if not link_element:
                    continue

                link = link_element['href']
                if link and not link.startswith('http'):
                    link = f"https://finance.yahoo.com{link}"


                # Extract source and time
                publishing_div = article.find("div", class_="publishing")
                if publishing_div:
                    source_time = publishing_div.get_text(strip=True).split("•")
                    source = source_time[0].strip()
                    time_ago = source_time[1].strip() if len(source_time) > 1 else "Unknown"
                else:
                    source = "Unknown"
                    time_ago = "Unknown"

                # Extract stock symbol and change
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
                    "Link": link,
                    "Source": source,
                    "Published": time_ago,
                    "Stock_Symbol": stock_info.get("symbol", ""),
                    "Stock_Change": stock_info.get("percent_change", "")
                })

            except Exception as e:
                print(f"Error processing article: {e}")
                continue

    finally:
        driver.quit()

    return news_data

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
    driver_path = "chromedriver"  # Update with the actual path to your WebDriver
    news_data = scrape_yahoo_finance_news(ticker, driver_path)
    save_to_csv(news_data, ticker)

if __name__ == "__main__":
    main()
