# -*- coding: utf-8 -*-
"""Pet rarity and shiny calculation system."""
import hashlib
import uuid
from datetime import datetime

# 稀有度等级定义
RARITY_LEVELS = {
    1: {"name": "普通", "name_en": "Common", "color": "white", "prob": 0.60, "stars": "★"},
    2: {"name": "精良", "name_en": "Uncommon", "color": "green", "prob": 0.25, "stars": "★★"},
    3: {"name": "稀有", "name_en": "Rare", "color": "blue", "prob": 0.10, "stars": "★★★"},
    4: {"name": "史诗", "name_en": "Epic", "color": "purple", "prob": 0.049, "stars": "★★★★"},
    5: {"name": "传说", "name_en": "Legendary", "color": "orange", "prob": 0.001, "stars": "★★★★★"},
}

SHINY_PROB = 0.01  # 闪光概率 1%，独立于稀有度判定
HASH_SALT = "terminal-buddy-rarity-salt-2024"


def get_mac_address() -> str:
    """获取当前计算机 MAC 地址."""
    mac = uuid.getnode()
    return ':'.join(f'{(mac >> i) & 0xff:02x}' for i in range(0, 48, 8))


def calculate_rarity(mac_address: str = None, timestamp: str = None, salt: str = HASH_SALT) -> int:
    """基于 MAC地址+时间+盐 计算稀有度等级(1-5)."""
    if mac_address is None:
        mac_address = get_mac_address()
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    raw = f"{mac_address}:{timestamp}:{salt}:rarity"
    hash_hex = hashlib.sha256(raw.encode()).hexdigest()
    # 取前8位十六进制转为0-1之间的浮点数
    hash_value = int(hash_hex[:8], 16) / 0xFFFFFFFF
    
    cumulative = 0.0
    for level in sorted(RARITY_LEVELS.keys()):
        cumulative += RARITY_LEVELS[level]["prob"]
        if hash_value < cumulative:
            return level
    return 1  # fallback


def calculate_shiny(mac_address: str = None, timestamp: str = None, salt: str = HASH_SALT) -> bool:
    """独立判定是否为闪光宠物(1%概率)."""
    if mac_address is None:
        mac_address = get_mac_address()
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    raw = f"{mac_address}:{timestamp}:{salt}:shiny"
    hash_hex = hashlib.sha256(raw.encode()).hexdigest()
    hash_value = int(hash_hex[:8], 16) / 0xFFFFFFFF
    
    return hash_value < SHINY_PROB


def get_rarity_info(rarity: int) -> dict:
    """获取稀有度等级信息."""
    return RARITY_LEVELS.get(rarity, RARITY_LEVELS[1])


def get_rarity_display(rarity: int, is_shiny: bool = False, lang: str = "zh") -> str:
    """获取稀有度显示字符串."""
    info = get_rarity_info(rarity)
    name = info["name"] if lang == "zh" else info["name_en"]
    stars = info["stars"]
    shiny_mark = " ✦闪光" if is_shiny and lang == "zh" else (" ✦Shiny" if is_shiny else "")
    return f"{stars} {name}{shiny_mark}"
