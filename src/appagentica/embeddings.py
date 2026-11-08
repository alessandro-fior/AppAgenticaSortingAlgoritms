"""Embedding locali eseguiti su CPU tramite FastEmbed."""
from functools import lru_cache
from fastembed import TextEmbedding

from appagentica import config


@lru_cache(maxsize=1)
def get_embedding_model() -> TextEmbedding:
    """Restituisce il modello singleton TextEmbedding di FastEmbed."""
    return TextEmbedding(model_name=config.EMBEDDING_MODEL)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Calcola i vettori di embedding per una lista di passaggi testuali."""
    return [vector.tolist() for vector in get_embedding_model().passage_embed(texts)]


def embed_query(text: str) -> list[float]:
    """Calcola il vettore di embedding per una singola query di ricerca."""
    return next(get_embedding_model().query_embed(text)).tolist()
