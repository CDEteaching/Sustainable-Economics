"""
Chapter 3, fig12: Kuznets curve (stylized inverted U).
English redraw (cde-figures skill) of the German original. Run:
    python fig12_kuznets_curve.py
Writes .ai / .svg / .png next to this script.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cde_figure_style import (
    apply_theme, new_canvas, add_ai_disclosure, draw_arrow,
    save_all, BRAND, INK_PRIMARY,
)

# ── DATA ────────────────────────────────────────────────────────────────────
LANG = "en"
OUT_NAME = "fig12_kuznets_curve"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

X_LABEL = "Income per capita"
Y_LABEL = "Inequality"
# ─────────────────────────────────────────────────────────────────────────

apply_theme()
fig, ax = new_canvas(figsize=(9, 5.4), xlim=(-1.2, 11), ylim=(-1.6, 6.2))

draw_arrow(ax, (0, 0), (10.6, 0), color=INK_PRIMARY, shrink=0, lw=1.6)
draw_arrow(ax, (0, 0), (0, 5.9), color=INK_PRIMARY, shrink=0, lw=1.6)
ax.text(5.3, -0.45, X_LABEL, ha="center", va="top", fontsize=15)
ax.text(-0.45, 2.9, Y_LABEL, ha="center", va="center", rotation=90, fontsize=15)

x = np.linspace(0.8, 9.8, 200)
y = 5.0 - 4.2 * ((x - 5.3) / 4.5) ** 2
ax.plot(x, y, color=BRAND["navy"], lw=3.5, solid_capstyle="round")

add_ai_disclosure(fig, lang=LANG)
save_all(fig, OUT_DIR, OUT_NAME)
