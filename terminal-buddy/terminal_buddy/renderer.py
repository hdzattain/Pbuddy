"""ASCII art animation renderer."""
from terminal_buddy.sprites import SPRITES
from terminal_buddy.themes import Theme, THEMES

class PetRenderer:
    """Renders pet ASCII art with animation state."""

    def __init__(self, species: str, theme: Theme | None = None):
        self.species = species
        self.theme = theme or THEMES["default"]
        self._frame_index = 0

    def get_frame(self, state: str = "idle") -> str:
        """Get the current animation frame for given state."""
        species_sprites = SPRITES.get(self.species, SPRITES["blob"])
        frames = species_sprites.get(state, species_sprites["idle"])
        if not frames:
            return "   ???   "
        return frames[self._frame_index % len(frames)]

    def next_frame(self, state: str = "idle") -> str:
        """Advance to next frame and return it (for idle animation)."""
        species_sprites = SPRITES.get(self.species, SPRITES["blob"])
        frames = species_sprites.get(state, species_sprites["idle"])
        if len(frames) > 1:
            self._frame_index = (self._frame_index + 1) % len(frames)
        return self.get_frame(state)

    def get_state_for_pet(self, pet) -> str:
        """Determine animation state based on pet stats."""
        if not pet.is_alive:
            return "sad"
        if pet.energy < 10:
            return "sleep"
        if pet.happiness < 20:
            return "sad"
        if pet.mood > 80:
            return "happy"
        if pet.hunger > 80:
            return "eat"
        return "idle"

    def reset_animation(self):
        self._frame_index = 0