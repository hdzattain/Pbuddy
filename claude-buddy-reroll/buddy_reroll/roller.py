"""Buddy pet generation core logic."""
import secrets
import string

from .constants import (
    SALT, SPECIES, RARITY_WEIGHTS, RARITY_FLOORS,
    EYES, HATS, STATS, SHINY_CHANCE
)
from .hasher import fnv1a_32
from .rng import Mulberry32
from .models import Buddy, BuddyStats, BuddyMatch


class BuddyRoller:
    """宠物生成器。"""

    def roll(self, uid: str) -> Buddy:
        """从 uid 确定性生成一只宠物。"""
        # 1. hash(uid + SALT) 得到种子
        seed = fnv1a_32(uid + SALT)
        # 2. 用种子初始化 Mulberry32
        rng = Mulberry32(seed)
        # 3. 按顺序 roll: rarity -> species -> eye -> hat -> shiny -> stats
        rarity = self._roll_rarity(rng)
        species = rng.pick(SPECIES)
        eye = rng.pick(EYES)
        hat = self._roll_hat(rng, rarity)
        shiny = self._roll_shiny(rng)
        stats = self._roll_stats(rng, rarity)

        return Buddy(
            species=species,
            rarity=rarity,
            eye=eye,
            hat=hat,
            shiny=shiny,
            stats=stats
        )

    def check(self, uid: str) -> Buddy:
        """check 是 roll 的别名。"""
        return self.roll(uid)

    def search(
        self,
        species: str | None = None,
        rarity: str | None = None,
        eye: str | None = None,
        hat: str | None = None,
        shiny: bool = False,
        min_stats: int | None = None,
        max_iterations: int = 50_000_000,
        count: int = 3,
    ) -> list[BuddyMatch]:
        """
        暴力搜索满足条件的 uid。
        每次生成随机 uid，roll 出 buddy，检查是否满足所有过滤条件。
        """
        results: list[BuddyMatch] = []
        iterations = 0

        while len(results) < count and iterations < max_iterations:
            # Generate random uid (16 alphanumeric characters)
            uid = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
            buddy = self.roll(uid)

            # Check all filters
            if species is not None and buddy.species != species:
                iterations += 1
                continue
            if rarity is not None and buddy.rarity != rarity:
                iterations += 1
                continue
            if eye is not None and buddy.eye != eye:
                iterations += 1
                continue
            if hat is not None and buddy.hat != hat:
                iterations += 1
                continue
            if shiny and not buddy.shiny:
                iterations += 1
                continue
            if min_stats is not None and buddy.stats.total() < min_stats:
                iterations += 1
                continue

            results.append(BuddyMatch(uid=uid, buddy=buddy))
            iterations += 1

        return results

    def _roll_rarity(self, rng: Mulberry32) -> str:
        """Roll rarity based on weights."""
        return rng.weighted_pick(RARITY_WEIGHTS)

    def _roll_hat(self, rng: Mulberry32, rarity: str) -> str:
        """Roll hat. Common rarity always gets 'none'."""
        if rarity == 'common':
            return 'none'
        return rng.pick(HATS)

    def _roll_shiny(self, rng: Mulberry32) -> bool:
        """Roll shiny status (1% chance)."""
        return rng.next() < SHINY_CHANCE

    def _roll_stats(self, rng: Mulberry32, rarity: str) -> BuddyStats:
        """
        Roll stats with floor based on rarity.

        Each pet has:
        - One peak stat (highest)
        - One dump stat (lowest)
        - All stats >= rarity floor
        """
        floor = RARITY_FLOORS[rarity]

        # Roll base stats (0-50 range, then add floor)
        raw_stats = [int(rng.next() * 51) + floor for _ in range(5)]

        # Pick peak and dump stats
        peak_idx = int(rng.next() * 5)
        dump_idx = int(rng.next() * 5)
        # Ensure they're different
        while dump_idx == peak_idx:
            dump_idx = int(rng.next() * 5)

        # Boost peak stat by 10-20
        raw_stats[peak_idx] += int(rng.next() * 11) + 10

        # Reduce dump stat by 5-15 (but not below floor)
        reduction = int(rng.next() * 11) + 5
        raw_stats[dump_idx] = max(floor, raw_stats[dump_idx] - reduction)

        return BuddyStats(
            debugging=raw_stats[0],
            patience=raw_stats[1],
            chaos=raw_stats[2],
            wisdom=raw_stats[3],
            snark=raw_stats[4]
        )
