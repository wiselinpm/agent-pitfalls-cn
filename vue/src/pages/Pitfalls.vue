<script setup>
import { computed, ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { usePitfalls } from '../composables/useContent';
import PitfallCard from '../components/PitfallCard.vue';

const route = useRoute();
const { all, severityCounts, categories, platforms } = usePitfalls();

const search = ref('');
const activeSeverity = ref('');
const activeCategories = ref(new Set());
const platform = ref('');

// 从 URL query 同步到 state（首次 mount + 路由变化）
function syncFromQuery() {
  const q = route.query;
  if (q.q) search.value = String(q.q);
  if (q.severity) activeSeverity.value = String(q.severity);
  if (q.platform) platform.value = String(q.platform);
  if (q.category) {
    activeCategories.value = new Set([String(q.category)]);
  } else if (Object.keys(q).length === 0) {
    // 没有任何 query → 清空筛选
    search.value = '';
    activeSeverity.value = '';
    platform.value = '';
    activeCategories.value.clear();
    activeCategories.value = new Set();
  }
}

onMounted(syncFromQuery);
watch(() => route.query, syncFromQuery);

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase();
  return all.value.filter((p) => {
    const matchQ = !q || p.title.toLowerCase().includes(q) || p.summary.toLowerCase().includes(q);
    const matchS = !activeSeverity.value || p.severity === activeSeverity.value;
    const matchP = !platform.value || p.platforms.includes(platform.value);
    const matchC = activeCategories.value.size === 0 || p.categories.some((c) => activeCategories.value.has(c));
    return matchQ && matchS && matchP && matchC;
  });
});

const visibleCount = computed(() => filtered.value.length);
const total = computed(() => all.value.length);

function toggleSeverity(v) {
  activeSeverity.value = activeSeverity.value === v ? '' : v;
}
function toggleCategory(v) {
  if (activeCategories.value.has(v)) activeCategories.value.delete(v);
  else activeCategories.value.add(v);
  activeCategories.value = new Set(activeCategories.value); // trigger reactivity
}

function removeChip(kind, value) {
  if (kind === 'severity') activeSeverity.value = '';
  else if (kind === 'platform') platform.value = '';
  else if (kind === 'category') {
    activeCategories.value.delete(value);
    activeCategories.value = new Set(activeCategories.value);
  } else if (kind === 'search') search.value = '';
}

const activeChips = computed(() => {
  const chips = [];
  if (activeSeverity.value) chips.push({ kind: 'severity', value: activeSeverity.value, label: activeSeverity.value });
  if (platform.value) chips.push({ kind: 'platform', value: platform.value, label: platform.value });
  for (const c of activeCategories.value) chips.push({ kind: 'category', value: c, label: '#' + c });
  if (search.value.trim()) chips.push({ kind: 'search', value: search.value.trim(), label: '「' + search.value.trim() + '」' });
  return chips;
});

function clearAll() {
  search.value = '';
  platform.value = '';
  activeSeverity.value = '';
  activeCategories.value.clear();
  activeCategories.value = new Set();
}

// ⌘K 快捷键
function onKeydown(e) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    const el = document.getElementById('search');
    if (el) { el.focus(); el.select(); }
  }
  if (e.key === 'Escape' && document.activeElement?.id === 'search') {
    search.value = '';
    document.activeElement.blur();
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown));
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown));
</script>

<template>
  <header class="mb-8">
    <div class="flex items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">避坑库</h1>
        <p class="mt-1 text-ink-600 dark:text-ink-300">
          <span class="font-semibold tabular-nums text-ink-900 dark:text-ink-100">{{ visibleCount }}</span>
          <span> / {{ total }} 条 · 按严重程度与平台筛选</span>
        </p>
      </div>
      <div class="hidden items-center gap-1.5 rounded-lg border border-ink-200 px-2 py-1 text-xs text-ink-500 md:flex dark:border-ink-700">
        <kbd class="rounded bg-ink-100 px-1.5 py-0.5 font-mono text-[10px] dark:bg-ink-800">⌘</kbd>
        <kbd class="rounded bg-ink-100 px-1.5 py-0.5 font-mono text-[10px] dark:bg-ink-800">K</kbd>
        <span class="ml-1">搜索</span>
      </div>
    </div>
  </header>

  <div class="card mb-6">
    <div class="relative">
      <span aria-hidden="true" class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-400">🔍</span>
      <input
        id="search"
        v-model="search"
        type="search"
        placeholder="按标题、症状、根因搜索…"
        class="w-full rounded-lg border border-ink-200 bg-white py-2.5 pl-10 pr-4 text-sm focus:border-accent focus:outline-none dark:border-ink-700 dark:bg-ink-900"
      />
    </div>
    <div class="mt-4 grid gap-3 md:grid-cols-2">
      <div>
        <p class="mb-2 text-xs font-medium uppercase tracking-wider text-ink-500">严重程度</p>
        <div class="row-pills -mx-1 flex gap-1.5 overflow-x-auto px-1 py-1">
          <button
            type="button"
            class="chip flex-shrink-0"
            :aria-pressed="activeSeverity === '' ? 'true' : 'false'"
            @click="toggleSeverity('')"
          >
            全部 <span class="text-ink-500 tabular-nums">{{ total }}</span>
          </button>
          <button
            v-for="s in (['critical', 'high', 'medium', 'low'])"
            :key="s"
            type="button"
            class="chip flex-shrink-0"
            :class="`badge-${s}`"
            :aria-pressed="activeSeverity === s ? 'true' : 'false'"
            @click="toggleSeverity(s)"
          >
            {{ s }} <span class="opacity-70 tabular-nums">{{ severityCounts[s] }}</span>
          </button>
        </div>
      </div>
      <div>
        <p class="mb-2 text-xs font-medium uppercase tracking-wider text-ink-500">平台</p>
        <select
          v-model="platform"
          class="w-full rounded-lg border border-ink-200 bg-white px-3 py-2 text-sm focus:border-accent focus:outline-none dark:border-ink-700 dark:bg-ink-900"
        >
          <option value="">全部平台</option>
          <option v-for="p in platforms" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>
    </div>
    <div class="mt-4">
      <p class="mb-2 text-xs font-medium uppercase tracking-wider text-ink-500">分类（可多选）</p>
      <div class="row-pills -mx-1 flex gap-1.5 overflow-x-auto px-1 py-1">
        <button
          v-for="c in categories"
          :key="c"
          type="button"
          class="chip flex-shrink-0"
          :aria-pressed="activeCategories.has(c) ? 'true' : 'false'"
          @click="toggleCategory(c)"
        >#{{ c }}</button>
      </div>
    </div>
    <div v-if="activeChips.length" class="mt-4 flex flex-wrap items-center gap-2 border-t border-ink-100 pt-4 text-xs dark:border-ink-800">
      <span class="text-ink-500">已应用：</span>
      <button
        v-for="c in activeChips"
        :key="c.kind + ':' + c.value"
        type="button"
        class="inline-flex items-center gap-1 rounded-full bg-accent/10 px-2.5 py-1 text-xs font-medium text-accent hover:bg-accent/20"
        @click="removeChip(c.kind, c.value)"
      > {{ c.label }} <span aria-hidden="true">×</span></button>
      <button type="button" class="ml-auto text-accent hover:underline" @click="clearAll">清空全部</button>
    </div>
  </div>

  <div v-if="filtered.length" class="stagger grid gap-3">
    <PitfallCard v-for="p in filtered" :key="p.id" :pitfall="p" show-arrow />
  </div>

  <div v-else class="mt-10">
    <div class="mx-auto max-w-md rounded-2xl border border-dashed border-ink-200 p-10 text-center dark:border-ink-700">
      <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-ink-100 text-2xl dark:bg-ink-800">
        🔍
      </div>
      <h3 class="mt-4 text-base font-semibold">没有匹配的条目</h3>
      <p class="mt-1 text-sm text-ink-500">
        试试放宽筛选条件，或者
        <button type="button" class="text-accent underline" @click="clearAll">清空全部筛选</button>。
      </p>
    </div>
  </div>
</template>