<template>
  <article class="prose prose-neutral max-w-none dark:prose-invert prose-tight anim-fade-up">
    <h1>数据 Schema</h1>
    <p>
      每个 pitfall 条目都是一份结构化的 markdown，包含 frontmatter（机器可读元数据）和正文（人类阅读）。
    </p>

    <h2>frontmatter 字段</h2>
    <div class="not-prose mt-4 overflow-x-auto rounded-lg border border-ink-200 dark:border-ink-800">
      <table class="w-full text-sm">
        <thead class="bg-ink-50 dark:bg-ink-900/40">
          <tr>
            <th class="px-4 py-2 text-left font-semibold">字段</th>
            <th class="px-4 py-2 text-left font-semibold">类型</th>
            <th class="px-4 py-2 text-left font-semibold">说明</th>
          </tr>
        </thead>
        <tbody>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">title</td>
            <td class="px-4 py-2 text-ink-500">string (4-120)</td>
            <td class="px-4 py-2">简洁标题，描述"是什么坑"</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">summary</td>
            <td class="px-4 py-2 text-ink-500">string (10-300)</td>
            <td class="px-4 py-2">一句话概括 + 修复方向</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">severity</td>
            <td class="px-4 py-2 text-ink-500">enum</td>
            <td class="px-4 py-2">critical / high / medium / low</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">platforms</td>
            <td class="px-4 py-2 text-ink-500">enum[]</td>
            <td class="px-4 py-2">claude-code / openai-agents / langchain / autogen / ...</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">categories</td>
            <td class="px-4 py-2 text-ink-500">enum[]</td>
            <td class="px-4 py-2">context-window / tool-use / prompt-injection / ...</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">symptoms</td>
            <td class="px-4 py-2 text-ink-500">string[]</td>
            <td class="px-4 py-2">至少 1 条可识别的现象描述</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">root_causes</td>
            <td class="px-4 py-2 text-ink-500">string[]</td>
            <td class="px-4 py-2">为什么会发生</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">fixes</td>
            <td class="px-4 py-2 text-ink-500">string[]</td>
            <td class="px-4 py-2">至少 1 条可执行的修复 / 缓解方案</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">references</td>
            <td class="px-4 py-2 text-ink-500">object[]</td>
            <td class="px-4 py-2">公开来源（GitHub issue / 官方 blog / 论坛讨论）</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">verified</td>
            <td class="px-4 py-2 text-ink-500">boolean</td>
            <td class="px-4 py-2">是否通过社区二次验证</td>
          </tr>
          <tr class="border-t border-ink-200 dark:border-ink-800">
            <td class="px-4 py-2 font-mono text-accent">discovered_at</td>
            <td class="px-4 py-2 text-ink-500">date</td>
            <td class="px-4 py-2">首次发现日期 (YYYY-MM-DD)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2 class="mt-8">severity 定义</h2>
    <ul>
      <li><strong class="text-red-500">critical</strong> — 生产事故级（数据丢失 / 安全漏洞 / RCE）</li>
      <li><strong class="text-orange-500">high</strong> — 主要功能不可用（崩溃 / 死循环 / 上下文溢出）</li>
      <li><strong class="text-yellow-600">medium</strong> — 性能 / 体验退化（成本异常 / 限速 / 兼容问题）</li>
      <li><strong class="text-emerald-500">low</strong> — 小问题（typo / 文档错误 / 边缘 case）</li>
    </ul>
  </article>
</template>