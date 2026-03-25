"""
primitives/counter.py — Counter primitive
==========================================
Animates a number counting up (or down) from start to end.
Classic "92%", "3.2 Billion" style data reveals.

TOML BLOCK
----------
[beats.counter]
start    = 0
end      = 92
label    = "%"        # appended after the number
duration = 2.5        # tweak: how long the count takes
color    = "RED"
position = "center"   # center | top | bottom | left | right
font_size = 88        # tweak: bigger = more emphasis
prefix   = ""         # optional prefix e.g. "$"
decimals = 0          # decimal places shown during count
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("counter")
class Counter(BasePrimitive):

    PARAMS = {
        "start": {
            "type": "float", "default": 0,
            "hint": "Starting value of the counter.",
            "tweak": "Start above 0 to imply 'already high' before reveal.",
        },
        "end": {
            "type": "float", "default": 100,
            "hint": "Final value displayed.",
            "tweak": "This is the number the viewer remembers.",
        },
        "label": {
            "type": "str", "default": "",
            "hint": "Text appended after the number (e.g. '%', 'B', 'x').",
            "tweak": "Unit that gives the number meaning.",
        },
        "prefix": {
            "type": "str", "default": "",
            "hint": "Text prepended before the number (e.g. '$', '~').",
            "tweak": "Use '~' for approximate, '$' for money.",
        },
        "duration": {
            "type": "float", "default": 2.5, "range": (0.5, 8.0),
            "hint": "How long the count animation takes.",
            "tweak": "Slower = more suspense. Faster = energetic.",
        },
        "color": {
            "type": "str", "default": "RED",
            "hint": "Colour of the number.",
            "tweak": "RED = danger/impact, GOLD = impressive, BLUE = informational.",
        },
        "position": {
            "type": "str", "default": "center",
            "options": ["center", "top", "bottom", "left", "right"],
            "hint": "Where on screen the counter appears.",
            "tweak": "center = hero number, top = subtitle style.",
        },
        "font_size": {
            "type": "int", "default": 88, "range": (32, 200),
            "hint": "Size of the number text.",
            "tweak": "Larger = the number is THE message.",
        },
        "decimals": {
            "type": "int", "default": 0, "range": (0, 4),
            "hint": "Decimal places shown during animation.",
            "tweak": "0 = integers only, 1-2 = precise data feel.",
        },
    }

    def render(self) -> str:
        start     = self.get("start", 0)
        end       = self.get("end", 100)
        label     = self.get("label", "").replace('"', '\\"')
        prefix    = self.get("prefix", "").replace('"', '\\"')
        duration  = self.get("duration", 2.5)
        color     = self.color(self.get("color", "RED"))
        position  = self.get("position", "center")
        font_size = self.get("font_size", 88)
        decimals  = self.get("decimals", 0)

        v = self.var("counter")

        pos_map = {
            "center": "ORIGIN",
            "top"   : "UP * 2.5",
            "bottom": "DOWN * 2.5",
            "left"  : "LEFT * 4",
            "right" : "RIGHT * 4",
        }
        pos = pos_map.get(position, "ORIGIN")

        return f"""# Counter: {start} → {end}{label}
{v}_tracker = ValueTracker({start})
{v}_num = DecimalNumber(
    {start},
    num_decimal_places={decimals},
    color="{color}",
    font_size={font_size},
).move_to({pos})

def {v}_updater(mob):
    val = {v}_tracker.get_value()
    mob.set_value(val)
    # Rebuild label alongside number
    mob.move_to({pos})

{v}_num.add_updater({v}_updater)

{v}_label = Text("{label}", font=FONT, color="{color}", font_size={font_size // 2})
{v}_prefix = Text("{prefix}", font=FONT, color="{color}", font_size={font_size // 2})

self.play(
    FadeIn({v}_num),
    run_time=0.3
)
self.play(
    {v}_tracker.animate.set_value({end}),
    run_time={duration},
    rate_func=smooth
)
{v}_num.remove_updater({v}_updater)
all_objects.add({v}_num)
"""
