"""
scene2.py — "What a Chip Really Is"
Origeno Educational Video Channel
Style: Oversimplified | Duration: ~100s | Resolution: 1080p | FPS: 30

Verified beat timing  (run_time budget calculated before coding):
  Beat 1  Chip Intro      ~14.5s
  Beat 2  Switch Grid     ~ 9.4s
  Beat 3  Logic Pulses    ~20.6s   ← pulse speed 0.10s/node, 2 rounds only
  Beat 4  Digital World   ~17.0s
  Beat 5  Devices         ~17.6s
  Beat 6  Precision       ~18.8s
  ──────────────────────────────
  TOTAL                   ~97.8s  (+fade overhead ≈ 100s)

Design rules (prevent previous Group/VGroup crash loop):
  • Switch grid: animate colour+position on permanent VMobjects — never swap objects
  • load_asset() always returns Group() — safe for any container
  • Containers holding asset results use Group(), pure-geometry containers use VGroup()
  • Pulse loops: 2 rounds max, speed 0.10s per node segment

Asset folder (all optional, built-in fallbacks if missing):
  scene2.py
  asset/
      chip.svg  or  chip.png
      node.svg  or  node.png
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

config.background_color = BG
# Resolution is intentionally NOT set here — controlled entirely by CLI flag:
#   manim -ql scene2.py Scene2   → 480p  fast preview
#   manim -qm scene2.py Scene2   → 720p  medium preview
#   manim -qh scene2.py Scene2   → 1080p final render
# FPS is set here so it applies at every quality level.
config.frame_rate = 60

# ─────────────────────────────────────────────
# ASSET PATHS
# ─────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR  = os.path.join(SCRIPT_DIR, "asset")
SVG_CHIP   = os.path.join(ASSET_DIR, "chip.svg")
SVG_NODE   = os.path.join(ASSET_DIR, "node.svg")


# ═══════════════════════════════════════════════
# ASSET LOADER  — always returns Group or None
# ═══════════════════════════════════════════════

def load_asset(svg_path, height=1.0, color=BLUE):
    """
    SVG  → SVGMobject styled with color, wrapped in Group
    PNG  → ImageMobject, wrapped in Group
    Bad / missing → None  (caller uses built-in fallback)
    Returns Group (not VGroup) so it is safe in any container.
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


def make_node(radius=0.18, color=GOLD):
    asset = load_asset(SVG_NODE, height=radius*2, color=color)
    if asset is not None:
        return asset
    outer = Circle(radius=radius, fill_color=color,
                   fill_opacity=0.9, stroke_width=0)
    inner = Circle(radius=radius*0.45, fill_color=WHITE_OP,
                   fill_opacity=0.6, stroke_width=0)
    return VGroup(outer, inner)


def make_phone(height=1.6) -> VGroup:
    body   = RoundedRectangle(corner_radius=0.14, width=height*0.48, height=height,
                              fill_color=DARK, fill_opacity=1,
                              stroke_color=SOFT_GRY, stroke_width=1.5)
    screen = RoundedRectangle(corner_radius=0.08, width=height*0.36, height=height*0.72,
                              fill_color="#1A3A5C", fill_opacity=1, stroke_width=0)
    gl1    = Line([-height*0.10, height*0.12, 0], [height*0.10, height*0.12, 0],
                  stroke_color=BLUE, stroke_width=1.5, stroke_opacity=0.7)
    gl2    = Line([-height*0.10, height*0.04, 0], [height*0.10, height*0.04, 0],
                  stroke_color=BLUE, stroke_width=1.0, stroke_opacity=0.5)
    home   = Circle(radius=0.06, stroke_color=SOFT_GRY,
                    stroke_width=1.2, fill_opacity=0
                    ).move_to([0, -height*0.41, 0])
    return VGroup(body, screen, gl1, gl2, home)


def make_laptop(width=2.0) -> VGroup:
    h      = width * 0.62
    lid    = RoundedRectangle(corner_radius=0.10, width=width, height=h,
                              fill_color=DARK, fill_opacity=1,
                              stroke_color=SOFT_GRY, stroke_width=1.5)
    screen = RoundedRectangle(corner_radius=0.06, width=width*0.82, height=h*0.76,
                              fill_color="#1A3A5C", fill_opacity=1, stroke_width=0)
    base   = RoundedRectangle(corner_radius=0.06, width=width*1.1, height=h*0.12,
                              fill_color=DARK, fill_opacity=1,
                              stroke_color=SOFT_GRY, stroke_width=1
                              ).move_to([0, -h/2-h*0.06, 0])
    return VGroup(lid, screen, base)


def make_datacenter(width=1.8) -> VGroup:
    h     = width * 0.75
    rack  = RoundedRectangle(corner_radius=0.08, width=width, height=h,
                             fill_color=DARK, fill_opacity=1,
                             stroke_color=SOFT_GRY, stroke_width=1.5)
    rows  = VGroup()
    for i, y in enumerate(np.arange(h/2-0.18, -h/2+0.08, -0.22)):
        bar = Rectangle(width=width*0.78, height=0.10,
                        fill_color=BLUE if i % 3 != 2 else GOLD,
                        fill_opacity=0.7, stroke_width=0).move_to([0, y, 0])
        rows.add(bar)
    light = Dot(radius=0.05, color=GREEN).move_to([width/2-0.14, h/2-0.14, 0])
    return VGroup(rack, rows, light)


def make_globe(radius=2.6) -> VGroup:
    # fill_opacity=0 — globe is decorative stroke-only, never covers foreground
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


# ═══════════════════════════════════════════════
# SCENE
# ═══════════════════════════════════════════════

class Scene2(MovingCameraScene):

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
    # BEAT 1  ·  ~14.5s  ·  Chip Introduction
    # ──────────────────────────────────────────
    def _beat1(self):
        self._reset_camera()

        chip = make_chip(size=2.8, color=BLUE)
        chip.move_to(ORIGIN)
        self.play(FadeIn(chip, scale=0.4, run_time=1.0))       # 1.0

        title = Text("A chip  =  Billions of Transistors",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.6))                  # 1.6

        narr = Text(
            "A chip... is not just a small component."
            "  Inside it... are billions of transistors.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))                   # 2.1

        # Flood 50 transistor dots
        rng = random.Random(42)
        cx, cy = chip.get_center()[:2]
        t_dots = VGroup(*[
            Dot(np.array([cx + rng.uniform(-1.1, 1.1),
                          cy + rng.uniform(-1.1, 1.1), 0]),
                radius=0.07, color=GOLD, fill_opacity=0.85)
            for _ in range(50)
        ])
        self.play(LaggedStart(
            *[FadeIn(d, scale=0.1) for d in t_dots],
            lag_ratio=0.06, run_time=2.5))                      # 4.6

        # Counter
        c_lbl = Text("Transistors:", font="Georgia",
                     font_size=26, color=DARK).move_to([4.8, 0.6, 0])
        c_val = Text("0", font="Georgia", font_size=42,
                     color=BLUE, weight=BOLD).move_to([4.8, -0.1, 0])
        self.play(FadeIn(c_lbl), FadeIn(c_val), run_time=0.4)   # 5.0

        for label in ["100 M", "500 M", "1 B"]:                 # 3 × 0.5s = 1.5s
            nv = Text(label, font="Georgia", font_size=42,
                      color=BLUE, weight=BOLD).move_to(c_val.get_center())
            self.play(ReplacementTransform(c_val, nv, run_time=0.5))
            c_val = nv                                           # 6.5

        self.play(
            self.camera.frame.animate.scale(0.72).move_to(chip.get_center()),
            run_time=4.5)                                        # 11.0
        self.wait(1.5)                                           # 12.5

        self.play(FadeOut(chip), FadeOut(t_dots), FadeOut(title),
                  FadeOut(narr), FadeOut(c_lbl), FadeOut(c_val),
                  run_time=0.5)                                  # 13.0

    # ──────────────────────────────────────────
    # BEAT 2  ·  ~9.4s  ·  Switch Grid ON/OFF
    #
    # Each cell = track RoundedRect + knob Circle (pure VMobjects).
    # Flipping animates set_fill + move_to — no object swapping.
    # ──────────────────────────────────────────
    def _beat2(self):
        self._reset_camera()

        title = Text("Transistor  =  Switch  (ON / OFF)",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))                  # 0.5

        narr = Text(
            "Every transistor works like a switch.  On... off..."
            "  But when billions connect...",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))                   # 1.0

        cols, rows   = 10, 8
        sw_w, sw_h   = 0.50, 0.25
        x_gap, y_gap = 1.12, 0.70
        total_w = (cols-1)*x_gap
        total_h = (rows-1)*y_gap
        origin  = np.array([-total_w/2, -total_h/2+0.2, 0])

        rng   = random.Random(7)
        cells = []          # [track, knob, is_on, centre_pos]
        tracks = VGroup()
        knobs  = VGroup()

        for r in range(rows):
            for c in range(cols):
                pos   = origin + np.array([c*x_gap, r*y_gap, 0])
                is_on = rng.random() > 0.5
                color = GREEN if is_on else RED
                track = RoundedRectangle(
                    corner_radius=sw_h/2, width=sw_w, height=sw_h,
                    fill_color=color, fill_opacity=1, stroke_width=0)
                track.move_to(pos)
                kx    = sw_w/2 - sw_h/2 if is_on else -sw_w/2 + sw_h/2
                knob  = Circle(radius=sw_h/2 - 0.02,
                               fill_color=WHITE_OP, fill_opacity=1, stroke_width=0)
                knob.move_to(pos + np.array([kx, 0, 0]))
                cells.append([track, knob, is_on, pos])
                tracks.add(track)
                knobs.add(knob)

        self.play(LaggedStart(
            *[FadeIn(t, scale=0.3) for t in tracks],
            lag_ratio=0.015, run_time=1.4))                     # 2.4
        self.play(LaggedStart(
            *[FadeIn(k, scale=0.3) for k in knobs],
            lag_ratio=0.015, run_time=0.7))                     # 3.1

        # 8 flip cycles × 0.5s = 4.0s
        rng2 = random.Random(99)
        for _ in range(8):
            anims = []
            for cell in cells:
                if rng2.random() < 0.30:
                    track, knob, is_on, cpos = cell
                    new_on   = not is_on
                    new_col  = GREEN if new_on else RED
                    new_kx   = (sw_w/2 - sw_h/2) if new_on else (-sw_w/2 + sw_h/2)
                    new_kpos = cpos + np.array([new_kx, 0, 0])
                    anims.append(track.animate.set_fill(new_col))
                    anims.append(knob.animate.move_to(new_kpos))
                    cell[2] = new_on
            if anims:
                self.play(*anims, run_time=0.50)
            else:
                self.wait(0.50)                                  # 7.1

        self.wait(1.0)                                           # 8.1
        self.play(FadeOut(tracks), FadeOut(knobs),
                  FadeOut(title), FadeOut(narr), run_time=0.5)  # 8.6

    # ──────────────────────────────────────────
    # BEAT 3  ·  ~20.6s  ·  Logic — Electricity Pulses
    #
    # Pulse speed: 0.10s per node segment (fast, visual only).
    # 2 rounds total (1× BLUE, 1× GOLD) to cap time.
    # ──────────────────────────────────────────
    def _beat3(self):
        self._reset_camera()

        title = Text("Logic  =  Intelligence",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "They create logic.  And that logic makes"
            " your phone smart, lets AI answer...",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # 6×5 circuit node grid
        cols, rows   = 6, 5
        x_gap, y_gap = 1.9, 1.35
        total_w = (cols-1)*x_gap
        total_h = (rows-1)*y_gap
        base    = np.array([-total_w/2, -total_h/2, 0])

        node_pos = {}
        nodes_vg = VGroup()
        for r in range(rows):
            for c in range(cols):
                p = base + np.array([c*x_gap, r*y_gap, 0])
                node_pos[(r, c)] = p
                nodes_vg.add(Dot(p, radius=0.14, color=BLUE, fill_opacity=0.85))

        traces = VGroup()
        for r in range(rows):
            for c in range(cols-1):
                traces.add(Line(node_pos[(r,c)], node_pos[(r,c+1)],
                                stroke_color=SOFT_GRY, stroke_width=1.5,
                                stroke_opacity=0.28))
        for r in range(rows-1):
            for c in range(cols):
                traces.add(Line(node_pos[(r,c)], node_pos[(r+1,c)],
                                stroke_color=SOFT_GRY, stroke_width=1.5,
                                stroke_opacity=0.28))

        self.play(FadeIn(traces, run_time=0.8), FadeIn(nodes_vg, run_time=0.8))

        # Paths: 5 horizontal rows + 6 vertical columns = 11 paths
        pulse_paths = (
            [[(r, c) for c in range(cols)] for r in range(rows)] +
            [[(r, c) for r in range(rows)] for c in range(cols)]
        )

        # speed: 0.10s/segment so row(6pts)=0.60+0.15=0.75s, col(5pts)=0.50+0.15=0.65s
        # 11 paths × ~0.70s avg × 2 colors = ~15.4s
        def run_pulse(path_keys, color):
            pts = [node_pos[k] for k in path_keys]
            dot = Dot(pts[0], radius=0.12, color=color, fill_opacity=1)
            self.add(dot)
            seg_time = 0.10 * len(pts)
            self.play(Succession(
                *[dot.animate.move_to(p) for p in pts[1:]],
                run_time=seg_time))
            rings = VGroup(*[
                Circle(radius=0.22, stroke_color=color,
                       stroke_width=2, stroke_opacity=0.7, fill_opacity=0
                       ).move_to(node_pos[k])
                for k in path_keys])
            self.add(rings)
            self.play(rings.animate.scale(1.5).set_opacity(0), run_time=0.15)
            self.remove(dot, rings)

        # 1 round BLUE + 1 round GOLD  (≈ 2 × 7.65s = 15.3s)
        for path in pulse_paths:
            run_pulse(path, BLUE)
        for path in pulse_paths:
            run_pulse(path, GOLD)

        self.play(self.camera.frame.animate.shift(LEFT*0.7), run_time=2.0)
        self.wait(0.5)
        self.play(FadeOut(traces), FadeOut(nodes_vg),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 4  ·  ~17s  ·  Digital World
    # ──────────────────────────────────────────
    def _beat4(self):
        self._reset_camera()

        title = Text("Logic powers the Digital World",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text("And it powers the entire digital world.",
                    font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # ── Globe: decorative background ring only — no fill cover ──
        # radius=2.2 keeps it inside frame; fill_opacity=0 so nothing is hidden;
        # added to scene BEFORE chip so chip always renders on top.
        globe = make_globe(radius=2.2)
        globe.move_to(ORIGIN)
        # Strip out the filled circle — keep only lat/lon strokes
        if len(globe.submobjects) >= 1:
            globe.submobjects[0].set_fill(opacity=0)   # clear the blue disc fill
        globe.set_opacity(0)
        self.add(globe)   # add behind everything else

        chip = make_chip(size=1.6, color=BLUE)
        chip.move_to(ORIGIN)
        self.play(
            FadeIn(chip, scale=0.5, run_time=0.7),
            globe.animate.set_opacity(1),
        )

        orbit_r     = 2.2
        orbit_nodes = Group()
        for angle in np.linspace(0, TAU, 9, endpoint=False):
            n = make_node(radius=0.22, color=GOLD)
            n.move_to([orbit_r*np.cos(angle), orbit_r*np.sin(angle), 0])
            orbit_nodes.add(n)

        arcs = VGroup(*[
            Line(n.get_center(), ORIGIN,
                 stroke_color=BLUE, stroke_width=1.2, stroke_opacity=0.32)
            for n in orbit_nodes])

        self.play(LaggedStart(
            *[FadeIn(n, scale=0.2) for n in orbit_nodes],
            lag_ratio=0.10, run_time=1.4))
        self.play(LaggedStart(
            *[Create(a) for a in arcs],
            lag_ratio=0.08, run_time=1.0))

        self.play(self.camera.frame.animate.scale(1.20), run_time=10.0)
        self.wait(1.5)

        self.play(FadeOut(chip), FadeOut(globe),
                  FadeOut(orbit_nodes), FadeOut(arcs),
                  FadeOut(title), FadeOut(narr), run_time=0.6)

    # ──────────────────────────────────────────
    # BEAT 5  ·  ~17.6s  ·  Digital Impact — Devices
    # ──────────────────────────────────────────
    def _beat5(self):
        self._reset_camera()

        title = Text("Digital  =  Controlled Electricity Flow",
                     font="Georgia", font_size=32, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "Everything digital you see... is electricity"
            " flowing through chips.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        phone  = make_phone(height=1.8).move_to([-4.2, 0.0, 0])
        laptop = make_laptop(width=2.2).move_to([ 0.0,-0.1, 0])
        dc     = make_datacenter(width=2.0).move_to([ 4.2, 0.0, 0])

        dev_labels = VGroup(
            Text("Smartphone",  font="Georgia", font_size=18,
                 color=DARK).next_to(phone,  DOWN, buff=0.30),
            Text("Laptop",      font="Georgia", font_size=18,
                 color=DARK).next_to(laptop, DOWN, buff=0.30),
            Text("Data Center", font="Georgia", font_size=18,
                 color=DARK).next_to(dc,     DOWN, buff=0.30),
        )

        self.play(
            FadeIn(phone,  scale=0.4, run_time=0.7),
            FadeIn(laptop, scale=0.4, run_time=0.7),
            FadeIn(dc,     scale=0.4, run_time=0.7),
            FadeIn(dev_labels,        run_time=0.7))

        # Pulse helper — 0.45s travel + 0.15s flash = 0.60s per hop
        def device_pulse(src, dst, color):
            p = Dot(src.get_right(), radius=0.12, color=color, fill_opacity=1)
            self.add(p)
            self.play(p.animate.move_to(dst.get_left()),
                      run_time=0.45, rate_func=linear)
            ring = Circle(radius=0.20, stroke_color=color,
                          stroke_width=2, stroke_opacity=0.8,
                          fill_opacity=0).move_to(dst.get_left())
            self.add(ring)
            self.play(ring.animate.scale(2.0).set_opacity(0), run_time=0.15)
            self.remove(p, ring)

        # 4 rounds × 4 hops × 0.60s = 9.6s
        for _ in range(4):
            device_pulse(phone,  laptop, BLUE)
            device_pulse(laptop, dc,     GOLD)
            device_pulse(dc,     laptop, BLUE)
            device_pulse(laptop, phone,  GOLD)

        self.play(self.camera.frame.animate.shift(RIGHT*0.6), run_time=3.0)
        self.wait(1.0)
        self.play(FadeOut(phone), FadeOut(laptop), FadeOut(dc),
                  FadeOut(dev_labels), FadeOut(title), FadeOut(narr),
                  run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 6  ·  ~18.8s  ·  Precision — dense dot grid
    # ──────────────────────────────────────────
    def _beat6(self):
        self._reset_camera()

        title = Text("Precision  is  Everything",
                     font="Georgia", font_size=38, color=DARK, weight=BOLD)
        title.to_corner(UL, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text("Being controlled with extreme precision.",
                    font="Georgia", font_size=22, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Dense 18×12 dot grid
        cols, rows   = 18, 12
        x_gap, y_gap = 0.62, 0.52
        total_w = (cols-1)*x_gap
        total_h = (rows-1)*y_gap
        base    = np.array([-total_w/2, -total_h/2, 0])

        dot_list = []
        dots_vg  = VGroup()
        for r in range(rows):
            for c in range(cols):
                d = Dot(base + np.array([c*x_gap, r*y_gap, 0]),
                        radius=0.055, color=SOFT_GRY, fill_opacity=0.40)
                dot_list.append(d)
                dots_vg.add(d)

        self.play(FadeIn(dots_vg, run_time=0.7))

        # Column lookup by index
        col_dots = [
            [dot_list[r*cols + c] for r in range(rows)]
            for c in range(cols)
        ]

        # 5 waves × (1.2s sweep + 0.25s reset) = 7.25s
        for wave in range(5):
            pulse_color = BLUE if wave % 2 == 0 else GOLD
            col_anims = [
                AnimationGroup(
                    *[d.animate.set_color(pulse_color).set_opacity(1.0)
                      for d in col_dots[c]],
                    run_time=0.08)
                for c in range(cols)
            ]
            self.play(LaggedStart(*col_anims, lag_ratio=0.06, run_time=1.2))
            self.play(dots_vg.animate.set_color(SOFT_GRY).set_opacity(0.40),
                      run_time=0.25)

        # Zoom in
        self.play(
            self.camera.frame.animate.scale(0.65).move_to(ORIGIN),
            run_time=7.0)
        self.wait(1.0)

        # Fade to black
        black_out = Rectangle(width=30, height=18,
                               fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(black_out)
        self.play(black_out.animate.set_fill(opacity=1), run_time=1.0)
        self.wait(0.2)