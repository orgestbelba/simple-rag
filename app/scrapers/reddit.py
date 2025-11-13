import requests
import time

class RedditScraper:
    """Scrapes Reddit discussions via pushshift (read-only, no auth)"""
    
    async def fetch(self, limit: int = 20):
        """Fetch Reddit posts from public subreddits"""
        articles = []
        
        subreddits = ["MachineLearning", "Python", "learnprogramming"]
        
        for subreddit in subreddits:
            try:
                # Using pushshift mirror API (no auth needed)
                url = f"https://api.pushshift.io/reddit/search/submission?subreddit={subreddit}&size=10&sort=desc"
                response = requests.get(url, timeout=10)
                
                if response.status_code != 200:
                    continue
                
                data = response.json()
                
                for post in data.get("data", [])[:5]:
                    articles.append({
                        "source": "reddit",
                        "title": post.get("title"),
                        "url": f"https://reddit.com{post.get('permalink', '')}",
                        "content": post.get("selftext", "")[:2000],
                        "author": post.get("author", "")
                    })
                
                time.sleep(0.5)
            
            except Exception as e:
                print(f"Error scraping {subreddit}: {e}")
                continue
        
        return articles