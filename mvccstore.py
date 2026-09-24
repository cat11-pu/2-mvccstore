"""mvccstore.py：多版本存储内核（基线：单版本，老入口在用）。"""
from __future__ import annotations


class Store:
    def __init__(self, initial=None):
        self.data = dict(initial or {})
        self.writes = 0
        self.conflicts = 0

    def begin(self) -> int:
        return self.writes

    def read(self, snapshot: int, key: str):
        return self.data.get(key)

    def write(self, key: str, value: str, snapshot: int = None) -> bool:
        self.data[key] = value
        self.writes += 1
        return True

    def chain(self) -> dict:
        return {key: [value] for key, value in self.data.items()}

    def collect(self, active_snapshots) -> int:
        return 0

    def stats(self) -> dict:
        return {"keys": len(self.data), "writes": self.writes, "conflicts": self.conflicts}


def latest(store: Store) -> dict:
    """老入口：定时任务按"当前值"出报表。"""
    return dict(sorted(store.data.items()))
