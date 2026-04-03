"""Tests for pet action commands."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil
from datetime import datetime, timedelta
from terminal_buddy.pet import Pet
from terminal_buddy.storage import PetStorage
from terminal_buddy.actions import PetActions
from terminal_buddy.i18n import set_language


class TestPetActions(unittest.TestCase):
    """Test PetActions class."""

    def setUp(self):
        """Set up temporary storage for each test."""
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_create_pet_basic(self):
        """Test basic pet creation."""
        pet, messages = self.actions.create_pet("Buddy", "blob")
        
        self.assertEqual(pet.name, "Buddy")
        self.assertEqual(pet.species, "blob")
        self.assertTrue(pet.is_alive)
        self.assertTrue(any("Welcome" in m for m in messages))

    def test_create_pet_invalid_species_defaults_to_blob(self):
        """Test invalid species defaults to blob."""
        pet, messages = self.actions.create_pet("Test", "invalid_species")
        
        self.assertEqual(pet.species, "blob")
        self.assertTrue(any("defaulting" in m.lower() for m in messages))

    def test_create_pet_all_starters(self):
        """Test creating pets with all starter species."""
        starters = ["blob", "duck", "cat", "cactus", "snail", "rabbit"]
        
        for species in starters:
            pet, messages = self.actions.create_pet(f"Pet_{species}", species)
            self.assertEqual(pet.species, species)


class TestInteractFeed(unittest.TestCase):
    """Test feed interaction."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_feed_increases_hunger(self):
        """Test feeding increases hunger."""
        pet = Pet(name="TestPet", species="blob")
        pet.hunger = 50
        self.storage.add_pet(pet)
        
        messages = self.actions.interact(pet, "feed")
        
        self.assertGreater(pet.hunger, 50)
        self.assertTrue(any("ate" in m.lower() for m in messages))

    def test_feed_max_hunger(self):
        """Test feeding at max hunger doesn't exceed 100."""
        pet = Pet(name="TestPet", species="blob")
        pet.hunger = 95
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "feed")
        
        self.assertLessEqual(pet.hunger, 100)

    def test_feed_gives_xp(self):
        """Test feeding gives XP."""
        pet = Pet(name="TestPet", species="blob")
        original_xp = pet.xp
        
        self.actions.interact(pet, "feed")
        
        self.assertGreater(pet.xp, original_xp)


class TestInteractPlay(unittest.TestCase):
    """Test play interaction."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_play_increases_mood(self):
        """Test playing increases mood."""
        pet = Pet(name="TestPet", species="blob")
        pet.mood = 50
        pet.energy = 50
        self.storage.add_pet(pet)
        
        messages = self.actions.interact(pet, "play")
        
        self.assertGreater(pet.mood, 50)
        self.assertTrue(any("fun" in m.lower() for m in messages))

    def test_play_decreases_energy(self):
        """Test playing decreases energy."""
        pet = Pet(name="TestPet", species="blob")
        pet.energy = 50
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "play")
        
        self.assertLess(pet.energy, 50)

    def test_play_gives_xp(self):
        """Test playing gives XP."""
        pet = Pet(name="TestPet", species="blob")
        original_xp = pet.xp
        
        self.actions.interact(pet, "play")
        
        self.assertGreater(pet.xp, original_xp)


class TestInteractSleep(unittest.TestCase):
    """Test sleep interaction."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_sleep_increases_energy(self):
        """Test sleeping increases energy."""
        pet = Pet(name="TestPet", species="blob")
        pet.energy = 30
        self.storage.add_pet(pet)
        
        messages = self.actions.interact(pet, "sleep")
        
        self.assertGreater(pet.energy, 30)
        self.assertTrue(any("nap" in m.lower() for m in messages))

    def test_sleep_decreases_hunger(self):
        """Test sleeping decreases hunger slightly."""
        pet = Pet(name="TestPet", species="blob")
        pet.hunger = 50
        pet.energy = 30
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "sleep")
        
        self.assertLess(pet.hunger, 50)

    def test_sleep_max_energy(self):
        """Test sleeping at max energy doesn't exceed 100."""
        pet = Pet(name="TestPet", species="blob")
        pet.energy = 90
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "sleep")
        
        self.assertLessEqual(pet.energy, 100)


class TestInteractTrain(unittest.TestCase):
    """Test train interaction."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_train_gives_xp(self):
        """Test training gives XP."""
        pet = Pet(name="TestPet", species="blob")
        pet.energy = 50
        original_xp = pet.xp
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "train")
        
        self.assertGreater(pet.xp, original_xp)

    def test_train_decreases_energy(self):
        """Test training decreases energy."""
        pet = Pet(name="TestPet", species="blob")
        pet.energy = 50
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "train")
        
        self.assertLess(pet.energy, 50)

    def test_train_decreases_mood(self):
        """Test training decreases mood slightly."""
        pet = Pet(name="TestPet", species="blob")
        pet.mood = 50
        pet.energy = 50
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "train")
        
        self.assertLess(pet.mood, 50)

    def test_train_too_tired(self):
        """Test training fails when too tired."""
        pet = Pet(name="TestPet", species="blob")
        pet.energy = 10
        self.storage.add_pet(pet)
        
        messages = self.actions.interact(pet, "train")
        
        self.assertTrue(any("too tired" in m.lower() for m in messages))


class TestInteractPet(unittest.TestCase):
    """Test pet (cuddle) interaction."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_pet_increases_mood(self):
        """Test petting increases mood."""
        pet = Pet(name="TestPet", species="blob")
        pet.mood = 50
        self.storage.add_pet(pet)
        
        messages = self.actions.interact(pet, "pet")
        
        self.assertGreater(pet.mood, 50)
        self.assertTrue(any("cuddle" in m.lower() for m in messages))

    def test_pet_max_mood(self):
        """Test petting at max mood doesn't exceed 100."""
        pet = Pet(name="TestPet", species="blob")
        pet.mood = 95
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "pet")
        
        self.assertLessEqual(pet.mood, 100)


class TestInteractEdgeCases(unittest.TestCase):
    """Test edge cases in interactions."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_interact_with_dead_pet(self):
        """Test interacting with dead pet."""
        pet = Pet(name="TestPet", species="blob")
        pet.is_alive = False
        self.storage.add_pet(pet)
        
        messages = self.actions.interact(pet, "feed")
        
        self.assertTrue(any("no longer with us" in m for m in messages))

    def test_unknown_action(self):
        """Test unknown action returns appropriate message."""
        pet = Pet(name="TestPet", species="blob")
        self.storage.add_pet(pet)
        
        messages = self.actions.interact(pet, "unknown_action")
        
        self.assertTrue(any("Unknown action" in m for m in messages))

    def test_action_case_insensitive(self):
        """Test actions are case insensitive."""
        pet = Pet(name="TestPet", species="blob")
        pet.hunger = 50
        self.storage.add_pet(pet)
        
        messages1 = self.actions.interact(pet, "FEED")
        self.assertTrue(any("ate" in m.lower() for m in messages1))
        
        messages2 = self.actions.interact(pet, "Feed")
        self.assertTrue(any("ate" in m.lower() for m in messages2))


class TestGetAllPets(unittest.TestCase):
    """Test get_all_pets method."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_get_all_pets_empty(self):
        """Test getting pets when none exist."""
        pets = self.actions.get_all_pets()
        self.assertEqual(len(pets), 0)

    def test_get_all_pets_multiple(self):
        """Test getting multiple pets."""
        self.actions.create_pet("Pet1", "blob")
        self.actions.create_pet("Pet2", "cat")
        
        pets = self.actions.get_all_pets()
        self.assertEqual(len(pets), 2)

    def test_get_all_pets_applies_tick(self):
        """Test get_all_pets applies time tick."""
        pet = Pet(name="TestPet", species="blob")
        pet.hunger = 50
        pet.last_interaction = (datetime.now() - timedelta(hours=2)).isoformat()
        self.storage.add_pet(pet)
        
        pets = self.actions.get_all_pets()
        
        # Hunger should have decayed due to tick
        self.assertLess(pets[0].hunger, 50)


class TestActionPersistence(unittest.TestCase):
    """Test that actions persist changes."""

    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")

    def test_feed_persists(self):
        """Test feed action persists changes."""
        pet, _ = self.actions.create_pet("TestPet", "blob")
        pet_id = pet.id
        pet.hunger = 50
        
        self.actions.interact(pet, "feed")
        
        # Load from storage and verify
        loaded = self.storage.get_pet(pet_id)
        self.assertGreater(loaded.hunger, 50)

    def test_level_up_persists(self):
        """Test level up from training persists."""
        pet = Pet(name="TestPet", species="blob")
        pet.xp = 90
        pet.energy = 50
        self.storage.add_pet(pet)
        
        self.actions.interact(pet, "train")
        
        # Load and verify level
        loaded = self.storage.get_pet(pet.id)
        if pet.level > 1:
            self.assertGreaterEqual(loaded.level, pet.level)


if __name__ == "__main__":
    unittest.main()
