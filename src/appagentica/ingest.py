"""Pipeline di indicizzazione del dataset degli algoritmi in Qdrant."""
from pathlib import Path
import json

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from rich.console import Console

from appagentica import config
from appagentica.embeddings import embed_documents

console = Console()


def build_text(item: dict) -> str:
    """Costruisce la rappresentazione testuale dell'algoritmo per il calcolo dell'embedding."""
    return (
        f"{item['name']} ({item['language']}). Algoritmo: {item['algorithm']}. "
        f"{item['description']} Quando usarlo: {item['use_when']} "
        f"Complessita media {item['time_avg']}, peggiore {item['time_worst']}, "
        f"spazio {item['space']}. Stabile: {'si' if item['stable'] else 'no'}. "
        f"In place: {'si' if item['in_place'] else 'no'}."
    )


def load_dataset(file_path: Path | str | None = None) -> list[dict]:
    """Carica e valida il file JSON contenente il catalogo degli algoritmi."""
    target_path = Path(file_path) if file_path else config.DATA_FILE
    if not target_path.exists():
        raise FileNotFoundError(f"File dataset non trovato: {target_path}")

    data = json.loads(target_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list) or not data:
        raise ValueError(f"Il dataset in {target_path} è vuoto o non è una lista JSON valida.")
    return data


def ingest_dataset(
    data_path: Path | str | None = None,
    qdrant_url: str | None = None,
    collection_name: str | None = None,
    batch_size: int = 64,
) -> int:
    """Indicizza il dataset in Qdrant creando la collection e caricando i punti.

    Returns:
        int: Numero di schede indicizzate.
    """
    items = load_dataset(data_path)
    url = qdrant_url or config.QDRANT_URL
    col_name = collection_name or config.COLLECTION_NAME

    qdrant = QdrantClient(url=url)

    texts = [build_text(item) for item in items]
    vectors = embed_documents(texts)
    if len(vectors) != len(items):
        raise RuntimeError("Il numero di vettori generati non coincide con il numero di elementi.")

    dim = len(vectors[0])
    if not qdrant.collection_exists(col_name):
        qdrant.create_collection(
            collection_name=col_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )

    points = [
        PointStruct(id=int(item["id"]), vector=vector, payload=item)
        for item, vector in zip(items, vectors)
    ]
    qdrant.upload_points(collection_name=col_name, points=points, batch_size=batch_size)
    return len(points)


def main() -> None:
    """Comando CLI per lanciare l'ingestione con feedback colorato."""
    console.print(f"[bold cyan]Avvio indicizzazione del catalogo algoritmi...[/bold cyan]")
    console.print(f"Dataset: [dim]{config.DATA_FILE}[/dim]")
    console.print(f"Modello embedding locale: [dim]{config.EMBEDDING_MODEL}[/dim]")
    console.print(f"Qdrant endpoint: [dim]{config.QDRANT_URL}[/dim]")

    try:
        count = ingest_dataset()
        console.print(
            f"[bold green]Completato con successo:[/bold green] {count} schede indicizzate nella collection "
            f"'{config.COLLECTION_NAME}'!"
        )
    except Exception as exc:
        console.print(f"[bold red]Errore durante l'ingestione:[/bold red] {exc}")
        raise


if __name__ == "__main__":
    main()
