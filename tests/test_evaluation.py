import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agroecosystem_pipeline.evaluation import evaluate_predictions, leave_one_group_out


class EvaluationTests(unittest.TestCase):
    def test_metrics_and_coverage(self):
        r = evaluate_predictions([10, 20], [12, 18], [9, 17], [11, 21])
        self.assertEqual((r.n, r.mean_error, r.rmse, r.interval_coverage), (2, 0, 2, 1))
    def test_bad_pair_lengths(self):
        with self.assertRaises(ValueError):
            evaluate_predictions([1, 2], [1])
    def test_intervals_must_pair(self):
        with self.assertRaises(ValueError):
            evaluate_predictions([1], [1], lower=[0])
    def test_group_holdout(self):
        groups = ["A", "A", "B", "C", "C"]
        splits = list(leave_one_group_out(groups))
        self.assertEqual(len(splits), 3)
        for train, test in splits:
            self.assertFalse({groups[i] for i in train} & {groups[i] for i in test})


if __name__ == "__main__":
    unittest.main()
