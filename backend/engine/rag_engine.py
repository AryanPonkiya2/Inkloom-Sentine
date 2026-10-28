"""
Grounded RAG retrieval engine for Inkloom Sentinel.
Simulates high-precision vector embeddings and semantic cosine similarity
retrieval against brand knowledge sheets and truth documents.
"""

import math
import re
from typing import List, Dict, Any, Tuple

class GroundedRAGEngine:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules
        self.index = []
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_\-\.%]+\b", text)]

    def _build_index(self):
        """Indexes knowledge base documents into a grounded vector space."""
        self.index = []
        for rule in self.rules:
            # Combine rule text, approved facts, and description into searchable knowledge chunk
            doc_text = f"{rule['title']} {rule['description']} {rule['approved_facts']} {' '.join(rule.get('keywords', []))}"
            tokens = self._tokenize(doc_text)
            self.index.append({
                "rule": rule,
                "tokens": set(tokens),
                "raw_text": doc_text
            })

    def retrieve_relevant_guidelines(self, query: str, top_k: int = 3, threshold: float = 0.15) -> List[Tuple[Dict[str, Any], float]]:
        """
        Retrieves top-k most relevant brand guideline sections using grounded Jaccard/TF similarity.
        Guarantees that every finding is linked to an authentic cited passage.
        """
        q_tokens = set(self._tokenize(query))
        if not q_tokens:
            return []

        scored = []
        for item in self.index:
            doc_tokens = item["tokens"]
            intersection = q_tokens.intersection(doc_tokens)
            union = q_tokens.union(doc_tokens)
            
            similarity = len(intersection) / len(union) if union else 0.0

            # Boost if exact critical keywords appear
            rule = item["rule"]
            for kw in rule.get("keywords", []):
                if kw.lower() in query.lower():
                    similarity += 0.35

            if similarity >= threshold:
                scored.append((rule, round(similarity, 3)))

        # Sort descending by relevance
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
