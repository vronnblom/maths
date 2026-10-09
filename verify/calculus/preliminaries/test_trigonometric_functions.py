"""Verification tests for content/calculus/preliminaries/trigonometric-functions.md (calc-trig-functions).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
is derived here from the statements (SymPy's own sin, cos and tan, `solveset` on the stated
interval, `function_range`, `periodicity`), not copied from the page's answers or solutions; the
answers are read with answer(label), as printed on the page.

Identities are checked twice: symbolically (`equal`, which simplifies, and `sp.expand_trig` /
`sp.trigsimp` as a second route), and numerically with `numeric_spot_check` at random reals. A
two-variable identity is spot-checked in t at random points, for each of several random s.

The page's decimal "Check" lines (calculator values to six places) are claims too: each printed
decimal is tested to be the value it approximates, rounded to the places shown.

The tests without @covers at the end check claims that no eg-/exr- label owns: the three results
the page The Limit of a Function relies on (and that their statements match its box
rem-calc-limit-school-facts), the properties of P(t), the identities, the zeros, lem-calc-sin-bounds
(numerically; its proof is the reviewer's), the period, amplitude and phase, and the widget
figure's caption and Try this.

The last section (the second pass) tests what the Author's round added or changed: property 3's
converse through the integer part, every interval obtained by a named order rule, the steps of the
lemma's proof, each new fact of the box rem-calc-trig-functions-school-facts and its uses in the
lemma (on exact grids), def-calc-radian, def-calc-period, the "Why radians" aside and Try this 2.
"""

import json
import random
import re
from pathlib import Path

import mpmath
import pytest
import sympy as sp
from sympy.calculus.util import function_range, periodicity

from mathcheck import ManualAnswer, answer, answer_type, covers, equal, limit_is, numeric_spot_check, s, t, theta, x

REPO = Path(__file__).resolve().parents[3]
PAGE = REPO / "content" / "calculus" / "preliminaries" / "trigonometric-functions.md"
LIMIT_PAGE = REPO / "content" / "calculus" / "limits" / "limit-of-a-function.md"

pi = sp.pi
R = sp.S.Reals
k = sp.Symbol("k", integer=True)        # an integer of either sign
m = sp.Symbol("m", integer=True)
y = sp.Symbol("y", real=True)
REALS = (-50, 50)                       # the interval for numeric spot checks "on random reals"


def deg_to_rad(d):
    """d degrees in radians: a full turn is 360 degrees and 2π radians."""
    return sp.nsimplify(d) * 2 * pi / 360


def rad_to_deg(r):
    return r * 360 / (2 * pi)


def rounds_to(value, printed: str) -> bool:
    """The exact value, rounded to the decimal places of `printed`, is `printed`
    (|value − printed| ≤ half a unit in the last place shown)."""
    places = len(printed.split(".")[1]) if "." in printed else 0
    half = sp.Rational(1, 2) / sp.Integer(10) ** places
    return bool(sp.Abs(sp.N(value, 50) - sp.Rational(printed)) <= half)


def spot2(lhs, rhs, outer=s, inner=t, count=8, seed=0):
    """A two-variable identity at random reals: for each of `count` random values of `outer`,
    numeric_spot_check in `inner`."""
    rng = random.Random(seed)
    for _ in range(count):
        sv = sp.Rational(rng.randint(-50 * 10**6, 50 * 10**6), 10**6)
        assert numeric_spot_check(lhs.subs(outer, sv), rhs.subs(outer, sv), inner, REALS)
    return True


def is_true(rel) -> bool:
    """A comparison of real constants that SymPy decides to be True (False or undecided fails)."""
    return rel is sp.true or bool(rel) is True


# ── Worked examples ───────────────────────────────────────────────────────────


@covers("eg-calc-trig-functions-radians")
def test_eg_calc_trig_functions_radians():
    r = sp.Rational(3, 10)
    th = deg_to_rad(150)
    # Step 1: 1 degree is π/180 radians, and 150 · π/180 = 5π/6.
    assert equal(deg_to_rad(1), pi / 180)
    assert equal(150 * pi / 180, th) and equal(th, 5 * pi / 6)
    # Step 2: the arc r·θ, derived as the fraction θ/(2π) of the circumference 2πr.
    arc = th / (2 * pi) * (2 * pi * r)
    assert equal(r * th, arc) and equal(arc, pi / 4)
    # Step 3: the sector ½ r² θ, derived as the fraction θ/(2π) of the disc's area πr².
    sector = th / (2 * pi) * (pi * r**2)
    assert equal(sp.Rational(1, 2) * r**2 * th, sector)
    assert equal(r**2, sp.Rational(9, 100))
    assert equal(sector, 3 * pi / 80)
    # The boxed decimals: π/4 ≈ 0.785 and 3π/80 ≈ 0.118.
    assert rounds_to(arc, "0.785") and rounds_to(sector, "0.118")
    # Check: 150/360 = 5/12; circumference 0.6π; 5/12 · 0.6π = π/4; disc π · 0.09; 5/12 · 0.09π = 0.0375π.
    assert equal(sp.Rational(150, 360), sp.Rational(5, 12))
    assert equal(2 * pi * r, sp.Rational(6, 10) * pi)
    assert equal(sp.Rational(5, 12) * sp.Rational(6, 10) * pi, pi / 4)
    assert equal(sp.Rational(5, 12) * sp.Rational(9, 100) * pi, sp.Rational(375, 10**4) * pi)
    assert equal(sp.Rational(375, 10**4) * pi, 3 * pi / 80)


@covers("eg-calc-trig-functions-special-values")
def test_eg_calc_trig_functions_special_values():
    c = sp.Symbol("c", real=True)
    # Step 1: cos(π/4) = sin(π/2 − π/4) = sin(π/4); c² + c² = 1 → c² = 1/2; c > 0 → c = √2/2.
    assert equal(sp.cos(pi / 4), sp.sin(pi / 2 - pi / 4)) and equal(sp.sin(pi / 2 - pi / 4), sp.sin(pi / 4))
    assert equal(sp.solveset(2 * c**2 - 1, c, sp.Interval.open(0, sp.oo)), sp.FiniteSet(sp.sqrt(2) / 2))
    assert equal((sp.sqrt(2) / 2) ** 2, sp.Rational(2, 4)) and equal(sp.Rational(2, 4), sp.Rational(1, 2))
    assert equal(sp.cos(pi / 4), sp.sqrt(2) / 2) and equal(sp.sin(pi / 4), sp.sqrt(2) / 2)
    # Step 2: cos(2π/3) = 2c² − 1 with c = cos(π/3), and = cos(π − π/3) = −c; 2c² + c − 1 = (2c − 1)(c + 1).
    c3 = sp.cos(pi / 3)
    assert equal(sp.cos(2 * pi / 3), 2 * c3**2 - 1) and equal(sp.cos(2 * pi / 3), -c3)
    assert equal(2 * c**2 + c - 1, (2 * c - 1) * (c + 1))
    assert equal(sp.solveset(2 * c**2 + c - 1, c, sp.Interval.open(0, sp.oo)), sp.FiniteSet(sp.Rational(1, 2)))
    assert equal(c3, sp.Rational(1, 2))
    assert equal(1 - sp.Rational(1, 4), sp.Rational(3, 4)) and equal(sp.sin(pi / 3) ** 2, sp.Rational(3, 4))
    assert equal(sp.sin(pi / 3), sp.sqrt(3) / 2)
    # Step 3: π/6 = π/2 − π/3, so cos(π/6) = sin(π/3) and sin(π/6) = cos(π/3).
    assert equal(pi / 6, pi / 2 - pi / 3)
    assert equal(sp.cos(pi / 6), sp.sqrt(3) / 2) and equal(sp.sin(pi / 6), sp.Rational(1, 2))
    # The tangents: 1/√3 = √3/3, 1 and √3.
    assert equal(sp.tan(pi / 6), 1 / sp.sqrt(3)) and equal(1 / sp.sqrt(3), sp.sqrt(3) / 3)
    assert equal(sp.tan(pi / 4), 1) and equal(sp.tan(pi / 3), sp.sqrt(3))
    # Check: π/3 ≈ 1.047198, cos 1.047198 ≈ 0.500000; π/4 ≈ 0.785398, sin 0.785398 ≈ 0.707107 ≈ 1.414214/2.
    assert rounds_to(pi / 3, "1.047198") and rounds_to(sp.cos(sp.Rational("1.047198")), "0.500000")
    assert rounds_to(pi / 4, "0.785398") and rounds_to(sp.sin(sp.Rational("0.785398")), "0.707107")
    assert rounds_to(sp.sqrt(2), "1.414214") and rounds_to(sp.Rational("1.414214") / 2, "0.707107")
    assert equal(sp.Rational(1, 4) + sp.Rational(3, 4), 1)
    for tv in (pi / 6, pi / 4, pi / 3):
        assert equal(sp.cos(tv) ** 2 + sp.sin(tv) ** 2, 1)


@covers("eg-calc-trig-functions-other-angles")
def test_eg_calc_trig_functions_other_angles():
    # 1. 5π/6 = π − π/6, sin(5π/6) = sin(π/6) = 1/2 (property 5)
    assert equal(5 * pi / 6, pi - pi / 6)
    assert equal(sp.sin(5 * pi / 6), sp.sin(pi / 6)) and equal(sp.sin(5 * pi / 6), sp.Rational(1, 2))
    # 2. 4π/3 = π/3 + π, cos(4π/3) = −cos(π/3) = −1/2 (property 7)
    assert equal(4 * pi / 3, pi / 3 + pi)
    assert equal(sp.cos(4 * pi / 3), -sp.cos(pi / 3)) and equal(sp.cos(4 * pi / 3), -sp.Rational(1, 2))
    # 3. sin(−π/4) = −sin(π/4), cos(−π/4) = cos(π/4) ≠ 0, tan(−π/4) = −tan(π/4) = −1
    assert equal(sp.sin(-pi / 4), -sp.sin(pi / 4)) and equal(sp.cos(-pi / 4), sp.cos(pi / 4))
    assert not equal(sp.cos(pi / 4), 0)
    assert equal(-sp.sin(pi / 4) / sp.cos(pi / 4), -sp.tan(pi / 4)) and equal(sp.tan(-pi / 4), -1)
    # 4. 17π/6 = 5π/6 + 2π, sin(17π/6) = sin(5π/6) = 1/2
    assert equal(17 * pi / 6, 5 * pi / 6 + 2 * pi)
    assert equal(sp.sin(17 * pi / 6), sp.sin(5 * pi / 6)) and equal(sp.sin(17 * pi / 6), sp.Rational(1, 2))
    # Check: the quadrants. P(5π/6) in the second (x < 0 < y), P(4π/3) in the third (x, y < 0),
    # P(−π/4) in the fourth (x > 0 > y).
    assert is_true(sp.cos(5 * pi / 6) < 0) and is_true(sp.sin(5 * pi / 6) > 0)
    assert is_true(sp.cos(4 * pi / 3) < 0) and is_true(sp.sin(4 * pi / 3) < 0)
    assert is_true(sp.cos(-pi / 4) > 0) and is_true(sp.sin(-pi / 4) < 0)
    # 17π/6 ≈ 8.901179 and sin 8.901179 ≈ 0.500000.
    assert rounds_to(17 * pi / 6, "8.901179") and rounds_to(sp.sin(sp.Rational("8.901179")), "0.500000")


@covers("eg-calc-trig-functions-sign")
def test_eg_calc_trig_functions_sign():
    # The t in (π/2, π) with sin t = 3/5, found by solveset, independently of the page's steps.
    sols = sp.solveset(sp.sin(x) - sp.Rational(3, 5), x, sp.Interval.open(pi / 2, pi))
    assert isinstance(sols, sp.FiniteSet) and len(sols) == 1
    (t0,) = sols
    # Step 1: cos² t = 1 − 9/25 = 16/25.
    assert equal(sp.cos(t0) ** 2, 1 - sp.Rational(9, 25)) and equal(1 - sp.Rational(9, 25), sp.Rational(16, 25))
    # Step 2: u = π − t lies in (0, π/2) for every t in (π/2, π) (the reversed inequalities), and cos t < 0.
    tt = sp.Symbol("t_", real=True)
    assert equal(sp.imageset(sp.Lambda(tt, pi - tt), sp.Interval.open(pi / 2, pi)), sp.Interval.open(0, pi / 2))
    assert equal(sp.cos(pi - t), -sp.cos(t))
    assert is_true(sp.cos(t0) < 0)
    # Steps 3, 4 and the box: cos t = −4/5, tan t = −3/4.
    assert equal(sp.cos(t0), -sp.Rational(4, 5))
    assert equal(sp.tan(t0), -sp.Rational(3, 4))
    assert equal(sp.Rational(3, 5) / (-sp.Rational(4, 5)), -sp.Rational(3, 4))
    # Check: (3/5)² + (−4/5)² = (9 + 16)/25 = 1; t = 2.498092 lies in (π/2, π), sin ≈ 0.600000,
    # cos ≈ −0.800000 (and 2.498092 is t rounded to six places).
    assert equal(sp.Rational(3, 5) ** 2 + sp.Rational(4, 5) ** 2, sp.Rational(9 + 16, 25)) and equal(sp.Rational(25, 25), 1)
    tv = sp.Rational("2.498092")
    assert is_true(pi / 2 < tv) and is_true(tv < pi)
    assert rounds_to(t0, "2.498092")
    assert rounds_to(sp.sin(tv), "0.600000") and rounds_to(sp.cos(tv), "-0.800000")


@covers("eg-calc-trig-functions-addition")
def test_eg_calc_trig_functions_addition():
    # Step 1: π/3 − π/4 = 4π/12 − 3π/12 = π/12
    assert equal(pi / 3 - pi / 4, 4 * pi / 12 - 3 * pi / 12) and equal(4 * pi / 12 - 3 * pi / 12, pi / 12)
    # Step 2: part (a), each displayed line, against SymPy's own cos(π/12).
    line1 = sp.cos(pi / 3) * sp.cos(pi / 4) + sp.sin(pi / 3) * sp.sin(pi / 4)
    line2 = sp.Rational(1, 2) * sp.sqrt(2) / 2 + sp.sqrt(3) / 2 * sp.sqrt(2) / 2
    line3 = (sp.sqrt(2) + sp.sqrt(6)) / 4
    assert equal(sp.cos(pi / 12), line1) and equal(line1, line2) and equal(line2, line3)
    assert equal(sp.cos(pi / 12), line3)
    # √3·√2 = √6
    assert equal(sp.sqrt(3) * sp.sqrt(2), sp.sqrt(6)) and equal(sp.sqrt(6) ** 2, 6)
    # Check: (1.414214 + 2.449490)/4 ≈ 0.965926; π/12 ≈ 0.261799; cos 0.261799 ≈ 0.965926.
    assert rounds_to(sp.sqrt(6), "2.449490")
    assert rounds_to((sp.Rational("1.414214") + sp.Rational("2.449490")) / 4, "0.965926")
    assert rounds_to(pi / 12, "0.261799") and rounds_to(sp.cos(sp.Rational("0.261799")), "0.965926")
    assert rounds_to(line3, "0.965926")


@covers("eg-calc-trig-functions-ferris-wheel")
def test_eg_calc_trig_functions_ferris_wheel():
    tm = sp.Symbol("t", nonnegative=True)               # minutes
    # Derived independently: the seat starts at the bottom of a circle of radius 20 about (0, 22),
    # i.e. at angle −π/2, and turns anticlockwise at 2π per 10 minutes: height 22 + 20 sin(−π/2 + 2πt/10).
    height = 22 + 20 * sp.sin(-pi / 2 + 2 * pi * tm / 10)
    # Step 1: 2πt/10 = πt/5.
    assert equal(2 * pi * tm / 10, pi * tm / 5)
    # Step 2: the start P(−π/2) = (0, −1).
    assert equal(sp.cos(-pi / 2), 0) and equal(sp.sin(-pi / 2), -1)
    # Step 3: sin(θ − π/2) = −sin(π/2 − θ) = −cos θ, and h(t) = 22 − 20 cos(πt/5).
    assert equal(sp.sin(theta - pi / 2), -sp.sin(pi / 2 - theta)) and equal(-sp.sin(pi / 2 - theta), -sp.cos(theta))
    assert numeric_spot_check(sp.sin(theta - pi / 2), -sp.cos(theta), theta, REALS)
    h = 22 - 20 * sp.cos(pi * tm / 5)
    assert equal(height, h)
    # Step 4: πt/5 − π/2 = (π/5)(t − 5/2); h = 20 sin((π/5)(t − 5/2)) + 22; amplitude 20, period
    # 2π/(π/5) = 10, phase 5/2, midline 22; heights fill [2, 42].
    assert equal(pi * tm / 5 - pi / 2, pi / 5 * (tm - sp.Rational(5, 2)))
    assert equal(h, 20 * sp.sin(pi / 5 * (tm - sp.Rational(5, 2))) + 22)
    xr = sp.Symbol("x", real=True)
    hx = h.subs(tm, xr)
    assert equal(periodicity(hx, xr), 10) and equal(2 * pi / (pi / 5), 10)
    assert equal(function_range(hx, xr, R), sp.Interval(2, 42))
    assert equal(sp.Interval(22 - 20, 22 + 20), sp.Interval(2, 42))
    # Step 5: 100 seconds = 5/3 minutes; (π/5)(5/3) = π/3; h(5/3) = 12; cos 5π = −1; h(25) = 42.
    assert equal(sp.Rational(100, 60), sp.Rational(5, 3))
    assert equal(pi / 5 * sp.Rational(5, 3), pi / 3)
    assert equal(h.subs(tm, sp.Rational(5, 3)), 12) and equal(height.subs(tm, sp.Rational(5, 3)), 12)
    assert equal(sp.cos(5 * pi), sp.cos(pi + 4 * pi)) and equal(sp.cos(5 * pi), -1)
    assert equal(h.subs(tm, 25), 42) and equal(height.subs(tm, 25), 42)
    # Check: h(0) = 2, h(10) = 2, h(5) = 42.
    assert equal(h.subs(tm, 0), 2) and equal(h.subs(tm, 10), 2) and equal(h.subs(tm, 5), 42)
    # "Why this matters": between 2 and 42 metres, repeating every 10 minutes (done above).


# ── Exercises ─────────────────────────────────────────────────────────────────


@covers("exr-calc-trig-functions-degrees-to-radians")
def test_exr_calc_trig_functions_degrees_to_radians():
    a, b = answer("exr-calc-trig-functions-degrees-to-radians")
    assert equal(a, deg_to_rad(210))
    assert equal(b, rad_to_deg(3 * pi / 4))
    # Round trips, as a second route.
    assert equal(rad_to_deg(a), 210) and equal(deg_to_rad(b), 3 * pi / 4)


@covers("exr-calc-trig-functions-arc-length")
def test_exr_calc_trig_functions_arc_length():
    got = answer("exr-calc-trig-functions-arc-length")
    r, th = sp.Rational(8, 10), sp.Rational(3, 10)
    # The arc is the fraction θ/(2π) of the circumference 2πr.
    assert equal(got, th / (2 * pi) * 2 * pi * r)
    # Arc length as an integral of the speed of φ ↦ r(cos φ, sin φ) over [0, θ], a second route.
    phi = sp.Symbol("phi", real=True)
    speed = sp.sqrt(sp.diff(r * sp.cos(phi), phi) ** 2 + sp.diff(r * sp.sin(phi), phi) ** 2)
    assert equal(got, sp.integrate(sp.trigsimp(speed), (phi, 0, th)))


@covers("exr-calc-trig-functions-multiples-of-pi")
def test_exr_calc_trig_functions_multiples_of_pi():
    a, b, c = answer("exr-calc-trig-functions-multiples-of-pi")
    assert equal(a, sp.sin(2026 * pi))
    assert equal(b, sp.sin(-7 * pi / 2))
    assert equal(c, sp.cos(5 * pi))
    # As instances of the propositions: k = 2026; −7π/2 = π/2 + 2(−2)π; 5π = π + 2·2π.
    assert equal(sp.sin(k * pi).subs(k, 2026), a)
    assert equal(-7 * pi / 2, pi / 2 + 2 * (-2) * pi) and equal(sp.sin(pi / 2 + 2 * k * pi).subs(k, -2), b)
    assert equal(5 * pi, pi + 2 * 2 * pi) and equal(sp.cos(pi), c)


@covers("exr-calc-trig-functions-exact-values")
def test_exr_calc_trig_functions_exact_values():
    a, b, c = answer("exr-calc-trig-functions-exact-values")
    assert equal(a, sp.cos(5 * pi / 6))
    assert equal(b, sp.sin(5 * pi / 4))
    assert equal(c, sp.tan(2 * pi / 3))
    # Second route: numerically at 30 digits.
    for got, exact in ((a, sp.cos(5 * pi / 6)), (b, sp.sin(5 * pi / 4)), (c, sp.tan(2 * pi / 3))):
        assert abs(sp.N(got - exact, 30)) < sp.Float("1e-25")


@covers("exr-calc-trig-functions-from-cosine")
def test_exr_calc_trig_functions_from_cosine():
    a, b = answer("exr-calc-trig-functions-from-cosine")
    sols = sp.solveset(sp.cos(x) + sp.Rational(5, 13), x, sp.Interval.open(pi, 3 * pi / 2))
    assert isinstance(sols, sp.FiniteSet) and len(sols) == 1
    (t0,) = sols
    assert equal(a, sp.sin(t0))
    assert equal(b, sp.tan(t0))
    # Second route: sin² = 1 − cos² and the sign of sin on (π, 3π/2).
    assert equal(a**2, 1 - sp.Rational(5, 13) ** 2)
    assert equal(function_range(sp.sin(x), x, sp.Interval.open(pi, 3 * pi / 2)), sp.Interval.open(-1, 0))
    assert is_true(a < 0)
    assert equal(b, a / (-sp.Rational(5, 13)))


@covers("exr-calc-trig-functions-addition")
def test_exr_calc_trig_functions_addition():
    got = answer("exr-calc-trig-functions-addition")
    assert equal(got, sp.sin(5 * pi / 12))
    # The solution's route: π/4 + π/6 = 5π/12 and part (c); and sin(5π/12) = cos(π/12) (property 6).
    assert equal(pi / 4 + pi / 6, 5 * pi / 12)
    assert equal(got, sp.sin(pi / 4) * sp.cos(pi / 6) + sp.cos(pi / 4) * sp.sin(pi / 6))
    assert equal(sp.sin(5 * pi / 12), sp.cos(pi / 2 - 5 * pi / 12)) and equal(pi / 2 - 5 * pi / 12, pi / 12)
    assert abs(sp.N(got - sp.sin(5 * pi / 12), 30)) < sp.Float("1e-25")


@covers("exr-calc-trig-functions-solve-sine")
def test_exr_calc_trig_functions_solve_sine():
    got = answer("exr-calc-trig-functions-solve-sine")
    assert answer_type("exr-calc-trig-functions-solve-sine") == "set"
    expected = sp.solveset(sp.sin(x) + sp.Rational(1, 2), x, sp.Interval.Ropen(0, 2 * pi))
    assert equal(got, expected)
    # Second route: each answer solves the equation and lies in [0, 2π), and there are exactly two
    # points of the circle with y = −1/2 (x² = 3/4).
    assert isinstance(got, sp.FiniteSet) and len(got) == 2
    for v in got:
        assert equal(sp.sin(v), -sp.Rational(1, 2)) and is_true(0 <= v) and is_true(v < 2 * pi)
    assert equal(sp.solveset(y**2 - (1 - sp.Rational(1, 4)), y, R), sp.FiniteSet(sp.sqrt(3) / 2, -sp.sqrt(3) / 2))
    # The solution's points: P(7π/6) = (−√3/2, −1/2), P(11π/6) = (√3/2, −1/2) = P(−π/6).
    assert equal((sp.cos(7 * pi / 6), sp.sin(7 * pi / 6)), (-sp.sqrt(3) / 2, -sp.Rational(1, 2)))
    assert equal((sp.cos(11 * pi / 6), sp.sin(11 * pi / 6)), (sp.sqrt(3) / 2, -sp.Rational(1, 2)))
    assert equal(-pi / 6 + 2 * pi, 11 * pi / 6) and equal(pi / 6 + pi, 7 * pi / 6)


@covers("exr-calc-trig-functions-widget-wave")
def test_exr_calc_trig_functions_widget_wave():
    a, b = answer("exr-calc-trig-functions-widget-wave")
    f = 2 * sp.sin(3 * x) + 1
    assert equal(a, sp.Max(*function_range(f, x, R).boundary))
    assert equal(function_range(f, x, R), sp.Interval(-1, 3))
    assert equal(b, periodicity(f, x))
    # Second route for the period: 2π/|b| with b = 3, and f(x + p) = f(x) symbolically.
    assert equal(b, 2 * pi / 3)
    assert equal(f.subs(x, x + b), f)
    # The solution: f(π/6) = 3; 2π/3 ≈ 2.09; three waves on [0, 2π]; the widget's wave between −1 and 3.
    assert equal(f.subs(x, pi / 6), 3)
    assert rounds_to(2 * pi / 3, "2.09")
    assert equal(2 * pi / b, 3)
    # The sliders can be set to a = 2, b = 3, c = 0, d = 1 (each on its slider's grid).
    params = widget_config()["parameters"]
    for name, value in (("a", 2), ("b", 3), ("c", 0), ("d", 1)):
        assert on_grid(params[name], value)


@covers("exr-calc-trig-functions-ferris-times")
def test_exr_calc_trig_functions_ferris_times():
    a, b = answer("exr-calc-trig-functions-ferris-times")
    h = 22 - 20 * sp.cos(pi * x / 5)
    sols = sp.solveset(h - 32, x, sp.Interval.Ropen(0, 10))
    assert isinstance(sols, sp.FiniteSet) and len(sols) == 2
    earlier, later = sorted(sols, key=lambda v: float(v))
    assert equal(a, earlier) and equal(b, later)
    # Second route: h at the answers, and the solution's steps (cos u = −1/2 for u in [0, 2π)).
    assert equal(h.subs(x, a), 32) and equal(h.subs(x, b), 32)
    assert equal(sp.solveset(sp.cos(x) + sp.Rational(1, 2), x, sp.Interval.Ropen(0, 2 * pi)),
                 sp.FiniteSet(2 * pi / 3, 4 * pi / 3))
    assert equal(5 * (2 * pi / 3) / pi, a) and equal(5 * (4 * pi / 3) / pi, b)
    # "after 3 1/3 minutes on the way up and after 6 2/3 minutes on the way down"
    assert equal(a, 3 + sp.Rational(1, 3)) and equal(b, 6 + sp.Rational(2, 3))
    assert is_true(sp.diff(h, x).subs(x, a) > 0) and is_true(sp.diff(h, x).subs(x, b) < 0)


@covers("exr-calc-trig-functions-cos-decreasing")
def test_exr_calc_trig_functions_cos_decreasing():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-trig-functions-cos-decreasing")
    u, v = sp.symbols("u v", real=True)
    md, dd = sp.symbols("m d", real=True)
    # v = m − d and u = m + d for m = (u + v)/2, d = (u − v)/2.
    assert equal(((u + v) / 2 - (u - v) / 2, (u + v) / 2 + (u - v) / 2), (v, u))
    # cos(m − d) − cos(m + d) = 2 sin m sin d (by parts (a) and (b)), symbolically and numerically.
    lhs, rhs = sp.cos(md - dd) - sp.cos(md + dd), 2 * sp.sin(md) * sp.sin(dd)
    assert equal(lhs, rhs) and equal(sp.expand_trig(lhs), rhs)
    assert spot2(lhs, rhs, outer=md, inner=dd)
    # The answer line: cos v − cos u = 2 sin((u + v)/2) sin((u − v)/2).
    assert equal(sp.cos(v) - sp.cos(u), 2 * sp.sin((u + v) / 2) * sp.sin((u - v) / 2))
    # For 0 ≤ v < u ≤ π: 0 < m < π and 0 < d ≤ π/2, so both sines are positive (property 8),
    # checked on exact pairs including both endpoints.
    assert equal(function_range(sp.sin(x), x, sp.Interval.open(0, pi)), sp.Interval.Lopen(0, 1))
    rng = random.Random(8)
    grid = [sp.Integer(0), pi] + [pi * sp.Rational(rng.randint(0, 10**6), 10**6) for _ in range(60)]
    for vv in grid:
        for uu in grid:
            if not is_true(vv < uu):
                continue
            mm, dv = (uu + vv) / 2, (uu - vv) / 2
            assert is_true(0 < mm) and is_true(mm < pi) and is_true(0 < dv) and is_true(dv <= pi / 2)
            assert is_true(sp.cos(vv) - sp.cos(uu) > 0)
    # SymPy's is_strictly_decreasing(cos, [0, π]) answers False (it asks for cos′ < 0, and
    # cos′ = −sin is 0 at both ends), so we cross-check on the open interval and the endpoints
    # separately instead: strictly decreasing on (0, π), with cos 0 = 1 above and cos π = −1 below
    # every value there.
    assert sp.is_strictly_decreasing(sp.cos(x), sp.Interval.open(0, pi))
    assert equal(function_range(sp.cos(x), x, sp.Interval.open(0, pi)), sp.Interval.open(-1, 1))
    assert equal(sp.cos(0), 1) and equal(sp.cos(pi), -1)


@covers("exr-calc-trig-functions-tan-period")
def test_exr_calc_trig_functions_tan_period():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-trig-functions-tan-period")
    # tan(t + π) = (−sin t)/(−cos t) = tan t, and cos(t + π) = −cos t (so the domain is kept).
    assert equal(sp.sin(t + pi), -sp.sin(t)) and equal(sp.cos(t + pi), -sp.cos(t))
    assert equal(sp.tan(t + pi), sp.tan(t))
    assert numeric_spot_check(sp.tan(t + pi), sp.tan(t), t, REALS)
    # The smallest period is π (SymPy's periodicity).
    assert equal(periodicity(sp.tan(x), x), pi)
    # tan p = tan 0 = 0 with cos p ≠ 0 forces sin p = 0; the zeros of tan on (0, π] are only π itself.
    assert equal(sp.tan(0), 0) and equal(sp.cos(0), 1)
    assert equal(sp.solveset(sp.tan(x), x, sp.Interval.Lopen(0, pi)), sp.FiniteSet(pi))
    assert equal(sp.solveset(sp.sin(x), x, sp.Interval.open(0, pi)), sp.S.EmptySet)


@covers("exr-calc-trig-functions-sin-over-theta")
def test_exr_calc_trig_functions_sin_over_theta():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-trig-functions-sin-over-theta")
    # Multiplying sin θ < θ by 1/θ and θ < sin θ / cos θ by cos θ/θ (both positive on (0, π/2)).
    assert equal(sp.sin(theta) / theta, sp.sin(theta) * (1 / theta))
    assert equal(sp.sin(theta) / sp.cos(theta) * (sp.cos(theta) / theta), sp.sin(theta) / theta)
    # For θ < 0: sin θ / θ and cos θ are unchanged by θ → −θ.
    assert equal((sp.sin(theta) / theta).subs(theta, -theta), sp.sin(theta) / theta)
    assert equal(sp.cos(-theta), sp.cos(theta))
    # The claim cos θ < sin θ/θ < 1 at many points of (0, π/2) and (−π/2, 0), at 60 digits, close to
    # 0 and to ±π/2 too.
    with mpmath.workdps(60):
        half = mpmath.pi / 2
        rng = random.Random(11)
        pts = [half * mpmath.mpf(rng.uniform(0.0005, 0.9995)) for _ in range(2000)]
        pts += [mpmath.mpf(10) ** -j for j in range(1, 20)] + [half - mpmath.mpf(10) ** -j for j in range(1, 20)]
        for p in pts:
            for q in (p, -p):
                ratio = mpmath.sin(q) / q
                assert mpmath.cos(q) < ratio < 1, q
    # And at exact points: π/6, π/4, π/3 and their negatives.
    for tv in (pi / 6, pi / 4, pi / 3, -pi / 6, -pi / 4, -pi / 3):
        assert is_true(sp.cos(tv) < sp.sin(tv) / tv) and is_true(sp.sin(tv) / tv < 1)
    # The squeeze it prepares (Where this leads): sin θ / θ → 1 as θ → 0.
    assert limit_is(sp.sin(theta) / theta, theta, 0, 1)


# ── Claims no eg-/exr- label owns ─────────────────────────────────────────────


def test_three_results_calc_limit_relies_on():
    # prop-calc-sin-bounded: −1 ≤ sin t ≤ 1 (and the same for cos) for real t: the range over ℝ.
    assert equal(function_range(sp.sin(t), t, R), sp.Interval(-1, 1))
    assert equal(function_range(sp.cos(t), t, R), sp.Interval(-1, 1))
    # Second route: from the Pythagorean identity, sin² t = 1 − cos² t ≤ 1, and |u| ≤ 1 iff u² ≤ 1.
    assert equal(sp.sin(t) ** 2, 1 - sp.cos(t) ** 2)
    assert equal(sp.solveset(y**2 <= 1, y, R), sp.Interval(-1, 1))
    # prop-calc-sin-multiples-of-pi: sin(kπ) = 0 for every integer k (k of either sign).
    assert equal(sp.sin(k * pi), 0)
    # Second route: k = 2m or k = 2m + 1, as in the proof.
    assert equal(sp.sin(2 * m * pi), 0) and equal(sp.sin((2 * m + 1) * pi), 0)
    assert equal(sp.cos(2 * m * pi), 1) and equal(sp.cos((2 * m + 1) * pi), -1)
    for kv in range(-25, 26):
        assert equal(sp.sin(kv * pi), 0)
    # prop-calc-sin-maxima: sin(π/2 + 2kπ) = 1 for every integer k.
    assert equal(sp.sin(pi / 2 + 2 * k * pi), 1)
    assert equal(sp.cos(pi / 2 + 2 * k * pi), 0)
    for kv in range(-25, 26):
        assert equal(sp.sin(pi / 2 + 2 * kv * pi), 1)
    # A real-but-not-integer k breaks both (so "integer" is needed): k = 1/2.
    assert not equal(sp.sin(sp.Rational(1, 2) * pi), 0)
    assert not equal(sp.sin(pi / 2 + 2 * sp.Rational(1, 4) * pi), 1)
    # "These are maxima": 1 is the largest value of sin.
    assert equal(sp.Max(*function_range(sp.sin(t), t, R).boundary), 1)


def _math_spans(text: str) -> list[str]:
    """The inline math of `text`, normalised: \\bigl/\\bigr and spacing dropped."""
    spans = re.findall(r"\$([^$]+)\$", text)
    return [re.sub(r"\s+", "", re.sub(r"\\big[lr]", "", s_)) for s_ in spans]


def _block(text: str, label: str) -> str:
    start = text.index(f":label: {label}")
    return text[start:text.index("\n:::", start)]


def test_statements_match_calc_limit_school_facts():
    # The box rem-calc-limit-school-facts on the page The Limit of a Function lists the three facts
    # that page takes from school; this page proves them. Same mathematics, same quantifiers.
    box = _block(LIMIT_PAGE.read_text(encoding="utf-8"), "rem-calc-limit-school-facts")
    bullets = [line[2:] for line in box.splitlines() if line.startswith("- ")]
    assert len(bullets) == 3
    assert "With $t$ in radians" in box
    page = PAGE.read_text(encoding="utf-8")
    bounded = _block(page, "prop-calc-sin-bounded")
    multiples = _block(page, "prop-calc-sin-multiples-of-pi")
    maxima = _block(page, "prop-calc-sin-maxima")
    # Box: "$\sin(k\pi) = 0$ for every integer $k$" ↔ "For every integer $k$, $\sin(k\pi) = 0$."
    assert _math_spans(bullets[0]) == [r"\sin(k\pi)=0", "k"]
    assert _math_spans(multiples) == ["k", r"\sin(k\pi)=0"]
    assert "every integer $k$" in bullets[0] and "For every integer $k$" in multiples
    # Box: "$\sin(π/2 + 2kπ) = 1$ for every integer $k$" ↔ "For every integer $k$, $\sin(π/2 + 2kπ) = 1$."
    assert _math_spans(bullets[1]) == [r"\sin(\frac{\pi}{2}+2k\pi)=1", "k"]
    assert _math_spans(maxima) == ["k", r"\sin(\frac{\pi}{2}+2k\pi)=1"]
    assert "every integer $k$" in bullets[1] and "For every integer $k$" in maxima
    # Box: "$-1 \le \sin t \le 1$ for every real number $t$" ↔ part (a) of "For every real number $t$".
    assert _math_spans(bullets[2]) == [r"-1\le\sint\le1", "t"]
    assert r"-1\le\sint\le1" in _math_spans(bounded)
    assert "every real number $t$" in bullets[2] and "For every real number $t$" in bounded
    # This page measures t in radians throughout (def-calc-sin-cos: t is a distance along the circle).
    assert "$t$ is always in radians" in page


def test_circle_properties():
    # rem-calc-trig-functions-circle-properties, each property symbolically (t, α real; k integer)
    # and numerically at random reals.
    al = sp.Symbol("alpha", real=True)
    P = lambda v: (sp.cos(v), sp.sin(v))  # noqa: E731
    # 1. P(0), P(π/2), P(π), P(3π/2)
    assert equal(P(0), (1, 0)) and equal(P(pi / 2), (0, 1)) and equal(P(pi), (-1, 0)) and equal(P(3 * pi / 2), (0, -1))
    # 2. The rotation by α (the rotation mapping A to P(α)) maps P(t) to P(t + α).
    rot = sp.Matrix([[sp.cos(al), -sp.sin(al)], [sp.sin(al), sp.cos(al)]])
    assert equal(tuple(rot * sp.Matrix([1, 0])), P(al))
    image = rot * sp.Matrix(P(t))
    assert equal(tuple(image), P(t + al))
    assert spot2(image[0], sp.cos(t + al), outer=al) and spot2(image[1], sp.sin(t + al), outer=al)
    # 3. P(t + 2kπ) = P(t); conversely P(s) = P(t) only when s − t ∈ 2πℤ (the zeros on one turn).
    assert equal(P(t + 2 * k * pi), P(t))
    assert equal(sp.solveset(sp.cos(x) - 1, x, sp.Interval.Ropen(0, 2 * pi)), sp.FiniteSet(0))
    assert equal(periodicity(sp.sin(x), x), 2 * pi) and equal(periodicity(sp.cos(x), x), 2 * pi)
    # 4.–7.
    for lhs, rhs in ((sp.cos(-t), sp.cos(t)), (sp.sin(-t), -sp.sin(t)),
                     (sp.cos(pi - t), -sp.cos(t)), (sp.sin(pi - t), sp.sin(t)),
                     (sp.cos(pi / 2 - t), sp.sin(t)), (sp.sin(pi / 2 - t), sp.cos(t)),
                     (sp.cos(t + pi), -sp.cos(t)), (sp.sin(t + pi), -sp.sin(t))):
        assert equal(lhs, rhs) and numeric_spot_check(lhs, rhs, t, REALS)
    # 7's reason: t + π = π − (−t).
    assert equal(t + pi, pi - (-t))
    # 8. Signs: cos, sin > 0 on (0, π/2); sin > 0 on (0, π).
    assert equal(function_range(sp.cos(x), x, sp.Interval.open(0, pi / 2)), sp.Interval.open(0, 1))
    assert equal(function_range(sp.sin(x), x, sp.Interval.open(0, pi / 2)), sp.Interval.open(0, 1))
    assert equal(function_range(sp.sin(x), x, sp.Interval.open(0, pi)), sp.Interval.Lopen(0, 1))
    # The reflections of the reasons: (x, y) → (x, −y), (−x, y), (y, x) map P(t) to P(−t), P(π − t), P(π/2 − t).
    assert equal((sp.cos(t), -sp.sin(t)), P(-t))
    assert equal((-sp.cos(t), sp.sin(t)), P(pi - t))
    assert equal((sp.sin(t), sp.cos(t)), P(pi / 2 - t))


def test_definitions_examples_and_radians():
    # Radian examples: full turn 2π, straight angle π, right angle π/2; 1° = 2π/360 = π/180;
    # 60° = 60π/180 = π/3; θ radians = 180θ/π degrees; 1 radian = 180/π ≈ 57.3 degrees.
    assert equal(deg_to_rad(360), 2 * pi) and equal(deg_to_rad(180), pi) and equal(deg_to_rad(90), pi / 2)
    assert equal(2 * pi / 360, pi / 180)
    assert equal(deg_to_rad(60), 60 * pi / 180) and equal(60 * pi / 180, pi / 3)
    assert equal(rad_to_deg(theta), 180 * theta / pi)
    assert equal(rad_to_deg(1), 180 / pi) and rounds_to(180 / pi, "57.3")
    # 30° = π/6 (the non-example and the first common mistake), 180° = π (the Summary).
    assert equal(deg_to_rad(30), pi / 6) and equal(sp.sin(pi / 6), sp.Rational(1, 2))
    # sin 30 ≈ −0.988, and 30 is "almost five full turns" (30/(2π) ≈ 4.77, between 4.5 and 5).
    assert rounds_to(sp.sin(30), "-0.988")
    assert is_true(sp.Rational(9, 2) < 30 / (2 * pi)) and is_true(30 / (2 * pi) < 5)
    # Circle of radius r: arc rθ and sector ½r²θ (fractions θ/(2π) of 2πr and πr²); at θ = 2π they are 2πr, πr².
    r = sp.Symbol("r", positive=True)
    assert equal(theta / (2 * pi) * 2 * pi * r, r * theta)
    assert equal(theta / (2 * pi) * pi * r**2, r**2 * theta / 2)
    assert equal((r * theta).subs(theta, 2 * pi), 2 * pi * r) and equal((r**2 * theta / 2).subs(theta, 2 * pi), pi * r**2)
    # Sin/cos example: P(0) = (1, 0), P(π/2) = (0, 1).
    assert equal((sp.cos(0), sp.sin(0)), (1, 0)) and equal((sp.cos(pi / 2), sp.sin(pi / 2)), (0, 1))
    # Tangent: (1, tan t) = P(t)/cos t; tan 0 = 0, sec 0 = 1; cos(π/2) = 0 (tan undefined there),
    # sin 0 = 0 (cot and csc undefined at 0); cot = 1/tan where both are defined and tan ≠ 0.
    assert equal((sp.cos(t) / sp.cos(t), sp.sin(t) / sp.cos(t)), (1, sp.tan(t)))
    assert equal(sp.tan(0), 0) and equal(sp.sec(0), 1) and equal(sp.cos(pi / 2), 0) and equal(sp.sin(0), 0)
    assert equal(sp.cot(t), 1 / sp.tan(t))


def test_pythagorean_identity_and_addition_formulas():
    # thm-calc-pythagorean-identity, symbolically (equal, and trigsimp) and at random reals.
    assert equal(sp.cos(t) ** 2 + sp.sin(t) ** 2, 1)
    assert equal(sp.trigsimp(sp.cos(t) ** 2 + sp.sin(t) ** 2), 1)
    assert numeric_spot_check(sp.cos(t) ** 2 + sp.sin(t) ** 2, sp.Integer(1), t, REALS)
    # 1 + tan² = sec² where cos ≠ 0.
    assert equal(1 + sp.tan(t) ** 2, sp.sec(t) ** 2)
    assert numeric_spot_check(1 + sp.tan(t) ** 2, 1 / sp.cos(t) ** 2, t, REALS)
    # thm-calc-addition-formulas (a)–(f).
    formulas = [
        (sp.cos(s - t), sp.cos(s) * sp.cos(t) + sp.sin(s) * sp.sin(t)),
        (sp.cos(s + t), sp.cos(s) * sp.cos(t) - sp.sin(s) * sp.sin(t)),
        (sp.sin(s + t), sp.sin(s) * sp.cos(t) + sp.cos(s) * sp.sin(t)),
        (sp.sin(s - t), sp.sin(s) * sp.cos(t) - sp.cos(s) * sp.sin(t)),
    ]
    for lhs, rhs in formulas:
        assert equal(lhs, rhs) and equal(sp.expand_trig(lhs), rhs)
        assert spot2(lhs, rhs)
    assert equal(sp.sin(2 * t), 2 * sp.sin(t) * sp.cos(t))
    assert numeric_spot_check(sp.sin(2 * t), 2 * sp.sin(t) * sp.cos(t), t, REALS)
    for form in (sp.cos(t) ** 2 - sp.sin(t) ** 2, 2 * sp.cos(t) ** 2 - 1, 1 - 2 * sp.sin(t) ** 2):
        assert equal(sp.cos(2 * t), form) and equal(sp.trigsimp(form - sp.cos(2 * t)), 0)
        assert numeric_spot_check(sp.cos(2 * t), form, t, REALS)
    # The proof of (a): both squared distances, displayed line by line.
    d1 = (sp.cos(s) - sp.cos(t)) ** 2 + (sp.sin(s) - sp.sin(t)) ** 2
    d1_mid = sp.cos(s) ** 2 + sp.sin(s) ** 2 + sp.cos(t) ** 2 + sp.sin(t) ** 2 - 2 * sp.cos(s) * sp.cos(t) - 2 * sp.sin(s) * sp.sin(t)
    assert equal(d1, d1_mid) and equal(d1_mid, 2 - 2 * (sp.cos(s) * sp.cos(t) + sp.sin(s) * sp.sin(t)))
    d2 = (sp.cos(s - t) - 1) ** 2 + sp.sin(s - t) ** 2
    d2_mid = sp.cos(s - t) ** 2 + sp.sin(s - t) ** 2 - 2 * sp.cos(s - t) + 1
    assert equal(d2, d2_mid) and equal(d2_mid, 2 - 2 * sp.cos(s - t))
    assert spot2(d1, d2)
    # The proof of (c): sin(s + t) = cos(π/2 − (s + t)) = cos((π/2 − s) − t).
    assert equal(sp.sin(s + t), sp.cos(pi / 2 - (s + t))) and equal(pi / 2 - (s + t), (pi / 2 - s) - t)
    # The counterexamples: sin(π/2 + π/2) = 0 ≠ 2 = sin π/2 + sin π/2; cos(2·0) = 1 ≠ 2 = 2 cos 0.
    assert equal(sp.sin(pi / 2 + pi / 2), 0) and equal(sp.sin(pi / 2) + sp.sin(pi / 2), 2)
    assert equal(sp.cos(2 * 0), 1) and equal(2 * sp.cos(0), 2)


def test_zeros_of_sine_and_cosine():
    # rem-calc-trig-functions-zeros: sin t = 0 exactly at kπ; cos t = 0 exactly at π/2 + kπ.
    assert equal(sp.sin(k * pi), 0) and equal(sp.cos(pi / 2 + k * pi), 0)
    # Converse: on one period [0, 2π) the zeros are only these, and 2π is a period.
    assert equal(sp.solveset(sp.sin(x), x, sp.Interval.Ropen(0, 2 * pi)), sp.FiniteSet(0, pi))
    assert equal(sp.solveset(sp.cos(x), x, sp.Interval.Ropen(0, 2 * pi)), sp.FiniteSet(pi / 2, 3 * pi / 2))
    # And over a wider window, independently: every zero in [−20, 20] is kπ (resp. π/2 + kπ).
    zs = sp.solveset(sp.sin(x), x, sp.Interval(-20, 20))
    assert equal(zs, sp.FiniteSet(*[j * pi for j in range(-6, 7)]))
    zc = sp.solveset(sp.cos(x), x, sp.Interval(-20, 20))
    assert equal(zc, sp.FiniteSet(*[pi / 2 + j * pi for j in range(-6, 6)]))
    # The reason of 2: cos t = sin(π/2 − t), zero when π/2 − t = jπ, i.e. t = π/2 + kπ with k = −j.
    assert equal(sp.cos(t), sp.sin(pi / 2 - t))
    j = sp.Symbol("j", integer=True)
    assert equal(pi / 2 - (pi / 2 + (-j) * pi), j * pi)


def test_lemma_sin_bounds():
    # lem-calc-sin-bounds: sin θ < θ < tan θ for 0 < θ < π/2. Numerically at 2000 random points and
    # approaching both ends (10⁻¹ … 10⁻²⁵ from 0 and from π/2), at 100 digits: near 0 the gaps are
    # about θ³/6 and θ³/3, far below double precision. This samples; the proof is the reviewer's.
    with mpmath.workdps(100):
        half = mpmath.pi / 2
        rng = random.Random(7)
        pts = [half * mpmath.mpf(rng.uniform(1e-6, 1 - 1e-6)) for _ in range(2000)]
        pts += [mpmath.mpf(10) ** -j_ for j_ in range(1, 26)]
        pts += [half - mpmath.mpf(10) ** -j_ for j_ in range(1, 26)]
        for p in pts:
            assert 0 < p < half
            assert mpmath.sin(p) < p < mpmath.tan(p), p
    # At exact points, symbolically: π/12, π/6, π/4, π/3, 5π/12, 1 (radian), 1/2.
    for tv in (pi / 12, pi / 6, pi / 4, pi / 3, 5 * pi / 12, sp.Integer(1), sp.Rational(1, 2)):
        assert is_true(sp.sin(tv) < tv) and is_true(tv < sp.tan(tv))
    # Approaching the ends: θ − sin θ ~ θ³/6 and tan θ − θ ~ θ³/3 at 0 (both positive);
    # tan θ → ∞ at π/2 from the left, while sin θ → 1 < π/2.
    assert limit_is((theta - sp.sin(theta)) / theta**3, theta, 0, sp.Rational(1, 6), dir="+")
    assert limit_is((sp.tan(theta) - theta) / theta**3, theta, 0, sp.Rational(1, 3), dir="+")
    assert limit_is(sp.tan(theta), theta, pi / 2, sp.oo, dir="-")
    assert limit_is(sp.sin(theta), theta, pi / 2, 1, dir="-") and is_true(1 < pi / 2)
    # The proof's areas: triangle OAP = ½|det(OA, OP)| = ½ sin θ; triangle OAT = ½ tan θ;
    # T = P / cos θ; the sector: ∫₀^θ ∫₀^1 ρ dρ dφ = θ/2 (a second route to the fact from school).
    th = sp.Symbol("theta", positive=True)
    Pv, Av = sp.Matrix([sp.cos(th), sp.sin(th)]), sp.Matrix([1, 0])
    Tv = sp.Matrix([1, sp.tan(th)])
    assert equal(sp.Matrix.hstack(Av, Pv).det() / 2, sp.sin(th) / 2)
    assert equal(sp.Matrix.hstack(Av, Tv).det() / 2, sp.tan(th) / 2)
    assert equal(tuple(Pv / sp.cos(th)), tuple(Tv))
    rho, phi = sp.symbols("rho phi", positive=True)
    assert equal(sp.integrate(sp.integrate(rho, (rho, 0, 1)), (phi, 0, th)), th / 2)
    # Step 2's algebra, with s = sin(θ/2), c = cos(θ/2): sin θ = 2sc, cos θ = c² − s²,
    # 0 < θ/2 < π/4 < π/2, and 2sc/(c² − s²) − 2sc/c² = 2s³/(c(c² − s²)) (> 0 when s, c, c² − s² > 0).
    sh, ch = sp.sin(theta / 2), sp.cos(theta / 2)
    assert equal(sp.sin(theta), 2 * sh * ch) and equal(sp.cos(theta), ch**2 - sh**2)
    assert numeric_spot_check(sp.sin(theta), 2 * sh * ch, theta, (0, pi / 2))
    assert numeric_spot_check(sp.cos(theta), ch**2 - sh**2, theta, (0, pi / 2))
    S, C = sp.symbols("S C", positive=True)
    assert equal(2 * S * C / (C**2 - S**2) - 2 * S * C / C**2, 2 * S**3 / (C * (C**2 - S**2)))
    assert equal((C**2 - S**2) * 2 * S * C / ((C**2 - S**2) * C**2), 2 * S * C / C**2)
    assert equal(C**2 * 2 * S * C / ((C**2 - S**2) * C**2), 2 * S * C / (C**2 - S**2))
    assert equal(2 * S * C / C**2, 2 * (S / C))
    assert is_true(pi / 4 < pi / 2)
    # rem-calc-trig-functions-sin-bounds-hypothesis: at 0 all three are 0; tan π = 0/(−1) = 0 < π;
    # for −π/2 < θ < 0 the inequalities reverse.
    assert equal(sp.sin(0), 0) and equal(sp.tan(0), 0)
    assert equal(sp.sin(pi) / sp.cos(pi), 0) and equal(sp.cos(pi), -1) and is_true(sp.tan(pi) < pi)
    for tv in (-pi / 3, -pi / 4, -pi / 6, -sp.Rational(1, 10)):
        assert is_true(sp.sin(tv) > tv) and is_true(tv > sp.tan(tv))
    assert equal(sp.tan(-theta), -sp.tan(theta))


def test_period_values_shape_and_wave():
    # Period 2π, and no smaller one (SymPy's periodicity, and the proof's route: sin(π/2 + p) = 1
    # with 0 < p < 2π has no solution).
    assert equal(periodicity(sp.sin(x), x), 2 * pi) and equal(periodicity(sp.cos(x), x), 2 * pi)
    assert equal(sp.solveset(sp.sin(pi / 2 + x) - 1, x, sp.Interval.open(0, 2 * pi)), sp.S.EmptySet)
    assert equal(sp.solveset(sp.cos(x) - 1, x, sp.Interval.open(0, 2 * pi)), sp.S.EmptySet)
    # Values: (√(1 − y²), y) and (y, √(1 − y²)) lie on the unit circle for y in [−1, 1].
    assert equal(sp.sqrt(1 - y**2) ** 2 + y**2, 1)
    # Shape: 0, 1, 0, −1, 0 at 0, π/2, π, 3π/2, 2π; cos t = sin(t + π/2) (via 6 at −t and 4).
    assert equal(tuple(sp.sin(v) for v in (0, pi / 2, pi, 3 * pi / 2, 2 * pi)), (0, 1, 0, -1, 0))
    assert equal(sp.cos(t), sp.sin(t + pi / 2)) and equal(sp.sin(pi / 2 - (-t)), sp.cos(-t))
    assert numeric_spot_check(sp.cos(t), sp.sin(t + pi / 2), t, REALS)
    # a sin(b(x − c)) + d: amplitude a, period 2π/b, phase c, midline d, derived independently for
    # sample values (a, b > 0) with periodicity and function_range.
    for a_, b_, c_, d_ in ((1, 1, 0, 0), (3, 2, 1, 2), (sp.Rational(1, 2), 4, -3, -2), (2, 3, 0, 1),
                           (20, pi / 5, sp.Rational(5, 2), 22), (sp.Rational(5, 2), sp.Rational(1, 2), sp.Rational(3, 4), sp.Rational(-3, 2))):
        f = a_ * sp.sin(b_ * (x - c_)) + d_
        assert equal(periodicity(f, x), 2 * pi / sp.Abs(b_))
        assert equal(function_range(f, x, R), sp.Interval(d_ - sp.Abs(a_), d_ + sp.Abs(a_)))
        assert equal(f, (a_ * sp.sin(b_ * x) + d_).subs(x, x - c_))         # shifted c to the right
        lo, hi = function_range(f, x, R).boundary
        assert equal((lo + hi) / 2, d_)                                   # midline
    # Common mistake: sin 2x has period π, not 4π; sin(2(x + π)) = sin(2x + 2π) = sin 2x.
    assert equal(periodicity(sp.sin(2 * x), x), pi)
    assert equal(sp.sin(2 * (x + pi)), sp.sin(2 * x + 2 * pi)) and equal(sp.sin(2 * x + 2 * pi), sp.sin(2 * x))
    # The looking-ahead in "Why radians": in degrees the limit carries the factor π/180
    # (s(x) = sin(πx/180), s(x)/x → π/180).
    assert limit_is(sp.sin(pi * x / 180) / x, x, 0, pi / 180)


# ── The widget figure wdg-calc-trig-functions-wave ─────────────────────────────


def widget_config() -> dict:
    """The JSON of the function-plot figure on the page (it has no table, so make_fixtures.py
    records nothing for it)."""
    text = PAGE.read_text(encoding="utf-8")
    block = _block(text.replace("::::", ":::"), "wdg-calc-trig-functions-wave")
    body = block.split("```{anywidget} ../../../widgets/function-plot.mjs", 1)[1].split("```", 1)[0]
    return json.loads(body)


def on_grid(slider: dict, value) -> bool:
    lo, hi, step = (sp.nsimplify(slider[key]) for key in ("min", "max", "step"))
    q = (sp.nsimplify(value) - lo) / step
    return bool(lo <= sp.nsimplify(value) <= hi and q.is_integer)


def test_widget_caption_and_try_this():
    cfg = widget_config()
    assert "table" not in cfg and "hole" not in cfg
    a_, b_, c_, d_ = sp.symbols("a b c d", real=True)
    f = sp.sympify(cfg["f"], locals={"a": a_, "b": b_, "c": c_, "d": d_, "x": x, "sin": sp.sin})
    assert equal(f, a_ * sp.sin(b_ * (x - c_)) + d_)
    # Caption: −7 ≤ x ≤ 7; a from 0.5 to 3 in steps of 0.5; b from 0.5 to 4 in steps of 0.5; c from
    # −3 to 3 in steps of 0.25; d from −2 to 2 in steps of 0.5; it starts at a = 1, b = 1, c = 0, d = 0.
    assert cfg["xRange"] == [-7, 7]
    expected = {"a": (1, 0.5, 3, 0.5), "b": (1, 0.5, 4, 0.5), "c": (0, -3, 3, 0.25), "d": (0, -2, 2, 0.5)}
    assert set(cfg["parameters"]) == set(expected)
    for name, (value, lo, hi, step) in expected.items():
        p = cfg["parameters"][name]
        assert (p["value"], p["min"], p["max"], p["step"]) == (value, lo, hi, step), name
    start = f.subs({a_: 1, b_: 1, c_: 0, d_: 0})
    assert equal(start, sp.sin(x))
    # "a wave between −1 and 1 that crosses the x-axis at the multiples of π ≈ 3.14 and repeats every
    # 2π ≈ 6.28": on [−7, 7] the zeros are −2π, −π, 0, π, 2π.
    assert equal(function_range(start, x, sp.Interval(-7, 7)), sp.Interval(-1, 1))
    assert equal(sp.solveset(start, x, sp.Interval(-7, 7)), sp.FiniteSet(*[j_ * pi for j_ in range(-2, 3)]))
    assert rounds_to(pi, "3.14") and rounds_to(2 * pi, "6.28")
    assert equal(periodicity(start, x), 2 * pi)
    # Every slider setting fits in the view yRange: |d| + a ≤ 2 + 3 = 5 < 5.5.
    y_lo, y_hi = cfg["yRange"]
    assert -5 >= y_lo and 5 <= y_hi
    # Try this 1: b = 2 (on the grid): period π, two complete waves on [0, 2π].
    assert on_grid(cfg["parameters"]["b"], 2)
    assert equal(periodicity(f.subs({a_: 1, b_: 2, c_: 0, d_: 0}), x), pi) and equal(2 * pi / pi, 2)
    # Try this 2: c = −1.5 (on the grid), close to −π/2 ≈ −1.571: the graph is close to cos.
    assert on_grid(cfg["parameters"]["c"], -1.5) and rounds_to(-pi / 2, "-1.571")
    g = f.subs({a_: 1, b_: 1, c_: sp.Rational(-3, 2), d_: 0})
    assert equal(g, sp.sin(x + sp.Rational(3, 2)))
    assert equal(sp.sin(x + pi / 2), sp.cos(x))
    # |sin(x + 1.5) − cos x| ≤ |π/2 − 1.5| < 0.071 everywhere (sin is 1-Lipschitz), sampled here.
    with mpmath.workdps(30):
        gap = max(abs(mpmath.sin(v + mpmath.mpf(1.5)) - mpmath.cos(v)) for v in mpmath.linspace(-7, 7, 2001))
        assert gap < mpmath.pi / 2 - mpmath.mpf(1.5) + mpmath.mpf(10) ** -20
    # Try this 3: c = 0, a = 3, d = 2: swings between −1 and 5, midline y = 2.
    assert on_grid(cfg["parameters"]["a"], 3) and on_grid(cfg["parameters"]["d"], 2)
    w = f.subs({a_: 3, b_: 1, c_: 0, d_: 2})
    assert equal(function_range(w, x, R), sp.Interval(-1, 5))
    assert equal(sum(function_range(w, x, R).boundary) / 2, 2)


# ── Second pass: the claims the Author's round added or changed ────────────────
# (vronnblom/maths#18, after review 5462488973: the facts box, property 3's converse, the order
# rules named in each step, def-calc-period, the "Why radians" aside and Try this 2.)


def _pythagorean_points() -> list[tuple[sp.Rational, sp.Rational]]:
    """Exact rational points of the unit circle (from Pythagorean triples), in all four quadrants."""
    pts = []
    for a_, b_, c_ in ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)):
        for p_, q_ in ((a_, b_), (b_, a_)):
            for sx in (1, -1):
                for sy in (1, -1):
                    pts.append((sp.Rational(sx * p_, c_), sp.Rational(sy * q_, c_)))
    return pts


def test_property_3_converse_by_the_integer_part():
    # Reason 3's converse: k = the integer part of (s − t)/(2π) (rem-calc-integer-part), then
    # 2kπ ≤ s − t < 2(k + 1)π, so u = s − t − 2kπ lies in [0, 2π), and P(s) = P(t + u). Checked for
    # exact s, t of either sign, including s − t a multiple of 2π (u = 0) and s − t < 0 (k < 0).
    rng = random.Random(3)
    pairs = [(sp.Rational(rng.randint(-40000, 40000), 1000), sp.Rational(rng.randint(-40000, 40000), 1000))
             for _ in range(60)]
    pairs += [(t0 + 2 * j_ * pi, t0) for t0 in (sp.Integer(0), sp.Rational(7, 3), -pi / 5) for j_ in (-3, 0, 1, 4)]
    for sv, tv in pairs:
        q = (sv - tv) / (2 * pi)
        kv = sp.floor(q)
        assert kv.is_integer and is_true(kv <= q) and is_true(q < kv + 1)
        assert is_true(2 * kv * pi <= sv - tv) and is_true(sv - tv < 2 * (kv + 1) * pi)   # × 2π > 0
        uv = sv - tv - 2 * kv * pi
        assert is_true(0 <= uv) and is_true(uv < 2 * pi)                                  # − 2kπ
        assert equal((sp.cos(sv), sp.sin(sv)), (sp.cos(tv + uv), sp.sin(tv + uv)))
        if equal(sp.cos(sv), sp.cos(tv)) and equal(sp.sin(sv), sp.sin(tv)):
            assert equal(uv, 0)
    # The remark's own example: the integer part of −1.5 is −2.
    assert equal(sp.floor(sp.Rational(-3, 2)), -2)
    # "Only one length in [0, 2π) leads from A to A": P(u) = A with u in [0, 2π) only for u = 0.
    zeros = sp.solveset(sp.cos(x) - 1, x, sp.Interval.Ropen(0, 2 * pi)).intersect(
        sp.solveset(sp.sin(x), x, sp.Interval.Ropen(0, 2 * pi)))
    assert equal(zeros, sp.FiniteSet(0))
    # The rotation mapping A to P(−t) maps P(t) to A and P(t + u) to P(u) (property 2 with α = −t).
    u_ = sp.Symbol("u", real=True)
    rot = sp.Matrix([[sp.cos(-t), -sp.sin(-t)], [sp.sin(-t), sp.cos(-t)]])
    assert equal(tuple(rot * sp.Matrix([sp.cos(t), sp.sin(t)])), (1, 0))
    assert equal(tuple(rot * sp.Matrix([sp.cos(t + u_), sp.sin(t + u_)])), (sp.cos(u_), sp.sin(u_)))


def test_order_rule_steps():
    # Each interval the page obtains by multiplying or adding (with the factor's sign named), by
    # SymPy's imageset of the stated map on the stated interval.
    v_ = sp.Symbol("v_", real=True)
    img = lambda f_, I: sp.imageset(sp.Lambda(v_, f_(v_)), I)  # noqa: E731
    # Lemma, step 2: θ/2 for 0 < θ < π/2 lies in (0, π/4), and π/4 < π/2.
    assert equal(img(lambda w: w / 2, sp.Interval.open(0, pi / 2)), sp.Interval.open(0, pi / 4))
    assert is_true(pi / 4 < pi / 2)
    # eg-…-sign: u = π − t for π/2 < t < π lies in (0, π/2); sol-…-from-cosine: u = t − π for
    # π < t < 3π/2 lies in (0, π/2).
    assert equal(img(lambda w: pi - w, sp.Interval.open(pi / 2, pi)), sp.Interval.open(0, pi / 2))
    assert equal(img(lambda w: w - pi, sp.Interval.open(pi, 3 * pi / 2)), sp.Interval.open(0, pi / 2))
    # sol-…-ferris-times: u = πt/5 maps [0, 10) onto [0, 2π), and t = 5u/π maps it back.
    assert equal(img(lambda w: pi * w / 5, sp.Interval.Ropen(0, 10)), sp.Interval.Ropen(0, 2 * pi))
    assert equal(img(lambda w: 5 * w / pi, sp.Interval.Ropen(0, 2 * pi)), sp.Interval.Ropen(0, 10))
    # Amplitude bullet: a·u + d for −1 ≤ u ≤ 1 and a > 0 fills [d − a, d + a] (sample a, d).
    for a_, d_ in ((1, 0), (3, 2), (sp.Rational(1, 2), -2), (20, 22)):
        assert equal(img(lambda w: a_ * w + d_, sp.Interval(-1, 1)), sp.Interval(d_ - a_, d_ + a_))
    # Period bullet and sol-…-tan-period: an integer k with kπ > 0 has k ≥ 1, and then 2kπ ≥ 2π, kπ ≥ π.
    kk = sp.Symbol("kk", integer=True)
    assert equal(sp.solveset(kk * pi > 0, kk, sp.S.Integers), sp.Range(1, sp.oo))
    assert equal(sp.solveset(2 * kk * pi >= 2 * pi, kk, sp.S.Integers), sp.Range(1, sp.oo))
    # Period bullet's route: sin(π/2 + p) = 1 with p > 0 only at p = 2π, 4π, …; the least is 2π.
    assert equal(sp.solveset(sp.sin(pi / 2 + x) - 1, x, sp.Interval.Lopen(0, 7 * pi)),
                 sp.FiniteSet(2 * pi, 4 * pi, 6 * pi))
    assert equal(sp.cos(pi / 2 + 2 * k * pi), 0)
    # eg-…-special-values, step 2: 2c² + c − 1 = (2c − 1)(c + 1); with c > 0 only c = 1/2 remains.
    cc = sp.Symbol("cc", real=True)
    assert equal(2 * cc**2 + cc - 1, (2 * cc - 1) * (cc + 1))
    assert equal(sp.solveset(2 * cc**2 + cc - 1, cc, sp.Interval.open(0, sp.oo)), sp.FiniteSet(sp.Rational(1, 2)))
    # prop-calc-sin-bounded (a): from 0 ≤ cos² t, 1 − cos² t ≤ 1; a number > 1 squares to > 1, and
    # one < −1 too (after multiplying by −1).
    assert equal(sp.solveset(y**2 > 1, y, sp.Interval.open(1, sp.oo)), sp.Interval.open(1, sp.oo))
    assert equal(sp.solveset(y**2 > 1, y, sp.Interval.open(-sp.oo, -1)), sp.Interval.open(-sp.oo, -1))
    # rem-calc-trig-functions-zeros: cos² t = 1 gives cos t = 1 or −1.
    assert equal(sp.solveset(y**2 - 1, y, R), sp.FiniteSet(-1, 1))
    # Values bullet: y in [−1, 1] gives 1 − y² ≥ 0, and exactly then.
    assert equal(sp.solveset(1 - y**2 >= 0, y, R), sp.Interval(-1, 1))
    # sol-…-cos-decreasing: for 0 ≤ v < u ≤ π, π − v ≤ π, and u − v ≤ π − v (subtracting v).
    rng = random.Random(5)
    grid = [sp.Integer(0), pi] + [pi * sp.Rational(rng.randint(0, 1000), 1000) for _ in range(40)]
    for vv in grid:
        for uu in grid:
            if is_true(vv < uu):
                assert is_true(0 < uu + vv) and is_true(uu + vv < 2 * pi)
                assert is_true(uu - vv <= pi - vv) and is_true(pi - vv <= pi)


def test_lemma_steps_after_the_round():
    # Step 1: every point (x, y) of the disc has x ≤ 1 (x² ≤ x² + y² ≤ 1); on the disc the largest x is 1.
    assert equal(sp.solveset(x**2 <= 1, x, R), sp.Interval(-1, 1))
    assert equal(function_range(sp.cos(x), x, sp.Interval(0, 2 * pi)).sup, 1)
    # Step 2, at 2000 points of (0, π/2) and close to both ends (60 digits): with s = sin(θ/2),
    # c = cos(θ/2): s > 0, 0 < c < 1, 0 < c² − s² < c², the factor 2sc/((c² − s²)c²) > 0, and the
    # two chains sin θ = 2sc < 2s ≤ θ and tan θ = 2sc/(c² − s²) > 2s/c ≥ θ.
    with mpmath.workdps(60):
        half = mpmath.pi / 2
        rng = random.Random(9)
        pts = [half * mpmath.mpf(rng.uniform(1e-6, 1 - 1e-6)) for _ in range(2000)]
        pts += [mpmath.mpf(10) ** -j_ for j_ in range(1, 20)] + [half - mpmath.mpf(10) ** -j_ for j_ in range(1, 20)]
        for p in pts:
            s_, c_ = mpmath.sin(p / 2), mpmath.cos(p / 2)
            assert s_ > 0 and 0 < c_ < 1
            assert 0 < c_**2 - s_**2 < c_**2
            assert 2 * s_ * c_ / ((c_**2 - s_**2) * c_**2) > 0
            assert 2 * s_ * c_ < 2 * s_ <= p
            assert 2 * s_ * c_ / (c_**2 - s_**2) > 2 * s_ / c_ >= p
            assert abs(2 * s_ * c_ - mpmath.sin(p)) < mpmath.mpf(10) ** -50
            assert abs(2 * s_ * c_ / (c_**2 - s_**2) - mpmath.tan(p)) < mpmath.mpf(10) ** -40 * (1 + mpmath.tan(p))


def _cone(pq):
    """Membership in the region between the radii OA and OP, for P = pq with angle in (0, π):
    y ≥ 0 and (x, y) not past the ray OP (cross product (x, y) × P ≥ 0)."""
    p_, q_ = pq
    return lambda X: X[1] >= 0 and X[0] * q_ - X[1] * p_ >= 0


def _in_triangle(X, V0, V1, V2):
    """Barycentric test: X is in the closed triangle V0V1V2."""
    (x0, y0), (x1, y1), (x2, y2) = V0, V1, V2
    det = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    l1 = ((X[0] - x0) * (y2 - y0) - (x2 - x0) * (X[1] - y0)) / det
    l2 = ((x1 - x0) * (X[1] - y0) - (X[0] - x0) * (y1 - y0)) / det
    return l1 >= 0 and l2 >= 0 and l1 + l2 <= 1


def test_facts_box_geometry():
    # rem-calc-trig-functions-school-facts, each new fact checked as an instance, and its uses in
    # the proof of lem-calc-sin-bounds, on exact rational points.
    O, A = (sp.Integer(0), sp.Integer(0)), (sp.Integer(1), sp.Integer(0))
    # Distance: the disc contains the segment between any two of its points (sampled, exact).
    rng = random.Random(4)
    disc = []
    while len(disc) < 40:
        X = (sp.Rational(rng.randint(-100, 100), 100), sp.Rational(rng.randint(-100, 100), 100))
        if X[0] ** 2 + X[1] ** 2 <= 1:
            disc.append(X)
    for X, Y in zip(disc, disc[1:]):
        for lam in (sp.Rational(1, 7), sp.Rational(1, 2), sp.Rational(5, 6)):
            Z = (lam * X[0] + (1 - lam) * Y[0], lam * X[1] + (1 - lam) * Y[1])
            assert Z[0] ** 2 + Z[1] ** 2 <= 1
    # Journeys and arcs: the arc traced by the journey of d from A, {P(τ) : 0 ≤ τ ≤ d}, has length d
    # (the arc-length integral, and the inscribed polygons 2n sin(d/(2n)) → d as a second route).
    d_, tau, nn = sp.Symbol("d", positive=True), sp.Symbol("tau", real=True), sp.Symbol("n", positive=True, integer=True)
    speed = sp.sqrt(sp.diff(sp.cos(tau), tau) ** 2 + sp.diff(sp.sin(tau), tau) ** 2)
    assert equal(sp.integrate(sp.simplify(speed), (tau, 0, d_)), d_)
    assert equal(sp.limit(2 * nn * sp.sin(d_ / (2 * nn)), nn, sp.oo), d_)
    # Rotations: for every point Q of the circle (here exact points in all four quadrants) the
    # rotation by α = atan2(Q) maps A to Q.
    for qx, qy in _pythagorean_points():
        assert equal(qx**2 + qy**2, 1)
        al = sp.atan2(qy, qx)
        rot = sp.Matrix([[sp.cos(al), -sp.sin(al)], [sp.sin(al), sp.cos(al)]])
        assert equal(tuple(rot * sp.Matrix(A)), (qx, qy))
    # Sectors, for arcs from A to P with P = (p, q) exact, 0 < θ < π/2 (the lemma's case):
    #  - the region between the radii is convex (θ < π), checked against its definition λX: the
    #    angle of every convex combination of two points λX, μY lies in [0, θ] (60 digits);
    #  - the triangle OAT is exactly the part of the region with x ≤ 1 (exact grid);
    #  - triangle OAP ⊆ sector ⊆ triangle OAT (exact grid), the two inclusions of the proof;
    #  - every point of the triangle OAP lies on a segment from O to a point Q of AP (the step that
    #    opens "The triangle OAP lies in the sector").
    N = 24
    grid = [(sp.Rational(i, N), sp.Rational(j, N)) for i in range(-N // 2, 2 * N) for j in range(-N // 2, 2 * N)]
    for P in [(p_, q_) for p_, q_ in _pythagorean_points() if p_ > 0 and q_ > 0]:
        T = (sp.Integer(1), P[1] / P[0])
        assert equal(T, (P[0] / P[0], P[1] / P[0]))                 # T = P / cos θ, on the ray OP
        in_region = _cone(P)
        with mpmath.workdps(60):
            th = mpmath.atan2(mpmath.mpf(P[1].p) / P[1].q, mpmath.mpf(P[0].p) / P[0].q)
            for _ in range(200):
                l1, l2 = mpmath.mpf(rng.uniform(0, 3)), mpmath.mpf(rng.uniform(0, 3))
                f1, f2 = th * mpmath.mpf(rng.random()), th * mpmath.mpf(rng.random())
                lam = mpmath.mpf(rng.random())
                Z = (lam * l1 * mpmath.cos(f1) + (1 - lam) * l2 * mpmath.cos(f2),
                     lam * l1 * mpmath.sin(f1) + (1 - lam) * l2 * mpmath.sin(f2))
                ang = mpmath.atan2(Z[1], Z[0])
                assert -mpmath.mpf(10) ** -50 <= ang <= th + mpmath.mpf(10) ** -50
        for X in grid:
            in_disc = X[0] ** 2 + X[1] ** 2 <= 1
            assert _in_triangle(X, O, A, T) == (in_region(X) and X[0] <= 1)
            if _in_triangle(X, O, A, P):
                assert in_region(X) and in_disc                            # triangle OAP ⊆ sector
                if X != O:
                    # Q = where the ray OX meets the line AP; Q is on the segment AP, X on OQ.
                    mu = (P[1] * 1 - 0 * (P[0] - 1)) / (X[1] * (1 - P[0]) + X[0] * P[1])
                    Q = (mu * X[0], mu * X[1])
                    lam = (Q[0] - A[0]) / (P[0] - A[0])
                    assert equal(Q[1], lam * P[1]) and 0 <= lam <= 1 and mu >= 1
            if in_region(X) and in_disc:
                assert _in_triangle(X, O, A, T)                            # sector ⊆ triangle OAT
    # The hypothesis θ < π is needed for convexity: for the arc of 3π/2 from A to (0, −1), the
    # region contains A and (0, −1), but not their midpoint (1/2, −1/2), whose angle is 7π/4.
    assert equal(sp.atan2(-sp.Rational(1, 2), sp.Rational(1, 2)) + 2 * pi, 7 * pi / 4)
    assert is_true(7 * pi / 4 > 3 * pi / 2)
    # Area: the sector of arc θ has area θ/2 (the double integral of the first pass); at θ = 2π the
    # disc has area π, and by a second route ∫ 2√(1 − x²) dx over [−1, 1] = π too.
    assert equal(sp.integrate(2 * sp.sqrt(1 - x**2), (x, -1, 1)), pi)
    assert equal((theta / 2).subs(theta, 2 * pi), pi)
    # The quarter arcs of property 1 have length π/2 each (the arc-length integral on each quadrant).
    for j_ in range(4):
        assert equal(sp.integrate(sp.simplify(speed), (tau, j_ * pi / 2, (j_ + 1) * pi / 2)), pi / 2)


def test_definitions_and_asides_after_the_round():
    # def-calc-radian: for an angle φ with 0 < φ < π, the arc inside it (length φ) is the shorter of
    # the two arcs (the other has length 2π − φ).
    phi_ = sp.Symbol("phi", positive=True)
    assert equal(sp.solveset(phi_ < 2 * pi - phi_, phi_, sp.Interval.open(0, 2 * pi)), sp.Interval.open(0, pi))
    # def-calc-period, used for tan: π is a period (the domain is kept: cos(t + π) = 0 exactly when
    # cos t = 0) and no p in (0, π) is (tan p = tan 0 = 0 has no solution there).
    assert equal(sp.solveset(sp.cos(x + pi), x, sp.Interval(-10, 10)), sp.solveset(sp.cos(x), x, sp.Interval(-10, 10)))
    assert equal(sp.solveset(sp.tan(x) - sp.tan(0), x, sp.Interval.open(0, pi)), sp.S.EmptySet)
    # "Why radians, and not degrees?": with θ = πx/180, s(x)/x = (π/180)·(sin θ/θ), and the
    # degree form of the lemma, s(x) < πx/180 < tan(πx/180), for 0 < x < 90 (sampled).
    xd = sp.Symbol("x_deg", positive=True)
    th = pi * xd / 180
    assert equal(sp.sin(th) / xd, (pi / 180) * (sp.sin(th) / th))
    assert equal(sp.imageset(sp.Lambda(xd, th), sp.Interval.open(0, 90)), sp.Interval.open(0, pi / 2))
    for xv in (sp.Rational(1, 10), 1, 30, 45, 60, sp.Rational(899, 10)):
        tv = pi * xv / 180
        assert is_true(sp.sin(tv) < tv) and is_true(tv < sp.tan(tv))
    # Try this 2: −π/2 is not on the c slider's grid, −1.5 is the grid value closest to it, and
    # c = −π/2 would match cos exactly.
    c_slider = widget_config()["parameters"]["c"]
    assert not on_grid(c_slider, -pi / 2)
    lo, hi, step = (sp.nsimplify(c_slider[key]) for key in ("min", "max", "step"))
    values = [lo + j_ * step for j_ in range(int((hi - lo) / step) + 1)]
    closest = min(values, key=lambda v: abs(float(v + pi / 2)))
    assert equal(closest, sp.Rational(-3, 2))
    assert equal(sp.sin(1 * (x - (-pi / 2))), sp.cos(x))
