# Phase 0 Summary: Discovery and Planning

## Status: ✅ COMPLETE

Phase 0 has been completed successfully. All planning documents have been created and key architectural decisions have been made.

---

## Deliverables Created

1. **PRD.md** - Product Requirements Document
   - User and problem definition
   - Success metrics
   - Assumptions
   - In/out of scope
   - User flows
   - Acceptance criteria
   - Risks and trade-offs
   - Implementation plan

2. **architecture.md** - Technical Architecture Document
   - High-level architecture
   - Component design (Frontend, Backend, Agent, Database)
   - Data flows
   - Database schema
   - API design
   - Agent architecture (skills + routing)
   - RAG pipeline (ingestion + retrieval)
   - Model provider abstraction
   - Artifact security
   - Deployment architecture
   - Observability
   - Security
   - Trade-offs and decisions

3. **design.md** - UI/UX Design Document
   - Design philosophy
   - Visual identity
   - Typography system
   - Color system
   - Spacing and layout
   - Component design
   - Information architecture
   - Conversational experience
   - Source citation design
   - Artifact viewer design
   - States and feedback
   - Responsive design
   - Accessibility
   - Design system
   - Differentiation from generic chatbots

4. **IMPLEMENTATION_CHECKLIST.md** - Comprehensive Implementation Checklist
   - Detailed checklist for all 11 phases
   - Granular tasks for each requirement
   - Final requirements audit
   - Assignment requirements cross-check

---

## Key Architectural Decisions

### 1. Agent Framework: **Anthropic Claude SDK**

**Rationale:**
- Official SDK with better stability
- Cleaner integration with Anthropic API
- Good documentation and examples
- Tool/function calling built-in
- Natural fit since Anthropic is primary cloud provider

**Alternative Considered:** Pi Coding Agent (less mature, fewer examples)

---

### 2. Retrieval Strategy: **sentence-transformers + FAISS**

**Rationale:**
- Runs completely locally (no external dependencies)
- Fast and reliable
- Easy to serialize/version control
- sentence-transformers: state-of-art embeddings, runs locally
- FAISS: fast similarity search, no external service

**Alternative Considered:** OpenAI embeddings + vector database (external dependency, costs money)

---

### 3. Frontend Framework: **React + Vite**

**Rationale:**
- Faster dev server than Next.js
- Simpler config for local demo
- No SSR complexity
- Perfect for local SPA

**Alternative Considered:** Next.js (overkill for local demo, no SEO needed)

---

### 4. Chunking Strategy: **Sliding Window with Overlap**

**Parameters:**
- Chunk size: 500 tokens (~750 words)
- Overlap: 50 tokens
- Preserve sentence boundaries

**Rationale:**
- Preserves context across boundaries
- Handles long episodes gracefully
- Standard practice for RAG

---

### 5. Artifact Security: **Sandboxed Iframe (Primary) + HTML Sanitization (Secondary)**

**Defense in Depth:**
1. **Layer 1:** Sandboxed iframe with restricted attributes
2. **Layer 2:** Content Security Policy headers
3. **Layer 3:** HTML sanitization (bleach/DOMPurify)
4. **Layer 4:** Frontend validation

**Rationale:**
- Browser-enforced security (most reliable)
- Defense in depth (multiple layers)
- Blocks JavaScript completely

---

### 6. Database: **PostgreSQL Only (No Redis)**

**Rationale:**
- One less service to manage
- PostgreSQL fast enough for single-user
- Simpler Docker Compose

**Trade-off:** Slight latency increase, but acceptable for demo

---

### 7. Ollama Deployment: **Host Machine (Not Docker)**

**Rationale:**
- Better GPU access
- Easier model management
- Avoids Docker GPU passthrough complexity

**Trade-off:** One more setup step, but better performance

---

### 8. Model Choice (Ollama): **llama3.2:8B** (Recommended)

**Why:**
- Good balance of quality and speed
- Realistic for developer machines
- Well-supported by Ollama
- Decent instruction-following

**Alternatives:** mistral:7B, mixtral:8x7b (slower but higher quality)

---

## Technology Stack Summary

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Validation:** Pydantic
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Agent:** Anthropic Claude SDK
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector Search:** FAISS
- **Database:** PostgreSQL 15

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **State Management:** React Query + Context API
- **HTTP Client:** Axios

### LLM Providers
- **Local (Mandatory):** Ollama (llama3.2:8B)
- **Cloud (Optional):** Anthropic (Claude 3.5 Sonnet)

### Infrastructure
- **Orchestration:** Docker Compose
- **Database:** PostgreSQL (Docker)
- **Backend:** Python/FastAPI (Docker)
- **Frontend:** React/Vite (Docker)
- **Ollama:** Host machine (for GPU access)

---

## Database Schema Design

### Tables

1. **sessions**
   - id (UUID, PK)
   - created_at (timestamp)
   - updated_at (timestamp)
   - title (varchar, nullable)
   - metadata (JSONB, nullable)

2. **messages**
   - id (UUID, PK)
   - session_id (UUID, FK → sessions)
   - role (varchar: 'user' | 'assistant')
   - content (text)
   - sources (JSONB, nullable)
   - created_at (timestamp)
   - metadata (JSONB, nullable)

3. **artifacts**
   - id (UUID, PK)
   - session_id (UUID, FK → sessions)
   - message_id (UUID, FK → messages, nullable)
   - type (varchar: 'markdown' | 'html' | 'css')
   - content (text)
   - created_at (timestamp)
   - metadata (JSONB, nullable)

4. **transcript_chunks**
   - id (UUID, PK)
   - episode_title (varchar)
   - guest (varchar, nullable)
   - source_file (varchar)
   - chunk_index (integer)
   - content (text)
   - created_at (timestamp)
   - metadata (JSONB, nullable)

**Note:** Embeddings stored in FAISS index file (not in database) for simplicity.

---

## API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `POST /api/sessions` - Create session
- `GET /api/sessions` - List sessions
- `GET /api/sessions/{session_id}` - Get session with messages
- `POST /api/sessions/{session_id}/messages` - Send message
- `GET /api/artifacts/{artifact_id}` - Get artifact
- `GET /api/config/models` - Get model configuration

---

## Agent Architecture

### Skills

1. **Grounded Q&A Skill**
   - Default for product/growth questions
   - Retrieves transcript chunks
   - Generates grounded answers
   - Extracts source citations

2. **Ship 30 for 30 Skill**
   - Triggered by keywords: "Ship 30", "essay", "write article"
   - Applies Ship 30 writing principles
   - Generates ~1,250 word essay
   - Grounds claims in sources

3. **Artifact Skill**
   - Triggered by: "create", "generate", "build" + "dashboard", "framework"
   - Generates Markdown or HTML/CSS
   - Returns structured artifact

### Routing Logic

```
User Message
    ↓
Intent Detection
    ↓
┌─────────────┐
│   Router    │
└─────────────┘
    ↓
    ├─→ Ship 30 keywords? → Ship 30 Skill
    ├─→ Artifact keywords? → Artifact Skill
    └─→ Default → Grounded Q&A Skill
```

---

## RAG Pipeline

### Ingestion

```
Lenny Transcripts (GitHub)
    ↓
Load & Parse (.txt, .md files)
    ↓
Clean (remove timestamps, normalize whitespace)
    ↓
Extract Metadata (episode title, guest)
    ↓
Chunk Text (500 tokens, 50 overlap)
    ↓
Generate Embeddings (sentence-transformers)
    ↓
Store Chunks (PostgreSQL)
    ↓
Build FAISS Index
    ↓
Save Index to Disk (faiss_index.bin)
```

### Retrieval

```
User Question
    ↓
Generate Query Embedding
    ↓
FAISS Similarity Search (top-K=5)
    ↓
Fetch Chunk Metadata (PostgreSQL)
    ↓
Return Ranked Chunks with Sources
```

---

## UI Design Principles

### Core Principles

1. **Editorial Quality Over Playfulness**
   - Professional, not cutesy
   - Confidence through clarity
   - Typography-first design

2. **Information Density Without Clutter**
   - Surface relevant context
   - Progressive disclosure
   - Every pixel serves a purpose

3. **Trust Through Transparency**
   - Always show sources
   - Make AI reasoning visible
   - Clear model/provider indicators

4. **Calm Technology**
   - Subtle animations
   - Quiet colors
   - Focus-friendly environment

5. **Memorable but Not Trendy**
   - Distinctive without gimmicks
   - Timeless over trendy
   - Professional over casual

### Key Differentiators from Generic Chatbots

❌ **Generic ChatGPT Clone:**
- Generic blue gradient
- Plain rounded bubbles
- No source attribution
- Random AI sparkle icons
- Generic template

✅ **The Lenny Growth Assistant:**
- Professional editorial layout
- Strong typography hierarchy
- Amber-highlighted source cards
- Clear episode/guest attribution
- Distinctive visual identity
- Model indicator visibility
- Purposeful whitespace

---

## Security Model

### Artifact Security (Defense in Depth)

1. **Sandboxed Iframe**
   - `sandbox="allow-same-origin"` only
   - No scripts, forms, navigation, popups

2. **Content Security Policy**
   - `default-src 'none'`
   - `style-src 'unsafe-inline'`
   - No external resources

3. **HTML Sanitization**
   - Whitelist allowed tags/attributes
   - Strip dangerous elements

4. **Frontend Validation**
   - Size limits (1MB max)
   - Type validation

### General Security

- No committed secrets
- .env.example with placeholders
- Parameterized SQL queries
- Input validation (Pydantic)
- Safe Markdown rendering
- Structured error responses (no stack traces)

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Hallucination | Strict prompt engineering, "insufficient evidence" responses |
| Retrieval quality | Chunking with overlap, test with known queries |
| Local model quality | Choose realistic model, provide cloud option |
| Response latency | Clear loading states, optimize chunk count |
| Service unavailable | Graceful error handling, retry logic, health checks |
| Prompt injection | System prompt separation, input validation |
| XSS attacks | Sandboxed iframe, CSP, HTML sanitization |
| Setup complexity | Clear step-by-step README, troubleshooting guide |

---

## Implementation Phases Overview

1. **Phase 1:** Project Foundation (2 hours)
2. **Phase 2:** FastAPI + PostgreSQL (3 hours)
3. **Phase 3:** Transcript Ingestion (3 hours)
4. **Phase 4:** Agent + Ollama (4 hours)
5. **Phase 5:** Frontend (6 hours)
6. **Phase 6:** Ship 30 Skill (2 hours)
7. **Phase 7:** Artifacts (4 hours)
8. **Phase 8:** Cloud Model (2 hours)
9. **Phase 9:** Hardening (4 hours)
10. **Phase 10:** Documentation (3 hours)
11. **Phase 11:** Final Evaluator Simulation (3 hours)

**Total Estimated Time:** ~36 hours of focused engineering

---

## Success Criteria

The project will be considered complete when:

1. ✅ Fresh clone → working demo in <10 minutes
2. ✅ All core features work (Q&A, sources, Ship 30, artifacts)
3. ✅ Ollama demo works without cloud credentials
4. ✅ UI is distinctive and polished
5. ✅ Security measures implemented (artifact isolation)
6. ✅ Documentation complete (README, PRD, architecture, design)
7. ✅ Tests pass (API, retrieval, agent, security)
8. ✅ No secrets committed
9. ✅ Demo-ready for 2-3 minute video

---

## Key Files Created in Phase 0

```
lenny-growth-assistant/
├── PRD.md                         ← Product Requirements
├── architecture.md                ← Technical Architecture
├── design.md                      ← UI/UX Design
├── IMPLEMENTATION_CHECKLIST.md    ← Detailed Checklist
└── PHASE_0_SUMMARY.md            ← This Document
```

---

## Next Steps

**PHASE 1: Project Foundation**

Tasks:
1. Initialize repository structure
2. Create Docker Compose configuration
3. Set up backend skeleton (FastAPI)
4. Set up frontend skeleton (React + Vite)
5. Create .env.example and .gitignore
6. Verify everything starts

**Estimated Time:** 2 hours

**Blocker Check:** None - ready to proceed

---

## Questions Resolved

1. **Agent Framework?** → Anthropic Claude SDK (cleaner, better documented)
2. **Retrieval Strategy?** → sentence-transformers + FAISS (local, simple)
3. **Frontend Framework?** → React + Vite (fast, simple)
4. **Ollama Model?** → llama3.2:8B (balanced quality/speed)
5. **Artifact Security?** → Sandboxed iframe + CSP + sanitization (defense in depth)
6. **Streaming?** → Start without, add if time permits (simpler, more reliable)

---

## Assumptions Made

1. **Hardware:** Evaluator can run small-to-medium Ollama model (7B-13B)
2. **Software:** Evaluator has Docker, Docker Compose, can install Ollama
3. **Network:** Evaluator can clone GitHub repos, optionally access Anthropic API
4. **Knowledge Scope:** Lenny's transcripts provide sufficient product/growth coverage
5. **User Preference:** Users prefer honest "I don't know" over hallucinated answers
6. **Scale:** Single-user local deployment (no multi-tenancy required)
7. **Data Freshness:** Static transcript corpus (no real-time updates)

---

## Open Questions (To Be Resolved During Implementation)

1. **Exact Ollama model choice** - Test llama3.2:8B vs. mistral:7B for quality/speed
2. **Streaming implementation** - Add if time permits and reliable with SDK
3. **Dark mode** - Add if time permits (Phase 2 feature)
4. **Model switching UI** - Basic or full-featured selector?

---

## Phase 0 Complete ✅

All planning documents are ready. Architecture is sound. Design is clear. Implementation plan is detailed.

**Ready to proceed to Phase 1: Project Foundation**

**Recommendation:** Review PRD.md, architecture.md, and design.md before proceeding to ensure alignment on product vision, technical approach, and UI design.

---

**Document Version:** 1.0  
**Created:** Phase 0 - Initial Planning  
**Status:** ✅ COMPLETE - Ready for Phase 1
