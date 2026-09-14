# Agent Transcripts

This directory contains transcripts and logs from AI coding agent sessions used during development of The Lenny Growth Assistant.

## Purpose

These transcripts demonstrate:
- Important implementation decisions
- Debugging sessions
- Failed attempts and how they were corrected
- Verification steps
- Design choices

## Sessions

### kiro-sessions/lenny-growth-assistant-build.jsonl

The primary build session. Kiro (using Claude Sonnet 4.5) was used as the coding agent to scaffold the backend, frontend, ingestion pipeline, retrieval layer, agent service, and tests.

Format: JSON Lines (jsonl), one event per line. Each event has:
- id: unique event ID
- timestamp: ISO 8601 time
- payload.type: user, assistant, tool_call, or tool_result
- payload.content (for messages) or payload.toolName / payload.args (for tools)

## Privacy

All secrets, API keys, and sensitive information have been removed or verified absent. The only credential strings present are the fake local development credentials (lenny_dev_password) that are already public in .env.example.

## Note on failed attempts

Kiro's session includes multiple iterations, corrections, and dead-ends (e.g., retrieval threshold tuning, FAISS index path resolution, Docker volume shadowing). These are preserved intentionally to show the debugging process, not just the final state.
