"""分批采集 — 把 source 切成小批，每批独立运行，避免被 harness 杀掉。

用法：
  python -m scripts.batch_a   # 国际 source (GitHub/HN/RSS/devto/stackoverflow/...)
  python -m scripts.batch_b   # 国内 source (zhihu/juejin/csdn/segmentfault/...)
  python -m scripts.batch_c   # 元搜索/微信/Bing (更慢)
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from collectors.dedupe import is_likely_duplicate  # noqa: E402
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


BATCH_A_SOURCES = (
    "github-issues", "github-releases",
    "hackernews", "rss",
    "stackoverflow", "devto",
    "lobsters", "huggingface-papers",
    "producthunt", "official-status",
    "vendor-blogs", "newsletters",
    "frameworks", "tldr", "dev-community", "forums",
    "extra-en", "awesome-repos",
    "arxiv", "arxiv-v2",
    "medium",
    "google-news",
)

BATCH_B_SOURCES = (
    "zhihu", "zhihu-v2", "juejin", "juejin-v2",
    "segmentfault", "infoq-cn", "cnblogs",
    "csdn", "oschina", "meituan", "sspai",
    "cloud-cn", "sogou-wechat",
)

BATCH_C_SOURCES = (
    "reddit", "reddit-v2",
    "meta-search",
)


def run_batch(sources: tuple[str, ...], out_dir: str) -> dict:
    """Run a single batch. Returns metrics dict."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s quick_collect: %(message)s",
    )
    log = logging.getLogger("quick_collect")

    from collectors.sources import all_collectors
    wanted = set(sources)

    drafts_by_fp: dict[str, object] = {}
    total_raw = total_kept = total_filtered = 0
    t0 = time.time()

    for coll in all_collectors():
        if coll.name not in wanted:
            continue
        n = kept = 0
        ss = time.time()
        try:
            for hit in safe_collect(coll):
                total_raw += 1
                n += 1
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
        log.info(
            "source=%-22s hits=%-5d kept=%-5d elapsed=%.1fs",
            coll.name, n, kept, time.time() - ss,
        )

    final = []
    seen_titles: list[str] = []
    for d in drafts_by_fp.values():
        if any(is_likely_duplicate("x", "y", d.title, t) for t in seen_titles):
            continue
        final.append(d)
        seen_titles.append(d.title)

    written, skipped = write_drafts(final, out_dir, overwrite=False)
    return {
        "raw": total_raw, "kept": total_kept, "filtered": total_filtered,
        "unique": len(final), "written": written, "skipped": skipped,
        "elapsed": time.time() - t0,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--batch", choices=["a", "b", "c"], required=True)
    args = p.parse_args(argv)

    sources = {
        "a": BATCH_A_SOURCES,
        "b": BATCH_B_SOURCES,
        "c": BATCH_C_SOURCES,
    }[args.batch]

    log = logging.getLogger("quick_collect")
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s")
    log.info("running batch %s: %d sources -> %s", args.batch, len(sources), args.out)
    metrics = run_batch(sources, args.out)
    log.info(
        "batch %s done: raw=%d kept=%d filtered=%d unique=%d written=%d skipped=%d elapsed=%.1fs",
        args.batch, metrics["raw"], metrics["kept"], metrics["filtered"],
        metrics["unique"], metrics["written"], metrics["skipped"],
        metrics["elapsed"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())