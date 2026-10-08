"""Verification tests for content/calculus/limits/one-sided-limits.md (calc-one-sided-limits).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps; the answers are read
with answer(label), as printed on the page.

The ε–δ checks follow verify/calculus/limits/test_limit_of_a_function.py, one side at a time: each
displayed step is asserted, a chosen δ is checked symbolically (on each branch of a min), and the
implication "x in the half-window ⇒ |f(x) − L| < ε" is tested on exact rational (ε, x) pairs up to
the edge of the half-window. Floats could hide a failure at the edge, so the sampled arithmetic is
exact (fractions.Fraction, or SymPy where a square root is involved). The Python functions raise
outside the domain the page gives, so a sampled point outside the domain fails the test.

One-sided limits are computed twice: with sp.limit(…, dir='+' / '-') through limit_is (which also
checks a table of values approaching the point), and from the formula that holds on that side. For
a piecewise function only the formula of the side is given to SymPy: SymPy 1.14 mis-evaluates
limits of Piecewise (on this page's functions it returns 0 for both one-sided limits of the
function of eg-calc-one-sided-limits-agree, whose one-sided limits are 4, and 3 for the right-hand
limit of the parcel price, which is 5), and of Heaviside.
"""

import random
from fractions import Fraction as Q

import pytest
import sympy as sp

from mathcheck import ManualAnswer, answer, c, covers, equal, limit_is, t, w, x

eps = sp.Symbol("epsilon", positive=True)
delta = sp.Symbol("delta", positive=True)
L = sp.Symbol("L", real=True)
N = 10**6


def eps_samples(seed, count=200, breaks=()):
    """Exact rational tolerances: tiny, moderate and huge ones, each break of a min (the ε where
    the branches meet) and its immediate neighbours, and random ones."""
    rng = random.Random(seed)
    fixed = [Q(1, 10**9), Q(1, 10**6), Q(1, 1000), Q(1, 100), Q(1, 10), Q(1, 2), Q(1), Q(3), Q(100), Q(10**6)]
    for b in breaks:
        fixed += [Q(b), Q(b) - Q(1, 10**9), Q(b) + Q(1, 10**9)]
    return fixed + [Q(rng.randint(1, 20 * N), N) for _ in range(count)]


def half_window(a, d, side, rng, count=40):
    """Exact rational points of the half-window a < x < a + d (side = +1) or a − d < x < a
    (side = −1): right next to a, within 10⁻⁹·d of the far edge, and random ones in between."""
    fractions = [Q(1, 10**9), Q(1, N), Q(N - 1, N), Q(10**9 - 1, 10**9)]
    fractions += [Q(rng.randint(1, N - 1), N) for _ in range(count)]
    for fr in fractions:
        yield a + side * d * fr


def window(a, d, rng, count=40):
    """Exact rational points of the punctured window 0 < |x − a| < d, on both sides."""
    yield from half_window(a, d, 1, rng, count)
    yield from half_window(a, d, -1, rng, count)


def one_sided_holds(f, a, lim, choose_delta, samples, side, seed=0, count=40):
    """x in the half-window of δ = choose_delta(ε) ⇒ |f(x) − L| < ε at every sampled (ε, x)."""
    rng = random.Random(seed)
    for e in samples:
        d = choose_delta(e)
        assert d > 0
        for xv in half_window(a, d, side, rng, count):
            assert (xv > a) if side > 0 else (xv < a)      # a is never in a half-window
            assert abs(f(xv) - lim) < e, f"side {side:+d}, ε = {e}, δ = {d}, x = {xv}: |f(x) − L| = {abs(f(xv) - lim)}"
    return True


def two_sided_holds(f, a, lim, choose_delta, samples, seed=0, count=40):
    """0 < |x − a| < δ ⇒ |f(x) − L| < ε at every sampled (ε, x), both sides."""
    rng = random.Random(seed)
    for e in samples:
        d = choose_delta(e)
        assert d > 0
        for xv in window(a, d, rng, count):
            assert xv != a
            assert abs(f(xv) - lim) < e, f"ε = {e}, δ = {d}, x = {xv}: |f(x) − L| = {abs(f(xv) - lim)}"
    return True


def empty_on(condition, var, domain):
    """The set of `var` in `domain` where `condition` holds (an inequality, or an And of them),
    compared with the empty set."""
    parts = condition.args if isinstance(condition, sp.And) else (condition,)
    solved = sp.Intersection(*(sp.solveset(cond, var, domain) for cond in parts))
    return equal(solved, sp.S.EmptySet)


def no_common_limit(left, right):
    """No number is within ε = ½|right − left| of both one-sided values: the two-sided limit fails
    the round ε directly from the definition, without the theorem (a second route to the page's
    'does not exist' verdicts)."""
    e = sp.Abs(right - left) / 2
    assert e.is_positive
    return empty_on(sp.And(sp.Abs(left - L) < e, sp.Abs(right - L) < e), L, sp.S.Reals)


def open_inside(lo, hi, LO, HI):
    """(lo, hi) ⊆ (LO, HI), from the endpoints: LO ≤ lo and hi ≤ HI (SymPy decides each)."""
    return (sp.sympify(LO) <= lo) is sp.true and (sp.sympify(hi) <= HI) is sp.true


def undefined(*_):
    raise ValueError("outside the domain the page gives")


def R(q):
    """A Fraction as a SymPy Rational."""
    return sp.Rational(q.numerator, q.denominator)


# ── Examples ──────────────────────────────────────────────────────────────────


@covers("eg-calc-one-sided-limits-agree")
def test_eg_calc_one_sided_limits_agree():
    left_formula, right_formula = x**2, 2 * x

    def f(v, at_two=0):
        return v * v if v < 2 else (at_two if v == 2 else 2 * v)

    # Step 1: f(2) = 0, from the middle line, and f is defined at every real number.
    assert f(2) == 0
    # The one-sided limits, by sp.limit on the formula of each side (not on the Piecewise, which
    # SymPy 1.14 gets wrong here) and, independently, by substituting into the polynomial.
    assert limit_is(left_formula, x, 2, 4, dir="-")
    assert limit_is(right_formula, x, 2, 4, dir="+")
    assert equal(left_formula.subs(x, 2), 4) and equal(right_formula.subs(x, 2), 4)
    # Step 2: |x² − 4| = |x − 2||x + 2|; 1 < x < 2 gives 3 < x + 2 < 4, so |x + 2| < 4 there.
    assert equal(sp.Abs(x**2 - 4), sp.Abs(x - 2) * sp.Abs(x + 2))
    assert equal(sp.imageset(sp.Lambda(x, x + 2), sp.Interval.open(1, 2)), sp.Interval.open(3, 4))
    assert empty_on(sp.Abs(x + 2) >= 4, x, sp.Interval.open(1, 2))
    # On that half-window |x² − 4| < 4|x − 2| (and without abs: 4 − x² − 4(2 − x) = −(x − 2)² < 0).
    assert empty_on(sp.Abs(x**2 - 4) >= 4 * sp.Abs(x - 2), x, sp.Interval.open(1, 2))
    assert equal((4 - x**2) - 4 * (2 - x), -((x - 2) ** 2))
    # Step 3, δ = min(1, ε/4), branch by branch: on a left half-window of width d ≤ 1, x² is
    # increasing, so |x² − 4| = 4 − x² < 4 − (2 − d)² = 4d − d²; the implication holds iff 4d − d² ≤ ε.
    assert equal(4 - (2 - delta) ** 2, 4 * delta - delta**2)
    sup = lambda d: 4 * d - d**2  # noqa: E731
    assert empty_on(sup(eps / 4) > eps, eps, sp.Interval.Lopen(0, 4))   # branch ε ≤ 4: δ = ε/4
    assert empty_on(sup(1) > eps, eps, sp.Interval(4, sp.oo))          # branch ε ≥ 4: δ = 1
    # δ ≤ 1 gives 2 − δ ≥ 1, so the half-window lies in (1, 2).
    # (Checked on each branch of the min: 2 − 1 = 1, and 2 − ε/4 ≥ 1 for ε ≤ 4.)
    assert equal(2 - sp.Min(1, eps / 4).subs(eps, 4), 1)
    assert empty_on(2 - eps / 4 < 1, eps, sp.Interval.Lopen(0, 4))
    # The implication on exact pairs, both branches and the break ε = 4; f(2) plays no part:
    # the same holds whatever value f has at 2.
    for at_two in (0, 4, -10**6):
        assert one_sided_holds(lambda v: f(v, at_two), 2, 4, lambda e: min(Q(1), e / 4), eps_samples(1, breaks=[4]), -1)
    # Step 4: for x > 2, |2x − 4| = 2|x − 2| = 2(x − 2); δ = ε/2, and sup 2(x − 2) on the window is ε.
    p = sp.Symbol("p", positive=True)          # p = x − 2 > 0
    assert equal(sp.Abs(2 * (2 + p) - 4), 2 * sp.Abs(p)) and equal(2 * sp.Abs(p), 2 * p)
    assert equal(2 * (eps / 2), eps)
    for at_two in (0, 4, 7):
        assert one_sided_holds(lambda v: f(v, at_two), 2, 4, lambda e: e / 2, eps_samples(2), 1)
    # Step 5: both one-sided limits are 4, so the limit is 4 (the theorem; its δ = min(δ₋, δ₊)
    # = min(1, ε/4, ε/2) on the whole punctured window), although f(2) = 0.
    assert two_sided_holds(f, 2, 4, lambda e: min(Q(1), e / 4, e / 2), eps_samples(3, breaks=[4]))
    assert limit_is(x**2, x, 2, 4) and limit_is(2 * x, x, 2, 4)
    assert not equal(sp.Integer(f(2)), 4)
    # Check: ε = 0.4: left δ = min(1, 0.1) = 0.1, x = 1.95 is in (1.9, 2), 1.95² = 3.8025 and
    # |3.8025 − 4| = 0.1975 < 0.4; right δ = 0.2, x = 2.15 is in (2, 2.2), |4.3 − 4| = 0.3 < 0.4.
    e = sp.Rational(4, 10)
    assert equal(sp.Min(1, e / 4), sp.Rational(1, 10)) and equal(e / 2, sp.Rational(2, 10))
    x1, x2 = sp.Rational(195, 100), sp.Rational(215, 100)
    assert sp.Rational(19, 10) < x1 < 2 and 2 < x2 < sp.Rational(22, 10)
    assert equal(x1**2, sp.Rational(38025, 10**4))
    assert equal(sp.Abs(x1**2 - 4), sp.Rational(1975, 10**4)) and sp.Rational(1975, 10**4) < e
    assert equal(2 * x2, sp.Rational(43, 10)) and equal(sp.Abs(2 * x2 - 4), sp.Rational(3, 10)) and sp.Rational(3, 10) < e
    # On the left the cap gives |x + 2| < 4 (sup 4 on (1, 2)); the two-sided window 0 < |x − 2| < 1
    # only gives |x + 2| < 5 (sup 5 on (1, 3)).
    assert equal(sp.imageset(sp.Lambda(x, x + 2), sp.Interval.open(1, 3)), sp.Interval.open(3, 5))


@covers("eg-calc-one-sided-limits-parcel")
def test_eg_calc_one_sided_limits_parcel():
    def P(v, at_two=3):
        if 0 < v < 2:
            return 3
        if v == 2:
            return at_two
        if 2 < v <= 10:
            return 5
        return undefined()

    # Step 1: P(2) = 3, from the first line (0 < w ≤ 2); P is defined on (0, 10], which contains
    # the open interval (0, 10) around 2.
    assert P(2) == 3
    assert sp.Interval.open(0, 10).is_subset(sp.Interval.Lopen(0, 10)) and sp.Interval.open(0, 10).contains(2)
    # Steps 2, 3: the formula of each side is a constant on the half-windows of δ = 1, which lie
    # inside (0, 2] and (2, 10] (the first and second lines of the price list).
    assert sp.Interval.open(1, 2).is_subset(sp.Interval.Lopen(0, 2))
    assert sp.Interval.open(2, 3).is_subset(sp.Interval.Lopen(2, 10))
    left = sp.limit(sp.Integer(3), w, 2, "-")
    right = sp.limit(sp.Integer(5), w, 2, "+")
    assert limit_is(sp.Integer(3), w, 2, left, dir="-") and equal(left, 3)
    assert limit_is(sp.Integer(5), w, 2, right, dir="+") and equal(right, 5)
    # δ = 1 works for every ε, and the value at 2 plays no part: the same with P(2) = 5 (the
    # price list with "0 < w < 2" on its first line) or any other value.
    for at_two in (3, 5, -1):
        assert one_sided_holds(lambda v: P(v, at_two), 2, 3, lambda _: Q(1), eps_samples(4), -1)
        assert one_sided_holds(lambda v: P(v, at_two), 2, 5, lambda _: Q(1), eps_samples(5), 1)
    # Step 4: 3 ≠ 5, so the limit does not exist; directly: no L is within 1 of both 3 and 5,
    # and every window 0 < |w − 2| < δ holds the points 2 ∓ ½min(δ, 1), with prices 3 and 5.
    assert not equal(left, right)
    assert no_common_limit(left, right)
    for d in [Q(1, 10**9), Q(1, 2), Q(1), Q(5), Q(10**6)]:
        h = min(d, Q(1)) / 2
        assert 0 < h < d and P(2 - h) == 3 and P(2 + h) == 5
    # Step 5: the jump is 5 − 3 = 2 (pounds).
    assert equal(right - left, 2)
    # Check: P(1.999) = 3 and P(2.001) = 5, 2 apart.
    assert P(Q(1999, 1000)) == 3 and P(Q(2001, 1000)) == 5
    assert equal(sp.Integer(P(Q(2001, 1000)) - P(Q(1999, 1000))), 2)
    # ... the widget found a δ on the right for ε = 0.5, and none on the left, where every value is
    # 3, at distance 2 ≥ 0.5 from 5 (test_figure_parcel_widget has the widget's claims).
    assert equal(sp.Abs(3 - 5), 2) and sp.Integer(2) >= sp.Rational(1, 2)


@covers("eg-calc-one-sided-limits-sqrt")
def test_eg_calc_one_sided_limits_sqrt():
    q, p = sp.Symbol("q", negative=True), sp.Symbol("p", positive=True)
    # The domain: √x is real for x ≥ 0 and for no x < 0; (0, 1) and every half-window (0, δ) lie
    # in [0, ∞).
    assert sp.sqrt(q).is_real is False and sp.sqrt(p).is_real and sp.sqrt(sp.Integer(0)).is_real
    assert sp.Interval.open(0, 1).is_subset(sp.Interval(0, sp.oo))
    assert open_inside(0, delta, 0, sp.oo)
    # The right-hand limit: sp.limit, and the value at 0 of √x (which is 0) as a second route.
    assert limit_is(sp.sqrt(x), x, 0, 0, dir="+")
    assert equal(sp.sqrt(sp.Integer(0)), 0)
    # Step 1: for x > 0, |√x − 0| = √x, and √x < ε exactly when x < ε² (solved for x > 0; and
    # without the square root: both sides non-negative, so compare squares, (√p)² = p).
    assert equal(sp.Abs(sp.sqrt(p) - 0), sp.sqrt(p))
    # (SymPy cannot solve it for a symbolic ε, so for exact ones from 10⁻⁹ to 10⁶.)
    for e in (sp.Rational(1, 10**9), sp.Rational(1, 10), sp.Rational(7, 3), sp.Integer(10**6)):
        assert equal(sp.solveset(sp.sqrt(x) < e, x, sp.Interval.open(0, sp.oo)), sp.Interval.open(0, e**2))
    assert equal(sp.sqrt(p) ** 2, p) and equal(eps**2, eps * eps)
    # Step 2: δ = ε² > 0, and it is the largest: x = ε² gives √x = ε exactly.
    assert (eps**2).is_positive
    assert equal(sp.sqrt(eps**2), eps)
    # Step 3: the implication on exact pairs (SymPy decides each √ comparison exactly).
    rng = random.Random(6)
    for e in eps_samples(6, count=40):
        er = R(e)
        for xv in half_window(Q(0), e * e, 1, rng, count=8):
            assert xv > 0                                           # in the domain
            assert (sp.Abs(sp.sqrt(R(xv)) - 0) < er) is sp.true, (e, xv)
    # Step 4: no interval (−r, 0) lies in the domain: its point −r/2 has no real square root.
    rr = sp.Symbol("r", positive=True)
    assert sp.sqrt(-rr / 2).is_real is False
    # Check: ε = 0.1: δ = 0.01; x = 0.0081 gives √x = 0.09 < 0.1; x = 0.01 gives exactly 0.1.
    e = sp.Rational(1, 10)
    assert equal(e**2, sp.Rational(1, 100))
    assert sp.Rational(81, 10**4) < e**2
    assert equal(sp.sqrt(sp.Rational(81, 10**4)), sp.Rational(9, 100)) and sp.Rational(9, 100) < e
    assert equal(sp.sqrt(sp.Rational(1, 100)), e)


# ── Exercises ─────────────────────────────────────────────────────────────────


@covers("exr-calc-one-sided-limits-abs-over-x")
def test_exr_calc_one_sided_limits_abs_over_x():
    f = sp.Abs(x) / x
    q, p = sp.Symbol("q", negative=True), sp.Symbol("p", positive=True)
    # The formula on each side: |x| = −x for x < 0 and x for x > 0, so f = −1 and f = 1 there.
    left_formula, right_formula = f.subs(x, q), f.subs(x, p)
    assert equal(left_formula, -1) and equal(right_formula, 1)
    # sp.limit on each side agrees with those formulas.
    assert limit_is(f, x, 0, left_formula, dir="-")
    assert limit_is(f, x, 0, right_formula, dir="+")
    # f is defined on (−1, 0) and on (0, 1) (only 0 is excluded), and δ = 1 works on each side.
    assert equal(sp.calculus.util.continuous_domain(f, x, sp.S.Reals), sp.S.Reals - sp.FiniteSet(0))
    g = lambda v: abs(v) / v  # noqa: E731
    assert one_sided_holds(g, 0, -1, lambda _: Q(1), eps_samples(7, count=50), -1)
    assert one_sided_holds(g, 0, 1, lambda _: Q(1), eps_samples(8, count=50), 1)
    got = answer("exr-calc-one-sided-limits-abs-over-x")
    assert equal(got, (left_formula, right_formula))
    # The solution: the limits differ, the two-sided limit does not exist, the jump is 2.
    assert no_common_limit(left_formula, right_formula)
    with pytest.raises(ValueError):
        sp.limit(f, x, 0, "+-")
    assert equal(right_formula - left_formula, 2)


@covers("exr-calc-one-sided-limits-piecewise")
def test_exr_calc_one_sided_limits_piecewise():
    left_formula, right_formula = 2 * x + 1, 4 - x

    def f(v, at_one=0):
        return 2 * v + 1 if v < 1 else (at_one if v == 1 else 4 - v)

    # (a), (b): sp.limit on the formula of each side, and substitution into it (both polynomials).
    left = sp.limit(left_formula, x, 1, "-")
    right = sp.limit(right_formula, x, 1, "+")
    assert limit_is(left_formula, x, 1, left, dir="-") and equal(left, left_formula.subs(x, 1))
    assert limit_is(right_formula, x, 1, right, dir="+") and equal(right, right_formula.subs(x, 1))
    # (c) f(1) = 0, from the definition.
    value = f(1)
    # (d) both one-sided limits agree, so the limit is their common value (the theorem's δ = min).
    assert equal(left, right)
    # The solution's steps: |(2x + 1) − 3| = 2|x − 1|, δ = ε/2; |(4 − x) − 3| = |1 − x| = |x − 1|, δ = ε.
    assert equal(sp.Abs(left_formula - 3), 2 * sp.Abs(x - 1))
    assert equal(sp.Abs(right_formula - 3), sp.Abs(1 - x)) and equal(sp.Abs(1 - x), sp.Abs(x - 1))
    for at_one in (0, 3, 100):
        assert one_sided_holds(lambda v: f(v, at_one), 1, int(left), lambda e: e / 2, eps_samples(9, count=60), -1)
        assert one_sided_holds(lambda v: f(v, at_one), 1, int(right), lambda e: e, eps_samples(10, count=60), 1)
    assert two_sided_holds(f, 1, int(left), lambda e: min(e / 2, e), eps_samples(11, count=60))
    got = answer("exr-calc-one-sided-limits-piecewise")
    assert equal(got, (left, right, sp.Integer(value), left))
    assert not equal(sp.Integer(value), left)   # the value at 1 is not the limit


@covers("exr-calc-one-sided-limits-sqrt-shift")
def test_exr_calc_one_sided_limits_sqrt_shift():
    f, e = sp.sqrt(x - 3), sp.Rational(1, 10)
    # The domain: x ≥ 3; every x < 3 gives a non-real square root.
    assert sp.sqrt(sp.Symbol("q", negative=True)).is_real is False
    assert limit_is(f, x, 3, 0, dir="+")
    # The good set for x > 3, solved with the square root, and again by squaring (both sides
    # non-negative): x − 3 < 0.01.
    good = sp.solveset(f < e, x, sp.Interval.open(3, sp.oo))
    assert equal(good, sp.solveset(x - 3 < e**2, x, sp.Interval.open(3, sp.oo)))
    assert isinstance(good, sp.Interval) and equal(good.inf, 3)
    largest = good.sup - 3
    got = answer("exr-calc-one-sided-limits-sqrt-shift")
    assert equal(got, largest)
    # It works, exactly, up to the edge of the half-window ...
    rng = random.Random(12)
    d = Q(str(got))
    for xv in half_window(Q(3), d, 1, rng, count=300):
        assert xv > 3 and (sp.sqrt(R(xv) - 3) < e) is sp.true
    # ... and no larger δ does: x = 3 + δ is in every larger half-window, and there √(x − 3) = 0.1.
    assert equal(f.subs(x, 3 + got), e)
    assert equal(3 + got, sp.Rational(301, 100))


@covers("exr-calc-one-sided-limits-claim")
def test_exr_calc_one_sided_limits_claim():
    # A counterexample (the solution's H; a Heaviside or Piecewise would trip SymPy 1.14's limit,
    # so each side is its constant formula): H = 0 for x < 0, 1 for x ≥ 0, defined everywhere.
    def H(v):
        return 0 if v < 0 else 1

    a = 0
    assert H(a) == 1
    right = sp.limit(sp.Integer(1), x, 0, "+")
    left = sp.limit(sp.Integer(0), x, 0, "-")
    assert limit_is(sp.Integer(1), x, 0, right, dir="+") and limit_is(sp.Integer(0), x, 0, left, dir="-")
    assert one_sided_holds(H, 0, 1, lambda _: Q(1), eps_samples(13, count=50), 1)
    assert one_sided_holds(H, 0, 0, lambda _: Q(1), eps_samples(14, count=50), -1)
    hypothesis = equal(right, H(a))            # lim_{x→0+} H(x) = H(0)
    # The conclusion fails: lim_{x→0} H(x) = H(0) = 1 fails the round ε = ½, since every window
    # holds x = −δ/2 with |H(x) − 1| = 1; and no number at all is within ½ of both 0 and 1.
    rng = random.Random(15)
    for d in [Q(1, 10**9), Q(1), Q(10**6)] + [Q(rng.randint(1, 10**9), N) for _ in range(100)]:
        assert 0 < abs(-d / 2 - a) < d and abs(H(-d / 2) - H(a)) >= Q(1, 2)
    assert no_common_limit(left, right)
    claim = not hypothesis                     # a counterexample makes the claim false
    got = answer("exr-calc-one-sided-limits-claim")
    assert equal(got, sp.true if claim else sp.false)


@covers("exr-calc-one-sided-limits-largest-delta")
def test_exr_calc_one_sided_limits_largest_delta():
    e, lim = sp.Rational(3, 100), 5
    left_formula, right_formula = x + 3, 3 * x - 1

    def g(v):
        return v + 3 if v < 2 else 3 * v - 1

    # Both one-sided limits are 5 (and g(2) = 5).
    assert limit_is(left_formula, x, 2, lim, dir="-") and limit_is(right_formula, x, 2, lim, dir="+")
    assert g(2) == 5
    # The good sets on each side, by solveset with abs and, without abs, from the sign of x − 2
    # (solveset with abs is not trusted alone).
    right_good = sp.solveset(sp.Abs(right_formula - lim) < e, x, sp.Interval.open(2, sp.oo))
    left_good = sp.solveset(sp.Abs(left_formula - lim) < e, x, sp.Interval.open(-sp.oo, 2))
    assert equal(right_good, sp.solveset(3 * x - 6 < e, x, sp.Interval.open(2, sp.oo)))
    assert equal(left_good, sp.solveset(2 - x < e, x, sp.Interval.open(-sp.oo, 2)))
    assert equal(right_good.inf, 2) and equal(left_good.sup, 2)
    d_right = right_good.sup - 2
    d_left = 2 - left_good.inf
    d_both = sp.Min(d_left, d_right)
    # The solution's steps: |3x − 6| = 3|x − 2|, |x − 2| for the left; equality at 2.01 and 1.97.
    assert equal(sp.Abs(3 * x - 6), 3 * sp.Abs(x - 2))
    assert equal(sp.Abs(g(sp.Rational(201, 100)) - lim), e) and equal(sp.Abs(g(sp.Rational(197, 100)) - lim), e)
    got = answer("exr-calc-one-sided-limits-largest-delta")
    assert equal(got, (d_right, d_left, d_both))
    # Each δ works, exactly up to the edge; (c) on the whole punctured window.
    assert one_sided_holds(g, 2, lim, lambda _: Q(str(d_right)), [Q(3, 100)], 1, count=2000)
    assert one_sided_holds(g, 2, lim, lambda _: Q(str(d_left)), [Q(3, 100)], -1, count=2000)
    assert two_sided_holds(g, 2, lim, lambda _: Q(str(d_both)), [Q(3, 100)], count=2000)
    # No larger δ on the right, nor for (c): every larger window contains x = 2 + δ₊.
    assert equal(sp.Abs(right_formula.subs(x, 2 + d_right) - lim), e)


@covers("exr-calc-one-sided-limits-parking")
def test_exr_calc_one_sided_limits_parking():
    def C(v):
        if 0 < v <= 1:
            return 2
        if 1 < v <= 2:
            return 4
        if 2 < v <= 3:
            return 6
        return undefined()

    # The half-windows of δ = 1, (0, 1) and (1, 2), lie in the lines 0 < t ≤ 1 and 1 < t ≤ 2,
    # where C is the constant 2 and 4.
    assert sp.Interval.open(0, 1).is_subset(sp.Interval.Lopen(0, 1))
    assert sp.Interval.open(1, 2).is_subset(sp.Interval.Lopen(1, 2))
    left = sp.limit(sp.Integer(C(Q(1, 2))), t, 1, "-")
    right = sp.limit(sp.Integer(C(Q(3, 2))), t, 1, "+")
    assert limit_is(sp.Integer(2), t, 1, left, dir="-") and limit_is(sp.Integer(4), t, 1, right, dir="+")
    assert one_sided_holds(C, 1, int(left), lambda _: Q(1), eps_samples(16, count=50), -1)
    assert one_sided_holds(C, 1, int(right), lambda _: Q(1), eps_samples(17, count=50), 1)
    # C(1) = 2 (first line) plays no part; the limit at 1 does not exist.
    assert C(1) == 2
    assert no_common_limit(left, right)
    got = answer("exr-calc-one-sided-limits-parking")
    assert equal(got, (left, right, right - left))


@covers("exr-calc-one-sided-limits-parameter")
def test_exr_calc_one_sided_limits_parameter():
    left = sp.limit(c * x + 1, x, 1, "-")
    right = sp.limit(5 - 2 * x, x, 1, "+")
    assert equal(left, (c * x + 1).subs(x, 1)) and equal(right, (5 - 2 * x).subs(x, 1))
    assert limit_is(5 - 2 * x, x, 1, right, dir="+")
    # The limit exists iff the one-sided limits agree (f(1) = 7 plays no part).
    solutions = sp.solveset(sp.Eq(left, right), c, sp.S.Reals)
    assert isinstance(solutions, sp.FiniteSet) and len(solutions) == 1
    (c0,) = tuple(solutions)
    got = answer("exr-calc-one-sided-limits-parameter")
    assert equal(got, c0)
    # The solution's steps: |(5 − 2x) − 3| = 2|x − 1|; |(cx + 1) − (c + 1)| = |c||x − 1|.
    assert equal(sp.Abs((5 - 2 * x) - 3), 2 * sp.Abs(x - 1))
    assert equal(sp.Abs((c * x + 1) - (c + 1)), sp.Abs(c) * sp.Abs(x - 1))
    for cv in (Q(0), Q(2), Q(-3), Q(1, 7), Q(10**3)):
        def f(v, cv=cv):
            return cv * v + 1 if v < 1 else (7 if v == 1 else 5 - 2 * v)

        assert limit_is(R(cv) * x + 1, x, 1, R(cv) + 1, dir="-")
        choose = (lambda _: Q(1)) if cv == 0 else (lambda e, cv=cv: e / abs(cv))
        assert one_sided_holds(f, 1, cv + 1, choose, eps_samples(18, count=30), -1, count=10)
        assert one_sided_holds(f, 1, 3, lambda e: e / 2, eps_samples(19, count=30), 1, count=10)
        if equal(R(cv), c0):
            assert two_sided_holds(f, 1, 3, lambda e, cv=cv: min(e / abs(cv), e / 2), eps_samples(20, count=30), count=10)
        else:
            assert no_common_limit(R(cv) + 1, right)


@covers("exr-calc-one-sided-limits-widget-eps")
def test_exr_calc_one_sided_limits_widget_eps():
    def P(v):
        if 0 < v <= 2:
            return 3
        if 2 < v <= 10:
            return 5
        return undefined()

    # On every left half-window with δ ≤ 2, P = 3 (first line), so |P(w) − 5| = 2 throughout;
    # a δ > 2 lets in w ≤ 0, outside the domain (0, 10], and fails.
    assert sp.Interval.open(0, 2).is_subset(sp.Interval.Lopen(0, 2))
    assert not sp.Interval.Lopen(0, 10).contains(0)
    dist = sp.Abs(3 - 5)
    # A δ exists iff that constant distance is < ε.
    expected = sp.solveset(dist < eps, eps, sp.Interval.open(0, sp.oo))
    got = answer("exr-calc-one-sided-limits-widget-eps")
    assert equal(got, expected)
    # Spot-check both directions on exact ε, including the break ε = 2 and its neighbours: for ε in
    # the set δ = 1 works; otherwise each δ has the point 2 − ½min(δ, 1) in its half-window, failing.
    rng = random.Random(21)
    for e in eps_samples(21, count=100, breaks=[2]):
        inside = expected.contains(R(e)) is sp.true
        if inside:
            assert one_sided_holds(P, 2, 5, lambda _: Q(1), [e], -1, count=20)
        else:
            for d in [Q(1, 10**9), Q(1), Q(2)] + [Q(rng.randint(1, 2 * N), N) for _ in range(20)]:
                pt = 2 - min(d, Q(1)) / 2
                assert 1 < pt < 2 and 2 - d < pt
                assert abs(P(pt) - 5) >= e
    # The solution's slider: 0.1, 0.2, …, 2.5; the left side has a δ exactly from ε = 2.1 on.
    slider = [sp.Rational(k, 10) for k in range(1, 26)]
    found = [v for v in slider if expected.contains(v) is sp.true]
    assert equal(found[0], sp.Rational(21, 10)) and equal(found[-1], sp.Rational(5, 2))
    assert expected.contains(2) is sp.false
    assert limit_is(sp.Integer(3), w, 2, 3, dir="-")   # from the left the limit is 3, not 5


@covers("exr-calc-one-sided-limits-reciprocal")
def test_exr_calc_one_sided_limits_reciprocal():
    q, p = sp.Symbol("q", negative=True), sp.Symbol("p", positive=True)
    # SymPy: 1/x → +∞ as x → 0+, so no real number is the right-hand limit.
    assert limit_is(1 / x, x, 0, sp.oo, dir="+")
    # (0, 1) lies in the domain ℝ \ {0}.
    assert equal(sp.calculus.util.continuous_domain(1 / x, x, sp.S.Reals), sp.S.Reals - sp.FiniteSet(0))
    # The solution's witness x = min(δ/2, 1/(|L| + 2)) with ε = 1, on many exact (L, δ): in the
    # half-window, and 1/x − L ≥ 1/x − |L| ≥ 2, so |1/x − L| > 1.
    # Property 3, L ≤ |L|: |L| − L is 0 for L ≥ 0 and −2L > 0 for L < 0.
    assert equal(sp.Abs(p) - p, 0) and equal(sp.Abs(sp.Integer(0)), 0)
    assert equal(sp.Abs(q) - q, -2 * q) and (-2 * q).is_positive
    rng = random.Random(22)
    Ls = [Q(0), Q(1), Q(-1), Q(10**6), Q(-10**6)] + [Q(rng.randint(-10**8, 10**8), 1000) for _ in range(300)]
    ds = [Q(10**6), Q(1), Q(1, 10**9)] + [Q(rng.randint(1, 10**9), N) for _ in range(30)]
    every_L_fails = True
    for lv in Ls:
        for d in ds:
            xv = min(d / 2, 1 / (abs(lv) + 2))
            assert 0 < xv < d
            assert 1 / xv >= abs(lv) + 2
            assert 1 / xv - lv >= 1 / xv - abs(lv) >= 2
            if not abs(1 / xv - lv) >= 1:
                every_L_fails = False
    got = answer("exr-calc-one-sided-limits-reciprocal")
    assert equal(got, sp.false if every_L_fails else sp.true)


@covers("exr-calc-one-sided-limits-reciprocal-left")
def test_exr_calc_one_sided_limits_reciprocal_left():
    # A manual answer (a proof): its key claims are checked here; it counts as covered only
    # through a reviewer's note in maths.manual_checked.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-one-sided-limits-reciprocal-left")
    assert limit_is(1 / x, x, 1, 1, dir="-")
    # Scratch work: 1/x − 1 = (1 − x)/x, positive on (0, 1); 1/x < 2 on (½, 1); so on (½, 1)
    # |1/x − 1| < 2(1 − x).
    assert equal(1 / x - 1, (1 - x) / x)
    assert empty_on((1 - x) / x <= 0, x, sp.Interval.open(0, 1))
    assert empty_on(1 / x >= 2, x, sp.Interval.open(sp.Rational(1, 2), 1))
    assert empty_on((1 - x) / x >= 2 * (1 - x), x, sp.Interval.open(sp.Rational(1, 2), 1))
    # δ = min(½, ε/2), branch by branch: 1/x − 1 decreases on (0, 1), so on a left half-window of
    # width d ≤ ½ its sup is 1/(1 − d) − 1 = d/(1 − d); the implication holds iff d/(1 − d) ≤ ε.
    assert equal(1 / (1 - delta) - 1, delta / (1 - delta))
    sup = lambda d: d / (1 - d)  # noqa: E731
    assert empty_on(sup(eps / 2) > eps, eps, sp.Interval.Lopen(0, 1))   # branch ε ≤ 1: δ = ε/2
    assert empty_on(sup(sp.Rational(1, 2)) > eps, eps, sp.Interval(1, sp.oo))   # branch ε ≥ 1: δ = ½
    # δ ≤ ½ keeps the half-window inside (½, 1), in the domain.
    # (On each branch of the min: 1 − ½ = ½, and 1 − ε/2 ≥ ½ for ε ≤ 1.)
    assert equal(1 - sp.Min(sp.Rational(1, 2), eps / 2).subs(eps, 1), sp.Rational(1, 2))
    assert empty_on(1 - eps / 2 < sp.Rational(1, 2), eps, sp.Interval.Lopen(0, 1))
    assert one_sided_holds(lambda v: 1 / v, 1, 1, lambda e: min(Q(1, 2), e / 2), eps_samples(23, breaks=[1]), -1)
    # Why the cap: ε = 4 alone would give δ = 2, whose half-window (−1, 1) contains 0, where 1/x is
    # undefined.
    assert sp.Interval.open(1 - 2, 1).contains(0)


# ── Unlabelled claims: the definition, the remark, the theorem, the figure, the rigorous track ──


def test_definition_example_and_non_example():
    def g(v):
        return v if v <= 0 else v + 1

    # lim_{x→0+} g(x) = 1 with δ = ε (|g(x) − 1| = |x| = x for x > 0), and lim_{x→0−} g(x) = 0.
    p = sp.Symbol("p", positive=True)
    assert equal(sp.Abs((p + 1) - 1), p)
    assert limit_is(x + 1, x, 0, 1, dir="+") and limit_is(x, x, 0, 0, dir="-")
    assert one_sided_holds(g, 0, 1, lambda e: e, eps_samples(24), 1)
    assert one_sided_holds(g, 0, 0, lambda e: e, eps_samples(25), -1)
    # Non-example: g(0) = 0 is not the right-hand limit: ε = ½, d = ½min(δ, 1) is in (0, δ) and
    # |g(d) − 0| = d + 1 > 1 > ½. The same witness as in the rigorous track's negation.
    assert g(0) == 0
    rng = random.Random(26)
    for dv in [Q(10**6), Q(1), Q(1, 10**9)] + [Q(rng.randint(1, 10**7), N) for _ in range(300)]:
        d = min(dv, Q(1)) / 2
        assert 0 < d < dv
        assert abs(g(d) - 0) == d + 1 > 1 > Q(1, 2)
    # "Every δ ≤ r gives a half-window inside (a, a + r)."
    rr = sp.Symbol("r", positive=True)
    aa = sp.Symbol("a", real=True)
    d_ = sp.Symbol("d", positive=True)              # δ = r − d ≤ r
    assert open_inside(aa, aa + (rr - d_), aa, aa + rr)


def test_remark_one_sided_unique_computable_claims():
    # ε = ½|L − M| > 0 for L ≠ M, ε + ε = |L − M|, x = a ± δ/2 lies in the half-window, and no
    # number is within ε of both L and M.
    gap = sp.Symbol("g", positive=True)
    M = L + gap
    e = sp.Abs(L - M) / 2
    assert e.is_positive and equal(e + e, sp.Abs(L - M))
    aa = sp.Symbol("a", real=True)
    assert (aa < aa + delta / 2) is sp.true and (aa + delta / 2 < aa + delta) is sp.true
    assert (aa - delta < aa - delta / 2) is sp.true and (aa - delta / 2 < aa) is sp.true
    # δ = min(δ₁, δ₂): a + δ/2 is in both half-windows (exact samples).
    rng = random.Random(27)
    for _ in range(300):
        d1, d2 = Q(rng.randint(1, 10**7), N), Q(rng.randint(1, 10**7), N)
        d = min(d1, d2)
        assert 0 < d / 2 < d1 and d / 2 < d2
    sv = sp.Symbol("s", real=True)                 # f(x) = L + g·s
    assert equal(sp.Abs((L + gap * sv) - L), gap * sp.Abs(sv)) and equal(sp.Abs((L + gap * sv) - M), gap * sp.Abs(sv - 1))
    assert empty_on(sp.And(sp.Abs(sv) < sp.Rational(1, 2), sp.Abs(sv - 1) < sp.Rational(1, 2)), sv, sp.S.Reals)


def test_thm_calc_limit_iff_one_sided_computable_claims():
    # Part (e): the punctured window is the union of the two half-windows (solved with abs and
    # without it), for exact a and δ.
    for av, dv in ((2, sp.Rational(3, 100)), (0, 1), (-sp.Rational(7, 3), sp.Rational(1, 10**6))):
        halves = sp.Union(sp.Interval.open(av - dv, av), sp.Interval.open(av, av + dv))
        with_abs = sp.solveset(sp.Abs(x - av) < dv, x, sp.S.Reals) - sp.FiniteSet(av)
        no_abs = sp.Intersection(sp.solveset(x - av < dv, x, sp.S.Reals), sp.solveset(av - x < dv, x, sp.S.Reals)) - sp.FiniteSet(av)
        assert equal(with_abs, halves) and equal(no_abs, halves)
    # "The one-sided limits make sense": r = min(a − c, d − a) (or the one that occurs, or 1 for ℝ)
    # gives (a − r, a + r) inside I.
    cases = [(sp.Interval.open(0, 10), 2, 2), (sp.Interval.open(-sp.oo, 5), 2, 3),
             (sp.Interval.open(0, sp.oo), 1, 1), (sp.S.Reals, 0, 1), (sp.Interval.open(-1, 1), sp.Rational(9, 10), sp.Rational(1, 10))]
    for I, av, rv in cases:
        ends = [av - I.inf] if I.inf.is_finite else []
        ends += [I.sup - av] if I.sup.is_finite else []
        r_ = sp.Min(*ends) if ends else sp.Integer(1)
        assert equal(r_, rv) and r_.is_positive
        assert sp.Interval.open(av - r_, av + r_).is_subset(I)
    # "Only if": each half-window of δ lies in the punctured window of δ.
    aa = sp.Symbol("a", real=True)
    # (A point of either half-window has 0 < |x − a| < δ: |x − a| is u or −u with 0 < u < δ.)
    u_ = sp.Symbol("u", positive=True)
    assert equal(sp.Abs((aa + u_) - aa), u_) and equal(sp.Abs((aa - u_) - aa), u_)
    # "If": δ = min(δ₁, δ₂) > 0, and both halves of its window fit in the half-windows of δ₁ and δ₂
    # (exact samples, including δ₁ = δ₂ and very different sizes).
    rng = random.Random(28)
    pairs = [(Q(1), Q(1)), (Q(1, 10**9), Q(10**6)), (Q(3, 100), Q(1, 100))]
    pairs += [(Q(rng.randint(1, 10**7), N), Q(rng.randint(1, 10**7), N)) for _ in range(200)]
    for d1, d2 in pairs:
        d = min(d1, d2)
        assert d > 0
        assert sp.Interval.open(-R(d), 0).is_subset(sp.Interval.open(-R(d1), 0))
        assert sp.Interval.open(0, R(d)).is_subset(sp.Interval.open(0, R(d2)))
        assert -d1 <= -d                               # the multiplication by −1 in the proof
    # On the page's examples: the δ of each side, combined by min, wins the two-sided round.
    f = lambda v: v * v if v < 2 else 2 * v  # noqa: E731
    left_d, right_d = (lambda e: min(Q(1), e / 4)), (lambda e: e / 2)
    assert two_sided_holds(f, 2, 4, lambda e: min(left_d(e), right_d(e)), eps_samples(29, breaks=[4]))
    # Exercise largest-delta: δ₋ = 0.03, δ₊ = 0.01, and the min is the largest two-sided δ.
    assert equal(sp.Min(sp.Rational(3, 100), sp.Rational(1, 100)), sp.Rational(1, 100))


def test_figure_parcel_widget():
    # The widget's f = 4 + sign(x − 2) is the parcel price on (1, 2) and (2, 3) (it differs only
    # at 2, which the widget never uses: there 4 + sign(0) = 4, while P(2) = 3).
    q, p = sp.Symbol("q", negative=True), sp.Symbol("p", positive=True)
    fw = 4 + sp.sign(x - 2)
    assert equal(fw.subs(x, 2 + q), 3) and equal(fw.subs(x, 2 + p), 5)
    assert equal(fw.subs(x, 2), 4)
    a_, lim = 2, 5
    reach = min(a_ - 1, 3 - a_)                 # the search reaches the ends of xRange [1, 3]
    assert reach == 1
    # Slider: 0.1, 0.2, …, 2.5 in steps of 0.1, starting at 0.5 (on the grid: 0.1 + 4·0.1).
    slider = [sp.Rational(k, 10) for k in range(1, 26)]
    assert equal(slider[0], sp.Rational(1, 10)) and equal(slider[-1], sp.Rational(5, 2))
    assert equal(sp.Rational(1, 10) + 4 * sp.Rational(1, 10), sp.Rational(1, 2))

    def left_ok(e):   # a δ exists on the left for ε: every value there is 3 (and δ up to the reach)
        return sp.Abs(3 - lim) < e

    def right_ok(e):
        return sp.Abs(5 - lim) < e

    # Caption, ε = 0.5: on the right every value is in the band, out to the edge of the view (δ = 1);
    # on the left no δ: the values (3) leave the band at points as close to 2 as one likes.
    e = sp.Rational(1, 2)
    assert right_ok(e) is sp.true and left_ok(e) is sp.false
    assert one_sided_holds(lambda v: 4 + (1 if v > 2 else -1), 2, 5, lambda _: Q(reach), [Q(1, 2)], 1, count=200)
    for d in (Q(1, 10**12), Q(1, 10**6), Q(1)):
        assert abs((4 - 1) - 5) >= Q(1, 2) and 1 <= 2 - d / 2 < 2
    # Try this, step 1: the right side's values are within ε of 5. Step 2: the first slider value
    # with a δ on the left is 2.1; at 2.0 the distance 2 is not < 2.
    first = next(v for v in slider if left_ok(v) is sp.true)
    assert equal(first, sp.Rational(21, 10))
    assert left_ok(sp.Integer(2)) is sp.false
    # Step 3: from 2.1 on both sides have a δ, but ε = 0.5 (and every ε ≤ 2) has none on the left,
    # so the definition's "for every ε > 0" fails for L = 5 (the limit does not exist).
    assert all(left_ok(v) is sp.true and right_ok(v) is sp.true for v in slider if v >= first)
    assert no_common_limit(sp.Integer(3), sp.Integer(5))


def test_rigorous_track_sqrt_minus_x():
    # √(−x) is real exactly for x ≤ 0: no x of its domain has 0 < x < δ.
    q, p = sp.Symbol("q", negative=True), sp.Symbol("p", positive=True)
    assert sp.sqrt(-p).is_real is False and sp.sqrt(-q).is_real and sp.sqrt(sp.Integer(0)).is_real
    # From the left, lim √(−x) = 0 as x → 0−, with δ = ε², as in eg-calc-one-sided-limits-sqrt.
    assert limit_is(sp.sqrt(-x), x, 0, 0, dir="-")
    assert equal(sp.sqrt(-(-eps**2)), eps)
    rng = random.Random(30)
    for e in eps_samples(30, count=30):
        for xv in half_window(Q(0), e * e, -1, rng, count=6):
            assert xv < 0 and (sp.sqrt(-R(xv)) < R(e)) is sp.true
