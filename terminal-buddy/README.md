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
| `Tab` | Switch pet | 切换宠物 |
| `N` | New pet | 创建新宠物 |
| `D` | Theme | 切换主题 |
| `Q` | Quit | 退出 |

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