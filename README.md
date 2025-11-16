# Simple RAG Search Engine

A semantic search engine that scrapes websites and lets you ask AI questions about them.

## Quick Start

### Setup
\`\`\`bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

### Scrape Articles
\`\`\`bash
python -c "
import asyncio
from app.services.load import scrape_and_load
from app.models import SessionLocal

db = SessionLocal()
asyncio.run(scrape_and_load(db))
"
\`\`\`

### Embed Articles
\`\`\`bash
python -c "
import asyncio
from app.services.embeddings import embed_all_articles
from app.models import SessionLocal

db = SessionLocal()
asyncio.run(embed_all_articles(db))
"
\`\`\`

### Run Server
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

Open: http://localhost:8000/docs

## API Endpoints

### Browse
- `GET /articles` - List all articles
- `GET /articles/{id}` - Get single article
- `GET /stats` - Statistics

### Search
- `POST /search` - Semantic search (no AI)
- `POST /rag-search` - With AI-generated answers

### Health
- `GET /health` - Health check

## Examples

### Search
\`\`\`bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"machine learning","top_k":5}'
\`\`\`

### RAG Search (with AI)
\`\`\`bash
curl -X POST http://localhost:8000/rag-search \
  -H "Content-Type: application/json" \
  -d '{"query":"Explain deep learning","top_k":3}'
\`\`\`

## With Docker
\`\`\`bash
docker-compose up --build
\`\`\`

## Data Sources

- **Wikipedia**: AI and tech articles
- **Dev.to**: Python and web development posts
- **Reddit**: Community discussions

No authentication needed - all data is publicly available!

## Optional: Enable OpenAI

To get LLM-powered answers:

1. Get an OpenAI API key: https://platform.openai.com/api-keys
2. Create `.env` file:
   \`\`\`
   OPENAI_API_KEY=sk-...
   \`\`\`
3. Restart server

Without it, `/rag-search` still works but returns article summaries instead of AI answers.

## Testing

\`\`\`bash
pytest tests/ -v
\`\`\`

## Project Structure

\`\`\`
simple-rag/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── scrapers/
│   │   ├── wikipedia.py
│   │   ├── blogs.py
│   │   └── reddit.py
│   ├── services/
│   │   ├── load.py
│   │   ├── embeddings.py
│   │   └── rag.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── .env (optional)
├── docker-compose.yml
├── Dockerfile
└── README.md
\`\`\`

## What You'll Learn

- **Data Engineering**: Web scraping with BeautifulSoup
- **Software Engineering**: REST API with FastAPI
- **AI Engineering**: Embeddings + semantic search + RAG
- **DevOps**: Docker containerization

Enjoy! 🚀