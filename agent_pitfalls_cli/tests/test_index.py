"""索引构建测试。"""

from pathlib import Path

from agent_pitfalls_cli.index import (
    load_records,
    save_cache,
    load_cache,
    cache_path,
    parse_pitfall,
    _split_frontmatter,
)

PITFALLS_DIR = Path(__file__).resolve().parents[2] / "web" / "src" / "content" / "pitfalls"


class TestSplitFrontmatter:
    def test_normal(self):
        meta, body = _split_frontmatter("---\ntitle: Test\n---\nBody here")
        assert meta["title"] == "Test"
        assert body == "Body here"

    def test_no_frontmatter(self):
        meta, body = _split_frontmatter("Just body text")
        assert meta == {}
        assert body == "Just body text"

    def test_empty(self):
        meta, body = _split_frontmatter("")
        assert meta == {}
        assert body == ""


class TestParsePitfall:
    def test_known_file(self):
        f = PITFALLS_DIR / "openai-tool-call-empty-arguments.md"
        if not f.exists():
            return
        rec = parse_pitfall(f)
        assert rec is not None
        assert rec.slug
        assert rec.title
        assert rec.severity in ("critical", "high", "medium", "low")
        assert len(rec.platforms) > 0

    def test_nonexistent(self):
        rec = parse_pitfall(Path("/nonexistent/file.md"))
        assert rec is None


class TestLoadRecords:
    def test_loads_from_default(self):
        records = load_records()
        assert len(records) > 0
        assert all(r.title for r in records)

    def test_loads_from_dir(self):
        records = load_records(str(PITFALLS_DIR))
        assert len(records) > 0

    def test_loads_single_file(self):
        f = PITFALLS_DIR / "openai-tool-call-empty-arguments.md"
        if not f.exists():
            return
        records = load_records(str(f))
        assert len(records) == 1
        assert "openai" in records[0].title.lower()


class TestCache:
    def test_roundtrip(self, tmp_path):
        records = load_records()
        if not records:
            return
        cp = tmp_path / "test-cache.json"
        save_cache(records, cp)
        loaded = load_cache(cp)
        assert loaded is not None
        assert len(loaded) == len(records)
        assert loaded[0].title == records[0].title

    def test_invalid_version(self, tmp_path):
        cp = tmp_path / "bad-cache.json"
        cp.write_text('{"version": "v1-99.99.99", "records": []}')
        loaded = load_cache(cp)
        assert loaded is None
