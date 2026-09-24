"""report.py：报表服务（老入口 build 不能改）。"""
from __future__ import annotations

from mvccstore import Store, latest


def build(store: Store, keys) -> list:
    """现存入口：按当前值出报表，定时任务在用，不能改。"""
    snapshot = latest(store)
    return [(key, snapshot.get(key)) for key in keys]


def build_at(store: Store, keys, snapshot: int) -> list:
    raise NotImplementedError("按快照出报表还没实现")
