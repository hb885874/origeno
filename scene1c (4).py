"""
scene3.py — "Inside the Making (Lithography)"
Origeno Educational Video Channel
Style: Oversimplified | Duration: ~80s | FPS: 60

Verified beat timing:
  Beat 1  Big Question      ~11.1s  — chip glitch + question mark
  Beat 2  Litho Intro       ~11.3s  — cleanroom bg + machine + CRITICAL stamp
  Beat 3  Light Printing    ~13.0s  — light beam through mask → wafer flood
  Beat 4  Extreme Light     ~14.5s  — nm counter + atom dots flood + zoom
  Beat 5  Layering Process  ~19.5s  — layer stack flood + counter + pan-up
  Beat 6  Failure           ~ 9.9s  — glitch stack + FAILED stamp + fade to black
  ─────────────────────────────────
  TOTAL                     ~79.4s  (+overhead ≈ 80s)

Design rules (same as scene2 — no crash loop):
  • load_asset() always returns Group or None
  • Containers holding asset results use Group()
  • Pure-geometry containers use VGroup()
  • No submobject index manipulation

Asset folder (all optional, built-in fallbacks):
  scene3.py
  asset/
      chip.svg   or chip.png
      wafer.svg  or wafer.png
      machine.svg or machine.png
      cleanroom.png  (Beat 2 background)
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

config.background_color = BG
# Resolution controlled by CLI flag — do NOT hardcode here:
#   manim -ql scene3.py Scene3   → 480p  preview
#   manim -qm scene3.py Scene3   → 720p  preview
#   manim -qh scene3.py Scene3   → 1080p final
config.frame_rate = 60

# ─────────────────────────────────────────────
# ASSET PATHS
#   scene3.py
#   asset/
#       chip.svg / chip.png
#       wafer.svg / wafer.png
#       machine.svg / machine.png
#       cleanroom.png
# ─────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR    = os.path.join(SCRIPT_DIR, "asset")
SVG_CHIP     = os.path.join(ASSET_DIR, "chip.svg")
SVG_WAFER    = os.path.join(ASSET_DIR, "wafer.svg")
SVG_MACHINE  = os.path.join(ASSET_DIR, "machine.svg")
IMG_CLEANROOM = os.path.join(ASSET_DIR, "cleanroom.png")


# ═══════════════════════════════════════════════
# ASSET LOADER
# ═══════════════════════════════════════════════

def load_asset(svg_path, height=1.0, color=BLUE):
    """
    SVG  → SVGMobject styled with color, wrapped in Group
    PNG  → ImageMobject, wrapped in Group
    Missing / corrupt → None  (caller uses built-in fallback)
    Always returns Group (not VGroup).
    """
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
    for i in np.arange(-size/2 + step, size/2, step):
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


def make_wafer(radius=1.2) -> VGroup:
    asset = load_asset(SVG_WAFER, height=radius*2, color=SOFT_GRY)
    if asset is not None:
        return asset
    # Fallback: silicon wafer — grey circle with subtle grid
    disc = Circle(radius=radius, fill_color="#C0C0C0", fill_opacity=1,
                  stroke_color=SOFT_GRY, stroke_width=2)
    notch = Arc(radius=radius, start_angle=-PI/2 - 0.15,
                angle=0.30, stroke_color=DARK, stroke_width=4)
    grid = VGroup()
    step = radius * 0.28
    for i in np.arange(-radius+step, radius, step):
        half = np.sqrt(max(0, radius**2 - i**2))
        if half > 0.05:
            grid.add(Line([i, -half, 0], [i, half, 0],
                          stroke_color=SOFT_GRY, stroke_width=0.6,
                          stroke_opacity=0.30))
            grid.add(Line([-half, i, 0], [half, i, 0],
                          stroke_color=SOFT_GRY, stroke_width=0.6,
                          stroke_opacity=0.30))
    return VGroup(disc, notch, grid)


def make_litho_machine(width=2.2) -> VGroup:
    asset = load_asset(SVG_MACHINE, height=width*0.9, color=DARK)
    if asset is not None:
        return asset
    h = width * 0.9
    # Main body
    body = RoundedRectangle(corner_radius=0.12, width=width, height=h,
                            fill_color=DARK, fill_opacity=1,
                            stroke_color=SOFT_GRY, stroke_width=1.5)
    # Lens housing (bottom protrusion)
    lens_housing = RoundedRectangle(corner_radius=0.08, width=width*0.38, height=h*0.28,
                                    fill_color="#2A2A2A", fill_opacity=1,
                                    stroke_color=SOFT_GRY, stroke_width=1
                                    ).move_to([0, -h/2 - h*0.14, 0])
    lens = Circle(radius=width*0.10, fill_color=PURPLE,
                  fill_opacity=0.85, stroke_color=WHITE_OP,
                  stroke_width=1.5).move_to([0, -h/2 - h*0.14, 0])
    # Light source indicator on top
    light_src = Circle(radius=width*0.07, fill_color=GOLD,
                       fill_opacity=1, stroke_width=0
                       ).move_to([0, h/2 - h*0.12, 0])
    # Panel details
    panel = Rectangle(width=width*0.65, height=h*0.30,
                      fill_color="#1A1A3A", fill_opacity=1,
                      stroke_color=BLUE, stroke_width=1
                      ).move_to([0, h*0.12, 0])
    # LED dots on panel
    leds = VGroup(*[
        Dot(radius=0.05, color=GREEN if i % 3 != 2 else RED
            ).move_to([-width*0.20 + i*0.18, h*0.12, 0])
        for i in range(5)
    ])
    return VGroup(body, lens_housing, lens, light_src, panel, leds)


def make_mask(width=1.8, height=0.35) -> VGroup:
    """EUV photomask — a thin rectangle with circuit pattern slots."""
    frame = Rectangle(width=width, height=height,
                      fill_color="#2A2A2A", fill_opacity=1,
                      stroke_color=GOLD, stroke_width=1.5)
    slots = VGroup()
    slot_w = width / 14
    for i in range(7):
        x = -width/2 + slot_w*1.5 + i*(slot_w*2)
        slots.add(Rectangle(width=slot_w*0.8, height=height*0.65,
                            fill_color=GOLD, fill_opacity=0.55,
                            stroke_width=0).move_to([x, 0, 0]))
    return VGroup(frame, slots)


def make_layer_block(width=3.5, height=0.28, color=BLUE, label="") -> VGroup:
    block = RoundedRectangle(corner_radius=0.04, width=width, height=height,
                             fill_color=color, fill_opacity=0.85,
                             stroke_color=WHITE_OP, stroke_width=1)
    items = VGroup(block)
    if label:
        t = Text(label, font="Georgia", font_size=11, color=WHITE_OP)
        t.move_to(block.get_center())
        items.add(t)
    return items


# ═══════════════════════════════════════════════
# SCENE
# ═══════════════════════════════════════════════

class Scene3(MovingCameraScene):

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
    # BEAT 1  ·  ~11s  ·  The Big Question
    # Chip zooms in → glitch → question mark
    # ──────────────────────────────────────────
    def _beat1(self):
        self._reset_camera()

        chip = make_chip(size=2.6, color=BLUE)
        chip.move_to(ORIGIN)
        self.play(FadeIn(chip, scale=0.5, run_time=0.6))

        title = Text("How is all this complexity made?",
                     font="Georgia", font_size=32, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "But the question is... how is all this complexity created?",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Faint internal layers ghost in over chip
        layers_ghost = VGroup(*[
            Rectangle(width=2.0, height=0.18,
                      fill_color=c, fill_opacity=0.18, stroke_width=0
                      ).move_to([0, -0.5 + i*0.28, 0])
            for i, c in enumerate([GOLD, BLUE, PURPLE, RED, GREEN])
        ])
        self.play(FadeIn(layers_ghost, run_time=1.5))

        # Glitch effect: rapid offset + colour flash
        # Use set_color() in animate chain — set_fill(color, opacity=kw) crashes
        for dx, dy in [(0.12,0.05), (-0.10,-0.06), (0.08,0.08), (0,0)]:
            flash_color = RED if dx != 0 else BLUE
            self.play(
                chip.animate.shift([dx, dy, 0]).set_color(flash_color),
                run_time=0.12)

        # Big question mark
        q_mark = Text("?", font="Georgia", font_size=140,
                      color=RED, weight=BOLD)
        q_mark.move_to(ORIGIN)
        self.play(FadeIn(q_mark, scale=0.3, run_time=0.8))

        # Ken Burns zoom-in
        self.play(
            self.camera.frame.animate.scale(0.78).move_to(ORIGIN),
            run_time=3.5)
        self.wait(1.5)

        self.play(FadeOut(chip), FadeOut(layers_ghost),
                  FadeOut(q_mark), FadeOut(title), FadeOut(narr),
                  run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 2  ·  ~11s  ·  Lithography Intro
    # Cleanroom bg → machine appears → wafer → CRITICAL stamp
    # ──────────────────────────────────────────
    def _beat2(self):
        self._reset_camera()

        # Background image (cleanroom) — graceful fallback
        if os.path.exists(IMG_CLEANROOM):
            bg = ImageMobject(IMG_CLEANROOM)
            bg.set_width(14.5).set_opacity(0.20).move_to(ORIGIN)
            self.add(bg)
        else:
            # Fallback: subtle grid pattern suggesting clean lab
            bg_lines = VGroup()
            for i in np.arange(-7, 7.5, 0.6):
                bg_lines.add(Line([i, -4.5, 0], [i, 4.5, 0],
                                  stroke_color=SOFT_GRY, stroke_width=0.5,
                                  stroke_opacity=0.12))
                bg_lines.add(Line([-7.5, i, 0], [7.5, i, 0],
                                  stroke_color=SOFT_GRY, stroke_width=0.5,
                                  stroke_opacity=0.12))
            self.add(bg_lines)
            bg = bg_lines

        title = Text("Lithography",
                     font="Georgia", font_size=52, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "The most critical step — lithography.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Litho machine — left side
        machine = make_litho_machine(width=2.4)
        machine.move_to([-2.8, 0.3, 0])
        self.play(FadeIn(machine, scale=0.4, run_time=0.8))

        # Wafer — right side, on a table line
        table = Line([-1.0, -1.6, 0], [5.5, -1.6, 0],
                     stroke_color=DARK, stroke_width=2)
        wafer = make_wafer(radius=1.1)
        wafer.move_to([2.5, -0.5, 0])
        self.play(Create(table, run_time=0.4),
                  FadeIn(wafer, scale=0.4, run_time=0.7))

        # CRITICAL stamp — drops from top
        stamp = Text("CRITICAL", font="Georgia",
                     font_size=60, color=RED, weight=BOLD)
        stamp.to_corner(UL, buff=0.45)
        stamp_start = stamp.copy().shift(UP * 3.5)
        self.add(stamp_start)
        self.play(stamp_start.animate.move_to(stamp.get_center()),
                  run_time=0.40)
        self.remove(stamp_start)
        self.add(stamp)

        # Ken Burns: zoom in on the machine + wafer layout
        self.play(
            self.camera.frame.animate.scale(0.72).move_to([-0.2, -0.1, 0]),
            run_time=2.0)
        self.wait(1.5)
        self.play(FadeOut(bg), FadeOut(machine), FadeOut(wafer),
                  FadeOut(table), FadeOut(stamp),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 3  ·  ~13s  ·  Light Printing
    # Light beam → mask → wafer, circuit dots flood onto wafer
    # ──────────────────────────────────────────
    def _beat3(self):
        self._reset_camera()

        title = Text("Light  to  Circuit Printing",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "Light passes through a mask... printing circuits onto silicon.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Vertical layout — shifted DOWN so nothing overlaps title (y~3.5) or narr (y~-3.5)
        # light_src: y=2.2  mask: y=0.4  wafer: y=-2.0  (clear of title+narr zones)
        LIGHT_Y  =  2.2
        MASK_Y   =  0.4
        WAFER_Y  = -2.0

        # Light source
        light_src = Circle(radius=0.22, fill_color=GOLD,
                           fill_opacity=1, stroke_width=0)
        light_src.move_to([0, LIGHT_Y, 0])
        src_glow = Circle(radius=0.40, stroke_color=GOLD,
                          stroke_width=2, stroke_opacity=0.40,
                          fill_opacity=0).move_to([0, LIGHT_Y, 0])
        self.play(FadeIn(light_src, scale=0.3, run_time=0.5),
                  FadeIn(src_glow, run_time=0.5))

        # Mask
        mask = make_mask(width=2.2)
        mask.move_to([0, MASK_Y, 0])
        self.play(FadeIn(mask, run_time=0.6))

        # Wafer — smaller so it stays within safe zone
        wafer = make_wafer(radius=1.0)
        wafer.move_to([0, WAFER_Y, 0])
        self.play(FadeIn(wafer, scale=0.5, run_time=0.6))

        # Light beam segments
        mask_top = MASK_Y + 0.18
        mask_bot = MASK_Y - 0.18
        beam_top = Line([0, LIGHT_Y, 0], [0, mask_top, 0],
                        stroke_color=GOLD, stroke_width=4, stroke_opacity=0.7)
        beam_bot = Line([0, mask_bot, 0], [0, WAFER_Y + 0.4, 0],
                        stroke_color=PURPLE, stroke_width=3.5, stroke_opacity=0.8)
        fan_beams = VGroup(*[
            Line([offset*0.35, mask_bot, 0],
                 [offset*0.90, WAFER_Y + 0.4, 0],
                 stroke_color=PURPLE, stroke_width=1.8, stroke_opacity=0.45)
            for offset in [-1.0, -0.5, 0, 0.5, 1.0]
        ])

        self.play(Create(beam_top, run_time=0.5))
        self.play(Create(beam_bot, run_time=0.4),
                  Create(fan_beams, run_time=0.6))

        # Circuit dots flood onto wafer — bounded to wafer radius
        rng = random.Random(55)
        circuit_dots = VGroup(*[
            Dot(np.array([rng.uniform(-0.75, 0.75),
                          WAFER_Y + rng.uniform(-0.65, 0.65), 0]),
                radius=0.042, color=BLUE, fill_opacity=0.80)
            for _ in range(20)
        ])
        self.play(LaggedStart(
            *[FadeIn(d, scale=0.1) for d in circuit_dots],
            lag_ratio=0.08, run_time=1.0))

        # Zoom into wafer area (safe — title/narr are outside this zone)
        self.play(
            self.camera.frame.animate.scale(0.72).move_to([0, WAFER_Y + 0.5, 0]),
            run_time=3.0)
        self.wait(1.0)

        self.play(FadeOut(light_src), FadeOut(src_glow),
                  FadeOut(mask), FadeOut(wafer), FadeOut(circuit_dots),
                  FadeOut(beam_top), FadeOut(beam_bot), FadeOut(fan_beams),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 4  ·  ~14.5s  ·  Extreme Light (EUV)
    # Wavelength counter counts down, atom dots flood
    # ──────────────────────────────────────────
    def _beat4(self):
        self._reset_camera()

        title = Text("Extreme Precision Light",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "Not normal light... wavelengths so small they work at the atomic level.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Wavelength visual — sine wave that shrinks
        wave_label = Text("Wavelength:", font="Georgia",
                          font_size=24, color=DARK).move_to([-3.5, 1.2, 0])
        self.play(FadeIn(wave_label, run_time=0.5))

        # Draw a sine wave that compresses over time
        def make_wave(frequency=1.0, color=GOLD, opacity=1.0) -> ParametricFunction:
            return ParametricFunction(
                lambda t: np.array([t * 4.0 - 2.0,
                                    0.5 * np.sin(frequency * TAU * t), 0]),
                t_range=[0, 1],
                stroke_color=color, stroke_width=3,
                stroke_opacity=opacity)

        wave = make_wave(frequency=1.5, color=GOLD)
        wave.move_to([2.0, 1.2, 0])
        self.play(Create(wave, run_time=0.8))

        # nm counter: 100 → 13 nm  (EUV = 13.5nm)
        nm_lbl = Text("nm scale:", font="Georgia",
                      font_size=26, color=DARK).move_to([-2.0, 0.0, 0])
        nm_val = Text("100 nm", font="Georgia",
                      font_size=44, color=BLUE, weight=BOLD).move_to([2.0, 0.0, 0])
        self.play(FadeIn(nm_lbl), FadeIn(nm_val), run_time=0.4)

        for label, new_wave_freq in [("50 nm", 2.5), ("13 nm", 5.5), ("13.5 nm EUV", 7.0)]:
            nv = Text(label, font="Georgia", font_size=44,
                      color=BLUE if "EUV" not in label else PURPLE,
                      weight=BOLD).move_to(nm_val.get_center())
            new_wave = make_wave(frequency=new_wave_freq,
                                 color=PURPLE if "EUV" in label else GOLD)
            new_wave.move_to([2.0, 1.2, 0])
            self.play(
                ReplacementTransform(nm_val, nv, run_time=0.4),
                ReplacementTransform(wave,   new_wave, run_time=0.4))
            nm_val = nv
            wave   = new_wave

        # Atom dots flood in — tiny, dense
        rng = random.Random(77)
        atom_dots = VGroup(*[
            Dot(np.array([rng.uniform(-5.5, 5.5),
                          rng.uniform(-2.8, -0.5), 0]),
                radius=0.045, color=SOFT_GRY, fill_opacity=0.55)
            for _ in range(100)
        ])
        self.play(LaggedStart(
            *[FadeIn(d, scale=0.1) for d in atom_dots],
            lag_ratio=0.02, run_time=1.0))

        # Highlight a few atoms with BLUE to show targeting
        highlight_dots = VGroup(*[
            Circle(radius=0.10, stroke_color=BLUE, stroke_width=1.5,
                   stroke_opacity=0.8, fill_opacity=0
                   ).move_to(atom_dots[i].get_center())
            for i in range(0, 20, 2)
        ])
        self.play(LaggedStart(
            *[Create(h) for h in highlight_dots],
            lag_ratio=0.05, run_time=0.8))

        # Ken Burns extreme zoom-in
        self.play(
            self.camera.frame.animate.scale(0.55).move_to([0, -1.5, 0]),
            run_time=4.5)
        self.wait(1.2)

        self.play(FadeOut(wave_label), FadeOut(wave),
                  FadeOut(nm_lbl), FadeOut(nm_val),
                  FadeOut(atom_dots), FadeOut(highlight_dots),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 5  ·  ~19.5s  ·  Layering Process
    # Layer blocks stack up, counter, pan-up camera
    # ──────────────────────────────────────────
    def _beat5(self):
        self._reset_camera()

        # Title and narr shown BEFORE layers start, then faded out so
        # the growing layer stack never covers them.
        title = Text("Hundreds of Layers",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "The same pattern is printed hundreds of times in layers."
            "  Every layer must align perfectly.",
            font="Georgia", font_size=19, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Hold for 2s so viewer reads both lines, then fade — layers will cover these zones
        self.wait(2.0)
        self.play(FadeOut(title), FadeOut(narr), run_time=0.6)

        # Layer counter — anchored to TOP-RIGHT of current camera frame
        # so it stays on screen throughout the pan-up.
        def counter_pos():
            cx = self.camera.frame.get_center()[0]
            cy = self.camera.frame.get_center()[1]
            fw = self.camera.frame.get_width()
            fh = self.camera.frame.get_height()
            return np.array([cx + fw/2 - 1.4, cy + fh/2 - 0.6, 0])

        layer_lbl = Text("Layers:", font="Georgia",
                         font_size=24, color=DARK)
        layer_val = Text("0", font="Georgia", font_size=40,
                         color=BLUE, weight=BOLD)
        layer_lbl.move_to(counter_pos() + np.array([0, 0.45, 0]))
        layer_val.move_to(counter_pos())
        self.play(FadeIn(layer_lbl), FadeIn(layer_val), run_time=0.4)

        # Layer colour palette — cycles through 6 colours
        layer_colors = [BLUE, GOLD, PURPLE, GREEN, RED, "#FF8C00",
                        "#00CED1", BLUE, GOLD, PURPLE,
                        GREEN, RED, "#FF8C00", "#00CED1",
                        BLUE, GOLD, PURPLE, GREEN, RED,
                        "#FF8C00", "#00CED1", BLUE, GOLD,
                        PURPLE, GREEN, RED, "#FF8C00",
                        "#00CED1", BLUE, GOLD]

        layer_names = [
            "Substrate", "Oxide", "Poly-Si", "Metal 1", "Dielectric",
            "Metal 2", "Nitride", "Metal 3", "Oxide 2", "Via Layer",
            "Metal 4", "Barrier", "Copper", "Cap Layer", "Passiv.",
            "Metal 5", "Oxide 3", "Metal 6", "Via 2", "Metal 7",
            "Insulator", "Metal 8", "Via 3", "Metal 9", "Oxide 4",
            "Metal 10", "Barrier 2", "Metal 11", "Via 4", "Top Metal",
        ]

        lw    = 3.8
        lh    = 0.25
        gap   = 0.01
        start_y = -3.5   # start below visible frame — layers grow up into view

        all_layers = VGroup()
        layer_count_vals = []

        # Pre-build all 30 layers off-screen
        for i in range(30):
            y = start_y + i * (lh + gap)
            block = make_layer_block(
                width=lw, height=lh,
                color=layer_colors[i],
                label=layer_names[i] if i < len(layer_names) else f"L{i+1}"
            )
            block.move_to([0, y, 0])
            all_layers.add(block)

        # Animate layers stacking — 30 layers × 0.25s = 7.5s
        for i, block in enumerate(all_layers):
            # Update counter
            nv = Text(str(i+1), font="Georgia", font_size=40,
                      color=BLUE, weight=BOLD).move_to(layer_val.get_center())
            self.play(
                FadeIn(block, shift=UP*0.15, run_time=0.25),
                ReplacementTransform(layer_val, nv, run_time=0.25),
            )
            layer_val = nv

        # Alignment check: faint vertical alignment lines
        align_l = DashedLine([- lw/2, start_y, 0],
                             [- lw/2, start_y + 30*(lh+gap), 0],
                             stroke_color=GOLD, stroke_width=1.2,
                             stroke_opacity=0.50, dash_length=0.15)
        align_r = DashedLine([lw/2, start_y, 0],
                             [lw/2, start_y + 30*(lh+gap), 0],
                             stroke_color=GOLD, stroke_width=1.2,
                             stroke_opacity=0.50, dash_length=0.15)
        self.play(Create(align_l, run_time=0.6),
                  Create(align_r, run_time=0.6))

        # Pan-up Ken Burns — follow the growing stack
        stack_top_y = start_y + 30*(lh+gap)
        self.play(
            self.camera.frame.animate.move_to([0, stack_top_y * 0.4, 0]),
            run_time=3.5)
        self.wait(1.5)

        self.play(FadeOut(all_layers), FadeOut(align_l), FadeOut(align_r),
                  FadeOut(layer_lbl), FadeOut(layer_val),
                  run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 6  ·  ~9.9s  ·  Failure Consequence
    # Layer shifts → glitch → FAILED stamp → fade to black
    # ──────────────────────────────────────────
    def _beat6(self):
        self._reset_camera()

        title = Text("One Mistake  =  Failure",
                     font="Georgia", font_size=38, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "If even one layer is wrong... the entire chip is worthless.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Rebuild a short representative stack (8 layers)
        layer_colors_6 = [BLUE, GOLD, PURPLE, GREEN, RED, "#FF8C00", BLUE, GOLD]
        lw, lh = 3.2, 0.30
        mini_stack = VGroup(*[
            make_layer_block(width=lw, height=lh, color=c)
            .move_to([0, -1.2 + i*(lh+0.02), 0])
            for i, c in enumerate(layer_colors_6)
        ])
        self.play(FadeIn(mini_stack, run_time=0.6))
        self.wait(0.2)

        # One "bad" layer shifts out of alignment
        bad_layer = mini_stack[4]
        self.play(bad_layer.animate.shift(RIGHT * 0.6), run_time=0.5)
        self.wait(0.2)

        # Strong glitch — stack rapidly offsets + colour flash × 5
        for dx, col in [(0.18, RED), (-0.20, GOLD), (0.15, RED),
                        (-0.12, BLUE), (0.0, RED)]:
            self.play(
                mini_stack.animate.shift([dx, 0, 0]).set_color(col),
                run_time=0.12)

        # FAILED stamp slides from right → lands at centre, ABOVE mini_stack
        # mini_stack top is at y ≈ -1.2 + 7*(0.32) = 1.04
        # stamp lands at y = 2.2 so it sits above the stack, below the title
        failed = Text("FAILED", font="Georgia",
                      font_size=80, color=RED, weight=BOLD)
        failed.move_to(RIGHT * 12)
        self.play(failed.animate.move_to([0, 2.2, 0]), run_time=0.55)

        # Brief shake
        for _ in range(3):
            self.play(self.camera.frame.animate.shift(RIGHT * 0.12), run_time=0.06)
            self.play(self.camera.frame.animate.shift(LEFT  * 0.12), run_time=0.06)

        self.wait(1.0)

        # Fade stack out (chip "ruined")
        self.play(
            mini_stack.animate.set_opacity(0.10),
            run_time=1.2)

        self.wait(0.5)

        # Fade to black
        black_out = Rectangle(width=30, height=18,
                               fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(black_out)
        self.play(black_out.animate.set_fill(BLACK, 1), run_time=1.0)
        self.wait(0.2)