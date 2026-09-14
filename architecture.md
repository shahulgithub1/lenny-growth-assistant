# Architecture Document: The Lenny Growth Assistant

## Executive Summary

The Lenny Growth Assistant is a full-stack AI application with a clean three-tier architecture: React frontend, FastAPI backend, and PostgreSQL database, enhanced with an agent layer for intelligent task routing. The system prioritizes **reliability, simplicity, and security** over architectural complexity.

**Key Architectural Decisions:**
- **Agent Framework**: Anthropic Claude SDK (cleaner implementation, better Anthropic integration)
- **Retrieval**: Sentence-transformers + FAISS (local, no external dependencies)
- **Model Abstraction**: Provider pattern with Ollama and Anthropic implementations
- **Artifact Security**: Sandboxed iframe with CSP + HTML sanitization
- **Deployment**: Docker Compose (single-command local deployment)

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [System Components](#system-components)
3. [Data Flow](#data-flow)
4. [Database Schema](#database-schema)
5. [API Design](#api-design)
6. [Agent Architecture](#agent-architecture)
7. [RAG Pipeline](#rag-pipeline)
8. [Model Provider Abstraction](#model-provider-abstraction)
9. [Artifact Security](#artifact-security)
10. [Deployment Architecture](#deployment-architecture)
11. [Observability](#observability)
12. [Security](#security)
13. [Trade-offs and Decisions](#trade-offs-and-decisions)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │          React Frontend (Vite)                          │    │
│  │  - Session UI    - Chat Interface   - Artifact Viewer  │    │
│  │  - State Management  - API Client   - Routing          │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                         HTTP/REST
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐        │
│  │   API Layer  │  │ Agent Router │  │  LLM Provider │        │
│  │  (FastAPI)   │  │  (Anthropic  │  │  Abstraction  │        │
│  │              │  │    SDK)      │  │               │        │
│  └──────────────┘  └──────────────┘  └───────────────┘        │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐        │
│  │  RAG System  │  │   Skills:    │  │  Persistence  │        │
│  │  - Retrieval │  │  - Grounded  │  │    Layer      │        │
│  │  - Indexing  │  │  - Ship30    │  │  (SQLAlchemy) │        │
│  │              │  │  - Artifacts │  │               │        │
│  └──────────────┘  └──────────────┘  └───────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                         PostgreSQL
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    PostgreSQL Database                           │
│  - Sessions   - Messages   - Artifacts   - TranscriptChunks     │
└─────────────────────────────────────────────────────────────────┘

              External Dependencies (Optional/Local)
┌─────────────────────────┐       ┌──────────────────────┐
│    Ollama (Local LLM)   │       │  Anthropic API       │
│    - llama3.2:3b        │       │  - Claude Sonnet     │
│    - Port 11434         │       │  (Optional)          │
└─────────────────────────┘       └──────────────────────┘
```

---

## System Components

### 1. Frontend (React + Vite)

**Technology**: React 18, Vite, TailwindCSS, React Query

**Responsibilities**:
- Render conversational UI
- Manage session state
- Display messages with source citations
- Render artifact viewer (sandboxed)
- Handle user input and validation
- Communicate with backend API
- Display loading/error states

**Key Components**:
- `SessionSidebar`: Session list, New Chat button
- `ConversationArea`: Message list, composer
- `MessageBubble`: Individual message with role/content
- `SourceCard`: Citation display with metadata
- `ArtifactViewer`: Sandboxed iframe renderer
- `ModelIndicator`: Current provider/model display
- `EmptyState`: Welcome screen with example prompts

**State Management**: React Query for server state, Context API for UI state

**Why React + Vite**:
- Vite: Fast dev server, simpler than Next.js for local demo
- React: Industry standard, excellent component ecosystem
- TailwindCSS: Rapid UI development with consistent design system
- No SSR needed for local demo

### 2. Backend (FastAPI)

**Technology**: FastAPI, Python 3.11+, Pydantic, SQLAlchemy

**Responsibilities**:
- Expose REST API
- Validate requests (Pydantic schemas)
- Route to agent
- Persist sessions/messages/artifacts
- Manage database connections
- Handle errors gracefully
- Structured logging

**Key Modules**:
- `api/routes/`: API endpoints (sessions, messages, health, artifacts)
- `api/schemas/`: Pydantic request/response models
- `services/agent_service.py`: Agent interaction
- `services/retrieval_service.py`: RAG system
- `services/llm_service.py`: Model provider abstraction
- `db/models.py`: SQLAlchemy models
- `db/migrations/`: Alembic migrations
- `core/config.py`: Environment configuration
- `core/logging.py`: Structured logging setup

**Why FastAPI**:
- Modern async Python framework
- Automatic OpenAPI docs
- Pydantic validation built-in
- Fast and type-safe
- Excellent for AI/ML services

### 3. Agent Layer (Anthropic Claude SDK)

**Technology**: Anthropic Claude SDK (Python), custom skill implementations

**Responsibilities**:
- Understand user intent
- Route to appropriate skill
- Maintain conversation context
- Generate responses
- Extract source citations
- Handle insufficient evidence

**Skills**:
1. **Grounded Q&A Skill**: Answer questions using retrieved transcripts
2. **Ship 30 Skill**: Transform insights into Ship 30 for 30 essays
3. **Artifact Skill**: Generate Markdown/HTML/CSS artifacts

**Agent Decision**: Anthropic Claude SDK

**Rationale**:
- Official SDK with better stability
- Cleaner integration with Anthropic API
- Good documentation and examples
- Tool/function calling built-in
- Natural fit since Anthropic is primary cloud provider

**Alternative Considered**: Pi Coding Agent
- Less mature ecosystem
- Fewer examples for RAG integration
- Would require custom routing logic

### 4. Database (PostgreSQL)

**Technology**: PostgreSQL 15, SQLAlchemy ORM, Alembic migrations

**Responsibilities**:
- Persist sessions, messages, artifacts
- Store transcript chunks and embeddings
- Maintain data integrity
- Support concurrent access

**Why PostgreSQL**:
- Robust, production-grade
- Excellent JSON support (artifact metadata)
- pgvector extension for embeddings (optional)
- Strong Docker support
- Familiar to most engineers

### 5. RAG System

**Technology**: sentence-transformers, FAISS, NumPy

**Responsibilities**:
- Index transcript chunks
- Generate embeddings
- Retrieve relevant chunks
- Preserve source metadata

**Why This Approach**:
- **sentence-transformers**: State-of-art embeddings, runs locally
- **FAISS**: Fast similarity search, no external service
- **Local**: No OpenAI/Anthropic embedding API calls
- **Simple**: No complex hybrid search or reranking

**Alternative Considered**: 
- OpenAI embeddings + vector database (Pinecone/Weaviate)
  - ❌ External dependency, costs money
- Hybrid search (BM25 + semantic)
  - ❌ Overkill for demo, adds complexity

---

## Data Flow

### Flow 1: Grounded Question Answering

```
1. User types question
   ↓
2. Frontend sends POST /api/sessions/{session_id}/messages
   ↓
3. Backend validates request (Pydantic)
   ↓
4. Backend retrieves conversation history (PostgreSQL)
   ↓
5. Backend calls retrieval service
   - Generate query embedding
   - FAISS similarity search
   - Return top-K transcript chunks with metadata
   ↓
6. Backend calls agent service
   - Pass user question + conversation history + retrieved chunks
   - Agent generates grounded response
   - Extract source citations
   ↓
7. Backend persists assistant message (PostgreSQL)
   ↓
8. Backend returns response with sources
   ↓
9. Frontend displays message + source cards
```

### Flow 2: Ship 30 Essay Generation

```
1. User requests: "Turn this into a Ship 30 essay"
   ↓
2. Backend detects intent (Ship 30 keywords)
   ↓
3. Agent routes to Ship 30 skill
   - Extract key insights from conversation
   - Apply Ship 30 writing principles
   - Generate ~1,250 word essay
   ↓
4. Backend returns formatted essay
   ↓
5. Frontend renders essay (Markdown or plain text with formatting)
```

### Flow 3: Artifact Generation

```
1. User requests artifact (e.g., "Create a dashboard")
   ↓
2. Backend detects artifact intent
   ↓
3. Agent routes to Artifact skill
   - Determine artifact type (Markdown/HTML/CSS)
   - Generate content
   - Return structured artifact
   ↓
4. Backend persists artifact (PostgreSQL)
   ↓
5. Backend returns artifact metadata + content
   ↓
6. Frontend opens Artifact Viewer
   - Render in sandboxed iframe (HTML)
   - Render with Markdown library (Markdown)
```

### Flow 4: Session Creation

```
1. User clicks "New Chat"
   ↓
2. Frontend sends POST /api/sessions
   ↓
3. Backend creates session (UUID, timestamp)
   ↓
4. Backend persists to PostgreSQL
   ↓
5. Backend returns session_id
   ↓
6. Frontend updates sidebar, switches to new session
```

---

## Database Schema

### Sessions Table

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    title VARCHAR(255),  -- Optional: first message preview
    metadata JSONB       -- Optional: user preferences, model config
);

CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);
```

### Messages Table

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,  -- 'user' | 'assistant'
    content TEXT NOT NULL,
    sources JSONB,              -- Array of source citations
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB              -- model_provider, model_name, token_count, etc.
);

CREATE INDEX idx_messages_session_id ON messages(session_id, created_at);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
```

**Sources JSONB Structure**:
```json
[
  {
    "episode_title": "Building Product Sense with Jules Walter",
    "guest": "Jules Walter",
    "excerpt": "Product sense is...",
    "chunk_id": "uuid-here",
    "source_file": "episode_123_transcript.txt"
  }
]
```

### Artifacts Table

```sql
CREATE TABLE artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    message_id UUID REFERENCES messages(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL,  -- 'markdown' | 'html' | 'css'
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB              -- title, description, size, etc.
);

CREATE INDEX idx_artifacts_session_id ON artifacts(session_id);
CREATE INDEX idx_artifacts_message_id ON artifacts(message_id);
```

### Transcript Chunks Table

```sql
CREATE TABLE transcript_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    episode_title VARCHAR(500),
    guest VARCHAR(255),
    source_file VARCHAR(500) NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384),      -- For pgvector, or store separately
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB              -- url, timestamp, speaker, etc.
);

CREATE INDEX idx_transcript_chunks_source_file ON transcript_chunks(source_file);
CREATE INDEX idx_transcript_chunks_episode_title ON transcript_chunks(episode_title);

-- If using pgvector:
-- CREATE INDEX idx_transcript_chunks_embedding ON transcript_chunks USING ivfflat (embedding vector_cosine_ops);
```

**Note**: Embedding storage strategy:
- **Option A**: Store in PostgreSQL with pgvector extension
- **Option B**: Store separately in FAISS index file, reference by chunk UUID
- **Decision**: Use Option B (FAISS index file) to avoid pgvector dependency, keep setup simpler

### Migrations

Use Alembic for database migrations:

```
backend/
  migrations/
    versions/
      001_create_sessions.py
      002_create_messages.py
      003_create_artifacts.py
      004_create_transcript_chunks.py
```

---

## API Design

### Base URL

```
http://localhost:8000/api
```

### Endpoints

#### Health Check

```http
GET /health

Response 200:
{
  "status": "healthy",
  "database": "connected",
  "ollama": "connected",  // or "unavailable"
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Create Session

```http
POST /api/sessions

Response 201:
{
  "id": "uuid-here",
  "created_at": "2024-01-15T10:30:00Z",
  "title": null,
  "metadata": {}
}
```

#### List Sessions

```http
GET /api/sessions?limit=50&offset=0

Response 200:
{
  "sessions": [
    {
      "id": "uuid-here",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z",
      "title": "How to improve retention?",
      "message_count": 5
    }
  ],
  "total": 100,
  "limit": 50,
  "offset": 0
}
```

#### Get Session

```http
GET /api/sessions/{session_id}

Response 200:
{
  "id": "uuid-here",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "title": "How to improve retention?",
  "messages": [
    {
      "id": "msg-uuid",
      "role": "user",
      "content": "How should a startup improve retention?",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "msg-uuid-2",
      "role": "assistant",
      "content": "Based on Lenny's podcast...",
      "sources": [...],
      "created_at": "2024-01-15T10:30:15Z",
      "metadata": {
        "model_provider": "ollama",
        "model_name": "llama3.2:8b"
      }
    }
  ]
}
```

#### Send Message

```http
POST /api/sessions/{session_id}/messages

Request:
{
  "content": "How should a startup improve retention?",
  "model_provider": "ollama"  // optional, defaults to env config
}

Response 200:
{
  "id": "msg-uuid",
  "role": "assistant",
  "content": "Based on Lenny's podcast...",
  "sources": [
    {
      "episode_title": "Retention Strategies",
      "guest": "Casey Winters",
      "excerpt": "The key to retention is...",
      "chunk_id": "chunk-uuid",
      "source_file": "episode_045.txt"
    }
  ],
  "created_at": "2024-01-15T10:30:15Z",
  "metadata": {
    "model_provider": "ollama",
    "model_name": "llama3.2:8b",
    "retrieval_count": 5,
    "generation_time_ms": 8500
  }
}

Error 400:
{
  "error": "validation_error",
  "message": "Content is required",
  "details": {...}
}

Error 500:
{
  "error": "llm_unavailable",
  "message": "Unable to connect to Ollama. Please ensure Ollama is running.",
  "details": {
    "provider": "ollama",
    "model": "llama3.2:8b"
  }
}
```

#### Get Artifact

```http
GET /api/artifacts/{artifact_id}

Response 200:
{
  "id": "artifact-uuid",
  "session_id": "session-uuid",
  "type": "html",
  "content": "<html>...</html>",
  "created_at": "2024-01-15T10:35:00Z",
  "metadata": {
    "title": "Growth Strategy Dashboard",
    "description": "Interactive dashboard",
    "size_bytes": 5432
  }
}
```

#### Get Model Config

```http
GET /api/config/models

Response 200:
{
  "current_provider": "ollama",
  "current_model": "llama3.2:8b",
  "available_providers": [
    {
      "name": "ollama",
      "status": "available",
      "models": ["llama3.2:8b", "mistral:7b"]
    },
    {
      "name": "anthropic",
      "status": "configured",  // or "unavailable" if no API key
      "models": ["claude-3-5-sonnet-20241022"]
    }
  ]
}
```

### Request Validation

All requests validated with Pydantic schemas:

```python
# Example schemas
class MessageCreateRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    model_provider: Optional[str] = None

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    sources: Optional[List[Source]] = []
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = {}

class Source(BaseModel):
    episode_title: str
    guest: Optional[str]
    excerpt: str
    chunk_id: UUID
    source_file: str
```

### Error Handling

Structured error responses:

```python
{
  "error": "error_code",        # machine-readable
  "message": "Human message",   # user-friendly
  "details": {...},             # optional debug info
  "request_id": "uuid"          # for log correlation
}
```

Common error codes:
- `validation_error`: Invalid request
- `llm_unavailable`: LLM service down
- `database_error`: Database connection failed
- `not_found`: Resource not found
- `internal_error`: Unexpected error

---

## Agent Architecture

### Overview

The agent uses **Anthropic Claude SDK** with a skill-based routing system.

### Agent Flow

```
User Message
    ↓
Intent Detection
    ↓
┌───────────────┐
│ Router Logic  │
└───────────────┘
    ↓
    ├─→ Grounded Q&A Skill ────→ Retrieval → Generate → Cite
    ├─→ Ship 30 Skill ─────────→ Extract Context → Generate Essay
    └─→ Artifact Skill ────────→ Generate Markdown/HTML/CSS
```

### Skill Definitions

#### 1. Grounded Q&A Skill

**Trigger**: Default for questions about product/growth

**Process**:
1. Receive user question + conversation history
2. Generate query embedding
3. Retrieve top-K transcript chunks (K=5)
4. Pass chunks + question to LLM with system prompt:
   ```
   You are a research assistant specializing in product and growth strategy.
   Answer the user's question using ONLY the provided transcript excerpts.
   If the transcripts don't contain sufficient information, explicitly say so.
   Always cite your sources.
   ```
5. Extract source citations from response
6. Return structured response

**Output**:
```python
{
  "content": "Based on Lenny's conversation with Casey Winters...",
  "sources": [
    {
      "episode_title": "...",
      "guest": "...",
      "excerpt": "...",
      "chunk_id": "..."
    }
  ],
  "confidence": "high" | "medium" | "low" | "insufficient"
}
```

#### 2. Ship 30 for 30 Skill

**Trigger**: Keywords like "Ship 30", "essay", "write article"

**Process**:
1. Extract key insights from current conversation
2. Retrieve additional context if needed
3. Apply Ship 30 writing principles:
   - Strong hook (first 2 sentences)
   - Clear narrative arc
   - Skimmable formatting (bullets, short paragraphs)
   - Strategic bold emphasis
   - Specific, actionable takeaways
   - ~1,250 words
4. Generate essay grounded in sources
5. Format with Markdown

**System Prompt**:
```
You are an expert Ship 30 for 30 writer. Transform the conversation into a 1,250-word essay following these principles:

1. Hook: Open with a compelling hook that makes the reader curious
2. Narrative: Tell a story, don't just list facts
3. Skimmable: Use bullets, short paragraphs, white space
4. Emphasis: Bold 3-5 key phrases for scanning
5. Takeaway: End with a specific, actionable insight

Ground all claims in the provided sources. Cite episodes when relevant.
```

**Output**:
```python
{
  "content": "# How Top Startups Build Retention\n\n...",
  "type": "ship30_essay",
  "word_count": 1247,
  "sources_used": [...]
}
```

#### 3. Artifact Skill

**Trigger**: Keywords like "create", "generate", "build" + "dashboard", "framework", "template"

**Process**:
1. Determine artifact type (Markdown/HTML)
2. Extract context from conversation
3. Generate structured content
4. Validate output format
5. Return artifact

**System Prompt**:
```
You are a skilled designer creating artifacts for product teams.
Generate {artifact_type} based on the conversation context.

For HTML artifacts:
- Use semantic HTML5
- Include inline CSS for styling
- Create responsive layouts
- Use professional design (whitespace, typography, color)
- NO external scripts or links
- NO forms that submit data
- NO JavaScript

Output ONLY the artifact content, no explanation.
```

**Output**:
```python
{
  "type": "html" | "markdown",
  "content": "...",
  "metadata": {
    "title": "...",
    "description": "..."
  }
}
```

### Routing Logic

```python
def route_message(message: str, conversation_history: List[Message]) -> str:
    """Determine which skill to use"""
    
    # Ship 30 triggers
    if any(keyword in message.lower() for keyword in 
           ["ship 30", "essay", "write article", "blog post"]):
        return "ship30"
    
    # Artifact triggers
    if any(keyword in message.lower() for keyword in 
           ["create", "generate", "build"]) and \
       any(artifact in message.lower() for artifact in 
           ["dashboard", "framework", "template", "document"]):
        return "artifact"
    
    # Default to grounded Q&A
    return "grounded_qa"
```

### Context Management

**Session Context Window**:
- Store full conversation history in database
- Pass last N messages to LLM (N=10 for context)
- Include retrieved chunks for grounded Q&A
- Token budget: ~4000 tokens for context, ~2000 for generation

**Context Structure**:
```python
[
  {"role": "system", "content": "You are..."},
  {"role": "user", "content": "How to improve retention?"},
  {"role": "assistant", "content": "Based on..."},
  {"role": "user", "content": "What should we do first?"},
  # Retrieved chunks as context
  {"role": "system", "content": "Relevant excerpts:\n[chunks]"}
]
```

---

## RAG Pipeline

### Ingestion Pipeline

```
Lenny Transcript Repo (GitHub)
    ↓
Clone/Download
    ↓
Load Transcript Files (.txt, .md)
    ↓
Clean & Parse
  - Remove timestamps
  - Extract metadata (episode title, guest)
  - Normalize whitespace
    ↓
Chunk Text
  - Strategy: Sliding window
  - Chunk size: 500 tokens (~750 words)
  - Overlap: 50 tokens
  - Preserve sentence boundaries
    ↓
Generate Embeddings
  - Model: sentence-transformers/all-MiniLM-L6-v2
  - Dimension: 384
  - Batch size: 32
    ↓
Store Chunks in PostgreSQL
Store Embeddings in FAISS Index
    ↓
Save FAISS Index to Disk
```

### Retrieval Pipeline

```
User Question
    ↓
Generate Query Embedding
  - Same model as ingestion
  - Dimension: 384
    ↓
FAISS Similarity Search
  - Metric: Cosine similarity
  - Top-K: 5 chunks
  - Threshold: 0.7 (configurable)
    ↓
Fetch Chunk Metadata from PostgreSQL
  - Episode title, guest, content
    ↓
Return Ranked Chunks with Sources
```

### Chunking Strategy

**Why Sliding Window with Overlap**:
- Preserves context across chunk boundaries
- Prevents splitting mid-sentence or mid-thought
- Handles long episodes gracefully

**Parameters**:
```python
CHUNK_SIZE = 500  # tokens
OVERLAP = 50      # tokens
MIN_CHUNK_SIZE = 100  # tokens (avoid tiny chunks)
```

**Metadata Preserved**:
- Episode title
- Guest name(s)
- Source filename
- Chunk index
- Transcript URL (if available)
- Timestamp (if available)

### Embedding Model

**Model**: `sentence-transformers/all-MiniLM-L6-v2`

**Why This Model**:
- ✅ Lightweight (80MB)
- ✅ Fast inference
- ✅ Good quality for retrieval
- ✅ Runs locally (no API calls)
- ✅ 384-dimensional embeddings (efficient)

**Alternative Considered**:
- `text-embedding-3-small` (OpenAI)
  - ❌ Requires API calls, costs money
- `all-mpnet-base-v2`
  - ❌ Larger (420MB), slower, marginal quality gain

### FAISS Index

**Index Type**: `IndexFlatL2` or `IndexFlatIP` (cosine similarity)

**Why FAISS**:
- ✅ Fast similarity search
- ✅ Runs locally
- ✅ Mature, well-tested
- ✅ Easy to serialize/load

**Storage**:
```
backend/data/
  faiss_index.bin       # FAISS index
  chunk_mapping.json    # chunk_id → metadata mapping
```

### Retrieval Quality

**Evaluation Strategy**:
- Manual test queries with known answers
- Verify top-K contains relevant content
- Adjust K and similarity threshold based on results

**Example Test Queries**:
- "How to improve user retention?"
- "What is product-market fit?"
- "How to prioritize features?"

---

## Model Provider Abstraction

### Provider Interface

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate completion from messages"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get current model name"""
        pass
```

### Ollama Provider

```python
class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url  # http://localhost:11434
        self.model = model         # llama3.2:8b
        self.client = OllamaClient(base_url)
    
    def generate(self, messages, max_tokens=2000, temperature=0.7, **kwargs):
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            )
            return {
                "content": response["message"]["content"],
                "model": self.model,
                "provider": "ollama"
            }
        except ConnectionError:
            raise LLMUnavailableError("Ollama is not running")
    
    def is_available(self) -> bool:
        try:
            self.client.list()
            return True
        except:
            return False
    
    def get_model_name(self) -> str:
        return self.model
```

### Anthropic Provider

```python
class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model  # claude-3-5-sonnet-20241022
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, messages, max_tokens=2000, temperature=0.7, **kwargs):
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )
            return {
                "content": response.content[0].text,
                "model": self.model,
                "provider": "anthropic",
                "usage": response.usage
            }
        except anthropic.AuthenticationError:
            raise LLMAuthError("Invalid Anthropic API key")
        except anthropic.APIConnectionError:
            raise LLMUnavailableError("Cannot connect to Anthropic API")
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_model_name(self) -> str:
        return self.model
```

### Provider Factory

```python
def get_llm_provider(config: AppConfig) -> LLMProvider:
    """Factory function to get LLM provider"""
    
    provider_name = config.MODEL_PROVIDER.lower()
    
    if provider_name == "ollama":
        return OllamaProvider(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL
        )
    elif provider_name == "anthropic":
        if not config.ANTHROPIC_API_KEY:
            raise ConfigError("ANTHROPIC_API_KEY not set")
        return AnthropicProvider(
            api_key=config.ANTHROPIC_API_KEY,
            model=config.ANTHROPIC_MODEL
        )
    else:
        raise ConfigError(f"Unknown provider: {provider_name}")
```

### Configuration

```python
# .env
MODEL_PROVIDER=ollama  # or anthropic

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Anthropic (optional)
ANTHROPIC_API_KEY=your-anthropic-api-key-here  # optional
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

---

## Artifact Security

### Threat Model

**Threats**:
1. **XSS (Cross-Site Scripting)**: Malicious HTML injects scripts that steal cookies, access localStorage, or manipulate parent frame
2. **Frame Busting**: Artifact attempts to break out of iframe
3. **Clickjacking**: Artifact overlays UI elements to trick user
4. **Data Exfiltration**: Artifact sends data to external servers
5. **Resource Abuse**: Artifact consumes excessive CPU/memory

### Defense Strategy: Defense in Depth

#### Layer 1: Sandboxed Iframe

```html
<iframe
  sandbox="allow-same-origin"
  srcDoc={artifactHTML}
  style="width: 100%; height: 100%; border: none;"
  title="Artifact Viewer"
/>
```

**Sandbox Attributes**:
- `allow-same-origin`: Allow CSS/styling (required for rendering)
- **NO** `allow-scripts`: JavaScript disabled
- **NO** `allow-forms`: Forms disabled
- **NO** `allow-top-navigation`: Cannot navigate parent
- **NO** `allow-popups`: Popups blocked

**Why This Works**:
- Iframe sandbox is browser-enforced
- Even if HTML contains `<script>`, it won't execute
- Cannot access parent window, cookies, localStorage

#### Layer 2: Content Security Policy

```http
Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; img-src data:;
```

**Policy**:
- `default-src 'none'`: Block all external resources
- `style-src 'unsafe-inline'`: Allow inline CSS (needed for generated HTML)
- `img-src data:`: Allow data URIs for images (optional)
- **NO** `script-src`: JavaScript blocked
- **NO** external fonts, stylesheets, or scripts

#### Layer 3: HTML Sanitization (Secondary Defense)

Use `DOMPurify` or `bleach` to sanitize HTML before rendering:

```python
import bleach

ALLOWED_TAGS = [
    'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'thead', 'tbody',
    'strong', 'em', 'b', 'i', 'u', 'br', 'hr',
    'a', 'img'
]

ALLOWED_ATTRS = {
    '*': ['class', 'id', 'style'],
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title']
}

def sanitize_html(html: str) -> str:
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True
    )
```

**Why Sanitization is Secondary**:
- Sandbox is primary defense (browser-enforced)
- Sanitization is defense-in-depth (catches bugs)
- Easier to maintain whitelist than blacklist

#### Layer 4: Frontend Validation

```typescript
function renderArtifact(artifact: Artifact) {
  // Validate artifact type
  if (!['html', 'markdown'].includes(artifact.type)) {
    throw new Error('Invalid artifact type');
  }
  
  // Check size
  if (artifact.content.length > 1_000_000) {
    throw new Error('Artifact too large');
  }
  
  // Render in sandboxed iframe
  return <ArtifactViewer artifact={artifact} />;
}
```

### Security Model Summary

| Threat | Defense | Layer |
|--------|---------|-------|
| XSS | Sandboxed iframe (no scripts) | Primary |
| Frame busting | Sandbox (no top-navigation) | Primary |
| External resources | CSP (block external) | Primary |
| Form submission | Sandbox (no forms) | Primary |
| Malicious script tags | HTML sanitization | Secondary |
| Size-based DoS | Size validation | Secondary |
| Prompt injection | Input validation, clear prompts | Secondary |

### Permitted Artifact Capabilities

✅ **Allowed**:
- Inline CSS styling
- Semantic HTML structure
- Static images (data URIs)
- Tables, lists, divs
- Links (sanitized, no `javascript:` protocol)

❌ **Blocked**:
- JavaScript execution
- External script loading
- Form submission
- Frame navigation
- External network requests (XHR, fetch)
- WebSocket connections
- Local storage access
- Cookie access

### Known Limitations

1. **Sophisticated Prompt Injection**: An adversarial user could potentially craft prompts that bypass safety instructions. This is an inherent LLM limitation.
2. **CSS-based Attacks**: While rare, sophisticated CSS can potentially leak data (e.g., CSS exfiltration via background images). CSP mitigates this.
3. **Resource Consumption**: Large artifacts may consume browser memory. Size validation helps but isn't perfect.

---

## Deployment Architecture

### Local Development (Docker Compose)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: lenny
      POSTGRES_PASSWORD: lenny_dev_password
      POSTGRES_DB: lenny_growth_assistant
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U lenny"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://lenny:lenny_dev_password@postgres:5432/lenny_growth_assistant
      MODEL_PROVIDER: ollama
      OLLAMA_BASE_URL: http://host.docker.internal:11434
      OLLAMA_MODEL: llama3.2:3b
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - ./backend/data:/app/data  # FAISS index persistence

  frontend:
    build: ./frontend
    environment:
      VITE_API_URL: http://localhost:8000
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend

volumes:
  postgres_data:
```

**Startup**:
```bash
docker compose up
```

**Ollama**: Runs on host machine (not in Docker) to access GPU if available

### Directory Structure

```
lenny-growth-assistant/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api/
│   │   ├── hooks/
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── schemas/
│   │   ├── services/
│   │   │   ├── agent_service.py
│   │   │   ├── retrieval_service.py
│   │   │   └── llm_service.py
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── data/
│   │   ├── faiss_index.bin
│   │   └── chunk_mapping.json
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic.ini
│
├── ingestion/
│   ├── scripts/
│   │   └── ingest_transcripts.py
│   ├── data/
│   │   └── transcripts/ (cloned from GitHub)
│   └── requirements.txt
│
├── tests/
│   ├── api/
│   ├── retrieval/
│   ├── agent/
│   └── security/
│
├── agent-transcripts/
│   └── (development logs)
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── PRD.md
├── architecture.md
├── design.md
└── LICENSE
```

---

## Observability

### Structured Logging

**Format**: JSON logs with structured fields

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "message_created",
    session_id=session_id,
    message_id=message_id,
    role="assistant",
    model_provider="ollama",
    retrieval_count=5,
    generation_time_ms=8500
)
```

**Key Fields**:
- `timestamp`: ISO8601
- `level`: INFO, WARNING, ERROR
- `event`: event name (snake_case)
- `session_id`: UUID
- `request_id`: UUID (correlation)
- `user_id`: (if auth added)
- Additional context fields

### Log Examples

```json
{
  "timestamp": "2024-01-15T10:30:15Z",
  "level": "INFO",
  "event": "retrieval_completed",
  "session_id": "uuid-here",
  "request_id": "uuid-here",
  "query": "How to improve retention?",
  "chunks_retrieved": 5,
  "retrieval_time_ms": 150
}

{
  "timestamp": "2024-01-15T10:30:20Z",
  "level": "ERROR",
  "event": "llm_generation_failed",
  "session_id": "uuid-here",
  "request_id": "uuid-here",
  "provider": "ollama",
  "model": "llama3.2:8b",
  "error": "ConnectionError: Connection refused",
  "retry_attempt": 1
}
```

### Health Endpoint

```http
GET /health

Response 200 (Healthy):
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "checks": {
    "database": "connected",
    "ollama": "connected",
    "faiss_index": "loaded"
  },
  "version": "1.0.0"
}

Response 503 (Unhealthy):
{
  "status": "unhealthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "checks": {
    "database": "connected",
    "ollama": "unavailable",
    "faiss_index": "loaded"
  },
  "version": "1.0.0"
}
```

### Metrics (Optional)

If time permits, track:
- Request count by endpoint
- Response latency (P50, P95, P99)
- LLM generation time
- Retrieval time
- Error rate by type
- Active sessions

Use Prometheus format for potential future integration.

---

## Security

### Authentication & Authorization

**Current Scope**: Single-user local deployment, no auth required

**Future Consideration**: If multi-user:
- JWT-based auth
- Session-based access control
- User ID on all database records

### Input Validation

- Pydantic schemas validate all API inputs
- Length limits on user messages (max 10,000 chars)
- Session ID format validation (UUID)
- Artifact size limits (1MB max)

### SQL Injection Prevention

- Use SQLAlchemy ORM (parameterized queries)
- Never construct SQL strings with user input
- All queries use bound parameters

### XSS Prevention

- Artifact sandboxing (detailed above)
- Markdown rendering with `react-markdown` (safe by default)
- CSP headers on frontend

### Secrets Management

- Never commit secrets to git
- .env.example with placeholders
- .gitignore includes .env, *.key, *.pem
- Environment variables for all secrets
- No secrets in logs

### CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**: Restrict to specific domain

### Rate Limiting

**Current Scope**: Not implemented (single-user)

**Future Consideration**: 
- FastAPI rate limiting middleware
- Per-session limits

---

## Trade-offs and Decisions

### Decision 1: Anthropic Claude SDK vs. Pi Coding Agent

**Choice**: Anthropic Claude SDK

**Rationale**:
- ✅ Official SDK, more stable
- ✅ Better documentation
- ✅ Natural fit with Anthropic as cloud provider
- ✅ Tool/function calling built-in
- ❌ Pi Agent is less mature, fewer examples

**Trade-off**: Less flexibility than custom agent, but more reliability

---

### Decision 2: sentence-transformers + FAISS vs. Vector Database

**Choice**: sentence-transformers + FAISS

**Rationale**:
- ✅ Runs completely locally
- ✅ No external dependencies
- ✅ Fast and reliable
- ✅ Easy to serialize/version control
- ❌ No built-in hybrid search
- ❌ No query analytics

**Trade-off**: Less sophisticated than Pinecone/Weaviate, but simpler and more reliable for demo

---

### Decision 3: React + Vite vs. Next.js

**Choice**: React + Vite

**Rationale**:
- ✅ Faster dev server
- ✅ Simpler config
- ✅ No SSR complexity
- ✅ Perfect for local SPA
- ❌ No built-in routing (use React Router if needed)

**Trade-off**: No SEO benefits, but not needed for local demo

---

### Decision 4: PostgreSQL Only vs. PostgreSQL + Redis

**Choice**: PostgreSQL only

**Rationale**:
- ✅ One less service to manage
- ✅ PostgreSQL fast enough for single-user
- ✅ Simpler Docker Compose
- ❌ No caching layer

**Trade-off**: Slight latency increase, but acceptable for demo

---

### Decision 5: Sandboxed Iframe vs. HTML Sanitization Only

**Choice**: Sandboxed iframe as primary, sanitization as secondary

**Rationale**:
- ✅ Browser-enforced security
- ✅ Defense in depth
- ✅ Blocks JavaScript completely
- ❌ More complex than sanitization alone

**Trade-off**: Slightly more complex implementation, but significantly more secure

---

### Decision 6: Ollama on Host vs. Ollama in Docker

**Choice**: Ollama on host machine

**Rationale**:
- ✅ Better GPU access
- ✅ Easier model management
- ✅ Avoids Docker GPU passthrough complexity
- ❌ Requires separate Ollama installation

**Trade-off**: One more setup step, but better performance and user experience

---

### Decision 7: Streaming vs. Request/Response

**Choice**: Start with request/response, add streaming if time permits

**Rationale**:
- ✅ Simpler implementation
- ✅ Easier error handling
- ✅ Anthropic SDK supports both
- ❌ Less responsive feel

**Trade-off**: Worse UX for slow models, but more reliable

---

### Decision 8: Chunking Strategy (Sliding Window with Overlap)

**Choice**: Sliding window with 50-token overlap

**Rationale**:
- ✅ Preserves context across boundaries
- ✅ Handles long episodes
- ✅ Standard practice
- ❌ Slight redundancy in storage

**Trade-off**: More chunks stored, but better retrieval quality

---

### Decision 9: Agent Routing (Keyword-based vs. LLM-based)

**Choice**: Start with keyword-based, upgrade to LLM if needed

**Rationale**:
- ✅ Fast and deterministic
- ✅ No extra LLM calls
- ✅ Easier to debug
- ❌ Less flexible than LLM classification

**Trade-off**: May miss edge cases, but sufficient for demo

---

### Decision 10: Single Database Instance vs. Replication

**Choice**: Single database instance

**Rationale**:
- ✅ Appropriate for local demo
- ✅ Simpler Docker Compose
- ❌ No high availability

**Trade-off**: Not production-ready, but perfect for take-home assignment

---

## Appendix: Architecture Diagram (Detailed)

```
┌───────────────────────────────────────────────────────────────────────┐
│                            USER BROWSER                                │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    React Frontend (Vite)                      │   │
│  │                                                               │   │
│  │  Components:                                                  │   │
│  │  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐        │   │
│  │  │ SessionSide │ │ Conversation │ │   Artifact    │        │   │
│  │  │    bar      │ │    Area      │ │    Viewer     │        │   │
│  │  └─────────────┘ └──────────────┘ └───────────────┘        │   │
│  │                                                               │   │
│  │  State: React Query + Context API                            │   │
│  │  Styling: TailwindCSS                                        │   │
│  │  API Client: Axios/Fetch                                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
                                │
                         HTTP REST API
                                │
┌───────────────────────────────▼───────────────────────────────────────┐
│                        FastAPI Backend                                 │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                       API Layer                               │   │
│  │  /api/health    /api/sessions    /api/messages               │   │
│  │  /api/artifacts    /api/config/models                        │   │
│  │  - Pydantic validation   - Error handling   - CORS           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                │                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Service Layer                              │   │
│  │                                                               │   │
│  │  ┌────────────────┐  ┌─────────────────┐  ┌──────────────┐ │   │
│  │  │ Agent Service  │  │ Retrieval Svc   │  │  LLM Service │ │   │
│  │  │                │  │                 │  │              │ │   │
│  │  │ - Router       │  │ - Embedding     │  │ - Provider   │ │   │
│  │  │ - Skills       │  │ - FAISS search  │  │   Factory    │ │   │
│  │  │ - Context mgmt │  │ - Metadata      │  │ - Ollama     │ │   │
│  │  └────────────────┘  └─────────────────┘  │ - Anthropic  │ │   │
│  │                                             └──────────────┘ │   │
│  │                                                               │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │               Skills (Anthropic SDK)                    │ │   │
│  │  │                                                          │ │   │
│  │  │  ┌────────────┐  ┌──────────┐  ┌────────────────┐    │ │   │
│  │  │  │ Grounded   │  │  Ship30  │  │   Artifacts    │    │ │   │
│  │  │  │    Q&A     │  │   Essay  │  │  MD/HTML/CSS   │    │ │   │
│  │  │  └────────────┘  └──────────┘  └────────────────┘    │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                │                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  Persistence Layer (SQLAlchemy)               │   │
│  │  Models: Session, Message, Artifact, TranscriptChunk         │   │
│  │  Migrations: Alembic                                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
                                │
                         PostgreSQL Protocol
                                │
┌───────────────────────────────▼────────────────────────────────────────┐
│                        PostgreSQL 15                                    │
│  Tables: sessions, messages, artifacts, transcript_chunks              │
│  Indexes: session_id, created_at, source_file                          │
│  Volume: postgres_data (persisted)                                     │
└─────────────────────────────────────────────────────────────────────────┘

         External Services (Local/Optional)

┌────────────────────────┐           ┌──────────────────────────┐
│   Ollama (Host)        │           │   Anthropic API          │
│   http://localhost     │           │   api.anthropic.com      │
│      :11434            │           │   (Optional)             │
│                        │           │                          │
│   Model:               │           │   Model:                 │
│   llama3.2:8b          │           │   claude-3-5-sonnet      │
└────────────────────────┘           └──────────────────────────┘

         Data Stores (Local Filesystem)

┌────────────────────────────────────────────────────────────────┐
│              backend/data/ (Docker Volume)                      │
│                                                                 │
│   faiss_index.bin          - FAISS similarity search index     │
│   chunk_mapping.json       - Chunk metadata mapping            │
│   embeddings.npy           - NumPy embedding cache (optional)  │
└─────────────────────────────────────────────────────────────────┘

         Ingestion Pipeline (One-time)

┌────────────────────────────────────────────────────────────────┐
│   ingestion/scripts/ingest_transcripts.py                      │
│                                                                 │
│   1. Clone ChatPRD/lennys-podcast-transcripts                  │
│   2. Load & parse .txt files                                   │
│   3. Chunk text (500 tokens, 50 overlap)                       │
│   4. Generate embeddings (sentence-transformers)               │
│   5. Build FAISS index                                         │
│   6. Store chunks in PostgreSQL                                │
│   7. Save index to disk                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

**Document Version**: 1.0  
**Last Updated**: Phase 0 - Initial Planning  
**Status**: Ready for Design Document
