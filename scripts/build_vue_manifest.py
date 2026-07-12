"""生成 Vue 站点所需的 manifest。

读取 web/src/content/pitfalls/ 全部 markdown，输出 vue/src/data/manifest.json。
Vue 端通过 import 静态加载，构建时打入 bundle。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "web" / "src" / "content" / "pitfalls"
OUT = ROOT / "vue" / "src" / "data" / "manifest.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_fm(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out = {}
    cur_key = None
    cur_list = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        # 列表项 - item
        if line.lstrip().startswith("- "):
            item = line.lstrip()[2:].strip().strip('"').strip("'")
            if cur_list is not None:
                cur_list.append(item)
            continue
        # 缩进的 key: value (在列表项中)
        if line.startswith("  ") and ":" in line:
            k, _, v = line.strip().partition(":")
            if cur_list is not None and isinstance(cur_list[-1], dict):
                cur_list[-1][k.strip()] = v.strip().strip('"').strip("'")
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            # 简单判断：列表开头
            if v == "" or v.startswith("[") or v == "|":
                if v.startswith("["):
                    # inline list
                    items = re.findall(r"'([^']*)'|\"([^\"]*)\"|(\w+)", v)
                    out[k] = [a or b or c for a, b, c in items]
                else:
                    out[k] = []
                    cur_list = out[k]
                    cur_key = k
                continue
            out[k] = v.strip('"').strip("'")
            cur_list = None
            cur_key = None
    return out


def main() -> int:
    if not SRC.exists():
        print(f"source dir not found: {SRC}")
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for f in sorted(SRC.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_fm(text)
        body_match = FRONTMATTER_RE.search(text)
        body = text[body_match.end():].strip() if body_match else text

        # 解析症状/根因/修复（如果不在 frontmatter 中）
        for key in ("symptoms", "root_causes", "fixes"):
            if key not in fm or not fm[key]:
                fm[key] = []

        # 平台/分类为字符串格式转数组
        for key in ("platforms", "categories", "tags"):
            v = fm.get(key, [])
            if isinstance(v, str):
                v = [s.strip() for s in v.strip("[]").split(",") if s.strip()]
            fm[key] = v

        # references
        if not fm.get("references"):
            fm["references"] = []

        # 严重程度
        sev = fm.get("severity", "medium")
        if isinstance(sev, str):
            sev = sev.strip().strip('"').strip("'").lower()

        # discovered_at
        d = fm.get("discovered_at", "")
        if d and isinstance(d, str):
            d = d.strip().strip('"').strip("'")

        verified = str(fm.get("verified", "false")).lower() in ("true", "1", "yes")

        entries.append({
            "id": f.stem,
            "title": fm.get("title", f.stem)[:120],
            "summary": fm.get("summary", "")[:300],
            "severity": sev,
            "platforms": fm.get("platforms", ["generic"]),
            "categories": fm.get("categories", []),
            "symptoms": fm.get("symptoms", []),
            "root_causes": fm.get("root_causes", []),
            "fixes": fm.get("fixes", []),
            "references": fm.get("references", []),
            "tags": fm.get("tags", []),
            "contributor": fm.get("contributor", "匿名"),
            "discovered_at": d,
            "verified": verified,
            "body": body[:5000],  # 截断防止单条太大
        })

    print(f"parsed {len(entries)} pitfalls")
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=None, separators=(",", ":"))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())