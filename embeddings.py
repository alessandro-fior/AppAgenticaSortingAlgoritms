"""Embedding locali condivisi tra ingestione e ricerca."""
from functools import lru_cache

from fastembed import TextEmbedding

import config


@lru_cache(maxsize=1)
def get_embedding_model() -> TextEmbedding:
    return TextEmbedding(model_name=config.EMBEDDING_MODEL)


def embed_documents(texts: list[str]) -> list[list[float]]:
    return [vector.tolist() for vector in get_embedding_model().passage_embed(texts)]


def embed_query(text: str) -> list[float]:
    return next(get_embedding_model().query_embed(text)).tolist()
