"""GitHub Issues 采集：扫描主流 agent 仓库的相关 issue。

受监控仓库清单见 WATCHED_REPOS。任何贡献者都可以在
`config/agents.yaml` 中追加仓库。
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get_json


WATCHED_REPOS = [
    ("anthropics", "claude-code"),
    ("openai", "openai-agents-python"),
    ("langchain-ai", "langchain"),
    ("langchain-ai", "langgraph"),
    ("microsoft", "autogen"),
    ("crewAIInc", "crewAI"),
    ("openinterpreter", "open-interpreter"),
    ("cursor", "cursor"),
    ("Aider-AI", "aider"),
    ("agno-agi", "agno"),
]


QUERIES = [
    "is:issue is:open label:bug",
    "is:issue is:closed label:bug",
]


def _search_issues(owner: str, repo: str, q: str) -> Iterable[dict]:
    url = "https://api.github.com/search/issues"
    params = {"q": f"repo:{owner}/{repo} {q}", "per_page": "20", "sort": "updated"}
    try:
        data = http_get_json(url, params=params)
    except Exception:
        return
    return data.get("items") or []


class GitHubIssuesCollector:
    name = "github-issues"

    def collect(self) -> Iterable[RawHit]:
        for owner, repo in WATCHED_REPOS:
            for q in QUERIES:
                for issue in _search_issues(owner, repo, q):
                    title = issue.get("title") or ""
                    url = issue.get("html_url") or ""
                    body = issue.get("body") or ""
                    summary = body[:280].replace("\r", " ")
                    reactions = issue.get("reactions") or {}
                    if not isinstance(reactions, dict):
                        reactions = {}
                    yield RawHit(
                        title=title,
                        url=url,
                        source=f"github:{owner}/{repo}",
                        summary=summary,
                        body=body,
                        author=(issue.get("user") or {}).get("login"),
                        published_at=_parse_dt(issue.get("created_at")),
                        score=int(issue.get("comments") or 0)
                        + int(reactions.get("total_count") or 0)
                        + int(issue.get("score") or 0),
                        tags=tuple(
                            label.get("name", "")
                            for label in (issue.get("labels") or [])
                            if isinstance(label, dict)
                        ),
                    )


def _parse_dt(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None