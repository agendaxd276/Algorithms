"""Measure the REAL algorithms: count comparisons, peak memory, recursion depth, wall time."""
import random
import sys
import time
import tracemalloc

sys.setrecursionlimit(20000)


class Counter:
    comparisons = 0


class Tracked:
    """An int that counts every comparison made on it (== != < <= > >=)."""
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __lt__(self, o): Counter.comparisons += 1; return self.v < o.v
    def __le__(self, o): Counter.comparisons += 1; return self.v <= o.v
    def __gt__(self, o): Counter.comparisons += 1; return self.v > o.v
    def __ge__(self, o): Counter.comparisons += 1; return self.v >= o.v
    def __eq__(self, o): Counter.comparisons += 1; return self.v == o.v
    def __ne__(self, o): Counter.comparisons += 1; return self.v != o.v
    def __sub__(self, o): return self.v - o.v      # arithmetic is free; returns plain int
    __hash__ = None


def count_sort(fn, values):
    arr = [Tracked(v) for v in values]
    Counter.comparisons = 0
    fn(arr)
    assert [t.v for t in arr] == sorted(values)
    return Counter.comparisons


def count_search(fn, values, key):
    arr = [Tracked(v) for v in values]
    k = Tracked(key)
    Counter.comparisons = 0
    fn(arr, k)
    return Counter.comparisons


def peak_extra_kib(fn, values):
    """Peak memory allocated BY the algorithm on top of the input list (tracemalloc)."""
    arr = list(values)
    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]
    tracemalloc.reset_peak()
    fn(arr)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return max(0, peak - base) / 1024


def max_depth(fn, values):
    """Deepest Python call stack the algorithm reaches (recursion = stack space)."""
    arr = list(values)
    depth = deepest = 0

    def prof(frame, event, arg):
        nonlocal depth, deepest
        if event == "call":
            depth += 1
            deepest = max(deepest, depth)
        elif event == "return":
            depth -= 1

    sys.setprofile(prof)
    try:
        fn(arr)
    finally:
        sys.setprofile(None)
    return deepest


def wall_ms(fn, make_input, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        data = make_input()
        t = time.perf_counter()
        fn(data)
        best = min(best, time.perf_counter() - t)
    return best * 1000
