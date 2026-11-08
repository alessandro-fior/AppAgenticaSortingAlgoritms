import unittest
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from appagentica.ingest import load_dataset, build_text


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.items = load_dataset()

    def test_dataset_not_empty(self):
        self.assertGreaterEqual(len(self.items), 36)

    def test_required_fields_present_and_types(self):
        required_fields = {
            "id": int,
            "name": str,
            "language": str,
            "algorithm": str,
            "time_avg": str,
            "time_worst": str,
            "space": str,
            "stable": bool,
            "in_place": bool,
            "description": str,
            "use_when": str,
            "code": str,
        }

        unique_ids = set()
        for idx, item in enumerate(self.items):
            self.assertIn("id", item, f"Elemento {idx} privo di 'id'")
            self.assertNotIn(item["id"], unique_ids, f"ID duplicato: {item['id']}")
            unique_ids.add(item["id"])

            for field, expected_type in required_fields.items():
                self.assertIn(field, item, f"Campo mancante '{field}' nell'algoritmo {item.get('name')}")
                self.assertIsInstance(
                    item[field],
                    expected_type,
                    f"Tipo errato per campo '{field}' in {item.get('name')}: atteso {expected_type}, ottenuto {type(item[field])}",
                )
                if expected_type is str:
                    self.assertTrue(len(item[field].strip()) > 0, f"Campo vuoto '{field}' in {item.get('name')}")

    def test_build_text_format(self):
        sample = self.items[0]
        text = build_text(sample)
        self.assertIn(sample["name"], text)
        self.assertIn(sample["language"], text)
        self.assertIn(sample["algorithm"], text)
        self.assertIn("Quando usarlo:", text)


if __name__ == "__main__":
    unittest.main()
