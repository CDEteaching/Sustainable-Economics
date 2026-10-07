"""
Chapter 3, fig3: economy and nature as two separate spheres.
English redraw (cde-figures skill) of the German original. Run:
    python fig3_economy_nature_separate.py
Writes .ai / .svg / .png next to this script.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cde_figure_style import (
    apply_theme, new_canvas, add_ai_disclosure, draw_box, draw_circle_node, draw_arrow,
    draw_people_glyph, draw_factory_glyph, draw_institution_glyph, draw_globe_glyph,
    draw_leaf_glyph, draw_cloud_glyph, save_all, BRAND, SURFACE, INK_SECONDARY,
)

# ── DATA ────────────────────────────────────────────────────────────────────
LANG = "en"
OUT_NAME = "fig3_economy_nature_separate"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

ECONOMY_LABEL = "Economy"
ECONOMY_ACTORS = [  # (label, glyph, centre)
    ("Households", draw_people_glyph, (2.0, 5.0)),
    ("Firms", draw_factory_glyph, (4.6, 5.0)),
    ("State", draw_institution_glyph, (2.0, 2.4)),
    ("Rest of the world", draw_globe_glyph, (4.6, 2.4)),
]
ECOSYSTEM_LABEL = "Ecosystem"
ECOSYSTEM_ITEMS = [  # (label, glyph, centre)
    ("Resource extraction", draw_leaf_glyph, (10.4, 4.5)),
    ("Emissions / waste", draw_cloud_glyph, (10.4, 3.0)),
]
ARROW_RESOURCES = "Resources"
ARROW_WASTE = "Waste and emissions"
# ─────────────────────────────────────────────────────────────────────────

apply_theme()
fig, ax = new_canvas(figsize=(13, 6.2), xlim=(0, 14), ylim=(0, 6.8))

# Economy: rounded box with four actor nodes
draw_box(ax, (0.6, 0.9), 5.4, 5.6, edge=BRAND["navy"], lw=2.2, radius=0.25)
ax.text(3.3, 6.05, ECONOMY_LABEL, ha="center", va="center", fontsize=17,
        fontweight="bold", color=BRAND["navy"])
for label, glyph, (cx, cy) in ECONOMY_ACTORS:
    draw_circle_node(ax, (cx, cy), 0.95, fill=BRAND["navy"], edge=BRAND["navy"])
    glyph(ax, (cx, cy + 0.12), 1.15)
    ax.text(cx, cy - 0.62, label, ha="center", va="center", fontsize=9.5, color=SURFACE, zorder=7)

# Ecosystem: large olive circle with two items
draw_circle_node(ax, (11.0, 3.7), 2.75, fill=BRAND["olive"], edge=BRAND["olive"])
ax.text(11.0, 5.55, ECOSYSTEM_LABEL, ha="center", va="center", fontsize=17,
        fontweight="bold", color=SURFACE, zorder=7)
for label, glyph, (cx, cy) in ECOSYSTEM_ITEMS:
    glyph(ax, (cx - 1.1, cy), 1.0)
    ax.text(cx - 0.4, cy, label, ha="left", va="center", fontsize=11.5, color=SURFACE, zorder=7)

# Flows between the two spheres
draw_arrow(ax, (8.0, 4.4), (6.2, 4.4), color=INK_SECONDARY, shrink=0, label=ARROW_RESOURCES)
draw_arrow(ax, (6.2, 3.0), (8.0, 3.0), color=INK_SECONDARY, shrink=0, label=ARROW_WASTE)

add_ai_disclosure(fig, lang=LANG)
save_all(fig, OUT_DIR, OUT_NAME)
