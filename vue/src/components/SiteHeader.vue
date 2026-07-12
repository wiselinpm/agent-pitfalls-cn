<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useTheme } from '../composables/useTheme';

const route = useRoute();
const router = useRouter();
const { theme, toggle } = useTheme();

const navItems = [
  { href: '/', label: '首页', match: (p) => p === '/' },
  { href: '/pitfalls', label: '避坑库', match: (p) => p.startsWith('/pitfalls') },
  { href: '/advisories', label: '安全公告', match: (p) => p.startsWith('/advisories') },
  { href: '/patterns', label: '应对模式', match: (p) => p.startsWith('/patterns') },
  { href: '/about', label: '关于', match: (p) => p === '/about' || p === '/contributing' },
];

const mobileOpen = ref(false);

function goToSearch() {
  if (route.path.startsWith('/pitfalls')) {
    const el = document.getElementById('search');
    if (el) {
      el.focus();
      el.select();
    }
  } else {
    router.push('/pitfalls');
    setTimeout(() => {
      const el = document.getElementById('search');
      if (el) el.focus();
    }, 200);
  }
}

function onKeydown(e) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    goToSearch();
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown));
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown));
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-ink-100/80 bg-white/70 backdrop-blur-md dark:border-ink-800 dark:bg-ink-900/70">
    <div class="container-page flex h-16 items-center justify-between">
      <router-link to="/" class="group flex items-center gap-2.5 font-semibold tracking-tight">
        <span class="inline-flex h-7 w-7 items-center justify-center rounded-lg bg-accent text-white shadow-sm transition-transform group-hover:rotate-3">
          <span class="text-sm font-bold">⚠</span>
        </span>
        <span class="hidden sm:inline">Agent Pitfalls</span>
      </router-link>
      <nav class="hidden gap-1 text-sm md:flex">
        <template v-for="item in navItems" :key="item.href">
          <router-link
            :to="item.href"
            class="rounded-lg px-3 py-1.5 transition-colors"
            :class="item.match(route.path)
              ? 'bg-accent/10 font-medium text-accent'
              : 'text-ink-600 hover:bg-ink-100 hover:text-ink-900 dark:text-ink-300 dark:hover:bg-ink-800 dark:hover:text-ink-100'"
          >
            {{ item.label }}
          </router-link>
        </template>
        <a
          href="https://github.com/agent-pitfalls/agent-pitfalls"
          rel="noopener"
          class="rounded-lg px-3 py-1.5 text-ink-600 transition-colors hover:bg-ink-100 hover:text-ink-900 dark:text-ink-300 dark:hover:bg-ink-800 dark:hover:text-ink-100"
        >GitHub ↗</a>
      </nav>
      <div class="flex items-center gap-1">
        <button
          type="button"
          aria-label="搜索"
          @click="goToSearch"
          class="hidden h-9 items-center gap-2 rounded-lg border border-ink-200 px-3 text-xs text-ink-500 transition-colors hover:border-accent hover:text-accent md:inline-flex dark:border-ink-700"
        >
          <span aria-hidden="true">🔍</span>
          <span class="hidden lg:inline">搜索</span>
          <kbd class="rounded bg-ink-100 px-1.5 font-mono text-[10px] leading-5 dark:bg-ink-800">⌘K</kbd>
        </button>
        <button
          aria-label="切换主题"
          @click="toggle"
          class="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-ink-200 text-base transition-all hover:border-accent hover:text-accent dark:border-ink-700"
        >🌓</button>
        <button
          aria-label="菜单"
          @click="mobileOpen = !mobileOpen"
          class="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-ink-200 text-base transition-all hover:border-accent md:hidden dark:border-ink-700"
        >☰</button>
      </div>
    </div>
    <div
      v-if="mobileOpen"
      class="border-t border-ink-100 md:hidden dark:border-ink-800"
    >
      <nav class="container-page flex flex-col gap-1 py-3">
        <template v-for="item in navItems" :key="item.href">
          <router-link
            :to="item.href"
            @click="mobileOpen = false"
            class="rounded-lg px-3 py-2 text-sm hover:bg-ink-100 dark:hover:bg-ink-800"
          >{{ item.label }}</router-link>
        </template>
        <a
          href="https://github.com/agent-pitfalls/agent-pitfalls"
          rel="noopener"
          class="rounded-lg px-3 py-2 text-sm hover:bg-ink-100 dark:hover:bg-ink-800"
        >GitHub ↗</a>
      </nav>
    </div>
  </header>
</template>