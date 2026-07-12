"""快速采集 — 仅跑高 yield 且稳定的 collector，跳过已知慢/失败的。

输出到 --out 目录。
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from collectors.dedupe import is_likely_duplicate, url_fingerprint  # noqa: E402
from collectors.emit import write_drafts  # noqa: E402
from collectors.normalize import normalize  # noqa: E402
from collectors.sources import safe_collect  # noqa: E402


PITFALL_KW = (
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
    "gotcha", "footgun", "trap", "caveat",
    "无法", "失败", "错误", "崩溃", "泄漏", "死循环",
    "坑", "避坑", "注意", "警告", "修复", "弃用", "过时",
    "上下文", "工具调用", "成本",
)


def _looks_like_pitfall(hit) -> bool:
    text = " ".join((hit.title or "", hit.summary or "", hit.body or "")).lower()
    return any(kw.lower() in text for kw in PITFALL_KW)


# 高 yield + 稳定的 source 名单（按经验）
HIGH_YIELD = (
    "github-issues", "github-releases", "rss", "hackernews",
    "zhihu-v2", "juejin-v2", "reddit-v2",
    "medium", "devto", "stackoverflow",
    "arxiv", "arxiv-v2", "awesome-repos",
    "segmentfault", "infoq-cn", "cnblogs", "csdn",
    "oschina", "meituan", "sspai", "cloud-cn",
    "lobsters", "huggingface-papers", "producthunt",
    "official-status", "vendor-blogs", "newsletters",
    "frameworks", "tldr", "dev-community", "forums",
    "extra-en", "meta-search",
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(ROOT / "data" / "raw5"))
    p.add_argument("--sources", nargs="*", default=None,
                   help="指定运行的 source（默认 HIGH_YIELD）")
    p.add_argument("--no-filter", action="store_true")
    p.add_argument("--per-source-timeout", type=int, default=120,
                   help="单个 source 超时（秒）")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log = logging.getLogger("quick_collect")

    from collectors.sources import all_collectors
    wanted = set(args.sources or HIGH_YIELD)

    drafts_by_fp: dict[str, object] = {}
    total_raw = total_kept = total_filtered = 0
    t0 = time.time()

    for coll in all_collectors():
        if coll.name not in wanted:
            continue
        n = kept = 0
        source_start = time.time()
        try:
            for hit in safe_collect(coll):
                total_raw += 1
                n += 1
                if not args.no_filter:
                    if not _looks_like_pitfall(hit) and hit.score < 1:
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
        except Exception as e:
            log.warning("source %s exception: %s", coll.name, e)
        elapsed = time.time() - source_start
        log.info(
            "source=%-22s hits=%-5d kept=%-5d elapsed=%.1fs",
            coll.name, n, kept, elapsed,
        )

    final = []
    seen_titles: list[str] = []
    for d in drafts_by_fp.values():
        if any(is_likely_duplicate("x", "y", d.title, t) for t in seen_titles):
            continue
        final.append(d)
        seen_titles.append(d.title)

    written, skipped = write_drafts(final, args.out, overwrite=False)
    elapsed = time.time() - t0
    log.info(
        "summary: raw=%d kept=%d filtered=%d unique=%d written=%d skipped=%d elapsed=%.1fs out=%s",
        total_raw, total_kept, total_filtered,
        len(final), written, skipped, elapsed, args.out,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())