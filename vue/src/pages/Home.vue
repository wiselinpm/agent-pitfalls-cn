<script setup>
import { computed } from 'vue';
import { usePitfalls } from '../composables/useContent';
import PitfallCard from '../components/PitfallCard.vue';

const { all, total, criticalCount, highCount, verifiedCount, withFixesCount, platformCount, topCategories, recentCount } = usePitfalls();

const featured = computed(() => all.value.slice(0, 6));

const lastUpdatedRel = computed(() => {
  const d = all.value[0]?.discovered_at;
  if (!d) return '—';
  const days = Math.floor((Date.now() - new Date(d).getTime()) / (24 * 60 * 60 * 1000));
  if (days < 1) return '今天';
  if (days < 7) return `${days} 天前`;
  if (days < 30) return `${Math.floor(days / 7)} 周前`;
  return `${Math.floor(days / 30)} 月前`;
});
</script>

<template>
  <!-- Hero -->
  <section class="relative -mt-4">
    <div aria-hidden="true" class="pointer-events-none absolute inset-x-0 -top-10 -z-10 mx-auto h-72 max-w-3xl rounded-full blur-3xl"
         style="background: radial-gradient(closest-side, var(--accent-glow), transparent 70%);"></div>
    <div class="grid gap-12 md:grid-cols-5 md:items-center">
      <div class="md:col-span-3">
        <div class="mb-5 inline-flex items-center gap-2 rounded-full border border-accent/40 bg-accent/5 px-3 py-1 text-xs font-medium text-accent">
          <span class="pulse-dot"></span>
          实时采集 · 上次更新 {{ lastUpdatedRel }}
        </div>
        <h1 class="text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl">
          别再被<span class="text-gradient">同一个坑</span><br class="hidden md:block" />绊倒两次
        </h1>
        <p class="mt-5 max-w-2xl text-lg leading-relaxed text-ink-600 dark:text-ink-300">
          我们抓取 GitHub Issues / 官方博客 / HN / Reddit / 知乎等全网关于
          <strong>AI Agent 开发避坑</strong> 的讨论，
          去重、归类、给出可执行的修复方案。
          每条都附公开来源，可以直接顺藤摸瓜。
        </p>
        <div class="mt-7 flex flex-wrap gap-3">
          <router-link to="/pitfalls" class="btn-primary">
            浏览避坑库
            <span aria-hidden="true">→</span>
          </router-link>
          <router-link to="/contributing" class="btn-ghost">如何贡献</router-link>
          <a href="https://github.com/agent-pitfalls/agent-pitfalls" rel="noopener" class="btn-ghost">
            GitHub
            <span aria-hidden="true">↗</span>
          </a>
        </div>
        <p class="mt-4 text-xs text-ink-500">
          内容采用 <a class="underline" href="/LICENSE">MIT</a> 协议开源 · 数据每周自动更新
        </p>
      </div>
      <div class="md:col-span-2">
        <div class="card card-hover anim-fade-up">
          <p class="text-xs font-medium uppercase tracking-wider text-ink-500">数据快照</p>
          <div class="mt-4 space-y-4">
            <div class="flex items-baseline justify-between border-b border-ink-100 pb-3 dark:border-ink-800">
              <div>
                <div class="text-3xl font-bold tabular-nums text-accent">{{ total.toLocaleString() }}</div>
                <div class="mt-0.5 text-xs text-ink-500">已收录条目</div>
              </div>
              <div class="text-right text-xs text-ink-500">
                覆盖 {{ platformCount }} 个平台
              </div>
            </div>
            <div class="grid grid-cols-2 gap-3 text-sm">
              <div class="flex items-center gap-2">
                <span class="badge badge-critical">critical</span>
                <span class="tabular-nums font-semibold">{{ criticalCount }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="badge badge-high">high</span>
                <span class="tabular-nums font-semibold">{{ highCount }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="badge badge-low">已验证</span>
                <span class="tabular-nums font-semibold">{{ verifiedCount }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="badge">含修复</span>
                <span class="tabular-nums font-semibold">{{ withFixesCount }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2 border-t border-ink-100 pt-3 text-xs text-ink-500 dark:border-ink-800">
              <span class="pulse-dot"></span>
              本周新增 {{ recentCount }} 条
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Trending -->
  <section v-if="topCategories.length" class="mt-16">
    <div class="mb-4 flex items-end justify-between">
      <h2 class="text-lg font-semibold">热门分类</h2>
      <router-link to="/pitfalls" class="text-sm text-accent hover:underline">全部 →</router-link>
    </div>
    <div class="row-pills -mx-4 flex gap-2 overflow-x-auto px-4 py-2">
      <router-link
        v-for="c in topCategories"
        :key="c.name"
        :to="`/pitfalls?category=${c.name}`"
        class="chip flex-shrink-0 hover-lift"
      >
        <span>#{{ c.name }}</span>
        <span class="text-ink-500 tabular-nums">{{ c.count }}</span>
      </router-link>
    </div>
  </section>

  <!-- Featured -->
  <section class="mt-16">
    <div class="mb-6 flex items-end justify-between">
      <div>
        <h2 class="text-2xl font-semibold">最新收录</h2>
        <p class="mt-1 text-sm text-ink-500">按收录时间倒序，共 {{ total }} 条</p>
      </div>
      <router-link to="/pitfalls" class="text-sm text-accent hover:underline">查看全部 →</router-link>
    </div>
    <div class="stagger grid gap-4 md:grid-cols-2">
      <PitfallCard v-for="p in featured" :key="p.id" :pitfall="p" show-arrow />
    </div>
  </section>

  <!-- How it works -->
  <section class="mt-20">
    <h2 class="text-2xl font-semibold">采集管线</h2>
    <p class="mt-2 text-sm text-ink-500">三步走：抓全网 → 清洗去重 → 结构化抽取</p>
    <div class="mt-6 grid gap-4 md:grid-cols-3">
      <div class="card card-hover">
        <div class="flex items-center gap-3">
          <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/10 text-base font-bold text-accent">1</div>
          <h3 class="font-semibold">采集</h3>
        </div>
        <p class="mt-3 text-sm leading-relaxed text-ink-600 dark:text-ink-300">
          28 个 source 并行抓取 GitHub Issues / RSS 博客 / HN / Reddit 镜像 / 知乎替代源等。
          项目自带的 <code class="rounded bg-ink-100 px-1 py-0.5 text-xs dark:bg-ink-800">collectors/</code> 全部可重跑。
        </p>
      </div>
      <div class="card card-hover">
        <div class="flex items-center gap-3">
          <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/10 text-base font-bold text-accent">2</div>
          <h3 class="font-semibold">清洗去重</h3>
        </div>
        <p class="mt-3 text-sm leading-relaxed text-ink-600 dark:text-ink-300">
          通过 URL 指纹 + 标题相似度合并重复问题，
          用关键词矩阵 + 标题语义过滤掉营销噪声与无关内容。
        </p>
      </div>
      <div class="card card-hover">
        <div class="flex items-center gap-3">
          <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/10 text-base font-bold text-accent">3</div>
          <h3 class="font-semibold">结构化抽取</h3>
        </div>
        <p class="mt-3 text-sm leading-relaxed text-ink-600 dark:text-ink-300">
          从 markdown body 自动抓 symptoms / root causes / fixes 三段，
          加上 severity / platforms / categories 标签。
          每条都附公开来源，可以直接顺藤摸瓜。
        </p>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="mt-20">
    <div class="card overflow-hidden text-center" style="background: linear-gradient(135deg, oklch(from var(--accent) l c h / 0.08), oklch(from var(--accent) l c h / 0.02));">
      <h2 class="text-xl font-semibold">踩过坑？贡献你的发现</h2>
      <p class="mt-2 text-sm text-ink-600 dark:text-ink-300">
        PR-driven 工作流 — 任何人都能在 GitHub 上提交新坑、补充修复方案、或追加来源链接。
      </p>
      <div class="mt-5 flex flex-wrap justify-center gap-3">
        <router-link to="/contributing" class="btn-primary">贡献指南</router-link>
        <router-link to="/about" class="btn-ghost">关于项目</router-link>
      </div>
    </div>
  </section>
</template>