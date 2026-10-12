#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_news_images.py
=======================
为公众号新闻文章下载配图。仅依赖 Python 标准库，无需安装任何第三方包。

两种输入：
  1. 直接图片 URL（--urls）：直接下载。
  2. 新闻文章 URL（--articles）：自动从页面提取头图
     （og:image / twitter:image / 正文首图）后下载。

用法：
  python download_news_images.py --out ./images --urls https://x.com/a.jpg ...
  python download_news_images.py --out ./images --articles https://news.site/123.html --max 4

输出：
  - 图片保存到 --out 目录，命名为 news_01.jpg / news_02.png ...
  - 同时生成 images_manifest.json（原图 URL -> 本地路径映射）和下载报告。
"""

import argparse
import html.parser
import json
import os
import re
import sys
import urllib.parse
import urllib.request

# 浏览器 UA，降低被反爬拦截的概率
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# 图片文件魔数（用于校验下载到的是不是真图片）
MAGIC = {
    b"\xff\xd8\xff": "jpg",
    b"\x89PNG": "png",
    b"GIF8": "gif",
    b"RIFF": "webp",  # 需进一步确认含 WEBP
}

# 过滤明显不是新闻配图的链接（站标 / 头像 / 追踪像素等）
SKIP_HINTS = (
    "logo", "icon", "avatar", "spinner", "pixel", "tracking",
    "banner-ad", "qrcode", "qr_code", "advert", "1x1", "favicon",
)


def _clean_ext(url: str) -> str:
    """从 URL 路径猜测扩展名。"""
    path = urllib.parse.urlparse(url).path
    m = re.search(r"\.([a-zA-Z0-9]{2,4})(?:[?#]|$)", path)
    return m.group(1).lower() if m else ""


def _looks_like_image(url: str) -> bool:
    ext = _clean_ext(url)
    return ext in ("jpg", "jpeg", "png", "gif", "webp", "bmp", "svg")


def _sniff_ext(data: bytes) -> str:
    for magic, ext in MAGIC.items():
        if data.startswith(magic):
            if ext == "webp":
                return "webp" if b"WEBP" in data[:16] else "bin"
            return ext
    return "bin"


def _fetch_bytes(url: str, timeout: int, ua: str) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception as exc:  # noqa: BLE001
        print(f"  [警告] 下载失败 {url}: {exc}", file=sys.stderr)
        return None


def _fetch_text(url: str, timeout: int, ua: str) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="ignore")
    except Exception as exc:  # noqa: BLE001
        print(f"  [警告] 抓取页面失败 {url}: {exc}", file=sys.stderr)
        return None


class _ImageExtractor(html.parser.HTMLParser):
    """从 HTML 中提取候选图片 URL，优先 og/twitter 头图。"""

    def __init__(self, base_url: str):
        super().__init__()
        self.base = base_url
        self.og = None
        self.twitter = None
        self.imgs: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta":
            prop = (d.get("property") or d.get("name") or "").lower()
            content = d.get("content") or ""
            if not content:
                return
            if prop in ("og:image", "og:image:url", "og:image:secure_url"):
                self.og = content
            elif prop in ("twitter:image", "twitter:image:src"):
                self.twitter = content
        elif tag == "img":
            src = d.get("src") or d.get("data-src") or d.get("data-original") or ""
            if src:
                self.imgs.append(src)

    def candidates(self) -> list[str]:
        out: list[str] = []
        for raw in (self.og, self.twitter, *self.imgs):
            if not raw:
                continue
            url = urllib.parse.urljoin(self.base, raw.strip())
            if url in out:
                continue
            low = url.lower()
            if any(h in low for h in SKIP_HINTS):
                continue
            if _looks_like_image(url) or url.startswith("data:"):
                out.append(url)
        return out


def collect_from_article(url: str, max_n: int, timeout: int, ua: str) -> list[str]:
    html_text = _fetch_text(url, timeout, ua)
    if not html_text:
        return []
    ext = _ImageExtractor(url)
    ext.feed(html_text)
    return ext.candidates()[:max_n]


def download(url: str, out_dir: str, index: int, timeout: int, ua: str) -> str | None:
    data = _fetch_bytes(url, timeout, ua)
    if not data:
        return None
    ext = _sniff_ext(data)
    if ext == "bin":
        # 退回到按 URL 猜测
        ext = _clean_ext(url) or "jpg"
    filename = f"news_{index:02d}.{ext}"
    path = os.path.join(out_dir, filename)
    with open(path, "wb") as f:
        f.write(data)
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="下载新闻配图（标准库实现）")
    ap.add_argument("--out", default="./images", help="图片输出目录")
    ap.add_argument("--urls", nargs="*", default=[], help="直接图片 URL 列表")
    ap.add_argument("--articles", nargs="*", default=[], help="新闻文章 URL 列表（自动提取头图）")
    ap.add_argument("--max", type=int, default=6, help="每个文章最多提取的图片数")
    ap.add_argument("--timeout", type=int, default=15, help="单次请求超时（秒）")
    ap.add_argument("--ua", default=DEFAULT_UA, help="自定义 User-Agent")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # 汇总所有待下载的图片 URL
    queue: list[str] = list(args.urls)

    # 直接图片 URL 也可能带 data: 或相对路径，标准化
    for art in args.articles:
        print(f"[信息] 解析文章：{art}")
        queue.extend(collect_from_article(art, args.max, args.timeout, args.ua))

    # 去重并保持顺序
    seen, ordered = set(), []
    for u in queue:
        if u not in seen:
            seen.add(u)
            ordered.append(u)

    if not ordered:
        print("[错误] 没有可下载的图片 URL。", file=sys.stderr)
        return 1

    print(f"[信息] 共发现 {len(ordered)} 张候选图片，开始下载到 {args.out}")

    manifest: list[dict] = []
    for i, url in enumerate(ordered, start=1):
        path = download(url, args.out, i, args.timeout, args.ua)
        if path:
            manifest.append({"index": i, "source": url, "local": path})
            print(f"  ✔ news_{i:02d} <- {url}")
        else:
            print(f"  ✘ 失败 #{i} <- {url}")

    manifest_path = os.path.join(args.out, "images_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    ok = len(manifest)
    print(f"[完成] 成功 {ok}/{len(ordered)} 张。清单见 {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
