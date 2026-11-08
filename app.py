"""Entrypoint per l'avvio della chat CLI di AppAgentica o import diretto."""
import sys
from pathlib import Path

# Garantisce che 'src' sia nel path Python
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from appagentica.rag import ask, main, make_clients, retrieve  # noqa: E402

__all__ = ["ask", "retrieve", "make_clients", "main"]

if __name__ == "__main__":
    main()
