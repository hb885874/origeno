"""
primitives/prop.py — Prop primitive
=====================================
Renders named icon props (chip, phone, globe, factory, etc.)
built from Manim geometric primitives. No external SVG files needed
for the built-in props — but SVG props are supported if a path is given.

TOML BLOCK
----------
[beats.prop]
name     = "chip"      # see BUILT_IN_PROPS
position = "center"    # center | left | right | top | bottom
scale    = 1.0         # tweak: 1.5 = bigger emphasis
color    = "BLUE"      # override prop colour
svg_path = ""          # path to .svg file (overrides built-in if given)

BUILT-IN PROPS
--------------
chip     — semiconductor chip (square with internal grid lines)
globe    — simplified globe (circle with latitude/longitude lines)
phone    — smartphone outline
factory  — factory silhouette

ADDING NEW BUILT-IN PROPS
--------------------------
Add a function _make_<name>(color) -> VGroup to this file and
register it in BUILT_IN_PROPS dict. No other changes needed.
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("prop")
class Prop(BasePrimitive):

    PARAMS = {
        "name": {
            "type"   : "str",
            "default": "chip",
            "options": ["chip", "globe", "phone", "factory"],
            "hint"   : "Which prop to show.",
            "tweak"  : "Visually anchors the topic of the beat.",
        },
        "position": {
            "type"   : "str",
            "default": "center",
            "options": ["center", "left", "right", "top", "bottom"],
            "hint"   : "Where the prop appears.",
            "tweak"  : "Offset from center to leave room for text.",
        },
        "scale": {
            "type"   : "float",
            "default": 1.0,
            "range"  : (0.3, 3.0),
            "hint"   : "Size multiplier.",
            "tweak"  : "1.5 = dominant visual, 0.5 = supporting detail.",
        },
        "color": {
            "type"   : "str",
            "default": "BLUE",
            "hint"   : "Colour override for the prop.",
            "tweak"  : "Match to the beat's emotional tone.",
        },
    }

    def render(self) -> str:
        name     = self.get("name", "chip")
        position = self.get("position", "center")
        scale    = self.get("scale", 1.0)
        color    = self.color(self.get("color", "BLUE"))
        svg_path = self.get("svg_path", "")

        v = self.var("prop")

        pos_map = {
            "center": "ORIGIN",
            "left"  : "LEFT * 3.5",
            "right" : "RIGHT * 3.5",
            "top"   : "UP * 2",
            "bottom": "DOWN * 2",
        }
        pos = pos_map.get(position, "ORIGIN")

        if svg_path:
            return (
                f"# Prop (SVG): {svg_path}\n"
                f"{v} = SVGMobject('{svg_path}')\n"
                f"{v}.set_color('{color}').scale({scale}).move_to({pos})\n"
                f"self.play(DrawBorderThenFill({v}), run_time=0.8)\n"
                f"all_objects.add({v})\n"
            )

        builder = BUILT_IN_PROPS.get(name, BUILT_IN_PROPS["chip"])
        build_code = builder(v, color, scale, pos)
        return build_code


def _chip_code(v, color, scale, pos) -> str:
    return (
        f"# Prop: chip\n"
        f"{v}_body = Square(side_length=1.2*{scale}, color='{color}',\n"
        f"                   stroke_width=2.5, fill_opacity=0.08,\n"
        f"                   fill_color='{color}')\n"
        f"{v}_body.move_to({pos})\n"
        f"{v}_lines = VGroup()\n"
        f"for _i in range(3):\n"
        f"    _off = (_i - 1) * 0.35 * {scale}\n"
        f"    {v}_lines.add(Line(\n"
        f"        {v}_body.get_left() + RIGHT*0.15*{scale} + UP*_off,\n"
        f"        {v}_body.get_right() - RIGHT*0.15*{scale} + UP*_off,\n"
        f"        color='{color}', stroke_width=1.2, stroke_opacity=0.5\n"
        f"    ))\n"
        f"    {v}_lines.add(Line(\n"
        f"        {v}_body.get_bottom() + UP*0.15*{scale} + RIGHT*_off,\n"
        f"        {v}_body.get_top() - UP*0.15*{scale} + RIGHT*_off,\n"
        f"        color='{color}', stroke_width=1.2, stroke_opacity=0.5\n"
        f"    ))\n"
        f"{v} = VGroup({v}_body, {v}_lines)\n"
        f"self.play(DrawBorderThenFill({v}_body), run_time=0.6)\n"
        f"self.play(Create({v}_lines), run_time=0.5)\n"
        f"all_objects.add({v})\n"
    )


def _globe_code(v, color, scale, pos) -> str:
    return (
        f"# Prop: globe\n"
        f"{v}_outer = Circle(radius=1.0*{scale}, color='{color}',\n"
        f"                    stroke_width=2.5, fill_opacity=0.05)\n"
        f"{v}_outer.move_to({pos})\n"
        f"{v}_lat1 = Ellipse(width=2.0*{scale}, height=0.6*{scale},\n"
        f"                    color='{color}', stroke_width=1, stroke_opacity=0.5)\n"
        f"{v}_lat1.move_to({pos})\n"
        f"{v}_lat2 = Ellipse(width=2.0*{scale}, height=1.2*{scale},\n"
        f"                    color='{color}', stroke_width=1, stroke_opacity=0.3)\n"
        f"{v}_lat2.move_to({pos})\n"
        f"{v}_merid = Line({pos} + UP*{scale}, {pos} + DOWN*{scale},\n"
        f"                  color='{color}', stroke_width=1, stroke_opacity=0.5)\n"
        f"{v} = VGroup({v}_outer, {v}_lat1, {v}_lat2, {v}_merid)\n"
        f"self.play(Create({v}), run_time=0.8)\n"
        f"all_objects.add({v})\n"
    )


def _phone_code(v, color, scale, pos) -> str:
    return (
        f"# Prop: phone\n"
        f"{v}_body = RoundedRectangle(corner_radius=0.2*{scale},\n"
        f"                             width=0.8*{scale}, height=1.5*{scale},\n"
        f"                             color='{color}', stroke_width=2.5,\n"
        f"                             fill_opacity=0.05)\n"
        f"{v}_body.move_to({pos})\n"
        f"{v}_screen = Rectangle(width=0.65*{scale}, height=1.1*{scale},\n"
        f"                        color='{color}', stroke_width=1,\n"
        f"                        stroke_opacity=0.4, fill_opacity=0.0)\n"
        f"{v}_screen.move_to({pos})\n"
        f"{v} = VGroup({v}_body, {v}_screen)\n"
        f"self.play(DrawBorderThenFill({v}), run_time=0.6)\n"
        f"all_objects.add({v})\n"
    )


def _factory_code(v, color, scale, pos) -> str:
    return (
        f"# Prop: factory\n"
        f"{v}_base = Rectangle(width=2.0*{scale}, height=1.0*{scale},\n"
        f"                      color='{color}', stroke_width=2,\n"
        f"                      fill_opacity=0.08, fill_color='{color}')\n"
        f"{v}_base.move_to({pos})\n"
        f"{v}_ch1 = Rectangle(width=0.25*{scale}, height=0.6*{scale},\n"
        f"                     color='{color}', stroke_width=2, fill_opacity=0.1)\n"
        f"{v}_ch1.next_to({v}_base, UP, buff=0).shift(LEFT*0.5*{scale})\n"
        f"{v}_ch2 = Rectangle(width=0.25*{scale}, height=0.8*{scale},\n"
        f"                     color='{color}', stroke_width=2, fill_opacity=0.1)\n"
        f"{v}_ch2.next_to({v}_base, UP, buff=0)\n"
        f"{v}_ch3 = Rectangle(width=0.25*{scale}, height=0.5*{scale},\n"
        f"                     color='{color}', stroke_width=2, fill_opacity=0.1)\n"
        f"{v}_ch3.next_to({v}_base, UP, buff=0).shift(RIGHT*0.5*{scale})\n"
        f"{v} = VGroup({v}_base, {v}_ch1, {v}_ch2, {v}_ch3)\n"
        f"self.play(DrawBorderThenFill({v}), run_time=0.8)\n"
        f"all_objects.add({v})\n"
    )


BUILT_IN_PROPS = {
    "chip"   : _chip_code,
    "globe"  : _globe_code,
    "phone"  : _phone_code,
    "factory": _factory_code,
}
