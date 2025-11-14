from pydantic import BaseModel
from datetime import datetime

class ArticleOut(BaseModel):
    id: str
    source: str
    title: str
    url: str
    content: str
    author: str
    scraped_at: datetime
    
    class Config:
        from_attributes = True

class ArticleList(BaseModel):
    articles: list[ArticleOut]
    total: int

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    title: str
    url: str
    source: str
    score: float
    snippet: str