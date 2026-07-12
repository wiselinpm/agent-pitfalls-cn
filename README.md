# Agent Pitfalls 🕳️

> 全网 agent 开发避坑信息整合 — 采集自 GitHub / 博客 / HN / Reddit / 知乎，社区维护、开源协作。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

## 这是什么

开发 AI Agent 时，每个团队都会反复踩同一批「坑」 — context window 静默截断、tool_call 空参数、prompt 注入、多 agent 死循环、token 成本爆炸……

这些坑散落在 GitHub Issues、各家官方博客、Hacker News、Reddit、知乎等十几个平台。
**Agent Pitfalls** 把它们汇集到一处，提供：

- 🩺 **症状**：用户/Agent 实际看到的现象
- 🧠 **根因**：为什么会发生
- 🛠️ **修复**：具体可执行的方案 + 代码示例
- 📚 **参考**：可点击的公开来源
- 🚨 **严重程度**：critical / high / medium / low

## 站点预览

站点采用 [Astro](https://astro.build) 静态生成 + Tailwind CSS，可一键部署到 GitHub Pages：

- 首页：统计 + 最新收录
- `/pitfalls` 避坑库：支持搜索 / 严重程度 / 平台 / 分类筛选
- `/advisories` 安全公告
- `/patterns` 应对模式
- `/schema` 数据 schema
- `/contributing` 贡献指南
- `/rss.xml` 订阅源

## 项目结构

```
.
├── web/                       # Astro 站点
│   ├── src/
│   │   ├── content/pitfalls/  # 避坑条目 Markdown（核心数据）
│   │   ├── content/advisories/# 安全公告
│   │   ├── content/patterns/  # 应对模式
│   │   ├── pages/             # 路由
│   │   ├── layouts/           # 布局
│   │   └── styles/            # 全局样式
│   └── public/                # 静态资源
├── collectors/                # Python 采集器
│   ├── base.py
│   ├── normalize.py
│   ├── dedupe.py
│   ├── emit.py
│   ├── sources/               # GitHub / RSS / HN / Reddit / 知乎
│   ├── run_all.py             # CLI 入口
│   └── tests/                 # pytest
├── docs/                      # 项目级文档
├── astro.config.mjs
├── tailwind.config.mjs
├── package.json
├── requirements.txt
└── LICENSE
```

## 快速开始

### 浏览站点（无需任何工具）

直接访问部署好的站点（或 clone 后 `npm install && npm run dev`）。

### 本地开发

```bash
# 前端
npm install
npm run dev          # http://localhost:4321
npm run build        # 静态站点输出到 dist/

# 采集器（可选）
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m collectors.run_all --out web/src/content/pitfalls
pytest -q collectors/tests
```

### 配置 GitHub Token

部分 GitHub API 端点有匿名 rate limit，强烈建议设置：

```bash
export GITHUB_TOKEN=ghp_xxx
```

## 如何贡献

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。简而言之：

1. Fork → 新建分支
2. 在 `web/src/content/pitfalls/` 新增一个 `.md` 文件，按 [docs/SCHEMA.md](./docs/SCHEMA.md) 填写 frontmatter
3. 提交 PR — CI 会自动校验 schema、字段完整性、链接可达性
4. 维护者 review 后合并

哪怕只是订正错别字、补充一个参考链接，也是受欢迎的贡献 ❤️

## 协议

- **代码**：MIT License
- **内容**（Markdown 条目）：CC-BY 4.0（默认）；如有第三方来源，引用时遵循各自来源的协议

## 致谢

本项目站在巨人的肩膀上 — 所有内容的真正作者是那些在 GitHub Issues、Hacker News、知乎专栏里分享踩坑经验的开发者们。我们只是搬运 + 整理 + 索引。

## Star History

如果这个项目帮到了你，欢迎点一个 ⭐ — 这是它被更多人看到的最好方式。