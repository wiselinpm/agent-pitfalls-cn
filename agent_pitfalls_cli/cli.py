"""CLI 入口 — 支持人类阅读 / JSON 输出 / 多种调用形态。"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .index import (
    DEFAULT_PITFALLS_GLOB,
    cache_path,
    load_cache,
    load_records,
    save_cache,
)
from .search import (
    ScanIssue,
    find_related_pitfalls,
    scan_project,
    search,
)
from .tokenize import detect_categories, detect_platforms, detect_severity


_LOG = logging.getLogger("agent_pitfalls_cli.cli")


# ===================================================================
# 输出格式化
# ===================================================================

COLOR = {
    "critical": "\033[1;31m",  # red bold
    "high": "\033[31m",       # red
    "medium": "\033[33m",     # yellow
    "low": "\033[36m",        # cyan
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
}


def _c(text: str, color: str, *, use_color: bool) -> str:
    if not use_color:
        return text
    return f"{COLOR.get(color, '')}{text}{COLOR['reset']}"


def _format_hit(hit, *, use_color: bool, show_body: bool) -> str:
    rec = hit.record
    sev_color = rec.severity if rec.severity in COLOR else "medium"
    lines = []
    title = _c(rec.title, "bold", use_color=use_color)
    sev = _c(f"[{rec.severity}]", sev_color, use_color=use_color)
    score = _c(f"score={hit.score:.2f}", "dim", use_color=use_color)
    lines.append(f"{title}  {sev}  {score}")
    if rec.summary:
        lines.append(f"  {rec.summary[:240]}")
    plat = ", ".join(rec.platforms) or "generic"
    cats = ", ".join(rec.categories) or "—"
    lines.append(
        _c(f"  platforms: {plat}", "dim", use_color=use_color)
    )
    lines.append(_c(f"  categories: {cats}", "dim", use_color=use_color))
    if hit.matched_fields:
        lines.append(
            _c(
                f"  matched: {', '.join(hit.matched_fields)}",
                "dim",
                use_color=use_color,
            )
        )
    lines.append(_c(f"  slug: {rec.slug}", "dim", use_color=use_color))
    if rec.references:
        first = rec.references[0]
        url = first.get("url") if isinstance(first, dict) else None
        if url:
            lines.append(_c(f"  ref: {url}", "dim", use_color=use_color))
    if hit.snippet:
        lines.append("")
        lines.append(_c("  ▸ " + hit.snippet[:280], "reset", use_color=use_color))
    if show_body and rec.body:
        lines.append("")
        lines.append(_c(rec.body.strip()[:1200], "dim", use_color=use_color))
    return "\n".join(lines)


# ===================================================================
# 子命令实现
# ===================================================================

def _build_index(args: argparse.Namespace) -> int:
    source = args.source or None
    records = load_records(source)
    if not records:
        print(_c(f"❌ 没有在 {source or '默认目录'} 找到 pitfall 文件", "high", use_color=not args.no_color), file=sys.stderr)
        return 1
    fp = save_cache(records)
    print(_c(f"✓ indexed {len(records)} pitfalls → {fp}", "low", use_color=not args.no_color))
    return 0


def _get_records(args: argparse.Namespace) -> list:
    """先尝试缓存；失败/缺失时回落到 live 加载。"""
    use_cache = not getattr(args, "no_cache", False)
    if use_cache:
        cached = load_cache()
        if cached:
            return cached
    records = load_records(getattr(args, "source", None))
    if use_cache and records:
        try:
            save_cache(records)
        except OSError:
            pass
    return records


def _cmd_search(args: argparse.Namespace) -> int:
    records = _get_records(args)
    if not records:
        print(_c("❌ 没有可用的 pitfalls（先运行 `agent-pitfalls build`）", "high", use_color=not args.no_color), file=sys.stderr)
        return 1
    result = search(
        records,
        args.query,
        top_k=args.top_k,
        platform=args.platform,
        category=args.category,
        severity=args.severity,
    )
    if args.json:
        payload = {
            "query": result.query,
            "expanded_query": result.expanded_query,
            "detected_platforms": list(result.detected_platforms),
            "detected_categories": list(result.detected_categories),
            "total_records": result.total_records,
            "hits": [h.to_dict(include_body=args.verbose) for h in result.hits],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    use_color = not args.no_color and sys.stdout.isatty()
    if not result.hits:
        print(_c(f"未找到与 {args.query!r} 相关的 pitfall。", "medium", use_color=use_color))
        return 0
    print(
        _c(
            f"🔍 {len(result.hits)}/{result.total_records} matches for {args.query!r}",
            "bold",
            use_color=use_color,
        )
    )
    if result.detected_platforms or result.detected_categories:
        meta = []
        if result.detected_platforms:
            meta.append(f"platforms={list(result.detected_platforms)}")
        if result.detected_categories:
            meta.append(f"categories={list(result.detected_categories)}")
        print(_c("  detected: " + ", ".join(meta), "dim", use_color=use_color))
    print()
    for i, hit in enumerate(result.hits, 1):
        print(f"{i}. {_format_hit(hit, use_color=use_color, show_body=args.verbose)}")
        print()
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    records = _get_records(args)
    for r in records:
        if r.slug == args.slug or r.file.endswith(args.slug):
            if args.json:
                print(json.dumps(r.to_dict(), ensure_ascii=False, indent=2))
                return 0
            print(f"# {r.title}\n")
            print(r.body.strip() or r.summary)
            return 0
    print(_c(f"❌ 找不到 slug={args.slug}", "high", use_color=not args.no_color), file=sys.stderr)
    return 1


def _cmd_list(args: argparse.Namespace) -> int:
    records = _get_records(args)
    records = sorted(records, key=lambda r: r.discovered_at or "", reverse=True)
    if args.severity:
        records = [r for r in records if r.severity == args.severity]
    if args.platform:
        wanted = {p.strip() for p in args.platform.split(",")}
        records = [r for r in records if r.platforms and (set(r.platforms) & wanted)]
    if args.category:
        wanted = {c.strip() for c in args.category.split(",")}
        records = [r for r in records if r.categories and (set(r.categories) & wanted)]
    records = records[: args.limit]
    if args.json:
        print(json.dumps([r.to_dict() for r in records], ensure_ascii=False, indent=2))
        return 0
    use_color = not args.no_color and sys.stdout.isatty()
    for r in records:
        sev = _c(f"[{r.severity}]", r.severity if r.severity in COLOR else "medium", use_color=use_color)
        plat = ",".join(r.platforms) or "generic"
        print(f"{sev} {r.title}  ({_c(plat, 'dim', use_color=use_color)})")
        print(_c(f"  {r.slug}", "dim", use_color=use_color))
    return 0


def _cmd_platforms(args: argparse.Namespace) -> int:
    records = _get_records(args)
    counter: dict[str, int] = {}
    for r in records:
        for p in r.platforms or ("generic",):
            counter[p] = counter.get(p, 0) + 1
    if args.json:
        print(json.dumps(counter, ensure_ascii=False, indent=2))
        return 0
    for k, v in sorted(counter.items(), key=lambda x: -x[1]):
        print(f"{k:<20} {v}")
    return 0


def _cmd_categories(args: argparse.Namespace) -> int:
    records = _get_records(args)
    counter: dict[str, int] = {}
    for r in records:
        for c in r.categories or ("uncategorized",):
            counter[c] = counter.get(c, 0) + 1
    if args.json:
        print(json.dumps(counter, ensure_ascii=False, indent=2))
        return 0
    for k, v in sorted(counter.items(), key=lambda x: -x[1]):
        print(f"{k:<20} {v}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    """对项目目录做静态扫描 + 知识库匹配。"""
    records = _get_records(args)
    if not records:
        print(_c("❌ 没有可用的 pitfalls（先运行 `agent-pitfalls build`）", "high", use_color=not args.no_color), file=sys.stderr)
        return 1
    project = args.path or "."
    issues = scan_project(project, records, max_issues=args.limit)
    if args.json:
        payload = {
            "project": project,
            "total_issues": len(issues),
            "issues": [
                {
                    **{
                        "rule_id": i.rule_id,
                        "title": i.title,
                        "file": i.file,
                        "line": i.line,
                        "snippet": i.snippet,
                        "matched_text": i.matched_text,
                        "platforms": list(i.platforms),
                        "categories": list(i.categories),
                    },
                    "related_pitfalls": [
                        h.to_dict() for h in find_related_pitfalls(i, records, top_k=2)
                    ],
                }
                for i in issues
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    use_color = not args.no_color and sys.stdout.isatty()
    if not issues:
        print(_c(f"✅ 在 {project} 未扫到已知坑模式", "low", use_color=use_color))
        return 0
    print(_c(f"🔍 在 {project} 扫到 {len(issues)} 个潜在坑：", "bold", use_color=use_color))
    print()
    for issue in issues:
        print(_c(f"● {issue.title}", "high", use_color=use_color))
        print(f"  {issue.file}:{issue.line}")
        print(_c(f"  > {issue.snippet}", "dim", use_color=use_color))
        related = find_related_pitfalls(issue, records, top_k=2)
        if related:
            for h in related:
                print(_c(f"    → {h.record.title}", "low", use_color=use_color))
                print(_c(f"      {h.record.slug}  [{h.record.severity}]", "dim", use_color=use_color))
        print()
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    """本地 HTTP 服务 — 给 Claude Code / Codex / OpenCode plugin 调用。"""
    try:
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    except ImportError:
        print("http.server not available", file=sys.stderr)
        return 1

    records = _get_records(args)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *fargs):  # noqa: N802
            _LOG.debug(fmt, *fargs)

        def _json(self, payload: dict, status: int = 200) -> None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):  # noqa: N802
            from urllib.parse import parse_qs, urlparse

            url = urlparse(self.path)
            qs = parse_qs(url.query)
            if url.path in ("/", "/health"):
                return self._json({"status": "ok", "records": len(records), "version": __version__})
            if url.path == "/search":
                q = (qs.get("q") or [""])[0]
                if not q:
                    return self._json({"error": "missing q"}, 400)
                platform = (qs.get("platform") or [None])[0]
                category = (qs.get("category") or [None])[0]
                severity = (qs.get("severity") or [None])[0]
                top_k = int((qs.get("top_k") or ["5"])[0])
                result = search(
                    records,
                    q,
                    top_k=top_k,
                    platform=platform,
                    category=category,
                    severity=severity,
                )
                return self._json({
                    "query": result.query,
                    "hits": [h.to_dict(include_body=True) for h in result.hits],
                    "detected_platforms": list(result.detected_platforms),
                    "detected_categories": list(result.detected_categories),
                })
            if url.path == "/platforms":
                counter: dict[str, int] = {}
                for r in records:
                    for p in r.platforms or ("generic",):
                        counter[p] = counter.get(p, 0) + 1
                return self._json(counter)
            if url.path == "/categories":
                counter = {}
                for r in records:
                    for c in r.categories or ("uncategorized",):
                        counter[c] = counter.get(c, 0) + 1
                return self._json(counter)
            if url.path.startswith("/pitfall/"):
                slug = url.path[len("/pitfall/"):]
                for r in records:
                    if r.slug == slug:
                        return self._json(r.to_dict())
                return self._json({"error": "not found", "slug": slug}, 404)
            return self._json({"error": "not found", "path": url.path}, 404)

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"agent-pitfalls serving on http://{args.host}:{args.port}  ({len(records)} records)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


def _cmd_version(args: argparse.Namespace) -> int:
    print(f"agent-pitfalls {__version__}")
    return 0


# ===================================================================
# argparse
# ===================================================================

def _add_common_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--source", "-s", default=None, help="pitfalls 源目录 / glob（默认: web/src/content/pitfalls）")
    p.add_argument("--no-cache", action="store_true", help="忽略缓存，直接 live 加载")
    p.add_argument("--no-color", action="store_true", help="禁用 ANSI 颜色")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-pitfalls",
        description="agent-pitfalls — 在开发期即时查询 AI agent 避坑知识",
    )
    parser.add_argument("--version", action="store_true", help="打印版本")
    sub = parser.add_subparsers(dest="cmd")

    # build
    p_build = sub.add_parser("build", help="构建/刷新索引缓存")
    p_build.add_argument("--source", "-s", default=None)
    p_build.add_argument("--no-color", action="store_true")
    p_build.set_defaults(func=_cmd_build_index if False else _build_index)  # type: ignore

    # search
    p_search = sub.add_parser("search", aliases=["s"], help="智能查询 pitfall")
    p_search.add_argument("query", help="自然语言查询，如 'claude code context overflow'")
    p_search.add_argument("--top-k", "-n", type=int, default=5)
    p_search.add_argument("--platform", help="按平台过滤，逗号分隔")
    p_search.add_argument("--category", help="按类别过滤，逗号分隔")
    p_search.add_argument("--severity", choices=["critical", "high", "medium", "low"])
    p_search.add_argument("--json", action="store_true", help="输出 JSON（供 LLM 调用）")
    p_search.add_argument("-v", "--verbose", action="store_true", help="打印 pitfall body")
    _add_common_flags(p_search)
    p_search.set_defaults(func=_cmd_search)

    # show
    p_show = sub.add_parser("show", help="按 slug 查看 pitfall 详情")
    p_show.add_argument("slug")
    p_show.add_argument("--json", action="store_true")
    _add_common_flags(p_show)
    p_show.set_defaults(func=_cmd_show)

    # list
    p_list = sub.add_parser("list", aliases=["ls"], help="列出 pitfalls")
    p_list.add_argument("--severity", choices=["critical", "high", "medium", "low"])
    p_list.add_argument("--platform")
    p_list.add_argument("--category")
    p_list.add_argument("--limit", "-n", type=int, default=50)
    p_list.add_argument("--json", action="store_true")
    _add_common_flags(p_list)
    p_list.set_defaults(func=_cmd_list)

    # platforms / categories
    p_pf = sub.add_parser("platforms", help="列出所有平台")
    p_pf.add_argument("--json", action="store_true")
    _add_common_flags(p_pf)
    p_pf.set_defaults(func=_cmd_platforms)

    p_cat = sub.add_parser("categories", help="列出所有类别")
    p_cat.add_argument("--json", action="store_true")
    _add_common_flags(p_cat)
    p_cat.set_defaults(func=_cmd_categories)

    # check
    p_check = sub.add_parser("check", help="扫描项目目录，识别已知坑模式")
    p_check.add_argument("path", nargs="?", default=".")
    p_check.add_argument("--limit", "-n", type=int, default=50)
    p_check.add_argument("--json", action="store_true")
    _add_common_flags(p_check)
    p_check.set_defaults(func=_cmd_check)

    # serve
    p_serve = sub.add_parser("serve", help="启动本地 HTTP 服务（供 plugin 调用）")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", "-p", type=int, default=8765)
    _add_common_flags(p_serve)
    p_serve.set_defaults(func=_cmd_serve)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    if not argv or argv[0] in ("-h", "--help"):
        parser = build_parser()
        parser.print_help()
        return 0
    if argv[0] in ("-V", "--version", "version"):
        return _cmd_version(argparse.Namespace())
    # 简化：如果只有 build，没子命令解析器时直接处理
    parser = build_parser()
    # 兼容 'agent-pitfalls search xxx' 直接调用
    args = parser.parse_args(argv)
    if getattr(args, "version", False):
        return _cmd_version(args)
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())