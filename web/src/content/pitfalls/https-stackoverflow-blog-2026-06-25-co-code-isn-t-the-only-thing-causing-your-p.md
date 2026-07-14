---
title: 'Code isn’t the only thing causing your production...'
summary: Ryan sits down with Anish Agarwal, CEO and co-founder of Traversal, to chat about why AI coding agents have made writing code easier but running it safely in production harder, why production failures are really caused by interactions between systems and not just the code itself,
severity: critical
platforms:
- generic
categories:
- observability
symptoms: []
root_causes: []
fixes: []
references:
- title: "Code isn’t the only thing causing your production failures​​​​‌uFEFF‍uFEFF​‍​‍‌‍uFEFFuFEFF‌uFEFF​‍‌‍‍‌‌‍‌uFEFF‌‍‍‌‌‍uFEFF‍​‍​‍​uFEFF‍‍​‍​‍‌uFEFF​uFEFF‌‍​‌‌‍uFEFF‍‌‍‍‌‌uFEFF‌​‌uFEFF‍‌​‍uFEFF‍‌‍‍‌‌‍uFEFFuFEFF​‍​‍​‍uFEFF​​‍​‍‌‍‍​‌uFEFF​‍‌‍‌‌‌‍‌‍​‍​‍​uFEFF‍‍​‍​‍‌‍‍​‌uFEFF‌​‌uFEFF‌​‌uFEFF​​‌uFEFF​uFEFF​uFEFF‍‍​‍uFEFFuFEFF​‍uFEFFuFEFF‌‍​uFEFF‌‍uFEFF‌‌uFEFF​uFEFF​‍uFEFF‍‌uFEFF​uFEFF‌uFEFF‌​‌‍​‌‌‍​uFEFF‌‍‍uFEFF‌‍uFEFFuFEFF‌uFEFF‌‍‌‍‌‌‌uFEFF​‍‌‍‌‍‌‍uFEFF​‌‍uFEFFuFEFF‌uFEFF‌uFEFF​‍uFEFF‍‌‍​uFEFF‌‍uFEFFuFEFF​‍uFEFFuFEFF‌‍‍‌‌‍uFEFF‍‌uFEFF‌​‌‍‌‌‌‍uFEFF‍‌uFEFF‌​​‍uFEFFuFEFF‌‍‌‌‌‍‌​‌‍‍‌‌uFEFF‌​​‍uFEFFuFEFF‌‍uFEFF‌‌‍uFEFFuFEFF‌‍‌​‌‍‌‌​uFEFFuFEFF‌‌uFEFF​​‌uFEFF​‍‌‍‌‌‌uFEFF​uFEFF‌‍‌‌‌‍uFEFF‍‌uFEFF‌​‌‍​‌‌uFEFF‌​‌‍‍‌‌‍uFEFFuFEFF‌‍uFEFF‍​uFEFF‍uFEFF‌‍‍‌‌‍‌​​uFEFFuFEFF‌‌‍‌‍​uFEFF‍​​uFEFF​uFEFF‌‍‌‌‌‍​‍​uFEFF‌‌‌‍‌‍​uFEFF​​​‍uFEFF‌​uFEFF​‌​uFEFF​‍​uFEFF​uFEFF​uFEFF‌uFEFF​‍uFEFF‌​uFEFF‌​​uFEFF‍​​uFEFF‌uFEFF‌‍‌‍​‍uFEFF‌​uFEFF‍​​uFEFF‌​‌‍‌​​uFEFF‍​​‍uFEFF‌‌‍‌‍​uFEFF‌uFEFF‌‍​‌‌‍​‍‌‍‌‍​uFEFF​‍​uFEFF​uFEFF​uFEFF​‌​uFEFF‍​‌‍​uFEFF​uFEFF​uFEFF​uFEFF‍‌​uFEFF‍uFEFF‌uFEFF‌​‌uFEFF‍‌‌uFEFF​​‌‍‌‌​uFEFFuFEFF‌‌‍​‍‌‍uFEFF​‌‍uFEFFuFEFF‌‍‌uFEFF‌‌​​‌‍uFEFFuFEFF‌uFEFF​uFEFF‌uFEFF‌​​uFEFF‍uFEFF‌uFEFF​​‌‍​‌‌uFEFF‌​‌‍‍​​uFEFFuFEFF‌‌uFEFF‌​‌‍‍‌‌uFEFF‌​‌‍uFEFF​‌‍‌‌​uFEFFuFEFFuFEFF‌‍​‍‌‍​‌‌uFEFF​uFEFF‌‍‌‌‌‌‌‌‌uFEFF​‍‌‍uFEFF​​uFEFFuFEFF‌‌‍‍​‌uFEFF‌​‌uFEFF‌​‌uFEFF​​‌uFEFF​uFEFF​‍‌‌​uFEFF​uFEFF‌​​‌​‍‌‌​uFEFF​‍‌​‌‍​‍‌‌​uFEFF​‍‌​‌‍‌‍​uFEFF‌‍uFEFF‌‌uFEFF​uFEFF​‍uFEFF‍‌uFEFF​uFEFF‌uFEFF‌​‌‍​‌‌‍​uFEFF‌‍‍uFEFF‌‍uFEFFuFEFF‌uFEFF‌‍‌‍‌‌‌uFEFF​‍‌‍‌‍‌‍uFEFF​‌‍uFEFFuFEFF‌uFEFF‌uFEFF​‍uFEFF‍‌‍​uFEFF‌‍uFEFFuFEFF​‍‌‍‌‍‍‌‌‍‌​​uFEFFuFEFF‌‌‍‌‍​uFEFF‍​​uFEFF​uFEFF‌‍‌‌‌‍​‍​uFEFF‌‌‌‍‌‍​uFEFF​​​‍uFEFF‌​uFEFF​‌​uFEFF​‍​uFEFF​uFEFF​uFEFF‌uFEFF​‍uFEFF‌​uFEFF‌​​uFEFF‍​​uFEFF‌uFEFF‌‍‌‍​‍uFEFF‌​uFEFF‍​​uFEFF‌​‌‍‌​​uFEFF‍​​‍uFEFF‌‌‍‌‍​uFEFF‌uFEFF‌‍​‌‌‍​‍‌‍‌‍​uFEFF​‍​uFEFF​uFEFF​uFEFF​‌​uFEFF‍​‌‍​uFEFF​uFEFF​uFEFF​uFEFF‍‌​‍‌‍‌uFEFF‌​‌uFEFF‍‌‌uFEFF​​‌‍‌‌​uFEFFuFEFF‌‌‍​‍‌‍uFEFF​‌‍uFEFFuFEFF‌‍‌uFEFF‌‌​​‌‍uFEFFuFEFF‌uFEFF​uFEFF‌uFEFF‌​​‍‌‍‌uFEFF​​‌‍​‌‌uFEFF‌​‌‍‍​​uFEFFuFEFF‌‌uFEFF‌​‌‍‍‌‌uFEFF‌​‌‍uFEFF​‌‍‌‌​‍‌‍‌uFEFF​​‌‍‌‌‌uFEFF​‍‌uFEFF​uFEFF‌uFEFF​​‌‍‌‌‌‍​uFEFF‌uFEFF‌​‌‍‍‌‌uFEFF‌‍‌‍‌‌​uFEFFuFEFF‌‌uFEFF​​‌uFEFF‌‌‌‍​‍‌‍uFEFF​‌‍‍‌‌uFEFF​uFEFF‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌uFEFFuFEFF‌"
  url: https://stackoverflow.blog/2026/06/25/code-isnt-causing-your-production-failures/
  source: stackoverflow-blog
tags:
- stackoverflow-blog
contributor: Phoebe Sajor
discovered_at: '2026-06-25'
verified: false
---
- [Code isn’t the only thing causing your production failures​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌‍​﻿‍​​﻿​﻿‌‍‌‌‌‍​‍​﻿‌‌‌‍‌‍​﻿​​​‍﻿‌​﻿​‌​﻿​‍​﻿​﻿​﻿‌﻿​‍﻿‌​﻿‌​​﻿‍​​﻿‌﻿‌‍‌‍​‍﻿‌​﻿‍​​﻿‌​‌‍‌​​﻿‍​​‍﻿‌‌‍‌‍​﻿‌﻿‌‍​‌‌‍​‍‌‍‌‍​﻿​‍​﻿​﻿​﻿​‌​﻿‍​‌‍​﻿​﻿​﻿​﻿‍‌​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌‍​﻿‍​​﻿​﻿‌‍‌‌‌‍​‍​﻿‌‌‌‍‌‍​﻿​​​‍﻿‌​﻿​‌​﻿​‍​﻿​﻿​﻿‌﻿​‍﻿‌​﻿‌​​﻿‍​​﻿‌﻿‌‍‌‍​‍﻿‌​﻿‍​​﻿‌​‌‍‌​​﻿‍​​‍﻿‌‌‍‌‍​﻿‌﻿‌‍​‌‌‍​‍‌‍‌‍​﻿​‍​﻿​﻿​﻿​‌​﻿‍​‌‍​﻿​﻿​﻿​﻿‍‌​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌](https://stackoverflow.blog/2026/06/25/code-isnt-causing-your-production-failures/) — stackoverflow-blog

## 摘要

Ryan sits down with Anish Agarwal, CEO and co-founder of Traversal, to chat about why AI coding agents have made writing code easier but running it safely in production harder, why production failures are really caused by interactions between systems and not just the code itself,
