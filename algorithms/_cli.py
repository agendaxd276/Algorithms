"""Tiny command-line front end shared by every algorithm module.

Usage:  python -m algorithms.sorting.bubble_sort [--variant normal|optimal|optimized]
Then type the numbers (and, for searches, the key on the next line) on stdin.
"""
import argparse


def _parse(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--variant", choices=("normal", "optimal", "optimized"),
                        default="optimal", help="which solution tier to run")
    return parser.parse_args()


def sort_main(variants, name):
    args = _parse(f"{name}: type space-separated integers, get them sorted")
    arr = list(map(int, input().split()))
    print(variants[args.variant](arr))


def search_main(variants, name, sorted_input=False):
    args = _parse(f"{name}: type space-separated integers, then the key")
    arr = list(map(int, input().split()))
    if sorted_input:
        arr.sort()
    key = int(input())
    index = variants[args.variant](arr, key)
    print(index if index != -1 else "NOT FOUND")
