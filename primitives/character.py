"""
primitives/character.py — Character primitive
==============================================
Renders the Origeno scientist stick-figure character and animates
common actions: walking in, pointing at something, holding a prop,
expressing emotions.

The character is built entirely from Manim primitives (no image files
needed) so it works on any machine without asset setup.

TOML BLOCK
----------
[beats.character]
action   = "walks-in"    # see ACTIONS below
position = "right"       # left | center | right
color    = "blue"        # blue | red | any palette key
target   = "map"         # for points-at: what to point at (descriptive)
run_time = 0.8           # tweak: walk/move animation speed

ACTIONS
-------
walks-in       — character enters from off-screen (left or right depending on position)
points-at      — character raises arm pointing (toward target side)
holds-prop     — character holds something (prop name from assets.icons)
shocked        — character jumps back slightly, arms up
wink           — quick scale pulse (comedic beat)
static         — character appears but doesn't animate
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("character")
class Character(BasePrimitive):

    PARAMS = {
        "action": {
            "type"   : "str",
            "default": "walks-in",
            "options": ["walks-in", "points-at", "holds-prop", "shocked", "wink", "static"],
            "hint"   : "What the character does this beat.",
            "tweak"  : "walks-in = intro, points-at = directing attention, shocked = reaction.",
        },
        "position": {
            "type"   : "str",
            "default": "right",
            "options": ["left", "center", "right"],
            "hint"   : "Where on screen the character stands.",
            "tweak"  : "right = leaves left side for text/charts.",
        },
        "color": {
            "type"   : "str",
            "default": "BLUE",
            "hint"   : "Character colour (scientist coat).",
            "tweak"  : "BLUE = neutral/protagonist, RED = antagonist/rival.",
        },
        "run_time": {
            "type"   : "float",
            "default": 0.8,
            "range"  : (0.2, 2.5),
            "hint"   : "Speed of the action animation.",
            "tweak"  : "0.3 = snappy, 1.5 = slow deliberate.",
        },
    }

    def render(self) -> str:
        action   = self.get("action", "walks-in")
        position = self.get("position", "right")
        color    = self.color(self.get("color", "BLUE"))
        run_time = self.get("run_time", 0.8)

        v = self.var("char")

        pos_map = {
            "left"  : "LEFT * 4.5",
            "center": "ORIGIN",
            "right" : "RIGHT * 4.5",
        }
        land_pos = pos_map.get(position, "RIGHT * 4.5")

        # Off-screen start — opposite side from position
        if position == "right":
            start_pos = "RIGHT * 9"
        elif position == "left":
            start_pos = "LEFT * 9"
        else:
            start_pos = "DOWN * 6"

        action_code = self._action_code(v, action, land_pos, run_time, color)

        return f"""# Character: {action} at {position}
def _make_character_{v}(color):
    \"\"\"Stick figure scientist built from Manim primitives.\"\"\"
    head = Circle(radius=0.25, color=color, stroke_width=2.5, fill_opacity=0)
    body = Line(UP*0.25, DOWN*0.6, color=color, stroke_width=2.5)
    l_arm = Line(DOWN*0.1, DOWN*0.3 + LEFT*0.45, color=color, stroke_width=2)
    r_arm = Line(DOWN*0.1, DOWN*0.3 + RIGHT*0.45, color=color, stroke_width=2)
    l_leg = Line(DOWN*0.6, DOWN*1.1 + LEFT*0.3, color=color, stroke_width=2)
    r_leg = Line(DOWN*0.6, DOWN*1.1 + RIGHT*0.3, color=color, stroke_width=2)
    fig = VGroup(head, body, l_arm, r_arm, l_leg, r_leg)
    head.move_to(UP*0.5)
    return fig

{v} = _make_character_{v}("{color}")
{v}.move_to({start_pos})
{action_code}
all_objects.add({v})
"""

    def _action_code(self, v, action, land_pos, run_time, color) -> str:
        if action == "walks-in":
            return (
                f"self.play({v}.animate.move_to({land_pos}),\n"
                f"          run_time={run_time}, rate_func=smooth)"
            )
        elif action == "static":
            return (
                f"{v}.move_to({land_pos})\n"
                f"self.play(FadeIn({v}), run_time=0.4)"
            )
        elif action == "points-at":
            return (
                f"self.play({v}.animate.move_to({land_pos}),\n"
                f"          run_time={run_time}, rate_func=smooth)\n"
                f"# Pointing gesture: right arm extends\n"
                f"self.play(\n"
                f"    {v}[2].animate.put_start_and_end_on(\n"
                f"        {v}[1].get_top() + DOWN*0.1,\n"
                f"        {v}[1].get_top() + DOWN*0.1 + RIGHT*0.9\n"
                f"    ),\n"
                f"    run_time=0.4\n"
                f")"
            )
        elif action == "shocked":
            return (
                f"{v}.move_to({land_pos})\n"
                f"self.play(FadeIn({v}), run_time=0.3)\n"
                f"self.play(\n"
                f"    {v}.animate.shift(LEFT*0.5 + UP*0.2).scale(1.1),\n"
                f"    run_time=0.25\n"
                f")\n"
                f"self.play({v}.animate.scale(1/1.1), run_time=0.2)"
            )
        elif action == "wink":
            return (
                f"{v}.move_to({land_pos})\n"
                f"self.play(FadeIn({v}), run_time=0.3)\n"
                f"self.play({v}.animate.scale(1.15), run_time=0.15)\n"
                f"self.play({v}.animate.scale(1/1.15), run_time=0.15)"
            )
        else:
            return (
                f"{v}.move_to({land_pos})\n"
                f"self.play(FadeIn({v}), run_time=0.5)"
            )
