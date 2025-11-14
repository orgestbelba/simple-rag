from sentence_transformers import SentenceTransformer
import chromadb

# Use free HuggingFace model (no API key needed)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Vector DB (in-memory, saved to disk)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("articles")

async def embed_all_articles(db_session):
    """Embed all unembed articles"""
    from app.models import Article
    
    # Get articles without embeddings
    unembed = db_session.query(Article).all()
    
    for article in unembed:
        try:
            # Create embedding text
            text = f"{article.title}\n{article.content}"
            
            # Generate embedding
            embedding = embedding_model.encode(text)
            
            # Store in Chroma
            collection.add(
                ids=[article.id],
                embeddings=[embedding.tolist()],
                metadatas={
                    "title": article.title,
                    "source": article.source,
                    "url": article.url
                },
                documents=[text]
            )
            
        except Exception as e:
            print(f"Error embedding {article.id}: {e}")
    
    print(f"✓ Embedded {len(unembed)} articles")

async def search_articles(query: str, top_k: int = 5) -> list:
    """Search by semantic similarity"""
    
    # Embed query
    query_embedding = embedding_model.encode(query)
    
    # Search
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    
    # Format results
    formatted = []
    if results["ids"]:
        for i, doc_id in enumerate(results["ids"][0]):
            formatted.append({
                "id": doc_id,
                "title": results["metadatas"][0][i]["title"],
                "url": results["metadatas"][0][i]["url"],
                "source": results["metadatas"][0][i]["source"],
                "score": float(results["distances"][0][i]) if results.get("distances") else 0,
                "snippet": results["documents"][0][i][:200]
            })
    
    return formatted