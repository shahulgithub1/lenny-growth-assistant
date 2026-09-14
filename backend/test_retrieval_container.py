#!/usr/bin/env python3
"""Test retrieval inside container."""
import os
import sys

# Check current settings
from app.core.config import settings
print(f"Current RETRIEVAL_THRESHOLD: {settings.retrieval_threshold}")
print(f"Current RETRIEVAL_TOP_K: {settings.retrieval_top_k}")
print()

from app.services.retrieval_service import retrieval_service

queries = [
    "What are the key principles of growth loops?",
    "How should a startup improve retention?"
]

for query in queries:
    print("=" * 70)
    print(f"Query: {query}")
    print("=" * 70)
    
    results = retrieval_service.retrieve_chunks(query, top_k=5)
    
    print(f"\nRetrieved {len(results)} chunks")
    
    if results:
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Score: {result['similarity']:.3f}")
            print(f"   Episode: {result['episode_title'][:60]}...")
            print(f"   Guest: {result.get('guest', 'N/A')[:60]}...")
            print(f"   Preview: {result['content'][:150]}...")
    else:
        print("⚠️  No results returned")
    print()
