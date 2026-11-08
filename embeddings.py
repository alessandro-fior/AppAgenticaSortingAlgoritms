"""Shim retrocompatibile: importa le funzioni di embedding da src/appagentica/embeddings.py."""
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from appagentica.embeddings import embed_documents, embed_query, get_embedding_model  # noqa: F401, E402
