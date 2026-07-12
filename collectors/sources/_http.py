"""共享 HTTP 工具 — 默认走环境变量里的 token。"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_UA = "agent-pitfalls/0.1 (+https://github.com/agent-pitfalls/agent-pitfalls)"
REQUEST_TIMEOUT = 30
RETRY_BACKOFF = (1.0, 3.0, 8.0)


class HTTPError(RuntimeError):
    """上游 HTTP 错误。"""


def http_get(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    token: str | None = None,
    timeout: int = REQUEST_TIMEOUT,
) -> bytes:
    """带重试的 GET；token 缺失时降级为匿名。"""
    full_url = url
    if params:
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
    h = {"User-Agent": DEFAULT_UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    token = token or os.environ.get("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(full_url, headers=h, method="GET")

    last_err: Exception | None = None
    for delay in (0.0, *RETRY_BACKOFF):
        if delay:
            time.sleep(delay)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504):
                continue
            raise HTTPError(f"HTTP {e.code} on {full_url}") from e
        except urllib.error.URLError as e:
            last_err = e
            continue
    raise HTTPError(f"Failed after retries: {last_err}")


def http_get_json(url: str, **kwargs: Any) -> Any:
    raw = http_get(url, **kwargs)
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise HTTPError(f"Invalid JSON from {url}: {e}") from e