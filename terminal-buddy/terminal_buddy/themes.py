"""Color themes for the TUI."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Theme:
    name: str
    primary: str
    secondary: str
    accent: str
    bg: str
    stat_high: str
    stat_mid: str
    stat_low: str
    stat_critical: str

THEMES: dict[str, Theme] = {
    "default": Theme(
        name="Default",
        primary="bright_cyan",
        secondary="bright_white",
        accent="bright_yellow",
        bg="",
        stat_high="bright_green",
        stat_mid="yellow",
        stat_low="bright_red",
        stat_critical="red",
    ),
    "forest": Theme(
        name="Forest",
        primary="green",
        secondary="bright_green",
        accent="yellow",
        bg="",
        stat_high="bright_green",
        stat_mid="yellow",
        stat_low="orange_red",
        stat_critical="red",
    ),
    "ocean": Theme(
        name="Ocean",
        primary="blue",
        secondary="cyan",
        accent="bright_cyan",
        bg="",
        stat_high="bright_blue",
        stat_mid="cyan",
        stat_low="bright_red",
        stat_critical="red",
    ),
    "sunset": Theme(
        name="Sunset",
        primary="bright_magenta",
        secondary="bright_red",
        accent="bright_yellow",
        bg="",
        stat_high="bright_green",
        stat_mid="yellow",
        stat_low="orange_red",
        stat_critical="red",
    ),
    "neon": Theme(
        name="Neon",
        primary="bright_magenta",
        secondary="bright_cyan",
        accent="bright_yellow",
        bg="",
        stat_high="bright_green",
        stat_mid="bright_yellow",
        stat_low="bright_red",
        stat_critical="red",
    ),
}