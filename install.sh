#!/usr/bin/env bash
# agent-pitfalls 一键安装脚本
# 用法：curl -fsSL https://.../install.sh | bash

set -euo pipefail

REPO="${AGENT_PITFALLS_REPO:-wiselinpm/agent-pitfalls-cn}"
INSTALL_DIR="${AGENT_PITFALLS_INSTALL_DIR:-$HOME/.agent-pitfalls}"

echo "▸ 安装 agent-pitfalls 到 $INSTALL_DIR"

# —— 1) 选择安装方式 ——
install_via_pip() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ 需要 python3"
    return 1
  fi
  python3 -m pip install --user agent-pitfalls
  echo "✓ pip install 完成。试试：agent-pitfalls --version"
}

install_via_pipx() {
  if ! command -v pipx >/dev/null 2>&1; then
    echo "❌ pipx 未安装，先：python3 -m pip install --user pipx"
    return 1
  fi
  pipx install agent-pitfalls
}

install_via_npm() {
  if ! command -v npm >/dev/null 2>&1; then
    echo "❌ 需要 npm"
    return 1
  fi
  npm i -g agent-pitfalls
  echo "✓ npm install 完成。试试：npx agent-pitfalls --version"
}

if command -v pipx >/dev/null 2>&1; then
  install_via_pipx
elif command -v python3 >/dev/null 2>&1; then
  install_via_pip
elif command -v npm >/dev/null 2>&1; then
  install_via_npm
else
  echo "❌ 没检测到 pipx / python3 / npm，请先装一个"
  exit 1
fi

# —— 2) 询问是否安装 Claude Code 插件 ——
echo
read -p "▸ 安装 Claude Code 插件? [y/N] " yn
if [[ "${yn:-N}" =~ ^[Yy]$ ]]; then
  mkdir -p "$HOME/.claude/plugins"
  if [[ -d "$INSTALL_DIR/plugin" ]]; then
    PLUGIN_SRC="$INSTALL_DIR/plugin"
  else
    PLUGIN_SRC="./plugin"
  fi
  rm -rf "$HOME/.claude/plugins/agent-pitfalls"
  ln -s "$(cd "$PLUGIN_SRC" && pwd)" "$HOME/.claude/plugins/agent-pitfalls"
  echo "✓ Claude Code 插件已链接到 ~/.claude/plugins/agent-pitfalls"
  echo "  重启 Claude Code 后可用：/pitfall <query>"
fi

# —— 3) 询问 Codex / OpenCode / Gemini ——
for cli in codex opencode gemini; do
  echo
  read -p "▸ 安装 $cli 集成? [y/N] " yn
  case "$cli:$yn" in
    codex:[Yy]*)
      mkdir -p "$HOME/.codex/prompts/agent-pitfalls"
      cp -r "${PLUGIN_SRC:-./plugin}/codex/"* "$HOME/.codex/prompts/agent-pitfalls/"
      echo "✓ Codex prompts 已安装"
      ;;
    opencode:[Yy]*)
      mkdir -p "$HOME/.opencode/plugins"
      rm -f "$HOME/.opencode/plugins/agent-pitfalls.json"
      ln -s "${PLUGIN_SRC:-./plugin}/opencode.json" "$HOME/.opencode/plugins/agent-pitfalls.json"
      echo "✓ OpenCode 插件已链接"
      ;;
    gemini:[Yy]*)
      mkdir -p "$HOME/.gemini/extensions/agent-pitfalls"
      cp "${PLUGIN_SRC:-./plugin}/gemini-extension.json" "$HOME/.gemini/extensions/agent-pitfalls/"
      echo "✓ Gemini extension 已安装"
      ;;
  esac
done

echo
echo "🎉 完成！"
echo "  agent-pitfalls search \"<your query>\"   # 智能查询"
echo "  agent-pitfalls check .                  # 项目避坑体检"
echo "  agent-pitfalls serve                    # 启动本地 MCP 服务"