#!/usr/bin/env python3
"""Test growth loops retrieval."""
import os
import sys
from pathlib import Path
import json

project_dir = Path('/Users/shahulhameed/Desktop/Lenny_Podcastt')
os.chdir(project_dir)
sys.path.insert(0, str(project_dir / 'backend'))

# Check chunk mapping for non-transcript files
print("=" * 70)
print("Checking chunk mapping for non-transcript files")
print("=" * 70)

mapping_path = project_dir / 'backend/data/chunk_mapping.json'
with open(mapping_path, 'r') as f:
    chunk_mapping = json.load(f)

# Count files
source_files = {}
for chunk_id, chunk_data in chunk_mapping.items():
    source = chunk_data.get('source_file', 'unknown')
    source_files[source] = source_files.get(source, 0) + 1

print(f"\nTotal chunks: {len(chunk_mapping)}")
print(f"Total unique files: {len(source_files)}")

# Show non-transcript files
print("\nNon-transcript files:")
for source, count in sorted(source_files.items()):
    if 'README' in source or 'CLAUDE' in source:
        print(f"  {source}: {count} chunks")

print("\n" + "=" * 70)
print("Testing retrieval for growth loop queries")
print("=" * 70)

from app.services.retrieval_service import retrieval_service

queries = [
    "growth loops",
    "What is a growth loop?",
    "How do growth loops work?",
    "What are the key principles of growth loops?"
]

for query in queries:
    print(f"\nQuery: {query}")
    print("-" * 70)
    
    results = retrieval_service.retrieve_chunks(query, top_k=5, threshold=0.0)
    
    print(f"Retrieved {len(results)} chunks")
    
    if results:
        for i, result in enumerate(results[:5], 1):
            print(f"\n{i}. Score: {result['similarity']:.3f}")
            print(f"   Source: {result['source_file']}")
            episode = result.get('episode_title', 'N/A')
            if len(episode) > 70:
                episode = episode[:67] + '...'
            print(f"   Episode: {episode}")
            preview = result['content'][:150].replace('\n', ' ')
            print(f"   Preview: {preview}...")
    else:
        print("⚠️  No results")
    print()
