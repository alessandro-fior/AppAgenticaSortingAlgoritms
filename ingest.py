"""Indicizza algorithms.json in Qdrant con embedding locali. Eseguire: python ingest.py"""
import json

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from rich.console import Console

import config
from embeddings import embed_documents

console = Console()


def build_text(item: dict) -> str:
    return (
        f"{item['name']} ({item['language']}). Algoritmo: {item['algorithm']}. "
        f"{item['description']} Quando usarlo: {item['use_when']} "
        f"Complessita media {item['time_avg']}, peggiore {item['time_worst']}, "
        f"spazio {item['space']}. Stabile: {'si' if item['stable'] else 'no'}. "
        f"In place: {'si' if item['in_place'] else 'no'}."
    )


def main() -> None:
    if not config.DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset non trovato: {config.DATA_FILE}")
    items = json.loads(config.DATA_FILE.read_text(encoding="utf-8-sig"))
    if not items:
        raise ValueError("Il dataset e vuoto.")
    qdrant = QdrantClient(url=config.QDRANT_URL)
    if config.LEGACY_EMBEDDING_MODEL:
        console.print(
            "[yellow]Valore EMBEDDING_MODEL precedente rilevato; uso il modello locale "
            f"{config.EMBEDDING_MODEL}.[/yellow]"
        )
    console.print(f"Creo embedding locali con [cyan]{config.EMBEDDING_MODEL}[/cyan]...")
    vectors = embed_documents([build_text(item) for item in items])
    if len(vectors) != len(items):
        raise RuntimeError("Il modello locale ha restituito un numero di embedding inatteso.")

    if not qdrant.collection_exists(config.COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=config.COLLECTION_NAME,
            vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
        )
    points = [
        PointStruct(id=int(item["id"]), vector=vector, payload=item)
        for item, vector in zip(items, vectors)
    ]
    qdrant.upload_points(collection_name=config.COLLECTION_NAME, points=points, batch_size=64)
    console.print(
        f"[green]Indicizzati {len(points)} algoritmi nella collection "
        f"'{config.COLLECTION_NAME}' su {config.QDRANT_URL}.[/green]"
    )


if __name__ == "__main__":
    main()
