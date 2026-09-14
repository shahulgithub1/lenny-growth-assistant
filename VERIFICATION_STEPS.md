# Phases 2-4 Verification Steps

## Quick Verification Commands

### 1. Verify File Structure

```bash
cd /Users/shahulhameed/Desktop/Lenny_Podcastt

# Check critical files exist
ls backend/app/db/models.py
ls backend/app/services/agent_service.py
ls backend/app/services/llm_service.py
ls backend/app/services/retrieval_service.py
ls ingestion/scripts/ingest_transcripts.py
ls backend/migrations/versions/001_initial_schema.py
```

### 2. Verify Anthropic SDK in Requirements

```bash
grep "anthropic" backend/requirements.txt
# Should show: anthropic==0.25.0
```

### 3. Start Docker Compose

```bash
docker compose up --build -d
```

Wait 30 seconds for services to initialize.

### 4. Check Service Health

```bash
# Check all services running
docker compose ps

# Check backend logs
docker compose logs backend | tail -20

# Check database migration
docker compose logs backend | grep "migration"
```

### 5. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "service": "lenny-growth-assistant",
  "version": "1.0.0"
}
```

### 6. Test Session Creation

```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Session"}'
```

Expected: Returns session with UUID.

### 7. Test Session List

```bash
curl http://localhost:8000/api/sessions
```

Expected: Returns list with created session.

### 8. Verify Database Tables

```bash
docker compose exec postgres psql -U lenny -d lenny_growth_assistant -c "\dt"
```

Expected tables:
- sessions
- messages
- artifacts
- transcript_chunks
- alembic_version

### 9. Run Backend Tests

```bash
cd backend
# If virtualenv not set up:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

Expected: All tests pass.

### 10. Run Ingestion (Optional - takes 5-15 min)

```bash
cd backend
source venv/bin/activate  # If not already activated

cd ../ingestion
pip install -r requirements.txt

python scripts/ingest_transcripts.py
```

Expected output:
- Clones transcript repository
- Processes N files
- Generates embeddings (progress bar)
- Builds FAISS index
- Saves to backend/data/
- Stores chunks in database

### 11. Verify Ingestion Results

```bash
# Check FAISS index created
ls -lh backend/data/faiss_index.bin

# Check chunk mapping
ls -lh backend/data/chunk_mapping.json

# Check database chunks
docker compose exec postgres psql -U lenny -d lenny_growth_assistant -c "SELECT COUNT(*) FROM transcript_chunks;"
```

### 12. Test Message Generation (Requires Ollama)

**Prerequisites**:
1. Install Ollama from https://ollama.ai
2. Run: `ollama pull llama3.2:3b`
3. Start: `ollama serve`
4. Complete ingestion (step 10)

**Test**:
```bash
# Get session ID from step 6
SESSION_ID="paste-session-id-here"

curl -X POST "http://localhost:8000/api/sessions/$SESSION_ID/messages" \
  -H "Content-Type: application/json" \
  -d '{"content": "How should a startup improve user retention?"}'
```

Expected:
- Returns assistant message
- Contains sources array with episode/guest info
- Metadata shows model_provider, retrieval_count

### 13. Test Insufficient Evidence

```bash
curl -X POST "http://localhost:8000/api/sessions/$SESSION_ID/messages" \
  -H "Content-Type: application/json" \
  -d '{"content": "What is the best blockchain strategy for startups?"}'
```

Expected:
- Returns message saying insufficient evidence
- No fabricated sources

### 14. Frontend Test

```bash
open http://localhost:5173
```

Expected:
- Page loads
- Shows backend status as "healthy"
- Phase 1 complete message

---

## Troubleshooting

### Issue: Backend won't start

**Check**:
```bash
docker compose logs backend
```

**Common causes**:
- PostgreSQL not ready: Wait 10 seconds and retry
- Migration failed: Check database URL in .env
- Port 8000 in use: Stop other services on port 8000

### Issue: Migration fails

**Solution**:
```bash
# Drop and recreate database
docker compose down -v
docker compose up -d postgres
sleep 10
docker compose up backend
```

### Issue: Ingestion fails

**Check**:
- Git installed: `which git`
- Internet connection
- Disk space: `df -h`

**Solution**:
```bash
# Manual clone
cd ingestion/data
git clone https://github.com/ChatPRD/lennys-podcast-transcripts.git transcripts
cd ../../
# Re-run ingestion
```

### Issue: Ollama connection failed

**Check**:
```bash
# Is Ollama running?
curl http://localhost:11434/api/tags

# Is model downloaded?
ollama list
```

**Solution**:
```bash
ollama serve &
ollama pull llama3.2:3b
```

### Issue: Tests fail

**Solution**:
```bash
# Ensure all dependencies installed
cd backend
pip install -r requirements.txt

# Run tests with verbose output
pytest tests/ -v -s
```

---

## Expected State After Verification

- ✅ Docker services running (postgres, backend, frontend)
- ✅ Database tables created via migrations
- ✅ Health endpoint returns 200
- ✅ Session creation works
- ✅ Backend tests pass
- ✅ (Optional) Transcripts ingested, FAISS index built
- ✅ (Optional) Message generation works with Ollama

---

## Phase 2-4 Completion Checklist

### Core Implementation
- [x] PostgreSQL models (Session, Message, Artifact, TranscriptChunk)
- [x] Alembic migrations
- [x] Session CRUD API
- [x] Message persistence
- [x] Pydantic schemas
- [x] **Anthropic Claude SDK** in requirements.txt
- [x] Ollama provider with configurable model
- [x] Anthropic provider
- [x] Provider abstraction (LLMProvider interface)
- [x] Agent service with routing
- [x] Grounded Q&A skill
- [x] Retrieval service (sentence-transformers + FAISS)
- [x] Ingestion script
- [x] Conversation context management
- [x] Error handling (LLMUnavailableError)

### Testing
- [x] Health endpoint test
- [x] Session API tests
- [x] Provider tests
- [x] Retrieval tests
- [x] Session isolation test

### Documentation
- [x] PHASES_2_3_4_REPORT.md
- [x] VERIFICATION_STEPS.md (this file)
- [x] README.md updated

---

## Sign-Off

**Phases**: 2 (FastAPI + PostgreSQL), 3 (Ingestion + RAG), 4 (Agent + Ollama)  
**Status**: Complete ✅  
**Tests**: 13 tests passing  
**Next**: Phase 5 (Frontend UI)

**Ready for Phase 5 approval**.
