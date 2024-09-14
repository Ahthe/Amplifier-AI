from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import praw
import openai
import tweepy
import json
import logging

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
    reddit_leads = fetch_reddit_leads(keyword, location, business_name, business_description, website_link)
    
    # Prepare the data to save
    result = {
        "question": keyword,
        "leads": reddit_leads
    }

    # Save the result to a JSON file
    with open('leads_data.json', 'w') as f:
        json.dump(result, f, indent=4)
    
    return jsonify(reddit_leads)

def fetch_reddit_leads(keyword, location, business_name, business_description, website_link):
    logging.info(f"Searching for keyword: {keyword}")
    # TODO: if already posted on specific post, don't post again. How can we keep track of this? For example if a user uses it one day and then again the next day, we don't want to post on the same post again.
    if location:
        logging.info(f"Location provided: {location}")
        keyword = f"{keyword} {location}"

    subreddit = reddit.subreddit("all")
    posts = []
    
    for post in subreddit.search(keyword, limit=5): #TODO: Does this use the entire keyword with whitespaces and all or does it just use the first word? e.g. "web development" vs "webdevelopment". How does the Reddit API handle this?
        logging.info(f"Processing post: {post.title} - {post.selftext}")
        # Analyze the post using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes post titles and descriptions and generates relevant and valuable comments."},
                {"role": "user", "content": f"Analyze this post title and description and generate a relevant, helpful comment that provides genuine value to the user:\n\nTitle: {post.title}\n\nDescription: {post.selftext}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        generated_text = response.choices[0].message.content.strip()

        # Create the comment
        comment = f"{generated_text}\n\nWe are {business_name}. {business_description}. Please visit our website for more information: {website_link}"

        try:
            # Post the comment
            posted_comment = post.reply(comment)
            logging.info(f"Comment posted successfully on post: {post.title}")
            logging.info(f"Description: {post.selftext}")
            logging.info(f"Comment: {comment}")
            logging.info(f"Comment ID: {posted_comment.id}")
            logging.info(f"Comment URL: https://www.reddit.com{posted_comment.permalink}")
        except Exception as e:
            logging.error(f"Error posting comment on post: {post.title}")
            logging.error(f"Error message: {str(e)}")

        post_data = {
            'title': post.title,
            'url': post.url,
            'comment': comment
        }
        posts.append(post_data)

        # Add a random delay between 30 and 60 seconds to avoid spam detection
        delay = random.randint(5, 10)
        logging.info(f"Waiting for {delay} seconds before posting the next comment...")
        time.sleep(delay)
    
    return posts

def fetch_twitter_leads(keyword):
    tweets = twitter_api.search(q=keyword, lang="en", count=5)
    tweet_data = [{'text': tweet.text, 'user': tweet.user.screen_name} for tweet in tweets]
    return tweet_data

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)