# SIT RAG Chatbot

Production-ready Retrieval-Augmented Generation (RAG) chatbot for **Siddaganga Institute of Technology (SIT)**, Tumakuru.

## Features

- ✅ **Strict Information Governance**: Answers only from official SIT documents
- ✅ **Zero Hallucination**: Explicitly refuses when information is not available
- ✅ **Multiple Query Modes**: Student, Exam, and Faculty/Admin modes
- ✅ **Source Citations**: Every answer includes document references
- ✅ **Production Ready**: FastAPI with proper error handling and logging

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/vaibhavjp/UniBot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Add Documents

Place official SIT documents (PDF, TXT, MD) in:
```
data/documents/
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

### 5. Test the API

```bash
# Ask a question
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the attendance requirement?", "mode": "student"}'

# Ingest documents
curl -X POST http://localhost:8000/api/ingest

# Check status
curl http://localhost:8000/api/status
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Health check |
| `/api/ask` | POST | Ask a question |
| `/api/ingest` | POST | Ingest documents |
| `/api/status` | GET | Service status |

## Query Modes

- **student**: Clear, step-by-step explanations for students
- **exam**: Focused on examination policies and procedures
- **faculty**: Detailed policy-oriented responses for staff

## Project Structure

```
UniBot/
├── app/                    # FastAPI application
│   ├── main.py            # Application entry point
│   ├── config.py          # Configuration
│   ├── models.py          # Request/Response models
│   └── routers/
│       └── chat.py        # API endpoints
├── core/                   # Core RAG components
│   ├── prompts/           # Prompt templates
│   ├── ingestion/         # Document loading & chunking
│   ├── embeddings/        # Embedding service
│   ├── vectorstore/       # FAISS vector store
│   └── rag/               # RAG pipeline
├── data/
│   └── documents/         # Place SIT PDFs here
├── tests/                 # API tests
├── requirements.txt
└── .env.example
```

## Documentation

- **OpenAPI Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## License

Internal use only - Siddaganga Institute of Technology
