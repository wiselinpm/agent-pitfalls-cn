"""搜索算法测试。"""

from agent_pitfalls_cli.index import PitfallRecord
from agent_pitfalls_cli.search import search, SearchHit, SearchResult


def _make_record(**kwargs) -> PitfallRecord:
    defaults = dict(
        slug="test-slug",
        file="test.md",
        title="Default title",
        summary="Default summary",
        severity="medium",
        platforms=("generic",),
        categories=("reliability",),
        symptoms=("symptom A", "symptom B"),
        root_causes=("root cause X",),
        fixes=("fix Y",),
        references=(),
        tags=(),
        contributor=None,
        discovered_at=None,
        verified=False,
        body="",
        body_text="",
        title_lower="",
        summary_lower="",
        all_tokens="",
    )
    defaults.update(kwargs)
    return PitfallRecord(**defaults)


class TestSearch:
    def _records(self):
        return [
            _make_record(
                slug="context-overflow",
                title="Claude Code 上下文静默截断",
                summary="context window 溢出后静默丢弃早期消息",
                severity="critical",
                platforms=("claude-code", "claude-api"),
                categories=("context-window",),
                symptoms=("agent 忽略早期指令", "token 成本上升"),
                root_causes=("context window 硬上限",),
                fixes=("滚动摘要", "关键 prompt 每轮重发"),
                all_tokens="claude code context window 上下文 截断 overflow silent truncation",
            ),
            _make_record(
                slug="tool-call-empty",
                title="OpenAI tool call arguments 空字符串",
                summary="tool_calls 返回空字符串导致 JSON 解析崩溃",
                severity="high",
                platforms=("openai-api", "openai-agents"),
                categories=("tool-use", "reliability"),
                symptoms=("tool call 空参数", "JSON decode error"),
                root_causes=("模型偶发返回空 arguments",),
                fixes=("safe_parse_args 补全", "累计到 finish_reason"),
                all_tokens="openai tool call empty arguments json decode",
            ),
            _make_record(
                slug="prompt-injection",
                title="Prompt 注入 via tool result",
                summary="间接注入导致 agent 被恶意接管",
                severity="critical",
                platforms=("generic",),
                categories=("prompt-injection", "security"),
                symptoms=("agent 执行非预期指令", "输出违规内容"),
                root_causes=("tool result 含恶意 prompt",),
                fixes=("输入消毒", "权限隔离"),
                all_tokens="prompt injection jailbreak indirect injection tool poisoning",
            ),
        ]

    def test_basic_search(self):
        result = search(self._records(), "context overflow", top_k=3)
        assert isinstance(result, SearchResult)
        assert len(result.hits) >= 1
        assert result.hits[0].record.slug == "context-overflow"

    def test_platform_detection(self):
        result = search(self._records(), "claude code 上下文", top_k=3)
        assert "claude-code" in result.detected_platforms

    def test_category_detection(self):
        result = search(self._records(), "tool call 空参数", top_k=3)
        assert "tool-use" in result.detected_categories

    def test_top_k_limit(self):
        result = search(self._records(), "agent", top_k=1)
        assert len(result.hits) <= 1

    def test_empty_records(self):
        result = search([], "anything", top_k=5)
        assert result.hits == []
        assert result.total_records == 0

    def test_hit_has_snippet(self):
        result = search(self._records(), "context window", top_k=1)
        assert result.hits[0].snippet

    def test_hit_to_dict(self):
        result = search(self._records(), "context", top_k=1)
        d = result.hits[0].to_dict()
        assert "slug" in d
        assert "score" in d
        assert "snippet" in d
        assert "matched_fields" in d

    def test_no_match(self):
        result = search(self._records(), "xyzzy plugh", top_k=5)
        assert len(result.hits) == 0
