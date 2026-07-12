"""智能搜索引擎。

核心思路 — 多字段加权的简化 BM25：

- ``title`` 权重 4.0 — 标题是用户最常匹配的目标
- ``summary`` 权重 2.0 — 摘要点出主题
- ``symptoms`` 权重 3.0 — 用户报现象时常描述症状
- ``root_causes`` 权重 1.5 — 解释「为什么」
- ``fixes`` 权重 1.5 — 解决方案
- ``all_tokens`` 权重 1.0 — 兜底全文

排序项：

- BM25 分数
- 平台匹配加成（query 提到 claude-code / langchain 等时 +50%）
- 类别匹配加成（query 提到 上下文 / cost / memory 时 +30%）
- 严重度匹配加成（query 显式要 critical 时优先）
- 验证状态加成（verified=True 略加分）

返回 :class:`SearchHit` — 含 score、命中片段、来源详情。
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from .index import PitfallRecord
from .tokenize import (
    expand_query,
    detect_categories,
    detect_platforms,
    detect_severity,
    tokenize,
)


# 字段权重
FIELD_WEIGHTS = {
    "title": 4.0,
    "summary": 2.0,
    "symptoms": 3.0,
    "root_causes": 1.5,
    "fixes": 1.5,
    "all_tokens": 1.0,
}

PLATFORM_MATCH_BOOST = 1.5
CATEGORY_MATCH_BOOST = 1.3
SEVERITY_BOOST = {"critical": 1.4, "high": 1.2, "medium": 1.0, "low": 0.9}
VERIFIED_BOOST = 1.05
QUALITY_BOOST = 1.3  # 有 symptoms+fixes 的条目加分
DOMAIN_BOOST = 1.2   # 匹配 agent 开发领域的条目加分

# 领域相关性：title/summary 里出现这些词才算「agent 开发」相关
# 注意："agent" 单独出现会匹配到保险 agent 等无关内容，所以用组合词
DOMAIN_KEYWORDS = (
    "llm", "ai ", "ai-", "gpt", "claude", "openai", "anthropic",
    "langchain", "langgraph", "autogen", "crewai", "cursor", "aider",
    "prompt", "rag", "embedding", "vector", "tool call", "function calling",
    "context window", "token", "model", "inference", "fine-tun",
    "multi-agent", "ai agent", "agent loop", "agent sdk", "agent crash",
    "mcp", "sandbox", "jailbreak", "injection",
    "hallucination", "retry", "rate limit", "streaming",
    "api", "sdk", "openai", "deepseek", "gemini",
)


@dataclass(frozen=True)
class SearchHit:
    record: PitfallRecord
    score: float
    matched_fields: tuple[str, ...]
    snippet: str

    def to_dict(self, *, include_body: bool = False) -> dict:
        d = {
            "slug": self.record.slug,
            "title": self.record.title,
            "summary": self.record.summary,
            "severity": self.record.severity,
            "platforms": list(self.record.platforms),
            "categories": list(self.record.categories),
            "symptoms": list(self.record.symptoms),
            "root_causes": list(self.record.root_causes),
            "fixes": list(self.record.fixes),
            "references": list(self.record.references),
            "tags": list(self.record.tags),
            "discovered_at": self.record.discovered_at,
            "verified": self.record.verified,
            "score": round(self.score, 3),
            "matched_fields": list(self.matched_fields),
            "snippet": self.snippet,
        }
        if include_body:
            d["body"] = self.record.body
        return d


# —— 内部 BM25 实现 ——

class _BM25Index:
    """针对单字段的小型 BM25；多个字段各自算一次 BM25 后加权重。"""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.docs = docs
        self.dl = [len(d) for d in docs]
        self.avgdl = max(1.0, sum(self.dl) / max(1, len(self.docs)))
        # df: token -> doc count
        df: Counter[str] = Counter()
        for d in docs:
            for t in set(d):
                df[t] += 1
        self.df = df
        self.n = max(1, len(self.docs))

    def idf(self, term: str) -> float:
        n = self.df.get(term, 0)
        return math.log(1 + (self.n - n + 0.5) / (n + 0.5))

    def score(self, query: list[str]) -> list[float]:
        scores = [0.0] * len(self.docs)
        for q in query:
            idf = self.idf(q)
            for i, doc in enumerate(self.docs):
                tf = doc.count(q)
                if tf == 0:
                    continue
                num = tf * (self.k1 + 1)
                den = tf + self.k1 * (1 - self.b + self.b * self.dl[i] / self.avgdl)
                scores[i] += idf * (num / den)
        return scores


def _build_field_docs(records: list[PitfallRecord]) -> dict[str, _BM25Index]:
    fields = {
        "title": [tokenize(r.title) for r in records],
        "summary": [tokenize(r.summary) for r in records],
        "symptoms": [tokenize(" ".join(r.symptoms)) for r in records],
        "root_causes": [tokenize(" ".join(r.root_causes)) for r in records],
        "fixes": [tokenize(" ".join(r.fixes)) for r in records],
        "all_tokens": [tokenize(r.all_tokens) for r in records],
    }
    return {name: _BM25Index(docs) for name, docs in fields.items()}


# —— 搜索主接口 ——

@dataclass
class SearchResult:
    hits: list[SearchHit]
    query: str
    expanded_query: list[str]
    detected_platforms: tuple[str, ...]
    detected_categories: tuple[str, ...]
    total_records: int


def search(
    records: list[PitfallRecord],
    query: str,
    *,
    top_k: int = 5,
    platform: str | None = None,
    category: str | None = None,
    severity: str | None = None,
) -> SearchResult:
    """主入口 — 智能查询，返回排序后的 hits。"""
    if not records:
        return SearchResult([], query, [], (), (), 0)

    raw_tokens = tokenize(query)
    expanded = expand_query(raw_tokens)
    # 用扩展后的 token 计算 BM25 — 同义词能拉中相关坑
    bm25 = _build_field_docs(records)

    field_scores: dict[str, list[float]] = {}
    for name, idx in bm25.items():
        field_scores[name] = idx.score(expanded)

    n = len(records)
    final = [0.0] * n
    matched_fields_per_doc: list[set[str]] = [set() for _ in range(n)]
    for name, scores in field_scores.items():
        w = FIELD_WEIGHTS[name]
        for i, s in enumerate(scores):
            if s > 0:
                final[i] += s * w
                matched_fields_per_doc[i].add(name)

    # 元信息加成
    wanted_platforms = set()
    if platform:
        wanted_platforms.update(p.strip() for p in platform.split(",") if p.strip())
    wanted_platforms.update(detect_platforms(query))

    wanted_categories = set()
    if category:
        wanted_categories.update(c.strip() for c in category.split(",") if c.strip())
    wanted_categories.update(detect_categories(query))

    wanted_severity = (severity or detect_severity(query) or "").lower() or None

    for i, rec in enumerate(records):
        if wanted_platforms:
            if rec.platforms and any(p in wanted_platforms for p in rec.platforms):
                final[i] *= PLATFORM_MATCH_BOOST
            else:
                # 若 query 显式提到平台但该 pitfall 没有任何平台 → 轻微降权
                if any(p not in ("generic",) for p in wanted_platforms):
                    final[i] *= 0.6
        if wanted_categories and rec.categories:
            if any(c in wanted_categories for c in rec.categories):
                final[i] *= CATEGORY_MATCH_BOOST
        if wanted_severity:
            boost = SEVERITY_BOOST.get(wanted_severity)
            if boost:
                final[i] *= boost
        if rec.verified:
            final[i] *= VERIFIED_BOOST
        # 质量加成：有 symptoms+fixes 的条目更实用
        if rec.symptoms and rec.fixes:
            final[i] *= QUALITY_BOOST
        # 领域相关性：title/summary 包含 agent 开发关键词的条目优先
        title_summary = (rec.title + " " + rec.summary).lower()
        has_domain = any(kw in title_summary for kw in DOMAIN_KEYWORDS)
        if has_domain:
            final[i] *= DOMAIN_BOOST
        elif final[i] > 0 and not any(kw in title_summary for kw in DOMAIN_KEYWORDS):
            # 非领域相关的条目降权（避免 "死循环" 匹配到传销新闻）
            final[i] *= 0.5

    # 收集 hits
    indexed = list(zip(final, records, matched_fields_per_doc))
    indexed.sort(key=lambda x: x[0], reverse=True)
    hits: list[SearchHit] = []
    for score, rec, fields in indexed:
        if score <= 0:
            continue
        snippet = _build_snippet(rec, query)
        hits.append(SearchHit(record=rec, score=score, matched_fields=tuple(fields), snippet=snippet))
        if len(hits) >= top_k:
            break

    return SearchResult(
        hits=hits,
        query=query,
        expanded_query=expanded,
        detected_platforms=tuple(sorted(wanted_platforms)),
        detected_categories=tuple(sorted(wanted_categories)),
        total_records=n,
    )


def _build_snippet(rec: PitfallRecord, query: str) -> str:
    """从 symptoms/root_causes/fixes 中挑最匹配的一行作 snippet。"""
    query_lower = query.lower()
    candidates: list[str] = []
    candidates.extend(rec.symptoms)
    candidates.extend(rec.root_causes)
    candidates.extend(rec.fixes)
    if rec.summary:
        candidates.append(rec.summary)
    if not candidates:
        return rec.title

    scored: list[tuple[int, str]] = []
    for line in candidates:
        text = (line or "").strip()
        if not text:
            continue
        overlap = sum(1 for t in tokenize(query_lower) if t in text.lower())
        scored.append((overlap, text))
    scored.sort(key=lambda x: x[0], reverse=True)
    if scored and scored[0][0] > 0:
        return scored[0][1][:280]
    return candidates[0][:280]


# —— 项目「避坑体检」 ——

# 静态扫描规则：扫描代码就能识别潜在坑
SCAN_RULES: list[dict] = [
    {
        "id": "verbose-logging",
        "title": "verbose 日志可能泄漏密钥/PII",
        "match": re.compile(r"verbose\s*=\s*True|debug\s*=\s*True|LANGCHAIN_TRACING_V2|set_debug"),
        "platform_hint": ("langchain", "openai-agents", "generic"),
        "categories": ("observability", "security"),
    },
    {
        "id": "hardcoded-key",
        "title": "硬编码 API Key / Secret",
        "match": re.compile(r"(sk-[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z\-_]{20,})"),
        "platform_hint": ("generic", "claude-api", "openai-api", "gemini-api"),
        "categories": ("security",),
    },
    {
        "id": "no-max-iterations",
        "title": "agent 循环无 max_iterations 保护",
        "match": re.compile(r"AgentExecutor\(|create_react_agent|create_openai_functions_agent"),
        "platform_hint": ("langchain",),
        "categories": ("multi-agent", "cost", "reliability"),
        "anti_match": re.compile(r"max_iterations\s*=\s*\d+"),
    },
    {
        "id": "no-truncate-tool-result",
        "title": "工具返回值未做长度截断",
        "match": re.compile(r"return\s+response\.text|return\s+result\.stdout|return\s+output\s*$", re.MULTILINE),
        "platform_hint": ("generic", "langchain", "openai-agents"),
        "categories": ("context-window", "cost", "tool-use"),
    },
    {
        "id": "no-rate-limit-handler",
        "title": "未处理 429 限流 / 缺少 retry/backoff",
        # 仅匹配「真的在调 LLM API」的代码 — 关键字"anthropic"出现在列表/字符串里不命中
        "match": re.compile(
            r"openai\.chat\.completions\.create\s*\("
            r"|anthropic\.Anthropic\s*\("
            r"|Anthropic\s*\(\s*api_key"
            r"|messages\.create\s*\("
            r"|client\.messages\.create\s*\(",
        ),
        "platform_hint": ("claude-api", "openai-api"),
        "categories": ("reliability",),
        # 同文件 50 行内有 retry / backoff / RateLimitError 即视为已处理
        "anti_match_window": re.compile(
            r"RateLimitError|HTTPStatusError|tenacity|backoff|@retry|retry_after"
        ),
    },
    {
        "id": "ignore-usage-tokens",
        "title": "未读取 usage.input_tokens 做预警",
        "match": re.compile(
            r"openai\.chat\.completions\.create\s*\("
            r"|messages\.create\s*\("
            r"|anthropic\.Anthropic\s*\(",
        ),
        "platform_hint": ("claude-api", "openai-api"),
        "categories": ("context-window", "cost"),
        "anti_match_window": re.compile(r"usage\.input_tokens|usage\.prompt_tokens"),
    },
    {
        "id": "system-prompt-once",
        "title": "system prompt 仅在首轮设置（长会话会漂移）",
        "match": re.compile(r"system\s*=\s*[\"'].*?[\"']", re.DOTALL),
        "platform_hint": ("claude-api", "openai-api"),
        "categories": ("context-window", "reliability"),
        "anti_match": re.compile(r"def\s+\w+.*system"),
    },
    {
        "id": "no-streaming-timeout",
        "title": "流式调用无 timeout",
        "match": re.compile(r"stream\s*=\s*True|client\.messages\.stream"),
        "platform_hint": ("claude-api", "openai-api"),
        "categories": ("streaming", "reliability"),
        "anti_match": re.compile(r"timeout\s*="),
    },
]


@dataclass
class ScanIssue:
    rule_id: str
    title: str
    file: str
    line: int
    snippet: str
    matched_text: str
    platforms: tuple[str, ...]
    categories: tuple[str, ...]


def scan_project(
    project_dir: str | object,
    records: list[PitfallRecord],
    *,
    max_issues: int = 50,
    window: int = 1500,
) -> list[ScanIssue]:
    """扫描项目代码 — 找出已知模式 → 返回 ScanIssue。

    ``anti_match``: 整个文件命中即视为已处理，跳过该规则。
    ``anti_match_window``: 在匹配位置 ``± window`` 字符内命中即视为已处理。
    """
    from pathlib import Path

    root = Path(str(project_dir))
    if not root.exists():
        return []

    issues: list[ScanIssue] = []
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".astro", "vue", "web", "agent_pitfalls_cli"}
    target_exts = {".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb"}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.suffix.lower() not in target_exts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for rule in SCAN_RULES:
            anti_global = rule.get("anti_match")
            if anti_global and anti_global.search(text):
                continue
            anti_local = rule.get("anti_match_window")
            for m in rule["match"].finditer(text):
                if anti_local:
                    lo = max(0, m.start() - window)
                    hi = min(len(text), m.end() + window)
                    if anti_local.search(text[lo:hi]):
                        continue
                line_no = text.count("\n", 0, m.start()) + 1
                line_start = text.rfind("\n", 0, m.start()) + 1
                line_end = text.find("\n", m.end())
                if line_end < 0:
                    line_end = len(text)
                snippet = text[line_start:line_end].strip()[:240]
                issues.append(
                    ScanIssue(
                        rule_id=rule["id"],
                        title=rule["title"],
                        file=str(path),
                        line=line_no,
                        snippet=snippet,
                        matched_text=m.group(0)[:120],
                        platforms=tuple(rule["platform_hint"]),
                        categories=tuple(rule["categories"]),
                    )
                )
                if len(issues) >= max_issues:
                    return issues
    return issues


def find_related_pitfalls(issue: ScanIssue, records: list[PitfallRecord], top_k: int = 3) -> list[SearchHit]:
    """对每个 ScanIssue 在知识库里找相关 pitfall。"""
    pseudo_query = " ".join([issue.title] + list(issue.categories) + list(issue.platforms))
    result = search(records, pseudo_query, top_k=top_k)
    return result.hits