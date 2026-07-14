---
title: 'Kubernetes v1.35: A Better Way to Pass Service Account Tokens to CSI Drivers'
summary: If you maintain a CSI driver that uses service account tokens, Kubernetes v1.35 brings a refinement you'll want to know about. Since the introduction of the TokenRequests feature , service account tokens requested by CSI drivers have been passed to them through the volume_context
severity: high
platforms:
- generic
categories:
- streaming
- security
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Kubernetes v1.35: A Better Way to Pass Service Account Tokens to CSI Drivers'
  url: https://kubernetes.io/blog/2026/01/07/kubernetes-v1-35-csi-sa-tokens-secrets-field-beta/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-01-07'
verified: false
---

- [Kubernetes v1.35: A Better Way to Pass Service Account Tokens to CSI Drivers](https://kubernetes.io/blog/2026/01/07/kubernetes-v1-35-csi-sa-tokens-secrets-field-beta/) — kubernetes-blog

## 摘要

If you maintain a CSI driver that uses service account tokens, Kubernetes v1.35 brings a refinement you'll want to know about. Since the introduction of the TokenRequests feature , service account tokens requested by CSI drivers have been passed to them through the volume_context
