---
title: SELinux Volume Label Changes goes GA (and likely implications in v1.37)
summary: 'If you run Kubernetes on Linux with SELinux in enforcing mode, plan ahead: a future release (anticipated to be v1.37) is expected to turn the SELinuxMount feature gate on by default. This makes volume setup faster for most workloads, but it can break applications that still depen'
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
- title: SELinux Volume Label Changes goes GA (and likely implications in v1.37)
  url: https://kubernetes.io/blog/2026/04/22/breaking-changes-in-selinux-volume-labeling/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-04-22'
verified: false
---

- [SELinux Volume Label Changes goes GA (and likely implications in v1.37)](https://kubernetes.io/blog/2026/04/22/breaking-changes-in-selinux-volume-labeling/) — kubernetes-blog

## 摘要

If you run Kubernetes on Linux with SELinux in enforcing mode, plan ahead: a future release (anticipated to be v1.37) is expected to turn the SELinuxMount feature gate on by default. This makes volume setup faster for most workloads, but it can break applications that still depen
