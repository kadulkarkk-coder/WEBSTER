"""
WEBSTER PDF Reader
==================
Reads and extracts text from PDF files with metadata.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from webster.core.logger import Logger


class PDFReader:
    """Extract text and metadata from PDF files."""

    def __init__(self):
        self.logger = Logger().get_logger("PDF")

    def read(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Read a PDF file and extract text."""
        if not os.path.exists(filepath):
            self.logger.error(f"File not found: {filepath}")
            return None
        try:
            import PyPDF2
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                pages = []
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
                    pages.append({"page": i + 1, "text": page_text.strip()})
                metadata = reader.metadata or {}
                return {
                    "title": metadata.get("/Title", Path(filepath).stem),
                    "author": metadata.get("/Author", ""),
                    "pages": len(pages),
                    "text": text.strip(),
                    "page_texts": pages,
                    "filepath": filepath,
                    "size": os.path.getsize(filepath),
                }
        except ImportError:
            return self._read_fallback(filepath)
        except Exception as e:
            self.logger.error(f"PDF read error: {e}")
            return None

    def _read_fallback(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Fallback using pdfminer."""
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(filepath)
            return {
                "title": Path(filepath).stem,
                "author": "",
                "pages": text.count("\f") + 1,
                "text": text.strip(),
                "page_texts": [],
                "filepath": filepath,
                "size": os.path.getsize(filepath),
            }
        except ImportError:
            self.logger.error("No PDF library available (install PyPDF2 or pdfminer)")
            return None

    def extract_text(self, filepath: str) -> Optional[str]:
        result = self.read(filepath)
        return result["text"] if result else None

    def search(self, filepath: str, query: str) -> List[Dict]:
        """Search for text within a PDF."""
        result = self.read(filepath)
        if not result:
            return []
        matches = []
        for page in result.get("page_texts", []):
            if query.lower() in page["text"].lower():
                matches.append({
                    "page": page["page"],
                    "context": self._get_context(page["text"], query),
                })
        return matches

    def _get_context(self, text: str, query: str, window: int = 100) -> str:
        idx = text.lower().find(query.lower())
        if idx == -1:
            return text[:200]
        start = max(0, idx - window)
        end = min(len(text), idx + len(query) + window)
        context = text[start:end].strip()
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
        return context
