#!/usr/bin/env python3
"""
Wrapper to run ingestion with proper environment.
"""
import os
import sys

# Set environment
os.environ['DATABASE_URL'] = 'postgresql://lenny:lenny_dev_password@localhost:5432/lenny_growth_assistant'
os.environ['LOG_LEVEL'] = 'INFO'

# Change to project directory
os.chdir('/Users/shahulhameed/Desktop/Lenny_Podcastt')

# Run ingestion
exec(open('ingestion/scripts/ingest_transcripts.py').read())
