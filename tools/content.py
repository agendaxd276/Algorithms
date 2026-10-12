"""Hand-written teaching content for each algorithm.  Measured numbers are NOT here - build_docs.py
inserts them from the real code, so claims and measurements can't drift apart."""

# theory[tier] = (best, average, worst, space)
ALGOS = {}

ALGOS["bubble_sort"] = dict(
    title="Bubble Sort", kind="sort", module="sorting/bubble_sort.py",
    one_liner="Swap neighbours that are out of order; each pass floats the largest remaining value to the end.",
    props=dict(stable="Yes", in_place="Yes", adaptive="Only with the early-exit flag"),
    theory=dict(normal=("O(n²)", "O(n²)", "O(n²)", "O(1)"),
                optimal=("O(n)", "O(n²)", "O(n²)", "O(1)"),
                optimized=("O(n)", "O(n²)", "O(n²)", "O(1)")),
    flow="""flowchart TD
    A["start: end = n-1"] --> B{"end > 0 ?"}
    B -- no --> Z["sorted"]
    B -- yes --> C["i = 0, last_swap = 0"]
    C --> D{"i < end ?"}
    D -- yes --> E{"a[i] > a[i+1] ?"}
    E -- yes --> F["swap, last_swap = i"] --> G["i = i + 1"]
    E -- no --> G
    G --> D
    D -- no --> H["end = last_swap"] --> B""",
    steps=[
        "Look at the first two neighbours, `arr[0]` and `arr[1]`.",
        "If the left one is **bigger**, swap them. Otherwise leave them.",
        "Step one position right and repeat until you reach the end of the *unsorted* part. "
        "The biggest value has now \"bubbled\" to the end and is in its **final** slot.",
        "Shrink the unsorted part by one (the last slot is finished) and start the next pass from the left.",
        "**Optimal tier:** if a whole pass made **zero swaps**, nothing is out of order, so stop early.",
    ],
    time_steps=[
        "**Count the comparisons.** Pass 1 compares n−1 pairs, pass 2 compares n−2, … the last pass compares 1. "
        "Total = (n−1) + (n−2) + … + 1 = **n(n−1)/2** → O(n²).",
        "**Best case (already sorted).** Normal tier still does all n(n−1)/2 comparisons → O(n²). "
        "With the swap flag, pass 1 makes n−1 comparisons and **no swaps**, so we stop → **O(n)**.",
        "**Worst case (reversed).** Every comparison swaps: n(n−1)/2 comparisons *and* n(n−1)/2 swaps → O(n²).",
        "**Average case (random).** Each pair is inverted with probability ½, so about n(n−1)/4 swaps, "
        "and the flag almost never fires early → still ≈ n(n−1)/2 comparisons → O(n²).",
    ],
    space_steps=[
        "Sorting happens inside the input list: no copy is made.",
        "Extra variables are just `i`, the pass counter, the `swapped` flag and one temporary for a swap → **O(1)**.",
        "No recursion, so no stack growth.",
    ],
    tiers=dict(
        normal=("Textbook double loop, no early exit.",
                "Always n(n−1)/2 comparisons, even when the input is already sorted."),
        optimal=("Add a `swapped` flag and stop when a pass changes nothing.",
                 "Best case drops to O(n). This is the version most people mean by \"bubble sort\". "
                 "(Sources disagree on bubble sort's best case: O(n) vs O(n²) - the difference is exactly "
                 "this flag.)"),
        optimized=("Remember the position of the **last swap**; everything after it is already sorted, "
                   "so the next pass can end there.",
                   "Skips sorted tails in one jump. Big win when only a few items are out of place; "
                   "no gain on random data."),
    ),
    when="Teaching and tiny or nearly-sorted inputs. For anything else prefer insertion sort (same O(n²), "
         "far fewer writes) or an O(n log n) sort.",
    faq=[("Is bubble sort ever the best choice?",
          "Almost never. Insertion sort has the same best/worst complexity and does less work per step."),
         ],
)

ALGOS["selection_sort"] = dict(
    title="Selection Sort", kind="sort", module="sorting/selection_sort.py",
    one_liner="Find the smallest remaining value and swap it to the front, again and again.",
    props=dict(stable="No", in_place="Yes", adaptive="No"),
    theory=dict(normal=("O(n²)", "O(n²)", "O(n²)", "O(1)"),
                optimal=("O(n²)", "O(n²)", "O(n²)", "O(1)"),
                optimized=("O(n²)", "O(n²)", "O(n²)", "O(1)")),
    flow="""flowchart TD
    A["i = 0"] --> B{"i < n-1 ?"}
    B -- no --> Z["sorted"]
    B -- yes --> C["smallest = i"]
    C --> D["scan j = i+1 .. n-1: if a[j] < a[smallest] then smallest = j"]
    D --> E{"smallest != i ?"}
    E -- yes --> F["swap a[i], a[smallest]"] --> G["i = i + 1"]
    E -- no --> G
    G --> B""",
    steps=[
        "Treat the array as two parts: a **sorted** prefix (empty at first) and an **unsorted** rest.",
        "Scan the whole unsorted part and remember where the **smallest** value is.",
        "Swap that smallest value with the first unsorted slot. The sorted prefix grows by one.",
        "Repeat until only one unsorted item remains (it is automatically the largest, so it's in place).",
    ],
    time_steps=[
        "**Count the comparisons.** Finding the minimum of k items always costs k−1 comparisons - there is "
        "no shortcut, even if the data is sorted. Passes scan n−1, n−2, …, 1 items → **n(n−1)/2** every time.",
        "**Best = average = worst = O(n²).** Selection sort cannot notice that the data is already sorted.",
        "**Swaps are the one cheap part:** at most one per pass → **≤ n−1 swaps (O(n))**, the fewest of any "
        "simple sort. Use it when writing is expensive.",
    ],
    space_steps=["Only `smallest`, `i`, `j` and a swap temporary → **O(1)**, in place, no recursion."],
    tiers=dict(
        normal=("Textbook version: always swap, even with itself.", "n(n−1)/2 comparisons in every case."),
        optimal=("Skip the last pass and skip swaps when the minimum is already in place.",
                 "The comparison count cannot be improved for this method - it is already optimal *for "
                 "selection sort*. For a better class, use heap sort: selection sort + a heap that finds each "
                 "minimum in O(log n)."),
        optimized=("**Double-ended selection**: each pass places the minimum **and** the maximum, "
                   "comparing items in pairs (3 comparisons per 2 items instead of 4).",
                   "About 25% fewer comparisons and half the passes. Still O(n²)."),
    ),
    when="When the number of writes must be minimal (flash memory, expensive swaps) and n is small.",
    faq=[("Why isn't selection sort stable?",
          "Sorting `[2a, 2b, 1]`: swapping `1` with `2a` puts `2a` *after* `2b`, so equal keys change order.")],
)

ALGOS["insertion_sort"] = dict(
    title="Insertion Sort", kind="sort", module="sorting/insertion_sort.py",
    one_liner="Grow a sorted prefix: take the next item and slide it left into its place - like sorting playing cards in your hand.",
    props=dict(stable="Yes", in_place="Yes", adaptive="Yes (O(n) on sorted input)"),
    theory=dict(normal=("O(n)", "O(n²)", "O(n²)", "O(1)"),
                optimal=("O(n)", "O(n²)", "O(n²)", "O(1)"),
                optimized=("O(n) comparisons", "O(n log n) comparisons, O(n²) moves",
                           "O(n log n) comparisons, O(n²) moves", "O(1)")),
    flow="""flowchart TD
    A["i = 1"] --> B{"i < n ?"}
    B -- no --> Z["sorted"]
    B -- yes --> C["item = a[i], j = i-1"]
    C --> D{"j >= 0 and a[j] > item ?"}
    D -- yes --> E["a[j+1] = a[j], j = j-1"] --> D
    D -- no --> F["a[j+1] = item, i = i+1"] --> B""",
    steps=[
        "The first element on its own is a sorted prefix of length 1.",
        "Pick up the next element (`item`).",
        "Walk left through the sorted prefix; every value **bigger** than `item` shifts one slot right.",
        "Drop `item` into the gap that opens up. The sorted prefix is now one longer.",
        "Repeat until the prefix covers the whole array.",
    ],
    time_steps=[
        "**Count the work per item.** Inserting item i compares it with 0…i items of the sorted prefix.",
        "**Best case (sorted):** each item is compared once and not moved → n−1 comparisons → **O(n)**.",
        "**Worst case (reversed):** item i is bigger than nothing, so it travels all the way left: "
        "1+2+…+(n−1) = n(n−1)/2 → **O(n²)**.",
        "**Average case (random):** on average it travels half the prefix → ≈ n²/4 → **O(n²)**.",
        "**Exact rule:** time = Θ(n + I), where I is the number of *inversions* (pairs out of order). "
        "That is why nearly-sorted data is fast.",
    ],
    space_steps=["One saved `item` and two indices → **O(1)**. The binary-insertion version still moves items with "
                 "`list.insert/pop` (an in-place memmove), so it stays O(1) extra."],
    tiers=dict(
        normal=("Swap the item left one step at a time.", "3 writes per step."),
        optimal=("Hold the item aside and **shift** bigger items right (no swaps).",
                 "Same comparisons, a third of the writes. Same big-O."),
        optimized=("**Binary insertion**: find the spot with binary search (O(log i) comparisons), then move "
                   "the item with one C-level `pop`/`insert`; check `a[i-1] <= item` first so sorted input "
                   "stays O(n).",
                   "Comparisons fall to O(n log n); moves stay O(n²) but run as a memmove, so on random data "
                   "this is dramatically faster in practice."),
    ),
    when="Small arrays (n < ~20-50), nearly-sorted data, streaming data (online). Real libraries use it as the "
         "finishing step inside quick sort / Timsort.",
    faq=[("Why do real sort functions call insertion sort?",
          "For tiny ranges its low overhead beats recursion; the O(n²) cost is irrelevant at n ≈ 16.")],
)

ALGOS["merge_sort"] = dict(
    title="Merge Sort", kind="sort", module="sorting/merge_sort.py",
    one_liner="Divide the array in half, sort each half, then merge the two sorted halves.",
    props=dict(stable="Yes", in_place="No (needs O(n) extra)", adaptive="Only in the optimized tier"),
    theory=dict(normal=("O(n log n)", "O(n log n)", "O(n log n)", "O(n)"),
                optimal=("O(n log n)", "O(n log n)", "O(n log n)", "O(n)"),
                optimized=("O(n)", "O(n log n)", "O(n log n)", "O(n)")),
    flow="""flowchart TD
    A["merge_sort(a, lo, hi)"] --> B{"hi - lo < 2 ?"}
    B -- yes --> Z["return (1 item is sorted)"]
    B -- no --> C["mid = (lo + hi) // 2"]
    C --> D["merge_sort(a, lo, mid)"] --> E["merge_sort(a, mid, hi)"]
    E --> F["merge the two sorted halves"] --> Z""",
    steps=[
        "**Divide:** split the array at the middle into a left and a right half.",
        "**Conquer:** sort each half by calling merge sort on it (a 0- or 1-item array is already sorted - "
        "this stops the recursion).",
        "**Merge:** keep one pointer at the front of each sorted half; repeatedly copy the **smaller** front "
        "item to the output and advance that pointer. When one half runs out, copy the rest of the other.",
        "Because the left item wins ties (`<=`), equal items keep their order: merge sort is **stable**.",
    ],
    time_steps=[
        "**Levels.** Halving n until size 1 takes log₂ n levels.",
        "**Work per level.** On each level the merges together touch all n items once: ≤ n−1 comparisons "
        "(and exactly n writes).",
        "**Total = n × log₂ n → O(n log n)**, written as the recurrence T(n) = 2·T(n/2) + O(n).",
        "**Best case:** halves already in order - each merge ends after n/2 comparisons → (n/2)·log₂ n, still "
        "O(n log n). The optimized tier checks `a[mid-1] <= a[mid]` and skips the merge, giving **O(n)**.",
        "**Worst case:** merges that interleave perfectly use n−1 comparisons each → n·log₂ n − n + 1. "
        "**Average** is within ~10% of that. No input can push it past O(n log n).",
    ],
    space_steps=[
        "Merging needs somewhere to put items while pointers move → an **auxiliary buffer**.",
        "Normal tier allocates new `left`/`right` lists at every level (peak ≈ 2n items).",
        "Optimal tier reuses **one buffer of n/2** items for the whole sort → **O(n)** extra.",
        "Recursion adds O(log n) stack frames - dominated by the O(n) buffer.",
    ],
    tiers=dict(
        normal=("Slice into new left/right lists, sort recursively, merge back.", "Simple; allocates at every level."),
        optimal=("One reusable half-size buffer; merge in place into the original list.",
                 "Same O(n log n); less memory and far fewer allocations."),
        optimized=("Add an **insertion-sort cutoff** for ranges ≤ 8 and **skip** the merge when the two halves "
                   "are already ordered.",
                   "Sorted input becomes O(n); fewer function calls. Honest trade-off: on adversarial inputs it can "
                   "use *more* comparisons than the normal tier (insertion sort on 8-item leaves) - the win is "
                   "fewer calls and the O(n) sorted case. Same ideas Python's Timsort builds on."),
    ),
    when="You need guaranteed O(n log n), a **stable** sort, or you are sorting linked lists / data on disk "
         "(external merge sort). Avoid when memory is tight.",
    faq=[("Merge sort or quick sort?",
          "Merge sort: guaranteed O(n log n) + stable but needs O(n) memory. Quick sort: in place and usually "
          "faster in practice, but the worst case needs care (see the optimized tier).")],
)

ALGOS["quick_sort"] = dict(
    title="Quick Sort", kind="sort", module="sorting/quick_sort.py",
    one_liner="Pick a pivot, put smaller items on its left and larger on its right, then sort both sides the same way.",
    props=dict(stable="No", in_place="Yes (normal tier copies)", adaptive="Optimized tier handles sorted/equal input"),
    theory=dict(normal=("O(n log n)", "O(n log n)", "O(n²)", "O(n) worst / O(log n) average"),
                optimal=("O(n log n)", "O(n log n)", "O(n²) (duplicates; astronomically rare otherwise)", "O(log n)"),
                optimized=("O(n) (all equal)", "O(n log n)", "O(n log n)", "O(log n)")),
    flow="""flowchart TD
    A["quick_sort(a, lo, hi)"] --> B{"small range ?"}
    B -- yes --> Z["return / insertion sort"]
    B -- no --> C["choose pivot"]
    C --> D["partition: smaller left, equal middle, larger right"]
    D --> E["recurse on the smaller side"]
    D --> F["loop on the larger side"]
    E --> Z
    F --> B""",
    steps=[
        "**Pick a pivot** (normal tier: the last element; optimal: random; optimized: median of first/middle/last).",
        "**Partition:** rearrange so that everything smaller than the pivot is to its left and everything larger "
        "to its right. The pivot is now in its **final** position.",
        "**Recurse** on the left part and on the right part (a part with 0 or 1 items is done).",
        "No merge step is needed - once both sides are sorted the whole range is sorted.",
        "**Optimized tier extras:** 3-way partition (items equal to the pivot are finished at once), insertion "
        "sort for ranges ≤ 16, recurse on the smaller side first, and fall back to heap sort if recursion gets "
        "deeper than 2·log₂ n (this combination is called **introsort**).",
    ],
    time_steps=[
        "**Cost of one partition** of k items = k−1 comparisons → O(k).",
        "**Best / average (balanced splits).** The pivot lands near the middle: T(n) = 2·T(n/2) + O(n) → "
        "**O(n log n)**. For random pivots the expected count is ≈ 2·n·ln n ≈ 1.39·n·log₂ n comparisons.",
        "**Worst case (pivot is always the min or max).** One side is empty: T(n) = T(n−1) + O(n) → "
        "n(n−1)/2 → **O(n²)**. With a *last-element* pivot this is triggered by **already-sorted, reversed "
        "or all-equal input** - common real-world data!",
        "**Fixes.** Random pivot: no fixed bad input. Median-of-three: kills sorted/reversed input. 3-way "
        "partition: kills all-equal input. Introsort depth limit: even adversarial inputs stay O(n log n).",
    ],
    space_steps=[
        "Normal tier builds new lower/greater lists at each level (O(n) extra) and recurses up to **n deep** on "
        "bad input → O(n) stack - on a 1000-item sorted list Python hits its recursion limit.",
        "Optimal/optimized tiers partition **in place** and always recurse into the **smaller** side first "
        "(looping on the larger), so the stack never exceeds log₂ n frames → **O(log n)**.",
    ],
    tiers=dict(
        normal=("Last element as pivot; build `lower` and `greater` lists; concatenate.",
                "Easy to read. O(n²) on sorted/reversed/all-equal input, O(n) recursion depth."),
        optimal=("In-place Lomuto partition + **random pivot** + recurse into the smaller side.",
                 "Expected O(n log n) for any input order and O(log n) stack. (Many duplicates still hurt "
                 "Lomuto.)"),
        optimized=("**Introsort**: median-of-three pivot, 3-way partition, insertion-sort cutoff (16), "
                   "smaller-side recursion, heap-sort fallback at depth 2·log₂ n.",
                   "Guaranteed O(n log n) worst case and O(n) on all-equal input. It may count slightly *more* "
                   "comparisons than the random-pivot version on random data (the insertion-sort cutoff) but "
                   "makes fewer calls. This is the design behind C++ `std::sort`."),
    ),
    when="General-purpose in-memory sorting where average speed matters. Use the optimized tier (or the "
         "library sort) - not the textbook version - on real data.",
    faq=[("Why is quick sort's worst case O(n²) but it is still popular?",
          "The worst case needs consistently terrible pivots. Randomization or median-of-three makes that "
          "vanishingly rare, and introsort makes it impossible.")],
)

ALGOS["heap_sort"] = dict(
    title="Heap Sort", kind="sort", module="sorting/heap_sort.py",
    one_liner="Arrange the data as a max-heap, then repeatedly move the largest value to the end.",
    props=dict(stable="No", in_place="Yes", adaptive="No"),
    theory=dict(normal=("O(n log n)", "O(n log n)", "O(n log n)", "O(log n) recursion"),
                optimal=("O(n log n)", "O(n log n)", "O(n log n)", "O(1)"),
                optimized=("O(n log n)", "O(n log n)", "O(n log n)", "O(1)")),
    flow="""flowchart TD
    A["build max-heap: sift down from n/2-1 to 0"] --> B["end = n-1"]
    B --> C{"end > 0 ?"}
    C -- no --> Z["sorted"]
    C -- yes --> D["swap a[0] and a[end]"]
    D --> E["sift a[0] down inside a[0..end-1]"]
    E --> F["end = end - 1"] --> C""",
    steps=[
        "Read the array as a binary tree: the children of index `i` are `2i+1` and `2i+2`.",
        "**Build a max-heap** (every parent ≥ its children) by sifting each non-leaf node down, starting from "
        "the last parent `n//2 − 1` and moving to index 0. Now `arr[0]` is the largest value.",
        "**Swap** the root with the last item of the heap. The largest value is now in its final slot; "
        "shrink the heap by one.",
        "**Sift the new root down** to restore the heap property.",
        "Repeat steps 3-4 until the heap has one item.",
    ],
    time_steps=[
        "**Build the heap:** a node at height h costs O(h) to sift, and there are ≈ n/2^(h+1) such nodes: "
        "Σ h·n/2^(h+1) = **O(n)** (not n log n - most nodes are near the bottom).",
        "**Extract n−1 times:** each swap is O(1) and each sift-down goes at most log₂ n levels → "
        "(n−1)·log₂ n = **O(n log n)**.",
        "**Best = average = worst = O(n log n)** for distinct keys: the heap's shape does not depend on "
        "the input order. (With **all-equal** keys, sifts stop immediately and the sort is O(n).)",
        "**Normal sift costs 2 comparisons per level** (find the larger child, compare with the parent). "
        "The optimized *bottom-up* variant spends 1 per level on the way down, then a few on the way up "
        "≈ n·log₂ n comparisons in total.",
    ],
    space_steps=[
        "The heap lives **inside** the input array → no copy.",
        "Normal tier: recursive `heapify` uses O(log n) stack. Optimal/optimized: iterative → **O(1)**.",
    ],
    tiers=dict(
        normal=("Recursive `heapify`; build from index n//2−1 down to 0.", "O(log n) recursion stack."),
        optimal=("Iterative sift-down loop - no recursion.", "True O(1) extra space."),
        optimized=("**Bottom-up sift** (Floyd): slide the hole to a leaf along the larger children, then climb "
                   "back to where the item fits.",
                   "≈ half the comparisons of the standard sift-down."),
    ),
    when="You need a hard O(n log n) worst case **and** O(1) extra memory (embedded systems, introsort's "
         "fallback). It is usually slower than quick sort because it jumps around memory (poor cache locality).",
    faq=[],
)

ALGOS["linear_search"] = dict(
    title="Linear Search", kind="search", module="searching/linear_search.py",
    one_liner="Check every element, one by one, until you find the key or run out of elements.",
    props=dict(stable="n/a", in_place="Yes", adaptive="Stops at the first match"),
    theory=dict(normal=("O(1)", "O(n)", "O(n)", "O(1)"),
                optimal=("O(1)", "O(n)", "O(n)", "O(1)"),
                optimized=("O(1)", "O(n)", "O(n)", "O(1)")),
    flow="""flowchart TD
    A["i = 0"] --> B{"i < n ?"}
    B -- no --> N["return -1 (not found)"]
    B -- yes --> C{"a[i] == key ?"}
    C -- yes --> F["return i"]
    C -- no --> D["i = i + 1"] --> B""",
    steps=[
        "Start at index 0.",
        "Compare `arr[i]` with the key. If equal, return `i` - done.",
        "Otherwise move to `i + 1`.",
        "If you run past the last element, the key is not there: return −1 (`NOT FOUND`).",
    ],
    time_steps=[
        "**Best case:** the key is the first element → **1 comparison, O(1)**.",
        "**Worst case:** the key is last *or missing* → **n comparisons, O(n)**.",
        "**Average case:** if the key is present and every position is equally likely, you look at "
        "(1+2+…+n)/n = **(n+1)/2** elements → O(n). A *missing* key always costs n.",
        "**Why you can't beat it:** on unsorted data, any element you skip might be the key, so Ω(n) is "
        "unavoidable - linear search is *optimal* for unsorted data.",
    ],
    space_steps=["Only the index variable → **O(1)**. (The sentinel variant temporarily overwrites the last slot "
                 "and restores it.)"],
    tiers=dict(
        normal=("The textbook `for` loop.", "One comparison per element."),
        optimal=("**Sentinel search**: place the key at the end so the loop needs no bounds check.",
                 "Asymptotically optimal already; this just trims the loop (about half the work per step in "
                 "compiled languages). In CPython the benefit is small."),
        optimized=("Use `list.index` - the same scan, executed by CPython's C loop.",
                   "Same O(n) but typically 5-50× faster in Python."),
    ),
    when="Unsorted data, small lists, or when you search once (sorting first would cost more than scanning).",
    faq=[("When is linear search better than binary search?",
          "When the data is unsorted, tiny, or searched only once - sorting costs O(n log n), more than one scan.")],
)

ALGOS["binary_search"] = dict(
    title="Binary Search", kind="search", module="searching/binary_search.py",
    one_liner="In a sorted array, look at the middle and throw away the half that cannot contain the key.",
    props=dict(stable="n/a", in_place="Yes", adaptive="Needs SORTED input"),
    theory=dict(normal=("O(1)", "O(log n)", "O(log n)", "O(1)"),
                optimal=("O(log n)", "O(log n)", "O(log n)", "O(1)"),
                optimized=("O(1)", "O(log log n) on evenly spread data", "O(n) on skewed data", "O(1)")),
    flow="""flowchart TD
    A["start = 0, end = n-1"] --> B{"start <= end ?"}
    B -- no --> N["return -1 (not found)"]
    B -- yes --> C["mid = start + (end-start)//2"]
    C --> D{"a[mid] == key ?"}
    D -- yes --> F["return mid"]
    D -- no --> E{"a[mid] < key ?"}
    E -- yes --> G["start = mid + 1"] --> B
    E -- no --> H["end = mid - 1"] --> B""",
    steps=[
        "**Requirement:** the array must already be sorted ascending.",
        "Keep a window `[start, end]`, initially the whole array.",
        "Look at the middle element `mid`. If it equals the key → done.",
        "If `arr[mid] < key`, the key can only be on the **right** → `start = mid + 1`. "
        "Otherwise it can only be on the **left** → `end = mid − 1`.",
        "Repeat. If the window becomes empty (`start > end`) the key is not present.",
    ],
    time_steps=[
        "**Each step halves the window:** n → n/2 → n/4 → … → 1. The number of halvings is "
        "**⌊log₂ n⌋ + 1** → O(log n). A million items need ≤ 20 steps; a billion ≤ 30.",
        "**Best case:** the key is exactly in the middle → **1 comparison, O(1)** (normal tier).",
        "**Worst case:** the key is missing or found at the very last step → ⌊log₂ n⌋ + 1 iterations "
        "(×2 comparisons per iteration in the normal tier because of `==` then `<`).",
        "**Average case:** ≈ log₂ n − 1 iterations → O(log n).",
        "**Trade-off in the optimal tier:** one comparison per iteration (`<` only) and it always runs the "
        "full ⌈log₂ n⌉ iterations - so no lucky O(1) exit, but fewer total comparisons on average and the "
        "**first** match is returned.",
        "**Optimized (interpolation):** guesses the position from the key's value. On evenly spread data "
        "≈ log₂ log₂ n probes; on skewed data (powers of 2) it can crawl at O(n).",
    ],
    space_steps=["Iterative: `start`, `end`, `mid` → **O(1)**. (A recursive version would use O(log n) stack.)",
                 "Input is **not** copied."],
    tiers=dict(
        normal=("Classic loop: compare `==`, then `<`; `end = mid − 1`.", "2 comparisons per iteration."),
        optimal=("**Lower-bound** form on a half-open window `[lo, hi)`: ONE comparison per iteration, "
                 "returns the first occurrence.",
                 "≈ log₂ n comparisons - the information-theoretic minimum - so O(log n) cannot be beaten "
                 "by comparison-based search. Python ships this as `bisect.bisect_left`."),
        optimized=("**Interpolation search**: probe `lo + (key−a[lo])·(hi−lo)/(a[hi]−a[lo])`.",
                   "Fastest on uniformly distributed numbers; falls back to O(n) on skewed data and "
                   "needs numeric keys. Early range check rejects out-of-range keys in O(1)."),
    ),
    when="Sorted data that is searched many times (sorting once costs O(n log n), each search then O(log n)). "
         "Also the idea behind `bisect`, database indexes and \"binary search on the answer\" problems.",
    faq=[("Why `mid = start + (end - start) // 2` and not `(start + end) // 2`?",
          "In C/Java `start + end` can overflow a 32-bit int. Python ints don't overflow, but the safe form "
          "is a good habit.")],
)

ORDER = ["linear_search", "binary_search", "bubble_sort", "selection_sort", "insertion_sort",
         "merge_sort", "quick_sort", "heap_sort"]

REFERENCES = {
    "sorting": [
        ("Time and Space Complexities of Sorting Algorithms Explained (Interview Kickstart)",
         "https://interviewkickstart.com/blogs/learn/time-complexities-of-all-sorting-algorithms"),
        ("Sorting Algorithms Cheat Sheet (NeetCode)", "https://neetcode.io/cheatsheets/sorting-algorithms"),
        ("Introsort (Wikipedia)", "https://en.wikipedia.org/wiki/Introsort"),
        ("Timsort (Wikipedia)", "https://en.wikipedia.org/wiki/Timsort"),
        ("Introspective Sorting and Selection Algorithms - Musser (PDF)",
         "https://webpages.charlotte.edu/rbunescu/courses/ou/cs4040/introsort.pdf"),
    ],
    "searching": [
        ("Searching Algorithms overview (archman.dev)",
         "https://archman.dev/docs/algorithms-and-data-structures/sorting-and-searching/searching-algorithms"),
    ],
}
