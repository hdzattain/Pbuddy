"""Tests for evolution system."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from terminal_buddy.pet import Pet
from terminal_buddy.evolution import EvolutionSystem, EVOLUTION_PATHS, STARTER_SPECIES
from terminal_buddy.i18n import set_language


class TestEvolutionPaths(unittest.TestCase):
    """Test evolution path configuration."""

    def test_six_evolution_chains_exist(self):
        """Verify 6 evolution chains are defined."""
        self.assertEqual(len(EVOLUTION_PATHS), 6, 
                         "Should have 6 evolution chains")

    def test_all_starter_species_have_evolution_paths(self):
        """Verify all starter species have evolution paths."""
        for starter in STARTER_SPECIES:
            self.assertIn(starter, EVOLUTION_PATHS,
                         f"Starter '{starter}' should have evolution path")

    def test_evolution_chain_has_two_stages(self):
        """Verify each chain has 2 evolution stages (Lv.5 and Lv.15)."""
        for starter, evolutions in EVOLUTION_PATHS.items():
            self.assertEqual(len(evolutions), 2,
                           f"Evolution chain for '{starter}' should have 2 stages")
            
            # First evolution at level 5
            self.assertEqual(evolutions[0][0], 5,
                           f"First evolution for '{starter}' should be at level 5")
            
            # Second evolution at level 15
            self.assertEqual(evolutions[1][0], 15,
                           f"Second evolution for '{starter}' should be at level 15")

    def test_starter_species_tuple(self):
        """Verify STARTER_SPECIES is properly defined."""
        expected_starters = ("blob", "duck", "cat", "cactus", "snail", "rabbit")
        self.assertEqual(STARTER_SPECIES, expected_starters)


class TestCheckEvolution(unittest.TestCase):
    """Test check_evolution method."""

    def test_level_5_triggers_first_evolution(self):
        """Test level 5 triggers first evolution for all starters."""
        evolution_map = {
            "blob": "ghost",
            "duck": "goose", 
            "cat": "owl",
            "cactus": "mushroom",
            "snail": "turtle",
            "rabbit": "capybara"
        }
        
        for starter, expected_evolution in evolution_map.items():
            pet = Pet(name="TestPet", species=starter, level=5)
            result = EvolutionSystem.check_evolution(pet)
            self.assertEqual(result, expected_evolution,
                           f"Level 5 {starter} should evolve to {expected_evolution}")

    def test_level_15_triggers_second_evolution(self):
        """Test level 15 triggers second evolution for evolved species."""
        evolution_map = {
            "ghost": "dragon",
            "goose": "penguin",
            "owl": "axolotl",
            "mushroom": "robot",
            "turtle": "octopus",
            "capybara": "chonk"
        }
        
        for evolved, expected_final in evolution_map.items():
            pet = Pet(name="TestPet", species=evolved, level=15)
            result = EvolutionSystem.check_evolution(pet)
            self.assertEqual(result, expected_final,
                           f"Level 15 {evolved} should evolve to {expected_final}")

    def test_non_evolution_level_no_change(self):
        """Test that non-evolution levels don't trigger evolution."""
        # Test level below 5
        pet = Pet(name="TestPet", species="blob", level=4)
        result = EvolutionSystem.check_evolution(pet)
        self.assertIsNone(result)
        
        # Test level between 5 and 15
        pet = Pet(name="TestPet", species="ghost", level=10)
        result = EvolutionSystem.check_evolution(pet)
        self.assertIsNone(result)

    def test_final_form_no_evolution(self):
        """Test that final forms don't evolve further."""
        final_forms = ["dragon", "penguin", "axolotl", "robot", "octopus", "chonk"]
        
        for species in final_forms:
            pet = Pet(name="TestPet", species=species, level=20)
            result = EvolutionSystem.check_evolution(pet)
            self.assertIsNone(result,
                            f"Final form '{species}' should not evolve")

    def test_dead_pet_no_evolution(self):
        """Test dead pets don't evolve."""
        pet = Pet(name="TestPet", species="blob", level=5)
        pet.is_alive = False
        result = EvolutionSystem.check_evolution(pet)
        self.assertIsNone(result)

    def test_unknown_species_no_evolution(self):
        """Test unknown species doesn't cause errors."""
        pet = Pet(name="TestPet", species="unknown_creature", level=5)
        result = EvolutionSystem.check_evolution(pet)
        # Should not raise an error, might return None
        self.assertIsNone(result)


class TestEvolve(unittest.TestCase):
    """Test evolve method."""

    def setUp(self):
        """Set language to English for consistent test results."""
        set_language("en")

    def test_evolve_changes_species(self):
        """Test evolve actually changes pet species."""
        pet = Pet(name="TestPet", species="blob", level=5)
        msg = EvolutionSystem.evolve(pet)
        
        self.assertEqual(pet.species, "ghost")
        self.assertIn("evolved", msg.lower())
        # Use translated species names (capitalized)
        self.assertIn("Blob", msg)
        self.assertIn("Ghost", msg)

    def test_evolve_returns_none_when_no_evolution(self):
        """Test evolve returns None when no evolution available."""
        pet = Pet(name="TestPet", species="dragon", level=20)
        msg = EvolutionSystem.evolve(pet)
        
        self.assertIsNone(msg)
        self.assertEqual(pet.species, "dragon")

    def test_evolve_message_format(self):
        """Test evolution message format is correct."""
        pet = Pet(name="Buddy", species="cat", level=5)
        msg = EvolutionSystem.evolve(pet)
        
        self.assertIn("Buddy", msg)
        # Use translated species names (capitalized)
        self.assertIn("Cat", msg)
        self.assertIn("Owl", msg)
        self.assertIn("evolved", msg.lower())


class TestGetEvolutionChain(unittest.TestCase):
    """Test get_evolution_chain method."""

    def test_full_chain_for_starter(self):
        """Test getting full evolution chain for starter species."""
        chain = EvolutionSystem.get_evolution_chain("blob")
        self.assertEqual(chain, ["blob", "ghost", "dragon"])

    def test_chain_for_unknown_species(self):
        """Test chain for unknown species returns just the species."""
        chain = EvolutionSystem.get_evolution_chain("unknown")
        self.assertEqual(chain, ["unknown"])

    def test_all_starter_chains(self):
        """Test all starter species have correct chains."""
        expected_chains = {
            "blob": ["blob", "ghost", "dragon"],
            "duck": ["duck", "goose", "penguin"],
            "cat": ["cat", "owl", "axolotl"],
            "cactus": ["cactus", "mushroom", "robot"],
            "snail": ["snail", "turtle", "octopus"],
            "rabbit": ["rabbit", "capybara", "chonk"]
        }
        
        for starter, expected in expected_chains.items():
            chain = EvolutionSystem.get_evolution_chain(starter)
            self.assertEqual(chain, expected)


class TestEvolutionEdgeCases(unittest.TestCase):
    """Test edge cases in evolution system."""

    def test_level_exactly_5(self):
        """Test evolution triggers at exactly level 5."""
        pet = Pet(name="TestPet", species="blob", level=5)
        result = EvolutionSystem.check_evolution(pet)
        self.assertEqual(result, "ghost")

    def test_level_exactly_15(self):
        """Test evolution triggers at exactly level 15."""
        pet = Pet(name="TestPet", species="ghost", level=15)
        result = EvolutionSystem.check_evolution(pet)
        self.assertEqual(result, "dragon")

    def test_level_above_15_still_evolved(self):
        """Test species evolved at 15 doesn't evolve further."""
        # Simulate a pet that was at level 10 ghost, then gained levels
        pet = Pet(name="TestPet", species="ghost", level=20)
        result = EvolutionSystem.check_evolution(pet)
        self.assertEqual(result, "dragon")

    def test_multiple_calls_idempotent(self):
        """Test calling evolve multiple times doesn't break."""
        pet = Pet(name="TestPet", species="blob", level=5)
        
        # First evolution
        EvolutionSystem.evolve(pet)
        self.assertEqual(pet.species, "ghost")
        
        # Second call should not change (already ghost, needs level 15)
        result = EvolutionSystem.check_evolution(pet)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
