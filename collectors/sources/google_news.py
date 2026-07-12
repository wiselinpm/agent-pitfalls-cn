"""Google News RSS 采集 — 通过 news.google.com 的公开 RSS 端点抓取新闻索引。

这是覆盖「全网」最稳定的途径：
- 无需 API key / cookie
- 通过 RSS 输出，结构稳定
- 自动覆盖所有被 Google News 索引的源（含中文/英文媒体、个人博客、官方公告）
- 支持 site: 查询（命中特定域名）

限制：返回的是 Google News 索引结果，不是原文站点直采，且排序受新闻价值权重影响。
"""

from __future__ import annotations

import email.utils
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable

from ..base import RawHit
from ._http import http_get


_LOG = logging.getLogger("collectors.google_news")


# 双语 query 集 — 覆盖国内外 + 主流 agent 框架
QUERIES_EN = [
    # 通用 agent 坑
    "Claude Code bug",
    "Claude Code outage",
    "Claude Code error",
    "OpenAI Agents SDK issue",
    "OpenAI Agents SDK breaking change",
    "LangChain error",
    "LangChain deprecation",
    "LangGraph memory leak",
    "agent prompt injection",
    "AI agent failure",
    "RAG hallucination",
    "function calling error",
    "LLM tool use bug",
    "agent rate limit",
    "agent timeout",
    "agent context window overflow",
    "agent cost explosion",
    "agent prompt leak",
    "agent infinite loop",
    "agent stuck",
    "agent retry loop",
    "agent OOM",
    "agent token limit",
    "agent slow response",
    # 框架
    "Cursor IDE issue",
    "Cursor agent mode bug",
    "Aider bug",
    "Cline error",
    "Continue.dev error",
    "Roo Code error",
    "Cody error",
    "Tabnine error",
    "Anthropic SDK breaking change",
    "OpenAI API breaking change",
    "OpenAI function calling deprecated",
    "Anthropic Claude API deprecation",
    # 模型
    "GPT-5 bug",
    "Claude Opus 4.5 bug",
    "Claude Sonnet 4.5 bug",
    "Gemini 2.5 Pro bug",
    "Llama 4 bug",
    # 安全
    "agent jailbreak",
    "prompt injection attack",
    "indirect prompt injection",
    "AI agent supply chain attack",
    "tool poisoning",
    "agent credential leak",
    "agent data exfiltration",
    "agent SSRF",
    "agent RCE",
    "agent privilege escalation",
    "model inversion attack",
    "membership inference attack",
    "agent sandbox escape",
    # 多 agent
    "multi-agent dead lock",
    "multi-agent infinite recursion",
    "autoGen failure",
    "CrewAI error",
    # 部署/性能
    "LLM inference cost",
    "GPU OOM inference",
    "vLLM error",
    "TGI error",
    "Ollama error",
    "llama.cpp crash",
    # MCP / Tooling
    "MCP server error",
    "MCP protocol bug",
    "tool calling schema validation",
    "agent tool hallucination",
    # 评测
    "agent eval failure",
    "LLM benchmark issue",
    "SWE-bench problem",
    # 行业事件
    "Anthropic outage",
    "OpenAI outage",
    "Replit agent bug",
    "Devin AI error",
    # 中文路径 — site:
    "site:anthropic.com incident",
    "site:status.openai.com incident",
    "site:status.anthropic.com incident",
]

QUERIES_ZH = [
    "Claude Code 报错",
    "Claude Code 问题",
    "LangChain 踩坑",
    "LangChain 报错",
    "OpenAI Agents SDK 问题",
    "OpenAI Agents SDK 教程",
    "AI Agent 内存泄漏",
    "AI Agent 部署",
    "Prompt 注入",
    "RAG 召回率",
    "RAG 踩坑",
    "大模型工具调用失败",
    "Function Calling 错误",
    "Agent 死循环",
    "Cursor 使用问题",
    "Cursor 教程 报错",
    "Aider 教程 报错",
    "LangGraph 实战 报错",
    "LangGraph 部署",
    "LangChain 弃用",
    "OpenAI API 限流",
    "Claude API 计费",
    "Claude API 报错",
    "LLM 部署 失败",
    "向量数据库 选型",
    "Embedding 召回",
    "MCP 协议",
    "MCP 服务器 错误",
    "Agent 工具调用 超时",
    "Agent 上下文 溢出",
    "LLM 安全 漏洞",
    "大模型 越狱",
    "AIGC 内容 安全",
    "智能体 评测",
    "LLM 推理 成本",
    "Coze 扣子 问题",
    "Dify 报错",
    "Dify 部署",
    "FastGPT 问题",
    "国产 LLM API 限流",
    "通义千问 API",
    "文心一言 API",
    "智谱 GLM 报错",
    "月之暗面 报错",
    "深度求索 报错",
    "DeepSeek 报错",
    "DeepSeek 限流",
    "Qwen 报错",
    "Qwen 限流",
]


class GoogleNewsCollector:
    name = "google-news"

    def collect(self) -> Iterable[RawHit]:
        for q in QUERIES_EN:
            yield from _fetch(q, hl="en-US", gl="US", ceid="US:en")
        for q in QUERIES_ZH:
            yield from _fetch(q, hl="zh-CN", gl="CN", ceid="CN:zh-Hans")


def _fetch(q: str, hl: str, gl: str, ceid: str) -> Iterable[RawHit]:
    url = "https://news.google.com/rss/search"
    try:
        raw = http_get(
            url,
            params={"q": q, "hl": hl, "gl": gl, "ceid": ceid},
            headers={"User-Agent": "agent-pitfalls/0.1 (+opensource)"},
            timeout=25,
        )
    except Exception as exc:
        _LOG.debug("google-news %r skipped: %s", q, exc)
        return
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        _LOG.debug("google-news parse fail %r: %s", q, exc)
        return
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        # Google News 用 redirect URL，真正的原文 URL 在 source/@url 里
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or "").strip()
        pub = item.findtext("pubDate")
        dt: datetime | None = None
        if pub:
            try:
                dt = email.utils.parsedate_to_datetime(pub)
            except (TypeError, ValueError):
                dt = None
        desc = (item.findtext("description") or "").strip()
        clean_desc = re.sub(r"<[^>]+>", " ", desc)
        clean_desc = re.sub(r"\s+", " ", clean_desc).strip()
        # 源站点
        src_el = item.find("source")
        src_url = src_el.get("url") if src_el is not None else None
        src_name = src_el.text if src_el is not None else None
        if not (title and link):
            continue
        yield RawHit(
            title=title,
            url=link,
            source=f"google-news:{src_name or 'unknown'}",
            summary=clean_desc[:280],
            body=clean_desc,
            published_at=dt,
            score=2,
            tags=("google-news", f"q:{q}", f"src:{src_name}" if src_name else ""),
            raw_metadata={"src_url": src_url, "guid": guid},
        )