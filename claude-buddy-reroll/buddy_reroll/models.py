"""Data models for Claude /buddy pet reroll."""
from dataclasses import dataclass


@dataclass(frozen=True)
class BuddyStats:
    """Buddy stats with 5 attributes."""
    debugging: int
    patience: int
    chaos: int
    wisdom: int
    snark: int

    def min_stat(self) -> int:
        """Return the minimum stat value."""
        return min(self.debugging, self.patience, self.chaos, self.wisdom, self.snark)

    def max_stat(self) -> int:
        """Return the maximum stat value."""
        return max(self.debugging, self.patience, self.chaos, self.wisdom, self.snark)

    def total(self) -> int:
        """Return the sum of all stats."""
        return self.debugging + self.patience + self.chaos + self.wisdom + self.snark


@dataclass(frozen=True)
class Buddy:
    """A Claude /buddy pet."""
    species: str
    rarity: str
    eye: str
    hat: str
    shiny: bool
    stats: BuddyStats


@dataclass(frozen=True)
class BuddyMatch:
    """Search result: uid + corresponding buddy."""
    uid: str
    buddy: Buddy
