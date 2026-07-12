<script setup>
defineProps({
  pitfall: { type: Object, required: true },
  showArrow: { type: Boolean, default: false },
});
</script>

<template>
  <router-link
    :to="`/pitfalls/${pitfall.id}`"
    class="card card-hover group block"
  >
    <div class="flex flex-wrap items-start gap-3">
      <div class="min-w-0 flex-1">
        <div class="flex flex-wrap items-center gap-2">
          <span class="badge" :class="`badge-${pitfall.severity}`">{{ pitfall.severity }}</span>
          <span
            v-for="pl in pitfall.platforms.slice(0, 2)"
            :key="pl"
            class="badge"
          >{{ pl }}</span>
          <span v-if="pitfall.verified" class="badge badge-low">✓</span>
        </div>
        <h3 class="mt-2 text-lg font-semibold leading-snug group-hover:text-accent">
          {{ pitfall.title }}
        </h3>
        <p class="mt-1.5 line-clamp-2 text-sm text-ink-600 dark:text-ink-300">
          {{ pitfall.summary }}
        </p>
        <div class="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-ink-500">
          <span v-for="c in pitfall.categories.slice(0, 3)" :key="c" class="hover:text-accent">#{{ c }}</span>
          <span class="ml-auto tabular-nums">{{ pitfall.discovered_at || '—' }}</span>
        </div>
      </div>
      <span
        v-if="showArrow"
        aria-hidden="true"
        class="hidden self-center text-ink-300 transition-transform group-hover:translate-x-1 group-hover:text-accent md:block"
      >→</span>
    </div>
  </router-link>
</template>