"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 4: How Chips Are Made  |  75 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 12s │ 12s │ Complexity intro   — chip zoom-in + COMPLEX stamp
Beat 2 │ 12s → 28s │ 16s │ Sand to silicon    — sand flood → silicon block
Beat 3 │ 28s → 46s │ 18s │ Wafer formation    — block morphs to wafer disc
Beat 4 │ 46s → 62s │ 16s │ Nano circuits      — wafer zooms → micro patterns
Beat 5 │ 62s → 75s │ 13s │ ASML reveal        — factory silhouette + ONLY ONE stamp
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 75s | No character | English only | Style: Oversimplified

LAYOUT ZONES
  TOP_Y   =  3.0   stamps / title panels
  STAGE_Y =  0.0   main stage (centred)
  NAR_Y   = -3.10  narration strip

Render:
  Preview : manim -pql scene4.py Scene4
  1080p   : manim -pqh scene4.py Scene4
  4K      : manim -pqk scene4.py Scene4
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────────────────
BG        = "#F5F0E8"
INK       = "#1A1008"
RED       = "#D42B2B"
BLUE      = "#2255AA"
GOLD      = "#C8960C"
CREAM     = "#FFFDF8"
SUBTLE    = "#9A8F7E"
WHITE     = "#FFFFFF"
ELECTRIC  = "#00C8FF"
SAND_COL  = "#C8A96E"   # warm sandy tan
SILICON   = "#8899BB"   # cool blue-grey for silicon block
WAFER_COL = "#B8C8D8"   # polished disc surface
WAFER_SHD = "#6678A0"   # darker ring / edge
FONT      = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.0
NAR_Y   = -3.10


# ─────────────────────────────────────────────────────────────
# TEXT HELPERS
# ─────────────────────────────────────────────────────────────
def T(text, size=34, color=INK, weight=BOLD):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)

def Ts(text, size=22, color=SUBTLE):
    return Text(text, font=FONT, font_size=size, color=color, weight=NORMAL)

def nar(text, size=32, color=INK):
    return T(text, size=size, color=color, weight=NORMAL).move_to([0, NAR_Y, 0])

def fit_text(text, max_width, size=28, color=INK, weight=BOLD):
    mob = T(text, size=size, color=color, weight=weight)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


# ─────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────
def ink_panel(w, h, fill=CREAM, stroke=INK, sw=2.5):
    shadow = RoundedRectangle(
        corner_radius=0.14, width=w+0.10, height=h+0.10,
        color=INK, fill_color=INK, fill_opacity=0.10, stroke_width=0
    ).shift(DR * 0.08)
    box = RoundedRectangle(
        corner_radius=0.14, width=w, height=h,
        color=stroke, fill_color=fill, fill_opacity=1, stroke_width=sw
    )
    return VGroup(shadow, box)

def stamp(text, color=RED, w=3.4, h=0.80):
    outer = Rectangle(width=w,       height=h,
                       color=color,  fill_color=color,
                       fill_opacity=0.10, stroke_width=4.5)
    inner = Rectangle(width=w-0.16,  height=h-0.16,
                       color=color,  fill_opacity=0, stroke_width=1.8)
    lbl   = fit_text(text, max_width=w-0.30, size=38, color=color)
    return VGroup(outer, inner, lbl)

def slam(scene, mob, from_dir=UP, rt=0.28):
    mob.shift(from_dir * 4.0)
    scene.add(mob)
    scene.play(mob.animate.shift(-from_dir * 4.0),
                run_time=rt, rate_func=rush_from)


# ─────────────────────────────────────────────────────────────
# PROP BUILDERS
# ─────────────────────────────────────────────────────────────
def make_chip(sc=1.0):
    base = Square(side_length=1.40*sc, color=INK, fill_color="#1C2833",
                   fill_opacity=1, stroke_width=4)
    die  = Square(side_length=0.90*sc, color=GOLD, fill_color="#2C3E50",
                   fill_opacity=1, stroke_width=2.5)
    grid = VGroup(*[
        Line([v*sc, -0.45*sc, 0], [v*sc,  0.45*sc, 0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30, 0.30, 4)
    ] + [
        Line([-0.45*sc, v*sc, 0], [0.45*sc, v*sc, 0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30, 0.30, 4)
    ])
    core = Square(side_length=0.26*sc, color=RED, fill_color=RED,
                   fill_opacity=1, stroke_width=0)
    pins = VGroup(*[
        Rectangle(width=0.08*sc, height=0.20*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([-0.48*sc + i*0.24*sc, sg*0.80*sc, 0])
        for i in range(5) for sg in [1, -1]
    ] + [
        Rectangle(width=0.20*sc, height=0.08*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([sg*0.80*sc, -0.48*sc + i*0.24*sc, 0])
        for i in range(5) for sg in [1, -1]
    ])
    return VGroup(base, pins, die, grid, core)


def make_chip_layered():
    """
    Chip with faint stacked layers visible on the side — Beat 1 visual.
    Main chip + 4 offset translucent shadow layers below-right.
    """
    layers = VGroup()
    for i in range(4, 0, -1):
        shade = Square(side_length=1.40, color=SUBTLE,
                        fill_color=SUBTLE, fill_opacity=0.12,
                        stroke_width=1.5, stroke_opacity=0.30)\
                  .shift(DR * i * 0.10)
        layers.add(shade)
    chip = make_chip(sc=1.0)
    return VGroup(layers, chip)


def make_sand_particles(n=160):
    """Scattered irregular sand dots filling the stage area."""
    np.random.seed(5)
    grains = VGroup()
    for _ in range(n):
        x    = np.random.uniform(-5.5, 5.5)
        y    = np.random.uniform(-1.8, 2.0)
        r    = np.random.uniform(0.04, 0.13)
        # slightly irregular: elongate some grains
        w    = r * np.random.uniform(1.0, 2.2)
        h    = r * np.random.uniform(0.6, 1.4)
        col  = interpolate_color(ManimColor(SAND_COL), ManimColor("#A07840"),
                                  np.random.uniform(0, 1))
        grain = Ellipse(width=w, height=h, color=col,
                         fill_color=col, fill_opacity=np.random.uniform(0.6, 1.0),
                         stroke_width=0)\
                  .move_to([x, y, 0])\
                  .rotate(np.random.uniform(0, PI))
        grains.add(grain)
    return grains


def make_silicon_block():
    """
    Clean rectangular silicon ingot — blue-grey with subtle face lines.
    Isometric-feel: main face + two side faces.
    """
    # Main face
    face  = Rectangle(width=2.80, height=2.00, color=INK,
                        fill_color=SILICON, fill_opacity=1, stroke_width=3)
    # Top face (parallelogram approximated via polygon)
    top_pts = [
        face.get_corner(UL),
        face.get_corner(UL) + RIGHT*0.55 + UP*0.32,
        face.get_corner(UR) + RIGHT*0.55 + UP*0.32,
        face.get_corner(UR),
    ]
    top   = Polygon(*top_pts, color=INK,
                     fill_color=interpolate_color(ManimColor(SILICON), ManimColor(WHITE), 0.25),
                     fill_opacity=1, stroke_width=2.5)
    # Right face
    rgt_pts = [
        face.get_corner(UR),
        face.get_corner(UR) + RIGHT*0.55 + UP*0.32,
        face.get_corner(DR) + RIGHT*0.55 + UP*0.32,
        face.get_corner(DR),
    ]
    rgt   = Polygon(*rgt_pts, color=INK,
                     fill_color=interpolate_color(ManimColor(SILICON), ManimColor(INK), 0.22),
                     fill_opacity=1, stroke_width=2.5)
    # Crystal grain lines on main face
    lines = VGroup(*[
        Line(face.get_left() + UP*(0.5 - i*0.28),
              face.get_right() + UP*(0.5 - i*0.28),
              color=WHITE, stroke_width=0.6, stroke_opacity=0.25)
        for i in range(5)
    ])
    return VGroup(top, rgt, face, lines)


def make_wafer():
    """
    Silicon wafer: polished circular disc with concentric rings and a flat edge.
    """
    r = 1.70
    # Main disc
    disc  = Circle(radius=r, color=INK,
                    fill_color=WAFER_COL, fill_opacity=1, stroke_width=3.5)
    # Concentric rings (reflective sheen)
    rings = VGroup(*[
        Circle(radius=r * frac, color=WAFER_SHD,
                fill_opacity=0, stroke_width=0.7, stroke_opacity=0.35)
        for frac in [0.85, 0.70, 0.52, 0.35, 0.18]
    ])
    # Flat edge notch (standard wafer orientation mark)
    notch = Arc(radius=r, start_angle=-PI/2 - 0.18,
                 angle=0.36, color=WAFER_SHD,
                 stroke_width=6, stroke_opacity=0.70)
    # Die grid overlay (faint — shows chips being cut from wafer)
    grid_lines = VGroup(*[
        Line([-r*0.92, v, 0], [r*0.92, v, 0],
              color=WAFER_SHD, stroke_width=0.8, stroke_opacity=0.40)
        for v in np.linspace(-r*0.88, r*0.88, 12)
    ] + [
        Line([v, -r*0.92, 0], [v, r*0.92, 0],
              color=WAFER_SHD, stroke_width=0.8, stroke_opacity=0.40)
        for v in np.linspace(-r*0.88, r*0.88, 12)
    ])
    # Centre label
    centre_dot = Dot(ORIGIN, radius=0.08, color=WAFER_SHD, fill_opacity=0.55)
    return VGroup(disc, rings, grid_lines, notch, centre_dot)


def make_micro_pattern(rows=18, cols=24, spacing=0.30):
    """
    Dense micro-circuit grid for Beat 4 — tiny coloured rectangles
    arranged in rows, simulating lithography patterns on a wafer.
    """
    np.random.seed(11)
    group  = VGroup()
    ox     = -(cols * spacing) / 2
    oy     = -(rows * spacing) / 2 + 0.20
    colors = [GOLD, ELECTRIC, RED, BLUE, WHITE]
    for r in range(rows):
        for c in range(cols):
            x   = ox + c * spacing + np.random.uniform(-0.04, 0.04)
            y   = oy + r * spacing + np.random.uniform(-0.04, 0.04)
            w   = np.random.uniform(0.08, 0.20)
            h   = np.random.uniform(0.04, 0.12)
            col = colors[np.random.randint(0, len(colors))]
            rect = Rectangle(width=w, height=h, color=col,
                               fill_color=col,
                               fill_opacity=np.random.uniform(0.45, 0.85),
                               stroke_width=0)\
                     .move_to([x, y, 0])\
                     .rotate(np.random.choice([0, PI/2]))
            group.add(rect)
    return group


def make_lightning(start, end, steps=8, seed=0):
    np.random.seed(seed)
    pts = [np.array(start)]
    for i in range(1, steps):
        t    = i / steps
        mid  = np.array(start)*(1-t) + np.array(end)*t
        d    = np.array(end) - np.array(start)
        perp = np.array([-d[1], d[0], 0])
        n    = np.linalg.norm(perp)
        if n > 1e-4: perp /= n
        pts.append(mid + perp*(np.random.rand()-0.5)*0.26)
    pts.append(np.array(end))
    bolt = VMobject(stroke_color=ELECTRIC, stroke_width=3.8, stroke_opacity=0.95)
    bolt.set_points_as_corners(pts)
    return bolt


def make_factory():
    """
    Stylised factory / machine silhouette for Beat 5 (ASML machine).
    Built entirely from rectangles + lines.
    """
    # Main body — large central cabinet
    body   = Rectangle(width=3.20, height=2.60, color=INK,
                         fill_color="#1E2A3A", fill_opacity=1, stroke_width=3.5)
    # Left wing — optical column
    l_col  = Rectangle(width=0.70, height=3.40, color=INK,
                         fill_color="#162030", fill_opacity=1, stroke_width=2.5)\
               .next_to(body, LEFT, buff=0)
    # Right wing — source module
    r_col  = Rectangle(width=0.90, height=2.00, color=INK,
                         fill_color="#162030", fill_opacity=1, stroke_width=2.5)\
               .next_to(body, RIGHT, buff=0).shift(DOWN*0.30)
    # Top nozzle
    nozzle = Rectangle(width=0.50, height=0.80, color=INK,
                         fill_color="#2A3A4A", fill_opacity=1, stroke_width=2)\
               .next_to(body, UP, buff=0).shift(LEFT*0.60)
    # Bottom base
    base   = Rectangle(width=4.20, height=0.40, color=INK,
                         fill_color="#0E161E", fill_opacity=1, stroke_width=2.5)\
               .next_to(body, DOWN, buff=0)
    # Central glow window
    window = RoundedRectangle(corner_radius=0.10, width=1.10, height=0.80,
                               color=ELECTRIC, fill_color=ELECTRIC,
                               fill_opacity=0.20, stroke_width=2.5)\
               .move_to(body.get_center())
    # Detail lines on body
    details = VGroup(*[
        Line(body.get_left() + RIGHT*0.35 + UP*(0.6 - i*0.40),
              body.get_right() + LEFT*0.35 + UP*(0.6 - i*0.40),
              color=ELECTRIC, stroke_width=0.8, stroke_opacity=0.30)
        for i in range(4)
    ])
    # Lens circles on left column
    lenses  = VGroup(*[
        Circle(radius=0.14, color=ELECTRIC, fill_color=ELECTRIC,
                fill_opacity=0.18, stroke_width=1.5)
        .move_to(l_col.get_center() + UP*(0.8 - j*0.55))
        for j in range(4)
    ])
    return VGroup(base, l_col, r_col, body, nozzle, details, lenses, window)


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene4(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Permanent fixtures ───────────────────────────────────────
        paper = VGroup(*[
            Line(LEFT*7.8, RIGHT*7.8, color=INK,
                  stroke_width=0.25, stroke_opacity=0.05).shift(UP*y)
            for y in np.arange(-4.6, 4.8, 0.46)
        ])
        nar_line = Line(LEFT*6.8, RIGHT*6.8, color=INK,
                         stroke_width=1.0, stroke_opacity=0.14)\
                     .move_to([0, -2.15, 0])
        self.add(paper, nar_line)

        # ══════════════════════════════════════════════════════════════
        # BEAT 1  │  0s → 12s  │  Complexity intro
        #
        # Layered chip fades in small → Ken Burns zoom-in.
        # "COMPLEX" red stamp slams from top.
        # Narration holds visibly before cross-fade.
        #
        # 0.00–0.80  chip fades in (small)            0.80s
        # 0.80–1.80  Ken Burns zoom-in                1.00s
        # 1.80–2.08  COMPLEX stamp slams              0.28s
        # 2.08–2.20  stamp wobble                     0.12s
        # 2.20–2.98  narration line 1 writes          0.78s
        # 2.98–4.18  hold                             1.20s
        # 4.18–4.68  narration cross-fades            0.50s
        # 4.68–10.0  hold                             5.32s
        # 10.0–12.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        chip_l = make_chip_layered().scale(0.60).move_to([0, STAGE_Y, 0])
        self.play(FadeIn(chip_l, run_time=0.80))
        self.play(chip_l.animate.scale(2.50), run_time=1.00, rate_func=smooth)

        PW1  = 5.0
        st1  = stamp("COMPLEX", color=RED, w=PW1, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st1, from_dir=UP, rt=0.28)
        self.play(Rotate(st1, PI/28, run_time=0.12, rate_func=there_and_back))

        n1a = nar("Making a chip...")
        n1b = nar("...is one of the most complex processes in the world.", color=RED)
        self.play(Write(n1a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n1a, run_time=0.25), FadeIn(n1b, run_time=0.25))
        self.wait(5.32)

        self.play(FadeOut(chip_l, run_time=0.60),
                   FadeOut(st1,   run_time=0.60),
                   FadeOut(n1b,   run_time=0.60))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  12s → 28s  │  Sand to silicon
        #
        # Sand particles flood in across stage.
        # Label "Sand → Silicon" panel appears.
        # Sand group transforms (ReplacementTransform) into silicon block.
        #
        # 0.00–0.50  "Sand → Silicon" panel           0.50s
        # 0.50–1.50  sand particles flood (lagged)    1.00s
        # 1.50–2.28  narration line 1 writes          0.78s
        # 2.28–3.48  hold                             1.20s
        # 3.48–3.98  narration cross-fades            0.50s
        # 3.98–5.48  hold                             1.50s
        # 5.48–7.48  sand morphs → silicon block      2.00s
        # 7.48–7.98  silicon block settle             0.50s
        # 7.98–14.0  hold                             6.02s
        # 14.0–16.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        PW2  = 4.6
        tp2  = ink_panel(PW2, 0.72).move_to([0, TOP_Y, 0])
        tt2  = fit_text("Sand  ->  Silicon", max_width=PW2-0.40, size=32)\
                 .move_to(tp2[1].get_center())
        self.play(GrowFromCenter(tp2, run_time=0.28),
                   Write(tt2, run_time=0.40))

        sand = make_sand_particles(n=160)
        self.play(LaggedStart(*[FadeIn(g, scale=0.4) for g in sand],
                               lag_ratio=0.005, run_time=1.00))

        n2a = nar("It all starts... with simple sand.")
        n2b = nar("Ordinary beach sand. Processed into pure silicon.", color=GOLD)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))
        self.wait(1.50)

        # Morph sand → silicon block
        sil_block = make_silicon_block().scale(0.90).move_to([0, STAGE_Y - 0.10, 0])
        self.play(
            ReplacementTransform(sand, sil_block, run_time=2.00,
                                  rate_func=smooth),
        )
        self.play(sil_block.animate.scale(1.05),
                   run_time=0.25, rate_func=there_and_back)

        self.wait(6.02)

        self.play(FadeOut(tp2,       run_time=0.55),
                   FadeOut(tt2,       run_time=0.55),
                   FadeOut(n2b,       run_time=0.55))
        # Keep sil_block for beat 3
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │   28s → 46s  │  Wafer formation
        #
        # Silicon block transforms → wafer disc.
        # Ken Burns zoom-in on wafer. Label panel appears.
        #
        # 0.00–0.50  "Silicon Wafer" panel            0.50s
        # 0.50–2.50  block morphs → wafer             2.00s
        # 2.50–3.50  Ken Burns zoom-in                1.00s
        # 3.50–4.28  narration writes                 0.78s
        # 4.28–5.48  hold                             1.20s
        # 5.48–5.98  narration cross-fades            0.50s
        # 5.98–16.0  hold                             10.02s
        # 16.0–18.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        PW3  = 4.4
        tp3  = ink_panel(PW3, 0.72).move_to([0, TOP_Y, 0])
        tt3  = fit_text("Silicon Wafer", max_width=PW3-0.40, size=32)\
                 .move_to(tp3[1].get_center())
        self.play(GrowFromCenter(tp3, run_time=0.28),
                   Write(tt3, run_time=0.40))

        wafer = make_wafer().scale(0.75).move_to([0, STAGE_Y, 0])
        self.play(
            ReplacementTransform(sil_block, wafer, run_time=2.00,
                                  rate_func=smooth),
        )

        # Ken Burns zoom-in on wafer
        self.play(wafer.animate.scale(1.35), run_time=1.00, rate_func=smooth)

        n3a = nar("That silicon is shaped into thin, polished wafers.")
        n3b = nar("Each wafer: 300mm wide. Thinner than a fingernail.", color=BLUE)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))
        self.wait(10.02)

        self.play(FadeOut(tp3,  run_time=0.55),
                   FadeOut(tt3,  run_time=0.55),
                   FadeOut(n3b,  run_time=0.55))
        # Keep wafer for beat 4
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │   46s → 62s  │  Nano circuits
        #
        # Wafer zooms in further. Micro-pattern grid floods over wafer.
        # Circuit traces flash. "Nanometer Precision" panel.
        #
        # 0.00–0.80  wafer zooms in (Ken Burns)       0.80s
        # 0.80–1.30  wafer fades slightly → micro pattern floods  1.30s
        # 1.30–1.58  "Nanometer Precision" stamp      0.28s
        # 1.58–1.70  stamp wobble                     0.12s
        # 1.70–2.80  electricity traces flash ×2      1.10s
        # 2.80–3.58  narration writes                 0.78s
        # 3.58–4.78  hold                             1.20s
        # 4.78–5.28  narration cross-fades            0.50s
        # 5.28–14.0  hold                             8.72s
        # 14.0–16.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        self.play(wafer.animate.scale(1.30), run_time=0.80, rate_func=smooth)

        micro = make_micro_pattern(rows=18, cols=24, spacing=0.30)\
                  .move_to([0, STAGE_Y, 0])
        self.play(
            wafer.animate.set_opacity(0.30),
            LaggedStart(*[FadeIn(rect, scale=0.3) for rect in micro],
                         lag_ratio=0.002, run_time=1.30),
        )

        PW4  = 5.2
        st4  = stamp("Nanometer Precision", color=BLUE, w=PW4, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st4, from_dir=UP, rt=0.28)
        self.play(Rotate(st4, -PI/30, run_time=0.12, rate_func=there_and_back))

        # Circuit trace flashes across micro pattern
        chip_c = ORIGIN
        trace_data = [
            (chip_c + LEFT*2.80+UP*0.60,  chip_c + RIGHT*2.80+UP*0.60),
            (chip_c + LEFT*2.80+DOWN*0.20, chip_c + RIGHT*2.80+DOWN*0.20),
            (chip_c + LEFT*2.80+DOWN*1.00, chip_c + RIGHT*2.80+DOWN*1.00),
            (chip_c + LEFT*1.20+UP*1.50,   chip_c + LEFT*1.20+DOWN*1.80),
            (chip_c + RIGHT*1.20+UP*1.50,  chip_c + RIGHT*1.20+DOWN*1.80),
        ]
        bolts = [make_lightning(a, b, seed=i*9) for i,(a,b) in enumerate(trace_data)]
        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 4.5),
                    time_width=0.50, run_time=0.55) for bolt in bolts])
        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 3.0),
                    time_width=0.40, run_time=0.55) for bolt in bolts])

        n4a = nar("On these wafers... circuits are built at the nanometer scale.")
        n4b = nar("Smaller than a virus. Billions of them.", color=ELECTRIC)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))
        self.wait(8.72)

        self.play(FadeOut(micro,  run_time=0.60),
                   FadeOut(wafer,  run_time=0.60),
                   FadeOut(st4,    run_time=0.60),
                   FadeOut(n4b,    run_time=0.60))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  62s → 75s  │  ASML reveal
        #
        # Factory machine silhouette slides in from right (pan-right feel).
        # Central window glows + pulses. "ONLY ONE" gold stamp slams.
        # "ASML" ink panel. Final narration. Zoom-out → fade to black.
        #
        # 0.00–1.00  factory slides in from right     1.00s
        # 1.00–1.40  centre glow pulses               0.40s
        # 1.40–1.68  ONLY ONE stamp slams             0.28s
        # 1.68–1.80  stamp wobble                     0.12s
        # 1.80–2.20  ASML label panel                 0.40s
        # 2.20–2.98  narration writes                 0.78s
        # 2.98–4.18  hold                             1.20s
        # 4.18–4.68  narration cross-fades            0.50s
        # 4.68–8.50  hold                             3.82s
        # 8.50–9.20  zoom-out                         0.70s
        # 9.20–10.7  fade to black overlay            1.50s
        # ══════════════════════════════════════════════════════════════
        factory = make_factory().scale(0.82).move_to([10.0, STAGE_Y - 0.20, 0])
        self.add(factory)
        self.play(
            factory.animate.move_to([0.60, STAGE_Y - 0.20, 0]),
            run_time=1.00, rate_func=smooth,
        )

        # Glow pulse on window (last element of factory VGroup)
        win = factory[-1]
        self.play(win.animate.set_fill(opacity=0.55).scale(1.15),
                   run_time=0.20, rate_func=there_and_back)
        self.play(win.animate.set_fill(opacity=0.30),
                   run_time=0.20, rate_func=smooth)

        # ONLY ONE stamp
        PW5a = 4.0
        st5  = stamp("ONLY ONE", color=GOLD, w=PW5a, h=0.82)\
                 .move_to([-3.50, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, PI/26, run_time=0.12, rate_func=there_and_back))

        # ASML label panel — left of factory
        PW5b  = 2.8
        asml_p = ink_panel(PW5b, 0.72, fill="#FFFBE6", stroke=GOLD, sw=3.0)\
                   .move_to([-3.50, 0.60, 0])
        asml_t = fit_text("ASML", max_width=PW5b-0.30, size=34, color=GOLD)\
                   .move_to(asml_p[1].get_center() + UP*0.10)
        asml_s = fit_text("Netherlands", max_width=PW5b-0.30, size=18,
                           color=GOLD, weight=NORMAL)\
                   .move_to(asml_p[1].get_center() + DOWN*0.16)
        self.play(GrowFromCenter(asml_p, run_time=0.22),
                   Write(asml_t,          run_time=0.28),
                   FadeIn(asml_s,         run_time=0.20))

        n5a = nar("Only one company builds these machines.")
        n5b = nar("ASML. And it's in the Netherlands.", color=GOLD)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))
        self.wait(3.82)

        # Zoom out
        stage_all = VGroup(factory, st5, asml_p, asml_t, asml_s)
        self.play(stage_all.animate.scale(0.74).shift(DOWN*0.10),
                   run_time=0.70, rate_func=smooth)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)