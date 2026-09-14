#!/usr/bin/env python3
"""
Test script to verify retrieval queries work correctly.
"""
import os
import sys
from pathlib import Path

# Change to project directory
project_dir = Path('/Users/shahulhameed/Desktop/Lenny_Podcastt')
os.chdir(project_dir)

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://lenny:lenny_dev_password@localhost:5432/lenny_growth_assistant'
os.environ['LOG_LEVEL'] = 'INFO'
os.environ['MODEL_PROVIDER'] = 'ollama'
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434'
os.environ['RETRIEVAL_THRESHOLD'] = '0.25'
os.environ['RETRIEVAL_TOP_K'] = '5'

# Add backend to path
sys.path.insert(0, str(project_dir / 'backend'))

from app.services.retrieval_service import RetrievalService

print("=" * 70)
print("Testing RAG Retrieval")
print("=" * 70)
print()

# Initialize retrieval service
service = RetrievalService()

# Test queries
queries = [
    "What are the key principles of growth loops?",
    "How should a startup improve retention?"
]

for query in queries:
    print(f"Query: {query}")
    print("-" * 70)
    
    try:
        results = service.retrieve_chunks(query, top_k=5)
        
        if not results:
            print("❌ No results returned")
        else:
            print(f"✅ Retrieved {len(results)} chunks")
            
            for i, result in enumerate(results, 1):
                score = result.get('score', 'N/A')
                score_str = f"{score:.3f}" if isinstance(score, (int, float)) else str(score)
                print(f"\n[{i}] Score: {score_str} | Method: {result.get('retrieval_method', 'N/A')}")
                print(f"    Episode: {result.get('episode_title', 'N/A')}")
                print(f"    Guest: {result.get('guest', 'N/A')}")
                print(f"    Source: {result.get('source_file', 'N/A')}")
                content_preview = result.get('content', '')[:150].replace('\n', ' ')
                print(f"    Content: {content_preview}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)
    print()

print("Testing complete!")
