"""FNV-1a 32-bit hash implementation."""
from .constants import FNV_OFFSET_BASIS, FNV_PRIME, FNV_MOD


def fnv1a_32(data: str) -> int:
    """
    FNV-1a 32-bit hash.

    独立实现，基于 FNV 哈希算法的公开规范：
    - offset_basis = 2166136261
    - prime = 16777619
    - 对每个字节：hash ^= byte, hash *= prime
    - 结果取 32-bit 无符号
    """
    hash_val = FNV_OFFSET_BASIS
    for byte in data.encode('utf-8'):
        hash_val ^= byte
        hash_val = (hash_val * FNV_PRIME) % FNV_MOD
    return hash_val
