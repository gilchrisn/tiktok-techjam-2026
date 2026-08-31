"""Geometry of the kernel. Offline. No LaTeX.

Captions follow SCRIPT.md. The picture is the claim.

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


def caption(text, size=22):
    return Text(
        text, font="Georgia", font_size=size, color=SOFT, disable_ligatures=True,
    ).to_edge(DOWN, buff=0.32)


def name(text, color=MUTED, size=16):
    return Text(text, font="Consolas", font_size=size, color=color)


def slots_row(n=10, width=0.68, height=1.05):
    g = VGroup()
    for _ in range(n):
        g.add(RoundedRectangle(
            corner_radius=0.06, width=width, height=height,
            stroke_color=MUTED, stroke_width=2, fill_color=CARD, fill_opacity=1,
        ))
    return g.arrange(RIGHT, buff=0.1)


class ArchitectureFilm(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.task()
        self.slit()
        self.policies()
        self.cover()
        self.barrier()
        self.flock()
        self.session()
        self.column()

    def say(self, old, text, size=22, run_time=0.45):
        new = caption(text, size=size)
        if old is None:
            self.play(FadeIn(new), run_time=run_time)
        else:
            self.play(FadeOut(old), FadeIn(new), run_time=run_time)
        return new

    def task(self):
        # 0:00-0:18  hidden product, ten slots, 0.107 vs 0.842
        dots = VGroup(*[Dot(radius=0.038, color=MUTED) for _ in range(120)])
        dots.arrange_in_grid(rows=8, cols=15, buff=0.16).move_to(LEFT * 1.8 + UP * 0.55)
        y = dots[67]
        y.set_color(GOLD).scale(1.7).set_z_index(3)
        cap = self.say(None, "One hidden product in a catalog of fifty thousand.")
        self.play(FadeIn(dots), run_time=1.2)
        self.play(Indicate(y, color=GOLD, scale_factor=1.5), run_time=0.9)
        self.wait(1.2)

        slots = slots_row().scale(0.92).move_to(DOWN * 1.55)
        lab = name("returned list of ten").next_to(slots, DOWN, buff=0.14)
        cap = self.say(cap, "Ten turns to land it in the ten.")
        self.play(FadeIn(slots), FadeIn(lab), run_time=0.9)
        self.wait(1.2)

        axis = Line(DOWN * 2.3, UP * 2.4, color=MUTED, stroke_width=2).move_to(RIGHT * 4.6)
        h0 = 0.107 * 4.4
        h1 = 0.842 * 4.4
        b0 = Rectangle(width=0.7, height=max(h0, 0.12), fill_color=MUTED, fill_opacity=1, stroke_width=0)
        b1 = Rectangle(width=0.7, height=h1, fill_color=CORAL, fill_opacity=1, stroke_width=0)
        base = axis.get_bottom() + LEFT * 1.15
        b0.move_to(base, aligned_edge=DOWN)
        b1.move_to(base + RIGHT * 1.05, aligned_edge=DOWN)
        n0 = name("0.107", MUTED, 14).next_to(b0, DOWN, buff=0.12)
        n1 = name("0.842", CORAL, 16).next_to(b1, DOWN, buff=0.12)
        cap = self.say(cap, "Starter 0.107. This agent 0.842.")
        self.play(FadeIn(axis), FadeIn(b0), FadeIn(b1), FadeIn(n0), FadeIn(n1), run_time=1.1)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in [dots, slots, lab, axis, b0, b1, n0, n1, cap]], run_time=0.4)

    def slit(self):
        # 0:18-0:42  only the ask enters
        box = RoundedRectangle(
            corner_radius=0.1, width=4.6, height=3.2,
            stroke_color=CORAL, stroke_width=3, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 1.4 + DOWN * 0.05)
        slit = Rectangle(width=0.22, height=0.55, fill_color=BG, fill_opacity=1, stroke_width=0)
        slit.move_to(box.get_left() + RIGHT * 0.01)
        box_lab = name("simulator").next_to(box, UP, buff=0.16)
        self.play(FadeIn(box), FadeIn(slit), FadeIn(box_lab), run_time=0.7)

        y = Dot(color=GOLD, radius=0.14).move_to(box.get_center() + RIGHT * 0.95 + UP * 0.55)
        y_lab = name("hidden product", GOLD, 15).next_to(y, RIGHT, buff=0.1)
        self.play(FadeIn(y, scale=0.5), FadeIn(y_lab), run_time=0.5)

        a = Square(side_length=0.28, color=CORAL, fill_opacity=1, fill_color=CORAL).move_to(LEFT * 5.4 + DOWN * 0.1)
        a_lab = name("ask", CORAL, 18).next_to(a, UP, buff=0.1)
        slate = VGroup(*[
            Rectangle(width=0.16, height=0.85, fill_color=CORAL, fill_opacity=0.85, stroke_width=0)
            for _ in range(10)
        ]).arrange(RIGHT, buff=0.05).move_to(LEFT * 5.2 + UP * 1.55)
        slate_lab = name("the ten", CORAL, 18).next_to(slate, UP, buff=0.1)
        msg = RoundedRectangle(
            corner_radius=0.2, width=1.4, height=0.7,
            stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.9, stroke_width=0,
        ).move_to(LEFT * 5.3 + DOWN * 1.85)
        msg_lab = name("titles", TEAL, 18).next_to(msg, DOWN, buff=0.1)
        cap = self.say(None, "They score the list, not the sentence.")
        self.play(
            FadeIn(a), FadeIn(a_lab), FadeIn(slate), FadeIn(slate_lab),
            FadeIn(msg), FadeIn(msg_lab), run_time=0.7,
        )
        self.wait(0.8)

        cap = self.say(cap, "Only the ask enters the simulator.")
        self.play(a.animate.move_to(slit.get_center() + LEFT * 0.05), run_time=0.9)
        self.play(a.animate.move_to(box.get_center() + LEFT * 0.55), run_time=0.6)
        self.play(a.animate.set_opacity(0.35), run_time=0.2)

        wall = box.get_left() + LEFT * 0.15 + UP * 1.35
        self.play(slate.animate.move_to(wall), run_time=0.8)
        self.play(slate.animate.move_to(wall + LEFT * 1.05 + DOWN * 0.15), run_time=0.3)
        scorer = RoundedRectangle(
            corner_radius=0.08, width=2.2, height=0.7,
            stroke_color=GOLD, stroke_width=2, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 1.4 + DOWN * 3.15)
        scorer_lab = name("scorer", GOLD, 14).move_to(scorer.get_center())
        self.play(FadeIn(scorer), FadeIn(scorer_lab), slate.animate.scale(0.55).move_to(scorer.get_center()), run_time=0.9)

        self.play(msg.animate.move_to(box.get_left() + LEFT * 0.2 + DOWN * 1.05), run_time=0.7)
        x = Text("x", font="Georgia", font_size=36, color=CORAL).move_to(msg.get_center())
        self.play(FadeIn(x), FadeOut(msg), run_time=0.4)
        self.play(FadeOut(x), FadeOut(msg_lab), run_time=0.25)

        cap = self.say(cap, "The next user sentence depends on the ask.", size=22)
        self.play(Circumscribe(y, color=GOLD), run_time=1.2)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in [
            box, slit, box_lab, y, y_lab, a, a_lab, slate, slate_lab,
            scorer, scorer_lab, cap,
        ]], run_time=0.4)

    def policies(self):
        # 0:42-1:04  titles vs ask+ranking
        split = Circle(radius=0.55, color=TEAL, stroke_width=3).move_to(LEFT * 0.8)
        split_lab = name("respond()").next_to(split, DOWN, buff=0.18)
        person = DashedVMobject(Circle(radius=1.15, color=TEAL, stroke_width=2), num_dashes=24)
        person.move_to(RIGHT * 4.6 + UP * 2.05)
        person_lab = name("person", TEAL).next_to(person, DOWN, buff=0.12)
        kernel = RoundedRectangle(
            corner_radius=0.12, width=2.8, height=1.6,
            stroke_color=CORAL, stroke_width=3, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 4.6 + DOWN * 2.0)
        kernel_lab = name("scorer", CORAL).next_to(kernel, DOWN, buff=0.12)
        self.play(Create(split), FadeIn(split_lab), FadeIn(person), FadeIn(person_lab),
                  FadeIn(kernel), FadeIn(kernel_lab), run_time=1.1)

        path_m = ArcBetweenPoints(split.get_center(), person.get_center(), angle=-TAU / 7)
        path_m.set_color(TEAL).set_stroke(width=3)
        path_r = ArcBetweenPoints(split.get_center(), kernel.get_center(), angle=TAU / 7)
        path_r.set_color(CORAL).set_stroke(width=3)
        lab_m = name("titles", TEAL, 18).next_to(path_m.point_from_proportion(0.5), UP, buff=0.08)
        lab_r = name("ask + list", CORAL, 18).next_to(path_r.point_from_proportion(0.5), DOWN, buff=0.08)
        cap = self.say(None, "Titles go to a person. The list goes to the scorer.", size=20)
        self.play(Create(path_m), Create(path_r), FadeIn(lab_m), FadeIn(lab_r), run_time=1.1)

        dm = Dot(color=TEAL, radius=0.11).move_to(split.get_center())
        dr = Dot(color=CORAL, radius=0.11).move_to(split.get_center())
        self.add(dm, dr)
        self.play(MoveAlongPath(dm, path_m), MoveAlongPath(dr, path_r), run_time=1.6, rate_func=linear)
        self.play(FadeOut(dm), FadeOut(dr), run_time=0.12)

        cap = self.say(cap, "The evaluator does not read the titles.", size=20)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in [
            split, split_lab, person, person_lab, kernel, kernel_lab,
            path_m, path_r, lab_m, lab_r, cap,
        ]], run_time=0.4)

    def cover(self):
        # 1:04-1:28  other covers the set
        ring = Circle(radius=2.15, color=MUTED, stroke_width=2).move_to(LEFT * 1.3 + UP * 0.15)
        dots = VGroup()
        for i in range(4):
            ang = i * TAU / 4 + TAU / 8
            d = Dot(color=INK, radius=0.16).move_to(
                ring.get_center() + 1.45 * np.array([np.cos(ang), np.sin(ang), 0])
            )
            d.set_z_index(4)
            dots.add(d)
        c_lab = name("four constraints").next_to(ring, UP, buff=0.28)
        well = RoundedRectangle(
            corner_radius=0.1, width=2.0, height=2.4,
            stroke_color=MUTED, stroke_width=2, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 4.4 + UP * 0.1)
        well.set_z_index(1)
        well_lab = name("told us").next_to(well, UP, buff=0.14)
        cap = self.say(None, "Four constraints to disclose.")
        self.play(Create(ring), LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.12),
                  FadeIn(c_lab), FadeIn(well), FadeIn(well_lab), run_time=1.3)

        wedge = Sector(
            radius=2.15, angle=TAU / 8, start_angle=TAU / 8 - TAU / 16,
            color=MUTED, fill_opacity=0.45, stroke_width=0,
        ).shift(ring.get_center())
        cap = self.say(cap, "A named facet is a slice.")
        self.play(FadeIn(wedge), run_time=0.7)
        self.wait(1.0)

        fill = Circle(radius=2.15, color=CORAL, fill_opacity=0.28, stroke_width=0).move_to(ring.get_center())
        cap = self.say(cap, "other covers everything. Two per turn.")
        self.play(FadeOut(wedge), FadeIn(fill), run_time=0.8)

        self.play(
            dots[0].animate.set_color(GOLD).scale(1.3).move_to(well.get_center() + UP * 0.5 + LEFT * 0.35),
            dots[1].animate.set_color(GOLD).scale(1.3).move_to(well.get_center() + UP * 0.5 + RIGHT * 0.35),
            run_time=1.1,
        )
        t1 = name("turn 1", CORAL, 18).next_to(well, DOWN, buff=0.18)
        self.play(FadeIn(t1), run_time=0.25)
        self.wait(1.0)

        self.play(
            dots[2].animate.set_color(GOLD).scale(1.3).move_to(well.get_center() + DOWN * 0.5 + LEFT * 0.35),
            dots[3].animate.set_color(GOLD).scale(1.3).move_to(well.get_center() + DOWN * 0.5 + RIGHT * 0.35),
            run_time=1.1,
        )
        t2 = name("turn 2", CORAL, 18).next_to(well, DOWN, buff=0.18)
        empty = name("nothing left", MUTED, 16).next_to(ring, DOWN, buff=0.2)
        self.bring_to_front(dots)
        self.play(FadeOut(t1), FadeIn(t2), FadeIn(empty), fill.animate.set_opacity(0.08), run_time=0.5)
        cap = self.say(cap, "All four are known by turn three.")
        self.wait(3.2)
        self.play(*[FadeOut(m) for m in [ring, fill, c_lab, well, well_lab, dots, t2, empty, cap]], run_time=0.4)

    def barrier(self):
        # 1:28-1:44  first-passage
        slots = slots_row()
        slots.move_to(UP * 0.35)
        idx = VGroup(*[name(str(i + 1), MUTED, 14).next_to(slots[i], DOWN, buff=0.1) for i in range(10)])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in slots], lag_ratio=0.04), FadeIn(idx), run_time=1.0)

        y = Dot(color=GOLD, radius=0.16).move_to(LEFT * 6.3 + UP * 0.35)
        cap = self.say(None, "If the hidden product is in the ten, the session stops.", size=20)
        self.play(FadeIn(y), run_time=0.35)
        self.play(y.animate.move_to(slots[0].get_center()), run_time=1.1)
        freeze = Rectangle(
            width=slots.width + 0.32, height=slots.height + 0.38,
            stroke_color=GOLD, stroke_width=4, fill_opacity=0,
        ).move_to(slots)
        self.play(Create(freeze), Flash(y, color=GOLD, line_length=0.2), run_time=0.7)
        self.wait(1.2)

        stack1 = VGroup(*[Dot(color=GOLD, radius=0.05) for _ in range(48)])
        stack1.arrange_in_grid(rows=6, cols=8, buff=0.08).next_to(slots[0], UP, buff=0.3)
        n1 = name("most hits, slot 1", GOLD, 15).next_to(stack1, UP, buff=0.12)
        self.play(
            FadeOut(freeze), FadeOut(idx),
            slots.animate.shift(DOWN * 0.45),
            y.animate.shift(DOWN * 0.45),
            FadeIn(stack1), FadeIn(n1),
            run_time=1.2,
        )
        cap = self.say(cap, "Most hits already sit in slot one.")
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in [slots, y, stack1, n1, cap]], run_time=0.35)

    def flock(self):
        # 1:44-2:08  keep / drop / category
        dots = VGroup(*[Dot(color=GOLD, radius=0.045) for _ in range(175)])
        dots.arrange_in_grid(rows=7, cols=25, buff=0.11).move_to(UP * 0.4)
        cap = self.say(None, "Sessions we had already solved.")
        self.play(FadeIn(dots), run_time=1.1)
        self.wait(1.0)

        rng = np.random.default_rng(0)
        jit = [0.05 * rng.standard_normal(3) * np.array([1, 1, 0]) for _ in range(175)]
        self.play(*[dots[i].animate.shift(jit[i]) for i in range(175)], run_time=0.6)
        self.play(*[dots[i].animate.shift(-jit[i]) for i in range(175)], run_time=0.6)
        cap = self.say(cap, "Popularity inside the ten. All stay.")
        self.wait(1.2)

        dying = VGroup(*dots[147:])
        cap = self.say(cap, "A window of 400 dropped 102 to 74. Rejected.", size=20)
        self.play(dying.animate.set_color(CORAL), run_time=0.45)
        self.play(FadeOut(dying), run_time=0.9)
        self.wait(1.3)

        extras = VGroup(*[Dot(color=TEAL, radius=0.05) for _ in range(8)])
        extras.arrange(RIGHT, buff=0.16).move_to(LEFT * 5.4 + DOWN * 2.35)
        token = name("I'm looking for {category}", GOLD, 16).next_to(extras, UP, buff=0.12)
        self.play(FadeIn(token), FadeIn(extras), run_time=0.5)
        dests = [dots.get_right() + RIGHT * 0.28 + DOWN * (i - 3.5) * 0.16 for i in range(8)]
        self.play(*[extras[i].animate.move_to(dests[i]).set_color(GOLD) for i in range(8)], run_time=1.0)
        cap = self.say(cap, "Opening category. 0.875 to 0.915.")
        self.play(FadeOut(token), run_time=0.3)
        self.wait(3.0)
        self.play(FadeOut(dots), FadeOut(extras), FadeOut(cap), run_time=0.35)

    def session(self):
        # 2:08-2:34  one browsing session, three turns
        turn = name("turn 1", INK, 22).to_edge(UP, buff=0.3)
        slots = slots_row().move_to(ORIGIN + DOWN * 0.35)
        ring = Circle(radius=1.35, color=MUTED, stroke_width=2).move_to(LEFT * 5.0 + UP * 0.2)
        cs = VGroup()
        for i in range(4):
            ang = i * TAU / 4 + TAU / 8
            cs.add(Dot(color=INK, radius=0.12).move_to(
                ring.get_center() + 0.85 * np.array([np.cos(ang), np.sin(ang), 0])
            ))
        cs.set_z_index(3)
        clab = name("not yet told").next_to(ring, DOWN, buff=0.16)
        cap = self.say(None, "Turn one. Browsing. No constraints yet.")
        self.play(FadeIn(turn), FadeIn(slots), Create(ring), FadeIn(cs), FadeIn(clab), run_time=1.1)
        self.wait(1.5)

        shown = VGroup(*[Dot(color=TEAL, radius=0.08) for _ in range(10)])
        for i, d in enumerate(shown):
            d.move_to(slots[i].get_center())
        cap = self.say(cap, "We ask other, and we still show ten items.")
        flood = Circle(radius=1.35, color=CORAL, fill_opacity=0.25, stroke_width=0).move_to(ring.get_center())
        well = VGroup()
        self.play(FadeIn(shown), FadeIn(flood), run_time=0.7)
        self.play(
            cs[0].animate.set_color(GOLD).move_to(RIGHT * 5.1 + UP * 0.55),
            cs[1].animate.set_color(GOLD).move_to(RIGHT * 5.6 + UP * 0.55),
            run_time=0.9,
        )
        told = name("told us").move_to(RIGHT * 5.35 + UP * 1.15)
        self.play(FadeIn(told), run_time=0.25)
        self.wait(1.4)

        turn2 = name("turn 2", INK, 22).to_edge(UP, buff=0.3)
        self.play(FadeOut(turn), FadeIn(turn2), run_time=0.35)
        self.play(
            cs[2].animate.set_color(GOLD).move_to(RIGHT * 5.1 + DOWN * 0.15),
            cs[3].animate.set_color(GOLD).move_to(RIGHT * 5.6 + DOWN * 0.15),
            flood.animate.set_opacity(0.06),
            run_time=0.9,
        )
        self.wait(1.3)

        turn3 = name("turn 3", INK, 22).to_edge(UP, buff=0.3)
        y = Dot(color=GOLD, radius=0.14).move_to(slots[0].get_center())
        cap = self.say(cap, "Turn three. The product enters at rank one.")
        y.move_to(slots[0].get_center())
        self.play(FadeOut(turn2), FadeIn(turn3), shown[0].animate.set_opacity(0), FadeIn(y), run_time=0.6)
        freeze = Rectangle(
            width=slots.width + 0.3, height=slots.height + 0.35,
            stroke_color=GOLD, stroke_width=4, fill_opacity=0,
        ).move_to(slots)
        self.play(Create(freeze), Flash(y, color=GOLD, line_length=0.2), run_time=0.7)
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in [
            turn3, slots, ring, cs, clab, shown, flood, told, y, freeze, cap,
        ]], run_time=0.4)

    def column(self):
        # 2:34-2:50  0.842, titles outside
        axis = Line(DOWN * 2.6, UP * 2.8, color=MUTED, stroke_width=2).move_to(LEFT * 0.3)
        top = name("1.0", MUTED, 14).next_to(axis.get_top(), LEFT, buff=0.16)
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
        mark = DashedLine(r_e.get_top() + LEFT * 1.2, r_e.get_top() + RIGHT * 2.6, color=INK, stroke_width=1.5)
        s_lab = name("0.842", INK, 24).next_to(mark, RIGHT, buff=0.12)

        cap = self.say(None, "Unmodified evaluator. Two hundred sessions.")
        self.play(Create(axis), FadeIn(top), run_time=0.35)
        self.play(FadeIn(r_h), FadeIn(lab_h), run_time=0.45)
        self.play(FadeIn(r_m), FadeIn(lab_m), run_time=0.4)
        self.play(FadeIn(r_e), FadeIn(lab_e), FadeIn(mark), FadeIn(s_lab), run_time=0.55)

        outside = DashedVMobject(Circle(radius=0.85, color=TEAL, stroke_width=2), num_dashes=18)
        outside.move_to(LEFT * 4.7 + UP * 0.15)
        mdot = Dot(color=TEAL, radius=0.12).move_to(outside.get_center())
        mlab = name("titles", TEAL, 16).next_to(outside, DOWN, buff=0.14)
        self.play(FadeIn(outside), FadeIn(mdot), FadeIn(mlab), run_time=0.5)
        cap = self.say(cap, "0.842. The message is not in that score.")
        self.play(Rotate(mdot, angle=TAU, about_point=outside.get_center()), run_time=2.0, rate_func=linear)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
