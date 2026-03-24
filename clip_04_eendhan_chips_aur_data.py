"""
clip_04_eendhan_chips_aur_data.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Eendhan — Chips aur Data"
Scenes: supply_chain_flow, cost_bars
Duration: ~90 seconds  (3:45 – 5:15)
RENDER: manim -pqh clip_04_eendhan_chips_aur_data.py EendhanChipsData
"""

from manim import *
import numpy as np, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from brand import *

# ╔══════════════════════════════════════╗
# ║              INPUTS                 ║
# ║  Edit these before each render      ║
# ╚══════════════════════════════════════╝
# Supply chain nodes
CHAIN_NODES = [
    {"label": "Taiwan",     "sub": "Chip Fab",        "color": C_STAT},
    {"label": "Shipped",    "sub": "Global Freight",  "color": C_DIM},
    {"label": "Data Center","sub": "Server Rack",     "color": C_INFRA},
    {"label": "AI Model",   "sub": "Training Run",    "color": C_GPT},
]

# Cost bars
SOURCE_COST    = "Source: Estimates — SemiAnalysis, 2023"

# Timing
T_NODE_BUILD   = 0.7    # each node fades in
T_NODE_LAG     = 0.22   # LaggedStart lag between nodes
T_ARROW_DRAW   = 0.55   # each connecting arrow draws
T_PULSE_HOLD   = 1.8    # hold after pulse travels the chain
T_CHAIN_HOLD   = 2.8    # hold on full chain
T_BAR_GROW     = 2.2    # bars grow up
T_LABEL_HOLD   = 3.2    # hold on final bar comparison
T_OUTRO        = 1.2
# ╚══════════════════════════════════════╝


# ── Icon builders ────────────────────────────────────────────────────────────

def chip_icon(color=C_STAT, size=0.72):
    """
    CPU chip: square body + small pins on all four sides.
    """
    body = Square(side_length=size,
                  fill_color=C_DARK, fill_opacity=1,
                  stroke_color=color, stroke_width=2.2)
    # Inner grid lines (2×2)
    h1 = Line(LEFT * size/2, RIGHT * size/2,
              color=color, stroke_width=0.8).shift(UP * size * 0.16)
    h2 = Line(LEFT * size/2, RIGHT * size/2,
              color=color, stroke_width=0.8).shift(DOWN * size * 0.16)
    v1 = Line(UP * size/2, DOWN * size/2,
              color=color, stroke_width=0.8).shift(LEFT * size * 0.16)
    v2 = Line(UP * size/2, DOWN * size/2,
              color=color, stroke_width=0.8).shift(RIGHT * size * 0.16)
    # Pins — 3 per side
    pins = VGroup()
    pin_len = size * 0.18
    for side_name, direction in [("UP", UP), ("DOWN", DOWN), ("LEFT", LEFT), ("RIGHT", RIGHT)]:
        for offset in [-0.22, 0.0, 0.22]:
            if side_name in ("UP", "DOWN"):
                start = direction * size/2 + RIGHT * offset * size
            else:
                start = direction * size/2 + UP * offset * size
            pin = Line(start, start + direction * pin_len,
                       color=color, stroke_width=1.4)
            pins.add(pin)
    return VGroup(body, h1, h2, v1, v2, pins)


def ship_icon(color=C_DIM, w=1.1, h=0.48):
    """Simple cargo ship silhouette: hull + deck box + funnel."""
    hull  = Polygon(
        LEFT * w/2 + DOWN * h/2,
        RIGHT * w/2 + DOWN * h/2,
        RIGHT * (w/2 - 0.15) + UP * h/2,
        LEFT  * (w/2 - 0.15) + UP * h/2,
        fill_color=color, fill_opacity=0.85, stroke_width=0
    )
    deck  = Rectangle(width=w * 0.45, height=h * 0.45,
                      fill_color=C_DARK, fill_opacity=1,
                      stroke_color=color, stroke_width=1.2)
    deck.move_to(UP * h * 0.55)
    funnel = Rectangle(width=w * 0.10, height=h * 0.38,
                       fill_color=color, fill_opacity=1, stroke_width=0)
    funnel.move_to(UP * h * 0.82 + RIGHT * w * 0.08)
    return VGroup(hull, deck, funnel)


def rack_icon(color=C_INFRA, w=0.72, h=1.1, n=5):
    """Server rack: outer frame + n server unit slots."""
    frame = Rectangle(width=w, height=h,
                      fill_color=C_DARK, fill_opacity=1,
                      stroke_color=color, stroke_width=2.0)
    units = VGroup()
    slot_h = (h - 0.18) / n
    for i in range(n):
        y = h/2 - 0.09 - slot_h/2 - i * slot_h
        slot = Rectangle(width=w - 0.18, height=slot_h * 0.72,
                         fill_color=color, fill_opacity=0.25,
                         stroke_color=color, stroke_width=0.8)
        slot.move_to(UP * y)
        # LED dot
        led = Circle(radius=0.035,
                     fill_color=C_GPT, fill_opacity=1, stroke_width=0)
        led.move_to(slot.get_right() + LEFT * 0.10)
        units.add(VGroup(slot, led))
    return VGroup(frame, units)


def brain_icon(color=C_GPT, r=0.55):
    """
    Simplified AI brain: circle + internal network of lines + dots.
    """
    outer = Circle(radius=r, color=color,
                   stroke_width=2.2, fill_opacity=0)
    # Internal nodes
    rng   = np.random.default_rng(3)
    pts   = [r * 0.65 * np.array([np.cos(a), np.sin(a), 0])
             for a in np.linspace(0, TAU, 6, endpoint=False)]
    pts.append(ORIGIN)
    nodes = VGroup(*[
        Circle(radius=0.055, fill_color=color,
               fill_opacity=1, stroke_width=0).move_to(p)
        for p in pts
    ])
    # Edges — not all, just enough to feel like a network
    edges = VGroup()
    connections = [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(0,1),(2,3),(4,5)]
    for a, b in connections:
        edges.add(Line(pts[a], pts[b],
                       color=color, stroke_width=0.9, stroke_opacity=0.55))
    return VGroup(outer, edges, nodes)


def flow_node(icon, label_str, sub_str, color):
    """
    Card that wraps an icon with a label below and sub-label beneath.
    Returns VGroup(card_bg, icon, label, sub).
    """
    card = RoundedRectangle(corner_radius=0.16, width=2.1, height=2.4,
                            fill_color=C_DARK, fill_opacity=1,
                            stroke_color=color, stroke_width=1.6)
    icon.move_to(UP * 0.38)
    lbl = Text(label_str, font="Arial", weight=BOLD,
               font_size=19, color=C_WHITE).move_to(DOWN * 0.38)
    sub = Text(sub_str,   font="Arial",
               font_size=14, color=color).move_to(DOWN * 0.72)
    return VGroup(card, icon, lbl, sub)


# ── Bar chart helpers ────────────────────────────────────────────────────────

def cost_bar(model, year, cost, label_str, color,
             bar_max_cost, bar_max_h, bar_w=1.4):
    """
    Returns VGroup(base_line, bar, model_lbl, year_lbl, cost_lbl).
    bar height scales linearly with cost / bar_max_cost.
    """
    h      = bar_max_h * (cost / bar_max_cost)
    bar    = Rectangle(width=bar_w, height=h,
                       fill_color=color, fill_opacity=1, stroke_width=0)
    # Anchor bar bottom to y=0
    bar.move_to(UP * h / 2)

    base   = Line(LEFT * bar_w/2, RIGHT * bar_w/2,
                  color=C_GRID, stroke_width=1.4)

    model_lbl = Text(model, font="Arial", weight=BOLD,
                     font_size=20, color=C_WHITE).next_to(bar, DOWN, buff=0.28)
    year_lbl  = Text(year,  font="Arial",
                     font_size=15, color=C_DIM).next_to(model_lbl, DOWN, buff=0.08)
    cost_lbl  = Text(label_str, font="Arial", weight=BOLD,
                     font_size=22, color=color).next_to(bar, UP, buff=0.18)
    return VGroup(base, bar, model_lbl, year_lbl, cost_lbl), h


# ── Main scene ───────────────────────────────────────────────────────────────

class EendhanChipsData(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (3:45 – 4:25)  ~40s
        # SUPPLY CHAIN FLOW
        # Four nodes in a horizontal row connected by animated arrows.
        # A glowing pulse dot travels along each arrow in sequence.
        # Camera starts on Taiwan node, pans right through the chain,
        # then pulls back to reveal the full pipeline.
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("Fuel")
        self.play(FadeIn(sec1), run_time=0.4)

        # Build four flow node cards
        icons = [
            chip_icon(color=C_STAT),
            ship_icon(color=C_DIM),
            rack_icon(color=C_INFRA),
            brain_icon(color=C_GPT),
        ]

        # Layout: evenly spaced, centred, within safe x range [-5.5, +5.5]
        N          = len(CHAIN_NODES)
        CARD_W     = 2.1
        CARD_GAP   = 0.55
        total_w    = N * CARD_W + (N - 1) * CARD_GAP
        xs         = [(-total_w/2 + CARD_W/2) + i * (CARD_W + CARD_GAP)
                      for i in range(N)]
        NODE_Y     = UP * 0.2

        nodes_built = []
        for i, (nd, icon) in enumerate(zip(CHAIN_NODES, icons)):
            fn = flow_node(icon, nd["label"], nd["sub"], nd["color"])
            fn.move_to(RIGHT * xs[i] + NODE_Y)
            nodes_built.append(fn)

        # Camera starts punched-in on Taiwan node
        self.play(
            self.camera.frame.animate
                .scale(0.55)
                .move_to(nodes_built[0].get_center()),
            run_time=0.6
        )

        # Taiwan node grows from point
        self.play(
            FadeIn(nodes_built[0], scale=0.05, rate_func=rush_into),
            run_time=T_NODE_BUILD
        )
        ripple(self, nodes_built[0].get_center(),
               color=C_STAT, n=3, base_r=0.5, run_t=0.6)
        self.wait(0.8)

        # Draw connecting arrows + reveal each subsequent node
        # Arrow tip-to-tip between card edges
        arrows = []
        for i in range(N - 1):
            left_card  = nodes_built[i]
            right_card = nodes_built[i + 1]
            start = left_card.get_right()  + RIGHT * 0.08
            end   = right_card.get_left()  + LEFT  * 0.08
            arr = Arrow(start, end,
                        color=CHAIN_NODES[i+1]["color"],
                        stroke_width=2.2,
                        max_tip_length_to_length_ratio=0.18,
                        buff=0)
            arrows.append(arr)

        for i in range(1, N):
            # Camera pans to next node while arrow draws
            self.play(
                self.camera.frame.animate.move_to(nodes_built[i].get_center()),
                Create(arrows[i-1], run_time=T_ARROW_DRAW, rate_func=smooth),
                run_time=T_ARROW_DRAW
            )
            self.play(
                FadeIn(nodes_built[i], scale=0.05, rate_func=rush_into),
                run_time=T_NODE_BUILD
            )
            ripple(self, nodes_built[i].get_center(),
                   color=CHAIN_NODES[i]["color"], n=2, base_r=0.4, run_t=0.5)
            self.wait(0.5)

        # Pull back to reveal full chain
        self.play(
            self.camera.frame.animate.restore(),
            run_time=0.8
        )
        self.wait(0.6)

        # Pulse dot travels Taiwan → AI Model along the arrows
        # Each pulse: dot spawns at arrow start, travels to end, then fades
        for i, arr in enumerate(arrows):
            pulse_dot = Dot(radius=0.13,
                            color=CHAIN_NODES[i+1]["color"],
                            fill_opacity=0.9)
            pulse_dot.move_to(arr.get_start())
            self.add(pulse_dot)
            self.play(
                MoveAlongPath(pulse_dot, arr, run_time=0.55, rate_func=smooth)
            )
            self.play(FadeOut(pulse_dot, scale=0.2), run_time=0.22)

        # Second full pulse pass — faster
        for i, arr in enumerate(arrows):
            pulse_dot = Dot(radius=0.10,
                            color=CHAIN_NODES[i+1]["color"],
                            fill_opacity=0.75)
            pulse_dot.move_to(arr.get_start())
            self.add(pulse_dot)
            self.play(
                MoveAlongPath(pulse_dot, arr, run_time=0.35, rate_func=linear)
            )
            self.play(FadeOut(pulse_dot, scale=0.2), run_time=0.15)

        self.wait(T_CHAIN_HOLD)

        # Taiwan label writes in as "bottleneck" callout below chain
        taiwan_callout = TAG("One island. Every AI model depends on it.",
                             color=C_STAT, size=17).move_to(DOWN * 1.85)
        self.play(AddTextLetterByLetter(taiwan_callout, time_per_char=0.035))
        self.wait(1.8)

        # Full clear before Beat 2
        chain_group = VGroup(*nodes_built, *arrows, taiwan_callout)
        self.play(
            FadeOut(chain_group),
            FadeOut(sec1),
            run_time=0.7
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (4:25 – 5:15)  ~50s
        # STACKED TIMELINE — horizontal spine with year nodes.
        # A cost bubble grows at each node, proportional to spend.
        # GPT-3 bubble is modest. GPT-4 bubble is 25× larger —
        # it dramatically overwhelms the earlier one.
        # Model label + cost label appear at each node.
        # Camera travels left→right along the timeline.
        # "Not faster. Exponential." writes in at the end.
        #
        # Layout (all within safe frame):
        #   Timeline spine:  y = 0,  x ∈ [-4.0, +4.0]
        #   Node 1 (GPT-3):  x = -2.8,  bubble radius = 0.38
        #   Node 2 (GPT-4):  x = +2.8,  bubble radius = 1.55
        #   Labels above/below nodes, cost labels above bubbles
        # ══════════════════════════════════════════════════════════════════

        sec2 = corner_lbl("Training Cost")
        self.play(FadeIn(sec2), run_time=0.4)

        # Timeline data
        # bubble_r scales with sqrt(cost) so area is proportional to cost
        # GPT-3: r = 0.38,  GPT-4: r = 0.38 * sqrt(100/4) = 0.38 * 5 = 1.9
        # Cap GPT-4 at 1.6 to stay in frame (tip at y = 0 + 1.6 + 0.4 label = 2.0 ✓)
        TIMELINE_Y   = 0.0
        SPINE_XL     = -4.2
        SPINE_XR     =  4.2
        NODES = [
            {"model": "GPT-3",  "year": "2020", "cost_str": "$4M",
             "x": -2.6, "r": 0.38, "color": C_INFRA},
            {"model": "GPT-4",  "year": "2023", "cost_str": "$100M+",
             "x":  2.6, "r": 1.58, "color": C_SPEED},
        ]

        # Spine draws in
        spine = Line(LEFT * abs(SPINE_XL), RIGHT * SPINE_XR,
                     color=C_GRID, stroke_width=2.0).move_to(UP * TIMELINE_Y)
        self.play(Create(spine, run_time=1.0, rate_func=smooth))

        # Camera starts punched in on left side — GPT-3 node
        self.play(
            self.camera.frame.animate
                .scale(0.62)
                .move_to(RIGHT * NODES[0]["x"] + UP * TIMELINE_Y),
            run_time=0.55
        )

        # Build nodes one by one, camera panning right
        built_bubbles  = []
        built_labels   = []

        for i, nd in enumerate(NODES):
            cx = nd["x"]
            cy = TIMELINE_Y
            col = nd["color"]

            # Tick mark on spine
            tick = Line(UP * 0.18, DOWN * 0.18,
                        color=col, stroke_width=2.2).move_to(RIGHT * cx + UP * cy)
            self.play(Create(tick, run_time=0.3))

            # Bubble grows from tick centre upward
            # Start at radius 0, grow to full radius
            bubble = Circle(radius=nd["r"],
                            fill_color=col, fill_opacity=0.18,
                            stroke_color=col, stroke_width=2.2)
            bubble.move_to(RIGHT * cx + UP * (cy + nd["r"]))

            bubble_zero = bubble.copy().scale(0.001)
            self.add(bubble_zero)
            self.play(
                ReplacementTransform(bubble_zero, bubble),
                run_time=1.2 if i == 1 else 0.7,
                rate_func=smooth
            )
            ripple(self, bubble.get_center(),
                   color=col, n=2, base_r=nd["r"] * 0.6, run_t=0.5)
            built_bubbles.append(bubble)

            # Year label below spine
            yr_lbl = TAG(nd["year"], color=C_DIM, size=15)
            yr_lbl.move_to(RIGHT * cx + DOWN * 0.48)

            # Model label below year
            mdl_lbl = Text(nd["model"], font="Arial", weight=BOLD,
                           font_size=20, color=C_WHITE)
            mdl_lbl.move_to(RIGHT * cx + DOWN * 0.90)

            # Cost label above bubble
            cost_lbl = Text(nd["cost_str"], font="Arial", weight=BOLD,
                            font_size=22, color=col)
            cost_lbl.move_to(RIGHT * cx + UP * (cy + nd["r"] * 2 + 0.35))

            self.play(
                FadeIn(yr_lbl,  shift=UP * 0.1),
                FadeIn(mdl_lbl, shift=UP * 0.1),
                run_time=0.5
            )
            slam_in(self, cost_lbl, bounces=2, run_t=0.55)
            built_labels.extend([tick, yr_lbl, mdl_lbl, cost_lbl])

            self.wait(0.8 if i == 0 else 0.4)

            # Pan camera to next node (or restore if last)
            if i < len(NODES) - 1:
                self.play(
                    self.camera.frame.animate
                        .move_to(RIGHT * NODES[i+1]["x"] + UP * TIMELINE_Y),
                    run_time=0.9, rate_func=smooth
                )

        # Pull back to show full timeline
        self.play(
            self.camera.frame.animate.restore(),
            run_time=0.8
        )
        self.wait(0.6)

        # Connecting arrow between bubbles — left to right
        # Arrow runs along the spine between the two node ticks
        arrow_spine = Arrow(
            RIGHT * (NODES[0]["x"] + 0.12),
            RIGHT * (NODES[1]["x"] - 0.12),
            color=C_GRID, stroke_width=1.6,
            max_tip_length_to_length_ratio=0.08,
            buff=0
        ).move_to(UP * TIMELINE_Y)
        self.play(Create(arrow_spine, run_time=0.7, rate_func=smooth))
        self.wait(0.4)

        # "25x" multiplier label appears above the arrow midpoint
        mult_lbl = TAG("25x", color=C_STAT, size=22)
        mult_lbl.move_to(UP * (TIMELINE_Y + 0.45))
        slam_in(self, mult_lbl, bounces=2, run_t=0.6)
        self.wait(0.8)

        # "Not faster. Exponential." writes in below timeline
        exp_tag = TAG("Not faster. Exponential.",
                      color=C_STAT, size=19).move_to(DOWN * 1.85)
        self.play(AddTextLetterByLetter(exp_tag, time_per_char=0.045))

        # Source tag
        src = SRC(SOURCE_COST)
        self.play(FadeIn(src), run_time=0.5)

        self.wait(T_LABEL_HOLD)

        # ── End fade ──
        timeline_group = VGroup(
            spine, arrow_spine, mult_lbl, exp_tag, src,
            *built_bubbles, *built_labels
        )
        self.play(
            FadeOut(timeline_group),
            FadeOut(sec2),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()