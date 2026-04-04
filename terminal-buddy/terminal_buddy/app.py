# -*- coding: utf-8 -*-
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
from terminal_buddy.i18n import get_text, set_language, get_language, toggle_language
from terminal_buddy.rarity import get_rarity_display
from terminal_buddy.breakthrough import get_breakthrough_status, get_material_display
from terminal_buddy.travel import get_travel_status, get_atlas_progress
from terminal_buddy.atlas_view import AtlasLanguageScreen, AtlasPetSelectScreen, AtlasDetailScreen


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
            self.update(get_text("no_pet_selected"))
            return

        lines = []
        lines.append(f"{get_text('name')}: {self.pet.name}")
        # 物种名称翻译
        species_display = get_text(f"species_{self.pet.species}")
        if species_display == f"species_{self.pet.species}":
            species_display = self.pet.species
        lines.append(f"{get_text('species')}: {species_display}  Lv.{self.pet.level}")
        
        # 稀有度显示
        rarity_display = get_rarity_display(self.pet.rarity, self.pet.is_shiny, get_language())
        lines.append(f"{get_text('rarity_label')}: {rarity_display}")
        # 阶段显示
        phase_display = get_breakthrough_status(self.pet, get_language())
        lines.append(f"{get_text('phase_label')}: {phase_display}")
        # 材料显示
        materials_display = get_material_display(self.pet, get_language())
        lines.append(f"{get_text('materials_label')}: {materials_display}")
        
        xp_needed = self.pet.xp_for_next_level
        lines.append(f"{get_text('xp')}: {self.pet.xp}/{xp_needed}")
        lines.append("")
        lines.append(f"{get_text('hunger')}: {self._bar(self.pet.hunger)} {self.pet.hunger}%")
        lines.append(f"{get_text('mood')}:   {self._bar(self.pet.mood)} {self.pet.mood}%")
        lines.append(f"{get_text('energy')}: {self._bar(self.pet.energy)} {self.pet.energy}%")
        lines.append(f"{get_text('tired_label')}: {self._bar(self.pet.tired)} {self.pet.tired}%")
        # 状态显示翻译
        status_text = get_text(self.pet.status_emoji)
        lines.append(f"{get_text('status')}: {status_text}")
        # 旅行状态
        travel_status = get_travel_status(self.pet, get_language())
        lines.append(f"{get_text('travel_label')}: {travel_status}")
        # 图鉴进度
        atlas_progress = get_atlas_progress(self.pet, get_language())
        lines.append(f"{get_text('atlas_label')}: {atlas_progress}")
        # 闪光水晶
        if self.pet.shiny_evolution_items > 0:
            lines.append(f"{get_text('shiny_items_label')}: {self.pet.shiny_evolution_items}")

        self.update(chr(10).join(lines))


class ActionBar(Horizontal):
    """Row of action buttons."""

    def compose(self):
        yield Button(get_text("feed_btn"), id="btn-feed", variant="primary")
        yield Button(get_text("play_btn"), id="btn-play")
        yield Button(get_text("sleep_btn"), id="btn-sleep")
        yield Button(get_text("train_btn"), id="btn-train")
        yield Button(get_text("pet_btn"), id="btn-pet")
        yield Button(get_text("breakthrough_btn"), id="btn-breakthrough")
        yield Button(get_text("travel_btn"), id="btn-travel")
        yield Button(get_text("atlas_view_btn"), id="btn-atlas-view")


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
            Label(get_text("create_new_pet"), classes="title"),
            Label(get_text("name_label")),
            Input(placeholder=get_text("name_placeholder"), id="input-name"),
            Label(get_text("species_label")),
            Input(placeholder=get_text("species_placeholder"), id="input-species"),
            Button(get_text("create_btn"), id="btn-create", variant="primary"),
            Button(get_text("cancel_btn"), id="btn-cancel"),
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
    height: auto;
    border: solid green;
    content-align: center middle;
}

#stats-panel {
    width: 1fr;
    height: auto;
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
        ("b", "breakthrough", "Break"),
        ("v", "travel", "Travel"),
        ("a", "atlas_view", "Atlas View"),
        ("tab", "next_pet", "Next Pet"),
        ("n", "new_pet", "New Pet"),
        ("d", "toggle_theme", "Theme"),
        ("l", "toggle_language", "Language"),
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

    @property
    def TITLE(self):
        return get_text("app_title")

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

    def action_breakthrough(self):
        self._do_action("breakthrough")

    def action_travel(self):
        self._do_action("travel")

    def action_atlas_view(self):
        """Open atlas view system."""
        self.push_screen(AtlasLanguageScreen(), self._on_atlas_lang_result)

    def _on_atlas_lang_result(self, result):
        if result is None:
            return
        lang, _ = result
        self.push_screen(
            AtlasPetSelectScreen(self.pets, lang=lang),
            lambda pet, _lang=lang: self._on_atlas_pet_result(pet, _lang),
        )

    def _on_atlas_pet_result(self, pet, lang):
        if pet is None:
            return
        self.push_screen(AtlasDetailScreen(pet, lang=lang))

    def action_next_pet(self):
        if self.pets:
            self.current_pet_index = (self.current_pet_index + 1) % len(self.pets)
            self._update_display()
            self._log_message(get_text("switched_to", name=self.pets[self.current_pet_index].name))

    def action_new_pet(self):
        self.push_screen(NewPetScreen(), self._on_new_pet_result)

    def action_toggle_theme(self):
        theme_names = list(THEMES.keys())
        self.current_theme_index = (self.current_theme_index + 1) % len(theme_names)
        theme_name = theme_names[self.current_theme_index]
        self._log_message(get_text("theme_changed", theme_name=THEMES[theme_name].name))

    def action_toggle_language(self):
        new_lang = toggle_language()
        lang_name = get_text("lang_zh" if new_lang == "zh" else "lang_en")
        self._log_message(get_text("lang_switched", lang=lang_name))
        # Refresh the UI
        self._update_display()
        # Rebuild action bar with new language
        action_bar = self.query_one("#action-bar", ActionBar)
        action_bar.remove_children()
        for btn in action_bar.compose():
            action_bar.mount(btn)

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
        elif button_id == "btn-breakthrough":
            self.action_breakthrough()
        elif button_id == "btn-travel":
            self.action_travel()
        elif button_id == "btn-atlas-view":
            self.action_atlas_view()


def main():
    """Entry point."""
    app = TerminalBuddyApp()
    app.run()


if __name__ == "__main__":
    main()
