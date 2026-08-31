"""Geometry film. No captions. Offline. No LaTeX.

Render from this folder:
  manim -qm --fps 30 -o architecture.mp4 film.py ArchitectureFilm
"""
from __future__ import annotations

import numpy as np
from manim import *

BG = "#14171B"
INK = "#EDEFF2"
MUTED = "#737D89"
TEAL = "#74B8B0"
CORAL = "#D9647A"
GOLD = "#D9A441"
CARD = "#1B1F25"


def name(text, color=MUTED, size=16):
    return Text(text, font="Consolas", font_size=size, color=color, disable_ligatures=True)


def slots_row(n=10, width=0.62, height=0.95):
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

    def task(self):
        dots = VGroup(*[Dot(radius=0.036, color=MUTED) for _ in range(120)])
        dots.arrange_in_grid(rows=8, cols=15, buff=0.15).move_to(LEFT * 2.4 + UP * 1.15)
        y = dots[67]
        y.set_color(GOLD).scale(1.7).set_z_index(3)
        cat_lab = name("50,000 products").next_to(dots, UP, buff=0.22)
        self.play(FadeIn(dots), FadeIn(cat_lab), run_time=1.1)
        self.play(Indicate(y, color=GOLD, scale_factor=1.5), run_time=0.8)
        self.wait(4.8)

        slots = slots_row().move_to(DOWN * 2.15)
        shown = VGroup(*[
            RoundedRectangle(
                corner_radius=0.04, width=0.38, height=0.55,
                fill_color=TEAL, fill_opacity=0.85, stroke_width=0,
            )
            for _ in range(10)
        ])
        for i, card in enumerate(shown):
            card.move_to(slots[i].get_center())
        lab = name("ten products / turn").next_to(slots, DOWN, buff=0.16)
        self.play(FadeIn(slots), FadeIn(shown), FadeIn(lab), run_time=1.0)
        self.wait(5.4)

        axis = Line(DOWN * 2.4, UP * 2.5, color=MUTED, stroke_width=2).move_to(RIGHT * 5.15)
        b0 = Rectangle(width=0.55, height=0.107 * 4.4, fill_color=MUTED, fill_opacity=1, stroke_width=0)
        b1 = Rectangle(width=0.55, height=0.842 * 4.4, fill_color=CORAL, fill_opacity=1, stroke_width=0)
        base = axis.get_bottom() + LEFT * 0.95
        b0.move_to(base, aligned_edge=DOWN)
        b1.move_to(base + RIGHT * 0.85, aligned_edge=DOWN)
        n0 = name("0.107", MUTED, 13).next_to(b0, DOWN, buff=0.12)
        n1 = name("0.842", CORAL, 15).next_to(b1, DOWN, buff=0.12)
        self.play(FadeIn(axis), FadeIn(b0), FadeIn(b1), FadeIn(n0), FadeIn(n1), run_time=0.9)
        self.wait(5.8)
        self.play(*[FadeOut(m) for m in [dots, cat_lab, slots, shown, lab, axis, b0, b1, n0, n1]], run_time=0.4)

    def slit(self):
        box = RoundedRectangle(
            corner_radius=0.1, width=4.2, height=2.8,
            stroke_color=CORAL, stroke_width=3, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 1.6 + UP * 0.35)
        slit = Rectangle(width=0.2, height=0.5, fill_color=BG, fill_opacity=1, stroke_width=0)
        slit.move_to(box.get_left() + RIGHT * 0.01)
        box_lab = name("simulator").next_to(box, UP, buff=0.18)
        self.play(FadeIn(box), FadeIn(slit), FadeIn(box_lab), run_time=0.8)
        self.wait(3.8)

        a = Square(side_length=0.28, color=CORAL, fill_opacity=1, fill_color=CORAL).move_to(LEFT * 5.5 + UP * 0.35)
        a_lab = name("ask", CORAL, 16).next_to(a, DOWN, buff=0.12)
        slate = VGroup(*[
            Rectangle(width=0.14, height=0.7, fill_color=CORAL, fill_opacity=0.85, stroke_width=0)
            for _ in range(10)
        ]).arrange(RIGHT, buff=0.05).move_to(LEFT * 5.3 + UP * 2.35)
        slate_lab = name("the ten", CORAL, 14).next_to(slate, UP, buff=0.1)
        msg = RoundedRectangle(
            corner_radius=0.16, width=1.4, height=0.55,
            fill_color=TEAL, fill_opacity=0.9, stroke_width=0,
        ).move_to(LEFT * 5.3 + DOWN * 1.85)
        msg_lab = name("sentence", TEAL, 14).next_to(msg, DOWN, buff=0.1)
        self.play(
            FadeIn(a), FadeIn(a_lab), FadeIn(slate), FadeIn(slate_lab),
            FadeIn(msg), FadeIn(msg_lab), run_time=0.7,
        )
        self.play(a.animate.move_to(box.get_center() + LEFT * 0.55), run_time=1.1)
        self.play(a.animate.set_opacity(0.35), FadeOut(a_lab), run_time=0.25)
        self.wait(3.2)

        wall = box.get_left() + LEFT * 0.25 + UP * 1.0
        self.play(slate.animate.move_to(wall), run_time=0.7)
        self.play(slate.animate.shift(LEFT * 0.9 + UP * 0.2), run_time=0.3)
        scorer = RoundedRectangle(
            corner_radius=0.08, width=2.2, height=0.65,
            stroke_color=GOLD, stroke_width=2, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 1.6 + DOWN * 2.55)
        scorer_lab = name("scored", GOLD, 14).move_to(scorer.get_center())
        self.play(FadeIn(scorer), FadeIn(scorer_lab), slate.animate.scale(0.5).move_to(scorer.get_center()), run_time=0.8)
        self.play(FadeOut(slate_lab), run_time=0.15)

        self.play(msg.animate.move_to(box.get_left() + LEFT * 0.35 + DOWN * 0.4), run_time=0.55)
        x = Text("x", font="Georgia", font_size=34, color=CORAL).move_to(msg.get_center())
        self.play(FadeIn(x), FadeOut(msg), FadeOut(msg_lab), run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(x), run_time=0.25)
        self.wait(6.8)
        self.play(*[FadeOut(m) for m in [
            box, slit, box_lab, a, slate, scorer, scorer_lab,
        ]], run_time=0.4)

    def policies(self):
        split = Circle(radius=0.5, color=TEAL, stroke_width=3).move_to(LEFT * 3.2)
        split_lab = name("respond()").next_to(split, DOWN, buff=0.18)

        person = DashedVMobject(Circle(radius=1.05, color=TEAL, stroke_width=2), num_dashes=22)
        person.move_to(RIGHT * 3.6 + UP * 2.15)
        person_lab = name("person", TEAL).next_to(person, UP, buff=0.12)
        examples = VGroup(*[
            Rectangle(width=0.55, height=0.14, fill_color=TEAL, fill_opacity=0.85, stroke_width=0)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.08).move_to(person.get_center())

        kernel = RoundedRectangle(
            corner_radius=0.12, width=2.6, height=1.35,
            stroke_color=CORAL, stroke_width=3, fill_color=CARD, fill_opacity=1,
        ).move_to(RIGHT * 3.6 + DOWN * 2.15)
        kernel_lab = name("scorer", CORAL).next_to(kernel, DOWN, buff=0.12)
        ids = VGroup(*[
            Rectangle(width=0.12, height=0.6, fill_color=CORAL, fill_opacity=0.85, stroke_width=0)
            for _ in range(10)
        ]).arrange(RIGHT, buff=0.04).move_to(kernel.get_center())

        self.play(
            Create(split), FadeIn(split_lab), FadeIn(person), FadeIn(person_lab),
            FadeIn(kernel), FadeIn(kernel_lab), run_time=1.0,
        )
        path_m = ArcBetweenPoints(split.get_right(), person.get_left(), angle=-TAU / 10)
        path_m.set_color(TEAL).set_stroke(width=3)
        path_r = ArcBetweenPoints(split.get_right(), kernel.get_left(), angle=TAU / 10)
        path_r.set_color(CORAL).set_stroke(width=3)
        lab_m = name("sentence", TEAL, 14).next_to(path_m, UP, buff=0.08)
        lab_r = name("ask + ids", CORAL, 14).next_to(path_r, DOWN, buff=0.08)
        self.play(Create(path_m), Create(path_r), FadeIn(lab_m), FadeIn(lab_r), run_time=1.0)
        self.play(FadeIn(examples), FadeIn(ids), run_time=0.6)
        self.wait(8.4)

        self.play(examples.animate.set_opacity(0.12), run_time=0.8)
        self.wait(10.4)
        self.play(*[FadeOut(m) for m in [
            split, split_lab, person, person_lab, examples, kernel, kernel_lab, ids,
            path_m, path_r, lab_m, lab_r,
        ]], run_time=0.4)

    def cover(self):
        ring = Circle(radius=1.7, color=MUTED, stroke_width=2).move_to(LEFT * 3.3 + UP * 0.4)
        dots = VGroup()
        for i in range(4):
            ang = i * TAU / 4 + TAU / 8
            d = Dot(color=INK, radius=0.14).move_to(
                ring.get_center() + 1.05 * np.array([np.cos(ang), np.sin(ang), 0])
            )
            d.set_z_index(4)
            dots.add(d)
        c_lab = name("four facts").next_to(ring, UP, buff=0.24)

        topics = ["color", "size", "brand", "material", "style", "fit", "use", "season", "price", "other"]
        chips = VGroup()
        for t in topics:
            col = CORAL if t == "other" else MUTED
            chip = RoundedRectangle(
                corner_radius=0.06, width=1.5, height=0.36,
                stroke_color=col, stroke_width=1.5, fill_color=CARD, fill_opacity=1,
            )
            lab = name(t, col, 13).move_to(chip.get_center())
            chips.add(VGroup(chip, lab))
        chips.arrange_in_grid(rows=5, cols=2, buff=0.1).move_to(RIGHT * 4.2 + UP * 0.35)

        self.play(Create(ring), FadeIn(dots), FadeIn(c_lab), FadeIn(chips), run_time=1.3)
        self.wait(5.4)

        wedge = Sector(
            radius=1.7, angle=TAU / 10, start_angle=TAU / 8 - TAU / 20,
            color=MUTED, fill_opacity=0.45, stroke_width=0,
        ).shift(ring.get_center())
        self.play(FadeIn(wedge), chips[0][0].animate.set_stroke(GOLD, 3), run_time=0.7)
        self.wait(4.4)

        fill = Circle(radius=1.7, color=CORAL, fill_opacity=0.28, stroke_width=0).move_to(ring.get_center())
        well = RoundedRectangle(
            corner_radius=0.1, width=2.1, height=1.15,
            stroke_color=GOLD, stroke_width=2, fill_color=CARD, fill_opacity=1,
        ).move_to(DOWN * 2.65)
        well.set_z_index(1)
        well_lab = name("handed back", GOLD, 14).next_to(well, UP, buff=0.1)
        self.play(
            FadeOut(wedge), FadeIn(fill),
            chips[-1][0].animate.set_stroke(CORAL, 4),
            FadeIn(well), FadeIn(well_lab),
            run_time=0.8,
        )
        self.play(
            dots[0].animate.set_color(GOLD).scale(1.2).move_to(well.get_center() + LEFT * 0.55),
            dots[1].animate.set_color(GOLD).scale(1.2).move_to(well.get_center() + LEFT * 0.18),
            run_time=1.0,
        )
        self.wait(3.2)
        self.play(
            dots[2].animate.set_color(GOLD).scale(1.2).move_to(well.get_center() + RIGHT * 0.18),
            dots[3].animate.set_color(GOLD).scale(1.2).move_to(well.get_center() + RIGHT * 0.55),
            run_time=1.0,
        )
        self.bring_to_front(dots)
        self.play(fill.animate.set_opacity(0.08), run_time=0.4)
        self.wait(5.8)
        self.play(*[FadeOut(m) for m in [ring, fill, c_lab, dots, chips, well, well_lab]], run_time=0.4)

    def barrier(self):
        slots = slots_row().move_to(ORIGIN)
        idx = VGroup(*[name(str(i + 1), MUTED, 14).next_to(slots[i], DOWN, buff=0.12) for i in range(10)])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in slots], lag_ratio=0.04), FadeIn(idx), run_time=0.9)
        y = Dot(color=GOLD, radius=0.15).move_to(LEFT * 6.2)
        self.play(FadeIn(y), y.animate.move_to(slots[0].get_center()), run_time=1.2)
        freeze = Rectangle(
            width=slots.width + 0.28, height=slots.height + 0.55,
            stroke_color=GOLD, stroke_width=4, fill_opacity=0,
        ).move_to(slots)
        self.play(Create(freeze), Flash(y, color=GOLD, line_length=0.18), run_time=0.6)
        self.wait(4.8)

        n1 = name("review count  →  rank 1", GOLD, 16).next_to(freeze, UP, buff=0.2)
        self.play(FadeIn(n1), run_time=0.4)
        self.wait(5.8)
        self.play(*[FadeOut(m) for m in [slots, idx, y, freeze, n1]], run_time=0.35)

    def flock(self):
        dots = VGroup(*[Dot(color=GOLD, radius=0.042) for _ in range(175)])
        dots.arrange_in_grid(rows=7, cols=25, buff=0.12).move_to(UP * 0.7)
        count = name("175 already solved").next_to(dots, UP, buff=0.28)
        self.play(FadeIn(dots), FadeIn(count), run_time=1.0)
        rng = np.random.default_rng(0)
        jit = [0.04 * rng.standard_normal(3) * np.array([1, 1, 0]) for _ in range(175)]
        self.play(*[dots[i].animate.shift(jit[i]) for i in range(175)], run_time=0.55)
        self.play(*[dots[i].animate.shift(-jit[i]) for i in range(175)], run_time=0.55)
        keep = name("inside the ten: all stay", TEAL, 16).next_to(dots, DOWN, buff=0.35)
        self.play(FadeIn(keep), run_time=0.3)
        self.wait(5.2)

        dying = VGroup(*dots[147:])
        drop = name("window of 400: 102 → 74", CORAL, 16).move_to(keep.get_center())
        self.play(dying.animate.set_color(CORAL), FadeOut(keep), FadeIn(drop), run_time=0.5)
        self.play(FadeOut(dying), run_time=0.8)
        self.wait(6.2)

        extras = VGroup(*[Dot(color=TEAL, radius=0.05) for _ in range(8)])
        extras.arrange(RIGHT, buff=0.18).next_to(dots, DOWN, buff=1.15)
        token = name("opening category  0.875 → 0.915", GOLD, 16).next_to(extras, DOWN, buff=0.18)
        self.play(FadeOut(drop), FadeIn(token), FadeIn(extras), run_time=0.5)
        dests = [dots.get_right() + RIGHT * 0.35 + DOWN * (i - 3.5) * 0.15 for i in range(8)]
        self.play(*[extras[i].animate.move_to(dests[i]).set_color(GOLD) for i in range(8)], run_time=0.9)
        self.wait(5.6)
        self.play(FadeOut(dots), FadeOut(extras), FadeOut(count), FadeOut(token), run_time=0.35)

    def session(self):
        turn = name("turn 1", INK, 22).to_edge(UP, buff=0.28)
        slots = slots_row().scale(0.92).move_to(DOWN * 0.15)
        ring = Circle(radius=1.05, color=MUTED, stroke_width=2).move_to(LEFT * 5.35 + UP * 0.9)
        cs = VGroup()
        for i in range(4):
            ang = i * TAU / 4 + TAU / 8
            cs.add(Dot(color=INK, radius=0.11).move_to(
                ring.get_center() + 0.62 * np.array([np.cos(ang), np.sin(ang), 0])
            ))
        cs.set_z_index(3)
        clab = name("not yet").next_to(ring, DOWN, buff=0.16)
        self.play(FadeIn(turn), FadeIn(slots), Create(ring), FadeIn(cs), FadeIn(clab), run_time=0.9)
        shown = VGroup(*[Dot(color=TEAL, radius=0.07) for _ in range(10)])
        for i, d in enumerate(shown):
            d.move_to(slots[i].get_center())
        flood = Circle(radius=1.05, color=CORAL, fill_opacity=0.25, stroke_width=0).move_to(ring.get_center())
        self.play(FadeIn(shown), FadeIn(flood), run_time=0.6)
        pile = VGroup()
        for i, src in enumerate((cs[0], cs[1])):
            dest = RIGHT * 5.35 + UP * (0.85 - i * 0.4)
            self.play(src.animate.set_color(GOLD).move_to(dest), run_time=0.4)
        told = name("told").move_to(RIGHT * 5.35 + UP * 1.35)
        self.play(FadeIn(told), run_time=0.2)
        self.wait(3.6)

        turn2 = name("turn 2", INK, 22).to_edge(UP, buff=0.28)
        self.play(FadeOut(turn), FadeIn(turn2), run_time=0.3)
        for i, src in enumerate((cs[2], cs[3])):
            dest = RIGHT * 5.35 + DOWN * (0.15 + i * 0.4)
            self.play(src.animate.set_color(GOLD).move_to(dest), run_time=0.35)
        self.play(flood.animate.set_opacity(0.06), run_time=0.3)
        self.wait(2.6)

        turn3 = name("turn 3", INK, 22).to_edge(UP, buff=0.28)
        y = Dot(color=GOLD, radius=0.13)
        y.move_to(slots[0].get_center())
        self.play(FadeOut(turn2), FadeIn(turn3), shown[0].animate.set_opacity(0), FadeIn(y), run_time=0.55)
        freeze = Rectangle(
            width=slots.width + 0.28, height=slots.height + 0.32,
            stroke_color=GOLD, stroke_width=4, fill_opacity=0,
        ).move_to(slots)
        self.play(Create(freeze), Flash(y, color=GOLD, line_length=0.18), run_time=0.55)
        self.wait(5.2)
        self.play(*[FadeOut(m) for m in [
            turn3, slots, ring, cs, clab, shown, flood, told, y, freeze,
        ]], run_time=0.35)

    def column(self):
        axis = Line(DOWN * 2.5, UP * 2.7, color=MUTED, stroke_width=2).move_to(RIGHT * 0.3)
        top = name("1.0", MUTED, 14).next_to(axis.get_top(), LEFT, buff=0.14)
        scale = 5.0
        r_h = Rectangle(width=1.45, height=0.50 * 0.915 * scale, fill_color=TEAL, fill_opacity=0.9, stroke_width=0)
        r_m = Rectangle(width=1.45, height=0.30 * 0.750 * scale, fill_color=GOLD, fill_opacity=0.9, stroke_width=0)
        r_e = Rectangle(width=1.45, height=0.20 * np.clip((11 - 3.02) / 10, 0, 1) * scale, fill_color=CORAL, fill_opacity=0.9, stroke_width=0)
        base = axis.get_bottom() + RIGHT * 0.7
        r_h.move_to(base, aligned_edge=DOWN + LEFT)
        r_m.next_to(r_h, UP, buff=0)
        r_e.next_to(r_m, UP, buff=0)
        lab_h = name("Hit  0.915", TEAL, 16).next_to(r_h, RIGHT, buff=0.2)
        lab_m = name("MRR  0.750", GOLD, 16).next_to(r_m, RIGHT, buff=0.2)
        lab_e = name("Eff  MTTC 3.02", CORAL, 16).next_to(r_e, RIGHT, buff=0.2)
        mark = DashedLine(r_e.get_top() + LEFT * 0.9, r_e.get_top() + RIGHT * 2.4, color=INK, stroke_width=1.5)
        s_lab = name("0.842", INK, 24).next_to(mark, RIGHT, buff=0.12)
        starter = name("starter 0.107", MUTED, 14).next_to(axis.get_bottom(), LEFT, buff=0.2)

        self.play(Create(axis), FadeIn(top), FadeIn(starter), run_time=0.4)
        self.play(FadeIn(r_h), FadeIn(lab_h), FadeIn(r_m), FadeIn(lab_m), FadeIn(r_e), FadeIn(lab_e), run_time=0.8)
        self.play(Create(mark), FadeIn(s_lab), run_time=0.5)

        outside = DashedVMobject(Circle(radius=0.8, color=TEAL, stroke_width=2), num_dashes=18)
        outside.move_to(LEFT * 4.8 + UP * 0.3)
        mdot = Dot(color=TEAL, radius=0.11).move_to(outside.get_center())
        mlab = name("sentence", TEAL, 15).next_to(outside, DOWN, buff=0.16)
        self.play(FadeIn(outside), FadeIn(mdot), FadeIn(mlab), run_time=0.45)
        self.play(Rotate(mdot, angle=TAU, about_point=outside.get_center()), run_time=2.2, rate_func=linear)
        self.wait(7.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
