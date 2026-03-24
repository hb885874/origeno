"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 3: Why Taiwan?  |  70 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 10s │ 10s │ The question      — char walks in, world map
Beat 2 │ 10s → 24s │ 14s │ TSMC reveal       — Taiwan glows, LEADER stamp
Beat 3 │ 24s → 40s │ 16s │ Market dominance  — 90% pie chart + counter
Beat 4 │ 40s → 58s │ 18s │ Global dependence — company arcs fly to Taiwan
Beat 5 │ 58s → 70s │ 12s │ Power realization — char shocked, Taiwan zooms
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 70s | Style: Oversimplified | English only

CHARACTER BEATS
  Beat 1: walks in from left, happy face, points at world map
  Beat 3: still visible left, shocked when 90% appears
  Beat 5: walks to centre-left, worried face + shake, sweat drops

LAYOUT ZONES
  TOP_Y   =  3.0    stamps / title panels
  FLOOR_Y = -1.65   character floor
  NAR_Y   = -3.10   narration strip
  CHAR_X  = -4.80   character rests here while map is on right

Taiwan dot world-coords: x ≈ +5.20, y ≈ +0.30

Render:
  Preview : manim -pql scene3.py Scene3
  1080p   : manim -pqh scene3.py Scene3
  4K      : manim -pqk scene3.py Scene3
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────
# PALETTE  (identical to Scene 1 / 2)
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
SKIN      = "#FDDBB4"
COAT_FILL = "#DDE8FF"
ELECTRIC  = "#00C8FF"
FONT      = "Georgia"

TOP_Y   =  3.0
FLOOR_Y = -1.65
NAR_Y   = -3.10
CHAR_X  = -4.80   # character rests here; map occupies right half
TW      = np.array([5.20, 0.30, 0])   # Taiwan world-map position


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


# ═════════════════════════════════════════════════════════════
# CHARACTER  (full port from Scene 1 — fixed arm/face system)
# ═════════════════════════════════════════════════════════════
class Character:
    HEAD_R = 0.30
    COAT_W = 0.62
    COAT_H = 0.88

    def __init__(self, color=BLUE, pos=ORIGIN, sc=1.0):
        self.c  = color
        self.sc = sc
        self._pos = np.array(pos, dtype=float)
        self._build()

    def _build(self):
        c  = self.c
        sc = self.sc

        head_cy  =  0.0
        coat_cy  =  head_cy - (self.HEAD_R + 0.06 + self.COAT_H / 2) * sc
        coat_top =  coat_cy + (self.COAT_H / 2) * sc
        coat_bot =  coat_cy - (self.COAT_H / 2) * sc
        coat_lx  = -(self.COAT_W / 2) * sc
        coat_rx  =  (self.COAT_W / 2) * sc
        sh_y     =  coat_top - 0.18 * sc

        self.head = Circle(radius=self.HEAD_R*sc, color=c,
                            fill_color=SKIN, fill_opacity=1, stroke_width=3)\
                      .move_to([0, head_cy, 0])

        self.face_happy = VGroup(
            Dot([-0.10*sc,  0.07*sc, 0], radius=0.048*sc, color=c),
            Dot([ 0.10*sc,  0.07*sc, 0], radius=0.048*sc, color=c),
            Arc(radius=0.13*sc, start_angle=-PI*0.82, angle=PI*0.64,
                 color=c, stroke_width=2.8).move_to([0, -0.07*sc, 0]),
        )
        self.face_shocked = VGroup(
            Circle(radius=0.068*sc, color=c, fill_color=WHITE,
                    fill_opacity=1, stroke_width=2.5).move_to([-0.11*sc, 0.07*sc, 0]),
            Circle(radius=0.068*sc, color=c, fill_color=WHITE,
                    fill_opacity=1, stroke_width=2.5).move_to([ 0.11*sc, 0.07*sc, 0]),
            Dot([-0.11*sc, 0.07*sc, 0], radius=0.034*sc, color=c),
            Dot([ 0.11*sc, 0.07*sc, 0], radius=0.034*sc, color=c),
            Circle(radius=0.065*sc, color=c, fill_color=INK,
                    fill_opacity=1, stroke_width=2.0).move_to([0, -0.10*sc, 0]),
            Line([-0.17*sc, 0.18*sc, 0], [-0.05*sc, 0.23*sc, 0],
                  color=c, stroke_width=2.4),
            Line([ 0.05*sc, 0.23*sc, 0], [ 0.17*sc, 0.18*sc, 0],
                  color=c, stroke_width=2.4),
        )
        self.face_worried = VGroup(
            Dot([-0.10*sc, 0.07*sc, 0], radius=0.048*sc, color=c),
            Dot([ 0.10*sc, 0.07*sc, 0], radius=0.048*sc, color=c),
            Arc(radius=0.12*sc, start_angle=PI*0.20, angle=PI*0.60,
                 color=c, stroke_width=2.8).move_to([0, -0.04*sc, 0]),
            Line([-0.16*sc, 0.18*sc, 0], [-0.05*sc, 0.24*sc, 0],
                  color=c, stroke_width=2.4),
            Line([ 0.05*sc, 0.24*sc, 0], [ 0.16*sc, 0.18*sc, 0],
                  color=c, stroke_width=2.4),
        )

        self.coat = RoundedRectangle(
            corner_radius=0.09*sc, width=self.COAT_W*sc, height=self.COAT_H*sc,
            color=c, fill_color=COAT_FILL, fill_opacity=1, stroke_width=3
        ).move_to([0, coat_cy, 0])

        self.coat_detail = VGroup(
            Line([coat_lx+0.14*sc, coat_top, 0],
                  [-0.06*sc, coat_cy+0.12*sc, 0], color=c, stroke_width=2),
            Line([coat_rx-0.14*sc, coat_top, 0],
                  [ 0.06*sc, coat_cy+0.12*sc, 0], color=c, stroke_width=2),
            Rectangle(width=0.17*sc, height=0.13*sc, color=c,
                        fill_color=CREAM, fill_opacity=1, stroke_width=1.8)
            .move_to([coat_lx+0.17*sc, coat_cy-0.20*sc, 0]),
        )

        self.arm_l = Line([coat_lx, sh_y, 0],
                           [coat_lx-0.14*sc, sh_y-0.52*sc, 0],
                           color=c, stroke_width=3.5)
        self.arm_r_rest = Line([coat_rx, sh_y, 0],
                                [coat_rx+0.14*sc, sh_y-0.52*sc, 0],
                                color=c, stroke_width=3.5)

        self.leg_l  = Line([coat_lx+0.12*sc, coat_bot, 0],
                            [coat_lx,          coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)
        self.leg_r  = Line([coat_rx-0.12*sc, coat_bot, 0],
                            [coat_rx,          coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)
        self.foot_l = Line([coat_lx,         coat_bot-0.56*sc, 0],
                            [coat_lx-0.20*sc, coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)
        self.foot_r = Line([coat_rx,         coat_bot-0.56*sc, 0],
                            [coat_rx+0.20*sc, coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)

        self._active_arm      = self.arm_r_rest
        self._active_arm_name = 'rest'
        self._active_face     = self.face_happy

        self.body = VGroup(
            self.coat, self.coat_detail,
            self.arm_l, self.arm_r_rest,
            self.leg_l, self.leg_r, self.foot_l, self.foot_r,
            self.head, self.face_happy,
        )
        self.body.move_to(self._pos)

    # ── Face swap
    def swap_face(self, scene, which, rt=0.22):
        faces = {'happy': self.face_happy,
                 'shocked': self.face_shocked,
                 'worried': self.face_worried}
        new = faces[which]
        if new is self._active_face:
            return
        new.move_to(self.head.get_center())
        scene.play(FadeOut(self._active_face, run_time=rt),
                    FadeIn(new, run_time=rt))
        self.body.remove(self._active_face)
        self.body.add(new)
        self._active_face = new

    # ── Arm swap — always rebuilds from live coat position
    def swap_arm(self, scene, which, rt=0.22):
        if which == self._active_arm_name:
            return
        c  = self.c
        sc = self.sc
        coat_rx  = (self.COAT_W / 2) * sc
        coat_top = self.coat.get_top()[1]
        sh_x     = self.coat.get_center()[0] + coat_rx
        sh_y     = coat_top - 0.18 * sc
        arm_defs = {
            'rest':   ([sh_x,          sh_y, 0], [sh_x+0.14*sc, sh_y-0.52*sc, 0]),
            'point':  ([sh_x,          sh_y, 0], [sh_x+0.60*sc, sh_y+0.16*sc, 0]),
            'raised': ([sh_x,          sh_y, 0], [sh_x+0.08*sc, sh_y+0.65*sc, 0]),
        }
        start, end = arm_defs[which]
        new = Line(start, end, color=c, stroke_width=3.5)
        old = self._active_arm
        scene.play(FadeOut(old, run_time=rt), FadeIn(new, run_time=rt))
        self.body.remove(old)
        self.body.add(new)
        self._active_arm      = new
        self._active_arm_name = which

    # ── Shock rays
    def make_shock_lines(self, n=10):
        ctr = self.head.get_center()
        r0  = self.head.radius
        return VGroup(*[
            Line(ctr+(r0+0.05)*np.array([np.cos(a), np.sin(a), 0]),
                  ctr+(r0+0.42)*np.array([np.cos(a), np.sin(a), 0]),
                  color=GOLD, stroke_width=3, stroke_opacity=0.92)
            for a in np.linspace(0, 2*PI, n, endpoint=False)
        ])

    # ── Shake
    def shake(self, scene, times=3):
        for _ in range(times):
            scene.play(self.body.animate.shift(RIGHT*0.08), run_time=0.06, rate_func=linear)
            scene.play(self.body.animate.shift(LEFT *0.16), run_time=0.06, rate_func=linear)
            scene.play(self.body.animate.shift(RIGHT*0.08), run_time=0.06, rate_func=linear)


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


def make_taiwan_marker():
    """Pulsing red dot + glow rings at Taiwan map position."""
    dot   = Dot(TW, radius=0.14, color=RED, fill_opacity=1)
    rings = VGroup(*[
        Circle(radius=r, color=RED,
                stroke_opacity=0.62 - i*0.18, stroke_width=2.5).move_to(TW)
        for i, r in enumerate([0.14, 0.28, 0.46])
    ])
    return dot, rings


def make_pie_slice(r, start_angle, sweep, color, fill_opacity=0.85, n=60):
    """
    Build a filled pie slice as a VMobject polygon.
    Avoids the Sector/AnnularSector keyword collision in Manim 0.20.
    Points: ORIGIN → arc points → back to ORIGIN.
    """
    angles = np.linspace(start_angle, start_angle + sweep, n)
    pts    = [np.array([0, 0, 0])]
    for a in angles:
        pts.append(np.array([r * np.cos(a), r * np.sin(a), 0]))
    pts.append(np.array([0, 0, 0]))
    mob = VMobject(color=color, fill_color=color,
                   fill_opacity=fill_opacity, stroke_width=2.5)
    mob.set_points_as_corners(pts)
    return mob


def make_pie_chart(pct=90):
    """
    Simple 2-slice pie: pct% in RED, rest in SUBTLE.
    Built from polygon slices — no Sector class used.
    Returns VGroup centred at ORIGIN.
    """
    r       = 1.55
    angle_a = TAU * pct / 100      # RED slice sweep
    start   = PI / 2               # 12 o'clock

    slice_r = make_pie_slice(r, start,           angle_a,           RED,   fill_opacity=0.90)
    slice_g = make_pie_slice(r, start + angle_a, TAU - angle_a,     SUBTLE, fill_opacity=0.55)
    border  = Circle(radius=r, color=INK, stroke_width=3, fill_opacity=0)
    return VGroup(slice_g, slice_r, border)


# ─────────────────────────────────────────────────────────────
# COMPANY LABEL BUILDER
# ─────────────────────────────────────────────────────────────
COMPANIES = ["Apple", "NVIDIA", "AMD", "Qualcomm", "Intel", "Google"]

# World positions for each company (approximate, on the left/top half of map)
COMPANY_POSITIONS = [
    np.array([-4.50,  1.80, 0]),   # Apple     — North America
    np.array([-3.80, -0.40, 0]),   # NVIDIA    — North America south
    np.array([-3.00,  0.90, 0]),   # AMD       — North America
    np.array([ 1.20,  2.20, 0]),   # Qualcomm  — Europe/Middle East
    np.array([-2.20,  2.40, 0]),   # Intel     — North Atlantic
    np.array([-4.20,  2.80, 0]),   # Google    — North America north
]


def make_company_labels():
    """Ink-panel labels for each company."""
    labels = VGroup()
    for name, pos in zip(COMPANIES, COMPANY_POSITIONS):
        pw  = 2.10
        pan = ink_panel(pw, 0.55, fill=CREAM, stroke=BLUE, sw=2.0)\
                .move_to(pos)
        txt = fit_text(name, max_width=pw-0.28, size=22, color=BLUE)\
                .move_to(pan[1].get_center())
        labels.add(VGroup(pan, txt))
    return labels


def make_company_arcs():
    """Curved arrows from each company position toward Taiwan."""
    arcs = VGroup()
    for pos in COMPANY_POSITIONS:
        arc = ArcBetweenPoints(
            pos + RIGHT * 0.55,          # start slightly right of label
            TW  + LEFT  * 0.20,          # end just left of Taiwan dot
            angle=-0.55,
            color=RED, stroke_width=2.2, stroke_opacity=0.70
        ).add_tip(tip_length=0.20)
        arcs.add(arc)
    return arcs


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene3(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Permanent fixtures ───────────────────────────────────────
        paper = VGroup(*[
            Line(LEFT*7.8, RIGHT*7.8, color=INK,
                  stroke_width=0.25, stroke_opacity=0.05).shift(UP*y)
            for y in np.arange(-4.6, 4.8, 0.46)
        ])
        floor_line = Line(LEFT*7.6, RIGHT*7.6, color=INK,
                           stroke_width=2.5, stroke_opacity=0.22)\
                       .move_to([0, FLOOR_Y, 0])
        nar_line   = Line(LEFT*6.8, RIGHT*6.8, color=INK,
                           stroke_width=1.0, stroke_opacity=0.14)\
                       .move_to([0, -2.15, 0])
        self.add(paper, floor_line, nar_line)

        # ── Character — starts off-screen left ───────────────────────
        CHAR_HEAD_Y = FLOOR_Y + 1.79
        char = Character(color=BLUE, pos=[-8.0, CHAR_HEAD_Y, 0], sc=1.0)
        self.add(char.body)

        # ══════════════════════════════════════════════════════════════
        # BEAT 1  │  0s → 10s  │  The question — char walks in, world map
        #
        # Char walks to CHAR_X. World map fades in on right half.
        # Char points at the map. "Why Taiwan?" panel slams.
        #
        # 0.00–1.20  char walks in                   1.20s
        # 1.20–1.60  map bg tint fades in            0.40s
        # 1.60–2.90  world dots appear (lagged)      1.30s
        # 2.90–3.08  arm → point                     0.18s
        # 3.08–3.36  panel slams                     0.28s
        # 3.36–3.48  panel wobble                    0.12s
        # 3.48–4.26  narration writes                0.78s
        # 4.26–7.26  hold                            3.00s
        # 7.26–7.76  narration fades                 0.50s
        # 7.76–10.0  hold / Ken Burns zoom starts    2.24s  (map stays)
        # ══════════════════════════════════════════════════════════════
        self.play(
            char.body.animate.move_to([CHAR_X, CHAR_HEAD_Y, 0]),
            run_time=1.20, rate_func=linear,
        )

        map_bg = Rectangle(width=15.5, height=9.5, fill_color=MAP_GREEN,
                             fill_opacity=0.28, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(map_bg, run_time=0.40))

        world = make_world_dots()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in world],
                               lag_ratio=0.003, run_time=1.30))

        char.swap_arm(self, 'point', rt=0.18)

        PW1  = 4.4
        st1  = stamp("Why Taiwan?", color=RED, w=PW1, h=0.82)\
                 .move_to([0.60, TOP_Y, 0])
        slam(self, st1, from_dir=UP, rt=0.28)
        self.play(Rotate(st1, PI/28, run_time=0.12, rate_func=there_and_back))

        n1 = nar("The question is... why Taiwan?", size=34)
        self.play(Write(n1, run_time=0.78))
        self.wait(3.00)
        self.play(FadeOut(n1, run_time=0.50))
        self.wait(0.10)

        # Ken Burns — gentle zoom toward Asia (shift world left, scale up slightly)
        self.play(
            world.animate.scale(1.12).shift(LEFT * 0.40),
            map_bg.animate.scale(1.12).shift(LEFT * 0.40),
            run_time=2.14, rate_func=smooth,
        )

        # ── B1 → B2 : clean up panel + arm, keep map + world
        self.play(
            FadeOut(st1, run_time=0.35),
            FadeOut(char._active_arm, run_time=0.35),
        )
        # Silently restore rest arm via live coat coords
        sc = char.sc
        coat_top_v = char.coat.get_top()[1]
        sh_x_v     = char.coat.get_center()[0] + (char.COAT_W/2)*sc
        sh_y_v     = coat_top_v - 0.18*sc
        rest_arm   = Line([sh_x_v, sh_y_v, 0],
                           [sh_x_v+0.14*sc, sh_y_v-0.52*sc, 0],
                           color=char.c, stroke_width=3.5)
        char.body.remove(char._active_arm)
        char.body.add(rest_arm)
        char._active_arm      = rest_arm
        char._active_arm_name = 'rest'
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  10s → 24s  │  TSMC reveal — Taiwan glows
        #
        # Taiwan dot + rings appear. TSMC label panel next to dot.
        # "LEADER" gold stamp slams. Char watches, happy face.
        #
        # 0.00–0.50  Taiwan dot + rings appear        0.85s (lagged)
        # 0.85–1.50  TSMC panel + connector           0.65s
        # 1.50–1.78  "LEADER" stamp slams             0.28s
        # 1.78–1.90  stamp wobble                     0.12s
        # 1.90–2.68  narration line 1                 0.78s
        # 2.68–3.88  hold                             1.20s
        # 3.88–4.38  narration cross-fades            0.50s
        # 4.38–12.0  hold                             7.62s
        # 12.0–14.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        dot_tw, rings = make_taiwan_marker()
        self.play(
            FadeIn(dot_tw, scale=0.2, run_time=0.50),
            LaggedStart(*[GrowFromCenter(r) for r in rings],
                         lag_ratio=0.22, run_time=0.85),
        )

        # TSMC label — LEFT of dot (dot at x≈5.2, panel at x≈3.1)
        PW_TW  = 2.55
        tw_pan = ink_panel(PW_TW, 0.72, fill="#FFFBE6", stroke=GOLD, sw=3.5)\
                   .move_to([3.10, 1.30, 0])
        tw_lbl = fit_text("TSMC", max_width=PW_TW-0.30, size=30, color=GOLD)\
                   .move_to(tw_pan[1].get_center() + UP*0.10)
        tw_sub = fit_text("Taiwan", max_width=PW_TW-0.30, size=18,
                           color=GOLD, weight=NORMAL)\
                   .move_to(tw_pan[1].get_center() + DOWN*0.16)
        tw_con = Line(tw_pan[1].get_right()+RIGHT*0.06, TW+LEFT*0.18,
                       color=GOLD, stroke_width=1.6, stroke_opacity=0.65)
        self.play(
            GrowFromCenter(tw_pan, run_time=0.35),
            Write(tw_lbl,          run_time=0.40),
            FadeIn(tw_sub,         run_time=0.30),
            Create(tw_con,         run_time=0.35),
        )

        # "LEADER" gold stamp — top right
        PW_L  = 3.4
        st_l  = stamp("LEADER", color=GOLD, w=PW_L, h=0.82)\
                  .move_to([4.20, TOP_Y, 0])
        slam(self, st_l, from_dir=UP, rt=0.28)
        self.play(Rotate(st_l, -PI/26, run_time=0.12, rate_func=there_and_back))

        # Ring second pulse
        self.play(rings.animate.scale(2.0).set_stroke(opacity=0),
                   run_time=0.70, rate_func=smooth)

        n2a = nar("The world's most advanced chip company...")
        n2b = nar("TSMC. Right here.", color=GOLD)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))
        self.wait(7.62)

        # Clean exit — keep dot_tw and map; remove labels/stamp/narration
        self.play(
            FadeOut(tw_pan, run_time=0.50),
            FadeOut(tw_lbl, run_time=0.50),
            FadeOut(tw_sub, run_time=0.50),
            FadeOut(tw_con, run_time=0.50),
            FadeOut(st_l,   run_time=0.50),
            FadeOut(rings,  run_time=0.50),
            FadeOut(n2b,    run_time=0.50),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  24s → 40s  │  Market dominance — 90% pie + counter
        #
        # Map + dot fade to BG. Pie chart appears centre-right.
        # Counter spins 0 → 90. Char goes shocked.
        #
        # 0.00–0.60  map + world dim to bg            0.60s
        # 0.60–1.30  pie chart grows                  0.70s
        # 1.30–1.58  "90% Advanced Chips" stamp       0.28s
        # 1.58–1.70  stamp wobble                     0.12s
        # 1.70–4.20  counter 0 → 90 spins             2.50s
        # 4.20–4.50  char shocked face + shock lines  0.30s
        # 4.50–5.28  narration writes                 0.78s
        # 5.28–6.48  hold                             1.20s
        # 6.48–6.98  narration cross-fades            0.50s
        # 6.98–14.0  hold                             7.02s
        # 14.0–16.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        self.play(
            world.animate.set_opacity(0.12),
            map_bg.animate.set_fill(opacity=0.10),
            dot_tw.animate.set_color(GOLD).scale(1.4),
            run_time=0.60,
        )

        pie = make_pie_chart(pct=90).scale(0.90).move_to([1.40, 0.30, 0])
        self.play(GrowFromCenter(pie, run_time=0.70))

        # Pie legend
        leg_r = VGroup(
            Square(side_length=0.22, color=RED, fill_color=RED,
                    fill_opacity=1, stroke_width=0),
            fit_text("TSMC  90%", max_width=2.2, size=20, color=INK,
                      weight=NORMAL),
        ).arrange(RIGHT, buff=0.14).next_to(pie, DOWN, buff=0.28)
        leg_r[1].set_color(RED)
        leg_g = VGroup(
            Square(side_length=0.22, color=SUBTLE, fill_color=SUBTLE,
                    fill_opacity=1, stroke_width=0),
            fit_text("Rest of world  10%", max_width=2.4, size=20,
                      color=INK, weight=NORMAL),
        ).arrange(RIGHT, buff=0.14).next_to(leg_r, DOWN, buff=0.12)
        leg_g[1].set_color(SUBTLE)
        legend = VGroup(leg_r, leg_g)
        self.play(FadeIn(legend, run_time=0.35))

        # Stamp
        PW3  = 5.0
        st3  = stamp("90% Advanced Chips", color=RED, w=PW3, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st3, from_dir=UP, rt=0.28)
        self.play(Rotate(st3, PI/30, run_time=0.12, rate_func=there_and_back))

        # Spinning counter
        cval    = ValueTracker(0)
        c_bg    = ink_panel(3.0, 0.86, fill=CREAM, stroke=RED, sw=2.5)\
                    .move_to([-3.20, 0.30, 0])
        self.play(GrowFromCenter(c_bg, run_time=0.25))

        def c_label():
            v = int(cval.get_value())
            return VGroup(
                T(f"{v}%", size=42, color=RED).move_to([-3.20, 0.30, 0]),
            )
        c_lbl = always_redraw(c_label)
        self.add(c_lbl)
        self.play(cval.animate.set_value(90),
                   run_time=2.50, rate_func=rush_from)

        # Char shocked
        shock = char.make_shock_lines(n=10)
        self.play(
            LaggedStart(*[GrowFromCenter(sl) for sl in shock],
                         lag_ratio=0.04, run_time=0.30),
        )
        char.swap_face(self, 'shocked', rt=0.22)

        n3a = nar("One company produces 90% of advanced chips.")
        n3b = nar("Ninety. Percent.", size=42, color=RED)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))
        self.wait(7.02)

        # Clean exit
        self.remove(c_lbl)
        self.play(
            FadeOut(pie,    run_time=0.55),
            FadeOut(legend, run_time=0.55),
            FadeOut(st3,    run_time=0.55),
            FadeOut(c_bg,   run_time=0.55),
            FadeOut(shock,  run_time=0.55),
            FadeOut(n3b,    run_time=0.55),
        )
        # Restore map opacity
        self.play(
            world.animate.set_opacity(0.38),
            map_bg.animate.set_fill(opacity=0.28),
            run_time=0.50,
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  40s → 58s  │  Global dependence — company arcs
        #
        # Company label panels flood in across the map.
        # Arc arrows draw from each company → Taiwan.
        # "Global Dependence" panel top. Char watches, still shocked.
        #
        # 0.00–0.50  "Global Dependence" panel        0.50s
        # 0.50–1.50  company labels flood in (lagged) 1.00s
        # 1.50–2.20  arc arrows draw (lagged)         0.70s
        # 2.20–2.90  4 ShowPassingFlash on arcs       0.70s
        # 2.90–3.68  narration writes                 0.78s
        # 3.68–4.88  hold                             1.20s
        # 4.88–5.38  narration cross-fades            0.50s
        # 5.38–16.0  hold                             10.62s
        # 16.0–18.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        PW4  = 5.2
        tp4  = ink_panel(PW4, 0.72).move_to([0, TOP_Y, 0])
        tt4  = fit_text("Global Dependence", max_width=PW4-0.40, size=30)\
                 .move_to(tp4[1].get_center())
        self.play(GrowFromCenter(tp4, run_time=0.28),
                   Write(tt4, run_time=0.40))

        co_labels = make_company_labels()
        self.play(LaggedStart(*[GrowFromCenter(lbl) for lbl in co_labels],
                               lag_ratio=0.15, run_time=1.00))

        co_arcs = make_company_arcs()
        self.play(LaggedStart(*[Create(arc) for arc in co_arcs],
                               lag_ratio=0.12, run_time=0.70))

        # Pulse arcs with passing flash ×4
        for _ in range(4):
            self.play(*[
                ShowPassingFlash(arc.copy().set_stroke(RED, 4.0),
                                  time_width=0.45, run_time=0.55)
                for arc in co_arcs
            ])

        n4a = nar("Apple, NVIDIA, AMD... they all depend on it.")
        n4b = nar("Every major tech company. One island.", color=RED)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))
        self.wait(10.62)

        # Clean exit — fade companies, arcs, panel; keep map + Taiwan dot
        self.play(
            FadeOut(co_labels, run_time=0.60),
            FadeOut(co_arcs,   run_time=0.60),
            FadeOut(tp4,       run_time=0.60),
            FadeOut(tt4,       run_time=0.60),
            FadeOut(n4b,       run_time=0.60),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  58s → 70s  │  Power realization
        #
        # World dims. Taiwan dot glows larger. Char walks to centre-left,
        # swaps to worried face, sweat drops, shakes.
        # "One Island Controls It All" stamp slams.
        # Camera zooms out (everything scales down). Fade to black.
        #
        # 0.00–0.60  world dims, Taiwan glows brighter  0.60s
        # 0.60–1.10  char walks toward centre-left      0.50s
        # 1.10–1.32  face → worried                     0.22s
        # 1.32–1.50  sweat drops appear                 0.18s
        # 1.50–1.78  stamp slams                        0.28s
        # 1.78–1.90  stamp wobble                       0.12s
        # 1.90–2.68  narration writes                   0.78s
        # 2.68–3.88  hold                               1.20s
        # 3.88–4.38  narration cross-fades              0.50s
        # 4.38–4.56  char shake                         0.18s
        # 4.56–7.00  hold                               2.44s
        # 7.00–7.70  zoom-out (scale down)              0.70s
        # 7.70–9.20  fade to black overlay              1.50s
        # ══════════════════════════════════════════════════════════════

        # World dims — Taiwan stays bright
        self.play(
            world.animate.set_opacity(0.08),
            map_bg.animate.set_fill(opacity=0.07),
            dot_tw.animate.scale(2.0).set_color(RED),
            run_time=0.60,
        )

        # Char walks closer to centre
        self.play(
            char.body.animate.move_to([-3.60, CHAR_HEAD_Y, 0]),
            run_time=0.50, rate_func=smooth,
        )
        char.swap_face(self, 'worried', rt=0.22)

        # Sweat drops
        hc    = char.head.get_center()
        sweat = VGroup(
            Dot(radius=0.07, color=BLUE, fill_opacity=0.80)
            .move_to(hc + RIGHT*0.36 + UP*0.16),
            Dot(radius=0.04, color=BLUE, fill_opacity=0.55)
            .move_to(hc + RIGHT*0.50 + UP*0.32),
        )
        self.add(sweat)
        self.play(FadeIn(sweat, scale=0.5, run_time=0.18))

        # Final stamp
        PW5  = 6.2
        st5  = stamp("One Island Controls It All", color=RED, w=PW5, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, -PI/28, run_time=0.12, rate_func=there_and_back))

        n5a = nar("Which means... the world's most powerful technology...")
        n5b = nar("Depends on one small island.", size=38, color=RED)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))

        char.shake(self, times=3)
        self.wait(2.44)

        # Zoom out
        stage = VGroup(world, map_bg, dot_tw, st5, char.body, sweat)
        self.play(stage.animate.scale(0.75).shift(DOWN*0.15),
                   run_time=0.70, rate_func=smooth)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)