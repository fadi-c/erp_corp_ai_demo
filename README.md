
# ERP AI Backend

flowchart TD
    %% Client
    Client[Client / Frontend] -->|HTTP Request| API[API (Django Ninja)]
    
    %% API endpoints
    API -->|/health| Health[Health Endpoint]
    API -->|/question| Question[Question Endpoint]
    API -->|/invoices| Invoices[Invoices Endpoint]
    
    %% Question pipeline
    Question --> HybridRetrieval[HybridRetrieval]
    HybridRetrieval -->|SQL route| SQLAnalytics[SQLAnalyticsService]
    HybridRetrieval -->|Keyword route| KeywordSearch[KeywordSearch]
    HybridRetrieval -->|Vector route| RAGPipeline[RAG Pipeline]
    
    %% RAG pipeline
    RAGPipeline --> RetrievalService[RetrievalService]
    RetrievalService -->|Query nearest embeddings| InvoiceEmbeddingDB[InvoiceEmbedding (pgvector)]
    InvoiceEmbeddingDB -->|Prefetch orders| Orders[Order & Product data]
    RetrievalService --> Context[Build context for LLM]
    
    %% LLM processing
    Context --> LLMFactory[LLMFactory]
    LLMFactory --> LLMModel[BaseLLM / OpenAI / Groq / Dev]
    LLMModel --> Answer[AI Answer returned to Client]
    
    %% Async embedding pipeline
    Invoice[Invoice created] -->|post_save signal| CeleryTask[Celery Task: generate_invoice_embedding]
    CeleryTask --> InvoiceEmbeddingDB
    CeleryBeat[Celery Beat: generate_missing_invoice_embeddings every 5 min] --> CeleryTask
    
    %% Observability
    API -->|metrics| Prometheus[Prometheus Metrics Server 5555]
    CeleryTask -->|metrics| Prometheus
    CeleryBeat -->|metrics| Prometheus
    
    %% Data seeding
    SeedData[Management Command: seed_data] -->|Generate Customers, Products, Orders, Invoices| ERPDB[PostgreSQL]
    SeedData -->|Generate Embeddings| InvoiceEmbeddingDB

A modern ERP backend with **AI-powered invoice analytics**, semantic search, embedding generation, and full observability.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Overview](#architecture-overview)
4. [Backend Architecture](#backend-architecture)
5. [Data Model](#data-model)
6. [AI / Semantic Search Pipeline](#ai--semantic-search-pipeline)
7. [Embedding Generation System](#embedding-generation-system)
8. [API Endpoints](#api-endpoints)
9. [Observability](#observability)
10. [Background Processing](#background-processing)
11. [Data Seeding](#data-seeding)
12. [Vector Search Implementation](#vector-search-implementation)
13. [Scalability & Extensibility](#scalability--extensibility)
14. [Future Improvements](#future-improvements)

---

## Project Overview

* ERP backend with **AI-powered analytics**
* Natural language question answering on invoices
* Semantic search using **vector embeddings** (pgvector / OpenAI / Dev / Local)
* Observability with **Prometheus metrics**
* Asynchronous pipeline for embedding generation using **Celery**

---

## Technology Stack

| Layer             | Technology / Library            | Purpose                                           |
| ----------------- | ------------------------------- | ------------------------------------------------- |
| Backend Framework | Django + Django Ninja           | API & ORM                                         |
| Database          | PostgreSQL + pgvector           | Relational storage + vector embeddings            |
| Async Processing  | Celery + Redis / Broker         | Async tasks & scheduler                           |
| AI / LLM          | OpenAI, Groq, Dev               | NLP & question answering                          |
| Embeddings        | OpenAI, Local, Dev              | Vector embeddings (1536 dimensions)               |
| Observability     | Prometheus + prometheus_client  | API & Celery monitoring                           |
| Testing / Seeding | Faker, FactoryBoy               | Generate realistic ERP demo data                  |
| Metrics           | Counter, Gauge, Histogram       | Track requests, latency, embeddings, Celery tasks |
| Deployment / Env  | .env, threading, os, celery CLI | Configuration & orchestration                     |

---

## Architecture Overview

```txt
Client
   |
   v
API (Django Ninja)
   |
   +--> ERP Services
   +--> AnalysisService
           |
           v
      Embedding Retrieval
           |
           v
      PostgreSQL + pgvector
           ^
           |
      Celery Workers
```

* API layer handles HTTP requests
* ERP layer handles models, repository, and services
* AI layer contains embeddings, retrieval, and LLM clients
* Celery pipeline asynchronously generates embeddings
* PostgreSQL + pgvector for storage and vector search

---

## Backend Architecture

```txt
api/
   endpoints.py
   schemas.py
erp/
   models.py
   repository.py
   services.py
   signals.py
analysis/
   hybrid_retrieval.py
   sql_analytics.py
   query_router.py
ai/
   embeddings/
   llm/
   rag_pipeline.py
   retrieval.py
workers/
   tasks.py
```

* Patterns: Repository, Service Layer, Event-driven signals, Async task pipeline
* AI & embeddings modules separated for flexibility and quick swapping

---

## Data Model

```txt
Customer
   |
   v
Invoice ---- Order ---- Product
   |
   v
InvoiceEmbedding (vector)
```

* Customer → Invoice (1-N)
* Invoice → Orders (N-M)
* InvoiceEmbedding → vector embeddings (dimension 1536)
* IVFFlat index for fast vector search

---

## AI / Semantic Search Pipeline

```txt
User Question
      |
      v
HybridRetrieval
      |
      +-- SQLAnalyticsService
      +-- KeywordSearch
      +-- RagPipeline -> RetrievalService
                     -> InvoiceEmbedding vector DB
      |
      v
LLMFactory -> BaseLLM -> answer
```

* **HybridRetrieval** routes questions to SQL / keyword / vector pipelines
* **RAG Pipeline** builds context from nearest embeddings
* LLMFactory selects the model (OpenAI / Groq / Dev)

---

## Embedding Generation System

```txt
Invoice created
      |
      v
post_save signal
      |
      v
Celery task generate_invoice_embedding
      |
      v
InvoiceEmbedding stored in pgvector
```

* Event-driven: Django signal → Celery task → embedding
* Scheduled recovery: `generate_missing_invoice_embeddings` every 5 minutes via Celery Beat

---

## API Endpoints

| Endpoint  | Method | Description                                |
| --------- | ------ | ------------------------------------------ |
| /health   | GET    | Status OK & latency metrics                |
| /question | POST   | Ask AI question → returns answer + sources |
| /invoices | GET    | Paginated invoice list                     |

---

## Observability

```txt
API / Celery Task
       |
       v
Prometheus Metrics
       |
       v
Ports 5555 (worker) / 5556 (beat)
```

Metrics exposed:

* `api_requests_total` (Counter)
* `api_request_latency_seconds` (Histogram)
* `missing_invoice_embeddings_total` (Gauge)
* `celery_task_total` (Counter)
* `celery_task_duration_seconds` (Histogram)

---

## Background Processing

* Celery worker and beat
* Async embedding pipeline
* Beat schedule:

```txt
generate_missing_invoice_embeddings every 5 min
```

---

## Data Seeding

* Command:

```bash
python manage.py seed_data
```

* Generates:

  * Customers, Products, Orders, Invoices
  * Real embeddings via EmbeddingFactory
* Uses Faker & FactoryBoy

---

## Vector Search Implementation

* pgvector with ivfflat index and cosine distance
* Prefetch + select_related to prevent N+1 queries
* Default result limit: 30
* RAG pipeline builds full context for LLM

---

## Scalability & Extensibility

* Async embedding pipeline (Celery)
* Hybrid retrieval (SQL / keyword / vector)
* Factory pattern for LLM & embeddings (swap OpenAI / Groq / Dev / Local)
* Full Prometheus monitoring

---

## Future Improvements

* Streaming LLM responses
* Embedding caching for faster vector search
* Multi-document retrieval for broader context
* Advanced dashboards for monitoring

