# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

from .ticker import Ticker
from .evolution import EvolutionSystem
from .i18n import get_text

if TYPE_CHECKING:
    from .pet import Pet
    from .storage import PetStorage


class PetActions:
    """High-level pet interaction commands."""
    
    def __init__(self, storage: "PetStorage"):
        self.storage = storage
    
    def interact(self, pet: "Pet", action: str) -> list[str]:
        messages = []
        
        tick_messages = Ticker.tick(pet)
        messages.extend(tick_messages)
        
        if not pet.is_alive:
            self.storage.update_pet(pet)
            return messages
        
        action = action.lower()
        action_msg = None
        
        if action == "feed":
            action_msg = pet.feed()
        elif action == "play":
            action_msg = pet.play()
        elif action == "sleep":
            action_msg = pet.sleep()
        elif action == "train":
            action_msg = pet.train()
        elif action == "pet":
            action_msg = pet.pet_action()
        else:
            messages.append(get_text("unknown_action", action=action))
            return messages
        
        if action_msg:
            messages.append(action_msg)
        
        evolution_msg = EvolutionSystem.evolve(pet)
        if evolution_msg:
            messages.append(evolution_msg)
        
        self.storage.update_pet(pet)
        
        return messages
    
    def create_pet(self, name: str, species: str) -> tuple["Pet", list[str]]:
        from .pet import Pet
        from .evolution import STARTER_SPECIES
        
        messages = []
        
        if species not in STARTER_SPECIES:
            species = "blob"
            messages.append(get_text("unknown_species"))
        
        pet = Pet(name=name, species=species)
        self.storage.add_pet(pet)
        
        messages.append(get_text("welcome_pet", name=pet.name, species=pet.species))
        messages.append(get_text("take_good_care"))
        
        return pet, messages
    
    def get_all_pets(self) -> list["Pet"]:
        pets = self.storage.load_pets()
        
        for pet in pets:
            Ticker.tick(pet)
            self.storage.update_pet(pet)
        
        return pets
