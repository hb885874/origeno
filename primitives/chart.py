"""
primitives/chart.py — Chart primitive
======================================
Renders bar charts or pie charts from data defined in the TOML.

TOML BLOCK — bar chart
-----------------------
[beats.chart]
type         = "bar"
grow_time    = 1.8        # tweak: slower = more suspense per bar
position     = "right"    # center | left | right
color_scheme = "default"  # default | mono | highlight_first

[[beats.chart.data]]
label = "USA"
value = 45

[[beats.chart.data]]
label = "China"
value = 28

TOML BLOCK — pie chart
-----------------------
[beats.chart]
type         = "pie"
grow_time    = 1.8
position     = "right"
color_scheme = "default"

[[beats.chart.data]]
label = "Taiwan"
value = 92

[[beats.chart.data]]
label = "Others"
value = 8

COLOR SCHEMES
-------------
default         — cycles through palette: RED, BLUE, GOLD, GREEN
mono            — all bars same colour (C_GRID)
highlight_first — first bar RED, rest C_GRID (emphasises the lead value)
"""

from primitives.base import BasePrimitive
from core.registry import register


_COLOR_CYCLES = {
    "default"        : ["C_RED", "C_BLUE", "C_GOLD", "C_GREEN", "C_DIM"],
    "mono"           : ["C_GRID"] * 10,
    "highlight_first": ["C_RED"] + ["C_GRID"] * 9,
}


@register("chart")
class Chart(BasePrimitive):

    PARAMS = {
        "type": {
            "type": "str", "default": "bar",
            "options": ["bar", "pie"],
            "hint": "Chart type.",
            "tweak": "bar = comparison, pie = composition/share.",
        },
        "grow_time": {
            "type": "float", "default": 1.8, "range": (0.5, 5.0),
            "hint": "Duration for bars/slices to grow in.",
            "tweak": "Slower = more suspense per element. 2.5+ = very dramatic.",
        },
        "position": {
            "type": "str", "default": "center",
            "options": ["center", "left", "right"],
            "hint": "Where on screen the chart appears.",
            "tweak": "right = leaves room for character on left.",
        },
        "color_scheme": {
            "type": "str", "default": "default",
            "options": ["default", "mono", "highlight_first"],
            "hint": "Colour assignment for bars/slices.",
            "tweak": "highlight_first = draw eye to the biggest/first value.",
        },
    }

    def render(self) -> str:
        chart_type   = self.get("type", "bar")
        grow_time    = self.get("grow_time", 1.8)
        position     = self.get("position", "center")
        color_scheme = self.get("color_scheme", "default")
        data         = self.cfg.get("data", [])

        if chart_type == "bar":
            return self._bar(data, grow_time, position, color_scheme)
        elif chart_type == "pie":
            return self._pie(data, grow_time, position, color_scheme)
        else:
            return f'# Chart: unknown type "{chart_type}" — skipped\n'

    def _bar(self, data, grow_time, position, scheme) -> str:
        if not data:
            return "# Chart (bar): no data provided — skipped\n"

        v = self.var("chart")
        colors = _COLOR_CYCLES.get(scheme, _COLOR_CYCLES["default"])

        pos_map = {
            "center": "ORIGIN",
            "left"  : "LEFT * 3",
            "right" : "RIGHT * 3",
        }
        pos = pos_map.get(position, "ORIGIN")

        max_val = max(d["value"] for d in data)
        bar_w = min(1.0, 5.0 / max(len(data), 1))
        gap   = bar_w * 0.3

        lines = [
            f"# Chart (bar): {len(data)} bars",
            f"{v}_bars = VGroup()",
            f"{v}_labels = VGroup()",
        ]

        for i, item in enumerate(data):
            label = item.get("label", f"Item {i+1}").replace('"', '\\"')
            val   = item["value"]
            h     = (val / max_val) * 3.0
            color = colors[i % len(colors)]
            x_off = (i - (len(data)-1)/2) * (bar_w + gap)

            lines += [
                f"# Bar {i+1}: {label} = {val}",
                f"{v}_bar{i} = Rectangle(width={bar_w:.2f}, height=0.001,",
                f"    fill_color={color}, fill_opacity=1, stroke_width=0)",
                f"{v}_bar{i}.move_to({pos} + RIGHT*{x_off:.2f} + DOWN*1.5)",
                f"{v}_lbl{i} = Text('{label}', font=FONT, font_size=14, color=C_DIM)",
                f"{v}_lbl{i}.next_to({v}_bar{i}, DOWN, buff=0.12)",
                f"{v}_bars.add({v}_bar{i})",
                f"{v}_labels.add({v}_lbl{i})",
            ]

        lines += [
            f"self.play(FadeIn({v}_labels), run_time=0.4)",
        ]

        for i, item in enumerate(data):
            val = item["value"]
            h   = (val / max_val) * 3.0
            x_off = (i - (len(data)-1)/2) * (bar_w + gap)
            lines += [
                f"self.play(",
                f"    {v}_bar{i}.animate.stretch_to_fit_height({h:.3f})",
                f"        .move_to({pos} + RIGHT*{x_off:.2f} + DOWN*(1.5 - {h:.3f}/2)),",
                f"    run_time={grow_time / max(len(data), 1):.2f}, rate_func=smooth",
                f")",
            ]

        lines.append(f"all_objects.add({v}_bars, {v}_labels)")

        return "\n".join(lines) + "\n"

    def _pie(self, data, grow_time, position, scheme) -> str:
        if not data:
            return "# Chart (pie): no data provided — skipped\n"

        v = self.var("chart")
        colors = _COLOR_CYCLES.get(scheme, _COLOR_CYCLES["default"])

        pos_map = {
            "center": "ORIGIN",
            "left"  : "LEFT * 3",
            "right" : "RIGHT * 3",
        }
        pos = pos_map.get(position, "ORIGIN")

        total = sum(d["value"] for d in data)
        radius = 1.8

        lines = [
            f"# Chart (pie): {len(data)} slices  total={total}",
            f"{v}_pie = VGroup()",
            f"{v}_start_angle = TAU / 4   # start at 12 o'clock",
        ]

        for i, item in enumerate(data):
            label  = item.get("label", f"Slice {i+1}").replace('"', '\\"')
            val    = item["value"]
            angle  = f"TAU * {val}/{total}"
            color  = colors[i % len(colors)]
            pct    = f"{val/total*100:.0f}%"

            lines += [
                f"# Slice {i+1}: {label} = {val} ({pct})",
                f"{v}_s{i} = AnnularSector(",
                f"    inner_radius=0, outer_radius={radius},",
                f"    angle={angle}, start_angle={v}_start_angle,",
                f"    fill_color={color}, fill_opacity=1, stroke_width=1.5,",
                f"    stroke_color=C_BG",
                f")",
                f"{v}_s{i}.move_to({pos})",
                f"{v}_start_angle += {angle}",
                f"{v}_pie.add({v}_s{i})",
            ]

        lines += [
            f"self.play(",
            f"    LaggedStart(",
            f"        *[GrowFromCenter(s) for s in {v}_pie],",
            f"        lag_ratio=0.15",
            f"    ),",
            f"    run_time={grow_time}, rate_func=smooth",
            f")",
            f"all_objects.add({v}_pie)",
        ]

        return "\n".join(lines) + "\n"
