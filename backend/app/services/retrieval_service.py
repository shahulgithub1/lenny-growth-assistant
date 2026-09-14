"""RAG retrieval service using sentence-transformers and FAISS."""
import json
import os
import re
from typing import List, Dict, Any, Set
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# High-value terms for lexical matching
HIGH_VALUE_TERMS = [
    "growth loop", "growth loops",
    "acquisition loop", "acquisition loops",
    "viral loop", "viral loops",
    "content loop", "content loops",
    "retention loop", "retention loops",
    "sales loop", "sales loops",
    "referral loop", "referral loops",
    "network effect", "network effects",
    "product-led growth", "PLG",
    "product market fit", "PMF",
    "activation rate", "retention rate", "retention",
    "churn rate", "conversion rate",
    "user retention", "improve retention", "increase retention",
    "customer retention", "retain users", "retaining users"
]


class RetrievalService:
    """Handles embedding generation and FAISS retrieval."""
    
    def __init__(self):
        self.model = None
        self.index = None
        self.chunk_mapping = None
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        self.index_path = os.path.join(self.data_dir, "faiss_index.bin")
        self.mapping_path = os.path.join(self.data_dir, "chunk_mapping.json")
    
    def _load_model(self):
        """Load sentence transformer model."""
        if self.model is None:
            logger.info("loading_embedding_model", model=self.model_name)
            self.model = SentenceTransformer(self.model_name)
            logger.info("embedding_model_loaded")
    
    def _load_index(self):
        """Load FAISS index and chunk mapping."""
        if self.index is None:
            if not os.path.exists(self.index_path):
                logger.warning("faiss_index_not_found", path=self.index_path)
                return False
            
            logger.info("loading_faiss_index", path=self.index_path)
            self.index = faiss.read_index(self.index_path)
            
            with open(self.mapping_path, 'r') as f:
                self.chunk_mapping = json.load(f)
            
            logger.info("faiss_index_loaded", chunks=len(self.chunk_mapping))
            return True
        return True
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text."""
        self._load_model()
        embedding = self.model.encode([text])[0]
        return embedding.astype('float32')
    
    def _lexical_search(self, query: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """
        Perform lexical/exact-term matching against chunks.
        Returns chunks containing high-value terms found in the query.
        """
        if not self._load_index():
            return []
        
        query_lower = query.lower()
        
        # Find high-value terms in query
        matched_terms = [term for term in HIGH_VALUE_TERMS if term.lower() in query_lower]
        
        if not matched_terms:
            return []
        
        logger.info("lexical_search", query=query, matched_terms=matched_terms)
        
        results = []
        for chunk_id, chunk_data in self.chunk_mapping.items():
            content_lower = chunk_data.get("content", "").lower()
            
            # Check if any matched term appears in content
            for term in matched_terms:
                if term.lower() in content_lower:
                    # Calculate term frequency score
                    term_count = content_lower.count(term.lower())
                    score = min(1.0, 0.3 + (term_count * 0.1))  # Score between 0.3 and 1.0
                    
                    results.append({
                        "chunk_id": chunk_id,
                        "similarity": score,
                        "lexical_term": term,
                        "episode_title": chunk_data.get("episode_title"),
                        "guest": chunk_data.get("guest"),
                        "content": chunk_data.get("content"),
                        "source_file": chunk_data.get("source_file"),
                        "excerpt": chunk_data.get("content", "")[:200] + "..."
                    })
                    break  # One match per chunk is enough
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        logger.info("lexical_search_completed", results_count=len(results))
        return results[:top_k]
    
    def retrieve_chunks(
        self, 
        query: str, 
        top_k: int = None,
        threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks using hybrid retrieval (semantic + lexical).
        Combines FAISS semantic search with exact term matching.
        """
        if top_k is None:
            top_k = settings.retrieval_top_k
        if threshold is None:
            threshold = settings.retrieval_threshold
        
        logger.info("retrieval_requested", query_length=len(query), top_k=top_k)
        
        if not self._load_index():
            logger.warning("retrieval_failed_no_index")
            return []
        
        # 1. Semantic retrieval via FAISS
        query_embedding = self.generate_embedding(query)
        query_embedding = np.array([query_embedding])
        
        # Search more candidates for hybrid approach
        search_k = min(top_k * 3, 50)
        distances, indices = self.index.search(query_embedding, search_k)
        
        # Convert distances to similarity scores
        similarities = 1 - distances[0]
        
        # Collect semantic results
        semantic_results = {}  # chunk_id -> result dict
        for idx, (similarity, chunk_idx) in enumerate(zip(similarities, indices[0])):
            if similarity < threshold:
                continue
            
            chunk_id = str(chunk_idx)
            if chunk_id not in self.chunk_mapping:
                continue
            
            chunk_data = self.chunk_mapping[chunk_id]
            semantic_results[chunk_id] = {
                "chunk_id": chunk_id,
                "similarity": float(similarity),
                "episode_title": chunk_data.get("episode_title"),
                "guest": chunk_data.get("guest"),
                "content": chunk_data.get("content"),
                "source_file": chunk_data.get("source_file"),
                "excerpt": chunk_data.get("content", "")[:200] + "...",
                "retrieval_method": "semantic"
            }
        
        # 2. Lexical retrieval for high-value terms
        lexical_results_list = self._lexical_search(query, top_k=20)
        lexical_results = {r["chunk_id"]: r for r in lexical_results_list}
        
        # Mark lexical results
        for chunk_id, result in lexical_results.items():
            result["retrieval_method"] = "lexical"
        
        # 3. Merge results (lexical takes precedence for overlaps)
        merged_results = {}
        
        # Add all lexical results first (they matched high-value terms)
        for chunk_id, result in lexical_results.items():
            merged_results[chunk_id] = result
        
        # Add semantic results that aren't already present
        for chunk_id, result in semantic_results.items():
            if chunk_id not in merged_results:
                merged_results[chunk_id] = result
            else:
                # Boost score if both methods found it
                merged_results[chunk_id]["similarity"] = max(
                    merged_results[chunk_id]["similarity"],
                    result["similarity"] + 0.1  # Boost for semantic agreement
                )
                merged_results[chunk_id]["retrieval_method"] = "hybrid"
        
        # Sort by similarity and return top_k
        results = sorted(merged_results.values(), key=lambda x: x["similarity"], reverse=True)[:top_k]
        
        logger.info(
            "retrieval_completed",
            results_count=len(results),
            semantic_count=len(semantic_results),
            lexical_count=len(lexical_results),
            top_similarity=results[0]["similarity"] if results else 0
        )
        
        return results


# Global retrieval service instance
retrieval_service = RetrievalService()
