---
title: 'The Invisible Rewrite: Modernizing the Kubernetes Image Promoter'
summary: Every container image you pull from registry.k8s.io got there through kpromo , the Kubernetes image promoter. It copies images from staging registries to production, signs them with cosign , replicates signatures across more than 20 regional mirrors, and generates SLSA provenance
severity: critical
platforms:
- generic
categories:
- streaming
- cost
- security
symptoms: []
root_causes: []
fixes: []
references:
- title: 'The Invisible Rewrite: Modernizing the Kubernetes Image Promoter'
  url: https://kubernetes.io/blog/2026/03/17/image-promoter-rewrite/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-03-17'
verified: false
---

- [The Invisible Rewrite: Modernizing the Kubernetes Image Promoter](https://kubernetes.io/blog/2026/03/17/image-promoter-rewrite/) — kubernetes-blog

## 摘要

Every container image you pull from registry.k8s.io got there through kpromo , the Kubernetes image promoter. It copies images from staging registries to production, signs them with cosign , replicates signatures across more than 20 regional mirrors, and generates SLSA provenance
