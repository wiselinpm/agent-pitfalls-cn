---
title: 'Kubernetes v1.36: Admission Policies That Can''t Be Deleted'
summary: If you've ever tried to enforce a security policy across a fleet of Kubernetes clusters, you've probably run into a frustrating chicken-and-egg problem. Your admission policies are API objects, which means they don't exist until someone creates them, and they can be deleted by an
severity: critical
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
- title: 'Kubernetes v1.36: Admission Policies That Can''t Be Deleted'
  url: https://kubernetes.io/blog/2026/05/04/kubernetes-v1-36-manifest-based-admission-control/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-05-04'
verified: false
---

- [Kubernetes v1.36: Admission Policies That Can't Be Deleted](https://kubernetes.io/blog/2026/05/04/kubernetes-v1-36-manifest-based-admission-control/) — kubernetes-blog

## 摘要

If you've ever tried to enforce a security policy across a fleet of Kubernetes clusters, you've probably run into a frustrating chicken-and-egg problem. Your admission policies are API objects, which means they don't exist until someone creates them, and they can be deleted by an
