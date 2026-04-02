"""Mulberry32 PRNG implementation."""


class Mulberry32:
    """
    Mulberry32 伪随机数生成器。

    独立实现，基于 Mulberry32 算法的公开规范。
    产生 [0, 1) 范围的浮点数。
    """

    def __init__(self, seed: int):
        """Initialize with a seed."""
        self._state = seed & 0xffffffff

    def next(self) -> float:
        """
        Generate next random number in [0, 1) range.

        Mulberry32 algorithm:
        - state = (state + 0x6D2B79F5) & 0xffffffff
        - z = state
        - z = (z ^ (z >> 15)) * (z | 1) & 0xffffffff
        - z ^= z + (z ^ (z >> 7)) * (z | 61) & 0xffffffff
        - z ^= z >> 14
        - return z / 2^32
        """
        self._state = (self._state + 0x6D2B79F5) & 0xffffffff
        z = self._state
        z = (z ^ (z >> 15)) * (z | 1) & 0xffffffff
        z ^= (z + ((z ^ (z >> 7)) * (z | 61) & 0xffffffff)) & 0xffffffff
        z ^= z >> 14
        return z / 4294967296.0  # 2^32

    def pick(self, items: tuple | list):
        """Randomly pick an item from a sequence."""
        if not items:
            raise ValueError("Cannot pick from empty sequence")
        idx = int(self.next() * len(items))
        return items[idx]

    def weighted_pick(self, weighted_items: tuple[tuple[str, int], ...]) -> str:
        """
        Pick an item based on weights.

        Args:
            weighted_items: Tuple of (item, weight) pairs.
        """
        total = sum(w for _, w in weighted_items)
        threshold = self.next() * total
        cumulative = 0
        for item, weight in weighted_items:
            cumulative += weight
            if threshold < cumulative:
                return item
        # Fallback to last item (shouldn't happen with valid weights)
        return weighted_items[-1][0]
