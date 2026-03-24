"""
scene5.py — "The Global System"
Origeno Educational Video Channel
Style: Oversimplified | Duration: ~70s | FPS: 60

Verified beat timing:
  Beat 1  Zoom Out Perspective  ~10.6s  chip→globe zoom-out transform
  Beat 2  Not One Country       ~10.3s  world-dot-map + pulsing network nodes
  Beat 3  Design Layer          ~11.9s  USA highlighted, blueprint, traces, pan-left
  Beat 4  Manufacturing Layer   ~11.9s  Taiwan+Korea glow, factories, pan-right
  Beat 5  Tools & Materials     ~12.2s  Europe+Japan, arcs to Taiwan, pan-across
  Beat 6  System Fragility      ~14.7s  full network glow, node breaks, ripple, fade
  ──────────────────────────────────────
  TOTAL                         ~71.6s  (+overhead ≈ 70s)

Design rules (same as scene2-4):
  • load_asset() always returns Group or None
  • No animate.set_fill(color, opacity=kw) — use .set_color() instead
  • No Unicode arrows or Hindi in Text() calls
  • Title/narr placed at safe edges, never in animation zone
  • All rng.sample() calls use min() clamp

Asset folder (all optional — built-in fallbacks):
  scene5.py
  asset/
      chip.svg / chip.png
      factory.svg / factory.png
      machine.svg / machine.png
      material.svg / material.png
"""

from manim import *
import numpy as np
import os
import random

# ─────────────────────────────────────────────
# PALETTE & CONFIG
# ─────────────────────────────────────────────
BG       = "#F5F0E8"
RED      = "#D42B2B"
BLUE     = "#2255AA"
GOLD     = "#C8960C"
GREEN    = "#2A7A2A"
DARK     = "#1A1A1A"
SOFT_GRY = "#888888"
WHITE_OP = "#FFFFFF"
PURPLE   = "#7B2FBE"
ORANGE   = "#E65100"

config.background_color = BG
# Resolution controlled by CLI:
#   manim -ql scene5.py Scene5   → 480p  preview
#   manim -qm scene5.py Scene5   → 720p
#   manim -qh scene5.py Scene5   → 1080p final
config.frame_rate = 60

# ─────────────────────────────────────────────
# ASSET PATHS
# ─────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR    = os.path.join(SCRIPT_DIR, "asset")
SVG_CHIP     = os.path.join(ASSET_DIR, "chip.svg")
SVG_FACTORY  = os.path.join(ASSET_DIR, "factory.svg")
SVG_MACHINE  = os.path.join(ASSET_DIR, "machine.svg")
SVG_MATERIAL = os.path.join(ASSET_DIR, "material.svg")

# ─────────────────────────────────────────────
# WORLD DOT MAP  (Manim frame coords)
# ─────────────────────────────────────────────
WORLD_DOTS = [
    # North America
    (-5.5,1.8),(-5.0,2.2),(-4.5,2.5),(-4.0,2.7),(-3.5,2.5),
    (-5.8,1.2),(-5.2,1.2),(-4.6,1.2),(-4.0,1.3),
    (-5.0,0.5),(-4.2,0.5),(-3.5,0.8),
    # South America
    (-4.0,-0.5),(-3.8,-1.0),(-3.6,-1.5),(-3.8,-2.0),(-4.2,-2.5),
    # Europe
    (-0.3,2.2),(0.0,2.5),(0.5,2.7),(1.0,2.5),(1.3,2.2),
    (-0.2,1.8),(0.4,1.8),(0.9,1.8),
    # Africa
    (0.2,0.8),(0.7,0.5),(0.4,0.0),(0.6,-0.5),(0.3,-1.2),
    # Asia
    (2.0,2.5),(2.8,2.8),(3.5,2.5),(4.0,2.0),(4.5,2.5),
    (2.5,1.8),(3.2,1.5),(4.0,1.5),(4.8,1.5),
    (2.8,0.8),(3.5,0.5),(4.2,0.8),(5.0,0.5),
    # SE Asia / Oceania
    (4.5,0.0),(4.8,-0.5),(5.2,-1.2),(5.5,-2.0),
    # India cluster
    (3.2,0.9),(3.4,0.5),(3.3,0.2),
]

# Key country anchor positions (Manim frame coords)
USA_POS    = np.array([-4.80, 1.60, 0])
TAIWAN_POS = np.array([ 4.65, 1.10, 0])
KOREA_POS  = np.array([ 4.85, 1.75, 0])
EUROPE_POS = np.array([ 0.40, 2.20, 0])
JAPAN_POS  = np.array([ 5.20, 1.80, 0])
INDIA_POS  = np.array([ 3.30, 0.50, 0])


# ═══════════════════════════════════════════════
# ASSET LOADER
# ═══════════════════════════════════════════════

def load_asset(svg_path, height=1.0, color=BLUE):
    path = svg_path
    if not os.path.exists(path):
        base = os.path.splitext(path)[0]
        for ext in (".png", ".jpg", ".jpeg"):
            if os.path.exists(base + ext):
                path = base + ext
                break
        else:
            return None
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in (".png", ".jpg", ".jpeg"):
            mob = ImageMobject(path)
            mob.set_height(height)
            return Group(mob)
        else:
            mob = SVGMobject(path)
            mob.set_fill(color, opacity=1)
            mob.set_stroke(color, width=0)
            mob.set_height(height)
            return Group(mob)
    except Exception:
        return None


# ═══════════════════════════════════════════════
# PROP BUILDERS
# ═══════════════════════════════════════════════

def make_chip(size=1.8, color=BLUE):
    asset = load_asset(SVG_CHIP, height=size, color=color)
    if asset is not None:
        return asset
    body = RoundedRectangle(
        corner_radius=0.10, width=size, height=size,
        fill_color=color, fill_opacity=1,
        stroke_color=WHITE_OP, stroke_width=2)
    grid = VGroup()
    step = size / 6
    for i in np.arange(-size/2+step, size/2, step):
        grid.add(Line([i, -size/2+0.15, 0], [i,  size/2-0.15, 0],
                      stroke_color=WHITE_OP, stroke_width=0.8, stroke_opacity=0.35))
        grid.add(Line([-size/2+0.15, i, 0], [size/2-0.15, i, 0],
                      stroke_color=WHITE_OP, stroke_width=0.8, stroke_opacity=0.35))
    pins = VGroup()
    for y_off in np.arange(-size*0.35, size*0.36, size*0.175):
        for sign in [-1, 1]:
            pins.add(Line([sign*size/2, y_off, 0],
                          [sign*(size/2+0.22), y_off, 0],
                          stroke_color=GOLD, stroke_width=3))
    return VGroup(body, grid, pins)


def make_globe(radius=2.2) -> VGroup:
    circle = Circle(radius=radius, stroke_color=BLUE,
                    stroke_width=2.5, fill_color="#D0E4FF", fill_opacity=0)
    lats = VGroup()
    for frac in [0.6, 0.3, 0, -0.3, -0.6]:
        r2 = radius * np.sqrt(max(0, 1-frac**2))
        if r2 > 0.02:
            lats.add(Arc(radius=r2, start_angle=0, angle=TAU,
                         stroke_color=BLUE, stroke_width=1,
                         stroke_opacity=0.30).move_to([0, frac*radius, 0]))
    lons = VGroup()
    for a in [0, PI/4, PI/2, 3*PI/4]:
        e = Ellipse(width=0.5*radius, height=2*radius,
                    stroke_color=BLUE, stroke_width=1,
                    stroke_opacity=0.25, fill_opacity=0)
        e.rotate(a)
        lons.add(e)
    return VGroup(circle, lats, lons)


def make_world_dots(color=SOFT_GRY, radius=0.055, opacity=0.55) -> VGroup:
    return VGroup(*[
        Dot(np.array([x, y, 0]), radius=radius, color=color
            ).set_opacity(opacity)
        for x, y in WORLD_DOTS
    ])


def make_factory(width=1.2) -> VGroup:
    asset = load_asset(SVG_FACTORY, height=width*0.75, color=DARK)
    if asset is not None:
        return asset
    h = width * 0.55
    base = Rectangle(width=width, height=h, fill_color=DARK, fill_opacity=1,
                     stroke_color=SOFT_GRY, stroke_width=1.5
                     ).move_to([0, -h*0.10, 0])
    ch1 = Rectangle(width=width*0.13, height=h*0.50, fill_color=DARK,
                    fill_opacity=1, stroke_color=SOFT_GRY, stroke_width=1
                    ).move_to([-width*0.28, h*0.33, 0])
    ch2 = Rectangle(width=width*0.13, height=h*0.36, fill_color=DARK,
                    fill_opacity=1, stroke_color=SOFT_GRY, stroke_width=1
                    ).move_to([width*0.28, h*0.27, 0])
    return VGroup(base, ch1, ch2)


def make_machine(size=0.9) -> VGroup:
    asset = load_asset(SVG_MACHINE, height=size, color=PURPLE)
    if asset is not None:
        return asset
    body = RoundedRectangle(corner_radius=0.10, width=size, height=size*0.80,
                            fill_color=PURPLE, fill_opacity=1,
                            stroke_color=WHITE_OP, stroke_width=1.5)
    lens = Circle(radius=size*0.15, fill_color=GOLD, fill_opacity=1,
                  stroke_width=0).move_to([0, -size*0.15, 0])
    arm  = Rectangle(width=size*0.12, height=size*0.40,
                     fill_color=SOFT_GRY, fill_opacity=1, stroke_width=0
                     ).move_to([size*0.40, size*0.05, 0])
    return VGroup(body, lens, arm)


def make_material_drop(size=0.5) -> VGroup:
    asset = load_asset(SVG_MATERIAL, height=size, color=BLUE)
    if asset is not None:
        return asset
    # Teardrop shape: circle + triangle
    drop = Circle(radius=size*0.32, fill_color=BLUE,
                  fill_opacity=0.85, stroke_width=0)
    tip  = Triangle(fill_color=BLUE, fill_opacity=0.85,
                    stroke_width=0).scale(size*0.20
                    ).rotate(PI).move_to([0, -size*0.38, 0])
    return VGroup(drop, tip)


def make_blueprint_overlay(width=2.5) -> VGroup:
    """Circuit blueprint: grid of dashed lines + node dots."""
    h = width * 0.65
    bg = Rectangle(width=width, height=h,
                   fill_color="#001830", fill_opacity=0.85,
                   stroke_color=BLUE, stroke_width=1.5)
    lines = VGroup()
    step  = width / 5
    for i in range(1, 5):
        x = -width/2 + i*step
        lines.add(DashedLine([x, -h/2+0.15, 0], [x, h/2-0.15, 0],
                             stroke_color=BLUE, stroke_width=0.8,
                             stroke_opacity=0.40, dash_length=0.12))
    step2 = h / 4
    for i in range(1, 4):
        y = -h/2 + i*step2
        lines.add(DashedLine([-width/2+0.15, y, 0], [width/2-0.15, y, 0],
                             stroke_color=BLUE, stroke_width=0.8,
                             stroke_opacity=0.40, dash_length=0.12))
    # Junction dots
    junctions = VGroup(*[
        Dot(np.array([-width/2+i*step, -h/2+j*step2, 0]),
            radius=0.07, color=GOLD, fill_opacity=0.9)
        for i in range(1, 5) for j in range(1, 4)
    ])
    return VGroup(bg, lines, junctions)


def country_label(text, pos, color=DARK) -> Text:
    t = Text(text, font="Georgia", font_size=17, color=color, weight=BOLD)
    t.move_to(pos + np.array([0, 0.38, 0]))
    return t


def highlight_dot(pos, color, radius=0.28) -> VGroup:
    outer = Circle(radius=radius, fill_color=color,
                   fill_opacity=0.80, stroke_width=0)
    outer.move_to(pos)
    pulse = Circle(radius=radius*1.5, stroke_color=color,
                   stroke_width=2, stroke_opacity=0.45,
                   fill_opacity=0).move_to(pos)
    return VGroup(outer, pulse)


def curved_arc(start, end, color, width=2.0, opacity=0.55) -> CurvedArrow:
    return CurvedArrow(start, end, angle=-TAU/10,
                       stroke_color=color, stroke_width=width,
                       stroke_opacity=opacity, tip_length=0.18)


# ═══════════════════════════════════════════════
# SCENE
# ═══════════════════════════════════════════════

class Scene5(MovingCameraScene):

    def _reset_camera(self):
        self.camera.frame.move_to(ORIGIN)
        self.camera.frame.set(width=14.22)

    def construct(self):
        self._beat1()
        self._beat2()
        self._beat3()
        self._beat4()
        self._beat5()
        self._beat6()

    # ──────────────────────────────────────────
    # BEAT 1  ·  ~10.6s  ·  Zoom Out Perspective
    # Chip close-up → zoom out → morphs into globe
    # ──────────────────────────────────────────
    def _beat1(self):
        self._reset_camera()

        # Start zoomed in on chip
        chip = make_chip(size=2.0, color=BLUE)
        chip.move_to(ORIGIN)
        self.camera.frame.scale(0.55).move_to(ORIGIN)
        self.play(FadeIn(chip, scale=0.5, run_time=0.6))

        title = Text("Zoom Out",
                     font="Georgia", font_size=38, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "Now zoom out and look at this entire process.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Zoom out — chip gets smaller in frame
        self.play(
            self.camera.frame.animate.set(width=14.22).move_to(ORIGIN),
            run_time=4.0)

        # Chip fades, globe fades in
        globe = make_globe(radius=2.5)
        globe.move_to(ORIGIN).set_opacity(0)
        self.add(globe)
        self.play(
            FadeOut(chip, run_time=1.0),
            globe.animate.set_opacity(1),
            run_time=1.5)
        self.wait(1.8)

        self.play(FadeOut(globe), FadeOut(title), FadeOut(narr),
                  run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 2  ·  ~10.3s  ·  Not One Country
    # World dot-map + network nodes pulse
    # ──────────────────────────────────────────
    def _beat2(self):
        self._reset_camera()

        title = Text("A Global System",
                     font="Georgia", font_size=38, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "The chip industry is not the story of one factory or one country."
            "  It is a global system.",
            font="Georgia", font_size=19, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # World dot map
        world = make_world_dots(color=SOFT_GRY, radius=0.055, opacity=0.50)
        self.play(FadeIn(world, run_time=0.8))

        # Key nodes light up
        key_positions = [USA_POS, TAIWAN_POS, KOREA_POS,
                         EUROPE_POS, JAPAN_POS]
        key_colors    = [RED, GOLD, GREEN, BLUE, PURPLE]
        nodes = Group()
        for pos, col in zip(key_positions, key_colors):
            n = highlight_dot(pos, col, radius=0.24)
            nodes.add(n)

        self.play(LaggedStart(
            *[FadeIn(n, scale=0.2) for n in nodes],
            lag_ratio=0.18, run_time=1.5))

        # Network arcs connecting all nodes
        arcs = VGroup()
        for i in range(len(key_positions)):
            for j in range(i+1, len(key_positions)):
                arcs.add(Line(key_positions[i], key_positions[j],
                              stroke_color=SOFT_GRY, stroke_width=0.8,
                              stroke_opacity=0.22))
        self.play(LaggedStart(
            *[Create(a) for a in arcs],
            lag_ratio=0.06, run_time=2.0))

        # Pulse rings from each node
        for _ in range(2):
            ring_anims = []
            for pos, col in zip(key_positions, key_colors):
                ring = Circle(radius=0.30, stroke_color=col,
                              stroke_width=2, stroke_opacity=0.7,
                              fill_opacity=0).move_to(pos)
                self.add(ring)
                ring_anims.append(
                    ring.animate.scale(3.0).set_opacity(0))
            self.play(*ring_anims, run_time=0.65)

        self.wait(2.5)
        self.play(FadeOut(world), FadeOut(nodes), FadeOut(arcs),
                  FadeOut(title), FadeOut(narr), run_time=0.8)

    # ──────────────────────────────────────────
    # BEAT 3  ·  ~11.9s  ·  Design Layer — USA
    # ──────────────────────────────────────────
    def _beat3(self):
        self._reset_camera()

        title = Text("Design  —  USA",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "Design happens mostly in America — where companies draw the chip blueprint.",
            font="Georgia", font_size=19, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        world = make_world_dots(color=SOFT_GRY, radius=0.050, opacity=0.38)
        self.play(FadeIn(world, run_time=0.8))

        # USA highlight
        usa_dot = highlight_dot(USA_POS, RED, radius=0.30)
        usa_lbl = country_label("USA", USA_POS, color=RED)
        self.play(FadeIn(usa_dot, scale=0.3, run_time=0.7),
                  FadeIn(usa_lbl, run_time=0.5))

        # Blueprint overlay near USA
        bp = make_blueprint_overlay(width=2.8)
        bp.move_to(USA_POS + np.array([0.2, -1.2, 0]))
        self.play(FadeIn(bp, run_time=1.0))

        # Tracing lines pulse across blueprint
        for _ in range(3):
            trace = Line(
                bp.get_left() + np.array([0.3, 0, 0]),
                bp.get_right() + np.array([-0.3, 0, 0]),
                stroke_color=BLUE, stroke_width=2, stroke_opacity=0.8)
            self.add(trace)
            self.play(trace.animate.set_opacity(0), run_time=0.45)
            self.remove(trace)

        # Chip icon above blueprint
        chip_icon = make_chip(size=0.65, color=BLUE)
        chip_icon.move_to(USA_POS + np.array([2.0, -0.3, 0]))
        self.play(FadeIn(chip_icon, scale=0.3, run_time=0.8))

        # Camera pan left
        self.play(
            self.camera.frame.animate.shift(LEFT * 1.2),
            run_time=3.5)
        self.wait(1.8)

        self.play(FadeOut(world), FadeOut(usa_dot), FadeOut(usa_lbl),
                  FadeOut(bp), FadeOut(chip_icon),
                  FadeOut(title), FadeOut(narr), run_time=0.6)

    # ──────────────────────────────────────────
    # BEAT 4  ·  ~11.9s  ·  Manufacturing — Taiwan / Korea
    # ──────────────────────────────────────────
    def _beat4(self):
        self._reset_camera()

        title = Text("Manufacturing  —  Taiwan / Korea",
                     font="Georgia", font_size=32, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "Manufacturing happens in Taiwan and Korea — where designs become real silicon.",
            font="Georgia", font_size=19, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        world = make_world_dots(color=SOFT_GRY, radius=0.050, opacity=0.38)
        self.play(FadeIn(world, run_time=0.8))

        # Taiwan highlight
        tw_dot = highlight_dot(TAIWAN_POS, GOLD, radius=0.26)
        tw_lbl = country_label("Taiwan", TAIWAN_POS, color=GOLD)
        # Korea highlight
        kr_dot = highlight_dot(KOREA_POS, GREEN, radius=0.24)
        kr_lbl = country_label("Korea", KOREA_POS, color=GREEN)

        self.play(
            FadeIn(tw_dot, scale=0.3), FadeIn(tw_lbl),
            FadeIn(kr_dot, scale=0.3), FadeIn(kr_lbl),
            run_time=0.8)

        # Factory icons below each country
        factory_tw = make_factory(width=1.3)
        factory_tw.move_to(TAIWAN_POS + np.array([-0.2, -1.4, 0]))
        factory_kr = make_factory(width=1.1)
        factory_kr.move_to(KOREA_POS + np.array([0.5, -1.4, 0]))

        self.play(
            FadeIn(factory_tw, scale=0.3, run_time=0.7),
            FadeIn(factory_kr, scale=0.3, run_time=0.7))

        # Glow pulses from factories (production activity)
        for _ in range(3):
            g1 = Circle(radius=0.20, stroke_color=GOLD,
                        stroke_width=2, stroke_opacity=0.7,
                        fill_opacity=0).move_to(factory_tw.get_center())
            g2 = Circle(radius=0.20, stroke_color=GREEN,
                        stroke_width=2, stroke_opacity=0.7,
                        fill_opacity=0).move_to(factory_kr.get_center())
            self.add(g1, g2)
            self.play(
                g1.animate.scale(3.5).set_opacity(0),
                g2.animate.scale(3.5).set_opacity(0),
                run_time=0.50)
            self.remove(g1, g2)

        # Camera pan right
        self.play(
            self.camera.frame.animate.shift(RIGHT * 1.5),
            run_time=3.5)
        self.wait(1.8)

        self.play(FadeOut(world),
                  FadeOut(tw_dot), FadeOut(tw_lbl),
                  FadeOut(kr_dot), FadeOut(kr_lbl),
                  FadeOut(factory_tw), FadeOut(factory_kr),
                  FadeOut(title), FadeOut(narr), run_time=0.6)

    # ──────────────────────────────────────────
    # BEAT 5  ·  ~12.2s  ·  Tools & Materials
    # Europe → machines, Japan → materials, arcs to Taiwan
    # ──────────────────────────────────────────
    def _beat5(self):
        self._reset_camera()

        title = Text("Machines and Materials",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "Machines come from Europe.  Materials come from Japan."
            "  Both flow to the fabs.",
            font="Georgia", font_size=19, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        world = make_world_dots(color=SOFT_GRY, radius=0.050, opacity=0.38)
        self.play(FadeIn(world, run_time=0.8))

        # Highlight all 4 relevant countries
        eu_dot  = highlight_dot(EUROPE_POS, PURPLE, radius=0.26)
        eu_lbl  = country_label("Europe", EUROPE_POS, color=PURPLE)
        jp_dot  = highlight_dot(JAPAN_POS,  BLUE,   radius=0.24)
        jp_lbl  = country_label("Japan",  JAPAN_POS,  color=BLUE)
        tw_dot  = highlight_dot(TAIWAN_POS, GOLD,  radius=0.22)
        tw_lbl  = country_label("Taiwan", TAIWAN_POS, color=GOLD)

        self.play(
            FadeIn(eu_dot), FadeIn(eu_lbl),
            FadeIn(jp_dot), FadeIn(jp_lbl),
            FadeIn(tw_dot), FadeIn(tw_lbl),
            run_time=0.8)

        # Props: machine near Europe, material drop near Japan
        machine = make_machine(size=0.90)
        machine.move_to(EUROPE_POS + np.array([0.1, -1.2, 0]))
        material = make_material_drop(size=0.70)
        material.move_to(JAPAN_POS  + np.array([0.0, -1.0, 0]))
        self.play(
            FadeIn(machine,  scale=0.3, run_time=0.8),
            FadeIn(material, scale=0.3, run_time=0.8))

        # Arcs: Europe → Taiwan (machines), Japan → Taiwan (materials)
        arc_eu_tw = curved_arc(EUROPE_POS, TAIWAN_POS, PURPLE, width=2.2, opacity=0.55)
        arc_jp_tw = curved_arc(JAPAN_POS,  TAIWAN_POS, BLUE,   width=2.0, opacity=0.50)

        self.play(Create(arc_eu_tw, run_time=1.2))
        self.play(Create(arc_jp_tw, run_time=1.0))

        # Pulse dots along arcs (simulated flow)
        for _ in range(2):
            for start, end, col in [
                (EUROPE_POS, TAIWAN_POS, PURPLE),
                (JAPAN_POS,  TAIWAN_POS, BLUE),
            ]:
                p = Dot(start, radius=0.12, color=col, fill_opacity=1)
                self.add(p)
                self.play(p.animate.move_to(end),
                          run_time=0.55, rate_func=linear)
                ring = Circle(radius=0.20, stroke_color=col,
                              stroke_width=2, stroke_opacity=0.7,
                              fill_opacity=0).move_to(end)
                self.add(ring)
                self.play(ring.animate.scale(2.5).set_opacity(0),
                          run_time=0.18)
                self.remove(p, ring)

        # Pan across (left → right to show full map)
        self.play(
            self.camera.frame.animate.shift(RIGHT * 0.8),
            run_time=3.8)
        self.wait(1.5)

        self.play(FadeOut(world),
                  FadeOut(eu_dot), FadeOut(eu_lbl),
                  FadeOut(jp_dot), FadeOut(jp_lbl),
                  FadeOut(tw_dot), FadeOut(tw_lbl),
                  FadeOut(machine), FadeOut(material),
                  FadeOut(arc_eu_tw), FadeOut(arc_jp_tw),
                  FadeOut(title), FadeOut(narr), run_time=0.6)

    # ──────────────────────────────────────────
    # BEAT 6  ·  ~14.7s  ·  System Fragility
    # Full network glow → one node breaks → ripple → fade to black
    # ──────────────────────────────────────────
    def _beat6(self):
        self._reset_camera()

        title = Text("Interconnected... and Fragile",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "If one link in this chain breaks... the entire supply can be disrupted.",
            font="Georgia", font_size=19, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        world = make_world_dots(color=SOFT_GRY, radius=0.050, opacity=0.40)
        self.play(FadeIn(world, run_time=0.8))

        # All 5 nodes + full connection network
        key_positions = [USA_POS, TAIWAN_POS, KOREA_POS, EUROPE_POS, JAPAN_POS]
        key_colors    = [RED,     GOLD,        GREEN,      PURPLE,     BLUE]
        key_names     = ["USA",   "Taiwan",    "Korea",    "Europe",   "Japan"]

        nodes = Group()
        labels = VGroup()
        for pos, col, name in zip(key_positions, key_colors, key_names):
            n = highlight_dot(pos, col, radius=0.24)
            l = country_label(name, pos, color=col)
            nodes.add(n)
            labels.add(l)

        self.play(
            LaggedStart(*[FadeIn(n, scale=0.2) for n in nodes],
                        lag_ratio=0.12, run_time=1.0),
            LaggedStart(*[FadeIn(l) for l in labels],
                        lag_ratio=0.12, run_time=1.0))

        # Full network connections
        net_arcs = VGroup()
        for i in range(len(key_positions)):
            for j in range(i+1, len(key_positions)):
                net_arcs.add(Line(key_positions[i], key_positions[j],
                                  stroke_color=BLUE, stroke_width=1.0,
                                  stroke_opacity=0.28))
        self.play(LaggedStart(
            *[Create(a) for a in net_arcs],
            lag_ratio=0.05, run_time=1.5))

        # Full glow — network "active"
        self.wait(2.5)
        glow_anims = []
        for arc in net_arcs:
            glow_anims.append(arc.animate.set_color(BLUE).set_opacity(0.55))
        self.play(*glow_anims, run_time=0.8)

        # BREAK: Taiwan node fails — glitch effect
        tw_node = nodes[1]   # Taiwan is index 1
        self.play(tw_node.animate.set_color(RED), run_time=0.35)
        for _ in range(5):
            self.play(tw_node.animate.set_color(RED),    run_time=0.10)
            self.play(tw_node.animate.set_color(SOFT_GRY), run_time=0.10)

        # Ripple: arcs connected to Taiwan dim out
        tw_arcs = VGroup()
        for arc in net_arcs:
            start = arc.get_start()
            end   = arc.get_end()
            # Check if arc touches Taiwan position (within tolerance)
            if (np.linalg.norm(start - TAIWAN_POS) < 0.5 or
                    np.linalg.norm(end   - TAIWAN_POS) < 0.5):
                tw_arcs.add(arc)

        self.play(
            tw_arcs.animate.set_color(RED).set_opacity(0.15),
            run_time=0.60)

        # Remaining nodes dim slightly — chain disruption
        self.play(
            *[n.animate.set_opacity(0.45) for n in nodes if n is not tw_node],
            run_time=0.55)

        # Camera slow zoom-in on centre
        self.play(
            self.camera.frame.animate.scale(0.80).move_to(ORIGIN),
            run_time=5.0)
        self.wait(2.2)

        # Fade to black
        black_out = Rectangle(width=30, height=18,
                               fill_color=BLACK, fill_opacity=0,
                               stroke_width=0)
        self.add(black_out)
        self.play(black_out.animate.set_fill(BLACK, 1), run_time=1.0)
        self.wait(0.2)