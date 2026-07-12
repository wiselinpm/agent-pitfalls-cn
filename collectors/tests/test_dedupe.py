"""测试 URL 指纹与标题相似度。"""

from __future__ import annotations

import pytest

from collectors.dedupe import is_likely_duplicate, title_similarity, url_fingerprint


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://example.com/a", "https://example.com/a"),
        ("https://Example.COM/a/", "https://example.com/a"),
        ("https://www.example.com/a", "https://example.com/a"),
        ("https://example.com/a?utm_source=x&id=1", "https://example.com/a?id=1"),
        ("http://example.com/a", "http://example.com/a"),
    ],
)
def test_url_fingerprint_normalization(url: str, expected: str) -> None:
    assert url_fingerprint(url) == expected


def test_url_fingerprint_query_order_independent() -> None:
    a = url_fingerprint("https://example.com/a?b=1&c=2")
    b = url_fingerprint("https://example.com/a?c=2&b=1")
    assert a == b


def test_title_similarity_identical() -> None:
    assert title_similarity("Hello World", "hello  world") == pytest.approx(1.0)


def test_title_similarity_low() -> None:
    assert title_similarity("Token overflow", "Sandbox escape") < 0.5


def test_is_likely_duplicate_url_match() -> None:
    assert is_likely_duplicate("https://x.com/a", "https://x.com/a/", "t", "t")


def test_is_likely_duplicate_title_match() -> None:
    assert is_likely_duplicate(
        "https://x.com/a",
        "https://y.com/b",
        "Context window silent truncation",
        "context window silent truncation",
    )


def test_is_not_duplicate() -> None:
    assert not is_likely_duplicate(
        "https://x.com/a",
        "https://y.com/b",
        "Token overflow",
        "Sandbox escape",
    )