# -*- coding: utf-8 -*-
from datetime import datetime
from typing import TYPE_CHECKING

from .i18n import get_text

if TYPE_CHECKING:
    from .pet import Pet


class Ticker:
    """Simulates time passing for pets, even when offline."""
    
    HUNGER_DECAY_PER_HOUR: float = 3.0
    MOOD_DECAY_PER_HOUR: float = 2.0
    ENERGY_RECOVERY_PER_HOUR: float = 5.0
    
    @staticmethod
    def tick(pet: "Pet") -> list[str]:
        messages = []
        
        if not pet.is_alive:
            return [get_text("no_longer_with_us", name=pet.name)]
        
        hours = Ticker.hours_since(pet.last_interaction)
        
        if hours <= 0:
            return messages
        
        hunger_loss = int(hours * Ticker.HUNGER_DECAY_PER_HOUR)
        mood_loss = int(hours * Ticker.MOOD_DECAY_PER_HOUR)
        energy_gain = int(hours * Ticker.ENERGY_RECOVERY_PER_HOUR)
        
        pet.hunger = max(0, pet.hunger - hunger_loss)
        pet.mood = max(0, pet.mood - mood_loss)
        pet.energy = min(100, pet.energy + energy_gain)
        
        if pet.hunger <= 0:
            pet.is_alive = False
            messages.append(get_text("starved", name=pet.name))
            return messages
        
        if hours >= 24:
            messages.append(get_text("missed_you", name=pet.name, hours=int(hours)))
        elif hours >= 1:
            messages.append(get_text("hours_passed", hours=int(hours), name=pet.name))
        
        if hunger_loss > 20:
            messages.append(get_text("getting_hungry", name=pet.name))
        if mood_loss > 15:
            messages.append(get_text("seems_lonely", name=pet.name))
        if energy_gain > 20:
            messages.append(get_text("well_rested", name=pet.name))
        
        pet.last_interaction = datetime.now().isoformat()
        
        return messages
    
    @staticmethod
    def hours_since(iso_time: str) -> float:
        try:
            last_time = datetime.fromisoformat(iso_time)
            now = datetime.now()
            delta = now - last_time
            return delta.total_seconds() / 3600.0
        except (ValueError, TypeError):
            return 0.0
