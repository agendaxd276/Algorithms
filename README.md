# [A L G O R I T H M S](https://www.youtube.com/playlist?list=PLF7ypemOdw8SY3Wm5fSUd13aDZvYqety3)
[<img height="50" src="https://img.shields.io/badge/youtube-red.svg?&style=for-the-badge&logo=youtube&logoColor=white" />][YouTube]

Searching and sorting in Python - each algorithm in **three tiers** (normal → optimal → optimized), with a
step-by-step guide, best / average / worst-case pictures, and time & space complexity **measured on the real code**.

![All sorts compared](docs/images/overview_sorts_average.svg)

# A. S E A R C H

| Algorithm | Best | Average | Worst | Space | Guide | Video |
|---|---|---|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) | O(1) | [docs](docs/linear_search.md) | [▶](https://youtu.be/Bp-hNxWKm3s) |
| Binary Search | O(log n) | O(log n) | O(log n) | O(1) | [docs](docs/binary_search.md) | [▶](https://youtu.be/Q-ITmLYHwMQ) |

# B. SORT

| Algorithm | Best | Average | Worst | Space | Guide | Video |
|---|---|---|---|---|---|---|
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | [docs](docs/insertion_sort.md) | [▶](https://youtu.be/BNrtNctyMxw) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | [docs](docs/selection_sort.md) | [▶](https://www.youtube.com/watch?v=yMVCgqbh7qQ) |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | [docs](docs/bubble_sort.md) | [▶](https://www.youtube.com/watch?v=DpNiewE-Mbg) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) (duplicates; astronomically rare otherwise) | O(log n) | [docs](docs/quick_sort.md) | [▶](https://youtu.be/fKoPcm-FPdQ) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | [docs](docs/merge_sort.md) | [▶](https://www.youtube.com/watch?v=nQ3dZzH4iLo) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | [docs](docs/heap_sort.md) | [▶](https://youtu.be/0T3dxGvx5Q4) |

<sub>Complexities shown are for the **optimal** tier; each guide covers all three. Cheat-sheet: [docs/COMPLEXITY.md](docs/COMPLEXITY.md).</sub>

## What are "normal", "optimal" and "optimized"?

Like asking a search engine for *"bubble sort"*, *"bubble sort optimal"*, *"bubble sort optimized"*:

| Tier | Meaning |
|---|---|
| **Normal** | the textbook version |
| **Optimal** | the best Big-O this algorithm family can reach (e.g. bubble sort that stops when nothing swapped → best case O(n)) |
| **Optimized** | engineering tweaks you would ship: lower constants, less memory, safer worst case (e.g. introsort) |

## Every guide answers the same questions

1. What is the time complexity - **best, average, worst**? Which input causes each?
2. What is the space complexity?
3. How does it work, step by step (with a worked example and pictures)?
4. Normal vs optimal vs optimized: what changes and what it buys you.

## Run it

```bash
echo "5 2 4 6 1 3" | python -m algorithms.sorting.quick_sort --variant optimized
printf "9 1 5 3\n5\n" | python -m algorithms.searching.binary_search
python -m unittest discover -s tests -t .      # fuzz every variant
python -m tools.build_docs                     # re-measure + regenerate docs/ (~40 s)
```

```python
from algorithms.sorting.merge_sort import merge_sort_optimized
from algorithms.registry import SORTS          # SORTS["heap_sort"]["optimal"](data)
```

How the repo is organised: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

[YouTube]: https://www.youtube.com/playlist?list=PLF7ypemOdw8SY3Wm5fSUd13aDZvYqety3
