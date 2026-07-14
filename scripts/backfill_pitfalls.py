"""Backfill symptoms / root_causes / fixes for existing pitfalls.

Strategy
========
1. Walk web/src/content/pitfalls/*.md
2. Parse frontmatter (simple regex; do NOT depend on PyYAML field order)
3. Detect: are symptoms, root_causes, fixes empty in frontmatter?
4. If yes: extract from body text using normalize._extract_body_structure()
5. If new data found: rewrite the markdown file with the new arrays inserted
   AFTER the closing `---` block, before existing body content.

Scope: only modifies pitfalls with empty arrays; never overwrites non-empty ones.

Usage
-----
    python scripts/backfill_pitfalls.py --dry-run    # show what would change
    python scripts/backfill_pitfalls.py --apply      # write back
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from collectors.normalize import _extract_body_structure  # type: ignore

PITFALLS_DIR = ROOT / "web" / "src" / "content" / "pitfalls"

# Frontmatter key → list-name for extraction
FIELDS = ("symptoms", "root_causes", "fixes")


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Return (frontmatter_str, body_str). None if file has no frontmatter."""
    if not text.startswith("---"):
        return None
    rest = text[3:]
    end = rest.find("\n---")
    if end == -1:
        return None
    fm = rest[:end].lstrip("\n")
    body = rest[end + 4:].lstrip("\n")
    return fm, body


def parse_list_field(fm: str, key: str) -> list[str]:
    """Parse a YAML-style list field from frontmatter. Tolerates both
    block (`- a\n- b`) and empty (`[]`/blank). Returns [] if not present.
    """
    lines = fm.splitlines()
    out: list[str] = []
    in_block = False
    for line in lines:
        if re.match(rf"^{key}\s*:", line):
            tail = line.split(":", 1)[1].strip()
            if tail in ("", "[]", "[ ]"):
                return []
            if tail.startswith("["):
                # inline list
                inside = tail.strip("[]").strip()
                if not inside:
                    return []
                return [s.strip().strip('"').strip("'") for s in inside.split(",")]
            in_block = True
            continue
        if in_block:
            stripped = line.strip()
            if not stripped:
                # blank line ends the block (uncommon but safe)
                return out
            if stripped.startswith("- "):
                item = stripped[2:].strip()
                # strip inline YAML quotes
                if (item.startswith('"') and item.endswith('"')) or (
                    item.startswith("'") and item.endswith("'")
                ):
                    item = item[1:-1]
                out.append(item)
            else:
                return out
    return out


def fm_field_is_empty(fm: str, key: str) -> bool:
    return len(parse_list_field(fm, key)) == 0


def render_list(items: list[str]) -> str:
    return "\n".join(f"  - {yaml_safe_str(s)}" for s in items)


def yaml_safe_str(s: str) -> str:
    """Quote a string for YAML frontmatter when it has colons/leading-hash/etc."""
    if not s:
        return '""'
    needs_quote = any((c in s) for c in ":#@&*!|>'\"%,") or s.startswith("- ") or s.lower() in {"yes", "no", "true", "false", "null"}
    if needs_quote:
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{esc}"'
    return s


def update_frontmatter(fm: str, additions: dict[str, list[str]]) -> str:
    """Insert list fields into frontmatter if not already present."""
    lines = fm.splitlines()
    new_lines = []
    keys_inserted = set()
    for line in lines:
        m = re.match(r"^([\w_-]+)\s*:", line)
        if m and m.group(1) in additions:
            new_lines.append(line)
            new_lines.append(render_list(additions[m.group(1)]))
            keys_inserted.add(m.group(1))
        else:
            new_lines.append(line)

    # Append any missing keys at the end of frontmatter
    missing = [k for k in additions if k not in keys_inserted]
    if missing:
        new_lines.append("")
        for k in missing:
            new_lines.append(f"{k}:")
            new_lines.append(render_list(additions[k]))

    return "\n".join(new_lines)


def process_file(fp: Path, apply: bool) -> tuple[bool, dict[str, list[str]]]:
    """Process a single markdown file.

    Returns (changed, new_fields).
    """
    text = fp.read_text(encoding="utf-8")
    parts = split_frontmatter(text)
    if parts is None:
        return False, {}
    fm, body = parts

    additions: dict[str, list[str]] = {}

    field_to_extract = {
        "symptoms": "symptoms",
        "root_causes": "root_causes",
        "fixes": "fixes",
    }
    needed = [k for k in FIELDS if fm_field_is_empty(fm, k)]
    if not needed:
        return False, {}

    sym, cause, fix = _extract_body_structure(body)
    if "symptoms" in needed and sym:
        additions["symptoms"] = list(sym)
    if "root_causes" in needed and cause:
        additions["root_causes"] = list(cause)
    if "fixes" in needed and fix:
        additions["fixes"] = list(fix)

    if not additions:
        return False, {}

    if apply:
        new_fm = update_frontmatter(fm, additions)
        new_text = f"---\n{new_fm}\n---{body if not body.startswith(chr(10)) else ''}"
        if not new_text.endswith("\n"):
            new_text += "\n"
        if new_text != text:
            fp.write_text(new_text, encoding="utf-8")
            return True, additions
        return False, additions

    return False, additions


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Backfill empty symptoms/root_causes/fixes in pitfall markdown")
    p.add_argument("--apply", action="store_true", help="write back changes (default: dry-run)")
    p.add_argument("--limit", type=int, default=0, help="cap files processed (0 = no cap)")
    args = p.parse_args(argv)

    files = sorted(PITFALLS_DIR.glob("*.md"))
    if args.limit:
        files = files[: args.limit]

    n_changed = 0
    n_fields_added = 0
    n_files_with_data = 0
    type_totals = {"symptoms": 0, "root_causes": 0, "fixes": 0}
    samples: list[tuple[str, dict]] = []

    for fp in files:
        changed, additions = process_file(fp, apply=False)
        if additions:
            n_files_with_data += 1
            n_fields_added += sum(len(v) for v in additions.values())
            for k, v in additions.items():
                type_totals[k] += len(v)
            if len(samples) < 5:
                samples.append((fp.name, additions))
            if args.apply:
                # re-process with apply=True to actually write
                process_file(fp, apply=True)
                n_changed += 1

    total = len(files)
    print(f"=== backfill {'APPLIED' if args.apply else 'DRY-RUN'} ===")
    print(f"  files scanned:    {total}")
    print(f"  with new data:    {n_files_with_data} ({n_files_with_data/total:.1%})")
    print(f"  items added:      {n_fields_added}")
    print(f"  by field:")
    for k, v in type_totals.items():
        print(f"    {k:14} {v}")
    print(f"  files written:    {n_changed}{'' if args.apply else ' (dry-run)'}")
    print()
    if samples:
        print("=== samples ===")
        for name, adds in samples[:3]:
            print(f"\n  {name[:80]}")
            for k, v in adds.items():
                v0 = v[0] if v else ""
                print(f"    {k}: {len(v)} items, e.g. '{v0[:80]}...'")

    return 0


if __name__ == "__main__":
    sys.exit(main())