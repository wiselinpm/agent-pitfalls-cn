<script setup>
import { ref } from 'vue';

const advisories = ref([
  {
    title: 'Claude Code Steganographic Marking — Anthropic 后台水印风险',
    summary: '研究表明 Claude Code 在请求中嵌入了「steganographic」标记用于识别，可能影响隐私和请求大小。',
    severity: 'critical',
    affected: ['claude-code'],
    published_at: '2026-07-08',
    references: [{ title: 'HN 讨论', url: 'https://news.ycombinator.com/' }],
  },
  {
    title: 'Prompt Injection via Tool Result — 间接注入攻击',
    summary: '通过工具调用结果中的恶意内容，攻击者可以劫持 agent 的后续行为。',
    severity: 'critical',
    affected: ['openai-agents', 'langchain', 'claude-code'],
    published_at: '2026-06-15',
    references: [{ title: 'OWASP LLM Top 10', url: 'https://owasp.org/' }],
  },
  {
    title: 'OpenAI Agents SDK — 工具 schema 注入',
    summary: '当工具定义接受外部数据时，攻击者可以通过 schema description 注入指令。',
    severity: 'high',
    affected: ['openai-agents'],
    published_at: '2026-05-20',
    references: [],
  },
]);

const tone = {
  critical: 'text-red-500',
  high: 'text-orange-500',
  medium: 'text-yellow-600',
  low: 'text-emerald-500',
};
</script>

<template>
  <header class="mb-8">
    <h1 class="text-3xl font-bold tracking-tight">安全公告</h1>
    <p class="mt-2 text-ink-600 dark:text-ink-300">
      收录影响 agent 框架的已知安全风险与漏洞公告。每条都附严重程度、受影响版本、修复建议。
    </p>
  </header>

  <div class="stagger space-y-3">
    <article v-for="a in advisories" :key="a.title" class="card card-hover">
      <div class="flex items-center gap-2">
        <span class="badge" :class="`badge-${a.severity}`">{{ a.severity }}</span>
        <span v-for="af in a.affected" :key="af" class="badge">{{ af }}</span>
        <span class="ml-auto text-xs text-ink-500 tabular-nums">{{ a.published_at }}</span>
      </div>
      <h2 class="mt-3 text-xl font-semibold">{{ a.title }}</h2>
      <p class="mt-2 text-ink-600 dark:text-ink-300">{{ a.summary }}</p>
      <div v-if="a.references.length" class="mt-3 text-sm">
        <span class="text-ink-500">参考：</span>
        <a
          v-for="r in a.references"
          :key="r.url"
          :href="r.url"
          target="_blank"
          rel="noopener"
          class="text-accent underline-offset-2 hover:underline"
        >{{ r.title }}</a>
      </div>
    </article>
  </div>
</template>