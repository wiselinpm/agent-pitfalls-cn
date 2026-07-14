/**
 * 纯函数分页工具 — 不依赖 Astro，可在脚本里复用
 */

export interface PageInfo<T> {
  page: number;
  perPage: number;
  total: number;
  totalPages: number;
  items: T[];
  hasPrev: boolean;
  hasNext: boolean;
}

export function paginate<T>(items: readonly T[], page: number, perPage: number): PageInfo<T> {
  const total = items.length;
  const totalPages = Math.max(1, Math.ceil(total / perPage));
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * perPage;
  return {
    page: safePage,
    perPage,
    total,
    totalPages,
    items: items.slice(start, start + perPage),
    hasPrev: safePage > 1,
    hasNext: safePage < totalPages,
  };
}

export const DEFAULT_PER_PAGE = 50;