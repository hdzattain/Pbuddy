"""CLI interface for buddy-reroll."""
import argparse
import secrets
import string
import sys

from buddy_reroll.roller import BuddyRoller
from buddy_reroll.display import (
    display_buddy, display_buddy_compact, display_gallery,
    display_stats_table, create_search_progress, console,
)
from buddy_reroll.constants import SPECIES, RARITIES, EYES, HATS


def main(argv: list[str] | None = None) -> None:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    
    args.func(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='buddy-reroll',
        description='Claude /buddy pet reroll tool — clean-room Python rewrite',
    )
    subparsers = parser.add_subparsers(dest='command')
    
    # search 命令
    search_p = subparsers.add_parser('search', help='Search for buddies matching criteria')
    search_p.add_argument('--species', choices=SPECIES, help='Target species')
    search_p.add_argument('--rarity', choices=RARITIES, help='Minimum rarity')
    search_p.add_argument('--eye', choices=EYES, help='Target eye style')
    search_p.add_argument('--hat', choices=HATS, help='Target hat')
    search_p.add_argument('--shiny', action='store_true', help='Require shiny')
    search_p.add_argument('--min-stats', type=int, metavar='N', help='All stats >= N')
    search_p.add_argument('--max', type=int, default=5_000_000, help='Max iterations')
    search_p.add_argument('--count', type=int, default=3, help='Number of results')
    search_p.set_defaults(func=cmd_search)
    
    # check 命令
    check_p = subparsers.add_parser('check', help='Check what buddy a uid produces')
    check_p.add_argument('uid', help='User ID to check')
    check_p.set_defaults(func=cmd_check)
    
    # gallery 命令
    gallery_p = subparsers.add_parser('gallery', help='Display all species ASCII art')
    gallery_p.set_defaults(func=cmd_gallery)
    
    # stats 命令
    stats_p = subparsers.add_parser('stats', help='Show probability statistics')
    stats_p.set_defaults(func=cmd_stats)
    
    return parser


def cmd_search(args) -> None:
    """执行搜索。带 Rich Progress bar 显示进度。"""
    roller = BuddyRoller()
    
    # 显示搜索条件
    filters = []
    if args.species: 
        filters.append(f"species={args.species}")
    if args.rarity: 
        filters.append(f"rarity>={args.rarity}")
    if args.eye: 
        filters.append(f"eye={args.eye}")
    if args.hat: 
        filters.append(f"hat={args.hat}")
    if args.shiny: 
        filters.append("shiny=true")
    if args.min_stats: 
        filters.append(f"all stats>={args.min_stats}")
    
    console.print(f"\n[bold]Searching:[/bold] {', '.join(filters) or 'any'}")
    console.print(f"[dim]Max iterations: {args.max:,} | Find: {args.count}[/dim]\n")
    
    # 使用 Progress bar 显示搜索进度
    results = []
    iterations = 0
    
    with create_search_progress() as progress:
        task = progress.add_task("Searching...", total=args.max)
        
        while len(results) < args.count and iterations < args.max:
            # 生成随机 uid
            uid = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
            buddy = roller.roll(uid)
            
            # 检查所有过滤条件
            matched = True
            if args.species is not None and buddy.species != args.species:
                matched = False
            if args.rarity is not None and buddy.rarity != args.rarity:
                matched = False
            if args.eye is not None and buddy.eye != args.eye:
                matched = False
            if args.hat is not None and buddy.hat != args.hat:
                matched = False
            if args.shiny and not buddy.shiny:
                matched = False
            if args.min_stats is not None and buddy.stats.min_stat() < args.min_stats:
                matched = False
            
            if matched:
                from buddy_reroll.models import BuddyMatch
                results.append(BuddyMatch(uid=uid, buddy=buddy))
            
            iterations += 1
            progress.update(task, completed=iterations)
    
    # 展示结果
    if not results:
        console.print("[red]No matches found![/red]")
    else:
        console.print(f"\n[green]Found {len(results)} match(es) in {iterations:,} iterations[/green]\n")
        for i, match in enumerate(results, 1):
            console.print(f"[bold]Match #{i}[/bold]")
            display_buddy(match.buddy, uid=match.uid)
            console.print()


def cmd_check(args) -> None:
    """查看指定 uid 的宠物。"""
    roller = BuddyRoller()
    buddy = roller.check(args.uid)
    
    console.print(f"\n[bold cyan]Buddy for UID: {args.uid}[/bold cyan]\n")
    display_buddy(buddy, uid=args.uid)


def cmd_gallery(args) -> None:
    """展示全部物种图鉴。"""
    display_gallery()


def cmd_stats(args) -> None:
    """显示概率统计。"""
    display_stats_table()


if __name__ == '__main__':
    main()
