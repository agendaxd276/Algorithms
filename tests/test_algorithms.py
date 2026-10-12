"""Fuzz every variant against Python's built-in `sorted` / linear scan.  Run: python -m unittest"""
import random
import unittest

from algorithms.registry import SEARCHES, SORTS


def shapes(rng):
    yield []
    yield [7]
    yield [2, 1]
    for n in (2, 3, 5, 8, 17, 33, 100):
        base = list(range(n))
        yield base[:]                                       # sorted
        yield base[::-1]                                    # reversed
        yield [3] * n                                       # all equal
        yield [rng.randint(0, 5) for _ in range(n)]         # many duplicates
        yield rng.sample(range(n * 3), n)                   # random distinct
        yield [rng.randint(-50, 50) for _ in range(n)]      # negatives
        yield base[: n // 2][::-1] + base[n // 2:]          # partly sorted


class SortTests(unittest.TestCase):
    def test_all_variants(self):
        rng = random.Random(1)
        for name, variants in SORTS.items():
            for tier, fn in variants.items():
                for data in shapes(rng):
                    arr = data[:]
                    out = fn(arr)
                    self.assertEqual(out, sorted(data), f"{name}/{tier} on {data}")
                    self.assertIs(out, arr, f"{name}/{tier} must sort in place")

    def test_stability(self):
        """Stable sorts must keep equal keys in input order (compare by key only)."""
        class Key:
            def __init__(self, k, tag): self.k, self.tag = k, tag
            def __lt__(self, o): return self.k < o.k
            def __le__(self, o): return self.k <= o.k
            def __gt__(self, o): return self.k > o.k
            def __ge__(self, o): return self.k >= o.k
        rng = random.Random(2)
        for name in ("bubble_sort", "insertion_sort", "merge_sort"):
            for tier, fn in SORTS[name].items():
                items = [Key(rng.randint(0, 4), i) for i in range(60)]
                expected = sorted(items, key=lambda x: x.k)
                fn(items)
                self.assertEqual([x.tag for x in items], [x.tag for x in expected], f"{name}/{tier}")

    def test_quick_sort_no_recursion_blowup(self):
        data = list(range(5000))
        self.assertEqual(SORTS["quick_sort"]["optimized"](data[:]), data)
        self.assertEqual(SORTS["quick_sort"]["optimized"]([1] * 5000), [1] * 5000)
        self.assertEqual(SORTS["quick_sort"]["optimal"](data[::-1]), data)


class SearchTests(unittest.TestCase):
    def test_linear(self):
        rng = random.Random(3)
        for tier, fn in SEARCHES["linear_search"].items():
            for data in shapes(rng):
                for key in set(data) | {-999, 999}:
                    arr = data[:]
                    expected = data.index(key) if key in data else -1
                    self.assertEqual(fn(arr, key), expected, f"{tier} {data} {key}")
                    self.assertEqual(arr, data, "must not leave the sentinel behind")

    def test_binary(self):
        rng = random.Random(4)
        for tier, fn in SEARCHES["binary_search"].items():
            for data in shapes(rng):
                data.sort()
                for key in set(data) | {-999, 999, 25}:
                    got = fn(data, key)
                    if key in data:
                        self.assertEqual(data[got], key, f"{tier} {data} {key}")
                        if tier == "optimal":
                            self.assertEqual(got, data.index(key), "optimal returns FIRST match")
                    else:
                        self.assertEqual(got, -1, f"{tier} {data} {key}")

    def test_interpolation_skewed(self):
        data = [2 ** i for i in range(60)]
        fn = SEARCHES["binary_search"]["optimized"]
        for i, v in enumerate(data):
            self.assertEqual(fn(data, v), i)
        self.assertEqual(fn(data, 3), -1)


if __name__ == "__main__":
    unittest.main()
