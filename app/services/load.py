from sqlalchemy.orm import Session
from app.models import Article
from app.scrapers.wikipedia import WikipediaScraper
from app.scrapers.blogs import DevtoScraper
from app.scrapers.reddit import RedditScraper

async def scrape_and_load(db: Session):
    """Run all scrapers and save to DB"""
    
    scrapers = [
        WikipediaScraper(),
        DevtoScraper(),
        RedditScraper()
    ]
    
    for scraper in scrapers:
        print(f"Running {scraper.__class__.__name__}...")
        
        try:
            items = await scraper.fetch(limit=20)
            
            for item in items:
                # Skip if already in DB
                existing = db.query(Article).filter(
                    Article.url == item["url"]
                ).first()
                
                if not existing:
                    article = Article(**item)
                    db.add(article)
            
            db.commit()
            print(f"✓ Loaded {len(items)} articles")
        
        except Exception as e:
            print(f"✗ Error: {e}")
    
    count = db.query(Article).count()
    print(f"✓ Total articles: {count}")

# Quick load script
if __name__ == "__main__":
    import asyncio
    from app.models import SessionLocal
    db = SessionLocal()
    asyncio.run(scrape_and_load(db))
    
    # Count
    count = db.query(Article).count()
    print(f"✓ Total articles: {count}")