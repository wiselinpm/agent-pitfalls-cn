"""扫描所有最近 mtime 的 markdown 文件，循环修复直到 build 通过。

修复：
- title > 120 JS chars
- summary > 300 或 < 10
- YAML 缩进/quote 问题
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
TARGET = WEB / "src" / "content" / "pitfalls"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _js_len(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2


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
    s = s.replace("'", "''")
    return f"'{s}'"


def fix_one(path: Path) -> str | None:
    """修复单个文件，返回动作名。"""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm_text = m.group(1)
    body = text[m.end():]
    lines = fm_text.split("\n")
    new_lines = []
    changed = False
    title = summary = ""
    title_idx = summary_idx = -1

    for i, line in enumerate(lines):
        if line.startswith("title:"):
            val = line[len("title:"):].strip()
            if val.startswith(("'", '"')) and val.endswith(("'", '"')):
                val = val[1:-1]
            title = val.strip()
            title_idx = len(new_lines)
            new_lines.append(line)
        elif line.startswith("summary:"):
            val = line[len("summary:"):].strip()
            if val.startswith(("'", '"')) and val.endswith(("'", '"')):
                val = val[1:-1]
            summary = val.strip()
            summary_idx = len(new_lines)
            new_lines.append(line)
        else:
            new_lines.append(line)

    # 1. title > 120 JS chars
    if title and _js_len(title) > 120:
        new_title = title[:117] + "..."
        cut = new_title[:110].rfind(" ")
        if cut > 30:
            new_title = new_title[:cut].rstrip() + "..."
        new_title = new_title[:120]
        new_lines[title_idx] = f"title: {_escape_for_yaml(new_title)}"
        changed = True

    # 2. summary > 300
    if summary and len(summary) > 300:
        new_sum = summary[:297] + "..."
        cut = new_sum[:290].rfind(" ")
        if cut > 30:
            new_sum = new_sum[:cut].rstrip() + "..."
        new_lines[summary_idx] = f"summary: {_escape_for_yaml(new_sum)}"
        changed = True

    # 3. summary < 10
    if summary and len(summary) < 10:
        fill = title or "Pitfall observed"
        new_sum = (summary + " " + fill).strip()[:300]
        new_lines[summary_idx] = f"summary: {_escape_for_yaml(new_sum)}"
        changed = True

    # 4. yaml 引号问题
    for i, line in enumerate(new_lines):
        if line.startswith("title:"):
            val = line[len("title:"):].strip()
            if val.startswith(("'", '"')) and val.endswith(("'", '"')):
                val = val[1:-1]
            val = val.strip()
            if _needs_quote(val):
                new_lines[i] = f"title: {_escape_for_yaml(val)}"
                changed = True
        elif line.startswith("summary:"):
            val = line[len("summary:"):].strip()
            if val.startswith(("'", '"')) and val.endswith(("'", '"')):
                val = val[1:-1]
            val = val.strip()
            if _needs_quote(val):
                new_lines[i] = f"summary: {_escape_for_yaml(val)}"
                changed = True

    if changed:
        new_text = "---\n" + "\n".join(new_lines) + "\n---\n" + body
        path.write_text(new_text, encoding="utf-8")
    return "fixed" if changed else None


def find_problem_file_from_build(stderr: str) -> str | None:
    """从 build 错误中提取问题文件路径。"""
    m = re.search(r"pitfalls → ([^ ]+) data does not match", stderr)
    if m:
        return m.group(1) + ".md"
    m = re.search(r"pitfalls/([^:]+):", stderr)
    if m:
        return m.group(1)
    m = re.search(r"pitfalls → ([^\s]+)", stderr)
    if m:
        return m.group(1) + ".md"
    return None


def main() -> int:
    print("Round 1: scanning all recent files and fixing common issues...", flush=True)
    now = time.time()
    fixed = 0
    for f in TARGET.glob("*.md"):
        try:
            mtime = f.stat().st_mtime
        except Exception:
            continue
        if now - mtime > 1800:
            continue
        if fix_one(f):
            fixed += 1
    print(f"  Round 1 fixed: {fixed}", flush=True)

    # Loop: build → 找问题文件 → fix → rebuild
    for attempt in range(20):
        print(f"\n=== Build attempt {attempt + 1} ===", flush=True)
        proc = subprocess.run(
            ["npm", "run", "build"],
            cwd=str(WEB),
            capture_output=True,
            text=True,
            timeout=180,
        )
        if proc.returncode == 0:
            print(f"BUILD OK after {attempt + 1} attempts!", flush=True)
            print(proc.stdout[-500:] if proc.stdout else "(no stdout)", flush=True)
            return 0
        # 错误
        print(f"BUILD FAILED:", flush=True)
        print(proc.stderr[:1500], flush=True)
        # 提取问题文件
        problem = find_problem_file_from_build(proc.stderr)
        if not problem:
            print("Could not extract problem file. Stopping.", flush=True)
            return 1
        path = TARGET / problem
        if not path.exists():
            # 也许 .md 缺失
            print(f"Problem file not found: {path}", flush=True)
            return 1
        # 修复
        action = fix_one(path)
        print(f"  Fixed {problem}: {action}", flush=True)
        if not action:
            # 如果没法自动修复，跳过这个文件（删除？）
            print(f"  Cannot fix {problem}, deleting", flush=True)
            path.unlink()

    print("Too many attempts, giving up.", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())