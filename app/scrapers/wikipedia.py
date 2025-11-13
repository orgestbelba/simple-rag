import requests
from bs4 import BeautifulSoup
import time

class WikipediaScraper:
    """Scrapes random Wikipedia articles on AI, tech topics"""
    
    BASE_URL = "https://en.wikipedia.org/wiki"
    TOPICS = [
        "Artificial_intelligence",
        "Machine_learning", 
        "Deep_learning",
        "Neural_network",
        "Natural_language_processing",
        "Computer_vision",
        "Data_science",
        "Python_(programming_language)",
        "Internet",
        "Web_development"
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    async def fetch(self, limit: int = 20):
        """Fetch Wikipedia articles"""
        articles = []
        
        for topic in self.TOPICS[:limit]:
            try:
                url = f"{self.BASE_URL}/{topic}"
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Get title
                title_elem = soup.find("h1", class_="firstHeading")
                if not title_elem:
                    continue
                title = title_elem.text
                
                # Get content (first 2000 chars)
                content_elem = soup.find("div", id="mw-content-text")
                if not content_elem:
                    continue
                
                # Extract paragraphs
                paragraphs = content_elem.find_all("p")
                content = "\n".join([p.text for p in paragraphs[:5]])[:2000]
                
                if not content or len(content) < 100:
                    continue
                
                articles.append({
                    "source": "wikipedia",
                    "title": title,
                    "url": url,
                    "content": content,
                    "author": "Wikipedia"
                })
                
                time.sleep(0.5)  # Be polite to servers
                
            except Exception as e:
                print(f"Error scraping {topic}: {e}")
                continue
        
        return articles