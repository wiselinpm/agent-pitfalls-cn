"""CLI 入口：调度所有 source -> normalize -> dedupe -> emit Markdown。"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

from .dedupe import is_likely_duplicate
from .emit import write_drafts
from .normalize import normalize
from .sources import all_collectors, safe_collect


_LOG = logging.getLogger("collectors.run_all")


# 强提示：标题/摘要里出现这些词，几乎一定是「坑」类讨论
PITFALL_KEYWORDS = (
    "bug", "issue", "broken", "fail", "fails", "failed", "failing",
    "crash", "hang", "leak", "leaks", "vulnerability", "vuln",
    "exploit", "injection", "jailbreak", "bypass",
    "deprecated", "deprecation", "migration", "migrate",
    "rate limit", "429", "500", "timeout", "oom", "memory leak",
    "infinite loop", "stuck", "retry", "throttle",
    "not working", "doesn't work", "doesn't support",
    "context window", "context length", "max tokens", "token limit",
    "tool_call", "tool use", "function calling",
    "warn", "warning", "fix", "fixes", "patch", "patched",
    "gotcha", "footgun", "trap", "caveat", "broken",
    "无法", "失败", "错误", "崩溃", "泄漏", "死循环",
    "坑", "避坑", "注意", "警告", "修复", "弃用", "过时",
    "上下文", "工具调用", "成本",
)


def _looks_like_pitfall(hit) -> bool:
    """粗筛：标题/摘要里出现强关键词则视为坑候选。"""
    haystack = " ".join((hit.title or "", hit.summary or "", hit.body or "")).lower()
    return any(kw.lower() in haystack for kw in PITFALL_KEYWORDS)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="运行所有 agent-pitfalls 采集器")
    p.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parents[1] / "web" / "src" / "content" / "pitfalls"),
        help="Markdown 输出目录",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="覆盖已存在的 Markdown（默认跳过）",
    )
    p.add_argument(
        "--no-filter",
        action="store_true",
        help="禁用 pitfall 关键词过滤（保留所有命中）",
    )
    p.add_argument(
        "--min-score",
        type=int,
        default=3,
        help="score 低于此值的命中会被丢弃（默认 3）；与关键词过滤取 OR",
    )
    p.add_argument("--verbose", "-v", action="store_true", help="debug 日志")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    drafts_by_fp: dict[str, object] = {}
    total_raw = 0
    total_kept = 0
    total_filtered = 0
    for coll in all_collectors():
        n = 0
        kept = 0
        for hit in safe_collect(coll):
            total_raw += 1
            n += 1
            if not args.no_filter:
                if not _looks_like_pitfall(hit) and hit.score < args.min_score:
                    total_filtered += 1
                    continue
            total_kept += 1
            kept += 1
            draft = normalize(hit)
            existing = drafts_by_fp.get(draft.fingerprint)
            if existing is None:
                drafts_by_fp[draft.fingerprint] = draft
                continue
            if draft.score > getattr(existing, "score", 0):
                drafts_by_fp[draft.fingerprint] = draft
        _LOG.info("source=%s hits=%d kept=%d", coll.name, n, kept)

    # 二轮：标题级去重（不同 URL 指向同一坑）
    final: list = []
    seen_titles: list = []
    for d in drafts_by_fp.values():
        dup = False
        for t in seen_titles:
            if is_likely_duplicate("x", "y", d.title, t):
                dup = True
                break
        if not dup:
            final.append(d)
            seen_titles.append(d.title)

    written, skipped = write_drafts(final, args.out, overwrite=args.overwrite)
    _LOG.info(
        "summary: raw=%d kept=%d filtered=%d unique=%d written=%d skipped=%d out=%s",
        total_raw,
        total_kept,
        total_filtered,
        len(final),
        written,
        skipped,
        args.out,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())