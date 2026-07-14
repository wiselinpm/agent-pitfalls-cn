import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const items = (await getCollection('pitfalls'))
    .sort((a, b) => +new Date(b.data.discovered_at ?? 0) - +new Date(a.data.discovered_at ?? 0))
    .slice(0, 50);

  // `context.site` 是 astro.config 里的 `site`；`context.url` 是当前请求 URL。
  // rss.xml.js 是 endpoint，不是 page；没有 `import.meta.env.BASE_URL`，
  // 通过 context.url 拿到 runtime base，然后拼绝对 URL。
  // GitHub Pages 项目页：URL = `${site}${context.url.pathname.replace(/\/rss\.xml$/, '')}p itfalls/${id}`
  const site = String(context.site ?? 'https://wiselinpm.github.io').replace(/\/$/, '');
  const base = context.url.pathname.replace(/\/rss\.xml$/, ''); // e.g. "/agent-pitfalls-cn" or "/"
  const linkFor = (id) => `${site}${base}/pitfalls/${id}`;

  return rss({
    title: 'Agent Pitfalls',
    description: '全网 agent 开发避坑信息整合',
    site: `${site}${base}`,
    items: items.map((p) => ({
      title: p.data.title,
      description: p.data.summary,
      pubDate: new Date(p.data.discovered_at ?? Date.now()),
      link: linkFor(p.id),
      categories: [...p.data.categories, ...p.data.platforms, p.data.severity],
    })),
    customData: '<language>zh-cn</language>',
  });
}
