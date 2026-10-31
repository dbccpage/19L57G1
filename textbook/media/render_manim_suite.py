"""Render 12 <=15-second Manim animations for the Genesis Textbook Wiki.

AuthorityEffect: None. Pedagogical visualizations of the frozen derivation and
post-freeze research extensions. Every animation is strictly <= 15.0 seconds.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from manim import (
    Scene,
    Text,
    VGroup,
    RoundedRectangle,
    Rectangle,
    Circle,
    Arrow,
    Line,
    DashedLine,
    FadeIn,
    FadeOut,
    Succession,
    Write,
    Create,
    Transform,
    Circumscribe,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    config,
)

# Palette
BG_COLOR = "#0B0F19"
CARD_BG = "#131B2E"
GOLD = "#F59E0B"
CYAN = "#38BDF8"
GREEN = "#34D399"
RED = "#F87171"
PURPLE = "#C084FC"
MUTED = "#94A3B8"
WHITE_HEX = "#F8FAFC"


def fitted_text(text: str, width: float, height: float, **kwargs) -> Text:
    """Wrap at word boundaries before fitting text inside its reserved region."""
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}".strip()
            if line and Text(candidate, **kwargs).width > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    result = Text("\n".join(lines), line_spacing=0.8, **kwargs)
    scale = min(1.0, width / max(result.width, 0.001), height / max(result.height, 0.001))
    return result.scale(scale)


def header_banner(act_label: str, title: str, badge: str) -> VGroup:
    bar = RoundedRectangle(
        width=13.2,
        height=0.95,
        corner_radius=0.15,
        stroke_color=CYAN,
        stroke_width=1.5,
        fill_color=CARD_BG,
        fill_opacity=0.95,
    ).to_edge(UP, buff=0.25)
    t_act = fitted_text(act_label, 3.0, 0.60, font_size=18, color=GOLD, weight="BOLD").move_to(
        bar.get_left() + RIGHT * 1.7
    )
    t_title = fitted_text(title, 9.1, 0.38, font_size=22, color=WHITE_HEX, weight="BOLD").move_to(
        bar.get_center() + RIGHT * 1.7 + UP * 0.18
    )
    t_badge = fitted_text(badge, 9.1, 0.22, font_size=12, color=CYAN).move_to(
        bar.get_center() + RIGHT * 1.7 + DOWN * 0.23
    )
    return VGroup(bar, t_act, t_title, t_badge)


def footer_caption(text_str: str, color: str = WHITE_HEX) -> VGroup:
    box = RoundedRectangle(
        width=13.2,
        height=0.8,
        corner_radius=0.12,
        stroke_color=MUTED,
        stroke_width=1.0,
        fill_color=CARD_BG,
        fill_opacity=0.95,
    ).to_edge(DOWN, buff=0.25)
    txt = fitted_text(text_str, 12.6, 0.56, font_size=19, color=color).move_to(box.get_center())
    return VGroup(box, txt)


def make_card(
    title: str,
    subtitle: str,
    width: float = 3.6,
    height: float = 1.6,
    stroke: str = CYAN,
) -> VGroup:
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        stroke_color=stroke,
        stroke_width=2.0,
        fill_color=CARD_BG,
        fill_opacity=0.95,
    )
    t1 = fitted_text(title, width - 0.35, height * 0.36, font_size=22, color=stroke, weight="BOLD").move_to(
        rect.get_center() + UP * height * 0.24
    )
    t2 = fitted_text(subtitle, width - 0.35, height * 0.38, font_size=16, color=WHITE_HEX).move_to(
        rect.get_center() + DOWN * height * 0.22
    )
    return VGroup(rect, t1, t2)


class Act00PreGenesisMark(Scene):
    """Units 00-04 & Start Here: The Mark <>, Pre-Genesis, and Inertia (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT I (U00-U04)",
            "The Opaque Mark <> and Inertia",
            "Status: ADMITTED / DERIVED | AuthorityEffect: None",
        )
        c1 = footer_caption("0:00-0:03 | We begin with one opaque written mark: <>")
        mark_box = RoundedRectangle(
            width=2.8,
            height=1.7,
            corner_radius=0.2,
            stroke_color=GOLD,
            stroke_width=3,
            fill_color=CARD_BG,
            fill_opacity=1.0,
        )
        mark_txt = Text("<>", font_size=56, color=GOLD, weight="BOLD").move_to(
            mark_box.get_center()
        )
        mark_grp = VGroup(mark_box, mark_txt).move_to(ORIGIN + UP * 0.3)

        self.play(FadeIn(hdr), FadeIn(c1), Create(mark_box), Write(mark_txt), run_time=2.2)
        self.wait(0.8)

        # Segment 2 (3-7s): Cross out preconceived notions
        c2 = footer_caption(
            "0:03-0:07 | A mark supplies no sets, numbers, containers, or rules."
        )
        notions = VGroup(
            make_card("Empty Set { }", "NOT inside <>", 3.1, 1.2, MUTED).move_to(
                LEFT * 4.5 + UP * 1.4
            ),
            make_card("Number 0", "NOT inside <>", 3.1, 1.2, MUTED).move_to(
                RIGHT * 4.5 + UP * 1.4
            ),
            make_card("Container [ ]", "NOT inside <>", 3.1, 1.2, MUTED).move_to(
                LEFT * 4.5 + DOWN * 0.8
            ),
            make_card("Identity A=A", "NOT inside <>", 3.1, 1.2, MUTED).move_to(
                RIGHT * 4.5 + DOWN * 0.8
            ),
        )
        strikes = VGroup(
            *[
                Line(
                    n.get_corner( UP + LEFT ) + RIGHT * 0.2 + DOWN * 0.15,
                    n.get_corner( DOWN + RIGHT ) + LEFT * 0.2 + UP * 0.15,
                    color=RED,
                    stroke_width=4,
                )
                for n in notions
            ]
        )
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(notions), run_time=1.5)
        c1 = c2
        self.play(Create(strikes), run_time=1.5)
        self.wait(1.0)

        # Segment 3 (7-11s): Supply changes nothing; Ledger tracks admissions
        c3 = footer_caption(
            "0:07-0:11 | genesis_underivable & supply_no_op: empty ledger derives nothing."
        )
        self.play(FadeOut(notions), FadeOut(strikes), mark_grp.animate.move_to(LEFT * 4.2 + UP * 0.3), Succession(FadeOut(c1), FadeIn(c3)), run_time=1.2)
        c1 = c3
        ledger = make_card(
            "Genesis Ledger",
            "data: 0 | forms: [] | insts: []",
            4.8,
            1.6,
            GREEN,
        ).move_to(RIGHT * 2.2 + UP * 1.1)
        sup = make_card(
            "step(EMPTY, Supply('a'))",
            "Result: EMPTY (no-op without admission)",
            4.8,
            1.4,
            CYAN,
        ).move_to(RIGHT * 2.2 + DOWN * 0.8)
        arr = Arrow(mark_grp.get_right(), ledger.get_left(), buff=0.25, color=GOLD)
        self.play(Create(arr), FadeIn(ledger), FadeIn(sup), run_time=1.8)
        self.wait(1.0)

        # Segment 4 (11-14s): Priced ledger summary
        c4 = footer_caption(
            "0:11-0:14 | Every structure is either ADMITTED at a stated price or DERIVED.",
            GOLD,
        )
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(ledger, color=GOLD), run_time=1.5)
        c1 = c4
        self.wait(1.5)


class Act01TokensErasureCollapse(Scene):
    """Units 05-16: Token Erasure & Observational Collapse (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT II (U05-U16)",
            "Token Erasure & Observational Collapse",
            "Lean: Erasure.erase_replay, Inertia.R2L_collapsed | Status: DERIVED",
        )
        c1 = footer_caption("0:00-0:03 | External tokens <a> and <ab> enter as numbered data 0 and 1.")
        t_box = make_card("Token History", "AdmitDatum('a'), AdmitDatum('ab')", 4.6, 1.5, GOLD).move_to(LEFT * 3.8 + UP * 1.0)
        e_box = make_card("Erased Regime R2L", "n_data = 2 | forms = [] | insts = []", 4.8, 1.5, CYAN).move_to(RIGHT * 3.2 + UP * 1.0)
        arr = Arrow(t_box.get_right(), e_box.get_left(), buff=0.2, color=GOLD)
        lbl = Text("erase_replay", font_size=16, color=GOLD).next_to(arr, UP, buff=0.1)

        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(t_box), run_time=1.8)
        self.play(Create(arr), FadeIn(lbl), FadeIn(e_box), run_time=1.5)

        c2 = footer_caption("0:03-0:07 | A 1-hole context C plugs datum 0 or datum 1 into a relation slot.")
        d0 = make_card("Datum 0", "plug(C, 0) -> False", 3.6, 1.3, PURPLE).move_to(LEFT * 3.2 + DOWN * 0.9)
        d1 = make_card("Datum 1", "plug(C, 1) -> False", 3.6, 1.3, PURPLE).move_to(RIGHT * 3.2 + DOWN * 0.9)
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(d0), FadeIn(d1), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | With zero recorded instances, every context gives the same answer.")
        col_badge = make_card("collapsed(R2L, 0, 1)", "Outside labels differ; inside tests agree", 6.2, 1.3, RED).move_to(ORIGIN + DOWN * 0.9)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeOut(d0), FadeOut(d1), FadeIn(col_badge), run_time=2.0)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Two distinct labels do not automatically create an internal separation.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(col_badge, color=GOLD), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act02SeparationAndMinimality(Scene):
    """Units 17-26: Separation Demand, Cost Minimality & Irreflexivity (12.5s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT III (U17-U26)",
            "Witnessed Separation, Cost Measures & Irreflexivity",
            "Lean: Minimality.cost1_insufficient_general, BL_separable, mu2_unique | Status: DERIVED",
        )
        c1 = footer_caption("0:00-0:03 | Imposing demand (0, 1): can a single item of cost 1 separate them?")
        cost1 = make_card("Cost 1 (mu1 = 1)", "Form alone OR Instance alone -> FAILS", 5.8, 1.4, RED).move_to(UP * 1.2)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(cost1), run_time=2.2)
        self.wait(0.8)

        c2 = footer_caption("0:03-0:07 | Cost 2: add a form and a fact. A context then distinguishes 0 from 1.")
        bl = make_card("Link BL: (0, [0, 1])", "Context [_, 1]: holds on 0, fails on 1", 4.1, 1.4, GREEN).move_to(LEFT * 4.2 + DOWN * 0.5)
        bd = make_card("Loop BD: (0, [0, 0])", "Context [_, 0]: holds on 0, fails on 1", 4.1, 1.4, CYAN).move_to(ORIGIN + DOWN * 0.5)
        u1 = make_card("Unary: (0, [0])", "mu2 = (2, 1): unique minimum in reading L", 4.1, 1.4, GOLD).move_to(RIGHT * 4.2 + DOWN * 0.5)
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(bl), FadeIn(bd), FadeIn(u1), run_time=2.2)
        c1 = c2
        self.wait(1.2)

        c3 = footer_caption("0:07-0:11 | mu1 ties 3 classes (in L); mu2 selects the unary witness uniquely.")
        self.play(Succession(FadeOut(c1), FadeIn(c3)), Circumscribe(u1, color=GOLD), run_time=1.8)
        c1 = c3
        self.wait(1.0)

        c4 = footer_caption("0:11-0:13 | Positive facts alone do not entail a global irreflexivity law.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(bd, color=CYAN), run_time=1.8)
        c1 = c4
        self.wait(1.0)


class Act03QuotientsCountingTransport(Scene):
    """Units 27-36: Quotient Barrier, Round Bound & Renaming Transport (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT IV (U27-U36)",
            "Quotient Barrier, Pair Counting & Renaming Transport",
            "Lean: Quot.quot_barrier, Counting.no_supply_round_bound, RuleBridge | Status: DERIVED",
        )
        c1 = footer_caption("0:00-0:03 | Quot.quot_barrier: an abstraction cannot see differences it merges.")
        q_card = make_card("Quotient Map q(0) = q(1)", "Any test factoring through q collapses 0 and 1", 5.8, 1.4, RED).move_to(UP * 1.2 + LEFT * 3.1)
        r_card = make_card("Fixed Carrier (n data)", "At most n(n-1)/2 unordered pairs", 5.4, 1.4, CYAN).move_to(UP * 1.2 + RIGHT * 3.2)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(q_card), run_time=2.0)

        c2 = footer_caption("0:03-0:07 | Without new supply, strict demand rounds halt within n(n-1)/2 steps.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(r_card), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | Renaming preserves separation. A uniform rule alone distinguishes no data.")
        t_card = make_card("Injective Renaming f", "collapsed_rename: preserves all context verdicts", 5.8, 1.4, GREEN).move_to(DOWN * 0.8 + LEFT * 3.1)
        rb_card = make_card("RuleBridge", "Uniform rule holds on all data -> separates nothing", 5.4, 1.4, GOLD).move_to(DOWN * 0.8 + RIGHT * 3.2)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(t_card), FadeIn(rb_card), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Progress.mark_progress: every valid imposed pair has a finite separating response.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(t_card, color=GREEN), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act04RefusalGeneratorCapacity(Scene):
    """Units 37-43: Refusal Routes, Demand Generator & Pigeonhole Capacity (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT V (U37-U43)",
            "Refusal Rungs, Demand Generator & Capacity Bounds",
            "Lean: Refusal, Generator.finite_marks_outrun, Pigeonhole, G1Class | Status: DERIVED",
        )
        c1 = footer_caption("0:00-0:03 | When a protected law blocks repair on the current carrier: 4 refusal rungs.")
        rungs = VGroup(
            make_card("1. Silent halt", "Carrier fixed, inert", 2.9, 1.3, MUTED),
            make_card("2. Untagged mark", "Merges occurrences", 2.9, 1.3, CYAN),
            make_card("3. Occurrence tag", "Separates steps", 2.9, 1.3, GOLD),
            make_card("4. Tagged translation", "Full witness separation", 3.1, 1.3, GREEN),
        ).arrange(RIGHT, buff=0.25).move_to(UP * 1.1)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(rungs), run_time=2.2)
        self.wait(0.8)

        c2 = footer_caption("0:03-0:07 | Pigeonhole capacity bound: k boolean views yield at most 2^k signatures.")
        cap = make_card("k Views -> 2^k Signatures", "When carrier > 2^k, two distinct points share a signature", 6.2, 1.5, RED).move_to(DOWN * 0.8 + LEFT * 3.0)
        g1 = make_card("G1Class Exclusion", "No bounded local alphabet clears an unbounded demand stream", 5.6, 1.5, PURPLE).move_to(DOWN * 0.8 + RIGHT * 3.2)
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(cap), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | Looking radius-d steps ahead still hits the finite capacity ceiling.")
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(g1), run_time=2.0)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Unbounded separation demands force either carrier growth or refusal.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(g1, color=GOLD), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act05RepresentedKernelHorizon(Scene):
    """Units 44-50: Represented Kernel, Rule 1, NoOutside & Horizon (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT VI (U44-U50)",
            "Represented Kernel, Rule 1 Dichotomy & Every-Stage Horizon",
            "Lean: Completion.rule1_repair_or_extension, NoOutside, Horizon.worldAt_spec | Status: DERIVED",
        )
        c1 = footer_caption("0:00-0:03 | Represented state splits into active support and unindexed notes.")
        st = make_card("Kernel World State", "support (active panel) + notes (unwatched field)", 5.8, 1.4, CYAN).move_to(UP * 1.2 + LEFT * 3.1)
        r1 = make_card("Rule 1 Dichotomy", "In-panel Repair OR Certified Exhaustion + Extension", 5.8, 1.4, GOLD).move_to(UP * 1.2 + RIGHT * 3.1)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(st), run_time=2.0)

        c2 = footer_caption("0:03-0:07 | Rule 1: either a single-column repair clears the obstruction, or extension fires.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(r1), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | NoOutside: negative certification coincides with the panel quotient.")
        no_out = make_card("NoOutside Quotient", "certNeg_iff_panelEquiv (notes invisible until promoted)", 5.8, 1.4, PURPLE).move_to(DOWN * 0.8 + LEFT * 3.1)
        hor = make_card("Horizon (Every Stage n)", "worldAt_spec & worldAt_quiescent proved for all n", 5.8, 1.4, GREEN).move_to(DOWN * 0.8 + RIGHT * 3.1)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(no_out), FadeIn(hor), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Initiality.unique_compliant: 1 of 64 candidate controllers passes all 6 probes.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(hor, color=GREEN), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act06PrimitiveDifferenceApartness(Scene):
    """Units 51-56: 9 Readings of Difference, Initial D2, Passage & Apartness (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT VII (U51-U56)",
            "Nine Readings of Difference, Initial Witness D2 & Apartness",
            "Lean: PrimitiveCore, PrimitiveCats.d2_initial, HigherStructure, Apartness | Status: FROZEN",
        )
        c1 = footer_caption("0:00-0:03 | PrimitiveCore: 9 readings of a difference (17 implications, 51 countermodels).")
        p_core = make_card("9 Readings of Difference", "17 proved implications | 51 separating countermodels", 5.8, 1.4, GOLD).move_to(UP * 1.2 + LEFT * 3.1)
        d2 = make_card("Initial Witness D2", "d2_initial: unique hom into any witnessed pair", 5.8, 1.4, CYAN).move_to(UP * 1.2 + RIGHT * 3.1)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(p_core), run_time=2.0)

        c2 = footer_caption("0:03-0:07 | PrimitiveCats: the 2-point witness D2 is initial, and no terminal object exists.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(d2), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | Apartness: irreflexivity + symmetry + cotransitivity earn equivalence.")
        hs = make_card("HigherStructure Rounds", "First graph supplied; observer created by round closure", 5.8, 1.4, PURPLE).move_to(DOWN * 0.8 + LEFT * 3.1)
        ap = make_card("Apartness -> Sameness", "indist_equivalence requires all 3 apartness laws", 5.8, 1.4, GREEN).move_to(DOWN * 0.8 + RIGHT * 3.1)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(hs), FadeIn(ap), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Dropping cotransitivity breaks transitivity of indistinguishability.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(ap, color=GREEN), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act07InterpreterControllerBoundary(Scene):
    """Units 57-58, 65-66: 13 Codes, Trace Idempotence & Interpreter Boundary (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT VIII (U57-U58, U65-U66)",
            "Effect Classes, Repeated Events & Interpreter Boundary",
            "Lean: InterpreterBoundary.family_missed, TransitionAlphabet, TraceAlgebra | Status: FROZEN / OPEN",
        )
        c1 = footer_caption("0:00-0:03 | Thirteen effect classes summarize individual steps; they are not an event alphabet.")
        codes = make_card("13 One-Step Effect Classes", "A common suffix can distinguish equal class signatures", 6.0, 1.4, CYAN).move_to(UP * 1.2 + LEFT * 3.0)
        alg = make_card("Idempotent Concrete Events", "Repeat the same event: step(step(s, e), e) = step(s, e)", 5.6, 1.4, PURPLE).move_to(UP * 1.2 + RIGHT * 3.2)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(codes), run_time=2.0)

        c2 = footer_caption("0:03-0:07 | Repeating one event adds no effect. Different events can fail to commute.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(alg), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | A notes-diagonal differs from all 64 coded steps; its notes change is inert.")
        ib = make_card("64 Constitution Descriptors", "A fixed interpreter runs this separate finite family", 6.0, 1.4, GOLD).move_to(DOWN * 0.8 + LEFT * 3.0)
        op = make_card("Denotational Bridge: OPEN", "The notes diagonal does not establish an uncoded interpreter's meaning", 5.6, 1.4, RED).move_to(DOWN * 0.8 + RIGHT * 3.2)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(ib), FadeIn(op), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | ControllerCategory: strict controllers agree on the reachable replay orbit.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(op, color=RED), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act08AttachmentLadderCompression(Scene):
    """Units 59-64: Attachment, Boundary d^2=0, Compression & WeightProfile (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT IX (U59-U64)",
            "Carrier Attachment, Boundary d^2 = 0, Compression & Profiles",
            "Lean: Attachment, BoundaryCancellation.d2_zero_unrestricted, Compression | Status: FROZEN",
        )
        c1 = footer_caption("0:00-0:03 | Attachment & GraphGenesis: internal repairs fix the graph; growth is supplied.")
        att = make_card("Attachment & GraphGenesis", "path4 != star4 | Carrier growth requires external supply", 5.8, 1.4, CYAN).move_to(UP * 1.2 + LEFT * 3.1)
        bd2 = make_card("BoundaryCancellation", "d2_zero_unrestricted: opposite signs cancel every codim-2 face", 5.8, 1.4, GREEN).move_to(UP * 1.2 + RIGHT * 3.1)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(att), run_time=2.0)

        c2 = footer_caption("0:03-0:07 | BoundaryCancellation: d^2 = 0 holds unrestrictedly; signless version fails.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(bd2), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | Compression & StableContent: quotient by signature preserves all Q-answers.")
        cmp = make_card("Compression & StableContent", "quotient_coarsest: merges only Q-indistinguishable points", 5.8, 1.4, GOLD).move_to(DOWN * 0.8 + LEFT * 3.1)
        wp = make_card("WeightProfile (No Division)", "Natural-number weights compared by cross-multiplication", 5.8, 1.4, PURPLE).move_to(DOWN * 0.8 + RIGHT * 3.1)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(cmp), FadeIn(wp), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Protected separation persists across replay in the declared passage machine.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(cmp, color=GOLD), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act09DescentRelativityFidelity(Scene):
    """Units 67-74: ObsDescent, ContactKernel, Naturality, Fidelity & Parked Iso (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "ACT X (U67-U74)",
            "Observer Descent, Naturality Obstruction, Fidelity & Canonical Iso",
            "Lean: ObsDescent, ContactKernel, PresentationNaturality, FidelityClosure, IsoBridge | Status: FROZEN",
        )
        c1 = footer_caption("0:00-0:03 | ObsDescent & ContactKernel: views descend iff constant on observer fibers.")
        od = make_card("ObsDescent & ContactKernel", "descend_exists_iff: factors through observer quotient", 5.8, 1.4, CYAN).move_to(UP * 1.2 + LEFT * 3.1)
        pn = make_card("PresentationNaturality & Breaking", "Fixed-point-free swap blocks any equivariant pair choice", 5.8, 1.4, RED).move_to(UP * 1.2 + RIGHT * 3.1)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(od), run_time=2.0)

        c2 = footer_caption("0:03-0:07 | Breaking symmetry: a side can be imposed from outside, not chosen equivariantly.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(pn), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | FidelityClosure & IsoBridge: round-trip coherence and canonical keys.")
        fc = make_card("PresentationRelativity & Fidelity", "Failed factorization forces a joint split; coherent paths", 5.8, 1.4, GOLD).move_to(DOWN * 0.8 + LEFT * 3.1)
        iso = make_card("Parked Iso / Form Family (U74)", "collapsed_transport & iso_of_relabel_eq on ordered reqs", 5.8, 1.4, GREEN).move_to(DOWN * 0.8 + RIGHT * 3.1)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(fc), FadeIn(iso), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Ordered requirements are a hypothesis of the relabel-to-isomorphism bridge.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(iso, color=GREEN), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act10InstitutionsSynergyPolicy(Scene):
    """Part 2 Units 00-11: Actors, Institutions, Synergy, Correspondence & Demurral (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "PART 2 · ACT XI (I00-I11)",
            "Actors, Institutions, Joint Knowledge & Assert-or-Demur Policy",
            "Lean: Inst.exceeds_iff, Correspondence, Policy.demur_carries_witness | Status: POST_FREEZE_PROVED",
        )
        c1 = footer_caption("1 | On inputs [0,1,2], p1=(0,1,0) merges (0,2); p2=(0,1,1) merges (1,2).")
        a1 = make_card("Actor 1: p1 = (0, 1, 0)", "Tells 0!=1, 1!=2 | Merges (0, 2)", 4.1, 1.4, CYAN).move_to(UP * 1.2 + LEFT * 4.2)
        a2 = make_card("Actor 2: p2 = (0, 1, 1)", "Tells 0!=1, 0!=2 | Merges (1, 2)", 4.1, 1.4, PURPLE).move_to(UP * 1.2 + ORIGIN)
        inst = make_card("Institution Q = [p1, p2]", "Signatures: (0,0), (1,1), (0,1) -> All 3 apart!", 4.3, 1.4, GREEN).move_to(UP * 1.2 + RIGHT * 4.2)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(a1), FadeIn(a2), run_time=2.2)

        c2 = footer_caption("2 | Together Q recovers q=(0,0,1). Neither member can recover q alone.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(inst), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("3 | Input alignment is supplied. Under the chosen policy, failed recovery returns demur with a conflict.")
        corr = make_card("Correspondence (I05-I08)", "Re-indexing one actor's data can change what Q knows", 5.8, 1.4, GOLD).move_to(DOWN * 0.8 + LEFT * 3.1)
        pol = make_card("Assert or Demur (I09-I11)", "demur_carries_witness: names exact pair (x, y) merged by Q", 5.8, 1.4, RED).move_to(DOWN * 0.8 + RIGHT * 3.1)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(corr), FadeIn(pol), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("4 | Recoverable does not mean correct. Agreement with a supplied target is a separate check.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(pol, color=GOLD), run_time=1.5)
        c1 = c4
        self.wait(1.0)


class Act11ProbingUncollapseVerdict(Scene):
    """Part 2 Units 12-17: Probing Cost n(n-1)/2, Uncollapse & Verdict Boundary (12.0s)."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR
        hdr = header_banner(
            "PART 2 · ACT XII (I12-I17)",
            "Discovery Tax n(n-1)/2, Uncollapse & Verdict-Level Interpreter",
            "Lean: Acquisition.acquisition_cost_exact, ResearchUncollapse, ResearchInterpreterVerdict | Status: PROVED",
        )
        c1 = footer_caption("0:00-0:03 | Probing an unknown actor on n data: fewer than n(n-1)/2 pair queries misses a pair.")
        prb = make_card("Exact Probe Cost: n(n-1)/2", "Below n(n-1)/2 queries, two different actors share a transcript", 6.0, 1.4, GOLD).move_to(UP * 1.2 + LEFT * 3.0)
        ref = make_card("Promised-Count Refuted (I15)", "At n = N, 'exactly N classes' needs 0 probes (not N-1)", 5.6, 1.4, RED).move_to(UP * 1.2 + RIGHT * 3.2)
        self.play(FadeIn(hdr), FadeIn(c1), FadeIn(prb), run_time=2.0)

        c2 = footer_caption("0:03-0:07 | Once acquired, a k-class partition compresses into ceil(log2 k) binary views.")
        self.play(Succession(FadeOut(c1), FadeIn(c2)), FadeIn(ref), run_time=2.0)
        c1 = c2
        self.wait(1.0)

        c3 = footer_caption("0:07-0:11 | Uncollapse requires a mentioning instance; later admissions can recollapse views.")
        unc = make_card("Uncollapse & Recollapse (I16)", "uncollapse_only_by_mention_delta | recollapse_changes_views", 6.0, 1.4, CYAN).move_to(DOWN * 0.8 + LEFT * 3.0)
        vrd = make_card("Verdict Boundary (I17)", "lawful_unique_at reflective worlds; diagonal escapes iff no code lawful", 5.6, 1.4, GREEN).move_to(DOWN * 0.8 + RIGHT * 3.2)
        self.play(Succession(FadeOut(c1), FadeIn(c3)), FadeIn(unc), FadeIn(vrd), run_time=2.2)
        c1 = c3
        self.wait(1.2)

        c4 = footer_caption("0:11-0:13 | Every claim is paired with its Lean theorem, Python check, and scope boundary.", GOLD)
        self.play(Succession(FadeOut(c1), FadeIn(c4)), Circumscribe(vrd, color=GREEN), run_time=1.5)
        c1 = c4
        self.wait(1.0)


SCENES = [
    ("Act00PreGenesisMark", "act00_pre_genesis_mark"),
    ("Act01TokensErasureCollapse", "act01_tokens_erasure_collapse"),
    ("Act02SeparationAndMinimality", "act02_separation_and_minimality"),
    ("Act03QuotientsCountingTransport", "act03_quotients_counting_transport"),
    ("Act04RefusalGeneratorCapacity", "act04_refusal_generator_capacity"),
    ("Act05RepresentedKernelHorizon", "act05_represented_kernel_horizon"),
    ("Act06PrimitiveDifferenceApartness", "act06_primitive_difference_apartness"),
    ("Act07InterpreterControllerBoundary", "act07_interpreter_controller_boundary"),
    ("Act08AttachmentLadderCompression", "act08_attachment_ladder_compression"),
    ("Act09DescentRelativityFidelity", "act09_descent_relativity_fidelity"),
    ("Act10InstitutionsSynergyPolicy", "act10_institutions_synergy_policy"),
    ("Act11ProbingUncollapseVerdict", "act11_probing_uncollapse_verdict"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts2/manim"))
    parser.add_argument("--work-dir", type=Path, default=Path("artifacts2/manim_build"))
    parser.add_argument("--scene", choices=[slug for _, slug in SCENES], action="append")
    args = parser.parse_args()
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = args.work_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    config.media_dir = str(work_dir)
    config.pixel_width = 960
    config.pixel_height = 540
    config.frame_rate = 15
    config.verbosity = "WARNING"
    config.disable_caching = True

    cls_map = {
        "Act00PreGenesisMark": Act00PreGenesisMark,
        "Act01TokensErasureCollapse": Act01TokensErasureCollapse,
        "Act02SeparationAndMinimality": Act02SeparationAndMinimality,
        "Act03QuotientsCountingTransport": Act03QuotientsCountingTransport,
        "Act04RefusalGeneratorCapacity": Act04RefusalGeneratorCapacity,
        "Act05RepresentedKernelHorizon": Act05RepresentedKernelHorizon,
        "Act06PrimitiveDifferenceApartness": Act06PrimitiveDifferenceApartness,
        "Act07InterpreterControllerBoundary": Act07InterpreterControllerBoundary,
        "Act08AttachmentLadderCompression": Act08AttachmentLadderCompression,
        "Act09DescentRelativityFidelity": Act09DescentRelativityFidelity,
        "Act10InstitutionsSynergyPolicy": Act10InstitutionsSynergyPolicy,
        "Act11ProbingUncollapseVerdict": Act11ProbingUncollapseVerdict,
    }

    for cls_name, slug in SCENES:
        if args.scene and slug not in args.scene:
            continue
        config.output_file = slug
        scene_cls = cls_map[cls_name]
        scene = scene_cls()
        scene.render()

        # Locate rendered mp4
        mp4_candidates = list(work_dir.rglob(f"{slug}.mp4"))
        if not mp4_candidates:
            raise RuntimeError(f"Missing rendered MP4 for {slug}")
        src_mp4 = mp4_candidates[0]
        dst_mp4 = out_dir / f"{slug}.mp4"
        dst_gif = out_dir / f"{slug}.gif"

        # Copy mp4 and generate high-quality palette GIF via ffmpeg
        dst_mp4.write_bytes(src_mp4.read_bytes())
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(dst_mp4),
                "-vf",
                "fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer",
                str(dst_gif),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Verify duration <= 15.0 seconds with ffprobe
        res = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(dst_mp4),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        dur = float(res.stdout.strip())
        assert dur <= 15.0, f"{slug} duration {dur:.2f}s exceeds 15.0s limit!"
        print(f"Rendered {slug}: {dur:.2f}s (<= 15.0s) | MP4: {dst_mp4.stat().st_size // 1024} KB | GIF: {dst_gif.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
