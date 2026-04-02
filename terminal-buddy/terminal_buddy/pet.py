# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from .i18n import get_text


@dataclass
class Pet:
    """A virtual pet with needs and growth."""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = "Buddy"
    species: str = "blob"
    hunger: int = 80
    mood: int = 80
    energy: int = 80
    xp: int = 0
    level: int = 1
    born_at: str = ""
    last_fed: str = ""
    last_interaction: str = ""
    is_alive: bool = True

    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.born_at:
            self.born_at = now
        if not self.last_fed:
            self.last_fed = now
        if not self.last_interaction:
            self.last_interaction = now

    @property
    def happiness(self) -> int:
        return (self.hunger + self.mood + self.energy) // 3

    @property
    def status_emoji(self) -> str:
        h = self.happiness
        if h >= 80: return "happy"
        if h >= 60: return "content"
        if h >= 40: return "neutral"
        if h >= 20: return "sad"
        return "critical"

    @property
    def xp_for_next_level(self) -> int:
        return self.level * 100

    def feed(self, amount: int = 20) -> str:
        if not self.is_alive:
            return get_text("no_longer_with_us", name=self.name)
        self.hunger = min(100, self.hunger + amount)
        self.last_fed = datetime.now().isoformat()
        self.last_interaction = datetime.now().isoformat()
        self.clamp_stats()
        xp_msg = self.gain_xp(5)
        msg = get_text("ate_snack", name=self.name, amount=amount)
        return msg if xp_msg is None else f"{self.name} {xp_msg}"

    def play(self, amount: int = 15) -> str:
        if not self.is_alive:
            return get_text("no_longer_with_us", name=self.name)
        self.mood = min(100, self.mood + amount)
        self.energy = max(0, self.energy - 10)
        self.last_interaction = datetime.now().isoformat()
        self.clamp_stats()
        xp_msg = self.gain_xp(10)
        msg = get_text("had_fun_playing", name=self.name, amount=amount)
        return msg if xp_msg is None else f"{self.name} {xp_msg}"

    def sleep(self, amount: int = 30) -> str:
        if not self.is_alive:
            return get_text("no_longer_with_us", name=self.name)
        self.energy = min(100, self.energy + amount)
        self.hunger = max(0, self.hunger - 5)
        self.last_interaction = datetime.now().isoformat()
        self.clamp_stats()
        xp_msg = self.gain_xp(3)
        msg = get_text("took_nap", name=self.name, amount=amount)
        return msg if xp_msg is None else f"{msg} {xp_msg}"

    def train(self, amount: int = 25) -> str:
        if not self.is_alive:
            return get_text("no_longer_with_us", name=self.name)
        if self.energy < 15:
            return get_text("too_tired_to_train", name=self.name)
        self.energy = max(0, self.energy - 15)
        self.mood = max(0, self.mood - 5)
        self.last_interaction = datetime.now().isoformat()
        self.clamp_stats()
        xp_msg = self.gain_xp(amount)
        msg = get_text("trained_hard", name=self.name)
        return msg if xp_msg is None else f"{msg} {xp_msg}"

    def pet_action(self, amount: int = 10) -> str:
        if not self.is_alive:
            return get_text("no_longer_with_us", name=self.name)
        self.mood = min(100, self.mood + amount)
        self.last_interaction = datetime.now().isoformat()
        self.clamp_stats()
        xp_msg = self.gain_xp(2)
        msg = get_text("enjoyed_cuddles", name=self.name, amount=amount)
        return msg if xp_msg is None else f"{self.name} {xp_msg}"

    def gain_xp(self, amount: int) -> str | None:
        if not self.is_alive:
            return None
        self.xp += amount
        if self.xp >= self.xp_for_next_level:
            self.xp -= self.xp_for_next_level
            self.level += 1
            return get_text("level_up", name=self.name, level=self.level)
        return None

    def clamp_stats(self) -> None:
        self.hunger = max(0, min(100, self.hunger))
        self.mood = max(0, min(100, self.mood))
        self.energy = max(0, min(100, self.energy))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "hunger": self.hunger,
            "mood": self.mood,
            "energy": self.energy,
            "xp": self.xp,
            "level": self.level,
            "born_at": self.born_at,
            "last_fed": self.last_fed,
            "last_interaction": self.last_interaction,
            "is_alive": self.is_alive,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Pet':
        return cls(
            id=data.get("id", uuid.uuid4().hex[:8]),
            name=data.get("name", "Buddy"),
            species=data.get("species", "blob"),
            hunger=data.get("hunger", 80),
            mood=data.get("mood", 80),
            energy=data.get("energy", 80),
            xp=data.get("xp", 0),
            level=data.get("level", 1),
            born_at=data.get("born_at", ""),
            last_fed=data.get("last_fed", ""),
            last_interaction=data.get("last_interaction", ""),
            is_alive=data.get("is_alive", True),
        )
