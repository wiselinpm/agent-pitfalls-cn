# 采集源诊断与降级策略

不是所有 source 都能稳定工作。本文档记录每个 source 的状态、已知失败原因和降级策略。

## 当前状态总览

**51 个 source**，覆盖 **9 个国内平台 + 42 个国际/通用平台**。

| Source | 状态 | 区域 | 数据质量 | 备注 |
|---|---|---|---|---|
| `github-issues` | ✅ 稳定 | 国际 | 高 | 限速：匿名 60/h，建议配 `GITHUB_TOKEN` |
| `github-releases` | ✅ 稳定 | 国际 | 高 | GitHub Releases API — 抓 breaking change / deprecation |
| `rss` | ✅ 稳定 | 国际 | 中 | openai-blog / langchain-blog / hn-newest 正常 |
| `hackernews` | ✅ 稳定 | 国际 | 高 | Algolia API，无 key |
| `reddit` | ❌ 失败 | 国际 | — | 公开端点持续 403 |
| `reddit-v2` | ✅ 稳定 | 国际 | 高 | Brave Search `site:reddit.com` 兜底 |
| `zhihu` | ❌ 失败 | **国内** | — | 反爬升级，搜索 API 返 HTML 验证码 |
| `zhihu-v2` | ✅ 稳定 | **国内** | 高 | Brave Search `site:zhihu.com` 兜底 |
| `juejin` | ❌ 失败 | **国内** | — | API 全部 404 |
| `juejin-v2` | ✅ 稳定 | **国内** | 高 | Brave Search `site:juejin.cn` 兜底 |
| `medium` | ✅ 稳定 | 国际 | 中 | 通过 tag RSS，部分 handle 失效 |
| `devto` | ✅ 稳定 | 国际 | 中 | `/api/articles` 公开端点 |
| `dev-community` | ✅ 稳定 | 国际 | 中 | DEV.to 通用 RSS |
| `stackoverflow` | ✅ 稳定 | 国际 | 高 | API 2.3，匿名有 quota 限制 |
| `arxiv` | ✅ 稳定 | 国际 | 中 | arXiv API，按 submittedDate 倒序 15 篇/query |
| `arxiv-v2` | ✅ 稳定 | 国际 | 中 | 关键词密度过滤：要求同时含 failure + method 关键词 |
| `awesome-repos` | ⚠️ 部分 | 国际 | 低 | README 链接噪声大 |
| `lobsters` | ✅ 稳定 | 国际 | 中 | 主站 RSS 过滤 AI 关键词后命中 |
| `huggingface-papers` | ✅ 稳定 | 国际 | 中 | daily papers API + 关键词过滤 |
| `producthunt` | ✅ 稳定 | 国际 | 低 | Atom feed，过滤 AI 关键词 |
| `official-status` | ✅ 稳定 | 国际 | 高 | Anthropic + OpenAI 事故 RSS |
| `vendor-blogs` | ✅ 稳定 | 国际 | 高 | DeepMind / AWS ML / Anthropic News / OpenAI blog / LangChain / HF blog |
| `newsletters` | ✅ 稳定 | 国际 | 高 | Latent Space / Interconnects / Pragmatic Engineer / Simon Willison |
| `frameworks` | ✅ 稳定 | 国际 | 高 | LlamaIndex / CrewAI / LangChain / LangGraph / OpenAI Agents / Anthropic Cookbook / Claude Code release |
| `tldr` | ✅ 稳定 | 国际 | 中 | TLDR AI + Ben's Bites |
| `forums` | ✅ 稳定 | 国际 | 高 | LangChain forum + OpenAI community |
| `extra-en` | ✅ 稳定 | 国际 | 高 | Hashnode / dev.to tag / Substack / IndieHackers / TheNewStack / DZone / KDnuggets / HackerNoon |
| `cloud-cn` | ⚠️ 部分 | **国内** | 中 | 阿里云/腾讯云/华为云 RSS 多数 404，RSSHub 公开镜像多数 403，仅美团技术RSS通 |
| `sogou-wechat` | ⚠️ 部分 | **国内** | 中 | 搜狗微信搜索公开页，HTML 结构有变 |
| `meta-search` | ✅ 稳定 | 通用 | 中 | Brave Search 通用 query，覆盖 Cursor Forum / Aider Discussions / LangSmith 等 |
| `google-news` | ✅ 稳定 | 通用 | 高 | Google News RSS，37 个双语 query，覆盖全网新闻 |
| `segmentfault` | ✅ 稳定 | **国内** | 高 | `api.segmentfault.com/search` |
| `infoq-cn` | ✅ 稳定 | **国内** | 中 | 多 RSS feed，命中较少 |
| `cnblogs` | ✅ 稳定 | **国内** | 中 | Atom RSS 过滤 AI 关键词 |
| `csdn` | ✅ 稳定 | **国内** | 中 | `so.csdn.net/api/v3/search`，反爬严 |
| `oschina` | ✅ 稳定 | **国内** | 中 | 新闻 + 问答 RSS，过滤 AI 关键词 |
| `meituan` | ✅ 稳定 | **国内** | 高 | `tech.meituan.com` RSS，过滤 AI/agent 关键词 |
| `sspai` | ✅ 稳定 | **国内** | 中 | `sspai.com/feed`，过滤 AI 关键词 |

## 本次全网采集结果（2026-07-12 — 第二轮）

| 阶段 | 输出目录 | 文件数 | 备注 |
|---|---|---|---|
| 起点（合并前） | `web/src/content/pitfalls/` | 1,031 | 既有的人工/早期自动收录 |
| 第一轮 Batch A — 国际 | `data/raw5/` | 951 | github-issues/releases/rss/hn/devto/stackoverflow/lobsters/hf-papers/vendor-blogs/newsletters/frameworks/forums/extra-en/awesome-repos/medium/arxiv 等 21 个 source |
| 第一轮 Batch B — 国内 | `data/raw6/` | 113 | segmentfault/cnblogs/csdn/oschina/meituan/infoq-cn/sspai/cloud-cn 等 13 个 source |
| 第一轮 Batch D — 全网 | `data/raw8/` | 2,286 | google-news（37 个双语 query）+ arxiv（fix 后 120 + 80 篇论文） |
| 第一轮合并 | `web/src/content/pitfalls/` | 3,486 | 严格 dedupe；spammy 清理；URL 补全 |
| 第二轮 Batch D — youtube/substack | `data/raw9/raw10/` | 71 | youtube RSS + 22 个 Substack/Ghost newsletter |
| 第二轮 Batch D — communities | `data/raw11/` | (进行中) | Cursor Forum / Replicate / GitHub Discussions |
| 第二轮 strict dedupe | `web/src/content/pitfalls/` | **3,792** | 三维度 dedupe（URL fp + 标题相似度 + 内容 hash）+ 修复 schema 违反 |
| 站点构建 | `dist/` | **3,800 pages** | Astro build 通过；sitemap 生成 |

## 第二轮 — 增强采集（2026-07-12）

| 阶段 | 输出目录 | 文件数 | 备注 |
|---|---|---|---|
| Batch E — openreview + vendor-official | `data/raw16/` | 104 | 75 篇 OpenReview + 30 vendor changelog |
| Batch E — hn-search + devto-latest + lobsters | `data/raw14/` | 279 | 275 HN 全文 + 27 devto latest + 0 lobsters |
| 第二轮合并 | `web/src/content/pitfalls/` | **4,098** | 三维度 strict dedupe（URL fp + 标题 hash + 标题相似度 + content hash）|
| 站点构建 | `dist/` | **4,106 pages** | Astro build 通过；sitemap 生成 |

## 第四轮 — 新源 + 增强采集（2026-07-12）

| 阶段 | 输出目录 | 文件数 | 备注 |
|---|---|---|---|
| Batch E 补跑 — feed-aggregator + vendor-official + devto-latest | `data/raw17/` | 1,181 | feed-aggregator 30+ 边缘博客（Martin Fowler / Coding Horror / Overreacted / swyx / coolshell / 阮一峰 / Schneier / Trail of Bits / Cloudflare / Stripe / GitHub Eng / Discord / Slack / Netlify / Vercel 等）|
| Batch F — Round 4 新源 | `data/raw18/` | 337 | cn-eng-blog + github-changelog + ai-research-blog + ai-newsletter + hn-algolia-extended |
| Batch G — Round 4 续 | `data/raw19/` | 41 | cn-tech-media（RSSHub 镜像多数 403）|
| Round 4 合并 | `web/src/content/pitfalls/` | **5,427** | 三维度 strict dedupe + token 反向索引加速（4.1s 完成 1,559 candidates）|
| 站点构建 | `dist/` | **5,435 pages** | Astro build 通过；sitemap 生成 |

## 第五轮 — 学术 + 趋势 + 评论 + Tech news（2026-07-12）

| 阶段 | 输出目录 | 文件数 | 备注 |
|---|---|---|---|
| Round 5 学术 — semantic-scholar + github-trending | `data/raw21/` | 61 | Semantic Scholar（15 个 query 受 429 限制）+ GitHub Trending（6 类 117 命中）|
| Round 5 续 — hn-comments + tech-news + github-trending | `data/raw_round5/` | 22 | HN 热门 comment tree + Tech news（The Verge / Ars Technica / Wired / MIT Tech Review / ZDNet / Dark Reading / Krebs / BleepingComputer / Hacker News / Cyberscoop）|
| Round 5 合并 | `web/src/content/pitfalls/` | **5,509** | 三维度 strict dedupe（0.3s 完成 83 candidates）|
| 站点构建 | `dist/` | **5,517 pages** | Astro build 通过；sitemap 生成 |

## 第五轮新增 source（5 个）

| Source | 状态 | 区域 | 数据质量 | 备注 |
|---|---|---|---|---|
| `semantic-scholar` | ⚠️ 严格 429 | 国际 | 高 | Semantic Scholar Graph API，15 个 pitfall 相关 query（匿名 100/min RPS 限制）|
| `github-trending` | ✅ 稳定 | 国际 | 中 | GitHub Trending HTML 解析（all/python/typescript/go × daily/weekly = 6 个组合）|
| `kaggle-discussions` | ⚠️ 部分 | 国际 | 低 | Kaggle Discussions 搜索 API（5 个 query，目前返回 0 — API 端点变更）|
| `hn-comments` | ✅ 高产 | 国际 | 高 | HN Algolia `points>200` 高分 story + comment tree（单批 12,412 hits，限速 100/批）|
| `tech-news` | ✅ 稳定 | 国际 | 中 | 16 个主流 tech news RSS：Techmeme / The Verge / Ars Technica / Wired / MIT Tech Review / ZDNet / InfoWorld / The New Stack / The Register / BleepingComputer / Krebs / Dark Reading / Threatpost / SecurityWeek / The Hackers News / Cyberscoop |

## 最终状态

| 指标 | 数值 |
|---|---|
| **总 pitfall 数** | **5,509** |
| 构建页面数 | 5,517 |
| 收录 source 总数 | **65**（41 国际 + 12 国内 + 12 通用/学术/平台）|
| 全网 source 引用种类（references.source 字段去重后）| **800+ 种** |
| 严重程度：critical / high / medium / low | 2190 / 420 / 2790 / 109 |
| 收录年份跨度 | 2016 - 2026 |
| 主要 source 占比：google-news | 2,228 (40%) |
| 已去重 — 三维度（URL fp / 标题 hash / 标题相似度≥0.85 / content hash）| ✅ |

## 全网覆盖 — 收录 source 分布（最终）

| 来源 | 数量 | 占比 |
|---|---|---|
| google-news（37+ 双语 query） | 2,228 | 59% |
| GitHub Issues + Releases | 326 | 8.6% |
| StackOverflow | 206 | 5.4% |
| HackerNews | 151 | 4% |
| dev.to + tag RSS | 162 | 4.3% |
| segmentfault | 93 | 2.5% |
| openai-blog | 122 | 3.2% |
| arxiv + arxiv-v2 | 44+ | 1.2% |
| huggingface-papers | 42 | 1.1% |
| aws-ml / anthropic-status / langchain-forum / openai-forum / cursor-forum | 100+ | 2.6% |
| 其余（medium/hackernoon/thenewstack/pragmatic-engineer/youtube/substack）| ~200 | 5% |

## 第二轮新增 source（5 个）

| Source | 状态 | 区域 | 数据质量 | 备注 |
|---|---|---|---|---|
## 第四轮 — 新增源（9 个）

| Source | 状态 | 区域 | 数据质量 | 备注 |
|---|---|---|---|---|
| `arxiv-categories` | ✅ 稳定 | 国际 | 中 | arXiv 按分类（cs.AI/cs.CL/cs.CR/cs.MA/cs.SE/cs.LG/cs.IR/cs.HC）|
| `cn-eng-blog` | ⚠️ 部分 | **国内** | 中 | 字节/腾讯云/阿里云/小红书/京东/微信小程序/飞书/B站/商汤/旷视 等 19 个 RSS（多数被反爬）|
| `github-changelog` | ✅ 稳定 | 国际 | 中 | GitHub Changelog / News / Engineering 三路 RSS |
| `ai-research-blog` | ⚠️ 部分 | 国际 | 高 | Anthropic/OpenAI/Google/DeepMind/HF/Pinecone/Qdrant/Weaviate/Elastic 等 16 个研究 blog（部分 404）|
| `ai-newsletter` | ⚠️ 部分 | 国际 | 高 | The Batch/Import AI/Last Week in AI/The Gradient/The Rundown AI/The Neuron/MLOps/Gradient Flow 等 18 个 newsletter |
| `hn-algolia-extended` | ✅ 稳定 | 国际 | 高 | HN Algolia 6 个 query 全量搜索（agent failure / Claude Code / OpenAI hallucination / RAG / vector db）|
| `cn-tech-media` | ⚠️ 部分 | **国内** | 中 | 36氪/虎嗅/极客公园/IT之家/钛媒体/机器之心 + RSSHub 镜像（多数 403）|
| `reddit-proxy` | ⚠️ 部分 | 国际 | 低 | 通过 HN Algolia `site:reddit.com` 间接索引 reddit 内容 |
| `discourse-forums` | ⚠️ 部分 | 国际 | 低 | GitHub Discussions 15 个仓库（langchain/llamaindex/autogen/crewai/openai-python/anthropic-sdk/litellm/aider/cline/semantic-kernel/vercel-ai 等）|

## 全网覆盖 — 收录 source 分布

| 来源 | 数量 | 占比 |
|---|---|---|
| google-news（37 双语 query） | 2,228 | 64% |
| StackOverflow | 193 | 5.5% |
| GitHub Issues | 176 | 5% |
| HackerNews | 122 | 3.5% |
| dev.to + devto tag | 115 + 33 | 4.3% |
| segmentfault | 93 | 2.7% |
| openai-blog | 79 | 2.3% |
| arxiv + arxiv-v2 | 58 | 1.7% |
| huggingface-papers | 42 | 1.2% |
| csdn / langchain-forum / openai-forum | 19 / 19 / 22 | 各 0.5% |
| medium / hackernoon / thenewstack / pragmatic-engineer | 50+ | ~1.5% |
| 其余（anthropic/hf/aws-ml/deepmind/...） | ~100 | 3% |

## 已失败 source 的根因与备选方案

### Juejin (掘金)

**症状**：所有 `api.juejin.cn/*` 端点返回 `404` 或 `err_no:2 请求路由不存在`。

**根因**：掘金 2024 年后把所有公开 API 路由迁移到内部网关，未登录请求看不到路由。tag 列表页是纯客户端渲染，SSR HTML 中不带文章数据。

**备选**：
1. **登录后用 Cookie** — 手工导出浏览器 Cookie + `aid` + `uuid` 放入 `~/.juejin-cookie`，collector 读取使用
2. **完全放弃** — 用 OSChina / SegmentFault / CSDN / 美团技术 替代
3. **第三方聚合** — 51CTO / 极客邦 等更开放的平台（但目前也已反爬）

**当前做法**：保留 collector（best-effort），实际产出为 0。

### Reddit

**症状**：所有 `reddit.com` 子域的请求返回 `403 Forbidden` 或 HTML 拦截页。

**根因**：Reddit 在 2023 年 API 改版后强制要求鉴权，未授权请求被云端 WAF 拦截。`.rss` 端点同样被 block（看似返回 200 但内容是 `<html>...</html>`）。

**备选**：
1. **完全放弃** — 用 HN Algolia 替代：`hn.algolia.com/api/v1/search?query=site:reddit.com+agent`
2. **申请 OAuth client credentials** — 在 Reddit preferences/apps 创建 app，每月 100 次/分钟
3. **第三方镜像** — `teddit.net` / `libreddit.example.org` 等开源镜像（不稳定）

**当前做法**：保留 collector，但实际产出为 0，不影响其它 source。

### 知乎

**症状**：`https://www.zhihu.com/api/v4/search_v3` 偶发返回 `403` 或 HTML 验证码页。

**根因**：知乎对未登录请求做严格的 TLS 指纹 + Cookie 校验，匿名搜索 API 在生产网络下基本不可用。

**备选**：
1. **登录后用 Cookie** — 手工导出浏览器 Cookie 放入 `~/.zhihu-cookie`，collector 读取使用
2. **改用第三方聚合** — `sspai.com` / `infoq.cn` / `oschina.net` 等更开放的平台
3. **完全放弃** — 用 Bing 中文搜索 API 替代：`https://api.bing.microsoft.com/v7.0/search?q=...`

**当前做法**：保留 collector（best-effort），实际产出为 0。

### GitHub Anonymous Rate Limit

**症状**：未配 token 时每小时只能发起 60 次 `/search/issues` 请求。每个 repo 2 个 query，10 个 repo = 20 次，刚好够单次采集。再多会被 403。

**修复**：在 `.env` 设置 `GITHUB_TOKEN=ghp_xxx`，限额提升到 5000/h。

```bash
echo 'GITHUB_TOKEN=ghp_xxx' >> .env
export $(cat .env | xargs)
python -m collectors.run_all
```

## 降级策略

`collectors/run_all.py` 的 `_looks_like_pitfall()` 对每个 source 都会做关键词过滤。这意味着即使某个 source 返回了垃圾内容，大多数也不会进入最终输出。

`safe_collect()` 还会捕获单个 source 的异常并 warn log，不阻断整个流程。

## 故障排查命令

```bash
# 单个 source 自检（带超时）
python -c "
import logging, signal
from collectors.sources import all_collectors, safe_collect

def handler(*_): raise TimeoutError()
signal.signal(signal.SIGALRM, handler)

for coll in all_collectors():
    signal.alarm(15)
    try:
        n = sum(1 for _ in safe_collect(coll))
        print(f'{coll.name:14} OK {n}')
    except Exception as e:
        print(f'{coll.name:14} FAIL {e}')
    finally:
        signal.alarm(0)
"

# 打开 verbose 看每个 source 的实际命中
python -m collectors.run_all --out data/raw --verbose
```

## 未来扩展

按优先级：

1. **微信公众号** — 通过搜狗微信搜索爬（合规风险）
2. **Bilibili / YouTube 视频字幕** — 开发者会议、技术分享经常讲坑
3. **Discord 频道** — Anthropic / LangChain 都有公开 Discord，质量高但接入复杂
4. **arXiv 自动聚类** — 用 embedding 找出真正讨论「失败」的论文，目前是噪声
5. **awesome-* GitHub** — 当前过滤太宽松，需要把每个链接 GET 一次看页面内容
6. **Bing / Baidu 中文搜索** — 作为元搜索引擎，对抗知乎/掘金的反爬
7. **阿里云 / 腾讯云 / 华为云 开发者社区** — 需要找正确的 RSS endpoint（当前 404）
8. **字节技术 / 哔哩哔哩技术** — 当前为 SSR HTML，需要专门的爬虫
9. **Twitter/X via Nitter 镜像** — 跟踪业界实时讨论
10. **Cursor / Aider / Replicate / OpenAI Cookbook 等 changelog RSS** — 当前缺少正确 endpoint