"""修复 pitfall 文件里的无效 URL + 去重。

1. 把 `/a/...` 之类的 segmentfault 相对路径补全成绝对 URL
2. 移除 content 中重复 slug（保留最早写入的版本）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "web" / "src" / "pitfalls" if False else ROOT / "web" / "src" / "content" / "pitfalls"

# 域名 -> 前缀
DOMAIN_PREFIX = {
    "segmentfault": "https://segmentfault.com",
    "juejin": "https://juejin.cn",
    "zhihu": "https://www.zhihu.com",
    "csdn": "https://blog.csdn.net",
    "cnblogs": "https://www.cnblogs.com",
    "oschina": "https://www.oschina.net",
    "infoq-cn": "https://www.infoq.cn",
    "sspai": "https://sspai.com",
    "meituan": "https://tech.meituan.com",
    "jianshu": "https://www.jianshu.com",
}

URL_LINE_RE = re.compile(r"^(\s+)url:\s+(\"?)(/[^\"\s]+)\2\s*$", re.MULTILINE)


def _domain_for(file: Path) -> str | None:
    text = file.read_text(encoding="utf-8", errors="ignore")
    # 找 source: 字段
    m = re.search(r"^source:\s*([^\n]+)", text, re.MULTILINE)
    if not m:
        return None
    src = m.group(1).strip().strip("'\"")
    for key, prefix in DOMAIN_PREFIX.items():
        if key in src:
            return prefix
    return None


def fix_urls(path: Path) -> bool:
    """修复文件里的相对 URL，返回是否做了改动。"""
    prefix = _domain_for(path)
    if prefix is None:
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    new_text, n = URL_LINE_RE.subn(rf"\1url: \2{prefix}\3\2", text)
    if n > 0:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args(argv)

    files = sorted(TARGET.glob("*.md"))
    fixed: list[Path] = []
    for f in files:
        try:
            if fix_urls(f):
                fixed.append(f)
        except Exception as e:
            print(f"FAIL {f}: {e}")
    print(f"files with relative URL fixed: {len(fixed)}")

    # 去重 — 同样的 slug 多份
    seen: dict[str, Path] = {}
    dup_files: list[Path] = []
    for f in files:
        # slug = filename without .md
        slug = f.stem
        if slug in seen:
            dup_files.append(f)
            continue
        seen[slug] = f
    print(f"duplicate slug files (will be removed): {len(dup_files)}")
    if args.apply:
        for f in dup_files:
            try:
                f.unlink()
            except Exception:
                pass
        for f in fixed:
            print(f"  fixed: {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())