from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models import Article, get_db
from app.schemas import ArticleOut, ArticleList, SearchRequest, SearchResult
from app.services.embeddings import search_articles

router = APIRouter()

@router.get("/articles", response_model=ArticleList)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """List all articles with pagination"""
    total = db.query(Article).count()
    articles = db.query(Article).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return ArticleList(
        articles=[ArticleOut.from_orm(a) for a in articles],
        total=total
    )

@router.get("/articles/{article_id}", response_model=ArticleOut)
async def get_article(article_id: str, db: Session = Depends(get_db)):
    """Get single article"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    return ArticleOut.from_orm(article)

@router.post("/search", response_model=list[SearchResult])
async def search(req: SearchRequest):
    """Search articles by similarity"""
    results = await search_articles(req.query, top_k=req.top_k)
    return [SearchResult(**r) for r in results]

@router.get("/stats")
async def stats(db: Session = Depends(get_db)):
    """Get statistics"""
    total = db.query(Article).count()
    by_source = {}
    
    for source in ["wikipedia", "devto", "reddit"]:
        count = db.query(Article).filter(Article.source == source).count()
        by_source[source] = count
    
    return {
        "total_articles": total,
        "by_source": by_source
    }

@router.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}