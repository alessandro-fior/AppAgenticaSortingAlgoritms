import unittest
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from appagentica import config


class TestConfig(unittest.TestCase):
    def test_base_dir_resolution(self):
        self.assertTrue(config.BASE_DIR.exists())
        self.assertTrue((config.BASE_DIR / "pyproject.toml").exists())

    def test_dataset_path(self):
        self.assertTrue(config.DATA_FILE.exists(), f"Dataset not found at {config.DATA_FILE}")

    def test_embedding_model_not_empty(self):
        self.assertTrue(len(config.EMBEDDING_MODEL) > 0)
        self.assertEqual(config.EMBEDDING_DIM, 384)


if __name__ == "__main__":
    unittest.main()
