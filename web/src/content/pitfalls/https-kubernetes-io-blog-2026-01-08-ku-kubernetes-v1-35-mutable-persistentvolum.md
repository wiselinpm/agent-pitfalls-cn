---
title: 'Kubernetes v1.35: Mutable PersistentVolume Node Affinity (alpha)'
summary: The PersistentVolume node affinity API dates back to Kubernetes v1.10. It is widely used to express that volumes may not be equally accessible by all nodes in the cluster. This field was previously immutable, and it is now mutable in Kubernetes v1.35 (alpha). This change opens a
severity: high
platforms:
- generic
categories:
- streaming
- observability
- memory
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Kubernetes v1.35: Mutable PersistentVolume Node Affinity (alpha)'
  url: https://kubernetes.io/blog/2026/01/08/kubernetes-v1-35-mutable-pv-nodeaffinity/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-01-08'
verified: false
---

- [Kubernetes v1.35: Mutable PersistentVolume Node Affinity (alpha)](https://kubernetes.io/blog/2026/01/08/kubernetes-v1-35-mutable-pv-nodeaffinity/) — kubernetes-blog

## 摘要

The PersistentVolume node affinity API dates back to Kubernetes v1.10. It is widely used to express that volumes may not be equally accessible by all nodes in the cluster. This field was previously immutable, and it is now mutable in Kubernetes v1.35 (alpha). This change opens a
