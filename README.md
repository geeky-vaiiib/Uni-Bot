# SIT RAG Chatbot

Production-ready Retrieval-Augmented Generation (RAG) chatbot for **Siddaganga Institute of Technology (SIT)**, Tumakuru. Powered by **Ollama** for completely local, API-free inference.

## ✨ Features

- 🎓 **Comprehensive Knowledge Base**: 25+ documents covering admissions, academics, placements, fees, hostel, library, and more
- 🔒 **Strict Information Governance**: Answers only from official SIT documents
- 🚫 **Zero Hallucination**: Explicitly refuses when information is not available
- 📱 **Beautiful React Frontend**: Modern UI with authentication and chat interface
- 🎯 **Multiple Query Modes**: Student, Exam, and Faculty/Admin modes
- 📚 **Source Citations**: Every answer includes document references
- 🏠 **100% Local**: Uses Ollama (Llama 3.2) - no API keys or usage limits!

## 📋 Knowledge Coverage

The chatbot can answer questions about:
- ✅ Attendance requirements (85%)
- ✅ Placement packages (₹5-45 LPA)
- ✅ Hostel fees & facilities
- ✅ Admission process (KCET/COMEDK)
- ✅ Grading system & CGPA
- ✅ Library timings & services
- ✅ Bus routes & transportation
- ✅ Dress code
- ✅ Exam schedules
- ✅ Fee structure (branch-wise)
- ✅ Scholarships & concessions
- ✅ Campus facilities
- ✅ Clubs & events
- ✅ Rules & regulations

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- [Ollama](https://ollama.ai) with `llama3.2` and `nomic-embed-text` models

### 1. Install Ollama Models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 2. Backend Setup

```bash
cd /Users/vaibhavjp/UniBot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access the App

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Health check |
| `/api/ask` | POST | Ask a question |
| `/api/ingest` | POST | Ingest/reload documents |
| `/api/status` | GET | Service status |

### Example API Usage

```bash
# Ask a question
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the attendance requirement?", "mode": "student"}'

# Force reload documents
curl -X POST "http://localhost:8000/api/ingest?force_reload=true"
```

## 🎯 Query Modes

- **student**: Clear, step-by-step explanations for students
- **exam**: Focused on examination policies and procedures
- **faculty**: Detailed policy-oriented responses for staff

## 📁 Project Structure

```
UniBot/
├── app/                    # FastAPI backend
│   ├── main.py            # Application entry point
│   ├── config.py          # Configuration
│   ├── models.py          # Request/Response models
│   └── routers/
│       └── chat.py        # API endpoints
├── core/                   # Core RAG components
│   ├── ingestion/         # Document loading & chunking
│   ├── embeddings/        # Ollama embedding service
│   ├── vectorstore/       # FAISS vector store
│   └── rag/               # RAG pipeline
├── frontend/              # React frontend
│   └── src/
│       ├── components/    # UI components
│       └── pages/         # Login, Signup, Chat
├── data/
│   ├── documents/         # SIT knowledge base (25+ docs)
│   └── vectorstore/       # FAISS index (auto-generated)
└── requirements.txt
```

## 📚 Adding New Knowledge

1. Add markdown/PDF files to `data/documents/`
2. Trigger re-ingestion:
   ```bash
   curl -X POST "http://localhost:8000/api/ingest?force_reload=true"
   ```

## 📖 Documentation

- **OpenAPI Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📄 License

Internal use only - Siddaganga Institute of Technology
