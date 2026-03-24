"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 6: The Global Chip War  |  75 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 12s │ 12s │ Conflict setup     — world map, "Global Chip Race"
Beat 2 │ 12s → 28s │ 16s │ USA vs China       — split screen blue/red
Beat 3 │ 28s → 44s │ 16s │ Tech side (USA)    — chips + AI icons + electricity
Beat 4 │ 44s → 60s │ 16s │ Mfg side (China)   — factories + gears flood
Beat 5 │ 60s → 75s │ 15s │ Taiwan balance     — Taiwan centre, arcs both sides
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 75s | No character | English only | Style: Oversimplified

LAYOUT ZONES
  TOP_Y   =  3.0   stamps / title panels
  STAGE_Y =  0.0   main stage
  NAR_Y   = -3.10  narration strip
  DIVIDER : x = 0  vertical centre line for split screen

COLOUR ASSIGNMENT
  USA side  : BLUE (#2255AA) + ELECTRIC (#00C8FF)
  China side: RED  (#D42B2B) + WARM_RED (#FF4444)
  Taiwan    : GOLD (#C8960C)

Render:
  Preview : manim -pql scene6.py Scene6
  1080p   : manim -pqh scene6.py Scene6
  4K      : manim -pqk scene6.py Scene6
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
ELECTRIC  = "#00C8FF"
USA_FILL  = "#D6E4FF"   # soft blue tint for USA panel
CHN_FILL  = "#FFD6D6"   # soft red tint for China panel
FONT      = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.0
NAR_Y   = -3.10

TW = np.array([0.0, 0.30, 0])   # Taiwan centred in Beat 5


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
# SPLIT SCREEN PANELS
# ─────────────────────────────────────────────────────────────
def make_usa_panel():
    """Left half — blue tint background panel."""
    panel = Rectangle(width=7.15, height=4.80, color=BLUE,
                       fill_color=USA_FILL, fill_opacity=0.50,
                       stroke_width=3)
    panel.move_to([-3.58, STAGE_Y + 0.50, 0])
    return panel

def make_china_panel():
    """Right half — red tint background panel."""
    panel = Rectangle(width=7.15, height=4.80, color=RED,
                       fill_color=CHN_FILL, fill_opacity=0.50,
                       stroke_width=3)
    panel.move_to([3.58, STAGE_Y + 0.50, 0])
    return panel

def make_divider():
    """Bold vertical centre line separating the two sides."""
    return Line(UP*2.90, DOWN*1.90, color=INK,
                 stroke_width=4, stroke_opacity=0.55)

def side_label(text, color, pos):
    """Bold country label for split screen."""
    pw = 3.0
    p  = ink_panel(pw, 0.72, fill=CREAM, stroke=color, sw=3.5).move_to(pos)
    t  = fit_text(text, max_width=pw-0.30, size=30, color=color)\
           .move_to(p[1].get_center())
    return VGroup(p, t)


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

def make_chip(sc=1.0):
    base = Square(side_length=1.40*sc, color=INK, fill_color="#1C2833",
                   fill_opacity=1, stroke_width=4)
    die  = Square(side_length=0.90*sc, color=GOLD, fill_color="#2C3E50",
                   fill_opacity=1, stroke_width=2.5)
    grid = VGroup(*[
        Line([v*sc,-0.45*sc,0],[v*sc,0.45*sc,0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30,0.30,4)
    ] + [
        Line([-0.45*sc,v*sc,0],[0.45*sc,v*sc,0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30,0.30,4)
    ])
    core = Square(side_length=0.26*sc, color=RED, fill_color=RED,
                   fill_opacity=1, stroke_width=0)
    pins = VGroup(*[
        Rectangle(width=0.08*sc, height=0.20*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([-0.48*sc+i*0.24*sc, sg*0.80*sc, 0])
        for i in range(5) for sg in [1,-1]
    ] + [
        Rectangle(width=0.20*sc, height=0.08*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([sg*0.80*sc,-0.48*sc+i*0.24*sc, 0])
        for i in range(5) for sg in [1,-1]
    ])
    return VGroup(base, pins, die, grid, core)

def make_server():
    """Server rack icon for the USA tech side."""
    rack = VGroup()
    for i in range(4):
        unit = RoundedRectangle(corner_radius=0.04, width=1.40, height=0.24,
                                 color=BLUE, fill_color="#1A2A3A",
                                 fill_opacity=1, stroke_width=2)\
                 .shift(DOWN*i*0.30)
        led  = Circle(radius=0.05, color=ELECTRIC, fill_color=ELECTRIC,
                       fill_opacity=1, stroke_width=0)\
                 .move_to(unit.get_right()+LEFT*0.12)
        slt  = Rectangle(width=0.80, height=0.08, color=SUBTLE,
                          fill_color=SUBTLE, fill_opacity=0.55)\
                 .move_to(unit.get_center())
        rack.add(unit, led, slt)
    border = RoundedRectangle(corner_radius=0.09, width=1.62, height=1.30,
                               color=BLUE, stroke_width=2.5, fill_opacity=0)
    return VGroup(rack, border)

def make_ai_node():
    """Simple AI brain-network node cluster."""
    np.random.seed(9)
    node_pos = [ORIGIN,
                UP*0.55, DOWN*0.55, LEFT*0.55, RIGHT*0.55,
                UP*0.40+RIGHT*0.40, DOWN*0.40+LEFT*0.40,
                UP*0.40+LEFT*0.40,  DOWN*0.40+RIGHT*0.40]
    nodes = VGroup(*[
        Circle(radius=0.09, color=ELECTRIC, fill_color=ELECTRIC,
                fill_opacity=0.85, stroke_width=0).move_to(p)
        for p in node_pos
    ])
    edges = VGroup(*[
        Line(node_pos[0], p, color=ELECTRIC,
              stroke_width=1.2, stroke_opacity=0.55)
        for p in node_pos[1:]
    ])
    return VGroup(edges, nodes)

def make_gear(r=0.40, teeth=10, pos=ORIGIN):
    """
    Simple gear shape using a polygon with alternating tall/short radii.
    """
    angles = []
    radii  = []
    for i in range(teeth):
        base_a = i * TAU / teeth
        angles += [base_a, base_a + 0.5*TAU/teeth]
        radii  += [r * 1.28, r]
    pts = [np.array([rad*np.cos(a), rad*np.sin(a), 0])
           for a, rad in zip(angles, radii)]
    gear = Polygon(*pts, color=INK, fill_color="#3A2010",
                    fill_opacity=0.90, stroke_width=2.5)
    hub  = Circle(radius=r*0.22, color=INK, fill_color="#1A0808",
                   fill_opacity=1, stroke_width=2)
    return VGroup(gear, hub).move_to(pos)

def make_small_factory(pos=ORIGIN, color=RED):
    """Compact factory for China manufacturing side."""
    body  = Rectangle(width=1.10, height=0.88, color=color,
                        fill_color="#2A1010", fill_opacity=1, stroke_width=2.5)\
              .move_to(pos)
    chim1 = Rectangle(width=0.18, height=0.40, color=color,
                        fill_color="#1A0808", fill_opacity=1, stroke_width=2)\
              .move_to(pos+UP*0.64+LEFT*0.25)
    chim2 = Rectangle(width=0.14, height=0.30, color=color,
                        fill_color="#1A0808", fill_opacity=1, stroke_width=2)\
              .move_to(pos+UP*0.54+RIGHT*0.20)
    base  = Rectangle(width=1.30, height=0.16, color=color,
                        fill_color="#1A0808", fill_opacity=1, stroke_width=1.5)\
              .move_to(pos+DOWN*0.52)
    win   = Rectangle(width=0.28, height=0.22, color=RED,
                        fill_color=RED, fill_opacity=0.22,
                        stroke_width=1.5).move_to(pos)
    return VGroup(base, body, chim1, chim2, win)

def make_lightning(start, end, steps=8, seed=0):
    np.random.seed(seed)
    pts = [np.array(start)]
    for i in range(1, steps):
        t    = i/steps
        mid  = np.array(start)*(1-t)+np.array(end)*t
        d    = np.array(end)-np.array(start)
        perp = np.array([-d[1],d[0],0])
        n    = np.linalg.norm(perp)
        if n>1e-4: perp/=n
        pts.append(mid+perp*(np.random.rand()-0.5)*0.26)
    pts.append(np.array(end))
    bolt = VMobject(stroke_color=ELECTRIC, stroke_width=3.8, stroke_opacity=0.95)
    bolt.set_points_as_corners(pts)
    return bolt


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene6(Scene):
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
        # BEAT 1  │  0s → 12s  │  Conflict setup
        #
        # World map fades in. "Global Chip Race" panel slams.
        # Slow Ken Burns zoom-in.
        #
        # 0.00–0.40  map bg fades in                 0.40s
        # 0.40–1.70  world dots appear               1.30s
        # 1.70–1.98  panel slams                     0.28s
        # 1.98–2.76  narration writes                0.78s
        # 2.76–3.96  hold                            1.20s
        # 3.96–4.46  narration cross-fades           0.50s
        # 4.46–9.46  hold + slow zoom                5.00s
        # 9.46–12.0  clean exit                      2.54s
        # ══════════════════════════════════════════════════════════════
        map_bg = Rectangle(width=15.5, height=9.5, fill_color=MAP_GREEN,
                             fill_opacity=0.26, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(map_bg, run_time=0.40))

        world = make_world_dots()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in world],
                               lag_ratio=0.003, run_time=1.30))

        PW1 = 5.4
        tp1 = ink_panel(PW1, 0.72).move_to([0, TOP_Y, 0])
        tt1 = fit_text("Global Chip Race", max_width=PW1-0.40, size=32)\
                .move_to(tp1[1].get_center())
        slam(self, tp1, from_dir=UP, rt=0.28)
        self.add(tt1)
        self.play(FadeIn(tt1, run_time=0.18))

        n1a = nar("That's why... a global chip race has already begun.")
        n1b = nar("The stakes could not be higher.", color=RED)
        self.play(Write(n1a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n1a, run_time=0.25), FadeIn(n1b, run_time=0.25))

        # Slow zoom
        self.play(
            world.animate.scale(1.08).shift(LEFT*0.20),
            map_bg.animate.scale(1.08).shift(LEFT*0.20),
            run_time=5.00, rate_func=smooth,
        )

        self.play(FadeOut(tp1, run_time=0.55),
                   FadeOut(tt1, run_time=0.55),
                   FadeOut(n1b, run_time=0.55),
                   FadeOut(world,  run_time=0.55),
                   FadeOut(map_bg, run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  12s → 28s  │  USA vs China split screen
        #
        # Two coloured panels slide in from opposite sides.
        # Country labels pop up. Vertical divider appears.
        # "USA vs China" title panel at top.
        #
        # 0.00–0.70  USA panel slides in from left    0.70s
        # 0.70–1.40  China panel slides in from right 0.70s
        # 1.40–1.60  divider appears                  0.20s
        # 1.60–1.88  country labels grow in           0.28s
        # 1.88–2.16  top title panel slams            0.28s
        # 2.16–2.94  narration writes                 0.78s
        # 2.94–4.14  hold                             1.20s
        # 4.14–4.64  narration cross-fades            0.50s
        # 4.64–14.0  hold                             9.36s
        # 14.0–16.0  clean exit (panels STAY for B3)  2.00s
        # ══════════════════════════════════════════════════════════════
        usa_panel = make_usa_panel()
        chn_panel = make_china_panel()

        usa_panel.shift(LEFT * 8)
        chn_panel.shift(RIGHT * 8)
        self.add(usa_panel, chn_panel)

        self.play(usa_panel.animate.shift(RIGHT*8),
                   run_time=0.70, rate_func=smooth)
        self.play(chn_panel.animate.shift(LEFT*8),
                   run_time=0.70, rate_func=smooth)

        divider = make_divider()
        self.play(Create(divider, run_time=0.20))

        usa_lbl = side_label("USA", BLUE, [-3.60, 1.90, 0])
        chn_lbl = side_label("China", RED,  [ 3.60, 1.90, 0])
        self.play(GrowFromCenter(usa_lbl, run_time=0.28),
                   GrowFromCenter(chn_lbl, run_time=0.28))

        PW2 = 4.4
        tp2 = ink_panel(PW2, 0.72).move_to([0, TOP_Y, 0])
        tt2 = fit_text("USA  vs  China", max_width=PW2-0.40, size=32)\
                .move_to(tp2[1].get_center())
        slam(self, tp2, from_dir=UP, rt=0.28)
        self.add(tt2)
        self.play(FadeIn(tt2, run_time=0.18))

        n2a = nar("The United States and China...")
        n2b = nar("Both racing for chip supremacy.", color=RED)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))
        self.wait(9.36)

        # Clean exit — panels + divider + labels STAY for Beat 3
        self.play(FadeOut(tp2, run_time=0.55),
                   FadeOut(tt2, run_time=0.55),
                   FadeOut(n2b, run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  28s → 44s  │  Tech side (USA — left panel)
        #
        # Left panel already visible. Chip + server + AI node
        # appear on USA side only. Electricity traces flash.
        # "Technology" panel on USA side. Gentle zoom-in left.
        #
        # 0.00–0.55  "Technology" label on USA side   0.55s
        # 0.55–1.00  chip grows in (left side)        0.45s
        # 1.00–1.40  server appears below chip        0.40s
        # 1.40–1.80  AI node appears beside chip      0.40s
        # 1.80–2.50  electricity traces flash x2      0.70s
        # 2.50–2.78  narration writes                 0.78s
        # 2.78–3.98  hold                             1.20s
        # 3.98–4.48  narration cross-fades            0.50s
        # 4.48–5.18  zoom-in on left                  0.70s
        # 5.18–14.0  hold                             8.82s
        # 14.0–16.0  clean exit (panels stay for B4)  2.00s
        # ══════════════════════════════════════════════════════════════
        PW3u = 3.0
        tp3u = ink_panel(PW3u, 0.62, fill=USA_FILL, stroke=BLUE, sw=2.5)\
                 .move_to([-3.60, TOP_Y, 0])
        tt3u = fit_text("Technology", max_width=PW3u-0.30, size=24, color=BLUE)\
                 .move_to(tp3u[1].get_center())
        self.play(GrowFromCenter(tp3u, run_time=0.28),
                   Write(tt3u, run_time=0.40))

        # Props on left (USA) side — x: -5.5 to -0.5
        chip_u  = make_chip(sc=0.82).move_to([-3.20, 0.55, 0])
        server_u = make_server().scale(0.72).move_to([-4.80, -0.40, 0])
        ai_u    = make_ai_node().scale(0.85).move_to([-1.60, 0.30, 0])

        self.play(GrowFromCenter(chip_u,   run_time=0.45))
        self.play(GrowFromCenter(server_u, run_time=0.40))
        self.play(GrowFromCenter(ai_u,     run_time=0.40))

        # Electricity traces on USA side
        chip_c = chip_u.get_center()
        trace_data = [
            (chip_c+LEFT*0.76+UP*0.20,   chip_c+LEFT*1.60+UP*0.55),
            (chip_c+RIGHT*0.76+UP*0.20,  ai_u.get_center()+LEFT*0.30),
            (chip_c+DOWN*0.76,            server_u.get_center()+UP*0.35),
        ]
        traces_u = VGroup(*[
            Line(a, b, color=ELECTRIC, stroke_width=1.6, stroke_opacity=0.50)
            for a,b in trace_data
        ])
        self.play(Create(traces_u, run_time=0.40))

        bolts = [make_lightning(a, b, seed=i*7) for i,(a,b) in enumerate(trace_data)]
        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 4.5),
                    time_width=0.50, run_time=0.55) for bolt in bolts])
        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 3.0),
                    time_width=0.40, run_time=0.35) for bolt in bolts])

        n3a = nar("On one side... technology dominates.")
        n3b = nar("Chips. Servers. Artificial Intelligence.", color=BLUE)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))

        # Zoom into left side — shift right slightly
        usa_objects = VGroup(usa_panel, usa_lbl, chip_u, server_u,
                              ai_u, traces_u, tp3u, tt3u)
        self.play(usa_objects.animate.scale(1.08).shift(RIGHT*0.18),
                   run_time=0.70, rate_func=smooth)
        self.wait(8.82)

        self.play(FadeOut(tp3u,    run_time=0.55),
                   FadeOut(tt3u,    run_time=0.55),
                   FadeOut(traces_u,run_time=0.55),
                   FadeOut(n3b,     run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  44s → 60s  │  Manufacturing side (China — right)
        #
        # Right panel still visible. 3 factories + 2 gears flood in
        # on China side. "Manufacturing" panel. Zoom-in on right side.
        #
        # 0.00–0.55  "Manufacturing" label on China   0.55s
        # 0.55–1.55  factories flood in (lagged)      1.00s
        # 1.55–2.05  gears appear                     0.50s
        # 2.05–2.83  narration writes                 0.78s
        # 2.83–4.03  hold                             1.20s
        # 4.03–4.53  narration cross-fades            0.50s
        # 4.53–5.23  zoom-in on right                 0.70s
        # 5.23–14.0  hold                             8.77s
        # 14.0–16.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        PW4c = 3.4
        tp4c = ink_panel(PW4c, 0.62, fill=CHN_FILL, stroke=RED, sw=2.5)\
                 .move_to([3.60, TOP_Y, 0])
        tt4c = fit_text("Manufacturing", max_width=PW4c-0.30, size=24, color=RED)\
                 .move_to(tp4c[1].get_center())
        self.play(GrowFromCenter(tp4c, run_time=0.28),
                   Write(tt4c, run_time=0.40))

        # Factories on right (China) side — x: +0.5 to +6.5
        fac_positions = [
            np.array([1.40, 0.50, 0]),
            np.array([3.50, 0.50, 0]),
            np.array([5.50, 0.50, 0]),
        ]
        factories_c = VGroup(*[
            make_small_factory(pos=p, color=RED) for p in fac_positions
        ])
        self.play(LaggedStart(*[GrowFromCenter(f) for f in factories_c],
                               lag_ratio=0.25, run_time=1.00))

        # Gears between factories
        gear1 = make_gear(r=0.38, teeth=10, pos=np.array([2.45, -0.68, 0]))
        gear2 = make_gear(r=0.30, teeth=8,  pos=np.array([4.50, -0.68, 0]))
        self.play(GrowFromCenter(gear1, run_time=0.28),
                   GrowFromCenter(gear2, run_time=0.28))
        # Spin gears
        self.play(Rotate(gear1, PI/3, run_time=0.35),
                   Rotate(gear2, -PI/3, run_time=0.35))

        n4a = nar("On the other side... manufacturing power.")
        n4b = nar("Factories. Scale. Industrial might.", color=RED)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))

        # Zoom into right side
        chn_objects = VGroup(chn_panel, chn_lbl, factories_c,
                              gear1, gear2, tp4c, tt4c)
        self.play(chn_objects.animate.scale(1.08).shift(LEFT*0.18),
                   run_time=0.70, rate_func=smooth)
        self.wait(8.77)

        self.play(FadeOut(tp4c,       run_time=0.55),
                   FadeOut(tt4c,       run_time=0.55),
                   FadeOut(n4b,        run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  60s → 75s  │  Taiwan — the balance
        #
        # Split panels slide apart. Taiwan dot appears centre-screen.
        # Two arc arrows: left arc (USA <-- Taiwan) and right arc
        # (Taiwan --> China). "CRUCIAL" gold stamp slams.
        # Dot pulses (subtle glitch). Final narration. Zoom-out. Fade.
        #
        # 0.00–0.60  panels slide to edges            0.60s
        # 0.60–1.10  Taiwan dot + glow rings          0.85s
        # 1.10–1.70  left arc draws (to USA icons)    0.60s
        # 1.70–2.30  right arc draws (to China facs)  0.60s
        # 2.30–2.58  CRUCIAL stamp slams              0.28s
        # 2.58–2.70  stamp wobble                     0.12s
        # 2.70–3.48  narration writes                 0.78s
        # 3.48–4.68  hold                             1.20s
        # 4.68–5.18  narration cross-fades            0.50s
        # 5.18–5.68  dot pulse (subtle)               0.50s
        # 5.68–7.18  hold                             1.50s
        # 7.18–7.88  zoom-out                         0.70s
        # 7.88–9.38  fade to black overlay            1.50s
        # ══════════════════════════════════════════════════════════════

        # Slide panels to edges, revealing centre
        self.play(
            usa_panel.animate.shift(LEFT*1.80),
            chn_panel.animate.shift(RIGHT*1.80),
            usa_lbl.animate.shift(LEFT*1.80),
            chn_lbl.animate.shift(RIGHT*1.80),
            chip_u.animate.shift(LEFT*1.80),
            server_u.animate.shift(LEFT*1.80),
            ai_u.animate.shift(LEFT*1.80),
            factories_c.animate.shift(RIGHT*1.80),
            gear1.animate.shift(RIGHT*1.80),
            gear2.animate.shift(RIGHT*1.80),
            divider.animate.set_opacity(0),
            run_time=0.60, rate_func=smooth,
        )

        # Taiwan marker at centre
        TW_CENTRE = np.array([0.0, 0.30, 0])
        dot_tw = Dot(TW_CENTRE, radius=0.18, color=GOLD, fill_opacity=1)
        rings  = VGroup(*[
            Circle(radius=r, color=GOLD,
                    stroke_opacity=0.62-i*0.18, stroke_width=2.5)\
              .move_to(TW_CENTRE)
            for i,r in enumerate([0.18, 0.35, 0.56])
        ])
        self.play(
            FadeIn(dot_tw, scale=0.2, run_time=0.50),
            LaggedStart(*[GrowFromCenter(r) for r in rings],
                         lag_ratio=0.22, run_time=0.85),
        )

        # Taiwan label
        tw_pan = ink_panel(2.55, 0.65, fill="#FFFBE6", stroke=GOLD, sw=3.5)\
                   .move_to([0.0, 1.30, 0])
        tw_lbl = fit_text("TAIWAN", max_width=2.25, size=28, color=GOLD)\
                   .move_to(tw_pan[1].get_center())
        self.play(GrowFromCenter(tw_pan, run_time=0.28),
                   Write(tw_lbl,          run_time=0.35))

        # Arc to USA side (curves left-upward)
        arc_usa = ArcBetweenPoints(
            TW_CENTRE + LEFT*0.22,
            np.array([-4.80, 0.40, 0]),
            angle=0.65,
            color=BLUE, stroke_width=2.8
        ).add_tip(tip_length=0.22)
        # Arc to China side (curves right-upward)
        arc_chn = ArcBetweenPoints(
            TW_CENTRE + RIGHT*0.22,
            np.array([ 4.80, 0.40, 0]),
            angle=-0.65,
            color=RED, stroke_width=2.8
        ).add_tip(tip_length=0.22)

        self.play(Create(arc_usa, run_time=0.60))
        self.play(Create(arc_chn, run_time=0.60))

        # CRUCIAL gold stamp
        PW5 = 4.0
        st5 = stamp("CRUCIAL", color=GOLD, w=PW5, h=0.82)\
                .move_to([0, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, PI/28, run_time=0.12, rate_func=there_and_back))

        n5a = nar("And in the middle... Taiwan.")
        n5b = nar("The tiny island that holds the balance of power.", color=GOLD)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))

        # Subtle dot pulse (glitch-feel)
        for _ in range(3):
            self.play(dot_tw.animate.scale(1.22).set_color(RED),
                       run_time=0.09, rate_func=linear)
            self.play(dot_tw.animate.scale(1/1.22).set_color(GOLD),
                       run_time=0.08, rate_func=linear)

        self.wait(1.50)

        # Zoom out
        stage_all = VGroup(usa_panel, chn_panel, usa_lbl, chn_lbl,
                            chip_u, server_u, ai_u, factories_c,
                            gear1, gear2, dot_tw, rings, tw_pan, tw_lbl,
                            arc_usa, arc_chn, st5)
        self.play(stage_all.animate.scale(0.76).shift(DOWN*0.12),
                   run_time=0.70, rate_func=smooth)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)