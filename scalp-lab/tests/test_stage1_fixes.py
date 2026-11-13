import unittest

import numpy as np
import pandas as pd

from bt.timeframes import tf_to_minutes
from bt import engine


class TimeframeTests(unittest.TestCase):
    def test_minutes(self):
        self.assertEqual(tf_to_minutes("1m"), 1)
        self.assertEqual(tf_to_minutes("5m"), 5)
        self.assertEqual(tf_to_minutes("15m"), 15)

    def test_hours(self):
        self.assertEqual(tf_to_minutes("1h"), 60)
        self.assertEqual(tf_to_minutes("4h"), 240)

    def test_days(self):
        self.assertEqual(tf_to_minutes("1d"), 1440)

    def test_invalid_values(self):
        for value in ("", "0m", "1w", "1.5h", "60", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    tf_to_minutes(value)


class FundingWalkForwardTests(unittest.TestCase):
    def test_funding_is_sliced_for_each_fold(self):
        n = 400
        close = 100 + np.cumsum(np.sin(np.arange(n) / 7) * 0.1)

        df = pd.DataFrame({
            "close": close,
            "high": close * 1.002,
            "low": close * 0.998,
            "funding": np.full(n, 0.0001),
        })

        signal = pd.Series(
            np.where(np.arange(n) % 20 < 10, 1.0, -1.0)
        )

        result = engine.walk_forward(
            df=df,
            sigs={"test": signal},
            train_bars=100,
            test_bars=50,
            fee=0.0004,
            slip=0.0002,
            tf_min=5,
        )

        self.assertNotIn("error", result)
        self.assertGreater(result["folds"], 0)
        self.assertTrue(result["funding_cost"])


if __name__ == "__main__":
    unittest.main()
