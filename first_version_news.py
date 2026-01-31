import os
from dotenv import load_dotenv
import requests

load_dotenv()

news_key = os.getenv('NEWS_API_KEY')

topic = "Python"
url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_key}&pageSize=5"

response = requests.get(url)

data = response.json()
print(type(data))

articles = data["articles"]
final_news = []

for article in articles:
    new_article = {
        "title": article["title"],
        "author": article["author"] or "Unknown",
        "source name": article["source"]["name"],
        "description": article["description"],
        "content": article["content"],
        "url": article["url"]
    }
    final_news.append(new_article)

print(final_news)