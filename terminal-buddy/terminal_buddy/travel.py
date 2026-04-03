# -*- coding: utf-8 -*-
"""Travel system - explore the world, collect atlas entries and breakthrough materials."""
import random
import hashlib
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .i18n import get_text
from .breakthrough import MATERIAL_KEYS, PHASES

if TYPE_CHECKING:
    from .pet import Pet


# 旅行阶段定义
TRAVEL_STAGES = {
    1: {
        "name": "中国之旅",
        "name_en": "China Tour",
        "duration_range": (1, 10),  # 分钟
        "material_key": "basic_stone",
        "locations": [
            "北京", "天津", "上海", "重庆", "河北", "山西", "辽宁", "吉林",
            "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南",
            "湖北", "湖南", "广东", "海南", "四川", "贵州", "云南", "陕西",
            "甘肃", "青海", "台湾", "内蒙古", "广西", "西藏", "宁夏", "新疆",
            "香港", "澳门",
        ],
    },
    2: {
        "name": "东南亚之旅",
        "name_en": "Southeast Asia Tour",
        "duration_range": (2, 15),
        "material_key": "intermediate_stone",
        "locations": [
            "泰国", "越南", "新加坡", "马来西亚", "印度尼西亚", "菲律宾",
            "缅甸", "柬埔寨", "老挝", "文莱", "东帝汶",
        ],
    },
    3: {
        "name": "欧洲之旅",
        "name_en": "Europe Tour",
        "duration_range": (3, 20),
        "material_key": "advanced_stone",
        "locations": [
            "英国", "法国", "德国", "意大利", "西班牙", "葡萄牙", "荷兰",
            "比利时", "瑞士", "奥地利", "瑞典", "挪威", "丹麦", "芬兰",
            "希腊", "波兰", "捷克", "匈牙利", "爱尔兰", "冰岛",
        ],
    },
    4: {
        "name": "美洲之旅",
        "name_en": "Americas Tour",
        "duration_range": (5, 25),
        "material_key": "master_stone",
        "locations": [
            "美国", "加拿大", "墨西哥", "古巴", "海地", "秘鲁",
            "巴西", "委内瑞拉", "阿根廷", "智利",
        ],
    },
    5: {
        "name": "非洲之旅",
        "name_en": "Africa Tour",
        "duration_range": (5, 30),
        "material_key": "ultimate_stone",
        "locations": [
            "摩洛哥", "南非", "尼日利亚", "坦桑尼亚", "中非",
            "马达加斯加", "毛里求斯", "津巴布韦", "肯尼亚", "刚果", "埃及", "利比亚",
        ],
    },
}

POLAR_LOCATIONS = ["北极", "南极"]
SHINY_EVOLUTION_PROB = 0.001  # 南北极 0.1% 概率获取闪光进化道具

# 材料掉落概率
NEW_LOCATION_MATERIAL_PROB = 0.10  # 新地点 10%
OLD_LOCATION_MATERIAL_PROB = 0.01  # 老地点 1%


def get_available_stage(pet: "Pet") -> int:
    """获取宠物当前可用的最高旅行阶段."""
    atlas = pet.travel_atlas or {}
    
    # 默认可用阶段1
    available = 1
    
    for stage_num in range(1, 6):
        stage_info = TRAVEL_STAGES[stage_num]
        stage_key = str(stage_num)
        visited = set(atlas.get(stage_key, []))
        all_locations = set(stage_info["locations"])
        
        if visited >= all_locations:  # 集齐了该阶段图鉴
            if stage_num < 5:
                available = stage_num + 1
            else:
                available = 6  # 解锁南北极
        else:
            break
    
    return min(available, 6)  # 最高6(南北极)


def is_polar_unlocked(pet: "Pet") -> bool:
    """检查是否解锁了南北极."""
    return get_available_stage(pet) >= 6


def start_travel(pet: "Pet") -> str | None:
    """开始一次旅行."""
    if pet.current_travel is not None:
        return get_text("already_traveling", name=pet.name)
    
    if not pet.is_alive:
        return get_text("no_longer_with_us", name=pet.name)
    
    available_stage = get_available_stage(pet)
    
    # 决定去哪个阶段
    if available_stage >= 6:
        # 可以去南北极，但也可以去之前的阶段
        # 10% 概率去南北极，90% 概率去已解锁的随机阶段
        if random.random() < 0.10:
            stage_num = 6
        else:
            stage_num = random.randint(1, 5)
    else:
        stage_num = available_stage
    
    # 选择目的地
    if stage_num == 6:
        location = random.choice(POLAR_LOCATIONS)
        duration_minutes = random.randint(10, 30)
        stage_name = "南北极探险"
    else:
        stage_info = TRAVEL_STAGES[stage_num]
        location = random.choice(stage_info["locations"])
        duration_minutes = random.randint(*stage_info["duration_range"])
        stage_name = stage_info["name"]
    
    now = datetime.now()
    end_time = now + timedelta(minutes=duration_minutes)
    
    pet.current_travel = {
        "stage": stage_num,
        "location": location,
        "stage_name": stage_name,
        "start_time": now.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_minutes": duration_minutes,
    }
    
    return get_text("travel_started",
                    name=pet.name,
                    location=location,
                    stage_name=stage_name,
                    duration=duration_minutes)


def check_travel_complete(pet: "Pet") -> list[str]:
    """检查旅行是否完成，返回结果消息列表."""
    messages = []
    
    if pet.current_travel is None:
        return messages
    
    try:
        end_time = datetime.fromisoformat(pet.current_travel["end_time"])
    except (ValueError, KeyError):
        pet.current_travel = None
        return messages
    
    if datetime.now() < end_time:
        return messages  # 还在旅行中
    
    # 旅行完成
    travel = pet.current_travel
    stage_num = travel["stage"]
    location = travel["location"]
    stage_name = travel["stage_name"]
    
    messages.append(get_text("travel_complete",
                            name=pet.name,
                            location=location,
                            stage_name=stage_name))
    
    # 初始化图鉴
    if pet.travel_atlas is None:
        pet.travel_atlas = {}
    
    # 处理南北极
    if stage_num == 6:
        polar_key = "polar"
        if polar_key not in pet.travel_atlas:
            pet.travel_atlas[polar_key] = []
        
        is_new = location not in pet.travel_atlas[polar_key]
        if is_new:
            pet.travel_atlas[polar_key].append(location)
            messages.append(get_text("new_atlas_entry", location=location))
        
        # 0.1% 概率获取闪光进化道具
        if random.random() < SHINY_EVOLUTION_PROB:
            pet.shiny_evolution_items = pet.shiny_evolution_items + 1
            messages.append(get_text("shiny_evolution_item_get"))
        
        pet.current_travel = None
        return messages
    
    # 普通阶段处理
    stage_key = str(stage_num)
    if stage_key not in pet.travel_atlas:
        pet.travel_atlas[stage_key] = []
    
    is_new_location = location not in pet.travel_atlas[stage_key]
    
    # 记录到图鉴
    if is_new_location:
        pet.travel_atlas[stage_key].append(location)
        messages.append(get_text("new_atlas_entry", location=location))
    
    # 检查是否刚集齐该阶段图鉴
    stage_info = TRAVEL_STAGES[stage_num]
    all_locations = set(stage_info["locations"])
    visited = set(pet.travel_atlas[stage_key])
    just_completed = is_new_location and visited >= all_locations
    
    # 材料掉落判定
    material_key = stage_info["material_key"]
    got_material = False
    
    if just_completed:
        # 集齐图鉴，必得突破材料
        got_material = True
        messages.append(get_text("atlas_complete", stage_name=stage_info["name"]))
    elif is_new_location:
        # 新地点 10% 概率
        got_material = random.random() < NEW_LOCATION_MATERIAL_PROB
    else:
        # 老地点 1% 概率
        got_material = random.random() < OLD_LOCATION_MATERIAL_PROB
    
    if got_material:
        pet.breakthrough_materials[material_key] = pet.breakthrough_materials.get(material_key, 0) + 1
        from .i18n import get_language
        lang = get_language()
        phase_info = PHASES[stage_num]
        material_name = phase_info["material"] if lang == "zh" else phase_info["material_en"]
        messages.append(get_text("material_obtained",
                                material=material_name))
    
    # 检查是否解锁了下一阶段
    if just_completed and stage_num < 5:
        next_stage = TRAVEL_STAGES[stage_num + 1]
        messages.append(get_text("next_stage_unlocked",
                                stage_name=next_stage["name"]))
    elif just_completed and stage_num == 5:
        messages.append(get_text("polar_unlocked"))
    
    pet.current_travel = None
    return messages


def get_travel_status(pet: "Pet", lang: str = "zh") -> str:
    """获取旅行状态显示."""
    if pet.current_travel is None:
        return get_text("not_traveling") if lang == "zh" else get_text("not_traveling", lang="en")
    
    travel = pet.current_travel
    try:
        end_time = datetime.fromisoformat(travel["end_time"])
        remaining = end_time - datetime.now()
        if remaining.total_seconds() <= 0:
            return get_text("travel_returning", location=travel["location"])
        minutes_left = int(remaining.total_seconds() / 60) + 1
        return get_text("traveling_to",
                       location=travel["location"],
                       minutes=minutes_left)
    except (ValueError, KeyError):
        return get_text("not_traveling")


def get_atlas_progress(pet: "Pet", lang: str = "zh") -> str:
    """获取图鉴进度显示."""
    atlas = pet.travel_atlas or {}
    parts = []
    
    for stage_num in range(1, 6):
        stage_info = TRAVEL_STAGES[stage_num]
        stage_key = str(stage_num)
        visited = len(atlas.get(stage_key, []))
        total = len(stage_info["locations"])
        stage_name = stage_info["name"] if lang == "zh" else stage_info["name_en"]
        
        if visited > 0:
            mark = "✓" if visited >= total else ""
            parts.append(f"{stage_name}: {visited}/{total}{mark}")
    
    # 南北极
    polar_visited = len(atlas.get("polar", []))
    if polar_visited > 0:
        polar_name = "南北极" if lang == "zh" else "Polar"
        parts.append(f"{polar_name}: {polar_visited}/{len(POLAR_LOCATIONS)}")
    
    if not parts:
        return get_text("no_atlas_entries") if lang != "en" else get_text("no_atlas_entries", lang="en")
    
    return " | ".join(parts)
