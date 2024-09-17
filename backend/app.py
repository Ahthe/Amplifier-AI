from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import praw
import openai
import tweepy
import json
import logging
import random
import time
import requests

from templates import generate_reddit_reply
from datetime import datetime

load_dotenv()


logging.basicConfig(filename='app.log', level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Reddit API credentials (loaded from the .env file)
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
# client = openai.Client()

# Twitter API credentials
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

# Social Searcher API key
SOCIAL_SEARCHER_API_KEY = os.getenv('SOCIAL_SEARCHER_API_KEY')

# Create Reddit API client (PRAW) - way to interact with Reddit API
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT,
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD)

# Create Twitter API client
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)



@app.route('/generate_leads', methods=['POST'])
def generate_leads():
    data = request.json
    keyword = data.get('keyword')
    business_name = data.get('name')
    business_description = data.get('description')
    location = data.get('location')
    website_link = data.get('website_link')
       
    # Generate leads from Reddit
    # reddit_leads = fetch_reddit_leads(keyword, location, business_name, business_description, website_link)

    # Generate leads from Twitter using Social Searcher
    twitter_leads = fetch_twitter_leads(keyword) # Can't leave actual Twitter API keys in the code, so we'll use Social Searcher for now so we don't need other parameters like location, business_name, etc.

    # Generate leads from LinkedIn using Social Searcher
    linkedin_leads = fetch_linkedin_leads(keyword)
    
    # Prepare the data to save
    result = {
        "question": keyword,
        "twitter_leads": twitter_leads,
        "linkedin_leads": linkedin_leads
    }

    # Save the result to a JSON file
    with open('leads_data.json', 'w') as f:
        json.dump(result, f, indent=4)
    
    return jsonify(result)

def fetch_reddit_leads(keyword, location, business_name, business_description, website_link):
    logging.info(f"Searching for keyword: {keyword}")
    # TODO: if already posted on specific post, don't post again. How can we keep track of this? For example if a user uses it one day and then again the next day, we don't want to post on the same post again.
    if location:
        logging.info(f"Location provided: {location}")
        keyword = f"{keyword} {location}"

    subreddit = reddit.subreddit("all")
    posts = {}
    
    # Load previously posted post IDs from a file to avoid duplicate posts
    try:
        with open('all_posts.json', 'r') as f:
            all_posts = json.load(f)
    except Exception as e:
        all_posts = {}

    # Set a limit for the number of new posts to comment on
    max_new_posts = 5
    new_posts_found = 0


    # Search through posts, but only comment on new ones
    for post in subreddit.search(keyword, limit=20):  # Increase the limit to search more posts
        logging.info(f"Processing post: {post.title}")

        # Skip if we've already posted in this exact post
        if post.id in all_posts:
            logging.info(f"Already processed this post: {post.title}, skipping...")
            continue  # Skip to the next post so we don't waste AI credits

        if post.archived:
            logging.info(f"Post is archived: {post.title}, skipping...")
            continue

        # Create the comment  
            
        comment = generate_reddit_reply(post, business_name, business_description, website_link)

        # Add the post ID to the list of all posts (before the try block)
        logging.info(f"Comment generated: {comment}") # Log the comment that was generated

        try:
            # Post the comment
            posted_comment = post.reply(comment)
            logging.info(f"Comment posted successfully on post: {post.title}")
            logging.info(f"Comment ID: {posted_comment.id}")
            logging.info(f"Comment URL: https://www.reddit.com{posted_comment.permalink}")

            # Increment the count of new posts found
            new_posts_found += 1

            # If we've found enough new posts, stop searching
            if new_posts_found >= max_new_posts:
                logging.info(f"Found {new_posts_found} new posts, stopping search.")
                break
            all_posts[post.id] = {
                'id': post.id,
                'description': post.title,
                'url': post.url,
                'timestamp': datetime.now().isoformat(),
                'comment': comment,
                "comment_url": f"https://www.reddit.com{posted_comment.permalink}"
            }
        except Exception as e:
            logging.error(f"Error posting comment on post: {post.title}")
            logging.error(f"Error COULD NOT POST ON THIS URL: {post.url}")
            logging.error(f"Error message: {str(e)}")

        

        # Save the updated list of posted post IDs to a file TODO: Improve this to not write the posts that haven't been replied too because of rate limits... We might just have to do not automatic posts and just show the user the posts and let them decide which ones to post on.
    with open('all_posts.json', 'w') as f: # by opening a file we overwrite the previous content
        json.dump(all_posts, f, indent=4) # add the list of posted posts to the file

        # Add a random delay between 30 and 60 seconds to avoid spam detection
        # delay = random.randint(5, 10)
        # logging.info(f"Waiting for {delay} seconds before posting the next comment...")
        # time.sleep(delay)
    
    return posts

def fetch_twitter_leads(keyword):
    logging.info(f"Fetching Twitter leads for keyword: {keyword}")
    
    # Social Searcher API endpoint for requesting data
    api_url_request = "https://api.social-searcher.com/v2/search"
    
    # Parameters for the initial API request (Step 1)
    params_request = {
        'key': SOCIAL_SEARCHER_API_KEY,
        'q': keyword,
        'network': 'twitter',  # Specify the network as 'twitter'
        'limit': 10  # Limit the number of results to 10
    }
    
    try:
        # Step 1: Make the initial request to collect data
        logging.info(f"Requesting data for keyword: {keyword}")
        response = requests.get(api_url_request, params=params_request)
        response.raise_for_status()
        
        data = response.json()
        requestid = data['meta'].get('requestid')
        
        if not requestid:
            logging.error("No requestid found in the response.")
            logging.error(f"Response content: {data}")
            return []
        
        logging.info(f"Received requestid: {requestid}")
        
        # Step 2: Wait before fetching the results
        wait_time = 60  # As per documentation, wait for 20-60 seconds
        logging.info(f"Waiting for {wait_time} seconds before fetching the results...")
        time.sleep(wait_time)
        
        # Social Searcher API endpoint for fetching results
        api_url_fetch = "https://api.social-searcher.com/v2/search"
        
        # Parameters for fetching the results
        params_fetch = {
            'key': SOCIAL_SEARCHER_API_KEY,
            'requestid': requestid,
            'page': 0,
            'limit': 10
        }
        
        # Retry logic in case the status is pending
        max_retries = 3
        retry_delay = 300  # Wait 5 minutes between retries
        
        for attempt in range(max_retries):
            logging.info(f"Fetching results for requestid: {requestid} (Attempt {attempt + 1})")
            response = requests.get(api_url_fetch, params=params_fetch)
            response.raise_for_status()
            
            data = response.json()
            status = data['meta'].get('status')
            
            if status == 'finished':
                logging.info("Data processing finished, extracting tweets...")
                tweets = []
                
                # Extract relevant tweet data
                for post in data.get('posts', []):
                    tweet_text = post.get('text', '')
                    tweet_user = post.get('user', {})
                    tweet_username = tweet_user.get('name', '')
                    tweet_user_id = tweet_user.get('id', '')
                    tweet_url = post.get('url', '')
                    post_timestamp = post.get('posted', '')

                    # Log the tweet data for debugging
                    logging.info(f"Tweet Text: {tweet_text}")
                    logging.info(f"Tweet User: {tweet_username}")
                    logging.info(f"Tweet URL: {tweet_url}")
                    logging.info(f"Tweet Posted At: {post_timestamp}")

                    tweet_data = {
                        'text': tweet_text,
                        'user': tweet_username,
                        'user_id': tweet_user_id,
                        'url': tweet_url,
                        'posted': post_timestamp
                    }
                    tweets.append(tweet_data)
                
                return tweets
            
            elif status == 'pending' or status == 'created':
                logging.info(f"Status is {status}, waiting for {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
            else:
                logging.error(f"Unexpected status: {status}")
                break
        
        logging.error("Max retries reached or unexpected status encountered.")
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response content: {response.text}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error fetching Twitter leads: {req_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    
    return []

def fetch_linkedin_leads(keyword):
    logging.info(f"Fetching LinkedIn leads for keyword: {keyword}")
    
    # Social Searcher API endpoint for requesting data
    api_url_request = "https://api.social-searcher.com/v2/search"
    
    # Parameters for the initial API request (Step 1)
    params_request = {
        'key': SOCIAL_SEARCHER_API_KEY,
        'q': keyword,
        'network': 'linkedin',  # Specify the network as 'linkedin'
        'limit': 10  # Limit the number of results to 10
    }
    
    try:
        # Step 1: Make the initial request to collect data
        logging.info(f"Requesting data for keyword: {keyword}")
        response = requests.get(api_url_request, params=params_request)
        response.raise_for_status()
        
        data = response.json()
        requestid = data['meta'].get('requestid')
        
        if not requestid:
            logging.error("No requestid found in the response.")
            logging.error(f"Response content: {data}")
            return []
        
        logging.info(f"Received requestid: {requestid}")
        
        # Step 2: Wait before fetching the results
        wait_time = 60  # As per documentation, wait for 20-60 seconds
        logging.info(f"Waiting for {wait_time} seconds before fetching the results...")
        time.sleep(wait_time)
        
        # Social Searcher API endpoint for fetching results
        api_url_fetch = "https://api.social-searcher.com/v2/search"
        
        # Parameters for fetching the results
        params_fetch = {
            'key': SOCIAL_SEARCHER_API_KEY,
            'requestid': requestid,
            'page': 0,
            'limit': 10
        }
        
        # Retry logic in case the status is pending
        max_retries = 3
        retry_delay = 300  # Wait 5 minutes between retries
        
        for attempt in range(max_retries):
            logging.info(f"Fetching results for requestid: {requestid} (Attempt {attempt + 1})")
            response = requests.get(api_url_fetch, params=params_fetch)
            response.raise_for_status()
            
            data = response.json()
            status = data['meta'].get('status')
            
            if status == 'finished':
                logging.info("Data processing finished, extracting LinkedIn posts...")
                linkedin_posts = []
                
                # Extract relevant post data
                for post in data.get('posts', []):
                    post_text = post.get('text', '')
                    post_user = post.get('user', {})
                    post_username = post_user.get('name', '')
                    post_user_id = post_user.get('id', '')
                    post_url = post.get('url', '')
                    post_timestamp = post.get('posted', '')

                    # Log the post data for debugging
                    logging.info(f"Post Text: {post_text}")
                    logging.info(f"Post User: {post_username}")
                    logging.info(f"Post URL: {post_url}")
                    logging.info(f"Post Posted At: {post_timestamp}")

                    post_data = {
                        'text': post_text,
                        'user': post_username,
                        'user_id': post_user_id,
                        'url': post_url,
                        'posted': post_timestamp
                    }
                    linkedin_posts.append(post_data)
                
                return linkedin_posts
            
            elif status == 'pending' or status == 'created':
                logging.info(f"Status is {status}, waiting for {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
            else:
                logging.error(f"Unexpected status: {status}")
                break
        
        logging.error("Max retries reached or unexpected status encountered.")
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response content: {response.text}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error fetching LinkedIn leads: {req_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    
    return []

# def fetch_twitter_leads(keyword):
#     tweets = twitter_api.search(q=keyword, lang="en", count=5)
#     tweet_data = [{'text': tweet.text, 'user': tweet.user.screen_name} for tweet in tweets]
#     return tweet_data



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)