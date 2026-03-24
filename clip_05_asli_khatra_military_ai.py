"""
clip_05_asli_khatra_military_ai.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Asli Khatra — Military AI"
Scenes: radar_screen, putin_quote
Duration: ~90 seconds  (5:15 – 6:45)
RENDER: manim -pqh clip_05_asli_khatra_military_ai.py AsliKhatra
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
# Radar blip positions (x, y) — kept within radar circle radius 2.6
BLIP_POSITIONS = [
    (-1.2,  1.4),
    ( 1.8,  0.6),
    (-0.4, -1.6),
    ( 0.9,  1.9),
    (-1.9, -0.5),
]

# Weapon types fired from blips
WEAPON_LABELS = ["Missile", "Drone", "Cyber", "Drone", "Missile"]
WEAPON_COLORS = [C_HOT1,   C_SPEED, C_INFRA, C_SPEED, C_HOT1]

# No-human badge
NO_HUMAN_TEXT = "NO HUMAN"
NO_HUMAN_SUB  = "Autonomous Action"

# Putin quote
QUOTE_YEAR    = "2017"
QUOTE_LINE_1  = '"Whoever leads in AI...'
QUOTE_LINE_2  = '...will rule the world."'
QUOTE_ATTR    = "— Vladimir Putin, 2017"
WARNING_TEXT  = "This was not sci-fi."
WARNING_SUB   = "This was a warning."

# Timing
T_RADAR_BUILD  = 1.2    # radar rings draw in
T_SWEEP_CYCLE  = 2.5    # one full radar sweep rotation
T_BLIP_LAG     = 0.22   # lag between blip appearances
T_FIRE_HOLD    = 0.6    # pause before each weapon fires
T_BADGE_HOLD   = 2.8    # hold on NO HUMAN badge
T_QUOTE_HOLD   = 3.5    # hold on full quote card
T_OUTRO        = 1.2
# ╚══════════════════════════════════════╝


# ── Icon builders ─────────────────────────────────────────────────────────────

def missile_icon(color=C_HOT1, size=0.38):
    """Simplified missile: elongated body + nose cone + fins."""
    body  = Rectangle(width=size * 0.32, height=size,
                      fill_color=color, fill_opacity=1, stroke_width=0)
    nose  = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    nose.scale(size * 0.18).move_to(UP * size * 0.62)
    fin_l = Polygon(
        LEFT  * size * 0.16 + DOWN * size * 0.38,
        LEFT  * size * 0.36 + DOWN * size * 0.55,
        LEFT  * size * 0.16 + DOWN * size * 0.22,
        fill_color=color, fill_opacity=1, stroke_width=0
    )
    fin_r = fin_l.copy().flip(UP)
    return VGroup(body, nose, fin_l, fin_r)


def drone_icon(color=C_SPEED, size=0.38):
    """Quadcopter drone: cross body + four rotor circles."""
    arm_h = Line(LEFT * size * 0.7, RIGHT * size * 0.7,
                 color=color, stroke_width=3.5)
    arm_v = Line(UP * size * 0.7, DOWN * size * 0.7,
                 color=color, stroke_width=3.5)
    centre = Circle(radius=size * 0.14,
                    fill_color=color, fill_opacity=1, stroke_width=0)
    rotors = VGroup()
    for dx, dy in [(0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)]:
        r = Circle(radius=size * 0.22,
                   color=color, stroke_width=1.8, fill_opacity=0)
        r.move_to(RIGHT * dx * size + UP * dy * size)
        rotors.add(r)
    return VGroup(arm_h, arm_v, centre, rotors)


def cyber_icon(color=C_INFRA, size=0.38):
    """Cyber threat: hexagon with a lightning bolt inside."""
    hex_ = RegularPolygon(n=6, radius=size * 0.72,
                          color=color, stroke_width=2.2, fill_opacity=0)
    # Lightning bolt from polygon points
    bolt = Polygon(
        RIGHT * size * 0.08 + UP   * size * 0.42,
        LEFT  * size * 0.18 + UP   * size * 0.05,
        RIGHT * size * 0.06 + UP   * size * 0.05,
        LEFT  * size * 0.08 + DOWN * size * 0.42,
        RIGHT * size * 0.18 + DOWN * size * 0.05,
        LEFT  * size * 0.06 + DOWN * size * 0.05,
        fill_color=color, fill_opacity=1, stroke_width=0
    )
    return VGroup(hex_, bolt)


def get_weapon_icon(label, color, size=0.34):
    if label == "Missile":
        return missile_icon(color, size)
    elif label == "Drone":
        return drone_icon(color, size)
    else:
        return cyber_icon(color, size)


def radar_rings(n=4, max_r=2.6, color=C_GPT):
    """Concentric radar rings."""
    rings = VGroup()
    for i in range(1, n + 1):
        r = max_r * i / n
        rings.add(Circle(radius=r, color=color,
                         stroke_width=1.0,
                         stroke_opacity=0.35 + 0.1 * i,
                         fill_opacity=0))
    return rings


def putin_silhouette(color=C_DIM, scale=1.0):
    """
    Abstract head+shoulder silhouette built from pure geometry.
    Head: circle. Shoulders: arc / trapezoid below.
    """
    head = Circle(radius=0.42 * scale,
                  fill_color=color, fill_opacity=1, stroke_width=0)
    head.move_to(UP * 0.52 * scale)
    shoulder = Polygon(
        LEFT  * 0.72 * scale + DOWN * 0.20 * scale,
        RIGHT * 0.72 * scale + DOWN * 0.20 * scale,
        RIGHT * 0.38 * scale + UP   * 0.28 * scale,
        LEFT  * 0.38 * scale + UP   * 0.28 * scale,
        fill_color=color, fill_opacity=1, stroke_width=0
    )
    return VGroup(head, shoulder)


# ── Main scene ────────────────────────────────────────────────────────────────

class AsliKhatra(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (5:15 – 5:55)  ~40s
        # RADAR SCREEN
        #
        # A dark radar circle with concentric rings and crosshairs builds.
        # A sweep line rotates one full cycle.
        # Blips appear one by one at fixed positions.
        # From each blip, a weapon icon fires outward (MoveAlongPath)
        # toward the edge — no human confirmation icon, just pure
        # autonomous action. After all weapons fire, a red "NO HUMAN"
        # badge slams in at centre.
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("Military AI")
        self.play(FadeIn(sec1), run_time=0.4)

        RADAR_R   = 2.6
        RADAR_C   = UP * 0.15   # slight upward offset to give room below

        # Dark radar background circle
        radar_bg = Circle(radius=RADAR_R,
                          fill_color="#010810", fill_opacity=1,
                          stroke_color=C_GPT, stroke_width=1.8)
        radar_bg.move_to(RADAR_C)

        # Concentric rings
        rings = radar_rings(n=4, max_r=RADAR_R, color=C_GPT)
        rings.move_to(RADAR_C)

        # Crosshairs
        cross_h = Line(LEFT * RADAR_R, RIGHT * RADAR_R,
                       color=C_GPT, stroke_width=0.8, stroke_opacity=0.4)
        cross_v = Line(DOWN * RADAR_R, UP * RADAR_R,
                       color=C_GPT, stroke_width=0.8, stroke_opacity=0.4)
        cross_h.move_to(RADAR_C)
        cross_v.move_to(RADAR_C)
        crosshairs = VGroup(cross_h, cross_v)

        # Build radar
        self.play(
            FadeIn(radar_bg, run_time=0.5),
            LaggedStart(*[Create(r) for r in rings], lag_ratio=0.18),
            run_time=T_RADAR_BUILD
        )
        self.play(
            Create(cross_h, run_time=0.4),
            Create(cross_v, run_time=0.4),
        )

        # Sweep line — rotates from UP one full cycle (360°)
        sweep = Line(RADAR_C, RADAR_C + UP * RADAR_R,
                     color=C_GPT, stroke_width=2.2, stroke_opacity=0.75)
        # Fading trail: three ghost lines slightly behind
        trail_angles = [8, 18, 32]   # degrees behind sweep
        trails = VGroup(*[
            Line(RADAR_C, RADAR_C + UP * RADAR_R,
                 color=C_GPT,
                 stroke_width=1.4,
                 stroke_opacity=0.18 - i * 0.04)
            .rotate(-a * DEGREES, about_point=RADAR_C)
            for i, a in enumerate(trail_angles)
        ])
        self.add(sweep, trails)
        self.play(
            Rotate(sweep,  angle=-TAU, about_point=RADAR_C),
            Rotate(trails, angle=-TAU, about_point=RADAR_C),
            run_time=T_SWEEP_CYCLE, rate_func=linear
        )
        self.remove(trails)

        # Blips appear at fixed positions with ripple pings
        blip_dots = []
        for (bx, by) in BLIP_POSITIONS:
            pos = RADAR_C + RIGHT * bx + UP * by
            dot = Dot(radius=0.10, color=C_GPT, fill_opacity=0.9)
            dot.move_to(pos)
            self.play(FadeIn(dot, scale=0.2), run_time=0.18)
            ripple(self, pos, color=C_GPT, n=2, base_r=0.18, run_t=0.35)
            blip_dots.append(dot)

        self.wait(0.5)

        # Weapon icons fire from each blip toward radar edge
        # Direction: from blip outward (normalised)
        weapon_icons_fired = []
        for i, ((bx, by), label, col) in enumerate(
                zip(BLIP_POSITIONS, WEAPON_LABELS, WEAPON_COLORS)):

            blip_pos = RADAR_C + RIGHT * bx + UP * by

            # Direction vector from radar centre through blip to edge
            direction = np.array([bx, by, 0])
            norm      = np.linalg.norm(direction[:2])
            if norm < 0.01:
                norm = 1.0
            direction = direction / norm

            # Fire target: radar edge
            fire_end  = RADAR_C + direction * (RADAR_R - 0.1)

            # Build icon, place at blip
            icon = get_weapon_icon(label, col, size=0.32)
            icon.move_to(blip_pos)

            # Tiny label tag below icon
            w_lbl = TAG(label, color=col, size=12)
            w_lbl.next_to(icon, DOWN, buff=0.08)

            self.play(FadeIn(icon, scale=0.2), run_time=0.22)

            # Travel path: straight line from blip to edge
            travel_path = Line(blip_pos, fire_end)
            self.play(
                MoveAlongPath(icon, travel_path, run_time=0.55, rate_func=rush_from),
                FadeOut(blip_dots[i], run_time=0.3),
            )
            self.play(FadeOut(icon, scale=0.1), run_time=0.18)

        self.wait(0.4)

        # "NO HUMAN" badge slams in at radar centre
        badge_bg = RoundedRectangle(
            corner_radius=0.18, width=3.0, height=1.0,
            fill_color=C_HOT1, fill_opacity=0.92, stroke_width=0
        ).move_to(RADAR_C)
        badge_text = Text(NO_HUMAN_TEXT, font="Arial", weight=BOLD,
                          font_size=28, color=C_WHITE)
        badge_text.move_to(RADAR_C + UP * 0.08)
        badge_sub  = Text(NO_HUMAN_SUB, font="Arial",
                          font_size=14, color=C_WHITE, fill_opacity=0.75)
        badge_sub.move_to(RADAR_C + DOWN * 0.32)

        badge = VGroup(badge_bg, badge_text, badge_sub)
        slam_in(self, badge, bounces=3, run_t=0.7)
        self.wait(T_BADGE_HOLD)

        # Camera punches in on badge
        self.play(
            self.camera.frame.animate.scale(0.65).move_to(RADAR_C),
            run_time=0.55
        )
        self.wait(1.0)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Full clear before Beat 2
        radar_group = VGroup(radar_bg, rings, crosshairs, sweep, badge)
        self.play(
            FadeOut(radar_group),
            FadeOut(sec1),
            run_time=0.7
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (5:55 – 6:45)  ~50s
        # PUTIN QUOTE CARD
        #
        # Layout (centred, safe frame):
        #   Year "2017" slams in gold — top anchor
        #   Abstract silhouette fades in — left side
        #   Quote card (dark rounded rect) — right side
        #     Line 1 writes in
        #     Line 2 writes in
        #   Attribution tag fades in below card
        #   Camera punch-in on quote
        #   "WARNING" sub-beat:
        #     WARNING_TEXT writes in, then WARNING_SUB
        # ══════════════════════════════════════════════════════════════════

        sec2 = corner_lbl("The Warning")
        self.play(FadeIn(sec2), run_time=0.4)

        # Year slams in at top
        yr_lbl = STAT(QUOTE_YEAR, color=C_STAT).scale(0.75).move_to(UP * 2.85)
        slam_in(self, yr_lbl, bounces=2, run_t=0.6)
        self.wait(0.4)

        # Silhouette — left side
        sil = putin_silhouette(color=C_DIM, scale=1.35)
        sil.move_to(LEFT * 3.4 + DOWN * 0.1)
        self.play(FadeIn(sil, scale=0.3, rate_func=rush_into), run_time=0.7)

        # Quote card — right side
        card_bg = RoundedRectangle(
            corner_radius=0.2, width=5.8, height=2.2,
            fill_color=C_DARK, fill_opacity=1,
            stroke_color=C_DIM, stroke_width=1.4
        ).move_to(RIGHT * 1.2 + DOWN * 0.1)

        # Left accent bar on card
        accent = RoundedRectangle(
            corner_radius=0.06, width=0.10, height=1.6,
            fill_color=C_HOT1, fill_opacity=1, stroke_width=0
        ).move_to(card_bg.get_left() + RIGHT * 0.13 + DOWN * 0.1)

        self.play(
            FadeIn(card_bg),
            FadeIn(accent),
            run_time=0.5
        )

        # Quote lines write in inside card
        q1 = Text(QUOTE_LINE_1, font="Arial", font_size=21,
                  color=C_WHITE, slant=ITALIC)
        q1.move_to(card_bg.get_center() + UP * 0.38 + RIGHT * 0.15)

        q2 = Text(QUOTE_LINE_2, font="Arial", font_size=21,
                  color=C_WHITE, slant=ITALIC)
        q2.move_to(card_bg.get_center() + DOWN * 0.12 + RIGHT * 0.15)

        self.play(AddTextLetterByLetter(q1, time_per_char=0.038))
        self.wait(0.2)
        self.play(AddTextLetterByLetter(q2, time_per_char=0.038))
        self.wait(0.3)

        # Attribution
        attr = TAG(QUOTE_ATTR, color=C_DIM, size=15)
        attr.next_to(card_bg, DOWN, buff=0.22)
        self.play(FadeIn(attr, shift=UP * 0.1), run_time=0.5)

        # Camera punch-in on full quote composition
        quote_group = VGroup(sil, card_bg, accent, q1, q2)
        self.play(
            self.camera.frame.animate
                .scale(0.78)
                .move_to(quote_group.get_center()),
            run_time=0.65
        )
        self.wait(1.4)
        self.play(self.camera.frame.animate.restore(), run_time=0.55)

        # Warning sub-beat — everything dims slightly
        dim = Rectangle(width=16, height=9,
                        fill_color="#000000", fill_opacity=0,
                        stroke_width=0)
        self.add(dim)
        self.play(dim.animate.set_fill(opacity=0.45), run_time=0.8)

        warn1 = BODY(WARNING_TEXT, color=C_HOT1, size=26)
        warn1.move_to(DOWN * 2.0)
        warn2 = BODY(WARNING_SUB,  color=C_WHITE, size=22)
        warn2.move_to(DOWN * 2.55)

        self.play(AddTextLetterByLetter(warn1, time_per_char=0.045))
        self.wait(0.2)
        self.play(AddTextLetterByLetter(warn2, time_per_char=0.045))

        self.wait(T_QUOTE_HOLD)

        # ── End fade ──
        full_group = VGroup(
            yr_lbl, sil, card_bg, accent, q1, q2,
            attr, warn1, warn2, dim
        )
        self.play(
            FadeOut(full_group),
            FadeOut(sec2),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()