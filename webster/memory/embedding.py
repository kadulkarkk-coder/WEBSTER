"""
WEBSTER Embedding Generator
============================
Generates text embeddings for vector search.
"""

from typing import List, Optional


class EmbeddingGenerator:
    """
    Generates embeddings for text using available models.
    """

    def __init__(self):
        self._model = None
        self._available = False
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            self._available = True
        except ImportError:
            try:
                import fastembed
                self._model = fastembed.TextEmbedding()
                self._available = True
            except ImportError:
                self._available = False

    def embed(self, text: str) -> List[float]:
        if not self._available:
            return []
        if hasattr(self._model, "encode"):
            return self._model.encode(text).tolist()
        return list(self._model.embed(text))[0].tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not self._available:
            return []
        return [self.embed(t) for t in texts]

    def is_available(self) -> bool:
        return self._available
