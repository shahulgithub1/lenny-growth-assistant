#!/usr/bin/env python3
"""Final retrieval test after hybrid implementation."""
import os
import sys
from pathlib import Path

project_dir = Path('/Users/shahulhameed/Desktop/Lenny_Podcastt')
os.chdir(project_dir)
sys.path.insert(0, str(project_dir / 'backend'))

from app.services.retrieval_service import retrieval_service

queries = [
    "What are the key principles of growth loops?",
    "How should a startup improve retention?"
]

for query in queries:
    print("=" * 80)
    print(f"Query: {query}")
    print("=" * 80)
    
    results = retrieval_service.retrieve_chunks(query, top_k=5)
    
    print(f"\nRetrieved {len(results)} chunks\n")
    
    if results:
        for i, result in enumerate(results, 1):
            print(f"{i}. Score: {result['similarity']:.3f} ({result.get('retrieval_method', 'unknown')})")
            print(f"   Episode: {result['episode_title']}")
            print(f"   Guest: {result.get('guest', 'N/A')}")
            print(f"   Source: {result['source_file']}")
            preview = result['content'][:200].replace('\n', ' ')
            print(f"   Preview: {preview}...")
            print()
    else:
        print("⚠️  No results returned\n")
