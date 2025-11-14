import requests
import time

class RedditScraper:
    """Scrapes Reddit discussions via pushshift (read-only, no auth).
    Falls back to Reddit public JSON if pushshift returns 0 items.
    """

    def _ua_session(self):
        s = requests.Session()
        s.headers.update({
            "User-Agent": "SimpleRAG/1.0 (+https://example.com)"
        })
        return s

    async def fetch(self, limit: int = 20):
        """Fetch Reddit posts from public subreddits (no DB writes)."""
        articles = []
        subreddits = ["MachineLearning", "Python", "learnprogramming"]
        session = self._ua_session()

        # --- Primary path: Pushshift (per spec) ---
        for subreddit in subreddits:
            try:
                url = (
                    "https://api.pushshift.io/reddit/search/submission"
                    f"?subreddit={subreddit}&size=10&sort=desc"
                )
                resp = session.get(url, timeout=10)
                if resp.status_code != 200:
                    continue
                data = resp.json()

                for post in data.get("data", [])[:5]:
                    if len(articles) >= limit:
                        break
                    articles.append({
                        "source": "reddit",
                        "title": post.get("title"),
                        "url": f"https://reddit.com{post.get('permalink', '')}",
                        "content": (post.get("selftext") or "")[:2000],
                        "author": post.get("author", "")
                    })
                time.sleep(0.4)
            except Exception as e:
                print(f"Error scraping (pushshift) {subreddit}: {e}")
                continue

            if len(articles) >= limit:
                break

        # --- Fallback: Reddit public JSON (no auth) ---
        if len(articles) == 0:
            for subreddit in subreddits:
                try:
                    # e.g. https://www.reddit.com/r/Python/new.json?limit=10
                    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=10"
                    resp = session.get(url, timeout=10)
                    if resp.status_code != 200:
                        continue
                    data = resp.json()
                    for child in data.get("data", {}).get("children", []):
                        if len(articles) >= limit:
                            break
                        post = child.get("data", {}) or {}
                        articles.append({
                            "source": "reddit",
                            "title": post.get("title"),
                            "url": "https://reddit.com" + post.get("permalink", ""),
                            "content": (post.get("selftext") or "")[:2000],
                            "author": post.get("author", "")
                        })
                    time.sleep(0.4)
                except Exception as e:
                    print(f"Error scraping (reddit.json) {subreddit}: {e}")
                    continue

                if len(articles) >= limit:
                    break

        return articles