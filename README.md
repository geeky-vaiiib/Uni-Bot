<p align="center">
  <img src="https://img.shields.io/badge/SIT-Tumakuru-blue?style=for-the-badge" alt="SIT Tumakuru"/>
  <img src="https://img.shields.io/badge/RAG-Powered-green?style=for-the-badge" alt="RAG Powered"/>
  <img src="https://img.shields.io/badge/Ollama-Local_LLM-orange?style=for-the-badge" alt="Ollama"/>
</p>

<h1 align="center">🎓 SIT Academic Assistant</h1>

<p align="center">
  <strong>AI-powered chatbot for Siddaganga Institute of Technology, Tumakuru</strong><br>
  <em>Powered by Retrieval-Augmented Generation (RAG) with 100% local inference</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/Ollama-Llama_3.2-FF6B6B" alt="Ollama"/>
  <img src="https://img.shields.io/badge/FAISS-Vector_Store-4285F4" alt="FAISS"/>
</p>

---

## � Overview

**SIT Academic Assistant** is a production-ready AI chatbot that answers student queries using official SIT documents. Unlike generic AI, it **never hallucinates** — it only provides verified information from the knowledge base or honestly says "I don't know."

### Why This Chatbot?

| ❌ Traditional Chatbots | ✅ SIT Academic Assistant |
|------------------------|---------------------------|
| Generic AI responses | Answers from official SIT documents only |
| Can hallucinate facts | Zero hallucination — admits when unsure |
| Requires API keys & costs | 100% local — no API limits or costs |
| No source verification | Every answer cites sources |

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Accurate & Verified
- Answers from 25+ official SIT documents
- Source citations with every response
- Zero hallucination policy

</td>
<td width="50%">

### 🏠 100% Local & Private
- Runs entirely on your machine
- No API keys or usage limits
- Student data never leaves your device

</td>
</tr>
<tr>
<td width="50%">

### 💬 Smart Query Modes
- **Student Mode**: Clear explanations
- **Exam Mode**: Exam policies & dates
- **Faculty Mode**: Administrative details

</td>
<td width="50%">

### 🎨 Modern UI
- Beautiful React frontend
- User authentication
- Mobile responsive design

</td>
</tr>
</table>

---

## � Knowledge Coverage

The chatbot can answer questions about:

| Category | Topics Covered |
|----------|---------------|
| **Academics** | Attendance (85%), Grading system, CGPA, Exam schedules |
| **Admissions** | KCET (E16), COMEDK (E125), Eligibility, Documents |
| **Placements** | Packages (₹5-45 LPA), Companies, Process |
| **Fees** | Branch-wise fees, Hostel charges, Scholarships |
| **Campus Life** | Library timings, Bus routes, Dress code, Clubs |
| **Facilities** | Hostels, Labs, Sports, Medical services |

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required software
- Python 3.9+
- Node.js 18+
- Ollama (https://ollama.ai)
```

### Step 1: Clone & Setup

```bash
git clone https://github.com/geeky-vaiiib/Uni-Bot.git
cd Uni-Bot

# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend && npm install && cd ..
```

### Step 2: Install AI Models

```bash
ollama pull llama3.2           # LLM for responses
ollama pull nomic-embed-text   # Embeddings for search
```

### Step 3: Run the App

**Terminal 1 — Backend:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

### Step 4: Open in Browser

| Service | URL |
|---------|-----|
| 🌐 Frontend | http://localhost:5173 |
| 📖 API Docs | http://localhost:8000/docs |

---

## 🔌 API Reference

### Ask a Question

```bash
POST /api/ask
```

```json
{
  "question": "What is the attendance requirement?",
  "mode": "student"
}
```

**Response:**
```json
{
  "answer": "The minimum attendance requirement is 85%...",
  "sources": [...],
  "confidence": "verified"
}
```

### Other Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ask` | POST | Ask a question |
| `/api/ingest?force_reload=true` | POST | Reload knowledge base |
| `/api/status` | GET | System health check |
| `/health` | GET | Simple health check |

---

## 📁 Project Structure

```
Uni-Bot/
├── 📂 app/                     # FastAPI Backend
│   ├── main.py                # Entry point
│   ├── config.py              # Settings
│   └── routers/chat.py        # API routes
│
├── 📂 core/                    # RAG Engine
│   ├── rag/                   # Retrieval pipeline
│   ├── embeddings/            # Ollama embeddings
│   ├── vectorstore/           # FAISS index
│   └── ingestion/             # Document processing
│
├── 📂 frontend/                # React UI
│   └── src/
│       ├── components/        # UI components
│       └── pages/             # Login, Signup, Chat
│
├── 📂 data/
│   ├── documents/             # 📄 SIT knowledge base
│   └── vectorstore/           # 🔍 Auto-generated index
│
└── requirements.txt
```

---

## � Adding New Knowledge

1. **Add documents** to `data/documents/` (supports `.md`, `.pdf`, `.txt`)

2. **Reload the knowledge base:**
   ```bash
   curl -X POST "http://localhost:8000/api/ingest?force_reload=true"
   ```

3. **Test your new content:**
   ```bash
   curl -X POST http://localhost:8000/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "Your question here", "mode": "student"}'
   ```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Llama 3.2 (via Ollama) |
| **Embeddings** | nomic-embed-text |
| **Vector Store** | FAISS |
| **Backend** | FastAPI + Python |
| **Frontend** | React 18 + Vite |
| **Styling** | CSS3 |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## � License

**Internal Use Only** — Siddaganga Institute of Technology

---

<p align="center">
  <strong>Built with ❤️ for SIT Students</strong><br>
  <em>Siddaganga Institute of Technology, Tumakuru</em>
</p>
