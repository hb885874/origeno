"""
scene1.py — "The Question Returns"
Origeno Educational Video Channel
Style: Oversimplified | Duration: 45s | Resolution: 1080p | FPS: 30

Fixes applied v4:
  - All Hindi text replaced with English
  - Emoji-style character in Beat 2
  - Beat 4: stamp top-left, icons lower arc — zero overlap
  - Beat 3: img_world_network.png background (fallback: dot map)
  - Beat 2: india_map.svg loaded via SVGMobject (fallback: simple outline)

HOW TO USE THE SVG:
  1. Get a clean single-fill India silhouette SVG from SVGRepo / Wikimedia
  2. Save it as  india_map.svg  in the same folder as this script
  3. Manim will auto-load and style it.  If the file is missing, a simple
     rounded rectangle placeholder is shown instead — no crash.
"""

from manim import *
import numpy as np
import os

# ─────────────────────────────────────────────
# GLOBAL PALETTE & CONFIG
# ─────────────────────────────────────────────
BG       = "#F5F0E8"
RED      = "#D42B2B"
BLUE     = "#2255AA"
GOLD     = "#C8960C"
GREEN    = "#2A7A2A"
DARK     = "#1A1A1A"
SOFT_GRY = "#888888"
WHITE_OP = "#FFFFFF"
SKIN     = "#F5C97A"

config.background_color = BG
config.pixel_width  = 1920
config.pixel_height = 1080
config.frame_rate   = 60

# ─────────────────────────────────────────────
# ASSET PATHS
# Folder structure:
#   scene1.py
#   asset/
#       img_world_network.png
#       india_map.svg
# ─────────────────────────────────────────────
SCRIPT_DIR        = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR         = os.path.join(SCRIPT_DIR, "asset")
IMG_WORLD_NETWORK = os.path.join(ASSET_DIR, "img_world_network.png")
SVG_INDIA_MAP     = os.path.join(ASSET_DIR, "india_map.svg")

# ─────────────────────────────────────────────
# WORLD DOT-MAP
# ─────────────────────────────────────────────
WORLD_DOTS = [
    # North America
    (-5.5, 1.8), (-5.0, 2.2), (-4.5, 2.5), (-4.0, 2.7), (-3.5, 2.5),
    (-5.8, 1.2), (-5.2, 1.2), (-4.6, 1.2), (-4.0, 1.3),
    (-5.0, 0.5), (-4.2, 0.5), (-3.5, 0.8),
    # South America
    (-4.0, -0.5), (-3.8, -1.0), (-3.6, -1.5), (-3.8, -2.0), (-4.2, -2.5),
    # Europe
    (-0.3, 2.2), (0.0, 2.5), (0.5, 2.7), (1.0, 2.5), (1.3, 2.2),
    (-0.2, 1.8), (0.4, 1.8), (0.9, 1.8),
    # Africa
    (0.2, 0.8), (0.7, 0.5), (0.4, 0.0), (0.6, -0.5), (0.3, -1.2),
    # Asia
    (2.0, 2.5), (2.8, 2.8), (3.5, 2.5), (4.0, 2.0), (4.5, 2.5),
    (2.5, 1.8), (3.2, 1.5), (4.0, 1.5), (4.8, 1.5),
    (2.8, 0.8), (3.5, 0.5), (4.2, 0.8), (5.0, 0.5),
    # SE Asia / Oceania
    (4.5, 0.0), (4.8, -0.5), (5.2, -1.2), (5.5, -2.0),
    # India cluster
    (3.2, 0.9), (3.4, 0.5), (3.3, 0.2),
]

# Country anchor positions (Manim frame coords)
INDIA_POS  = np.array([3.30,  0.50, 0])
USA_POS    = np.array([-4.80, 1.60, 0])
CHINA_POS  = np.array([4.20,  1.50, 0])
TAIWAN_POS = np.array([4.75,  1.20, 0])


# ═══════════════════════════════════════════════
# PROP BUILDERS
# ═══════════════════════════════════════════════

def make_world_dots(dot_color=SOFT_GRY, radius=0.06, opacity=1.0) -> VGroup:
    dots = VGroup()
    for (x, y) in WORLD_DOTS:
        d = Dot(point=np.array([x, y, 0]), radius=radius, color=dot_color)
        d.set_opacity(opacity)
        dots.add(d)
    return dots


def make_chip(size=0.9, color=BLUE) -> VGroup:
    body = RoundedRectangle(
        corner_radius=0.08, width=size, height=size,
        fill_color=color, fill_opacity=1,
        stroke_color=WHITE_OP, stroke_width=2)
    grid = VGroup()
    for i in [-size*0.20, 0, size*0.20]:
        grid.add(Line([i, -size/2+0.12, 0], [i,  size/2-0.12, 0],
                      stroke_color=WHITE_OP, stroke_width=1, stroke_opacity=0.45))
        grid.add(Line([-size/2+0.12, i, 0], [size/2-0.12, i, 0],
                      stroke_color=WHITE_OP, stroke_width=1, stroke_opacity=0.45))
    pins = VGroup()
    for y_off in [-size*0.24, 0, size*0.24]:
        for sign in [-1, 1]:
            pins.add(Line(
                [sign*size/2,           y_off, 0],
                [sign*(size/2 + 0.18),  y_off, 0],
                stroke_color=GOLD, stroke_width=3))
    return VGroup(body, grid, pins)


def make_factory(size=0.9) -> VGroup:
    base = Rectangle(
        width=size, height=size*0.55,
        fill_color=DARK, fill_opacity=1,
        stroke_color=SOFT_GRY, stroke_width=1.5)
    base.move_to([0, -size*0.10, 0])
    ch1 = Rectangle(width=size*0.13, height=size*0.38,
                    fill_color=DARK, fill_opacity=1,
                    stroke_color=SOFT_GRY, stroke_width=1
                    ).move_to([-size*0.28, size*0.27, 0])
    ch2 = Rectangle(width=size*0.13, height=size*0.28,
                    fill_color=DARK, fill_opacity=1,
                    stroke_color=SOFT_GRY, stroke_width=1
                    ).move_to([size*0.28, size*0.22, 0])
    smoke = Arc(radius=0.11, start_angle=PI/2, angle=PI,
                stroke_color=SOFT_GRY, stroke_width=1.5, stroke_opacity=0.5
                ).move_to([-size*0.28+0.11, size*0.50, 0])
    return VGroup(base, ch1, ch2, smoke)


def make_globe(radius=0.45) -> VGroup:
    circle = Circle(radius=radius, stroke_color=BLUE,
                    stroke_width=3, fill_color="#D0E4FF", fill_opacity=0.30)
    lats = VGroup()
    for frac in [0.5, 0.25, -0.25, -0.5]:
        r_lat = radius * np.sqrt(max(0.0, 1.0 - frac**2))
        if r_lat > 0.02:
            lats.add(Arc(radius=r_lat, start_angle=0, angle=TAU,
                         stroke_color=BLUE, stroke_width=1,
                         stroke_opacity=0.4).move_to([0, frac*radius, 0]))
    lons = VGroup()
    for angle in [0, PI/3, 2*PI/3]:
        e = Ellipse(width=0.4*radius, height=2*radius,
                    stroke_color=BLUE, stroke_width=1,
                    stroke_opacity=0.4, fill_opacity=0)
        e.rotate(angle)
        lons.add(e)
    return VGroup(circle, lats, lons)


def make_gear(radius=0.38, teeth=8) -> VGroup:
    outer  = Circle(radius=radius, fill_color=GOLD,
                    fill_opacity=0.65, stroke_color=GOLD, stroke_width=2)
    inner  = Circle(radius=radius*0.50, fill_color=GOLD,
                    fill_opacity=1, stroke_width=0)
    teeth_g = VGroup()
    for i in range(teeth):
        angle = i * TAU / teeth
        tooth = Rectangle(width=radius*0.22, height=radius*0.30,
                          fill_color=GOLD, fill_opacity=1, stroke_width=0)
        tooth.move_to([np.cos(angle)*(radius+0.10),
                       np.sin(angle)*(radius+0.10), 0])
        tooth.rotate(angle)
        teeth_g.add(tooth)
    return VGroup(outer, inner, teeth_g)


def make_dollar() -> VGroup:
    circle = Circle(radius=0.36, fill_color=GREEN,
                    fill_opacity=1, stroke_width=0)
    sign   = Text("$", font="Georgia", font_size=28, color=WHITE_OP, weight=BOLD)
    return VGroup(circle, sign)


# ── EMOJI-STYLE CHARACTER ────────────────────────────────────────────────────
def make_character_curious(scale=1.0) -> VGroup:
    """
    Flat Oversimplified-style character.
    Head + body + limbs + question-mark speech bubble. No external files needed.
    """
    g = VGroup()

    # Torso
    body = RoundedRectangle(
        corner_radius=0.12, width=0.52*scale, height=0.55*scale,
        fill_color=BLUE, fill_opacity=1, stroke_width=0)
    body.move_to([0, -0.28*scale, 0])
    g.add(body)

    # Head
    head = Circle(radius=0.26*scale,
                  fill_color=SKIN, fill_opacity=1, stroke_width=0)
    head.move_to([0, 0.28*scale, 0])
    g.add(head)

    # Eyes
    eye_l = Dot([-0.09*scale, 0.32*scale, 0], radius=0.05*scale, color=DARK)
    eye_r = Dot([ 0.09*scale, 0.32*scale, 0], radius=0.05*scale, color=DARK)
    g.add(eye_l, eye_r)

    # Raised left eyebrow (curious)
    brow = Arc(radius=0.08*scale, start_angle=PI*0.15, angle=PI*0.65,
               stroke_color=DARK, stroke_width=int(2*scale+1)
               ).move_to([-0.09*scale, 0.41*scale, 0])
    g.add(brow)

    # Open mouth
    mouth = Arc(radius=0.06*scale, start_angle=-PI*0.75, angle=PI*1.5,
                stroke_color=DARK, stroke_width=int(2*scale+1)
                ).move_to([0, 0.18*scale, 0])
    g.add(mouth)

    # Right arm — raised toward chip
    arm_r = ArcBetweenPoints(
        np.array([ 0.26*scale, -0.10*scale, 0]),
        np.array([ 0.62*scale,  0.22*scale, 0]),
        angle=-PI/4,
        stroke_color=SKIN, stroke_width=int(6*scale+1))
    g.add(arm_r)

    # Left arm — relaxed down
    arm_l = Line(
        [-0.26*scale, -0.10*scale, 0],
        [-0.38*scale, -0.50*scale, 0],
        stroke_color=SKIN, stroke_width=int(6*scale+1))
    g.add(arm_l)

    # Legs
    leg_l = Line([-0.13*scale, -0.55*scale, 0],
                 [-0.18*scale, -0.90*scale, 0],
                 stroke_color=BLUE, stroke_width=int(6*scale+1))
    leg_r = Line([ 0.13*scale, -0.55*scale, 0],
                 [ 0.18*scale, -0.90*scale, 0],
                 stroke_color=BLUE, stroke_width=int(6*scale+1))
    g.add(leg_l, leg_r)

    # Speech bubble with "?"
    bubble = RoundedRectangle(
        corner_radius=0.10, width=0.42*scale, height=0.38*scale,
        fill_color=WHITE_OP, fill_opacity=0.95,
        stroke_color=DARK, stroke_width=1.5)
    bubble.move_to([0.56*scale, 0.56*scale, 0])
    q_mark = Text("?", font="Georgia", font_size=int(22*scale),
                  color=RED, weight=BOLD)
    q_mark.move_to(bubble.get_center())
    tail = Polygon(
        [0.38*scale, 0.43*scale, 0],
        [0.50*scale, 0.38*scale, 0],
        [0.46*scale, 0.52*scale, 0],
        fill_color=WHITE_OP, fill_opacity=0.95, stroke_width=0)
    g.add(tail, bubble, q_mark)

    return g


# ═══════════════════════════════════════════════
# MAIN SCENE
# ═══════════════════════════════════════════════
class Scene1(MovingCameraScene):

    def _reset_camera(self):
        """Instantly snap camera back to default — no animation."""
        self.camera.frame.move_to(ORIGIN)
        self.camera.frame.set(width=14.22)

    def construct(self):
        self._beat1()
        self._beat2()
        self._beat3()
        self._beat4()
        self._beat5()

    # ──────────────────────────────────────────
    # BEAT 1  ·  0 → 8s  ·  Callback Setup
    # ──────────────────────────────────────────
    def _beat1(self):
        black_rect = Rectangle(
            width=20, height=12,
            fill_color=BLACK, fill_opacity=1, stroke_width=0)
        self.add(black_rect)

        ghost_dots = make_world_dots(dot_color=SOFT_GRY, radius=0.05, opacity=0.12)
        ghost_chip = make_chip(size=0.8, color=BLUE)
        ghost_chip.set_opacity(0.15).move_to(ORIGIN)
        taiwan_ghost = Dot(TAIWAN_POS, radius=0.14, color=RED).set_opacity(0.18)

        recall_text = Text(
            "A question...", font="Georgia",
            font_size=52, color=DARK, weight=BOLD, slant=ITALIC)
        recall_text.move_to(UP * 0.7).set_opacity(0)

        narr1 = Text(
            "In the last episode... we left a question hanging.",
            font="Georgia", font_size=22, color=SOFT_GRY, slant=ITALIC)
        narr1.to_edge(DOWN, buff=0.45).set_opacity(0)

        self.play(
            FadeOut(black_rect,   run_time=1.6),
            FadeIn(ghost_dots,    run_time=2.0),
            FadeIn(ghost_chip,    run_time=2.0),
            FadeIn(taiwan_ghost,  run_time=2.0),
        )
        self.play(
            FadeIn(recall_text, run_time=0.7),
            FadeIn(narr1,       run_time=0.7),
        )
        self.play(
            self.camera.frame.animate.scale(0.90).shift(UP * 0.15),
            run_time=3.8,
        )
        self.wait(0.2)
        self.play(
            FadeOut(ghost_dots), FadeOut(ghost_chip),
            FadeOut(taiwan_ghost), FadeOut(recall_text), FadeOut(narr1),
            run_time=0.8,
        )

    # ──────────────────────────────────────────
    # BEAT 2  ·  8 → 18s  ·  Core Question
    # ──────────────────────────────────────────
    def _beat2(self):
        self._reset_camera()

        # ── India map — SVGMobject with fallback ──────────────────────────
        if os.path.exists(SVG_INDIA_MAP):
            india_poly = SVGMobject(SVG_INDIA_MAP)
            # Force flat fill: GOLD fill, matching stroke, no internal sub-paths visible
            india_poly.set_fill(GOLD, opacity=0.80)
            india_poly.set_stroke(GOLD, width=2.0)
            # Scale to a good display height (~3 Manim units tall)
            india_poly.set_height(3.2)
        else:
            # Fallback: simple rounded rectangle as placeholder
            india_poly = RoundedRectangle(
                corner_radius=0.3, width=2.0, height=3.2,
                fill_color=GOLD, fill_opacity=0.30,
                stroke_color=GOLD, stroke_width=2.5)
        india_poly.move_to([-1.8, 0.1, 0])

        chip = make_chip(size=0.75, color=BLUE)
        chip.move_to(india_poly.get_center())

        pulse = Circle(radius=0.55, stroke_color=BLUE,
                       stroke_width=3, stroke_opacity=0.7, fill_opacity=0)
        pulse.move_to(chip.get_center())

        trace_l = Line(chip.get_left(),  chip.get_left()  + LEFT*0.5,
                       stroke_color=BLUE, stroke_width=2)
        trace_r = Line(chip.get_right(), chip.get_right() + RIGHT*0.5,
                       stroke_color=GOLD, stroke_width=2)

        # Emoji-style curious character
        character = make_character_curious(scale=1.0)
        character.move_to([1.6, -0.35, 0])

        q_text = Text(
            "Can India build\nits own chips?",
            font="Georgia", font_size=38, color=DARK, weight=BOLD,
            line_spacing=1.2)
        q_text.move_to([4.2, 0.5, 0])

        narr2 = Text("Can India build its own chips?",
                     font="Georgia", font_size=22, color=SOFT_GRY, slant=ITALIC)
        narr2.to_edge(DOWN, buff=0.45)

        self.play(DrawBorderThenFill(india_poly, run_time=1.6))
        self.play(
            FadeIn(chip,      scale=0.5, run_time=0.6),
            FadeIn(character, scale=0.4, run_time=0.9),
            FadeIn(q_text,              run_time=0.9),
            FadeIn(narr2,               run_time=0.7),
        )
        pulse_copy = pulse.copy()
        self.add(pulse_copy)
        self.play(
            pulse_copy.animate.scale(1.9).set_opacity(0),
            Create(trace_l, run_time=0.5),
            Create(trace_r, run_time=0.5),
            run_time=0.8,
        )
        self.remove(pulse_copy)

        # Character bob animation
        self.play(
            character.animate.shift(UP * 0.12),
            run_time=0.35, rate_func=there_and_back,
        )
        self.play(
            self.camera.frame.animate.scale(0.88).shift(LEFT * 0.4),
            run_time=5.0,
        )
        self.wait(0.4)
        self.play(
            FadeOut(india_poly), FadeOut(chip),
            FadeOut(trace_l),    FadeOut(trace_r),
            FadeOut(character),  FadeOut(q_text), FadeOut(narr2),
            run_time=0.6,
        )

    # ──────────────────────────────────────────
    # BEAT 3  ·  18 → 28s  ·  Stakes Expansion
    # img_world_network.png as background (fallback: dot map)
    # ──────────────────────────────────────────
    def _beat3(self):
        self._reset_camera()

        # Background image
        if os.path.exists(IMG_WORLD_NETWORK):
            bg_img = ImageMobject(IMG_WORLD_NETWORK)
            bg_img.set_width(14.5)
            bg_img.set_opacity(0.22)
            bg_img.move_to(ORIGIN)
            self.add(bg_img)
        else:
            bg_img = make_world_dots(dot_color=SOFT_GRY, radius=0.052, opacity=0.50)
            self.add(bg_img)

        usa_dot    = Dot(USA_POS,    radius=0.24, color=RED,  fill_opacity=0.88)
        china_dot  = Dot(CHINA_POS,  radius=0.24, color=RED,  fill_opacity=0.88)
        taiwan_dot = Dot(TAIWAN_POS, radius=0.18, color=GOLD, fill_opacity=0.92)
        india_dot  = Dot(INDIA_POS,  radius=0.22, color=BLUE, fill_opacity=0.55)

        usa_lbl    = Text("USA",    font="Georgia", font_size=19, color=RED,  weight=BOLD).next_to(usa_dot,    UP,   buff=0.12)
        china_lbl  = Text("China",  font="Georgia", font_size=19, color=RED,  weight=BOLD).next_to(china_dot,  UP,   buff=0.12)
        taiwan_lbl = Text("Taiwan", font="Georgia", font_size=16, color=GOLD, weight=BOLD).next_to(taiwan_dot, UR,   buff=0.08)
        india_lbl  = Text("India",  font="Georgia", font_size=19, color=BLUE, weight=BOLD).next_to(india_dot,  DOWN, buff=0.12)

        arc_tw_usa = CurvedArrow(TAIWAN_POS, USA_POS,
                                 angle=-TAU/9,
                                 stroke_color=GOLD, stroke_width=1.8,
                                 stroke_opacity=0.45, tip_length=0.16)
        arc_tw_eu  = CurvedArrow(TAIWAN_POS, np.array([0.5, 2.5, 0]),
                                 angle=-TAU/12,
                                 stroke_color=GOLD, stroke_width=1.2,
                                 stroke_opacity=0.30, tip_length=0.13)

        stakes_text = Text(
            "Compete?   Cost?",
            font="Georgia", font_size=48, color=DARK, weight=BOLD)
        stakes_text.move_to([0, -2.5, 0])

        narr3 = Text(
            "Can it really compete in this race... and if not... what is the cost?",
            font="Georgia", font_size=21, color=SOFT_GRY, slant=ITALIC)
        narr3.to_edge(DOWN, buff=0.45)

        self.play(
            FadeIn(usa_dot),   FadeIn(china_dot),
            FadeIn(taiwan_dot), FadeIn(india_dot),
            FadeIn(usa_lbl),   FadeIn(china_lbl),
            FadeIn(taiwan_lbl), FadeIn(india_lbl),
            run_time=1.0,
        )
        self.play(
            Create(arc_tw_usa, run_time=1.0),
            Create(arc_tw_eu,  run_time=1.0),
        )
        self.play(
            FadeIn(stakes_text, run_time=0.7),
            FadeIn(narr3,       run_time=0.6),
        )
        self.play(
            self.camera.frame.animate.shift(RIGHT * 0.9),
            run_time=5.0,
        )
        self.wait(0.4)
        self.play(
            FadeOut(bg_img),
            *[FadeOut(m) for m in [
                usa_dot, china_dot, taiwan_dot, india_dot,
                usa_lbl, china_lbl, taiwan_lbl, india_lbl,
                arc_tw_usa, arc_tw_eu, stakes_text, narr3,
            ]],
            run_time=0.7,
        )

    # ──────────────────────────────────────────
    # BEAT 4  ·  28 → 36s  ·  Answer Twist
    # Stamp: top-left corner | Icons: lower arc ring — no overlap
    # ──────────────────────────────────────────
    def _beat4(self):
        self._reset_camera()

        # Chip — centred slightly above middle to leave room below for icons
        chip = make_chip(size=1.1, color=BLUE)
        chip.move_to([0, 0.3, 0])
        self.play(FadeIn(chip, scale=0.5, run_time=0.6))

        # ── STAMP pinned to top-left corner — never overlaps icons ──
        stamp = Text("NOT SIMPLE", font="Georgia",
                     font_size=62, color=RED, weight=BOLD)
        stamp.to_corner(UL, buff=0.45)

        # Fly in from off-screen above
        stamp_offscreen = stamp.copy().shift(UP * 3.5)
        self.add(stamp_offscreen)
        self.play(
            stamp_offscreen.animate.move_to(stamp.get_center()),
            run_time=0.40,
        )
        self.remove(stamp_offscreen)
        self.add(stamp)

        # Chip glitch
        for _ in range(3):
            self.play(chip.animate.set_fill(RED,  opacity=0.9), run_time=0.06)
            self.play(chip.animate.set_fill(BLUE, opacity=1.0), run_time=0.06)

        # ── ICONS in lower arc ring (y = -1.5 to -2.4) ──
        #    Stamp top ~+2.8, icons bottom ~-1.5 → clear separation
        icon_data = [
            (make_factory(size=0.72), (-4.0, -1.6), "Factory"),
            (make_gear(radius=0.34),  (-1.8, -2.2), "R&D"),
            (make_dollar(),           ( 0.0, -2.5), "Capital"),
            (make_globe(radius=0.34), ( 1.8, -2.2), "Markets"),
            (make_chip(size=0.52, color=GOLD), (4.0, -1.6), "Chip IP"),
        ]

        icons_group  = VGroup()
        labels_group = VGroup()
        for ico, (x, y), lbl in icon_data:
            ico.move_to([x, y, 0]).set_opacity(0)
            icons_group.add(ico)
            t = Text(lbl, font="Georgia", font_size=16, color=DARK)
            t.move_to([x, y - 0.62, 0]).set_opacity(0)
            labels_group.add(t)

        narr4 = Text("The answer... is not simple.",
                     font="Georgia", font_size=22, color=SOFT_GRY, slant=ITALIC)
        narr4.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr4, run_time=0.4))

        self.play(
            LaggedStart(
                *[ico.animate.set_opacity(1) for ico in icons_group],
                lag_ratio=0.18, run_time=1.8,
            )
        )
        self.play(labels_group.animate.set_opacity(1), run_time=0.5)

        self.play(
            self.camera.frame.animate.scale(1.18),
            run_time=3.2,
        )
        self.wait(0.3)
        self.play(
            FadeOut(chip), FadeOut(stamp),
            FadeOut(icons_group), FadeOut(labels_group), FadeOut(narr4),
            run_time=0.5,
        )

    # ──────────────────────────────────────────
    # BEAT 5  ·  36 → 45s  ·  System Reveal
    # ──────────────────────────────────────────
    def _beat5(self):
        self._reset_camera()

        factory = make_factory(size=1.05)
        factory.move_to(ORIGIN)
        self.play(FadeIn(factory, scale=0.35, run_time=0.7))

        # "SYSTEM" stamp — pinned to top-left corner (never overlaps icons)
        # Icons live at y = 1.6..3.0 (top arc) and y = -1.2..-2.6 (bottom arc)
        # Stamp sits at top-left corner, well clear of the icon ring.
        system_stamp = Text("SYSTEM", font="Georgia",
                            font_size=68, color=BLUE, weight=BOLD)
        system_stamp.to_corner(UL, buff=0.45)
        system_stamp_start = system_stamp.copy().shift(LEFT * 6)
        self.add(system_stamp_start)
        self.play(
            system_stamp_start.animate.move_to(system_stamp.get_center()),
            run_time=0.50,
        )
        self.remove(system_stamp_start)
        self.add(system_stamp)

        world_bg = make_world_dots(dot_color=SOFT_GRY, radius=0.05, opacity=0.30)
        self.play(FadeIn(world_bg, run_time=0.8))

        # Network node icons
        node_data = [
            ((-4.2,  1.6), make_gear(radius=0.26)),
            ((-3.0,  2.4), make_chip(size=0.40, color=GOLD)),
            ((-1.5,  2.8), make_dollar()),
            (( 0.0,  3.0), make_globe(radius=0.26)),
            (( 1.5,  2.8), make_chip(size=0.40, color=RED)),
            (( 3.0,  2.4), make_factory(size=0.46)),
            (( 4.2,  1.6), make_gear(radius=0.26)),
            (( 4.0, -1.2), make_dollar()),
            (( 2.5, -2.2), make_globe(radius=0.26)),
            (( 0.0, -2.6), make_chip(size=0.40, color=BLUE)),
            ((-2.5, -2.2), make_factory(size=0.46)),
            ((-4.0, -1.2), make_gear(radius=0.26)),
        ]

        nodes = VGroup()
        for (x, y), ico in node_data:
            ico.scale(0.72).move_to([x, y, 0])
            nodes.add(ico)

        arcs = VGroup()
        for ico in nodes:
            arcs.add(Line(
                ORIGIN, ico.get_center(),
                stroke_color=BLUE, stroke_width=1.3, stroke_opacity=0.38))

        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.25) for n in nodes],
                lag_ratio=0.10, run_time=2.0,
            )
        )
        self.play(
            LaggedStart(
                *[Create(a) for a in arcs],
                lag_ratio=0.07, run_time=1.4,
            )
        )

        # Single narration line at bottom — no duplicate sub_text
        narr5 = Text(
            "Building chips is not just building a factory. It's building a system.",
            font="Georgia", font_size=22, color=SOFT_GRY, slant=ITALIC)
        narr5.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(narr5, run_time=0.6))
        self.play(
            self.camera.frame.animate.scale(1.14),
            run_time=4.0,
        )
        self.wait(0.5)

        # Fade to black
        black_out = Rectangle(
            width=30, height=18,
            fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(black_out)
        self.play(black_out.animate.set_fill(opacity=1), run_time=1.0)
        self.wait(0.2)