import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil
from terminal_buddy.pet import Pet
from terminal_buddy.ticker import Ticker
from terminal_buddy.evolution import EvolutionSystem, STARTER_SPECIES
from terminal_buddy.storage import PetStorage
from terminal_buddy.actions import PetActions
from terminal_buddy.i18n import set_language


class TestPet(unittest.TestCase):
    def setUp(self):
        set_language("en")
    
    def tearDown(self):
        set_language("zh")
    
    def test_pet_creation(self):
        pet = Pet(name="TestPet", species="blob")
        self.assertEqual(pet.name, "TestPet")
        self.assertEqual(pet.species, "blob")
        self.assertEqual(pet.level, 1)
        self.assertTrue(pet.is_alive)
    
    def test_pet_feed(self):
        pet = Pet(name="TestPet")
        pet.hunger = 50
        msg = pet.feed(20)
        self.assertEqual(pet.hunger, 70)
        self.assertIn("ate a snack", msg)
    
    def test_pet_play(self):
        pet = Pet(name="TestPet")
        pet.mood = 50
        pet.energy = 50
        msg = pet.play(15)
        self.assertEqual(pet.mood, 65)
        self.assertEqual(pet.energy, 40)
        self.assertIn("had fun", msg)
    
    def test_pet_sleep(self):
        pet = Pet(name="TestPet")
        pet.energy = 50
        msg = pet.sleep(30)
        self.assertEqual(pet.energy, 80)
        self.assertIn("nap", msg)
    
    def test_pet_train(self):
        pet = Pet(name="TestPet")
        pet.energy = 50
        pet.mood = 50
        msg = pet.train(25)
        self.assertEqual(pet.energy, 35)
        self.assertEqual(pet.mood, 45)
        self.assertIn("trained", msg)
    
    def test_pet_pet_action(self):
        pet = Pet(name="TestPet")
        pet.mood = 50
        msg = pet.pet_action(10)
        self.assertEqual(pet.mood, 60)
        self.assertIn("cuddles", msg)
    
    def test_pet_gain_xp_and_level_up(self):
        pet = Pet(name="TestPet")
        pet.xp = 90
        msg = pet.gain_xp(20)
        self.assertEqual(pet.level, 2)
        self.assertIn("Level up", msg)
    
    def test_pet_happiness(self):
        pet = Pet(name="TestPet")
        pet.hunger = 60
        pet.mood = 60
        pet.energy = 60
        self.assertEqual(pet.happiness, 60)
    
    def test_pet_to_dict_from_dict(self):
        pet = Pet(name="TestPet", species="cat")
        data = pet.to_dict()
        self.assertEqual(data["name"], "TestPet")
        self.assertEqual(data["species"], "cat")
        
        restored = Pet.from_dict(data)
        self.assertEqual(restored.name, "TestPet")
        self.assertEqual(restored.species, "cat")
    
    def test_pet_new_fields_defaults(self):
        """Test new fields have correct defaults."""
        pet = Pet(name="TestPet")
        self.assertEqual(pet.rarity, 1)
        self.assertFalse(pet.is_shiny)
        self.assertEqual(pet.rarity_color, "white")
        self.assertEqual(pet.phase, 1)
        self.assertEqual(pet.breakthrough_materials, {})
        self.assertEqual(pet.travel_atlas, {})
        self.assertIsNone(pet.current_travel)
        self.assertEqual(pet.shiny_evolution_items, 0)
    
    def test_pet_to_dict_includes_new_fields(self):
        """Test to_dict includes rarity/breakthrough/travel fields."""
        pet = Pet(name="TestPet", rarity=3, is_shiny=True, phase=2)
        pet.breakthrough_materials = {"basic_stone": 1}
        pet.travel_atlas = {"1": ["北京"]}
        data = pet.to_dict()
        self.assertEqual(data["rarity"], 3)
        self.assertTrue(data["is_shiny"])
        self.assertEqual(data["phase"], 2)
        self.assertEqual(data["breakthrough_materials"], {"basic_stone": 1})
        self.assertEqual(data["travel_atlas"], {"1": ["北京"]})
    
    def test_pet_from_dict_backward_compatible(self):
        """Test from_dict works with old data without new fields."""
        old_data = {"name": "OldPet", "species": "blob", "level": 5}
        pet = Pet.from_dict(old_data)
        self.assertEqual(pet.name, "OldPet")
        self.assertEqual(pet.rarity, 1)
        self.assertEqual(pet.phase, 1)
        self.assertEqual(pet.travel_atlas, {})
    
    def test_level_cap_prevents_level_up(self):
        """Test level cap from breakthrough system."""
        pet = Pet(name="TestPet", level=14, phase=1)
        pet.xp = 1390  # xp_for_next_level at 14 is 1400
        msg = pet.gain_xp(20)
        self.assertEqual(pet.level, 15)
        # Now at cap, further XP should not increase level
        msg = pet.gain_xp(10000)
        self.assertEqual(pet.level, 15)
        self.assertEqual(pet.xp, 0)


class TestTicker(unittest.TestCase):
    def test_hours_since(self):
        from datetime import datetime, timedelta
        past = (datetime.now() - timedelta(hours=2)).isoformat()
        hours = Ticker.hours_since(past)
        self.assertAlmostEqual(hours, 2, delta=0.1)
    
    def test_tick_reduces_hunger(self):
        pet = Pet(name="TestPet")
        pet.hunger = 50
        from datetime import datetime, timedelta
        pet.last_interaction = (datetime.now() - timedelta(hours=1)).isoformat()
        Ticker.tick(pet)
        self.assertLess(pet.hunger, 50)


class TestEvolution(unittest.TestCase):
    def test_check_evolution_blob(self):
        pet = Pet(name="TestPet", species="blob", level=5)
        result = EvolutionSystem.check_evolution(pet)
        self.assertEqual(result, "ghost")
    
    def test_evolve(self):
        pet = Pet(name="TestPet", species="blob", level=5)
        msg = EvolutionSystem.evolve(pet)
        self.assertEqual(pet.species, "ghost")
        self.assertIn("evolved", msg)
    
    def test_get_evolution_chain(self):
        chain = EvolutionSystem.get_evolution_chain("blob")
        self.assertEqual(chain, ["blob", "ghost", "dragon"])


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_pets(self):
        pet = Pet(name="TestPet")
        self.storage.add_pet(pet)
        loaded = self.storage.load_pets()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].name, "TestPet")
    
    def test_get_pet(self):
        pet = Pet(name="TestPet")
        self.storage.add_pet(pet)
        found = self.storage.get_pet(pet.id)
        self.assertEqual(found.name, "TestPet")
    
    def test_remove_pet(self):
        pet = Pet(name="TestPet")
        self.storage.add_pet(pet)
        result = self.storage.remove_pet(pet.id)
        self.assertTrue(result)
        self.assertEqual(len(self.storage.load_pets()), 0)


class TestActions(unittest.TestCase):
    def setUp(self):
        set_language("en")
        self.temp_dir = tempfile.mkdtemp()
        self.storage = PetStorage(storage_dir=self.temp_dir)
        self.actions = PetActions(self.storage)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        set_language("zh")
    
    def test_create_pet(self):
        pet, msgs = self.actions.create_pet("Buddy", "blob")
        self.assertEqual(pet.name, "Buddy")
        self.assertEqual(pet.species, "blob")
    
    def test_interact_feed(self):
        pet, _ = self.actions.create_pet("Buddy", "blob")
        pet.hunger = 50
        self.storage.update_pet(pet)
        msgs = self.actions.interact(pet, "feed")
        self.assertTrue(any("ate" in m for m in msgs))


if __name__ == "__main__":
    unittest.main()
