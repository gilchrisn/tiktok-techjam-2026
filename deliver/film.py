"""Geometry of the kernel. Offline. No LaTeX.

The picture is the claim. Captions name objects, they do not restate them.

Render from this folder:
  manim -qm --fps 30 -o architecture.mp4 film.py ArchitectureFilm
"""
from __future__ import annotations

import numpy as np
from manim import *

BG = "#14171B"
INK = "#EDEFF2"
SOFT = "#A6AFBA"
MUTED = "#737D89"
TEAL = "#74B8B0"
CORAL = "#D9647A"
GOLD = "#D9A441"
CARD = "#1B1F25"


def caption(text, color=SOFT, size=22):
    return Text(text, font="Georgia", font_size=size, color=color).to_edge(DOWN, buff=0.32)


def name(text, color=MUTED, size=16):
    return Text(text, font="Consolas", font_size=size, color=color)


class ArchitectureFilm(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.fork()
        self.slit()
        self.cover()
        self.barrier()
        self.flock()
        self.column()

    def wipe(self):
        leftover = [m for m in self.mobjects if m is not None]
        if leftover:
            self.play(*[FadeOut(m) for m in leftover], run_time=0.45)

    def fork(self):
        # One point. Two paths. ~20s
        split = Circle(radius=0.55, color=TEAL, stroke_width=3).move_to(LEFT * 0.8)
        split_lab = name("respond()").next_to(split, DOWN, buff=0.18)
        self.play(Create(split), FadeIn(split_lab), run_time=0.8)

        incoming = Dot(color=INK, radius=0.1).move_to(LEFT * 6.2)
        in_path = Line(LEFT * 6.2, split.get_left(), color=MUTED, stroke_width=2)
        self.play(GrowFromPoint(in_path, in_path.get_start()), incoming.animate.move_to(split.get_center()), run_time=1.1)
        self.remove(incoming)

        person = DashedVMobject(Circle(radius=1.15, color=TEAL, stroke_width=2), num_dashes=24)
        person.move_to(RIGHT * 4.6 + UP * 2.05)
        person_lab = name("person", TEAL).next_to(person, DOWN, buff=0.12)

        kernel = RoundedRectangle(
            corner_radius=0.12, width=2.8, height=1.6,
            stroke_color=CORAL, stroke_width=3, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 4.6 + DOWN * 2.0)
        kernel_lab = name("kernel", CORAL).next_to(kernel, DOWN, buff=0.12)

        self.play(FadeIn(person), FadeIn(person_lab), FadeIn(kernel), FadeIn(kernel_lab), run_time=0.9)

        path_m = ArcBetweenPoints(split.get_center(), person.get_center(), angle=-TAU / 7)
        path_m.set_color(TEAL).set_stroke(width=3)
        path_r = ArcBetweenPoints(split.get_center(), kernel.get_center(), angle=TAU / 7)
        path_r.set_color(CORAL).set_stroke(width=3)
        lab_m = name("m", TEAL, 18).next_to(path_m.point_from_proportion(0.45), UP, buff=0.08)
        lab_r = name("a, R", CORAL, 18).next_to(path_r.point_from_proportion(0.45), DOWN, buff=0.08)

        self.play(Create(path_m), Create(path_r), FadeIn(lab_m), FadeIn(lab_r), run_time=1.2)

        cap = caption("One call. Two paths.")
        self.play(FadeIn(cap), run_time=0.4)

        for _ in range(3):
            dm = Dot(color=TEAL, radius=0.11).move_to(split.get_center())
            dr = Dot(color=CORAL, radius=0.11).move_to(split.get_center())
            self.add(dm, dr)
            self.play(
                MoveAlongPath(dm, path_m),
                MoveAlongPath(dr, path_r),
                run_time=2.6,
                rate_func=linear,
            )
            self.play(FadeOut(dm), FadeOut(dr), run_time=0.2)

        self.wait(2.0)
        self.play(FadeOut(cap), run_time=0.3)
        self._split = split
        self._paths = VGroup(path_m, path_r, lab_m, lab_r, in_path, split_lab, person, person_lab, kernel, kernel_lab)

    def slit(self):
        # Domain of customer_reply is a slit that only a fits. ~28s
        self.play(FadeOut(self._split), FadeOut(self._paths), run_time=0.45)

        box = RoundedRectangle(
            corner_radius=0.1, width=4.6, height=3.2,
            stroke_color=CORAL, stroke_width=3, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 1.3 + DOWN * 0.15)
        slit = Rectangle(width=0.22, height=0.55, fill_color=BG, fill_opacity=1, stroke_width=0)
        slit.move_to(box.get_left() + RIGHT * 0.01)
        box_lab = name("customer_reply").next_to(box, UP, buff=0.16)
        self.play(FadeIn(box), FadeIn(slit), FadeIn(box_lab), run_time=0.8)

        y = Dot(color=GOLD, radius=0.14).move_to(box.get_center() + RIGHT * 0.9 + UP * 0.55)
        y_lab = name("y  frozen", GOLD, 15).next_to(y, RIGHT, buff=0.12)
        self.play(FadeIn(y, scale=0.5), FadeIn(y_lab), run_time=0.6)

        a = Square(side_length=0.28, color=CORAL, fill_opacity=1, fill_color=CORAL).move_to(LEFT * 5.4 + DOWN * 0.15)
        a_lab = name("a", CORAL, 18).next_to(a, UP, buff=0.1)
        slate = VGroup(*[
            Rectangle(width=0.16, height=0.85, fill_color=CORAL, fill_opacity=0.85, stroke_width=0)
            for _ in range(10)
        ]).arrange(RIGHT, buff=0.05).move_to(LEFT * 5.2 + UP * 1.55)
        slate_lab = name("R", CORAL, 18).next_to(slate, UP, buff=0.1)
        msg = RoundedRectangle(
            corner_radius=0.2, width=1.35, height=0.7,
            stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.9, stroke_width=0,
        ).move_to(LEFT * 5.3 + DOWN * 1.85)
        msg_lab = name("m", TEAL, 18).next_to(msg, DOWN, buff=0.1)
        self.play(
            FadeIn(a), FadeIn(a_lab), FadeIn(slate), FadeIn(slate_lab),
            FadeIn(msg), FadeIn(msg_lab), run_time=0.8,
        )

        cap = caption("Only the ask fits the domain.")
        self.play(FadeIn(cap), run_time=0.3)

        # a slides through the slit
        self.play(a.animate.move_to(slit.get_center() + LEFT * 0.05), run_time=1.1)
        self.play(a.animate.move_to(box.get_center() + LEFT * 0.6), run_time=0.7)
        self.play(a.animate.set_opacity(0.35), run_time=0.25)

        # R is too wide; bounce, then fall to scorer
        wall = box.get_left() + LEFT * 0.15 + UP * 1.4
        self.play(slate.animate.move_to(wall), run_time=0.9)
        bounce = wall + LEFT * 1.1 + DOWN * 0.15
        self.play(slate.animate.move_to(bounce), run_time=0.35)
        scorer = RoundedRectangle(
            corner_radius=0.08, width=2.2, height=0.7,
            stroke_color=GOLD, stroke_width=2, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 1.3 + DOWN * 3.15)
        scorer_lab = name("scorer", GOLD, 14).move_to(scorer.get_center())
        self.play(FadeIn(scorer), FadeIn(scorer_lab), slate.animate.scale(0.55).move_to(scorer.get_center()), run_time=1.0)
        self.play(slate.animate.set_opacity(0.4), run_time=0.2)

        # m hits the wall and vanishes
        self.play(msg.animate.move_to(box.get_left() + LEFT * 0.2 + DOWN * 1.1), run_time=0.8)
        x = Text("x", font="Georgia", font_size=36, color=CORAL).move_to(msg.get_center())
        self.play(FadeIn(x), FadeOut(msg), run_time=0.45)
        self.play(FadeOut(x), FadeOut(msg_lab), run_time=0.3)

        cap2 = caption("The next user sentence is a function of a. Not of R. Not of m.")
        self.play(FadeOut(cap), FadeIn(cap2), Circumscribe(y, color=GOLD), run_time=1.4)
        self.wait(12.5)

        self.play(*[FadeOut(m) for m in [
            box, slit, box_lab, y, y_lab, a, a_lab, slate, slate_lab,
            scorer, scorer_lab, cap2,
        ]], run_time=0.5)

    def cover(self):
        # Four points. A wedge vs the disk. ~35s
        ring = Circle(radius=2.15, color=MUTED, stroke_width=2).move_to(LEFT * 1.3 + UP * 0.15)
        dots = VGroup()
        for i in range(4):
            ang = i * TAU / 4 + TAU / 8
            d = Dot(color=INK, radius=0.16).move_to(
                ring.get_center() + 1.45 * np.array([np.cos(ang), np.sin(ang), 0])
            )
            d.set_z_index(4)
            dots.add(d)
        c_lab = name("C  four constraints").next_to(ring, UP, buff=0.28)
        self.play(Create(ring), LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.15), FadeIn(c_lab), run_time=1.4)

        well = RoundedRectangle(
            corner_radius=0.1, width=2.0, height=2.4,
            stroke_color=MUTED, stroke_width=2, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 4.4 + UP * 0.1)
        well.set_z_index(1)
        well_lab = name("D").next_to(well, UP, buff=0.14)
        self.play(FadeIn(well), FadeIn(well_lab), run_time=0.5)

        # facet = a thin wedge covering at most one
        wedge = Sector(
            radius=2.15, angle=TAU / 8, start_angle=TAU / 8 - TAU / 16,
            color=MUTED, fill_opacity=0.45, stroke_width=0,
        ).shift(ring.get_center())
        cap = caption("A facet label is a wedge.")
        self.play(FadeIn(wedge), FadeIn(cap), run_time=0.9)
        self.wait(2.2)

        # other = the disk
        fill = Circle(radius=2.15, color=CORAL, fill_opacity=0.28, stroke_width=0).move_to(ring.get_center())
        cap2 = caption("other is the disk. The cap is two.")
        self.play(FadeOut(wedge), FadeIn(fill), FadeOut(cap), FadeIn(cap2), run_time=1.0)

        # two leave, then two. empty at turn 3
        first = VGroup(dots[0], dots[1])
        rest = VGroup(dots[2], dots[3])
        self.play(
            first[0].animate.set_color(GOLD).scale(1.35).move_to(well.get_center() + UP * 0.5 + LEFT * 0.35),
            first[1].animate.set_color(GOLD).scale(1.35).move_to(well.get_center() + UP * 0.5 + RIGHT * 0.35),
            run_time=1.3,
        )
        t1 = name("t = 1", CORAL, 18).next_to(well, DOWN, buff=0.2)
        self.play(FadeIn(t1), run_time=0.3)
        self.wait(2.5)

        self.play(
            rest[0].animate.set_color(GOLD).scale(1.35).move_to(well.get_center() + DOWN * 0.5 + LEFT * 0.35),
            rest[1].animate.set_color(GOLD).scale(1.35).move_to(well.get_center() + DOWN * 0.5 + RIGHT * 0.35),
            run_time=1.3,
        )
        t2 = name("t = 2   empty", CORAL, 18).next_to(well, DOWN, buff=0.2)
        self.bring_to_front(dots)
        self.play(FadeOut(t1), FadeIn(t2), fill.animate.set_opacity(0.08), ring.animate.set_stroke(MUTED, 1), run_time=0.6)

        cap3 = caption("Always-other empties C by the start of turn 3.")
        self.play(FadeOut(cap2), FadeIn(cap3), run_time=0.6)
        self.wait(14.0)
        self.play(*[FadeOut(m) for m in [ring, fill, c_lab, well, well_lab, dots, t2, cap3]], run_time=0.45)

    def barrier(self):
        # First ten slots. Gold enters. The row freezes. ~30s
        slots = VGroup()
        for i in range(10):
            s = RoundedRectangle(
                corner_radius=0.06, width=0.72, height=1.15,
                stroke_color=MUTED, stroke_width=2, fill_color=CARD, fill_opacity=1,
            )
            slots.add(s)
        slots.arrange(RIGHT, buff=0.12).move_to(UP * 0.55)
        idx = VGroup(*[
            name(str(i + 1), MUTED, 14).next_to(slots[i], DOWN, buff=0.12)
            for i in range(10)
        ])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in slots], lag_ratio=0.05), FadeIn(idx), run_time=1.2)

        gate = Line(
            slots.get_right() + RIGHT * 0.35 + UP * 1.1,
            slots.get_right() + RIGHT * 0.35 + DOWN * 1.1,
            color=GOLD, stroke_width=6,
        )
        gate_lab = name("stop", GOLD, 16).next_to(gate, RIGHT, buff=0.12)
        self.play(Create(gate), FadeIn(gate_lab), run_time=0.5)

        y = Dot(color=GOLD, radius=0.16).move_to(LEFT * 6.4 + UP * 0.55)
        cap = caption("If y is in the ten, the session records that turn and breaks.")
        self.play(FadeIn(y), FadeIn(cap), run_time=0.5)
        self.play(y.animate.move_to(slots[0].get_center()), run_time=1.4)
        freeze = Rectangle(
            width=slots.width + 0.35, height=slots.height + 0.4,
            stroke_color=GOLD, stroke_width=4, fill_opacity=0,
        ).move_to(slots)
        self.play(Create(freeze), Flash(y, color=GOLD, line_length=0.22), run_time=0.8)
        self.wait(3.5)

        # mass already at rank 1: delay has nothing to buy
        self.play(FadeOut(freeze), FadeOut(gate), FadeOut(gate_lab), FadeOut(idx), run_time=0.4)
        stack1 = VGroup(*[Dot(color=GOLD, radius=0.055) for _ in range(61)])
        stack1.arrange_in_grid(rows=7, cols=9, buff=0.08).next_to(slots[0], UP, buff=0.35)
        rest = VGroup(*[Dot(color=MUTED, radius=0.055) for _ in range(26)])
        rest.arrange_in_grid(rows=4, cols=7, buff=0.08).next_to(slots[4], UP, buff=0.55)
        n1 = name("122 already r = 1", GOLD, 16).next_to(stack1, UP, buff=0.16)
        n2 = name("53 later", MUTED, 16).next_to(rest, UP, buff=0.16)
        # 61+26 is a 1:2 scale of 122:53 so the picture fits
        self.play(
            slots.animate.shift(DOWN * 0.55),
            y.animate.shift(DOWN * 0.55),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in stack1], lag_ratio=0.01),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in rest], lag_ratio=0.02),
            FadeIn(n1), FadeIn(n2),
            run_time=1.8,
        )
        cap2 = caption("Delay pays only if rank can still move. Rank 1 cannot.")
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.6)
        zlab = name("wait = 0", CORAL, 16).next_to(n1, RIGHT, buff=0.25)
        self.play(FadeIn(zlab), run_time=0.4)
        self.wait(11.0)
        self.play(*[FadeOut(m) for m in [slots, y, stack1, rest, n1, n2, zlab, cap2]], run_time=0.45)

    def flock(self):
        # 175 already-solved. Keep / drop / add. ~25s
        dots = VGroup(*[Dot(color=GOLD, radius=0.045) for _ in range(175)])
        dots.arrange_in_grid(rows=7, cols=25, buff=0.11).move_to(UP * 0.35)
        cap = caption("175 already-solved hits.")
        self.play(FadeIn(dots), FadeIn(cap), run_time=1.4)

        # within-10: shuffle in place, none leave
        rng = np.random.default_rng(0)
        jitters = [0.06 * rng.standard_normal(3) * np.array([1, 1, 0]) for _ in range(175)]
        self.play(*[dots[i].animate.shift(jitters[i]) for i in range(175)], run_time=0.8)
        self.play(*[dots[i].animate.shift(-jitters[i]) for i in range(175)], run_time=0.8)
        capk = caption("Popularity inside the ten. None leave.")
        self.play(FadeOut(cap), FadeIn(capk), run_time=0.5)
        self.wait(3.2)

        # 400-window: 28 vanish (scale model of 102 -> 74)
        dying = VGroup(*dots[147:])
        capd = caption("Popularity over four hundred. Twenty-eight already-solved hits drop.")
        self.play(dying.animate.set_color(CORAL), FadeOut(capk), FadeIn(capd), run_time=0.6)
        self.play(FadeOut(dying), run_time=1.1)
        self.wait(3.5)

        # category: 8 new
        extras = VGroup(*[Dot(color=TEAL, radius=0.05) for _ in range(8)])
        extras.arrange(RIGHT, buff=0.16).move_to(LEFT * 5.5 + DOWN * 2.4)
        token = name("I'm looking for {category}", GOLD, 16).next_to(extras, UP, buff=0.14)
        self.play(FadeIn(token), FadeIn(extras), run_time=0.6)
        dests = [dots.get_right() + RIGHT * 0.25 + DOWN * (i - 3.5) * 0.16 for i in range(8)]
        self.play(*[extras[i].animate.move_to(dests[i]).set_color(GOLD) for i in range(8)], run_time=1.2)
        capc = caption("Opening category is already in the first sentence. Eight hits, none lost.")
        self.play(FadeOut(token), FadeOut(capd), FadeIn(capc), run_time=0.6)
        self.wait(6.5)
        self.play(FadeOut(dots), FadeOut(extras), FadeOut(capc), run_time=0.4)

    def column(self):
        # S as a stacked height. m remains outside. ~18s
        axis = Line(DOWN * 2.6, UP * 2.8, color=MUTED, stroke_width=2).move_to(LEFT * 0.4)
        top = name("1.0", MUTED, 14).next_to(axis.get_top(), LEFT, buff=0.16)
        self.play(Create(axis), FadeIn(top), run_time=0.4)

        # S = 0.50 h + 0.30 MRR + 0.20 Eff = 0.842
        scale = 5.2
        h = 0.50 * 0.915 * scale
        mrr = 0.30 * 0.750 * scale
        eff = 0.20 * np.clip((11 - 3.02) / 10, 0, 1) * scale
        base = axis.get_bottom() + RIGHT * 0.85
        r_h = Rectangle(width=1.6, height=h, fill_color=TEAL, fill_opacity=0.9, stroke_width=0)
        r_m = Rectangle(width=1.6, height=mrr, fill_color=GOLD, fill_opacity=0.9, stroke_width=0)
        r_e = Rectangle(width=1.6, height=eff, fill_color=CORAL, fill_opacity=0.9, stroke_width=0)
        r_h.move_to(base, aligned_edge=DOWN + LEFT)
        r_m.next_to(r_h, UP, buff=0)
        r_e.next_to(r_m, UP, buff=0)
        lab_h = name("Hit  0.915", TEAL, 16).next_to(r_h, RIGHT, buff=0.2)
        lab_m = name("MRR  0.750", GOLD, 16).next_to(r_m, RIGHT, buff=0.2)
        lab_e = name("Eff   MTTC 3.02", CORAL, 16).next_to(r_e, RIGHT, buff=0.2)
        mark = DashedLine(
            r_e.get_top() + LEFT * 1.2, r_e.get_top() + RIGHT * 2.8,
            color=INK, stroke_width=1.5,
        )
        s_lab = name("S = 0.842", INK, 22).next_to(mark, RIGHT, buff=0.1)

        self.play(FadeIn(r_h, shift=UP * 0.2), FadeIn(lab_h), run_time=0.7)
        self.play(FadeIn(r_m, shift=UP * 0.2), FadeIn(lab_m), run_time=0.5)
        self.play(FadeIn(r_e, shift=UP * 0.2), FadeIn(lab_e), run_time=0.5)
        self.play(Create(mark), FadeIn(s_lab), run_time=0.5)

        outside = DashedVMobject(Circle(radius=0.85, color=TEAL, stroke_width=2), num_dashes=18)
        outside.move_to(LEFT * 4.6 + UP * 0.2)
        mdot = Dot(color=TEAL, radius=0.12).move_to(outside.get_center())
        mlab = name("m  not in S", TEAL, 16).next_to(outside, DOWN, buff=0.16)
        self.play(FadeIn(outside), FadeIn(mdot), FadeIn(mlab), run_time=0.7)
        self.play(Rotate(mdot, angle=TAU, about_point=outside.get_center()), run_time=3.2, rate_func=linear)

        cap = caption("0.84 is the adapter. The teal path is the idea the kernel cannot see.")
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(8.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
