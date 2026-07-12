import { computed } from 'vue';
import manifest from '../data/manifest.json';

// 全部 pitfalls（按 discovered_at 倒序）
const sorted = [...manifest].sort((a, b) => {
  const ta = a.discovered_at ? new Date(a.discovered_at).getTime() : 0;
  const tb = b.discovered_at ? new Date(b.discovered_at).getTime() : 0;
  return tb - ta;
});

export function usePitfalls() {
  const all = computed(() => sorted);
  const total = computed(() => all.value.length);

  const criticalCount = computed(() =>
    all.value.filter((p) => p.severity === 'critical').length,
  );
  const highCount = computed(() =>
    all.value.filter((p) => p.severity === 'high').length,
  );
  const verifiedCount = computed(() => all.value.filter((p) => p.verified).length);
  const withFixesCount = computed(() => all.value.filter((p) => p.fixes.length > 0).length);
  const platformCount = computed(() => new Set(all.value.flatMap((p) => p.platforms)).size);

  const topCategories = computed(() => {
    const m = new Map();
    for (const p of all.value) {
      for (const c of p.categories) m.set(c, (m.get(c) ?? 0) + 1);
    }
    return [...m.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([name, count]) => ({ name, count }));
  });

  const severityCounts = computed(() => ({
    critical: all.value.filter((p) => p.severity === 'critical').length,
    high: all.value.filter((p) => p.severity === 'high').length,
    medium: all.value.filter((p) => p.severity === 'medium').length,
    low: all.value.filter((p) => p.severity === 'low').length,
  }));

  const categories = computed(() =>
    [...new Set(all.value.flatMap((p) => p.categories))].sort(),
  );
  const platforms = computed(() =>
    [...new Set(all.value.flatMap((p) => p.platforms))].sort(),
  );

  function findById(id) {
    return all.value.find((p) => p.id === id) || null;
  }

  function related(p, limit = 4) {
    if (!p) return [];
    return all.value
      .filter(
        (e) =>
          e.id !== p.id &&
          (e.categories.some((c) => p.categories.includes(c)) ||
            e.platforms.some((pl) => p.platforms.includes(pl))),
      )
      .slice(0, limit);
  }

  function neighbors(p) {
    if (!p) return { prev: null, next: null };
    const idx = all.value.findIndex((x) => x.id === p.id);
    return {
      prev: idx > 0 ? all.value[idx - 1] : null,
      next: idx < all.value.length - 1 ? all.value[idx + 1] : null,
    };
  }

  return {
    all,
    total,
    criticalCount,
    highCount,
    verifiedCount,
    withFixesCount,
    platformCount,
    topCategories,
    severityCounts,
    categories,
    platforms,
    findById,
    related,
    neighbors,
  };
}