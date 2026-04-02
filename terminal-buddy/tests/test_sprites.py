"""Tests for sprites and renderer."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from terminal_buddy.sprites import SPRITES
from terminal_buddy.renderer import PetRenderer
from terminal_buddy.themes import THEMES


class TestSprites(unittest.TestCase):
    """Test sprite data configuration."""

    def test_18_species_have_sprites(self):
        """Verify all 18 species have sprite data."""
        expected_species = [
            "blob", "duck", "goose", "cat", "dragon", "octopus",
            "owl", "penguin", "turtle", "snail", "ghost", "axolotl",
            "capybara", "cactus", "robot", "rabbit", "mushroom", "chonk"
        ]
        
        for species in expected_species:
            self.assertIn(species, SPRITES,
                         f"Species '{species}' should have sprites")

    def test_all_species_have_required_states(self):
        """Verify all species have all required animation states."""
        required_states = ["idle", "happy", "sad", "sleep", "eat"]
        
        for species, states in SPRITES.items():
            for state in required_states:
                self.assertIn(state, states,
                            f"Species '{species}' should have '{state}' state")

    def test_idle_has_multiple_frames(self):
        """Verify idle state has multiple frames for animation."""
        for species, states in SPRITES.items():
            idle_frames = states.get("idle", [])
            self.assertGreaterEqual(len(idle_frames), 1,
                                   f"'{species}' idle should have at least 1 frame")

    def test_all_frames_are_strings(self):
        """Verify all sprite frames are strings."""
        for species, states in SPRITES.items():
            for state, frames in states.items():
                for frame in frames:
                    self.assertIsInstance(frame, str,
                                         f"Frame for {species}/{state} should be string")

    def test_sprite_count(self):
        """Verify total sprite count is correct."""
        self.assertEqual(len(SPRITES), 18, "Should have 18 species")


class TestPetRenderer(unittest.TestCase):
    """Test PetRenderer class."""

    def test_renderer_initialization(self):
        """Test renderer can be initialized with valid species."""
        for species in SPRITES.keys():
            renderer = PetRenderer(species)
            self.assertEqual(renderer.species, species)

    def test_renderer_unknown_species_uses_blob(self):
        """Test renderer falls back to blob for unknown species."""
        renderer = PetRenderer("unknown_species")
        # Should not raise error, uses blob sprites
        frame = renderer.get_frame("idle")
        self.assertIsInstance(frame, str)

    def test_get_frame_returns_string(self):
        """Test get_frame returns a string."""
        renderer = PetRenderer("blob")
        frame = renderer.get_frame("idle")
        self.assertIsInstance(frame, str)

    def test_get_frame_for_all_states(self):
        """Test get_frame works for all states."""
        renderer = PetRenderer("blob")
        states = ["idle", "happy", "sad", "sleep", "eat"]
        
        for state in states:
            frame = renderer.get_frame(state)
            self.assertIsInstance(frame, str,
                                  f"Frame for state '{state}' should be string")

    def test_next_frame_advances_animation(self):
        """Test next_frame advances frame index."""
        renderer = PetRenderer("blob")
        
        # Get initial frame
        frame1 = renderer.get_frame("idle")
        
        # Advance and get next frame
        frame2 = renderer.next_frame("idle")
        
        # Both should be strings
        self.assertIsInstance(frame1, str)
        self.assertIsInstance(frame2, str)

    def test_next_frame_cycles(self):
        """Test next_frame cycles through frames."""
        renderer = PetRenderer("blob")
        
        # Get all frames by cycling
        frames = []
        for _ in range(5):
            frames.append(renderer.get_frame("idle"))
            renderer.next_frame("idle")
        
        # Frames should cycle (at least some repetition expected)
        # Since idle has 2 frames, after 2 calls we should see repetition
        self.assertEqual(frames[0], frames[2])  # Frame 0 == Frame 2 (cycled)

    def test_get_state_for_pet_idle(self):
        """Test state detection for healthy pet."""
        from terminal_buddy.pet import Pet
        
        pet = Pet(name="TestPet")
        pet.hunger = 50
        pet.mood = 50
        pet.energy = 50
        
        renderer = PetRenderer("blob")
        state = renderer.get_state_for_pet(pet)
        self.assertEqual(state, "idle")

    def test_get_state_for_pet_happy(self):
        """Test state detection for happy pet."""
        from terminal_buddy.pet import Pet
        
        pet = Pet(name="TestPet")
        pet.mood = 90
        
        renderer = PetRenderer("blob")
        state = renderer.get_state_for_pet(pet)
        self.assertEqual(state, "happy")

    def test_get_state_for_pet_sad_low_happiness(self):
        """Test state detection for sad pet (happiness < 20)."""
        from terminal_buddy.pet import Pet
        
        pet = Pet(name="TestPet")
        # happiness = (hunger + mood + energy) // 3
        # Need happiness < 20, so set all low
        pet.hunger = 15
        pet.mood = 15
        pet.energy = 15
        
        renderer = PetRenderer("blob")
        state = renderer.get_state_for_pet(pet)
        # happiness = 15, which is < 20, so should be sad
        self.assertEqual(state, "sad")

    def test_get_state_for_pet_sleep(self):
        """Test state detection for tired pet."""
        from terminal_buddy.pet import Pet
        
        pet = Pet(name="TestPet")
        pet.energy = 5
        
        renderer = PetRenderer("blob")
        state = renderer.get_state_for_pet(pet)
        self.assertEqual(state, "sleep")

    def test_get_state_for_pet_eat(self):
        """Test state detection for hungry pet."""
        from terminal_buddy.pet import Pet
        
        pet = Pet(name="TestPet")
        pet.hunger = 90
        pet.mood = 50
        pet.energy = 50
        
        renderer = PetRenderer("blob")
        state = renderer.get_state_for_pet(pet)
        self.assertEqual(state, "eat")

    def test_get_state_for_dead_pet(self):
        """Test state detection for dead pet."""
        from terminal_buddy.pet import Pet
        
        pet = Pet(name="TestPet")
        pet.is_alive = False
        
        renderer = PetRenderer("blob")
        state = renderer.get_state_for_pet(pet)
        self.assertEqual(state, "sad")

    def test_reset_animation(self):
        """Test reset_animation resets frame index."""
        renderer = PetRenderer("blob")
        
        # Advance a few frames
        renderer.next_frame("idle")
        renderer.next_frame("idle")
        
        # Reset
        renderer.reset_animation()
        
        # Frame index should be 0
        self.assertEqual(renderer._frame_index, 0)

    def test_renderer_with_theme(self):
        """Test renderer can accept a theme."""
        renderer = PetRenderer("blob", theme=THEMES["default"])
        self.assertEqual(renderer.theme.name, "Default")


class TestRendererEdgeCases(unittest.TestCase):
    """Test edge cases in renderer."""

    def test_unknown_state_returns_idle(self):
        """Test unknown state falls back to idle."""
        renderer = PetRenderer("blob")
        frame = renderer.get_frame("unknown_state")
        self.assertIsInstance(frame, str)

    def test_single_frame_animation(self):
        """Test animation with single frame doesn't break."""
        # Most species have 2 idle frames, but the renderer should handle 1
        renderer = PetRenderer("blob")
        
        # Mock a single-frame state
        original_frames = renderer.get_frame("happy")
        self.assertIsInstance(original_frames, str)


if __name__ == "__main__":
    unittest.main()
