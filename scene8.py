"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 8: India's Opportunity  |  70 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 12s │ 12s │ Initiative start   — India box glows, START stamp
Beat 2 │ 12s → 28s │ 16s │ Mission reveal     — MISSION stamp + glow lines
Beat 3 │ 28s → 46s │ 18s │ Infrastructure     — 5 factories rise + bar chart
Beat 4 │ 46s → 60s │ 14s │ Growth trajectory  — line chart draws upward
Beat 5 │ 60s → 70s │ 10s │ Open question      — "?" stamp + pulse + fade
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 70s | No character | English only | Style: Oversimplified

LAYOUT
  India box  : centred at INDIA_C = (0.0, 0.0) — stage centre for this scene
               (unlike Scene 7 where it was on the right; here India is the
               sole focus so we centre it)
  Factories  : x = -4.5 to -0.5, y = -0.8 (left of India, right half clear)
  Charts     : x = +2.0 to +5.5 (right of India)
  TOP_Y      :  3.0
  NAR_Y      : -3.10

Render:
  Preview : manim -pql scene8.py Scene8
  1080p   : manim -pqh scene8.py Scene8
  4K      : manim -pqk scene8.py Scene8
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────────────────
BG         = "#F5F0E8"
INK        = "#1A1008"
RED        = "#D42B2B"
BLUE       = "#2255AA"
GOLD       = "#C8960C"
CREAM      = "#FFFDF8"
MAP_GREEN  = "#C8D8B0"
SUBTLE     = "#9A8F7E"
WHITE      = "#FFFFFF"
ORANGE     = "#E07820"
INDIA_FILL = "#FFD080"
GREEN_COL  = "#1A8A2A"
ELECTRIC   = "#00C8FF"
FONT       = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.0
NAR_Y   = -3.10

# India box centred at stage centre for this scene
INDIA_C = np.array([0.0, 0.0, 0])


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
    return VGroup(*[Dot([x,y,0], radius=0.028, color=BLUE, fill_opacity=0.22)
                    for x,y in pts])


def make_india_box():
    """Rounded rectangle India box — centred at INDIA_C."""
    box = RoundedRectangle(corner_radius=0.18, width=2.20, height=2.60,
                            color=ORANGE, fill_color=INDIA_FILL,
                            fill_opacity=0.82, stroke_width=3.5)\
            .move_to(INDIA_C)
    lbl = T("India", size=30, color=ORANGE).move_to(INDIA_C)
    return VGroup(box, lbl)


def make_india_glow_rings():
    """Three concentric orange rings around India box."""
    return VGroup(*[
        Circle(radius=r, color=ORANGE,
                stroke_opacity=0.55 - i*0.16, stroke_width=2.2)\
          .move_to(INDIA_C)
        for i, r in enumerate([1.45, 1.80, 2.20])
    ])


def make_glow_lines(n=8):
    """
    Short radial lines emanating from India box — represent
    the semiconductor mission spreading outward.
    """
    lines = VGroup()
    for a in np.linspace(0, TAU, n, endpoint=False):
        start = INDIA_C + 1.20 * np.array([np.cos(a), np.sin(a), 0])
        end   = INDIA_C + 2.20 * np.array([np.cos(a), np.sin(a), 0])
        lines.add(Line(start, end, color=ELECTRIC,
                        stroke_width=2.0, stroke_opacity=0.65))
    return lines


def make_factory_rising(pos, color=INK):
    """
    Factory that slides up from below — used in Beat 3 flood.
    Returns VGroup positioned at pos.
    """
    body  = Rectangle(width=1.10, height=0.88, color=color,
                        fill_color="#1E2A3A", fill_opacity=1, stroke_width=2.5)
    chim1 = Rectangle(width=0.18, height=0.38, color=color,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=2)\
              .next_to(body, UP, buff=0).shift(LEFT*0.25)
    chim2 = Rectangle(width=0.14, height=0.28, color=color,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=2)\
              .next_to(body, UP, buff=0).shift(RIGHT*0.18)
    base  = Rectangle(width=1.30, height=0.16, color=color,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=1.5)\
              .next_to(body, DOWN, buff=0)
    win   = Rectangle(width=0.30, height=0.22, color=GREEN_COL,
                        fill_color=GREEN_COL, fill_opacity=0.28,
                        stroke_width=1.5).move_to(body.get_center())
    return VGroup(base, body, chim1, chim2, win).move_to(pos)


def make_bar_chart():
    """
    5-bar rising bar chart for Beat 3.
    Each bar is grown with GrowFromEdge(bar, DOWN).
    Positioned to the RIGHT of India box (x: 2.8 to 5.6).
    """
    heights = [0.55, 0.90, 1.35, 1.85, 2.40]
    colors  = [BLUE, BLUE, ORANGE, ORANGE, GREEN_COL]
    bar_w   = 0.52
    gap     = 0.18
    ox      = 3.40 - ((len(heights)-1) * (bar_w+gap)) / 2
    oy      = -0.90   # axis y

    bars = VGroup()
    for i, (h, col) in enumerate(zip(heights, colors)):
        x   = ox + i*(bar_w+gap)
        bar = Rectangle(width=bar_w, height=h, color=col,
                          fill_color=col, fill_opacity=0.85, stroke_width=2)\
                .move_to([x, oy + h/2, 0])
        bars.add(bar)

    axis  = Line(LEFT*1.40, RIGHT*1.40, color=INK, stroke_width=2.5)\
              .move_to([3.40, oy, 0])
    ylbls = VGroup(*[
        Ts(yr, size=16, color=SUBTLE).move_to([ox + i*(bar_w+gap), oy-0.28, 0])
        for i, yr in enumerate(["21","22","23","24","25"])
    ])
    title = fit_text("India Fab Investment",
                      max_width=3.00, size=19, color=INK, weight=NORMAL)\
              .move_to([3.40, oy + 2.75, 0])
    return VGroup(bars, axis, ylbls, title)


def make_line_chart():
    """
    Upward-trending line chart drawn with VMobject for Beat 4.
    The line is created progressively via Create().
    Positioned RIGHT of India box.
    """
    # Data points (x offset from chart origin, y value)
    data = [(0.00, 0.20), (0.55, 0.45), (1.10, 0.80),
            (1.65, 1.20), (2.20, 1.70), (2.75, 2.10),
            (3.00, 2.35)]   # slight slowdown near top
    ox, oy = 2.80, -0.90

    pts = [np.array([ox + dx, oy + dy, 0]) for dx, dy in data]

    line = VMobject(stroke_color=GREEN_COL, stroke_width=3.5,
                     stroke_opacity=0.95)
    line.set_points_as_corners(pts)

    # Dot markers at each data point
    dots = VGroup(*[
        Dot(p, radius=0.07, color=GREEN_COL, fill_opacity=1) for p in pts
    ])

    # Axes
    ax_x = Line([ox-0.15, oy, 0], [ox+3.20, oy, 0],
                 color=INK, stroke_width=2.2)
    ax_y = Line([ox-0.15, oy, 0], [ox-0.15, oy+2.70, 0],
                 color=INK, stroke_width=2.2)

    title = fit_text("Growth Trajectory", max_width=2.80,
                      size=19, color=INK, weight=NORMAL)\
              .move_to([ox+1.50, oy+2.95, 0])

    return VGroup(ax_x, ax_y, title), line, dots


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene8(Scene):
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
        # BEAT 1  │  0s → 12s  │  Initiative start
        #
        # Faint world map + India box glows at centre.
        # "START" green stamp slams. Ken Burns zoom-in.
        #
        # 0.00–0.40  world map fades in (dim)        0.40s
        # 0.40–1.10  India box grows from centre     0.70s
        # 1.10–1.95  glow rings appear (lagged)      0.85s
        # 1.95–2.23  START stamp slams               0.28s
        # 2.23–2.35  stamp wobble                    0.12s
        # 2.35–3.13  narration writes                0.78s
        # 3.13–4.33  hold                            1.20s
        # 4.33–4.83  narration cross-fades           0.50s
        # 4.83–9.83  hold + slow zoom                5.00s
        # 9.83–12.0  clean exit (stamp only)         2.17s
        # ══════════════════════════════════════════════════════════════
        map_bg = Rectangle(width=15.5, height=9.5, fill_color=MAP_GREEN,
                             fill_opacity=0.16, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(map_bg, run_time=0.40))

        world = make_world_dots()
        self.add(world)

        india  = make_india_box()
        g_rings = make_india_glow_rings()
        self.play(GrowFromCenter(india, run_time=0.70))
        self.play(LaggedStart(*[GrowFromCenter(r) for r in g_rings],
                               lag_ratio=0.22, run_time=0.85))

        PW1 = 4.0
        st1 = stamp("START", color=GREEN_COL, w=PW1, h=0.82)\
                .move_to([0, TOP_Y, 0])
        slam(self, st1, from_dir=UP, rt=0.28)
        self.play(Rotate(st1, PI/28, run_time=0.12, rate_func=there_and_back))

        n1a = nar("India has now started taking steps.")
        n1b = nar("The semiconductor race has begun.", color=GREEN_COL)
        self.play(Write(n1a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n1a, run_time=0.25), FadeIn(n1b, run_time=0.25))

        # Slow zoom-in
        self.play(
            india.animate.scale(1.08),
            g_rings.animate.scale(1.08),
            run_time=5.00, rate_func=smooth,
        )

        self.play(FadeOut(st1, run_time=0.55),
                   FadeOut(n1b, run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  12s → 28s  │  Mission reveal
        #
        # "MISSION" blue stamp. 8 glow lines radiate outward from
        # India box — represent semiconductor mission spreading.
        # ShowPassingFlash on each line. "Semiconductor Mission" panel.
        #
        # 0.00–0.28  MISSION stamp slams             0.28s
        # 0.28–0.40  stamp wobble                    0.12s
        # 0.40–0.90  "Semiconductor Mission" panel   0.50s
        # 0.90–1.60  glow lines create (lagged)      0.70s
        # 1.60–2.30  passing flash on lines x2       0.70s
        # 2.30–3.08  narration writes                0.78s
        # 3.08–4.28  hold                            1.20s
        # 4.28–4.78  narration cross-fades           0.50s
        # 4.78–14.0  hold + pan-right                9.22s
        # 14.0–16.0  clean exit                      2.00s
        # ══════════════════════════════════════════════════════════════
        PW2a = 3.6
        st2  = stamp("MISSION", color=BLUE, w=PW2a, h=0.82)\
                 .move_to([-3.20, TOP_Y, 0])
        slam(self, st2, from_dir=UP, rt=0.28)
        self.play(Rotate(st2, -PI/28, run_time=0.12, rate_func=there_and_back))

        PW2b = 4.8
        tp2  = ink_panel(PW2b, 0.72, fill="#E8F0FF", stroke=BLUE, sw=2.5)\
                 .move_to([3.00, TOP_Y, 0])
        tt2  = fit_text("Semiconductor Mission",
                         max_width=PW2b-0.40, size=26, color=BLUE)\
                 .move_to(tp2[1].get_center())
        self.play(GrowFromCenter(tp2, run_time=0.28),
                   Write(tt2, run_time=0.40))

        g_lines = make_glow_lines(n=8)
        self.play(LaggedStart(*[Create(ln) for ln in g_lines],
                               lag_ratio=0.09, run_time=0.70))

        # Passing flash on lines
        for _ in range(2):
            self.play(*[
                ShowPassingFlash(ln.copy().set_stroke(ELECTRIC, 3.5),
                                  time_width=0.50, run_time=0.35)
                for ln in g_lines
            ])

        n2a = nar("With its semiconductor mission...")
        n2b = nar("And long-term plans to build capacity.", color=BLUE)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))

        # Slow pan right
        self.play(
            india.animate.shift(LEFT*0.25),
            g_rings.animate.shift(LEFT*0.25),
            g_lines.animate.shift(LEFT*0.25),
            run_time=9.22, rate_func=smooth,
        )

        self.play(FadeOut(st2,    run_time=0.55),
                   FadeOut(tp2,    run_time=0.55),
                   FadeOut(tt2,    run_time=0.55),
                   FadeOut(g_lines,run_time=0.55),
                   FadeOut(n2b,    run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  28s → 46s  │  Infrastructure build
        #
        # 5 factory icons slide up from below the stage on the LEFT side.
        # Bar chart on the RIGHT grows bar by bar.
        # Zoom-in on factories.
        #
        # Factories at x: -5.5, -4.2, -3.0, -1.8, -0.6  y: -0.80
        # Bar chart at x: 2.8 – 5.6
        #
        # 0.00–0.50  "New Factories" panel           0.50s
        # 0.50–2.00  5 factories slide up (lagged)   1.50s
        # 2.00–2.70  bar chart axis + title appear   0.70s
        # 2.70–3.60  5 bars grow one by one          0.90s  (0.18s each)
        # 3.60–4.38  narration writes                0.78s
        # 4.38–5.58  hold                            1.20s
        # 5.58–6.08  narration cross-fades           0.50s
        # 6.08–6.78  zoom-in on factories            0.70s
        # 6.78–16.0  hold                            9.22s
        # 16.0–18.0  clean exit (chart stays for B4) 2.00s
        # ══════════════════════════════════════════════════════════════
        PW3 = 4.4
        tp3 = ink_panel(PW3, 0.72).move_to([0, TOP_Y, 0])
        tt3 = fit_text("New Factories", max_width=PW3-0.40, size=30)\
                .move_to(tp3[1].get_center())
        self.play(GrowFromCenter(tp3, run_time=0.28),
                   Write(tt3, run_time=0.40))

        fac_xs   = [-5.50, -4.20, -3.00, -1.80, -0.60]
        fac_y    = -0.80
        factories = VGroup(*[
            make_factory_rising(pos=np.array([x, fac_y, 0]))
            for x in fac_xs
        ])
        # Start off below screen, slide up
        factories.shift(DOWN * 3.5)
        self.add(factories)
        self.play(
            LaggedStart(*[
                f.animate.shift(UP * 3.5)
                for f in factories
            ], lag_ratio=0.20, run_time=1.50, rate_func=smooth),
        )

        # Bar chart
        chart      = make_bar_chart()
        bars_grp   = chart[0]
        rest_grp   = VGroup(chart[1], chart[2], chart[3])
        self.play(FadeIn(rest_grp, run_time=0.40))
        for bar in bars_grp:
            self.play(GrowFromEdge(bar, DOWN, run_time=0.18))

        n3a = nar("New fab plants... new investments...")
        n3b = nar("Growing infrastructure.", color=GREEN_COL)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))

        # Zoom-in on factories side
        fac_zone = VGroup(factories, india, g_rings)
        self.play(fac_zone.animate.scale(1.06).shift(RIGHT*0.15),
                   run_time=0.70, rate_func=smooth)
        self.wait(9.22)

        self.play(FadeOut(tp3, run_time=0.55),
                   FadeOut(tt3, run_time=0.55),
                   FadeOut(n3b, run_time=0.55))
        # Keep: factories, bars_grp, rest_grp, india, g_rings
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  46s → 60s  │  Growth trajectory
        #
        # Bar chart fades. Line chart draws progressively upward.
        # Line slows near the top — "the question remains".
        # Pan-up effect via shifting everything down.
        #
        # 0.00–0.40  bar chart fades out             0.40s
        # 0.40–0.80  line chart axes + title appear  0.40s
        # 0.80–2.00  line draws progressively        1.20s
        # 2.00–2.40  dots pop in                     0.40s
        # 2.40–3.18  narration writes                0.78s
        # 3.18–4.38  hold                            1.20s
        # 4.38–4.88  narration cross-fades           0.50s
        # 4.88–5.58  pan-up (shift stage down)       0.70s
        # 5.58–12.0  hold                            6.42s
        # 12.0–14.0  clean exit                      2.00s
        # ══════════════════════════════════════════════════════════════
        self.play(FadeOut(chart, run_time=0.40))

        axes, line_mob, dots_mob = make_line_chart()
        self.play(FadeIn(axes, run_time=0.40))
        self.play(Create(line_mob, run_time=1.20, rate_func=linear))
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots_mob],
                               lag_ratio=0.08, run_time=0.40))

        n4a = nar("The growth has begun...")
        n4b = nar("But the question remains.", color=ORANGE)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))

        # Pan-up — shift stage content down slightly
        pan_group = VGroup(factories, fac_zone, axes, line_mob, dots_mob,
                            chart, india, g_rings)
        self.play(pan_group.animate.shift(DOWN*0.35),
                   run_time=0.70, rate_func=smooth)
        self.wait(6.42)

        self.play(FadeOut(axes,     run_time=0.55),
                   FadeOut(line_mob, run_time=0.55),
                   FadeOut(dots_mob, run_time=0.55),
                   FadeOut(factories,run_time=0.55),
                   FadeOut(n4b,      run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  60s → 70s  │  Open question
        #
        # India box stays centred. "?" gold stamp slams.
        # Subtle electric pulse on glow rings.
        # World map dims. Zoom-out. Fade to black.
        #
        # 0.00–0.28  "?" stamp slams                 0.28s
        # 0.28–0.40  stamp wobble                    0.12s
        # 0.40–0.70  "Can India Lead?" panel         0.30s
        # 0.70–1.48  narration writes                0.78s
        # 1.48–2.68  hold                            1.20s
        # 2.68–3.18  narration cross-fades           0.50s
        # 3.18–3.63  ring pulse (3 x there_and_back) 0.45s
        # 3.63–5.13  hold                            1.50s
        # 5.13–5.83  zoom-out                        0.70s
        # 5.83–7.33  fade to black                   1.50s
        # ══════════════════════════════════════════════════════════════

        # Restore India to centre after pan shift
        self.play(india.animate.move_to(INDIA_C),
                   g_rings.animate.move_to(INDIA_C),
                   run_time=0.25)

        PW5a = 2.2
        st5  = stamp("?", color=GOLD, w=PW5a, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, PI/22, run_time=0.12, rate_func=there_and_back))

        PW5b = 4.4
        tp5  = ink_panel(PW5b, 0.72, fill="#FFFBE6", stroke=GOLD, sw=2.5)\
                 .move_to([0, TOP_Y - 1.10, 0])
        tt5  = fit_text("Can India Lead?", max_width=PW5b-0.40, size=28, color=GOLD)\
                 .move_to(tp5[1].get_center())
        self.play(GrowFromCenter(tp5, run_time=0.18),
                   Write(tt5, run_time=0.28))

        n5a = nar("Can India make the right moves...")
        n5b = nar("At the right time?", size=40, color=GOLD)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))

        # Subtle ring pulse
        for _ in range(3):
            self.play(g_rings.animate.scale(1.08).set_stroke(color=GOLD),
                       run_time=0.08, rate_func=linear)
            self.play(g_rings.animate.scale(1/1.08).set_stroke(color=ORANGE),
                       run_time=0.07, rate_func=linear)

        self.wait(1.50)

        # Zoom out
        stage_all = VGroup(india, g_rings, st5, tp5, tt5, map_bg, world)
        self.play(stage_all.animate.scale(0.78).shift(DOWN*0.10),
                   run_time=0.70, rate_func=smooth)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)