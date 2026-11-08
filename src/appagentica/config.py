"""Configurazione centralizzata e gestione variabili d'ambiente."""
from pathlib import Path
import os
from dotenv import load_dotenv

# Risale da src/appagentica/ alla radice del progetto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Il file .env locale prevale su eventuali variabili omonime d'ambiente
load_dotenv(BASE_DIR / ".env", override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip()
CHAT_MODEL = os.getenv("CHAT_MODEL", "openrouter/free").strip()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sorting_algorithms").strip()

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
configured_embedding_model = os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL).strip()
# Riconosce e migra automaticamente se nel file .env era rimasto il modello OpenAI legacy
LEGACY_EMBEDDING_MODEL = configured_embedding_model == "text-embedding-3-small"
EMBEDDING_MODEL = (
    DEFAULT_EMBEDDING_MODEL if LEGACY_EMBEDDING_MODEL else configured_embedding_model
)
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "384"))

# Risoluzione dinamica del percorso del dataset
_env_data_file = os.getenv("DATA_FILE", "").strip()
if _env_data_file:
    candidate = Path(_env_data_file)
    DATA_FILE = candidate if candidate.is_absolute() else (BASE_DIR / candidate)
elif (BASE_DIR / "data" / "algorithms.json").exists():
    DATA_FILE = BASE_DIR / "data" / "algorithms.json"
else:
    DATA_FILE = BASE_DIR / "algorithms.json"


def require_api_key() -> str:
    """Verifica e restituisce la chiave API OpenRouter valida.

    Raises:
        RuntimeError: Se la chiave è assente, segnaposto o di formato non valido.
    """
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "sk-or-v1-...":
        raise RuntimeError(
            f"OPENROUTER_API_KEY mancante: crea una chiave su OpenRouter e inseriscila in .env (cartella: {BASE_DIR})."
        )
    if not OPENROUTER_API_KEY.startswith("sk-or-"):
        raise RuntimeError(
            "La chiave in OPENROUTER_API_KEY non ha il formato OpenRouter (sk-or-...). "
            "Sostituiscila con una chiave creata su https://openrouter.ai/keys."
        )
    return OPENROUTER_API_KEY
