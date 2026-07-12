// Astro 5 Content Collections 配置 — 定义避坑条目的强 schema
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const pitfalls = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './web/src/content/pitfalls' }),
  schema: z.object({
    title: z.string().min(4).max(120),
    summary: z.string().min(10).max(300),
    severity: z.enum(['critical', 'high', 'medium', 'low']),
    platforms: z.array(z.enum([
      'claude-code', 'openai-agents', 'langchain', 'autogen', 'crewai',
      'langgraph', 'open-interpreter', 'devin', 'cursor', 'aider',
      'claude-api', 'openai-api', 'gemini-api', 'generic',
    ])).default(['generic']),
    categories: z.array(z.enum([
      'context-window', 'tool-use', 'streaming', 'cost', 'security',
      'observability', 'memory', 'multi-agent', 'prompt-injection',
      'sandbox', 'reliability', 'latency', 'state', 'tokenization',
    ])).default([]),
    symptoms: z.array(z.string()).default([]),
    root_causes: z.array(z.string()).default([]),
    fixes: z.array(z.string()).default([]),
    references: z.array(z.object({
      title: z.string(),
      url: z.string().url(),
      source: z.string().optional(),
      accessed_at: z.string().optional(),
    })).default([]),
    tags: z.array(z.string()).default([]),
    discovered_at: z.coerce.date().optional(),
    verified: z.boolean().default(false),
    contributor: z.string().optional(),
  }),
});

const advisories = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './web/src/content/advisories' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    severity: z.enum(['critical', 'high', 'medium', 'low']),
    affected: z.array(z.string()),
    published_at: z.coerce.date(),
    references: z.array(z.object({
      title: z.string(),
      url: z.string().url(),
    })).default([]),
  }),
});

const patterns = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './web/src/content/patterns' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    use_when: z.string(),
    pros: z.array(z.string()).default([]),
    cons: z.array(z.string()).default([]),
    example: z.string().optional(),
  }),
});

export const collections = { pitfalls, advisories, patterns };