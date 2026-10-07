"""
Shared visual style + save helpers for CDE-branded PowerPoint charts.

Categorical palette: CDE olive-green (site nav-pill #869E2F, from
cdeteaching.github.io/Basics-of-sustainability) plus purple/brown/pink chosen
by Christoph, each nudged in OKLCH (lightness/chroma only, hue held) to clear
an accessibility-validated CVD/normal-vision ΔE gate (deuteranopia/
protanopia/tritanopia simulation + CAM02-UCS ΔE, threshold ≥ 8 under CVD /
≥ 15 normal vision, adjacent pairs). See ../references/palette.md for the
full derivation and validator output.

Import this from a chart template, never hardcode colors in the template itself.
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation, PillowWriter

# ── palette (light surface — see references/palette.md) ─────────────────────
SURFACE = "#FFFFFF"
INK_PRIMARY = "#222322"      # titles, value labels, direct labels
INK_SECONDARY = "#6B685F"    # axis ticks, legend text (5.6:1 on white)
GRIDLINE = "#D8D5CE"         # hairline horizontal gridlines only
BRAND_NAVY = "#003A70"       # headline/title accent — text only, never a data mark

# Categorical, fixed order — validated adjacent-pair CVD + normal-vision floor.
# Caps at 4 series for line/bar; beyond that, facet or fold into "Other"
# rather than adding a 5th hue.
CATEGORICAL = [
    "#869E2F",  # 1 olive   (site nav-pill green, unchanged brand hue)
    "#9E6CB4",  # 2 purple  (nudged from Christoph's #9970AB — chroma raised to clear the 0.10 floor)
    "#815208",  # 3 brown   (nudged from Christoph's #BF812D — darkened; at the original L it was
                #            almost indistinguishable from olive under deuteranopia, ΔE 1.3)
    "#CF72A3",  # 4 pink    (nudged from Christoph's #DE77AE — lightness trimmed into the validated band)
]

# Sequential — single hue (chart-navy), light -> dark, for magnitude encoding
# (heatmap-style or a single ordered series). Step 700 lands near brand navy.
SEQUENTIAL = ["#A0E9FF", "#80C8FF", "#5BA1F3", "#357CCA", "#0558A3", "#00347D"]

# ── AI transparency notice (EU AI Act Art. 50) ───────────────────────────────
# Charts are AI-assisted content, so every chart discloses that — but not by
# stamping it onto the image itself (pixels get reused/cropped/re-exported
# without their context). Instead this fixed wording goes into the chart's
# README.md as its own line (see SKILL.md workflow step 7), and a Quarto
# embed links to that README (see SKILL.md's Quarto section). Fixed wording,
# not part of a template's editable DATA block — if it needs to change, edit
# it here. Pick the language to match the chart's own language; don't reword
# the strings themselves per chart.
AI_DISCLOSURE = "This chart was created with the assistance of Claude Code (Anthropic) — transparency notice per EU AI Act Art. 50."
AI_DISCLOSURE_DE = "Diese Grafik wurde mit Unterstützung von Claude Code (Anthropic) erstellt — Transparenzhinweis gem. Art. 50 EU AI Act."

FONT_CANDIDATES = ["Roboto", "Lato", "Segoe UI", "DejaVu Sans"]


def _first_available_font():
    installed = {f.name for f in fm.fontManager.ttflist}
    for name in FONT_CANDIDATES:
        if name in installed:
            return name
    return "sans-serif"


def apply_theme():
    """Call once per script, before creating any figure."""
    font = _first_available_font()
    matplotlib.rcParams.update({
        "font.family": font,
        "font.size": 13,
        "text.color": INK_PRIMARY,
        "axes.edgecolor": GRIDLINE,
        "axes.labelcolor": INK_SECONDARY,
        "axes.titlecolor": INK_PRIMARY,
        "xtick.color": INK_SECONDARY,
        "ytick.color": INK_SECONDARY,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
    })


def add_footer(fig, source_note):
    """Chart footer: data source note only. The AI-assistance disclosure
    (EU AI Act Art. 50) does not go on the image — it lives in the chart's
    README.md instead, see AI_DISCLOSURE / AI_DISCLOSURE_DE above."""
    fig.text(0.02, 0.02, source_note, fontsize=8.5, color=INK_SECONDARY, ha="left", va="bottom")


def style_axes(ax, *, y_grid=True, x_grid=False):
    """Recessive chrome: no top/right spine, hairline gridlines, muted ticks."""
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRIDLINE)
        ax.spines[side].set_linewidth(1)
    ax.tick_params(colors=INK_SECONDARY, labelsize=11, length=0)
    ax.grid(False)
    if y_grid:
        ax.yaxis.grid(True, color=GRIDLINE, linewidth=1, zorder=0)
    if x_grid:
        ax.xaxis.grid(True, color=GRIDLINE, linewidth=1, zorder=0)
    ax.set_axisbelow(True)


def ease_out_cubic(t):
    """t in [0,1] -> eased [0,1]. Used for bar-grow / doughnut-sweep animation."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


# ── output sizing ─────────────────────────────────────────────────────────
# 16:9 widescreen content area, sized to drop straight into a PPT slide.
FIGSIZE = (10, 5.63)
PNG_DPI = 300      # print/export-quality static chart
GIF_DPI = 120      # screen resolution is enough for an inserted GIF; keeps file size sane


def save_png(fig, path):
    fig.savefig(path, dpi=PNG_DPI, bbox_inches="tight", facecolor=SURFACE)
    print(f"saved {path}")


def save_gif(fig, update_fn, n_frames, path, *, fps=25, hold_seconds=1.5):
    """
    update_fn(frame_index) mutates the artists in place for that frame.
    Holds the final frame for `hold_seconds` before the GIF loops (PowerPoint
    autoplays inserted GIFs and loops them, so the pause reads as "done").
    """
    hold_frames = int(fps * hold_seconds)
    total = n_frames + hold_frames

    def _frame(i):
        update_fn(min(i, n_frames - 1))

    anim = FuncAnimation(fig, _frame, frames=total, interval=1000 / fps)
    anim.save(path, writer=PillowWriter(fps=fps), dpi=GIF_DPI, savefig_kwargs={"facecolor": SURFACE})
    plt.close(fig)
    print(f"saved {path}")
