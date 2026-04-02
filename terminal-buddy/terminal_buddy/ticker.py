from datetime import datetime
from typing import TYPE_CHECKING

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
            return [f"{pet.name} is no longer with us..."]
        
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
            messages.append(f"{pet.name} has starved... You should have fed them!")
            return messages
        
        if hours >= 24:
            messages.append(f"{pet.name} missed you! ({int(hours)} hours passed)")
        elif hours >= 1:
            messages.append(f"{int(hours)} hours have passed since you last checked on {pet.name}.")
        
        if hunger_loss > 20:
            messages.append(f"{pet.name} is getting hungry...")
        if mood_loss > 15:
            messages.append(f"{pet.name} seems lonely...")
        if energy_gain > 20:
            messages.append(f"{pet.name} is well rested!")
        
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
