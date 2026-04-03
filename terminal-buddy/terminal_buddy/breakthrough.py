# -*- coding: utf-8 -*-
"""Pet breakthrough (advancement) system - phase progression every 15 levels."""
from typing import TYPE_CHECKING

from .i18n import get_text

if TYPE_CHECKING:
    from .pet import Pet


# 阶段定义: 每15级一个阶段
PHASES = {
    1: {"name": "初阶", "name_en": "Novice", "level_range": (1, 15), "material": "初级突破石", "material_en": "Basic Breakthrough Stone"},
    2: {"name": "中阶", "name_en": "Intermediate", "level_range": (16, 30), "material": "中级突破石", "material_en": "Intermediate Breakthrough Stone"},
    3: {"name": "高阶", "name_en": "Advanced", "level_range": (31, 45), "material": "高级突破石", "material_en": "Advanced Breakthrough Stone"},
    4: {"name": "超阶", "name_en": "Master", "level_range": (46, 60), "material": "特级突破石", "material_en": "Master Breakthrough Stone"},
    5: {"name": "极阶", "name_en": "Ultimate", "level_range": (61, 75), "material": "终极突破石", "material_en": "Ultimate Breakthrough Stone"},
}

# 材料类型映射 (阶段 -> 材料key)
MATERIAL_KEYS = {
    1: "basic_stone",
    2: "intermediate_stone",
    3: "advanced_stone",
    4: "master_stone",
    5: "ultimate_stone",
}


def get_phase_info(phase: int) -> dict:
    """获取阶段信息."""
    return PHASES.get(phase, PHASES[1])


def get_level_cap(phase: int) -> int:
    """获取当前阶段的等级上限."""
    info = get_phase_info(phase)
    return info["level_range"][1]


def can_breakthrough(pet: "Pet") -> bool:
    """检查宠物是否可以突破."""
    if pet.phase >= 5:
        return False
    level_cap = get_level_cap(pet.phase)
    if pet.level < level_cap:
        return False
    # 检查是否拥有当前阶段对应的突破材料
    material_key = MATERIAL_KEYS[pet.phase]
    return pet.breakthrough_materials.get(material_key, 0) > 0


def perform_breakthrough(pet: "Pet") -> str | None:
    """执行突破，消耗材料，提升阶段."""
    if not can_breakthrough(pet):
        return None
    
    material_key = MATERIAL_KEYS[pet.phase]
    pet.breakthrough_materials[material_key] = pet.breakthrough_materials.get(material_key, 0) - 1
    
    old_phase = pet.phase
    pet.phase += 1
    
    old_info = get_phase_info(old_phase)
    new_info = get_phase_info(pet.phase)
    
    return get_text("breakthrough_success", 
                    name=pet.name,
                    old_phase=old_info["name"],
                    new_phase=new_info["name"])


def get_breakthrough_status(pet: "Pet", lang: str = "zh") -> str:
    """获取突破状态显示."""
    phase_info = get_phase_info(pet.phase)
    phase_name = phase_info["name"] if lang == "zh" else phase_info["name_en"]
    level_cap = get_level_cap(pet.phase)
    
    if pet.phase >= 5 and pet.level >= level_cap:
        return f"{phase_name} (MAX)" if lang == "en" else f"{phase_name}（已满级）"
    
    return f"{phase_name} ({pet.level}/{level_cap})"


def get_material_display(pet: "Pet", lang: str = "zh") -> str:
    """获取突破材料背包显示."""
    items = []
    for phase_num, material_key in MATERIAL_KEYS.items():
        count = pet.breakthrough_materials.get(material_key, 0)
        if count > 0:
            phase_info = PHASES[phase_num]
            mat_name = phase_info["material"] if lang == "zh" else phase_info["material_en"]
            items.append(f"{mat_name} x{count}")
    
    if not items:
        return get_text("no_materials")
    return ", ".join(items)
