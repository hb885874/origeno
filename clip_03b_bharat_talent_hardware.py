"""
clip_03b_bharat_talent_hardware.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Bharat: Talent Superpower, Hardware Underdog"
Scenes: talent_drain, infra_gap, player_vs_supplier
Duration: ~90 seconds
RENDER: manim -pqh clip_03b_bharat_talent_hardware.py BharatTalentHardware
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
# Beat 1 — talent drain
N_TALENT_DOTS   = 38          # dots that accumulate inside India
DRAIN_TARGETS   = [
    {"label": "Silicon Valley", "pos": (-5.2,  1.2), "color": C_USER},
    {"label": "London",         "pos": (-4.8, -0.8), "color": C_INFRA},
    {"label": "Singapore",      "pos": ( 4.6,  0.4), "color": C_GPT},
    {"label": "Toronto",        "pos": (-3.8,  2.2), "color": C_SPEED},
]

# Beat 2 — infra gap bars
BAR_DATA = [
    {"label": "Talent",         "fill": 0.92, "color": C_GPT,  "sub": "World #1"},
    {"label": "Infrastructure", "fill": 0.07, "color": C_HOT1, "sub": "Near zero"},
]
BAR_MAX_H   = 3.4
BASELINE_Y  = -1.5

# Beat 3 — player vs supplier
ROLE_PLAYER   = "Player"
ROLE_SUPPLIER = "Supplier"
INDIA_CURRENT = "Supplier"

# Timing
T_DOT_ACCUM    = 2.2
T_DRAIN_LAG    = 0.14
T_DRAIN_TRAVEL = 0.9
T_BAR_GROW     = 2.2
T_BAR_HOLD     = 2.5
T_NODE_BUILD   = 0.8
T_FINAL_HOLD   = 3.0
T_OUTRO        = 1.2
# ╚══════════════════════════════════════╝


# ── India outline (simplified polygon) ───────────────────────────────────────
# Approximate India silhouette as a polygon — enough to be recognisable
# Points are (x, y) in Manim units, scaled to fit ~2.2 wide × 2.8 tall
# Traced roughly: top-left (J&K) → top-right → east coast → south tip →
# west coast → back up. Centred at ORIGIN.

# ── India box representation ──────────────────────────────────────────────────

def india_outline(color=C_FIN, stroke_w=1.8, w=2.6, h=3.2):
    """
    Simple labelled rectangle representing India.
    Width slightly narrower than height to suggest portrait orientation.
    """
    box = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        fill_color=color, fill_opacity=0.08,
        stroke_color=color, stroke_width=stroke_w
    )
    lbl = Text("India", font="Arial", weight=BOLD,
               font_size=28, color=color, fill_opacity=0.35)
    return VGroup(box, lbl)


def random_pts_in_india(n, outline_mob, seed=42):
    """Sample n random points inside the box with a small inset margin."""
    x_min = outline_mob.get_left()[0]   + 0.25
    x_max = outline_mob.get_right()[0]  - 0.25
    y_min = outline_mob.get_bottom()[1] + 0.25
    y_max = outline_mob.get_top()[1]    - 0.25
    rng   = np.random.default_rng(seed)
    return [
        np.array([rng.uniform(x_min, x_max),
                  rng.uniform(y_min, y_max), 0])
        for _ in range(n)
    ]


# ── Role node builder ─────────────────────────────────────────────────────────

def role_node(label, color, r=0.68, active=False):
    """
    Hexagonal node with label inside.
    active=True → filled, brighter. active=False → hollow, dim.
    """
    hex_ = RegularPolygon(n=6, radius=r,
                          fill_color=color if active else C_DARK,
                          fill_opacity=0.85 if active else 0.12,
                          stroke_color=color,
                          stroke_width=2.5 if active else 1.4)
    lbl  = Text(label, font="Arial", weight=BOLD,
                font_size=20 if active else 17,
                color=C_WHITE if active else C_DIM)
    return VGroup(hex_, lbl)


# ── Main scene ────────────────────────────────────────────────────────────────

class BharatTalentHardware(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (~30s)
        # TALENT DRAIN
        #
        # India outline draws in. "India" title slams in.
        # 38 researcher dots bloom inside the outline with LaggedStart.
        # Brief hold — the talent pool.
        # Then arrows pull batches of dots outward toward 4 global
        # company destinations. Each destination label appears as the
        # dots arrive. India outline dims slightly.
        # Tag: "World's largest AI talent pool — leaving."
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("Talent")
        self.play(FadeIn(sec1), run_time=0.4)

        # India title
        india_title = H1("India", color=C_FIN).scale(1.05).move_to(UP * 2.85)
        slam_in(self, india_title, bounces=2, run_t=0.55)
        self.wait(0.3)

        # India outline — centred slightly right to leave label room left
        INDIA_C = RIGHT * 0.2 + DOWN * 0.1

        outline = india_outline(color=C_FIN)
        outline.move_to(INDIA_C)
        INDIA_C = outline.get_center()

        self.play(
            Create(outline[0], run_time=1.0, rate_func=smooth),   # box draws in
            FadeIn(outline[1], run_time=0.8),                      # label fades in
        )

        # Researcher dots accumulate inside outline
        dot_pts = random_pts_in_india(N_TALENT_DOTS, outline, seed=42)
        dot_pts = [p for p in dot_pts]   # already in world coords (outline centred)

        talent_dots = VGroup(*[
            Dot(radius=0.085, color=C_FIN, fill_opacity=0.85).move_to(p)
            for p in dot_pts
        ])

        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.1, rate_func=rush_into)
                  for d in talent_dots],
                lag_ratio=0.045
            ),
            run_time=T_DOT_ACCUM
        )
        self.wait(0.7)

        # Drain — dots flow outward to destinations
        # Split dots into 4 groups, one per destination
        group_size = N_TALENT_DOTS // len(DRAIN_TARGETS)
        dest_labels = []

        for i, dest in enumerate(DRAIN_TARGETS):
            start_idx = i * group_size
            end_idx   = start_idx + group_size
            group_dots = list(talent_dots)[start_idx:end_idx]

            dest_pos = np.array([dest["pos"][0], dest["pos"][1], 0])
            col      = dest["color"]

            # Arrow from India centre toward destination
            arr_start = INDIA_C + normalize(dest_pos - INDIA_C) * 1.4
            arr_end   = dest_pos - normalize(dest_pos - INDIA_C) * 0.55
            arr_end[0] = np.clip(arr_end[0], -6.0, 6.0)
            arr_end[1] = np.clip(arr_end[1], -3.2, 3.2)

            drain_arrow = Arrow(
                arr_start, arr_end,
                color=col, stroke_width=1.6,
                max_tip_length_to_length_ratio=0.14, buff=0
            )

            # Destination label
            d_lbl = TAG(dest["label"], color=col, size=15)
            d_lbl.move_to(dest_pos + normalize(dest_pos) * 0.42)
            d_lbl.move_to(np.clip(d_lbl.get_center(), -6.0, 6.0) * np.array([1, 1, 0])
                          + np.array([0, 0, 0]))
            d_lbl.move_to(np.array([
                np.clip(dest_pos[0], -5.8, 5.8),
                np.clip(dest_pos[1] + (0.38 if dest_pos[1] >= 0 else -0.38), -3.2, 3.2),
                0
            ]))

            # Draw arrow, then dots travel along it
            self.play(Create(drain_arrow, run_time=0.4, rate_func=smooth))
            self.play(
                LaggedStart(
                    *[dot.animate.move_to(arr_end) for dot in group_dots],
                    lag_ratio=T_DRAIN_LAG
                ),
                run_time=T_DRAIN_TRAVEL
            )
            for dot in group_dots:
                self.remove(dot)
            ripple(self, arr_end, color=col, n=2, base_r=0.22, run_t=0.35)
            self.play(FadeIn(d_lbl, shift=normalize(dest_pos) * 0.12),
                      run_time=0.3)
            dest_labels.append(VGroup(drain_arrow, d_lbl))

        # Outline dims — India is being hollowed out
        self.play(
            outline.animate.set_stroke(opacity=0.30).set_fill(opacity=0.04),
            run_time=0.7
        )

        # Tag
        drain_tag = TAG("World's largest AI talent pool — leaving.",
                        color=C_STAT, size=17).move_to(DOWN * 2.75)
        self.play(AddTextLetterByLetter(drain_tag, time_per_char=0.038))
        self.wait(1.8)

        # Full clear
        beat1 = VGroup(outline, india_title, *dest_labels, drain_tag)
        self.play(FadeOut(beat1), FadeOut(sec1), run_time=0.65)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (~25s)
        # INFRA GAP — two bars side by side
        #
        # "Talent" bar grows almost to top — green, full.
        # "Infrastructure" bar barely lifts off baseline — red, near zero.
        # The visual contrast is immediate and brutal.
        # Labels + sub-tags appear. Camera punches in on infra bar.
        # ══════════════════════════════════════════════════════════════════

        sec2 = corner_lbl("Infrastructure Gap")
        self.play(FadeIn(sec2), run_time=0.4)

        axis = Line(LEFT * 3.8, RIGHT * 3.8,
                    color=C_GRID, stroke_width=1.6).move_to(UP * BASELINE_Y)
        self.play(Create(axis, run_time=0.5, rate_func=smooth))

        BAR_W   = 1.8
        BAR_XS  = [-1.6, 1.6]

        bar_groups  = []
        bar_heights = []

        for bd, bx in zip(BAR_DATA, BAR_XS):
            h   = BAR_MAX_H * bd["fill"]
            bar = Rectangle(width=BAR_W, height=max(h, 0.04),
                            fill_color=bd["color"], fill_opacity=1,
                            stroke_width=0)
            bar.move_to(RIGHT * bx + UP * (BASELINE_Y + h / 2))

            lbl = Text(bd["label"], font="Arial", weight=BOLD,
                       font_size=21, color=C_WHITE)
            lbl.move_to(RIGHT * bx + UP * (BASELINE_Y - 0.42))

            sub = Text(bd["sub"], font="Arial", font_size=14,
                       color=bd["color"])
            sub.move_to(RIGHT * bx + UP * (BASELINE_Y - 0.80))

            pct = Text(f"{int(bd['fill']*100)}%", font="Arial",
                       weight=BOLD, font_size=22, color=bd["color"])
            pct.move_to(RIGHT * bx + UP * (BASELINE_Y + h + 0.38))

            # Start bar at zero
            zb = bar.copy().stretch(0.001, 1).move_to(
                RIGHT * bx + UP * (BASELINE_Y + 0.001))

            bar_groups.append((bar, lbl, sub, pct, zb, bx, h))
            bar_heights.append(h)

        # Add zero-height bars
        for _, _, _, _, zb, _, _ in bar_groups:
            self.add(zb)

        # Both bars grow simultaneously
        self.play(
            *[ReplacementTransform(zb, bar)
              for bar, _, _, _, zb, _, _ in bar_groups],
            run_time=T_BAR_GROW, rate_func=smooth
        )

        # Labels and pct slam in
        for bar, lbl, sub, pct, _, bx, h in bar_groups:
            pct.move_to(RIGHT * bx + UP * (BASELINE_Y + h + 0.38))
            slam_in(self, pct, bounces=2, run_t=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(lbl) for _, lbl, _, _, _, _, _ in bar_groups],
                *[FadeIn(sub) for _, _, sub, _, _, _, _ in bar_groups],
                lag_ratio=0.15
            ),
            run_time=0.6
        )
        self.wait(0.5)

        # Camera punches in on infra bar — nearly invisible
        infra_bx = BAR_XS[1]
        infra_h  = bar_heights[1]
        self.play(
            self.camera.frame.animate
                .scale(0.55)
                .move_to(RIGHT * infra_bx + UP * (BASELINE_Y + 0.5)),
            run_time=0.6
        )
        self.wait(1.0)
        self.play(self.camera.frame.animate.restore(), run_time=0.55)

        # Infra tag
        infra_tag = TAG("Talent: full. Hardware: empty.",
                        color=C_STAT, size=18).move_to(DOWN * 3.1)
        self.play(AddTextLetterByLetter(infra_tag, time_per_char=0.042))
        self.wait(T_BAR_HOLD)

        # Clear
        beat2_mobs = VGroup(axis, infra_tag,
                            *[bar for bar, _, _, _, _, _, _ in bar_groups],
                            *[lbl for _, lbl, _, _, _, _, _ in bar_groups],
                            *[sub for _, _, sub, _, _, _, _ in bar_groups],
                            *[pct for _, _, _, pct, _, _, _ in bar_groups])
        self.play(FadeOut(beat2_mobs), FadeOut(sec2), run_time=0.65)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 3  (~25s)
        # PLAYER vs SUPPLIER
        #
        # Two hexagonal role nodes appear side by side:
        #   "Player"   — LEFT  — dim, hollow, question mark above
        #   "Supplier" — RIGHT — lit, filled, India arrow points to it
        #
        # India label sits between them with an arrow pointing RIGHT
        # toward Supplier. Player node has a "?" above it.
        # Camera punches in on each node in sequence.
        # Final line: "Not yet a Player." writes in slowly.
        # ══════════════════════════════════════════════════════════════════

        sec3 = corner_lbl("Role")
        self.play(FadeIn(sec3), run_time=0.4)

        NODE_Y  = UP * 0.55
        NODE_XL = LEFT  * 2.8
        NODE_XR = RIGHT * 2.8

        # Player node — dim
        player_node = role_node(ROLE_PLAYER, color=C_DIM, active=False)
        player_node.move_to(NODE_XL + NODE_Y)

        # Supplier node — active/lit
        supplier_node = role_node(ROLE_SUPPLIER, color=C_FIN, active=True)
        supplier_node.move_to(NODE_XR + NODE_Y)

        # "?" above player
        q_mark = STAT("?", color=C_DIM).scale(0.55)
        q_mark.move_to(NODE_XL + NODE_Y + UP * 1.18)

        # India label + arrow in the middle
        india_lbl = H2("India", color=C_FIN).move_to(DOWN * 0.35)
        mid_arrow = Arrow(
            DOWN * 0.28, NODE_XR + NODE_Y + LEFT * 0.72 + DOWN * 0.08,
            color=C_FIN, stroke_width=2.4,
            max_tip_length_to_length_ratio=0.15, buff=0
        )

        # Draw nodes
        self.play(
            FadeIn(player_node,   scale=0.2, rate_func=rush_into),
            FadeIn(supplier_node, scale=0.2, rate_func=rush_into),
            run_time=T_NODE_BUILD
        )
        self.play(
            FadeIn(q_mark, scale=0.1, rate_func=rush_into),
            run_time=0.4
        )
        self.play(
            FadeIn(india_lbl, shift=UP * 0.12),
            run_time=0.4
        )
        self.play(
            Create(mid_arrow, run_time=0.55, rate_func=smooth)
        )

        # Ripple on supplier — India's current role lights up
        ripple(self, NODE_XR + NODE_Y, color=C_FIN, n=3, base_r=0.5, run_t=0.6)

        # Camera: punch-in on Player node — dim, hollow
        self.play(
            self.camera.frame.animate.scale(0.62).move_to(NODE_XL + NODE_Y),
            run_time=0.55
        )
        self.wait(0.9)

        # Pan to Supplier — lit up
        self.play(
            self.camera.frame.animate.move_to(NODE_XR + NODE_Y),
            run_time=0.7
        )
        self.wait(0.9)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Sub-labels below each node
        player_sub = TAG("Not yet", color=C_DIM, size=15)
        player_sub.move_to(NODE_XL + NODE_Y + DOWN * 1.05)
        supplier_sub = TAG("For now", color=C_FIN, size=15)
        supplier_sub.move_to(NODE_XR + NODE_Y + DOWN * 1.05)

        self.play(
            FadeIn(player_sub,   shift=UP * 0.1),
            FadeIn(supplier_sub, shift=UP * 0.1),
            run_time=0.5
        )
        self.wait(0.5)

        # Emotional closing line — writes in slowly
        closing = BODY("AI race mein India ka role abhi —",
                       color=C_DIM, size=20).move_to(DOWN * 2.15)
        closing2 = BODY("supplier ka zyada. player ka kam.",
                        color=C_STAT, size=22).move_to(DOWN * 2.65)

        self.play(AddTextLetterByLetter(closing,  time_per_char=0.040))
        self.play(AddTextLetterByLetter(closing2, time_per_char=0.048))
        self.wait(T_FINAL_HOLD)

        # ── End fade ──
        beat3 = VGroup(
            player_node, supplier_node, q_mark,
            india_lbl, mid_arrow,
            player_sub, supplier_sub,
            closing, closing2
        )
        self.play(
            FadeOut(beat3),
            FadeOut(sec3),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()