# Lenny Growth Assistant

A full-stack AI assistant for exploring product and growth ideas from Lenny Rachitsky's podcast transcripts.

I built this as a Forward Deployed Engineer take-home. The goal was to make something useful for product and growth questions while keeping answers grounded in the underlying transcripts instead of relying on the model's general knowledge.

The app supports three main workflows:

* **Grounded Q&A** — ask product and growth questions and get answers with transcript sources.
* **Ship 30 for 30** — turn research into a roughly 1,250-word piece using Ship 30 writing principles.
* **Artifacts** — generate Markdown or HTML/CSS documents and view them directly inside the app.

## What I built

The application has a React frontend, FastAPI backend, PostgreSQL database, local transcript retrieval, and a model/provider layer that supports both Anthropic and Ollama.

The main flow looks like this:

```text
React UI
   ↓
FastAPI
   ↓
Agent / Skill Router
   ↓
Transcript Retrieval
   ↓
Lenny Podcast Knowledge Base
   ↓
Anthropic or Ollama
```

For grounded questions, the agent can call a transcript-search tool and use the retrieved chunks as evidence. Sources are returned with the response so the user can see where the answer came from.

## Features

### Grounded Q&A

Ask questions such as:

> How should an early-stage startup improve retention?

The assistant searches the Lenny transcript knowledge base, uses relevant passages to form the answer, and shows the supporting episodes.

If the knowledge base doesn't contain enough information to answer confidently, the assistant is instructed to say so instead of making up an answer.

Follow-up questions keep the context of the current conversation.

### Ship 30 for 30

The assistant has a separate writing workflow for turning transcript research into a longer piece.

The skill is designed around Ship 30 for 30 principles, including:

* A strong opening
* A clear narrative
* Useful takeaways
* Skimmable sections
* Selective emphasis
* Grounding claims in Lenny's content

The target length is approximately 1,250 words.

### Artifacts

The assistant can generate reusable documents and small web artifacts.

Supported output includes:

* Markdown
* HTML/CSS

Generated artifacts open in an **Artifact Viewer** next to the conversation rather than being dumped into the chat as a large block of code.

Generated HTML is treated as untrusted content and is isolated/sanitized before being displayed.

### Conversations

Each conversation has its own session and message history.

The application supports:

* Creating conversations
* Switching between conversations
* Deleting conversations
* Continuing previous conversations
* Persisting messages and generated artifacts

## Tech stack

**Frontend**

* React
* TypeScript
* Vite
* Tailwind CSS
* React Query

**Backend**

* FastAPI
* Python 3.11
* SQLAlchemy
* Alembic
* Pydantic

**Database**

* PostgreSQL 15

**Agent**

* Anthropic Claude Agent SDK
* Custom retrieval tool for transcript search

**Retrieval**

* Sentence Transformers
* FAISS
* PostgreSQL metadata/storage

**Models**

* Anthropic Claude
* Ollama
* `llama3.2:3b` for the local demo

## Running locally

### Prerequisites

You will need:

* Docker Desktop
* Git
* Ollama if you want to run the local model

An Anthropic API key is optional if you want to use Claude instead of Ollama.

### 1. Clone the repository

```bash
git clone https://github.com/shahulgithub1/lenny-growth-assistant.git
cd lenny-growth-assistant
```

### 2. Configure the environment

Copy the example environment file:

```bash
cp .env.example .env
```

For a local Ollama setup, the important settings are:

```env
MODEL_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2:3b
```

If you want to use Anthropic instead:

```env
MODEL_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 3. Set up Ollama

Install Ollama and start it.

Then pull the model:

```bash
ollama pull llama3.2:3b
```

The backend runs inside Docker, so it connects to Ollama on the host through:

```text
host.docker.internal:11434
```

### 4. Start the application

```bash
./start.sh
```

The application starts the required Docker services.

Open:

* Frontend: http://localhost:5173
* Backend: http://localhost:8000
* API docs: http://localhost:8000/docs

## Transcript knowledge base

The transcript repository used by the application is:

`https://github.com/ChatPRD/lennys-podcast-transcripts`

The ingestion pipeline:

1. Downloads the transcript repository.
2. Parses the transcript metadata.
3. Splits transcripts into overlapping chunks.
4. Generates embeddings using Sentence Transformers.
5. Builds a FAISS index.
6. Stores transcript chunks and metadata in PostgreSQL.
7. Keeps metadata that allows retrieved content to be traced back to the original episode.

The current knowledge base contains more than 10,000 transcript chunks from the ingested podcast library.

The ingestion process can be run again when the source transcript repository changes.

## Provider setup

The application separates model configuration from application logic.

The provider can be changed through environment variables rather than changing the application code.

### Ollama

Useful for the local/demo setup:

```env
MODEL_PROVIDER=ollama
OLLAMA_MODEL=llama3.2:3b
```

### Anthropic

Used with the Claude Agent SDK and retrieval tool:

```env
MODEL_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

The active provider and model are shown in the application UI.

One of the trade-offs here is that the smaller local model is convenient for a fully local demo, but generally produces weaker responses than a larger cloud model. Keeping retrieval separate from generation means the same knowledge base can be used with either provider.

## Project structure

```text
lenny-growth-assistant/
├── agent-transcripts/       # Agent development notes/transcripts
├── backend/                 # FastAPI application
│   ├── app/
│   ├── migrations/
│   └── tests/
├── frontend/                # React application
├── ingestion/               # Transcript ingestion pipeline
├── tests/                   # Additional test material
├── PRD.md                   # Product requirements
├── architecture.md          # Technical architecture
├── design.md                # UI/UX decisions
├── docker-compose.yml
├── start.sh
├── .env.example
└── README.md
```

## Testing

Backend tests can be run with:

```bash
docker compose exec backend pytest tests/ -v
```

The project includes tests covering:

* API endpoints
* Session handling
* Retrieval
* Hybrid retrieval
* Grounding behavior
* Agent behavior
* LLM providers
* Artifact generation
* Artifact API behavior
* Metadata quality
* Health checks

The frontend TypeScript code can be checked with:

```bash
cd frontend
npx tsc --noEmit
```

## Design decisions

A few decisions were intentional.

**Retrieval is kept separate from generation.**

The transcript search layer is deterministic and provider-independent. This makes it possible to switch between Anthropic and Ollama without rebuilding the knowledge base.

**The agent gets a retrieval tool rather than receiving the entire transcript collection.**

This keeps the context focused and gives the agent an explicit way to retrieve evidence when answering a question.

**Artifacts are treated as untrusted content.**

Generated HTML is isolated from the main application rather than being inserted directly into the React DOM.

**The local model is a first-class provider.**

Ollama provides a way to demonstrate the complete application without requiring a cloud model for every interaction.

## Documentation

* [PRD](PRD.md) — product requirements and scope decisions
* [Architecture](architecture.md) — system architecture and technical decisions
* [Design](design.md) — UI/UX decisions
* [Quick Start](QUICK_START.md) — setup and demo instructions
* [Ingestion Report](INGESTION_REPORT.md) — transcript ingestion details
* [Implementation Reports](PHASES_5_6_7_REPORT.md) — implementation history
* [Verification Steps](VERIFICATION_STEPS.md) — verification and testing notes

## Demo

The intended demo flow is:

1. Ask a grounded product/growth question and show the sources.
2. Ask a follow-up question to demonstrate conversation context.
3. Ask an unsupported question and show the assistant declining to invent an answer.
4. Generate a Ship 30 article.
5. Generate an artifact and open it in the Artifact Viewer.
6. Switch to the local Ollama model and explain the provider architecture.

The full demo is designed to fit into roughly 2–3 minutes.

## Assignment

This project was built for the **Forward Deployed Engineer take-home assignment**.

The repository includes the requested product requirements, architecture/design documentation, agent development notes, automated tests, local deployment setup, and demo workflow.

---

Built with React, FastAPI, PostgreSQL, FAISS, Claude, and Ollama.
