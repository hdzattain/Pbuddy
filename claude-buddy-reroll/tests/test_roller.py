"""Tests for BuddyRoller."""
import unittest

from buddy_reroll.roller import BuddyRoller
from buddy_reroll.constants import SPECIES, RARITIES, EYES, HATS, RARITY_FLOORS


class TestBuddyRoller(unittest.TestCase):
    """Test BuddyRoller pet generation."""

    def setUp(self):
        self.roller = BuddyRoller()

    def test_same_uid_same_buddy(self):
        uid = "test_user_123"
        buddy1 = self.roller.roll(uid)
        buddy2 = self.roller.roll(uid)
        self.assertEqual(buddy1, buddy2)

    def test_different_uid_different_buddy(self):
        buddy1 = self.roller.roll("user1")
        buddy2 = self.roller.roll("user2")
        self.assertNotEqual(buddy1, buddy2)

    def test_check_is_alias(self):
        uid = "test_user_456"
        buddy1 = self.roller.roll(uid)
        buddy2 = self.roller.check(uid)
        self.assertEqual(buddy1, buddy2)

    def test_species_in_valid_set(self):
        for i in range(100):
            buddy = self.roller.roll(f"user_{i}")
            self.assertIn(buddy.species, SPECIES)

    def test_rarity_in_valid_set(self):
        for i in range(100):
            buddy = self.roller.roll(f"user_{i}")
            self.assertIn(buddy.rarity, RARITIES)

    def test_eye_in_valid_set(self):
        for i in range(100):
            buddy = self.roller.roll(f"user_{i}")
            self.assertIn(buddy.eye, EYES)

    def test_hat_in_valid_set(self):
        for i in range(100):
            buddy = self.roller.roll(f"user_{i}")
            self.assertIn(buddy.hat, HATS)

    def test_common_hat_is_none(self):
        common_found = 0
        for i in range(1000):
            buddy = self.roller.roll(f"user_{i}")
            if buddy.rarity == "common":
                common_found += 1
                self.assertEqual(buddy.hat, "none")
        self.assertGreater(common_found, 0)

    def test_rarity_distribution(self):
        counts = {r: 0 for r in RARITIES}
        for i in range(10000):
            buddy = self.roller.roll(f"user_{i}")
            counts[buddy.rarity] += 1
        total = 10000
        self.assertGreater(counts["common"], total * 0.50)
        self.assertLess(counts["common"], total * 0.70)

    def test_stats_within_valid_range(self):
        for i in range(100):
            buddy = self.roller.roll(f"user_{i}")
            floor = RARITY_FLOORS[buddy.rarity]
            self.assertGreaterEqual(buddy.stats.debugging, floor)
            self.assertGreaterEqual(buddy.stats.patience, floor)
            self.assertGreaterEqual(buddy.stats.chaos, floor)
            self.assertGreaterEqual(buddy.stats.wisdom, floor)
            self.assertGreaterEqual(buddy.stats.snark, floor)

    def test_stats_has_peak_and_dump(self):
        for i in range(100):
            buddy = self.roller.roll(f"user_{i}")
            stats_list = [
                buddy.stats.debugging,
                buddy.stats.patience,
                buddy.stats.chaos,
                buddy.stats.wisdom,
                buddy.stats.snark,
            ]
            max_val = max(stats_list)
            min_val = min(stats_list)
            # There should be at least one peak stat (may have ties)
            peak_count = sum(1 for s in stats_list if s == max_val)
            self.assertGreaterEqual(peak_count, 1)
            # Peak should be noticeably higher than dump
            self.assertGreater(max_val - min_val, 5)

    def test_shiny_probability(self):
        shiny_count = 0
        total = 5000
        for i in range(total):
            buddy = self.roller.roll(f"user_{i}")
            if buddy.shiny:
                shiny_count += 1
        shiny_rate = shiny_count / total
        self.assertGreater(shiny_rate, 0.003)
        self.assertLess(shiny_rate, 0.02)

    def test_stats_methods(self):
        buddy = self.roller.roll("test_user")
        self.assertEqual(
            buddy.stats.total(),
            buddy.stats.debugging + buddy.stats.patience +
            buddy.stats.chaos + buddy.stats.wisdom + buddy.stats.snark
        )

    def test_search_finds_matches(self):
        results = self.roller.search(rarity="common", count=2, max_iterations=10000)
        self.assertGreaterEqual(len(results), 1)
        for match in results:
            self.assertEqual(match.buddy.rarity, "common")

    def test_search_respects_count(self):
        results = self.roller.search(rarity="common", count=3, max_iterations=10000)
        self.assertLessEqual(len(results), 3)

    def test_search_filters_species(self):
        target_species = SPECIES[0]
        results = self.roller.search(species=target_species, count=1, max_iterations=50000)
        if results:
            self.assertEqual(results[0].buddy.species, target_species)


if __name__ == "__main__":
    unittest.main()
