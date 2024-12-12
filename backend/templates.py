from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional
class SocialMediaResponse(BaseModel):
    """Structure for social media responses"""
    response_text: str = Field(..., description="The main response text")
    business_mention: Optional[str] = Field(None, description="How the business was mentioned")
    confidence_score: float = Field(..., description="How confident the model is about the response relevance (0-1)")

parser = PydanticOutputParser(pydantic_object=SocialMediaResponse)

def create_social_response_chain(model_name="gpt-4o-mini"):
    """Creates a reusable chain for social media responses"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model=model_name,
        temperature=0.7
    )
    
    # Use the global parser
    parser = globals()['parser']

    # Create a template that's more focused and structured
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful social media expert who provides valuable responses while naturally 
        incorporating business mentions naturally. Focus on:
        1. Authenticity and value-first approach
        2. Natural conversation flow
        3. Mentioning businesses in a natural non-intrusive way
        4. Maintaining appropriate platform tone (Reddit: casual, LinkedIn: professional, Twitter: concise)
        
        If the business mention feels forced, prioritize providing valuable information instead."""),
        ("human", """Context:
        Platform: {platform}
        Post: {post_text}
        
        Business Info:
        Name: {business_name}
        Description: {business_description}
        Website: {website_link}
        
        Generate a helpful response that prioritizes value while naturally mentioning the business smoothly and not like a promotional bot.
        {format_instructions}""")
    ])

    # Create the chain
    chain = (
        prompt 
        | llm 
        | parser
    )
    
    return chain

def generate_social_reply(
    platform: str,
    post_text: str,
    business_name: str,
    business_description: str,
    website_link: str
) -> str:
    """Generic social media response generator"""
    
    # Create the chain
    chain = create_social_response_chain()
    
    # Generate response
    response = chain.invoke({
        "platform": platform,
        "post_text": post_text,
        "business_name": business_name,
        "business_description": business_description,
        "website_link": website_link,
        "format_instructions": globals()['parser'].get_format_instructions()
    })
    
    # Only include business mention if confidence is high enough
    # if response.confidence_score < 0.7:
    #     return response.response_text
    
    return response.response_text

# Platform-specific functions now just call the generic function with different parameters
def generate_reddit_reply(post, business_name, business_description, website_link):
    return generate_social_reply(
        "reddit",
        f"{post.title}\n\n{post.selftext[:5000]}",
        business_name,
        business_description,
        website_link
    )

def generate_twitter_reply(tweet, business_name, business_description, website_link):
    return generate_social_reply(
        "twitter",
        tweet.get('text', ''),
        business_name,
        business_description,
        website_link
    )

def generate_linkedin_reply(post, business_name, business_description, website_link):
    return generate_social_reply(
        "linkedin",
        post.get('text', ''),
        business_name,
        business_description,
        website_link
    )
