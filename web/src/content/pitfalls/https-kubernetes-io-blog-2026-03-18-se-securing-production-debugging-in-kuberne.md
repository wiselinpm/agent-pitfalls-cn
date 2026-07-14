---
title: Securing Production Debugging in Kubernetes
summary: 'During production debugging, the fastest route is often broad access such as cluster-admin (a ClusterRole that grants administrator-level access), shared bastions/jump boxes, or long-lived SSH keys. It works in the moment, but it comes with two common problems: auditing becomes d'
severity: critical
platforms:
- generic
categories:
- streaming
- observability
- sandbox
symptoms: []
root_causes: []
fixes: []
references:
- title: Securing Production Debugging in Kubernetes
  url: https://kubernetes.io/blog/2026/03/18/securing-production-debugging-in-kubernetes/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-03-18'
verified: false
---

- [Securing Production Debugging in Kubernetes](https://kubernetes.io/blog/2026/03/18/securing-production-debugging-in-kubernetes/) — kubernetes-blog

## 摘要

During production debugging, the fastest route is often broad access such as cluster-admin (a ClusterRole that grants administrator-level access), shared bastions/jump boxes, or long-lived SSH keys. It works in the moment, but it comes with two common problems: auditing becomes d
