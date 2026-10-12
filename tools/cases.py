"""Best / average / worst CASES, found by measurement instead of by assumption.

Sorting: try many input shapes (sorted, reversed, all-equal, organ-pipe, saw-tooth, plus
adversarial permutations constructed for merge / quick sort).  best = fewest comparisons,
worst = most, average = mean over several random permutations.
Searching: average = mean over EVERY key that is present (exact), best/worst = min/max
over first/middle/last/missing keys on evenly-spaced and geometric data.
"""
import random

from tools.instrument import count_search, count_sort

CASES = ("best", "average", "worst")
RANDOM_SEEDS = range(5)


def _balanced_for_last_pivot(v):
    """Permutation whose LAST element is the median at every recursion level (quick-sort best)."""
    if len(v) <= 1:
        return v[:]
    m = len(v) // 2
    return _balanced_for_last_pivot(v[:m]) + _balanced_for_last_pivot(v[m + 1:]) + [v[m]]


def _merge_worst(v, leaf=1):
    """Permutation that makes every merge fully interleave (merge-sort worst case).
    leaf > 1: leaves of that size are reversed - the worst case for an insertion-sort cutoff."""
    if len(v) <= leaf:
        return v[::-1] if leaf > 1 else v[:]
    left, right = (v[0::2], v[1::2]) if len(v) % 2 == 0 else (v[1::2], v[0::2])
    return _merge_worst(left, leaf) + _merge_worst(right, leaf)


def sort_shapes(n):
    asc = list(range(1, n + 1))
    half = n // 2
    return {
        "sorted": asc,
        "reversed": asc[::-1],
        "all equal": [1] * n,
        "organ-pipe": asc[:half] + asc[half:][::-1],
        "saw-tooth": [i % 8 for i in range(n)],
        "balanced-pivot permutation": _balanced_for_last_pivot(asc),
        "perfectly interleaving permutation": _merge_worst(asc),
        "interleaving permutation, reversed leaves": _merge_worst(asc, 8),
    }


def random_perm(n, seed):
    return random.Random(seed).sample(range(1, n + 1), n)


def evaluate_sort(fn, n):
    """-> {case: (shape name, input, comparisons)}.  average input is the seed-0 permutation."""
    shapes = sort_shapes(n)
    scored = {name: count_sort(fn, v) for name, v in shapes.items()}
    best = min(scored, key=scored.get)
    worst = max(scored, key=scored.get)
    avg = sum(count_sort(fn, random_perm(n, s)) for s in RANDOM_SEEDS) / len(RANDOM_SEEDS)
    return {"best": (best, shapes[best], scored[best]),
            "average": ("random", random_perm(n, 0), avg),
            "worst": (worst, shapes[worst], scored[worst])}


def search_datasets(n):
    return {"evenly spaced": [i * 3 for i in range(n)],
            "geometric (powers of 2)": [2 ** i for i in range(n)]}


def search_keys(vals):
    n = len(vals)
    return {"first": vals[0], "middle": vals[(n - 1) // 2], "last": vals[-1],
            "missing (too small)": vals[0] - 1, "missing (too large)": vals[-1] + 1,
            "missing (in a gap)": vals[n // 2] + 1}


def evaluate_search(algo, fn, n):
    """-> {case: (description, values, key, comparisons)}."""
    scored = []
    if algo == "linear_search":
        base = list(range(0, n * 2, 2))
        random.Random(0).shuffle(base)
        datasets = {"unsorted": base}
        keys_of = lambda v: {"first": v[0], "middle": v[(n - 1) // 2], "last": v[-1],
                             "missing": -1}
    else:
        datasets = search_datasets(n)
        keys_of = search_keys
    for dname, vals in datasets.items():
        for kname, key in keys_of(vals).items():
            scored.append((count_search(fn, vals, key), f"{kname} key, {dname} data", vals, key))
    best, worst = min(scored, key=lambda s: s[0]), max(scored, key=lambda s: s[0])
    base_vals = list(datasets.values())[0]
    avg = sum(count_search(fn, base_vals, k) for k in base_vals) / n
    return {"best": (best[1], best[2], best[3], best[0]),
            "average": (f"every present key, {list(datasets)[0]} data", base_vals,
                        base_vals[n // 3], avg),
            "worst": (worst[1], worst[2], worst[3], worst[0])}
