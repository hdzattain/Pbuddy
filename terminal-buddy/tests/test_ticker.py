"""Tests for time passage system."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime, timedelta
from terminal_buddy.pet import Pet
from terminal_buddy.ticker import Ticker


class TestTickerConstants(unittest.TestCase):
    """Test ticker decay rate constants."""

    def test_hunger_decay_rate(self):
        """Test hunger decay rate is -3 per hour."""
        self.assertEqual(Ticker.HUNGER_DECAY_PER_HOUR, 3.0)

    def test_mood_decay_rate(self):
        """Test mood decay rate is -2 per hour."""
        self.assertEqual(Ticker.MOOD_DECAY_PER_HOUR, 2.0)

    def test_energy_recovery_rate(self):
        """Test energy recovery rate is +5 per hour."""
        self.assertEqual(Ticker.ENERGY_RECOVERY_PER_HOUR, 5.0)


class TestHoursSince(unittest.TestCase):
    """Test hours_since static method."""

    def test_hours_since_recent_time(self):
        """Test hours since a very recent time."""
        now = datetime.now().isoformat()
        hours = Ticker.hours_since(now)
        self.assertAlmostEqual(hours, 0, delta=0.1)

    def test_hours_since_one_hour_ago(self):
        """Test hours since one hour ago."""
        past = (datetime.now() - timedelta(hours=1)).isoformat()
        hours = Ticker.hours_since(past)
        self.assertAlmostEqual(hours, 1, delta=0.1)

    def test_hours_since_multiple_hours(self):
        """Test hours since multiple hours ago."""
        for hours_ago in [2, 5, 10, 24, 48]:
            past = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
            hours = Ticker.hours_since(past)
            self.assertAlmostEqual(hours, hours_ago, delta=0.5,
                                  msg=f"Failed for {hours_ago} hours ago")

    def test_hours_since_invalid_string(self):
        """Test hours_since handles invalid string."""
        hours = Ticker.hours_since("not a valid datetime")
        self.assertEqual(hours, 0.0)

    def test_hours_since_none(self):
        """Test hours_since handles None."""
        hours = Ticker.hours_since(None)
        self.assertEqual(hours, 0.0)

    def test_hours_since_empty_string(self):
        """Test hours_since handles empty string."""
        hours = Ticker.hours_since("")
        self.assertEqual(hours, 0.0)


class TestTickerTick(unittest.TestCase):
    """Test tick method."""

    def test_tick_no_time_passed(self):
        """Test tick with no time passed doesn't change stats."""
        pet = Pet(name="TestPet")
        original_hunger = pet.hunger
        original_mood = pet.mood
        original_energy = pet.energy
        
        # Set last interaction to now
        pet.last_interaction = datetime.now().isoformat()
        
        messages = Ticker.tick(pet)
        
        self.assertEqual(pet.hunger, original_hunger)
        self.assertEqual(pet.mood, original_mood)
        self.assertEqual(pet.energy, original_energy)

    def test_tick_one_hour_decay(self):
        """Test tick with 1 hour passed applies correct decay."""
        pet = Pet(name="TestPet")
        pet.hunger = 50
        pet.mood = 50
        pet.energy = 50
        
        # Set last interaction to 1 hour ago
        pet.last_interaction = (datetime.now() - timedelta(hours=1)).isoformat()
        
        Ticker.tick(pet)
        
        # Expected: hunger -3, mood -2, energy +5
        self.assertEqual(pet.hunger, 47)  # 50 - 3
        self.assertEqual(pet.mood, 48)    # 50 - 2
        self.assertEqual(pet.energy, 55)  # 50 + 5

    def test_tick_multiple_hours_decay(self):
        """Test tick with multiple hours applies correct decay."""
        pet = Pet(name="TestPet")
        pet.hunger = 100
        pet.mood = 100
        pet.energy = 50
        
        # Set last interaction to 5 hours ago
        pet.last_interaction = (datetime.now() - timedelta(hours=5)).isoformat()
        
        Ticker.tick(pet)
        
        # Expected: hunger -15, mood -10, energy +25
        self.assertEqual(pet.hunger, 85)   # 100 - 15
        self.assertEqual(pet.mood, 90)     # 100 - 10
        self.assertEqual(pet.energy, 75)   # 50 + 25

    def test_tick_updates_last_interaction(self):
        """Test tick updates last_interaction timestamp."""
        pet = Pet(name="TestPet")
        pet.last_interaction = (datetime.now() - timedelta(hours=1)).isoformat()
        old_time = pet.last_interaction
        
        Ticker.tick(pet)
        
        self.assertNotEqual(pet.last_interaction, old_time)

    def test_tick_dead_pet(self):
        """Test tick on dead pet returns appropriate message."""
        pet = Pet(name="TestPet")
        pet.is_alive = False
        
        messages = Ticker.tick(pet)
        
        self.assertTrue(any("no longer with us" in m for m in messages))


class TestTickerBoundaryValues(unittest.TestCase):
    """Test boundary values in ticker."""

    def test_hunger_does_not_go_negative(self):
        """Test hunger doesn't go below 0."""
        pet = Pet(name="TestPet")
        pet.hunger = 10
        pet.mood = 50
        pet.energy = 50
        
        # Set last interaction to 10 hours ago (would be -30 hunger)
        pet.last_interaction = (datetime.now() - timedelta(hours=10)).isoformat()
        
        Ticker.tick(pet)
        
        self.assertGreaterEqual(pet.hunger, 0)

    def test_mood_does_not_go_negative(self):
        """Test mood doesn't go below 0."""
        pet = Pet(name="TestPet")
        pet.hunger = 50
        pet.mood = 5
        pet.energy = 50
        
        # Set last interaction to 5 hours ago (would be -10 mood)
        pet.last_interaction = (datetime.now() - timedelta(hours=5)).isoformat()
        
        Ticker.tick(pet)
        
        self.assertGreaterEqual(pet.mood, 0)

    def test_energy_does_not_exceed_100(self):
        """Test energy doesn't exceed 100."""
        pet = Pet(name="TestPet")
        pet.hunger = 50
        pet.mood = 50
        pet.energy = 90
        
        # Set last interaction to 5 hours ago (would be +25 energy)
        pet.last_interaction = (datetime.now() - timedelta(hours=5)).isoformat()
        
        Ticker.tick(pet)
        
        self.assertLessEqual(pet.energy, 100)

    def test_zero_time_interval(self):
        """Test tick with zero time interval."""
        pet = Pet(name="TestPet")
        original_hunger = pet.hunger
        
        # Set to now
        pet.last_interaction = datetime.now().isoformat()
        
        messages = Ticker.tick(pet)
        
        # No decay with 0 hours
        self.assertEqual(pet.hunger, original_hunger)

    def test_starvation_kills_pet(self):
        """Test pet dies when hunger reaches 0."""
        pet = Pet(name="TestPet")
        pet.hunger = 3  # Will go to 0 with 1 hour
        pet.mood = 50
        pet.energy = 50
        
        pet.last_interaction = (datetime.now() - timedelta(hours=1)).isoformat()
        
        Ticker.tick(pet)
        
        self.assertFalse(pet.is_alive)


class TestTickerMessages(unittest.TestCase):
    """Test ticker message generation."""

    def test_no_message_for_short_absence(self):
        """Test no time-related message for short absence."""
        pet = Pet(name="TestPet")
        pet.last_interaction = (datetime.now() - timedelta(minutes=30)).isoformat()
        
        messages = Ticker.tick(pet)
        
        # No "hours passed" message for < 1 hour
        self.assertFalse(any("hours have passed" in m for m in messages))

    def test_message_for_one_hour_absence(self):
        """Test message appears for 1+ hour absence."""
        pet = Pet(name="TestPet")
        pet.last_interaction = (datetime.now() - timedelta(hours=2)).isoformat()
        
        messages = Ticker.tick(pet)
        
        self.assertTrue(any("hours have passed" in m for m in messages))

    def test_message_for_24_hour_absence(self):
        """Test special message for 24+ hour absence."""
        pet = Pet(name="TestPet")
        pet.hunger = 80
        pet.mood = 80
        pet.last_interaction = (datetime.now() - timedelta(hours=25)).isoformat()
        
        messages = Ticker.tick(pet)
        
        self.assertTrue(any("missed you" in m for m in messages))

    def test_hunger_warning_message(self):
        """Test hunger warning appears when hungry."""
        pet = Pet(name="TestPet")
        pet.hunger = 80
        pet.mood = 80
        pet.energy = 80
        
        # 8 hours = 24 hunger loss > 20
        pet.last_interaction = (datetime.now() - timedelta(hours=8)).isoformat()
        
        messages = Ticker.tick(pet)
        
        self.assertTrue(any("hungry" in m.lower() for m in messages))

    def test_lonely_message(self):
        """Test lonely message appears when mood drops significantly."""
        pet = Pet(name="TestPet")
        pet.hunger = 80
        pet.mood = 80
        pet.energy = 80
        
        # 8 hours = 16 mood loss > 15
        pet.last_interaction = (datetime.now() - timedelta(hours=8)).isoformat()
        
        messages = Ticker.tick(pet)
        
        self.assertTrue(any("lonely" in m.lower() for m in messages))

    def test_rested_message(self):
        """Test rested message appears when energy recovers."""
        pet = Pet(name="TestPet")
        pet.hunger = 80
        pet.mood = 80
        pet.energy = 50
        
        # 5 hours = 25 energy gain > 20
        pet.last_interaction = (datetime.now() - timedelta(hours=5)).isoformat()
        
        messages = Ticker.tick(pet)
        
        self.assertTrue(any("rested" in m.lower() for m in messages))


if __name__ == "__main__":
    unittest.main()
