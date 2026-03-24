"""
clip_07_export_bans_tech_war.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Export Bans aur Tech War"
Scenes: trade_flow_gate, parallel_door
Duration: ~75 seconds  (8:00 – 9:15)
RENDER: manim -pqh clip_07_export_bans_tech_war.py ExportBansTechWar
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
# Beat 1 — trade flow
USA_LABEL      = "USA"
CHINA_LABEL    = "China"
CHIP_LABEL     = "H100 Chip"
GATE_LABEL     = "Export Ban"
YEAR_BAN       = "2022"
REROUTE_LABEL  = "Flow Blocked"
BAN_SUB        = "NVIDIA H100 — Forbidden"

# Beat 2 — parallel door
DOOR_LABEL_1   = "NO ENTRY"
DOOR_LABEL_2   = "Own Door"
COMPANIES      = ["Huawei", "SMIC", "Cambricon"]
SPEED_LABEL    = "Development accelerated"
IRONY_LINE     = "The ban may have sped them up."

# Timing
T_NODE_BUILD   = 0.7
T_FLOW_TRAVEL  = 0.5    # each chip packet travels
T_GATE_SLAM    = 0.55
T_BAN_HOLD     = 2.2
T_REROUTE      = 0.9
T_DOOR_BUILD   = 0.8
T_WALK_THRU    = 0.9
T_ECO_BUILD    = 1.2
T_FINAL_HOLD   = 2.8
T_OUTRO        = 1.2
# ╚══════════════════════════════════════╝


# ── Icon builders ─────────────────────────────────────────────────────────────

def country_node(label, color, r=0.58):
    """Filled circle + country label below."""
    circ = Circle(radius=r, fill_color=color,
                  fill_opacity=0.18, stroke_color=color, stroke_width=2.2)
    init = Text(label[0], font="Arial", weight=BOLD,
                font_size=26, color=color)
    lbl  = TAG(label, color=color, size=16).next_to(circ, DOWN, buff=0.18)
    return VGroup(circ, init, lbl)


def chip_packet(color=C_STAT, size=0.22):
    """Small chip square used as a travelling packet."""
    sq  = Square(side_length=size, fill_color=color,
                 fill_opacity=1, stroke_width=0)
    dot = Circle(radius=size * 0.18, fill_color=C_BG,
                 fill_opacity=1, stroke_width=0)
    return VGroup(sq, dot)


def gate_icon(color=C_HOT1, w=0.18, h=1.6):
    """
    A vertical gate bar — two posts + horizontal crossbar.
    Represents a border gate / checkpoint.
    """
    post_l = Rectangle(width=w, height=h,
                       fill_color=color, fill_opacity=1, stroke_width=0)
    post_r = post_l.copy()
    post_l.move_to(LEFT  * 0.55)
    post_r.move_to(RIGHT * 0.55)
    bar    = Rectangle(width=1.28, height=w * 0.85,
                       fill_color=color, fill_opacity=1, stroke_width=0)
    bar.move_to(UP * h * 0.42)
    return VGroup(post_l, post_r, bar)


def door_frame(color, w=1.1, h=1.8, label=""):
    """
    A door: rectangular frame (open top) + optional label.
    """
    left_post  = Line(DOWN * h/2, UP * h/2,
                      color=color, stroke_width=3.5)
    right_post = left_post.copy()
    top_bar    = Line(LEFT * w/2, RIGHT * w/2,
                      color=color, stroke_width=3.5).move_to(UP * h/2)
    left_post.move_to( LEFT  * w/2)
    right_post.move_to(RIGHT * w/2)
    frame = VGroup(left_post, right_post, top_bar)
    if label:
        lbl = TAG(label, color=color, size=15).move_to(UP * (h/2 + 0.32))
        return VGroup(frame, lbl)
    return VGroup(frame)


def person_dot(color=C_USER, r=0.14):
    """Tiny person: circle head + rect body."""
    head = Circle(radius=r * 0.55, fill_color=color,
                  fill_opacity=1, stroke_width=0).move_to(UP * r * 0.85)
    body = Rectangle(width=r * 0.75, height=r * 0.95,
                     fill_color=color, fill_opacity=1,
                     stroke_width=0).move_to(DOWN * r * 0.05)
    return VGroup(head, body)


# ── Main scene ────────────────────────────────────────────────────────────────

class ExportBansTechWar(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (8:00 – 8:40)  ~40s
        # TRADE FLOW → GATE SLAMS → REROUTE
        #
        # Layout:
        #   USA node  (left,  x=-4.5)
        #   Gate      (centre, x=0)
        #   China node (right, x=+4.5)
        #
        # Phase A — Free flow:
        #   Horizontal pipe connects USA → China.
        #   5 chip packets travel the pipe left→right with LaggedStart.
        #   Labels: "H100 Chip", year "2022" at top.
        #
        # Phase B — Gate slams shut:
        #   Gate icon drops from above onto the pipe centre.
        #   "Export Ban" label slams in red on the gate.
        #   Pipe changes colour to dim/red.
        #
        # Phase C — Reroute:
        #   New dotted line attempts to arc over/under the gate
        #   but dead-ends with an X — flow is truly blocked.
        #   "NVIDIA H100 — Forbidden" pill appears.
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("Tech War")
        self.play(FadeIn(sec1), run_time=0.4)

        # Year anchor
        yr_lbl = STAT(YEAR_BAN, color=C_STAT).scale(0.7).move_to(UP * 3.0)
        slam_in(self, yr_lbl, bounces=2, run_t=0.55)

        # USA and China nodes
        NODE_Y  = UP * 0.4
        usa_node = country_node(USA_LABEL,   C_USER).move_to(LEFT  * 4.5 + NODE_Y)
        chn_node = country_node(CHINA_LABEL, C_HOT1).move_to(RIGHT * 4.5 + NODE_Y)

        self.play(
            FadeIn(usa_node, scale=0.3, rate_func=rush_into),
            run_time=T_NODE_BUILD
        )
        self.play(
            FadeIn(chn_node, scale=0.3, rate_func=rush_into),
            run_time=T_NODE_BUILD
        )

        # Pipe — horizontal line connecting them
        pipe_start = LEFT  * 3.85 + NODE_Y
        pipe_end   = RIGHT * 3.85 + NODE_Y
        pipe = Line(pipe_start, pipe_end,
                    color=C_INFRA, stroke_width=3.2)
        self.play(Create(pipe, run_time=0.7, rate_func=smooth))

        # Chip label above pipe — positioned LEFT of gate centre so gate never covers it
        # Gate lands at NODE_Y (y=0.4), gate height=1.6, top at y≈1.2
        # Place label at y=1.55 and x=-2.2 so it's left of gate, clearly visible
        chip_lbl = TAG(CHIP_LABEL, color=C_STAT, size=16)
        chip_lbl.move_to(LEFT * 2.2 + NODE_Y + UP * 1.25)
        self.play(FadeIn(chip_lbl, shift=DOWN * 0.1), run_time=0.4)

        # Phase A — 5 chip packets travel left→right
        for _ in range(2):
            packets = [chip_packet() for _ in range(5)]
            for p in packets:
                p.move_to(pipe_start)
                self.add(p)
            self.play(
                LaggedStart(
                    *[p.animate.move_to(pipe_end)
                      for p in packets],
                    lag_ratio=0.18
                ),
                run_time=1.4
            )
            for p in packets:
                self.remove(p)
        self.wait(0.3)

        # Phase B — Gate slams down from above
        gate = gate_icon(color=C_HOT1)
        gate.move_to(NODE_Y + UP * 4.5)   # starts off-screen top
        self.add(gate)

        gate_lbl = TAG(GATE_LABEL, color=C_HOT1, size=17)
        gate_lbl.move_to(NODE_Y + DOWN * 1.1)

        self.play(
            gate.animate.move_to(NODE_Y),
            run_time=T_GATE_SLAM, rate_func=rush_into
        )
        # Gate bounce
        self.play(
            gate.animate.shift(UP * 0.18),
            run_time=0.12, rate_func=there_and_back
        )

        # Pipe turns red/dim — blocked
        self.play(
            pipe.animate.set_color(C_HOT1).set_stroke(opacity=0.35),
            FadeIn(gate_lbl, shift=UP * 0.1),
            run_time=0.5
        )

        # Camera punch-in on gate
        self.play(
            self.camera.frame.animate.scale(0.68).move_to(NODE_Y),
            run_time=0.5
        )

        # "NVIDIA H100 — Forbidden" pill
        ban_pill = pill_label(BAN_SUB, color=C_HOT1, text_size=17)
        ban_pill.move_to(NODE_Y + DOWN * 1.65)
        slam_in(self, ban_pill, bounces=2, run_t=0.6)
        self.wait(T_BAN_HOLD)

        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Phase C — Reroute attempt arcs over gate, dead-ends with X
        # Arc path from pipe_start over the gate, comes back down to dead-end
        arc_pts = [
            pipe_start,
            LEFT  * 1.8 + NODE_Y + UP * 1.6,
            RIGHT * 0.0 + NODE_Y + UP * 1.8,
            RIGHT * 1.8 + NODE_Y + UP * 1.6,
        ]
        reroute_solid = VMobject(color=C_DIM, stroke_width=1.8)
        reroute_solid.set_points_smoothly([np.array(p) for p in arc_pts])
        reroute = DashedVMobject(reroute_solid, num_dashes=18, dashed_ratio=0.55)
        self.play(Create(reroute, run_time=T_REROUTE, rate_func=smooth))

        # X mark at dead-end
        dead_pos = RIGHT * 1.8 + NODE_Y + UP * 1.6
        x_mark   = VGroup(
            Line(dead_pos + UP*0.18 + LEFT*0.18,
                 dead_pos + DOWN*0.18 + RIGHT*0.18,
                 color=C_HOT1, stroke_width=3.0),
            Line(dead_pos + DOWN*0.18 + LEFT*0.18,
                 dead_pos + UP*0.18 + RIGHT*0.18,
                 color=C_HOT1, stroke_width=3.0),
        )
        self.play(
            Create(x_mark[0], run_time=0.2),
            Create(x_mark[1], run_time=0.2),
        )
        self.wait(1.6)

        # Full clear
        beat1_group = VGroup(
            usa_node, chn_node, pipe, gate, gate_lbl,
            chip_lbl, ban_pill, reroute, x_mark, yr_lbl
        )
        self.play(
            FadeOut(beat1_group),
            FadeOut(sec1),
            run_time=0.65
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (8:40 – 9:15)  ~35s
        # PARALLEL DOOR
        #
        # Layout:
        #   Left side (x=-2.2): Original door — red frame, "NO ENTRY" sign,
        #                        padlock icon on it. Represents US ban.
        #   Right side (x=+2.2): Empty space — then China builds its own
        #                         door (green frame, "Own Door" label).
        #
        # Animation:
        #   1. Original locked door draws in on left.
        #   2. "NO ENTRY" label slams in above it.
        #   3. A person dot approaches left door → bounces back (blocked).
        #   4. Camera pans right — blank space.
        #   5. China's door draws itself from scratch (posts grow up).
        #   6. Company nodes (Huawei, SMIC, Cambricon) appear below new door.
        #   7. Person dot walks through the new door easily.
        #   8. "Development accelerated" + irony line write in.
        # ══════════════════════════════════════════════════════════════════

        sec2 = corner_lbl("China Responds")
        self.play(FadeIn(sec2), run_time=0.4)

        DOOR_Y    = UP * 0.3
        DOOR_L_X  = LEFT  * 2.8
        DOOR_R_X  = RIGHT * 2.8

        # ── Left door — locked ──
        left_door = door_frame(C_HOT1, w=1.2, h=2.0)
        left_door.move_to(DOOR_L_X + DOOR_Y)

        # Padlock — simple icon: rect body + arc shackle
        lock_body  = Rectangle(width=0.45, height=0.38,
                               fill_color=C_HOT1, fill_opacity=1,
                               stroke_width=0)
        lock_shackle = Arc(radius=0.22, start_angle=0,
                           angle=PI, color=C_HOT1, stroke_width=3.5)
        lock_shackle.move_to(lock_body.get_top() + UP * 0.02)
        padlock = VGroup(lock_body, lock_shackle)
        padlock.move_to(DOOR_L_X + DOOR_Y)

        no_entry_lbl = TAG(DOOR_LABEL_1, color=C_HOT1, size=18)
        no_entry_lbl.move_to(DOOR_L_X + DOOR_Y + UP * 1.42)

        self.play(
            Create(left_door[0][0], run_time=0.4),   # left post
            Create(left_door[0][1], run_time=0.4),   # right post
            Create(left_door[0][2], run_time=0.4),   # top bar
        )
        self.play(
            FadeIn(padlock, scale=0.2, rate_func=rush_into),
            run_time=0.4
        )
        slam_in(self, no_entry_lbl, bounces=2, run_t=0.55)
        self.wait(0.5)

        # Person dot walks toward left door — bounces back
        walker = person_dot(color=C_USER)
        walker.move_to(LEFT * 5.2 + DOOR_Y + DOWN * 0.2)
        self.add(walker)
        self.play(
            walker.animate.move_to(DOOR_L_X + LEFT * 0.85 + DOOR_Y + DOWN * 0.2),
            run_time=0.7, rate_func=smooth
        )
        # Bounce back
        self.play(
            walker.animate.move_to(DOOR_L_X + LEFT * 1.6 + DOOR_Y + DOWN * 0.2),
            run_time=0.35, rate_func=rush_into
        )
        self.wait(0.3)

        # Camera pans right — blank space where new door will be
        self.play(
            self.camera.frame.animate.move_to(DOOR_R_X + DOOR_Y),
            run_time=0.7, rate_func=smooth
        )
        self.wait(0.4)

        # ── Right door — China builds its own ──
        # Posts grow upward from ground
        right_post_l = Line(
            DOOR_R_X + DOOR_Y + LEFT  * 0.6 + DOWN * 1.0,
            DOOR_R_X + DOOR_Y + LEFT  * 0.6 + DOWN * 1.0,
            color=C_GPT, stroke_width=3.5
        )
        right_post_r = Line(
            DOOR_R_X + DOOR_Y + RIGHT * 0.6 + DOWN * 1.0,
            DOOR_R_X + DOOR_Y + RIGHT * 0.6 + DOWN * 1.0,
            color=C_GPT, stroke_width=3.5
        )
        self.add(right_post_l, right_post_r)

        # Posts grow upward
        self.play(
            right_post_l.animate.put_start_and_end_on(
                DOOR_R_X + DOOR_Y + LEFT  * 0.6 + DOWN * 1.0,
                DOOR_R_X + DOOR_Y + LEFT  * 0.6 + UP   * 1.0
            ),
            right_post_r.animate.put_start_and_end_on(
                DOOR_R_X + DOOR_Y + RIGHT * 0.6 + DOWN * 1.0,
                DOOR_R_X + DOOR_Y + RIGHT * 0.6 + UP   * 1.0
            ),
            run_time=T_DOOR_BUILD, rate_func=smooth
        )

        # Top bar draws across
        right_top = Line(
            DOOR_R_X + DOOR_Y + LEFT  * 0.6 + UP * 1.0,
            DOOR_R_X + DOOR_Y + RIGHT * 0.6 + UP * 1.0,
            color=C_GPT, stroke_width=3.5
        )
        self.play(Create(right_top, run_time=0.4, rate_func=smooth))

        own_door_lbl = TAG(DOOR_LABEL_2, color=C_GPT, size=18)
        own_door_lbl.move_to(DOOR_R_X + DOOR_Y + UP * 1.42)
        self.play(FadeIn(own_door_lbl, shift=DOWN * 0.1), run_time=0.4)

        # Company nodes — two rows so pills never overlap
        # Row 1 (top):    Huawei, SMIC  — side by side
        # Row 2 (bottom): Cambricon     — centred
        co_nodes = VGroup()
        co_layout = [
            (COMPANIES[0], RIGHT * -1.15, DOWN * 1.45),   # Huawei — left
            (COMPANIES[1], RIGHT *  1.15, DOWN * 1.45),   # SMIC   — right
            (COMPANIES[2], RIGHT *  0.0,  DOWN * 2.05),   # Cambricon — centre below
        ]
        for co, dx, dy in co_layout:
            nd = pill_label(co, color=C_GPT, text_size=14)
            nd.move_to(DOOR_R_X + DOOR_Y + dx + dy)
            co_nodes.add(nd)

        self.play(
            LaggedStart(
                *[FadeIn(nd, shift=UP * 0.15) for nd in co_nodes],
                lag_ratio=0.22
            ),
            run_time=0.8
        )
        self.wait(0.4)

        # Camera pulls back to show both doors
        self.play(
            self.camera.frame.animate.restore(),
            run_time=0.65
        )
        self.wait(0.3)

        # Person dot (now China-coloured) walks through right door easily
        walker2 = person_dot(color=C_HOT1)
        walker2.move_to(DOOR_R_X + LEFT * 0.85 + DOOR_Y + DOWN * 0.2)
        self.add(walker2)
        self.play(
            walker2.animate.move_to(DOOR_R_X + RIGHT * 1.6 + DOOR_Y + DOWN * 0.2),
            run_time=T_WALK_THRU, rate_func=smooth
        )
        self.remove(walker2)
        ripple(self, DOOR_R_X + RIGHT * 1.6 + DOOR_Y + DOWN * 0.2,
               color=C_GPT, n=2, base_r=0.25, run_t=0.4)

        self.wait(0.4)

        # "Development accelerated" writes in below
        speed_lbl = TAG(SPEED_LABEL, color=C_GPT, size=17)
        speed_lbl.move_to(DOWN * 2.45)
        self.play(AddTextLetterByLetter(speed_lbl, time_per_char=0.04))

        # Irony line — the twist
        irony_lbl = TAG(IRONY_LINE, color=C_STAT, size=16)
        irony_lbl.move_to(DOWN * 2.95)
        self.play(FadeIn(irony_lbl, shift=UP * 0.08), run_time=0.5)

        self.wait(T_FINAL_HOLD)

        # ── End fade ──
        beat2_group = VGroup(
            left_door, padlock, no_entry_lbl, walker,
            right_post_l, right_post_r, right_top,
            own_door_lbl, co_nodes,
            speed_lbl, irony_lbl
        )
        self.play(
            FadeOut(beat2_group),
            FadeOut(sec2),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()