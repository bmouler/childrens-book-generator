#!/usr/bin/env python3
import unittest

import numpy as np

import make_music as M


class BedTests(unittest.TestCase):
    RATE = 8000
    SECONDS = 30.0

    def test_same_seed_gives_same_samples_and_modes_differ(self):
        night = M.compose("night", self.SECONDS, self.RATE, seed=7)
        again = M.compose("night", self.SECONDS, self.RATE, seed=7)
        morning = M.compose("morning", self.SECONDS, self.RATE, seed=7)
        self.assertTrue(np.array_equal(night, again))
        self.assertFalse(np.array_equal(night, morning))

    def test_bed_has_exact_length_safe_peak_and_soft_ends(self):
        for mode in ("night", "morning"):
            sig = M.compose(mode, self.SECONDS, self.RATE, seed=7)
            self.assertEqual(len(sig), int(self.SECONDS * self.RATE))
            self.assertTrue(np.all(np.isfinite(sig)))
            self.assertAlmostEqual(float(np.max(np.abs(sig))), M.PEAK, places=3)
            self.assertLess(abs(float(sig[0])), 0.01)
            self.assertLess(abs(float(sig[-1])), 0.01)

    def test_rejects_unknown_mode(self):
        with self.assertRaises(ValueError):
            M.compose("noon", self.SECONDS, self.RATE)


if __name__ == "__main__":
    unittest.main()
