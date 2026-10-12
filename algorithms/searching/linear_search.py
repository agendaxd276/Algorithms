"""Linear search - look at every element until the key shows up.

Contract (all variants): return the index of the FIRST match, or -1.
Works on unsorted data.  Best O(1) | Average O(n) | Worst O(n) | Space O(1).
"""


def linear_search_normal(arr, key):
    """Normal: the textbook loop, one comparison per element."""
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1


def linear_search_optimal(arr, key):
    """Optimal: sentinel search.

    Theta(n) is already the best possible for UNSORTED data (an adversary can hide
    the key in whichever slot you skip), so "optimal" here means the leanest loop:
    plant the key at the end so the loop needs no `i < n` bounds test.
    Temporarily writes to arr[-1] (restored before returning; not thread-safe).
    """
    n = len(arr)
    if n == 0:
        return -1
    last = arr[-1]
    arr[-1] = key              # sentinel guarantees the loop stops
    i = 0
    while arr[i] != key:
        i += 1
    arr[-1] = last             # put the real last element back
    if i < n - 1 or last == key:   # found earlier, or the sentinel slot really matched
        return i
    return -1


def linear_search_optimized(arr, key):
    """Optimized: let CPython's C loop do the scanning (list.index).

    Same O(n) comparisons, but the loop runs in C - typically 10-50x faster than
    a Python-level loop.  This is what you would ship.
    """
    try:
        return arr.index(key)
    except ValueError:
        return -1


VARIANTS = {"normal": linear_search_normal,
            "optimal": linear_search_optimal,
            "optimized": linear_search_optimized}

if __name__ == "__main__":
    from algorithms._cli import search_main
    search_main(VARIANTS, "Linear search")
