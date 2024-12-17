import praw
import pandas as pd
import os

# Authenticate to Reddit
def authenticate_reddit():
    reddit = praw.Reddit(
        client_id = "fQDkZ8adjzphnERTn1Fb3g", # Delete before upload
        client_secret = "kp6jmowegNpxgfiqUNcSiJIGc51DHQ", # Delete before upload
        user_agent = "sentiment_analysis:v1.0 (by /u/Electrical_Mine_7039)" # Delete before upload
    )

# Fetch posts from WallStreetBets and RKLB
def fetch_reddit_data(reddit, subreddit_name, limit=100, filename="reddit_data.csv"):
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    # Fetch 'hot' posts
    for post in subreddit.hot(limit=limit):
        posts_data.append({
            'title': post.title,
            'selftext': post.selftext,
            'score': post.score,
            'num_comments': post.num_comments,
            'url': post.url
        })

    # Create a data frame
    df = pd.DataFrame(posts_data)

     # Get the current directory of the script (in the "collecting" folder)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path to the "data/raw_data/reddit_data" folder
    data_directory = os.path.join(current_directory, "..", "data", "raw_data", "reddit_data")
    
    # Ensure the directory exists
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)  # Create the directory if it doesn't exist
    
    # Save the DataFrame to a CSV file in the specified directory
    file_path = os.path.join(data_directory, filename)
    df.to_csv(file_path, index=False)
    print(f"Data from {subreddit_name} saved to {file_path}")

# Main function to collect and save data
if __name__ == "__main__":
    # Authenticate to Reddit
    reddit = authenticate_reddit()

    # List of subreddits we are concerned about
    subreddits = ["WallStreetBets", "RKLB"]

    # Collect data from each subreddit and save to csv
    for subreddit in subreddits:
        print(f"Collecting data from {subreddit}...")
        fetch_reddit_data(reddit, subreddit, filename=f"{subreddit}_posts.csv")
        print(f"Finished collecting data from {subreddit}")