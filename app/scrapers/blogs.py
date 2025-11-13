import requests
from bs4 import BeautifulSoup
import time

class DevtoScraper:
    """Scrapes dev.to articles (no auth needed, JSON API available)"""
    
    async def fetch(self, limit: int = 30):
        """Fetch dev.to articles (they have public JSON API)"""
        articles = []
        
        try:
            # Dev.to has a public API
            url = "https://dev.to/api/articles?tag=python&per_page=30"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data[:limit]:
                articles.append({
                    "source": "devto",
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("description", "")[:2000],
                    "author": item.get("user", {}).get("name", "")
                })
                time.sleep(0.2)
        
        except Exception as e:
            print(f"Error scraping dev.to: {e}")
        
        return articles