---
title: The real serverless compute to database connection problem, solved
summary: '<p>There is a long-standing myth that serverless compute inherently requires more connections to traditional databases. The real issue is not the number of connections needed during normal operation, but that some serverless platforms can leak connections when functions are suspe'
severity: critical
platforms:
- generic
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: The real serverless compute to database connection problem, solved
  url: https://vercel.com/blog/the-real-serverless-compute-to-database-connection-problem-solved
  source: vercel-blog
tags:
- vercel-blog
contributor: Malte Ubl
discovered_at: '2025-08-13'
verified: false
---
- [The real serverless compute to database connection problem, solved](https://vercel.com/blog/the-real-serverless-compute-to-database-connection-problem-solved) — vercel-blog

## 摘要

<p>There is a long-standing myth that serverless compute inherently requires more connections to traditional databases. The real issue is not the number of connections needed during normal operation, but that some serverless platforms can leak connections when functions are suspe
