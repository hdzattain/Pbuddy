# -*- coding: utf-8 -*-
"""Internationalization module for terminal-buddy."""

# Current language (default: Simplified Chinese)
_current_lang = "zh"

# English texts
LANG_EN = {
    # Button labels
    "feed_btn": "Feed [F]",
    "play_btn": "Play [P]",
    "sleep_btn": "Sleep [S]",
    "train_btn": "Train [T]",
    "pet_btn": "Pet [E]",
    
    # Menu/Action labels
    "feed": "Feed",
    "play": "Play",
    "sleep": "Sleep",
    "train": "Train",
    "pet": "Pet",
    "new_pet": "New Pet",
    "next_pet": "Next Pet",
    "theme": "Theme",
    "language": "Language",
    "quit": "Quit",
    
    # App title
    "app_title": "Terminal Buddy",
    
    # Create pet screen
    "create_new_pet": "Create New Pet",
    "name_label": "Name:",
    "species_label": "Species:",
    "name_placeholder": "Enter pet name",
    "species_placeholder": "blob, duck, cat, cactus, snail, rabbit",
    "create_btn": "Create",
    "cancel_btn": "Cancel",
    
    # Stats panel
    "no_pet_selected": "No pet selected",
    "name": "Name",
    "species": "Species",
    "xp": "XP",
    "hunger": "Hunger",
    "mood": "Mood",
    "energy": "Energy",
    "status": "Status",
    
    # Pet action messages
    "ate_snack": "{name} ate a snack! (+{amount} hunger)",
    "had_fun_playing": "{name} had fun playing! (+{amount} mood, -10 energy)",
    "took_nap": "{name} took a nap! (+{amount} energy, -5 hunger)",
    "trained_hard": "{name} trained hard! (-15 energy, -5 mood)",
    "enjoyed_cuddles": "{name} enjoyed the cuddles! (+{amount} mood)",
    
    # Level up
    "level_up": "Level up! {name} is now level {level}!",
    
    # Status messages
    "no_longer_with_us": "{name} is no longer with us...",
    "too_tired_to_train": "{name} is too tired to train!",
    
    # Action messages
    "unknown_action": "Unknown action: {action}",
    "unknown_species": "Unknown species, defaulting to 'blob'",
    "welcome_pet": "Welcome {name} the {species}!",
    "take_good_care": "Take good care of them!",
    "switched_to": "Switched to {name}",
    "theme_changed": "Theme: {theme_name}",
    
    # Ticker messages
    "starved": "{name} has starved... You should have fed them!",
    "missed_you": "{name} missed you! ({hours} hours passed)",
    "hours_passed": "{hours} hours have passed since you last checked on {name}.",
    "getting_hungry": "{name} is getting hungry...",
    "seems_lonely": "{name} seems lonely...",
    "well_rested": "{name} is well rested!",
    
    # Evolution
    "evolved": "{name} is evolving! {old} → {new}",
    
    # Rarity
    "rarity_label": "Rarity",
    "rarity_result": "Rarity: {rarity}",
    "shiny_congratulations": "WOW! A SHINY pet! You are incredibly lucky!",
    "shiny_label": "✦ Shiny",
    
    # Breakthrough
    "phase_label": "Phase",
    "materials_label": "Materials",
    "breakthrough_btn": "Break [B]",
    "breakthrough_success": "{name} broke through! {old_phase} -> {new_phase}!",
    "cannot_breakthrough": "{name} cannot break through yet! (Need materials or higher level)",
    "level_capped": "{name} has reached the level cap ({level})! Breakthrough required!",
    "no_materials": "No materials",
    
    # Travel
    "travel_btn": "Travel [V]",
    "atlas_btn": "Atlas [A]",
    "travel_label": "Travel",
    "atlas_label": "Atlas",
    "already_traveling": "{name} is already traveling!",
    "travel_started": "{name} set off for {stage_name} - {location}! (~{duration} min)",
    "travel_complete": "{name} returned from {stage_name} - {location}!",
    "new_atlas_entry": "New atlas entry: {location}!",
    "atlas_complete": "Atlas complete for {stage_name}! Guaranteed breakthrough material!",
    "material_obtained": "Obtained breakthrough material: {material}!",
    "next_stage_unlocked": "New travel stage unlocked: {stage_name}!",
    "polar_unlocked": "Polar expedition unlocked! Explore the Arctic and Antarctic!",
    "shiny_evolution_item_get": "Incredible! Found a Shiny Evolution Crystal!",
    "not_traveling": "Not traveling",
    "travel_returning": "Returning from {location}...",
    "traveling_to": "Traveling to {location} (~{minutes} min left)",
    "no_atlas_entries": "No atlas entries yet",
    "shiny_items_label": "Shiny Crystals",
    
    # Language toggle
    "lang_switched": "Language: {lang}",
    "lang_en": "English",
    "lang_zh": "简体中文",
    
    # Tired status
    "tired": "Tired",
    "tired_label": "Fatigue",
    "feeling_exhausted": "{name} is feeling exhausted...",
    "too_exhausted": "{name} is too exhausted!",
    "exhausted": "Exhausted",
    
    # Status translations
    "happy": "Happy",
    "content": "Content",
    "neutral": "Neutral",
    "sad": "Sad",
    "critical": "Critical",
    
    # Species names
    "species_blob": "Blob",
    "species_duck": "Duck",
    "species_cat": "Cat",
    "species_cactus": "Cactus",
    "species_snail": "Snail",
    "species_rabbit": "Rabbit",
    "species_ghost": "Ghost",
    "species_goose": "Goose",
    "species_owl": "Owl",
    "species_mushroom": "Mushroom",
    "species_turtle": "Turtle",
    "species_capybara": "Capybara",
    "species_dragon": "Dragon",
    "species_penguin": "Penguin",
    "species_axolotl": "Axolotl",
    "species_octopus": "Octopus",
    "species_robot": "Robot",
    "species_chonk": "Chonk",
    
    # Evolution message
    "evolved_message": "{name} evolved from {old} to {new}!",
}

# Simplified Chinese texts
LANG_ZH = {
    # Button labels
    "feed_btn": "喂食 [F]",
    "play_btn": "玩耍 [P]",
    "sleep_btn": "睡觉 [S]",
    "train_btn": "训练 [T]",
    "pet_btn": "抚摸 [E]",
    
    # Menu/Action labels
    "feed": "喂食",
    "play": "玩耍",
    "sleep": "睡觉",
    "train": "训练",
    "pet": "抚摸",
    "new_pet": "新宠物",
    "next_pet": "下一只",
    "theme": "主题",
    "language": "语言",
    "quit": "退出",
    
    # App title
    "app_title": "终端伙伴",
    
    # Create pet screen
    "create_new_pet": "创建新宠物",
    "name_label": "名字：",
    "species_label": "种类：",
    "name_placeholder": "输入宠物名字",
    "species_placeholder": "史莱姆(blob), 鸭子(duck), 猫咪(cat), 仙人掌(cactus), 蜗牛(snail), 兔子(rabbit)",
    "create_btn": "创建",
    "cancel_btn": "取消",
    
    # Stats panel
    "no_pet_selected": "未选择宠物",
    "name": "名字",
    "species": "种类",
    "xp": "经验",
    "hunger": "饥饿",
    "mood": "心情",
    "energy": "精力",
    "status": "状态",
    
    # Pet action messages
    "ate_snack": "{name} 开心地吃了起来！(+{amount} 饥饿)",
    "had_fun_playing": "{name} 欢快地玩耍！(+{amount} 心情, -10 精力)",
    "took_nap": "{name} 进入了梦乡！(+{amount} 精力, -5 饥饿)",
    "trained_hard": "{name} 刻苦训练！(-15 精力, -5 心情)",
    "enjoyed_cuddles": "{name} 享受你的抚摸！(+{amount} 心情)",
    
    # Level up
    "level_up": "升级了！{name} 现在是 {level} 级！",
    
    # Status messages
    "no_longer_with_us": "{name} 已经离开了我们...",
    "too_tired_to_train": "{name} 太累了，无法训练！",
    
    # Action messages
    "unknown_action": "未知操作：{action}",
    "unknown_species": "未知种类，默认使用 'blob'",
    "welcome_pet": "欢迎 {name} 这只 {species}！",
    "take_good_care": "好好照顾它吧！",
    "switched_to": "切换到 {name}",
    "theme_changed": "主题：{theme_name}",
    
    # Ticker messages
    "starved": "{name} 饿坏了...你应该喂它的！",
    "missed_you": "{name} 想念你！({hours} 小时过去了)",
    "hours_passed": "距离上次查看 {name} 已经过去了 {hours} 小时。",
    "getting_hungry": "{name} 饿了...",
    "seems_lonely": "{name} 看起来很孤单...",
    "well_rested": "{name} 休息得很好！",
    
    # Evolution
    "evolved": "{name} 进化了！{old} → {new}",
    
    # Rarity
    "rarity_label": "稀有度",
    "rarity_result": "稀有度：{rarity}",
    "shiny_congratulations": "哇！闪光宠物！你真是太幸运了！",
    "shiny_label": "✦ 闪光",
    
    # Breakthrough
    "phase_label": "阶段",
    "materials_label": "材料",
    "breakthrough_btn": "突破 [B]",
    "breakthrough_success": "{name} 突破成功！{old_phase} → {new_phase}！",
    "cannot_breakthrough": "{name} 暂时无法突破！（需要突破材料或更高等级）",
    "level_capped": "{name} 已达到等级上限（{level}级）！需要突破！",
    "no_materials": "无材料",
    
    # Travel
    "travel_btn": "旅行 [V]",
    "atlas_btn": "图鉴 [A]",
    "travel_label": "旅行",
    "atlas_label": "图鉴",
    "already_traveling": "{name} 正在旅行中！",
    "travel_started": "{name} 出发前往{stage_name} - {location}！(约{duration}分钟)",
    "travel_complete": "{name} 从{stage_name} - {location}归来！",
    "new_atlas_entry": "新图鉴记录：{location}！",
    "atlas_complete": "{stage_name}图鉴已集齐！必定获得突破材料！",
    "material_obtained": "获得突破材料：{material}！",
    "next_stage_unlocked": "新旅行阶段解锁：{stage_name}！",
    "polar_unlocked": "南北极探险已解锁！去探索极地吧！",
    "shiny_evolution_item_get": "不可思议！获得了闪光进化水晶！",
    "not_traveling": "未在旅行",
    "travel_returning": "正从{location}返回...",
    "traveling_to": "正在前往{location}（约{minutes}分钟）",
    "no_atlas_entries": "暂无图鉴记录",
    "shiny_items_label": "闪光水晶",
    
    # Language toggle
    "lang_switched": "语言：{lang}",
    "lang_en": "English",
    "lang_zh": "简体中文",
    
    # 疲劳状态
    "tired": "疲劳",
    "tired_label": "疲劳",
    "feeling_exhausted": "{name} 感到精疲力尽...",
    "too_exhausted": "{name} 太累了！",
    "exhausted": "精疲力尽",
    
    # 状态翻译
    "happy": "开心",
    "content": "满足",
    "neutral": "平静",
    "sad": "伤心",
    "critical": "危急",
    
    # 物种名称
    "species_blob": "史莱姆",
    "species_duck": "鸭子",
    "species_cat": "猫咪",
    "species_cactus": "仙人掌",
    "species_snail": "蜗牛",
    "species_rabbit": "兔子",
    "species_ghost": "幽灵",
    "species_goose": "大鹅",
    "species_owl": "猫头鹰",
    "species_mushroom": "蘑菇",
    "species_turtle": "海龟",
    "species_capybara": "水豚",
    "species_dragon": "龙",
    "species_penguin": "企鹅",
    "species_axolotl": "美西螈",
    "species_octopus": "章鱼",
    "species_robot": "机器人",
    "species_chonk": "胖兔",
    
    # 进化消息
    "evolved_message": "{name} 从 {old} 进化为 {new}！",
}

_LANGS = {
    "en": LANG_EN,
    "zh": LANG_ZH,
}


def get_text(key: str, lang: str = None, **kwargs) -> str:
    """Get localized text for a key.
    
    Args:
        key: The text key
        lang: Language code ('en' or 'zh'), defaults to current language
        **kwargs: Format arguments for the text
        
    Returns:
        Localized and formatted text
    """
    if lang is None:
        lang = _current_lang
    
    texts = _LANGS.get(lang, LANG_ZH)
    text = texts.get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text


def set_language(lang: str) -> None:
    """Set the current language.
    
    Args:
        lang: Language code ('en' or 'zh')
    """
    global _current_lang
    if lang in _LANGS:
        _current_lang = lang


def get_language() -> str:
    """Get the current language code."""
    return _current_lang


def toggle_language() -> str:
    """Toggle between 'en' and 'zh'.
    
    Returns:
        The new language code
    """
    global _current_lang
    _current_lang = "en" if _current_lang == "zh" else "zh"
    return _current_lang
