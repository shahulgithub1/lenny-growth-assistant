# Quick Start Guide - The Lenny Growth Assistant

## Prerequisites

1. **Docker Desktop** - Running
2. **Ollama** (optional for local LLM)
   ```bash
   # Install Ollama: https://ollama.ai
   ollama pull llama3.2:3b
   ollama serve
   ```
3. **Anthropic API Key** (optional for Claude Agent SDK tool calling)

## Start the Application

### Option 1: Quick Start (Recommended)

```bash
# From project root
./start.sh
```

This will:
- Start PostgreSQL database
- Run database migrations
- Ingest Lenny's transcript data (if not already done)
- Start FastAPI backend on http://localhost:8000
- Start React frontend on http://localhost:5173

### Option 2: Manual Start

```bash
# Start all services
docker-compose up -d

# Run ingestion (first time only)
./run_ingestion.sh

# Backend will be on http://localhost:8000
# Frontend will be on http://localhost:5173
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://lennyadmin:lennypassword@localhost:5432/lennydb

# LLM Provider: "ollama" or "anthropic"
MODEL_PROVIDER=ollama

# Ollama (if using)
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2:3b

# Anthropic (if using - required for Ship 30 and Artifact tool calling)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

## Using the Application

### 1. Open Frontend

Navigate to http://localhost:5173

You'll see the welcome screen with example prompts.

### 2. Try Grounded Q&A

Ask questions about product and growth:
- "How should a startup improve retention?"
- "What does product-market fit look like?"
- "What are the key principles of growth loops?"

The assistant will:
- Search Lenny's transcripts
- Provide grounded answers
- Show source citations

### 3. Try Ship 30 Essay Generation

Request an essay:
- "Turn this into a Ship 30 essay"
- "Write a blog post about growth loops"

The assistant will:
- Generate ~1,250-word essay
- Apply Ship 30 writing principles
- Ground claims in transcripts
- Format with Markdown

### 4. Try Artifact Generation

Request visual artifacts:
- "Create a one-page product strategy framework"
- "Generate a dashboard showing key growth metrics"

The assistant will:
- Generate HTML or Markdown artifact
- Display in sandboxed viewer
- Allow preview/code toggle
- Enable code copying

## Features Showcase

### Distinctive UI
- Not a ChatGPT clone
- Editorial typography
- Amber source citations
- Professional color scheme
- Beautiful empty state

### Source Grounding
- All answers grounded in Lenny's transcripts
- Episode titles and guests shown
- Relevant excerpts displayed
- No fabricated claims

### Session Management
- Multiple conversations
- Session history (Today, Last 7 Days, Older)
- Persistent across refresh
- Auto-titled from first message

### Responsive Design
- Mobile: Drawer sidebar, full-screen artifacts
- Tablet: Adjusted layouts
- Desktop: Multi-column with side panels

### Accessibility
- Keyboard navigation (Tab, ⌘+Enter, Escape)
- Screen reader support (ARIA labels)
- High contrast (WCAG AA)
- Reduced motion support

### Security (Artifacts)
- Sandboxed iframe (no JavaScript execution)
- HTML sanitization (DOMPurify)
- No external resources
- Safe styling only

## Troubleshooting

### Backend won't start
```bash
# Check Docker
docker ps

# Check logs
docker-compose logs backend

# Restart
docker-compose restart backend
```

### Ollama connection failed
```bash
# Verify Ollama is running
ollama list

# Check Ollama URL in .env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### Frontend build errors
```bash
cd frontend
npm install
npm run dev
```

### Transcripts not loaded
```bash
# Re-run ingestion
./run_ingestion.sh

# Check logs
docker-compose logs ingestion
```

### Database issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d
./run_ingestion.sh
```

## API Documentation

### Backend API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints
- `GET /health` - Health check
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - List sessions
- `GET /api/sessions/{id}` - Get session with messages
- `POST /api/sessions/{id}/messages` - Send message
- `GET /api/artifacts/{id}` - Get artifact
- `GET /api/sessions/{id}/artifacts` - List session artifacts

## Running Tests

### Backend Tests
```bash
docker-compose exec backend pytest tests/ -v
```

### Manual Testing Checklist
- [ ] Create new conversation
- [ ] Ask grounded Q&A question
- [ ] Verify sources appear
- [ ] Generate Ship 30 essay
- [ ] Create HTML artifact
- [ ] View artifact in viewer
- [ ] Toggle to code view
- [ ] Copy artifact code
- [ ] Switch sessions
- [ ] Test mobile responsive
- [ ] Test keyboard navigation
- [ ] Test error states (stop Ollama)

## Demo Script (2-3 Minutes)

### Minute 1: Grounded Q&A
1. Open app, show distinctive UI
2. Ask: "How should a startup improve retention?"
3. Show source citations with amber cards
4. Highlight Lenny's podcast grounding

### Minute 2: Ship 30 Essay
1. Ask: "Turn this into a Ship 30 essay"
2. Show ~1,250-word formatted output
3. Point out bold emphasis, structure
4. Highlight Ship 30 writing principles

### Minute 3: Artifact Viewer
1. Ask: "Create a one-page product strategy framework"
2. Show artifact viewer sliding in
3. Toggle between preview and code
4. Explain sandboxed security

### Bonus: Show Features
- Session sidebar with history
- Mobile responsive (resize browser)
- Model indicator (Ollama/Anthropic)
- Empty state with example prompts

## Architecture Highlights

### Tech Stack
- **Frontend**: React 18, TypeScript, TailwindCSS, Vite
- **Backend**: FastAPI, Python 3.11, SQLAlchemy
- **Database**: PostgreSQL 15
- **Agent**: Anthropic Claude Agent SDK
- **RAG**: sentence-transformers + FAISS
- **LLM**: Ollama (llama3.2:3b) or Anthropic (Claude Sonnet)

### Key Design Decisions
1. **Claude Agent SDK** - Not just Anthropic API, proper agent with tool calling
2. **Local RAG** - No external embedding APIs, fully self-contained
3. **Provider Abstraction** - Ollama and Anthropic swappable
4. **Sandboxed Artifacts** - Defense-in-depth security
5. **Ship 30 Principles** - Encoded from official guide

### RAG Pipeline
1. Lenny transcripts chunked (500 tokens, 50 overlap)
2. Embeddings via sentence-transformers (all-MiniLM-L6-v2)
3. FAISS similarity search (top-5 chunks)
4. Sources preserved with episode metadata
5. Citations displayed in UI

### Agent Skills
1. **Grounded Q&A** - Default, retrieval-augmented answers
2. **Ship 30** - Essay generation with writing principles
3. **Artifact** - Markdown/HTML document generation

## Support

For issues or questions:
1. Check this guide
2. Review `PHASES_5_6_7_REPORT.md`
3. Check `architecture.md` and `design.md`
4. Review backend logs: `docker-compose logs`

## What's Next

Phase 8+:
- Cloud model expansion
- Security hardening
- Operational readiness
- Production deployment
- Evaluator simulation

**Current Status**: Phases 5-7 Complete - Ready for Demo ✅
