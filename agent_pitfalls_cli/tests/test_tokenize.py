"""分词与同义词扩展测试。"""

from agent_pitfalls_cli.tokenize import (
    tokenize,
    expand_query,
    detect_platforms,
    detect_categories,
    detect_severity,
)


class TestTokenize:
    def test_chinese(self):
        tokens = tokenize("上下文 溢出")
        assert "上下文" in tokens
        assert "溢出" in tokens

    def test_chinese_compound(self):
        # 连续中文字符会作为一个 token
        tokens = tokenize("上下文溢出")
        assert any("上下文" in t for t in tokens)

    def test_english(self):
        tokens = tokenize("context window overflow")
        assert "context" in tokens
        assert "window" in tokens
        assert "overflow" in tokens

    def test_mixed(self):
        tokens = tokenize("claude code 上下文 问题")
        assert "claude" in tokens
        assert "code" in tokens
        assert "上下文" in tokens

    def test_empty(self):
        assert tokenize("") == []

    def test_numbers(self):
        tokens = tokenize("error 429 too many")
        assert "429" in tokens
        assert "too" in tokens
        assert "many" in tokens


class TestExpandQuery:
    def test_expands_synonyms(self):
        expanded = expand_query(["token"])
        assert "token" in expanded
        assert any("上下文" in t for t in expanded)

    def test_expands_platform(self):
        expanded = expand_query(["claude-code"])
        assert "claude code" in expanded
        assert "claudecode" in expanded

    def test_deduplication(self):
        expanded = expand_query(["token", "context"])
        # 无重复
        assert len(expanded) == len(set(expanded))


class TestDetectPlatforms:
    def test_claude_code(self):
        assert "claude-code" in detect_platforms("claude code context overflow")

    def test_langchain(self):
        assert "langchain" in detect_platforms("langchain token cost runaway")

    def test_openai_api(self):
        assert "openai-api" in detect_platforms("openai api 429 rate limit")

    def test_none(self):
        assert len(detect_platforms("random text")) == 0


class TestDetectCategories:
    def test_context_window(self):
        assert "context-window" in detect_categories("context window 上下文 overflow")

    def test_cost(self):
        assert "cost" in detect_categories("token cost 账单爆炸")

    def test_security(self):
        assert "security" in detect_categories("security vulnerability 漏洞")


class TestDetectSeverity:
    def test_critical(self):
        assert detect_severity("critical 严重 崩溃") == "critical"

    def test_high(self):
        assert detect_severity("high 故障 broken") == "high"

    def test_none(self):
        assert detect_severity("random") is None
