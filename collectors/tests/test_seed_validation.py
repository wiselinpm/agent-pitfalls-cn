"""端到端校验：所有种子 pitfall 都符合 schema 必填要求。"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PITFALLS_DIR = ROOT / "web" / "src" / "content" / "pitfalls"

REQUIRED_FIELDS = ("title", "summary", "severity")
VALID_SEVERITY = {"critical", "high", "medium", "low"}


def _all_pitfall_paths() -> list[Path]:
    if not PITFALLS_DIR.exists():
        return []
    return sorted(PITFALLS_DIR.glob("*.md"))


@pytest.mark.skipif(not _all_pitfall_paths(), reason="no seed pitfalls yet")
def test_seed_count_at_least_ten() -> None:
    assert len(_all_pitfall_paths()) >= 10


def _split_frontmatter(text: str) -> str:
    import re

    if not text.startswith("---"):
        raise AssertionError("missing leading ---")
    rest = text[4:]
    m = re.search(r"\n---\s*(?:\n|$)", rest)
    if not m:
        raise AssertionError("missing closing ---")
    return rest[: m.start()]


@pytest.mark.skipif(not _all_pitfall_paths(), reason="no seed pitfalls yet")
def test_seed_required_fields() -> None:
    for path in _all_pitfall_paths():
        text = path.read_text(encoding="utf-8")
        fm = yaml.safe_load(_split_frontmatter(text))
        for f in REQUIRED_FIELDS:
            assert f in fm and fm[f], f"{path.name} missing {f}"
        assert fm["severity"] in VALID_SEVERITY, f"{path.name} bad severity"
        assert fm["title"] and 4 <= len(fm["title"]) <= 120, path
        assert fm["summary"] and 10 <= len(fm["summary"]) <= 300, path


@pytest.mark.skipif(not _all_pitfall_paths(), reason="no seed pitfalls yet")
def test_seed_has_at_least_one_reference() -> None:
    for path in _all_pitfall_paths():
        text = path.read_text(encoding="utf-8")
        fm = yaml.safe_load(_split_frontmatter(text))
        refs = fm.get("references") or []
        assert refs, f"{path.name} has no references"