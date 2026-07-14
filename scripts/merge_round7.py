"""Fast Round 7 merge — hash-based dedupe + token-shingle similarity.

沿用 merge_round4.py 的高速去重策略：
- URL fingerprint hash (O(1))
- Title SHA1 hash (O(1))
- 标题 token-set Jaccard 用倒排索引（O(title_len)）
- 正文 hash 去重
- 三维度去重（URL + 标题相似度 + 正文 hash）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TARGET = ROOT / "web" / "src" / "content" / "pitfalls"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LIST_URL_RE = re.compile(r"-\s+title:\s*[^\n]*\n\s+url:\s*(\S+)", re.MULTILINE)
TITLE_LINE_RE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
NON_ALNUM = re.compile(r"[^\w一-鿿]+", re.UNICODE)
TOKEN_RE = re.compile(r"[一-鿿]+|[A-Za-z][A-Za-z0-9]+", re.UNICODE)


def _parse_fm(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _normalize(s: str) -> str:
    return NON_ALNUM.sub(" ", (s or "").lower()).strip()


def _tokens(s: str) -> set[str]:
    return set(TOKEN_RE.findall((s or "").lower()))


def _text_hash(*parts: str) -> str:
    h = hashlib.sha1()
    for p in parts:
        h.update(_normalize(p).encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()


def _title_sim(a: str, b: str) -> float:
    from difflib import SequenceMatcher
    na = _normalize(a)
    nb = _normalize(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def _fp_from_file(path: Path, text: str) -> str:
    fm = _parse_fm(text)
    fp = fm.get("fingerprint", "")
    if fp:
        return fp
    m = LIST_URL_RE.search(text[:2000])
    if m:
        url = m.group(1).strip().strip('"').strip("'")
        from collectors.dedupe import url_fingerprint
        return url_fingerprint(url)
    return path.stem


def _source_score(text: str) -> tuple[int, str]:
    fm = _parse_fm(text)
    src = (fm.get("source") or "").strip()
    refs = re.findall(r"source:\s*([^\n]+)", text)
    if refs:
        specific = [s for s in refs if ":" in s]
        src = specific[0] if specific else refs[0]
    score = 0
    if src:
        score = 1
        if ":" in src:
            score = 2
        if src in ("anthropic", "openai", "langchain", "github"):
            score = 3
    return (score, src)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--in-dir", default=".", help="候选目录，默认当前目录")
    p.add_argument("--quality", choices=["all", "medium", "high"], default="medium")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--report", default="dedup_report_round7.json")
    p.add_argument("--sim-threshold", type=float, default=0.85)
    args = p.parse_args(argv)

    print(f"loading candidates from: {args.in_dir}", flush=True)
    candidates: list[tuple[Path, str, dict]] = []
    in_dir = (ROOT / args.in_dir).resolve()
    if not in_dir.exists():
        print(f"  ERROR: {in_dir} not found")
        return 1

    cnt = 0
    for f in sorted(in_dir.glob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
            fm = _parse_fm(text)
        except Exception:
            continue
        fp = _fp_from_file(f, text)
        candidates.append((f, fp, fm))
        cnt += 1
    print(f"  {args.in_dir}: {cnt} files", flush=True)

    print(f"\nloading existing pitfalls from target...", flush=True)
    existing: list[tuple[Path, str]] = []
    for f in TARGET.glob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
            existing.append((f, _fp_from_file(f, text)))
        except Exception:
            continue
    print(f"  existing: {len(existing)}", flush=True)

    # === 1. 收集现有 pitfalls 的 token 反向索引 ===
    print(f"\nbuilding token inverted index...", flush=True)
    token_index: dict[str, set[int]] = defaultdict(set)
    existing_titles: list[tuple[int, str]] = []
    existing_paths: list[Path] = []
    for i, (path, fp) in enumerate(existing):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            existing_paths.append(path)
            existing_titles.append((i, ""))
            continue
        existing_paths.append(path)
        fm = _parse_fm(text)
        title = (fm.get("title") or "").strip()
        existing_titles.append((i, title))
        toks = _tokens(title)
        if len(toks) < 3:
            continue
        for t in toks:
            if len(t) >= 2:
                token_index[t].add(i)

    print(f"  indexed {len(token_index)} unique tokens", flush=True)

    # === 2. 准备 store ===
    url_groups: dict[str, tuple[Path, dict]] = {}
    title_hashes: dict[str, tuple[Path, dict]] = {}
    body_hashes: dict[str, tuple[Path, dict]] = {}

    removed: list[dict] = []

    # 把现有 pitfalls 先入 store
    for path, fp in existing:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            fm = _parse_fm(text)
        except Exception:
            continue
        title = (fm.get("title") or "").strip()
        summary = (fm.get("summary") or "").strip()
        url_groups[fp] = (path, fm)
        title_hashes[hashlib.sha1(_normalize(title).encode()).hexdigest()] = (path, fm)
        body_hashes[_text_hash(title, summary)] = (path, fm)

    # === 3. 处理新 candidates ===
    n_kept = 0
    n_dup_url = 0
    n_dup_title = 0
    n_dup_body = 0
    n_dup_sim = 0
    n_quality = 0
    t0 = time.time()
    for i, (path, fp, fm) in enumerate(candidates):
        if i % 100 == 0:
            elapsed = time.time() - t0
            print(f"  [{i}/{len(candidates)}] kept={n_kept} dup_url={n_dup_url} dup_title={n_dup_title} dup_sim={n_dup_sim} elapsed={elapsed:.1f}s", flush=True)
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        title = (fm.get("title") or "").strip()
        summary = (fm.get("summary") or "").strip()

        # 质量门槛
        sev = (fm.get("severity") or "").lower()
        has_struct = bool(fm.get("symptoms") or fm.get("fixes") or fm.get("root_causes"))
        if args.quality == "high":
            if sev not in ("critical", "high") and not has_struct:
                removed.append({"removed_path": str(path.relative_to(ROOT)), "reason": "quality-low"})
                n_quality += 1
                continue
        elif args.quality == "medium":
            if sev == "low" and not has_struct:
                removed.append({"removed_path": str(path.relative_to(ROOT)), "reason": "quality-low"})
                n_quality += 1
                continue

        # URL fingerprint
        if fp in url_groups:
            removed.append({"removed_path": str(path.relative_to(ROOT)), "reason": f"dup-url:{fp}", "kept": str(url_groups[fp][0].relative_to(ROOT))})
            n_dup_url += 1
            continue

        # 标题 hash
        th = hashlib.sha1(_normalize(title).encode()).hexdigest()
        if th in title_hashes:
            removed.append({"removed_path": str(path.relative_to(ROOT)), "reason": f"dup-title-hash:{th[:8]}", "kept": str(title_hashes[th][0].relative_to(ROOT))})
            n_dup_title += 1
            continue

        # 正文 hash
        bh = _text_hash(title, summary)
        if bh in body_hashes:
            removed.append({"removed_path": str(path.relative_to(ROOT)), "reason": f"dup-body-hash:{bh[:8]}", "kept": str(body_hashes[bh][0].relative_to(ROOT))})
            n_dup_body += 1
            continue

        # 标题相似度（用倒排索引加速）
        cand_tokens = _tokens(title)
        if len(cand_tokens) >= 3:
            cand_idx_set: set[int] = set()
            for t in cand_tokens:
                if len(t) >= 2 and t in token_index:
                    cand_idx_set.update(token_index[t])
            is_dup = False
            for idx in cand_idx_set:
                if idx >= len(existing_titles):
                    continue
                _, prev_title = existing_titles[idx]
                if not prev_title:
                    continue
                prev_tokens = _tokens(prev_title)
                if not prev_tokens:
                    continue
                intersection = cand_tokens & prev_tokens
                union = cand_tokens | prev_tokens
                if not union:
                    continue
                jacc = len(intersection) / len(union)
                if jacc < 0.5:
                    continue
                sim = _title_sim(title, prev_title)
                if sim >= args.sim_threshold:
                    removed.append({
                        "removed_path": str(path.relative_to(ROOT)),
                        "reason": f"dup-title-sim:{sim:.2f}",
                        "kept": str(existing_paths[idx].relative_to(ROOT)),
                    })
                    n_dup_sim += 1
                    is_dup = True
                    break
            if is_dup:
                continue

        # 通过 — 加入 store
        url_groups[fp] = (path, fm)
        title_hashes[th] = (path, fm)
        body_hashes[bh] = (path, fm)
        for t in cand_tokens:
            if len(t) >= 2:
                token_index[t].add(len(existing_titles))
        existing_titles.append((len(existing_titles), title))
        existing_paths.append(path)
        n_kept += 1

    print(f"\n=== Dedup Summary ===", flush=True)
    print(f"existing in target: {len(existing)}", flush=True)
    print(f"candidates: {len(candidates)}", flush=True)
    print(f"kept: {n_kept}", flush=True)
    print(f"dup-url: {n_dup_url}", flush=True)
    print(f"dup-title-hash: {n_dup_title}", flush=True)
    print(f"dup-body-hash: {n_dup_body}", flush=True)
    print(f"dup-title-sim: {n_dup_sim}", flush=True)
    print(f"quality-low: {n_quality}", flush=True)
    print(f"elapsed: {time.time()-t0:.1f}s", flush=True)

    if args.apply:
        print(f"\nwriting new files to {TARGET}...", flush=True)
        written = 0
        skipped = 0
        for fp_val, (path, fm) in url_groups.items():
            if path.parent == TARGET:
                continue
            target_path = TARGET / path.name
            if target_path.exists():
                skipped += 1
                continue
            target_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            written += 1
        print(f"written: {written}, skipped (already in target): {skipped}", flush=True)

        report_path = ROOT / args.report
        report_path.write_text(
            json.dumps({"removed": removed[:2000], "kept": n_kept,
                        "dup_url": n_dup_url, "dup_title_hash": n_dup_title,
                        "dup_body_hash": n_dup_body, "dup_title_sim": n_dup_sim,
                        "quality_low": n_quality}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"report: {report_path}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())