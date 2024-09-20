import openai

def generate_reddit_reply(post, business_name, business_description, website_link):
    description = post.selftext[:5000]
    response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a thoughtful and insightful Reddit user who provides genuine and valuable responses to posts. Your goal is to assist users by offering advice, insights, or solutions. And naturally mention our business, {business_name}, in a way that adds value to the conversation. Include our link, {website_link}, if it fits naturally, explaining briefly how it might help with their issue. Avoid being overly promotional or spammy. Maintain a neutral and helpful tone throughout your response."
                },
                
                {
                    "role": "user",
                    "content": f"""
                        Please analyze the following Reddit post's title and description and craft a genuine and helpful reply that provides value to the user. 
                        Find a way to naturally recommend our business and talk as if you've personally used it and how it helped you, if it is relevant and can be seamlessly integrated into your response. 
                        If you can't mention the business naturally, focus solely on providing valuable advice. Focus on speaking in a neutral tone and avoid using exclaimation marks. 
                        Please try to find a way to personally RECOMMEND {business_name}, in the reply naturally and preferably mention the, as well.
                        when promiting the business ensure you have mentioned the name. if the website link is relevent then add that too.
                        Everything after this point is information for you to use in your response. reply only with the generated comment and nothing else. 
                        make the english simple and smooth and answer in under 
                        Title: {post.title}
                        Description: {description}
                        Our Business Name: {business_name}
                        Our Business Description: {business_description}
                        Our Website Link: {website_link}
                    """
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
    return response.choices[0].message.content.strip()

def generate_twitter_reply(tweet, business_name, business_description, website_link):
    tweet_text = tweet.get('text', '')
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a thoughtful and insightful Twitter user who provides genuine and valuable responses to tweets. Your goal is to assist users by offering advice, insights, or solutions. And naturally mention our business, {business_name}, in a way that adds value to the conversation. Include our link, {website_link}, if it fits naturally, explaining briefly how it might help with their issue. Avoid being overly promotional or spammy. Maintain a neutral and helpful tone throughout your response."
            },
            {
                "role": "user",
                "content": f"""
                    Please analyze the following tweet and craft a genuine and helpful reply that provides value to the user.
                    Find a way to naturally recommend our business and talk as if you've personally used it and how it helped you, if it is relevant and can be seamlessly integrated into your response.
                    If you can't mention the business naturally, focus solely on providing valuable advice. Focus on speaking in a neutral tone and avoid using exclamation marks.
                    Please try to find a way to personally RECOMMEND {business_name}, in the reply naturally and preferably mention the, as well.
                    when promoting the business ensure you have mentioned the name. if the website link is relevant then add that too.
                    Everything after this point is information for you to use in your response. reply only with the generated comment and nothing else.
                    make the english simple and smooth and answer in under 280 characters.
                    Tweet: {tweet_text}
                    Our Business Name: {business_name}
                    Our Business Description: {business_description}
                    Our Website Link: {website_link}
                """
            }
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generate_linkedin_reply(post, business_name, business_description, website_link):
    post_text = post.get('text', '')
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a thoughtful and insightful LinkedIn user who provides genuine and valuable responses to posts. Your goal is to assist users by offering advice, insights, or solutions. And naturally mention our business, {business_name}, in a way that adds value to the conversation. Include our link, {website_link}, if it fits naturally, explaining briefly how it might help with their issue. Avoid being overly promotional or spammy. Maintain a neutral and professional tone throughout your response."
            },
            {
                "role": "user",
                "content": f"""
                    Please analyze the following LinkedIn post and craft a genuine and helpful reply that provides value to the user.
                    Find a way to naturally recommend our business and talk as if you've personally used it and how it helped you, if it is relevant and can be seamlessly integrated into your response.
                    If you can't mention the business naturally, focus solely on providing valuable advice. Focus on speaking in a neutral tone and avoid using exclamation marks.
                    Please try to find a way to personally RECOMMEND {business_name}, in the reply naturally and preferably mention the, as well.
                    when promoting the business ensure you have mentioned the name. if the website link is relevant then add that too.
                    Everything after this point is information for you to use in your response. reply only with the generated comment and nothing else.
                    make the english simple and smooth and answer in under 500 characters.
                    Post: {post_text}
                    Our Business Name: {business_name}
                    Our Business Description: {business_description}
                    Our Website Link: {website_link}
                """
            }
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()