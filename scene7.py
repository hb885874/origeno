"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 7: India's Reality  |  80 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 12s │ 12s │ India intro       — India shape on world map
Beat 2 │ 12s → 28s │ 16s │ Import dependency — arrows flood into India
Beat 3 │ 28s → 44s │ 16s │ Everyday devices  — phone/laptop/car icons
Beat 4 │ 44s → 64s │ 20s │ Reliance          — DEPENDENT stamp + arrow flood
Beat 5 │ 64s → 80s │ 16s │ Story not finished — rising bar chart + factory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 80s | No character | English only | Style: Oversimplified

INDIA MAP POSITION
  India dot cluster centred near x=2.40, y=-0.55 on the world dot-map.
  A highlighted India silhouette is approximated by a filled polygon
  using ~12 points that give a rough subcontinent shape.

LAYOUT ZONES
  TOP_Y   =  3.0   stamps / title panels
  STAGE_Y =  0.0   main stage
  NAR_Y   = -3.10  narration strip

Render:
  Preview : manim -pql scene7.py Scene7
  1080p   : manim -pqh scene7.py Scene7
  4K      : manim -pqk scene7.py Scene7
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
MAP_GREEN = "#C8D8B0"
SUBTLE    = "#9A8F7E"
WHITE     = "#FFFFFF"
ORANGE    = "#E07820"   # India saffron accent
INDIA_FILL= "#FFD080"   # warm highlight for India shape
FONT      = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.0
NAR_Y   = -3.10

# India centroid on the world dot-map coordinate system
INDIA_C = np.array([2.40, -0.55, 0])


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
def make_world_dots():
    np.random.seed(42)
    pts = []
    for _ in range(90):  pts.append((np.random.uniform(-6.5,-3.2), np.random.uniform(0.3, 2.5)))
    for _ in range(55):  pts.append((np.random.uniform(-5.3,-3.6), np.random.uniform(-2.5,0.2)))
    for _ in range(55):  pts.append((np.random.uniform(-0.7, 1.7), np.random.uniform(1.1, 2.6)))
    for _ in range(70):  pts.append((np.random.uniform(-0.4, 2.0), np.random.uniform(-2.3,1.0)))
    for _ in range(155): pts.append((np.random.uniform( 2.0, 6.6), np.random.uniform(-0.3,2.8)))
    for _ in range(40):  pts.append((np.random.uniform( 4.2, 6.3), np.random.uniform(-2.8,-0.5)))
    np.random.shuffle(pts)
    return VGroup(*[Dot([x,y,0], radius=0.028, color=BLUE, fill_opacity=0.38)
                    for x,y in pts])


def make_india_shape():
    """
    Rounded rectangle box representing India on the map.
    Centred at INDIA_C = (2.40, -0.55).
    """
    box = RoundedRectangle(corner_radius=0.18, width=1.80, height=2.20,
                            color=ORANGE, fill_color=INDIA_FILL,
                            fill_opacity=0.80, stroke_width=3.5)\
            .move_to(INDIA_C)
    lbl = T("India", size=26, color=ORANGE)\
            .move_to(INDIA_C)
    return VGroup(box, lbl)


def make_india_glow(scale=1.0):
    """Pulsing glow rings around India centroid."""
    return VGroup(*[
        Circle(radius=r*scale, color=ORANGE,
                stroke_opacity=0.55 - i*0.16, stroke_width=2.2)\
          .move_to(INDIA_C)
        for i, r in enumerate([1.20, 1.50, 1.85])
    ])


def make_import_arrows(n=8):
    """
    Arrows from world source points toward India centroid.
    Sources spread across Africa, Europe, East Asia, Americas.
    """
    np.random.seed(17)
    sources = [
        np.array([-4.80,  1.60, 0]),   # North America
        np.array([-3.60, -0.40, 0]),   # South America
        np.array([-0.40,  1.80, 0]),   # Europe
        np.array([ 0.60, -0.20, 0]),   # Middle East
        np.array([ 1.00,  2.00, 0]),   # Central Asia
        np.array([ 4.60,  1.20, 0]),   # East Asia
        np.array([ 5.40, -0.60, 0]),   # SE Asia
        np.array([ 0.40, -1.60, 0]),   # Africa
    ]
    arcs = VGroup()
    for i, src in enumerate(sources[:n]):
        angle = 0.45 if src[0] < INDIA_C[0] else -0.45
        arc = ArcBetweenPoints(
            src,
            INDIA_C + RIGHT*0.18 + UP*0.10,
            angle=angle,
            color=BLUE, stroke_width=2.0, stroke_opacity=0.72
        ).add_tip(tip_length=0.20)
        arcs.add(arc)
    return arcs


def make_phone():
    body   = RoundedRectangle(corner_radius=0.14, width=0.85, height=1.42,
                               color=INK, fill_color="#2C3E50",
                               fill_opacity=1, stroke_width=3)
    screen = RoundedRectangle(corner_radius=0.08, width=0.65, height=1.05,
                               color="#D6EAF8", fill_color="#D6EAF8",
                               fill_opacity=1, stroke_width=1.5)
    notch  = Rectangle(width=0.22, height=0.07, color=INK,
                        fill_color=INK, fill_opacity=1,
                        stroke_width=0).next_to(screen, UP, buff=0.04)
    btn    = Circle(radius=0.07, color="#888", fill_color="#888",
                     fill_opacity=1, stroke_width=0)\
               .next_to(body, DOWN, buff=-0.17)
    return VGroup(body, screen, notch, btn)


def make_laptop():
    """Simple open-laptop icon."""
    screen_body = RoundedRectangle(corner_radius=0.10, width=1.60, height=1.05,
                                    color=INK, fill_color="#2C3E50",
                                    fill_opacity=1, stroke_width=3)
    screen_face = RoundedRectangle(corner_radius=0.07, width=1.36, height=0.84,
                                    color="#D6EAF8", fill_color="#D6EAF8",
                                    fill_opacity=1, stroke_width=1.5)\
                    .move_to(screen_body.get_center())
    # Keyboard base — trapezoidal approximated by wider rectangle
    base = Rectangle(width=1.80, height=0.26, color=INK,
                      fill_color="#1A2A3A", fill_opacity=1,
                      stroke_width=2.5)\
             .next_to(screen_body, DOWN, buff=0)
    hinge = Rectangle(width=1.60, height=0.08, color=INK,
                       fill_color="#0E1820", fill_opacity=1,
                       stroke_width=0).next_to(screen_body, DOWN, buff=0)
    return VGroup(screen_body, screen_face, hinge, base)


def make_car():
    body = RoundedRectangle(corner_radius=0.20, width=1.95, height=0.63,
                             color=INK, fill_color="#2C3E50",
                             fill_opacity=1, stroke_width=3)
    roof = RoundedRectangle(corner_radius=0.16, width=1.08, height=0.44,
                             color=INK, fill_color="#2C3E50",
                             fill_opacity=1, stroke_width=3)\
             .next_to(body, UP, buff=-0.17)
    wl   = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.28,
                             color="#D6EAF8", fill_color="#D6EAF8",
                             fill_opacity=1, stroke_width=1.5)\
             .move_to(roof.get_center() + LEFT*0.27 + UP*0.03)
    wr   = wl.copy().shift(RIGHT*0.42)
    tl   = Circle(radius=0.22, color=INK, fill_color="#555",
                   fill_opacity=1, stroke_width=3)\
             .move_to(body.get_bottom() + LEFT*0.62)
    tr   = tl.copy().move_to(body.get_bottom() + RIGHT*0.62)
    hl   = Circle(radius=0.09, color=WHITE, fill_color=WHITE,
                   fill_opacity=1, stroke_width=0).move_to(tl.get_center())
    hr   = hl.copy().move_to(tr.get_center())
    return VGroup(body, roof, wl, wr, tl, tr, hl, hr)


def make_small_factory(pos=ORIGIN):
    body  = Rectangle(width=1.10, height=0.88, color=INK,
                        fill_color="#1E2A3A", fill_opacity=1, stroke_width=2.5)\
              .move_to(pos)
    chim1 = Rectangle(width=0.18, height=0.40, color=INK,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=2)\
              .move_to(pos+UP*0.64+LEFT*0.25)
    chim2 = Rectangle(width=0.14, height=0.30, color=INK,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=2)\
              .move_to(pos+UP*0.54+RIGHT*0.20)
    base  = Rectangle(width=1.30, height=0.16, color=INK,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=1.5)\
              .move_to(pos+DOWN*0.52)
    win   = Rectangle(width=0.28, height=0.22, color=GOLD,
                        fill_color=GOLD, fill_opacity=0.22,
                        stroke_width=1.5).move_to(pos)
    return VGroup(base, body, chim1, chim2, win)


def make_rising_bar_chart():
    """
    4-bar rising trend chart — each bar taller than previous.
    Drawn as rectangles with an x-axis line.
    """
    bar_h  = [0.60, 1.05, 1.55, 2.20]
    bar_w  = 0.55
    gap    = 0.20
    colors = [BLUE, BLUE, ORANGE, GOLD]
    bars   = VGroup()
    ox     = -((len(bar_h)-1) * (bar_w+gap)) / 2

    for i, (h, col) in enumerate(zip(bar_h, colors)):
        x   = ox + i*(bar_w+gap)
        bar = Rectangle(width=bar_w, height=h, color=col,
                          fill_color=col, fill_opacity=0.85,
                          stroke_width=2)\
                .move_to([x, h/2 - 0.05, 0])
        bars.add(bar)

    axis_x = Line(LEFT*1.20, RIGHT*1.20, color=INK,
                   stroke_width=2.5)\
               .move_to([0, -0.05, 0])
    year_lbls = VGroup(*[
        Ts(yr, size=18, color=SUBTLE)\
          .move_to([ox + i*(bar_w+gap), -0.32, 0])
        for i, yr in enumerate(["2021", "2022", "2023", "2024"])
    ])
    title_lbl = fit_text("India Chip Investment",
                          max_width=3.20, size=20, color=INK, weight=NORMAL)\
                  .move_to([0, 2.55, 0])
    return VGroup(bars, axis_x, year_lbls, title_lbl)


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene7(Scene):
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
        # BEAT 1  │  0s → 12s  │  India intro
        #
        # World map fades in. India shape appears highlighted.
        # Glow rings pulse. "India" panel + narration.
        # Ken Burns zoom-in toward India.
        #
        # 0.00–0.40  map bg fades in                 0.40s
        # 0.40–1.70  world dots appear (lagged)      1.30s
        # 1.70–2.10  India shape fades in            0.40s
        # 2.10–2.95  glow rings appear               0.85s
        # 2.95–3.23  "India" panel slams             0.28s
        # 3.23–4.01  narration writes                0.78s
        # 4.01–5.21  hold                            1.20s
        # 5.21–5.71  narration cross-fades           0.50s
        # 5.71–9.71  hold + slow zoom toward India   4.00s
        # 9.71–12.0  clean exit (panel only)         2.29s
        # ══════════════════════════════════════════════════════════════
        map_bg = Rectangle(width=15.5, height=9.5, fill_color=MAP_GREEN,
                             fill_opacity=0.26, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(map_bg, run_time=0.40))

        world = make_world_dots()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in world],
                               lag_ratio=0.003, run_time=1.30))

        india   = make_india_shape()
        glows   = make_india_glow(scale=1.0)
        self.play(FadeIn(india, run_time=0.40))
        self.play(LaggedStart(*[GrowFromCenter(r) for r in glows],
                               lag_ratio=0.22, run_time=0.85))

        PW1 = 3.6
        tp1 = ink_panel(PW1, 0.72, fill="#FFF8E8", stroke=ORANGE, sw=3.0)\
                .move_to([INDIA_C[0], TOP_Y, 0])
        tt1 = fit_text("India", max_width=PW1-0.30, size=34, color=ORANGE)\
                .move_to(tp1[1].get_center())
        slam(self, tp1, from_dir=UP, rt=0.28)
        self.add(tt1)
        self.play(FadeIn(tt1, run_time=0.18))

        n1a = nar("And India?")
        n1b = nar("Where does India stand in this race?", color=ORANGE)
        self.play(Write(n1a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n1a, run_time=0.25), FadeIn(n1b, run_time=0.25))

        # Slow Ken Burns zoom toward India
        self.play(
            world.animate.scale(1.12).shift(LEFT*0.60+DOWN*0.20),
            map_bg.animate.scale(1.12).shift(LEFT*0.60+DOWN*0.20),
            india.animate.scale(1.12).shift(LEFT*0.60+DOWN*0.20),
            glows.animate.scale(1.12).shift(LEFT*0.60+DOWN*0.20),
            run_time=4.00, rate_func=smooth,
        )

        self.play(FadeOut(tp1, run_time=0.55),
                   FadeOut(tt1, run_time=0.55),
                   FadeOut(n1b, run_time=0.55))
        # Keep: world, map_bg, india, glows
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  12s → 28s  │  Import dependency
        #
        # "IMPORT" stamp slams. 8 import arrows draw in lagged
        # from world sources toward India.
        #
        # 0.00–0.28  IMPORT stamp slams             0.28s
        # 0.28–0.40  stamp wobble                   0.12s
        # 0.40–1.40  8 arrows draw in (lagged)      1.00s
        # 1.40–2.18  narration writes               0.78s
        # 2.18–3.38  hold                           1.20s
        # 3.38–3.88  narration cross-fades          0.50s
        # 3.88–14.0  hold                           10.12s
        # 14.0–16.0  clean exit (arrows stay B3)    2.00s
        # ══════════════════════════════════════════════════════════════
        PW2 = 3.8
        st2 = stamp("IMPORT", color=BLUE, w=PW2, h=0.82)\
                .move_to([0, TOP_Y, 0])
        slam(self, st2, from_dir=UP, rt=0.28)
        self.play(Rotate(st2, PI/28, run_time=0.12, rate_func=there_and_back))

        arrows = make_import_arrows(n=8)
        self.play(LaggedStart(*[Create(a) for a in arrows],
                               lag_ratio=0.12, run_time=1.00))

        n2a = nar("India doesn't make chips... it imports them.")
        n2b = nar("Every single one. From abroad.", color=BLUE)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))
        self.wait(10.12)

        self.play(FadeOut(st2, run_time=0.55),
                   FadeOut(n2b, run_time=0.55))
        # Keep: arrows, world, india, glows
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  28s → 44s  │  Everyday devices
        #
        # Phone, laptop, car pop in — positioned along the import
        # arrow paths (midpoints) to show the goods flowing in.
        # Zoom-in on India.
        #
        # 0.00–0.50  "Phones, Laptops, Cars" panel   0.50s
        # 0.50–0.78  phone pops in                   0.28s
        # 0.78–1.06  laptop pops in                  0.28s
        # 1.06–1.34  car pops in                     0.28s
        # 1.34–1.56  icon labels fade in             0.22s
        # 1.56–2.34  narration writes                0.78s
        # 2.34–3.54  hold                            1.20s
        # 3.54–4.04  narration cross-fades           0.50s
        # 4.04–4.74  zoom-in on India                0.70s
        # 4.74–14.0  hold                            9.26s
        # 14.0–16.0  clean exit                      2.00s
        # ══════════════════════════════════════════════════════════════
        PW3 = 5.6
        tp3 = ink_panel(PW3, 0.72).move_to([0, TOP_Y, 0])
        tt3 = fit_text("Phones, Laptops, Cars", max_width=PW3-0.40, size=28)\
                .move_to(tp3[1].get_center())
        self.play(GrowFromCenter(tp3, run_time=0.28),
                   Write(tt3, run_time=0.40))

        # Place icons near India but slightly spread — not on top of each other
        phone  = make_phone().scale(0.72).move_to(INDIA_C + LEFT*2.20 + UP*0.80)
        laptop = make_laptop().scale(0.72).move_to(INDIA_C + UP*1.60)
        car    = make_car().scale(0.68).move_to(INDIA_C + RIGHT*2.50 + UP*0.80)

        ph_lbl = Ts("Phone").next_to(phone,  DOWN, buff=0.18)
        lp_lbl = Ts("Laptop").next_to(laptop, DOWN, buff=0.18)
        ca_lbl = Ts("Car").next_to(car,    DOWN, buff=0.18)

        for icon, lbl in [(phone, ph_lbl), (laptop, lp_lbl), (car, ca_lbl)]:
            self.play(GrowFromCenter(icon, run_time=0.28))
        self.play(FadeIn(ph_lbl, run_time=0.08),
                   FadeIn(lp_lbl, run_time=0.08),
                   FadeIn(ca_lbl, run_time=0.08))

        n3a = nar("Every phone... every laptop... every car...")
        n3b = nar("All running on imported chips.", color=ORANGE)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))

        # Zoom-in toward India
        all_stage = VGroup(world, map_bg, india, glows, arrows,
                            phone, laptop, car, ph_lbl, lp_lbl, ca_lbl)
        self.play(all_stage.animate.scale(1.10).shift(LEFT*0.40+DOWN*0.10),
                   run_time=0.70, rate_func=smooth)
        self.wait(9.26)

        self.play(FadeOut(tp3,   run_time=0.55),
                   FadeOut(tt3,   run_time=0.55),
                   FadeOut(n3b,   run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  44s → 64s  │  Reliance on others
        #
        # "DEPENDENT" red stamp slams. Passing flash on all arrows
        # (looped 4x) to show continuous flow. Slow pan-left + zoom.
        #
        # 0.00–0.28  DEPENDENT stamp slams          0.28s
        # 0.28–0.40  stamp wobble                   0.12s
        # 0.40–2.60  4 rounds ShowPassingFlash       2.20s  (0.55s each)
        # 2.60–3.38  narration writes               0.78s
        # 3.38–4.58  hold                           1.20s
        # 4.58–5.08  narration cross-fades          0.50s
        # 5.08–5.78  slow pan-left + zoom           0.70s
        # 5.78–18.0  hold                           12.22s
        # 18.0–20.0  clean exit                     2.00s
        # ══════════════════════════════════════════════════════════════
        PW4 = 5.0
        st4 = stamp("DEPENDENT", color=RED, w=PW4, h=0.82)\
                .move_to([0, TOP_Y, 0])
        slam(self, st4, from_dir=UP, rt=0.28)
        self.play(Rotate(st4, -PI/26, run_time=0.12, rate_func=there_and_back))

        # Looped passing flash on all arrows — shows continuous flow
        for _ in range(4):
            self.play(*[
                ShowPassingFlash(
                    arc.copy().set_stroke(BLUE, 3.5),
                    time_width=0.45, run_time=0.55
                )
                for arc in arrows
            ])

        n4a = nar("India depends heavily on other countries.")
        n4b = nar("For the technology that powers its future.", color=RED)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))

        # Pan-left + slight zoom
        self.play(all_stage.animate.shift(RIGHT*0.30).scale(0.96),
                   run_time=0.70, rate_func=smooth)
        self.wait(12.22)

        # Clean exit — fade all except world dots + map_bg + india (stay for B5)
        self.play(
            FadeOut(st4,    run_time=0.60),
            FadeOut(n4b,    run_time=0.60),
            FadeOut(arrows, run_time=0.60),
            FadeOut(phone,  run_time=0.60),
            FadeOut(laptop, run_time=0.60),
            FadeOut(car,    run_time=0.60),
            FadeOut(ph_lbl, run_time=0.60),
            FadeOut(lp_lbl, run_time=0.60),
            FadeOut(ca_lbl, run_time=0.60),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  64s → 80s  │  Story not finished
        #
        # India shape stays. Rising bar chart appears beside India.
        # Small factory icon below chart. "OPPORTUNITY" gold stamp.
        # Zoom-out. Fade to black.
        #
        # 0.00–0.60  world dims slightly             0.60s
        # 0.60–0.88  OPPORTUNITY stamp slams         0.28s
        # 0.88–1.00  stamp wobble                    0.12s
        # 1.00–1.70  bar chart grows bar by bar      0.70s
        # 1.70–2.10  factory appears below chart     0.40s
        # 2.10–2.88  narration writes                0.78s
        # 2.88–4.08  hold                            1.20s
        # 4.08–4.58  narration cross-fades           0.50s
        # 4.58–7.58  hold                            3.00s
        # 7.58–8.28  zoom-out                        0.70s
        # 8.28–9.78  fade to black overlay           1.50s
        # ══════════════════════════════════════════════════════════════

        # Dim world slightly — India stays bright
        self.play(
            world.animate.set_opacity(0.18),
            map_bg.animate.set_fill(opacity=0.12),
            run_time=0.60,
        )

        PW5 = 5.4
        st5 = stamp("OPPORTUNITY", color=GOLD, w=PW5, h=0.82)\
                .move_to([0, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, PI/30, run_time=0.12, rate_func=there_and_back))

        # Bar chart — positioned LEFT of India so it doesn't overlap the shape
        chart = make_rising_bar_chart().scale(0.80)\
                  .move_to([-3.20, 0.40, 0])

        # Animate bars growing one by one
        bars_grp = chart[0]   # VGroup of 4 bars
        rest_grp = VGroup(chart[1], chart[2], chart[3])  # axis + labels + title
        self.play(FadeIn(rest_grp, run_time=0.25))
        for bar in bars_grp:
            self.play(GrowFromEdge(bar, DOWN, run_time=0.18))

        # Factory — below chart, slightly right
        factory = make_small_factory(pos=np.array([-3.20, -1.55, 0]))\
                    .scale(0.80)
        self.play(GrowFromCenter(factory, run_time=0.40))

        n5a = nar("But the story doesn't end here...")
        n5b = nar("India is starting to change this.", color=GOLD)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))
        self.wait(3.00)

        # Zoom out
        stage_all = VGroup(world, map_bg, india, glows, chart,
                            factory, st5)
        self.play(stage_all.animate.scale(0.78).shift(DOWN*0.10),
                   run_time=0.70, rate_func=smooth)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)