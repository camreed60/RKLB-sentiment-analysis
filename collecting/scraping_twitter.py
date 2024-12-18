import tweepy
import pandas as pd


bearer_token = "AAAAAAAAAAAAAAAAAAAAADFVxgEAAAAA%2BdXfiB6sZifsOJCR9fCr2%2F%2BBqao%3D1pCK48kWE7bgr8VB7VauMIAzP51nVgdaghuwjIrfZNvoyJ91GC"

# Initialize Twitter Client for v2 API
client = tweepy.Client(bearer_token=bearer_token)

# Function to fetch tweets using Twitter v2 API
def fetch_tweets_v2(query, max_results=50):
    # Fetch tweets based on a query using Twitter API v2.
    
    try:
        # Fetch recent tweets with necessary fields
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["id", "created_at", "text", "public_metrics", "lang"],
            user_fields=["username"],
            expansions=["author_id"]
        )
        
        # Check if data exists
        if not response.data:
            print("No tweets found.")
            return []

        # Extract relevant data from response
        tweets_data = []
        users = {u["id"]: u["username"] for u in response.includes.get("users", [])}

        for tweet in response.data:
            tweets_data.append({
                "id": tweet.id,
                "created_at": tweet.created_at,
                "text": tweet.text,
                "username": users.get(tweet.author_id, "unknown"),
                "likes": tweet.public_metrics.get("like_count", 0),
                "retweets": tweet.public_metrics.get("retweet_count", 0)
            })
        
        return tweets_data

    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        return []

# Fetch tweets for #RKLB using API v2
query = "#RKLB lang:en"  # Adding 'lang:en' to the query ensures English tweets
tweets_data = fetch_tweets_v2(query, max_results=50)

# Save the raw data to a clean CSV file
if tweets_data:
    df = pd.DataFrame(tweets_data)
    # Save with proper formatting
    df.to_csv(
        "rklb_raw_tweets_v2.csv",
        index=False,          # Don't include row numbers
        encoding="utf-8",     # Standard UTF-8 encoding
        quoting=1             # Quote all fields to handle special characters like commas
    )
    
    print("Tweets saved to rklb_raw_tweets_v2.csv")
else:
    print("No tweets fetched.")

