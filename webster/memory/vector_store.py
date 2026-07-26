"""
WEBSTER Vector Store
====================
ChromaDB-based vector store for semantic memory.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class VectorStore:
    """
    ChromaDB wrapper for vector-based semantic search.
    Stores embeddings of conversations, notes, and knowledge.
    """

    def __init__(self, persist_dir: str = "webster/database/vector_store"):
        self.persist_dir = persist_dir
        self._client = None
        self._collection = None
        self._available = False
        self._init_store()

    def _init_store(self):
        try:
            import chromadb
            Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=self.persist_dir)
            self._collection = self._client.get_or_create_collection(
                name="webster_memory",
                metadata={"hnsw:space": "cosine"}
            )
            self._available = True
        except ImportError:
            self._available = False
        except Exception as e:
            self._available = False

    def add(self, text: str, metadata: Optional[Dict] = None, doc_id: Optional[str] = None):
        if not self._available:
            return
        import uuid
        doc_id = doc_id or str(uuid.uuid4())
        self._collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        if not self._available:
            return []
        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=n_results
            )
            items = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    items.append({
                        "text": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0,
                    })
            return items
        except:
            return []

    def delete(self, doc_id: str):
        if self._available:
            try:
                self._collection.delete(ids=[doc_id])
            except:
                pass

    def count(self) -> int:
        if self._available:
            try:
                return self._collection.count()
            except:
                return 0
        return 0

    def is_available(self) -> bool:
        return self._available
