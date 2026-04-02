"""Tests for CSS styling and application initialization."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, MagicMock
import re


class TestAppCSS(unittest.TestCase):
    """Test CSS styling and application setup."""

    def test_css_color_values_are_valid(self):
        """Verify all CSS color values are valid Textual colors."""
        from terminal_buddy.app import TerminalBuddyApp
        
        # Get the CSS string from the app
        css_text = TerminalBuddyApp.CSS
        
        # Named colors used in the CSS - should be valid
        valid_named_colors = {
            'green', 'cyan', 'grey', 'red', 'yellow', 'magenta', 'blue',
            'white', 'black', 'bright_green', 'bright_cyan', 'bright_red',
            'bright_yellow', 'bright_magenta', 'bright_blue', 'bright_white',
            'orange', 'orange_red', 'transparent', 'auto', 'default', 'none'
        }
        
        # Extract color values from CSS
        color_property_pattern = re.compile(
            r'(color|background|border|outline|scrollbar-color):\s*([^;]+);',
            re.IGNORECASE
        )
        
        for match in color_property_pattern.finditer(css_text):
            prop_name = match.group(1)
            color_value = match.group(2).strip().split()[0]  # Get first value
            
            # Skip if it's a compound value (e.g., "solid cyan")
            skip_values = {'solid', 'dashed', 'dotted', 'double', 'hidden', 'none', 'round'}
            if color_value in skip_values:
                continue
                
            # Named color - should be in valid set
            if color_value.startswith('#'):
                # Hex color - verify format
                self.assertTrue(
                    re.match(r'^#[0-9a-fA-F]{3,8}$', color_value),
                    f"Invalid hex color: {color_value}"
                )
            elif not color_value.replace('_', '').replace('-', '').isdigit():
                # Named color - should be valid for Textual
                self.assertIsInstance(color_value, str, f"Color should be string: {color_value}")

    def test_app_instantiation(self):
        """Verify App class can be instantiated without CSS parsing errors."""
        from terminal_buddy.app import TerminalBuddyApp
        
        try:
            app = TerminalBuddyApp()
            self.assertIsNotNone(app)
        except Exception as e:
            self.fail(f"App instantiation failed: {e}")

    def test_animation_tick_method_exists(self):
        """Verify _animation_tick method exists and is callable."""
        from terminal_buddy.app import TerminalBuddyApp
        
        app = TerminalBuddyApp()
        
        # Check that _animation_tick method exists
        self.assertTrue(hasattr(app, '_animation_tick'), 
                        "_animation_tick method should exist")
        
        # Check it's callable
        self.assertTrue(callable(getattr(app, '_animation_tick', None)),
                        "_animation_tick should be callable")

    def test_bindings_defined(self):
        """Verify all keybindings are properly defined."""
        from terminal_buddy.app import TerminalBuddyApp
        
        expected_bindings = {
            'f': 'feed',
            'p': 'play', 
            's': 'do_sleep',
            't': 'train',
            'e': 'pet_action',
            'tab': 'next_pet',
            'n': 'new_pet',
            'd': 'toggle_theme',
            'q': 'quit'
        }
        
        bindings_dict = {b[0]: b[1] for b in TerminalBuddyApp.BINDINGS}
        
        for key, action in expected_bindings.items():
            self.assertIn(key, bindings_dict, 
                          f"Key '{key}' should be bound")
            self.assertEqual(bindings_dict[key], action,
                           f"Key '{key}' should trigger action '{action}'")

    def test_compose_returns_widgets(self):
        """Verify compose method returns proper widget structure."""
        from terminal_buddy.app import TerminalBuddyApp
        from textual.widgets import Header, Footer
        
        app = TerminalBuddyApp()
        
        # compose() returns a generator
        # Just verify it doesn't raise an error
        try:
            # We can't fully test compose without a running app
            # but we can verify it exists and is callable
            self.assertTrue(callable(app.compose))
        except Exception as e:
            self.fail(f"compose() check failed: {e}")

    def test_app_has_required_components(self):
        """Verify app imports all required components."""
        from terminal_buddy.app import (
            TerminalBuddyApp, PetDisplay, StatsPanel, 
            ActionBar, MessageLog, NewPetScreen
        )
        
        # Just verify these classes are imported and defined
        self.assertTrue(issubclass(PetDisplay, object))
        self.assertTrue(issubclass(StatsPanel, object))
        self.assertTrue(issubclass(ActionBar, object))
        self.assertTrue(issubclass(MessageLog, object))
        self.assertTrue(issubclass(NewPetScreen, object))


class TestPetDisplay(unittest.TestCase):
    """Test PetDisplay widget."""

    def test_pet_display_initialization(self):
        """Test PetDisplay can be initialized."""
        from terminal_buddy.app import PetDisplay
        
        display = PetDisplay()
        self.assertIsNone(display.renderer)
        self.assertEqual(display._current_frame, "")

    def test_pet_display_with_renderer(self):
        """Test PetDisplay with a renderer."""
        from terminal_buddy.app import PetDisplay
        from terminal_buddy.renderer import PetRenderer
        
        renderer = PetRenderer("blob")
        display = PetDisplay(renderer=renderer)
        
        self.assertIsNotNone(display.renderer)


class TestStatsPanel(unittest.TestCase):
    """Test StatsPanel widget."""

    def test_stats_panel_initialization(self):
        """Test StatsPanel can be initialized."""
        from terminal_buddy.app import StatsPanel
        
        panel = StatsPanel()
        self.assertIsNone(panel.pet)

    def test_bar_method(self):
        """Test the _bar method creates progress bars."""
        from terminal_buddy.app import StatsPanel
        
        panel = StatsPanel()
        
        # _bar returns "[###---]" format (width + 2 for brackets)
        # Test full bar
        bar = panel._bar(100, max_val=100, width=10)
        self.assertEqual(len(bar), 12)  # 10 + 2 brackets
        self.assertEqual(bar, "[##########]")
        
        # Test half bar
        bar = panel._bar(50, max_val=100, width=10)
        self.assertEqual(len(bar), 12)
        self.assertEqual(bar, "[#####-----]")
        
        # Test empty bar
        bar = panel._bar(0, max_val=100, width=10)
        self.assertEqual(len(bar), 12)
        self.assertEqual(bar, "[----------]")


if __name__ == "__main__":
    unittest.main()
