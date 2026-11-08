"""AppAgentica: Consulente intelligente RAG per algoritmi di ordinamento."""

from appagentica import config
from appagentica.embeddings import embed_documents, embed_query, get_embedding_model
from appagentica.ingest import build_text, ingest_dataset, load_dataset
from appagentica.rag import ask, format_context, make_clients, retrieve

__version__ = "1.0.0"
__all__ = [
    "config",
    "embed_documents",
    "embed_query",
    "get_embedding_model",
    "build_text",
    "load_dataset",
    "ingest_dataset",
    "retrieve",
    "format_context",
    "ask",
    "make_clients",
]
