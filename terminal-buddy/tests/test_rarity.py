# -*- coding: utf-8 -*-
"""Tests for rarity and shiny calculation system."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from terminal_buddy.rarity import (
    calculate_rarity, calculate_shiny, get_rarity_info, get_rarity_display,
    get_mac_address, RARITY_LEVELS, SHINY_PROB, HASH_SALT
)


class TestRarityCalculation(unittest.TestCase):
    def test_calculate_rarity_returns_valid_level(self):
        """稀有度结果应在1-5之间"""
        result = calculate_rarity("aa:bb:cc:dd:ee:ff", "2024-01-01T00:00:00")
        self.assertIn(result, [1, 2, 3, 4, 5])
    
    def test_calculate_rarity_deterministic(self):
        """相同输入应产生相同结果"""
        r1 = calculate_rarity("aa:bb:cc:dd:ee:ff", "2024-01-01T00:00:00")
        r2 = calculate_rarity("aa:bb:cc:dd:ee:ff", "2024-01-01T00:00:00")
        self.assertEqual(r1, r2)
    
    def test_calculate_rarity_different_inputs_may_differ(self):
        """不同输入可能产生不同结果"""
        results = set()
        for i in range(100):
            r = calculate_rarity("aa:bb:cc:dd:ee:ff", f"2024-01-01T00:00:{i:02d}")
            results.add(r)
        self.assertGreater(len(results), 1)
    
    def test_calculate_rarity_defaults(self):
        """不传参数应使用默认MAC和时间"""
        result = calculate_rarity()
        self.assertIn(result, [1, 2, 3, 4, 5])
    
    def test_probability_distribution(self):
        """大量采样验证概率分布大致正确(统计测试，容许误差)"""
        counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        n = 10000
        for i in range(n):
            r = calculate_rarity(f"mac:{i}", f"time:{i}")
            counts[r] += 1
        # 1星应该最多(~60%)
        self.assertGreater(counts[1], n * 0.4)
        # 5星应该最少
        self.assertLess(counts[5], n * 0.05)


class TestShinyCalculation(unittest.TestCase):
    def test_calculate_shiny_returns_bool(self):
        result = calculate_shiny("aa:bb:cc:dd:ee:ff", "2024-01-01T00:00:00")
        self.assertIsInstance(result, bool)
    
    def test_calculate_shiny_deterministic(self):
        r1 = calculate_shiny("aa:bb:cc:dd:ee:ff", "2024-01-01T00:00:00")
        r2 = calculate_shiny("aa:bb:cc:dd:ee:ff", "2024-01-01T00:00:00")
        self.assertEqual(r1, r2)
    
    def test_shiny_is_rare(self):
        """大量采样中闪光应该很少(约1%)"""
        shiny_count = sum(
            1 for i in range(5000)
            if calculate_shiny(f"mac:{i}", f"time:{i}")
        )
        # 允许较大误差
        self.assertLess(shiny_count, 5000 * 0.05)


class TestRarityInfo(unittest.TestCase):
    def test_get_rarity_info_valid(self):
        for level in range(1, 6):
            info = get_rarity_info(level)
            self.assertIn("name", info)
            self.assertIn("color", info)
            self.assertIn("prob", info)
    
    def test_get_rarity_info_invalid_returns_default(self):
        info = get_rarity_info(99)
        self.assertEqual(info, RARITY_LEVELS[1])


class TestRarityDisplay(unittest.TestCase):
    def test_display_chinese(self):
        result = get_rarity_display(1, False, "zh")
        self.assertIn("★", result)
        self.assertIn("普通", result)
    
    def test_display_english(self):
        result = get_rarity_display(1, False, "en")
        self.assertIn("★", result)
        self.assertIn("Common", result)
    
    def test_display_shiny(self):
        result = get_rarity_display(3, True, "zh")
        self.assertIn("✦", result)
        self.assertIn("闪光", result)
    
    def test_display_shiny_english(self):
        result = get_rarity_display(3, True, "en")
        self.assertIn("Shiny", result)


class TestMacAddress(unittest.TestCase):
    def test_get_mac_address_format(self):
        mac = get_mac_address()
        self.assertIsInstance(mac, str)
        parts = mac.split(":")
        self.assertEqual(len(parts), 6)


if __name__ == "__main__":
    unittest.main()
