"""Selection sort - repeatedly pick the smallest remaining item and put it in front.

Contract (all variants): sort `arr` ascending IN PLACE and return it.  NOT stable.
Best/Average/Worst O(n^2) comparisons (always!) | at most n-1 swaps | Space O(1).
"""


def selection_sort_normal(arr):
    """Normal: find the minimum of the unsorted part, swap it to the front."""
    n = len(arr)
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            if arr[j] < arr[smallest]:
                smallest = j
        arr[smallest], arr[i] = arr[i], arr[smallest]
    return arr


def selection_sort_optimal(arr):
    """Optimal: identical comparison count - n(n-1)/2 can't be improved for this method.

    Only trims busywork: the last element needs no pass, and a swap is skipped when the
    minimum is already in place.  Its real selling point is the minimum NUMBER OF WRITES
    (<= n-1 swaps), useful when writing is expensive (flash memory).
    For a better complexity class switch algorithms: heap sort is "selection sort with
    a heap" and finds each minimum in O(log n).
    """
    n = len(arr)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            if arr[j] < arr[smallest]:
                smallest = j
        if smallest != i:
            arr[smallest], arr[i] = arr[i], arr[smallest]
    return arr


def selection_sort_optimized(arr):
    """Optimized: double-ended selection - place the min AND the max in every pass.

    Handles two elements per pass (half the passes) and uses the "compare the pair
    first" trick: 3 comparisons per 2 elements instead of 4, ~25% fewer than normal.
    Still O(n^2).
    """
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        small = big = lo
        j = lo
        while j < hi:                           # walk the window in pairs
            a, b = j, j + 1
            if arr[b] < arr[a]:
                a, b = b, a                     # now arr[a] <= arr[b]
            if arr[a] < arr[small]:
                small = a
            if arr[big] < arr[b]:
                big = b
            j += 2
        if j == hi:                             # odd leftover element
            if arr[j] < arr[small]:
                small = j
            elif arr[big] < arr[j]:
                big = j
        arr[lo], arr[small] = arr[small], arr[lo]
        if big == lo:                           # the max was just moved by the swap above
            big = small
        arr[hi], arr[big] = arr[big], arr[hi]
        lo += 1
        hi -= 1
    return arr


VARIANTS = {"normal": selection_sort_normal,
            "optimal": selection_sort_optimal,
            "optimized": selection_sort_optimized}

if __name__ == "__main__":
    from algorithms._cli import sort_main
    sort_main(VARIANTS, "Selection sort")
