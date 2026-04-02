from __future__ import annotations
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pet import Pet


class PetStorage:
    """Manages pet data persistence."""
    
    DEFAULT_DIR = Path.home() / ".terminal-buddy"
    
    def __init__(self, storage_dir: Path | str | None = None):
        self.storage_dir = Path(storage_dir) if storage_dir else self.DEFAULT_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._pets_file = self.storage_dir / "pets.json"
    
    def save_pets(self, pets: list["Pet"]) -> None:
        data = [pet.to_dict() for pet in pets]
        with open(self._pets_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_pets(self) -> list["Pet"]:
        from .pet import Pet
        
        if not self._pets_file.exists():
            return []
        
        try:
            with open(self._pets_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                return []
            
            return [Pet.from_dict(pet_data) for pet_data in data]
        except (json.JSONDecodeError, IOError):
            return []
    
    def add_pet(self, pet: "Pet") -> None:
        pets = self.load_pets()
        pets.append(pet)
        self.save_pets(pets)
    
    def remove_pet(self, pet_id: str) -> bool:
        pets = self.load_pets()
        original_count = len(pets)
        pets = [pet for pet in pets if pet.id != pet_id]
        
        if len(pets) < original_count:
            self.save_pets(pets)
            return True
        return False
    
    def get_pet(self, pet_id: str) -> "Pet" | None:
        pets = self.load_pets()
        for pet in pets:
            if pet.id == pet_id:
                return pet
        return None
    
    def update_pet(self, pet: "Pet") -> None:
        pets = self.load_pets()
        for i, existing_pet in enumerate(pets):
            if existing_pet.id == pet.id:
                pets[i] = pet
                self.save_pets(pets)
                return
        
        pets.append(pet)
        self.save_pets(pets)
