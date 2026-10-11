"""
Chapter 2, fig8: circular flow model including unpaid work, based on
Elson (2000, Progress of the World's Women). Own redraw in the style of
fig6 (simple economic circuit) and fig7 (extended economic circuit):
steel-blue rounded boxes, Frutiger, black curved arrows. Run:
    python fig8_circular_flow_elson.py
Writes .ai / .svg / .png next to this script.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
from matplotlib.font_manager import FontProperties, fontManager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from cde_figure_style import apply_theme, new_canvas, add_ai_disclosure, save_all

# ── DATA ────────────────────────────────────────────────────────────────────
LANG = "en"
OUT_NAME = "fig8_circular_flow_elson"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE = "#7795B6"        # box colour sampled from fig6/fig7
BLUE_LIGHT = "#C9D6E5"  # work not included in GDP
INK = "#000000"
GREY = "#8C8C8C"
HATCH = "#9DB3CB"       # subtle stripes so white text stays readable

# work types (fill, hatch, text colour, legend text)
WORK = {
    "formal": (BLUE, None, "#FFFFFF", "formal work, included in GDP"),
    "informal": (BLUE, "//", "#FFFFFF", "informal work, undercounted in GDP"),
    "unpaid": (BLUE_LIGHT, None, INK, "volunteer and unpaid care work, not included in GDP"),
}

# sector: (header, header xy, [(label, work type, x0, y0, w, h), ...])
SECTORS = {
    "private": ("private sector", (14.0, 23.55), [
        ("formal paid work", "formal", 10.5, 21.3, 7.0, 1.6),
        ("informal paid and unpaid work", "informal", 10.5, 19.4, 7.0, 1.6),
    ]),
    "public": ("public sector", (17.6, 16.75), [
        ("formal paid work", "formal", 15.5, 14.4, 6.0, 1.7),
    ]),
    "ngo": ("NGO sector", (6.2, 13.45), [
        ("formal paid work", "formal", 4.6, 11.1, 5.6, 1.6),
        ("volunteer work", "unpaid", 4.6, 9.3, 5.6, 1.6),
    ]),
    "domestic": ("domestic sector", (12.0, 7.75), [
        ("unpaid care work", "unpaid", 8.5, 4.4, 7.0, 2.7),
    ]),
}

# flow types (colour, linestyle, linewidth, legend text)
FLOW = {
    "market": (INK, "-", 3.0, "marketed goods and services and payments"),
    "public": (BLUE, "-", 3.0, "public services, income transfers and payments,\nless taxes and user fees"),
    "ngo": (INK, (0, (1.2, 1.2)), 2.6, "marketed and non-marketed goods and services,\nincluding information and advocacy"),
    "labour": (GREY, (0, (4, 2.5)), 2.4, "inputs of paid labour"),
    "volunteer": (GREY, (0, (4, 2, 1, 2)), 2.4, "inputs of paid labour and volunteer work"),
    "depletion": (GREY, "-", 2.4, "depletion of human capabilities"),
}

# (flow type, start, end, curvature)
EDGES = [
    ("market", (10.5, 22.1), (8.5, 5.8), 0.85),
    ("market", (11.2, 19.4), (9.2, 12.7), 0.12),
    ("market", (13.2, 19.4), (15.5, 15.25), 0.35),
    ("public", (20.6, 16.1), (16.4, 19.4), 0.2),
    ("public", (15.5, 14.9), (10.2, 11.9), -0.15),
    ("public", (17.5, 14.4), (15.5, 6.6), -0.25),
    ("ngo", (8.6, 9.3), (10.4, 7.1), 0.25),
    ("volunteer", (9.3, 7.1), (6.2, 9.3), -0.3),
    ("labour", (15.5, 6.3), (21.5, 14.9), 0.32),
    ("labour", (15.5, 5.0), (17.5, 21.7), 0.75),
    ("depletion", (10.0, 4.4), (8.2, 2.6), -0.15),
    ("depletion", (14.0, 4.4), (15.8, 2.6), 0.15),
]
DEPLETION_LABEL = ("depletion of human capabilities", (12.0, 2.25))
# ─────────────────────────────────────────────────────────────────────────

FONT_DIR = os.path.dirname(next(f.fname for f in fontManager.ttflist
                                if os.path.basename(f.fname) == "FrutigerNeueLTPro-Regular.otf"))
LIGHT = FontProperties(fname=os.path.join(FONT_DIR, "FrutigerNeueLTPro-Light.otf"))
REGULAR = FontProperties(fname=os.path.join(FONT_DIR, "FrutigerNeueLTPro-Regular.otf"))
BOLD = FontProperties(fname=os.path.join(FONT_DIR, "FrutigerNeueLTPro-Bold.otf"))


def box(ax, label, kind, x0, y0, w, h, size=15):
    fill, hatch, text_colour, _ = WORK[kind]
    pad = min(h, w) * 0.42
    ax.add_patch(FancyBboxPatch((x0 + pad, y0 + pad), w - 2 * pad, h - 2 * pad,
                                boxstyle=f"round,pad={pad},rounding_size={pad}",
                                facecolor=fill, edgecolor=HATCH if hatch else "none",
                                hatch=hatch, linewidth=0, zorder=3))
    ax.text(x0 + w / 2, y0 + h / 2, label, ha="center", va="center", fontsize=size,
            color=text_colour, fontproperties=LIGHT, zorder=4)


def arrow(ax, kind, start, end, rad):
    colour, ls, lw, _ = FLOW[kind]
    # line and head drawn separately so dashed flows keep a solid head
    ax.add_patch(FancyArrowPatch(start, end, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-", color=colour, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=6, capstyle="butt", zorder=2))
    ax.add_patch(FancyArrowPatch(start, end, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-|>,head_length=0.75,head_width=0.38",
                                 mutation_scale=22, color=colour, lw=0, shrinkA=0, shrinkB=0,
                                 zorder=2.5))


matplotlib.rcParams["hatch.linewidth"] = 1.6
apply_theme()
fig, ax = new_canvas(figsize=(12, 15), xlim=(0.5, 24), ylim=(-8.4, 24.4))

for header, (hx, hy), boxes in SECTORS.values():
    ax.text(hx, hy, header, ha="center", va="center", fontsize=15, color=INK,
            fontproperties=REGULAR)
    for b in boxes:
        box(ax, *b)

for kind, start, end, rad in EDGES:
    arrow(ax, kind, start, end, rad)
ax.text(*DEPLETION_LABEL[1], DEPLETION_LABEL[0], ha="center", va="center", fontsize=12,
        color=INK, fontproperties=REGULAR, style="italic")

# ── legend ────────────────────────────────────────────────────────────────
ax.add_line(Line2D([1.2, 23.3], [0.9, 0.9], color=INK, lw=0.8))
y = 0.0
for kind in FLOW:
    colour, ls, lw, text = FLOW[kind]
    yy = y - 0.35 * text.count("\n")
    ax.add_patch(FancyArrowPatch((1.4, yy), (3.6, yy), arrowstyle="-", color=colour, lw=lw,
                                 linestyle=ls, shrinkA=0, shrinkB=4, capstyle="butt"))
    ax.add_patch(FancyArrowPatch((1.4, yy), (3.6, yy), arrowstyle="-|>,head_length=0.6,head_width=0.3",
                                 mutation_scale=22, color=colour, lw=0, shrinkA=0, shrinkB=0))
    ax.text(4.1, yy, text, ha="left", va="center", fontsize=11, color=INK,
            fontproperties=REGULAR, linespacing=1.25)
    y -= 1.0 + 0.7 * text.count("\n")

y = 0.0
for kind, (fill, hatch, _, text) in WORK.items():
    ax.add_patch(FancyBboxPatch((15.2, y - 0.35), 1.4, 0.7, boxstyle="round,pad=0,rounding_size=0.25",
                                facecolor=fill, edgecolor=HATCH if hatch else "none",
                                hatch=hatch, linewidth=0))
    ax.text(16.9, y, text.replace(", not", ",\nnot"), ha="left", va="center", fontsize=11,
            color=INK, fontproperties=REGULAR, linespacing=1.25)
    y -= 1.3

add_ai_disclosure(fig, lang=LANG)
save_all(fig, OUT_DIR, OUT_NAME)
