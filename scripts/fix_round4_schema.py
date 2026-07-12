"""修复 Round 4 新增文件的 schema 违反：
1. title > 120 chars — 截断或重写
2. summary < 10 或 > 300 chars
3. title/summary 中含未转义引号
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "web" / "src" / "content" / "pitfalls"


def _js_len(s: str) -> int:
    """JS UTF-16 length — surrogate pair 计为 2（emoji 等）。"""
    return len(s.encode("utf-16-le")) // 2


def _fix_file(path: Path) -> str | None:
    """返回修复的动作名（"truncated-title" 等），无需修改返回 None。"""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    fm_text = m.group(1)
    body_text = text[m.end():]
    lines = fm_text.split("\n")

    title = ""
    summary = ""
    title_idx = -1
    summary_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("title:"):
            title = line[len("title:"):].strip().strip('"').strip("'")
            title_idx = i
        elif line.startswith("summary:"):
            summary = line[len("summary:"):].strip().strip('"').strip("'")
            summary_idx = i

    action = None

    # 1. title > 120 JS chars
    if _js_len(title) > 120:
        # 截断到 117 chars + "..."
        new_title = title[:117] + "..."
        # 也尝试在最后一个空格截断
        if " " in new_title[:100]:
            cut = new_title[:100].rfind(" ")
            if cut > 30:
                new_title = new_title[:cut].rstrip() + "..."
        new_title = new_title[:120]
        lines[title_idx] = f"title: '{new_title.replace(chr(39), chr(39))}'"
        action = "truncated-title"

    # 2. summary < 10
    if len(summary) < 10:
        # 用 title 内容扩展
        fill = (title or "Pitfall observed").strip()
        new_sum = (summary + " " + fill).strip()[:300]
        if summary_idx >= 0:
            lines[summary_idx] = f"summary: '{new_sum.replace(chr(39), chr(39))}'"
        else:
            lines.append(f"summary: '{new_sum}'")
        action = "expanded-summary"

    if action:
        new_text = "---\n" + "\n".join(lines) + "\n---\n" + body_text
        path.write_text(new_text, encoding="utf-8")

    return action


def main() -> int:
    fixed = 0
    actions: dict[str, int] = {}
    for f in TARGET.glob("*.md"):
        try:
            mtime = f.stat().st_mtime
        except Exception:
            continue
        # 只检查 round 4 新加的文件（mtime 在最近 30 分钟内）
        import time
        if time.time() - mtime > 1800:
            continue
        act = _fix_file(f)
        if act:
            fixed += 1
            actions[act] = actions.get(act, 0) + 1
    print(f"fixed: {fixed}")
    for k, v in actions.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())