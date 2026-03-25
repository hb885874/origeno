"""
primitives/glitch.py — Glitch primitive
=========================================
Applies a rapid scale+colour flash to an on-screen object to simulate
a glitch/error/corrupted-data effect. Best used on text or props that
were added in a previous beat (transition = "keep").

TOML BLOCK
----------
[beats.glitch]
target   = "title"    # descriptive — used only in comment, no auto-lookup
duration = 0.4        # tweak: shorter = more violent glitch
repeats  = 3          # tweak: more = more chaotic
color    = "RED"      # flash colour

NOTE ON TARGET
--------------
The glitch primitive does not auto-look up the target object by name.
Instead it generates a comment `# glitch target: <target>` and wraps
the most recently added object (last item in all_objects) in the effect.
For precise control, the scene.py can be manually adjusted after generation
— but since scene.py is machine-generated, the better approach is to
always use glitch on the LAST object added in the current beat.
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("glitch")
class Glitch(BasePrimitive):

    PARAMS = {
        "target": {
            "type"   : "str",
            "default": "last_object",
            "hint"   : "Descriptive name of what glitches (for readability).",
            "tweak"  : "Applied to the last object added to all_objects.",
        },
        "duration": {
            "type"   : "float",
            "default": 0.4,
            "range"  : (0.1, 1.5),
            "hint"   : "Total glitch effect duration.",
            "tweak"  : "0.15 = instant violent glitch, 0.8 = slow degradation.",
        },
        "repeats": {
            "type"   : "int",
            "default": 3,
            "range"  : (1, 10),
            "hint"   : "How many flash cycles.",
            "tweak"  : "1 = single jolt, 5+ = full corruption.",
        },
        "color": {
            "type"   : "str",
            "default": "RED",
            "hint"   : "Flash colour.",
            "tweak"  : "RED = error, CYAN = digital corruption.",
        },
    }

    def render(self) -> str:
        target   = self.get("target", "last_object")
        duration = self.get("duration", 0.4)
        repeats  = self.get("repeats", 3)
        color    = self.color(self.get("color", "RED"))

        v        = self.var("glitch")
        step_t   = duration / max(repeats * 2, 1)

        return f"""# Glitch: {target}
# Applied to last object in all_objects
{v}_target = all_objects[-1] if len(all_objects) > 0 else VGroup()
for _gi in range({repeats}):
    self.play(
        {v}_target.animate.scale(1.06).set_color('{color}'),
        run_time={step_t:.3f}
    )
    self.play(
        {v}_target.animate.scale(1/1.06).set_color(C_WHITE),
        run_time={step_t:.3f}
    )
# Restore original colour after glitch
self.play(
    {v}_target.animate.set_color(C_WHITE),
    run_time=0.1
)
"""
