# wechat-news-flow-skill · 一键安装脚本（Windows PowerShell）
# 用法：powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/IronZheng/wechat-news-flow-skill/main/install.ps1 | iex"

$ErrorActionPreference = "Stop"

$Repo   = "IronZheng/wechat-news-flow-skill"
$Branch = "main"
$Base   = "https://raw.githubusercontent.com/$Repo/$Branch"

# 目标目录：用户级 skills（Windows 路径）
$Target = Join-Path $env:USERPROFILE ".workbuddy\skills\wechat-news-flow"
New-Item -ItemType Directory -Force -Path (Join-Path $Target "scripts"),
  (Join-Path $Target "references"),
  (Join-Path $Target "assets") | Out-Null

$Files = @(
  "SKILL.md",
  "scripts/download_news_images.py",
  "references/writing-guide.md",
  "assets/article-template.html"
)

Write-Host "==> 安装 wechat-news-flow-skill -> $Target"
foreach ($f in $Files) {
  Write-Host "    -> $f"
  Invoke-WebRequest -Uri "$Base/$f" -OutFile (Join-Path $Target $f) -UseBasicParsing
}

Write-Host "==> 完成。请刷新 / 重启你的 Agent 以激活该 Skill。"
