# Implementation Checklist: The Lenny Growth Assistant

## Phase 0: Discovery and Planning ✅

- [x] Analyze all assignment requirements
- [x] Make architectural decisions
- [x] Create PRD.md
- [x] Create architecture.md
- [x] Create design.md
- [x] Define implementation plan
- [x] Create this checklist

---

## Phase 1: Project Foundation

### Repository Structure
- [ ] Initialize git repository
- [ ] Create .gitignore (Python, Node, env files, secrets)
- [ ] Create .env.example with all variables
- [ ] Create README.md skeleton
- [ ] Set up directory structure:
  - [ ] frontend/
  - [ ] backend/
  - [ ] agent/
  - [ ] ingestion/
  - [ ] tests/
  - [ ] agent-transcripts/

### Docker Setup
- [ ] Create docker-compose.yml
- [ ] Configure PostgreSQL service
- [ ] Configure backend service
- [ ] Configure frontend service
- [ ] Set up volume persistence
- [ ] Test `docker compose up`

### Backend Foundation
- [ ] Initialize Python project (requirements.txt)
- [ ] Install FastAPI, SQLAlchemy, Pydantic
- [ ] Install Anthropic SDK
- [ ] Install sentence-transformers, FAISS
- [ ] Create app structure (api/, services/, db/, core/)
- [ ] Create main.py with FastAPI app
- [ ] Add CORS middleware
- [ ] Create config.py (environment variables)
- [ ] Create logging.py (structured logging)
- [ ] Verify backend starts

### Frontend Foundation
- [ ] Initialize React + Vite project
- [ ] Install dependencies (React Query, Axios, TailwindCSS)
- [ ] Set up TailwindCSS configuration
- [ ] Create component structure
- [ ] Create API client
- [ ] Verify frontend starts
- [ ] Verify frontend can reach backend health endpoint

---

## Phase 2: FastAPI + PostgreSQL

### Database Schema
- [ ] Set up Alembic for migrations
- [ ] Create initial migration
- [ ] Define Session model (id, created_at, updated_at, title, metadata)
- [ ] Define Message model (id, session_id, role, content, sources, created_at, metadata)
- [ ] Define Artifact model (id, session_id, message_id, type, content, created_at, metadata)
- [ ] Define TranscriptChunk model (id, episode_title, guest, source_file, chunk_index, content, created_at, metadata)
- [ ] Create indexes (session_id, created_at, source_file)
- [ ] Run migrations
- [ ] Verify tables created

### API Endpoints
- [ ] Implement GET /health
- [ ] Implement POST /api/sessions (create session)
- [ ] Implement GET /api/sessions (list sessions)
- [ ] Implement GET /api/sessions/{session_id} (get session with messages)
- [ ] Implement POST /api/sessions/{session_id}/messages (send message)
- [ ] Implement GET /api/artifacts/{artifact_id} (get artifact)
- [ ] Implement GET /api/config/models (get model configuration)

### Pydantic Schemas
- [ ] Create SessionResponse schema
- [ ] Create MessageCreateRequest schema
- [ ] Create MessageResponse schema
- [ ] Create Source schema
- [ ] Create ArtifactResponse schema
- [ ] Create ErrorResponse schema
- [ ] Add validation rules

### Error Handling
- [ ] Implement structured error responses
- [ ] Create custom exception classes
- [ ] Add error handlers for FastAPI
- [ ] Add request_id to all responses
- [ ] Log all errors with context

### Tests
- [ ] Test GET /health endpoint
- [ ] Test session creation
- [ ] Test session retrieval
- [ ] Test session listing
- [ ] Test message creation
- [ ] Test request validation (invalid inputs)
- [ ] Test error responses
- [ ] Test session isolation (messages don't leak between sessions)

---

## Phase 3: Transcript Ingestion

### Data Acquisition
- [ ] Clone https://github.com/ChatPRD/lennys-podcast-transcripts
- [ ] Explore transcript file structure
- [ ] Document file formats (.txt, .md, etc.)
- [ ] Identify metadata extraction strategy (titles, guests)

### Ingestion Script
- [ ] Create ingestion/scripts/ingest_transcripts.py
- [ ] Implement transcript loader (read files)
- [ ] Implement cleaning logic:
  - [ ] Remove timestamps
  - [ ] Extract episode title
  - [ ] Extract guest name(s)
  - [ ] Normalize whitespace
- [ ] Implement chunking logic:
  - [ ] Sliding window (500 tokens, 50 overlap)
  - [ ] Preserve sentence boundaries
  - [ ] Preserve metadata per chunk
- [ ] Implement embedding generation:
  - [ ] Load sentence-transformers model
  - [ ] Generate embeddings in batches
- [ ] Store chunks in PostgreSQL
- [ ] Build FAISS index
- [ ] Save FAISS index to disk (backend/data/faiss_index.bin)
- [ ] Save chunk mapping to disk (backend/data/chunk_mapping.json)

### Retrieval System
- [ ] Implement load_faiss_index() function
- [ ] Implement generate_query_embedding() function
- [ ] Implement retrieve_chunks() function:
  - [ ] Accept query string
  - [ ] Generate embedding
  - [ ] FAISS similarity search (top-K=5)
  - [ ] Fetch chunk metadata from PostgreSQL
  - [ ] Return ranked chunks with sources
- [ ] Test retrieval with known queries

### Documentation
- [ ] Document chunking parameters in architecture.md
- [ ] Document retrieval strategy
- [ ] Document how to run ingestion
- [ ] Document expected output (chunk count, index size)

### Tests
- [ ] Test chunking preserves metadata
- [ ] Test retrieval returns relevant chunks for known query
- [ ] Test retrieval handles empty results
- [ ] Test retrieval with insufficient evidence

---

## Phase 4: Agent + Ollama

### LLM Provider Abstraction
- [ ] Create LLMProvider abstract base class
- [ ] Implement OllamaProvider:
  - [ ] __init__ with base_url and model
  - [ ] generate() method
  - [ ] is_available() method
  - [ ] get_model_name() method
  - [ ] Error handling (connection refused, timeout)
- [ ] Implement provider factory function
- [ ] Test Ollama provider with local Ollama

### Agent Setup (Anthropic SDK)
- [ ] Initialize Anthropic Claude SDK
- [ ] Create agent configuration
- [ ] Define system prompts for each skill
- [ ] Implement context management (conversation history)

### Grounded Q&A Skill
- [ ] Create grounded_qa skill module
- [ ] Implement intent detection (Q&A vs. other)
- [ ] Implement retrieval integration:
  - [ ] Generate query from user message
  - [ ] Retrieve top-K chunks
  - [ ] Format chunks for LLM context
- [ ] Implement LLM prompt:
  - [ ] System prompt: "Answer using ONLY provided transcripts"
  - [ ] Include conversation history
  - [ ] Include retrieved chunks
- [ ] Implement source citation extraction
- [ ] Implement "insufficient evidence" detection
- [ ] Test end-to-end Q&A flow

### Session Context Management
- [ ] Load conversation history from database
- [ ] Pass last N messages to LLM (N=10)
- [ ] Include retrieved chunks in context
- [ ] Manage token budget (~4000 context, ~2000 generation)

### Routing Logic
- [ ] Implement route_message() function:
  - [ ] Detect Ship 30 keywords
  - [ ] Detect artifact keywords
  - [ ] Default to grounded Q&A
- [ ] Route to appropriate skill

### Failure Handling
- [ ] Handle Ollama unavailable
- [ ] Handle model timeout
- [ ] Handle malformed LLM response
- [ ] Handle empty retrieval
- [ ] Return structured errors to frontend

### Tests
- [ ] Test Ollama provider is_available()
- [ ] Test generate() with simple prompt
- [ ] Test routing to grounded Q&A
- [ ] Test retrieval integration
- [ ] Test source citation extraction
- [ ] Test context preservation across messages
- [ ] Test Ollama failure handling

---

## Phase 5: Frontend

### Design System
- [ ] Set up CSS variables (colors, spacing, typography)
- [ ] Create design tokens
- [ ] Configure TailwindCSS with custom theme
- [ ] Create Button component
- [ ] Create Input component
- [ ] Create Card component

### Core Layout
- [ ] Create App.tsx with main layout
- [ ] Implement Header component:
  - [ ] Logo/product name
  - [ ] Model indicator (provider + model)
- [ ] Implement SessionSidebar component:
  - [ ] New Chat button
  - [ ] Session list
  - [ ] Temporal grouping (Today, Yesterday, Last 7 Days)
  - [ ] Session item with title and metadata
- [ ] Implement responsive layout (sidebar → drawer on mobile)

### Conversation Components
- [ ] Create ConversationArea component
- [ ] Create MessageList component
- [ ] Create MessageBubble component:
  - [ ] User message (right-aligned)
  - [ ] Assistant message (left-aligned, with icon)
  - [ ] Timestamp
  - [ ] Model indicator on assistant messages
- [ ] Create MessageComposer component:
  - [ ] Auto-expanding textarea
  - [ ] Send button
  - [ ] Keyboard shortcut (Cmd/Ctrl+Enter)
  - [ ] Disabled state during generation
- [ ] Style messages with design system

### Source Citations
- [ ] Create SourceCard component:
  - [ ] Episode title
  - [ ] Guest name
  - [ ] Excerpt/quote
  - [ ] Metadata (episode number, date)
  - [ ] Amber highlighting
- [ ] Create SourceList component (grid layout)
- [ ] Display sources below assistant messages

### Empty State
- [ ] Create EmptyState component:
  - [ ] Product logo/icon
  - [ ] Value proposition text
  - [ ] Example prompts (clickable)
- [ ] Center vertically and horizontally

### Loading States
- [ ] Create LoadingMessage component:
  - [ ] Animated dots
  - [ ] Status text ("Searching transcripts...")
- [ ] Display during message generation

### Error States
- [ ] Create ErrorMessage component:
  - [ ] Clear error message
  - [ ] Actionable guidance
  - [ ] Retry button
- [ ] Handle Ollama unavailable
- [ ] Handle API errors
- [ ] Handle insufficient evidence response

### API Integration
- [ ] Create API client with axios
- [ ] Implement createSession()
- [ ] Implement getSessions()
- [ ] Implement getSession()
- [ ] Implement sendMessage()
- [ ] Use React Query for state management
- [ ] Handle loading states
- [ ] Handle errors

### Model Indicator
- [ ] Create ModelIndicator component
- [ ] Display current provider + model
- [ ] Update on model switch (if time permits)

### Navigation
- [ ] Implement New Chat button (creates session, switches view)
- [ ] Implement session switching (click session in sidebar)
- [ ] Maintain active session state
- [ ] Update URL if using routing (optional)

### Responsive Design
- [ ] Test mobile layout (<640px)
- [ ] Test tablet layout (641px-1024px)
- [ ] Test desktop layout (>1024px)
- [ ] Make sidebar collapsible on mobile
- [ ] Stack source cards vertically on mobile

### Accessibility
- [ ] Add keyboard navigation (Tab, Enter, Escape)
- [ ] Add focus indicators
- [ ] Add ARIA labels to buttons
- [ ] Add semantic HTML (nav, main, article)
- [ ] Test with keyboard only
- [ ] Test color contrast (WCAG AA)
- [ ] Add reduced motion support

### Tests
- [ ] Manual UI test: Create new chat
- [ ] Manual UI test: Send message
- [ ] Manual UI test: View sources
- [ ] Manual UI test: Switch sessions
- [ ] Manual UI test: Responsive layout
- [ ] Manual UI test: Keyboard navigation
- [ ] Manual UI test: Error states

---

## Phase 6: Ship 30 Skill

### Ship 30 Research
- [ ] Read https://www.ship30for30.com/post/how-to-start-writing-online-the-ship-30-for-30-ultimate-guide
- [ ] Document Ship 30 principles:
  - [ ] Strong hook (first 2 sentences)
  - [ ] Narrative progression
  - [ ] Skimmable formatting
  - [ ] Bullets and short paragraphs
  - [ ] Bold emphasis (3-5 key phrases)
  - [ ] ~1,250 words
  - [ ] Specific, actionable takeaway

### Ship 30 Skill Implementation
- [ ] Create ship30_skill module
- [ ] Implement Ship 30 system prompt (encode principles)
- [ ] Implement extract_context() (from conversation)
- [ ] Implement generate_essay() function:
  - [ ] Extract key insights from conversation
  - [ ] Retrieve additional context if needed
  - [ ] Generate essay with Ship 30 prompt
  - [ ] Validate word count (~1,250)
  - [ ] Ensure grounding in sources
- [ ] Format output with Markdown

### Routing Integration
- [ ] Update route_message() to detect Ship 30 keywords
- [ ] Route to Ship 30 skill
- [ ] Return formatted essay

### Tests
- [ ] Test Ship 30 generation from conversation
- [ ] Verify word count (~1,250 ±100)
- [ ] Verify hook quality
- [ ] Verify skimmable formatting (bullets, bold)
- [ ] Verify grounding (sources cited)
- [ ] Test with different conversation topics

---

## Phase 7: Artifacts

### Artifact Generation Skill
- [ ] Create artifact_skill module
- [ ] Implement determine_artifact_type() (Markdown vs. HTML)
- [ ] Implement generate_markdown() function
- [ ] Implement generate_html_css() function:
  - [ ] System prompt: semantic HTML, inline CSS, no JS
  - [ ] Generate based on conversation context
  - [ ] Validate HTML structure
- [ ] Persist artifact to database

### HTML Sanitization
- [ ] Install bleach or similar sanitization library
- [ ] Define allowed HTML tags
- [ ] Define allowed attributes
- [ ] Implement sanitize_html() function
- [ ] Test with malicious HTML samples

### Artifact Viewer Component
- [ ] Create ArtifactViewer component:
  - [ ] Panel that slides in from right
  - [ ] Header (title, type, timestamp, close button)
  - [ ] Code/Preview toggle
  - [ ] Preview mode: sandboxed iframe
  - [ ] Code mode: syntax-highlighted code
- [ ] Implement sandboxed iframe:
  - [ ] sandbox="allow-same-origin" (only)
  - [ ] srcDoc attribute
  - [ ] CSP headers
- [ ] Implement code view with syntax highlighting (Prism.js)
- [ ] Responsive: Full-screen modal on mobile

### Artifact Security
- [ ] Implement sandboxed iframe rendering
- [ ] Add CSP meta tag to iframe content
- [ ] Sanitize HTML before rendering
- [ ] Test XSS prevention:
  - [ ] <script> tags
  - [ ] onclick handlers
  - [ ] javascript: URLs
  - [ ] External resources
- [ ] Document security model in architecture.md

### Routing Integration
- [ ] Update route_message() to detect artifact keywords
- [ ] Route to artifact skill
- [ ] Return artifact metadata + content

### Frontend Integration
- [ ] Display artifact trigger in chat ("I've created a dashboard")
- [ ] Add "View Artifact" button
- [ ] Open ArtifactViewer on click
- [ ] Display artifact in viewer

### Tests
- [ ] Test Markdown artifact generation
- [ ] Test HTML artifact generation
- [ ] Test artifact persistence
- [ ] Test artifact retrieval
- [ ] Test sandboxed iframe blocks <script>
- [ ] Test sanitization blocks malicious HTML
- [ ] Test artifact viewer opens/closes
- [ ] Test code/preview toggle
- [ ] Manual security test: try to break sandbox

---

## Phase 8: Cloud Model (Anthropic)

### Anthropic Provider
- [ ] Implement AnthropicProvider class:
  - [ ] __init__ with api_key and model
  - [ ] generate() method
  - [ ] is_available() method
  - [ ] get_model_name() method
  - [ ] Error handling (auth error, connection error)
- [ ] Update provider factory to support "anthropic"
- [ ] Test Anthropic provider (if API key available)

### Configuration
- [ ] Add ANTHROPIC_API_KEY to .env.example (optional)
- [ ] Add ANTHROPIC_MODEL to .env.example
- [ ] Update config.py to load Anthropic settings
- [ ] Document how to enable Anthropic in README

### Model Switching (Optional)
- [ ] Implement GET /api/config/models endpoint
- [ ] Return available providers and models
- [ ] Frontend: fetch model config on load
- [ ] Frontend: display current provider/model
- [ ] Optional: Add model selector UI

### Graceful Fallback
- [ ] Handle missing ANTHROPIC_API_KEY gracefully
- [ ] Return clear error if Anthropic selected but not configured
- [ ] Verify Ollama still works without Anthropic credentials

### Tests
- [ ] Test Anthropic provider with valid API key
- [ ] Test Anthropic provider without API key (error)
- [ ] Test model switching (if implemented)
- [ ] Verify Ollama continues working without Anthropic

---

## Phase 9: Hardening

### Structured Logging
- [ ] Implement structured JSON logging with structlog
- [ ] Add request_id to all requests
- [ ] Add session_id to all logs
- [ ] Log key events:
  - [ ] Session created
  - [ ] Message sent
  - [ ] Retrieval completed
  - [ ] LLM generation started/completed
  - [ ] Errors
- [ ] Never log secrets (API keys, passwords)

### Error Handling
- [ ] Review all try/except blocks
- [ ] Ensure all errors return structured responses
- [ ] Add retry logic for LLM calls (exponential backoff)
- [ ] Handle database connection errors
- [ ] Handle FAISS index loading errors
- [ ] Handle retrieval failures

### Security Review
- [ ] Verify no secrets in .env.example
- [ ] Verify .gitignore includes .env, *.key
- [ ] Verify all database queries use parameterized queries (SQLAlchemy)
- [ ] Verify input validation on all endpoints
- [ ] Verify artifact sanitization and sandboxing
- [ ] Verify CORS is not wide open in production
- [ ] Verify no secrets in logs

### Resilience Testing
- [ ] Test: Ollama unavailable
- [ ] Test: PostgreSQL unavailable
- [ ] Test: FAISS index missing
- [ ] Test: Model timeout
- [ ] Test: Malformed LLM response
- [ ] Test: Empty retrieval
- [ ] Test: Database full (simulate)
- [ ] Test: Large message (10,000 chars)
- [ ] Test: Artifact too large (>1MB)

### Performance Optimization
- [ ] Profile LLM response time
- [ ] Profile retrieval time
- [ ] Optimize FAISS search if needed
- [ ] Add database indexes if missing
- [ ] Consider connection pooling

### Automated Tests
- [ ] Write API tests:
  - [ ] Health endpoint
  - [ ] Session CRUD
  - [ ] Message creation
  - [ ] Validation errors
- [ ] Write retrieval tests:
  - [ ] Relevant query returns relevant chunks
  - [ ] Empty query behavior
  - [ ] Metadata preserved
- [ ] Write agent tests:
  - [ ] Routing to correct skill
  - [ ] Grounded Q&A flow
  - [ ] Ship 30 generation
  - [ ] Artifact generation
- [ ] Write provider tests:
  - [ ] Ollama available/unavailable
  - [ ] Anthropic available/unavailable
- [ ] Write security tests:
  - [ ] HTML sanitization
  - [ ] Sandbox effectiveness (manual)
  - [ ] SQL injection prevention (parameterized queries)

---

## Phase 10: Documentation

### README.md
- [ ] Write product overview
- [ ] List features
- [ ] Document architecture (high-level)
- [ ] List requirements:
  - [ ] Docker & Docker Compose
  - [ ] Ollama
  - [ ] (Optional) Anthropic API key
- [ ] Write installation instructions:
  - [ ] Clone repository
  - [ ] Copy .env.example to .env
  - [ ] Configure environment variables
- [ ] Write PostgreSQL setup (automatic with Docker Compose)
- [ ] Write Ollama setup:
  - [ ] Install Ollama
  - [ ] Download model: `ollama pull llama3.2:3b`
  - [ ] Start Ollama: `ollama serve`
  - [ ] Verify: `ollama list`
- [ ] Write ingestion instructions:
  - [ ] `python ingestion/scripts/ingest_transcripts.py`
  - [ ] Expected output (chunk count)
- [ ] Write startup instructions:
  - [ ] `docker compose up`
  - [ ] Access frontend: http://localhost:5173
  - [ ] Access backend: http://localhost:8000
- [ ] Write test instructions:
  - [ ] `pytest backend/tests/`
- [ ] Write troubleshooting section:
  - [ ] Ollama not running
  - [ ] Model not downloaded
  - [ ] Database connection failed
  - [ ] Frontend can't reach backend
  - [ ] Ingestion errors
- [ ] Document cloud provider setup (optional):
  - [ ] Set ANTHROPIC_API_KEY in .env
  - [ ] Change MODEL_PROVIDER=anthropic
- [ ] Document security notes
- [ ] Document known limitations
- [ ] Write demo instructions (2-3 minute flow)

### .env.example
- [ ] Add DATABASE_URL with example
- [ ] Add MODEL_PROVIDER with default (ollama)
- [ ] Add OLLAMA_BASE_URL
- [ ] Add OLLAMA_MODEL
- [ ] Add ANTHROPIC_API_KEY (commented, optional)
- [ ] Add ANTHROPIC_MODEL (commented)
- [ ] Add comments explaining each variable
- [ ] Mark required vs. optional

### Finalize Architecture.md
- [ ] Add architecture diagram (ASCII or image)
- [ ] Document all components
- [ ] Document data flows
- [ ] Document database schema
- [ ] Document API endpoints
- [ ] Document agent architecture
- [ ] Document RAG pipeline
- [ ] Document model abstraction
- [ ] Document artifact security
- [ ] Document trade-offs and decisions

### Finalize Design.md
- [ ] Document visual identity
- [ ] Document typography
- [ ] Document color system
- [ ] Document spacing and layout
- [ ] Document component designs
- [ ] Document conversational experience
- [ ] Document source citation design
- [ ] Document artifact viewer
- [ ] Document states and feedback
- [ ] Document responsive design
- [ ] Document accessibility
- [ ] Document differentiation from generic chatbots

### Manual UI Test Plan
- [ ] Create tests/manual_ui_tests.md
- [ ] Document test cases:
  - [ ] New chat creation
  - [ ] Send message
  - [ ] View sources
  - [ ] Follow-up question (context preserved)
  - [ ] Switch sessions (context isolated)
  - [ ] Unsupported question (insufficient evidence)
  - [ ] Ship 30 essay generation
  - [ ] Markdown artifact generation
  - [ ] HTML artifact generation
  - [ ] Artifact viewer (code/preview toggle)
  - [ ] Model indicator visibility
  - [ ] Responsive layout (mobile, tablet, desktop)
  - [ ] Keyboard navigation
  - [ ] Error states (Ollama down, API error)

### Agent Transcripts
- [ ] Review coding agent transcripts from development
- [ ] Remove any secrets or sensitive information
- [ ] Organize by topic/phase
- [ ] Include important decisions and reasoning
- [ ] Include failed attempts and corrections
- [ ] Save to agent-transcripts/ directory

### Known Limitations
- [ ] Document in README.md:
  - [ ] Single-user local deployment (no auth)
  - [ ] No real-time transcript updates
  - [ ] Local model quality varies
  - [ ] Potential prompt injection vulnerability
  - [ ] Artifact sandbox not 100% foolproof
  - [ ] No fine-tuning on Lenny transcripts

---

## Phase 11: Final Evaluator Simulation

### Fresh Clone Simulation
- [ ] Delete repository locally
- [ ] Clone from scratch
- [ ] Follow README exactly
- [ ] Note any missing steps
- [ ] Note any unclear instructions

### Setup Verification
- [ ] Install prerequisites (Docker, Ollama)
- [ ] Download Ollama model
- [ ] Start Ollama
- [ ] Copy .env.example to .env
- [ ] Configure .env (verify defaults work)
- [ ] Run `docker compose up`
- [ ] Verify PostgreSQL starts
- [ ] Verify backend starts
- [ ] Verify frontend starts
- [ ] Check health endpoint: http://localhost:8000/health

### Ingestion Verification
- [ ] Run ingestion script
- [ ] Verify transcripts loaded
- [ ] Verify chunks created
- [ ] Verify FAISS index created
- [ ] Check database: transcript_chunks table populated
- [ ] Check files: faiss_index.bin exists

### Feature Testing
- [ ] Open frontend: http://localhost:5173
- [ ] See empty state with example prompts
- [ ] Click "New Chat"
- [ ] Send grounded question: "How to improve retention?"
- [ ] Verify sources appear
- [ ] Verify source citations correct
- [ ] Ask follow-up: "What should we do first?"
- [ ] Verify context preserved
- [ ] Click "New Chat" again
- [ ] Verify second session independent (no bleed)
- [ ] Ask unsupported question: "What's the best blockchain strategy?"
- [ ] Verify insufficient evidence response
- [ ] Request Ship 30 essay: "Turn this into a Ship 30 essay"
- [ ] Verify ~1,250 word essay
- [ ] Verify Ship 30 formatting (hook, bullets, bold)
- [ ] Request Markdown artifact: "Create a retention framework"
- [ ] Verify artifact created
- [ ] Verify artifact viewer opens
- [ ] Request HTML artifact: "Create a dashboard"
- [ ] Verify HTML renders in sandbox
- [ ] Verify code/preview toggle works
- [ ] Try to inject XSS: "<script>alert('XSS')</script>"
- [ ] Verify script doesn't execute

### Provider Testing
- [ ] Verify model indicator shows "ollama · llama3.2:3b"
- [ ] (If Anthropic configured) Switch to Anthropic
- [ ] (If Anthropic configured) Verify responses work
- [ ] Stop Ollama
- [ ] Try to send message
- [ ] Verify friendly error appears
- [ ] Start Ollama
- [ ] Verify recovery

### Tests
- [ ] Run `pytest backend/tests/`
- [ ] Verify all tests pass
- [ ] Check test coverage (optional)

### Logs
- [ ] Check backend logs
- [ ] Verify structured logging
- [ ] Verify request_id present
- [ ] Verify session_id present
- [ ] Verify no secrets logged

### Failure States
- [ ] Stop PostgreSQL container
- [ ] Try to send message
- [ ] Verify graceful error
- [ ] Start PostgreSQL
- [ ] Delete FAISS index file
- [ ] Restart backend
- [ ] Verify error handling

### Security Audit
- [ ] Verify no .env file committed
- [ ] Verify no secrets in git history
- [ ] Verify .gitignore includes sensitive files
- [ ] Verify artifact sandbox works
- [ ] Verify SQL queries parameterized (check code)

### Deliverables Check
- [ ] README.md complete
- [ ] PRD.md complete
- [ ] architecture.md complete
- [ ] design.md complete
- [ ] .env.example complete
- [ ] .gitignore complete
- [ ] docker-compose.yml works
- [ ] tests/ directory populated
- [ ] agent-transcripts/ populated
- [ ] All required features implemented

---

## Final Requirements Audit

### Technology Requirements
- [ ] FastAPI backend ✓
- [ ] Pydantic validation ✓
- [ ] PostgreSQL database ✓
- [ ] SQLAlchemy ORM ✓
- [ ] Database migrations (Alembic) ✓
- [ ] Claude Agent SDK or Pi Coding Agent ✓
- [ ] Ollama integration (mandatory) ✓
- [ ] Cloud LLM (Anthropic) ✓
- [ ] React frontend ✓
- [ ] Modern frontend framework ✓

### Core Features
- [ ] Start new conversation ✓
- [ ] Ask product/growth questions ✓
- [ ] Receive grounded answers ✓
- [ ] See transcript sources ✓
- [ ] Ask follow-up questions (context preserved) ✓
- [ ] Explicit "insufficient evidence" responses ✓
- [ ] Ship 30 for 30 essay generation ✓
- [ ] Markdown artifact generation ✓
- [ ] HTML/CSS artifact generation ✓
- [ ] Artifacts render in-app ✓
- [ ] Switch between Ollama/cloud ✓
- [ ] Provider/model visible in UI ✓

### Agent Architecture
- [ ] Dedicated Grounded Q&A skill ✓
- [ ] Dedicated Ship 30 skill ✓
- [ ] Dedicated Artifact skill ✓
- [ ] Clear skill routing ✓
- [ ] Agent SDK properly implemented ✓

### RAG System
- [ ] Lenny transcripts ingested ✓
- [ ] Transcript chunking implemented ✓
- [ ] Chunk metadata preserved ✓
- [ ] Embeddings generated ✓
- [ ] Retrieval system implemented ✓
- [ ] Source tracking ✓
- [ ] Source attribution ✓

### Security
- [ ] HTML artifacts isolated (sandboxed iframe) ✓
- [ ] XSS prevention ✓
- [ ] No committed secrets ✓
- [ ] .env.example provided ✓
- [ ] .gitignore configured ✓
- [ ] Input validation ✓
- [ ] Parameterized queries ✓
- [ ] Safe Markdown rendering ✓

### Infrastructure
- [ ] Docker Compose ✓
- [ ] One-command startup ✓
- [ ] PostgreSQL in Docker ✓
- [ ] Database migrations ✓
- [ ] Health endpoint ✓
- [ ] Structured logging ✓
- [ ] Error handling ✓

### Frontend Quality
- [ ] Distinctive UI (not generic chatbot) ✓
- [ ] Session sidebar ✓
- [ ] New Chat functionality ✓
- [ ] Message composer ✓
- [ ] Source citations display ✓
- [ ] Artifact viewer ✓
- [ ] Loading states ✓
- [ ] Error states ✓
- [ ] Empty state ✓
- [ ] Responsive design ✓
- [ ] Accessibility (keyboard, contrast, semantic HTML) ✓

### Documentation
- [ ] README.md complete ✓
- [ ] PRD.md ✓
- [ ] architecture.md ✓
- [ ] design.md ✓
- [ ] .env.example ✓
- [ ] Setup instructions ✓
- [ ] Ollama instructions ✓
- [ ] Ingestion instructions ✓
- [ ] Troubleshooting guide ✓
- [ ] Known limitations ✓

### Testing
- [ ] API tests ✓
- [ ] Session tests ✓
- [ ] Retrieval tests ✓
- [ ] Agent routing tests ✓
- [ ] Provider tests ✓
- [ ] Persistence tests ✓
- [ ] Security tests ✓
- [ ] Manual UI test plan ✓

### Demo Readiness
- [ ] Fresh clone → working demo in <10 minutes ✓
- [ ] Ollama demo works without cloud credentials ✓
- [ ] Grounded Q&A demo ready ✓
- [ ] Follow-up question demo ready ✓
- [ ] Source citation demo ready ✓
- [ ] Ship 30 essay demo ready ✓
- [ ] Artifact viewer demo ready ✓
- [ ] Model indicator visible ✓
- [ ] Application looks polished ✓

### Agent Transcripts
- [ ] Development transcripts saved ✓
- [ ] Transcripts organized ✓
- [ ] Secrets removed from transcripts ✓
- [ ] Transcripts show reasoning and decisions ✓

---

## Assignment Requirements Cross-Check

- [ ] FastAPI ✓
- [ ] Claude Agent SDK or Pi Coding Agent ✓
- [ ] PostgreSQL ✓
- [ ] Migrations ✓
- [ ] Ollama (mandatory) ✓
- [ ] Cloud LLM (optional) ✓
- [ ] Provider abstraction ✓
- [ ] Lenny transcripts ✓
- [ ] RAG system ✓
- [ ] Grounded Q&A ✓
- [ ] Source citations ✓
- [ ] Ship 30 skill ✓
- [ ] Artifacts (Markdown, HTML/CSS) ✓
- [ ] Artifact viewer ✓
- [ ] Artifact security ✓
- [ ] Docker Compose ✓
- [ ] Distinctive UI ✓
- [ ] Responsive ✓
- [ ] Accessibility ✓
- [ ] Tests ✓
- [ ] README ✓
- [ ] PRD ✓
- [ ] architecture.md ✓
- [ ] design.md ✓
- [ ] .env.example ✓
- [ ] .gitignore ✓
- [ ] agent-transcripts ✓
- [ ] Demo-ready ✓

---

**Status**: Phase 0 Complete ✅  
**Next Phase**: Phase 1 - Project Foundation  
**Estimated Total Time**: ~36 hours of focused implementation
