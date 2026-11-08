"""Entrypoint per l'indicizzazione del catalogo in Qdrant."""
import sys
from pathlib import Path

# Garantisce che 'src' sia nel path Python
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from appagentica.ingest import build_text, ingest_dataset, load_dataset, main  # noqa: E402

__all__ = ["build_text", "load_dataset", "ingest_dataset", "main"]

if __name__ == "__main__":
    main()
