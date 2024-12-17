import praw
import pandas as pd
import os

# Authenticate to Reddit
def authenticate_reddit():
    try:
        reddit = praw.Reddit(
            client_id = "fQDkZ8adjzphnERTn1Fb3g", # Delete before upload
            client_secret = "kp6jmowegNpxgfiqUNcSiJIGc51DHQ", # Delete before upload
            user_agent = "sentiment_analysis:v1.0 (by /u/Electrical_Mine_7039)" # Delete before upload
        )

    # Test authentication by checking if the Reddit instance is valid
        print("Authentication successful") 
        return reddit
    except Exception as e:
        print("Error during Reddit authentication:", e)
        return None  # Return None if authentication fails

# Fetch posts from WallStreetBets and RKLB
def fetch_reddit_data(reddit, subreddit_name, limit=1000, filename="reddit_data.csv"):
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    # Keywords related to RKLB
    relevant_keywords = [
        'RKLB', 'Rocket Lab', 'rocketlab', 'rocket labs', 'rocketlabs', 'rklb', 
        'Rocket lab', 'Rocket labs', 'rocket lab usa', 'rocket lab space', 
        'Rocket Lab USA', 'rocket lab stock', 'rocket lab news', 'rocket lab launch', 
        'rocket lab shares', 'rocket lab updates', 'rocket lab earnings', 
        'rocket lab missions', 'Electron rocket', 'rocket lab Electron', 
        'Electron launch', 'Neutron rocket', 'rocket lab Neutron', 
        'rocket lab spacecraft', 'rocket lab satellites', 'rocket lab orbit', 
        'rocket lab booster', 'rocket lab reusability', 'RKLB stock', 'RKLB news', 
        'RKLB earnings', 'RKLB updates', 'RKLB share price', 'RKLB forecast', 
        'RKLB analysis', 'RKLB valuation', 'rocket lab investor', 'rocket lab financials', 
        'rocket lab NASDAQ', 'NASDAQ RKLB', 'rocket lab orbital launch', 
        'Rocket Lab space systems', 'Rocket Lab recovery', 'Rocket Lab Photon', 
        'Photon satellite', 'Rocket Lab technology', 'rocket lab space services',
        'rocket lab manufacturing', 'RKLB space', 'RKLB launch', 'RKLB mission', 
        'RKLB reusability', 'rocket lab propulsion', 'RKLB market', 'rocket lab future',
        'rocket lab partnerships', 'rocket lab success', 'rocket lab growth'
    ]


    # Define the sorting methods to be used
    sorting_methods = {
        "hot": subreddit.hot(limit=limit),
        "new": subreddit.new(limit=limit),
        "top": subreddit.top(limit=limit),
        "controversial": subreddit.controversial(limit=limit)
    }

    # Fetch posts from each sorting method
    for sorting_method, posts in sorting_methods.items():
        print(f"Fetching {sorting_method} posts from {subreddit_name}...")
        for post in posts:
            # Filter posts that contain relevant keywords in the title or selftext
            if any(keyword.lower() in post.title.lower() for keyword in relevant_keywords) or \
            any(keyword.lower() in post.selftext.lower() for keyword in relevant_keywords):
                posts_data.append({
                    'title': post.title,
                    'selftext': post.selftext,
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'url': post.url
                })
    
    # If no relevant posts were found
    if not posts_data:
        print(f"No relevant posts found in {subreddit_name}.")
        return None

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
    subreddits = ["WallStreetBets", "RKLB", "RocketLab", "stocks", "SpaceXMasterrace", "investing", "SpaceX", "SmallStreetBets"]

    # Collect data from each subreddit and save to csv
    for subreddit in subreddits:
        print(f"Collecting data from {subreddit}...")
        fetch_reddit_data(reddit, subreddit, filename=f"{subreddit}_posts.csv")
        print(f"Finished collecting data from {subreddit}")