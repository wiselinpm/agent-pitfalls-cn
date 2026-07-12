"""Pitfall 索引：解析 ``web/src/content/pitfalls/*.md`` frontmatter，构造可检索结构。

输出 :class:`PitfallRecord` 列表 — 字段已脱壳、可直接喂给搜索引擎与 CLI 输出。
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable

import yaml

from . import __version__

_LOG = logging.getLogger("agent_pitfalls_cli.index")


# 仓库内默认 pitfalls 目录
DEFAULT_PITFALLS_GLOB = "web/src/content/pitfalls/*.md"


@dataclass(frozen=True)
class PitfallRecord:
    """单条 pitfall 的结构化表示。"""

    slug: str
    file: str
    title: str
    summary: str
    severity: str
    platforms: tuple[str, ...]
    categories: tuple[str, ...]
    symptoms: tuple[str, ...]
    root_causes: tuple[str, ...]
    fixes: tuple[str, ...]
    references: tuple[dict, ...]
    tags: tuple[str, ...]
    contributor: str | None
    discovered_at: str | None
    verified: bool

    # 索引字段（非原始 frontmatter）
    body: str = ""  # 完整 markdown body
    body_text: str = ""  # body 去掉 markdown 标记
    title_lower: str = ""
    summary_lower: str = ""
    all_tokens: str = ""  # 拼好用于 BM25 的全文

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """分离 YAML frontmatter 与 body。"""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, m.group(2)


def _md_to_text(body: str) -> str:
    """去掉 markdown 标记，留纯文本。"""
    if not body:
        return ""
    # 去代码块
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]+`", " ", body)
    # 去链接 [text](url) → text
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    # 去标题符号
    body = re.sub(r"^#{1,6}\s*", "", body, flags=re.MULTILINE)
    body = re.sub(r"[*_>~\-]+", " ", body)
    return re.sub(r"\s+", " ", body).strip()


def parse_pitfall(path: Path) -> PitfallRecord | None:
    """解析单条 pitfall 文件。"""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        _LOG.debug("read %s failed: %s", path, exc)
        return None
    meta, body = _split_frontmatter(text)
    if not meta:
        return None

    title = str(meta.get("title") or "").strip()
    if not title:
        return None
    summary = str(meta.get("summary") or "").strip()
    severity = str(meta.get("severity") or "medium").lower()

    def _tuple(v) -> tuple[str, ...]:
        if v is None:
            return ()
        if isinstance(v, (list, tuple)):
            return tuple(str(x) for x in v if x)
        return (str(v),)

    def _refs(v) -> tuple[dict, ...]:
        if not v:
            return ()
        if isinstance(v, dict):
            return (v,)
        if isinstance(v, list):
            return tuple(x for x in v if isinstance(x, dict))
        return ()

    slug = path.stem
    body_text = _md_to_text(body)
    all_tokens = " ".join(
        [
            title,
            summary,
            " ".join(_tuple(meta.get("symptoms"))),
            " ".join(_tuple(meta.get("root_causes"))),
            " ".join(_tuple(meta.get("fixes"))),
            body_text,
        ]
    ).lower()

    return PitfallRecord(
        slug=slug,
        file=str(path),
        title=title,
        summary=summary,
        severity=severity,
        platforms=_tuple(meta.get("platforms")),
        categories=_tuple(meta.get("categories")),
        symptoms=_tuple(meta.get("symptoms")),
        root_causes=_tuple(meta.get("root_causes")),
        fixes=_tuple(meta.get("fixes")),
        references=_refs(meta.get("references")),
        tags=_tuple(meta.get("tags")),
        contributor=meta.get("contributor"),
        discovered_at=str(meta.get("discovered_at") or "") or None,
        verified=bool(meta.get("verified")),
        body=body,
        body_text=body_text,
        title_lower=title.lower(),
        summary_lower=summary.lower(),
        all_tokens=all_tokens,
    )


def load_records(
    source: str | os.PathLike | None = None,
    *,
    glob_pattern: str = DEFAULT_PITFALLS_GLOB,
) -> list[PitfallRecord]:
    """从目录或 glob 加载所有 pitfall 记录。

    参数:
        source: 目录路径 / 单文件 / glob 字符串；为 None 时使用项目内默认路径
        glob_pattern: 当 source 是目录时使用的 glob
    """
    if source is None:
        # 项目根目录下的 web/src/content/pitfalls
        here = Path(__file__).resolve().parents[1]
        candidates = [
            here / "web" / "src" / "content" / "pitfalls",
        ]
        for c in candidates:
            if c.exists():
                files = sorted(c.glob("*.md"))
                break
        else:
            return []
    else:
        p = Path(source)
        if p.is_file():
            files = [p]
        elif p.is_dir():
            files = sorted(p.glob(glob_pattern.split("/")[-1] if "/" in glob_pattern else glob_pattern))
        elif any(ch in str(source) for ch in "*?["):
            files = sorted(Path(".").glob(str(source)))
        else:
            return []

    out: list[PitfallRecord] = []
    for f in files:
        rec = parse_pitfall(f)
        if rec:
            out.append(rec)
    return out


# —— 缓存（pickle/JSON），加速下次启动 ——

CACHE_VERSION = f"v1-{__version__}"


def cache_path(root: Path | None = None) -> Path:
    root = root or Path.home() / ".cache" / "agent-pitfalls"
    root.mkdir(parents=True, exist_ok=True)
    return root / f"index-{CACHE_VERSION}.json"


def save_cache(records: list[PitfallRecord], dest: Path | None = None) -> Path:
    dest = dest or cache_path()
    payload = {
        "version": CACHE_VERSION,
        "count": len(records),
        "records": [_serialize(r) for r in records],
    }
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=None), encoding="utf-8")
    return dest


def load_cache(path: Path | None = None) -> list[PitfallRecord] | None:
    p = path or cache_path()
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if data.get("version") != CACHE_VERSION:
        return None
    return [_deserialize(d) for d in data.get("records", [])]


def _serialize(r: PitfallRecord) -> dict:
    return {
        "slug": r.slug,
        "file": r.file,
        "title": r.title,
        "summary": r.summary,
        "severity": r.severity,
        "platforms": list(r.platforms),
        "categories": list(r.categories),
        "symptoms": list(r.symptoms),
        "root_causes": list(r.root_causes),
        "fixes": list(r.fixes),
        "references": list(r.references),
        "tags": list(r.tags),
        "contributor": r.contributor,
        "discovered_at": r.discovered_at,
        "verified": r.verified,
        "body": r.body,
        "body_text": r.body_text,
        "title_lower": r.title_lower,
        "summary_lower": r.summary_lower,
        "all_tokens": r.all_tokens,
    }


def _deserialize(d: dict) -> PitfallRecord:
    return PitfallRecord(
        slug=d["slug"],
        file=d["file"],
        title=d["title"],
        summary=d.get("summary", ""),
        severity=d.get("severity", "medium"),
        platforms=tuple(d.get("platforms", [])),
        categories=tuple(d.get("categories", [])),
        symptoms=tuple(d.get("symptoms", [])),
        root_causes=tuple(d.get("root_causes", [])),
        fixes=tuple(d.get("fixes", [])),
        references=tuple(d.get("references", [])),
        tags=tuple(d.get("tags", [])),
        contributor=d.get("contributor"),
        discovered_at=d.get("discovered_at"),
        verified=bool(d.get("verified")),
        body=d.get("body", ""),
        body_text=d.get("body_text", ""),
        title_lower=d.get("title_lower", ""),
        summary_lower=d.get("summary_lower", ""),
        all_tokens=d.get("all_tokens", ""),
    )


def fingerprint(records: Iterable[PitfallRecord]) -> str:
    """用 titles + files 计算指纹，用于缓存失效判断。"""
    h = hashlib.sha256()
    for r in records:
        h.update(r.slug.encode("utf-8"))
        h.update(b"|")
    return h.hexdigest()[:16]