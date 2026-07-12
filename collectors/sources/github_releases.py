"""GitHub Releases API 采集 — 跟踪 agent 工具的版本更新 / Breaking Change。

相比 RSS feed，releases API 更稳定，且带完整的 release notes（通常会写
breaking changes、迁移指南、bug fix），对 pitfall 库特别有价值。
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get_json


WATCHED_REPOS = [
    # 主流 agent 框架
    ("langchain-ai", "langchain"),
    ("langchain-ai", "langgraph"),
    ("openai", "openai-agents-python"),
    ("openai", "openai-python"),
    ("anthropics", "claude-code"),
    ("anthropics", "anthropic-sdk-python"),
    ("anthropics", "anthropic-sdk-typescript"),
    ("microsoft", "autogen"),
    ("crewAIInc", "crewAI"),
    ("openinterpreter", "open-interpreter"),
    ("Aider-AI", "aider"),
    ("agno-agi", "agno"),
    ("run-llama", "llama_index"),
    ("chatchat-space", "langchain4j"),
    ("steven-tey", "novel"),
    ("vercel", "ai"),
    ("vercel", "ai-chatbot"),
    ("supabase", "ai"),
    # 编辑器/IDE 集成
    ("cursor", "cursor"),
    ("cline", "cline"),
    ("continuedev", "continue"),
    ("aws-samples", "q-cli"),
    # 评测/安全
    ("anthropics", "claude-cookbooks"),
    ("openai", "evals"),
    ("openai", "TikToken"),
]


class GitHubReleasesCollector:
    name = "github-releases"

    def collect(self) -> Iterable[RawHit]:
        for owner, repo in WATCHED_REPOS:
            for rel in _fetch(owner, repo):
                yield rel


def _fetch(owner: str, repo: str) -> Iterable[RawHit]:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    try:
        items = http_get_json(url, params={"per_page": 10}) or []
    except Exception:
        return
    if not isinstance(items, list):
        return
    for rel in items:
        title = rel.get("name") or rel.get("tag_name") or ""
        url_out = rel.get("html_url") or ""
        body = rel.get("body") or ""
        published = rel.get("published_at")
        dt: datetime | None = None
        if published:
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            except ValueError:
                dt = None
        # 评分：breaking change / security / deprecation 关键词加分
        score = 0
        body_lower = body.lower()
        for kw in ("breaking", "deprecat", "security", "cve", "vulnerability"):
            if kw in body_lower:
                score += 3
        if not (title and url_out):
            continue
        yield RawHit(
            title=f"[{owner}/{repo}] {title}",
            url=url_out,
            source=f"github-releases:{owner}/{repo}",
            summary=body[:280].replace("\r", " "),
            body=body,
            author=(rel.get("author") or {}).get("login"),
            published_at=dt,
            score=score,
            tags=("release", f"repo:{owner}/{repo}"),
        )