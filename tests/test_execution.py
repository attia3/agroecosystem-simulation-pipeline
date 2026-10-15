"""Tests of model-independent, dry-run-safe execution and audit records."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agroecosystem_pipeline.execution import execute_model, save_run_record, sha256_file


class ExecutionTests(unittest.TestCase):
    def test_dry_run_no_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = execute_model(["not-a-real-executable"], tmp)
            self.assertTrue(result.dry_run)
            self.assertIsNone(result.return_code)
            output = save_run_record(result, Path(tmp) / "run.json")
            self.assertEqual(json.loads(output.read_text())["command"], ["not-a-real-executable"])

    def test_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            path.write_bytes(b"abc")
            self.assertEqual(sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_missing_directory(self):
        with self.assertRaises(NotADirectoryError):
            execute_model(["echo"], "/unlikely-nonexistent-directory-xyz")


if __name__ == "__main__":
    unittest.main()
