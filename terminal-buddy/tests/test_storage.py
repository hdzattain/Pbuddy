"""Tests for pet data persistence."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from terminal_buddy.pet import Pet
from terminal_buddy.storage import PetStorage


class TestPetStorage(unittest.TestCase):
    """Test PetStorage class."""

    def setUp(self):
        """Set up temporary directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory after each test."""
        shutil.rmtree(self.temp_dir)

    def test_storage_dir_created(self):
        """Test storage directory is created if it doesn't exist."""
        new_dir = Path(self.temp_dir) / "subdir" / "storage"
        storage = PetStorage(storage_dir=new_dir)
        self.assertTrue(new_dir.exists())

    def test_save_and_load_single_pet(self):
        """Test saving and loading a single pet."""
        pet = Pet(name="Buddy", species="cat")
        self.storage.save_pets([pet])
        
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "Buddy")
        self.assertEqual(loaded[0].species, "cat")

    def test_save_and_load_multiple_pets(self):
        """Test saving and loading multiple pets."""
        pets = [
            Pet(name="Buddy", species="blob"),
            Pet(name="Max", species="cat"),
            Pet(name="Luna", species="duck")
        ]
        self.storage.save_pets(pets)
        
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 3)
        names = [p.name for p in loaded]
        self.assertIn("Buddy", names)
        self.assertIn("Max", names)
        self.assertIn("Luna", names)

    def test_load_empty_storage(self):
        """Test loading from empty storage returns empty list."""
        loaded = self.storage.load_pets()
        self.assertEqual(loaded, [])

    def test_load_nonexistent_file(self):
        """Test loading when pets.json doesn't exist."""
        # Don't save anything
        loaded = self.storage.load_pets()
        self.assertEqual(loaded, [])

    def test_add_pet(self):
        """Test adding a pet to storage."""
        pet = Pet(name="NewPet", species="rabbit")
        self.storage.add_pet(pet)
        
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "NewPet")

    def test_add_multiple_pets(self):
        """Test adding multiple pets sequentially."""
        pet1 = Pet(name="Pet1", species="blob")
        pet2 = Pet(name="Pet2", species="cat")
        
        self.storage.add_pet(pet1)
        self.storage.add_pet(pet2)
        
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 2)

    def test_remove_pet(self):
        """Test removing a pet from storage."""
        pet = Pet(name="ToRemove", species="blob")
        self.storage.add_pet(pet)
        
        result = self.storage.remove_pet(pet.id)
        self.assertTrue(result)
        
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 0)

    def test_remove_nonexistent_pet(self):
        """Test removing a pet that doesn't exist."""
        result = self.storage.remove_pet("nonexistent_id")
        self.assertFalse(result)

    def test_get_pet(self):
        """Test getting a specific pet by ID."""
        pet = Pet(name="FindMe", species="snail")
        self.storage.add_pet(pet)
        
        found = self.storage.get_pet(pet.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "FindMe")
        self.assertEqual(found.species, "snail")

    def test_get_nonexistent_pet(self):
        """Test getting a pet that doesn't exist."""
        found = self.storage.get_pet("nonexistent_id")
        self.assertIsNone(found)

    def test_update_pet(self):
        """Test updating an existing pet."""
        pet = Pet(name="ToUpdate", species="blob")
        self.storage.add_pet(pet)
        
        # Modify pet
        pet.hunger = 50
        pet.mood = 60
        pet.level = 5
        
        self.storage.update_pet(pet)
        
        # Load and verify
        loaded = self.storage.get_pet(pet.id)
        self.assertEqual(loaded.hunger, 50)
        self.assertEqual(loaded.mood, 60)
        self.assertEqual(loaded.level, 5)

    def test_update_nonexistent_pet_adds_it(self):
        """Test updating nonexistent pet adds it to storage."""
        pet = Pet(name="NewPet", species="cat")
        self.storage.update_pet(pet)
        
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "NewPet")


class TestStorageDataIntegrity(unittest.TestCase):
    """Test data integrity in storage operations."""

    def setUp(self):
        """Set up temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.temp_dir)

    def test_pet_all_attributes_preserved(self):
        """Test all pet attributes are preserved through save/load."""
        original = Pet(
            name="TestPet",
            species="dragon",
            hunger=75,
            mood=85,
            energy=65,
            xp=250,
            level=8,
            is_alive=True
        )
        
        self.storage.save_pets([original])
        loaded = self.storage.load_pets()[0]
        
        self.assertEqual(loaded.name, original.name)
        self.assertEqual(loaded.species, original.species)
        self.assertEqual(loaded.hunger, original.hunger)
        self.assertEqual(loaded.mood, original.mood)
        self.assertEqual(loaded.energy, original.energy)
        self.assertEqual(loaded.xp, original.xp)
        self.assertEqual(loaded.level, original.level)
        self.assertEqual(loaded.is_alive, original.is_alive)

    def test_dead_pet_preserved(self):
        """Test dead pet status is preserved."""
        pet = Pet(name="DeadPet", species="blob")
        pet.is_alive = False
        
        self.storage.save_pets([pet])
        loaded = self.storage.load_pets()[0]
        
        self.assertFalse(loaded.is_alive)

    def test_timestamps_preserved(self):
        """Test timestamps are preserved."""
        pet = Pet(name="TestPet")
        original_born = pet.born_at
        original_fed = pet.last_fed
        original_interaction = pet.last_interaction
        
        self.storage.save_pets([pet])
        loaded = self.storage.load_pets()[0]
        
        self.assertEqual(loaded.born_at, original_born)
        self.assertEqual(loaded.last_fed, original_fed)
        self.assertEqual(loaded.last_interaction, original_interaction)

    def test_file_encoding_utf8(self):
        """Test file is saved with UTF-8 encoding."""
        pet = Pet(name="テスト", species="blob")  # Japanese characters
        self.storage.save_pets([pet])
        
        # Read file directly and verify encoding
        file_path = Path(self.temp_dir) / "pets.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("テスト", content)


class TestStorageCorruptionHandling(unittest.TestCase):
    """Test handling of corrupted storage files."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_invalid_json_returns_empty_list(self):
        """Test invalid JSON returns empty list instead of crashing."""
        # Write invalid JSON
        file_path = Path(self.temp_dir) / "pets.json"
        with open(file_path, 'w') as f:
            f.write("not valid json {{{")
        
        loaded = self.storage.load_pets()
        self.assertEqual(loaded, [])

    def test_non_list_json_returns_empty_list(self):
        """Test non-list JSON returns empty list."""
        file_path = Path(self.temp_dir) / "pets.json"
        with open(file_path, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        loaded = self.storage.load_pets()
        self.assertEqual(loaded, [])

    def test_empty_file_returns_empty_list(self):
        """Test empty file returns empty list."""
        file_path = Path(self.temp_dir) / "pets.json"
        with open(file_path, 'w') as f:
            f.write("")
        
        loaded = self.storage.load_pets()
        self.assertEqual(loaded, [])


class TestStorageEdgeCases(unittest.TestCase):
    """Test edge cases in storage."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_save_empty_list(self):
        """Test saving empty list doesn't cause errors."""
        self.storage.save_pets([])
        loaded = self.storage.load_pets()
        self.assertEqual(loaded, [])

    def test_overwrite_existing_data(self):
        """Test that save_pets overwrites existing data."""
        pet1 = Pet(name="First", species="blob")
        self.storage.save_pets([pet1])
        
        pet2 = Pet(name="Second", species="cat")
        self.storage.save_pets([pet2])
        
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "Second")

    def test_default_storage_dir(self):
        """Test default storage directory is correct."""
        storage = PetStorage()
        expected_dir = Path.home() / ".terminal-buddy"
        self.assertEqual(storage.storage_dir, expected_dir)


if __name__ == "__main__":
    unittest.main()
