"""Insertion sort - grow a sorted prefix by inserting the next item where it belongs.

Contract (all variants): sort `arr` ascending IN PLACE and return it.  Stable.
Best O(n) (sorted input) | Average O(n^2) | Worst O(n^2) (reversed) | Space O(1).
"""


def insertion_sort_normal(arr):
    """Normal: bubble the new item left with repeated swaps (3 writes per step)."""
    for i in range(1, len(arr)):
        while i > 0 and arr[i - 1] > arr[i]:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            i -= 1
    return arr


def insertion_sort_optimal(arr):
    """Optimal: hold the item aside and SHIFT larger items right (1 write per step)."""
    for i in range(1, len(arr)):
        item = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > item:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = item
    return arr


def insertion_sort_optimized(arr):
    """Optimized: binary-search the insertion point, then move the item with C-level list.insert/pop.

    Comparisons drop from O(n^2) to O(n log n) (moves stay O(n^2), but a memmove is
    far cheaper than a Python loop).  A one-comparison check first keeps the O(n) best case.
    """
    for i in range(1, len(arr)):
        item = arr[i]
        if arr[i - 1] <= item:                  # already in place: the common sorted case
            continue
        lo, hi = 0, i                           # find first position whose value > item
        while lo < hi:
            mid = (lo + hi) // 2
            if item < arr[mid]:
                hi = mid
            else:
                lo = mid + 1
        arr.insert(lo, arr.pop(i))              # two C-level memmoves, no temporary copy
    return arr


VARIANTS = {"normal": insertion_sort_normal,
            "optimal": insertion_sort_optimal,
            "optimized": insertion_sort_optimized}

if __name__ == "__main__":
    from algorithms._cli import sort_main
    sort_main(VARIANTS, "Insertion sort")
