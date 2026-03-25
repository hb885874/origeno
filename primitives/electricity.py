"""
primitives/electricity.py — Electricity primitive
===================================================
Animates a travelling dot along a path to simulate electric current,
data flow, or signal propagation. Used for chip circuit traces and
network data movement.

TOML BLOCK
----------
[beats.electricity]
mode      = "chip-traces"  # chip-traces | path
color     = "CYAN"
run_time  = 1.5            # tweak: speed of the travelling dot
path_from = "left"         # for mode=path: start side
path_to   = "right"        # for mode=path: end side

MODES
-----
chip-traces  — radiating lines from center, dot travels outward
path         — single dot travels from path_from to path_to
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("electricity")
class Electricity(BasePrimitive):

    PARAMS = {
        "mode": {
            "type"   : "str",
            "default": "chip-traces",
            "options": ["chip-traces", "path"],
            "hint"   : "Animation style.",
            "tweak"  : "chip-traces = radiating from center, path = A→B travel.",
        },
        "color": {
            "type"   : "str",
            "default": "CYAN",
            "hint"   : "Colour of the travelling dot and traces.",
            "tweak"  : "CYAN = data/electric, GOLD = energy/power.",
        },
        "run_time": {
            "type"   : "float",
            "default": 1.5,
            "range"  : (0.3, 4.0),
            "hint"   : "Duration of the travel animation.",
            "tweak"  : "Faster = urgent signal, slower = deliberate flow.",
        },
    }

    def render(self) -> str:
        mode     = self.get("mode", "chip-traces")
        color    = self.color(self.get("color", "CYAN"))
        run_time = self.get("run_time", 1.5)

        v = self.var("elec")

        if mode == "chip-traces":
            return f"""# Electricity: chip-traces
{v}_traces = VGroup()
_trace_dirs = [RIGHT, LEFT, UP, DOWN, UR, UL, DR, DL]
for _td in _trace_dirs:
    _tline = Line(ORIGIN, _td * 2.5, color='{color}',
                  stroke_width=1.2, stroke_opacity=0.4)
    {v}_traces.add(_tline)
self.play(
    LaggedStart(*[Create(t) for t in {v}_traces], lag_ratio=0.1),
    run_time={run_time}
)
{v}_dot = Dot(color='{color}', radius=0.12)
{v}_dot.move_to(ORIGIN)
self.play(
    {v}_dot.animate.shift(RIGHT * 2.5),
    run_time={run_time * 0.5},
    rate_func=linear
)
self.remove({v}_dot)
all_objects.add({v}_traces)
"""
        else:  # path
            path_from = self.get("path_from", "left")
            path_to   = self.get("path_to", "right")
            start = "LEFT * 6.5" if path_from == "left" else "RIGHT * 6.5"
            end   = "RIGHT * 6.5" if path_to == "right" else "LEFT * 6.5"
            return f"""# Electricity: path {path_from} → {path_to}
{v}_line = Line({start}, {end}, color='{color}',
                stroke_width=1.5, stroke_opacity=0.4,
                stroke_dash_array=[5, 5])
self.play(Create({v}_line), run_time=0.5)
{v}_dot = Dot(color='{color}', radius=0.14)
{v}_dot.move_to({start})
self.play(
    {v}_dot.animate.move_to({end}),
    run_time={run_time},
    rate_func=linear
)
self.remove({v}_dot)
all_objects.add({v}_line)
"""