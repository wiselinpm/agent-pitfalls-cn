"""Agent Pitfalls 采集器框架。

每个 source 都继承 BaseCollector 并实现 collect()，返回 RawHit 列表；
run_all 会调度所有 source，normalize + dedupe + emit 出最终 Markdown 文件。
"""

__version__ = "0.1.0"