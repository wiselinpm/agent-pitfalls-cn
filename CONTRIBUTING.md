# 贡献指南

感谢你愿意花时间让 Agent Pitfalls 变得更好 🙌

## 行为准则

请阅读并遵守 [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)。简短版：**尊重、就事论事、欢迎新手**。

## 提交新避坑条目（最常见）

### 1. 选个文件名

文件名用 `kebab-case`，简短描述问题。例：

```
web/src/content/pitfalls/langchain-agent-infinite-loop.md
```

### 2. 写 frontmatter

最小可用模板：

```yaml
---
title: 简洁描述问题（一行，≤120 字）
summary: 2-3 句话讲清楚发生了什么（≤300 字）
severity: critical | high | medium | low
platforms: [claude-code, generic]          # 见 SCHEMA.md 枚举
categories: [context-window, tool-use]     # 可选
symptoms:
  - 用户/Agent 实际看到的现象
root_causes:
  - 为什么会发生
fixes:
  - 具体可执行的修复步骤
references:
  - title: 来源标题
    url: https://...
    source: GitHub / HN / 知乎
contributor: your-github-handle
discovered_at: 2026-01-15
verified: false   # 首次提交保持 false，维护者复核后改为 true
---
```

### 3. 写正文

正文使用 Markdown，可以包含：

- 复现步骤（编号列表）
- 代码示例（用代码块并标注语言）
- 「为什么不容易发现」小节
- 推荐替代方案对比表

### 4. 本地预览

```bash
npm install
npm run dev
# 访问 http://localhost:4321/pitfalls/your-file-name
```

### 5. 提交 PR

PR 标题：`pitfall: <一句话描述>`
PR 正文模板：

```markdown
## 解决了什么坑
<一段话说明>

## 来源
- <link1>
- <link2>

## 测试
- [ ] 本地构建通过 `npm run build`
- [ ] frontmatter 通过 zod 校验
- [ ] 所有 reference 链接都是公开可访问的
```

## 改进现有条目

任何字段都可以改：

- 补充 `symptoms` / `fixes`
- 增加 `references`
- 修正 `severity`
- 翻译英文条目为中文（或反之）

直接 fork → 修改 → PR 即可。

## 新增采集源

在 `collectors/sources/` 下新建文件，继承 `BaseCollector` 协议。详见 [collectors/README.md](./collectors/README.md)。

提交前请确保：

- `pytest -q collectors/tests` 全绿
- 你的 collector 在网络异常时不会抛异常（应被 `safe_collect` 兜住）
- 一份对应的 `collectors/tests/test_<your_source>.py`

## 改进 UI / 文案

`web/src/pages/`、`web/src/components/`、`web/src/layouts/` 下的任何文件都欢迎调整。
如果改动较大，建议先开 issue 讨论。

## 报告问题

- 内容错误：开 issue 标注「correction」
- 站点 bug：用浏览器 console 截图
- 紧急安全问题：直接邮件 maintainer，不要公开 issue

## 发布节奏

- 内容 PR：随时 review
- 版本发布：每月初
- 重大 schema 变更：通过 RFC 流程（详见 `docs/RFC.md`）

## 维护者

参见 [`MAINTAINERS.md`](./MAINTAINERS.md)。

谢谢！🎉