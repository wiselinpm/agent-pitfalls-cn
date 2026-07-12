---
title: AI Agent 调用外部工具有标准方案吗？MCP 协议 + Bedrock 实战详解
summary: 做了一个 AI Agent，需要它读 S3 文件、查 DynamoDB、调内部 API。每个工具都要写 function calling 的 schema 和调用逻辑，工具一多维护成本很高。有没有标准化的方案？
severity: medium
platforms:
- generic
categories:
- tool-use
symptoms: []
root_causes: []
fixes: []
references:
- title: AI Agent 调用外部工具有标准方案吗？MCP 协议 + Bedrock 实战详解
  url: https://segmentfault.com/a/1190000047652243
  source: segmentfault
tags:
- segmentfault
- agent 工具调用
contributor: 亚马逊云开发者
discovered_at: '2026-03-13'
verified: false
---

- [AI Agent 调用外部工具有标准方案吗？MCP 协议 + Bedrock 实战详解](https://segmentfault.com/a/1190000047652243) — segmentfault

## 摘要

做了一个 AI Agent，需要它读 S3 文件、查 DynamoDB、调内部 API。每个工具都要写 function calling 的 schema 和调用逻辑，工具一多维护成本很高。有没有标准化的方案？
