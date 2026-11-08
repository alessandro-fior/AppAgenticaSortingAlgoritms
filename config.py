"""Shim retrocompatibile: importa la configurazione da src/appagentica/config.py."""
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from appagentica.config import *  # noqa: F401, F403, E402
from appagentica.config import require_api_key  # noqa: F401, E402
