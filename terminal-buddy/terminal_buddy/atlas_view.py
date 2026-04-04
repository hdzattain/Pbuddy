# -*- coding: utf-8 -*-
"""Atlas view screens - multi-level navigation for pet travel atlas."""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Static
from textual.containers import Vertical, Center, VerticalScroll

from .travel import TRAVEL_STAGES, POLAR_LOCATIONS, get_available_stage
from .breakthrough import PHASES, MATERIAL_KEYS
from .i18n import get_text


class AtlasLanguageScreen(Screen):
    """Language selection screen for atlas view."""

    CSS = """
    #lang-select-panel {
        width: 50;
        height: auto;
        padding: 2;
        border: solid green;
    }
    #atlas-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    #lang-prompt {
        text-align: center;
        margin-bottom: 1;
    }
    #btn-lang-en, #btn-lang-zh {
        width: 100%;
        margin: 1 0;
    }
    #btn-lang-back {
        width: 100%;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="lang-select-panel"):
                yield Label("Atlas View / \u56fe\u9274\u67e5\u770b", id="atlas-title")
                yield Label("Select Language / \u9009\u62e9\u8bed\u8a00", id="lang-prompt")
                yield Button("English", id="btn-lang-en", variant="primary")
                yield Button("\u7b80\u4f53\u4e2d\u6587", id="btn-lang-zh", variant="primary")
                yield Button("Back / \u8fd4\u56de", id="btn-lang-back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-lang-en":
            self.dismiss(("en", None))
        elif event.button.id == "btn-lang-zh":
            self.dismiss(("zh", None))
        elif event.button.id == "btn-lang-back":
            self.dismiss(None)


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
        title = "Select Pet" if self.lang == "en" else "\u9009\u62e9\u5ba0\u7269"
        back = "Back" if self.lang == "en" else "\u8fd4\u56de"

        with Center():
            with Vertical(id="pet-select-panel"):
                yield Label(title, id="pet-select-title")
                for i, pet in enumerate(self.pets):
                    species_key = f"species_{pet.species}"
                    species_name = get_text(species_key, lang=self.lang)
                    if species_name == species_key:
                        species_name = pet.species
                    label = f"{pet.name} ({species_name}) Lv.{pet.level}"
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

        status = ("UNLOCKED" if self.lang == "en" else "\u5df2\u89e3\u9501") if self.is_unlocked else ("LOCKED" if self.lang == "en" else "\u672a\u89e3\u9501")

        bar_width = 25
        filled = int(visited_count / total * bar_width) if total > 0 else 0
        empty = bar_width - filled
        bar = "[" + "\u2588" * filled + "\u2591" * empty + "]"
        percent = int(visited_count / total * 100) if total > 0 else 0

        complete_mark = ""
        if visited_count >= total:
            complete_mark = " \u2713 COMPLETE" if self.lang == "en" else " \u2713 \u5df2\u5b8c\u6210"

        header = f"\u2550\u2550\u2550 Stage {self.stage_num}: {name} [{status}] \u2550\u2550\u2550"
        progress = f"  {bar} {visited_count}/{total} ({percent}%){complete_mark}"

        lines = [header, progress]

        if self.is_unlocked and self.visited_locations:
            loc_label = "Visited" if self.lang == "en" else "\u5df2\u8bbf\u95ee"
            display_locs = self.visited_locations[:8]
            locations_text = f"  {loc_label}: {', '.join(display_locs)}"
            if len(self.visited_locations) > 8:
                more = f" +{len(self.visited_locations) - 8} more" if self.lang == "en" else f" +{len(self.visited_locations) - 8} \u66f4\u591a"
                locations_text += more
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
        title = "Polar Expedition" if self.lang == "en" else "\u5357\u5317\u6781\u63a2\u9669"
        status = ("UNLOCKED" if self.lang == "en" else "\u5df2\u89e3\u9501") if self.is_unlocked else ("LOCKED" if self.lang == "en" else "\u672a\u89e3\u9501")

        total = len(POLAR_LOCATIONS)
        visited = len(self.polar_visited)

        bar_width = 25
        filled = int(visited / total * bar_width) if total > 0 else 0
        empty = bar_width - filled
        bar = "[" + "\u2588" * filled + "\u2591" * empty + "]"

        header = f"\u2550\u2550\u2550 \u2605 {title} [{status}] \u2605 \u2550\u2550\u2550"
        progress = f"  {bar} {visited}/{total}"

        lines = [header, progress]

        if self.polar_visited:
            loc_label = "Explored" if self.lang == "en" else "\u5df2\u63a2\u7d22"
            lines.append(f"  {loc_label}: {', '.join(self.polar_visited)}")

        if self.shiny_items > 0:
            crystal_label = "Shiny Evolution Crystals" if self.lang == "en" else "\u95ea\u5149\u8fdb\u5316\u6c34\u6676"
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
        title = "Breakthrough Materials" if self.lang == "en" else "\u7a81\u7834\u6750\u6599"
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
            empty_msg = "No materials collected yet" if self.lang == "en" else "\u6682\u65e0\u6750\u6599"
            lines.append(f"  {empty_msg}")

        return chr(10).join(lines)

    def on_mount(self):
        self.update(self._render_content())


class AtlasDetailScreen(Screen):
    """Atlas detail screen showing full travel progress for a pet."""

    CSS = """
    #atlas-detail-container {
        width: 100%;
        height: 1fr;
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
        margin: 1 0;
        padding: 1;
        border: solid green;
    }

    .stage-widget-locked {
        width: 100%;
        height: auto;
        margin: 1 0;
        padding: 1;
        border: solid grey;
    }

    .polar-widget {
        width: 100%;
        height: auto;
        margin: 1 0;
        padding: 1;
        border: solid cyan;
    }

    .material-widget {
        width: 100%;
        height: auto;
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

        title_text = f"{self.pet.name} ({species_name}) Lv.{self.pet.level}"
        atlas_title = "Atlas" if self.lang == "en" else "\u56fe\u9274"

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

            back_text = "Back" if self.lang == "en" else "\u8fd4\u56de"
            yield Button(back_text, id="btn-atlas-back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-atlas-back":
            self.dismiss(None)
