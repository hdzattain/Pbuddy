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
    rarity: int = 1
    is_shiny: bool = False
    rarity_color: str = "white"
    phase: int = 1
    breakthrough_materials: dict = field(default_factory=dict)
    travel_atlas: dict = field(default_factory=dict)
    current_travel: dict | None = None
    shiny_evolution_items: int = 0
    tired: int = 0  # 疲劳度 0-100，0为完全不疲劳

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
        if self.tired >= 80:
            return "exhausted"
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
        self.tired += 10
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
        self.tired = max(0, self.tired - 20)
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
        if self.tired >= 80:
            return get_text("too_tired_to_train", name=self.name)
        self.energy = max(0, self.energy - 15)
        self.mood = max(0, self.mood - 5)
        self.tired += 15
        self.last_interaction = datetime.now().isoformat()
        self.clamp_stats()
        xp_msg = self.gain_xp(amount)
        msg = get_text("trained_hard", name=self.name)
        return msg if xp_msg is None else f"{msg} {xp_msg}"

    def pet_action(self, amount: int = 10) -> str:
        if not self.is_alive:
            return get_text("no_longer_with_us", name=self.name)
        self.mood = min(100, self.mood + amount)
        self.tired += 3
        self.last_interaction = datetime.now().isoformat()
        self.clamp_stats()
        xp_msg = self.gain_xp(2)
        msg = get_text("enjoyed_cuddles", name=self.name, amount=amount)
        return msg if xp_msg is None else f"{self.name} {xp_msg}"

    def gain_xp(self, amount: int) -> str | None:
        if not self.is_alive:
            return None
        # 检查是否已达阶段等级上限
        from .breakthrough import get_level_cap
        level_cap = get_level_cap(self.phase)
        if self.level >= level_cap:
            self.xp = 0
            return get_text("level_capped", name=self.name, level=level_cap)
        self.xp += amount
        if self.xp >= self.xp_for_next_level:
            self.xp -= self.xp_for_next_level
            self.level += 1
            # 升级后再次检查上限
            if self.level >= level_cap:
                self.xp = 0
            return get_text("level_up", name=self.name, level=self.level)
        return None

    def clamp_stats(self) -> None:
        self.hunger = max(0, min(100, self.hunger))
        self.mood = max(0, min(100, self.mood))
        self.energy = max(0, min(100, self.energy))
        self.tired = max(0, min(100, self.tired))

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
            "rarity": self.rarity,
            "is_shiny": self.is_shiny,
            "rarity_color": self.rarity_color,
            "phase": self.phase,
            "breakthrough_materials": self.breakthrough_materials,
            "travel_atlas": self.travel_atlas,
            "current_travel": self.current_travel,
            "shiny_evolution_items": self.shiny_evolution_items,
            "tired": self.tired,
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
            rarity=data.get("rarity", 1),
            is_shiny=data.get("is_shiny", False),
            rarity_color=data.get("rarity_color", "white"),
            phase=data.get("phase", 1),
            breakthrough_materials=data.get("breakthrough_materials", {}),
            travel_atlas=data.get("travel_atlas", {}),
            current_travel=data.get("current_travel", None),
            shiny_evolution_items=data.get("shiny_evolution_items", 0),
            tired=data.get("tired", 0),
        )
