import unittest
from types import SimpleNamespace
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from appagentica.rag import format_context, retrieve


class TestRAG(unittest.TestCase):
    def test_format_context_empty(self):
        self.assertEqual(format_context([]), "")

    def test_format_context_valid(self):
        mock_point = SimpleNamespace(
            payload={
                "name": "TestSort",
                "language": "Python",
                "algorithm": "Quicksort",
                "time_avg": "O(n log n)",
                "time_worst": "O(n^2)",
                "space": "O(log n)",
                "stable": False,
                "in_place": True,
                "description": "Ordinamento di prova.",
                "use_when": "Test unitario.",
                "code": "test_sort()",
            }
        )
        context = format_context([mock_point])
        self.assertIn("TestSort", context)
        self.assertIn("Quicksort", context)
        self.assertIn("```python", context)

    def test_retrieve_empty_question_raises(self):
        with self.assertRaises(ValueError):
            retrieve("   ")


if __name__ == "__main__":
    unittest.main()
