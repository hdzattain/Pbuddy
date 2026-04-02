"""Terminal Buddy Textual TUI Application."""
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container, Grid
from textual.widgets import Header, Footer, Static, Button, Label, Input, RichLog
from textual.screen import Screen
from textual import on

from terminal_buddy.pet import Pet
from terminal_buddy.actions import PetActions
from terminal_buddy.storage import PetStorage
from terminal_buddy.renderer import PetRenderer
from terminal_buddy.evolution import STARTER_SPECIES
from terminal_buddy.themes import THEMES

class PetDisplay(Static):
    """Widget that shows the pet ASCII art with animation."""

    def __init__(self, renderer: PetRenderer | None = None, **kwargs):
        super().__init__(**kwargs)
        self.renderer = renderer
        self._current_frame = ""

    def set_renderer(self, renderer: PetRenderer):
        self.renderer = renderer
        self.update_display()

    def update_display(self, state: str = "idle"):
        if self.renderer:
            self._current_frame = self.renderer.get_frame(state)
            self.update(self._current_frame)

    def next_frame(self, state: str = "idle"):
        if self.renderer:
            self._current_frame = self.renderer.next_frame(state)
            self.update(self._current_frame)

class StatsPanel(Static):
    """Widget showing pet stats with colored bars."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pet = None

    def set_pet(self, pet):
        self.pet = pet
        self.update_stats()

    def _bar(self, value, max_val=100, width=20):
        filled = int(value / max_val * width)
        empty = width - filled
        return "[" + "#" * filled + "-" * empty + "]"

    def update_stats(self):
        if not self.pet:
            self.update("No pet selected")
            return

        lines = []
        lines.append(f"Name: {self.pet.name}")
        lines.append(f"Species: {self.pet.species}  Lv.{self.pet.level}")
        xp_needed = self.pet.xp_for_next_level
        lines.append(f"XP: {self.pet.xp}/{xp_needed}")
        lines.append("")
        lines.append(f"Hunger: {self._bar(self.pet.hunger)} {self.pet.hunger}%")
        lines.append(f"Mood:   {self._bar(self.pet.mood)} {self.pet.mood}%")
        lines.append(f"Energy: {self._bar(self.pet.energy)} {self.pet.energy}%")
        lines.append(f"Status: {self.pet.status_emoji}")

        self.update(chr(10).join(lines))

class ActionBar(Horizontal):
    """Row of action buttons."""

    def compose(self):
        yield Button("Feed [F]", id="btn-feed", variant="primary")
        yield Button("Play [P]", id="btn-play")
        yield Button("Sleep [S]", id="btn-sleep")
        yield Button("Train [T]", id="btn-train")
        yield Button("Pet [E]", id="btn-pet")


class MessageLog(RichLog):
    """Scrollable message log."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_scroll = True

    def add_message(self, message: str):
        self.write(message)

class NewPetScreen(Screen):
    """Screen for creating a new pet."""

    def compose(self):
        yield Grid(
            Label("Create New Pet", classes="title"),
            Label("Name:"),
            Input(placeholder="Enter pet name", id="input-name"),
            Label("Species:"),
            Input(placeholder="blob, duck, cat, cactus, snail, rabbit", id="input-species"),
            Button("Create", id="btn-create", variant="primary"),
            Button("Cancel", id="btn-cancel"),
            id="new-pet-grid"
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-create":
            name_input = self.query_one("#input-name", Input)
            species_input = self.query_one("#input-species", Input)
            name = name_input.value.strip() or "Buddy"
            species = species_input.value.strip() or "blob"
            self.dismiss((name, species))
        elif event.button.id == "btn-cancel":
            self.dismiss(None)

class TerminalBuddyApp(App):
    """Main application."""

    TITLE = "Terminal Buddy"
    CSS = """
Screen {
    align: center middle;
}

#new-pet-grid {
    width: 60;
    height: auto;
    border: solid green;
    padding: 1;
}

#new-pet-grid .title {
    text-align: center;
    text-style: bold;
}

#pet-display {
    width: 24;
    height: 12;
    border: solid green;
    content-align: center middle;
}

#stats-panel {
    width: 1fr;
    height: 12;
    border: solid cyan;
    padding: 1;
}

#action-bar {
    height: 3;
    dock: bottom;
    align: center middle;
}

#message-log {
    height: 8;
    border: solid grey;
}
"""

    BINDINGS = [
        ("f", "feed", "Feed"),
        ("p", "play", "Play"),
        ("s", "do_sleep", "Sleep"),
        ("t", "train", "Train"),
        ("e", "pet_action", "Pet"),
        ("tab", "next_pet", "Next Pet"),
        ("n", "new_pet", "New Pet"),
        ("d", "toggle_theme", "Theme"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.storage = PetStorage()
        self.pet_actions = PetActions(self.storage)
        self.pets = []
        self.current_pet_index = 0
        self.current_theme_index = 0
        self.renderer = None
    def compose(self):
        yield Header()
        with Horizontal():
            yield PetDisplay(id="pet-display")
            yield StatsPanel(id="stats-panel")
        yield ActionBar(id="action-bar")
        yield MessageLog(id="message-log")
        yield Footer()

    def on_mount(self):
        self.pets = self.pet_actions.get_all_pets()
        if not self.pets:
            self.push_screen(NewPetScreen(), self._on_new_pet_result)
        else:
            self._update_display()
        self.set_interval(0.8, self._animation_tick)

    def _on_new_pet_result(self, result):
        if result:
            name, species = result
            pet, messages = self.pet_actions.create_pet(name, species)
            self.pets = self.pet_actions.get_all_pets()
            self.current_pet_index = len(self.pets) - 1
            self._update_display()
            for msg in messages:
                self._log_message(msg)
        elif not self.pets:
            self.exit()
    def _animation_tick(self):
        if self.pets:
            pet_display = self.query_one("#pet-display", PetDisplay)
            if pet_display.renderer:
                state = pet_display.renderer.get_state_for_pet(self.pets[self.current_pet_index])
                pet_display.next_frame(state)

    def _update_display(self):
        if not self.pets:
            return
        pet = self.pets[self.current_pet_index]
        self.renderer = PetRenderer(pet.species)
        pet_display = self.query_one("#pet-display", PetDisplay)
        pet_display.set_renderer(self.renderer)
        state = self.renderer.get_state_for_pet(pet)
        pet_display.update_display(state)
        stats_panel = self.query_one("#stats-panel", StatsPanel)
        stats_panel.set_pet(pet)

    def _log_message(self, message):
        msg_log = self.query_one("#message-log", MessageLog)
        msg_log.add_message(message)

    def _do_action(self, action):
        if not self.pets:
            return
        pet = self.pets[self.current_pet_index]
        messages = self.pet_actions.interact(pet, action)
        for msg in messages:
            self._log_message(msg)
        self._update_display()
    def action_feed(self):
        self._do_action("feed")

    def action_play(self):
        self._do_action("play")

    def action_do_sleep(self):
        self._do_action("sleep")

    def action_train(self):
        self._do_action("train")

    def action_pet_action(self):
        self._do_action("pet")

    def action_next_pet(self):
        if self.pets:
            self.current_pet_index = (self.current_pet_index + 1) % len(self.pets)
            self._update_display()
            self._log_message(f"Switched to {self.pets[self.current_pet_index].name}")

    def action_new_pet(self):
        self.push_screen(NewPetScreen(), self._on_new_pet_result)

    def action_toggle_theme(self):
        theme_names = list(THEMES.keys())
        self.current_theme_index = (self.current_theme_index + 1) % len(theme_names)
        theme_name = theme_names[self.current_theme_index]
        self._log_message(f"Theme: {THEMES[theme_name].name}")

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if button_id == "btn-feed":
            self.action_feed()
        elif button_id == "btn-play":
            self.action_play()
        elif button_id == "btn-sleep":
            self.action_do_sleep()
        elif button_id == "btn-train":
            self.action_train()
        elif button_id == "btn-pet":
            self.action_pet_action()

def main():
    """Entry point."""
    app = TerminalBuddyApp()
    app.run()


if __name__ == "__main__":
    main()