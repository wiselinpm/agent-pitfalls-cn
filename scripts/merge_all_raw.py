"""Merge all raw batches (data/raw, raw2, raw3, raw4, raw5, raw6, raw7) into
web/src/content/pitfalls/，按 URL fingerprint 去重 + 质量门槛。
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TARGET = ROOT / "web" / "src" / "content" / "pitfalls"

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


def _fp(path: Path, text: str) -> str:
    fm = _parse_fm(text)
    fp = fm.get("fingerprint", "")
    if fp:
        return fp
    m = LIST_URL_RE.search(text[:2000])
    if m:
        url = m.group(1).strip().strip('"').strip("'")
        from collectors.dedupe import url_fingerprint
        return url_fingerprint(url)
    return ""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--in-dirs", nargs="*",
        default=[
            "data/raw5", "data/raw6", "data/raw7",
            "data/raw4", "data/raw3", "data/raw2", "data/raw",
        ],
        help="输入 raw 目录列表（按优先级排）",
    )
    p.add_argument("--quality", choices=["all", "high", "medium"], default="medium")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    existing_fps: set[str] = set()
    existing_files = list(TARGET.glob("*.md"))
    for f in existing_files:
        try:
            text = f.read_text(encoding="utf-8")
            fp = _fp(f, text)
            if fp:
                existing_fps.add(fp)
        except Exception:
            continue

    added = skipped_dup = skipped_quality = skipped_err = 0
    by_source: dict[str, int] = {}

    for d in args.in_dirs:
        in_dir = (ROOT / d).resolve()
        if not in_dir.exists():
            print(f"skip (missing): {in_dir}")
            continue
        for f in sorted(in_dir.glob("*.md")):
            try:
                text = f.read_text(encoding="utf-8")
                fm = _parse_fm(text)
            except Exception:
                skipped_err += 1
                continue
            fp = _fp(f, text)
            if not fp:
                skipped_err += 1
                continue
            if fp in existing_fps:
                skipped_dup += 1
                continue
            sev = (fm.get("severity") or "").lower()
            has_symptoms = bool(fm.get("symptoms"))
            has_fixes = bool(fm.get("fixes"))
            if args.quality == "high":
                if sev not in ("critical", "high") and not (has_symptoms or has_fixes):
                    skipped_quality += 1
                    continue
            elif args.quality == "medium":
                if sev == "low" and not (has_symptoms or has_fixes):
                    skipped_quality += 1
                    continue
            if not args.dry_run:
                shutil.copy2(f, TARGET / f.name)
            added += 1
            existing_fps.add(fp)
            by_source[fm.get("source", "unknown")] = by_source.get(fm.get("source", "unknown"), 0) + 1

    print(f"\n=== MERGE ===")
    print(f"existing pitfalls before: {len(existing_files)}")
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