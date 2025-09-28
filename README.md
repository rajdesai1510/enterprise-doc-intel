# 📄 Enterprise Document Intelligence System

**LLM-Powered Knowledge Extraction & Retrieval (RAG)**

🔗 **Live API (Swagger UI):**  
👉 https://enterprise-docs-ai-production.up.railway.app/docs

---

## 🚀 Overview

The **Enterprise Document Intelligence System** is a cloud-native, multi-tenant platform that enables organizations to ingest documents, extract knowledge, and perform **secure, explainable, LLM-powered question answering** over their internal data.

This system is designed for **real enterprise use cases** such as:

- Internal knowledge search
- Policy & compliance analysis
- Research intelligence
- Document-heavy decision support

---

## ✨ Key Features

### 🔐 Authentication & RBAC

- JWT-based authentication
- Role-based access control (Admin / User)
- Strict per-user document isolation (multi-tenancy)

### 📥 Intelligent Document Ingestion

- PDF upload with automatic parsing
- Adaptive chunking strategy based on:
  - Document structure
  - End-use (Q&A focused retrieval)
- Rich metadata captured for traceability

### 🔍 Semantic Search + RAG

- High-performance vector search using **Pinecone**
- Retrieval-Augmented Generation (RAG)
- **Groq-powered LLM inference** for low-latency responses
- Answers strictly grounded in retrieved document context

### 📌 Source Citations

- Every response includes:
  - Source document name
  - Chunk index
  - Relevance score
- Enables explainability and enterprise trust

### 📊 Usage Analytics

- Per-user query tracking
- Usage logging for monitoring and future billing
- Designed for scalability and observability

### ☁️ Cloud-Native Architecture

- Fully Dockerized backend
- Deployed on **Railway**
- External managed services for reliability and scale

---

## 🧠 System Architecture

```
Client (Swagger / UI)
        ↓
FastAPI Backend (Railway)
    ├── Auth & RBAC
    ├── Document Upload & Parsing
    ├── Adaptive Chunking Engine
    ├── Vector Store (Pinecone)
    ├── RAG Pipeline
    └── Usage Analytics
        ↓
External Services
    ├── Supabase Postgres (Metadata + Analytics)
    ├── Pinecone (Vector Search)
    └── Groq (LLM Inference)
```

---

## 🗂 Backend Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── upload.py            # Document ingestion
│   │   ├── query.py             # RAG query endpoint
│   │   ├── admin.py             # Admin operations
│   │   └── dependencies.py      # Security dependencies
│   │
│   ├── core/
│   │   ├── config.py            # Centralized configuration
│   │   ├── database.py          # SQLAlchemy setup
│   │   └── security.py          # JWT utilities
│   │
│   ├── models/
│   │   ├── user.py              # User schema
│   │   ├── document.py          # Document metadata
│   │   └── usage.py             # Query analytics
│   │
│   ├── services/
│   │   ├── auth.py              # Auth logic
│   │   ├── chunking.py          # Adaptive chunking
│   │   ├── vector_store.py      # Pinecone upsert logic
│   │   ├── retriever.py         # Semantic retrieval
│   │   ├── rag.py               # RAG orchestration
│   │   ├── llm.py               # Groq integration
│   │   └── analytics.py         # Usage tracking
│   │
│   ├── utils/
│   │   └── file_loader.py       # PDF text extraction
│   │
│   └── main.py                  # Application entry point
│
├── Dockerfile
└── requirements.txt
```

---

## 🔍 RAG Execution Flow

1. User uploads a document
2. Document is parsed and chunked intelligently
3. Chunks are embedded and stored in Pinecone
4. User submits a query
5. Relevant chunks are retrieved semantically
6. Retrieved context is passed to the LLM
7. Final answer is generated with citations

---

## 📌 Example API Response

```json
{
  "answer": "The internship duration mentioned in the document is 6 months.",
  "sources": [
    {
      "filename": "Internship_Description.pdf",
      "chunk_index": 3,
      "score": 0.91
    }
  ]
}
```

---

## 🛡️ Security & Isolation

- Namespace-based vector isolation per user
- JWT validation on every request
- No cross-user data leakage
- LLM responses restricted to retrieved context only

---

## 📈 Designed for Scale

- Stateless backend
- External vector and database services
- Ready for hybrid dense + sparse search
- Easy extension to streaming and reranking