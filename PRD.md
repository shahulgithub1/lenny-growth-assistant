# Product Requirements Document: The Lenny Growth Assistant

## Executive Summary

The Lenny Growth Assistant is an AI-powered conversational research tool designed for product and growth professionals who need actionable insights grounded in Lenny Rachitsky's extensive podcast library. Unlike generic AI chatbots, this assistant provides verified, sourced answers with complete transparency, helps transform insights into publication-ready content, and enables rapid artifact generation—all while running entirely locally or with optional cloud enhancement.

---

## User and Problem

### Target User

**Primary Persona: Product/Growth Professional**
- Role: Product Manager, Growth Lead, Founder, or Strategy Lead
- Context: Building or scaling a product
- Pain: Scattered across hundreds of hours of Lenny's content
- Need: Fast, credible answers with clear source attribution

### Problems Solved

1. **Time Investment**: Reading/watching hundreds of hours of Lenny's content is impractical
2. **Source Credibility**: Generic AI tools invent plausible-sounding but unsourced advice
3. **Context Loss**: Switching between research and content creation breaks flow
4. **Artifact Creation**: Converting insights into actionable formats (essays, frameworks, dashboards) is manual work
5. **Privacy/Cost**: Cloud-only solutions raise data privacy and cost concerns

### Value Proposition

A trustworthy AI research assistant that:
- Answers product/growth questions using **only** Lenny's verified content
- Shows exact sources for every claim
- Transforms research into Ship 30 for 30-style essays
- Generates interactive artifacts (Markdown, HTML/CSS)
- Works completely offline with local models
- Maintains conversation context across follow-ups

---

## Success Metrics

### Product Metrics (Target)

1. **Citation Coverage Rate**: ≥95% of grounded answers include at least one source citation
2. **Answer Confidence**: User satisfaction with "I don't know" responses when evidence is insufficient (target: users prefer honest "insufficient evidence" over hallucinated answers)
3. **Multi-turn Success**: ≥80% of follow-up questions successfully use prior context
4. **Artifact Generation Success**: ≥90% of requested artifacts render correctly in viewer
5. **Session Isolation**: 100% of sessions maintain independent context (no cross-session leakage)

### Operational Metrics (Target)

1. **Response Latency (P95)**:
   - Ollama (local): <30s for grounded Q&A
   - Cloud (Anthropic): <10s for grounded Q&A
2. **System Availability**: ≥99% health endpoint uptime
3. **Ingestion Success**: 100% of Lenny transcripts successfully chunked and indexed
4. **Artifact Security**: 0 XSS vulnerabilities in artifact viewer
5. **Startup Reliability**: Fresh clone → running demo in <10 minutes

### Evaluation Metrics

1. **Setup Time**: Time from `git clone` to working demo
2. **Documentation Clarity**: Evaluator can run without external help
3. **UI Polish**: Product feels production-ready, not prototype
4. **Failure Handling**: Graceful degradation when Ollama/cloud unavailable

---

## Assumptions

### Technical Assumptions

1. **Local Environment**: Evaluator has Docker, Docker Compose, and can install Ollama
2. **Hardware**: Evaluator's machine can run a small-to-medium Ollama model (e.g., 7B-13B parameters)
3. **Network**: Evaluator can clone GitHub repos and optionally access Anthropic API
4. **Storage**: ~10GB available for Docker images, models, and transcripts

### Product Assumptions

1. **Knowledge Scope**: Lenny's transcripts provide sufficient coverage for common product/growth questions
2. **User Intent**: Users prefer "I don't know" over confident but unsourced answers
3. **Ship 30 Value**: Product/growth professionals value the specific Ship 30 for 30 writing framework
4. **Artifact Use Case**: Users want to quickly generate shareable documents/dashboards from research

### Business Assumptions

1. **Evaluation Context**: This is a take-home assignment, not production software
2. **Auth Not Required**: Single-user local deployment (no multi-tenant auth)
3. **Scale**: Optimized for single user, not thousands of concurrent users
4. **Data Freshness**: Static transcript corpus (no real-time updates required)

---

## Scope

### ✅ In Scope

#### Core Features
- [x] Conversational Q&A grounded in Lenny's transcripts
- [x] Source citation display with episode/guest metadata
- [x] Multi-turn conversation with context preservation
- [x] Independent session management
- [x] "Insufficient evidence" responses when knowledge base lacks support
- [x] Ship 30 for 30-style essay generation (1,250 words)
- [x] Markdown artifact generation
- [x] HTML/CSS artifact generation
- [x] In-app artifact viewer with rendering
- [x] Model provider abstraction (Ollama + Cloud)
- [x] Provider/model visibility in UI

#### Infrastructure
- [x] FastAPI backend with Pydantic validation
- [x] PostgreSQL with migrations
- [x] Docker Compose one-command startup
- [x] Ollama local LLM integration (mandatory)
- [x] Optional Anthropic cloud LLM
- [x] Structured logging and observability
- [x] Health/diagnostics endpoints

#### Ingestion & RAG
- [x] Lenny transcript ingestion pipeline
- [x] Chunking with metadata preservation
- [x] Retrieval system (practical, not over-engineered)
- [x] Source tracking and attribution

#### Agent Architecture
- [x] Claude Agent SDK or Pi Coding Agent
- [x] Dedicated skill: Grounded Q&A
- [x] Dedicated skill: Ship 30 for 30 essay generation
- [x] Dedicated skill: Artifact generation
- [x] Clear routing between skills

#### Security
- [x] Artifact HTML isolation (XSS prevention)
- [x] No committed secrets (.env.example, .gitignore)
- [x] Input validation and parameterized queries
- [x] Safe Markdown/HTML rendering

#### Frontend
- [x] Distinctive, polished UI (not generic ChatGPT clone)
- [x] Session sidebar with history
- [x] New Chat functionality
- [x] Message composer
- [x] Source citation display
- [x] Artifact viewer panel
- [x] Loading/error/empty states
- [x] Responsive design
- [x] Accessibility (keyboard nav, contrast, semantic HTML)

#### Documentation & Testing
- [x] README.md with setup instructions
- [x] PRD.md (this document)
- [x] architecture.md
- [x] design.md
- [x] .env.example
- [x] Automated tests (API, sessions, retrieval, agent, security)
- [x] Manual UI test plan
- [x] Agent transcripts/logs

### ❌ Out of Scope

#### Authentication & Multi-tenancy
- User authentication/login (single-user local deployment)
- User registration
- Team/organization features
- Role-based access control
- API keys per user

**Reason**: Assignment is for local demo, not multi-user SaaS. Auth adds complexity without evaluator value.

#### Advanced RAG Features
- Hybrid search (keyword + semantic)
- Reranking models
- Query decomposition
- Self-querying retrieval
- Retrieval evaluation framework

**Reason**: Start with practical retrieval. Add complexity only if needed.

#### Real-time Updates
- Live transcript ingestion
- Webhook-based updates
- Scheduled refresh
- Change detection

**Reason**: Static corpus is sufficient for demo.

#### Advanced Artifact Features
- Artifact versioning
- Artifact collaboration
- Artifact export (PDF, etc.)
- Artifact templates library
- Interactive charts/visualizations

**Reason**: Core artifact rendering is sufficient to demonstrate capability.

#### Production Operations
- Kubernetes deployment
- Auto-scaling
- Multi-region deployment
- CDN integration
- Rate limiting per user
- Usage analytics dashboard

**Reason**: Docker Compose local deployment is appropriate for take-home assignment.

#### Model Fine-tuning
- Custom model training
- Fine-tuning on Lenny transcripts
- Model evaluation suite
- A/B testing infrastructure

**Reason**: Off-the-shelf models with good prompting are sufficient.

#### Mobile App
- Native iOS/Android apps
- Mobile-specific features
- Offline mobile sync

**Reason**: Responsive web UI is sufficient.

---

## User Flows

### Flow 1: New User First Session

1. User opens application
2. Sees polished empty state with example prompts
3. Sees model indicator (e.g., "Ollama - llama3.2")
4. Clicks example prompt or types question: *"How should a startup improve user retention?"*
5. Loading state appears (streaming or spinner)
6. Assistant retrieves relevant transcript chunks
7. Assistant generates grounded answer with citations
8. User sees formatted response with source cards
9. Source cards show: episode title, guest, relevant excerpt
10. User clicks source to see more context

**Success**: User understands the product immediately, receives grounded answer with clear sources.

### Flow 2: Follow-up Question

1. User has existing conversation (Flow 1)
2. User asks follow-up: *"What would Lenny recommend doing first?"*
3. Assistant understands context (prior question about retention)
4. Assistant retrieves additional context if needed
5. Assistant generates contextual answer referencing prior discussion
6. User sees coherent multi-turn conversation

**Success**: Context preserved, no need to repeat information.

### Flow 3: Unsupported Question

1. User asks: *"What's the best marketing strategy for blockchain startups?"*
2. Assistant searches knowledge base
3. Retrieval returns insufficient evidence
4. Assistant responds honestly: *"I don't have enough information in Lenny's transcripts to answer this confidently. The available content doesn't specifically address blockchain marketing strategies."*
5. Assistant optionally suggests related topics that ARE covered

**Success**: User trusts system more due to honesty, no hallucinated sources.

### Flow 4: Ship 30 Essay Generation

1. User has grounded conversation about product-market fit
2. User requests: *"Turn this into a Ship 30 for 30 essay"*
3. System routes to Ship 30 skill
4. Skill applies writing principles (hook, skimmable format, bold emphasis, ~1,250 words)
5. Essay generated using grounded information from conversation
6. User sees formatted essay with:
   - Strong opening hook
   - Clear narrative
   - Bullet points and bold emphasis
   - Specific takeaways
   - Source grounding
7. Essay renders beautifully in chat or artifact viewer

**Success**: Publication-ready content generated from research in seconds.

### Flow 5: Artifact Generation (HTML Dashboard)

1. User has conversation about growth metrics
2. User requests: *"Create a one-page growth strategy dashboard"*
3. System routes to artifact skill
4. Skill generates HTML/CSS artifact
5. Artifact viewer panel opens (slides in on desktop)
6. HTML renders in sandboxed iframe
7. User sees interactive dashboard with:
   - Proper styling
   - Organized sections
   - Professional appearance
8. User can inspect artifact code if needed

**Success**: Interactive artifact rendered safely, useful output.

### Flow 6: New Chat (Session Isolation)

1. User has existing conversation about retention
2. User clicks "New Chat" button
3. New session created with fresh context
4. Sidebar shows both sessions
5. User asks about pricing strategy
6. Assistant has no memory of retention conversation
7. User can switch between sessions
8. Each session maintains independent context

**Success**: Clean separation, no context bleed.

### Flow 7: Model Switching (Optional)

1. User sees current model indicator: "Ollama - llama3.2"
2. User has configured ANTHROPIC_API_KEY
3. User switches to "Anthropic - Claude Sonnet"
4. Model indicator updates
5. Subsequent questions use Claude
6. User can switch back to Ollama

**Success**: Seamless provider switching, clear visibility.

### Flow 8: Error Handling (Ollama Unavailable)

1. User starts application without Ollama running
2. User asks question
3. Backend detects Ollama connection failure
4. User sees friendly error: *"Unable to connect to Ollama. Please ensure Ollama is running and the model is downloaded."*
5. Error includes link to troubleshooting section
6. User starts Ollama
7. User retries question
8. System works normally

**Success**: Clear error message, actionable guidance, no crash.

---

## Acceptance Criteria

### Core Functionality
- [ ] User can start new conversation
- [ ] User can ask product/growth question
- [ ] Assistant provides grounded answer with citations
- [ ] Sources display episode, guest, and excerpt
- [ ] User can ask follow-up question with preserved context
- [ ] Assistant explicitly states when evidence is insufficient
- [ ] User can generate Ship 30 for 30 essay (~1,250 words)
- [ ] Essay follows Ship 30 principles (hook, skimmable, bold, narrative)
- [ ] User can generate Markdown artifact
- [ ] User can generate HTML/CSS artifact
- [ ] Artifacts render in in-app viewer
- [ ] User can switch between Ollama and cloud provider
- [ ] Current provider/model visible in UI
- [ ] Multiple sessions remain independent

### Technical Requirements
- [ ] FastAPI backend with Pydantic validation
- [ ] PostgreSQL with migrations
- [ ] Claude Agent SDK or Pi Coding Agent implemented
- [ ] Ollama integration works (mandatory)
- [ ] Anthropic integration works (optional)
- [ ] Model provider abstraction implemented
- [ ] Lenny transcripts ingested from GitHub repo
- [ ] Transcripts chunked with metadata
- [ ] Retrieval returns relevant chunks
- [ ] Source metadata preserved
- [ ] Agent routes to correct skill
- [ ] Grounded Q&A skill implemented
- [ ] Ship 30 skill implemented
- [ ] Artifact skill implemented

### Security
- [ ] HTML artifacts isolated (XSS prevention)
- [ ] No secrets committed
- [ ] .env.example provided
- [ ] .gitignore includes .env
- [ ] Input validation implemented
- [ ] Parameterized database queries
- [ ] Safe Markdown rendering
- [ ] Artifact cannot access parent frame
- [ ] Artifact cannot execute server-side code

### Infrastructure
- [ ] docker-compose.yml provided
- [ ] `docker compose up` starts all services
- [ ] PostgreSQL runs in Docker
- [ ] Database migrations run automatically or via clear command
- [ ] Health endpoint returns 200 when healthy
- [ ] Structured logging implemented
- [ ] Errors logged with context (session_id, request_id)

### Frontend
- [ ] UI is distinctive (not generic ChatGPT clone)
- [ ] Empty state shows example prompts
- [ ] Session sidebar with history
- [ ] New Chat button creates fresh session
- [ ] Message composer with send button
- [ ] Messages render with clear hierarchy
- [ ] Source citations display prominently
- [ ] Artifact viewer opens beside conversation
- [ ] Loading states show during generation
- [ ] Error states show friendly messages
- [ ] Responsive layout works on smaller screens
- [ ] Keyboard navigation works for main controls
- [ ] Sufficient color contrast (WCAG AA)

### Documentation
- [ ] README.md with complete setup instructions
- [ ] Exact Ollama installation commands
- [ ] Exact model download commands
- [ ] Exact ingestion commands
- [ ] Troubleshooting section
- [ ] PRD.md (this document)
- [ ] architecture.md with diagrams
- [ ] design.md with UI rationale
- [ ] .env.example with comments
- [ ] Known limitations documented

### Testing
- [ ] API tests (health, validation, errors)
- [ ] Session tests (create, retrieve, isolation)
- [ ] Retrieval tests (relevant query returns relevant chunk)
- [ ] Agent routing tests
- [ ] Provider tests (Ollama, Anthropic, missing provider)
- [ ] Persistence tests (sessions, messages, artifacts)
- [ ] Security tests (unsafe artifact handling)
- [ ] Manual UI test plan documented

### Demo Readiness
- [ ] Fresh clone → working demo in <10 minutes
- [ ] Ollama demo works without cloud credentials
- [ ] Grounded Q&A demo ready
- [ ] Follow-up question demo ready
- [ ] Ship 30 essay demo ready
- [ ] Artifact viewer demo ready
- [ ] Source citation demo ready
- [ ] Model indicator visible
- [ ] Application looks polished in 2-3 minute demo

---

## Risks and Trade-offs

### Risk 1: Hallucination / Unsupported Claims
**Description**: LLM may generate plausible-sounding but unsupported claims.

**Mitigation**:
- Strict prompt engineering: "Only use provided transcript chunks"
- Post-processing validation: Check that citations exist
- "Insufficient evidence" responses when retrieval is weak
- Clear source attribution for every claim

**Residual Risk**: LLM may still misinterpret source material. Evaluator review is final verification.

### Risk 2: Retrieval Quality
**Description**: Retrieval may miss relevant content or return irrelevant chunks.

**Mitigation**:
- Chunking strategy preserves context (overlap, metadata)
- Retrieval returns top-K with configurable K
- Test retrieval with known queries
- Document chunking/retrieval strategy in architecture.md

**Trade-off**: Simple retrieval (embeddings + cosine similarity) vs. complex hybrid search. Choosing simple for demo reliability.

### Risk 3: Local Model Quality (Ollama)
**Description**: Smaller Ollama models may produce lower-quality responses than Claude.

**Mitigation**:
- Choose reasonable Ollama model (e.g., llama3.2:8B or mixtral)
- Optimize prompts for smaller models
- Provide cloud option for better quality
- Document model choice in architecture.md

**Trade-off**: Model size vs. accessibility. Assignment requires Ollama demo, so we optimize for reliability over maximum quality.

### Risk 4: Response Latency
**Description**: Ollama may take 20-30s for complex queries, frustrating users.

**Mitigation**:
- Clear loading states with streaming if practical
- Set user expectation in empty state ("Thoughtful answers take a moment")
- Optimize chunk count passed to LLM
- Optional cloud provider for faster responses

**Trade-off**: Response quality vs. speed. We prioritize quality (grounded answers) over speed.

### Risk 5: Ollama/Cloud Service Unavailable
**Description**: Services may be down, misconfigured, or unreachable.

**Mitigation**:
- Graceful error handling with actionable messages
- Health checks for Ollama connectivity
- Retry logic with exponential backoff
- Clear troubleshooting documentation
- Fallback behavior (no silent crashes)

**Trade-off**: Complexity vs. resilience. We implement basic retry/error handling, not full circuit breaker patterns.

### Risk 6: Database Failure
**Description**: PostgreSQL may crash, run out of storage, or have connection issues.

**Mitigation**:
- Health endpoint checks database connectivity
- Connection pooling with timeouts
- Graceful error messages to user
- Docker volume persistence

**Trade-off**: Single database instance (no replication) is appropriate for local demo.

### Risk 7: Prompt Injection
**Description**: User may attempt to manipulate agent via prompt injection.

**Mitigation**:
- System prompt clearly separates instructions from user input
- Input validation and sanitization
- Clear boundary between retrieval content and user questions
- Document limitation in architecture.md

**Residual Risk**: Sophisticated prompt injection may still succeed. This is an acceptable limitation for demo.

### Risk 8: Unsafe HTML Artifacts
**Description**: Generated HTML may contain XSS, malicious scripts, or parent frame access.

**Mitigation**:
- Sandboxed iframe with restricted sandbox attributes
- Content Security Policy headers
- No inline JavaScript allowed
- HTML sanitization if practical
- Document security model in architecture.md

**Residual Risk**: Complex attacks may bypass sandbox. Evaluator should not execute malicious prompts.

### Risk 9: Data Leakage
**Description**: Sessions may leak context between users (in future multi-user scenario).

**Mitigation**:
- Session isolation via unique session_id
- Database queries filter by session_id
- Automated test: verify session independence
- Clear session boundaries in code

**Trade-off**: Single-user demo doesn't face true multi-tenancy risk, but we design defensively.

### Risk 10: Ingestion Failure
**Description**: Transcript ingestion may fail due to format changes, network issues, or parsing errors.

**Mitigation**:
- Ingestion script with clear error messages
- Validation: check chunk count after ingestion
- Document expected transcript format
- Manual verification of ingestion success

**Trade-off**: No auto-retry or monitoring (appropriate for one-time ingestion).

### Risk 11: Ship 30 Quality
**Description**: Generated essays may not match Ship 30 quality standards.

**Mitigation**:
- Study Ship 30 for 30 guide thoroughly
- Encode principles explicitly in skill prompt
- Test with multiple examples
- Iterate on prompt engineering
- Document Ship 30 principles in agent code

**Trade-off**: LLM may interpret principles differently than human writer. We optimize prompt, accept LLM limitations.

### Risk 12: Artifact Rendering Inconsistency
**Description**: Generated HTML/CSS may render differently across browsers or break layout.

**Mitigation**:
- Test artifact viewer in Chrome/Safari/Firefox
- Use standard HTML/CSS (no experimental features)
- Responsive artifact viewer
- Fallback: display code if rendering fails

**Trade-off**: We test major browsers but can't guarantee all edge cases.

### Risk 13: Setup Complexity
**Description**: Evaluator may struggle with Docker, Ollama, or environment setup.

**Mitigation**:
- Clear step-by-step README
- .env.example with comments
- Troubleshooting section
- Exact commands (copy-paste ready)
- Health endpoint for diagnostics

**Trade-off**: We document clearly but can't control evaluator's environment.

---

## Implementation Plan

### Phase 0: Discovery and Planning ✓
- [x] Analyze requirements
- [x] Make architectural decisions
- [x] Create PRD.md
- [x] Create architecture.md
- [x] Create design.md
- [x] Define implementation checklist

### Phase 1: Project Foundation
- [ ] Initialize repository structure
- [ ] Set up backend/FastAPI skeleton
- [ ] Set up frontend skeleton
- [ ] Set up agent skeleton
- [ ] Create Docker Compose configuration
- [ ] Create .env.example
- [ ] Create .gitignore
- [ ] Verify everything starts

### Phase 2: FastAPI + PostgreSQL
- [ ] Define database schema
- [ ] Create migration scripts
- [ ] Implement models (Session, Message, Artifact, TranscriptChunk)
- [ ] Implement health endpoint
- [ ] Implement session CRUD API
- [ ] Implement message API
- [ ] Implement validation with Pydantic
- [ ] Implement structured error responses
- [ ] Write API tests
- [ ] Verify persistence

### Phase 3: Transcript Ingestion
- [ ] Clone Lenny transcript repo
- [ ] Implement transcript loader
- [ ] Implement cleaning logic
- [ ] Implement chunking with overlap
- [ ] Preserve metadata (episode, guest, filename)
- [ ] Implement indexing (embeddings)
- [ ] Implement retrieval function
- [ ] Create ingestion CLI command
- [ ] Test retrieval with known queries
- [ ] Document ingestion process

### Phase 4: Agent + Ollama
- [ ] Implement LLM provider abstraction
- [ ] Implement Ollama provider
- [ ] Set up agent framework (Claude SDK or Pi)
- [ ] Implement grounded Q&A skill
- [ ] Integrate retrieval into Q&A skill
- [ ] Implement source citation extraction
- [ ] Implement session context management
- [ ] Implement "insufficient evidence" logic
- [ ] Handle Ollama failures gracefully
- [ ] Test end-to-end with Ollama

### Phase 5: Frontend
- [ ] Design component structure
- [ ] Implement design system (typography, colors, spacing)
- [ ] Implement session sidebar
- [ ] Implement New Chat button
- [ ] Implement message composer
- [ ] Implement message display
- [ ] Implement source citation cards
- [ ] Implement model indicator
- [ ] Implement loading states
- [ ] Implement error states
- [ ] Implement empty state with examples
- [ ] Make responsive
- [ ] Add keyboard navigation
- [ ] Test accessibility

### Phase 6: Ship 30 Skill
- [ ] Study Ship 30 for 30 guide
- [ ] Document Ship 30 principles
- [ ] Implement Ship 30 skill
- [ ] Integrate with agent routing
- [ ] Test essay generation
- [ ] Verify ~1,250 word count
- [ ] Verify formatting (hook, bullets, bold, narrative)
- [ ] Verify grounding in sources

### Phase 7: Artifacts
- [ ] Implement artifact generation skill
- [ ] Implement Markdown generation
- [ ] Implement HTML/CSS generation
- [ ] Implement artifact persistence
- [ ] Implement artifact viewer component
- [ ] Implement sandboxed iframe rendering
- [ ] Implement artifact panel (responsive)
- [ ] Test XSS prevention
- [ ] Test artifact rendering
- [ ] Document security model

### Phase 8: Cloud Model
- [ ] Implement Anthropic provider
- [ ] Implement provider switching logic
- [ ] Update UI to show provider/model
- [ ] Handle missing API key gracefully
- [ ] Test Anthropic integration
- [ ] Verify Ollama still works without cloud credentials
- [ ] Document cloud setup

### Phase 9: Hardening
- [ ] Implement structured logging
- [ ] Add request_id/session_id to logs
- [ ] Implement error handling throughout
- [ ] Implement retry logic for LLM calls
- [ ] Handle all failure scenarios gracefully
- [ ] Review security (input validation, SQL injection, XSS)
- [ ] Write remaining tests (retrieval, agent, security)
- [ ] Optimize performance where needed
- [ ] Test failure modes

### Phase 10: Documentation
- [ ] Write comprehensive README.md
- [ ] Finalize architecture.md with diagrams
- [ ] Finalize design.md with UI rationale
- [ ] Create .env.example with detailed comments
- [ ] Write troubleshooting guide
- [ ] Write manual UI test plan
- [ ] Document known limitations
- [ ] Collect agent transcripts

### Phase 11: Final Evaluator Simulation
- [ ] Fresh clone simulation
- [ ] Follow README exactly
- [ ] Test all user flows
- [ ] Test all failure modes
- [ ] Verify no secrets committed
- [ ] Run all automated tests
- [ ] Verify demo readiness
- [ ] Final requirements audit

---

## Open Questions (To Be Resolved)

1. **Agent Framework**: Claude Agent SDK vs. Pi Coding Agent?
   - Decision: Evaluate both for cleanest implementation
   - Lean toward Claude SDK if Anthropic is primary cloud provider

2. **Retrieval Strategy**: Simple embeddings vs. hybrid search?
   - Decision: Start simple, add complexity only if needed
   - Likely: OpenAI embeddings (text-embedding-3-small) or sentence-transformers

3. **Ollama Model**: Which model for demo?
   - Options: llama3.2:8B, mistral:7B, mixtral:8x7b
   - Decision: Balance quality, speed, accessibility

4. **Frontend Framework**: React+Next.js vs. React+Vite vs. alternative?
   - Decision: React+Vite (simpler for local demo, fast dev experience)
   - Next.js if SSR/routing provides clear benefit

5. **Artifact Isolation**: Sandboxed iframe vs. HTML sanitization vs. both?
   - Decision: Sandboxed iframe as primary defense, sanitization as secondary

6. **Streaming**: Implement SSE streaming or simple request/response?
   - Decision: Streaming if reliable with chosen agent framework, otherwise simple

---

## Timeline Estimate (Implementation)

- **Phase 1**: 2 hours
- **Phase 2**: 3 hours
- **Phase 3**: 3 hours
- **Phase 4**: 4 hours
- **Phase 5**: 6 hours
- **Phase 6**: 2 hours
- **Phase 7**: 4 hours
- **Phase 8**: 2 hours
- **Phase 9**: 4 hours
- **Phase 10**: 3 hours
- **Phase 11**: 3 hours

**Total Estimated**: ~36 hours of focused engineering

---

## Appendix: Key Assignment Requirements Mapping

| Requirement | PRD Section | Status |
|------------|-------------|--------|
| FastAPI backend | Technical Requirements, Phase 2 | Planned |
| PostgreSQL | Technical Requirements, Phase 2 | Planned |
| Claude Agent SDK or Pi | Technical Requirements, Phase 4 | Planned |
| Ollama (mandatory) | Technical Requirements, Phase 4 | Planned |
| Cloud LLM (optional) | Technical Requirements, Phase 8 | Planned |
| Lenny transcripts | Technical Requirements, Phase 3 | Planned |
| RAG system | Technical Requirements, Phase 3-4 | Planned |
| Grounded Q&A | In Scope, Flow 1-3 | Planned |
| Source citations | In Scope, Flow 1 | Planned |
| Ship 30 skill | In Scope, Flow 4, Phase 6 | Planned |
| Markdown artifacts | In Scope, Phase 7 | Planned |
| HTML/CSS artifacts | In Scope, Phase 7 | Planned |
| Artifact viewer | In Scope, Flow 5, Phase 7 | Planned |
| Artifact security | Security, Risk 8, Phase 7 | Planned |
| Distinctive UI | In Scope, Phase 5 | Planned |
| Docker Compose | In Scope, Phase 1 | Planned |
| Tests | In Scope, Phase 2-9 | Planned |
| Documentation | In Scope, Phase 10 | Planned |
| README | Documentation, Phase 10 | Planned |
| PRD | This document | ✓ |
| architecture.md | Phase 0 | Next |
| design.md | Phase 0 | Next |

---

**Document Version**: 1.0  
**Last Updated**: Phase 0 - Initial Planning  
**Status**: Ready for Architecture & Design Planning
