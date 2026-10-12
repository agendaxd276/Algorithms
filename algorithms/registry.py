"""Registry of every algorithm and its three solution tiers (import this, not the package)."""
from algorithms.searching import binary_search, linear_search
from algorithms.sorting import (bubble_sort, heap_sort, insertion_sort, merge_sort,
                                quick_sort, selection_sort)

SEARCHES = {"linear_search": linear_search.VARIANTS, "binary_search": binary_search.VARIANTS}
SORTS = {"bubble_sort": bubble_sort.VARIANTS, "selection_sort": selection_sort.VARIANTS,
         "insertion_sort": insertion_sort.VARIANTS, "merge_sort": merge_sort.VARIANTS,
         "quick_sort": quick_sort.VARIANTS, "heap_sort": heap_sort.VARIANTS}
