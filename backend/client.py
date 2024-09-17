import requests
def make_post_request():
    url = 'http://localhost:5000/generate_leads'
    data = {
        "keyword": "software engineering job market",
        "name": "Headstarter",
        "description": "10x your software engineering skills with Headstarter! We help you get into top tech companies.",
        "location": "",
        "website_link": "https://headstarter.co"
    }
    response = requests.post(url, json=data)

    print(response.json())

make_post_request()