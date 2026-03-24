"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 1: The Hidden Dependency  |  45 seconds  |  Oversimplified style

FIXES
─────
1. ARM POSITION FIX
   Shoulder origin = coat_top - 0.18*sc  (upper chest, NOT above coat).
   All arm Lines start from there → arms hang from shoulders, not head.

2. TEXT OVERFLOW FIX
   Panel text uses fit_text() which calls .scale_to_fit_width(panel_w - 0.4)
   so text can NEVER exceed its box regardless of string length.

3. ENGLISH ONLY — no Hindi font anywhere.

4. NO OVERLAPS — char left half, icons right half, clear zones every beat.

Render:
  Preview : manim -pql scene1_cold_open.py Scene1
  1080p   : manim -pqh scene1_cold_open.py Scene1
  4K      : manim -pqk scene1_cold_open.py Scene1
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
SKIN      = "#FDDBB4"
COAT_FILL = "#DDE8FF"
ELECTRIC  = "#00C8FF"
FONT      = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.4
FLOOR_Y = -1.65
NAR_Y   = -3.10


# ─────────────────────────────────────────────────────────────
# TEXT HELPERS
# ─────────────────────────────────────────────────────────────
def T(text, size=34, color=INK, weight=BOLD):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)

def Ts(text, size=22, color=SUBTLE):
    return Text(text, font=FONT, font_size=size, color=color, weight=NORMAL)

def nar(text, size=32, color=INK):
    """Narration line — always at NAR_Y, never on stage."""
    return T(text, size=size, color=color, weight=NORMAL).move_to([0, NAR_Y, 0])

def fit_text(text, max_width, size=28, color=INK, weight=BOLD):
    """
    Text that auto-scales to stay within max_width.
    Use for ANY text going inside a panel.
    """
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
    outer = Rectangle(width=w,      height=h,
                       color=color, fill_color=color,
                       fill_opacity=0.10, stroke_width=4.5)
    inner = Rectangle(width=w-0.16, height=h-0.16,
                       color=color, fill_opacity=0, stroke_width=1.8)
    lbl   = fit_text(text, max_width=w-0.30, size=38, color=color)
    return VGroup(outer, inner, lbl)

def slam(scene, mob, from_dir=UP, rt=0.28):
    mob.shift(from_dir * 4.0)
    scene.add(mob)
    scene.play(mob.animate.shift(-from_dir * 4.0),
                run_time=rt, rate_func=rush_from)


# ═════════════════════════════════════════════════════════════
# CHARACTER
# ═════════════════════════════════════════════════════════════
class Character:
    """
    Bean-head Oversimplified character.

    COORDINATE SYSTEM (all at sc=1, centred at ORIGIN before move_to):
    ──────────────────────────────────────────────────────────────────
      head centre   : y =  0.0
      coat centre   : y = -(HEAD_R + gap + COAT_H/2)  = -0.79
      coat top      : y = coat_cy + COAT_H/2           = -0.35
      shoulder      : y = coat_top - 0.18              = -0.53  ← CHEST level
      coat bottom   : y = coat_cy - COAT_H/2           = -1.23

    Arms start at (±coat_rx, shoulder_y) → hang downward / extend outward.
    Legs start at (coat_lx/rx, coat_bot).
    Face features are at head-centre-relative coords → no drift on move_to.
    """

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

        # ── Key y-coordinates (at sc=1, centred at ORIGIN)
        head_cy   =  0.0
        coat_cy   =  head_cy - (self.HEAD_R + 0.06 + self.COAT_H / 2) * sc
        coat_top  =  coat_cy + (self.COAT_H / 2) * sc
        coat_bot  =  coat_cy - (self.COAT_H / 2) * sc
        coat_lx   = -(self.COAT_W / 2) * sc
        coat_rx   =  (self.COAT_W / 2) * sc
        # SHOULDER = upper-chest region, below coat top
        sh_y      =  coat_top - 0.18 * sc   # ← was +0.22 (BUG). Now -0.18.

        # ── Head
        self.head = Circle(
            radius=self.HEAD_R * sc, color=c,
            fill_color=SKIN, fill_opacity=1, stroke_width=3
        ).move_to([0, head_cy, 0])

        # ── Face features (coords relative to head centre = ORIGIN here)
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

        # ── Coat
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

        # ── Arms — all start at (±coat_rx, sh_y) which is CHEST level
        self.arm_l         = Line([coat_lx,           sh_y, 0],
                                   [coat_lx - 0.14*sc, sh_y - 0.52*sc, 0],
                                   color=c, stroke_width=3.5)
        self.arm_r_rest    = Line([coat_rx,           sh_y, 0],
                                   [coat_rx + 0.14*sc, sh_y - 0.52*sc, 0],
                                   color=c, stroke_width=3.5)
        self.arm_r_point   = Line([coat_rx,           sh_y, 0],
                                   [coat_rx + 0.60*sc, sh_y + 0.16*sc, 0],
                                   color=c, stroke_width=3.5)
        self.arm_r_raised  = Line([coat_rx,           sh_y, 0],
                                   [coat_rx + 0.08*sc, sh_y + 0.65*sc, 0],
                                   color=c, stroke_width=3.5)

        # ── Legs
        self.leg_l  = Line([coat_lx+0.12*sc, coat_bot, 0],
                            [coat_lx,          coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)
        self.leg_r  = Line([coat_rx-0.12*sc, coat_bot, 0],
                            [coat_rx,          coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)
        self.foot_l = Line([coat_lx,          coat_bot-0.56*sc, 0],
                            [coat_lx-0.20*sc,  coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)
        self.foot_r = Line([coat_rx,          coat_bot-0.56*sc, 0],
                            [coat_rx+0.20*sc,  coat_bot-0.56*sc, 0],
                            color=c, stroke_width=3.5)

        # ── Active trackers
        self._active_arm      = self.arm_r_rest
        self._active_arm_name = 'rest'
        self._active_face = self.face_happy

        # ── Assemble flat VGroup at ORIGIN, then move_to pos once
        self.body = VGroup(
            self.coat, self.coat_detail,
            self.arm_l, self.arm_r_rest,
            self.leg_l, self.leg_r, self.foot_l, self.foot_r,
            self.head,
            self.face_happy,   # drawn last → on top of head fill
        )
        self.body.move_to(self._pos)

    # ── Face swap ────────────────────────────────────────────
    def swap_face(self, scene, which, rt=0.22):
        """Move new face to current head centre, cross-fade."""
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

    # ── Arm swap ─────────────────────────────────────────────
    def swap_arm(self, scene, which, rt=0.22):
        """
        Rebuilds the requested arm Line anchored to the coat's CURRENT
        world position, so it is always attached to the shoulder.
        We do NOT reuse the pre-built arm objects (they drift); instead
        we create a fresh Line each time from live coat coordinates.
        """
        if which == self._active_arm_name:
            return
        c  = self.c
        sc = self.sc
        # Live shoulder anchor — derived from coat's actual current position
        coat_rx = (self.COAT_W / 2) * sc
        coat_top = self.coat.get_top()[1]          # current world y of coat top
        sh_x = self.coat.get_center()[0] + coat_rx # current world x of right shoulder
        sh_y = coat_top - 0.18 * sc                # chest level
        arm_defs = {
            'rest':   ([sh_x,           sh_y, 0], [sh_x + 0.14*sc, sh_y - 0.52*sc, 0]),
            'point':  ([sh_x,           sh_y, 0], [sh_x + 0.60*sc, sh_y + 0.16*sc, 0]),
            'raised': ([sh_x,           sh_y, 0], [sh_x + 0.08*sc, sh_y + 0.65*sc, 0]),
        }
        start, end = arm_defs[which]
        new = Line(start, end, color=c, stroke_width=3.5)
        old = self._active_arm
        scene.play(FadeOut(old, run_time=rt), FadeIn(new, run_time=rt))
        self.body.remove(old)
        self.body.add(new)
        self._active_arm      = new
        self._active_arm_name = which

    # ── Shock rays ───────────────────────────────────────────
    def make_shock_lines(self, n=10):
        ctr = self.head.get_center()
        r0  = self.head.radius
        return VGroup(*[
            Line(ctr + (r0+0.05)*np.array([np.cos(a), np.sin(a), 0]),
                  ctr + (r0+0.42)*np.array([np.cos(a), np.sin(a), 0]),
                  color=GOLD, stroke_width=3, stroke_opacity=0.92)
            for a in np.linspace(0, 2*PI, n, endpoint=False)
        ])

    # ── Shake ────────────────────────────────────────────────
    def shake(self, scene, times=3):
        for _ in range(times):
            scene.play(self.body.animate.shift(RIGHT*0.08),
                        run_time=0.06, rate_func=linear)
            scene.play(self.body.animate.shift(LEFT *0.16),
                        run_time=0.06, rate_func=linear)
            scene.play(self.body.animate.shift(RIGHT*0.08),
                        run_time=0.06, rate_func=linear)


# ─────────────────────────────────────────────────────────────
# PROPS
# ─────────────────────────────────────────────────────────────
def make_globe():
    ocean = Circle(radius=1.55, color=INK, fill_color="#A8C8E8",
                    fill_opacity=1, stroke_width=3.5)
    blobs = [
        Ellipse(width=0.90, height=0.60, color=INK, fill_color="#7DB87D",
                 fill_opacity=1, stroke_width=1.5).move_to([-0.42, 0.36, 0]),
        Ellipse(width=0.70, height=0.54, color=INK, fill_color="#7DB87D",
                 fill_opacity=1, stroke_width=1.5).move_to([ 0.84, 0.24, 0]),
        Ellipse(width=0.50, height=0.37, color=INK, fill_color="#7DB87D",
                 fill_opacity=1, stroke_width=1.5).move_to([-1.04, 0.12, 0]),
        Ellipse(width=0.34, height=0.23, color=INK, fill_color="#7DB87D",
                 fill_opacity=1, stroke_width=1.2).move_to([ 0.50,-0.80, 0]),
    ]
    lats = VGroup(*[
        Arc(radius=1.55*abs(np.cos(lat)), angle=2*PI,
             color=WHITE, stroke_width=0.6, stroke_opacity=0.28)
        .move_to([0, 1.55*np.sin(lat), 0])
        for lat in [0.45,-0.45,0.90,-0.90]
    ])
    longs = VGroup(*[
        Arc(radius=1.55, angle=PI, start_angle=a,
             color=WHITE, stroke_width=0.5, stroke_opacity=0.20)
        for a in np.linspace(0, PI, 5)
    ])
    nodes = VGroup(*[
        VGroup(
            Circle(radius=0.09, color=GOLD, fill_color=GOLD,
                    fill_opacity=1,    stroke_width=0),
            Circle(radius=0.18, color=GOLD, fill_color=GOLD,
                    fill_opacity=0.22, stroke_width=0),
        ).move_to(p)
        for p in [[-0.38,0.80,0],[0.90,0.50,0],[-1.10,0.32,0],
                   [0.30,-0.34,0],[-0.60,-0.50,0],[1.10,-0.14,0]]
    ])
    return VGroup(ocean, *blobs, lats, longs, nodes)


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


def make_bank():
    base  = Rectangle(width=2.04, height=0.30, color=INK,
                        fill_color="#7A6040", fill_opacity=1, stroke_width=2.5)
    step  = Rectangle(width=1.74, height=0.23, color=INK,
                        fill_color="#8A7050", fill_opacity=1,
                        stroke_width=2).next_to(base, UP, buff=0)
    cols  = VGroup(*[
        Rectangle(width=0.17, height=0.90, color=INK,
                    fill_color="#B8A070", fill_opacity=1, stroke_width=2)
        .move_to(step.get_top() + UP*0.45 + RIGHT*(-0.62+i*0.41))
        for i in range(4)
    ])
    entab = Rectangle(width=1.88, height=0.23, color=INK,
                       fill_color="#7A6040", fill_opacity=1,
                       stroke_width=2).next_to(cols, UP, buff=0)
    ped   = Triangle(color=INK, fill_color="#6A5030",
                      fill_opacity=1, stroke_width=2.5)\
              .scale(0.54).next_to(entab, UP, buff=0)
    return VGroup(base, step, cols, entab, ped)


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
        .move_to([sg*0.80*sc, -0.48*sc+i*0.24*sc, 0])
        for i in range(5) for sg in [1,-1]
    ])
    return VGroup(base, pins, die, grid, core)


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


def make_lightning(start, end, steps=8, seed=0):
    np.random.seed(seed)
    pts = [np.array(start)]
    for i in range(1, steps):
        t   = i/steps
        mid = np.array(start)*(1-t) + np.array(end)*t
        d   = np.array(end) - np.array(start)
        perp = np.array([-d[1], d[0], 0])
        n = np.linalg.norm(perp)
        if n > 1e-4: perp /= n
        pts.append(mid + perp*(np.random.rand()-0.5)*0.28)
    pts.append(np.array(end))
    bolt = VMobject(stroke_color=ELECTRIC, stroke_width=3.8, stroke_opacity=0.95)
    bolt.set_points_as_corners(pts)
    return bolt


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene1(Scene):
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

        # ── Character ────────────────────────────────────────────────
        # sc=1.0: head r=0.30, coat h=0.88, legs ~0.56 below coat
        # Total height ≈ 0.60(head) + 0.88(coat) + 0.56(leg) = 2.04
        # Place body so feet rest on FLOOR_Y:
        # feet_y = coat_bot - 0.56 = (head_cy - 0.79 - 0.44) - 0.56 = head_cy - 1.79
        # We want feet_y = FLOOR_Y, so head_cy = FLOOR_Y + 1.79
        CHAR_HEAD_Y = FLOOR_Y + 1.79
        char = Character(color=BLUE, pos=[-8.0, CHAR_HEAD_Y, 0], sc=1.0)
        self.add(char.body)

        # ══════════════════════════════════════════════════════════════
        # BEAT 1  │  0s → 8s  │  Walk in + globe + shocked face
        #
        # Char walks to x=-3.5 (left third).
        # Globe at x=+3.2 (right third). Guaranteed no overlap.
        #
        # 0.00–1.40  char walks in from left         1.40s
        # 1.40–1.70  head tilt                       0.30s
        # 1.70–2.10  globe fades in (right)          0.40s
        # 2.10–2.40  question bubble pops            0.30s
        # 2.40–2.68  top panel slams                 0.28s
        # 2.68–2.90  panel text appears              0.22s
        # 2.90–3.65  narration writes                0.75s
        # 3.65–3.93  narration cross-fades           0.28s
        # 3.93–4.28  shock lines burst               0.35s
        # 4.28–4.50  face swaps shocked              0.22s
        # 4.50–8.00  hold                            3.50s
        # ══════════════════════════════════════════════════════════════
        self.play(
            char.body.animate.move_to([-3.50, CHAR_HEAD_Y, 0]),
            run_time=1.40, rate_func=linear,
        )
        self.play(
            Rotate(char.head, PI/16, about_point=char.head.get_center()),
            run_time=0.30, rate_func=there_and_back,
        )

        globe = make_globe().scale(0.88).move_to([3.20, STAGE_Y + 0.10, 0])
        self.play(FadeIn(globe, run_time=0.40))

        # Question bubble — positioned above char head
        q_pos  = char.head.get_center() + UP*0.50 + RIGHT*0.42
        q_circ = Circle(radius=0.38, color=RED, fill_color=CREAM,
                          fill_opacity=1, stroke_width=3.0).move_to(q_pos)
        q_text = fit_text("?", max_width=0.50, size=44, color=RED).move_to(q_pos)
        q_bub  = VGroup(q_circ, q_text)
        self.play(GrowFromCenter(q_bub, run_time=0.30))
        self.play(q_bub.animate.scale(1.08), run_time=0.16, rate_func=there_and_back)

        # Top panel — text uses fit_text to stay inside box
        PW1  = 6.0
        tp1  = ink_panel(PW1, 0.72).move_to([0, TOP_Y, 0])
        tt1  = fit_text("The world's most powerful AI depends on...",
                         max_width=PW1-0.40, size=26, color=INK, weight=NORMAL)\
                 .move_to(tp1[1].get_center())
        slam(self, tp1, from_dir=UP, rt=0.28)
        self.add(tt1)
        self.play(FadeIn(tt1, run_time=0.22))

        n1a = nar("The world's most powerful AI...")
        n1b = nar("...depends on something you never see.", color=RED)
        self.play(Write(n1a, run_time=0.75))
        self.wait(1.20)   # hold so viewer can read the line
        self.play(FadeOut(n1a, run_time=0.35), FadeIn(n1b, run_time=0.35))

        shock = char.make_shock_lines(n=10)
        self.play(LaggedStart(*[GrowFromCenter(sl) for sl in shock],
                               lag_ratio=0.04, run_time=0.35))
        char.swap_face(self, 'shocked', rt=0.22)
        self.wait(1.80)   # reduced from 3.50 to compensate for 1.70s added above

        # ── B1 → B2
        self.play(
            FadeOut(globe,  run_time=0.35),
            FadeOut(q_bub,  run_time=0.35),
            FadeOut(tp1,    run_time=0.35),
            FadeOut(tt1,    run_time=0.35),
            FadeOut(shock,  run_time=0.35),
            FadeOut(n1b,    run_time=0.35),
            char.body.animate.move_to([-4.80, CHAR_HEAD_Y, 0]),
        )
        char.swap_face(self, 'happy', rt=0.18)
        self.wait(0.08)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  8s → 16s  │  Phone / Car / Bank
        #
        # Char at x=-4.8. Icons RIGHT half: x=0.0, 2.4, 4.8
        # Char right edge ≈ x=-4.5, phone left edge ≈ x=-0.5 → gap 4u ✓
        #
        # 0.00–0.55  top panel + title               0.55s
        # 0.55–0.73  arm → point                     0.18s
        # 0.73–1.01  phone pops in                   0.28s
        # 1.01–1.29  car pops in                     0.28s
        # 1.29–1.57  bank pops in                    0.28s
        # 1.57–1.79  labels fade in                  0.22s
        # 1.79–2.99  narration writes                1.20s
        # 2.99–8.00  hold                            5.01s
        # ══════════════════════════════════════════════════════════════
        PW2 = 5.0
        tp2 = ink_panel(PW2, 0.72).move_to([1.20, TOP_Y, 0])
        tt2 = fit_text("Everything runs on...", max_width=PW2-0.40, size=30)\
                .move_to(tp2[1].get_center())
        self.play(GrowFromCenter(tp2, run_time=0.32), Write(tt2, run_time=0.40))

        char.swap_arm(self, 'point', rt=0.18)

        phone = make_phone().scale(0.82).move_to([ 0.00, STAGE_Y - 0.05, 0])
        car   = make_car().scale(0.76).move_to(  [ 2.40, STAGE_Y - 0.22, 0])
        bank  = make_bank().scale(0.76).move_to( [ 4.80, STAGE_Y - 0.05, 0])

        ph_lbl = Ts("Phone").next_to(phone, DOWN, buff=0.22)
        ca_lbl = Ts("Car").next_to(car,    DOWN, buff=0.22)
        bk_lbl = Ts("Bank").next_to(bank,  DOWN, buff=0.22)

        for icon, lbl in [(phone, ph_lbl), (car, ca_lbl), (bank, bk_lbl)]:
            self.play(GrowFromCenter(icon, run_time=0.28))
            self.play(FadeIn(lbl, run_time=0.10))

        n2 = nar("Your phone... your car... even your bank...")
        self.play(Write(n2, run_time=1.20))
        self.wait(5.01)

        # ── B2 → B3
        # Arm swap + full icon fadeout happen together before chip appears
        b2_icons = VGroup(phone, car, bank, ph_lbl, ca_lbl, bk_lbl)
        self.play(
            FadeOut(tp2,     run_time=0.40),
            FadeOut(tt2,     run_time=0.40),
            FadeOut(n2,      run_time=0.40),
            FadeOut(b2_icons,run_time=0.40),                # full fadeout, not dim
            FadeOut(char._active_arm, run_time=0.40),       # arm fades with icons
        )
        # Silently rebuild rest arm at current coat position and update trackers
        sc = char.sc
        coat_top = char.coat.get_top()[1]
        sh_x = char.coat.get_center()[0] + (char.COAT_W / 2) * sc
        sh_y = coat_top - 0.18 * sc
        rest_arm = Line([sh_x, sh_y, 0],
                         [sh_x + 0.14*sc, sh_y - 0.52*sc, 0],
                         color=char.c, stroke_width=3.5)
        char.body.remove(char._active_arm)
        char.body.add(rest_arm)
        char._active_arm      = rest_arm
        char._active_arm_name = 'rest'
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  16s → 24s  │  Chip + stamp + electricity
        #
        # Char at x=-4.8. Chip at x=+1.2. Gap ≈ 4u ✓
        #
        # 0.00–0.70  chip grows                      0.70s
        # 0.70–0.98  CHIPS stamp slams               0.28s
        # 0.98–1.10  stamp wobble                    0.12s
        # 1.10–1.80  traces appear                   0.70s
        # 1.80–2.50  electricity flash ×2            0.70s
        # 2.50–2.72  glow burst                      0.22s
        # 2.72–3.47  narration part 1                0.75s
        # 3.47–3.75  narration swap                  0.28s
        # 3.75–4.35  chip scale up                   0.60s
        # 4.35–4.57  face → shocked                  0.22s
        # 4.57–8.00  hold                            3.43s
        # ══════════════════════════════════════════════════════════════
        chip = make_chip(sc=1.0).scale(1.28).move_to([1.20, STAGE_Y+0.55, 0])
        self.play(GrowFromCenter(chip, run_time=0.70))

        chips_st = stamp("CHIPS", color=RED, w=2.80, h=0.78)\
                     .move_to([4.00, TOP_Y, 0])
        slam(self, chips_st, from_dir=UP, rt=0.28)
        self.play(Rotate(chips_st, PI/26, run_time=0.12, rate_func=there_and_back))

        chip_c = chip.get_center()
        trace_data = [
            (chip_c + LEFT*1.00+UP*0.26,    chip_c + LEFT*2.20+UP*0.70),
            (chip_c + LEFT*1.00+DOWN*0.26,  chip_c + LEFT*2.20+DOWN*0.70),
            (chip_c + RIGHT*1.00+UP*0.26,   chip_c + RIGHT*2.00+UP*0.70),
            (chip_c + RIGHT*1.00+DOWN*0.26, chip_c + RIGHT*2.00+DOWN*0.70),
            (chip_c + UP*1.00,              chip_c + UP*2.10),
        ]
        traces = VGroup(*[
            Line(a, b, color=GOLD, stroke_width=2.0, stroke_opacity=0.55)
            for a, b in trace_data
        ])
        self.play(Create(traces, run_time=0.70))

        bolts = [make_lightning(a, b, seed=i*5) for i,(a,b) in enumerate(trace_data)]
        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 5.0),
                    time_width=0.55, run_time=0.70) for bolt in bolts])

        glow = Circle(radius=0.20, color=ELECTRIC, fill_color=ELECTRIC,
                       fill_opacity=0.55, stroke_width=0).move_to(chip_c)
        self.add(glow)
        self.play(glow.animate.scale(4.0).set_opacity(0),
                   run_time=0.22, rate_func=smooth)
        self.remove(glow)

        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 3.5),
                    time_width=0.45, run_time=0.38) for bolt in bolts])

        n3a = nar("Everything runs on... one tiny thing.")
        n3b = nar("Chips.", size=54, color=RED)
        self.play(Write(n3a, run_time=0.75))
        self.wait(1.20)   # hold so viewer can read
        self.play(FadeOut(n3a, run_time=0.35), FadeIn(n3b, run_time=0.35))
        self.play(chip.animate.scale(1.20), run_time=0.60, rate_func=smooth)
        char.swap_face(self, 'shocked', rt=0.22)
        self.wait(1.80)   # reduced from 3.43 to compensate for added holds

        # ── B3 → B4  (char slides fully off-screen for world map beat)
        self.play(
            FadeOut(chip,     run_time=0.38),
            FadeOut(traces,   run_time=0.38),
            FadeOut(chips_st, run_time=0.38),
            FadeOut(n3b,      run_time=0.38),
            char.body.animate.move_to([-8.5, CHAR_HEAD_Y, 0]),
        )
        self.wait(0.08)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  24s → 34s  │  World map + Taiwan
        #
        # Char fully off-screen. Full-width map with no character clutter.
        #
        # 0.00–0.40  map tint fades in               0.40s
        # 0.40–1.70  world dots appear               1.30s
        # 1.70–2.55  Taiwan dot + rings              0.85s
        # 2.55–3.30  TAIWAN panel + connector        0.75s
        # 3.30–4.00  arc arrow draws                 0.70s
        # 4.00–4.80  ring second pulse               0.80s
        # 4.80–5.80  narration part 1                1.00s
        # 5.80–6.10  hold                            0.30s
        # 6.10–6.50  narration swap                  0.40s
        # 6.50–10.0  hold                            3.50s
        # ══════════════════════════════════════════════════════════════
        map_bg = Rectangle(width=15.5, height=9.5, fill_color=MAP_GREEN,
                             fill_opacity=0.28, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(map_bg, run_time=0.40))

        world = make_world_dots()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in world],
                               lag_ratio=0.003, run_time=1.30))

        TW = np.array([5.20, 0.30, 0])
        dot_tw = Dot(TW, radius=0.14, color=RED, fill_opacity=1)
        rings  = VGroup(*[
            Circle(radius=r, color=RED,
                    stroke_opacity=0.65-i*0.18, stroke_width=2.5).move_to(TW)
            for i,r in enumerate([0.14,0.28,0.46])
        ])
        self.play(
            FadeIn(dot_tw, scale=0.2, run_time=0.50),
            LaggedStart(*[GrowFromCenter(r) for r in rings],
                         lag_ratio=0.22, run_time=0.85),
        )

        # Panel LEFT of dot (dot at x=5.2 → panel at x=3.1, stays on screen)
        PW4   = 2.60
        tw_p  = ink_panel(PW4, 0.65, fill="#FFF0F0", stroke=RED, sw=3.5)\
                  .move_to([3.00, 1.20, 0])
        tw_t  = fit_text("TAIWAN", max_width=PW4-0.30, size=30, color=RED)\
                  .move_to(tw_p[1].get_center())
        tw_ln = Line(tw_p[1].get_right()+RIGHT*0.06, TW+LEFT*0.18,
                      color=RED, stroke_width=1.6, stroke_opacity=0.60)
        self.play(
            GrowFromCenter(tw_p, run_time=0.35),
            Write(tw_t,          run_time=0.40),
            Create(tw_ln,        run_time=0.35),
        )

        arc = ArcBetweenPoints(TW+LEFT*0.18, np.array([-0.5,0.65,0]),
                                angle=-0.72, color=RED,
                                stroke_width=2.8).add_tip(tip_length=0.24)
        self.play(Create(arc, run_time=0.70))
        self.play(rings.animate.scale(2.1).set_stroke(opacity=0),
                   run_time=0.80, rate_func=smooth)

        n4a = nar("These chips come from one tiny island.")
        n4b = nar("Taiwan.", size=54, color=RED)
        self.play(Write(n4a, run_time=1.00))
        self.wait(1.20)   # hold so viewer can read
        self.play(FadeOut(n4a, run_time=0.35), FadeIn(n4b, run_time=0.35))
        self.wait(2.00)   # reduced from 3.50 to compensate

        # ── B4 → B5  (keep map_bg, world, dot_tw)
        self.play(
            FadeOut(tw_p,  run_time=0.38),
            FadeOut(tw_t,  run_time=0.38),
            FadeOut(tw_ln, run_time=0.38),
            FadeOut(arc,   run_time=0.38),
            FadeOut(rings, run_time=0.38),
            FadeOut(n4b,   run_time=0.38),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  34s → 45s  │  Worried char + glitch + fade to black
        #
        # Char walks back in to x=-4.5 (left).
        # Ghost icons RIGHT half: x=0.0, 2.2, 4.4
        # Map stays dimmed in background.
        #
        # 0.00–0.50  char walks back in              0.50s
        # 0.50–0.72  face → worried                  0.22s
        # 0.72–0.90  sweat drops appear              0.18s
        # 0.90–1.20  warning panel slams             0.30s
        # 1.20–1.32  warn text fades in              0.12s
        # 1.32–1.92  ghost icons fade in             0.60s
        # 1.92–2.92  narration part 1                1.00s
        # 2.92–3.32  hold                            0.40s
        # 3.32–3.76  glitch (6 steps)                0.44s
        # 3.76–4.31  icons fade out                  0.55s
        # 4.31–5.01  map + dot dim                   0.70s
        # 5.01–5.46  narration swap                  0.45s
        # 5.46–5.68  char shake                      0.22s
        # 5.68–7.18  hold                            1.50s
        # 7.18–8.68  fade to black overlay           1.50s
        # ══════════════════════════════════════════════════════════════
        self.play(
            char.body.animate.move_to([-4.50, CHAR_HEAD_Y, 0]),
            run_time=0.50, rate_func=smooth,
        )
        char.swap_face(self, 'worried', rt=0.22)

        # Sweat drops — placed relative to current head position
        hc = char.head.get_center()
        sweat = VGroup(
            Dot(radius=0.07, color=BLUE, fill_opacity=0.80)
            .move_to(hc + RIGHT*0.36 + UP*0.16),
            Dot(radius=0.04, color=BLUE, fill_opacity=0.55)
            .move_to(hc + RIGHT*0.50 + UP*0.32),
        )
        self.add(sweat)
        self.play(FadeIn(sweat, scale=0.5, run_time=0.18))

        PW5   = 6.4
        warn_p = ink_panel(PW5, 0.72, fill="#FFF0F0", stroke=RED, sw=3.5)\
                   .move_to([0, TOP_Y, 0])
        warn_t = fit_text("What if the supply stops?",
                           max_width=PW5-0.40, size=30, color=RED)\
                   .move_to(warn_p[1].get_center())
        slam(self, warn_p, from_dir=UP, rt=0.30)
        self.add(warn_t)
        self.play(FadeIn(warn_t, run_time=0.12))

        # Ghost icons — right half only
        ph5 = make_phone().scale(0.62).move_to([ 0.00, STAGE_Y-0.05, 0])
        ca5 = make_car().scale(0.58).move_to(  [ 2.20, STAGE_Y-0.20, 0])
        bk5 = make_bank().scale(0.58).move_to( [ 4.40, STAGE_Y-0.05, 0])
        icons5 = VGroup(ph5, ca5, bk5)
        self.play(FadeIn(icons5, run_time=0.60))

        n5a = nar("If this supply stops...")
        n5b = nar("The whole world stops.", size=44, color=RED)
        self.play(Write(n5a, run_time=1.00))
        self.wait(0.40)

        # Simultaneous glitch on all icons
        for dx, op in [(0.08,0.50),(-0.16,0.88),(0.08,0.32),
                        (-0.09,0.65),(0.10,0.18),(-0.07,0.18)]:
            self.play(icons5.animate.shift(RIGHT*dx).set_opacity(op),
                       run_time=0.07, rate_func=linear)

        self.play(FadeOut(icons5, run_time=0.55, rate_func=smooth))
        self.play(
            world.animate.set_opacity(0.10),
            map_bg.animate.set_fill(opacity=0.07),
            dot_tw.animate.set_opacity(0.12),
            run_time=0.70, rate_func=smooth,
        )
        self.play(FadeOut(n5a, run_time=0.22), FadeIn(n5b, run_time=0.22))

        char.shake(self, times=3)
        self.wait(1.50)

        # ── Fade to black via overlay (safe — no Group.set_opacity issues)
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)