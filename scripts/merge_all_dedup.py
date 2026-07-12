"""三维度严格 dedupe + merge — 把所有 raw 目录里的 markdown 合并到
web/src/content/pitfalls/，按 URL fingerprint + 标题相似度 + 内容 hash 严格去重。

保留规则：
- 同一组里 score 最高的
- 同分时保留 source 字段更具体的（带具体名称而非泛指）
- 同分时保留文件更早的（mtime 早）

输出报告：dedup_report.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TARGET = ROOT / "web" / "src" / "content" / "pitfalls"


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LIST_URL_RE = re.compile(r"-\s+title:\s*[^\n]*\n\s+url:\s*(\S+)", re.MULTILINE)
TITLE_LINE_RE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
SUMMARY_LINE_RE = re.compile(r"^summary:\s*(.+?)\s*$", re.MULTILINE)
NON_ALNUM = re.compile(r"[^\w一-鿿]+", re.UNICODE)


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
    """从文件内容提取 URL fingerprint。"""
    fm = _parse_fm(text)
    fp = fm.get("fingerprint", "")
    if fp:
        return fp
    m = LIST_URL_RE.search(text[:2000])
    if m:
        url = m.group(1).strip().strip('"').strip("'")
        from collectors.dedupe import url_fingerprint
        return url_fingerprint(url)
    return path.stem  # fallback


def _source_score(text: str) -> tuple[int, str]:
    """给 source 字段打分：来源越具体（越不像 "google-news"）分数越高。"""
    fm = _parse_fm(text)
    src = (fm.get("source") or "").strip()
    # 在 references 块里找 source
    refs = re.findall(r"source:\s*([^\n]+)", text)
    ref_sources = [s.strip() for s in refs]
    # 优先使用 references 里的 source
    if ref_sources:
        # 带具体子源（如 google-news:VentureBeat）的得分高于泛源
        specific = [s for s in ref_sources if ":" in s]
        if specific:
            src = specific[0]
        else:
            src = ref_sources[0]
    # 评分
    score = 0
    if src:
        score = 1
        if ":" in src:
            score = 2  # 带具体子源
        if src in ("anthropic", "openai", "langchain", "github"):
            score = 3  # 官方源
    return (score, src)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--in-dirs", nargs="*",
        default=[
            "data/raw8", "data/raw6", "data/raw5",
            "data/raw4", "data/raw3", "data/raw2", "data/raw",
        ],
    )
    p.add_argument("--quality", choices=["all", "medium", "high"], default="medium")
    p.add_argument("--apply", action="store_true",
                   help="实际写入；缺省只 dry-run")
    p.add_argument("--report", default="dedup_report.json")
    args = p.parse_args(argv)

    # 收集所有候选文件
    candidates: list[tuple[Path, str, dict]] = []  # (path, fp, fm)
    for d in args.in_dirs:
        in_dir = (ROOT / d).resolve()
        if not in_dir.exists():
            print(f"skip (missing): {in_dir}")
            continue
        for f in sorted(in_dir.glob("*.md")):
            try:
                text = f.read_text(encoding="utf-8")
                fm = _parse_fm(text)
            except Exception:
                continue
            fp = _fp_from_file(f, text)
            candidates.append((f, fp, fm))

    # 现有 pitfalls（target 里已有的）
    existing: list[tuple[Path, str]] = []
    for f in TARGET.glob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
            existing.append((f, _fp_from_file(f, text)))
        except Exception:
            continue

    # === 三维度去重 ===
    # 收集 (fp -> representative)
    title_hashes: dict[str, tuple[Path, dict, str]] = {}
    body_hashes: dict[str, tuple[Path, dict, str]] = {}
    url_groups: dict[str, tuple[Path, dict, str]] = {}
    title_sim_groups: list[tuple[str, Path, dict]] = []  # (title, path, fm)
    by_fp: dict[str, list[tuple[Path, dict]]] = defaultdict(list)

    removed: list[dict] = []

    def _key_score(item: tuple[Path, dict]) -> tuple:
        path, fm = item
        mtime = path.stat().st_mtime
        score = int(fm.get("score") or 0) if isinstance(fm.get("score"), int) else 0
        src_score, src = _source_score(path.read_text(encoding="utf-8", errors="ignore"))
        # 评分：score 高 > source 具体 > mtime 早
        return (-score, -src_score, mtime, path.name)

    def _maybe_replace(group_key: str, new: tuple[Path, dict], store: dict):
        """把更优的写入 store，并把被替换的移到 removed。"""
        if group_key not in store:
            store[group_key] = new
            return
        existing_item = store[group_key]
        existing_path = existing_item[0]
        existing_fm = existing_item[1]
        # 比较
        new_score = _key_score(new)
        old_score = _key_score(existing_item)
        if new_score < old_score:
            # new 更好
            removed.append({
                "removed_path": str(existing_path.relative_to(ROOT)),
                "removed_score": int(existing_fm.get("score") or 0),
                "reason": f"replaced-by:{new[0].name}",
                "group": group_key,
            })
            store[group_key] = new
        else:
            # 保留旧的，丢弃新的
            removed.append({
                "removed_path": str(new[0].relative_to(ROOT)),
                "removed_score": int(new[1].get("score") or 0),
                "reason": f"kept:{existing_path.name}",
                "group": group_key,
            })

    # 1. 把 target 里现有的 pitfall 先入 store
    for path, fp in existing:
        try:
            text = path.read_text(encoding="utf-8")
            fm = _parse_fm(text)
        except Exception:
            continue
        title = (fm.get("title") or "").strip()
        summary = (fm.get("summary") or "").strip()
        url_groups[fp] = (path, fm)
        title_hashes[hashlib.sha1(_normalize(title).encode()).hexdigest()] = (path, fm)
        body_hashes[_text_hash(title, summary)] = (path, fm)
        title_sim_groups.append((title, path, fm))

    # 2. 处理新 candidates
    for path, fp, fm in candidates:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        title = (fm.get("title") or "").strip()
        summary = (fm.get("summary") or "").strip()
        new_item = (path, fm)

        # 质量门槛
        sev = (fm.get("severity") or "").lower()
        has_struct = bool(fm.get("symptoms") or fm.get("fixes") or fm.get("root_causes"))
        if args.quality == "high":
            if sev not in ("critical", "high") and not has_struct:
                removed.append({"removed_path": str(path.relative_to(ROOT)), "reason": "quality-low"})
                continue
        elif args.quality == "medium":
            if sev == "low" and not has_struct:
                removed.append({"removed_path": str(path.relative_to(ROOT)), "reason": "quality-low"})
                continue

        # URL fingerprint
        if fp in url_groups:
            removed.append({
                "removed_path": str(path.relative_to(ROOT)),
                "reason": f"dup-url:{fp}",
                "kept": str(url_groups[fp][0].relative_to(ROOT)),
            })
            _maybe_replace(fp, new_item, url_groups)
            continue

        # 标题 hash
        th = hashlib.sha1(_normalize(title).encode()).hexdigest()
        if th in title_hashes:
            existing_item = title_hashes[th]
            # existing_item is (path, fm, text) — convert to (path, fm)
            removed.append({
                "removed_path": str(path.relative_to(ROOT)),
                "reason": f"dup-title-hash:{th[:8]}",
                "kept": str(existing_item[0].relative_to(ROOT)),
            })
            _maybe_replace(th, new_item, {th: (existing_item[0], existing_item[1])})
            continue

        # 正文 hash
        bh = _text_hash(title, summary)
        if bh in body_hashes:
            existing_item = body_hashes[bh]
            removed.append({
                "removed_path": str(path.relative_to(ROOT)),
                "reason": f"dup-body-hash:{bh[:8]}",
                "kept": str(existing_item[0].relative_to(ROOT)),
            })
            _maybe_replace(bh, new_item, {bh: (existing_item[0], existing_item[1])})
            continue

        # 标题相似度（与已有组比较）
        is_dup = False
        for prev_title, prev_path, prev_fm in title_sim_groups:
            sim = _title_sim(title, prev_title)
            if sim >= 0.85:
                removed.append({
                    "removed_path": str(path.relative_to(ROOT)),
                    "reason": f"dup-title-sim:{sim:.2f}",
                    "kept": str(prev_path.relative_to(ROOT)),
                })
                is_dup = True
                break
        if is_dup:
            continue

        # 通过 — 加入 store
        url_groups[fp] = (path, fm)
        title_hashes[th] = (path, fm)
        body_hashes[bh] = (path, fm)
        title_sim_groups.append((title, path, fm))

    # 3. 写入 target
    if args.apply:
        written = 0
        for fp, (path, fm) in url_groups.items():
            if path.parent == TARGET:
                continue  # 已是 target 中的文件
            target_path = TARGET / path.name
            if not target_path.exists():
                target_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                written += 1
        print(f"written: {written}")

    # 4. 报告
    summary = Counter(r["reason"].split(":")[0] for r in removed)
    print("\n=== Dedup Summary ===")
    print(f"existing in target: {len(existing)}")
    print(f"candidates from raw: {len(candidates)}")
    print(f"removed: {len(removed)}")
    for reason, count in summary.most_common():
        print(f"  {reason:20s}: {count}")
    print(f"\nfinal unique groups (by fp): {len(url_groups)}")

    if args.apply:
        report_path = ROOT / args.report
        report_path.write_text(
            json.dumps({"removed": removed[:1000], "summary": dict(summary)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\nreport written to {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())