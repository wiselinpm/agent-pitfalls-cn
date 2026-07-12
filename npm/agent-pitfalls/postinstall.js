#!/usr/bin/env node
/**
 * npm postinstall — 友好提示与自动安装 Python 端
 */

"use strict";

const { spawnSync } = require("node:child_process");
const { existsSync } = require("node:fs");
const { join } = require("node:path");

function findInPATH(name) {
  const ext = process.platform === "win32" ? ".cmd" : "";
  const dirs = (process.env.PATH || "").split(process.platform === "win32" ? ";" : ":");
  for (const dir of dirs) {
    const p = join(dir, name + ext);
    if (existsSync(p)) return p;
  }
  return null;
}

function findPython() {
  for (const c of ["python3", "python"]) {
    try {
      const r = spawnSync(c, ["--version"], { stdio: "ignore" });
      if (r.status === 0) return c;
    } catch (_) {}
  }
  return null;
}

function main() {
  // 已经装了？跳过
  for (const c of ["agent-pitfalls", "apf"]) {
    if (findInPATH(c)) {
      console.log("[agent-pitfalls] ✓ CLI 已在 PATH 中");
      return;
    }
  }

  const py = findPython();
  if (!py) {
    console.warn("[agent-pitfalls] 未检测到 Python，CLI 子命令暂不可用。");
    console.warn("[agent-pitfalls] 请手动运行：pip install agent-pitfalls");
    return;
  }

  console.log("[agent-pitfalls] 正在通过 pip 安装 Python 端实现…");
  const r = spawnSync(py, ["-m", "pip", "install", "--user", "agent-pitfalls"], {
    stdio: "inherit",
  });
  if (r.status === 0) {
    console.log("[agent-pitfalls] ✓ 安装完成，试试：agent-pitfalls search \"...\"");
  } else {
    console.warn("[agent-pitfalls] pip install 失败，可手动运行：pip install agent-pitfalls");
  }
}

try {
  main();
} catch (e) {
  // postinstall 失败不阻断 npm install
  console.warn("[agent-pitfalls] postinstall 警告：", e.message);
}
