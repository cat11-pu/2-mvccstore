"""walstore.py：版本链的追加日志（待实现重放与残尾处理）。"""
from __future__ import annotations


class Wal:
    def __init__(self, path=None):
        self.records = []
        self.truncated = 0

    def append(self, record: dict) -> None:
        self.records.append(record)

    def replay(self, store) -> int:
        raise NotImplementedError("重放还没实现")

    def dump(self) -> bytes:
        raise NotImplementedError("落盘还没实现")

    def load(self, blob: bytes) -> int:
        raise NotImplementedError("载入还没实现")
