"""Tests for Mulberry32 PRNG implementation."""
import unittest

from buddy_reroll.rng import Mulberry32


class TestMulberry32(unittest.TestCase):
    """Test Mulberry32 PRNG."""

    def test_deterministic(self):
        """Same seed should produce same sequence."""
        rng1 = Mulberry32(12345)
        rng2 = Mulberry32(12345)

        seq1 = [rng1.next() for _ in range(100)]
        seq2 = [rng2.next() for _ in range(100)]

        self.assertEqual(seq1, seq2)

    def test_different_seeds_different_sequences(self):
        """Different seeds should produce different sequences."""
        rng1 = Mulberry32(12345)
        rng2 = Mulberry32(54321)

        seq1 = [rng1.next() for _ in range(10)]
        seq2 = [rng2.next() for _ in range(10)]

        self.assertNotEqual(seq1, seq2)

    def test_range_is_zero_to_one(self):
        """Generated values should be in [0, 1) range."""
        rng = Mulberry32(12345)

        for _ in range(1000):
            val = rng.next()
            self.assertGreaterEqual(val, 0.0)
            self.assertLess(val, 1.0)

    def test_distribution(self):
        """Values should be roughly uniformly distributed."""
        rng = Mulberry32(12345)
        buckets = [0] * 10

        for _ in range(10000):
            val = rng.next()
            bucket = int(val * 10)
            buckets[bucket] += 1

        # Each bucket should have roughly 1000 values
        # Allow for 30% variance due to randomness
        for count in buckets:
            self.assertGreater(count, 700)
            self.assertLess(count, 1300)

    def test_pick_from_list(self):
        """pick() should select items from list."""
        rng = Mulberry32(12345)
        items = ['a', 'b', 'c', 'd', 'e']

        picked = [rng.pick(items) for _ in range(100)]

        # All picks should be from the original list
        for item in picked:
            self.assertIn(item, items)

    def test_pick_empty_raises(self):
        """pick() with empty sequence should raise."""
        rng = Mulberry32(12345)
        with self.assertRaises(ValueError):
            rng.pick([])

    def test_weighted_pick(self):
        """weighted_pick() should respect weights."""
        rng = Mulberry32(12345)
        weighted_items = (('a', 80), ('b', 20))

        picks = [rng.weighted_pick(weighted_items) for _ in range(1000)]

        count_a = picks.count('a')
        count_b = picks.count('b')

        # 'a' should be picked roughly 80% of the time
        self.assertGreater(count_a, 700)
        self.assertLess(count_a, 900)

        # 'b' should be picked roughly 20% of the time
        self.assertGreater(count_b, 100)
        self.assertLess(count_b, 300)

    def test_seed_masking(self):
        """Seed should be masked to 32 bits."""
        # Large seed should be masked
        rng1 = Mulberry32(2**33 + 123)
        rng2 = Mulberry32(123)

        seq1 = [rng1.next() for _ in range(10)]
        seq2 = [rng2.next() for _ in range(10)]

        self.assertEqual(seq1, seq2)


if __name__ == "__main__":
    unittest.main()
