<template>
  <footer class="mt-20 border-t border-ink-100 py-10 text-center text-xs text-ink-500 dark:border-ink-800 dark:text-ink-400">
    <div class="container-page flex flex-col items-center justify-between gap-2 md:flex-row">
      <p>© {{ year }} Agent Pitfalls · 内容采用 <a class="underline" href="/LICENSE">MIT</a> 协议</p>
      <p>采集自全网 · 社区维护 · 欢迎 <router-link class="underline" to="/contributing">贡献</router-link></p>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>