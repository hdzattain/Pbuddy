# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

from .ticker import Ticker
from .evolution import EvolutionSystem
from .i18n import get_text
from .rarity import calculate_rarity, calculate_shiny, get_rarity_info, get_rarity_display
from .breakthrough import can_breakthrough, perform_breakthrough
from .travel import start_travel, check_travel_complete

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
        elif action == "breakthrough":
            if can_breakthrough(pet):
                action_msg = perform_breakthrough(pet)
            else:
                action_msg = get_text("cannot_breakthrough", name=pet.name)
        elif action == "travel":
            # 先检查是否有旅行完成
            travel_msgs = check_travel_complete(pet)
            if travel_msgs:
                messages.extend(travel_msgs)
                action_msg = None
            else:
                action_msg = start_travel(pet)
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
        
        # 计算稀有度和闪光
        rarity = calculate_rarity()
        is_shiny = calculate_shiny()
        rarity_info = get_rarity_info(rarity)
        pet.rarity = rarity
        pet.is_shiny = is_shiny
        pet.rarity_color = rarity_info["color"]
        
        self.storage.add_pet(pet)
        
        # 物种名称翻译
        species_display = get_text(f"species_{pet.species}")
        if species_display == f"species_{pet.species}":
            species_display = pet.species
        messages.append(get_text("welcome_pet", name=pet.name, species=species_display))
        
        # 显示稀有度信息
        rarity_display = get_rarity_display(rarity, is_shiny)
        messages.append(get_text("rarity_result", rarity=rarity_display))
        if is_shiny:
            messages.append(get_text("shiny_congratulations"))
        
        messages.append(get_text("take_good_care"))
        
        return pet, messages
    
    def get_all_pets(self) -> list["Pet"]:
        pets = self.storage.load_pets()
        
        for pet in pets:
            Ticker.tick(pet)
            self.storage.update_pet(pet)
        
        return pets
