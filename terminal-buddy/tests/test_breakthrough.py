# -*- coding: utf-8 -*-
"""Tests for breakthrough (phase progression) system."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from terminal_buddy.pet import Pet
from terminal_buddy.breakthrough import (
    get_phase_info, get_level_cap, can_breakthrough, perform_breakthrough,
    get_breakthrough_status, get_material_display, PHASES, MATERIAL_KEYS
)


class TestPhaseInfo(unittest.TestCase):
    def test_all_phases_defined(self):
        for phase in range(1, 6):
            info = get_phase_info(phase)
            self.assertIn("name", info)
            self.assertIn("level_range", info)
            self.assertIn("material", info)
    
    def test_invalid_phase_returns_phase1(self):
        info = get_phase_info(99)
        self.assertEqual(info, PHASES[1])


class TestLevelCap(unittest.TestCase):
    def test_phase_caps(self):
        self.assertEqual(get_level_cap(1), 15)
        self.assertEqual(get_level_cap(2), 30)
        self.assertEqual(get_level_cap(3), 45)
        self.assertEqual(get_level_cap(4), 60)
        self.assertEqual(get_level_cap(5), 75)


class TestCanBreakthrough(unittest.TestCase):
    def test_cannot_at_low_level(self):
        pet = Pet(name="Test", level=5, phase=1)
        self.assertFalse(can_breakthrough(pet))
    
    def test_cannot_without_materials(self):
        pet = Pet(name="Test", level=15, phase=1)
        self.assertFalse(can_breakthrough(pet))
    
    def test_can_with_level_and_materials(self):
        pet = Pet(name="Test", level=15, phase=1)
        pet.breakthrough_materials = {"basic_stone": 1}
        self.assertTrue(can_breakthrough(pet))
    
    def test_cannot_at_max_phase(self):
        pet = Pet(name="Test", level=75, phase=5)
        pet.breakthrough_materials = {"ultimate_stone": 1}
        self.assertFalse(can_breakthrough(pet))


class TestPerformBreakthrough(unittest.TestCase):
    def test_successful_breakthrough(self):
        pet = Pet(name="Test", level=15, phase=1)
        pet.breakthrough_materials = {"basic_stone": 2}
        msg = perform_breakthrough(pet)
        self.assertIsNotNone(msg)
        self.assertEqual(pet.phase, 2)
        self.assertEqual(pet.breakthrough_materials["basic_stone"], 1)
    
    def test_failed_breakthrough(self):
        pet = Pet(name="Test", level=5, phase=1)
        msg = perform_breakthrough(pet)
        self.assertIsNone(msg)
        self.assertEqual(pet.phase, 1)


class TestBreakthroughStatus(unittest.TestCase):
    def test_status_normal(self):
        pet = Pet(name="Test", level=5, phase=1)
        status = get_breakthrough_status(pet, "zh")
        self.assertIn("初阶", status)
        self.assertIn("5/15", status)
    
    def test_status_max(self):
        pet = Pet(name="Test", level=75, phase=5)
        status = get_breakthrough_status(pet, "zh")
        self.assertIn("已满级", status)
    
    def test_status_english(self):
        pet = Pet(name="Test", level=5, phase=1)
        status = get_breakthrough_status(pet, "en")
        self.assertIn("Novice", status)


class TestMaterialDisplay(unittest.TestCase):
    def test_no_materials(self):
        pet = Pet(name="Test")
        display = get_material_display(pet, "zh")
        # Should show "无材料" or similar
        self.assertIsInstance(display, str)
    
    def test_with_materials(self):
        pet = Pet(name="Test")
        pet.breakthrough_materials = {"basic_stone": 3}
        display = get_material_display(pet, "zh")
        self.assertIn("3", display)


if __name__ == "__main__":
    unittest.main()
