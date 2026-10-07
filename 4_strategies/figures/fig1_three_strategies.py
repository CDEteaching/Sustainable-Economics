"""
Chapter 4, fig1: the three sustainability strategies (sufficiency, consistency,
efficiency), once as questions for the individual, once for society.
English redraw (cde-figures skill) of the German original. Run:
    python fig1_three_strategies.py
Writes .ai / .svg / .png next to this script.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Circle
from cde_figure_style import (
    apply_theme, new_canvas, add_ai_disclosure, save_all, BRAND, INK_PRIMARY, INK_SECONDARY,
)

# ── DATA ────────────────────────────────────────────────────────────────────
LANG = "en"
OUT_NAME = "fig1_three_strategies"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# (heading, {strategy: question})
TRIADS = [
    ("Individual level", {
        "Sufficiency": "“What do I really\nneed, and why?”",
        "Consistency": "“How can I make\nwhat I need\nsustainable?”",
        "Efficiency": "“How can I minimize\nresource use in\nproduction and\nconsumption?”",
    }),
    ("Societal level", {
        "Sufficiency": "“What do we as a\nsociety really need,\nand why?”",
        "Consistency": "“How can we make\nwhat we need\nsustainable?”",
        "Efficiency": "“How can we as a\nsociety minimize\nresource use?”",
    }),
]
COLORS = {"Sufficiency": BRAND["olive"], "Consistency": BRAND["orange"], "Efficiency": BRAND["navy"]}
# ─────────────────────────────────────────────────────────────────────────

apply_theme()
fig, ax = new_canvas(figsize=(14, 7.6), xlim=(0, 20), ylim=(-0.6, 10.2))

R = 2.45
for i, (heading, questions) in enumerate(TRIADS):
    cx = 5.0 + i * 10.0
    ax.text(cx, 9.75, heading, ha="center", va="center", fontsize=15,
            fontweight="bold", color=INK_SECONDARY)
    centres = {
        "Sufficiency": (cx, 6.6),
        "Consistency": (cx - 1.75, 3.75),
        "Efficiency": (cx + 1.75, 3.75),
    }
    # where each circle's text sits, pushed away from the overlap
    text_pos = {
        "Sufficiency": (cx, 7.15),
        "Consistency": (cx - 2.35, 3.3),
        "Efficiency": (cx + 2.35, 3.3),
    }
    for name, (x, y) in centres.items():
        ax.add_patch(Circle((x, y), R, facecolor=COLORS[name], edgecolor="none",
                            alpha=0.78, zorder=2))
    for name, (tx, ty) in text_pos.items():
        ax.text(tx, ty + 0.85, name, ha="center", va="center", fontsize=13,
                fontweight="bold", color="#FFFFFF", zorder=4)
        ax.text(tx, ty - 0.35, questions[name], ha="center", va="center", fontsize=10.5,
                color="#FFFFFF", zorder=4, linespacing=1.25)

add_ai_disclosure(fig, lang=LANG)
save_all(fig, OUT_DIR, OUT_NAME)
