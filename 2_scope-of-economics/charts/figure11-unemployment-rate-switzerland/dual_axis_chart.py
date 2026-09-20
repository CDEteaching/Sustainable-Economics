"""
CDE-styled dual-axis line chart — for two series in different units that
need independent y-axes (e.g. a rate in % and an absolute headcount).

Not a shared cde-charts template (line_chart.py is single-axis, up to 4
series in the SAME unit) — this is a one-off, bespoke script for this
specific chart, built from the same cde_style building blocks so it stays
visually consistent with the rest of the book.

Unlike line_chart.py this uses a REAL numeric year x-axis (not an evenly
spaced index) and plots every available year (no thinning/sampling) — the
underlying data has sharp single-year spikes (e.g. 1922, 1936, 1997) that a
5-year sampling grid can flatten out or miss entirely depending on where the
grid points happen to fall. Full annual resolution + a true calendar axis
avoids both problems, and no per-point markers keeps a ~100-point line
readable (markers stay only at each series' final point).

HOW TO USE: edit the DATA block below (or the CSV paths it reads from),
then run: python dual_axis_chart.py
Two files land next to this script: <OUT_NAME>.png and <OUT_NAME>.gif
"""

import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cde_style import (
    apply_theme, save_png, save_gif, add_footer,
    CATEGORICAL, INK_PRIMARY, INK_SECONDARY, BRAND_NAVY, GRIDLINE, SURFACE, FIGSIZE,
)

# ── DATA — edit this block ──────────────────────────────────────────────────
TITLE = "Arbeitslosigkeit in der Schweiz"
SUBTITLE = "Registrierte Arbeitslose (Anzahl) und Arbeitslosenquote (%), 1920–2025"

HSSO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hsso_f18a_full_1913-1995.csv")
SECO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seco_amarbma_full_1984-2025.csv")
YEAR_START, YEAR_HSSO_END, YEAR_SECO_START, YEAR_END = 1920, 1995, 1996, 2025

SERIES_LEFT_NAME = "Arbeitslosenquote"
LEFT_Y_LABEL = "Arbeitslosenquote (%)"
LEFT_VALUE_FMT = "{:.2f}%"

SERIES_RIGHT_NAME = "Arbeitslose"
RIGHT_Y_LABEL = "Registrierte Arbeitslose (Anzahl)"
RIGHT_VALUE_FMT = "{:,.0f}"

X_TICKS = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025]
SOURCE_NOTE = "Quelle: 1920–1995 Historische Statistik der Schweiz HSSO, Tab. F.18a; 1996–2025 SNB-Datenportal (Reihe SECO amarbma, Total)"
LANG = "de"
OUT_NAME = "abbildung11-arbeitslosenquote-schweiz"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
# ─────────────────────────────────────────────────────────────────────────

# Load full annual data, stitch at YEAR_HSSO_END/YEAR_SECO_START. Keyed by
# year (not appended positionally) and re-sorted at the end — the HSSO
# source workbook has one stray duplicate row (1936) appended out of
# sequence after 1995, which would otherwise draw a spurious line segment
# jumping back and forth in time.
by_year = {}
with open(HSSO_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        y = int(row["year"])
        if YEAR_START <= y <= YEAR_HSSO_END:
            by_year[y] = (float(row["registrierte_arbeitslose_total"]), float(row["arbeitslosenquote_pct"]))
with open(SECO_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        y = int(row["year"])
        if YEAR_SECO_START <= y <= YEAR_END:
            by_year[y] = (float(row["registrierte_arbeitslose_jahresdurchschnitt"]), float(row["arbeitslosenquote_pct_jahresdurchschnitt"]))

years = sorted(by_year)
count = [by_year[y][0] for y in years]
rate = [by_year[y][1] for y in years]

apply_theme()
x = np.array(years, dtype=float)
color_left = CATEGORICAL[0]   # olive — rate
color_right = CATEGORICAL[1]  # purple — absolute count

x_pad = (x[-1] - x[0]) * 0.02  # small breathing room, not a label reservation


def build_axes(ax_left):
    ax_left.set_facecolor(SURFACE)
    ax_left.spines["top"].set_visible(False)
    ax_left.spines["left"].set_color(color_left)
    ax_left.spines["left"].set_linewidth(1.4)
    ax_left.spines["bottom"].set_color(GRIDLINE)
    ax_left.spines["bottom"].set_linewidth(1)
    ax_left.tick_params(axis="y", colors=color_left, labelsize=11, length=0)
    ax_left.tick_params(axis="x", colors=INK_SECONDARY, labelsize=11, length=0)
    ax_left.yaxis.grid(True, color=GRIDLINE, linewidth=1, zorder=0)
    ax_left.set_axisbelow(True)
    ax_left.set_xticks(X_TICKS)
    ax_left.set_xticklabels([str(t) for t in X_TICKS])
    ax_left.set_ylabel(LEFT_Y_LABEL, color=color_left, fontweight="bold")
    ax_left.set_ylim(0, max(rate) * 1.12)
    ax_left.set_xlim(x[0] - x_pad, x[-1] + x_pad)

    ax_right = ax_left.twinx()
    ax_right.set_facecolor("none")
    ax_right.spines["top"].set_visible(False)
    ax_right.spines["left"].set_visible(False)
    ax_right.spines["right"].set_color(color_right)
    ax_right.spines["right"].set_linewidth(1.4)
    ax_right.tick_params(axis="y", colors=color_right, labelsize=11, length=0)
    ax_right.grid(False)
    ax_right.set_ylabel(RIGHT_Y_LABEL, color=color_right, fontweight="bold")
    ax_right.set_ylim(0, max(count) * 1.12)
    return ax_right


def add_titles(fig):
    fig.text(0.02, 0.97, TITLE, fontsize=17, fontweight="bold", color=BRAND_NAVY, ha="left", va="top")
    fig.text(0.02, 0.91, SUBTITLE, fontsize=12, color=INK_SECONDARY, ha="left", va="top")
    add_footer(fig, SOURCE_NOTE)


def legend_labels():
    return (
        f"{SERIES_LEFT_NAME} ({LEFT_VALUE_FMT.format(rate[-1])}, {years[-1]})",
        f"{SERIES_RIGHT_NAME} ({RIGHT_VALUE_FMT.format(count[-1])}, {years[-1]})",
    )


# ── static PNG ──────────────────────────────────────────────────────────────
fig, ax_left = plt.subplots(figsize=FIGSIZE)
fig.subplots_adjust(top=0.80, bottom=0.10, left=0.09, right=0.90)
ax_right = build_axes(ax_left)
add_titles(fig)

(line_l,) = ax_left.plot(x, rate, color=color_left, linewidth=2.2, zorder=4)
ax_left.plot(x[-1], rate[-1], marker="o", markersize=7, markerfacecolor="#FFFFFF",
             markeredgecolor=color_left, markeredgewidth=2, zorder=5)

(line_r,) = ax_right.plot(x, count, color=color_right, linewidth=2.2, zorder=3)
ax_right.plot(x[-1], count[-1], marker="o", markersize=7, markerfacecolor="#FFFFFF",
              markeredgecolor=color_right, markeredgewidth=2, zorder=4)

label_left, label_right = legend_labels()
ax_left.legend([line_l, line_r], [label_left, label_right], loc="upper left",
               frameon=False, fontsize=11, labelcolor=[color_left, color_right],
               handlelength=1.4, bbox_to_anchor=(0.0, 1.0))

save_png(fig, os.path.join(OUT_DIR, f"{OUT_NAME}.png"))
plt.close(fig)

# ── animated GIF ─────────────────────────────────────────────────────────────
fig, ax_left = plt.subplots(figsize=FIGSIZE)
fig.subplots_adjust(top=0.80, bottom=0.10, left=0.09, right=0.90)
ax_right = build_axes(ax_left)
add_titles(fig)

(line_l,) = ax_left.plot([], [], color=color_left, linewidth=2.2, zorder=4)
(marker_l,) = ax_left.plot([], [], marker="o", markersize=7, markerfacecolor="#FFFFFF",
                            markeredgecolor=color_left, markeredgewidth=2, zorder=5)
(line_r,) = ax_right.plot([], [], color=color_right, linewidth=2.2, zorder=3)
(marker_r,) = ax_right.plot([], [], marker="o", markersize=7, markerfacecolor="#FFFFFF",
                             markeredgecolor=color_right, markeredgewidth=2, zorder=4)

label_left, label_right = legend_labels()
legend = ax_left.legend([line_l, line_r], [label_left, label_right], loc="upper left",
                         frameon=False, fontsize=11, labelcolor=[color_left, color_right],
                         handlelength=1.4, bbox_to_anchor=(0.0, 1.0))
legend.set_visible(False)

DRAW_FRAMES, LABEL_FRAMES = 40, 12
TOTAL = DRAW_FRAMES + LABEL_FRAMES


def reveal_point(xs, ys, frac):
    pos = frac * (len(xs) - 1)
    idx = int(np.floor(pos))
    rem = pos - idx
    if idx >= len(xs) - 1:
        return xs, ys
    xr = np.append(xs[: idx + 1], xs[idx] + rem * (xs[idx + 1] - xs[idx]))
    yr = np.append(ys[: idx + 1], ys[idx] + rem * (ys[idx + 1] - ys[idx]))
    return xr, yr


def update(i):
    if i < DRAW_FRAMES:
        frac = i / (DRAW_FRAMES - 1)
        xr, yr = reveal_point(x, np.array(rate), frac)
        line_l.set_data(xr, yr)
        marker_l.set_data([xr[-1]], [yr[-1]])
        xr2, yr2 = reveal_point(x, np.array(count), frac)
        line_r.set_data(xr2, yr2)
        marker_r.set_data([xr2[-1]], [yr2[-1]])
    else:
        j = i - DRAW_FRAMES
        legend.set_visible(True)
        legend.set_alpha(min(1.0, (j + 1) / LABEL_FRAMES))


save_gif(fig, update, TOTAL, os.path.join(OUT_DIR, f"{OUT_NAME}.gif"))
