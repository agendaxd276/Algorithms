"""Regenerate docs/*.md and docs/images/*.svg from the REAL algorithm code.

    python -m tools.build_docs

Everything numeric (comparisons, memory, stack depth, timings) is measured by running the
algorithms in algorithms/ - nothing is copied from a table.  Hand-written explanations live in
tools/content.py.
"""
import inspect
import os
import platform
import random

from algorithms.registry import SEARCHES, SORTS
from tools import svgkit
from tools.cases import CASES, evaluate_search, evaluate_sort, random_perm
from tools.content import ALGOS, ORDER, REFERENCES
from tools.instrument import max_depth, peak_extra_kib, wall_ms
from tools.tracers import TRACERS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS, IMG = os.path.join(ROOT, "docs"), os.path.join(ROOT, "docs", "images")
TIERS = ("normal", "optimal", "optimized")
N_SORT, N_SEARCH, N_SHAPE = 64, 63, 32
GROWTH = [8, 16, 32, 64, 128, 256, 512]
# which tier's best/avg/worst INPUTS are drawn in the "visual cases" picture
CASE_TIER = {"bubble_sort": "optimal", "selection_sort": "optimal", "insertion_sort": "optimal",
             "merge_sort": "normal", "quick_sort": "normal", "heap_sort": "normal",
             "linear_search": "normal", "binary_search": "normal"}


def variants(name):
    return (SORTS.get(name) or SEARCHES[name])


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def num(v):
    return f"{v:,.0f}" if v >= 100 or abs(v - round(v)) < 0.05 else f"{v:,.1f}"


# ------------------------------------------------------------------ measurement
def measure(name):
    kind = ALGOS[name]["kind"]
    fns = variants(name)
    out = {"cases": {}, "growth": {}, "space": {}, "time": {}}
    n = N_SORT if kind == "sort" else N_SEARCH
    for tier, fn in fns.items():
        if kind == "sort":
            out["cases"][tier] = evaluate_sort(fn, n)
            out["growth"][tier] = [evaluate_sort(fn, g) for g in GROWTH]
        else:
            out["cases"][tier] = evaluate_search(name, fn, n)
            out["growth"][tier] = [evaluate_search(name, fn, g) for g in GROWTH]
    if kind == "sort":
        rnd = random_perm(3000, 1)
        for tier, fn in fns.items():
            out["space"][tier] = (peak_extra_kib(fn, rnd), max_depth(fn, list(range(800))))
            data = random_perm(2000, 3)
            out["time"][tier] = wall_ms(fn, lambda: data[:])
    else:
        big = list(range(0, 200000, 2))
        base = big[:] if name == "binary_search" else random.Random(5).sample(big, len(big))
        reps = 2000 if name == "binary_search" else 10
        keys = [random.Random(9).randrange(len(big)) * 2 + 1 for _ in range(reps)]   # absent keys
        for tier, fn in fns.items():
            def run(_data, fn=fn):
                for k in keys:
                    fn(base, k)
            out["time"][tier] = wall_ms(run, lambda: None) / reps * 1000   # microseconds per search
            out["space"][tier] = (0.0, max_depth(lambda a: fn(base, 1), []))
    return out


def comp(case_tuple, kind):
    return case_tuple[2] if kind == "sort" else case_tuple[3]


# ------------------------------------------------------------------ visuals
def make_steps_svg(name):
    a = ALGOS[name]
    frames = [f for f in TRACERS[name]()[0] if f["milestone"]]
    if a["kind"] == "sort":
        legend = [("bar", "untouched"), ("cmp", "comparing / split"), ("act", "swapped / moved / pivot"),
                  ("done", "final position")]
        sub = "Example input [5, 2, 4, 6, 1, 3] - milestone steps (full trace in the table below)"
    else:
        legend = [("bar", "still possible"), ("dim", "ruled out"), ("cmp", "probe"), ("done", "found")]
        sub = "Milestone steps; lo / mid / hi mark the search window"
    write(os.path.join(IMG, f"{name}_steps.svg"),
          svgkit.steps_strip(f"{a['title']} - step by step", sub, frames, legend,
                             cols=3 if len(frames) > 4 else 2))


def make_cases_svg(name, m):
    a, kind = ALGOS[name], ALGOS[name]["kind"]
    tier = CASE_TIER[name]
    shapes = []
    if kind == "sort":
        fn = variants(name)[tier]
        res = evaluate_sort(fn, N_SHAPE)
        for case in CASES:
            shape, vals, c = res[case]
            shapes.append((f"{case.title()} case", vals, f"{shape} - {num(c)} comparisons (n={N_SHAPE})", {}))
    else:
        fn = variants(name)[tier]
        res = evaluate_search(name, fn, N_SHAPE - 1)
        for case in CASES:
            desc, vals, key, c = res[case]
            marks = {vals.index(key): "act"} if key in vals else {}
            shapes.append((f"{case.title()} case", vals, f"{desc} - {num(c)} comparisons (n={N_SHAPE - 1})",
                           marks))
    title = f"{a['title']} - the three cases ({tier} tier)"
    write(os.path.join(IMG, f"{name}_cases.svg"),
          svgkit.case_shapes(title, "Input that triggers each case (found by measurement, not assumed)", shapes))


def make_compare_svg(name, m):
    kind = ALGOS[name]["kind"]
    n = N_SORT if kind == "sort" else N_SEARCH
    series = {t: [comp(m["cases"][t][c], kind) for c in CASES] for t in TIERS}
    write(os.path.join(IMG, f"{name}_comparisons.svg"),
          svgkit.grouped_bars(f"{ALGOS[name]['title']} - comparisons by case and tier",
                              f"Measured on the real code, n = {n}. Lower is better.",
                              [c.title() for c in CASES], series))


def make_growth_svg(name, m):
    kind = ALGOS[name]["kind"]
    series = {t: [max(1, comp(r["worst"], kind)) for r in m["growth"][t]] for t in TIERS}
    write(os.path.join(IMG, f"{name}_growth.svg"),
          svgkit.line_chart(f"{ALGOS[name]['title']} - worst-case comparisons as n grows",
                            "A straight line on log-log axes: steeper = faster growth. Measured, n = 8 … 512.",
                            GROWTH, series, "comparisons"))


def make_overview(measured):
    for case, label in (("average", "average"), ("worst", "worst")):
        series = {ALGOS[n]["title"].replace(" Sort", ""):
                  [max(1, comp(r[case], "sort")) for r in measured[n]["growth"]["optimal"]]
                  for n in ORDER if ALGOS[n]["kind"] == "sort"}
        write(os.path.join(IMG, f"overview_sorts_{label}.svg"),
              svgkit.line_chart(f"All sorts, optimal tier - {label}-case comparisons",
                                "Measured on the real code. Curves that are exactly equal share one label (e.g. n(n-1)/2).",
                                GROWTH, series, "comparisons"))
    series = {ALGOS[n]["title"].replace(" Search", "") + f" ({t})": [max(1, comp(r["worst"], "search")) for r in measured[n]["growth"][t]]
              for n in ("linear_search", "binary_search") for t in ("normal", "optimized")}
    write(os.path.join(IMG, "overview_searches_worst.svg"),
          svgkit.line_chart("Searches - worst-case comparisons", "Linear is O(n); binary is O(log n); "
                            "interpolation (optimized binary) collapses on skewed data.",
                            GROWTH, series, "comparisons"))


# ------------------------------------------------------------------ markdown
def md_complexity_table(theory):
    rows = ["| Tier | Best | Average | Worst | Space |", "|---|---|---|---|---|"]
    for t in TIERS:
        b, a, w, s = theory[t]
        rows.append(f"| **{t.title()}** | {b} | {a} | {w} | {s} |")
    return "\n".join(rows)


def md_measured(name, m):
    kind = ALGOS[name]["kind"]
    n = N_SORT if kind == "sort" else N_SEARCH
    rows = [f"| Tier | Best | Average | Worst |", "|---|---|---|---|"]
    for t in TIERS:
        cells = []
        for c in CASES:
            tup = m["cases"][t][c]
            cells.append(f"{num(comp(tup, kind))} <br><sub>{tup[0] if kind == 'sort' else tup[0]}</sub>")
        rows.append(f"| **{t.title()}** | " + " | ".join(cells) + " |")
    out = [f"**Comparisons, n = {n}** (each cell: count and the input that produced it)", "", *rows, ""]
    if kind == "sort":
        out += ["| Tier | Extra memory (KiB, n=3000 random) | Max call-stack depth (n=800 sorted) | "
                "Time (ms, n=2000 random) |", "|---|---|---|---|"]
        for t in TIERS:
            kib, depth = m["space"][t]
            out.append(f"| **{t.title()}** | {kib:,.1f} | {depth} | {m['time'][t]:,.1f} |")
    else:
        out += ["| Tier | Time per search (µs, n=100,000, key absent) |", "|---|---|"]
        for t in TIERS:
            out.append(f"| **{t.title()}** | {m['time'][t]:,.1f} |")
    out += ["", f"<sub>Timings are indicative only (CPython {platform.python_version()}, one machine); "
            f"comparison counts, memory and stack depth are deterministic.</sub>"]
    return "\n".join(out)


def md_trace(name):
    frames, final = TRACERS[name]()
    rows = ["| # | What happens | Array after the step |", "|---|---|---|"]
    for i, f in enumerate(frames, 1):
        rows.append(f"| {i} | {f['caption']} | `{f['arr']}` |")
    return "\n".join(rows)


def md_tier_section(name, tier):
    a = ALGOS[name]
    fn = variants(name)[tier]
    idea, why = a["tiers"][tier]
    b, av, w, sp = a["theory"][tier]
    src = inspect.getsource(fn).rstrip()
    return (f"### {tier.title()} - `{fn.__name__}`\n\n**Idea:** {idea}\n\n{why}\n\n"
            f"| Best | Average | Worst | Space |\n|---|---|---|---|\n| {b} | {av} | {w} | {sp} |\n\n"
            f"```python\n{src}\n```\n")


def faq_block(name, m):
    a, kind = ALGOS[name], ALGOS[name]["kind"]
    qt = CASE_TIER[name]                        # the tier whose theory + measurements headline the page
    t = a["theory"][qt]
    others = [x for x in TIERS if x != qt and a["theory"][x] != t]
    n = N_SORT if kind == "sort" else N_SEARCH
    lines = [
        f"**What is the time complexity of {a['title'].lower()}?**  ",
        f"Best case **{t[0]}**, average case **{t[1]}**, worst case **{t[2]}** ({qt} tier"
        + (f"; the {' and '.join(others)} tier{'s' if len(others) > 1 else ''} differ - see the table below)."
           if others else "; the same for every tier)."),
        "",
        f"**What is the space complexity of {a['title'].lower()}?**  ",
        f"**{t[3]}** extra space ({qt} tier)"
        + (f"; other tiers: " + ", ".join(f"{x} {a['theory'][x][3]}" for x in others
                                          if a["theory"][x][3] != t[3]) + "." if any(
            a["theory"][x][3] != t[3] for x in others) else "."),
        "",
        "**Best case / average case / worst case - what input causes each?**  ",
    ]
    for c in CASES:
        tup = m["cases"][qt][c]
        lines.append(f"- **{c.title()}:** {tup[0]} → {num(comp(tup, kind))} comparisons at n = {n} ({qt} tier)")
    lines += ["", "**Is it stable / in place / adaptive?**  ",
              f"Stable: {a['props']['stable']} · In place: {a['props']['in_place']} · "
              f"Adaptive: {a['props']['adaptive']}", "",
              "**Normal vs optimal vs optimized solution?**  ",
              "See [section 6](#6-normal-vs-optimal-vs-optimized-solutions).", ""]
    for q, ans in a["faq"]:
        lines += [f"**{q}**  ", ans, ""]
    return "\n".join(lines)


def build_algo_doc(name, m):
    a, kind = ALGOS[name], ALGOS[name]["kind"]
    refs = REFERENCES["sorting" if kind == "sort" else "searching"]
    tier_code = "\n".join(md_tier_section(name, t) for t in TIERS)
    has_shot = os.path.exists(os.path.join(DOCS, "screenshots", f"{name}.png"))
    shot = f" ·\nOriginal hand-drawn notes: [`screenshots/{name}.png`](screenshots/{name}.png)" if has_shot else ""
    doc = f"""# {a['title']}

> {a['one_liner']}

![{a['title']} step by step](images/{name}_steps.svg)

[← All algorithms](../README.md) · Source: [`algorithms/{a['module']}`](../algorithms/{a['module']}){shot}

## Quick answers

{faq_block(name, m)}

### Complexity at a glance

{md_complexity_table(a['theory'])}

## 1. How it works - step by step

```mermaid
{a['flow']}
```

{chr(10).join(f"{i}. {s}" for i, s in enumerate(a['steps'], 1))}

## 2. Worked example

{"Sorting" if kind == "sort" else "Searching"} the example below, one step at a time (every row is a snapshot taken by
[`tools/tracers.py`](../tools/tracers.py), which is tested to end in the right answer).

{md_trace(name)}

## 3. Visual cases - best, average, worst

![Best, average and worst inputs](images/{name}_cases.svg)

The picture shows the **input** that triggers each case. Bars are values (sorting) or sorted/unsorted data
with the searched key highlighted (searching).

{md_measured(name, m)}

![Comparisons by case and tier](images/{name}_comparisons.svg)

## 4. Time complexity - step by step

{chr(10).join(f"{i}. {s}" for i, s in enumerate(a['time_steps'], 1))}

![Worst-case growth](images/{name}_growth.svg)

## 5. Space complexity - step by step

{chr(10).join(f"{i}. {s}" for i, s in enumerate(a['space_steps'], 1))}

## 6. Normal vs optimal vs optimized solutions

| | Normal | Optimal | Optimized |
|---|---|---|---|
| **Idea** | {a['tiers']['normal'][0]} | {a['tiers']['optimal'][0]} | {a['tiers']['optimized'][0]} |
| **Why it matters** | {a['tiers']['normal'][1]} | {a['tiers']['optimal'][1]} | {a['tiers']['optimized'][1]} |

*Normal* = the textbook version. *Optimal* = the best Big-O this algorithm family can reach.
*Optimized* = engineering tweaks you would ship (constant factors, memory, robustness).

{tier_code}
## 7. When to use it

{a['when']}

## Further reading

""" + "\n".join(f"- [{t}]({u})" for t, u in refs) + "\n"
    write(os.path.join(DOCS, f"{name}.md"), doc)


DECISION_FLOW = """```mermaid
flowchart TD
    S["I need to..."] --> Q1{"find an item or sort?"}
    Q1 -- find --> Q2{"is the data sorted?"}
    Q2 -- no --> L["Linear search - O(n)"]
    Q2 -- yes --> Q3{"searching many times?"}
    Q3 -- yes --> B["Binary search - O(log n)"]
    Q3 -- no --> L
    Q1 -- sort --> Q4{"just use the library?"}
    Q4 -- yes --> T["sorted() / list.sort() - Timsort"]
    Q4 -- "no, I'm learning or constrained" --> Q5{"small or nearly sorted?"}
    Q5 -- yes --> I["Insertion sort"]
    Q5 -- no --> Q6{"need stable or guaranteed speed?"}
    Q6 -- "stable" --> M["Merge sort"]
    Q6 -- "guaranteed + O(1) memory" --> H["Heap sort"]
    Q6 -- "fastest on average" --> QS["Quick sort - optimized (introsort)"]
```"""


def build_complexity_doc(measured):
    sort_rows = ["| Algorithm | Best | Average | Worst | Space | Stable | Avg comparisons @ n=64 (optimal tier) |",
                 "|---|---|---|---|---|---|---|"]
    for n in ORDER:
        a = ALGOS[n]
        if a["kind"] != "sort":
            continue
        b, av, w, sp = a["theory"]["optimal"]
        c = comp(measured[n]["cases"]["optimal"]["average"], "sort")
        sort_rows.append(f"| [{a['title']}]({n}.md) | {b} | {av} | {w} | {sp} | {a['props']['stable']} | {num(c)} |")
    search_rows = ["| Algorithm | Best | Average | Worst | Space | Needs sorted input |", "|---|---|---|---|---|---|"]
    for n in ("linear_search", "binary_search"):
        a = ALGOS[n]
        b, av, w, sp = a["theory"]["normal"]
        search_rows.append(f"| [{a['title']}]({n}.md) | {b} | {av} | {w} | {sp} | "
                           f"{'No' if n == 'linear_search' else 'Yes'} |")
    doc = f"""# Complexity cheat-sheet

All numbers on the algorithm pages are **measured** by running the code in `algorithms/`
(`python -m tools.build_docs` regenerates them). This page is the one-screen summary.

## Searching

{chr(10).join(search_rows)}

![Search growth](images/overview_searches_worst.svg)

## Sorting

{chr(10).join(sort_rows)}

![Average-case growth](images/overview_sorts_average.svg)

![Worst-case growth](images/overview_sorts_worst.svg)

## Is O(n log n) the limit? (the "optimal" question)

Any sort that works **only by comparing items** needs at least log₂(n!) ≈ n·log₂ n comparisons in the worst
case: there are n! possible orders, and each comparison has two outcomes, so you need ≥ log₂(n!) comparisons to
tell them apart. So **O(n log n) is the optimal complexity class** for comparison sorting, and merge sort, heap
sort and (introsort-style) quick sort all reach it. Bubble, selection and insertion sort do not - their value is
simplicity, tiny constant factors on small inputs, or adaptivity.
Sorts that *don't* compare (counting / radix / bucket sort) can reach O(n + k) when keys are small integers.

Python's built-in `sorted()` / `list.sort()` is **Timsort**: a stable merge-sort/insertion-sort hybrid that is
O(n) on already-sorted data and O(n log n) otherwise ([Timsort on Wikipedia](https://en.wikipedia.org/wiki/Timsort)).
The optimized tiers here borrow its ideas (insertion-sort cutoff, skipping merges of ordered runs).

## Which algorithm should I use?

{DECISION_FLOW}

## The three tiers, in one table

| Algorithm | Normal (textbook) | Optimal (best Big-O for the family) | Optimized (what you'd ship) |
|---|---|---|---|
""" + "\n".join(
        f"| [{ALGOS[n]['title']}]({n}.md) | {ALGOS[n]['tiers']['normal'][0]} | {ALGOS[n]['tiers']['optimal'][0]} "
        f"| {ALGOS[n]['tiers']['optimized'][0]} |" for n in ORDER) + "\n\n## References\n\n" + "\n".join(
        f"- [{t}]({u})" for t, u in REFERENCES["sorting"] + REFERENCES["searching"]) + "\n"
    write(os.path.join(DOCS, "COMPLEXITY.md"), doc)


def main():
    measured = {}
    for name in ORDER:
        print("measuring", name, flush=True)
        measured[name] = measure(name)
        make_steps_svg(name)
        make_cases_svg(name, measured[name])
        make_compare_svg(name, measured[name])
        make_growth_svg(name, measured[name])
        build_algo_doc(name, measured[name])
    make_overview(measured)
    build_complexity_doc(measured)
    print("done")


if __name__ == "__main__":
    main()
