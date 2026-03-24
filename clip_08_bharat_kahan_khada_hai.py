"""
clip_08b_india_final.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "India — User ya Builder?"
Scenes: asset_checklist, broken_chain, diverging_paths
Duration: ~90 seconds
RENDER: manim -pqh clip_08b_india_final.py IndiaFinal
"""

from manim import *
import numpy as np, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from brand import *

# ╔══════════════════════════════════════╗
# ║              INPUTS                 ║
# ║  Edit these before each render      ║
# ╚══════════════════════════════════════╝
# Beat 1 — asset checklist
ASSETS_STRONG = [
    ("Talent",    "#1 Globally"),
    ("Startups",  "1000+ AI startups"),
    ("Data",      "1.4B users"),
    ("Market",    "Massive scale"),
]
ASSETS_WEAK = [
    ("GPUs",      "Near zero"),
    ("Chips",     "No fab"),
    ("Compute",   "Imported"),
]

# Beat 2 — broken chain
CHAIN_NODES = [
    {"label": "Research",    "sub": "India",         "color": C_FIN},
    {"label": "Design",      "sub": "India",         "color": C_FIN},
    {"label": "Manufacture", "sub": "???",           "color": C_HOT1},
    {"label": "Deploy",      "sub": "India",         "color": C_DIM},
]

# Beat 3 — diverging paths
PATH_USER    = "User"
PATH_BUILDER = "Builder"
FINAL_Q      = "Kya India sirf AI ka user banega?"
FINAL_Q2     = "Ya future ka builder?"

# Timing
T_TICK_LAG    = 0.22
T_CHAIN_BUILD = 0.7
T_BREAK_HOLD  = 2.5
T_PATH_BUILD  = 1.0
T_FINAL_HOLD  = 3.8
T_OUTRO       = 1.2
# ╚══════════════════════════════════════╝


# ── Helpers ───────────────────────────────────────────────────────────────────

def india_box(color=C_FIN, w=2.2, h=2.8):
    box = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        fill_color=color, fill_opacity=0.08,
        stroke_color=color, stroke_width=1.8
    )
    lbl = Text("India", font="Arial", weight=BOLD,
               font_size=24, color=color, fill_opacity=0.30)
    return VGroup(box, lbl)


def checkmark(color=C_GPT, size=0.22):
    """Green tick — two line segments."""
    p1 = LEFT  * size * 0.4  + DOWN * size * 0.1
    p2 = LEFT  * size * 0.05 + DOWN * size * 0.38
    p3 = RIGHT * size * 0.5  + UP   * size * 0.28
    l1 = Line(p1, p2, color=color, stroke_width=3.2)
    l2 = Line(p2, p3, color=color, stroke_width=3.2)
    return VGroup(l1, l2)


def cross_mark(color=C_HOT1, size=0.22):
    """Red X."""
    l1 = Line(LEFT*size + UP*size,   RIGHT*size + DOWN*size,
              color=color, stroke_width=3.2)
    l2 = Line(LEFT*size + DOWN*size, RIGHT*size + UP*size,
              color=color, stroke_width=3.2)
    return VGroup(l1, l2)


def asset_row(label, sub, mark_type, row_color):
    """Single checklist row: mark + label + sub."""
    mark = checkmark(row_color) if mark_type == "check" else cross_mark(row_color)
    lbl  = Text(label, font="Arial", weight=BOLD,
                font_size=19, color=C_WHITE)
    sub_t = Text(sub, font="Arial", font_size=14, color=row_color)
    lbl.next_to(mark, RIGHT, buff=0.28)
    sub_t.next_to(lbl, RIGHT, buff=0.22)
    return VGroup(mark, lbl, sub_t)


def chain_node(label, sub, color, r=0.52):
    """Hexagonal chain node."""
    hex_ = RegularPolygon(n=6, radius=r,
                          fill_color=color, fill_opacity=0.18,
                          stroke_color=color, stroke_width=2.0)
    lbl  = Text(label, font="Arial", weight=BOLD,
                font_size=16, color=C_WHITE)
    sub_t = Text(sub, font="Arial", font_size=12,
                 color=color).next_to(hex_, DOWN, buff=0.18)
    return VGroup(hex_, lbl, sub_t)


def path_node(label, color, active=True, r=0.62):
    """Destination node for diverging paths."""
    circ = Circle(radius=r,
                  fill_color=color,
                  fill_opacity=0.85 if active else 0.12,
                  stroke_color=color,
                  stroke_width=2.5 if active else 1.2)
    lbl  = Text(label, font="Arial", weight=BOLD,
                font_size=20,
                color=C_WHITE if active else C_DIM)
    return VGroup(circ, lbl)


# ── Main scene ────────────────────────────────────────────────────────────────

class IndiaFinal(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (~30s)
        # ASSET CHECKLIST
        #
        # India box reappears left of centre.
        # Right side: two-column checklist builds row by row.
        # Strong assets (Talent, Startups, Data, Market) → green ticks,
        #   each row slides in from right with LaggedStart.
        # Weak assets (GPUs, Chips, Compute) → red crosses,
        #   each slides in slower, more ominous.
        # Camera punches in on the crosses.
        # Tag: "Hardware gap — the missing piece."
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("India Today")
        self.play(FadeIn(sec1), run_time=0.4)

        # India box — left side
        BOX_POS = LEFT * 3.8 + UP * 0.2
        box = india_box()
        box.move_to(BOX_POS)
        self.play(
            Create(box[0], run_time=0.8, rate_func=smooth),
            FadeIn(box[1]),
            run_time=0.8
        )

        # Section divider line
        divider = Line(UP * 2.8, DOWN * 2.8,
                       color=C_GRID, stroke_width=1.2).move_to(LEFT * 1.8)
        self.play(Create(divider, run_time=0.4))

        # ── Two-column layout ──
        # Left column  (x = RIGHT*0.2):  strong assets — green ticks
        # Right column (x = RIGHT*3.2):  weak assets   — red crosses
        # Row step = 0.72, both columns centred vertically

        # Section headers
        hdr_strong = TAG("Strengths", color=C_GPT,  size=15).move_to(
            RIGHT * 0.2 + UP * 2.1)
        hdr_weak   = TAG("Gaps",      color=C_HOT1, size=15).move_to(
            RIGHT * 3.5 + UP * 2.1)
        self.play(
            FadeIn(hdr_strong, shift=DOWN * 0.1),
            FadeIn(hdr_weak,   shift=DOWN * 0.1),
            run_time=0.4
        )

        # Strong rows — left column
        N_STRONG   = len(ASSETS_STRONG)
        strong_rows = []
        for i, (label, sub) in enumerate(ASSETS_STRONG):
            row = asset_row(label, sub, "check", C_GPT)
            y   = (N_STRONG - 1) * 0.72 / 2 - i * 0.72
            row.move_to(RIGHT * 0.2 + UP * y)
            row.shift(RIGHT * 8)
            strong_rows.append(row)
            self.add(row)

        self.play(
            LaggedStart(
                *[row.animate.shift(LEFT * 8) for row in strong_rows],
                lag_ratio=T_TICK_LAG
            ),
            run_time=1.4
        )
        self.wait(0.5)

        # Weak rows — right column
        N_WEAK   = len(ASSETS_WEAK)
        weak_rows = []
        for i, (label, sub) in enumerate(ASSETS_WEAK):
            row = asset_row(label, sub, "cross", C_HOT1)
            y   = (N_WEAK - 1) * 0.72 / 2 - i * 0.72
            row.move_to(RIGHT * 3.5 + UP * y)
            row.shift(RIGHT * 8)
            weak_rows.append(row)
            self.add(row)

        self.play(
            LaggedStart(
                *[row.animate.shift(LEFT * 8) for row in weak_rows],
                lag_ratio=T_TICK_LAG * 1.4
            ),
            run_time=1.4
        )

        # Camera punches in on crosses — right column
        crosses_centre = RIGHT * 3.5 + UP * 0.0
        self.play(
            self.camera.frame.animate.scale(0.65).move_to(crosses_centre),
            run_time=0.55
        )
        ripple(self, crosses_centre, color=C_HOT1, n=3, base_r=0.4, run_t=0.55)
        self.wait(1.2)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Tag
        hw_tag = TAG("Hardware gap — the missing piece.",
                     color=C_STAT, size=17).move_to(DOWN * 2.9)
        self.play(AddTextLetterByLetter(hw_tag, time_per_char=0.038))
        self.wait(1.8)

        # Clear
        beat1 = VGroup(box, divider, hw_tag, hdr_strong, hdr_weak,
                       *strong_rows, *weak_rows)
        self.play(FadeOut(beat1), FadeOut(sec1), run_time=0.6)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (~25s)
        # BROKEN CHAIN
        #
        # Four chain nodes in a horizontal row:
        #   Research → Design → Manufacture → Deploy
        # First two glow India-green and connect with solid arrows.
        # "Manufacture" node is red/orange — the broken link.
        # Arrow between Design→Manufacture draws as dashed, then
        # snaps apart with a visual break (X on the link).
        # Last node (Deploy) is dim — unreachable.
        # Semiconductor warning tag writes in.
        # ══════════════════════════════════════════════════════════════════

        sec2 = corner_lbl("The Warning")
        self.play(FadeIn(sec2), run_time=0.4)

        # Semiconductor parallel label at top
        parallel_lbl = TAG("Semiconductors  →  Now AI?",
                           color=C_STAT, size=17).move_to(UP * 2.85)
        self.play(FadeIn(parallel_lbl, shift=DOWN * 0.1), run_time=0.5)

        N      = len(CHAIN_NODES)
        STEP   = 3.0
        NODE_Y = UP * 0.3
        xs     = [-(N - 1) * STEP / 2 + i * STEP for i in range(N)]

        nodes = []
        for nd, x in zip(CHAIN_NODES, xs):
            cn = chain_node(nd["label"], nd["sub"], nd["color"])
            cn.move_to(RIGHT * x + NODE_Y)
            nodes.append(cn)

        # Nodes build left to right
        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.2, rate_func=rush_into) for n in nodes],
                lag_ratio=0.22
            ),
            run_time=T_CHAIN_BUILD * N
        )

        # Arrows between nodes
        arrows = []
        for i in range(N - 1):
            start = nodes[i].get_right()   + RIGHT * 0.08
            end   = nodes[i+1].get_left()  + LEFT  * 0.08
            col   = CHAIN_NODES[i+1]["color"]
            if i == 1:
                # Design → Manufacture: dashed — broken link
                solid = Line(start, end, color=col, stroke_width=1.8)
                arr   = DashedVMobject(solid, num_dashes=8, dashed_ratio=0.5)
            else:
                arr = Arrow(start, end, color=col, stroke_width=2.0,
                            max_tip_length_to_length_ratio=0.18, buff=0)
            arrows.append(arr)

        # Draw solid arrows first
        self.play(
            Create(arrows[0], run_time=0.5),
            run_time=0.5
        )
        self.play(
            Create(arrows[1], run_time=0.7),   # dashed broken link
            run_time=0.7
        )

        # X on the broken link — snaps apart
        mid = (nodes[1].get_right() + nodes[2].get_left()) / 2 + NODE_Y * 0
        break_x = VGroup(
            Line(mid + LEFT*0.22 + UP*0.22,
                 mid + RIGHT*0.22 + DOWN*0.22,
                 color=C_HOT1, stroke_width=4.0),
            Line(mid + LEFT*0.22 + DOWN*0.22,
                 mid + RIGHT*0.22 + UP*0.22,
                 color=C_HOT1, stroke_width=4.0),
        )
        self.play(
            Create(break_x[0], run_time=0.2),
            Create(break_x[1], run_time=0.2),
        )
        ripple(self, mid, color=C_HOT1, n=2, base_r=0.3, run_t=0.45)

        # Deploy arrow — dim, unreachable
        self.play(
            Create(arrows[2], run_time=0.5),
            run_time=0.5
        )
        self.wait(0.5)

        # Camera punches in on broken link
        self.play(
            self.camera.frame.animate.scale(0.62).move_to(mid + NODE_Y),
            run_time=0.55
        )
        self.wait(1.2)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Warning tag
        warn_tag = TAG("Design: India.  Manufacturing: somewhere else.",
                       color=C_HOT1, size=16).move_to(DOWN * 2.2)
        self.play(AddTextLetterByLetter(warn_tag, time_per_char=0.036))
        self.wait(T_BREAK_HOLD)

        # Clear
        beat2 = VGroup(*nodes, *arrows, break_x, warn_tag, parallel_lbl)
        self.play(FadeOut(beat2), FadeOut(sec2), run_time=0.6)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 3  (~30s)
        # DIVERGING PATHS
        #
        # India box reappears at centre-left.
        # Two paths fork from it — upper-right and lower-right.
        # Upper path → "User" node  (dim, hollow)
        # Lower path → "Builder" node (bright, gold glow)
        # An arrow tip appears at the fork, hovering undecided —
        #   it drifts toward User, then back, then toward Builder,
        #   then settles pointing at Builder with a question mark.
        # Investment comparison tag appears.
        # Final two lines write in slowly — the emotional hook.
        # ══════════════════════════════════════════════════════════════════

        sec3 = corner_lbl("The Question")
        self.play(FadeIn(sec3), run_time=0.4)

        # India box at left
        FORK_POS  = LEFT * 3.2 + UP * 0.0
        box2 = india_box()
        box2.move_to(FORK_POS)
        self.play(
            FadeIn(box2, scale=0.3, rate_func=rush_into),
            run_time=0.6
        )

        # Fork point — just right of box
        FORK      = FORK_POS + RIGHT * 1.4
        USER_END  = RIGHT * 3.2 + UP   * 1.6
        BUILD_END = RIGHT * 3.2 + DOWN * 1.6

        # Path lines
        path_user  = Line(FORK, USER_END,
                          color=C_DIM, stroke_width=2.2, stroke_opacity=0.55)
        path_build = Line(FORK, BUILD_END,
                          color=C_FIN, stroke_width=2.8)

        self.play(
            Create(path_user,  run_time=T_PATH_BUILD, rate_func=smooth),
            Create(path_build, run_time=T_PATH_BUILD, rate_func=smooth),
        )

        # Destination nodes
        user_node  = path_node(PATH_USER,    C_DIM, active=False)
        build_node = path_node(PATH_BUILDER, C_FIN, active=True)
        user_node.move_to(USER_END)
        build_node.move_to(BUILD_END)

        self.play(
            FadeIn(user_node,  scale=0.2, rate_func=rush_into),
            FadeIn(build_node, scale=0.2, rate_func=rush_into),
            run_time=0.7
        )
        ripple(self, BUILD_END, color=C_FIN, n=3, base_r=0.4, run_t=0.6)
        self.wait(0.4)

        # Sub-labels under nodes
        user_sub  = TAG("consumer", color=C_DIM, size=14)
        build_sub = TAG("creator",  color=C_FIN, size=14)
        user_sub.next_to(user_node,  UP, buff=0.22)
        build_sub.next_to(build_node, DOWN, buff=0.22)
        self.play(
            FadeIn(user_sub,  shift=DOWN * 0.1),
            FadeIn(build_sub, shift=UP   * 0.1),
            run_time=0.5
        )

        # Undecided arrow at fork — drifts between paths
        undecided = Arrow(
            FORK + LEFT * 0.1, FORK + RIGHT * 0.5 + UP * 0.4,
            color=C_STAT, stroke_width=2.8,
            max_tip_length_to_length_ratio=0.25, buff=0
        )
        self.play(FadeIn(undecided, scale=0.2), run_time=0.4)

        # Drift toward User
        self.play(
            undecided.animate.put_start_and_end_on(
                FORK + LEFT * 0.1,
                FORK + RIGHT * 0.6 + UP * 0.8
            ),
            run_time=0.7, rate_func=smooth
        )
        self.wait(0.3)
        # Drift back toward Builder
        self.play(
            undecided.animate.put_start_and_end_on(
                FORK + LEFT * 0.1,
                FORK + RIGHT * 0.6 + DOWN * 0.8
            ),
            run_time=0.8, rate_func=smooth
        )
        self.wait(0.3)
        # Settle — pointing between both, slightly toward Builder
        self.play(
            undecided.animate.put_start_and_end_on(
                FORK + LEFT * 0.1,
                FORK + RIGHT * 0.55 + DOWN * 0.2
            ),
            run_time=0.6, rate_func=smooth
        )

        # Question mark at fork
        q = STAT("?", color=C_STAT).scale(0.5).move_to(FORK + UP * 0.72)
        slam_in(self, q, bounces=2, run_t=0.5)
        self.wait(0.6)

        # Investment comparison pill
        inv_tag = TAG("USA + China invest 100x more annually.",
                      color=C_DIM, size=15).move_to(DOWN * 2.55)
        self.play(FadeIn(inv_tag, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        # Camera pulls back slightly for the closing lines
        self.play(
            self.camera.frame.animate.scale(1.08).move_to(DOWN * 0.3),
            run_time=0.6
        )

        # Final emotional hook — writes in slowly
        q1 = BODY(FINAL_Q,  color=C_DIM,  size=21).move_to(DOWN * 3.15)
        q2 = BODY(FINAL_Q2, color=C_STAT, size=24).move_to(DOWN * 3.65)

        self.play(AddTextLetterByLetter(q1, time_per_char=0.042))
        self.wait(0.3)
        self.play(AddTextLetterByLetter(q2, time_per_char=0.055))
        self.wait(T_FINAL_HOLD)

        # ── End fade ──
        beat3 = VGroup(
            box2, path_user, path_build,
            user_node, build_node,
            user_sub, build_sub,
            undecided, q, inv_tag,
            q1, q2
        )
        self.play(
            FadeOut(beat3),
            FadeOut(sec3),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()