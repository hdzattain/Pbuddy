# -*- coding: utf-8 -*-
"""Atlas view screens - multi-level navigation for pet travel atlas."""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Static
from textual.containers import Vertical, Center, VerticalScroll

from .travel import TRAVEL_STAGES, POLAR_LOCATIONS, get_available_stage
from .breakthrough import PHASES, MATERIAL_KEYS
from .i18n import get_text


class AtlasPetSelectScreen(Screen):
    """Pet selection screen for atlas view."""

    CSS = """
    #pet-select-panel {
        width: 60;
        height: auto;
        padding: 2;
        border: solid green;
    }
    #pet-select-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    .pet-select-btn {
        width: 100%;
        margin: 0 0 1 0;
    }
    #btn-pet-back {
        width: 100%;
        margin-top: 1;
    }
    """

    def __init__(self, pets: list, lang: str = "zh"):
        super().__init__()
        self.pets = pets
        self.lang = lang

    def compose(self) -> ComposeResult:
        title = get_text("select_pet", lang=self.lang)
        back = get_text("back", lang=self.lang)

        with Center():
            with Vertical(id="pet-select-panel"):
                yield Label(title, id="pet-select-title")
                for i, pet in enumerate(self.pets):
                    species_key = f"species_{pet.species}"
                    species_name = get_text(species_key, lang=self.lang)
                    if species_name == species_key:
                        species_name = pet.species
                    label = f"{pet.name} ({species_name}) {get_text('level_prefix', lang=self.lang)}{pet.level}"
                    yield Button(label, id=f"btn-pet-{i}", classes="pet-select-btn")
                yield Button(back, id="btn-pet-back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-pet-back":
            self.dismiss(None)
        elif event.button.id and event.button.id.startswith("btn-pet-"):
            index = int(event.button.id.split("-")[-1])
            self.dismiss(self.pets[index])


class StageProgressWidget(Static):
    """Widget displaying progress for a single travel stage."""

    def __init__(self, stage_num: int, stage_info: dict, visited: list,
                 is_unlocked: bool, lang: str = "zh", **kwargs):
        super().__init__(**kwargs)
        self.stage_num = stage_num
        self.stage_info = stage_info
        self.visited_locations = visited
        self.is_unlocked = is_unlocked
        self.lang = lang

    def _render_content(self) -> str:
        name = self.stage_info["name"] if self.lang == "zh" else self.stage_info["name_en"]
        total = len(self.stage_info["locations"])
        visited_count = len(self.visited_locations)

        status = get_text("unlocked", lang=self.lang) if self.is_unlocked else get_text("locked", lang=self.lang)

        bar_width = 20
        filled = int(visited_count / total * bar_width) if total > 0 else 0
        empty = bar_width - filled
        bar = "[" + "\u2588" * filled + "\u2591" * empty + "]"
        percent = int(visited_count / total * 100) if total > 0 else 0

        complete_mark = ""
        if visited_count >= total:
            complete_mark = f" \u2713 {get_text('complete', lang=self.lang)}"

        stage_label = get_text("stage_label", lang=self.lang)
        header = f"\u2550\u2550\u2550 {stage_label} {self.stage_num}: {name} [{status}] \u2550\u2550\u2550"
        progress = f"  {bar} {visited_count}/{total} ({percent}%){complete_mark}"

        lines = [header, progress]

        if self.is_unlocked and self.visited_locations:
            loc_label = get_text("visited_label", lang=self.lang)
            display_locs = self.visited_locations[:8]
            locations_text = f"  {loc_label}: {', '.join(display_locs)}"
            if len(self.visited_locations) > 8:
                more_label = get_text("more_label", lang=self.lang)
                locations_text += f" +{len(self.visited_locations) - 8} {more_label}"
            lines.append(locations_text)

        return chr(10).join(lines)

    def on_mount(self):
        self.update(self._render_content())


class PolarWidget(Static):
    """Widget displaying polar expedition progress."""

    def __init__(self, polar_visited: list, is_unlocked: bool,
                 shiny_items: int, lang: str = "zh", **kwargs):
        super().__init__(**kwargs)
        self.polar_visited = polar_visited
        self.is_unlocked = is_unlocked
        self.shiny_items = shiny_items
        self.lang = lang

    def _render_content(self) -> str:
        title = get_text("polar_expedition", lang=self.lang)
        status = get_text("unlocked", lang=self.lang) if self.is_unlocked else get_text("locked", lang=self.lang)

        total = len(POLAR_LOCATIONS)
        visited = len(self.polar_visited)

        bar_width = 20
        filled = int(visited / total * bar_width) if total > 0 else 0
        empty = bar_width - filled
        bar = "[" + "\u2588" * filled + "\u2591" * empty + "]"

        header = f"\u2550\u2550\u2550 \u2605 {title} [{status}] \u2605 \u2550\u2550\u2550"
        progress = f"  {bar} {visited}/{total}"

        lines = [header, progress]

        if self.polar_visited:
            loc_label = get_text("explored_label", lang=self.lang)
            lines.append(f"  {loc_label}: {', '.join(self.polar_visited)}")

        if self.shiny_items > 0:
            crystal_label = get_text("shiny_crystals_label", lang=self.lang)
            lines.append(f"  {crystal_label}: {self.shiny_items}")

        return chr(10).join(lines)

    def on_mount(self):
        self.update(self._render_content())


class MaterialWidget(Static):
    """Widget displaying breakthrough material collection progress."""

    def __init__(self, materials: dict, lang: str = "zh", **kwargs):
        super().__init__(**kwargs)
        self.materials = materials
        self.lang = lang

    def _render_content(self) -> str:
        title = get_text("breakthrough_materials_title", lang=self.lang)
        lines = [f"\u2550\u2550\u2550 {title} \u2550\u2550\u2550"]

        has_any = False
        for phase_num in range(1, 6):
            phase_info = PHASES[phase_num]
            mat_key = MATERIAL_KEYS[phase_num]
            count = self.materials.get(mat_key, 0)
            mat_name = phase_info["material_en"] if self.lang == "en" else phase_info["material"]

            indicator = "\u25cf" if count > 0 else "\u25cb"
            lines.append(f"  {indicator} {mat_name}: x{count}")
            if count > 0:
                has_any = True

        if not has_any:
            empty_msg = get_text("no_materials_yet", lang=self.lang)
            lines.append(f"  {empty_msg}")

        return chr(10).join(lines)

    def on_mount(self):
        self.update(self._render_content())


class AtlasDetailScreen(Screen):
    """Atlas detail screen showing full travel progress for a pet."""

    CSS = """
    #atlas-detail-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    .atlas-header {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    .stage-widget {
        width: 100%;
        height: auto;
        min-height: 5;
        margin: 1 0;
        padding: 1;
        border: solid green;
    }

    .stage-widget-locked {
        width: 100%;
        height: auto;
        min-height: 5;
        margin: 1 0;
        padding: 1;
        border: solid grey;
    }

    .polar-widget {
        width: 100%;
        height: auto;
        min-height: 5;
        margin: 1 0;
        padding: 1;
        border: solid cyan;
    }

    .material-widget {
        width: 100%;
        height: auto;
        min-height: 5;
        margin: 1 0;
        padding: 1;
        border: solid yellow;
    }

    #btn-atlas-back {
        margin-top: 1;
        width: auto;
    }
    """

    def __init__(self, pet, lang: str = "zh"):
        super().__init__()
        self.pet = pet
        self.lang = lang

    def compose(self) -> ComposeResult:
        atlas = self.pet.travel_atlas or {}
        available_stage = get_available_stage(self.pet)

        species_key = f"species_{self.pet.species}"
        species_name = get_text(species_key, lang=self.lang)
        if species_name == species_key:
            species_name = self.pet.species

        level_prefix = get_text("level_prefix", lang=self.lang)
        title_text = f"{self.pet.name} ({species_name}) {level_prefix}{self.pet.level}"
        atlas_title = get_text("atlas_title", lang=self.lang)

        with VerticalScroll(id="atlas-detail-container"):
            yield Label(
                f"\u2550\u2550\u2550\u2550\u2550\u2550\u2550 {title_text} - {atlas_title} \u2550\u2550\u2550\u2550\u2550\u2550\u2550",
                classes="atlas-header",
            )

            for stage_num in range(1, 6):
                stage_info = TRAVEL_STAGES[stage_num]
                stage_key = str(stage_num)
                visited = atlas.get(stage_key, [])
                is_unlocked = stage_num <= available_stage
                css_class = "stage-widget" if is_unlocked else "stage-widget-locked"

                yield StageProgressWidget(
                    stage_num=stage_num,
                    stage_info=stage_info,
                    visited=visited,
                    is_unlocked=is_unlocked,
                    lang=self.lang,
                    classes=css_class,
                )

            polar_visited = atlas.get("polar", [])
            polar_unlocked = available_stage >= 6
            yield PolarWidget(
                polar_visited=polar_visited,
                is_unlocked=polar_unlocked,
                shiny_items=self.pet.shiny_evolution_items,
                lang=self.lang,
                classes="polar-widget",
            )

            yield MaterialWidget(
                materials=self.pet.breakthrough_materials or {},
                lang=self.lang,
                classes="material-widget",
            )

            yield Button(get_text("back", lang=self.lang), id="btn-atlas-back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-atlas-back":
            self.dismiss(None)
