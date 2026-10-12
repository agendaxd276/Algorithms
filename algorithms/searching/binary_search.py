"""Binary search - halve the search window every step.  Requires SORTED input.

Contract (all variants): return an index of the key, or -1.
Best O(1) | Average O(log n) | Worst O(log n) | Space O(1).
"""


def binary_search_normal(arr, key):
    """Normal: classic three-way compare (==, then <) on the middle element."""
    start, end = 0, len(arr) - 1
    while start <= end:
        mid = start + (end - start) // 2      # never overflows in C/Java either
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            start = mid + 1
        else:
            end = mid - 1
    return -1


def binary_search_optimal(arr, key):
    """Optimal: "lower bound" form - ONE comparison per step, returns the FIRST match.

    Floor(log2 n) + 1 comparisons is the information-theoretic minimum for a
    comparison-based search, so no algorithm can beat O(log n) here.
    The half-open window [lo, hi) removes the off-by-one traps of `end = mid - 1`.
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < key:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(arr) and arr[lo] == key else -1


def binary_search_optimized(arr, key):
    """Optimized: interpolation search - guess WHERE the key should be.

    Probes lo + (key - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo]) instead of the
    middle.  On evenly spread numbers it needs ~log2(log2 n) probes; on skewed
    data (e.g. powers of two) it degrades to O(n).  Numbers only (needs subtraction).
    In production Python, prefer `bisect.bisect_left` (a C implementation of the
    optimal version above).
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= key <= arr[hi]:
        if arr[hi] == arr[lo]:                 # flat window: avoid divide-by-zero
            return lo if arr[lo] == key else -1
        pos = lo + (key - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])
        if arr[pos] == key:
            return pos
        if arr[pos] < key:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


VARIANTS = {"normal": binary_search_normal,
            "optimal": binary_search_optimal,
            "optimized": binary_search_optimized}

if __name__ == "__main__":
    from algorithms._cli import search_main
    search_main(VARIANTS, "Binary search", sorted_input=True)
