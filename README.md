<div align="center">
  <h1><strong>AGENCY AI ORCHESTRATOR</strong></h1>
  <p><em>Enterprise-grade, Multi-Agent System for Digital Agency Workflow Automation</em></p>

  <br>
  <p>
    <img src="https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/LangGraph-000000?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph">
    <img src="https://img.shields.io/badge/Groq_Cloud-F55036?style=for-the-badge&logo=groq&logoColor=white" alt="Groq">
    <img src="https://img.shields.io/badge/LangSmith-000000?style=for-the-badge&logo=langchain&logoColor=white" alt="LangSmith">
    <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
    <br>
    <img src="https://img.shields.io/badge/SQLAlchemy_Async-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
    <img src="https://img.shields.io/badge/ClickUp-7B68EE?style=for-the-badge&logo=clickup&logoColor=white" alt="ClickUp">
    <img src="https://img.shields.io/badge/Brevo-0092FF?style=for-the-badge&logo=brevo&logoColor=white" alt="Brevo">
    <img src="https://img.shields.io/badge/Telegram_API-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/Google_Cloud_Run-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Cloud Run">
  </p>
</div>

<hr>

## Project Overview

**Agency AI Orchestrator** is a high-performance, production-ready AI backend designed to convert human-in-the-loop manual administrative tasks into autonomous AI-driven workflows. Built specifically for digital agencies, it intelligently integrates existing stacks (ClickUp, Brevo, Telegram) using complex reasoning powered by Large Language Models.

## Core Architecture & Capabilities

* **Multi-Agent Orchestration:** Utilizes **LangGraph** to govern complex, multi-step stateful AI workflows, managing transitions between data extraction, reasoning, and third-party execution.
* **Artificial Intelligence:** Powered by **Groq Cloud (Llama-3)**, ensuring ultra-low latency inference for rapid intent classification, budget estimation, and granular task extraction from Statement of Work (SOW) documents.
* **High-Performance Database:** Integrates **Supabase (PostgreSQL)**. Features non-blocking data persistence using **Async SQLAlchemy**, with **Alembic** for robust database schema versioning.
* **Robust Security:** Webhook endpoints are strictly protected via **Shared Secret Authentication**. The system verifies the `X-Webhook-Signature` header against the secure environment Telegram Bot Token to prevent unauthorized executions.

## Automated Workflows

### 1. Auto-Lead Qualification & Proposal
* Automatically parses incoming email payloads.
* AI classifies the intent (`LEAD`, `SPAM`, `SUPPORT`) and extracts estimated budgets.
* Generates contextual, dynamic draft proposals including estimated timelines based on project complexity.
* Dispatches real-time **Telegram** notifications containing the parsed lead summary and the generated proposal.

### 2. Project Kickoff Automation
* Ingests Statement of Work (SOW) documents upon project closure.
* AI extracts and structures actionable tasks dynamically.
* Autonomously provisions **ClickUp** architecture by creating the necessary Folder, List, and performing batch Task creation.
* Triggers **Brevo** to dispatch a polished, automated onboarding email sequence directly to the client.

## Technology Stack

<div align="center">
  <table style="width: 100%; border-collapse: collapse;">
    <tr>
      <th style="text-align: center; border-bottom: 2px solid #ddd; padding: 10px;">Category</th>
      <th style="text-align: center; border-bottom: 2px solid #ddd; padding: 10px;">Technologies</th>
    </tr>
    <tr>
      <td style="padding: 10px;"><b>Core Framework</b></td>
      <td style="padding: 10px;">Python 3.12, FastAPI</td>
    </tr>
    <tr>
      <td style="padding: 10px;"><b>AI & Orchestration</b></td>
      <td style="padding: 10px;">LangGraph, Groq Cloud (Llama-3), LangSmith</td>
    </tr>
    <tr>
      <td style="padding: 10px;"><b>Database & ORM</b></td>
      <td style="padding: 10px;">Supabase, PostgreSQL, SQLAlchemy (Async), Alembic</td>
    </tr>
    <tr>
      <td style="padding: 10px;"><b>Integrations</b></td>
      <td style="padding: 10px;">ClickUp API, Brevo API, Telegram Bot API</td>
    </tr>
    <tr>
      <td style="padding: 10px;"><b>Deployment</b></td>
      <td style="padding: 10px;">Docker, Google Cloud Run</td>
    </tr>
  </table>
</div>

## Directory Structure

The repository is built strictly adhering to **Clean Architecture** and **SOLID Principles**.

```text
agency-ai-orchestrator/
├── alembic/              # Database migration configurations and version scripts.
├── app/                  # Main application source code.
│   ├── agents/           # LangGraph definitions. Contains AI workflow logic (Workflow A & B).
│   ├── api/              # Entrypoints & Routing. Houses the FastAPI controllers and Webhooks.
│   ├── core/             # Centralized settings, structured loggers, exceptions, cache, and observability setup.
│   ├── db/               # Database connection logic, specifically the Async SQLAlchemy Supabase engine.
│   ├── models/           # Pydantic schemas (DTOs) for robust validation and SQLAlchemy ORM schemas.
│   └── services/         # Business logic & 3rd party wrappers (Groq, ClickUp, Brevo, Telegram).
├── Dockerfile            # Multi-stage container definitions optimized for Google Cloud Run.
├── requirements.txt      # Pinned Python dependencies.
└── .env.example          # Template for all required environment variables.
```

## Deployment & Scalability

This system is architected for **Industrial-Scale Deployment**. 
* **Containerization:** The repository includes a highly optimized, multi-stage `Dockerfile` based on `python:3.12-slim`.
* **Serverless Execution:** Designed to be deployed on **Google Cloud Run**, taking full advantage of scale-to-zero capabilities to eliminate idle costs while easily scaling horizontally under high-throughput webhook loads.
* **Background Tasks:** Time-intensive AI reasoning and third-party API dispatches are strictly handled via FastAPI `BackgroundTasks` to guarantee sub-second HTTP responses, preventing webhook timeouts.

## Environment Configuration

To run the orchestrator locally or configure it for production, copy `.env.example` to `.env` and ensure the following keys are populated. The system uses `pydantic-settings` to strictly validate these upon startup:

```env
# ---------------------------------------------------------
# CORE SETTINGS
# ---------------------------------------------------------
APP_NAME=agency-ai-orchestrator
PYTHON_VERSION=3.12.0
DEBUG=True

# ---------------------------------------------------------
# AI / LLM (GROQ CLOUD)
# ---------------------------------------------------------
GROQ_API_KEY=your_groq_api_key

# ---------------------------------------------------------
# GOOGLE CLOUD PLATFORM (GCP)
# ---------------------------------------------------------
GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
GCP_PROJECT_ID=your_gcp_project_id  # Used specifically for Google Cloud deployments
GCP_REGION=asia-southeast2

# ---------------------------------------------------------
# INTEGRATIONS
# ---------------------------------------------------------
# ClickUp
CLICKUP_API_TOKEN=your_clickup_api_token
CLICKUP_TEAM_ID=your_clickup_team_id

# Brevo (Transactional Email)
BREVO_API_KEY=your_brevo_api_key
SENDER_EMAIL=your_sender_email@domain.com

# Telegram (Notifications)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# ---------------------------------------------------------
# OBSERVABILITY & TRACING (LANGSMITH)
# ---------------------------------------------------------
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=agency-ai-orchestrator

# ---------------------------------------------------------
# DATABASE (SUPABASE / POSTGRESQL)
# ---------------------------------------------------------
SUPABASE_URL=https://your_project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_DB_URL=postgresql+asyncpg://user:password@aws-0-region.pooler.supabase.com:6543/postgres
PASSWORD_SUPABASE=your_database_password
PROJECT_ID=your_supabase_project_id  # This is the Supabase Project ID read by the application
```

## Quick Start (Local)

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Database Migration:**
   Apply the Alembic migrations to build your database schema in Supabase before running the app. If this is skipped, the app will crash upon saving data.
   ```bash
   alembic upgrade head
   ```
3. **Start the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Manual Testing

Once the application is running locally (e.g., at `http://localhost:8000`), you can immediately test the Webhook endpoints via `cURL` without needing Swagger. Make sure to replace `your_telegram_bot_token` with your actual token from the `.env` file.

**Test Auto-Lead Qualification:**
```bash
curl -X POST "http://localhost:8000/api/v1/webhooks/incoming-lead" \
     -H "Content-Type: application/json" \
     -H "X-Webhook-Signature: your_telegram_bot_token" \
     -d '{
           "sender_email": "client@example.com",
           "subject": "Need a new website",
           "body": "Hi, we are looking to build an e-commerce website with around 50 products. Our budget is approximately $10,000. Can we schedule a call?"
         }'
```

<hr>
<div align="center">
  <p><em>Built with Clean Architecture, SOLID Principles, and strict dependency injection. Production-ready.</em></p>
</div>
