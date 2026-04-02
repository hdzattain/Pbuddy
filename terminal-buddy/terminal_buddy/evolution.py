from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pet import Pet


#Eulution paths
EVOLUTION_PATHS: dict[str, list[tuple[int, str]]] = {
    "blob": [(5, "ghost"), (15, "dragon")],
    "duck": [(5, "goose"), (15, "penguin")],
    "cat": [(5, "owl"), (15, "axolotl")],
    "cactus": [(5, "mushroom"), (15, "robot")],
    "snail": [(5, "turtle"), (15, "octopus")],
    "rabbit": [(5, "capybara"), (15, "chonk")],
}

STARTER_SPECIES = ("blob", "duck", "cat", "cactus", "snail", "rabbit")


class EvolutionSystem:
    """Manages pet evolution based on level."""
    
    @staticmethod
    def check_evolution(pet: "Pet") -> str | None:
        if not pet.is_alive:
            return None
        
        if pet.species in EVOLUTION_PATHS:
            for threshold, evolved_species in EVOLUTION_PATHS[pet.species]:
                if pet.level >= threshold:
                    return evolved_species
        
        for starter, evolutions in EVOLUTION_PATHS.items():
            for i, (threshold, evolved_species) in enumerate(evolutions):
                if pet.species == evolved_species and i + 1 < len(evolutions):
                    next_threshold, next_species = evolutions[i + 1]
                    if pet.level >= next_threshold:
                        return next_species
        
        return None
    
    @staticmethod
    def evolve(pet: "Pet") -> str | None:
        new_species = EvolutionSystem.check_evolution(pet)
        
        if new_species is None:
            return None
        
        old_species = pet.species
        pet.species = new_species
        
        return f"{pet.name} evolved from {old_species} to {new_species}!"
    
    @staticmethod
    def get_evolution_chain(species: str) -> list[str]:
        if species not in EVOLUTION_PATHS:
            return [species]
        
        chain = [species]
        for threshold, evolved_species in EVOLUTION_PATHS[species]:
            chain.append(evolved_species)
        
        return chain
