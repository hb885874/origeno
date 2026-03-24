"""
clip_03_khiladi_kaun_hain.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Khiladi Kaun Hain?"
Scenes: america_cards, china_grid, europe_balance
Duration: ~95 seconds  (2:10 – 3:45)
RENDER: manim -pqh clip_03_khiladi_kaun_hain.py KhiladiKaunHain
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
# America — company cards
COMPANIES = [
    {"name": "OpenAI",    "stat": "GPT-4o",        "color": C_GPT},
    {"name": "Google",    "stat": "Gemini",         "color": C_INFRA},
    {"name": "Anthropic", "stat": "Claude",         "color": C_SPEED},
    {"name": "Meta",      "stat": "Llama (Open)",   "color": C_USER},
]
USA_TAG     = "Top AI Researchers — concentrated in one city"

# China — population grid
CHINA_POP   = "1.4B"
CHINA_LABS  = "100+"
CHINA_TAG   = "State-funded labs  •  Massive scale  •  Daily data"

# Europe — balance labels
EU_LEFT     = "Innovation"
EU_RIGHT    = "Regulation"
EU_ACT      = "EU AI Act  —  2024"
EU_TAG_L    = "Risk?"
EU_TAG_R    = "Wisdom?"

# Timing
T_CARD_SLIDE   = 0.55   # each card slides in
T_CARD_LAG     = 0.18   # lag between cards
T_SEGMENT_HOLD = 2.8    # hold at end of each segment
T_SHRINK       = 0.65   # shrink to corner transition
T_DOT_LAG      = 0.012  # lag between dot appearances in grid
T_LINE_LAG     = 0.025  # lag between data lines
T_BALANCE_HOLD = 3.2    # hold on tipping balance
T_OUTRO        = 1.4
# ╚══════════════════════════════════════╝


# ── Helpers ─────────────────────────────────────────────────────────────────

def company_card(name, stat_text, color, w=2.6, h=1.55):
    """
    Rounded card with:
      • coloured left accent stripe
      • company name (H2 size)
      • stat / product tag below
    """
    bg      = RoundedRectangle(corner_radius=0.14, width=w, height=h,
                               fill_color=C_DARK, fill_opacity=1,
                               stroke_color=color, stroke_width=1.6)
    accent  = RoundedRectangle(corner_radius=0.07, width=0.12, height=h * 0.72,
                               fill_color=color, fill_opacity=1, stroke_width=0)
    accent.move_to(bg.get_left() + RIGHT * 0.14)
    name_t  = Text(name,      font="Arial", weight=BOLD,
                   font_size=22, color=C_WHITE)
    stat_t  = Text(stat_text, font="Arial",
                   font_size=16, color=color)
    name_t.move_to(bg.get_center() + UP   * 0.26 + RIGHT * 0.12)
    stat_t.move_to(bg.get_center() + DOWN * 0.24 + RIGHT * 0.12)
    return VGroup(bg, accent, name_t, stat_t)


def balance_beam(beam_len=4.8, color=C_GRID):
    """
    A simple balance / scale:
      pivot  — triangle at centre bottom
      beam   — horizontal bar
    Returns VGroup(pivot, beam).
    Pivot tip sits at ORIGIN.
    """
    pivot = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    pivot.scale(0.28).move_to(DOWN * 0.18)
    beam  = Line(LEFT * beam_len / 2, RIGHT * beam_len / 2,
                 color=color, stroke_width=3.5)
    beam.move_to(UP * 0.18)
    return VGroup(pivot, beam)


def pan_label(text, color, side="left"):
    """Label that hangs below one end of the balance beam."""
    box = RoundedRectangle(corner_radius=0.12, width=1.9, height=0.68,
                           fill_color=C_DARK, fill_opacity=1,
                           stroke_color=color, stroke_width=1.6)
    txt = Text(text, font="Arial", weight=BOLD,
               font_size=20, color=color)
    return VGroup(box, txt)


# ── Main scene ───────────────────────────────────────────────────────────────

class KhiladiKaunHain(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (2:10 – 2:55)  ~45s
        # AMERICA — four company cards slide in from the right, one by one.
        # Each card lands with a subtle bounce. Camera pans slightly right
        # as cards accumulate. Researcher dominance tag writes in below.
        # Cards then shrink to upper-left corner as context.
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("America")
        self.play(FadeIn(sec1), run_time=0.5)

        # Country label slams in, then shrinks to anchor
        usa_title = H1("USA", color=C_USER).scale(1.1).move_to(UP * 2.6)
        slam_in(self, usa_title, bounces=2, run_t=0.6)
        self.wait(0.4)
        self.play(usa_title.animate.scale(0.55).move_to(LEFT * 5.6 + UP * 2.9),
                  run_time=0.4)

        # Build four cards — centred row, slight vertical stagger
        CARD_W      = 2.6
        CARD_GAP    = 0.28
        total_w     = len(COMPANIES) * CARD_W + (len(COMPANIES) - 1) * CARD_GAP
        start_x     = -total_w / 2 + CARD_W / 2
        STAGGER_Y   = [0.18, -0.18, 0.18, -0.18]   # slight wave

        cards       = []
        card_targets = []
        for i, co in enumerate(COMPANIES):
            cx = start_x + i * (CARD_W + CARD_GAP)
            cy = STAGGER_Y[i]
            card = company_card(co["name"], co["stat"], co["color"])
            # Start off-screen right
            card.move_to(RIGHT * 9 + UP * cy)
            cards.append(card)
            card_targets.append((cx, cy))
            self.add(card)

        # Slide in one by one with LaggedStart
        self.play(
            LaggedStart(
                *[card.animate.move_to(RIGHT * tx + UP * ty)
                  for card, (tx, ty) in zip(cards, card_targets)],
                lag_ratio=T_CARD_LAG
            ),
            run_time=T_CARD_SLIDE * len(COMPANIES) + 0.6
        )

        # Camera breathes right slightly to frame all four cards
        self.play(
            self.camera.frame.animate.scale(1.05).move_to(RIGHT * 0.3),
            run_time=0.6
        )
        self.wait(0.6)

        # Researcher tag writes in below the cards
        usa_tag = TAG(USA_TAG, color=C_DIM, size=16).move_to(DOWN * 1.55)
        self.play(AddTextLetterByLetter(usa_tag, time_per_char=0.032))
        self.wait(T_SEGMENT_HOLD)

        # Camera restore before transition
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Full clear — China gets a blank stage
        usa_group = VGroup(*cards, usa_tag, usa_title)
        self.play(
            FadeOut(usa_group),
            FadeOut(sec1),
            run_time=0.7
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (2:55 – 3:20)  ~25s
        # CHINA — population dot grid (14 cols × 10 rows = 140 dots).
        # Dots appear with LaggedStart. Then data lines radiate outward
        # from random dots — representing daily data generation.
        # Counter "1.4B" slams in. Labs tag fades in.
        # ══════════════════════════════════════════════════════════════════

        sec2 = corner_lbl("China")
        self.play(FadeIn(sec2), run_time=0.4)

        chn_title = H1("China", color=C_HOT1).scale(1.1).move_to(UP * 2.6)
        slam_in(self, chn_title, bounces=2, run_t=0.6)
        self.wait(0.3)
        self.play(chn_title.animate.scale(0.55).move_to(LEFT * 5.6 + UP * 2.9),
                  run_time=0.4)

        # Dot grid — 14 cols × 10 rows
        DCOLS, DROWS  = 14, 10
        DOT_STEP_X    = 0.72
        DOT_STEP_Y    = 0.58
        DOT_R         = 0.072
        rng           = np.random.default_rng(7)

        grid_dots = VGroup()
        dot_positions = []
        for r in range(DROWS):
            for c in range(DCOLS):
                x = (c - DCOLS / 2 + 0.5) * DOT_STEP_X
                y = (r - DROWS / 2 + 0.5) * DOT_STEP_Y + 0.2
                dot = Circle(radius=DOT_R,
                             fill_color=C_HOT1, fill_opacity=0,
                             stroke_width=0).move_to(RIGHT * x + UP * y)
                grid_dots.add(dot)
                dot_positions.append(np.array([x, y, 0]))

        # Appear left-to-right, top-to-bottom
        self.play(
            LaggedStart(
                *[dot.animate.set_fill(opacity=rng.uniform(0.45, 0.90))
                  for dot in grid_dots],
                lag_ratio=T_DOT_LAG
            ),
            run_time=2.2
        )
        self.wait(0.4)

        # Data lines radiate from ~20 random dots outward
        # Lines shoot out to random directions and fade
        line_sources = rng.choice(len(dot_positions), size=22, replace=False)
        data_lines   = VGroup()
        for idx in line_sources:
            src  = dot_positions[idx]
            angle = rng.uniform(0, TAU)
            length = rng.uniform(0.55, 1.4)
            end  = src + length * np.array([np.cos(angle), np.sin(angle), 0])
            ln   = Line(src, end, color=C_INFRA,
                        stroke_width=1.2, stroke_opacity=0)
            data_lines.add(ln)

        self.play(
            LaggedStart(
                *[ln.animate.set_stroke(opacity=rng.uniform(0.35, 0.75))
                  for ln in data_lines],
                lag_ratio=T_LINE_LAG
            ),
            run_time=1.4
        )

        # Ripple pulses from centre of grid — data pulsing outward
        ripple(self, UP * 0.2, color=C_HOT1, n=4, base_r=0.4, run_t=0.8)
        self.wait(0.3)

        # "1.4B" stat slams in — overlaid centre of grid
        pop_stat = STAT(CHINA_POP, color=C_STAT).move_to(UP * 0.2)
        # Dark backing so stat is readable over the dots
        pop_bg   = Rectangle(width=3.2, height=1.2,
                             fill_color=C_BG, fill_opacity=0.78,
                             stroke_width=0).move_to(UP * 0.2)
        self.add(pop_bg)
        slam_in(self, pop_stat, bounces=2, run_t=0.7)

        # Labs pill below
        labs_pill = pill_label(f"Labs: {CHINA_LABS}", color=C_HOT1, text_size=18)
        labs_pill.move_to(DOWN * 1.55)
        self.play(FadeIn(labs_pill, shift=UP * 0.2), run_time=0.5)

        # China tag writes in
        chn_tag = TAG(CHINA_TAG, color=C_DIM, size=15).move_to(DOWN * 2.05)
        self.play(AddTextLetterByLetter(chn_tag, time_per_char=0.030))
        self.wait(T_SEGMENT_HOLD)

        # Full clear — Europe gets a blank stage
        china_group = VGroup(grid_dots, data_lines, pop_stat, pop_bg,
                             labs_pill, chn_tag, chn_title)
        self.play(
            FadeOut(china_group),
            FadeOut(sec2),
            run_time=0.7
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 3  (3:20 – 3:45)  ~25s
        # EUROPE — a balance / scale.
        # Beam starts level. "Innovation" pan on left, "Regulation" on right.
        # EU AI Act label appears. Beam tips RIGHT (regulation wins).
        # Tag line "Wisdom? Or biggest mistake?" writes in below.
        # ══════════════════════════════════════════════════════════════════

        sec3 = corner_lbl("Europe")
        self.play(FadeIn(sec3), run_time=0.4)

        eu_title = H1("Europe", color=C_INFRA).scale(1.1).move_to(UP * 2.6)
        slam_in(self, eu_title, bounces=2, run_t=0.6)
        self.wait(0.3)
        self.play(eu_title.animate.scale(0.55).move_to(UP * 2.85),
                  run_time=0.4)

        # Build balance — pivot at ORIGIN, beam horizontal
        scale_group = balance_beam(beam_len=5.0, color=C_GRID)
        pivot, beam = scale_group

        self.play(
            FadeIn(pivot, scale=0.05, rate_func=rush_into),
            run_time=0.5
        )
        self.play(
            Create(beam, run_time=0.7, rate_func=smooth)
        )

        # Left pan — Innovation
        pan_l = pan_label(EU_LEFT, color=C_GPT, side="left")
        pan_l.move_to(LEFT * 2.4 + DOWN * 0.85)
        # Right pan — Regulation
        pan_r = pan_label(EU_RIGHT, color=C_SPEED, side="right")
        pan_r.move_to(RIGHT * 2.4 + DOWN * 0.85)

        # Hanging lines from beam ends to pans
        hang_l = Line(LEFT * 2.5 + UP * 0.18, LEFT * 2.5 + DOWN * 0.52,
                      color=C_GRID, stroke_width=1.6)
        hang_r = Line(RIGHT * 2.5 + UP * 0.18, RIGHT * 2.5 + DOWN * 0.52,
                      color=C_GRID, stroke_width=1.6)

        self.play(
            Create(hang_l), Create(hang_r),
            run_time=0.5
        )
        self.play(
            FadeIn(pan_l, shift=DOWN * 0.15),
            FadeIn(pan_r, shift=DOWN * 0.15),
            run_time=0.6
        )
        self.wait(0.7)

        # EU AI Act label writes in above the beam centre
        eu_act = TAG(EU_ACT, color=C_INFRA, size=17).move_to(UP * 0.82)
        self.play(AddTextLetterByLetter(eu_act, time_per_char=0.04))
        self.wait(0.5)

        # Camera punch-in on the balance
        self.play(
            self.camera.frame.animate.scale(0.78).move_to(DOWN * 0.1),
            run_time=0.6
        )

        # Beam tips RIGHT — regulation side drops
        # Achieved by rotating the entire beam+hangs+pans group
        tilt_group = VGroup(beam, hang_l, hang_r, pan_l, pan_r)
        self.play(
            Rotate(tilt_group, angle=-18 * DEGREES,
                   about_point=ORIGIN + UP * 0.18),
            run_time=1.1, rate_func=there_and_back_with_pause
        )

        # Hold tilted — then settle back to slight tilt (regulation wins)
        self.play(
            Rotate(tilt_group, angle=-10 * DEGREES,
                   about_point=ORIGIN + UP * 0.18),
            run_time=0.9, rate_func=smooth
        )
        self.wait(0.5)

        # Restore camera
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Wisdom / mistake tags appear under respective pans
        tag_r = TAG(EU_TAG_R, color=C_GPT,   size=15).move_to(LEFT  * 2.4 + DOWN * 2.05)
        tag_l = TAG(EU_TAG_L, color=C_SPEED, size=15).move_to(RIGHT * 2.4 + DOWN * 2.05)
        self.play(
            FadeIn(tag_r, shift=UP * 0.12),
            FadeIn(tag_l, shift=UP * 0.12),
            run_time=0.6
        )
        self.wait(T_BALANCE_HOLD)

        # ── End fade ──
        eu_group = VGroup(scale_group, tilt_group, eu_act,
                          tag_l, tag_r, eu_title)
        self.play(
            FadeOut(eu_group),
            FadeOut(sec3),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()