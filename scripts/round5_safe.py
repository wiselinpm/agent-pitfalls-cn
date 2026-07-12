"""Round 5 — 单进程快速版（限制每 source 最多 50 hits，避免 harness 杀掉）。

输出到 data/raw_round5/
"""
from __future__ import annotations
import sys, time, signal
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


# Round 5 源 + 单源 max_hits
SOURCES = [
    ("acl-anthology", 50),
]


class _TimeoutError(Exception):
    pass


def _alarm_handler(signum, frame):
    raise _TimeoutError()


def main() -> int:
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    log = logging.getLogger("round5_safe")

    def _log(msg):
        print(msg, flush=True)
        log.info(msg.replace("\n", " "))

    OUT = ROOT / "data" / "raw_round6"
    OUT.mkdir(exist_ok=True, parents=True)

    from collectors.sources import all_collectors

    # 整体超时 50 秒
    signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(160)

    drafts_by_fp: dict = {}
    total_kept = 0
    total_raw = 0
    t0 = time.time()

    try:
        for coll in all_collectors():
            wanted = next((limit for name, limit in SOURCES if name == coll.name), None)
            if wanted is None:
                continue
            _log(f"=== {coll.name} (limit {wanted}) ===")
            n = 0
            kept = 0
            source_start = time.time()
            try:
                for hit in safe_collect(coll):
                    total_raw += 1
                    n += 1
                    if n > wanted:
                        break
                    if not _looks_like_pitfall(hit):
                        continue
                    draft = normalize(hit)
                    existing = drafts_by_fp.get(draft.fingerprint)
                    if existing is None or draft.score > getattr(existing, "score", 0):
                        drafts_by_fp[draft.fingerprint] = draft
                    kept += 1
                    total_kept += 1
            except Exception as e:
                _log(f"source {coll.name}: {e}")
            elapsed = time.time() - source_start
            _log(f"  {coll.name}: raw={n} kept={kept} elapsed={elapsed:.1f}s")
            # 检查剩余时间
            remaining = 50 - (time.time() - t0)
            if remaining < 5:
                _log(f"  remaining time {remaining:.1f}s — stopping early")
                break
    except _TimeoutError:
        log.warning("global timeout reached", flush=True)

    # 写文件
    final = list(drafts_by_fp.values())
    seen = set()
    filtered = []
    for d in final:
        key = d.fingerprint
        if key in seen:
            continue
        seen.add(key)
        filtered.append(d)
    written, skipped = write_drafts(filtered, str(OUT), overwrite=False)
    elapsed = time.time() - t0
    log.info(f"summary: raw={total_raw} kept={total_kept} unique={len(filtered)} written={written} skipped={skipped} elapsed={elapsed:.1f}s out={OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())