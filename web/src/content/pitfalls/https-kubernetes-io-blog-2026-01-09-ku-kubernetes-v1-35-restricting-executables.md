---
title: 'Kubernetes v1.35: Restricting executables invoked by kubeconfigs via exec plugin allowList added to kuberc'
summary: Did you know that kubectl can run arbitrary executables, including shell scripts, with the full privileges of the invoking user, and without your knowledge? Whenever you download or auto-generate a kubeconfig , the users[n].exec.command field can specify an executable to fetch cr
severity: critical
platforms:
- generic
categories:
- security
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: 'Kubernetes v1.35: Restricting executables invoked by kubeconfigs via exec plugin allowList added to kuberc'
  url: https://kubernetes.io/blog/2026/01/09/kubernetes-v1-35-kuberc-credential-plugin-allowlist/
  source: kubernetes-blog
tags:
- kubernetes-blog
discovered_at: '2026-01-09'
verified: false
---

- [Kubernetes v1.35: Restricting executables invoked by kubeconfigs via exec plugin allowList added to kuberc](https://kubernetes.io/blog/2026/01/09/kubernetes-v1-35-kuberc-credential-plugin-allowlist/) — kubernetes-blog

## 摘要

Did you know that kubectl can run arbitrary executables, including shell scripts, with the full privileges of the invoking user, and without your knowledge? Whenever you download or auto-generate a kubeconfig , the users[n].exec.command field can specify an executable to fetch cr
