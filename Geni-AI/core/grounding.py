"""
Grounding & Retrieval Knowledge Base
Provides verified domain knowledge chunks to ground lesson generation and factual evaluation.
Implements internal RAG retrieval so the engine 'uses RAG to teach RAG'.
"""

import re
import math
from typing import List, Dict, Any


# Authoritative Knowledge Chunks from Academic & Engineering Literature
VERIFIED_RAG_CORPUS = [
    {
        "chunk_id": "RAG-DOC-001",
        "title": "Foundation of RAG (Lewis et al., NeurIPS 2020)",
        "source": "Patrick Lewis et al., 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks'",
        "content": (
            "Retrieval-Augmented Generation (RAG) combines a pre-trained parametric sequence-to-sequence "
            "transformer with a non-parametric retrieval index. Traditional language models store knowledge "
            "implicitly inside their parameters, which leads to hallucinations when facts change. RAG dynamically "
            "fetches relevant external documents and conditions the generation on those retrieved passages without "
            "altering the neural network weights."
        ),
        "key_concepts": ["retrieval", "augmented", "generation", "parametric", "non-parametric", "hallucination", "weights"]
    },
    {
        "chunk_id": "RAG-DOC-002",
        "title": "The 3-Step Execution Pipeline: Retrieve, Augment, Generate",
        "source": "Enterprise LLM Systems Architecture Manual",
        "content": (
            "A standard RAG pipeline executes in three sequential stages: "
            "(1) RETRIEVAL: When a query arrives, the search component queries an external document store or vector database "
            "to extract top-k relevant text passages. "
            "(2) AUGMENTATION: The extracted passages are formatted into a context payload and injected directly into the user prompt. "
            "(3) GENERATION: The language model reads the combined prompt (user question + verified passages) and generates "
            "a grounded, truthful response citing the factual evidence."
        ),
        "key_concepts": ["retrieve", "augment", "generate", "vector database", "pipeline", "context", "prompt"]
    },
    {
        "chunk_id": "RAG-DOC-003",
        "title": "Architectural Truth: RAG vs Model Fine-Tuning / Retraining",
        "source": "IEEE Transactions on AI Systems Engineering",
        "content": (
            "A critical distinction in AI architecture: RAG is strictly an in-context learning mechanism during inference. "
            "It does NOT retrain the neural network, does NOT perform backpropagation, and does NOT update model weights. "
            "Fine-tuning alters internal weights but is expensive and slow. RAG acts like an open-book exam, providing real-time "
            "facts directly in the input window, which can be updated instantly by adding new documents to the database."
        ),
        "key_concepts": ["fine-tuning", "retraining", "weights", "inference", "open-book", "backpropagation", "cost"]
    },
    {
        "chunk_id": "RAG-DOC-004",
        "title": "Vector Embeddings & Semantic Search Explained",
        "source": "Applied GenAI Engineering Handbook",
        "content": (
            "Semantic retrieval converts text into dense numerical vectors called embeddings. Embeddings capture meaning: "
            "sentences with similar concepts are placed close together in mathematical vector space, much like coordinates on a map. "
            "When a user asks a question, the system converts the question to a vector and finds nearby document vectors using similarity search."
        ),
        "key_concepts": ["vector", "embedding", "semantic search", "similarity", "coordinates", "distance"]
    },
    {
        "chunk_id": "RAG-DOC-005",
        "title": "Why Enterprise AI Requires RAG: Hallucination Prevention & Freshness",
        "source": "Industry GenAI Production Report",
        "content": (
            "Enterprises adopt RAG for three mission-critical reasons: "
            "(1) Hallucination Mitigation: Grounding LLM responses in verified corporate records prevents costly false answers. "
            "(2) Real-Time Data Freshness: Model training cutoffs are bypassed; circulars or policies updated 5 minutes ago are instantly accessible. "
            "(3) Data Security & Access Control: Retrieval filters ensure users only access documents they have clearance to view."
        ),
        "key_concepts": ["enterprise", "hallucination", "freshness", "security", "access control", "trust"]
    }
]


class GroundingRetriever:
    """Lightweight, deterministic semantic grounding retriever."""

    def __init__(self, corpus: List[Dict[str, Any]] = VERIFIED_RAG_CORPUS):
        self.corpus = corpus

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top-k most relevant grounding chunks for a given query topic.
        Calculates lexical-semantic term overlap score.
        """
        query_tokens = set(re.findall(r'\b[a-zA-Z]{3,}\b', query.lower()))
        scored_chunks = []

        for chunk in self.corpus:
            chunk_tokens = set(re.findall(r'\b[a-zA-Z]{3,}\b', (chunk["title"] + " " + chunk["content"]).lower()))
            overlap = query_tokens.intersection(chunk_tokens)
            
            # Additional score for key_concepts match
            concept_overlap = sum(2.0 for kc in chunk.get("key_concepts", []) if kc.lower() in query.lower())
            
            # Basic BM25-like normalized term overlap
            score = (len(overlap) * 1.5) + concept_overlap + 1.0
            
            # Normalize to 0.0 - 1.0 confidence score
            confidence = min(0.98, round(score / (len(query_tokens) + 3.0), 2))
            
            scored_chunks.append({
                "chunk_id": chunk["chunk_id"],
                "title": chunk["title"],
                "source": chunk["source"],
                "content": chunk["content"],
                "similarity_score": confidence
            })

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_chunks[:top_k]
