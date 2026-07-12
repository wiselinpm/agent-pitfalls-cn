# Collectors

把全网关于 agent 开发的「坑」采回到本仓库 `web/src/content/pitfalls/` 下，供 Astro 站点渲染。

## 架构

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ GitHub API  │  │  RSS Feeds  │  │ Hacker News │  │ Reddit JSON │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       └────────┬───────┴────────┬───────┴────────┬───────┘
                ▼                ▼                ▼
           ┌────────────────────────────────────────┐
           │  BaseCollector.collect() -> RawHit[]    │
           └────────────────┬───────────────────────┘
                            ▼
                  ┌───────────────────────┐
                  │  normalize: RawHit ->  │
                  │     PitfallDraft       │
                  └─────────┬─────────────┘
                            ▼
                  ┌───────────────────────┐
                  │  dedupe by URL fp /    │
                  │  title similarity      │
                  └─────────┬─────────────┘
                            ▼
                  ┌───────────────────────┐
                  │  emit: write Markdown  │
                  └───────────────────────┘
```

## 运行

```bash
pip install -r requirements.txt
python -m collectors.run_all --out web/src/content/pitfalls
```

可选参数：

- `--overwrite` — 覆盖已存在的 Markdown（默认跳过，便于人工编辑的内容不被覆盖）
- `--verbose` / `-v` — debug 日志

## 新增 source

1. 在 `collectors/sources/` 新建 `xxx.py`
2. 继承 `BaseCollector` 协议，实现 `collect() -> Iterable[RawHit]`
3. 用 `from ._http import http_get_json` 复用带重试的 HTTP 工具
4. 在 `collectors/sources/__init__.py::all_collectors()` 注册
5. 在 `collectors/tests/test_xxx.py` 写单测（使用 monkeypatch 替换 http 调用）

示例：

```python
from __future__ import annotations
from typing import Iterable
from ..base import RawHit

class MyCollector:
    name = "my-source"

    def collect(self) -> Iterable[RawHit]:
        # ... fetch + yield RawHit ...
        yield RawHit(title=..., url=..., source="my-source", summary=...)
```

## 故障处理

- 网络/解析异常：单个 source 抛异常会被 `safe_collect` 捕获，仅打 warning，不影响其它 source
- Rate limit：`_http.http_get` 自动重试 3 次，遵守 `Retry-After`
- 重复条目：URL 指纹（去除 utm/www/末尾斜杠）+ 标题相似度 > 0.82 视为同一坑

## 测试

```bash
pytest -q collectors/tests
pytest --cov=collectors collectors/tests   # 覆盖率报告
```

## 已知限制

- **知乎**搜索 API 经常返回 HTML 验证码，本 collector 会静默跳过
- **X / Twitter** 需要付费 API，本仓库暂未内置
- **微信公众号**内容不在公开网络，不收录
- **Discord / Slack 群聊**质量参差，不收录（除非官方频道）