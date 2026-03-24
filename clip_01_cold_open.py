"""
clip_01_cold_open.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Pehli Chingari — Cold Open"
Scenes: eye_duel, arms_race_track
Duration: ~50 seconds
RENDER: manim -pqh clip_01_cold_open.py ColdOpen
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
HUMAN_ERROR_RATE   = 26       # % — human top-5 error on ImageNet 2012
MACHINE_ERROR_RATE = 16       # % — AlexNet top-5 error on ImageNet 2012
LABEL_HUMAN        = "Human"
LABEL_MACHINE      = "AlexNet"
LABEL_YEAR         = "2012"
LABEL_DATASET      = "ImageNet"
LABEL_TITLE        = "AI Arms Race"
LABEL_STAKE        = "duniya ka future"

# Timing beats (seconds)
T_EYE_BUILD        = 1.6    # eyes draw in slower
T_SCAN_HOLD        = 2.2    # pause after scan + ripple
T_BAR_GROW         = 2.0    # bars grow more deliberately
T_RESULT_HOLD      = 3.2    # viewer reads the gap
T_TRANSITION       = 0.9    # shrink to corner
T_TRACK_BUILD      = 1.4    # rails draw in
T_RACE_HOLD        = 1.2    # pause after nodes finish racing
T_TITLE_HOLD       = 3.8    # title sits on screen longer
T_OUTRO_HOLD       = 2.0    # end breath
# ╚══════════════════════════════════════╝


# ── Helpers ────────────────────────────────────────────────────────────────

def make_eye(color, stroke=2.5):
    """Geometric eye: ellipse + iris + pupil, centred at ORIGIN."""
    outer = Ellipse(width=2.6, height=1.25,
                    color=color, stroke_width=stroke, fill_opacity=0)
    iris  = Circle(radius=0.50, color=color,
                   stroke_width=stroke, fill_opacity=0)
    pupil = Circle(radius=0.22, color=color,
                   fill_opacity=1, stroke_width=0)
    return VGroup(outer, iris, pupil)


def make_accuracy_bar(label_str, error_pct, bar_color, bar_width_max=2.8):
    """
    Returns (VGroup(lbl, track, bar, pct), fill_width).
    bar_width_max maps to 100% accuracy.
    """
    accuracy = 100 - error_pct
    fill_w   = bar_width_max * (accuracy / 100)

    lbl   = TAG(label_str, color=C_WHITE, size=18)
    track = Rectangle(width=bar_width_max, height=0.28,
                      fill_color=C_DARK, fill_opacity=1,
                      stroke_color=C_GRID, stroke_width=1.2)
    bar   = Rectangle(width=fill_w, height=0.28,
                      fill_color=bar_color, fill_opacity=1,
                      stroke_width=0)
    pct   = TAG(f"{accuracy}%", color=bar_color, size=17)
    return VGroup(lbl, track, bar, pct), fill_w


def glowing_node(color, radius=0.28):
    """Small filled circle with a soft halo."""
    core = Circle(radius=radius,
                  fill_color=color, fill_opacity=1, stroke_width=0)
    halo = Circle(radius=radius * 1.9,
                  fill_color=color, fill_opacity=0.12, stroke_width=0)
    return VGroup(halo, core)


# ── Main scene ─────────────────────────────────────────────────────────────

class ColdOpen(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (0:00 – 0:05)
        # Year + dataset label appear as context anchors
        # ══════════════════════════════════════════════════════════════════
        year_lbl = STAT(LABEL_YEAR, color=C_STAT).scale(0.9).move_to(UP * 3.0)

        self.play(
            FadeIn(year_lbl, scale=0.05, rate_func=rush_into),
            run_time=0.8
        )
        self.wait(1.2)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (0:05 – 0:18)
        # Human eye (left) vs Machine eye (right) — draw in side by side
        # ══════════════════════════════════════════════════════════════════
        human_eye   = make_eye(color=C_USER).move_to(LEFT  * 2.8 + UP * 0.9)
        machine_eye = make_eye(color=C_GPT ).move_to(RIGHT * 2.8 + UP * 0.9)
        human_tag   = TAG(LABEL_HUMAN,   color=C_USER, size=17).next_to(human_eye,   UP, buff=0.22)
        machine_tag = TAG(LABEL_MACHINE, color=C_GPT,  size=17).next_to(machine_eye, UP, buff=0.22)
        vs_line     = DashedLine(UP * 2.2, DOWN * 1.8,
                                 color=C_GRID, stroke_width=1.5, dash_length=0.12)
        vs_text     = TAG("VS", color=C_DIM, size=19).move_to(UP * 0.9)

        # Eyes draw in simultaneously
        self.play(
            LaggedStart(
                AnimationGroup(
                    Create(human_eye[0]),
                    Create(machine_eye[0])
                ),
                AnimationGroup(
                    FadeIn(human_eye[1],   scale=0.05, rate_func=rush_into),
                    FadeIn(machine_eye[1], scale=0.05, rate_func=rush_into),
                    FadeIn(human_eye[2],   scale=0.05, rate_func=rush_into),
                    FadeIn(machine_eye[2], scale=0.05, rate_func=rush_into),
                ),
                lag_ratio=0.45
            ),
            run_time=T_EYE_BUILD
        )
        self.play(
            FadeIn(human_tag),
            FadeIn(machine_tag),
            Create(vs_line, run_time=0.7),
            FadeIn(vs_text),
            run_time=0.9
        )

        # Cyan scan line sweeps vertically across machine eye — "reading"
        scan = Line(
            machine_eye.get_left()  + LEFT  * 0.05,
            machine_eye.get_right() + RIGHT * 0.05,
            color=C_INFRA, stroke_width=2.0
        ).move_to(machine_eye.get_top())

        self.play(
            scan.animate.move_to(machine_eye.get_bottom()),
            run_time=1.4, rate_func=linear
        )
        self.remove(scan)
        ripple(self, machine_eye.get_center(), color=C_GPT, n=3, base_r=0.4, run_t=0.7)

        # Camera punches in slightly
        self.play(
            self.camera.frame.animate.scale(0.82).move_to(UP * 0.5),
            run_time=0.7
        )
        self.wait(T_SCAN_HOLD)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 3  (0:18 – 0:33)
        # Accuracy bars grow under each eye — machine bar is visibly longer
        # ══════════════════════════════════════════════════════════════════
        self.play(self.camera.frame.animate.restore(), run_time=0.45)

        h_group, h_fill_w = make_accuracy_bar(LABEL_HUMAN,   HUMAN_ERROR_RATE,   C_USER)
        m_group, m_fill_w = make_accuracy_bar(LABEL_MACHINE, MACHINE_ERROR_RATE, C_GPT)

        h_lbl, h_track, h_bar, h_pct = h_group
        m_lbl, m_track, m_bar, m_pct = m_group

        # Position under respective eyes
        h_lbl.move_to(   LEFT * 2.8 + DOWN * 0.60)
        h_track.move_to( LEFT * 2.8 + DOWN * 1.05)
        h_bar.move_to(   h_track.get_left() + RIGHT * h_fill_w / 2 + DOWN * 1.05)
        h_pct.next_to(   h_track, RIGHT, buff=0.18).shift(DOWN * 0.50)

        m_lbl.move_to(   RIGHT * 2.8 + DOWN * 0.60)
        m_track.move_to( RIGHT * 2.8 + DOWN * 1.05)
        m_bar.move_to(   m_track.get_left() + RIGHT * m_fill_w / 2 + DOWN * 1.05)
        m_pct.next_to(   m_track, RIGHT, buff=0.18).shift(DOWN * 0.50)

        # Start bars at zero width, grow to target
        h_bar_zero = h_bar.copy().stretch(0.001, 0).move_to(
            h_track.get_left() + RIGHT * 0.001 + DOWN * 1.05
        )
        m_bar_zero = m_bar.copy().stretch(0.001, 0).move_to(
            m_track.get_left() + RIGHT * 0.001 + DOWN * 1.05
        )

        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(h_lbl), FadeIn(h_track)),
                AnimationGroup(FadeIn(m_lbl), FadeIn(m_track)),
                lag_ratio=0.2
            ),
            run_time=0.8
        )
        self.add(h_bar_zero, m_bar_zero)
        self.play(
            ReplacementTransform(h_bar_zero, h_bar),
            ReplacementTransform(m_bar_zero, m_bar),
            run_time=T_BAR_GROW, rate_func=smooth
        )
        self.play(
            FadeIn(h_pct, scale=0.4),
            FadeIn(m_pct, scale=0.4),
            run_time=0.6
        )

        # Camera punches in on the machine bar — the winner
        self.play(
            self.camera.frame.animate.scale(0.65).move_to(RIGHT * 2.8 + DOWN * 1.0),
            run_time=0.7
        )
        ripple(self, machine_eye.get_center(), color=C_GPT, n=2, base_r=0.5, run_t=0.6)
        self.wait(T_RESULT_HOLD)
        self.play(self.camera.frame.animate.restore(), run_time=0.7)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 4  (0:33 – 0:50)
        # Transition → full-width race track
        # Scene 1 content shrinks to upper-left as memory/context
        # ══════════════════════════════════════════════════════════════════
        scene1_group = VGroup(
            human_eye, machine_eye,
            human_tag, machine_tag,
            vs_line, vs_text,
            h_lbl, h_track, h_bar, h_pct,
            m_lbl, m_track, m_bar, m_pct,
        )
        self.play(
            scene1_group.animate.scale(0.18).move_to(LEFT * 5.5 + UP * 3.0),
            run_time=T_TRANSITION
        )

        # ── Race track — three separate lanes ──
        #
        # Safe frame:  x ∈ [−6.8, +6.8],  y ∈ [−3.8, +3.8]
        # Layout (top → bottom):
        #   UP*2.6        title  "AI Arms Race"
        #   UP*1.8        tick year labels
        #   UP*0.9        lane 0  (USA / OpenAI)
        #   ORIGIN        lane 1  (China / Baidu)
        #   DOWN*0.9      lane 2  (EU / DeepMind)
        #   DOWN*1.8      "duniya ka future" stake tag
        #
        # Lane labels sit to the RIGHT of the track end (+4.2 → +6.4) so they
        # never overlap the nodes which travel LEFT→RIGHT and stop at +4.0.

        LANE_YS   = [UP * 0.9, ORIGIN, DOWN * 0.9]
        COLORS    = [C_GPT,          C_USER,          C_SPEED]
        N_LABELS  = ["USA / OpenAI", "China / Baidu", "EU / DeepMind"]

        # Track runs x: −4.8 → +4.2  (leaves room for label on the right)
        TRACK_X_L = -4.8
        TRACK_X_R =  4.2
        START_X   = -4.6   # node start — just inside left edge of track
        END_X     =  4.0   # node final stop — just before label zone

        rails     = VGroup()
        lane_lbls = VGroup()
        for ly, lc, ll in zip(LANE_YS, COLORS, N_LABELS):
            rail = Line(LEFT * 4.8, RIGHT * 4.2,
                        color=C_GRID, stroke_width=1.6).move_to(ly)
            rails.add(rail)
            # Label sits to the right of the track, centred on its lane Y
            lbl = TAG(ll, color=lc, size=14).move_to(RIGHT * 5.3 + ly)
            lane_lbls.add(lbl)

        # Year ticks — short marks between top and bottom lane only
        # Labels sit ABOVE the top lane (UP*1.4) so they don't touch nodes
        tick_years = ["2012", "2015", "2017", "2020", "2023", "2025"]
        tick_xs    = np.linspace(TRACK_X_L, TRACK_X_R, len(tick_years))
        ticks      = VGroup()
        tick_lbls  = VGroup()

        for x, yr in zip(tick_xs, tick_years):
            # Tick spans only between top rail and bottom rail
            t = Line(UP * 0.9, DOWN * 0.9,
                     color=C_GRID, stroke_width=0.9).move_to(RIGHT * x)
            ticks.add(t)
            # Year label above the top lane, clear of nodes
            lbl = TAG(yr, color=C_DIM, size=13).move_to(RIGHT * x + UP * 1.35)
            tick_lbls.add(lbl)

        self.play(
            LaggedStart(*[Create(r) for r in rails], lag_ratio=0.2),
            run_time=T_TRACK_BUILD
        )
        self.play(
            LaggedStart(*[Create(t)            for t in ticks],     lag_ratio=0.10),
            LaggedStart(*[FadeIn(l, scale=0.3) for l in tick_lbls], lag_ratio=0.10),
            LaggedStart(*[FadeIn(ll)           for ll in lane_lbls], lag_ratio=0.2),
            run_time=1.0
        )

        # ── One glowing node per lane, starts at left of track ──
        nodes = VGroup()
        for ly, lc in zip(LANE_YS, COLORS):
            nd = glowing_node(lc, radius=0.26).move_to(RIGHT * START_X + ly)
            nodes.add(nd)

        self.play(
            LaggedStart(*[FadeIn(n, scale=0.05, rate_func=rush_into) for n in nodes],
                        lag_ratio=0.22),
            run_time=0.9
        )

        # ── Three acceleration phases: slow → mid → sprint ──
        # All nodes stop at END_X = 4.0 — safely left of the lane labels at 5.3
        PHASE_XS    = [-1.4,  1.6,  END_X]
        PHASE_TIMES = [ 1.8,  1.3,  0.9]
        PHASE_RATES = [smooth, smooth, rush_from]

        for target_x, run_t, rate in zip(PHASE_XS, PHASE_TIMES, PHASE_RATES):
            anims = [nd.animate.move_to(RIGHT * target_x + ly)
                     for nd, ly in zip(nodes, LANE_YS)]
            self.play(*anims, run_time=run_t, rate_func=rate)

            if target_x < END_X:
                for nd, lc in zip(nodes, COLORS):
                    ripple(self, nd.get_center(), color=lc, n=2, base_r=0.30, run_t=0.36)

        self.wait(T_RACE_HOLD)

        # Fade year_lbl out before title — clears the top zone
        self.play(FadeOut(year_lbl), run_time=0.4)

        # ── Title slams in — positioned above tick labels, within safe frame ──
        title = H1(LABEL_TITLE, color=C_SPEED)
        title.scale(1.4).move_to(UP * 2.6)
        slam_in(self, title, bounces=3, run_t=0.75)

        # Stake tag — below bottom lane, above screen bottom
        stake = TAG(LABEL_STAKE, color=C_DIM, size=19).move_to(DOWN * 1.75)
        self.play(AddTextLetterByLetter(stake, time_per_char=0.055))

        # Camera breathes slightly outward — reveal full composition
        self.play(
            self.camera.frame.animate.scale(1.10),
            run_time=1.2, rate_func=there_and_back
        )
        self.wait(T_TITLE_HOLD)

        # ── End fade ──
        self.play(
            FadeOut(title),
            FadeOut(stake),
            FadeOut(rails),
            FadeOut(lane_lbls),
            FadeOut(ticks),
            FadeOut(tick_lbls),
            FadeOut(nodes),
            FadeOut(scene1_group),
            FadeOut(bg),
            run_time=1.4
        )
        self.wait(T_OUTRO_HOLD)