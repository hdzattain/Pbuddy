# -*- coding: utf-8 -*-
"""Tests for travel system."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from terminal_buddy.pet import Pet
from terminal_buddy.travel import (
    get_available_stage, is_polar_unlocked, start_travel, check_travel_complete,
    get_travel_status, get_atlas_progress, TRAVEL_STAGES, POLAR_LOCATIONS
)


class TestAvailableStage(unittest.TestCase):
    def test_default_stage_1(self):
        pet = Pet(name="Test")
        self.assertEqual(get_available_stage(pet), 1)
    
    def test_stage_2_after_completing_china(self):
        pet = Pet(name="Test")
        pet.travel_atlas = {"1": list(TRAVEL_STAGES[1]["locations"])}
        self.assertEqual(get_available_stage(pet), 2)
    
    def test_polar_unlocked_after_all_stages(self):
        pet = Pet(name="Test")
        pet.travel_atlas = {}
        for stage_num in range(1, 6):
            pet.travel_atlas[str(stage_num)] = list(TRAVEL_STAGES[stage_num]["locations"])
        self.assertEqual(get_available_stage(pet), 6)


class TestIsPolarUnlocked(unittest.TestCase):
    def test_not_unlocked_by_default(self):
        pet = Pet(name="Test")
        self.assertFalse(is_polar_unlocked(pet))
    
    def test_unlocked_after_all_stages(self):
        pet = Pet(name="Test")
        pet.travel_atlas = {}
        for stage_num in range(1, 6):
            pet.travel_atlas[str(stage_num)] = list(TRAVEL_STAGES[stage_num]["locations"])
        self.assertTrue(is_polar_unlocked(pet))


class TestStartTravel(unittest.TestCase):
    def test_start_travel_creates_travel(self):
        pet = Pet(name="Test")
        msg = start_travel(pet)
        self.assertIsNotNone(msg)
        self.assertIsNotNone(pet.current_travel)
        self.assertIn("stage", pet.current_travel)
        self.assertIn("location", pet.current_travel)
    
    def test_cannot_start_while_traveling(self):
        pet = Pet(name="Test")
        pet.current_travel = {"stage": 1, "location": "北京", "end_time": (datetime.now() + timedelta(hours=1)).isoformat()}
        msg = start_travel(pet)
        # 检查返回了消息（正在旅行中）
        self.assertIsNotNone(msg)
        # 中文消息包含"旅行中"
        self.assertIn("旅行中", msg)
    
    def test_dead_pet_cannot_travel(self):
        pet = Pet(name="Test")
        pet.is_alive = False
        msg = start_travel(pet)
        self.assertIsNotNone(msg)


class TestCheckTravelComplete(unittest.TestCase):
    def test_no_travel_returns_empty(self):
        pet = Pet(name="Test")
        msgs = check_travel_complete(pet)
        self.assertEqual(msgs, [])
    
    def test_ongoing_travel_returns_empty(self):
        pet = Pet(name="Test")
        pet.current_travel = {
            "stage": 1, "location": "北京", "stage_name": "中国之旅",
            "end_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        msgs = check_travel_complete(pet)
        self.assertEqual(msgs, [])
    
    def test_completed_travel_returns_messages(self):
        pet = Pet(name="Test")
        pet.current_travel = {
            "stage": 1, "location": "北京", "stage_name": "中国之旅",
            "start_time": (datetime.now() - timedelta(minutes=20)).isoformat(),
            "end_time": (datetime.now() - timedelta(minutes=1)).isoformat()
        }
        msgs = check_travel_complete(pet)
        self.assertGreater(len(msgs), 0)
        self.assertIsNone(pet.current_travel)  # travel cleared
    
    def test_new_location_added_to_atlas(self):
        pet = Pet(name="Test")
        pet.current_travel = {
            "stage": 1, "location": "北京", "stage_name": "中国之旅",
            "start_time": (datetime.now() - timedelta(minutes=20)).isoformat(),
            "end_time": (datetime.now() - timedelta(minutes=1)).isoformat()
        }
        check_travel_complete(pet)
        self.assertIn("北京", pet.travel_atlas.get("1", []))
    
    @patch("terminal_buddy.travel.random.random", return_value=0.05)
    def test_new_location_material_drop(self, mock_rand):
        """新地点10%概率掉材料，mock random=0.05 < 0.10 所以应该掉落"""
        pet = Pet(name="Test")
        pet.current_travel = {
            "stage": 1, "location": "北京", "stage_name": "中国之旅",
            "start_time": (datetime.now() - timedelta(minutes=20)).isoformat(),
            "end_time": (datetime.now() - timedelta(minutes=1)).isoformat()
        }
        msgs = check_travel_complete(pet)
        self.assertGreater(pet.breakthrough_materials.get("basic_stone", 0), 0)
    
    @patch("terminal_buddy.travel.random.random", return_value=0.50)
    def test_old_location_no_material(self, mock_rand):
        """老地点1%概率掉材料，mock random=0.50 不会掉落"""
        pet = Pet(name="Test")
        pet.travel_atlas = {"1": ["北京"]}  # 已去过
        pet.current_travel = {
            "stage": 1, "location": "北京", "stage_name": "中国之旅",
            "start_time": (datetime.now() - timedelta(minutes=20)).isoformat(),
            "end_time": (datetime.now() - timedelta(minutes=1)).isoformat()
        }
        msgs = check_travel_complete(pet)
        self.assertEqual(pet.breakthrough_materials.get("basic_stone", 0), 0)
    
    def test_atlas_complete_gives_material(self):
        """集齐图鉴必得突破材料"""
        pet = Pet(name="Test")
        # 差最后一个地点就集齐
        all_locs = list(TRAVEL_STAGES[1]["locations"])
        last_loc = all_locs[-1]
        pet.travel_atlas = {"1": all_locs[:-1]}
        pet.current_travel = {
            "stage": 1, "location": last_loc, "stage_name": "中国之旅",
            "start_time": (datetime.now() - timedelta(minutes=20)).isoformat(),
            "end_time": (datetime.now() - timedelta(minutes=1)).isoformat()
        }
        msgs = check_travel_complete(pet)
        self.assertGreater(pet.breakthrough_materials.get("basic_stone", 0), 0)

    def test_polar_travel_complete(self):
        """南北极旅行完成"""
        pet = Pet(name="Test")
        pet.current_travel = {
            "stage": 6, "location": "北极", "stage_name": "南北极探险",
            "start_time": (datetime.now() - timedelta(minutes=20)).isoformat(),
            "end_time": (datetime.now() - timedelta(minutes=1)).isoformat()
        }
        msgs = check_travel_complete(pet)
        self.assertGreater(len(msgs), 0)
        self.assertIn("北极", pet.travel_atlas.get("polar", []))


class TestTravelStatus(unittest.TestCase):
    def test_not_traveling(self):
        pet = Pet(name="Test")
        status = get_travel_status(pet)
        self.assertIsInstance(status, str)
    
    def test_traveling(self):
        pet = Pet(name="Test")
        pet.current_travel = {
            "location": "北京",
            "end_time": (datetime.now() + timedelta(minutes=5)).isoformat()
        }
        status = get_travel_status(pet)
        self.assertIn("北京", status)


class TestAtlasProgress(unittest.TestCase):
    def test_empty_atlas(self):
        pet = Pet(name="Test")
        progress = get_atlas_progress(pet)
        self.assertIsInstance(progress, str)
    
    def test_with_progress(self):
        pet = Pet(name="Test")
        pet.travel_atlas = {"1": ["北京", "上海"]}
        progress = get_atlas_progress(pet, "zh")
        self.assertIn("中国之旅", progress)
        self.assertIn("2/", progress)


if __name__ == "__main__":
    unittest.main()
