"""Dependency-free SVG helpers (light + dark aware via CSS custom properties in each file).

Palette = the dataviz reference palette, categorical slots 1-3 (validated in both modes):
blue #2a78d6 / orange #eb6834 / aqua #1baf7a (dark: #3987e5 / #d95926 / #199e70).
Every bar carries its numeric label, so colour is never the only channel.
"""
from html import escape

STYLE = """<style>
svg{--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--grid:#e3e2de;--bar:#c4cad3;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4;--s6:#008300}
@media (prefers-color-scheme:dark){svg{--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--grid:#363633;
--bar:#4b5058;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300}}
text{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;fill:var(--ink)}
.t{font-size:15px;font-weight:600}.sub{font-size:11px;fill:var(--ink2)}.lab{font-size:10.5px;fill:var(--ink2)}
.val{font-size:10.5px;font-weight:600}.cap{font-size:11px}.idx{font-size:9px;fill:var(--ink2)}
.grid{stroke:var(--grid);stroke-width:1}.axis{stroke:var(--ink2);stroke-width:1}
.bar{fill:var(--bar)}.cmp{fill:var(--s1)}.act{fill:var(--s2)}.done{fill:var(--s3)}.dim{fill:var(--bar);opacity:.45}
.s1{fill:var(--s1)}.s2{fill:var(--s2)}.s3{fill:var(--s3)}.s4{fill:var(--s4)}.s5{fill:var(--s5)}.s6{fill:var(--s6)}
.l1{stroke:var(--s1)}.l2{stroke:var(--s2)}.l3{stroke:var(--s3)}.l4{stroke:var(--s4)}.l5{stroke:var(--s5)}.l6{stroke:var(--s6)}
.line{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.frame{fill:none;stroke:var(--grid);stroke-width:1}
</style>"""


def svg_doc(w, h, body, title, desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>'
            f'<desc>{escape(desc or title)}</desc>\n{STYLE}\n'
            f'<rect width="{w}" height="{h}" rx="10" fill="var(--surface)"/>\n{body}\n</svg>\n')


def text(x, y, s, cls="lab", anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(str(s))}</text>'


def wrap(s, width):
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur] if cur else lines


def bars(values, x, y, w, h, marks=None, labels=None, vmax=None):
    """One mini bar chart: value labels on top, optional index/pointer labels below."""
    marks, labels = marks or {}, labels or {}
    n = len(values)
    vmax = vmax or max(max(values), 1)
    slot = w / n
    bw = slot * 0.72
    out = []
    for i, v in enumerate(values):
        bh = max(2.0, (h - 16) * v / vmax)
        bx = x + i * slot + (slot - bw) / 2
        out.append(f'<rect x="{bx:.1f}" y="{y + h - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="2" '
                   f'class="{marks.get(i, "bar")}"/>')
        out.append(text(bx + bw / 2, y + h - bh - 3, v, "val", "middle"))
        out.append(text(bx + bw / 2, y + h + 11, labels.get(i, i), "idx", "middle"))
    out.append(f'<line x1="{x}" x2="{x + w}" y1="{y + h}" y2="{y + h}" class="axis"/>')
    return "\n".join(out)


def legend(items, x, y):
    out, cx = [], x
    for cls, label in items:
        out.append(f'<rect x="{cx}" y="{y - 9}" width="11" height="11" rx="2" class="{cls}"/>')
        out.append(text(cx + 16, y, label, "lab"))
        cx += 24 + 6.2 * len(label)
    return "\n".join(out)


def steps_strip(title, subtitle, frames, legend_items, cols=3, fw=250, fh=170):
    """Grid of bar-chart frames, each with a numbered caption.  frames: dicts(arr, marks, labels, caption)."""
    rows = (len(frames) + cols - 1) // cols
    W, H = cols * fw + 20, 78 + rows * fh + 8
    body = [text(20, 28, title, "t"), text(20, 46, subtitle, "sub"), legend(legend_items, 20, 66)]
    vmax = max(max(f["arr"]) for f in frames)
    for k, f in enumerate(frames):
        cx, cy = 10 + (k % cols) * fw, 78 + (k // cols) * fh
        body.append(f'<rect x="{cx + 4}" y="{cy}" width="{fw - 8}" height="{fh - 6}" rx="8" class="frame"/>')
        body.append(text(cx + 14, cy + 16, f"Step {k + 1}", "val"))
        body.append(bars(f["arr"], cx + 16, cy + 24, fw - 32, 78, f.get("marks"), f.get("labels"), vmax))
        for li, line in enumerate(wrap(f["caption"], 38)[:3]):
            body.append(text(cx + 14, cy + 128 + li * 13, line, "cap"))
    return svg_doc(W, H, "\n".join(body), title, subtitle)


def grouped_bars(title, subtitle, groups, series, note=""):
    """groups: list of labels (x); series: {name: [values per group]} - names get slots 1..3."""
    W, H, L, R, T, B = 640, 330, 56, 20, 84, 44
    names = list(series)
    vmax = max(max(v) for v in series.values()) or 1
    step = nice_step(vmax / 4)
    top = step * 4 if step * 4 >= vmax else step * 5
    nticks = round(top / step)
    pw, ph = W - L - R, H - T - B
    out = [text(20, 26, title, "t"), text(20, 44, subtitle, "sub"),
           legend([(f"s{i + 1}", n) for i, n in enumerate(names)], 20, 66)]
    for tick in range(0, nticks + 1):
        yv = step * tick
        yy = T + ph - ph * tick / nticks
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{yy:.1f}" y2="{yy:.1f}" class="grid"/>')
        out.append(text(L - 6, yy + 4, fmt(yv), "lab", "end"))
    gw = pw / len(groups)
    bw = gw * 0.78 / len(names)
    for g, glabel in enumerate(groups):
        gx = L + g * gw + gw * 0.11
        for s, name in enumerate(names):
            v = series[name][g]
            bh = max(1.5, ph * v / top)
            bx = gx + s * bw
            out.append(f'<rect x="{bx + 1:.1f}" y="{T + ph - bh:.1f}" width="{bw - 2:.1f}" height="{bh:.1f}" '
                       f'rx="3" class="s{s + 1}"/>')
            out.append(text(bx + bw / 2, T + ph - bh - 4, full(v), "val", "middle"))
        out.append(text(L + g * gw + gw / 2, H - B + 18, glabel, "cap", "middle"))
    out.append(f'<line x1="{L}" x2="{W - R}" y1="{T + ph}" y2="{T + ph}" class="axis"/>')
    if note:
        out.append(text(20, H - 8, note, "sub"))
    return svg_doc(W, H, "\n".join(out), title, subtitle)


def line_chart(title, subtitle, xs, series, ylabel, direct_labels=True):
    """Log-log line chart: series {name: [y per x]}; slots 1..6 in fixed order."""
    import math
    W, H, L, R, T, B = 720, 370, 62, 215, 100, 46
    names = list(series)
    ymin = max(1, min(min(v) for v in series.values()))
    ymax = max(max(v) for v in series.values())
    lo, hi = math.floor(math.log10(ymin)), math.ceil(math.log10(ymax))
    pw, ph = W - L - R, H - T - B
    x0, x1 = math.log2(xs[0]), math.log2(xs[-1])
    px = lambda x: L + pw * (math.log2(x) - x0) / (x1 - x0)
    py = lambda y: T + ph - ph * (math.log10(max(y, 1)) - lo) / (hi - lo)
    out = [text(20, 26, title, "t"), text(20, 44, subtitle, "sub"),
           legend([(f"s{i + 1}", n) for i, n in enumerate(names)], 20, 66)]
    for e in range(lo, hi + 1):
        yy = py(10 ** e)
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{yy:.1f}" y2="{yy:.1f}" class="grid"/>')
        out.append(text(L - 6, yy + 4, fmt(10 ** e), "lab", "end"))
    for x in xs:
        out.append(text(px(x), H - B + 16, x, "lab", "middle"))
    out.append(text((L + W - R) / 2, H - 8, "input size n (log scale)", "sub", "middle"))
    out.append(text(14, T - 12, ylabel + " (log scale)", "sub"))
    groups = {}                                 # identical curves share one end label
    for i, name in enumerate(names):
        pts = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in zip(xs, series[name]))
        out.append(f'<polyline points="{pts}" class="line l{i + 1}"/>')
        for x, y in zip(xs, series[name]):
            out.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="3" class="s{i + 1}" '
                       f'stroke="var(--surface)" stroke-width="2"/>')
        groups.setdefault(tuple(series[name]), []).append((i, name))
    if direct_labels:                           # end-of-line labels, nudged apart
        ends = sorted((py(vals[-1]), members) for vals, members in groups.items())
        last = -99
        for yy, members in ends:
            yy = max(yy, last + 14)
            label = " = ".join(n for _, n in members)
            out.append(f'<rect x="{W - R + 6}" y="{yy - 5:.1f}" width="9" height="9" rx="2" '
                       f'class="s{members[0][0] + 1}"/>')
            out.append(text(W - R + 19, yy + 4, label, "lab"))
            last = yy
    out.append(f'<line x1="{L}" x2="{W - R}" y1="{T + ph}" y2="{T + ph}" class="axis"/>')
    return svg_doc(W, H, "\n".join(out), title, subtitle)


def case_shapes(title, subtitle, shapes):
    """shapes: [(heading, values, caption, marks)] drawn side by side (best / average / worst inputs)."""
    n = len(shapes)
    cw = 250
    W, H = n * cw + 20, 190
    out = [text(20, 26, title, "t"), text(20, 44, subtitle, "sub")]
    for k, (head, vals, cap, marks) in enumerate(shapes):
        cx = 10 + k * cw
        out.append(f'<rect x="{cx + 4}" y="58" width="{cw - 8}" height="{H - 66}" rx="8" class="frame"/>')
        out.append(text(cx + 14, 76, head, "val"))
        out.append(bars_thin(vals, cx + 16, 84, cw - 32, 60, marks))
        for li, line in enumerate(wrap(cap, 38)[:2]):
            out.append(text(cx + 14, 168 + li * 12 - 2, line, "cap"))
    return svg_doc(W, H, "\n".join(out), title, subtitle)


def bars_thin(values, x, y, w, h, marks=None):
    """Compact bars (no per-bar labels) for showing the SHAPE of an input of ~32 items."""
    marks = marks or {}
    n = len(values)
    vmax = max(max(values), 1)
    slot = w / n
    out = []
    for i, v in enumerate(values):
        bh = max(2.0, h * v / vmax)
        out.append(f'<rect x="{x + i * slot + .5:.1f}" y="{y + h - bh:.1f}" width="{max(slot - 1, 1):.1f}" '
                   f'height="{bh:.1f}" class="{marks.get(i, "bar")}"/>')
    out.append(f'<line x1="{x}" x2="{x + w}" y1="{y + h}" y2="{y + h}" class="axis"/>')
    return "\n".join(out)


def nice_step(v):
    import math
    if v <= 0:
        return 1
    e = 10 ** math.floor(math.log10(v))
    for m in (1, 2, 5, 10):
        if m * e >= v:
            return m * e


def full(v):
    """Exact label: 2,016 or 1,899.4 -> 1,899 (keeps one decimal only for small values)."""
    return f"{v:,.0f}" if v >= 100 or abs(v - round(v)) < 0.05 else f"{v:,.1f}"


def fmt(v):
    if v >= 1_000_000:
        return f"{v / 1_000_000:.0f}M"
    if v >= 1000:
        return f"{v / 1000:.1f}k".replace(".0k", "k")
    return f"{v:.0f}" if abs(v - round(v)) < 0.05 else f"{v:.1f}"
