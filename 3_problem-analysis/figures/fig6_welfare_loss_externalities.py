"""
Chapter 3, fig6: welfare loss (grey triangle) with external costs.
English redraw (cde-figures skill) of the German original. Run:
    python fig6_welfare_loss_externalities.py
Writes .ai / .svg / .png next to this script.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Polygon
from cde_figure_style import (
    apply_theme, new_canvas, add_ai_disclosure, draw_arrow,
    save_all, BRAND, INK_PRIMARY, INK_SECONDARY, GRIDLINE,
)

# ── DATA ────────────────────────────────────────────────────────────────────
LANG = "en"
OUT_NAME = "fig6_welfare_loss_externalities"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

DEMAND_LABEL = "Demand"
PRIVATE_MC_LABEL = "Private\nmarginal cost"
SOCIAL_MC_LABEL = "Social\nmarginal cost"
X_LABEL, Y_LABEL = "y", "p"

# Linear curves p = a + b*y
DEMAND = (9.0, -0.8)
PRIVATE_MC = (1.0, 0.8)
SOCIAL_MC = (3.0, 0.8)   # private marginal cost + external cost per unit
Y_MAX = 9.5
# ─────────────────────────────────────────────────────────────────────────


def p(curve, y):
    return curve[0] + curve[1] * y


def intersect(c1, c2):
    y = (c2[0] - c1[0]) / (c1[1] - c2[1])
    return y, p(c1, y)


apply_theme()
fig, ax = new_canvas(figsize=(8, 7.4), xlim=(-1.0, 11.5), ylim=(-1.6, 10.2))

# Axes
draw_arrow(ax, (0, 0), (10.6, 0), color=INK_PRIMARY, shrink=0, lw=1.6)
draw_arrow(ax, (0, 0), (0, 10), color=INK_PRIMARY, shrink=0, lw=1.6)
ax.text(10.8, -0.05, X_LABEL, fontsize=15, style="italic", ha="left", va="center")
ax.text(-0.05, 10.25, Y_LABEL, fontsize=15, style="italic", ha="center", va="bottom")

y_a, p_a = intersect(DEMAND, PRIVATE_MC)   # market outcome A
y_b, p_b = intersect(DEMAND, SOCIAL_MC)    # optimum B

# Welfare loss triangle
ax.add_patch(Polygon([(y_b, p_b), (y_a, p_a), (y_a, p(SOCIAL_MC, y_a))], closed=True,
                     facecolor="#D9D9D9", edgecolor="none", zorder=1))

# Curves
ys = [0, Y_MAX]
ax.plot(ys, [p(DEMAND, y) for y in ys], color=BRAND["olive"], lw=3, zorder=3)
ax.plot([0, 8.6], [p(PRIVATE_MC, 0), p(PRIVATE_MC, 8.6)], color=BRAND["navy"], lw=3, zorder=3)
ax.plot([0, 6.2], [p(SOCIAL_MC, 0), p(SOCIAL_MC, 6.2)], color=BRAND["orange"], lw=3,
        ls=(0, (3, 2)), zorder=3)
ax.text(Y_MAX + 0.15, p(DEMAND, Y_MAX), DEMAND_LABEL, fontsize=12, va="center", color=BRAND["olive"])
ax.text(8.75, p(PRIVATE_MC, 8.6), PRIVATE_MC_LABEL, fontsize=12, va="center", color=BRAND["navy"])
ax.text(6.35, p(SOCIAL_MC, 6.2), SOCIAL_MC_LABEL, fontsize=12, va="center", color=BRAND["orange"])

# Points with guide lines to the axes
for (yy, pp), name, pname, yname in [((y_a, p_a), "A", "p′", "y′"),
                                     ((y_b, p_b), "B", "p*", "y*")]:
    ax.plot([0, yy], [pp, pp], color=INK_SECONDARY, lw=1, ls=(0, (4, 3)), zorder=2)
    ax.plot([yy, yy], [0, pp], color=INK_SECONDARY, lw=1, ls=(0, (4, 3)), zorder=2)
    ax.plot(yy, pp, "o", color=INK_PRIMARY, ms=8, zorder=5)
    ax.text(yy + (0.25 if name == "A" else -0.25), pp + 0.3, name, fontsize=13,
            fontweight="bold", ha="left" if name == "A" else "right")
    ax.text(-0.2, pp, pname, fontsize=13, ha="right", va="center", style="italic")
    ax.text(yy, -0.3, yname, fontsize=13, ha="center", va="top", style="italic")

add_ai_disclosure(fig, lang=LANG)
save_all(fig, OUT_DIR, OUT_NAME)
