# claude-buddy-reroll

> Claude /buddy 宠物多次抽取工具 — Python 净室重写版
> 
> Claude /buddy Pet Reroll Tool — Clean-room Python Rewrite

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/pypi-v0.1.0-green.svg)](https://pypi.org/project/claude-buddy-reroll/)

一个优雅的终端工具，用于探索和搜索 Claude /buddy 宠物系统。基于公开信息的净室重写实现。

An elegant terminal tool for exploring and searching the Claude /buddy pet system. Clean-room implementation based on publicly available information.

---

## ✨ Features / 功能特性

- 🎲 **确定性生成** — 从 userID 通过哈希算法确定性生成宠物
- 🔍 **暴力搜索** — 搜索满足条件的完美宠物（物种/稀有度/属性/Shiny）
- 🖼️ **物种图鉴** — 全部 18 种物种的精美 ASCII art 展示
- 📊 **概率统计** — 详细的稀有度概率与属性分析
- 🎨 **Rich 终端** — 彩色进度条、表格和卡片式输出

---

## 📦 Installation / 安装

```bash
# 从 PyPI 安装
pip install claude-buddy-reroll

# 或从 GitHub 安装最新版
pip install git+https://github.com/hdzattain/claude-buddy-reroll.git
```

---

## 🚀 Quick Start / 快速开始

### 查看你的宠物 / Check Your Buddy

```bash
buddy-reroll check <your-user-id>
```

### 搜索梦想宠物 / Search for Dream Buddy

```bash
# 搜索传说级龙族 Shiny 宠物
buddy-reroll search --species dragon --rarity legendary --shiny

# 搜索所有属性 >= 80 的宠物
buddy-reroll search --min-stats 80 --count 5

# 搜索戴皇冠的猫
buddy-reroll search --species cat --hat crown
```

### 浏览物种图鉴 / Browse Species Gallery

```bash
buddy-reroll gallery
```

### 查看概率统计 / View Statistics

```bash
buddy-reroll stats
```

---

## 🐾 Species Gallery / 物种图鉴

| Species | Description | 描述 |
|---------|-------------|------|
| **duck** | Classic water fowl | 经典水禽，嘎嘎叫 |
| **goose** | Honking guardian |  honking 守护者 |
| **blob** | Amorphous friend | 无定形软泥朋友 |
| **cat** | Feline companion | 猫咪伙伴 |
| **dragon** | Mythical fire breather | 神话喷火兽 |
| **octopus** | Eight-armed genius | 八臂天才 |
| **owl** | Wise night watcher | 智慧夜行者 |
| **penguin** | Antarctic wanderer | 南极漫游者 |
| **turtle** | Slow and steady | 稳重慢行 |
| **snail** | Shell-backed explorer | 背壳探险家 |
| **ghost** | Ethereal spirit | 空灵幽灵 |
| **axolotl** | Aquatic salamander | 水生美西螈 |
| **capybara** | Chill giant rodent | 淡定巨鼠 |
| **cactus** | Spiky desert plant | 带刺沙漠植物 |
| **robot** | Mechanical friend | 机械朋友 |
| **rabbit** | Hoppy companion | 跳跃伙伴 |
| **mushroom** | Fungal friend | 真菌朋友 |
| **chonk** | Absolute unit | 绝对单位 |

---

## 🔬 How It Works / 工作原理

Claude /buddy 系统通过 `hash(userID + SALT)` 确定性生成宠物属性。本工具是基于公开信息的 **净室重写**（clean-room rewrite），核心算法如下：

- **哈希算法**: FNV-1a 32-bit
- **随机数生成**: Mulberry32 PRNG
- **盐值**: `friend-2026-401`

### Rarity Probabilities / 稀有度概率

| Rarity | Probability | Stars |
|--------|-------------|-------|
| ★ Common | 60% | ★ |
| ★★ Uncommon | 25% | ★★ |
| ★★★ Rare | 10% | ★★★ |
| ★★★★ Epic | 4% | ★★★★ |
| ★★★★★ Legendary | 1% | ★★★★★ |

### Stats / 属性

| Stat | Description | 描述 |
|------|-------------|------|
| **DEBUGGING** | Problem-solving ability | 问题解决能力 |
| **PATIENCE** | Ability to wait calmly | 冷静等待能力 |
| **CHAOS** | Unpredictable energy level | 不可预测的能量 |
| **WISDOM** | Knowledge and insight | 知识与洞察力 |
| **SNARK** | Sarcastic wit level | 讽刺机智程度 |

---

## 📖 CLI Reference / 命令参考

```
buddy-reroll [command] [options]

Commands:
  search    Search for buddies matching criteria
            Options: --species, --rarity, --eye, --hat, --shiny, --min-stats, --max, --count
            
  check     Check what buddy a uid produces
            Usage: buddy-reroll check <uid>
            
  gallery   Display all species ASCII art
            Usage: buddy-reroll gallery
            
  stats     Show probability statistics
            Usage: buddy-reroll stats
```

---

## 🛠️ Development / 开发

```bash
# 克隆仓库
git clone https://github.com/hdzattain/claude-buddy-reroll.git
cd claude-buddy-reroll

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/ -v
```

---

## 📄 License / 许可证

MIT License — see [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer / 免责声明

This is an **independent clean-room rewrite** based on publicly available information. Not affiliated with, endorsed by, or connected to Anthropic. Claude and /buddy are trademarks of Anthropic, PBC.

本项目是基于公开信息的独立净室重写，与 Anthropic 无任何关联、认可或联系。Claude 和 /buddy 是 Anthropic, PBC 的商标。

---

<div align="center">

**Made with 💜 by hdzattain**

If you find this tool useful, please consider giving it a ⭐ on GitHub!

如果这个项目对你有帮助，欢迎点个 ⭐！

</div>
