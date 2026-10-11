"""
Shared visual style + save helpers for CDE textbook figures (diagrams, icons).

Raw brand palette pulled from cdeteaching/Basics-of-sustainability's own
theme.scss / theme.css — see ../references/palette.md for the full
derivation. Unlike the cde-charts skill's cde_style.py, these hexes are used
AS-IS here: figures in this skill are illustrative (diagrams, icon/pictogram
sets), not data-encoding chart marks, so the CVD-adjacent-pair validation
that drove cde-charts' palette doesn't govern this use the same way (see
references/palette.md for when it still matters — e.g. a multi-color icon
set used as a legend).

Import this from a diagram/icon template, never hardcode a hex value or a
fig.savefig call in the template itself.
"""

import os
import textwrap

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import (
    FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon, Ellipse, PathPatch,
)
from matplotlib.path import Path

# ── palette (raw brand hex — see references/palette.md) ─────────────────────
SURFACE = "#FFFFFF"
INK_PRIMARY = "#222322"      # titles, labels — site's own body-text color
INK_SECONDARY = "#6B685F"    # subtitles, arrow labels, source/disclosure notes
GRIDLINE = "#D8D5CE"

BRAND_NAVY = "#003A70"       # theme.scss $primary
BRAND_ORANGE = "#E54D23"     # theme.scss $sidebar-hl
BRAND_OLIVE = "#869E2F"      # theme.css --bs-nav-pills-link-active-bg
BRAND_TEAL = "#7BADAD"       # theme.css .readings-header background
BRAND_SLATE = "#1A2533"      # theme.css .circle-button background

BRAND = {
    "navy": BRAND_NAVY,
    "orange": BRAND_ORANGE,
    "olive": BRAND_OLIVE,
    "teal": BRAND_TEAL,
    "slate": BRAND_SLATE,
}

# ── AI transparency notice (EU AI Act Art. 50) ───────────────────────────────
# Same fixed-wording pattern as the cde-charts skill's cde_style.py — see
# that file's comment for why this lives here rather than in a template's
# editable DATA block. Diagrams get this footer automatically; icons don't
# (see SKILL.md — a tiny inline pictogram isn't the place for a sentence of
# disclosure text; put one disclosure line on the page/figure that hosts the
# icon set instead).
AI_DISCLOSURE = "Figure created with the assistance of Claude Code (Anthropic) — transparency notice per EU AI Act Art. 50."
AI_DISCLOSURE_DE = "Abbildung erstellt mit Unterstützung von Claude Code (Anthropic) — Transparenzhinweis gem. Art. 50 EU AI Act."

FONT_CANDIDATES = ["Roboto", "Lato", "Segoe UI", "DejaVu Sans"]

DIAGRAM_FIGSIZE = (10, 6.5)
ICON_FIGSIZE = (3, 3)


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
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
    })


def new_canvas(*, figsize=DIAGRAM_FIGSIZE, xlim=(0, 12), ylim=(0, 8), transparent=False):
    """A full-bleed, aspect-locked, axis-free canvas in data coordinates
    (xlim/ylim) — draw shapes directly in those units, no pixel math."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if transparent:
        ax.set_facecolor("none")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax


def add_title(fig, title, subtitle="", *, top_margin=0.16):
    """Reserves space at the top of the canvas and draws a title (+ optional
    subtitle), matching the cde-charts skill's chart title style."""
    fig.subplots_adjust(top=1 - top_margin)
    fig.text(0.02, 0.99, title, fontsize=16, fontweight="bold",
              color=BRAND_NAVY, ha="left", va="top")
    if subtitle:
        fig.text(0.02, 0.99 - top_margin * 0.42, subtitle, fontsize=11,
                  color=INK_SECONDARY, ha="left", va="top")


def add_ai_disclosure(fig, *, lang="en"):
    """Fixed one-line EU AI Act Art. 50 transparency notice, bottom-left."""
    text = AI_DISCLOSURE_DE if lang == "de" else AI_DISCLOSURE
    fig.text(0.02, 0.012, text, fontsize=7, color=INK_SECONDARY, ha="left", va="bottom")


def wrap_label(text, width_chars=16):
    """Approximate word-wrap for box/node labels. matplotlib doesn't auto-wrap
    text to a shape's bounds, so tune width_chars by eye against the box size
    and fontsize — re-run and check the PNG rather than guessing twice."""
    return "\n".join(textwrap.wrap(text, width_chars))


# ── drawing primitives ───────────────────────────────────────────────────────

def draw_box(ax, xy, width, height, label="", *, fill=SURFACE, edge=INK_PRIMARY,
             text_color=None, fontsize=12, fontweight="normal", radius=0.15,
             lw=1.6, zorder=2):
    """Rounded box with a centered label. xy is the bottom-left corner, in
    the canvas's data coordinates."""
    x, y = xy
    box = FancyBboxPatch((x, y), width, height,
                          boxstyle=f"round,pad=0,rounding_size={radius}",
                          linewidth=lw, edgecolor=edge, facecolor=fill, zorder=zorder)
    ax.add_patch(box)
    if label:
        ax.text(x + width / 2, y + height / 2, label, ha="center", va="center",
                 fontsize=fontsize, fontweight=fontweight,
                 color=text_color or INK_PRIMARY, zorder=zorder + 1)
    return box


def draw_circle_node(ax, center, radius, label="", *, fill=SURFACE, edge=INK_PRIMARY,
                      text_color=None, fontsize=12, fontweight="normal", lw=1.6, zorder=2):
    """Circular node with a centered label."""
    c = Circle(center, radius, linewidth=lw, edgecolor=edge, facecolor=fill, zorder=zorder)
    ax.add_patch(c)
    if label:
        ax.text(center[0], center[1], label, ha="center", va="center",
                 fontsize=fontsize, fontweight=fontweight,
                 color=text_color or INK_PRIMARY, zorder=zorder + 1)
    return c


def draw_arrow(ax, start, end, *, color=INK_SECONDARY, lw=2.0, style="-|>",
                curve=0.0, shrink=14, label="", label_fontsize=10, zorder=1):
    """Arrow between two node centers. `shrink` (points) pulls the visible
    line back from each end so it stops at a node's edge rather than its
    center, without needing exact shape-boundary geometry — the standard
    matplotlib pattern for node-to-node diagram arrows. `curve` is a
    connectionstyle rad value: 0 = straight, +/- bows left/right."""
    arrow = FancyArrowPatch(start, end, arrowstyle=style, color=color,
                             linewidth=lw, connectionstyle=f"arc3,rad={curve}",
                             shrinkA=shrink, shrinkB=shrink,
                             mutation_scale=16, zorder=zorder)
    ax.add_patch(arrow)
    if label:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my + 0.25, label, ha="center", va="bottom",
                 fontsize=label_fontsize, color=INK_SECONDARY, zorder=zorder + 1)
    return arrow


# ── icon glyphs (small pictograms for inside a diagram node) ────────────────
# Deliberately simplified silhouettes, not pixel-accurate icon-font recreations
# — built for recognizability at small size inside a colored circle/box, the
# same way the reference figures on the site use plain, flat icon marks.
# `size` is roughly the glyph's own bounding box (pass ~1.1-1.3x the node
# radius); `center` is the node's center. Each draws in a single `color`
# (default white, for a colored circle background) — call again with a
# different `color`/`center` for a two-tone or repeated icon.

def draw_people_glyph(ax, center, size, color="#FFFFFF", zorder=6):
    """Two simplified person silhouettes (head + shoulders), side by side."""
    cx, cy = center
    r_head = size * 0.16
    for dx in (-size * 0.20, size * 0.20):
        hx, hy = cx + dx, cy + size * 0.20
        ax.add_patch(Circle((hx, hy), r_head, facecolor=color, edgecolor="none", zorder=zorder))
        top_w, bot_w = size * 0.26, size * 0.42
        y_top, y_bot = cy + size * 0.03, cy - size * 0.30
        pts = [(hx - top_w / 2, y_top), (hx + top_w / 2, y_top),
               (hx + bot_w / 2, y_bot), (hx - bot_w / 2, y_bot)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none", zorder=zorder))


def draw_factory_glyph(ax, center, size, color="#FFFFFF", zorder=6):
    """A flat-roofed building block, a short chimney, and a single smoke
    puff — kept deliberately compact/centered (an earlier taller
    multi-puff version poked past the enclosing circle's edge and read as
    a blob on a stick rather than a factory)."""
    cx, cy = center
    bw, bh = size * 0.56, size * 0.26
    bx, by = cx - bw / 2, cy - size * 0.21
    ax.add_patch(Rectangle((bx, by), bw, bh, facecolor=color, edgecolor="none", zorder=zorder))
    cw, ch = size * 0.09, size * 0.14
    chx, chy0 = cx + bw * 0.18, by + bh
    ax.add_patch(Rectangle((chx - cw / 2, chy0), cw, ch, facecolor=color, edgecolor="none", zorder=zorder))
    ax.add_patch(Circle((chx + size * 0.02, chy0 + ch + size * 0.09), size * 0.055,
                         facecolor=color, edgecolor="none", alpha=0.85, zorder=zorder))


def draw_institution_glyph(ax, center, size, color="#FFFFFF", zorder=6):
    """A pediment triangle over columns over a base platform — government
    building / public-institution glyph."""
    cx, cy = center
    tw, th, apex_y = size * 0.66, size * 0.22, center[1] + size * 0.32
    ax.add_patch(Polygon([(cx - tw / 2, apex_y - th), (cx + tw / 2, apex_y - th), (cx, apex_y)],
                          closed=True, facecolor=color, edgecolor="none", zorder=zorder))
    base_w, base_h = size * 0.70, size * 0.07
    ax.add_patch(Rectangle((cx - base_w / 2, cy - size * 0.34), base_w, base_h,
                            facecolor=color, edgecolor="none", zorder=zorder))
    n_col, col_w, col_h, col_y0, span = 4, size * 0.06, size * 0.34, cy - size * 0.27, size * 0.58
    for i in range(n_col):
        x = cx - span / 2 + i * (span / (n_col - 1))
        ax.add_patch(Rectangle((x - col_w / 2, col_y0), col_w, col_h,
                                facecolor=color, edgecolor="none", zorder=zorder))


def draw_globe_glyph(ax, center, size, color="#FFFFFF", zorder=6):
    """An outlined circle with a horizontal and vertical meridian ellipse —
    globe / abroad glyph."""
    cx, cy = center
    r, lw = size * 0.34, max(size * 0.10, 1.4)
    ax.add_patch(Circle((cx, cy), r, facecolor="none", edgecolor=color, linewidth=lw, zorder=zorder))
    ax.add_patch(Ellipse((cx, cy), width=2 * r, height=1.1 * r, facecolor="none",
                          edgecolor=color, linewidth=lw * 0.8, zorder=zorder))
    ax.add_patch(Ellipse((cx, cy), width=1.1 * r, height=2 * r, facecolor="none",
                          edgecolor=color, linewidth=lw * 0.8, zorder=zorder))


def draw_leaf_glyph(ax, center, size, color="#FFFFFF", zorder=6, angle_deg=35):
    """A leaf silhouette: a wide almond (two 3-point bezier curves), tilted
    (default 35°) the way a leaf icon conventionally sits — an earlier
    narrower, unrotated version read as a flame/droplet instead."""
    import math
    cx, cy = center
    w, h = size * 0.50, size * 0.62
    raw = [
        (0, -h / 2),
        (w / 2, -h / 2 * 0.15), (0, h / 2),
        (-w / 2, -h / 2 * 0.15), (0, -h / 2),
    ]
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    verts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in raw]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]
    ax.add_patch(PathPatch(Path(verts, codes), facecolor=color, edgecolor="none", zorder=zorder))


def draw_cloud_glyph(ax, center, size, color="#FFFFFF", zorder=6):
    """A flat cloud puff (base ellipse + three overlapping circles) —
    emissions/waste glyph."""
    cx, cy = center
    base_y = cy - size * 0.08
    ax.add_patch(Ellipse((cx, base_y), width=size * 0.62, height=size * 0.24,
                          facecolor=color, edgecolor="none", zorder=zorder))
    r = size * 0.16
    for dx, dy, rr in [(-size * 0.16, size * 0.06, r * 0.9), (0, size * 0.14, r * 1.15),
                        (size * 0.17, size * 0.05, r * 0.85)]:
        ax.add_patch(Circle((cx + dx, base_y + dy), rr, facecolor=color, edgecolor="none", zorder=zorder))


# ── external SVG icons (e.g. downloaded Noun Project files) ─────────────────
# Preferred over the hand-drawn glyphs above whenever Christoph has supplied
# a source icon file — see SKILL.md "Sourcing icons from Noun Project".
# Requires `svgelements` (pip install svgelements), unlike the rest of this
# module which only needs matplotlib/numpy — not vendored, install once.

def draw_svg_icon(ax, center, size, svg_path, *, color="#FFFFFF", zorder=6):
    """Draws an external SVG icon as real vector paths (not a rasterized
    image) — parsed with svgelements, then converted to matplotlib
    PathPatch objects so the result stays a genuine editable path in the
    .ai/.svg output, matching the flat single-color style of this skill's
    hand-drawn glyphs. The source file's own fill/stroke colors are
    ignored; every subpath is painted `color`. Scaled (preserving aspect)
    and centered so its bounding box fits a `size`-wide/tall box at
    `center`, the same convention as draw_people_glyph() etc.

    Known limitation: icons whose shape depends on an even-odd fill rule
    (a ring, a letter with a counter/hole) may render with the hole filled
    solid — matplotlib's default winding rule doesn't always match SVG's.
    Check the PNG; if a hole is wrong, that icon needs `fill_rule="evenodd"`
    handling this function doesn't yet do.

    Does NOT handle attribution — call record_icon_credit() separately for
    every Noun Project icon used (free-tier icons require a visible credit).
    """
    from svgelements import SVG, Shape, Path as SVGPath

    svg = SVG.parse(svg_path)
    # Match any drawable shape, not just literal <path> elements — icons
    # commonly mix in <rect>/<circle>/<ellipse>/<polygon>/<polyline> (e.g. a
    # government-building icon's columns as <rect>s). SVGPath(shape) below
    # converts any of them to path segments uniformly, with each element's
    # own (and any ancestor <g>'s) transform already applied by svgelements.
    paths = [e for e in svg.elements() if isinstance(e, Shape)]
    if not paths:
        raise ValueError(f"no drawable shapes found in {svg_path}")

    xs, ys = [], []
    for p in paths:
        bbox = p.bbox()
        if bbox:
            x0, y0, x1, y1 = bbox
            xs += [x0, x1]
            ys += [y0, y1]
    if not xs:
        raise ValueError(f"could not compute a bounding box for {svg_path}")
    src_x0, src_x1 = min(xs), max(xs)
    src_y0, src_y1 = min(ys), max(ys)
    src_w, src_h = src_x1 - src_x0, src_y1 - src_y0
    scale = size / max(src_w, src_h) if max(src_w, src_h) else 1.0
    cx, cy = center

    def to_canvas(pt):
        # SVG's y-axis points down; this canvas's points up — flip it.
        x = (pt.x - src_x0 - src_w / 2) * scale
        y = -(pt.y - src_y0 - src_h / 2) * scale
        return (cx + x, cy + y)

    for shape in paths:
        p = shape if isinstance(shape, SVGPath) else SVGPath(shape)
        verts, codes = [], []
        for seg in p:
            name = type(seg).__name__
            if name == "Move":
                verts.append(to_canvas(seg.end)); codes.append(Path.MOVETO)
            elif name == "Line":
                verts.append(to_canvas(seg.end)); codes.append(Path.LINETO)
            elif name == "QuadraticBezier":
                verts.append(to_canvas(seg.control)); codes.append(Path.CURVE3)
                verts.append(to_canvas(seg.end)); codes.append(Path.CURVE3)
            elif name == "CubicBezier":
                verts.append(to_canvas(seg.control1)); codes.append(Path.CURVE4)
                verts.append(to_canvas(seg.control2)); codes.append(Path.CURVE4)
                verts.append(to_canvas(seg.end)); codes.append(Path.CURVE4)
            elif name == "Close":
                verts.append(to_canvas(seg.end)); codes.append(Path.CLOSEPOLY)
            elif name == "Arc":
                for t in (0.2, 0.4, 0.6, 0.8, 1.0):
                    verts.append(to_canvas(seg.point(t))); codes.append(Path.LINETO)
            # unknown segment types are skipped rather than raising, so one
            # odd element doesn't sink the whole icon
        if verts:
            ax.add_patch(PathPatch(Path(verts, codes), facecolor=color, edgecolor="none", zorder=zorder))


def record_icon_credit(out_dir, icon_name, creator, url):
    """Appends one attribution line to CREDITS.md in the figure's output
    folder. Call once per Noun Project icon actually used in that figure —
    free-tier Noun Project icons require a visible credit; this is what
    makes that credit traceable back to the source when the textbook's
    credits/colophon page gets compiled."""
    path = os.path.join(out_dir, "CREDITS.md")
    line = f"- \"{icon_name}\" by {creator}, from the Noun Project — {url}\n"
    header = "# Icon credits\n\nRequired for free-tier Noun Project icons used in this figure.\n\n"
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"credited {icon_name!r} in {path}")


# ── save (three formats from one figure) ─────────────────────────────────────

def save_all(fig, out_dir, out_name, *, transparent=False):
    """Writes <out_name>.ai, .svg, and .png from the same figure.

    .ai is a PDF-compatible file — this is literally what Illustrator's own
    "Create PDF Compatible File" .ai format is, so Illustrator opens and
    fully edits it (paths + live text). TrueType fonts are embedded
    (pdf.fonttype=42) so text stays selectable/editable rather than being
    outlined. What it will NOT carry is Illustrator's own private metadata
    (named layers beyond PDF's own layer support, swatch-library entries) —
    cosmetic, not an editing blocker.

    .svg keeps text as real <text> elements (svg.fonttype='none') for
    portability, version-control diffing, and direct web/Quarto use.

    .png is a flat 300dpi preview for a quick look without opening either.
    """
    ai_path = os.path.join(out_dir, f"{out_name}.ai")
    svg_path = os.path.join(out_dir, f"{out_name}.svg")
    png_path = os.path.join(out_dir, f"{out_name}.png")
    facecolor = "none" if transparent else SURFACE

    matplotlib.rcParams["pdf.fonttype"] = 42
    fig.savefig(ai_path, format="pdf", facecolor=facecolor, transparent=transparent)

    matplotlib.rcParams["svg.fonttype"] = "none"
    fig.savefig(svg_path, format="svg", facecolor=facecolor, transparent=transparent)

    fig.savefig(png_path, format="png", dpi=300, facecolor=facecolor, transparent=transparent)

    for p in (ai_path, svg_path, png_path):
        print(f"saved {p}")
