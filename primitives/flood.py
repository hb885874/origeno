"""
primitives/flood.py — Flood primitive
=======================================
Floods the screen with N copies of an icon/object, appearing in
a LagggedStart wave. Classic "factories everywhere", "phones
everywhere" effect.

TOML BLOCK
----------
[beats.flood]
object      = "chip"     # prop name or short text
count       = 20         # tweak: more = overwhelming feeling
spread_time = 2.0        # tweak: slower = objects accumulate dramatically
color       = "BLUE"
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("flood")
class Flood(BasePrimitive):

    PARAMS = {
        "object": {
            "type": "str", "default": "chip",
            "hint": "What object floods the screen.",
            "tweak": "Match to the beat's topic.",
        },
        "count": {
            "type": "int", "default": 20, "range": (5, 60),
            "hint": "How many copies appear.",
            "tweak": "More = overwhelming, fewer = manageable scale.",
        },
        "spread_time": {
            "type": "float", "default": 2.0, "range": (0.5, 5.0),
            "hint": "Total duration for all objects to appear.",
            "tweak": "Slower = objects accumulate with tension.",
        },
        "color": {
            "type": "str", "default": "BLUE",
            "hint": "Colour of the flood objects.",
        },
    }

    def render(self) -> str:
        obj_name    = self.get("object", "chip")
        count       = self.get("count", 20)
        spread_time = self.get("spread_time", 2.0)
        color       = self.color(self.get("color", "BLUE"))

        v = self.var("flood")

        return f"""# Flood: {count}x {obj_name}
import random as _rand_{v}
_rand_{v}.seed(42)
{v}_group = VGroup()
for _fi in range({count}):
    _fx = _rand_{v}.uniform(-6.5, 6.5)
    _fy = _rand_{v}.uniform(-3.5, 3.5)
    _item = Square(side_length=0.3, color='{color}',
                   stroke_width=1.5, fill_opacity=0.15,
                   fill_color='{color}')
    _item.move_to([_fx, _fy, 0])
    {v}_group.add(_item)
self.play(
    LaggedStart(*[FadeIn(obj, scale=0.2) for obj in {v}_group],
                lag_ratio={spread_time / max(count, 1):.3f}),
    run_time={spread_time}
)
all_objects.add({v}_group)
"""
