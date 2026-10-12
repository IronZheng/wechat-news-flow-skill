#!/usr/bin/env bash
# wechat-news-flow-skill · 一键安装脚本（macOS / Linux）
# 用法：curl -fsSL https://raw.githubusercontent.com/IronZheng/wechat-news-flow-skill/main/install.sh | bash
set -euo pipefail

REPO="IronZheng/wechat-news-flow-skill"
BRANCH="main"
BASE="https://raw.githubusercontent.com/${REPO}/${BRANCH}"

# 目标目录：用户级 skills
TARGET="${HOME}/.workbuddy/skills/wechat-news-flow"
mkdir -p "${TARGET}/scripts" "${TARGET}/references" "${TARGET}/assets"

FILES=(
  "SKILL.md"
  "scripts/download_news_images.py"
  "references/writing-guide.md"
  "assets/article-template.html"
)

echo "==> 安装 wechat-news-flow-skill -> ${TARGET}"
for f in "${FILES[@]}"; do
  echo "    -> ${f}"
  curl -fsSL "${BASE}/${f}" -o "${TARGET}/${f}"
done

echo "==> 完成。请刷新 / 重启你的 Agent 以激活该 Skill。"
