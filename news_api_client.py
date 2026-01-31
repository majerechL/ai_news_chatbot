import os
from dotenv import load_dotenv
import requests
import logging

class NewsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/V2/"

    def fetch_news(self, topic, page_size=5):
        url, params = self.build_requests(topic, page_size)
        
        try:
            response = self.make_api_call(url, params)
            articles = response.get("articles")
            return self.format_articles(articles)
        
        except requests.RequestException as e:
            logging.error(f"Error fetching news articles: {e}")
            raise

    def build_requests(self, topic, page_size):
        url = f"{self.base_url}everything"
        params = {"q": topic, "apiKey": self.api_key, "pageSize": page_size}
        return url, params
    
    def make_api_call(self, url, params):
        response = requests.get(url, params)
        response.raise_for_status()
        return response.json()
    
    def format_articles(self, articles):
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
        return final_news
    
if __name__ == "__main__":
    load_dotenv()
    news_key = os.getenv('NEWS_API_KEY')

    news_client = NewsAPIClient(news_key)
    topic = "AI"
    formatted_articles = news_client.fetch_news(topic)

    for article in formatted_articles:
        print(article["title"], "-",article["description"])