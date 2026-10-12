"""Step-by-step replays of each algorithm on a tiny example (feeds the docs' tables and SVG strips).

Each tracer mirrors the REAL algorithm's logic and records a snapshot per step.  Frames:
  arr, marks {index: css class}, labels {index: text}, caption, milestone (shown in the SVG strip).
tests/test_tracers.py asserts every tracer ends in the correct final state.
"""

SORT_EXAMPLE = [5, 2, 4, 6, 1, 3]
LINEAR_EXAMPLE = ([8, 3, 5, 9, 2], 9)
BINARY_EXAMPLE = ([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23)


class Rec:
    def __init__(self):
        self.frames = []

    def snap(self, arr, caption, marks=None, labels=None, milestone=False):
        self.frames.append({"arr": list(arr), "marks": dict(marks or {}), "labels": dict(labels or {}),
                            "caption": caption, "milestone": milestone})


def _done(lo, hi):
    return {i: "done" for i in range(lo, hi)}


def trace_bubble(data=SORT_EXAMPLE):
    a, r, n = list(data), Rec(), len(data)
    r.snap(a, "Start: unsorted array.", milestone=True)
    for p in range(n - 1):
        swapped = False
        for i in range(n - 1 - p):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
                r.snap(a, f"Pass {p + 1}: {a[i + 1]} > {a[i]}, swap.", {i: "act", i + 1: "act", **_done(n - p, n)})
            else:
                r.snap(a, f"Pass {p + 1}: {a[i]} <= {a[i + 1]}, keep.", {i: "cmp", i + 1: "cmp", **_done(n - p, n)})
        end = f"End of pass {p + 1}: {a[n - 1 - p]} bubbled into its final slot."
        if not swapped:
            end = f"Pass {p + 1} made no swap, so the array is sorted: stop early."
        r.snap(a, end, _done(n - 1 - p, n) if swapped else _done(0, n), milestone=True)
        if not swapped:
            break
    r.snap(a, "Sorted.", _done(0, n))
    return r.frames, a


def trace_selection(data=SORT_EXAMPLE):
    a, r, n = list(data), Rec(), len(data)
    r.snap(a, "Start: unsorted array.", milestone=True)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        window = a[i:]
        if m != i:
            a[i], a[m] = a[m], a[i]
            cap = f"Smallest of {window} is {a[i]}: swap it to index {i}."
            marks = {**_done(0, i + 1), m: "act"}
        else:
            cap = f"Smallest of {window} is {a[i]}, already at index {i}: no swap."
            marks = _done(0, i + 1)
        r.snap(a, cap, marks, milestone=True)
    r.snap(a, "Sorted.", _done(0, n))
    return r.frames, a


def trace_insertion(data=SORT_EXAMPLE):
    a, r, n = list(data), Rec(), len(data)
    r.snap(a, "Start: a[0] alone is a sorted prefix.", _done(0, 1), milestone=True)
    for i in range(1, n):
        item, j = a[i], i - 1
        r.snap(a, f"Pick up {item}; it must go into the sorted prefix {a[:i]}.", {**_done(0, i), i: "act"})
        while j >= 0 and a[j] > item:
            a[j + 1] = a[j]
            j -= 1
            view = list(a)
            view[j + 1] = item                  # show the held item sitting in the hole
            r.snap(view, f"{a[j + 2]} > {item}: shift {a[j + 2]} right.", {j + 2: "cmp", j + 1: "act"})
        a[j + 1] = item
        r.snap(a, f"Drop {item} at index {j + 1}. Prefix is sorted up to index {i}.",
               {**_done(0, i + 1), j + 1: "act"}, milestone=True)
    r.snap(a, "Sorted.", _done(0, n))
    return r.frames, a


def trace_merge(data=SORT_EXAMPLE):
    a, r = list(data), Rec()
    r.snap(a, "Start: unsorted array.", milestone=True)

    def sort(lo, hi, depth=0):
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        r.snap(a, f"Split {a[lo:hi]} into {a[lo:mid]} and {a[mid:hi]}.", {i: "cmp" for i in range(lo, hi)})
        sort(lo, mid, depth + 1)
        sort(mid, hi, depth + 1)
        left, right = a[lo:mid], a[mid:hi]
        a[lo:hi] = sorted(left + right)      # same result as the two-pointer merge
        r.snap(a, f"Merge {left} + {right} -> {a[lo:hi]}.", {i: "act" for i in range(lo, hi)}, milestone=True)
    sort(0, len(a))
    r.snap(a, "Sorted.", _done(0, len(a)))
    return r.frames, a


def trace_quick(data=SORT_EXAMPLE):
    a, r = list(data), Rec()
    r.snap(a, "Start: unsorted array.", milestone=True)
    fixed = set()

    def qs(lo, hi):
        if lo > hi:
            return
        if lo == hi:
            fixed.add(lo)
            return
        pivot, i = a[hi], lo
        r.snap(a, f"Range {a[lo:hi + 1]}: pivot = last item = {pivot}.", {**{k: "done" for k in fixed}, hi: "act"})
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        fixed.add(i)
        r.snap(a, f"Partition: smaller items left, larger right. Pivot {pivot} is final at index {i}.",
               {k: "done" for k in fixed}, milestone=True)
        qs(lo, i - 1)
        qs(i + 1, hi)
    qs(0, len(a) - 1)
    r.snap(a, "Sorted.", _done(0, len(a)))
    return r.frames, a


def trace_heap(data=SORT_EXAMPLE):
    a, r, n = list(data), Rec(), len(data)
    r.snap(a, "Start: unsorted array (read it as a binary tree: children of i are 2i+1, 2i+2).", milestone=True)

    def sift(i, size):
        while True:
            c = 2 * i + 1
            if c >= size:
                return
            if c + 1 < size and a[c] < a[c + 1]:
                c += 1
            if a[i] < a[c]:
                a[i], a[c] = a[c], a[i]
                r.snap(a, f"Sift down: parent {a[c]} < child {a[i]}, swap.", {i: "act", c: "act", **_done(size, n)})
                i = c
            else:
                return
    for i in range(n // 2 - 1, -1, -1):
        sift(i, n)
    r.snap(a, f"Max-heap built: the largest item ({a[0]}) is at index 0.", {0: "act"}, milestone=True)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        r.snap(a, f"Swap root with index {end}: {a[end]} is now final.", {0: "act", **_done(end, n)})
        sift(0, end)
        r.snap(a, f"Heap restored on indices 0..{end - 1}.", _done(end, n), milestone=True)
    r.snap(a, "Sorted.", _done(0, n))
    return r.frames, a


def trace_linear(example=LINEAR_EXAMPLE):
    a, key = example
    r = Rec()
    r.snap(a, f"Looking for {key}. Start at index 0.", {}, {}, milestone=True)
    for i, v in enumerate(a):
        if v == key:
            r.snap(a, f"a[{i}] = {v} equals {key}: FOUND at index {i}.", {i: "done"}, {i: "key"}, milestone=True)
            return r.frames, i
        r.snap(a, f"a[{i}] = {v} is not {key}: move on.", {i: "cmp", **{k: "dim" for k in range(i)}},
               milestone=(i == 0))
    r.snap(a, "End of array: NOT FOUND.", {k: "dim" for k in range(len(a))}, milestone=True)
    return r.frames, -1


def trace_binary(example=BINARY_EXAMPLE):
    a, key = example
    r = Rec()
    lo, hi = 0, len(a) - 1
    r.snap(a, f"Looking for {key} in a SORTED array. Window = whole array.", {}, {lo: "lo", hi: "hi"}, milestone=True)
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        dim = {k: "dim" for k in range(len(a)) if k < lo or k > hi}
        lab = {lo: "lo", hi: "hi", mid: "mid"} if mid not in (lo, hi) else {lo: "lo", hi: "hi"}
        if a[mid] == key:
            r.snap(a, f"mid = {mid}: a[{mid}] = {a[mid]} equals {key}: FOUND.", {**dim, mid: "done"}, lab, True)
            return r.frames, mid
        if a[mid] < key:
            r.snap(a, f"mid = {mid}: {a[mid]} < {key}, so the key is to the right: lo = {mid + 1}.",
                   {**dim, mid: "cmp"}, lab, True)
            lo = mid + 1
        else:
            r.snap(a, f"mid = {mid}: {a[mid]} > {key}, so the key is to the left: hi = {mid - 1}.",
                   {**dim, mid: "cmp"}, lab, True)
            hi = mid - 1
    r.snap(a, "Window is empty: NOT FOUND.", {k: "dim" for k in range(len(a))}, {}, True)
    return r.frames, -1


TRACERS = {"bubble_sort": trace_bubble, "selection_sort": trace_selection, "insertion_sort": trace_insertion,
           "merge_sort": trace_merge, "quick_sort": trace_quick, "heap_sort": trace_heap,
           "linear_search": trace_linear, "binary_search": trace_binary}
