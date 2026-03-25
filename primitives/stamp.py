"""
primitives/stamp.py — Stamp primitive
======================================
Renders a bold text label that slams onto screen from a direction.
Classic "ZERO CHIPS", "SUBSCRIBE", "NOW" style overlays.

MANIM CE COMPATIBILITY NOTE (v0.20.1+)
---------------------------------------
- rate_func must be passed to self.play(), NOT inside .animate()
- 'bounce' does not exist in Manim CE — use 'there_and_back' or 'wiggle'
- The slam effect uses FadeIn with shift for the entry, then a scale
  pulse to simulate impact weight

TOML BLOCK
----------
[beats.stamp]
text         = "ZERO CHIPS"
color        = "RED"          # palette key or hex
from_dir     = "TOP"          # TOP | BOTTOM | LEFT | RIGHT | CENTER
run_time     = 0.6            # tweak: 0.3=snappy  1.2=slow dramatic
bounce_count = 3              # tweak: 1=subtle  3=medium  5+=very bouncy
font_size    = 52             # tweak: larger = more emphasis
position     = "center"       # center | top | bottom | left | right
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("stamp")
class Stamp(BasePrimitive):

    PARAMS = {
        "text": {
            "type": "str", "default": "TEXT",
            "hint": "The text displayed on screen.",
            "tweak": "Change the message.",
        },
        "color": {
            "type": "str", "default": "RED",
            "options": ["RED", "BLUE", "GOLD", "GREEN", "WHITE"],
            "hint": "Palette key or hex colour for the text.",
            "tweak": "RED = alert/danger, GOLD = highlight, BLUE = info.",
        },
        "from_dir": {
            "type": "str", "default": "TOP",
            "options": ["TOP", "BOTTOM", "LEFT", "RIGHT", "CENTER"],
            "hint": "Direction the stamp flies in from.",
            "tweak": "TOP feels dramatic, CENTER feels like a reveal.",
        },
        "run_time": {
            "type": "float", "default": 0.6, "range": (0.1, 2.0),
            "hint": "Duration of the fly-in animation.",
            "tweak": "0.3 = snappy/urgent  1.0 = slow dramatic  0.6 = balanced",
        },
        "bounce_count": {
            "type": "int", "default": 3, "range": (0, 5),
            "hint": "Number of scale pulses after landing (impact feel).",
            "tweak": "0 = clean stop  2 = subtle impact  4 = heavy slam",
        },
        "font_size": {
            "type": "int", "default": 52, "range": (24, 120),
            "hint": "Text size in points.",
            "tweak": "Larger = more visual dominance.",
        },
        "position": {
            "type": "str", "default": "center",
            "options": ["center", "top", "bottom", "left", "right"],
            "hint": "Where on screen the stamp lands.",
            "tweak": "center = focus  top = title position.",
        },
    }

    def render(self) -> str:
        text         = self.get("text", "TEXT").replace('"', '\\"')
        color        = self.color(self.get("color", "RED"))
        from_dir     = self.get("from_dir", "TOP").upper()
        run_time     = self.get("run_time", 0.6)
        bounce_count = self.get("bounce_count", 3)
        font_size    = self.get("font_size", 52)
        position     = self.get("position", "center")

        v = self.var("stamp")

        # Fly-in shift direction (opposite of from_dir = comes FROM that side)
        shift_map = {
            "TOP"   : "DOWN * 0",   # FadeIn with shift UP means comes from above
            "BOTTOM": "UP * 0",
            "LEFT"  : "RIGHT * 0",
            "RIGHT" : "LEFT * 0",
            "CENTER": "UP * 0",
        }
        # shift for FadeIn: the shift direction is where it COMES FROM
        fadein_shift_map = {
            "TOP"   : "UP * 4",
            "BOTTOM": "DOWN * 4",
            "LEFT"  : "LEFT * 8",
            "RIGHT" : "RIGHT * 8",
            "CENTER": "UP * 0",
        }
        fadein_shift = fadein_shift_map.get(from_dir, "UP * 4")

        # Landing position
        pos_map = {
            "center": "ORIGIN",
            "top"   : "UP * 2.5",
            "bottom": "DOWN * 2.5",
            "left"  : "LEFT * 3.5",
            "right" : "RIGHT * 3.5",
        }
        land_pos = pos_map.get(position, "ORIGIN")

        # Build bounce pulses as separate play() calls
        # Each pulse: scale up slightly then back — simulates impact weight
        bounce_lines = ""
        if bounce_count > 0:
            scale_up   = 1.0 + (0.06 * min(bounce_count, 5))
            scale_down = round(1.0 / scale_up, 4)
            pulse_time = max(0.06, run_time * 0.15)
            bounce_lines = f"""# Impact bounce pulses
self.play({v}.animate.scale({scale_up:.3f}), run_time={pulse_time:.3f}, rate_func=there_and_back)
"""

        return f"""# Stamp: "{text}"
{v} = Text("{text}", font=FONT, color="{color}",
         font_size={font_size}, weight=BOLD)
{v}.move_to({land_pos})
self.play(
    FadeIn({v}, shift={fadein_shift}),
    run_time={run_time},
    rate_func=rush_from
)
{bounce_lines}all_objects.add({v})
"""