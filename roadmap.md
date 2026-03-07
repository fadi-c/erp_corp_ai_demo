
---


# ERP_CORP AI-Native Backend Demo

Minimal backend prototype inspired by the architecture described in the ERP_CORP job description.

The goal of this project is to demonstrate how an **AI-native backend** can connect business data (ERP-like datasets) with **RAG workflows, agents, and typed APIs**.

This project intentionally focuses on:

- clean architecture
- typed APIs
- AI-native design
- reproducibility with Docker
- low operational cost

It is designed to run **fully locally**.

---

# Goals of the Demo

This project demonstrates the following technical capabilities:

- Django backend architecture
- High-performance typed APIs using Django Ninja
- Data validation using Pydantic
- ERP-like data modeling
- Retrieval-Augmented Generation (RAG)
- AI workflows on business data
- Async job processing
- Observability and monitoring
- Fully containerized environment

The goal is not to reproduce a full ERP, but to simulate **real-world enterprise data workflows**.

---

# High-Level Architecture

The system architecture follows an **AI-native backend design**.



```
          +-----------------------+
          |      Frontend         |
          | (optional dashboard)  |
          | React / Typescript    |
          +-----------+-----------+
                      |
                      |
                      v
             +------------------+
             |    API Layer     |
             | Django Ninja     |
             | Typed endpoints  |
             +--------+---------+
                      |
                      |
                      v
           +----------------------+
           |   Backend Services   |
           | Django + Pydantic    |
           | Business logic       |
           +----------+-----------+
                      |
        +-------------+-------------+
        |                           |
        v                           v
+--------------+            +----------------+
| PostgreSQL   |            | Async Workers  |
| ERP data     |            | Celery         |
| pgvector     |            | Redis queue    |
+------+-------+            +--------+-------+
       |                             |
       |                             |
       v                             v
 +------------+               +--------------+
 | RAG Engine |               | LLM Provider |
 | Embeddings |               | OpenAI API   |
 +------------+               +--------------+
```


---

# Core Concept

The backend simulates an **AI-native ERP intelligence layer**.

Instead of traditional dashboards, users can ask questions such as:

```

Why did our margin decrease in March?

````

The system:

1. Retrieves relevant ERP data
2. Uses vector search to find context
3. Calls an LLM
4. Generates an explanation

This is an example of **Retrieval-Augmented Generation (RAG)** applied to enterprise data.

---

# Technology Stack

| Layer | Technology | Purpose |
|------|------|------|
| Backend | Django | Core backend framework |
| API | Django Ninja | High-performance typed APIs |
| Validation | Pydantic | Request/response validation |
| Database | PostgreSQL | Core relational database |
| Vector Search | pgvector | Embeddings storage |
| Queue | Redis | Async task broker |
| Workers | Celery | Background processing |
| AI | OpenAI API | LLM for analysis |
| Monitoring | Prometheus | Metrics collection |
| Dashboard | Grafana | Observability |
| Containers | Docker | Reproducible environment |

All components run **locally using Docker Compose**.

---

# Why This Stack

## Django

Django provides:

- mature ORM
- authentication system
- admin interface
- strong ecosystem

It is well suited for **data-heavy SaaS backends**.

---

## Django Ninja

Django Ninja adds modern API capabilities to Django:

- type-safe endpoints
- OpenAPI documentation
- fast request parsing
- Pydantic integration

Example:

```python
@api.get("/invoices")
def list_invoices(request) -> List[InvoiceSchema]:
    return Invoice.objects.all()
````

---

## Pydantic

Pydantic provides:

* strict validation
* schema generation
* JSON parsing
* typing guarantees

This is particularly useful when interacting with **LLM outputs**.

---

## PostgreSQL + pgvector

PostgreSQL stores structured ERP data.

The pgvector extension enables:

* vector embeddings
* semantic search
* RAG pipelines

Example stored entities:

```
customers
products
orders
invoices
```

---

## Celery + Redis

Async workers handle heavy tasks:

* data ingestion
* embeddings generation
* AI analysis
* background workflows

Why async?

LLM calls are slow and should not block API requests.

---

## OpenAI API

Used for:

* embeddings generation
* analysis of ERP data
* natural language explanations

This keeps the AI layer **simple and realistic**.

---

## Prometheus + Grafana

Observability stack.

Prometheus collects metrics such as:

```
API latency
AI request duration
worker task execution time
database query time
```

Grafana provides dashboards for monitoring system health.

---

# Data Model (ERP Simulation)

Instead of integrating a real ERP, the demo uses a **simplified schema**.

```
Customer
    id
    name
    industry

Product
    id
    name
    category

Invoice
    id
    customer_id
    amount
    margin
    date
    description

Order
    id
    product_id
    quantity
    price
```

These tables simulate typical **ERP financial data**.

---

# AI Workflow

The AI pipeline works as follows.

```
User question
      |
      v
API endpoint
(Django Ninja)
      |
      v
RAG service
      |
      v
Vector search
(pgvector)
      |
      v
Relevant invoices retrieved
      |
      v
LLM call
(OpenAI)
      |
      v
Generated explanation
      |
      v
API response
```

---

# Example Query

User question:

```
Which customers have the largest margin drop?
```

Pipeline:

```
1. Retrieve relevant invoices
2. Generate embeddings
3. Perform vector search
4. Send context to LLM
5. Generate explanation
```

---

# Async Processing Flow

Some tasks run in background workers.

Example:

```
New invoice created
       |
       v
Celery task triggered
       |
       v
Embedding generated
       |
       v
Stored in pgvector
       |
       v
Available for RAG queries
```

---

# Monitoring Flow

```
API request
     |
     v
Metrics exported
(prometheus-client)
     |
     v
Prometheus collects data
     |
     v
Grafana dashboards
```

---

# Project Structure

```
ERP_CORP-ai-demo/

backend/
    manage.py

    core/
        settings.py
        urls.py

    api/
        router.py
        schemas.py

    erp/
        models.py
        services.py

    ai/
        rag.py
        embeddings.py
        agents.py

    workers/
        tasks.py

docker/
    Dockerfile
    docker-compose.yml

requirements.txt
README.md
```

---

# Running the Project

Build and start the environment:

```
docker compose up --build
```

Services started:

```
backend API
postgres database
redis queue
celery worker
prometheus
grafana
```

---

# Expected Endpoints

```
GET /api/invoices
GET /api/customers
POST /api/question
```

Example:

```
POST /api/question
{
  "question": "Why did our margins drop in March?"
}
```

---

# Cost

This demo is designed to be extremely cheap.

| Component    | Cost |
| ------------ | ---- |
| Local stack  | Free |
| Docker       | Free |
| OpenAI usage | ~5€  |

Total cost: **under 10€**.

---

# Future Improvements

Possible extensions:

* agent-based workflows
* automated anomaly detection
* ERP connectors
* React dashboard
* multi-tenant architecture

---

# Purpose of This Demo

This project demonstrates the foundations of an **AI-native backend**.

It focuses on:

* architecture
* developer experience
* realistic AI integration

The implementation is intentionally minimal but reflects **modern SaaS backend design**.

---