---
title: 'Kubernetes v1.36: Deprecation and removal of Service ExternalIPs'
summary: The .spec.externalIPs field for Service was an early attempt to provide cloud-load-balancer-like functionality for non-cloud clusters. Unfortunately, the API assumes that every user in the cluster is fully trusted, and in any situation where that is not the case, it enables vario
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
- title: 'Kubernetes v1.36: Deprecation and removal of Service ExternalIPs'
  url: https://kubernetes.io/blog/2026/05/14/kubernetes-v1-36-deprecation-and-removal-of-service-externalips/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-05-14'
verified: false
---

- [Kubernetes v1.36: Deprecation and removal of Service ExternalIPs](https://kubernetes.io/blog/2026/05/14/kubernetes-v1-36-deprecation-and-removal-of-service-externalips/) — kubernetes-blog

## 摘要

The .spec.externalIPs field for Service was an early attempt to provide cloud-load-balancer-like functionality for non-cloud clusters. Unfortunately, the API assumes that every user in the cluster is fully trusted, and in any situation where that is not the case, it enables vario
