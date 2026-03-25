"""
primitives/map.py — Map primitive
===================================
Renders a world dot-map with optional country highlights and
trade-route arcs. Built entirely from Manim dot grids — no external
map image files required.

TOML BLOCK
----------
[beats.map]
type      = "world-dots"   # world-dots (only type currently)
highlight = "Taiwan"       # country name to highlight (see KNOWN_REGIONS)
arc_from  = "USA"          # draw arc FROM this region  (optional)
arc_to    = "Taiwan"       # draw arc TO this region    (optional)
dot_color = "GRID"         # base dot colour
highlight_color = "RED"    # colour for highlighted region
arc_color = "GOLD"         # colour for arc line

KNOWN REGIONS (highlight / arc_from / arc_to)
----------------------------------------------
Approximate screen-space positions used for dots and arc endpoints.
Extend KNOWN_REGIONS dict to add more regions.

SCALING NOTE
------------
The dot-map is a simplified schematic, not a geographically accurate
projection. Positions are chosen to be visually recognisable on a
14.2 × 8.0 Manim frame.
"""

from primitives.base import BasePrimitive
from core.registry import register


# Approximate [x, y] positions in Manim frame coordinates
# Frame: x ∈ [−7.1, +7.1], y ∈ [−4.0, +4.0]
KNOWN_REGIONS: dict[str, tuple[float, float]] = {
    "USA"          : (-5.2,  0.5),
    "Canada"       : (-5.0,  1.8),
    "Mexico"       : (-4.8, -0.5),
    "Brazil"       : (-3.0, -1.8),
    "UK"           : (-0.5,  1.6),
    "France"       : (-0.2,  1.2),
    "Germany"      : ( 0.2,  1.5),
    "Russia"       : ( 2.8,  2.2),
    "China"        : ( 4.2,  1.0),
    "India"        : ( 3.4, -0.2),
    "Japan"        : ( 5.2,  1.2),
    "Taiwan"       : ( 4.8,  0.6),
    "South Korea"  : ( 5.0,  1.0),
    "Australia"    : ( 5.0, -2.5),
    "South Africa" : ( 1.2, -2.8),
    "Egypt"        : ( 1.0,  0.2),
    "Saudi Arabia" : ( 2.0, -0.2),
}


@register("map")
class Map(BasePrimitive):

    PARAMS = {
        "type": {
            "type"   : "str",
            "default": "world-dots",
            "options": ["world-dots"],
            "hint"   : "Map style. Only world-dots currently.",
            "tweak"  : "Future: satellite | outline | regions.",
        },
        "highlight": {
            "type"   : "str",
            "default": None,
            "hint"   : "Region name to highlight (see KNOWN_REGIONS in map.py).",
            "tweak"  : "Draws a glowing circle over the region.",
        },
        "arc_from": {
            "type"   : "str",
            "default": None,
            "hint"   : "Start region for trade-route arc.",
            "tweak"  : "Combined with arc_to draws a curved arrow between regions.",
        },
        "arc_to": {
            "type"   : "str",
            "default": None,
            "hint"   : "End region for trade-route arc.",
            "tweak"  : "Arrow direction: arc_from → arc_to.",
        },
        "dot_color": {
            "type"   : "str",
            "default": "GRID",
            "hint"   : "Base colour for all map dots.",
            "tweak"  : "Darker = map recedes, lighter = map dominates.",
        },
        "highlight_color": {
            "type"   : "str",
            "default": "RED",
            "hint"   : "Colour for the highlighted region marker.",
            "tweak"  : "RED = danger/focus, GOLD = opportunity.",
        },
        "arc_color": {
            "type"   : "str",
            "default": "GOLD",
            "hint"   : "Colour of the trade-route arc.",
            "tweak"  : "GOLD = trade/flow, RED = tension.",
        },
    }

    def render(self) -> str:
        highlight       = self.get("highlight")
        arc_from        = self.get("arc_from")
        arc_to          = self.get("arc_to")
        dot_color       = self.color(self.get("dot_color", "GRID"))
        highlight_color = self.color(self.get("highlight_color", "RED"))
        arc_color       = self.color(self.get("arc_color", "GOLD"))

        v = self.var("map")

        lines = [
            f"# Map: world-dots",
            f"# Build dot grid (simplified world map schematic)",
            f"{v}_dots = VGroup()",
            f"_map_data = [",
        ]

        # Generate a coarse dot grid representing world landmasses
        # This is a schematic, not a projection
        dots = _world_dot_positions()
        for x, y in dots:
            lines.append(f"    ({x:.1f}, {y:.1f}),")

        lines += [
            f"]",
            f"for _mx, _my in _map_data:",
            f"    _d = Dot(point=[_mx, _my, 0], radius=0.04,",
            f"             color='{dot_color}', fill_opacity=0.6)",
            f"    {v}_dots.add(_d)",
            f"",
            f"self.play(",
            f"    LaggedStart(*[FadeIn(d, scale=0.1) for d in {v}_dots],",
            f"                lag_ratio=0.002),",
            f"    run_time=1.4",
            f")",
            f"all_objects.add({v}_dots)",
        ]

        # Highlight
        if highlight and highlight in KNOWN_REGIONS:
            hx, hy = KNOWN_REGIONS[highlight]
            lines += [
                f"",
                f"# Highlight: {highlight}",
                f"{v}_hl = Circle(radius=0.35, color='{highlight_color}',",
                f"               stroke_width=2.5, fill_opacity=0.2,",
                f"               fill_color='{highlight_color}')",
                f"{v}_hl.move_to([{hx}, {hy}, 0])",
                f"self.play(Create({v}_hl), run_time=0.6)",
                f"ripple(self, [{hx}, {hy}, 0], color='{highlight_color}',",
                f"       n=2, base_r=0.3, run_t=0.5)",
                f"all_objects.add({v}_hl)",
            ]

        # Arc
        if arc_from and arc_to:
            if arc_from in KNOWN_REGIONS and arc_to in KNOWN_REGIONS:
                fx, fy = KNOWN_REGIONS[arc_from]
                tx, ty = KNOWN_REGIONS[arc_to]
                lines += [
                    f"",
                    f"# Trade arc: {arc_from} → {arc_to}",
                    f"{v}_arc = ArcBetweenPoints(",
                    f"    start=[{fx}, {fy}, 0],",
                    f"    end=[{tx}, {ty}, 0],",
                    f"    angle=TAU/6,",
                    f"    color='{arc_color}',",
                    f"    stroke_width=2.0",
                    f")",
                    f"self.play(Create({v}_arc), run_time=1.0)",
                    f"all_objects.add({v}_arc)",
                ]
            else:
                missing = [r for r in [arc_from, arc_to] if r not in KNOWN_REGIONS]
                lines.append(
                    f"# WARNING: arc region(s) not in KNOWN_REGIONS: {missing}"
                    f" — add to primitives/map.py KNOWN_REGIONS dict"
                )

        return "\n".join(lines) + "\n"


def _world_dot_positions() -> list[tuple[float, float]]:
    """
    Returns a coarse list of (x, y) positions representing world landmasses
    as a schematic dot grid. Not geographically accurate — designed to be
    visually recognisable on a 14.2 × 8.0 Manim frame.

    To improve the map: replace this list with a proper Robinson-projection
    coastline dataset sampled to ~300 points.
    """
    import math
    # Generate a rough grid and keep points that are "land"
    # This is a very simplified approximation
    points = []

    # North America
    for x in [-6.5, -6.0, -5.5, -5.0, -4.5, -4.0]:
        for y in [-0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]:
            points.append((x + (y * 0.05), y))

    # South America
    for x in [-4.5, -4.0, -3.5, -3.0]:
        for y in [-2.5, -2.0, -1.5, -1.0, -0.5]:
            points.append((x, y))

    # Europe
    for x in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        for y in [0.8, 1.2, 1.6, 2.0]:
            points.append((x, y))

    # Africa
    for x in [-0.5, 0.0, 0.5, 1.0, 1.5]:
        for y in [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5]:
            points.append((x, y))

    # Asia
    for x in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
        for y in [-0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]:
            points.append((x + (y * 0.03), y))

    # Australia
    for x in [4.5, 5.0, 5.5]:
        for y in [-2.5, -2.0]:
            points.append((x, y))

    return points
