# Job Market Intelligence — RAG Pipeline

> Query the job market with natural language. Built with LangChain, ChromaDB, FastAPI & Docker.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=flat-square)
![MLflow](https://img.shields.io/badge/MLflow-tracked-orange?style=flat-square)
![Build](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)

---

## What This Project Does

Most job market tools show you raw listings. This pipeline lets you **ask questions**:

- *"What MLOps skills are companies hiring for right now?"*
- *"Which Python libraries appear most in AI Engineer job descriptions?"*
- *"How many roles require Docker vs Kubernetes?"*

It scrapes real job postings → vectorizes them → serves answers via a REST API. End to end. Production ready.

---

## Architecture

```
Job Boards (LinkedIn / Indeed)
        │
        ▼
   [scraper/]          ← Python scraper, collects raw job postings
        │
        ▼
   [pipeline/]         ← Cleans, chunks & embeds text into vectors
        │
        ▼
   [chroma_db/]        ← ChromaDB vector store (local, persistent)
        │
        ▼
   [api/]              ← FastAPI endpoint — ask questions in plain English
        │
        ▼
   [tracking/]         ← MLflow experiment & query tracking
```

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Orchestration | LangChain | RAG pipeline management |
| Vector Store | ChromaDB | Local, fast, zero cost |
| Embeddings | HuggingFace | Free, runs locally |
| API | FastAPI | Production-grade REST |
| Containerisation | Docker + Compose | Runs anywhere |
| Experiment Tracking | MLflow | Full query + metric logging |
| Language | Python 3.10+ | |

---

## Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/Harry160820/job-market-rag.git
cd job-market-rag
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run with Docker (recommended)
```bash
docker-compose up --build
```

### 4. Query the API
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What MLOps skills are most in demand?"}'
```

---

## Project Structure

```
job-market-rag/
├── scraper/          # Job posting scraper
├── pipeline/         # Embedding & ingestion pipeline
├── chroma_db/        # Vector store (persistent)
├── api/              # FastAPI app
├── data/             # Raw & processed job data
├── tracking/         # MLflow tracking setup
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## MLflow Tracking

All queries and pipeline runs are tracked via MLflow.

```bash
mlflow ui
# Open http://localhost:5000
```

---
## Demo

[▶ Watch Demo on YouTube](https://youtu.be/-SsSkb7bWW8)

```

```
## Roadmap

- [x] Project structure & Docker setup
- [ ] Scraper — LinkedIn & Indeed job postings
- [ ] Embedding pipeline — chunk & vectorize
- [ ] ChromaDB ingestion
- [ ] FastAPI query endpoint
- [ ] MLflow experiment tracking
- [ ] GitHub Actions CI/CD
- [ ] Live demo deployment

---

## Follow the Build

This project is being built completely in public — every commit documented.

- YouTube: [HarryCommits](https://youtube.com/@harrycommits)
- LinkedIn: [Hari Om](https://www.linkedin.com/in/hari-om-17b093189/)
- X: [@HarryCommits](https://x.com/HarryCommits)

---

## Author

**Harry** — AI/MLOps Engineer

---

⭐ Star this repo if you're following the build — it helps more people find it.
