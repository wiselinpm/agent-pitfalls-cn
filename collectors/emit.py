"""将 PitfallDraft 序列化为 Markdown 文件。"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .normalize import PitfallDraft


FRONTMATTER_ORDER = [
    "title",
    "summary",
    "severity",
    "platforms",
    "categories",
    "symptoms",
    "root_causes",
    "fixes",
    "references",
    "tags",
    "contributor",
    "discovered_at",
    "verified",
]


def _yaml_block(d: dict) -> str:
    # default_style="'" 风险：内嵌 ' 必须 '' 转义
    # 改用 default_flow_style=False + 不强制引号；safe_dump 在含特殊字符时会自动加引号
    return yaml.safe_dump(
        d, allow_unicode=True, sort_keys=False, width=10000, default_flow_style=False
    ).strip()


def render_markdown(draft: PitfallDraft) -> str:
    """渲染单条 PitfallDraft 为 Markdown 字符串。"""
    payload = {
        "title": _flatten(draft.title),
        "summary": _flatten(draft.summary),
        "severity": draft.severity,
        "platforms": list(draft.platforms),
        "categories": list(draft.categories),
        "symptoms": list(draft.symptoms),
        "root_causes": list(draft.root_causes),
        "fixes": list(draft.fixes),
        "references": [
            {**r, "title": _flatten(r.get("title", ""))} for r in draft.references
        ],
        "tags": list(draft.tags),
    }
    if draft.contributor:
        payload["contributor"] = draft.contributor
    if draft.discovered_at:
        payload["discovered_at"] = draft.discovered_at
    payload["verified"] = draft.verified

    # 保证顺序与字段集合正确
    ordered = {k: payload[k] for k in FRONTMATTER_ORDER if k in payload}

    body = [
        "---",
        _yaml_block(ordered),
        "---",
        "",
    ]
    for r in draft.references:
        title = r.get("title") or r.get("url")
        url = r.get("url")
        src = r.get("source") or ""
        body.append(f"- [{title}]({url}){(' — ' + src) if src else ''}")
    body.append("")
    body.append("## 摘要")
    body.append("")
    body.append(draft.summary or draft.title)
    body.append("")
    if draft.score:
        body.append(f"_来源热度：{draft.score}_")
        body.append("")
    return "\n".join(body)


def write_drafts(
    drafts: list[PitfallDraft],
    out_dir: str | Path,
    *,
    overwrite: bool = False,
) -> tuple[int, int]:
    """把 drafts 写入 out_dir，返回 (written, skipped) 数量。"""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written = 0
    skipped = 0
    for d in drafts:
        path = out / f"{_safe_filename(d.slug)}.md"
        if path.exists() and not overwrite:
            skipped += 1
            continue
        path.write_text(render_markdown(d), encoding="utf-8")
        written += 1
    return written, skipped


_SAFE_NAME_RE = re.compile(r"[^a-z0-9一-鿿\-]+")


def _safe_filename(slug: str) -> str:
    return _SAFE_NAME_RE.sub("-", slug).strip("-") or "untitled"


def _flatten(s: str) -> str:
    """把多行内容折叠为单行，去除多余空白。"""
    if not s:
        return s or ""
    return re.sub(r"\s+", " ", s).strip()