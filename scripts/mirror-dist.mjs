// Mirror dist/* into dist/<base>/* so any local static HTTP server
// (python -m http.server, nginx, file preview) reproduces GitHub
// Pages project-page routing for the base path declared in
// astro.config.mjs.
//
// Pure ESM script — runs after `astro build` and never touches anything
// else. Idempotent: re-running overwrites the mirror.

import { readdir, mkdir, copyFile, stat, rm } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT    = join(__dirname, '..');
const SRC_DIR = join(ROOT, 'dist');
const BASE    = '/agent-pitfalls-cn'; // keep in sync with astro.config.mjs `base`
const SUB     = BASE.replace(/^\//, ''); // 'agent-pitfalls-cn'
const DST_DIR = join(SRC_DIR, SUB);

async function exists(p) {
  try { await stat(p); return true; } catch { return false; }
}

async function copyOne(src, dst) {
  await mkdir(dirname(dst), { recursive: true });
  const s = await stat(src);
  if (s.isDirectory()) {
    await mkdir(dst, { recursive: true });
    for (const entry of await readdir(src)) {
      await copyOne(join(src, entry), join(dst, entry));
    }
  } else {
    await copyFile(src, dst);
  }
}

if (!(await exists(SRC_DIR))) {
  console.error(`mirror-dist: ${SRC_DIR} does not exist — run \`npm run build\` first.`);
  process.exit(1);
}

if (await exists(DST_DIR)) {
  await rm(DST_DIR, { recursive: true, force: true });
}
await mkdir(DST_DIR, { recursive: true });

for (const entry of await readdir(SRC_DIR)) {
  if (entry === SUB) continue; // skip self
  await copyOne(join(SRC_DIR, entry), join(DST_DIR, entry));
}

console.log(`mirror-dist: copied dist/* → dist/${SUB}/`);
console.log(`Serve with:  python3 -m http.server -d dist 8000`);
console.log(`Then visit:  http://localhost:8000/${SUB}/`);
