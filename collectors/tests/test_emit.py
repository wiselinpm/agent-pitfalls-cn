"""测试 emit 层。"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from collectors.base import RawHit
from collectors.emit import render_markdown, write_drafts
from collectors.normalize import normalize


def _draft():
    return normalize(
        RawHit(
            title="Sample Pitfall",
            url="https://example.com/x",
            source="test",
            summary="summary",
            body="body",
        )
    )


def _split_frontmatter(text: str) -> str:
    """提取 frontmatter 文本（不含前后 ---），允许前置 HTML 注释。"""
    import re

    # 跳过前导注释/空行
    cleaned = re.sub(r"^(?:<!--.*?-->\s*)+", "", text, flags=re.DOTALL).lstrip()
    if not cleaned.startswith("---"):
        raise AssertionError("missing leading ---")
    rest = cleaned[4:]
    m = re.search(r"\n---\s*(?:\n|$)", rest)
    if not m:
        raise AssertionError("missing closing ---")
    return rest[: m.start()]


def test_render_markdown_has_frontmatter(tmp_path: Path) -> None:
    md = render_markdown(_draft())
    # emit 可能带一个 HTML 注释行（自动生成标记），但 frontmatter 必含 ---
    assert "---" in md
    fm = yaml.safe_load(_split_frontmatter(md))
    assert fm["title"] == "Sample Pitfall"
    assert "references" in fm
    assert "verified" in fm


def test_write_drafts_skips_existing(tmp_path: Path) -> None:
    d1 = _draft()
    w, s = write_drafts([d1], tmp_path)
    assert w == 1 and s == 0
    w2, s2 = write_drafts([d1], tmp_path)
    assert w2 == 0 and s2 == 1


def test_write_drafts_overwrite(tmp_path: Path) -> None:
    d1 = _draft()
    write_drafts([d1], tmp_path)
    w, s = write_drafts([d1], tmp_path, overwrite=True)
    assert w == 1 and s == 0


def test_filename_safety(tmp_path: Path) -> None:
    d = normalize(
        RawHit(
            title="!!!",
            url="https://example.com/x",
            source="t",
            summary="s",
        )
    )
    write_drafts([d], tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].name.endswith(".md")
    assert files[0].name != ".md"