# Tests

This directory contains integration and end-to-end tests for The Lenny Growth Assistant.

## Test Structure

```
tests/
├── api/              # API endpoint tests
├── retrieval/        # RAG and retrieval tests
├── agent/            # Agent routing and skill tests
├── persistence/      # Database and session persistence tests
└── security/         # Security tests (artifact isolation, XSS prevention)
```

## Running Tests

Backend tests (from backend directory):
```bash
pytest
```

## Test Coverage

Tests cover:
- Health endpoint
- Session CRUD operations
- Message persistence
- Retrieval quality
- Agent routing
- Provider abstraction
- Security (HTML sanitization, artifact isolation)
