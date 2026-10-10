"""Verification tests for content/calculus/limits/squeeze-theorem.md (calc-squeeze-theorem).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps; the answers are read
with answer(label), as printed on the page.

The inequalities of lem-calc-sin-cos-near-zero are checked two ways: exactly, by SymPy (each
difference is 0 at x = 0 and has a derivative SymPy proves positive on (0, π/2), and the
functions have the stated parity), and at high precision on a grid of 0 < |x| < π/2 that runs
down to 10⁻³⁰ and up to π/2 − 10⁻³⁰, with the working precision raised near 0 so that each
margin (as small as x⁴/24) is far above the rounding. sp.is_strictly_increasing is not used: it
answers False for x − sin x on [0, π/2] (its derivative 1 − cos x vanishes at the endpoint 0).

The ε–δ chain of prf-calc-squeeze is checked on each branch of δ = min(δ₁, δ₂, r) and on exact
rational (ε, x) pairs up to the edge of the window, for a concrete squeeze in which every term of
the min matters.
"""

import json
import random
from fractions import Fraction as Q
from itertools import pairwise
from pathlib import Path

import mpmath
import pytest
import sympy as sp

from mathcheck import ManualAnswer, answer, answer_type, covers, equal, limit_is, theta, x

REPO = Path(__file__).resolve().parents[3]
PAGE = REPO / "content" / "calculus" / "limits" / "squeeze-theorem.md"

pi = sp.pi
eps = sp.Symbol("epsilon", positive=True)
L = sp.Symbol("L", real=True)
y = sp.Symbol("y", real=True)
OPEN = sp.Interval.open(0, pi / 2)                       # 0 < x < π/2
PUNCTURED = sp.Interval.open(-pi / 2, pi / 2) - sp.FiniteSet(0)   # 0 < |x| < π/2


def rounds_to(value, printed: str) -> bool:
    """The exact value, rounded to the decimal places of `printed`, is `printed`
    (|value − printed| ≤ half a unit in the last place shown)."""
    places = len(printed.split(".")[1]) if "." in printed else 0
    half = sp.Rational(1, 2) / sp.Integer(10) ** places
    return bool(sp.Abs(sp.N(value, 50) - sp.Rational(printed)) <= half)


def positive_on_open(expr) -> bool:
    """expr > 0 on (0, π/2), exactly: expr is 0 at 0 and expr' > 0 on (0, π/2) (SymPy's solveset
    finds no point of (0, π/2) where expr' ≤ 0), so expr is strictly increasing on [0, π/2)."""
    d = sp.diff(expr, x)
    return equal(expr.subs(x, 0), 0) and equal(sp.solveset(d <= 0, x, OPEN), sp.S.EmptySet)


def where(domain, *conditions, var=x):
    """The points of `domain` where at least one of the conditions holds (solveset takes no Or)."""
    return sp.Union(*(sp.solveset(c, var, domain) for c in conditions))


def grid(n=2000, deep=30):
    """(working precision, point) for points of (0, π/2): 10⁻ᵏ and 3·10⁻ᵏ (near 0) and π/2 − 10⁻ᵏ
    (near π/2) for k = 1 … deep, with 6k + 40 digits, and a uniform grid of n − 1 points."""
    for k_ in range(1, deep + 1):
        dps = 6 * k_ + 40
        with mpmath.workdps(dps):
            ten = mpmath.mpf(10) ** -k_
            for p in (ten, 3 * ten, mpmath.pi / 2 - ten):
                yield dps, p
    with mpmath.workdps(60):
        for j in range(1, n):
            yield 60, mpmath.pi / 2 * j / n


def holds_on_grid(margins, both_signs=True, **kw) -> bool:
    """Every number margins(x) returns is positive, and far above the rounding, at every grid point
    x and (if both_signs) at −x."""
    for dps, p in grid(**kw):
        with mpmath.workdps(dps):
            floor = mpmath.mpf(10) ** -(dps - 15)
            for xv in ((p, -p) if both_signs else (p,)):
                for i, m in enumerate(margins(xv)):
                    assert m > floor, f"margin {i} at x = {mpmath.nstr(xv, 20)}: {mpmath.nstr(m, 10)}"
    return True


# ── lem-calc-sin-cos-near-zero ─────────────────────────────────────────────────


def test_lemma_sin_cos_near_zero_exact():
    # Parity, so that 0 < x < π/2 settles 0 < |x| < π/2 (step 1 of the proof):
    # |sin(−x)| = |sin x|, cos(−x) = cos x, sin(−x)/(−x) = sin x/x; and |x| = x, |sin x| = sin x there.
    assert equal(sp.Abs(sp.sin(-x)), sp.Abs(sp.sin(x)))
    assert equal(sp.cos(-x), sp.cos(x))
    assert equal(sp.sin(-x) / (-x), sp.sin(x) / x)
    assert equal(sp.solveset(sp.sin(x) <= 0, x, OPEN), sp.S.EmptySet)      # sin x > 0 on (0, π/2)
    assert equal(sp.solveset(sp.cos(x) <= 0, x, OPEN), sp.S.EmptySet)      # cos x > 0 on (0, π/2)
    # (a) x − sin x > 0: zero at 0, derivative 1 − cos x > 0.
    assert positive_on_open(x - sp.sin(x))
    # (b) cos x − (1 − x²/2) > 0: zero at 0, derivative x − sin x > 0 (by (a)) …
    assert equal(sp.diff(sp.cos(x) - (1 - x**2 / 2), x), x - sp.sin(x))
    assert equal(sp.cos(0) - 1, 0)
    # … and cos x < 1.
    assert equal(sp.solveset(sp.cos(x) >= 1, x, OPEN), sp.S.EmptySet)
    # (c) sin x/x < 1 is (a) divided by x > 0; cos x < sin x/x is sin x − x cos x > 0 (times x > 0):
    # zero at 0, derivative x sin x > 0 (x > 0 and sin x > 0, above).
    assert equal(sp.diff(sp.sin(x) - x * sp.cos(x), x), x * sp.sin(x))
    assert equal((sp.sin(x) - x * sp.cos(x)).subs(x, 0), 0)


def test_lemma_sin_cos_near_zero_grid():
    mp = mpmath
    # (a) |sin x| < |x|; (b) 1 − x²/2 < cos x < 1; (c) cos x < sin x/x < 1, at ±each grid point.
    assert holds_on_grid(lambda v: [abs(v) - abs(mp.sin(v))])
    assert holds_on_grid(lambda v: [mp.cos(v) - (1 - v**2 / 2), 1 - mp.cos(v)])
    assert holds_on_grid(lambda v: [mp.sin(v) / v - mp.cos(v), 1 - mp.sin(v) / v])


def test_lemma_proof_steps():
    s_ = sp.Symbol("s", real=True)
    # The lemma on sine, angle and tangent, used in the proof: sin t < t < tan t on (0, π/2).
    assert holds_on_grid(lambda v: [v - mpmath.sin(v), mpmath.tan(v) - v], both_signs=False)
    # (c): multiplying t < sin t/cos t by cos t/t > 0 gives cos t < sin t/t.
    t_ = sp.Symbol("t", positive=True)
    assert equal((sp.sin(t_) / sp.cos(t_)) * (sp.cos(t_) / t_), sp.sin(t_) / t_)
    assert equal(t_ * (sp.cos(t_) / t_), sp.cos(t_))
    # (b): the double-angle identity, 1 − cos x = 2 sin²(x/2), i.e. cos 2s = 1 − 2 sin² s at s = x/2.
    assert equal(1 - sp.cos(x), 2 * sp.sin(x / 2) ** 2)
    assert equal(sp.cos(2 * s_), 1 - 2 * sp.sin(s_) ** 2)
    assert equal((1 - 2 * sp.sin(s_) ** 2).subs(s_, x / 2), sp.cos(x))
    # s = x/2: 0 < |x| < π/2 gives 0 < |s| < π/4 < π/2, so (a) applies at s.
    assert equal(sp.Abs(x / 2), sp.Abs(x) / 2)
    assert equal(sp.imageset(sp.Lambda(x, x / 2), PUNCTURED), sp.Interval.open(-pi / 4, pi / 4) - sp.FiniteSet(0))
    assert (pi / 4 < pi / 2) is sp.true
    # sin² s < s² = x²/4, so 2 sin² s < x²/2, and 1 − x²/2 < 1 − 2 sin² s = cos x; and 0 < 2 sin² s.
    assert equal((x / 2) ** 2, x**2 / 4) and equal(2 * (x**2 / 4), x**2 / 2)
    assert equal((1 - 2 * sp.sin(s_) ** 2 - x**2 / 2) + 2 * sp.sin(s_) ** 2, 1 - x**2 / 2)
    assert holds_on_grid(lambda v: [(v / 2) ** 2 - mpmath.sin(v / 2) ** 2,
                                    v**2 / 2 - 2 * mpmath.sin(v / 2) ** 2,
                                    2 * mpmath.sin(v / 2) ** 2])


# ── lem-calc-sin-cos-limits-at-zero, thm-calc-sin-x-over-x, cor-calc-one-minus-cos-over-x ──


def test_limits_at_zero():
    # (a) with δ = ε: ||x| − 0| = |x|, so 0 < |x| < ε gives ||x| − 0| < ε.
    assert equal(sp.Abs(sp.Abs(x) - 0), sp.Abs(x))
    assert limit_is(sp.Abs(x), x, 0, 0)
    assert limit_is(sp.sin(x), x, 0, 0)
    assert limit_is(sp.cos(x), x, 0, 1)
    # (c): the lower bound 1 − x²/2 approaches 1 − 0²/2 = 1.
    assert equal((1 - x**2 / 2).subs(x, 0), 1) and limit_is(1 - x**2 / 2, x, 0, 1)


def test_sin_x_over_x():
    assert limit_is(sp.sin(x) / x, x, 0, 1)
    # Why this matters: the calculator values and the table, to the digits shown, at ±x.
    for xv, printed in (("0.1", "0.0998334"), ("0.01", "0.00999983"), ("0.001", "0.000999999833")):
        assert rounds_to(sp.sin(sp.Rational(xv)), printed)
    for xv, printed in (("0.1", "0.998334"), ("0.01", "0.999983"), ("0.001", "0.9999998")):
        for sign in (1, -1):
            v = sign * sp.Rational(xv)
            assert rounds_to(sp.sin(v) / v, printed)
    # Why radians: in degrees the ratio is sin(πx/180)/x → π/180; at x = 0.01 it is ≈ 0.0174533,
    # and π/180 ≈ 0.0174533.
    assert limit_is(sp.sin(pi * x / 180) / x, x, 0, pi / 180)
    assert rounds_to(sp.sin(pi * sp.Rational(1, 100) / 180) / sp.Rational(1, 100), "0.0174533")
    assert rounds_to(pi / 180, "0.0174533")
    # Common mistake "Working in degrees": the right value in radians, sin 0.01/0.01 ≈ 0.999983.
    assert rounds_to(sp.sin(sp.Rational(1, 100)) / sp.Rational(1, 100), "0.999983")


def test_why_radians_degree_ratio_proof():
    # Why radians, the proof that sin(cx)/x → c for every c > 0 (and so → π/180 in degrees), step
    # by step: lemma (b) and (c) at cx, × c > 0, and the squeeze theorem with r = π/(2c).
    c = sp.Symbol("c", positive=True)
    # An angle of x degrees is πx/180 radians: the ratio in degrees is sin(cx)/x with c = π/180 > 0.
    c_deg = pi / 180
    assert equal(sp.sin(pi * x / 180) / x, (sp.sin(c * x) / x).subs(c, c_deg)) and c_deg.is_positive
    # |cx| = |c| |x| = c|x| (c > 0), and multiplying 0 < |x| < π/(2c) by c gives 0 < |cx| < π/2.
    assert equal(sp.Abs(c * x), sp.Abs(c) * sp.Abs(x)) and equal(sp.Abs(c), c)
    assert equal(c * 0, 0) and equal(c * (pi / (2 * c)), pi / 2)
    for c0 in (c_deg, sp.Integer(3), sp.Rational(1, 2)):
        window = sp.Interval.open(-pi / (2 * c0), pi / (2 * c0)) - sp.FiniteSet(0)
        assert equal(sp.imageset(sp.Lambda(x, c0 * x), window), PUNCTURED)
    # (cx)² = c²x², and c · sin(cx)/(cx) = sin(cx)/x, c · (1 − c²x²/2) = c − c³x²/2.
    assert equal((c * x) ** 2, c**2 * x**2)
    assert equal(c * (sp.sin(c * x) / (c * x)), sp.sin(c * x) / x)
    assert equal(c * (1 - c**2 * x**2 / 2), c - c**3 * x**2 / 2)
    # The chains 1 − c²x²/2 < cos(cx) < sin(cx)/(cx) < 1 and c − c³x²/2 < sin(cx)/x < c, at ±each
    # point of 0 < |x| < π/(2c) (the grid of (0, π/2), divided by c), for three values of c.
    mp = mpmath
    for c_val in (lambda: mp.pi / 180, lambda: mp.mpf(3), lambda: mp.mpf(1) / 2):
        def margins(v, c_val=c_val):
            cv = c_val()
            xv = v / cv
            u = cv * xv
            return [mp.cos(u) - (1 - cv**2 * xv**2 / 2), mp.sin(u) / u - mp.cos(u), 1 - mp.sin(u) / u,
                    mp.sin(u) / xv - (cv - cv**3 * xv**2 / 2), cv - mp.sin(u) / xv]
        assert holds_on_grid(margins)
    # The limits of the bounds: c − c³x²/2 → c − 0 = c, the constant c → c; and r = π/(2c) > 0.
    assert equal(sp.limit(c - c**3 * x**2 / 2, x, 0), c) and equal((c - c**3 * x**2 / 2).subs(x, 0), c)
    assert (pi / (2 * c)).is_positive and (1 / c).is_positive and (pi / 2).is_positive
    # The conclusion, for every c > 0 (SymPy's limit), and with tables for the three values.
    assert equal(sp.limit(sp.sin(c * x) / x, x, 0), c)
    for c0 in (c_deg, sp.Integer(3), sp.Rational(1, 2)):
        assert limit_is(sp.sin(c0 * x) / x, x, 0, c0)
        assert limit_is(c0 - c0**3 * x**2 / 2, x, 0, c0)
    # The mistake "Working in degrees": the ratio approaches π/180, not 1.
    assert limit_is(sp.sin(c_deg * x) / x, x, 0, pi / 180) and not equal(pi / 180, 1)


def test_pi_bound_as_cited():
    # The cited statement, prop-calc-pi-bounds on calc-trig-functions (vronnblom/maths#31, not
    # merged): 2√2 < π < 4. Only the left inequality is used on this page. Checked exactly, and by
    # a second route: sin(π/4) = 1/√2, tan(π/4) = 1, and sin θ < θ < tan θ at θ = π/4 (× 4).
    assert (2 * sp.sqrt(2) < pi) is sp.true and (pi < 4) is sp.true
    assert equal(sp.sin(pi / 4), 1 / sp.sqrt(2)) and equal(sp.tan(pi / 4), 1)
    assert (sp.sin(pi / 4) < pi / 4) is sp.true and (pi / 4 < sp.tan(pi / 4)) is sp.true
    assert equal(4 / sp.sqrt(2), 2 * sp.sqrt(2)) and equal(4 * sp.tan(pi / 4), 4)
    # × ½ (positive), as on the page: ½ · 2√2 = √2 and ½ · π = π/2, so √2 < π/2.
    assert equal(sp.Rational(1, 2) * 2 * sp.sqrt(2), sp.sqrt(2)) and equal(sp.Rational(1, 2) * pi, pi / 2)
    assert (sp.sqrt(2) < pi / 2) is sp.true


def test_corollary_one_minus_cos_over_x():
    # Rewriting on 0 < |x| < π/2: cos x = cos|x| > 0, so 1 + cos x > 1 > 0.
    assert equal(sp.solveset(sp.cos(x) <= 0, x, sp.Interval.open(-pi / 2, pi / 2)), sp.S.EmptySet)
    assert equal(sp.solveset(1 + sp.cos(x) <= 1, x, sp.Interval.open(-pi / 2, pi / 2)), sp.S.EmptySet)
    assert equal((1 - sp.cos(x)) * (1 + sp.cos(x)), sp.sin(x) ** 2)
    F = sp.sin(x) / x * (sp.sin(x) / (1 + sp.cos(x)))
    assert equal((1 - sp.cos(x)) / x, (1 - sp.cos(x)) * (1 + sp.cos(x)) / (x * (1 + sp.cos(x))))
    assert equal((1 - sp.cos(x)) * (1 + sp.cos(x)) / (x * (1 + sp.cos(x))), sp.sin(x) ** 2 / (x * (1 + sp.cos(x))))
    assert equal(sp.sin(x) ** 2 / (x * (1 + sp.cos(x))), F)
    # The limits of the parts: 1 + cos x → M = 2, and M ≠ 0, so the quotient law applies.
    M = sp.limit(1 + sp.cos(x), x, 0)
    assert equal(M, 2) and limit_is(1 + sp.cos(x), x, 0, 2)
    assert (M != 0) is True and M.is_nonzero
    assert limit_is(sp.sin(x) / (1 + sp.cos(x)), x, 0, sp.Rational(0, 2))
    assert limit_is(F, x, 0, 1 * 0)
    # The original quotient has denominator limit 0 (so the quotient law cannot apply to it directly).
    assert limit_is(x, x, 0, 0) and limit_is(1 - sp.cos(x), x, 0, 0)
    assert limit_is((1 - sp.cos(x)) / x, x, 0, 0)


# ── thm-calc-squeeze, rem-calc-squeeze-theorem-distance, rem-calc-squeeze-theorem-hypotheses ──


def test_squeeze_proof_delta_chain():
    # A concrete squeeze in which each term of δ = min(δ₁, δ₂, r) matters: a = 0, L = 0, r = 1,
    # g(x) = −2|x|, h(x) = 3|x|, and f(x) = x for |x| < 1, f(x) = 4|x| otherwise (so the
    # inequalities hold on 0 < |x| < 1 and fail for every |x| ≥ 1).
    r0 = sp.Integer(1)
    g, h = -2 * sp.Abs(x), 3 * sp.Abs(x)
    assert equal(where(sp.Interval.open(-1, 1) - sp.FiniteSet(0), g > x, x > h), sp.S.EmptySet)
    assert equal(where(sp.S.Reals - sp.Interval.open(-1, 1), g > 4 * sp.Abs(x), 4 * sp.Abs(x) > h),
                 sp.S.Reals - sp.Interval.open(-1, 1))
    # δ₁ = ε/2 wins every round for g, δ₂ = ε/3 for h: |g − 0| = 2|x|, |h − 0| = 3|x|.
    assert equal(sp.Abs(g - 0), 2 * sp.Abs(x)) and equal(sp.Abs(h - 0), 3 * sp.Abs(x))
    assert equal(2 * (eps / 2), eps) and equal(3 * (eps / 3), eps)
    d1, d2 = eps / 2, eps / 3
    delta = sp.Min(d1, d2, r0)
    assert delta.is_positive
    # δ on each branch: for ε ≤ 3, ε/3 ≤ ε/2 and ε/3 ≤ 1, so δ = ε/3 = δ₂; for ε > 3,
    # 1 < ε/3 < ε/2, so δ = 1 = r. On each, δ ≤ δ₁, δ ≤ δ₂ and δ ≤ r.
    e_ = sp.Symbol("e", positive=True)
    small, large = 3 * e_ / (1 + e_), 3 + e_        # every ε in (0, 3), and every ε > 3
    assert (sp.simplify(small / 2 - small / 3)).is_positive and (sp.simplify(1 - small / 3)).is_positive
    assert (sp.simplify(large / 3 - 1)).is_positive and (sp.simplify(large / 2 - large / 3)).is_positive
    assert equal(delta.subs(eps, 3), 1)

    def f(v):
        return v if abs(v) < 1 else 4 * abs(v)

    def gq(v):
        return -2 * abs(v)

    def hq(v):
        return 3 * abs(v)

    rng = random.Random(3)
    N = 10**6
    samples = [Q(1, 10**9), Q(1, 1000), Q(1, 10), Q(1), Q(3) - Q(1, 10**9), Q(3), Q(3) + Q(1, 10**9), Q(10), Q(1000)]
    samples += [Q(rng.randint(1, 20 * N), N) for _ in range(200)]
    for e in samples:
        dv = min(e / 2, e / 3, Q(1))
        for fr in [Q(1, 10**9), Q(1, N), Q(N - 1, N), Q(10**9 - 1, 10**9)] + [Q(rng.randint(1, N - 1), N) for _ in range(20)]:
            for xv in (dv * fr, -dv * fr):
                # x is in both windows and in the punctured interval of the hypothesis …
                assert abs(xv) < e / 2 and abs(xv) < e / 3 and abs(xv) < 1
                # … so L − ε < g(x) ≤ f(x) ≤ h(x) < L + ε, and |f(x) − L| < ε.
                assert -e < gq(xv) <= f(xv) <= hq(xv) < e
                assert abs(f(xv)) < e
    # Without r the chain breaks: at ε = 30, min(δ₁, δ₂) = 10, and x = 9 is in that window with
    # |f(9)| = 36 > 30.
    assert min(Q(30) / 2, Q(30) / 3) == 10 and abs(f(Q(9))) > 30


def test_distance_remark_and_equal_functions():
    b_ = sp.Symbol("b", positive=True)
    # |y − L| ≤ b says L − b ≤ y ≤ L + b (part (b) of the distance proposition, as used): with
    # u = y − L, |u| ≤ b is −b ≤ u ≤ b, and y = u + L.
    u_ = sp.Symbol("u", real=True)
    assert equal(sp.solveset(sp.Abs(u_) <= b_, u_, sp.S.Reals), sp.Interval(-b_, b_))
    assert equal(-b_ + L, L - b_) and equal(b_ + L, L + b_)       # u ↦ u + L is increasing
    assert equal((L - b_).subs(b_, 0), L) and equal((L + b_).subs(b_, 0), L)
    # The Example: x|x| is x² for x ≥ 0 and −x² for x < 0, and −x² ≤ x|x| ≤ x² for every real x.
    p, q = sp.Symbol("p", nonnegative=True), sp.Symbol("q", negative=True)
    assert equal(p * sp.Abs(p), p**2) and equal(q * sp.Abs(q), -q**2)
    # (solveset cannot handle x|x| on all of R, so on each half, with |x| = x or −x as just checked)
    assert equal(where(sp.Interval(0, sp.oo), -x**2 > x * x, x * x > x**2), sp.S.EmptySet)
    assert equal(where(sp.Interval.open(-sp.oo, 0), -x**2 > x * (-x), x * (-x) > x**2), sp.S.EmptySet)
    assert limit_is(-x**2, x, 0, 0) and limit_is(x**2, x, 0, 0) and limit_is(x * sp.Abs(x), x, 0, 0)


def test_hypotheses_counterexamples():
    s_fn = sp.Abs(x) / x
    p, q = sp.Symbol("p", positive=True), sp.Symbol("q", negative=True)
    assert equal(s_fn.subs(x, p), 1) and equal(s_fn.subs(x, q), -1)
    # s has no limit at 0: the one-sided limits differ (SymPy's limit, cross-checked by tables) …
    assert limit_is(s_fn, x, 0, 1, dir="+") and limit_is(s_fn, x, 0, -1, dir="-")
    # … and, as in the remark, no L is within ε = 1 of both 1 and −1; 2 = |1 − (−1)|.
    both = sp.Intersection(sp.solveset(sp.Abs(1 - L) < 1, L, sp.S.Reals), sp.solveset(sp.Abs(-1 - L) < 1, L, sp.S.Reals))
    assert equal(both, sp.S.EmptySet)
    assert equal(sp.Abs(L - (-1)), sp.Abs(-1 - L)) and equal(sp.Abs(1 - (-1)), 2)
    # s takes only the values 1 (x > 0) and −1 (x < 0), checked above; solveset cannot handle
    # |x|/x, so the inequalities are checked on those two values.
    # 1: −1 ≤ s ≤ 1 for x ≠ 0, and the bounds have limits −1 and 1 (different).
    assert all(-1 <= v <= 1 for v in (s_fn.subs(x, p), s_fn.subs(x, q)))
    assert limit_is(sp.Integer(-1), x, 0, -1) and limit_is(sp.Integer(1), x, 0, 1)
    # 2: g = h = 1: 1 ≤ s ≤ 1 holds for every x > 0 (s = 1) and for no x < 0 (s = −1 < 1).
    assert equal(s_fn.subs(x, p), 1) and (s_fn.subs(x, q) < 1) is sp.true
    # 3: g = −1 ≤ s for every x ≠ 0 (a lower bound alone).
    assert all(-1 <= v for v in (s_fn.subs(x, p), s_fn.subs(x, q)))


def test_sin_one_over_x_has_no_limit():
    # The Non-example and the common mistakes: −1 ≤ sin(1/x) ≤ 1, and sin(1/x) has no limit at 0.
    # SymPy's limit gives the bounds, not a value; a second route: sin(1/x) = 1 at
    # x = 1/(2πm + π/2) and −1 at x = 1/(2πm − π/2), points of both kinds in every window.
    assert isinstance(sp.limit(sp.sin(1 / x), x, 0), sp.AccumBounds)
    m = sp.Symbol("m", integer=True, positive=True)
    assert equal(sp.sin(2 * pi * m + pi / 2), 1) and equal(sp.sin(2 * pi * m - pi / 2), -1)
    assert limit_is(1 / (2 * pi * x + pi / 2), x, sp.oo, 0) and limit_is(1 / (2 * pi * x - pi / 2), x, sp.oo, 0)


# ── The widget figure wdg-calc-squeeze-theorem-band ───────────────────────────


def widget_config() -> dict:
    text = PAGE.read_text(encoding="utf-8")
    start = text.index(":label: wdg-calc-squeeze-theorem-band")
    body = text[start:].split("```{anywidget} ../../../widgets/function-plot.mjs", 1)[1].split("```", 1)[0]
    return json.loads(body)


def test_widget_three_settings_and_caption():
    cfg = widget_config()
    k_ = sp.Symbol("k", real=True)
    f = sp.sympify(cfg["f"], locals={"k": k_, "x": x, "abs": sp.Abs, "sin": sp.sin})
    # The slider for k takes exactly the values −1, 0 and 1, and starts at 0.
    p = cfg["parameters"]["k"]
    assert (p["value"], p["min"], p["max"], p["step"]) == (0, -1, 1, 1)
    values = [p["min"] + i * p["step"] for i in range(int((p["max"] - p["min"]) / p["step"]) + 1)]
    assert values == [-1, 0, 1]
    # The three settings: g = −|x|, f = x sin(1/x), h = |x|.
    assert equal(f.subs(k_, -1), -sp.Abs(x))
    assert equal(f.subs(k_, 0), x * sp.sin(1 / x))
    assert equal(f.subs(k_, 1), sp.Abs(x))
    assert cfg["xRange"] == [-0.5, 0.5] and cfg["hole"] == {"x": 0, "y": 0} and cfg["trace"] == {"x": 0.25}
    # The table: the six points, and the values for k = 0 to the digits shown (even in x).
    pts = ["0.1", "0.01", "0.001", "-0.001", "-0.01", "-0.1"]
    assert cfg["table"]["points"] == [float(v) for v in pts]
    shown = ["-0.0544021", "-0.00506366", "0.00082688", "0.00082688", "-0.00506366", "-0.0544021"]
    fx = x * sp.sin(1 / x)
    for xv, printed in zip(pts, shown):
        v = fx.subs(x, sp.Rational(xv))
        assert rounds_to(v, printed)
        # At each point g ≤ f ≤ h (in exact arithmetic, evaluated to 50 digits).
        assert (-sp.Abs(sp.Rational(xv)) <= v) is sp.true and (v <= sp.Abs(sp.Rational(xv))) is sp.true
    # The caption: at k = 0, f swings between the heights −|x| and |x| (they bound it: |sin(1/x)| ≤ 1,
    # tested in the example) and reaches both, faster and faster near 0: f = |x| at x = 2/((4m + 1)π)
    # and f = −|x| at x = 2/((4m + 3)π), for every integer m ≥ 0, points that approach 0.
    m = sp.Symbol("m", integer=True, nonnegative=True)
    up, down = 2 / ((4 * m + 1) * pi), 2 / ((4 * m + 3) * pi)
    assert equal(sp.sin(1 / up), 1) and equal(sp.sin(1 / down), -1)
    assert equal(fx.subs(x, up), sp.Abs(up)) and equal(fx.subs(x, down), -sp.Abs(down))
    assert limit_is(up.subs(m, x), x, sp.oo, 0) and limit_is(down.subs(m, x), x, sp.oo, 0)
    # Try this: the band at x = 0.001 is from −0.001 to 0.001, of width 2|x| = 0.002.
    assert equal(sp.Abs(sp.Rational(1, 1000)) - (-sp.Abs(sp.Rational(1, 1000))), sp.Rational(2, 1000))


# ── Worked examples ──────────────────────────────────────────────────────────


@covers("eg-calc-squeeze-theorem-oscillating")
def test_eg_calc_squeeze_theorem_oscillating():
    fx = x * sp.sin(1 / x)
    # Step 2: |x sin(1/x) − 0| = |x| |sin(1/x)| ≤ |x|, from −1 ≤ sin(1/x) ≤ 1.
    assert equal(sp.Abs(fx - 0), sp.Abs(x) * sp.Abs(sp.sin(1 / x)))
    assert equal(sp.solveset(sp.Abs(y) <= 1, y, sp.S.Reals), sp.Interval(-1, 1))
    assert equal(sp.calculus.util.function_range(sp.sin(y), y, sp.S.Reals), sp.Interval(-1, 1))
    # Step 3 and the box (SymPy's limit, cross-checked by its table of values).
    assert limit_is(fx, x, 0, 0)
    # Check: the table at k = 0 against the band (|f(x)| ≤ |x| at x = 0.1, 0.01, 0.001).
    for xv, printed in (("0.1", "-0.0544021"), ("0.01", "-0.00506366"), ("0.001", "0.00082688")):
        v = fx.subs(x, sp.Rational(xv))
        assert rounds_to(v, printed) and (sp.Abs(v) <= sp.Rational(xv)) is sp.true
    # At x = 1/π the value is 0; at x = 2/π it is 2/π, on the upper edge |x|.
    assert equal(fx.subs(x, 1 / pi), 0)
    assert equal(fx.subs(x, 2 / pi), 2 / pi) and equal(fx.subs(x, 2 / pi), sp.Abs(2 / pi))


@covers("eg-calc-squeeze-theorem-sin-3x")
def test_eg_calc_squeeze_theorem_sin_3x():
    S, C = sp.sin(x), sp.cos(x)
    # Step 2, line by line.
    lines = [
        sp.sin(3 * x),
        sp.sin(2 * x) * C + sp.cos(2 * x) * S,
        2 * S * C**2 + (1 - 2 * S**2) * S,
        2 * S * (1 - S**2) + S - 2 * S**3,
        3 * S - 4 * S**3,
    ]
    for lhs, rhs in pairwise(lines):
        assert equal(lhs, rhs)
    # The addition formulas used: sin(s + t) with s = 2x, t = x; sin 2x, cos 2x; cos² = 1 − sin².
    assert equal(sp.sin(2 * x), 2 * S * C) and equal(sp.cos(2 * x), 1 - 2 * S**2) and equal(C**2, 1 - S**2)
    # Step 3: sin 3x/x = (sin x/x)(3 − 4 sin² x).
    assert equal(sp.sin(3 * x) / x, S / x * (3 - 4 * S**2))
    # Step 4: the limits of the factors, and step 5.
    assert limit_is(S**2, x, 0, 0) and limit_is(4 * S**2, x, 0, 0) and limit_is(3 - 4 * S**2, x, 0, 3)
    assert limit_is(sp.sin(3 * x) / x, x, 0, 3)
    # Check: sin 0.03/0.01 ≈ 2.99955; at x = π/2, sin(3π/2) = −1 = 3 − 4.
    assert rounds_to(sp.sin(sp.Rational(3, 100)) / sp.Rational(1, 100), "2.99955")
    assert equal(sp.sin(3 * pi / 2), -1) and equal((3 * S - 4 * S**3).subs(x, pi / 2), 3 - 4)


@covers("eg-calc-squeeze-theorem-small-angle")
def test_eg_calc_squeeze_theorem_small_angle():
    err = 1 - sp.sin(theta) / theta
    assert equal((theta - sp.sin(theta)) / theta, err)
    # Step 1: 0 < 1 − sin θ/θ < θ²/2 on 0 < |θ| < π/2 (on the grid; and exactly: it is (c) and (b)
    # of the lemma, checked in test_lemma_sin_cos_near_zero_exact).
    assert holds_on_grid(lambda v: [1 - mpmath.sin(v) / v, v**2 / 2 - (1 - mpmath.sin(v) / v)])
    # Step 1's last sentence: the relative error is positive at both signs of θ, θ is larger than
    # sin θ in absolute value (|sin θ| < |θ|), and θ > sin θ for θ > 0, but θ < sin θ for θ < 0
    # (so "always overestimates", the wording before the first review, was false for θ < 0):
    # sin(−t) − (−t) = t − sin t > 0 on (0, π/2).
    assert holds_on_grid(lambda v: [abs(v) - abs(mpmath.sin(v))])
    assert holds_on_grid(lambda v: [v - mpmath.sin(v), mpmath.sin(-v) - (-v)], both_signs=False)
    assert equal(sp.sin(-x) - (-x), x - sp.sin(x)) and positive_on_open(x - sp.sin(x))
    tenth = sp.Rational(1, 10)
    assert (sp.sin(-tenth) > -tenth) is sp.true and ((1 - sp.sin(-tenth) / (-tenth)) > 0) is sp.true
    # Step 2: θ²/2 ≤ 0.01 exactly when |θ| ≤ √0.02.
    root = sp.sqrt(sp.Rational(2, 100))
    assert equal(sp.solveset(theta**2 / 2 <= sp.Rational(1, 100), theta, sp.S.Reals), sp.Interval(-root, root))
    assert equal(theta**2, sp.Abs(theta) ** 2) and equal(root**2, sp.Rational(2, 100))
    assert rounds_to(root, "0.141421") and rounds_to(root, "0.141")
    # Step 3, as the page now argues it (no decimal value of π; the page no longer prints
    # π/2 ≈ 1.571, so that check is gone): 2√2 < π (test_pi_bound_as_cited), × ½ gives √2 < π/2;
    # √0.02 and √2 are non-negative with squares 0.02 < 2, so √0.02 < √2; transitivity gives
    # √0.02 < π/2, and every θ with 0 < |θ| ≤ √0.02 is in 0 < |θ| < π/2, where step 1 applies.
    assert (2 * sp.sqrt(2) < pi) is sp.true and (sp.sqrt(2) < pi / 2) is sp.true
    assert root.is_nonnegative and sp.sqrt(2).is_nonnegative
    assert equal(sp.sqrt(2) ** 2, 2) and sp.Rational(2, 100) < 2 and (root < sp.sqrt(2)) is sp.true
    assert (root < pi / 2) is sp.true
    assert (sp.Interval(-root, root) - sp.FiniteSet(0)).is_subset(PUNCTURED)
    # The pendulum threshold: for 0 < |θ| ≤ √0.02, 1 − sin θ/θ < θ²/2 ≤ 0.01, on a grid of
    # (0, √0.02] including √0.02 itself.
    with mpmath.workdps(60):
        hundredth = mpmath.mpf(1) / 100
        r_mp = mpmath.sqrt(mpmath.mpf(2) / 100)
        pts = [r_mp * j / 4000 for j in range(1, 4001)] + [mpmath.mpf(10) ** -k_ for k_ in range(2, 15)]
        for tv in pts:
            for v in (tv, -tv):
                e = 1 - mpmath.sin(v) / v
                assert 0 < e < v**2 / 2 and v**2 / 2 <= hundredth * (1 + mpmath.mpf(10) ** -50)
                assert e < hundredth
    # At θ = √0.02 exactly: θ²/2 = 0.01, and the error is below it.
    assert equal(root**2 / 2, sp.Rational(1, 100))
    assert ((1 - sp.sin(root) / root) < sp.Rational(1, 100)) is sp.true
    # In degrees: 180√0.02/π ≈ 8.10 ≈ 8.1.
    assert rounds_to(180 * root / pi, "8.10") and rounds_to(180 * root / pi, "8.1")
    # Check: sin 0.14 ≈ 0.139543, 1 − sin 0.14/0.14 ≈ 0.00326 < 0.14²/2 = 0.0098 < 0.01.
    t14 = sp.Rational(14, 100)
    assert rounds_to(sp.sin(t14), "0.139543") and rounds_to(err.subs(theta, t14), "0.00326")
    assert equal(t14**2 / 2, sp.Rational(98, 10000)) and (err.subs(theta, t14) < t14**2 / 2) is sp.true
    assert sp.Rational(98, 10000) < sp.Rational(1, 100)
    # At θ = √0.02 the error is ≈ 0.00333, about a third of 0.01.
    assert rounds_to(err.subs(theta, root), "0.00333")
    # Looking ahead: (1 − sin θ/θ)/θ² → 1/6, a third of the bound's 1/2.
    assert limit_is(err / theta**2, theta, 0, sp.Rational(1, 6))
    assert equal(sp.Rational(1, 6) / sp.Rational(1, 2), sp.Rational(1, 3))


# ── Exercises ────────────────────────────────────────────────────────────────


@covers("exr-calc-squeeze-theorem-sin-2x")
def test_exr_calc_squeeze_theorem_sin_2x():
    assert equal(sp.sin(2 * x) / x, 2 * sp.cos(x) * sp.sin(x) / x)
    assert limit_is(2 * sp.cos(x), x, 0, 2)
    expected = sp.limit(sp.sin(2 * x) / x, x, 0)
    assert limit_is(sp.sin(2 * x) / x, x, 0, expected)
    assert equal(answer("exr-calc-squeeze-theorem-sin-2x"), expected)


@covers("exr-calc-squeeze-theorem-x2-cos")
def test_exr_calc_squeeze_theorem_x2_cos():
    f = x**2 * sp.cos(1 / x)
    # |x² cos(1/x) − 0| = x² |cos(1/x)| ≤ x², and x² → 0.
    assert equal(sp.Abs(f - 0), x**2 * sp.Abs(sp.cos(1 / x)))
    assert equal(sp.Abs(x**2), sp.Abs(x) ** 2) and equal(sp.Abs(x) ** 2, x**2)
    assert equal(sp.calculus.util.function_range(sp.cos(y), y, sp.S.Reals), sp.Interval(-1, 1))
    expected = sp.limit(f, x, 0)
    assert limit_is(f, x, 0, expected) and limit_is(x**2, x, 0, 0)
    assert equal(answer("exr-calc-squeeze-theorem-x2-cos"), expected)


@covers("exr-calc-squeeze-theorem-tan")
def test_exr_calc_squeeze_theorem_tan():
    assert equal(sp.tan(x) / x, (sp.sin(x) / x) / sp.cos(x))
    assert limit_is(sp.cos(x), x, 0, 1)        # M = 1 ≠ 0
    expected = sp.limit(sp.tan(x) / x, x, 0)
    assert limit_is(sp.tan(x) / x, x, 0, expected)
    assert equal(answer("exr-calc-squeeze-theorem-tan"), expected)


@covers("exr-calc-squeeze-theorem-one-minus-cos-x2")
def test_exr_calc_squeeze_theorem_one_minus_cos_x2():
    G = (sp.sin(x) / x) ** 2 / (1 + sp.cos(x))
    # The rewrite, one line per `=` (as the page now displays it), on 0 < |x| < π/2, where
    # 1 + cos x > 1 > 0.
    assert equal((1 - sp.cos(x)) / x**2, (1 - sp.cos(x)) * (1 + sp.cos(x)) / (x**2 * (1 + sp.cos(x))))
    assert equal((1 - sp.cos(x)) * (1 + sp.cos(x)) / (x**2 * (1 + sp.cos(x))), sp.sin(x) ** 2 / (x**2 * (1 + sp.cos(x))))
    assert equal((1 - sp.cos(x)) / x**2, sp.sin(x) ** 2 / (x**2 * (1 + sp.cos(x))))
    assert equal(sp.sin(x) ** 2 / (x**2 * (1 + sp.cos(x))), G)
    assert limit_is((sp.sin(x) / x) ** 2, x, 0, 1) and limit_is(1 / (1 + sp.cos(x)), x, 0, sp.Rational(1, 2))
    expected = sp.limit((1 - sp.cos(x)) / x**2, x, 0)
    assert limit_is((1 - sp.cos(x)) / x**2, x, 0, expected)
    # Second route: 1 − cos x = 2 sin²(x/2), so the quotient is (1/2)(sin(x/2)/(x/2))² → 1/2.
    assert equal((1 - sp.cos(x)) / x**2, sp.Rational(1, 2) * (sp.sin(x / 2) / (x / 2)) ** 2)
    assert equal(answer("exr-calc-squeeze-theorem-one-minus-cos-x2"), expected)


@covers("exr-calc-squeeze-theorem-sqrt-sin")
def test_exr_calc_squeeze_theorem_sqrt_sin():
    f = sp.sqrt(sp.Abs(x)) * sp.sin(1 / x)
    assert equal(sp.Abs(f - 0), sp.sqrt(sp.Abs(x)) * sp.Abs(sp.sin(1 / x)))
    assert limit_is(sp.sqrt(sp.Abs(x)), x, 0, 0)
    # SymPy's limit, cross-checked against the bound √|x| at sample points (|f| ≤ √|x|).
    expected = sp.limit(f, x, 0)
    assert limit_is(f, x, 0, expected)
    for k_ in range(1, 12):
        for v in (sp.Rational(1, 10**k_), -sp.Rational(3, 10**k_)):
            assert (sp.Abs(f.subs(x, v)) <= sp.sqrt(sp.Abs(v))) is sp.true
    assert equal(answer("exr-calc-squeeze-theorem-sqrt-sin"), expected)


@covers("exr-calc-squeeze-theorem-pendulum")
def test_exr_calc_squeeze_theorem_pendulum():
    tol = sp.Rational(5, 1000)
    good = sp.solveset(theta**2 / 2 <= tol, theta, sp.S.Reals)
    assert isinstance(good, sp.Interval) and equal(good.inf, -good.sup)
    r_max = good.sup
    # r = sup works: (−r, r) lies in the solution set; no larger r works: for r' = r + p (p > 0),
    # θ = (r + r')/2 has 0 < θ < r' and θ²/2 > 0.005.
    assert sp.Interval.open(-r_max, r_max).is_subset(good)
    p = sp.Symbol("p", positive=True)
    mid = (r_max + (r_max + p)) / 2
    assert sp.expand(mid**2 / 2 - tol).is_positive
    got = answer("exr-calc-squeeze-theorem-pendulum")
    assert equal(got, r_max)
    # The solution's claims: r < π/2, now by 0.1 < 1 < √2 < π/2 (1 and √2 are non-negative with
    # squares 1 < 2; √2 < π/2 from 2√2 < π, as in the example), so 0 < |θ| < 0.1 lies in
    # 0 < |θ| < π/2; in degrees 18/π ≈ 5.73; the ratio to √0.02 is 1/√2.
    assert equal(sp.Integer(1) ** 2, 1) and equal(sp.sqrt(2) ** 2, 2) and (sp.Integer(1) < sp.sqrt(2)) is sp.true
    assert sp.Rational(1, 10) < 1 and (sp.sqrt(2) < pi / 2) is sp.true
    assert (got < pi / 2) is sp.true
    assert (sp.Interval.open(-got, got) - sp.FiniteSet(0)).is_subset(PUNCTURED)
    assert equal(180 * got / pi, 18 / pi) and rounds_to(18 / pi, "5.73")
    assert equal(got / sp.sqrt(sp.Rational(2, 100)), 1 / sp.sqrt(2))
    # The bound of the example then gives a relative error below 0.005 on 0 < |θ| < r.
    with mpmath.workdps(50):
        for j in range(1, 2001):
            v = mpmath.mpf(1) / 10 * j / 2001
            for w in (v, -v):
                assert 1 - mpmath.sin(w) / w < w**2 / 2 < mpmath.mpf(5) / 1000


@covers("exr-calc-squeeze-theorem-different-limits")
def test_exr_calc_squeeze_theorem_different_limits():
    assert answer_type("exr-calc-squeeze-theorem-different-limits") == "bool"
    # A counterexample to the claim: s(x) = |x|/x is defined at every x ≠ 0, −1 ≤ s ≤ 1 there,
    # and its one-sided limits at 0 differ, so it has no limit; the claim is false.
    s_fn = sp.Abs(x) / x
    p, q = sp.Symbol("p", positive=True), sp.Symbol("q", negative=True)
    assert equal(s_fn.subs(x, p), 1) and equal(s_fn.subs(x, q), -1)
    assert all(-1 <= v <= 1 for v in (s_fn.subs(x, p), s_fn.subs(x, q)))
    assert limit_is(s_fn, x, 0, 1, dir="+") and limit_is(s_fn, x, 0, -1, dir="-")
    claim_holds = False
    assert equal(answer("exr-calc-squeeze-theorem-different-limits"), sp.true if claim_holds else sp.false)


@covers("exr-calc-squeeze-theorem-direct-cor")
def test_exr_calc_squeeze_theorem_direct_cor():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-squeeze-theorem-direct-cor")
    # 0 < 1 − cos x < x²/2 and |(1 − cos x)/x − 0| < |x|/2, on 0 < |x| < π/2 (grid).
    assert holds_on_grid(lambda v: [1 - mpmath.cos(v), v**2 / 2 - (1 - mpmath.cos(v)),
                                    abs(v) / 2 - abs((1 - mpmath.cos(v)) / v)])
    q = sp.Symbol("q", positive=True)       # q = |x|
    assert equal(q**2 / (2 * q), q / 2)
    assert equal(sp.Abs((1 - sp.cos(x)) / x), sp.Abs(1 - sp.cos(x)) / sp.Abs(x))
    assert limit_is(sp.Abs(x) / 2, x, 0, 0)
    assert limit_is((1 - sp.cos(x)) / x, x, 0, 0)


@covers("exr-calc-squeeze-theorem-parabola")
def test_exr_calc_squeeze_theorem_parabola():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-squeeze-theorem-parabola")
    # f(0) = 0: |y| ≤ 0² has the only solution y = 0. As the solution now argues it: |f(0)| ≤ 0 and
    # |f(0)| ≥ 0 leave, by trichotomy, only |f(0)| = 0, and |y| = 0 only for y = 0.
    assert equal(sp.solveset(sp.Abs(y) <= 0**2, y, sp.S.Reals), sp.FiniteSet(0))
    assert equal(sp.Interval(-sp.oo, 0).intersect(sp.Interval(0, sp.oo)), sp.FiniteSet(0))
    assert equal(sp.solveset(sp.Eq(sp.Abs(y), 0), y, sp.S.Reals), sp.FiniteSet(0))
    # |f(x)/x − 0| = |f(x)|/|x| ≤ x²/|x| = |x| for x ≠ 0, and |x| → 0.
    assert equal(x**2 / sp.Abs(x), sp.Abs(x))
    assert limit_is(sp.Abs(x), x, 0, 0)
    # The example f(x) = x² cos(1/x): |f(x)| ≤ x², and f(x)/x → 0.
    f = x**2 * sp.cos(1 / x)
    assert equal(sp.Abs(f), x**2 * sp.Abs(sp.cos(1 / x)))
    assert equal(sp.Abs(x**2), sp.Abs(x) ** 2) and equal(sp.Abs(x) ** 2, x**2)
    assert equal(sp.solveset(sp.Abs(y) <= 1, y, sp.S.Reals), sp.Interval(-1, 1))   # −1 ≤ c ≤ 1 ⇔ |c| ≤ 1
    assert equal(sp.calculus.util.function_range(sp.cos(y), y, sp.S.Reals), sp.Interval(-1, 1))
    # … and at x = 0 (with f(0) = 0): |0| = 0 ≤ 0 = 0².
    assert equal(sp.Abs(0), 0) and sp.Abs(0) <= sp.Integer(0) ** 2
    assert limit_is(f / x, x, 0, 0)
