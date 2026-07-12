"""扫描所有最近 mtime 的 markdown 文件，修复 YAML frontmatter 问题：
- title 含未转义冒号 → 加引号
- title 含 `#` 或特殊字符 → 加引号
- summary 含特殊字符 → 加引号
- 多行 frontmatter 折叠
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "web" / "src" / "content" / "pitfalls"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _needs_quote(s: str) -> bool:
    if not s:
        return False
    if any(c in s for c in [":", "#", "[", "]", "{", "}", "&", "*", "|", ">", "<", "%", "@", "`", "\n"]):
        return True
    if s.startswith(("-", "?", " ", "\t")):
        return True
    if s.endswith(" "):
        return True
    return False


def _escape_for_yaml(s: str) -> str:
    """单引号包裹 + 内部 ' 转义为 ''"""
    s = s.replace("'", "''")
    return f"'{s}'"


def _fix_file(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = m.group(1)
    body = text[m.end():]
    lines = fm.split("\n")
    new_lines: list[str] = []
    changed = False

    # 检查 title 和 summary 行
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("title:"):
            val = line[len("title:"):].strip()
            # 去掉已有引号
            if val.startswith('"') or val.startswith("'"):
                val = val[1:]
                if val.endswith('"') or val.endswith("'"):
                    val = val[:-1]
            val = val.strip()
            if _needs_quote(val):
                # 折叠多行：如果下一行不以空格或不是新 key，继续读取直到遇空行/下一个key
                new_lines.append(f"title: {_escape_for_yaml(val)}")
                changed = True
                i += 1
                continue
            new_lines.append(line)
            i += 1
            continue
        elif line.startswith("summary:"):
            val = line[len("summary:"):].strip()
            if val.startswith('"') or val.startswith("'"):
                val = val[1:]
                if val.endswith('"') or val.endswith("'"):
                    val = val[:-1]
            val = val.strip()
            if _needs_quote(val):
                new_lines.append(f"summary: {_escape_for_yaml(val)}")
                changed = True
                i += 1
                continue
            new_lines.append(line)
            i += 1
            continue
        else:
            new_lines.append(line)
            i += 1

    if changed:
        new_text = "---\n" + "\n".join(new_lines) + "\n---\n" + body
        path.write_text(new_text, encoding="utf-8")
    return "fixed" if changed else None


def main() -> int:
    fixed = 0
    total = 0
    now = time.time()
    for f in TARGET.glob("*.md"):
        try:
            mtime = f.stat().st_mtime
        except Exception:
            continue
        if now - mtime > 1800:  # 仅修复最近 30 分钟修改的
            continue
        total += 1
        if _fix_file(f):
            fixed += 1
    print(f"scanned: {total}, fixed: {fixed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())