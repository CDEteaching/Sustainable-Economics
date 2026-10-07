"""
CDE-styled line chart template — produces a static PNG (300dpi) and an
animated GIF (line draws left-to-right, then holds) for PowerPoint.

HOW TO USE: copy this file next to the target chart's output folder, edit the
DATA block below with the real data and labels, then run:
    python line_chart.py
Two files land next to this script: <OUT_NAME>.png and <OUT_NAME>.gif
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cde_style import (
    apply_theme, style_axes, save_png, save_gif, add_footer,
    CATEGORICAL, INK_PRIMARY, INK_SECONDARY, BRAND_NAVY, FIGSIZE,
)

# ── DATA — edit this block ──────────────────────────────────────────────────
TITLE = "Gross domestic product per capita in Switzerland"
SUBTITLE = "In US dollars at 2011 prices, 1851–2018"
X_LABELS = ["1851", "1860", "1870", "1880", "1890", "1900", "1910", "1920",
            "1930", "1940", "1950", "1960", "1970", "1980", "1990", "2000",
            "2010", "2018"]
SERIES = {
    "GDP per capita": [2444, 2934, 2954, 3869, 5309, 6612, 8048, 7364,
                      9969, 9802, 11541, 16358, 23479, 27406, 34250, 43251,
                      57219, 61373],
}
Y_LABEL = "USD (2011 prices)"
VALUE_FMT = "{:,.0f}"
SOURCE_NOTE = "Source: Maddison Project Database, Release 2020 (Bolt & van Zanden, 2020), rug.nl/ggdc/historicaldevelopment/maddison"
LANG = "en"  # "en" or "de" — language of the fixed AI-disclosure footer line, match chart language
TICK_EVERY = 1  # show every Nth x label (e.g. 5 for an annual series spanning decades)
OUT_NAME = "figure0-gdp-per-capita-switzerland"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
# ─────────────────────────────────────────────────────────────────────────

apply_theme()
n = len(X_LABELS)
x = np.arange(n)
names = list(SERIES.keys())
colors = {name: CATEGORICAL[i % len(CATEGORICAL)] for i, name in enumerate(names)}

# always keep the last point labeled, even if it doesn't fall on the stride
tick_idx = sorted(set(range(0, n, TICK_EVERY)) | {n - 1})

# End-label gap and the xlim room reserved for it both scale with the number
# of points — a fixed 0.08 data-unit gap is a comfortable ~2% of the axis on
# a 5-point chart but nearly invisible on a 30+ point annual series.
LABEL_DX = max(n * 0.02, 0.08)


def build_axes(ax):
    style_axes(ax, y_grid=True)
    ax.set_xticks(x[tick_idx])
    ax.set_xticklabels([X_LABELS[i] for i in tick_idx])
    ax.set_ylabel(Y_LABEL)
    ymax = max(max(v) for v in SERIES.values())
    ax.set_ylim(0, ymax * 1.18)
    ax.set_xlim(-0.3, n - 1 + (0.3 if n == 1 else max(1.3, LABEL_DX * 12)))  # room for end labels


def add_titles(fig):
    fig.text(0.02, 0.97, TITLE, fontsize=17, fontweight="bold", color=BRAND_NAVY, ha="left", va="top")
    fig.text(0.02, 0.91, SUBTITLE, fontsize=12, color=INK_SECONDARY, ha="left", va="top")
    add_footer(fig, SOURCE_NOTE)


def reveal_point(xs, ys, frac):
    """Interpolated (x, y) arrays showing the line up to `frac` of its length."""
    pos = frac * (len(xs) - 1)
    idx = int(np.floor(pos))
    rem = pos - idx
    if idx >= len(xs) - 1:
        return xs, ys
    xr = np.append(xs[: idx + 1], xs[idx] + rem * (xs[idx + 1] - xs[idx]))
    yr = np.append(ys[: idx + 1], ys[idx] + rem * (ys[idx + 1] - ys[idx]))
    return xr, yr


# ── static PNG ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=FIGSIZE)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.98)
build_axes(ax)
add_titles(fig)

for name in names:
    y = SERIES[name]
    c = colors[name]
    ax.plot(x, y, color=c, linewidth=2.5, marker="o", markersize=6,
            markerfacecolor="#FFFFFF", markeredgecolor=c,
            markeredgewidth=2, zorder=3, label=name)
    ax.text(x[-1] + LABEL_DX, y[-1], f"{name}  {VALUE_FMT.format(y[-1])}",
            color=c, fontsize=11, fontweight="bold", va="center", ha="left")

if len(names) >= 2:
    ax.legend(loc="upper left", frameon=False, fontsize=10, labelcolor=INK_SECONDARY,
               handlelength=1.2, bbox_to_anchor=(0.0, 1.0))

save_png(fig, os.path.join(OUT_DIR, f"{OUT_NAME}.png"))
plt.close(fig)

# ── animated GIF ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=FIGSIZE)
fig.subplots_adjust(top=0.82, bottom=0.12, left=0.08, right=0.98)
build_axes(ax)
add_titles(fig)

lines, markers, labels = {}, {}, {}
for name in names:
    c = colors[name]
    (line,) = ax.plot([], [], color=c, linewidth=2.5, zorder=3)
    (marker,) = ax.plot([], [], marker="o", markersize=7, markerfacecolor="#FFFFFF",
                         markeredgecolor=c, markeredgewidth=2, zorder=4)
    label = ax.text(0, 0, "", color=c, fontsize=11, fontweight="bold", va="center", ha="left", alpha=0)
    lines[name], markers[name], labels[name] = line, marker, label

DRAW_FRAMES, LABEL_FRAMES = 40, 12
TOTAL = DRAW_FRAMES + LABEL_FRAMES


def update(i):
    if i < DRAW_FRAMES:
        frac = i / (DRAW_FRAMES - 1)
        for name in names:
            y = np.array(SERIES[name], dtype=float)
            xr, yr = reveal_point(x.astype(float), y, frac)
            lines[name].set_data(xr, yr)
            markers[name].set_data([xr[-1]], [yr[-1]])
    else:
        j = i - DRAW_FRAMES
        alpha = min(1.0, (j + 1) / LABEL_FRAMES)
        for name in names:
            y = SERIES[name]
            labels[name].set_position((x[-1] + LABEL_DX, y[-1]))
            labels[name].set_text(f"{name}  {VALUE_FMT.format(y[-1])}")
            labels[name].set_alpha(alpha)


if len(names) >= 2:
    ax.legend(loc="upper left", frameon=False, fontsize=10, labelcolor=INK_SECONDARY,
              handlelength=1.2, bbox_to_anchor=(0.0, 1.0), handles=[
                  plt.Line2D([0], [0], color=colors[n], linewidth=2.5) for n in names], labels=names)

save_gif(fig, update, TOTAL, os.path.join(OUT_DIR, f"{OUT_NAME}.gif"))
