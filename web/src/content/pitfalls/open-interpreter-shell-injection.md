---
title: Open Interpreter 直接执行模型生成的 shell 命令，没有沙箱
summary: 'Open Interpreter 默认把模型生成的 Python / shell 代码直接 `exec`，没有 docker 隔离；如果 prompt 被注入，agent 会在宿主机上执行任意命令。'
severity: critical
platforms: ['open-interpreter', 'generic']
categories: [security, sandbox]
symptoms:
  - agent 提示「正在执行 rm -rf ~/important」
  - /etc/passwd 被意外修改
  - 容器外的服务被 agent 调用
root_causes:
  - 默认 auto_run 开启
  - 没有 docker mode 或 E2B sandbox
fixes:
  - 生产环境必须开 --docker 或 -y 配合 docker-compose 隔离
  - 用 safe_mode=True 启用只读白名单
  - 在 system prompt 里写明「只允许执行 npm / pip / pytest 类只读/可逆操作」
references:
  - title: Open Interpreter 安全模式
    url: https://github.com/openinterpreter/open-interpreter/blob/main/docs/SAFE_MODES.md
    source: GitHub
contributor: agent-pitfalls-bot
discovered_at: 2025-06-30
verified: true
---
