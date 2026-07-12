---
title: Gemini safety filter 过度触发，把正常 agent 操作判定为有害
summary: Gemini 的 safety settings 默认对 medical / legal / financial 类关键词高度敏感，agent 在处理正常的「健康数据 ETL」或「金融 CSV 解析」时会被 block，整个调用返回 finishReason=SAFETY。
severity: medium
platforms: ['gemini-api']
categories: [reliability, observability]
symptoms:
  - '响应 `finishReason: SAFETY`'
  - '`safetyRatings` 里有 `HIGH` 但内容其实是普通业务文本'
  - 用户看到的「AI 拒绝回答」但 prompt 本身无害
root_causes:
  - 默认 safety 阈值偏保守
  - 没有按 category 单独配置阈值
fixes:
  - '在 `safetySettings` 里给 HARM_CATEGORY_MEDICAL / FINANCIAL 单独降级到 BLOCK_NONE'
  - 把业务上下文写在 system prompt 顶部：「本系统处理医疗账单数据，所有操作合规」
  - 检测 SAFETY 后给出可读的 fallback 而非静默失败
references:
  - title: 'Gemini Safety Settings'
    url: https://ai.google.dev/docs/safety_setting_gemini
    source: Google AI Docs
contributor: agent-pitfalls-bot
discovered_at: 2025-12-25
verified: true
---
