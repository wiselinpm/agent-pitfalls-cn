#!/usr/bin/env node
/**
 * build-search-index.mjs
 *
 * 扫描 web/src/content/pitfalls/*.md 的 frontmatter，构建客户端搜索 manifest：
 *   web/public/search-index.json
 *
 * 设计目标：
 *   - 不引入 gray-matter 等依赖，纯 regex + 原生 fs
 *   - 单次扫描 ~8K 文件 < 2s（async + 并发批次）
 *   - 与 pitfalls/index.astro 排序保持一致（discovered_at 倒序）
 *
 * 运行：
 *   node scripts/build-search-index.mjs
 *   npm run index:build
 *
 * 同时被 prebuild / predev 自动触发，避免忘记刷新 manifest。
 */

import { readdir, readFile, writeFile, stat, mkdir } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT      = join(__dirname, '..');
const SRC_DIR   = join(ROOT, 'web', 'src', 'content', 'pitfalls');
const OUT_PATH  = join(ROOT, 'web', 'public', 'search-index.json');

const CONCURRENCY = 64; // 8K 文件分批并发读

// --- frontmatter 提取（纯 regex，足够覆盖本仓库的 frontmatter 形态） ---

// 字段提取：支持 yaml scalar / flow list / block list
const RE_FIELD = /^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$/;
const RE_LIST_ITEM = /^\s*-\s+(.*)$/;

function parseFrontmatter(raw) {
  // 只在文件最开头匹配 --- ... ---
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return null;
  const block = m[1];

  const fields = {};
  let currentListKey = null;

  for (const line of block.split(/\r?\n/)) {
    if (!line.trim()) continue;
    const li = line.match(RE_LIST_ITEM);
    if (li) {
      if (!currentListKey) continue;
      const v = li[1].trim().replace(/^['"]|['"]$/g, '');
      (fields[currentListKey] ??= []).push(v);
      continue;
    }
    const fm = line.match(RE_FIELD);
    if (fm) {
      const [, key, rawValue] = fm;
      const value = rawValue.trim();
      if (value === '' || value === '|' || value === '>') {
        // 空值或 block scalar 起始：当作 list 处理
        currentListKey = key;
        fields[key] ??= [];
        continue;
      }
      // inline list: [a, b, "c"]
      if (value.startsWith('[') && value.endsWith(']')) {
        const inner = value.slice(1, -1).trim();
        fields[key] = inner
          ? inner.split(',').map((s) => s.trim().replace(/^['"]|['"]$/g, '')).filter(Boolean)
          : [];
        currentListKey = null;
        continue;
      }
      // scalar: 去引号
      fields[key] = value.replace(/^['"]|['"]$/g, '');
      currentListKey = null;
    }
  }

  return fields;
}

function pickString(v, fallback = '') {
  return typeof v === 'string' ? v : fallback;
}
function pickList(v) {
  return Array.isArray(v) ? v : [];
}
function toIso(v) {
  if (!v) return undefined;
  const s = String(v);
  // 仅保留 YYYY-MM-DD，避免时区漂移
  return s.length >= 10 ? s.slice(0, 10) : s;
}

// --- main ---

async function exists(p) {
  try { await stat(p); return true; } catch { return false; }
}

async function readOne(file) {
  const id = file.replace(/\.md$/, '');
  const full = join(SRC_DIR, file);
  const raw = await readFile(full, 'utf8');
  const fm = parseFrontmatter(raw);
  if (!fm) return null;

  const date = toIso(fm.discovered_at);
  return {
    id,
    title: pickString(fm.title, id),
    summary: pickString(fm.summary, ''),
    severity: pickString(fm.severity, 'medium'),
    platforms: pickList(fm.platforms),
    categories: pickList(fm.categories),
    ...(date ? { date } : {}),
  };
}

async function run() {
  if (!(await exists(SRC_DIR))) {
    console.error(`build-search-index: ${SRC_DIR} 不存在`);
    process.exit(1);
  }

  const t0 = Date.now();
  const files = (await readdir(SRC_DIR))
    .filter((f) => f.endsWith('.md') && !f.startsWith('_'));

  // 分批并发，避免打开 8K fd
  const out = new Array(files.length);
  let cursor = 0;
  async function worker() {
    while (cursor < files.length) {
      const i = cursor++;
      out[i] = await readOne(files[i]);
    }
  }
  const workers = Array.from({ length: Math.min(CONCURRENCY, files.length) }, worker);
  await Promise.all(workers);

  const items = out.filter(Boolean);

  // 与 pitfalls/index.astro 排序保持一致：discovered_at 倒序
  items.sort((a, b) => {
    const ta = a.date ? Date.parse(a.date) : 0;
    const tb = b.date ? Date.parse(b.date) : 0;
    return tb - ta;
  });

  await mkdir(dirname(OUT_PATH), { recursive: true });
  await writeFile(OUT_PATH, JSON.stringify(items), 'utf8');

  const dt = Date.now() - t0;
  const sizeKb = (Buffer.byteLength(JSON.stringify(items)) / 1024).toFixed(1);
  console.log(`build-search-index: ${items.length} 条 → ${OUT_PATH} (${sizeKb} KB, ${dt} ms)`);
}

run().catch((e) => {
  console.error('build-search-index 失败:', e);
  process.exit(1);
});