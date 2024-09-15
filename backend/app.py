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

    # # Generate leads from Twitter using Social Searcher
    twitter_leads = fetch_twitter_leads(keyword) # Can't leave actual Twitter API keys in the code, so we'll use Social Searcher for now so we don't need other parameters like location, business_name, etc.

    # # Generate leads from LinkedIn using Social Searcher
    # linkedin_leads = fetch_linkedin_leads(keyword)
    
    # Prepare the data to save
    result = {
        "question": keyword,
        "leads": twitter_leads,
    }

    # Save the result to a JSON file
    with open('leads_data.json', 'w') as f:
        json.dump(result, f, indent=4)
    
    return jsonify(twitter_leads)

def fetch_reddit_leads(keyword, location, business_name, business_description, website_link):
    logging.info(f"Searching for keyword: {keyword}")
    # TODO: if already posted on specific post, don't post again. How can we keep track of this? For example if a user uses it one day and then again the next day, we don't want to post on the same post again.
    if location:
        logging.info(f"Location provided: {location}")
        keyword = f"{keyword} {location}"

    subreddit = reddit.subreddit("all")
    posts = []
    
    # Load previously posted post IDs from a file to avoid duplicate posts
    try:
        with open('all_posts.json', 'r') as f:
            all_posts = json.load(f)
    except FileNotFoundError:
        all_posts = []

    # Set a limit for the number of new posts to comment on
    max_new_posts = 5
    new_posts_found = 0


    # Search through posts, but only comment on new ones
    for post in subreddit.search(keyword, limit=20):  # Increase the limit to search more posts
        logging.info(f"Processing post: {post.title}")

        # Skip if we've already posted in this exact post
        if post.id in all_posts:
            logging.info(f"Already processed this post: {post.title}, skipping...")
            continue # Skip to the next post so we don't waste ai credits

        # TODO: Test this out and see if it works with gpt-4o-mini and finds relevant posts
        # # Analyze the post using OpenAI GPT to check relevance
        # relevance_check = openai.ChatCompletion.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #     {"role": "system", "content": "You are a helpful assistant that determines if a post is relevant to a business. Respond with only 'yes' or 'no'."},
        #     {"role": "user", "content": f"Is this post relevant to a business that offers {business_description}? Post title: {post.title}, Post description: {truncated_description}"}
        #     ],
        #     max_tokens=10, # Limit the response to a single word
        #     temperature=0
        # )
        # relevance_response = relevance_check.choices[0].message.content.strip().lower()

        # # If the post is not relevant, skip it
        # if "no" in relevance_response:
        #     logging.info(f"Post is not relevant: {post.title}, skipping...")
        #     continue

        truncated_description = post.selftext[:5000]  # Limit description to 5000 characters because token limit is 16385 tokens for 3.5 at least TODO: check if this is the case for gpt-4o-mini
        # Generate a comment using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
            {"role": "system", "content": "You are a helpful reddit user that analyzes post titles and descriptions and generates relevant and valuable replies."},
            {"role": "user", "content": f"Analyze this post title and description and generate a genuine helpful reply that provides genuine value to the user. If it is appropriate and relevant to the post, subtly mention our business and very briefly tell them how it can help the user with their issue. Otherwise, just provide a helpful reply without promoting the business if it will come across as spammy.\n\nTitle: {post.title}\n\nDescription: {truncated_description}\n\nOur Business Name: {business_name}\n\nBusiness Description: {business_description}\n\nWebsite Link: {website_link}"}
            ],
            max_tokens=200,
            temperature=0.7
        )
        generated_text = response.choices[0].message.content.strip()

        # Create the comment
        comment = generated_text

        # Add the post ID to the list of all posts (before the try block)
        all_posts.append(post.id)

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

        except Exception as e:
            logging.error(f"Error posting comment on post: {post.title}")
            logging.error(f"Error message: {str(e)}")

        post_data = {
            'title': post.title,
            'url': post.url,
            'comment': comment
        }
        posts.append(post_data)

        # Save the updated list of posted post IDs to a file
        with open('all_posts.json', 'w') as f: # by opening a file we overwrite the previous content
            json.dump(all_posts, f, indent=4) # add the list of posted posts to the file

        # Add a random delay between 30 and 60 seconds to avoid spam detection
        # delay = random.randint(5, 10)
        # logging.info(f"Waiting for {delay} seconds before posting the next comment...")
        # time.sleep(delay)
    
    return posts

def fetch_twitter_leads(keyword):
    logging.info(f"Fetching Twitter leads for keyword: {keyword}")
    
    # Social Searcher API endpoint
    api_url = "https://api.social-searcher.com/v2/search"
    
    # Parameters for the API request
    params = {
        'key': SOCIAL_SEARCHER_API_KEY,
        'q': keyword,
        'network': 'twitter',  # Specify the network as 'twitter'
        'limit': 5  # Limit the number of results to 5
    }
    
    # Log the request URL for debugging
    logging.info(f"Request URL: {api_url}")
    logging.info(f"Request Parameters: {params}")
    
    try:
        # Make the GET request to the Social Searcher API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        data = response.json()
        tweets = []
        
        # Extract relevant tweet data
        for post in data.get('posts', []):
            tweet_text = post.get('text', '')
            tweet_user = post.get('user', {}).get('name', '')
            tweet_url = post.get('url', '')

            # Log the tweet data for debugging
            logging.info(f"Tweet Text: {tweet_text}")
            logging.info(f"Tweet User: {tweet_user}")
            logging.info(f"Tweet URL: {tweet_url}")

            # Simulate posting the comment (since we can't actually post without the Twitter API)
            tweet_data = {
                'text': tweet_text,
                'user': tweet_user,
                'url': tweet_url
            }
            tweets.append(tweet_data)
        
        return tweets
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error fetching Twitter leads: {req_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    
    return []

def fetch_linkedin_leads(keyword):
    logging.info(f"Fetching LinkedIn leads for keyword: {keyword}")
    
    # Social Searcher API endpoint
    api_url = "https://api.social-searcher.com/v2/search"
    
    # Parameters for the API request
    params = {
        'key': SOCIAL_SEARCHER_API_KEY,
        'q': keyword,
        'network': 'linkedin',  # Specify the network as 'linkedin'
        'limit': 5  # Limit the number of results to 5
    }
    
    try:
        # Make the GET request to the Social Searcher API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        data = response.json()
        linkedin_posts = []
        
        # Extract relevant LinkedIn post data
        for post in data.get('posts', []):
            post_text = post.get('text', '')
            post_user = post.get('user', {}).get('name', '')
            post_url = post.get('url', '')

            post_data = {
                'text': post_text,
                'user': post_user,
                'url': post_url
            }
            linkedin_posts.append(post_data)
        
        return linkedin_posts
    
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
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