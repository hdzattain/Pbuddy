# terminal-buddy

> 在终端里养一只属于你的 ASCII 宠物 | Raise your ASCII pets in the terminal

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/terminal-buddy.svg)](https://badge.fury.io/py/terminal-buddy)

```
    ╭────────────────────────────╮
    │      Terminal Buddy        │
    │                            │
    │       へ   ╱|、            │
    │      (  ˘ 。7              │
    │       |、 ~ヽ               │
    │       じし_,)ノ            │
    │                            │
    │  Your ASCII pet companion  │
    ╰────────────────────────────╯
```

---

## What is this? / 这是什么？

**English:**

terminal-buddy is a virtual pet game that runs right in your terminal. Remember those Tamagotchi keychains from the 90s? This is that, but for hackers. Your pet gets hungry, happy, sleepy — and misses you even when you are away.

**中文：**

terminal-buddy 是一个终端虚拟宠物养成游戏。就像当年的电子宠物（拓麻歌子），但是跑在你的终端里。你的宠物会饿、会开心、会困，即使你不在也会想你。

---

## Features / 功能

| Feature | 功能 |
|---------|------|
| **18 Adorable Species** | 18 种可爱的 ASCII 宠物物种 |
| **Real-time Interaction** | 实时互动：喂食、玩耍、睡觉、训练、抚摸 |
| **Evolution System** | 进化系统：宠物升级后会进化为新物种 |
| **Offline Time Flow** | 离线时间流逝：即使关掉终端，宠物也在等你回来 |
| **5 Color Themes** | 5 种主题配色方案 |
| **Auto-save** | 自动保存：宠物数据安全持久化 |
| **Multi-pet Support** | 多宠物支持：同时养多只宠物 |
| **Rarity System** | 稀有度系统：1-5星概率等级 + 闪光宠物 |
| **Breakthrough System** | 进阶突破：5阶段突破进阶机制 |
| **Travel & Atlas** | 旅行图鉴：5大区域87个地点收集 |
| **Polar Exploration** | 南北极探险：解锁闪光进化道具 |
| **Fatigue System** | 疲劳系统：活动积累疲劳，休息恢复 |

---

## Installation / 安装

```bash
# From PyPI
pip install terminal-buddy

# Or install from source
pip install git+https://github.com/hdzattain/terminal-buddy.git
```

---

## Quick Start / 快速开始

```bash
terminal-buddy
```

**English:** Launch the app and create your first pet! Choose a name and species, and begin your journey as a digital pet parent.

**中文：** 首次启动会让你创建一只新宠物。选择名字和物种，开始你的养宠之旅！

---

## Controls / 操作

| Key | Action | 说明 |
|-----|--------|------|
| `F` | Feed | 喂食 |
| `P` | Play | 玩耍 |
| `S` | Sleep | 睡觉 |
| `T` | Train | 训练（获得经验值）|
| `E` | Pet | 抚摸 |
| `B` | Breakthrough | 突破 |
| `V` | Travel | 旅行 |
| `Tab` | Switch pet | 切换宠物 |
| `N` | New pet | 创建新宠物 |
| `D` | Theme | 切换主题 |
| `Q` | Quit | 退出 |

---

## Rarity System / 稀有度系统

**English:**

Every pet is assigned a rarity level at creation, calculated using a SHA256 hash of the system's MAC address, creation timestamp, and a hash salt.

**中文：**

每只宠物在创建时会被分配一个稀有度等级，基于系统 MAC 地址、创建时间和哈希盐的 SHA256 哈希值计算。

| Stars | Rarity / 稀有度 | Probability / 概率 | Color / 颜色 |
|-------|-----------------|-------------------|--------------|
| ★ | Common / 普通 | 60% | White / 白色 |
| ★★ | Uncommon / 精良 | 25% | Green / 绿色 |
| ★★★ | Rare / 稀有 | 10% | Blue / 蓝色 |
| ★★★★ | Epic / 史诗 | 4.9% | Purple / 紫色 |
| ★★★★★ | Legendary / 传说 | 0.1% | Orange / 橙色 |

**Shiny Pets / 闪光宠物：** Independent of rarity, every pet has a 1% chance of being Shiny, determined by a separate hash calculation.

独立于稀有度，每只宠物有 1% 概率成为闪光宠物，由独立的哈希计算决定。

---

## Breakthrough System / 进阶突破系统

**English:**

Pets advance through 5 breakthrough phases. Each phase spans 15 levels. Breakthrough requires consuming the corresponding phase material.

**中文：**

宠物可以通过 5 个进阶阶段突破。每个阶段跨越 15 个等级，突破需要消耗对应阶段的突破材料。

| Phase / 阶段 | Name | 名称 | Level Range / 等级范围 | Material / 材料 |
|-------------|------|------|----------------------|----------------|
| 1 | Novice | 初阶 | 1 - 15 | Basic Breakthrough Stone / 初级突破石 |
| 2 | Intermediate | 中阶 | 16 - 30 | Intermediate Breakthrough Stone / 中级突破石 |
| 3 | Advanced | 高阶 | 31 - 45 | Advanced Breakthrough Stone / 高级突破石 |
| 4 | Master | 超阶 | 46 - 60 | Master Breakthrough Stone / 特级突破石 |
| 5 | Ultimate | 极阶 | 61 - 75 | Ultimate Breakthrough Stone / 终极突破石 |

Press `B` to attempt breakthrough. 按 `B` 键尝试突破。

---

## Travel System / 旅行系统

**English:**

Send your pet on journeys across the world to collect atlas entries and breakthrough materials. Travel unlocks progressively through 5 stages.

**中文：**

派遣宠物进行世界旅行，收集图鉴条目和突破材料。旅行系统按 5 个阶段逐步解锁。

| Stage / 阶段 | Region / 区域 | Locations / 地点数 |
|-------------|--------------|-------------------|
| 1 | China / 中国 | 34 provinces / 34个省份 |
| 2 | Southeast Asia / 东南亚 | 11 countries / 11个国家 |
| 3 | Europe / 欧洲 | 20 countries / 20个国家 |
| 4 | Americas / 美洲 | 12 countries / 12个国家 |
| 5 | Africa / 非洲 | 10 countries / 10个国家 |

Material drop rules / 材料掉落规则：

- New location: 10% drop rate / 新地点：10% 掉落率
- Visited location: 1% drop rate / 已访问地点：1% 掉落率
- Complete all entries in a stage: guaranteed material / 集齐一个阶段全部图鉴：必得突破材料

Press `V` to start a journey. 按 `V` 键开始旅行。

---

## Polar Exploration / 南北极探险

**English:**

After completing all 5 travel stages, the Arctic and Antarctic regions unlock. Each polar expedition has a 0.1% chance of yielding a Shiny Evolution Item — a rare consumable that triggers a special shiny evolution.

**中文：**

完成全部 5 个旅行阶段后解锁南北极地图。每次极地探险有 0.1% 概率获得闪光进化道具——一种触发特殊闪光进化的稀有消耗品。

---

## Fatigue System / 疲劳系统

**English:**

Pets accumulate fatigue through activities. High fatigue affects performance and triggers an exhausted state.

**中文：**

宠物通过活动积累疲劳度。疲劳度过高会影响表现并触发精疲力尽状态。

| Activity / 活动 | Fatigue Change / 疲劳变化 |
|-----------------|---------------------------|
| Play / 玩耍 | +10 |
| Train / 训练 | +15 |
| Pet / 抚摸 | +3 |
| Sleep / 睡觉 | -20 |
| Idle (per hour) / 空闲（每小时） | -3 |

When fatigue reaches 80 or above, the pet enters an exhausted state and cannot train.

当疲劳度达到 80 及以上时，宠物进入精疲力尽状态，无法进行训练。

---

## Evolution / 进化

**English:** Your pet evolves as it levels up! Each starter species has two evolution stages.

**中文：** 你的宠物会随着等级提升而进化！每个初始物种都有两次进化机会。

| Starter / 初始 | Level 5 / Lv.5 | Level 15 / Lv.15 |
|---------------|----------------|------------------|
| blob | ghost | dragon |
| duck | goose | penguin |
| cat | owl | axolotl |
| cactus | mushroom | robot |
| snail | turtle | octopus |
| rabbit | capybara | chonk |

### Species Names / 物种名称

| English | 中文 | Type / 类型 |
|---------|------|-------------|
| Blob | 史莱姆 | Starter / 初始 |
| Duck | 鸭子 | Starter / 初始 |
| Cat | 猫咪 | Starter / 初始 |
| Cactus | 仙人掌 | Starter / 初始 |
| Snail | 蜗牛 | Starter / 初始 |
| Rabbit | 兔子 | Starter / 初始 |
| Ghost | 幽灵 | Evolution I / 一阶进化 |
| Goose | 大鹅 | Evolution I / 一阶进化 |
| Owl | 猫头鹰 | Evolution I / 一阶进化 |
| Mushroom | 蘑菇 | Evolution I / 一阶进化 |
| Turtle | 海龟 | Evolution I / 一阶进化 |
| Capybara | 水豚 | Evolution I / 一阶进化 |
| Dragon | 龙 | Evolution II / 二阶进化 |
| Penguin | 企鹅 | Evolution II / 二阶进化 |
| Axolotl | 美西螈 | Evolution II / 二阶进化 |
| Octopus | 章鱼 | Evolution II / 二阶进化 |
| Robot | 机器人 | Evolution II / 二阶进化 |
| Chonk | 胖兔 | Evolution II / 二阶进化 |

---

## Themes / 主题

**English:** Choose from 5 beautiful terminal color schemes. Press `D` while running to cycle through themes.

**中文：** 支持 5 种终端配色主题，按 `D` 键在运行时切换。

- **Default** — Clean and classic
- **Forest** — Nature vibes
- **Ocean** — Deep sea calm
- **Sunset** — Warm and cozy
- **Neon** — Cyberpunk energy

---

## Development / 开发

```bash
git clone https://github.com/hdzattain/terminal-buddy.git
cd terminal-buddy
pip install -e ".[dev]"
python -m pytest tests/ -v
```

---

## Pet Data / 宠物数据

**English:** Your pets are safely stored in:

**中文：** 宠物数据保存在：

```
~/.terminal-buddy/pets.json
```

---

## License

MIT License — see [LICENSE](LICENSE) file for details.

---

## Related / 相关项目

- [claude-buddy-reroll](https://github.com/hdzattain/claude-buddy-reroll) — Claude `/buddy` 宠物重刷工具

---

<div align="center">

**Made with care for terminal lovers everywhere**

*给所有终端爱好者的礼物*

</div>