"""agent-pitfalls CLI — 在开发期即时查询 agent 避坑知识。

通过 ``agent-pitfalls`` 命令（pip 安装）或 ``npx agent-pitfalls`` 调用，
提供面向 LLM Agent 开发的「症状→根因→修复」知识检索能力。

主要子命令：

- ``search`` — 自然语言查询
- ``check`` — 对照当前项目做避坑检查
- ``list`` — 浏览 pitfalls 列表
- ``show`` — 查看某条 pitfall 详情
- ``platforms`` / ``categories`` — 元信息
- ``serve`` — 启动本地 HTTP 服务，给 plugin 调用
"""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]