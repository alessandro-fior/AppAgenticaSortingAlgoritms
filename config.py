from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# In questo progetto il file locale deve prevalere anche su eventuali variabili
# omonime ereditate da PowerShell (per esempio una vecchia chiave OpenAI).
load_dotenv(BASE_DIR / ".env", override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sorting_algorithms").strip()
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
CHAT_MODEL = os.getenv("CHAT_MODEL", "openrouter/free").strip()
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
configured_embedding_model = os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL).strip()
# Migra automaticamente il vecchio valore OpenAI rimasto in un .env preesistente.
LEGACY_EMBEDDING_MODEL = configured_embedding_model == "text-embedding-3-small"
EMBEDDING_MODEL = (
    DEFAULT_EMBEDDING_MODEL if LEGACY_EMBEDDING_MODEL else configured_embedding_model
)
EMBEDDING_DIM = 384
DATA_FILE = Path(os.getenv("DATA_FILE", str(BASE_DIR / "algorithms.json")))
if not DATA_FILE.is_absolute():
    DATA_FILE = BASE_DIR / DATA_FILE


def require_api_key() -> str:
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
