"""Bubble sort - repeatedly swap neighbours that are out of order.

Contract (all variants): sort `arr` ascending IN PLACE and return it.  Stable.
Normal: Best/Avg/Worst O(n^2) | Optimal & Optimized: Best O(n), Avg/Worst O(n^2) | Space O(1).
"""


def bubble_sort_normal(arr):
    """Normal: n-1 passes, always.  The sorted tail shrinks, but there is no early exit."""
    n = len(arr)
    for p in range(n - 1):
        for i in range(n - 1 - p):             # last p items are already in place
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


def bubble_sort_optimal(arr):
    """Optimal: stop as soon as a whole pass makes no swap (that means "sorted").

    Turns the best case (already sorted input) from O(n^2) into O(n).
    """
    n = len(arr)
    for p in range(n - 1):
        swapped = False
        for i in range(n - 1 - p):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
    return arr


def bubble_sort_optimized(arr):
    """Optimized: remember WHERE the last swap happened; everything after it is sorted.

    Skips the already-sorted tail in one jump, so mostly-sorted data finishes in far
    fewer comparisons than the plain early-exit flag.
    """
    end = len(arr) - 1                          # last index that may still be unsorted
    while end > 0:
        last_swap = 0
        for i in range(end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                last_swap = i
        end = last_swap
    return arr


VARIANTS = {"normal": bubble_sort_normal,
            "optimal": bubble_sort_optimal,
            "optimized": bubble_sort_optimized}

if __name__ == "__main__":
    from algorithms._cli import sort_main
    sort_main(VARIANTS, "Bubble sort")
