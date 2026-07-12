#!/usr/bin/env node
/**
 * agent-pitfalls — npx 入口
 *
 * 优先级：
 *   1. 环境变量 AGENT_PITFALLS_BIN 指定的二进制
 *   2. $PATH 里的 agent-pitfalls / apf
 *   3. python -m agent_pitfalls_cli
 *   4. pipx run agent-pitfalls
 *   5. uv tool run agent-pitfalls
 *
 * 任一可用就把 stdio 透传给真正的实现，避免 Node 端重复实现 BM25 / 索引。
 */

"use strict";

const { spawnSync } = require("node:child_process");
const which = require("which");

function findPython() {
  for (const c of ["python3", "python"]) {
    try {
      const r = spawnSync(c, ["--version"], { stdio: "ignore" });
      if (r.status === 0) return c;
    } catch (_) {}
  }
  return null;
}

function run(cmd, args) {
  const r = spawnSync(cmd, args, { stdio: "inherit" });
  if (r.error) {
    console.error("[agent-pitfalls] 执行失败：", r.error.message);
    process.exit(1);
  }
  process.exit(r.status || 0);
}

function main() {
  const args = process.argv.slice(2);

  // 1) 显式覆盖
  if (process.env.AGENT_PITFALLS_BIN) {
    return run(process.env.AGENT_PITFALLS_BIN, args);
  }

  // 2) PATH
  for (const c of ["agent-pitfalls", "apf"]) {
    try {
      const p = which.sync(c, { nothrow: true });
      if (p) return run(p, args);
    } catch (_) {}
  }

  // 3) python -m
  const py = findPython();
  if (py) {
    const r = spawnSync(py, ["-m", "agent_pitfalls_cli", ...args], { stdio: "inherit" });
    if (!r.error && typeof r.status === "number") {
      process.exit(r.status || 0);
    }
  }

  // 4) pipx / uvx
  for (const c of ["pipx", "uvx"]) {
    try {
      const p = which.sync(c, { nothrow: true });
      if (p) {
        const r = spawnSync(p, ["run", "agent-pitfalls", ...args], { stdio: "inherit" });
        if (r.status === 0) process.exit(0);
      }
    } catch (_) {}
  }

  // 5) uv tool
  try {
    const uv = which.sync("uv", { nothrow: true });
    if (uv) {
      const r = spawnSync(uv, ["tool", "run", "agent-pitfalls", ...args], { stdio: "inherit" });
      if (r.status === 0) process.exit(0);
    }
  } catch (_) {}

  console.error(
    [
      "❌ agent-pitfalls 找不到 Python 实现，请先安装：",
      "   pip install agent-pitfalls",
      "   pipx install agent-pitfalls",
      "   uv tool install agent-pitfalls",
      "或设置 AGENT_PITFALLS_BIN 指向已安装的二进制。",
    ].join("\n")
  );
  process.exit(127);
}

main();