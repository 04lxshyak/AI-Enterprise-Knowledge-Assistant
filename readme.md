# EKA – Enterprise Knowledge Assistant 🚀

> **Production-grade RAG system** that transforms enterprise documents into an AI-powered Q&A assistant. Built with modern tech stack: Next.js, FastAPI, PostgreSQL + pgvector, and LangChain.

**💡 The Problem:** Teams waste 2-3 hours daily searching through scattered documents (PDFs, Word docs, wikis) instead of focusing on high-value work.

**✅ The Solution:** Upload documents once, ask questions in natural language, get instant answers with source citations. Think "ChatGPT for your company's knowledge base."

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/next.js-14+-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-009688.svg)](https://fastapi.tiangolo.com)

## 🎥 Product Demo

🔗 **Try it now:** https://eka-ten.vercel.app  

[![EKA – Enterprise Knowledge Assistant Demo](https://img.youtube.com/vi/6fdRzY7N60M/0.jpg)](https://youtu.be/6fdRzY7N60M)

---

## 🎯 Key Features

- 📄 **Multi-format document processing** (PDF, DOCX, TXT) with smart chunking
- 🔍 **Vector search** via PostgreSQL + pgvector for semantic retrieval
- 💬 **Streaming answers** from GPT-4 with automatic source citations
- 🔐 **JWT auth** + per-user document isolation
- 📊 **Analytics** for usage tracking and cost monitoring

---

## 🛠️ Tech Stack

**Frontend:** Next.js 14 (App Router, TypeScript) · Tailwind + shadcn/ui · SSE streaming

**Backend:** FastAPI (Python 3.12+, async) · SQLAlchemy · LangChain · Pydantic v2

**Data & AI:** PostgreSQL + pgvector · VoyageAI embeddings · OpenAI GPT-4 · Supabase storage

**DevOps:** Docker Compose · Multi-stage builds · `uv` dependency manager

---

## 📐 Architecture

**Clean Architecture** with Repository Pattern: `Router → Service → Repository → Database`

**Backend:** Domain-driven modules (`auth`, `documents`, `chat`, `analytics`, `users`) with FastAPI dependency injection.

📄 **Detailed C4 diagrams** in `docs/c4/`

---

## 🔄 RAG Pipeline

```
1. Upload → Extract text → Chunk (512 tokens, semantic boundaries)
2. Generate embeddings (VoyageAI) → Store in pgvector
3. Query → Embed → Cosine similarity search → Top-K retrieval
4. Build prompt → GPT-4 generation → Stream response + citations
```



---

## 🎯 Design Decisions

**Architecture:** Repository pattern + dependency injection for testability and maintainability.

**RAG Strategy:** Hybrid chunking (semantic + 512 token limit) with metadata filtering for accurate retrieval.

**Trade-offs:** PDF parsing struggles with complex tables; large docs split into chunks; embedding costs scale with volume.

**Roadmap:** Rate limiting → Multi-tenant orgs → Redis caching → Multimodal RAG



## 🛠️ Technical Highlights

**Backend:** Clean Architecture (Router → Service → Repository) · Async/await · Custom error handling · Argon2 + JWT auth · FastAPI DI

**AI/ML:** Full RAG pipeline (not just PDF chat) · Production pgvector indexing · Embedding batching + cost tracking · Prompt optimization

**Frontend:** Next.js App Router (SSR + SSE streaming) · TypeScript · shadcn/ui components

**DevOps:** Docker multi-stage builds · Environment validation · Health checks

**Approach:** Clear docs · Explicit trade-offs · Business-focused problem solving  

---

## 📚 Resources

[Architecture Diagrams](docs/c4/) · [Data Model](docs/data-model/datamodel.md) · [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/) · [pgvector](https://github.com/pgvector/pgvector)

---

## Maintainer

This repository is maintained by [04lxshyak](https://github.com/04lxshyak).
Original project by [aarizah](https://github.com/aarizah) / Alex Ariza Herrera.

---

## 📝 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---



## 👤 Original Author

**Alex Ariza Herrera**  
Software Engineer | Full-Stack + AI | LLM Integrations | AI-Driven Product Development

- 💼 **LinkedIn:** [linkedin.com/in/alex-ariza-herrera/](https://www.linkedin.com/in/alex-ariza-herrera/)
- 🌐 **Portfolio:** [alexariza.dev](https://alexariza.dev)

---

<div align="center">
  
**⭐ If this project helped you, consider starring it on GitHub!**

</div>
