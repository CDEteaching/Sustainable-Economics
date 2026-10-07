"""
Chapter 3, fig9: direct and indirect rebound effects of an energy-saving car.
English redraw (cde-figures skill) of the German original. Run:
    python fig9_rebound_effect_car.py
Writes .ai / .svg / .png next to this script.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from cde_figure_style import (
    apply_theme, new_canvas, add_ai_disclosure, draw_box, draw_circle_node, draw_arrow,
    save_all, BRAND, SURFACE, INK_PRIMARY,
)

# ── DATA ────────────────────────────────────────────────────────────────────
LANG = "en"
OUT_NAME = "fig9_rebound_effect_car"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

CAR_LABEL = "Energy-saving car"
GREY_ENERGY_LABEL = "Grey energy"
LOWER_COSTS_LABEL = "Lower\nenergy costs"
INDIRECT_LABEL, DIRECT_LABEL = "indirect", "direct"
INDIRECT_USE_LABEL = "Flight for\na holiday"
DIRECT_USE_LABEL = "Longer or more\nfrequent trips"
SAVING_LABEL = "less energy"
MORE_LABEL = "more energy"
ENERGY_LABEL = "Energy\nuse"

REBOUND = BRAND["orange"]
SAVING = BRAND["olive"]
# ─────────────────────────────────────────────────────────────────────────


def draw_car_glyph(ax, center, size, color=SURFACE, zorder=6):
    """Side view of a small car: body, cabin and two wheels."""
    cx, cy = center
    bw, bh = size * 0.80, size * 0.20
    ax.add_patch(FancyBboxPatch((cx - bw / 2, cy - bh / 2), bw, bh,
                                boxstyle=f"round,pad=0,rounding_size={size * 0.06}",
                                facecolor=color, edgecolor="none", zorder=zorder))
    top = cy + bh / 2
    ax.add_patch(Polygon([(cx - bw * 0.30, top - 0.01), (cx - bw * 0.16, top + size * 0.17),
                          (cx + bw * 0.16, top + size * 0.17), (cx + bw * 0.32, top - 0.01)],
                         closed=True, facecolor=color, edgecolor="none", zorder=zorder))
    for dx in (-bw * 0.28, bw * 0.28):
        ax.add_patch(Circle((cx + dx, cy - bh / 2), size * 0.10, facecolor=color,
                            edgecolor=BRAND["navy"], lw=1.5, zorder=zorder + 1))


apply_theme()
fig, ax = new_canvas(figsize=(13, 6), xlim=(0, 15), ylim=(-0.5, 6.4))

car, top_cost, bot_cost = (1.6, 3.0), (5.0, 4.9), (5.0, 1.1)
top_use, bot_use, energy = (9.6, 4.9), (9.6, 1.1), (13.6, 3.0)

# Car with grey energy flowing into it
draw_circle_node(ax, car, 1.05, fill=BRAND["navy"], edge=BRAND["navy"])
draw_car_glyph(ax, (car[0], car[1] + 0.05), 1.5)
ax.text(car[0], car[1] - 1.35, CAR_LABEL, ha="center", va="top", fontsize=11, fontweight="bold")
ax.text(car[0], 6.05, GREY_ENERGY_LABEL, ha="center", va="center", fontsize=11, color=INK_PRIMARY)
draw_arrow(ax, (car[0], 5.75), (car[0], car[1] + 1.1), color="#9A968C", shrink=0, lw=3)

# Rebound pathways (orange) and the direct saving (olive)
for c in (top_cost, bot_cost):
    draw_box(ax, (c[0] - 1.25, c[1] - 0.55), 2.5, 1.1, LOWER_COSTS_LABEL, edge=REBOUND, fontsize=11)
for c in (top_use, bot_use):
    draw_box(ax, (c[0] - 1.45, c[1] - 0.6), 2.9, 1.2, c is top_use and INDIRECT_USE_LABEL
             or DIRECT_USE_LABEL, edge=REBOUND, fontsize=11)
draw_circle_node(ax, energy, 0.95, ENERGY_LABEL, fill=BRAND["navy"], edge=BRAND["navy"],
                 text_color=SURFACE, fontsize=12, fontweight="bold")

draw_arrow(ax, (2.5, 3.55), (3.75, 4.6), color=REBOUND, shrink=0, lw=2.6, zorder=8)
draw_arrow(ax, (2.5, 2.45), (3.75, 1.4), color=REBOUND, shrink=0, lw=2.6, zorder=8)
draw_arrow(ax, (6.25, top_cost[1]), (8.15, top_use[1]), color=REBOUND, shrink=2, lw=2.6,
           label=INDIRECT_LABEL, label_fontsize=11)
draw_arrow(ax, (6.25, bot_cost[1]), (8.15, bot_use[1]), color=REBOUND, shrink=2, lw=2.6,
           label=DIRECT_LABEL, label_fontsize=11)
for (x0, y0), (x1, y1), dy, rot in (((11.05, 4.75), (12.85, 3.6), 0.32, -33),
                                    ((11.05, 1.25), (12.85, 2.4), 0.32, 33)):
    draw_arrow(ax, (x0, y0), (x1, y1), color=REBOUND, shrink=0, lw=2.6, zorder=8)
    ax.text((x0 + x1) / 2 + 0.15, (y0 + y1) / 2 + dy, MORE_LABEL, ha="center", va="center",
            fontsize=10.5, color=REBOUND, fontweight="bold", rotation=rot)
draw_arrow(ax, (car[0] + 1.1, car[1]), (energy[0] - 0.95, energy[1]), color=SAVING, shrink=2, lw=3.2)
ax.text(7.3, car[1] + 0.2, SAVING_LABEL, ha="center", va="bottom", fontsize=11.5,
        fontweight="bold", color=SAVING)

add_ai_disclosure(fig, lang=LANG)
save_all(fig, OUT_DIR, OUT_NAME)
