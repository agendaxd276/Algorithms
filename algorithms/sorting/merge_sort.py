"""Merge sort - split in half, sort each half, merge the two sorted halves.

Contract (all variants): sort `arr` ascending IN PLACE and return it.  Stable.
Best/Average/Worst O(n log n) (optimized: best O(n)) | Space O(n).
"""


def merge_sort_normal(arr):
    """Normal: slice into new left/right lists at every level, merge back into arr."""
    if len(arr) > 1:
        mid = len(arr) // 2
        left, right = arr[:mid], arr[mid:]
        merge_sort_normal(left)
        merge_sort_normal(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:             # <= keeps equal items in original order
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr


def _merge(a, aux, lo, mid, hi):
    """Merge sorted a[lo:mid] and a[mid:hi]: park only the LEFT run in aux (n/2 buffer).

    The write index k never overtakes the right-run read index j, so nothing unread is lost.
    """
    m = mid - lo
    aux[:m] = a[lo:mid]
    i, j, k = 0, mid, lo
    while i < m and j < hi:
        if a[j] < aux[i]:                       # strict <: ties take the left item (stable)
            a[k] = a[j]
            j += 1
        else:
            a[k] = aux[i]
            i += 1
        k += 1
    while i < m:                                # leftover right items are already in place
        a[k] = aux[i]
        i += 1
        k += 1


def _sort(a, aux, lo, hi):
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    _sort(a, aux, lo, mid)
    _sort(a, aux, mid, hi)
    _merge(a, aux, lo, mid, hi)


def merge_sort_optimal(arr):
    """Optimal: ONE reusable half-size buffer instead of fresh lists at every level."""
    _sort(arr, [None] * (len(arr) // 2 + 1), 0, len(arr))
    return arr


_CUTOFF = 8


def _insertion(a, lo, hi):
    for i in range(lo + 1, hi):
        item = a[i]
        j = i - 1
        while j >= lo and a[j] > item:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = item


def _sort_fast(a, aux, lo, hi):
    if hi - lo <= _CUTOFF:                      # tiny ranges: insertion sort beats recursion
        _insertion(a, lo, hi)
        return
    mid = (lo + hi) // 2
    _sort_fast(a, aux, lo, mid)
    _sort_fast(a, aux, mid, hi)
    if not (a[mid] < a[mid - 1]):               # halves already in order: nothing to merge
        return
    _merge(a, aux, lo, mid, hi)


def merge_sort_optimized(arr):
    """Optimized: single half-size buffer + insertion-sort cutoff for tiny ranges + skip merges of
    already-ordered halves (makes sorted input O(n)).  Same ideas as Python's Timsort."""
    _sort_fast(arr, [None] * (len(arr) // 2 + 1), 0, len(arr))
    return arr


VARIANTS = {"normal": merge_sort_normal,
            "optimal": merge_sort_optimal,
            "optimized": merge_sort_optimized}

if __name__ == "__main__":
    from algorithms._cli import sort_main
    sort_main(VARIANTS, "Merge sort")
