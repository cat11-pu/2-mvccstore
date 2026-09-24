"""把 sample/timeline.json 跑一遍，打印验收面（三个子系统）。"""
import json
import os
import sys

import report
from mvccstore import Store
from walstore import Wal


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "timeline.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    store = Store(spec["initial"])
    wal = Wal()
    snapshots = {}
    reads = []
    for step in spec["steps"]:
        if step["op"] == "begin":
            snapshots[step["id"]] = store.begin()
        elif step["op"] == "read":
            reads.append((step["id"], step["key"], store.read(snapshots[step["id"]], step["key"])))
        else:
            ok = store.write(step["key"], step["value"], snapshots[step.get("snapshot")] if step.get("snapshot") else None)
            if ok:
                wal.append({"key": step["key"], "value": step["value"]})
    print("读到的值 =", reads)
    print("写冲突条数 =", store.stats()["conflicts"])
    print("按快照出报表 =", report.build_at(store, spec["report_keys"], snapshots["r2"]))
    print("老入口报表（当前值） =", report.build(store, spec["report_keys"]))
    blob = wal.dump()
    fresh = Store(spec["initial"])
    replayed = Wal().load(blob)
    Wal().load(blob[:-3] + b"\x00\x00\x00")
    print("重放条数 =", replayed)
    print("残尾忽略 =", Wal().truncated)
    print("回收的版本数 =", store.collect([snapshots[i] for i in spec["active"]]))
    print("当前版本链长度 =", sorted((key, len(chain)) for key, chain in store.chain().items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
