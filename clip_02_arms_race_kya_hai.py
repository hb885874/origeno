"""
clip_02_arms_race_kya_hai.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "AI Arms Race hai kya?"
Scenes: history_morph, invisible_war, hub_spoke
Duration: ~80 seconds  (0:50 – 2:10)
RENDER: manim -pqh clip_02_arms_race_kya_hai.py ArmsRaceKyaHai
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
# Era labels (shown under each icon morph)
ERA_1_LBL   = "Land"
ERA_2_LBL   = "Oil"
ERA_3_LBL   = "Atom"
ERA_NOW_LBL = "AI"

# Hub-spoke labels
COUNTRY_LABELS = ["America", "China", "Europe"]
DOMAIN_LABELS  = ["Compute", "Data", "Algorithms"]

# Timing
T_ICON_BUILD   = 1.0    # each icon draws in
T_MORPH        = 1.2    # ReplacementTransform between icons
T_ERA_HOLD     = 1.6    # pause on each era
T_DARK_FADE    = 1.4    # fade to near-black
T_STREAM_HOLD  = 2.8    # data streams visible
T_HUB_BUILD    = 1.0    # hub node grows
T_SPOKE_LAG    = 0.18   # LaggedStart lag between spokes
T_FINAL_HOLD   = 3.2    # hub-spoke final hold
T_OUTRO        = 1.4    # end fade
# ╚══════════════════════════════════════╝


# ── Icon builders (pure geometry, no external assets) ──────────────────────

def make_flag(color=C_USER):
    """Simple flag: vertical pole + rectangular banner."""
    pole   = Line(DOWN * 0.9, UP * 0.9,
                  color=C_WHITE, stroke_width=3)
    banner = Rectangle(width=1.05, height=0.68,
                       fill_color=color, fill_opacity=0.85,
                       stroke_color=color, stroke_width=1.5)
    banner.next_to(pole, RIGHT, buff=0)
    banner.shift(UP * 0.28)
    return VGroup(pole, banner)


def make_barrel(color=C_HOT2):
    """Oil barrel: rounded rect body + two horizontal bands."""
    body  = RoundedRectangle(corner_radius=0.18,
                             width=0.95, height=1.4,
                             fill_color=color, fill_opacity=0.85,
                             stroke_color=color, stroke_width=1.5)
    band1 = Line(LEFT * 0.47, RIGHT * 0.47,
                 color=C_DARK, stroke_width=3.5).shift(UP  * 0.32)
    band2 = Line(LEFT * 0.47, RIGHT * 0.47,
                 color=C_DARK, stroke_width=3.5).shift(DOWN * 0.32)
    top   = Ellipse(width=0.95, height=0.22,
                    fill_color=color, fill_opacity=1,
                    stroke_color=color, stroke_width=1.5).shift(UP * 0.7)
    return VGroup(body, band1, band2, top)


def make_atom(color=C_INFRA):
    """Atom: nucleus dot + three elliptical orbits at different angles."""
    nucleus = Circle(radius=0.18,
                     fill_color=color, fill_opacity=1, stroke_width=0)
    orbits  = VGroup()
    for angle in [0, 60, 120]:
        orb = Ellipse(width=1.8, height=0.55,
                      color=color, stroke_width=2, fill_opacity=0)
        orb.rotate(angle * DEGREES)
        orbits.add(orb)
    return VGroup(orbits, nucleus)


def make_ai_core(color=C_GPT):
    """AI node: hexagon outline + inner circle + 'AI' text."""
    hex_  = RegularPolygon(n=6, radius=0.75,
                           color=color, stroke_width=2.5, fill_opacity=0)
    inner = Circle(radius=0.38,
                   color=color, stroke_width=1.5, fill_opacity=0)
    label = Text("AI", font="Arial", weight=BOLD,
                 font_size=26, color=color)
    return VGroup(hex_, inner, label)


# ── Hub-spoke helpers ───────────────────────────────────────────────────────

def spoke_positions(n, radius, start_angle=90):
    """Return n evenly-spaced points on a circle of given radius."""
    angles = [start_angle + i * (360 / n) for i in range(n)]
    return [radius * np.array([
        np.cos(a * DEGREES),
        np.sin(a * DEGREES),
        0
    ]) for a in angles]


def country_icon(label, color):
    """Small circle with country initial + label below."""
    circ = Circle(radius=0.42, color=color,
                  stroke_width=2.2, fill_opacity=0)
    init = Text(label[0], font="Arial", weight=BOLD,
                font_size=22, color=color)
    lbl  = TAG(label, color=color, size=15)
    lbl.next_to(circ, DOWN, buff=0.14)
    return VGroup(circ, init, lbl)


def domain_icon(label, color):
    """Rounded rectangle badge with domain label."""
    bg  = RoundedRectangle(corner_radius=0.14,
                           width=1.55, height=0.52,
                           fill_color=C_DARK, fill_opacity=1,
                           stroke_color=color, stroke_width=1.8)
    txt = TAG(label, color=color, size=14)
    return VGroup(bg, txt)


# ── Main scene ──────────────────────────────────────────────────────────────

class ArmsRaceKyaHai(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (0:50 – 1:24)  ~34s
        # History morph:  flag → barrel → atom
        # Each icon draws in, holds, then morphs into the next.
        # Era label sits below, ReplacementTransforms with each morph.
        # Camera punches in on each icon, pulls back before morph.
        # ══════════════════════════════════════════════════════════════════

        # ── section corner label ──
        section_lbl = corner_lbl("History")
        self.play(FadeIn(section_lbl), run_time=0.5)

        # ── Icon 1: Flag ──
        flag     = make_flag(color=C_USER).scale(1.1).move_to(ORIGIN)
        era_lbl  = H2(ERA_1_LBL, color=C_USER).move_to(DOWN * 1.8)

        self.play(
            Create(flag[0], run_time=0.6),                         # pole
            FadeIn(flag[1], scale=0.05, rate_func=rush_into),     # banner
            run_time=T_ICON_BUILD
        )
        self.play(FadeIn(era_lbl, shift=UP * 0.15), run_time=0.5)

        # Camera punch-in on flag
        self.play(
            self.camera.frame.animate.scale(0.72).move_to(flag.get_center()),
            run_time=0.6
        )
        self.wait(T_ERA_HOLD)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # ── Morph flag → barrel ──
        barrel    = make_barrel(color=C_HOT2).scale(1.1).move_to(ORIGIN)
        era_lbl2  = H2(ERA_2_LBL, color=C_HOT2).move_to(DOWN * 1.8)

        self.play(
            ReplacementTransform(flag,    barrel),
            ReplacementTransform(era_lbl, era_lbl2),
            run_time=T_MORPH
        )

        # Camera punch-in on barrel
        self.play(
            self.camera.frame.animate.scale(0.72).move_to(barrel.get_center()),
            run_time=0.6
        )
        self.wait(T_ERA_HOLD)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # ── Morph barrel → atom ──
        atom      = make_atom(color=C_INFRA).scale(1.1).move_to(ORIGIN)
        era_lbl3  = H2(ERA_3_LBL, color=C_INFRA).move_to(DOWN * 1.8)

        self.play(
            ReplacementTransform(barrel,   atom),
            ReplacementTransform(era_lbl2, era_lbl3),
            run_time=T_MORPH
        )

        # Camera punch-in: orbit lines draw attention to atomic structure
        self.play(
            self.camera.frame.animate.scale(0.68).move_to(atom.get_center()),
            run_time=0.6
        )
        self.wait(T_ERA_HOLD)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Atom + label shrink to upper-left — stays as context (3B1B Principle 3)
        history_ctx = VGroup(atom, era_lbl3)
        self.play(
            history_ctx.animate.scale(0.22).move_to(LEFT * 5.5 + UP * 3.0),
            run_time=0.7
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (1:24 – 1:35)  ~11s
        # DEPTH REVEAL — "the invisible war"
        #
        # Step 1: Camera aggressively punches IN (scale down) while
        #         everything on screen fades to black — feels like
        #         tunnelling through the screen into darkness.
        #
        # Step 2: In the darkness, a vast grid of tiny glowing nodes
        #         fades in all around — rows and columns extending to
        #         the edges of the frame, simulating depth/scale.
        #         Nodes have randomised opacity and slight size variation
        #         to break the mechanical regularity.
        #
        # Step 3: Ripple rings pulse outward from centre, as if a signal
        #         is propagating through this invisible network.
        #
        # Step 4: Camera slowly pulls back out to normal scale,
        #         nodes fade away — world returns.
        # ══════════════════════════════════════════════════════════════════

        # Step 1 — tunnel push + blackout
        dark_rect = Rectangle(
            width=30, height=18,
            fill_color="#000000", fill_opacity=0,
            stroke_width=0
        )
        self.add(dark_rect)
        self.play(
            dark_rect.animate.set_fill(opacity=1.0),
            self.camera.frame.animate.scale(0.35),
            FadeOut(section_lbl),
            run_time=1.2, rate_func=rush_into
        )
        self.wait(0.3)

        # Step 2 — node grid materialises in darkness
        # Grid: 11 cols × 7 rows, spacing 1.2 × 0.95
        # Placed BEFORE camera restore so they fill the zoomed-in frame
        COLS, ROWS   = 11, 7
        COL_STEP     = 1.2
        ROW_STEP     = 0.95
        rng          = np.random.default_rng(42)   # deterministic

        grid_nodes = VGroup()
        for r in range(ROWS):
            for c in range(COLS):
                x = (c - COLS // 2) * COL_STEP
                y = (r - ROWS // 2) * ROW_STEP
                # Vary radius and opacity slightly per node for organic feel
                radius  = rng.uniform(0.055, 0.13)
                opacity = rng.uniform(0.25, 0.90)
                color   = [C_INFRA, C_GPT, C_INFRA, C_INFRA][rng.integers(4)]
                dot = Circle(
                    radius=radius,
                    fill_color=color, fill_opacity=0,
                    stroke_width=0
                ).move_to(RIGHT * x + UP * y)
                dot.target_opacity = opacity
                grid_nodes.add(dot)

        # Thin connector lines between adjacent nodes (horizontal + vertical)
        # Only a sparse subset — every other connection — keeps it clean
        connectors = VGroup()
        for r in range(ROWS):
            for c in range(COLS - 1):
                if rng.random() > 0.55:   # ~45% of horizontal lines drawn
                    x1 = (c     - COLS // 2) * COL_STEP
                    x2 = (c + 1 - COLS // 2) * COL_STEP
                    y  = (r     - ROWS // 2) * ROW_STEP
                    ln = Line(RIGHT * x1 + UP * y, RIGHT * x2 + UP * y,
                              color=C_INFRA, stroke_width=0.4,
                              stroke_opacity=rng.uniform(0.08, 0.22))
                    connectors.add(ln)
        for r in range(ROWS - 1):
            for c in range(COLS):
                if rng.random() > 0.65:   # ~35% of vertical lines drawn
                    x  = (c     - COLS // 2) * COL_STEP
                    y1 = (r     - ROWS // 2) * ROW_STEP
                    y2 = (r + 1 - ROWS // 2) * ROW_STEP
                    ln = Line(RIGHT * x + UP * y1, RIGHT * x + UP * y2,
                              color=C_INFRA, stroke_width=0.4,
                              stroke_opacity=rng.uniform(0.08, 0.22))
                    connectors.add(ln)

        # Connectors appear first — very faint structure emerging from black
        self.play(
            LaggedStart(
                *[FadeIn(ln) for ln in connectors],
                lag_ratio=0.015
            ),
            run_time=1.0
        )

        # Nodes bloom in with LaggedStart — centre-out feel
        centre_sorted = sorted(
            grid_nodes,
            key=lambda d: np.linalg.norm(d.get_center()[:2])
        )
        self.play(
            LaggedStart(
                *[dot.animate.set_fill(opacity=dot.target_opacity)
                  for dot in centre_sorted],
                lag_ratio=0.018
            ),
            run_time=1.4
        )

        # Step 3 — ripple pulses from centre — signal propagating
        for _ in range(2):
            ripple(self, ORIGIN, color=C_INFRA, n=3, base_r=0.3, run_t=0.7)
            self.wait(0.2)

        self.wait(0.5)

        # Step 4 — camera pulls back out, grid fades, darkness lifts
        self.play(
            self.camera.frame.animate.restore(),
            FadeOut(grid_nodes),
            FadeOut(connectors),
            run_time=1.1, rate_func=smooth
        )
        self.play(
            dark_rect.animate.set_fill(opacity=0),
            run_time=0.8
        )
        self.remove(dark_rect)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 3  (1:35 – 2:10)  ~35s
        # Hub-spoke diagram:
        #   Centre  — AI hexagon node
        #   Top arc — 3 country nodes  (America, China, Europe)
        #   Bot arc — 3 domain badges  (Compute, Data, Algorithms)
        # Everything builds with LaggedStart; camera breathes outward.
        # ══════════════════════════════════════════════════════════════════

        section_lbl2 = corner_lbl("The Race")
        self.play(FadeIn(section_lbl2), run_time=0.4)

        # ── Hub ──
        hub = make_ai_core(color=C_GPT).move_to(ORIGIN)
        self.play(
            FadeIn(hub[0], scale=0.05, rate_func=rush_into),   # hexagon
            run_time=T_HUB_BUILD
        )
        self.play(
            FadeIn(hub[1], scale=0.05, rate_func=rush_into),   # inner circle
            FadeIn(hub[2], scale=0.05, rate_func=rush_into),   # "AI" label
            run_time=0.5
        )
        ripple(self, ORIGIN, color=C_GPT, n=3, base_r=0.5, run_t=0.6)
        self.wait(0.4)

        # ── Country spokes  (top semicircle, radius 2.6) ──
        C_POSITIONS  = spoke_positions(3, radius=2.6, start_angle=90)
        C_COLORS     = [C_USER, C_HOT1, C_INFRA]

        country_icons  = []
        country_spokes = []
        for pos, lbl, col in zip(C_POSITIONS, COUNTRY_LABELS, C_COLORS):
            icon  = country_icon(lbl, col).move_to(pos)
            spoke = DashedLine(
                hub.get_center() + normalize(pos) * 0.76,
                pos             - normalize(pos) * 0.55,
                color=col, stroke_width=1.4,
                dash_length=0.10, dashed_ratio=0.55
            )
            country_icons.append(icon)
            country_spokes.append(spoke)

        self.play(
            LaggedStart(
                *[AnimationGroup(
                    Create(spk, run_time=0.7),
                    FadeIn(ico, scale=0.3, rate_func=rush_into)
                  )
                  for spk, ico in zip(country_spokes, country_icons)],
                lag_ratio=T_SPOKE_LAG
            ),
            run_time=1.6
        )

        # Camera pulls back gently to frame countries
        self.play(
            self.camera.frame.animate.scale(1.18).move_to(UP * 0.2),
            run_time=0.7
        )
        self.wait(0.8)

        # ── Domain spokes  (bottom semicircle, radius 2.4) ──
        D_POSITIONS = spoke_positions(3, radius=2.4, start_angle=270)
        D_COLORS    = [C_SPEED, C_STAT, C_GPT]

        domain_icons  = []
        domain_spokes = []
        for pos, lbl, col in zip(D_POSITIONS, DOMAIN_LABELS, D_COLORS):
            icon  = domain_icon(lbl, col).move_to(pos)
            spoke = DashedLine(
                hub.get_center() + normalize(pos) * 0.76,
                pos             - normalize(pos) * 0.40,
                color=col, stroke_width=1.4,
                dash_length=0.10, dashed_ratio=0.55
            )
            domain_icons.append(icon)
            domain_spokes.append(spoke)

        self.play(
            LaggedStart(
                *[AnimationGroup(
                    Create(spk, run_time=0.7),
                    FadeIn(ico, scale=0.3, rate_func=rush_into)
                  )
                  for spk, ico in zip(domain_spokes, domain_icons)],
                lag_ratio=T_SPOKE_LAG
            ),
            run_time=1.6
        )

        # Camera breathes out to reveal full hub-spoke composition
        self.play(
            self.camera.frame.animate.scale(1.08).move_to(DOWN * 0.15),
            run_time=0.9
        )
        self.wait(0.6)

        # Pulse — ripple rings from hub outward along each spoke
        for col in [C_GPT, C_USER, C_HOT1, C_INFRA]:
            ripple(self, ORIGIN, color=col, n=2, base_r=0.6, run_t=0.45)

        # ── "Sabse powerful AI" question label writes in below hub ──
        question = TAG("Who builds the most powerful AI first?",
                       color=C_STAT, size=17).move_to(DOWN * 3.4)
        self.play(AddTextLetterByLetter(question, time_per_char=0.04))
        self.wait(T_FINAL_HOLD)

        # ── End fade ──
        all_hub = VGroup(
            hub,
            *country_icons, *country_spokes,
            *domain_icons,  *domain_spokes,
        )
        self.play(
            FadeOut(all_hub),
            FadeOut(question),
            FadeOut(section_lbl2),
            FadeOut(history_ctx),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()