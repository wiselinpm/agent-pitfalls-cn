/**
 * Site-wide constants. Single source of truth for repo URL,
 * brand name, etc. — tweak here, propagates everywhere.
 *
 * Keep in sync with `astro.config.mjs` `site` (used by sitemap + RSS).
 */

export const SITE_CONFIG = {
  /** GitHub repo. Must match `git remote get-url origin` after stripping .git. */
  github: 'https://github.com/wiselinpm/agent-pitfalls-cn',
  /** Repo path used for "edit on GitHub" links — owner/repo only, no scheme. */
  githubRepo: 'wiselinpm/agent-pitfalls-cn',
  /** Default branch for "edit on GitHub" links. */
  githubBranch: 'main',
  /** Brand name. */
  name: 'Agent Pitfalls',
} as const;
