#!/usr/bin/env python3
"""
Wrapper to run ingestion with proper environment and error handling.
"""
import os
import sys
from pathlib import Path

# Change to project directory
project_dir = Path('/Users/shahulhameed/Desktop/Lenny_Podcastt')
os.chdir(project_dir)

# Set ONLY the environment variables needed by the app (not Docker Compose vars)
# This prevents pydantic validation errors from extra env vars
os.environ['DATABASE_URL'] = 'postgresql://lenny:lenny_dev_password@localhost:5432/lenny_growth_assistant'
os.environ['LOG_LEVEL'] = 'INFO'
os.environ['MODEL_PROVIDER'] = 'ollama'
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434'

# Remove any .env file loading to avoid validation errors
# The ingestion script will use environment variables directly
if 'DOT_ENV_PATH' in os.environ:
    del os.environ['DOT_ENV_PATH']

# Add backend to path
sys.path.insert(0, str(project_dir / 'backend'))

print("=" * 60)
print("Starting Lenny Transcript Ingestion")
print("=" * 60)
print()

try:
    # Import and run the ingestion script
    from ingestion.scripts.ingest_transcripts import main
    main()
    print()
    print("=" * 60)
    print("Ingestion completed successfully!")
    print("=" * 60)
except Exception as e:
    print()
    print("=" * 60)
    print(f"ERROR: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
