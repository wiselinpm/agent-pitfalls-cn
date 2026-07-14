/**
 * Path helpers — Astro `base` 不会被自动拼到硬编码 `href="/..."` 上。
 * 这里提供一个 `withBase()` 统一处理。
 *
 * - `BASE`: 来自 vite 的 `import.meta.env.BASE_URL`，等于 `astro.config.mjs` 里的 `base`
 *           在 SSR 里 `import.meta.env` 不可用，回落到 `Astro` 全局拿 base
 * - `withBase('/pitfalls')` → 在 base='/' 时返回 '/pitfalls'，
 *                              在 base='/agent-pitfalls-cn' 时返回 '/agent-pitfalls-cn/pitfalls'
 */

export const BASE = (import.meta.env?.BASE_URL ?? '/').replace(/\/$/, '');

export function withBase(path: string): string {
  if (!path || path.startsWith('http')) return path;
  const cleaned = path.startsWith('/') ? path : `/${path}`;
  return `${BASE}${cleaned}` || cleaned;
}
