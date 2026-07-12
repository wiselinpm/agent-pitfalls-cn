<script setup>
import { computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { marked } from 'marked';
import { usePitfalls } from '../composables/useContent';
import PitfallCard from '../components/PitfallCard.vue';

const route = useRoute();
const { findById, related, neighbors } = usePitfalls();

const pitfall = computed(() => findById(route.params.id));
const relatedList = computed(() => related(pitfall.value));
const nav = computed(() => neighbors(pitfall.value));

const bodyHtml = computed(() => {
  if (!pitfall.value?.body) return '';
  try {
    return marked.parse(pitfall.value.body, { breaks: true, gfm: true });
  } catch {
    return '';
  }
});

const severityTone = {
  critical: 'text-red-500 dark:text-red-400',
  high: 'text-orange-500 dark:text-orange-400',
  medium: 'text-yellow-600 dark:text-yellow-400',
  low: 'text-emerald-500 dark:text-emerald-400',
};

// Reading progress bar
function updateProgress() {
  const bar = document.getElementById('reading-progress');
  if (!bar || !pitfall.value) return;
  const article = document.querySelector('article');
  if (!article) return;
  const rect = article.getBoundingClientRect();
  const total = article.scrollHeight;
  const scrolled = -rect.top + window.innerHeight * 0.2;
  const pct = Math.max(0, Math.min(1, scrolled / total));
  bar.style.transform = `scaleX(${pct})`;
}

let raf = null;
function onScroll() {
  if (raf) return;
  raf = requestAnimationFrame(() => {
    updateProgress();
    raf = null;
  });
}

let scrollTimer = null;
watch(pitfall, () => {
  // 滚动到顶部
  window.scrollTo({ top: 0 });
  if (scrollTimer) clearTimeout(scrollTimer);
  scrollTimer = setTimeout(updateProgress, 100);
});

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true });
  updateProgress();
});
onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll);
  if (raf) cancelAnimationFrame(raf);
  if (scrollTimer) clearTimeout(scrollTimer);
});
</script>

<template>
  <template v-if="!pitfall">
    <div class="card text-center">
      <h1 class="text-2xl font-bold">未找到该条目</h1>
      <p class="mt-2 text-ink-500">id: <code>{{ route.params.id }}</code></p>
      <router-link to="/pitfalls" class="btn-primary mt-4">返回避坑库</router-link>
    </div>
  </template>

  <template v-else>
    <div class="fixed inset-x-0 top-0 z-50 h-0.5 bg-transparent">
      <div id="reading-progress" class="h-full origin-left bg-accent transition-transform" style="transform: scaleX(0);"></div>
    </div>

    <nav class="mb-6 flex items-center gap-2 text-sm text-ink-500">
      <router-link to="/pitfalls" class="hover:text-accent">← 避坑库</router-link>
      <span aria-hidden="true">/</span>
      <span class="truncate text-ink-700 dark:text-ink-200">{{ pitfall.title }}</span>
    </nav>

    <div class="grid gap-10 lg:grid-cols-[1fr_280px]">
      <article class="prose prose-neutral max-w-none dark:prose-invert prose-tight anim-fade-up min-w-0">
        <header class="not-prose">
          <div class="flex flex-wrap items-center gap-2">
            <span class="badge" :class="`badge-${pitfall.severity}`">{{ pitfall.severity }}</span>
            <span v-for="pl in pitfall.platforms" :key="pl" class="badge">{{ pl }}</span>
            <span v-if="pitfall.verified" class="badge badge-low">✓ 已验证</span>
          </div>
          <h1 class="mt-4 text-3xl font-bold tracking-tight md:text-4xl">{{ pitfall.title }}</h1>
          <p class="mt-3 text-lg leading-relaxed text-ink-600 dark:text-ink-300">{{ pitfall.summary }}</p>
        </header>

        <section v-if="pitfall.symptoms.length" class="not-prose mt-10">
          <div class="flex items-baseline gap-3">
            <h2 class="text-lg font-semibold">🚨 症状</h2>
            <span class="text-xs text-ink-500">怎么识别自己撞上了这个坑</span>
          </div>
          <ul class="mt-3 space-y-2">
            <li v-for="(s, i) in pitfall.symptoms" :key="i" class="flex gap-3 rounded-lg border border-red-200 bg-red-50/60 p-3 text-sm dark:border-red-900/60 dark:bg-red-950/30">
              <span aria-hidden="true" class="mt-0.5 text-red-500">•</span>
              <span>{{ s }}</span>
            </li>
          </ul>
        </section>

        <section v-if="pitfall.root_causes.length" class="not-prose mt-8">
          <div class="flex items-baseline gap-3">
            <h2 class="text-lg font-semibold">🧠 根因</h2>
            <span class="text-xs text-ink-500">为什么会发生</span>
          </div>
          <ul class="mt-3 space-y-2">
            <li v-for="(s, i) in pitfall.root_causes" :key="i" class="flex gap-3 rounded-lg border border-amber-200 bg-amber-50/60 p-3 text-sm dark:border-amber-900/60 dark:bg-amber-950/30">
              <span aria-hidden="true" class="mt-0.5 text-amber-500">•</span>
              <span>{{ s }}</span>
            </li>
          </ul>
        </section>

        <section v-if="pitfall.fixes.length" class="not-prose mt-8">
          <div class="flex items-baseline gap-3">
            <h2 class="text-lg font-semibold">🛠️ 修复 / 缓解</h2>
            <span class="text-xs text-ink-500">推荐方案</span>
          </div>
          <ul class="mt-3 space-y-2">
            <li v-for="(s, i) in pitfall.fixes" :key="i" class="flex gap-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 text-sm dark:border-emerald-900/60 dark:bg-emerald-950/30">
              <span aria-hidden="true" class="mt-0.5 text-emerald-500">✓</span>
              <span>{{ s }}</span>
            </li>
          </ul>
        </section>

        <section v-if="bodyHtml" class="mt-10">
          <div v-html="bodyHtml"></div>
        </section>

        <section v-if="pitfall.references.length" class="not-prose mt-10">
          <h2 class="text-lg font-semibold">📚 参考来源</h2>
          <ul class="mt-3 space-y-2">
            <li v-for="(r, i) in pitfall.references" :key="i" class="flex items-start gap-2 rounded-lg border border-ink-200 bg-ink-50/60 p-3 text-sm hover:border-accent dark:border-ink-800 dark:bg-ink-900/40">
              <span aria-hidden="true" class="mt-0.5 text-accent">↗</span>
              <a :href="r.url" target="_blank" rel="noopener noreferrer" class="min-w-0 flex-1 font-medium underline-offset-2 hover:underline">
                {{ r.title }}
              </a>
              <span v-if="r.source" class="flex-shrink-0 rounded bg-ink-200 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-ink-700 dark:bg-ink-800 dark:text-ink-300">{{ r.source }}</span>
            </li>
          </ul>
        </section>

        <nav class="not-prose mt-14 grid gap-3 border-t border-ink-100 pt-8 sm:grid-cols-2 dark:border-ink-800">
          <router-link v-if="nav.prev" :to="`/pitfalls/${nav.prev.id}`" class="card card-hover group">
            <p class="text-xs uppercase tracking-wider text-ink-500">← 上一条</p>
            <p class="mt-2 line-clamp-2 text-sm font-medium group-hover:text-accent">{{ nav.prev.title }}</p>
          </router-link>
          <div v-else></div>
          <router-link v-if="nav.next" :to="`/pitfalls/${nav.next.id}`" class="card card-hover group sm:text-right">
            <p class="text-xs uppercase tracking-wider text-ink-500">下一条 →</p>
            <p class="mt-2 line-clamp-2 text-sm font-medium group-hover:text-accent">{{ nav.next.title }}</p>
          </router-link>
        </nav>

        <footer class="not-prose mt-10 flex flex-wrap items-center gap-3 text-sm text-ink-500">
          <span>收录于 <strong class="text-ink-700 dark:text-ink-300">{{ pitfall.discovered_at || '未注明' }}</strong></span>
          <span>·</span>
          <span>贡献者 <strong class="text-ink-700 dark:text-ink-300">{{ pitfall.contributor }}</strong></span>
          <a :href="`https://github.com/agent-pitfalls/agent-pitfalls/edit/main/web/src/content/pitfalls/${pitfall.id}.md`"
             target="_blank" rel="noopener noreferrer"
             class="ml-auto inline-flex items-center gap-1 text-accent hover:underline">
            在 GitHub 上编辑
            <span aria-hidden="true">↗</span>
          </a>
        </footer>
      </article>

      <aside class="hidden lg:block">
        <div class="sticky top-20 space-y-4">
          <div class="card anim-fade-up">
            <p class="text-xs font-medium uppercase tracking-wider text-ink-500">TL;DR</p>
            <p class="mt-3 text-sm leading-relaxed text-ink-700 dark:text-ink-200">{{ pitfall.summary }}</p>
            <dl class="mt-5 space-y-3 text-sm">
              <div>
                <dt class="text-xs uppercase tracking-wider text-ink-500">严重程度</dt>
                <dd :class="['mt-1 font-semibold capitalize', severityTone[pitfall.severity]]">{{ pitfall.severity }}</dd>
              </div>
              <div>
                <dt class="text-xs uppercase tracking-wider text-ink-500">涉及平台</dt>
                <dd class="mt-1 flex flex-wrap gap-1">
                  <span v-for="p in pitfall.platforms" :key="p" class="badge">{{ p }}</span>
                </dd>
              </div>
              <div v-if="pitfall.categories.length">
                <dt class="text-xs uppercase tracking-wider text-ink-500">分类</dt>
                <dd class="mt-1 flex flex-wrap gap-1">
                  <span v-for="c in pitfall.categories" :key="c" class="badge">#{{ c }}</span>
                </dd>
              </div>
              <div class="grid grid-cols-2 gap-3 border-t border-ink-100 pt-3 dark:border-ink-800">
                <div>
                  <dt class="text-xs uppercase tracking-wider text-ink-500">症状</dt>
                  <dd class="mt-1 text-lg font-bold tabular-nums">{{ pitfall.symptoms.length }}</dd>
                </div>
                <div>
                  <dt class="text-xs uppercase tracking-wider text-ink-500">修复</dt>
                  <dd class="mt-1 text-lg font-bold tabular-nums text-emerald-600 dark:text-emerald-400">{{ pitfall.fixes.length }}</dd>
                </div>
              </div>
              <div v-if="pitfall.verified" class="flex items-center gap-2 rounded-lg bg-emerald-50 px-3 py-2 text-xs font-medium text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                <span>✓</span>
                已通过社区验证
              </div>
            </dl>
          </div>

          <div v-if="relatedList.length" class="card">
            <p class="text-xs font-medium uppercase tracking-wider text-ink-500">相关条目</p>
            <ul class="mt-3 space-y-3">
              <li v-for="r in relatedList" :key="r.id">
                <router-link :to="`/pitfalls/${r.id}`" class="group block">
                  <div class="flex items-center gap-1.5">
                    <span class="badge" :class="`badge-${r.severity}`">{{ r.severity }}</span>
                  </div>
                  <p class="mt-1 line-clamp-2 text-sm font-medium leading-snug group-hover:text-accent">{{ r.title }}</p>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </aside>
    </div>
  </template>
</template>