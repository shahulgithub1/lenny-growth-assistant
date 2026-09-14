#!/bin/bash
# Run transcript ingestion

set -e

echo "Starting transcript ingestion..."
echo ""

cd ingestion
python scripts/ingest_transcripts.py

echo ""
echo "Ingestion complete!"
