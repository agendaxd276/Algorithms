"""Heap sort - build a max-heap, then repeatedly swap the root to the end and re-heapify.

Contract (all variants): sort `arr` ascending IN PLACE and return it.  NOT stable.
Best/Average/Worst O(n log n) | Space O(1) (normal: O(log n) recursion stack).
"""


# ---------------------------------------------------------------- normal
def _heapify(arr, n, i):
    """Recursive sift-down of arr[i] inside the heap arr[:n]."""
    largest = i
    left, right = 2 * i + 1, 2 * i + 2
    if left < n and arr[largest] < arr[left]:
        largest = left
    if right < n and arr[largest] < arr[right]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


def heap_sort_normal(arr):
    """Normal: recursive heapify. Leaves (index >= n//2) are already heaps, so skip them."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):         # build max-heap bottom-up
        _heapify(arr, n, i)
    for end in range(n - 1, 0, -1):             # move current max to its final slot
        arr[0], arr[end] = arr[end], arr[0]
        _heapify(arr, end, 0)
    return arr


# ---------------------------------------------------------------- optimal
def _sift_down(a, lo, i, n):
    """Iterative sift-down on the heap stored in a[lo:lo+n] (i is relative to lo)."""
    while True:
        child = 2 * i + 1
        if child >= n:
            return
        if child + 1 < n and a[lo + child] < a[lo + child + 1]:
            child += 1
        if a[lo + i] < a[lo + child]:
            a[lo + i], a[lo + child] = a[lo + child], a[lo + i]
            i = child
        else:
            return


def heapsort_range(a, lo, hi):
    """Heap-sort a[lo:hi] in place with O(1) extra space (also used by quick sort's fallback)."""
    n = hi - lo
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(a, lo, i, n)
    for end in range(n - 1, 0, -1):
        a[lo], a[lo + end] = a[lo + end], a[lo]
        _sift_down(a, lo, 0, end)


def heap_sort_optimal(arr):
    """Optimal: iterative sift-down, so no recursion stack - truly O(1) extra space."""
    heapsort_range(arr, 0, len(arr))
    return arr


# ---------------------------------------------------------------- optimized
def _sift_down_bottom_up(a, i, n):
    """Floyd's trick: slide down to a leaf along the larger children (1 comparison per
    level instead of 2), then climb back up to where the item really belongs."""
    item = a[i]
    j = i
    while 2 * j + 1 < n:                        # 1) descend to a leaf
        child = 2 * j + 1
        if child + 1 < n and a[child] < a[child + 1]:
            child += 1
        j = child
    while a[j] < item:                          # 2) climb up until item fits
        j = (j - 1) // 2
    carry, a[j] = a[j], item                    # 3) rotate the path: item in, ancestors up
    while j > i:
        j = (j - 1) // 2
        carry, a[j] = a[j], carry


def heap_sort_optimized(arr):
    """Optimized: bottom-up heapsort - about n*log2(n) comparisons instead of 2*n*log2(n)."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down_bottom_up(arr, i, n)
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down_bottom_up(arr, 0, end)
    return arr


VARIANTS = {"normal": heap_sort_normal,
            "optimal": heap_sort_optimal,
            "optimized": heap_sort_optimized}

if __name__ == "__main__":
    from algorithms._cli import sort_main
    sort_main(VARIANTS, "Heap sort")
