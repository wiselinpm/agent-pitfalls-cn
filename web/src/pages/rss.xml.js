import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const items = (await getCollection('pitfalls'))
    .sort((a, b) => +new Date(b.data.discovered_at ?? 0) - +new Date(a.data.discovered_at ?? 0))
    .slice(0, 50);
  return rss({
    title: 'Agent Pitfalls',
    description: '全网 agent 开发避坑信息整合',
    site: context.site ?? 'https://agent-pitfalls.dev',
    items: items.map((p) => ({
      title: p.data.title,
      description: p.data.summary,
      pubDate: new Date(p.data.discovered_at ?? Date.now()),
      link: `/pitfalls/${p.id}`,
      categories: [...p.data.categories, ...p.data.platforms, p.data.severity],
    })),
    customData: '<language>zh-cn</language>',
  });
}