"""合并 data/raw2 到 web/src/content/pitfalls。

按 URL fingerprint 去重，保留高质量 (critical/high + 有结构化抽取)。
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "web" / "src" / "content" / "pitfalls"


def _resolve_raw_dir(args) -> Path:
    if getattr(args, "in_dir", None):
        return Path(args.in_dir).resolve()
    return ROOT / "data" / "raw2"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LIST_URL_RE = re.compile(r"-\s+title:\s*[^\n]*\n\s+url:\s*(\S+)", re.MULTILINE)


def _parse_fm(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _fingerprint_from_file(path: Path, text: str) -> str:
    """从 file 内容里提取 URL，再调用 url_fingerprint。"""
    fm = _parse_fm(text)
    # 优先用 fingerprint 字段；否则从 references 列表抓 url
    fp = fm.get("fingerprint", "")
    if fp:
        return fp
    # 抓 references[0].url
    m = LIST_URL_RE.search(text[:2000])
    if m:
        url = m.group(1).strip()
        # 去掉可能的引号
        url = url.strip('"').strip("'")
        from collectors.dedupe import url_fingerprint

        return url_fingerprint(url)
    return ""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--quality", choices=["all", "high"], default="high",
                   help="all=全量, high=critical/high/有结构化抽取 (默认 high)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--in-dir", dest="in_dir", default=None,
                   help="输入 raw 目录（默认 data/raw2）")
    args = p.parse_args(argv)

    raw_dir = _resolve_raw_dir(args)
    if not raw_dir.exists():
        print(f"input dir not found: {raw_dir}")
        return 1

    # 已存在文件清单
    existing_fps: set[str] = set()
    existing_files = list(TARGET.glob("*.md"))
    for f in existing_files:
        try:
            text = f.read_text(encoding="utf-8")
            fp = _fingerprint_from_file(f, text)
            if fp:
                existing_fps.add(fp)
        except Exception:
            continue

    new_files = sorted(raw_dir.glob("*.md"))
    print(f"existing pitfalls: {len(existing_files)}  (fps={len(existing_fps)})")
    print(f"input dir: {raw_dir}  files: {len(new_files)}")

    added = 0
    skipped_dup = 0
    skipped_quality = 0
    skipped_err = 0
    by_source: dict[str, int] = {}

    for f in new_files:
        try:
            text = f.read_text(encoding="utf-8")
            fm = _parse_fm(text)
        except Exception:
            skipped_err += 1
            continue

        fp = _fingerprint_from_file(f, text)
        if not fp:
            skipped_err += 1
            continue
        if fp in existing_fps:
            skipped_dup += 1
            continue

        # 质量门槛
        if args.quality == "high":
            sev = (fm.get("severity") or "").lower()
            has_symptoms = bool(fm.get("symptoms"))
            has_fixes = bool(fm.get("fixes"))
            if sev not in ("critical", "high") and not (has_symptoms or has_fixes):
                skipped_quality += 1
                continue

        # 写入
        target_path = TARGET / f.name
        if not args.dry_run:
            shutil.copy2(f, target_path)
        added += 1
        by_source[fm.get("source", "unknown")] = by_source.get(fm.get("source", "unknown"), 0) + 1

    print()
    print(f"added:        {added}")
    print(f"skipped dup:  {skipped_dup}")
    print(f"skipped qual: {skipped_quality}")
    print(f"skipped err:  {skipped_err}")
    print()
    print("=== added by source ===")
    for s, c in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {c:3}  {s}")

    return 0


if __name__ == "__main__":
    sys.exit(main())