"""诊断脚本：单独测每个 collector 命中数 + 采样。

用法：python -m scripts._test_collectors
"""
from __future__ import annotations

import logging
import signal
import sys

logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(name)s: %(message)s")

from collectors.sources import all_collectors, safe_collect


class _Alarm(Exception):
    pass


def _alarm_handler(*_):
    raise _Alarm()


def _run_one(name: str, max_n: int = 30, timeout: int = 20) -> tuple[str, int, list[str]]:
    """同步执行一个 collector，带超时。"""
    signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(timeout)
    n = 0
    samples: list[str] = []
    try:
        for coll in all_collectors():
            if coll.name != name:
                continue
            for hit in safe_collect(coll):
                n += 1
                if len(samples) < 2:
                    samples.append(f"{hit.title[:70]} | {hit.url[:80]}")
                if n >= max_n:
                    break
    except _Alarm:
        return (name, -1, samples)
    except Exception as e:
        return (name, -2, [f"EXC: {type(e).__name__}: {str(e)[:120]}"])
    finally:
        signal.alarm(0)
    return (name, n, samples)


def main() -> int:
    for coll in all_collectors():
        name, n, samples = _run_one(coll.name)
        if n == -1:
            print(f"{name:20} TIMEOUT")
        elif n == -2:
            print(f"{name:20} {samples[0]}")
        elif n > 0:
            print(f"{name:20} OK {n}")
            for s in samples:
                print(f"    - {s}")
        else:
            print(f"{name:20} EMPTY")
    print("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())