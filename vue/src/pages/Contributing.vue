<template>
  <article class="prose prose-neutral max-w-none dark:prose-invert prose-tight anim-fade-up">
    <h1>贡献指南</h1>
    <p>
      欢迎提交新坑、补充修复、或修正错误。所有内容通过 GitHub PR 提交，由社区维护者 review。
    </p>

    <h2>1. Fork & Clone</h2>
    <pre><code>git clone https://github.com/agent-pitfalls/agent-pitfalls
cd agent-pitfalls</code></pre>

    <h2>2. 创建新的 pitfall 文件</h2>
    <p>在 <code>web/src/content/pitfalls/</code> 下创建 <code>your-slug.md</code>，模板：</p>
    <pre><code>---
title: 简洁的标题，不超过 80 字
summary: 1-2 句概括，含可执行的修复方向
severity: critical | high | medium | low
platforms: [claude-code, openai-agents, langchain]
categories: [tool-use, prompt-injection]
symptoms:
  - 症状 1
  - 症状 2
root_causes:
  - 根因 1
fixes:
  - 修复方案 1（可执行）
references:
  - title: 来源标题
    url: https://...
    source: github
contributor: 你的名字
discovered_at: 2026-07-12
---

# 详细描述

## 复现步骤
...
</code></pre>

    <h2>3. 验证本地构建</h2>
    <pre><code>pnpm install
pnpm --filter web build
python -m pytest -q</code></pre>

    <h2>4. 提交 PR</h2>
    <pre><code>git checkout -b feat/your-pitfall
git add web/src/content/pitfalls/your-slug.md
git commit -m "docs: add pitfall - your-slug"
git push origin feat/your-pitfall</code></pre>
    <p>然后在 GitHub 上创建 PR。CI 会跑构建 + 测试，review 后合并。</p>

    <h2>贡献者约定</h2>
    <ul>
      <li><strong>质量优先于数量</strong>。一条高质量条目胜过十条空话。</li>
      <li><strong>必有公开来源</strong>。没有公开来源的踩坑，我们不收录。</li>
      <li><strong>每条 pitfall 至少 1 个可执行修复</strong>。仅描述现象不收。</li>
    </ul>
  </article>
</template>