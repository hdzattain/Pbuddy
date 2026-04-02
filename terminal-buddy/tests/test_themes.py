"""Tests for color themes."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from terminal_buddy.themes import Theme, THEMES


class TestThemeDataclass(unittest.TestCase):
    """Test Theme dataclass."""

    def test_theme_creation(self):
        """Test creating a theme."""
        theme = Theme(
            name="Test",
            primary="blue",
            secondary="white",
            accent="yellow",
            bg="",
            stat_high="green",
            stat_mid="yellow",
            stat_low="red",
            stat_critical="dark_red"
        )
        
        self.assertEqual(theme.name, "Test")
        self.assertEqual(theme.primary, "blue")

    def test_theme_is_frozen(self):
        """Test Theme is immutable (frozen)."""
        theme = Theme(
            name="Test",
            primary="blue",
            secondary="white",
            accent="yellow",
            bg="",
            stat_high="green",
            stat_mid="yellow",
            stat_low="red",
            stat_critical="dark_red"
        )
        
        with self.assertRaises(AttributeError):
            theme.primary = "red"


class TestThemesDictionary(unittest.TestCase):
    """Test THEMES dictionary."""

    def test_five_themes_exist(self):
        """Test exactly 5 themes are defined."""
        self.assertEqual(len(THEMES), 5)

    def test_default_theme_exists(self):
        """Test default theme exists."""
        self.assertIn("default", THEMES)

    def test_forest_theme_exists(self):
        """Test Forest theme exists."""
        self.assertIn("forest", THEMES)

    def test_ocean_theme_exists(self):
        """Test Ocean theme exists."""
        self.assertIn("ocean", THEMES)

    def test_sunset_theme_exists(self):
        """Test Sunset theme exists."""
        self.assertIn("sunset", THEMES)

    def test_neon_theme_exists(self):
        """Test Neon theme exists."""
        self.assertIn("neon", THEMES)

    def test_all_themes_are_theme_objects(self):
        """Test all themes are Theme instances."""
        for key, theme in THEMES.items():
            self.assertIsInstance(theme, Theme,
                                f"Theme '{key}' should be Theme instance")

    def test_theme_keys_lowercase(self):
        """Test theme keys are lowercase."""
        for key in THEMES.keys():
            self.assertEqual(key, key.lower(),
                           f"Theme key '{key}' should be lowercase")


class TestThemeStructure(unittest.TestCase):
    """Test theme data structure completeness."""

    def test_all_themes_have_name(self):
        """Test all themes have a name."""
        for key, theme in THEMES.items():
            self.assertTrue(hasattr(theme, 'name'),
                          f"Theme '{key}' should have 'name'")
            self.assertIsInstance(theme.name, str,
                                f"Theme '{key}' name should be string")

    def test_all_themes_have_primary(self):
        """Test all themes have primary color."""
        for key, theme in THEMES.items():
            self.assertTrue(hasattr(theme, 'primary'),
                          f"Theme '{key}' should have 'primary'")

    def test_all_themes_have_secondary(self):
        """Test all themes have secondary color."""
        for key, theme in THEMES.items():
            self.assertTrue(hasattr(theme, 'secondary'),
                          f"Theme '{key}' should have 'secondary'")

    def test_all_themes_have_accent(self):
        """Test all themes have accent color."""
        for key, theme in THEMES.items():
            self.assertTrue(hasattr(theme, 'accent'),
                          f"Theme '{key}' should have 'accent'")

    def test_all_themes_have_background(self):
        """Test all themes have background color."""
        for key, theme in THEMES.items():
            self.assertTrue(hasattr(theme, 'bg'),
                          f"Theme '{key}' should have 'bg'")

    def test_all_themes_have_stat_colors(self):
        """Test all themes have stat colors."""
        stat_attrs = ['stat_high', 'stat_mid', 'stat_low', 'stat_critical']
        
        for key, theme in THEMES.items():
            for attr in stat_attrs:
                self.assertTrue(hasattr(theme, attr),
                              f"Theme '{key}' should have '{attr}'")


class TestThemeValues(unittest.TestCase):
    """Test theme color values are valid."""

    def test_primary_colors_not_empty(self):
        """Test primary colors are not empty."""
        for key, theme in THEMES.items():
            self.assertTrue(len(theme.primary) > 0,
                          f"Theme '{key}' primary should not be empty")

    def test_secondary_colors_not_empty(self):
        """Test secondary colors are not empty."""
        for key, theme in THEMES.items():
            self.assertTrue(len(theme.secondary) > 0,
                          f"Theme '{key}' secondary should not be empty")

    def test_accent_colors_not_empty(self):
        """Test accent colors are not empty."""
        for key, theme in THEMES.items():
            self.assertTrue(len(theme.accent) > 0,
                          f"Theme '{key}' accent should not be empty")

    def test_stat_high_color_not_empty(self):
        """Test stat_high colors are not empty."""
        for key, theme in THEMES.items():
            self.assertTrue(len(theme.stat_high) > 0,
                          f"Theme '{key}' stat_high should not be empty")

    def test_stat_mid_color_not_empty(self):
        """Test stat_mid colors are not empty."""
        for key, theme in THEMES.items():
            self.assertTrue(len(theme.stat_mid) > 0,
                          f"Theme '{key}' stat_mid should not be empty")

    def test_stat_low_color_not_empty(self):
        """Test stat_low colors are not empty."""
        for key, theme in THEMES.items():
            self.assertTrue(len(theme.stat_low) > 0,
                          f"Theme '{key}' stat_low should not be empty")

    def test_stat_critical_color_not_empty(self):
        """Test stat_critical colors are not empty."""
        for key, theme in THEMES.items():
            self.assertTrue(len(theme.stat_critical) > 0,
                          f"Theme '{key}' stat_critical should not be empty")


class TestSpecificThemeValues(unittest.TestCase):
    """Test specific theme values."""

    def test_default_theme_values(self):
        """Test Default theme has correct values."""
        theme = THEMES["default"]
        self.assertEqual(theme.name, "Default")
        self.assertEqual(theme.primary, "bright_cyan")

    def test_forest_theme_values(self):
        """Test Forest theme has correct values."""
        theme = THEMES["forest"]
        self.assertEqual(theme.name, "Forest")
        self.assertEqual(theme.primary, "green")

    def test_ocean_theme_values(self):
        """Test Ocean theme has correct values."""
        theme = THEMES["ocean"]
        self.assertEqual(theme.name, "Ocean")
        self.assertEqual(theme.primary, "blue")

    def test_sunset_theme_values(self):
        """Test Sunset theme has correct values."""
        theme = THEMES["sunset"]
        self.assertEqual(theme.name, "Sunset")
        self.assertEqual(theme.primary, "bright_magenta")

    def test_neon_theme_values(self):
        """Test Neon theme has correct values."""
        theme = THEMES["neon"]
        self.assertEqual(theme.name, "Neon")
        self.assertEqual(theme.primary, "bright_magenta")


class TestThemeNames(unittest.TestCase):
    """Test theme names match their keys."""

    def test_theme_names_capitalized(self):
        """Test theme names are properly capitalized."""
        expected_names = {
            "default": "Default",
            "forest": "Forest",
            "ocean": "Ocean",
            "sunset": "Sunset",
            "neon": "Neon"
        }
        
        for key, expected_name in expected_names.items():
            self.assertEqual(THEMES[key].name, expected_name)


if __name__ == "__main__":
    unittest.main()
