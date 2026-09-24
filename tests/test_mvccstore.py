import unittest

import report
from mvccstore import Store, latest


class TestStore(unittest.TestCase):
    def test_read_initial(self):
        self.assertEqual(Store({"a": "0"}).read(0, "a"), "0")

    def test_missing_key(self):
        self.assertIsNone(Store().read(0, "ghost"))

    def test_latest_entry(self):
        store = Store()
        store.write("a", "1")
        self.assertEqual(latest(store), {"a": "1"})

    def test_build_uses_current_values(self):
        store = Store({"a": "0"})
        store.write("a", "1")
        self.assertEqual(report.build(store, ["a"]), [("a", "1")])

    def test_stats_counts_writes(self):
        store = Store()
        store.write("a", "1")
        self.assertEqual(store.stats()["writes"], 1)


if __name__ == "__main__":
    unittest.main()
