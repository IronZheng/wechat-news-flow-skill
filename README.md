<div align="center">

# wechat-news-flow-skill

**公众号新闻时事热点工作流 Skill** · A WeChat Official-Account News Workflow Skill

让 Agent 帮你运营新闻类公众号的两步流水线：找热点选题 → 给定命题出成稿。
*A two-step pipeline that lets your agent run a news-style WeChat Official Account: discover trending topics → draft a publish-ready article from any given subject.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/IronZheng/wechat-news-flow-skill?style=social)](https://github.com/IronZheng/wechat-news-flow-skill/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/IronZheng/wechat-news-flow-skill/pulls)
[![Platform](https://img.shields.io/badge/platform-WorkBuddy-blue)](https://www.workbuddy.cn)
[![Language](https://img.shields.io/badge/language-中文%20%7C%20English-orange)](./README.md)

**语言 / Language：** [中文](#中文) · [English](#english)

</div>

---

## 中文

### 这是什么

一个让 Agent 帮你运营**新闻类公众号**的 Skill。两条流水线，覆盖"找选题"到"出成稿"：

- **模式 A（没选题时）**：搜近 48 小时内的真实热点，聚合去重后给你 5–8 个可写的选题方向（事件 / 为什么热 / 建议角度 / 信源提示）。
- **模式 B（给了命题时）**：检索新闻出处与资料、下载对应新闻配图，产出一篇**内联样式、可直接复制粘贴进公众号编辑器**的 HTML 文章。

### ✨ 功能特性

- 🔥 **近 48h 热点聚合**：`WebSearch` 锁定 `freshness=d2`（近 48 小时），多路并行检索国内 + 国际维度，去重评级。
- 📝 **命题成稿**：自动检索权威来源（官媒 / 政府公告 / 主流财经科技媒体），关键事实标注信源。
- 🖼️ **配图下载**：内置纯标准库脚本，支持图片直链 + 文章 URL 自动提取头图（`og:image`），无需安装任何依赖。
- 🎨 **公众号兼容排版**：整篇 HTML 全部内联样式（公众号编辑器会剥离 `<style>` 与外链 CSS，内联样式才会保留）。
- ⚡ **一键安装**：提供 Windows / macOS / Linux 安装脚本，Agent 也能直接执行。

### 📦 安装

#### 方式一：脚本一键安装（推荐）

**Windows（PowerShell）：**

```powershell
powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/IronZheng/wechat-news-flow-skill/main/install.ps1 | iex"
```

**macOS / Linux：**

```bash
curl -fsSL https://raw.githubusercontent.com/IronZheng/wechat-news-flow-skill/main/install.sh | bash
```

#### 方式二：手动安装

把本仓库的以下四个部分复制到本地 skills 目录：

```
SKILL.md
scripts/download_news_images.py
references/writing-guide.md
assets/article-template.html
```

- **用户级**（所有项目可用）：`~/.workbuddy/skills/wechat-news-flow/`
- **项目级**（仅当前项目）：`<你的项目>/.workbuddy/skills/wechat-news-flow/`

复制完成后刷新 / 重启 Agent 即可生效。

#### 方式三：让 Agent 帮你装

直接对 Agent 说："安装 wechat-news-flow-skill"，让它执行上面的脚本即可（Agent 内部一键安装）。

### 🚀 使用

| 你想做 | 对 Agent 说 |
|-------|------------|
| 找热点选题 | 「帮我找点热点写」「最近有什么新闻可以写」「给我几个选题方向」 |
| 给定命题出稿 | 「写一篇关于 XX 的新闻稿」「整理 XX 事件的来龙去脉」 |

Agent 会按 `SKILL.md` 的流程自动跑完「搜资料 → 下配图 → 出成稿」。

### 📁 目录结构

```
wechat-news-flow/
├── SKILL.md                      # 技能主指令（两种模式 + 工作流）
├── scripts/
│   └── download_news_images.py   # 纯标准库配图下载（直链 / 文章自动提取头图）
├── references/
│   └── writing-guide.md          # 公众号写作与排版规范（结构 / 文风 / 内联样式）
├── assets/
│   └── article-template.html     # 内联样式排版骨架（可直接改）
├── install.ps1                   # Windows 一键安装脚本
├── install.sh                    # macOS / Linux 一键安装脚本
├── .gitignore
├── LICENSE
└── README.md
```

### 🔧 工作原理

#### 模式 A · 找选题（用户无方向）

1. 多路 `WebSearch`（`freshness=d2`）覆盖「今日要闻 / 热搜 / 财经 / 科技 / 国际」等维度。
2. 合并结果，剔除旧闻与重复，按**影响力 / 讨论度 / 成稿价值**排序。
3. 输出 5–8 个选题方向表格：事件、为什么热、建议切入角度、信源提示。
4. 你选一个编号，自动转入模式 B。

#### 模式 B · 出成稿（用户给命题）

1. **拆事实点**：把命题拆成需核实的维度（发生了什么 / 为什么重要 / 背景 / 各方反应 / 后续看点）。
2. **检索资料**：`WebSearch` 多角度 + `WebFetch` 打开权威页面，提取关键事实、数据、原话、时间线，并标注信源。
3. **下载配图**：运行 `download_news_images.py`，挑 2–4 张与事件强相关的图，自动校验、去重、命名。
4. **撰写文章**：按 `writing-guide.md` + `article-template.html`，生成全内联样式 HTML（标题 + 导语 + 2–4 小节 + 结语 + 信源）。
5. **交付**：`article.html`（可直接复制）+ `images/`（配图 + 清单）+ `sources.md`（信源与发布提示）。

### 💡 示例输出

**模式 A（选题方向节选）：**

| # | 热点事件 | 为什么热 | 建议切入角度 |
|---|---------|---------|------------|
| 1 | 中东局势升级，油价破 105 美元 | 持续发酵，牵动全球油价黄金 | 一图看懂冲突如何影响你的油价 |
| 2 | 复旦发布纯视觉机器人"端侧大脑" | 国产机器人 + AI 硬科技 | 机器人不再靠预设地图，意味着什么 |

**模式 B（成稿交付）：**

```
news-output/<日期>-<主题>/
├── article.html        # 内联样式，整段复制即可粘贴进公众号
├── images/             # news_01.jpg … + images_manifest.json
└── sources.md          # 信源清单 + 发布提示
```

### ⚠️ 注意事项

1. **图片发布**：公众号不能直接外链外部图。成稿里的图默认内嵌 base64（复制粘贴通常自动上传素材库）；若未带过，请先上传 `images/` 里的原图到素材库，再按 `images_manifest.json` 对应位置插入。
2. **二次核对**：关键数字（比分、排名、金额）发布前请再核一遍公开报道。
3. **信源与版权**：配图来自新华社、中国日报等，使用时保留图注署名；商用请自行确认授权。
4. **客观中立**：涉及国际冲突等议题，脚本与成稿只陈述事实与各方表态，不站队、不渲染。

### 📄 License

[MIT](./LICENSE) © IronZheng（白露）

---

## English

### What is this

A Skill that lets your Agent run a **news-style WeChat Official Account**. Two pipelines cover the full loop from "find a topic" to "ship the draft":

- **Mode A (no topic yet):** Searches real, trending news from the last 48 hours, de-duplicates and ranks it, then hands you 5–8 writable topic ideas (event / why it's hot / suggested angle / source hints).
- **Mode B (given a subject):** Researches the story's sources and materials, downloads the relevant news images, and produces a **fully inline-styled HTML article you can copy-paste straight into the WeChat editor**.

### ✨ Features

- 🔥 **48h trending aggregation:** `WebSearch` pinned to `freshness=d2` (last 48h), fanned out across domestic + international dimensions, then de-duplicated and ranked.
- 📝 **Draft from a subject:** Auto-researches authoritative sources (state media / government notices / major finance & tech outlets) and attributes every key fact to a source.
- 🖼️ **Image downloader:** A pure standard-library script that grabs images from direct URLs *or* auto-extracts the hero image (`og:image`) from an article URL — no third-party dependencies.
- 🎨 **WeChat-compatible layout:** The entire HTML uses inline styles only (the WeChat editor strips `<style>` and external CSS; inline styles survive).
- ⚡ **One-click install:** Ships Windows / macOS / Linux install scripts that an Agent can also run directly.

### 📦 Installation

#### Option 1: One-line script (recommended)

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/IronZheng/wechat-news-flow-skill/main/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -fsSL https://raw.githubusercontent.com/IronZheng/wechat-news-flow-skill/main/install.sh | bash
```

#### Option 2: Manual install

Copy these four parts from the repo into your local skills directory:

```
SKILL.md
scripts/download_news_images.py
references/writing-guide.md
assets/article-template.html
```

- **User scope** (all projects): `~/.workbuddy/skills/wechat-news-flow/`
- **Project scope** (current project only): `<your-project>/.workbuddy/skills/wechat-news-flow/`

Refresh / restart the Agent afterwards.

#### Option 3: Let the Agent install it

Just tell your Agent: "install wechat-news-flow-skill" and it will run the script above (true in-Agent one-click install).

### 🚀 Usage

| What you want | Say to the Agent |
|-------|------------|
| Find trending topics | "帮我找点热点写" / "find me some trending topics to write about" |
| Draft from a subject | "写一篇关于 XX 的新闻稿" / "write a news piece about XX" |

The Agent runs the `SKILL.md` flow end-to-end: research → download images → draft the article.

### 📁 Project Structure

```
wechat-news-flow/
├── SKILL.md                      # Skill instructions (two modes + workflow)
├── scripts/
│   └── download_news_images.py   # Stdlib-only image downloader (URLs / auto hero from article)
├── references/
│   └── writing-guide.md          # WeChat writing & layout guide (structure / tone / inline styles)
├── assets/
│   └── article-template.html     # Inline-styled layout skeleton (editable)
├── install.ps1                   # Windows one-click installer
├── install.sh                    # macOS / Linux one-click installer
├── .gitignore
├── LICENSE
└── README.md
```

### 🔧 How it works

#### Mode A · Find topics (no direction given)

1. Fan out `WebSearch` with `freshness=d2` across "top headlines / trending / finance / tech / world".
2. Merge results, drop stale news and duplicates, rank by **impact / discussion / draft value**.
3. Output a 5–8 row topic table: event, why it's hot, suggested angle, source hints.
4. You pick a number; it jumps straight to Mode B.

#### Mode B · Draft the article (subject given)

1. **Break down facts:** Split the subject into verifiable dimensions (what happened / why it matters / background / reactions / what's next).
2. **Research:** `WebSearch` from multiple angles + `WebFetch` authoritative pages to extract facts, figures, quotes, and timelines, attributing each to a source.
3. **Download images:** Run `download_news_images.py`, pick 2–4 strongly relevant images; auto-validated, de-duplicated, and renamed.
4. **Write:** Following `writing-guide.md` + `article-template.html`, generate fully inline-styled HTML (title + lead + 2–4 sections + closing + sources).
5. **Deliver:** `article.html` (copy-ready) + `images/` (pictures + manifest) + `sources.md` (sources & publishing notes).

### 💡 Example output

**Mode A (topic ideas, excerpt):**

| # | Trending event | Why it's hot | Suggested angle |
|---|---------|---------|------------|
| 1 | Middle-East escalation, oil above $105 | Ongoing, moves global oil & gold | One chart: how the conflict hits your fuel price |
| 2 | Fudan releases vision-only robot "edge brain" | Domestic robotics + AI hardware | What it means when robots stop relying on preset maps |

**Mode B (delivered draft):**

```
news-output/<date>-<topic>/
├── article.html        # inline-styled, copy the whole thing into WeChat
├── images/             # news_01.jpg … + images_manifest.json
└── sources.md          # source list + publishing notes
```

### ⚠️ Notes

1. **Images on publish:** WeChat can't hotlink external images. The draft embeds images as base64 by default (paste usually auto-uploads to the media library); if they don't carry over, upload the originals from `images/` to the media library first, then insert per `images_manifest.json`.
2. **Double-check:** Verify key figures (scores, rankings, amounts) against public reports before publishing.
3. **Sources & rights:** Images come from Xinhua, China Daily, etc. — keep the captions/attribution; confirm commercial-use licensing yourself.
4. **Neutral & factual:** On sensitive topics (e.g. international conflict), the script and drafts state facts and positions only — no taking sides, no hype.

### 📄 License

[MIT](./LICENSE) © IronZheng（白露）

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=IronZheng/wechat-news-flow-skill&type=Date)](https://star-history.com/#IronZheng/wechat-news-flow-skill&Date)

If this Skill helps you, please **Star ⭐** and share, and feel free to open Issues / PRs to improve it together.
