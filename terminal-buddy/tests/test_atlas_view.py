# -*- coding: utf-8 -*-
"""Tests for atlas_view.py - data logic and render content."""
import unittest
from unittest.mock import MagicMock, patch
from terminal_buddy.i18n import set_language
from terminal_buddy.pet import Pet
from terminal_buddy.atlas_view import StageProgressWidget, PolarWidget, MaterialWidget
from terminal_buddy.travel import TRAVEL_STAGES, POLAR_LOCATIONS


class TestStageProgressWidget(unittest.TestCase):
    def setUp(self):
        set_language("en")

    def tearDown(self):
        set_language("zh")

    def test_unlocked_empty_stage(self):
        """未访问任何地点的已解锁阶段"""
        stage_info = TRAVEL_STAGES[1]
        widget = StageProgressWidget(
            stage_num=1, stage_info=stage_info,
            visited=[], is_unlocked=True, lang="en"
        )
        content = widget._render_content()
        self.assertIn("Stage 1", content)
        self.assertIn("China Tour", content)
        self.assertIn("0/34", content)
        self.assertIn("UNLOCKED", content)

    def test_locked_stage(self):
        """未解锁阶段"""
        stage_info = TRAVEL_STAGES[3]
        widget = StageProgressWidget(
            stage_num=3, stage_info=stage_info,
            visited=[], is_unlocked=False, lang="en"
        )
        content = widget._render_content()
        self.assertIn("LOCKED", content)
        self.assertIn("Europe Tour", content)

    def test_partially_visited(self):
        """部分访问的阶段"""
        stage_info = TRAVEL_STAGES[1]
        visited = ["北京", "上海", "广东"]
        widget = StageProgressWidget(
            stage_num=1, stage_info=stage_info,
            visited=visited, is_unlocked=True, lang="zh"
        )
        content = widget._render_content()
        self.assertIn("3/34", content)
        self.assertIn("已解锁", content)
        self.assertIn("已访问", content)

    def test_completed_stage(self):
        """全部完成的阶段"""
        stage_info = TRAVEL_STAGES[2]
        all_locations = stage_info["locations"][:]
        widget = StageProgressWidget(
            stage_num=2, stage_info=stage_info,
            visited=all_locations, is_unlocked=True, lang="en"
        )
        content = widget._render_content()
        total = len(all_locations)
        self.assertIn(f"{total}/{total}", content)
        self.assertIn("COMPLETE", content)

    def test_chinese_display(self):
        """中文显示"""
        stage_info = TRAVEL_STAGES[1]
        widget = StageProgressWidget(
            stage_num=1, stage_info=stage_info,
            visited=["北京"], is_unlocked=True, lang="zh"
        )
        content = widget._render_content()
        self.assertIn("中国之旅", content)
        self.assertIn("已解锁", content)

    def test_many_visited_locations_truncated(self):
        """超过8个已访问地点应截断显示"""
        stage_info = TRAVEL_STAGES[1]
        visited = stage_info["locations"][:10]
        widget = StageProgressWidget(
            stage_num=1, stage_info=stage_info,
            visited=visited, is_unlocked=True, lang="en"
        )
        content = widget._render_content()
        self.assertIn("+2 more", content)


class TestPolarWidget(unittest.TestCase):
    def setUp(self):
        set_language("en")

    def tearDown(self):
        set_language("zh")

    def test_locked_polar(self):
        """未解锁的南北极"""
        widget = PolarWidget(
            polar_visited=[], is_unlocked=False,
            shiny_items=0, lang="en"
        )
        content = widget._render_content()
        self.assertIn("Polar Expedition", content)
        self.assertIn("LOCKED", content)
        self.assertIn("0/2", content)

    def test_unlocked_with_visits(self):
        """已解锁并有访问记录"""
        widget = PolarWidget(
            polar_visited=["北极"], is_unlocked=True,
            shiny_items=0, lang="zh"
        )
        content = widget._render_content()
        self.assertIn("南北极探险", content)
        self.assertIn("已解锁", content)
        self.assertIn("1/2", content)
        self.assertIn("北极", content)

    def test_shiny_items_display(self):
        """显示闪光水晶"""
        widget = PolarWidget(
            polar_visited=["北极", "南极"], is_unlocked=True,
            shiny_items=3, lang="en"
        )
        content = widget._render_content()
        self.assertIn("Shiny Evolution Crystals", content)
        self.assertIn("3", content)

    def test_chinese_polar(self):
        """中文南北极"""
        widget = PolarWidget(
            polar_visited=[], is_unlocked=False,
            shiny_items=0, lang="zh"
        )
        content = widget._render_content()
        self.assertIn("南北极探险", content)
        self.assertIn("未解锁", content)


class TestMaterialWidget(unittest.TestCase):
    def setUp(self):
        set_language("en")

    def tearDown(self):
        set_language("zh")

    def test_no_materials(self):
        """无材料"""
        widget = MaterialWidget(materials={}, lang="en")
        content = widget._render_content()
        self.assertIn("Breakthrough Materials", content)
        self.assertIn("No materials collected yet", content)

    def test_with_materials(self):
        """有材料"""
        materials = {"basic_stone": 2, "advanced_stone": 1}
        widget = MaterialWidget(materials=materials, lang="en")
        content = widget._render_content()
        self.assertIn("x2", content)
        self.assertIn("x1", content)
        # 有材料的指示器
        self.assertIn("●", content)

    def test_chinese_materials(self):
        """中文材料显示"""
        materials = {"basic_stone": 1}
        widget = MaterialWidget(materials=materials, lang="zh")
        content = widget._render_content()
        self.assertIn("突破材料", content)
        self.assertIn("初级突破石", content)
        self.assertIn("x1", content)

    def test_all_empty_materials(self):
        """所有材料为0"""
        widget = MaterialWidget(materials={}, lang="zh")
        content = widget._render_content()
        self.assertIn("暂无材料", content)


class TestAtlasDataCompatibility(unittest.TestCase):
    """测试与现有 travel_atlas 数据结构的兼容性"""

    def setUp(self):
        set_language("en")

    def tearDown(self):
        set_language("zh")

    def test_empty_atlas(self):
        """空图鉴的宠物"""
        pet = Pet(name="TestPet", species="blob")
        pet.travel_atlas = {}
        # 应该不会报错
        from terminal_buddy.travel import get_available_stage
        stage = get_available_stage(pet)
        self.assertEqual(stage, 1)

    def test_atlas_with_data(self):
        """有图鉴数据的宠物"""
        pet = Pet(name="TestPet", species="blob")
        pet.travel_atlas = {
            "1": ["北京", "上海"],
            "2": ["泰国"],
        }
        from terminal_buddy.travel import get_available_stage
        stage = get_available_stage(pet)
        self.assertEqual(stage, 1)  # 阶段1未完成

    def test_none_atlas(self):
        """travel_atlas 为 None"""
        pet = Pet(name="TestPet", species="blob")
        pet.travel_atlas = None
        # Widget 应该处理 None
        stage_info = TRAVEL_STAGES[1]
        atlas = pet.travel_atlas or {}
        visited = atlas.get("1", [])
        widget = StageProgressWidget(
            stage_num=1, stage_info=stage_info,
            visited=visited, is_unlocked=True, lang="en"
        )
        content = widget._render_content()
        self.assertIn("0/34", content)


if __name__ == "__main__":
    unittest.main()
