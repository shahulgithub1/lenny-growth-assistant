# The Lenny Growth Assistant

AI-powered research assistant for product and growth teams, grounded in Lenny Rachitsky's podcast library.

**Forward Deployed Engineer Take-Home Assignment** - Full-Stack AI Product

---

## Quick Start

```bash
# Clone and enter directory
cd Lenny_Podcastt

# Start all services (Docker Compose)
./start.sh

# Open frontend
open http://localhost:5173
```

See **[QUICK_START.md](QUICK_START.md)** for detailed setup and demo guide.

---

## Features

### 🎯 Grounded Q&A
- Ask questions about product and growth
- Answers grounded in Lenny's podcast transcripts
- Source citations with episode and guest info
- No fabricated claims

### ✍️ Ship 30 for 30 Essays
- Generate ~1,250-word essays
- Ship 30 writing principles encoded
- Strong hooks, narrative arc, skimmable structure
- Grounded in Lenny's insights

### 🎨 Artifact Generation
- Create Markdown documents and frameworks
- Generate HTML/CSS dashboards
- Sandboxed secure viewer
- Preview and code modes

### 💎 Distinctive UI
- Not a ChatGPT clone
- Editorial typography and professional design
- Amber source citations
- Responsive mobile/tablet/desktop
- Accessible (WCAG AA)

---

## Architecture

### Tech Stack
- **Frontend**: React 18 + TypeScript + TailwindCSS + Vite
- **Backend**: FastAPI + Python 3.11 + SQLAlchemy
- **Database**: PostgreSQL 15
- **Agent**: Anthropic Claude Agent SDK (tool calling)
- **RAG**: sentence-transformers + FAISS (local, no external APIs)
- **LLM**: Ollama (llama3.2:3b) or Anthropic (Claude Sonnet)

### Agent Skills
1. **Grounded Q&A** - Retrieval-augmented answers from transcripts
2. **Ship 30** - Essay generation with Ship 30 for 30 principles
3. **Artifact** - Secure document/dashboard generation

### Security (Artifacts)
- Sandboxed iframe (no JavaScript execution)
- DOMPurify HTML sanitization
- CSP enforcement
- No external resources

---

## Project Status

✅ **Phase 0**: Requirements, architecture, design  
✅ **Phase 1**: Docker setup, FastAPI skeleton, React skeleton  
✅ **Phase 2**: PostgreSQL, sessions, messages, Alembic migrations  
✅ **Phase 3**: Transcript ingestion, RAG pipeline, FAISS indexing  
✅ **Phase 4**: Claude Agent SDK integration, tool calling, Ollama fallback  
✅ **Phase 5**: Complete frontend UI, responsive design, accessibility  
✅ **Phase 6**: Ship 30 for 30 skill with writing principles  
✅ **Phase 7**: Artifact generation and secure viewer  

**Next**: Phase 8 - Cloud model expansion, hardening, deployment

See **[PHASES_5_6_7_REPORT.md](PHASES_5_6_7_REPORT.md)** for detailed implementation report.

---

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Setup and demo guide
- **[PRD.md](PRD.md)** - Product requirements
- **[architecture.md](architecture.md)** - System architecture
- **[design.md](design.md)** - UI/UX design system
- **[PHASES_5_6_7_REPORT.md](PHASES_5_6_7_REPORT.md)** - Implementation report

---

## Demo (2-3 Minutes)

### 1. Grounded Q&A (45s)
Ask: *"How should a startup improve retention?"*
- Show grounded answer with sources
- Highlight amber citation cards

### 2. Ship 30 Essay (45s)
Ask: *"Turn this into a Ship 30 essay"*
- Show ~1,250-word formatted output
- Point out hooks, bold emphasis, structure

### 3. Artifact Viewer (45s)
Ask: *"Create a product strategy framework"*
- Show artifact sliding in
- Toggle preview/code
- Explain sandboxed security

### Bonus: Features (30s)
- Session sidebar with history
- Mobile responsive
- Model indicator
- Distinctive design

---

## Key Highlights

### Technical
- ✅ Claude Agent SDK (not just Anthropic API)
- ✅ Tool calling for retrieval (agent decides when to search)
- ✅ Local RAG (no external embedding APIs)
- ✅ Provider abstraction (Ollama + Anthropic)
- ✅ Sandboxed artifact security

### Product
- ✅ Grounded in real Lenny transcripts (no fabrication)
- ✅ Ship 30 principles from official guide
- ✅ Distinctive UI (not ChatGPT clone)
- ✅ Session persistence
- ✅ Source transparency

### Engineering
- ✅ Full-stack TypeScript + Python
- ✅ Docker Compose single-command deployment
- ✅ Database migrations (Alembic)
- ✅ Responsive + accessible frontend
- ✅ Comprehensive documentation

---

## Requirements Met

Per Forward Deployed Engineer assignment:

✅ **Anthropic Claude Agent SDK** - Using `claude-agent-sdk>=0.2.140` with tool calling  
✅ **RAG with Lenny's Transcripts** - Grounded retrieval from podcast library  
✅ **Multiple Skills** - Grounded Q&A, Ship 30, Artifacts  
✅ **Local Deployment** - Docker Compose, works offline with Ollama  
✅ **Production Quality** - Polished UI, error handling, security  
✅ **Distinctive Design** - Not generic chatbot, editorial aesthetic  

---

## Running Locally

### Prerequisites
- Docker Desktop
- Ollama (optional, for local LLM)
- Anthropic API key (optional, for Claude Agent SDK tool calling)

### Start
```bash
./start.sh
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Test
```bash
docker-compose exec backend pytest tests/ -v
```

---

## Configuration

Copy `.env.example` to `.env`:

```bash
# LLM Provider
MODEL_PROVIDER=ollama  # or "anthropic"

# Ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2:3b

# Anthropic (for Claude Agent SDK tool calling)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

---

## License

MIT

---

**Status**: Phases 5-7 Complete - Ready for Evaluator Demo ✅
