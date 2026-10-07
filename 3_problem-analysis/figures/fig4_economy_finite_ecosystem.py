"""
Chapter 3, fig4: the economy embedded in a finite ecosystem ("full world").
English redraw (cde-figures skill) of the German original. Run:
    python fig4_economy_finite_ecosystem.py
Writes .ai / .svg / .png next to this script.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Circle, FancyArrow
from cde_figure_style import (
    apply_theme, new_canvas, add_ai_disclosure, draw_box, draw_arrow,
    save_all, BRAND, SURFACE, INK_PRIMARY, INK_SECONDARY,
)

# ── DATA ────────────────────────────────────────────────────────────────────
LANG = "en"
OUT_NAME = "fig4_economy_finite_ecosystem"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

ECOSYSTEM_LABEL = "Finite global ecosystem"
ECONOMY_LABEL = "Growing\neconomic\nsubsystem"
SOURCE_LABEL = "Source functions"
SINK_LABEL = "Sink functions"
SUN_LABEL = "Solar\nenergy"
FULL_WORLD_LABEL = "\"Full world\""
RECYCLING_LABEL = "Recycled matter"
WASTE_HEAT_LABEL = "Waste heat"
ENERGY, RESOURCES = "Energy", "Resources"
# ─────────────────────────────────────────────────────────────────────────

apply_theme()
fig, ax = new_canvas(figsize=(9, 9), xlim=(0, 10), ylim=(-0.4, 10))
TEAL_LIGHT = "#DCE9E9"

# Ecosystem circle and economy box
ax.add_patch(Circle((5, 5.2), 4.0, facecolor=TEAL_LIGHT, edgecolor=BRAND["olive"], lw=3, zorder=1))
ax.text(5, 8.65, ECOSYSTEM_LABEL, ha="center", va="center", fontsize=14,
        fontweight="bold", color=BRAND["olive"])
draw_box(ax, (3.0, 3.0), 4.0, 4.6, fill=SURFACE, edge=BRAND["navy"], lw=2, radius=0.1)
ax.text(5, 5.5, ECONOMY_LABEL, ha="center", va="center", fontsize=13,
        fontweight="bold", color=BRAND["navy"], zorder=4)

# Source (left) and sink (right) functions
ax.text(1.55, 5.2, SOURCE_LABEL, rotation=90, ha="center", va="center",
        fontsize=11.5, fontweight="bold", color=INK_PRIMARY)
ax.text(8.45, 5.2, SINK_LABEL, rotation=270, ha="center", va="center",
        fontsize=11.5, fontweight="bold", color=INK_PRIMARY)


def flow(x, y, label):
    """Block arrow pointing right, with its label inside."""
    ax.add_patch(FancyArrow(x, y, 1.5, 0, width=0.62, head_width=0.95, head_length=0.45,
                            length_includes_head=True, facecolor=BRAND["teal"],
                            edgecolor=BRAND["navy"], lw=1.2, zorder=5))
    ax.text(x + 0.62, y, label, ha="center", va="center", fontsize=10,
            fontweight="bold", color=INK_PRIMARY, zorder=6)


# Inflows cross the left edge of the economy, outflows the right edge
flow(2.15, 6.5, ENERGY)
flow(2.15, 4.3, RESOURCES)
flow(6.35, 6.5, ENERGY)
flow(6.35, 4.3, RESOURCES)

# Recycling loop at the bottom of the economy
draw_box(ax, (3.9, 2.55), 2.2, 0.75, RECYCLING_LABEL, fill="#EEF2E0",
         edge=BRAND["olive"], fontsize=10, lw=1.4, zorder=6)
draw_arrow(ax, (6.9, 3.95), (6.1, 2.95), color=INK_SECONDARY, curve=-0.4, shrink=2, zorder=7)
draw_arrow(ax, (3.9, 2.95), (3.15, 3.95), color=INK_SECONDARY, curve=-0.4, shrink=2, zorder=7)

# Solar energy in, waste heat out
ax.add_patch(Circle((1.0, 9.0), 0.62, facecolor="#FFF4D6", edgecolor="#E8A33C", lw=1.6, zorder=3))
ax.add_patch(Circle((1.0, 9.18), 0.17, facecolor="#E8A33C", edgecolor="none", zorder=4))
ax.text(1.0, 8.78, SUN_LABEL, ha="center", va="center", fontsize=8, color=INK_PRIMARY, zorder=4)
draw_arrow(ax, (1.5, 8.6), (2.45, 7.05), color="#E8A33C", shrink=0, lw=2.2)
draw_arrow(ax, (5, 1.25), (5, 0.35), color=INK_SECONDARY, shrink=0, lw=2.2)
ax.text(5, 0.05, WASTE_HEAT_LABEL, ha="center", va="center", fontsize=10.5,
        fontweight="bold", color=INK_PRIMARY)
ax.text(0.45, 5.2 + 2.5, FULL_WORLD_LABEL, ha="left", va="center", fontsize=11,
        fontweight="bold", color=INK_PRIMARY)

add_ai_disclosure(fig, lang=LANG)
save_all(fig, OUT_DIR, OUT_NAME)
