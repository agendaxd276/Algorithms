"""Quick sort - pick a pivot, put smaller items left and larger right, recurse on both sides.

Contract (all variants): sort `arr` ascending IN PLACE and return it.  NOT stable.
Best/Average O(n log n) | Worst O(n^2) (normal: sorted input; optimized: O(n log n) guaranteed).
"""
import random

from algorithms.sorting.heap_sort import heapsort_range


def quick_sort_normal(arr):
    """Normal: last element is the pivot, build new lists (O(n) extra per level).

    Worst case: sorted, reversed or all-equal input - the pivot is always the min/max,
    so one side is empty and recursion goes n levels deep.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    lower, greater = [], []
    for x in arr[:-1]:                          # one pass, one comparison per item
        (lower if x < pivot else greater).append(x)
    arr[:] = quick_sort_normal(lower) + [pivot] + quick_sort_normal(greater)
    return arr


def _quick_random(a, lo, hi):
    while lo < hi:
        p = random.randint(lo, hi)              # random pivot: no fixed "bad input" exists
        a[p], a[hi] = a[hi], a[p]
        pivot = a[hi]
        i = lo                                  # Lomuto partition, in place
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        if i - lo < hi - i:                     # recurse into the SMALLER side only,
            _quick_random(a, lo, i - 1)         # loop on the larger: stack depth <= log2(n)
            lo = i + 1
        else:
            _quick_random(a, i + 1, hi)
            hi = i - 1


def quick_sort_optimal(arr):
    """Optimal: in-place partition + random pivot -> expected O(n log n), O(log n) stack.

    (Lomuto still degrades to O(n^2) on many duplicates - the optimized version fixes that.)
    """
    _quick_random(arr, 0, len(arr) - 1)
    return arr


_CUTOFF = 16


def _median3(x, y, z):
    if x < y:
        if y < z:
            return y
        return z if x < z else x
    if x < z:
        return x
    return z if y < z else y


def _insertion(a, lo, hi):                      # sorts a[lo..hi] inclusive
    for i in range(lo + 1, hi + 1):
        item = a[i]
        j = i - 1
        while j >= lo and a[j] > item:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = item


def _intro(a, lo, hi, depth):
    while hi - lo + 1 > _CUTOFF:
        if depth == 0:                          # recursion too deep -> bad pivots: bail out
            heapsort_range(a, lo, hi + 1)       # to heap sort, guaranteeing O(n log n)
            return
        depth -= 1
        pivot = _median3(a[lo], a[(lo + hi) // 2], a[hi])
        lt, i, gt = lo, lo, hi                  # 3-way (Dutch flag) partition
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif pivot < a[i]:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        # a[lo:lt] < pivot,  a[lt:gt+1] == pivot (done),  a[gt+1:hi+1] > pivot
        if lt - lo < hi - gt:
            _intro(a, lo, lt - 1, depth)
            lo = gt + 1
        else:
            _intro(a, gt + 1, hi, depth)
            hi = lt - 1
    _insertion(a, lo, hi)


def quick_sort_optimized(arr):
    """Optimized: introsort-style.

    median-of-three pivot (kills sorted/reversed worst cases) + 3-way partition (equal
    keys cost O(n), not O(n^2)) + insertion sort for tiny ranges + smaller-side recursion
    + heap-sort fallback when depth exceeds 2*log2(n).  Worst case O(n log n).
    """
    _intro(arr, 0, len(arr) - 1, 2 * len(arr).bit_length())
    return arr


VARIANTS = {"normal": quick_sort_normal,
            "optimal": quick_sort_optimal,
            "optimized": quick_sort_optimized}

if __name__ == "__main__":
    from algorithms._cli import sort_main
    sort_main(VARIANTS, "Quick sort")
