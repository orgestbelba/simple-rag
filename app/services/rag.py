from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from app.services.embeddings import search_articles
from sqlalchemy.orm import Session
from app.models import Article
import os
from dotenv import load_dotenv

load_dotenv()
# Try to use OpenAI, fall back to simple text generation
try:
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    HAS_LLM = True
except:
    HAS_LLM = False
    print("⚠️  OpenAI API key not set. Using basic search only.")

async def rag_search(query: str, db: Session) -> dict:
    """Search + AI generation"""
    
    # Step 1: Find similar articles
    search_results = await search_articles(query, top_k=3)
    
    if not search_results:
        return {
            "query": query,
            "answer": "No articles found for your query.",
            "sources": [],
            "confidence": 0.0
        }
    
    # Step 2: Get full content
    article_ids = [r["id"] for r in search_results]
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
    
    # Step 3: Create context
    context = "\n---\n".join([
        f"[{a.source.upper()}] {a.title}\n{a.content}\nSource: {a.url}"
        for a in articles
    ])
    
    # Step 4: Generate answer
    if HAS_LLM:
        prompt = f"""Based on the following articles, answer the question concisely in 2-3 sentences.

ARTICLES:
{context}

QUESTION: {query}

ANSWER:"""
        
        try:
            response = llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            answer = f"Could not generate answer: {str(e)}"
    else:
        # Fallback: just summarize first article
        answer = f"Based on the top result: {articles[0].content[:200]}..."
    
    return {
        "query": query,
        "answer": answer,
        "sources": [
            {
                "title": s["title"],
                "url": s["url"],
                "source": s["source"],
                "similarity": s["score"]
            }
            for s in search_results
        ],
        "confidence": search_results[0]["score"] if search_results else 0.0
    }