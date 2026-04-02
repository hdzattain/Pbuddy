"""Rich-based display for buddy information."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

from buddy_reroll.models import Buddy, BuddyMatch, BuddyStats
from buddy_reroll.constants import SPECIES, RARITIES, STATS, RARITY_WEIGHTS
from buddy_reroll.ascii_art import SPECIES_ART, HAT_ART

# 稀有度颜色映射
RARITY_COLORS = {
    "common": "bright_black",
    "uncommon": "green",
    "rare": "blue",
    "epic": "magenta",
    "legendary": "yellow",
}

RARITY_STARS = {
    "common": "★",
    "uncommon": "★★",
    "rare": "★★★",
    "epic": "★★★★",
    "legendary": "★★★★★",
}

# 属性颜色映射
STAT_COLORS = {
    "debugging": "cyan",
    "patience": "green",
    "chaos": "red",
    "wisdom": "blue",
    "snark": "magenta",
}

console = Console()


def _get_stat_color(value: int) -> str:
    """根据属性值返回颜色。"""
    if value >= 80:
        return "bright_green"
    elif value >= 60:
        return "green"
    elif value >= 40:
        return "yellow"
    elif value >= 20:
        return "orange3"
    else:
        return "red"


def stat_bar(value: int, width: int = 20) -> str:
    """生成属性条形图字符串。"""
    filled = int(value / 100 * width)
    return "█" * filled + "░" * (width - filled)


def _format_ascii_with_hat(art: str, hat: str) -> str:
    """将帽子叠加到ASCII art上方。"""
    hat_emoji = HAT_ART.get(hat, "")
    if not hat_emoji:
        return art.strip("\n")
    
    lines = art.strip("\n").split("\n")
    # 在第一行上方添加帽子
    return hat_emoji + "\n" + "\n".join(lines)


def display_buddy(buddy: Buddy, uid: str | None = None) -> None:
    """
    显示单个宠物的卡片式信息。
    
    使用 Rich Panel 包裹，包含：
    - ASCII art（带帽子）
    - 物种名、稀有度（带颜色和星星）
    - 眼睛、帽子、shiny 标记
    - 属性条形图（用 █ 和 ░ 渲染，颜色根据数值变化）
    - 如果提供 uid，显示在底部
    """
    # 构建标题
    rarity_color = RARITY_COLORS.get(buddy.rarity, "white")
    stars = RARITY_STARS.get(buddy.rarity, "")
    
    shiny_text = " [bold yellow]✨SHINY✨[/bold yellow]" if buddy.shiny else ""
    title = f"[bold]{buddy.species.upper()}[/bold] [{rarity_color}]{stars}[/{rarity_color}]{shiny_text}"
    
    # 获取ASCII art
    art = SPECIES_ART.get(buddy.species, SPECIES_ART["blob"])
    art_with_hat = _format_ascii_with_hat(art, buddy.hat)
    
    # 构建属性表格
    stats_lines = []
    stat_names = ["debugging", "patience", "chaos", "wisdom", "snark"]
    stat_values = [
        buddy.stats.debugging,
        buddy.stats.patience,
        buddy.stats.chaos,
        buddy.stats.wisdom,
        buddy.stats.snark,
    ]
    
    for name, value in zip(stat_names, stat_values):
        color = _get_stat_color(value)
        bar = stat_bar(value, width=15)
        label = name[:4].upper()
        stats_lines.append(f"[{STAT_COLORS[name]}]{label}[/{STAT_COLORS[name]}]: [{color}]{bar}[/{color}] {value}")
    
    # 构建内容
    content_lines = [
        f"[dim]Eye:[/dim] {buddy.eye}  [dim]Hat:[/dim] {buddy.hat}",
        "",
        art_with_hat,
        "",
        *stats_lines,
    ]
    
    if uid:
        content_lines.extend(["", f"[dim]UID: {uid}[/dim]"])
    
    content = "\n".join(content_lines)
    
    # 创建Panel
    panel = Panel(
        content,
        title=title,
        border_style=rarity_color,
        box=box.ROUNDED,
        padding=(1, 2),
    )
    
    console.print(panel)


def display_buddy_compact(match: BuddyMatch, index: int) -> None:
    """紧凑模式显示搜索结果（一行摘要 + uid）。"""
    buddy = match.buddy
    rarity_color = RARITY_COLORS.get(buddy.rarity, "white")
    shiny_mark = "✨" if buddy.shiny else " "
    
    text = Text()
    text.append(f"#{index} ", style="bold")
    text.append(f"[{shiny_mark}{buddy.species}] ", style=rarity_color)
    text.append(f"{buddy.rarity} ", style=rarity_color)
    text.append(f"eye={buddy.eye} hat={buddy.hat} ", style="dim")
    text.append(f"stats={buddy.stats.total()} ", style="cyan")
    text.append(f"uid={match.uid}", style="dim")
    
    console.print(text)


def display_gallery() -> None:
    """
    展示全部 18 种物种的图鉴。
    使用 Rich Columns 每行 3 个，每个用 Panel 包裹。
    """
    panels = []
    
    for species in SPECIES:
        art = SPECIES_ART.get(species, SPECIES_ART["blob"])
        # 去掉开头的空行
        art_clean = art.strip("\n")
        
        panel = Panel(
            art_clean,
            title=f"[bold]{species}[/bold]",
            box=box.SIMPLE,
            padding=(1, 1),
            width=20,
        )
        panels.append(panel)
    
    console.print("\n[bold cyan]🐾 Buddy Species Gallery 🐾[/bold cyan]\n")
    console.print(Columns(panels, equal=True, column_first=False))
    console.print()


def display_stats_table() -> None:
    """
    显示概率统计表。
    包含：稀有度概率、物种数量、属性范围等。
    用 Rich Table 渲染。
    """
    # 稀有度概率表
    rarity_table = Table(
        title="[bold]Rarity Probabilities[/bold]",
        box=box.ROUNDED,
    )
    rarity_table.add_column("Rarity", style="bold")
    rarity_table.add_column("Weight", justify="right")
    rarity_table.add_column("Probability", justify="right")
    rarity_table.add_column("Stat Floor", justify="right")
    
    for rarity, weight in RARITY_WEIGHTS:
        color = RARITY_COLORS.get(rarity, "white")
        prob = weight / 100
        from buddy_reroll.constants import RARITY_FLOORS
        floor = RARITY_FLOORS.get(rarity, 0)
        rarity_table.add_row(
            f"[{color}]{rarity}[/{color}]",
            str(weight),
            f"{prob:.0%}",
            str(floor),
        )
    
    # 物种表
    species_table = Table(
        title="[bold]Species Information[/bold]",
        box=box.ROUNDED,
    )
    species_table.add_column("Count", justify="right")
    species_table.add_column("Species Names")
    
    species_table.add_row(str(len(SPECIES)), ", ".join(SPECIES))
    
    # 属性表
    stats_table = Table(
        title="[bold]Stats Information[/bold]",
        box=box.ROUNDED,
    )
    stats_table.add_column("Stat", style="bold")
    stats_table.add_column("Description")
    
    stat_descriptions = {
        "DEBUGGING": "Problem-solving ability",
        "PATIENCE": "Ability to wait calmly",
        "CHAOS": "Unpredictable energy level",
        "WISDOM": "Knowledge and insight",
        "SNARK": "Sarcastic wit level",
    }
    
    for stat in STATS:
        desc = stat_descriptions.get(stat, "")
        color = STAT_COLORS.get(stat.lower(), "white")
        stats_table.add_row(f"[{color}]{stat}[/{color}]", desc)
    
    # 其他信息
    other_table = Table(
        title="[bold]Other Probabilities[/bold]",
        box=box.ROUNDED,
    )
    other_table.add_column("Feature")
    other_table.add_column("Probability", justify="right")
    
    from buddy_reroll.constants import SHINY_CHANCE
    other_table.add_row("Shiny", f"{SHINY_CHANCE:.0%}")
    other_table.add_row("Non-none Hat (non-common)", "~43%")
    
    console.print("\n[bold cyan]📊 Buddy Reroll Statistics 📊[/bold cyan]\n")
    console.print(rarity_table)
    console.print()
    console.print(species_table)
    console.print()
    console.print(stats_table)
    console.print()
    console.print(other_table)
    console.print()


def create_search_progress() -> Progress:
    """创建搜索进度条。"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        console=console,
    )
