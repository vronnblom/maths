"""Verification tests for content/calculus/limits/index.md (calc-limits-chapter).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps; the answers are read
with answer(label), as printed on the page (`\\infty` is read as sp.oo).

Each solution's displayed steps are asserted, not only its answer: the factorisations, the windows
on which a simplified formula agrees with the function, the one-sided limits, the identities, and
the inequalities. Limits are computed twice: by sp.limit through limit_is (which also checks a table
of values approaching the point) and from the simplified formula the solution reaches. Statements
"on a set" are checked by solveset on the whole set, and cross-checked at exact rational points
(fractions.Fraction, or SymPy's exact algebraic numbers where a root appears): floats could hide a
failure at the edge of a window.
"""

import random
from fractions import Fraction as Q

import mpmath
import pytest
import sympy as sp

from mathcheck import ManualAnswer, a, answer, b, covers, equal, equal_on_domain, limit_is, t, x

M = sp.Symbol("M", positive=True)
L = sp.Symbol("L", positive=True)
pos = sp.Symbol("p", positive=True)          # a positive number: x − c for x > c, or −x for x < 0
neg = sp.Symbol("q", negative=True)          # a negative number
N = 10**6


def punctured(c, r):
    """The set 0 < |x − c| < r, as SymPy's union of two open intervals."""
    return sp.Union(sp.Interval.open(c - r, c), sp.Interval.open(c, c + r))


def solved(condition, domain):
    """The set of x in `domain` where `condition` (an inequality) holds."""
    return sp.solveset(condition, x, domain)


def exact_points(c, r, rng, count=40):
    """Exact rational points of 0 < |x − c| < r: next to c, within 10⁻⁹·r of the edges, random."""
    fractions = [Q(1, 10**9), Q(1, N), Q(N - 1, N), Q(10**9 - 1, 10**9)]
    fractions += [Q(rng.randint(1, N - 1), N) for _ in range(count)]
    for fr in fractions:
        yield Q(c) + Q(r) * fr
        yield Q(c) - Q(r) * fr


# ── Review exercises ────────────────────────────────────────────────────────────────────────


@covers("exr-calc-limits-review-substitute-or-simplify")
def test_exr_calc_limits_review_substitute_or_simplify():
    p = x**2 + 2 * x - 3
    # (a) the denominator is 2 ≠ 0 at 1, and p(1)/q(1) = (1 + 2 − 3)/2 = 0.
    assert equal((x**2 + 1).subs(x, 1), 2) and equal(p.subs(x, 1), 1 + 2 - 3)
    assert equal(p.subs(x, 1) / (x**2 + 1).subs(x, 1), 0)
    assert limit_is(p / (x**2 + 1), x, 1, 0)
    # (b) both vanish at 1; the two factorisations.
    assert equal(p.subs(x, 1), 0) and equal((x**2 - 1).subs(x, 1), 1 - 1)
    assert equal(sp.expand((x - 1) * (x + 3)), p)
    assert equal(sp.expand((x - 1) * (x + 1)), x**2 - 1)
    # 0 < |x − 1| < 2 is −1 < x < 1 or 1 < x < 3 (part (e) of prop-calc-abs-interval), which
    # contains neither zero ±1 of x² − 1; there the quotient equals (x + 3)/(x + 1).
    window = punctured(1, 2)
    assert equal(solved(sp.Abs(x - 1) < 2, sp.S.Reals) - {1}, window)
    assert equal(sp.Intersection(sp.solveset(x**2 - 1, x, sp.S.Reals), window), sp.S.EmptySet)
    assert equal_on_domain(p / (x**2 - 1), (x + 3) / (x + 1), x, sp.Interval.open(-1, 1))
    assert equal_on_domain(p / (x**2 - 1), (x + 3) / (x + 1), x, sp.Interval.open(1, 3))
    # Direct substitution in (x + 3)/(x + 1): denominator 2 ≠ 0 at 1, value 4/2.
    assert equal((x + 1).subs(x, 1), 2) and equal(((x + 3) / (x + 1)).subs(x, 1), sp.Rational(4, 2))
    # The limits, from the original quotients (limit_is) and from the simplified one (above).
    expected = (sp.Integer(0), sp.Rational(4, 2))
    assert limit_is(p / (x**2 - 1), x, 1, expected[1])
    assert equal(answer("exr-calc-limits-review-substitute-or-simplify"), expected)


@covers("exr-calc-limits-review-sine-over-quadratic")
def test_exr_calc_limits_review_sine_over_quadratic():
    q = x**2 + 3 * x
    # x² + 3x = x(x + 3), zero exactly at 0 and −3.
    assert equal(sp.expand(x * (x + 3)), q)
    assert equal(sp.solveset(q, x, sp.S.Reals), sp.FiniteSet(0, -3))
    # sin x/(x² + 3x) = (sin x / x)·1/(x + 3) wherever x ≠ 0, −3 (both sides undefined at 0, −3).
    assert equal(sp.sin(x) / q - (sp.sin(x) / x) * (1 / (x + 3)), 0)
    for c in (0, -3):
        assert (sp.sin(x) / q).subs(x, c).has(sp.zoo, sp.nan)
        assert ((sp.sin(x) / x) * (1 / (x + 3))).subs(x, c).has(sp.zoo, sp.nan)
    # 0 < |x| < 3 contains neither zero.
    assert equal(sp.Intersection(sp.FiniteSet(0, -3), punctured(0, 3)), sp.S.EmptySet)
    # The factors' limits: sin x/x → 1 (thm-calc-sin-x-over-x), 1/(x + 3) → 1/3 (denominator 3).
    assert limit_is(sp.sin(x) / x, x, 0, 1)
    assert equal((x + 3).subs(x, 0), 3)
    assert limit_is(1 / (x + 3), x, 0, sp.Rational(1, 3))
    # The product law, and the limit of the original quotient by a second route.
    expected = 1 * sp.Rational(1, 3)
    assert limit_is(sp.sin(x) / q, x, 0, expected)
    assert equal(answer("exr-calc-limits-review-sine-over-quadratic"), expected)


@covers("exr-calc-limits-review-abs-quotient")
def test_exr_calc_limits_review_abs_quotient():
    f = (x**2 - 4) / sp.Abs(x - 2)
    assert equal(sp.expand((x - 2) * (x + 2)), x**2 - 4)
    # The signs of x − 2 on each side, and |x − 2| there (solveset on the whole half-line).
    right, left = sp.Interval.open(2, sp.oo), sp.Interval.open(-sp.oo, 2)
    assert equal(solved(x - 2 > 0, right), right) and equal(solved(x - 2 < 0, left), left)
    # equal_on_domain gives its variable only the sign of the domain (x > 0 on (2, ∞), not x > 2),
    # so the claims "for x > 2" and "for x < 2" are checked with x = 2 + p and x = 2 − p, p > 0.
    assert equal(sp.Abs(x - 2).subs(x, 2 + pos), (x - 2).subs(x, 2 + pos))
    assert equal(sp.Abs(x - 2).subs(x, 2 - pos), (-(x - 2)).subs(x, 2 - pos))
    # f = x + 2 for x > 2 and −(x + 2) for x < 2.
    assert equal(f.subs(x, 2 + pos), (x + 2).subs(x, 2 + pos))
    assert equal(f.subs(x, 2 - pos), (-(x + 2)).subs(x, 2 - pos))
    # The formulas' limits at 2 (direct substitution), and f's one-sided limits (SymPy on f with
    # its Abs, and the table of values).
    assert equal((x + 2).subs(x, 2), 4) and equal((-(x + 2)).subs(x, 2), -4)
    lim_left, lim_right = sp.Integer(-4), sp.Integer(4)
    assert limit_is(f, x, 2, lim_left, dir="-") and limit_is(f, x, 2, lim_right, dir="+")
    assert equal(answer("exr-calc-limits-review-abs-quotient"), (lim_left, lim_right))
    # The one-sided limits differ, so no limit; SymPy's two-sided limit agrees that there is none.
    assert not equal(lim_left, lim_right)
    with pytest.raises(ValueError):
        sp.limit(f, x, 2, "+-")
    # f is defined on (1, 3) except at 2, and the jump is 4 − (−4) = 8.
    rng = random.Random(3)
    for xv in exact_points(2, 1, rng):
        assert 1 < xv < 3 and xv != 2
        assert (xv * xv - 4) / abs(xv - 2) == (xv + 2 if xv > 2 else -(xv + 2))
    assert equal(lim_right - lim_left, 8)


@covers("exr-calc-limits-review-asymptotes")
def test_exr_calc_limits_review_asymptotes():
    num, den = 2 * x**2 + 2 * x, x**2 - 2 * x - 3
    f = num / den
    # The factorisations, the zeros of the denominator, and the cancelled form off −1, 3.
    assert equal(sp.expand(2 * x * (x + 1)), num) and equal(sp.expand((x + 1) * (x - 3)), den)
    zeros = sp.solveset(den, x, sp.S.Reals)
    assert equal(zeros, sp.FiniteSet(-1, 3))
    off = sp.Complement(sp.S.Reals, zeros)
    for piece in (sp.Interval.open(-sp.oo, -1), sp.Interval.open(-1, 3), sp.Interval.open(3, sp.oo)):
        assert equal(sp.Intersection(piece, off), piece)
        assert equal_on_domain(f, 2 * x / (x - 3), x, piece)

    # At 3: 2x ≥ 6 on (3, 4) (in fact > 6), 1/(x − 3) → ∞ from the right, so f → ∞ from the right.
    assert equal(solved(2 * x <= 6, sp.Interval.open(3, 4)), sp.S.EmptySet)
    assert limit_is(1 / (x - 3), x, 3, sp.oo, dir="+")
    assert limit_is(f, x, 3, sp.oo, dir="+")
    # The pole from the other side: f → −∞ as x → 3⁻ (2x → 6 > 0, 1/(x − 3) → −∞). The page
    # needs only one side for the asymptote; this checks the pole all the same.
    assert limit_is(f, x, 3, -sp.oo, dir="-")
    # The δ the page's propositions build for the right-hand limit (reciprocal power: min(1, 1/height);
    # product: height M/m with m = 6, then min with r = 1), checked at exact rational points.
    rng = random.Random(4)
    for mv in [Q(1, 1000), Q(1), Q(6), Q(1000), Q(10**9)] + [Q(rng.randint(1, 10**10), 1000) for _ in range(100)]:
        d = min(min(Q(1), 1 / (mv / 6)), Q(1))
        for fr in (Q(1, 10**9), Q(1, 2), Q(10**9 - 1, 10**9), Q(rng.randint(1, N - 1), N)):
            xv = 3 + d * fr
            assert (2 * xv * xv + 2 * xv) / (xv * xv - 2 * xv - 3) > mv

    # At −1: on 0 < |x + 1| < 1 (no zero 3 there) f = 2x/(x − 3), whose value at −1 is
    # (−2)/(−4) = 1/2; both one-sided limits are 1/2, so no vertical asymptote: a hole.
    window = punctured(-1, 1)
    assert equal(solved(sp.Abs(x + 1) < 1, sp.S.Reals) - {-1}, window)
    assert 3 not in window
    assert equal((x - 3).subs(x, -1), -4) and equal((2 * x).subs(x, -1), -2)
    hole = sp.Rational(-2, -4)
    assert equal((2 * x / (x - 3)).subs(x, -1), hole)
    assert limit_is(f, x, -1, hole, dir="+") and limit_is(f, x, -1, hole, dir="-")
    assert limit_is(f, x, -1, hole)
    assert f.subs(x, -1).has(sp.nan, sp.zoo)        # f itself is undefined at −1: a hole at (−1, 1/2)

    # Horizontal asymptotes: degrees 2 and 2, leading coefficients 2 and 1, so the limit 2/1 at ±∞.
    assert sp.degree(num, x) == 2 and sp.degree(den, x) == 2
    assert equal(sp.LC(num, x), 2) and equal(sp.LC(den, x), 1)
    horizontal = sp.Rational(2, 1)
    assert limit_is(f, x, sp.oo, horizontal) and limit_is(f, x, -sp.oo, horizontal)

    # (a): the zeros of the denominator at which a one-sided limit of f is ∞ or −∞, found by
    # SymPy's one-sided limits at each zero; (b): the set of finite limits at ±∞.
    vertical = {c for c in zeros if any(sp.limit(f, x, c, d).is_infinite for d in ("+", "-"))}
    assert vertical == {sp.Integer(3)}
    assert {sp.limit(f, x, sp.oo), sp.limit(f, x, -sp.oo)} == {horizontal}
    assert equal(answer("exr-calc-limits-review-asymptotes"), (sp.Integer(3), horizontal))


@covers("exr-calc-limits-review-root-and-factor")
def test_exr_calc_limits_review_root_and_factor():
    F = (sp.sqrt(x + 1) - 2) / (x**2 - 9)
    s = sp.sqrt(x + 1) + 2
    window = punctured(3, 1)
    # 0 < |x − 3| < 1 is 2 < x < 3 or 3 < x < 4; there x + 1 > 3 and x² − 9 = (x − 3)(x + 3) ≠ 0.
    assert equal(solved(sp.Abs(x - 3) < 1, sp.S.Reals) - {3}, window)
    assert equal(solved(x + 1 <= 3, window), sp.S.EmptySet)
    assert equal(sp.expand((x - 3) * (x + 3)), x**2 - 9)
    assert equal(sp.Intersection(sp.solveset(x**2 - 9, x, sp.S.Reals), window), sp.S.EmptySet)
    # s ≥ 2 > 0 there; and (√(x + 1))² = x + 1.
    assert equal(solved(s < 2, sp.Interval.open(2, 4)), sp.S.EmptySet)
    assert equal(sp.sqrt(x + 1).subs(x, 2 + pos) ** 2, (x + 1).subs(x, 2 + pos))
    # The displayed chain, each line equal to the next on both halves of the window.
    chain = [
        F,
        ((x + 1) - 4) / ((x**2 - 9) * s),
        (x - 3) / ((x - 3) * (x + 3) * s),
        1 / ((x + 3) * s),
    ]
    for lhs, rhs in zip(chain, chain[1:]):
        for half in (sp.Interval.open(2, 3), sp.Interval.open(3, 4)):
            assert equal_on_domain(lhs, rhs, x, half)
    assert equal((x + 1 - 4), x - 3)
    # The limits of the pieces as x → 3, and of the original function by a second route.
    assert limit_is(x + 1, x, 3, 4) and limit_is(x + 3, x, 3, 6)
    assert equal(sp.sqrt(4), 2) and limit_is(sp.sqrt(x + 1), x, 3, 2)
    assert limit_is(s, x, 3, 4)
    assert limit_is((x + 3) * s, x, 3, 6 * 4)
    expected = sp.Rational(1, 6 * 4)
    assert limit_is(1 / ((x + 3) * s), x, 3, expected)
    assert limit_is(F, x, 3, expected)
    assert equal(answer("exr-calc-limits-review-root-and-factor"), expected)


@covers("exr-calc-limits-review-oscillation-over-sine")
def test_exr_calc_limits_review_oscillation_over_sine():
    F = x**2 * sp.sin(1 / x) / sp.sin(x)
    half = sp.Interval.open(0, sp.pi / 2)
    # cos x > 0 on (0, π/2), and cos(−x) = cos x.
    assert equal(solved(sp.cos(x) <= 0, half), sp.S.EmptySet)
    assert equal(sp.cos(-x), sp.cos(x))
    # cos x < sin x / x on (0, π/2): g = sin x − x cos x has g(0) = 0 and g' = x sin x > 0 there,
    # so g > 0 and, dividing by x > 0, sin x / x − cos x > 0. Both sides are even, so the same
    # holds on (−π/2, 0). (SymPy's solveset cannot do the transcendental inequality itself; a
    # 60-digit sample, right up to both edges, is the second route.)
    g = sp.sin(x) - x * sp.cos(x)
    assert equal(g.subs(x, 0), 0) and equal(sp.diff(g, x), x * sp.sin(x))
    assert equal(solved(sp.sin(x) <= 0, half), sp.S.EmptySet)
    assert equal((sp.sin(x) / x).subs(x, -x), sp.sin(x) / x)
    # The rewriting F = 1/(sin x / x) · x sin(1/x) wherever both are defined.
    assert equal(F - (1 / (sp.sin(x) / x)) * x * sp.sin(1 / x), 0)
    # |x sin(1/x) − 0| = |x| |sin(1/x)| ≤ |x|: sin takes values in [−1, 1] on the reals (SymPy's
    # function_range), and 1/x is real for x ≠ 0.
    assert equal(sp.Abs(x * sp.sin(1 / x) - 0), sp.Abs(x) * sp.Abs(sp.sin(1 / x)))
    assert equal(sp.calculus.util.function_range(sp.sin(x), x, sp.S.Reals), sp.Interval(-1, 1))
    assert (1 / pos).is_real and (1 / neg).is_real
    # The bound on F itself, on the window of the solution: for 0 < |x| < π/2,
    #   |F(x)| = |x / sin x| · |x sin(1/x)| < (1/cos x) · |x|,
    # from 0 < cos x < sin x / x and |x sin(1/x)| ≤ |x|. Checked at 60 digits at sample points of
    # both halves, near 0 and within 10⁻⁹ of ±π/2, together with cos x < sin x / x and the steps.
    rng = random.Random(6)
    with mpmath.workdps(60):
        edge = mpmath.pi / 2
        fracs = [mpmath.mpf(10) ** -k for k in range(1, 13)] + [1 - mpmath.mpf(10) ** -k for k in range(1, 10)]
        fracs += [mpmath.mpf(rng.random()) for _ in range(300)]
        for fr in fracs:
            for xv in (edge * fr, -edge * fr):
                c, sx = mpmath.cos(xv), mpmath.sin(xv)
                Fv = xv**2 * mpmath.sin(1 / xv) / sx
                assert c > 0 and c < sx / xv and sx != 0
                assert abs(xv * mpmath.sin(1 / xv)) <= abs(xv)
                assert abs(Fv) <= abs(xv) / c, f"x = {xv}: |F| = {abs(Fv)}, |x|/cos x = {abs(xv) / c}"
    # The bound tends to 0, so it squeezes F to 0 (a second route to the answer).
    assert limit_is(sp.Abs(x) / sp.cos(x), x, 0, 0)
    # The factors' limits, and the product.
    assert limit_is(1 / (sp.sin(x) / x), x, 0, 1)
    assert limit_is(sp.Abs(x), x, 0, 0)
    assert limit_is(x * sp.sin(1 / x), x, 0, 0)
    expected = sp.Integer(1 * 0)
    # The original quotient, by SymPy and the table of values (a third route).
    assert limit_is(F, x, 0, expected)
    assert equal(answer("exr-calc-limits-review-oscillation-over-sine"), expected)


@covers("exr-calc-limits-review-average-cost")
def test_exr_calc_limits_review_average_cost():
    # The model, from the statement: 3600 euros fixed plus 8 euros per kilogram, over x kilograms.
    A = (3600 + 8 * x) / x
    assert equal(A, (8 * x + 3600) / x)
    half_line = sp.Interval.open(0, sp.oo)
    # (a) numerator and denominator of degree 1, leading coefficients 8 and 1: the limit is 8/1.
    assert sp.degree(8 * x + 3600, x) == 1 and sp.degree(x, x) == 1
    assert sp.LC(8 * x + 3600, x) == 8 and sp.LC(x, x) == 1
    limit = sp.Rational(8, 1)
    assert limit_is(A, x, sp.oo, limit)
    # The interpretation: the limit is the cost of one more kilogram.
    assert equal(sp.diff(3600 + 8 * x, x), limit)
    # (b) on x > 0: A < 10 ⇔ 8x + 3600 < 10x ⇔ 3600 < 2x ⇔ x > 1800, each as a set of x > 0.
    sets = [solved(cond, half_line) for cond in
            (A < 10, 8 * x + 3600 < 10 * x, 3600 < 2 * x, x > 1800)]
    for one in sets:
        assert equal(one, sets[0])
    below = sets[0]
    # The smallest N: "A(x) < 10 for every x > N" holds exactly when (N, ∞) misses the set where
    # A(x) ≥ 10 (x > 0), i.e. when N ≥ its supremum s; if s is attained, x = s defeats every
    # N < s. So the smallest N is s.
    not_below = solved(A >= 10, half_line)
    assert equal(sp.Union(below, not_below), half_line)
    assert equal(sp.Intersection(below, not_below), sp.S.EmptySet)
    smallest = not_below.sup
    assert smallest in not_below
    assert equal(below, sp.Interval.open(smallest, sp.oo))
    assert equal(A.subs(x, smallest), 10)
    # The page's A(1800) = 18 000/1800 = 10.
    assert equal(8 * 1800 + 3600, 18000) and equal(sp.Rational(18000, 1800), 10)
    # Exact rational samples either side of the threshold.
    def Aq(v):
        return (Q(8) * v + 3600) / v
    rng = random.Random(11)
    for _ in range(300):
        assert Aq(Q(1800) + Q(rng.randint(1, 10**9), 10**6)) < 10
        assert Aq(Q(rng.randint(1, 1800 * 10**6), 10**6)) >= 10
    assert Aq(Q(1800)) == 10 and Aq(Q(1800) + Q(1, 10**12)) < 10 and Aq(Q(1800) - Q(1, 10**12)) > 10
    # The round ε = 2: A − 8 = 3600/x > 0 on x > 0, so |A − 8| = A − 8, and |A − 8| < 2 exactly
    # when A < 10. The winning thresholds N must also keep x > N inside x > 0, so N ≥ 0; the
    # smallest winning one is the same 1800.
    assert equal(sp.together(A - 8), 3600 / x)
    assert equal(((8 * x + 3600) - 8 * x) / x, 3600 / x)
    assert equal(solved(A - 8 <= 0, half_line), sp.S.EmptySet)
    assert equal(solved(sp.Abs(A - limit) < 2, half_line), below)
    assert equal(limit + 2, 10)
    assert equal(answer("exr-calc-limits-review-average-cost"), (limit, smallest))


@covers("exr-calc-limits-review-root-over-line")
def test_exr_calc_limits_review_root_over_line():
    f = sp.sqrt(4 * x**2 + 1) / (x - 1)
    reals = sp.S.Reals
    # 4x² + 1 ≥ 1 > 0 everywhere, so √(4x² + 1) ≥ 1 everywhere (equality only at 0).
    assert equal(solved(4 * x**2 + 1 < 1, reals), sp.S.EmptySet)
    assert equal(solved(sp.sqrt(4 * x**2 + 1) < 1, reals), sp.S.EmptySet)
    assert equal(sp.solveset(sp.sqrt(4 * x**2 + 1) - 1, x, reals), sp.FiniteSet(0))
    # (a) for x < 0 (x = −p, p > 0): √(x²) = −x, 4 + 1/x² > 0, −x·√(4 + 1/x²) = √(4x² + 1),
    # (x − 1)/(−x) = −1 + 1/x, and f = √(4 + 1/x²)/(−1 + 1/x).
    assert equal(sp.sqrt(x**2).subs(x, -pos), (-x).subs(x, -pos))
    assert equal(sp.sqrt(neg**2), -neg)
    assert equal_on_domain(sp.sqrt(x**2), -x, x, sp.Interval.open(-sp.oo, 0))
    assert equal(solved(4 + 1 / x**2 <= 0, sp.Interval.open(-sp.oo, 0)), sp.S.EmptySet)
    assert equal(sp.expand((-x) ** 2 * (4 + 1 / x**2)), 4 * x**2 + 1)
    assert equal((-x * sp.sqrt(4 + 1 / x**2)).subs(x, -pos), sp.sqrt(4 * x**2 + 1).subs(x, -pos))
    assert equal((x - 1) / (-x), -1 + 1 / x)
    rewritten = sp.sqrt(4 + 1 / x**2) / (-1 + 1 / x)
    assert equal_on_domain(f, rewritten, x, sp.Interval.open(-sp.oo, 0))
    assert equal(f.subs(x, -pos), rewritten.subs(x, -pos))
    # The pieces' limits as x → −∞, and the limit of f by two routes.
    assert limit_is(1 / x, x, -sp.oo, 0) and limit_is(1 / x**2, x, -sp.oo, 0)
    assert limit_is(4 + 1 / x**2, x, -sp.oo, 4) and limit_is(sp.sqrt(4 + 1 / x**2), x, -sp.oo, 2)
    # √4 = 2, as 2 ≥ 0 and 2² = 4 (the reason the page now gives).
    assert sp.Integer(2) >= 0 and equal(sp.Integer(2) ** 2, 4) and equal(sp.sqrt(4), 2)
    assert limit_is(-1 + 1 / x, x, -sp.oo, -1)
    lim_a = sp.Rational(2, -1)
    assert limit_is(rewritten, x, -sp.oo, lim_a) and limit_is(f, x, -sp.oo, lim_a)
    # (b) g = 1/(x − 1) → −∞ as x → 1⁻; h ≥ 1 on (0, 1); so f → −∞ as x → 1⁻.
    assert equal(f, sp.sqrt(4 * x**2 + 1) * (1 / (x - 1)))
    assert limit_is(1 / (x - 1), x, 1, -sp.oo, dir="-")
    lim_b = -sp.oo
    assert limit_is(f, x, 1, lim_b, dir="-")
    # The δ the page's propositions build: reciprocal power at height M/m = M gives min(1, 1/M),
    # then min with r = 1. At exact points of (1 − δ, 1), f(x) < −M (SymPy compares the exact
    # algebraic numbers).
    rng = random.Random(8)
    for mv in [sp.Rational(1, 1000), sp.Integer(1), sp.Integer(1000), sp.Integer(10**9)] + \
              [sp.Rational(rng.randint(1, 10**7), 1000) for _ in range(30)]:
        d = sp.Min(sp.Min(1, 1 / mv), 1)
        for fr in (sp.Rational(1, 10**9), sp.Rational(1, 2), sp.Rational(10**9 - 1, 10**9)):
            xv = 1 - d * fr
            assert 0 < xv < 1 and (f.subs(x, xv) < -mv) is sp.true
    # The aside: the limit 2 at ∞, and the vertical asymptote x = 1 (from the right: ∞).
    assert limit_is(f, x, sp.oo, 2)
    assert limit_is(f, x, 1, sp.oo, dir="+")
    assert equal(answer("exr-calc-limits-review-root-over-line"), (lim_a, lim_b))


@covers("exr-calc-limits-review-positive-over-square")
def test_exr_calc_limits_review_positive_over_square():
    # A proof: answer() has nothing to read. The key claims are tested below; the exercise counts
    # as covered only through the reviewer's maths.manual_checked note.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limits-review-positive-over-square")
    avals = (0, 2, sp.Rational(-1, 3))

    # (a) ε = L/2 > 0, and |f − L| < L/2 means L − L/2 < f < L + L/2, whose left end is L/2.
    assert (L / 2).is_positive and equal(L - L / 2, L / 2)
    fx = sp.Symbol("f_x", real=True)
    assert equal(sp.solveset(sp.Abs(fx - L) < L / 2, fx, sp.S.Reals), sp.Interval.open(L - L / 2, L + L / 2))
    # The aside after (a): for L > 0, F → ∞ from both sides. 1/(x − a)² → ∞ on both sides (n = 2
    # even), and the r of (a) followed by the factor proposition's δ = min(min(1, 1/(M/m)), r),
    # m = L/2, wins every height M, at exact points; for three functions with an explicit δ(ε).
    for av in avals:
        assert limit_is(1 / (x - av) ** 2, x, av, sp.oo)

    def chain(f, av, lv, delta_for):
        r, m = delta_for(lv / 2), lv / 2
        rng = random.Random(12)
        heights = [Q(1, 10**6), Q(1), Q(7), Q(10**9)] + [Q(rng.randint(1, 10**10), 1000) for _ in range(40)]
        for mv in heights:
            d = min(min(Q(1), 1 / (mv / m)), r)
            for xv in exact_points(av, d, rng, count=8):
                assert 0 < abs(xv - av) < r and f(xv) > m
                assert f(xv) / (xv - av) ** 2 > mv, f"a = {av}, M = {mv}, δ = {d}, x = {xv}"
        return True

    for fexpr, av, lv, fq, dq in (
        (3 - 4 * (x - 1), 1, 3, lambda v: 3 - 4 * (v - 1), lambda e: e / 4),       # |f − 3| = 4|x − 1|
        ((x**2 - 1) / (x - 1), 1, 2, lambda v: (v * v - 1) / (v - 1), lambda e: e),  # undefined at 1
        (sp.Rational(1, 2) + x**2, 0, sp.Rational(1, 2), lambda v: Q(1, 2) + v * v, lambda e: min(Q(1), e)),
    ):
        assert limit_is(fexpr, x, av, lv)
        assert chain(fq, Q(av), Q(lv), dq)
        assert limit_is(fexpr / (x - av) ** 2, x, av, sp.oo)

    # (b) The preamble: (x − a)² ≠ 0 for x ≠ a; g = 1/(x − a) has the one-sided limits ∞ and −∞.
    for av in avals:
        assert equal(sp.solveset((x - av) ** 2, x, sp.S.Reals), sp.FiniteSet(av))
        assert limit_is(1 / (x - av), x, av, sp.oo, dir="+")
        assert limit_is(1 / (x - av), x, av, -sp.oo, dir="-")

    # (i) f = |x − a|. f → 0, with δ = ε, at exact points: |f(x) − 0| = |x − a| < ε.
    rng = random.Random(13)
    for av in avals:
        assert limit_is(sp.Abs(x - av), x, av, 0)
        for ev in (Q(1, 10**6), Q(1, 3), Q(1), Q(50)):
            assert all(abs(abs(xv - Q(av)) - 0) < ev for xv in exact_points(Q(av), ev, rng, count=10))
    # F = |x − a|/(x − a)² = 1/|x − a| off a, which is 1·g on the right and (−1)·g on the left
    # (x = a + p and x = a − p, p > 0, symbolic a).
    Fi = sp.Abs(x - a) / (x - a) ** 2
    assert equal(sp.Abs(pos) ** 2, pos**2) and (sp.Abs(pos) - 0).is_positive
    assert equal(Fi.subs(x, a + pos), (1 / sp.Abs(x - a)).subs(x, a + pos))
    assert equal(Fi.subs(x, a - pos), (1 / sp.Abs(x - a)).subs(x, a - pos))
    assert equal(Fi.subs(x, a + pos), (1 * 1 / (x - a)).subs(x, a + pos))
    assert equal(Fi.subs(x, a - pos), (-1 * 1 / (x - a)).subs(x, a - pos))
    for av in avals:
        Fiv = Fi.subs(a, av)
        assert limit_is(Fiv, x, av, sp.oo, dir="+") and limit_is(Fiv, x, av, sp.oo, dir="-")
        assert limit_is(Fiv, x, av, sp.oo)

    # (ii) f = (x − a)²: f(a) = 0 and f → 0; F = 1 on 0 < |x − a| < 1, so F → 1, a real number.
    for av in avals:
        f2 = (x - av) ** 2
        assert equal(f2.subs(x, av), 0) and limit_is(f2, x, av, 0)
        for half in (sp.Interval.open(av - 1, av), sp.Interval.open(av, av + 1)):
            assert equal_on_domain(f2 / (x - av) ** 2, 1, x, half)
        assert limit_is(f2 / (x - av) ** 2, x, av, 1)
        assert sp.limit(f2 / (x - av) ** 2, x, av).is_finite

    # (iii) f = x − a: f(a) = 0 and f → 0; F = 1/(x − a) = g off a.
    for av in avals:
        f3 = x - av
        F3 = f3 / (x - av) ** 2
        assert equal(f3.subs(x, av), 0) and limit_is(f3, x, av, 0)
        assert equal_on_domain(F3, 1 / (x - av), x, sp.Interval.open(av, av + 1))
        assert equal_on_domain(F3, 1 / (x - av), x, sp.Interval.open(av - 1, av))
        # The one-sided limits differ (∞ on the right, −∞ on the left), so there is no real
        # limit, and the two-sided limit is neither ∞ nor −∞: SymPy's two-sided limit is zoo.
        assert limit_is(F3, x, av, sp.oo, dir="+") and limit_is(F3, x, av, -sp.oo, dir="-")
        assert sp.limit(F3, x, av, "+-") is sp.zoo
        # Not ∞: F < 0 < 1 at every x in (a − 1, a), so no left window has F > 1 (the height
        # M = 1). Not −∞: F > 0 > −1 at every x in (a, a + 1).
        assert equal(solved(F3 >= 0, sp.Interval.open(av - 1, av)), sp.S.EmptySet)
        assert equal(solved(F3 <= 0, sp.Interval.open(av, av + 1)), sp.S.EmptySet)
        assert equal(solved(F3 > 1, sp.Interval.open(av - 1, av)), sp.S.EmptySet)
        assert equal(solved(F3 < -1, sp.Interval.open(av, av + 1)), sp.S.EmptySet)
    # The same signs for symbolic a: F(a − p) = −1/p < 0 and F(a + p) = 1/p > 0.
    F3a = (x - a) / (x - a) ** 2
    assert F3a.subs(x, a - pos).is_negative and F3a.subs(x, a + pos).is_positive


@covers("exr-calc-limits-review-root-parameters")
def test_exr_calc_limits_review_root_parameters():
    F = sp.sqrt(x**2 + a * x + 1) - b * x
    target = sp.Integer(-2)
    # Where it is defined: for x > |a|, x > 0, x + a > 0 and x² + ax + 1 = x(x + a) + 1 > 1. With
    # x = |a| + p (p > 0), split on the sign of a.
    ap, an = sp.Symbol("a_p", nonnegative=True), sp.Symbol("a_n", negative=True)
    for av in (ap, an):
        xv = sp.Abs(av) + pos
        assert xv.is_positive and (xv + av).is_positive
        assert (sp.expand(xv**2 + av * xv + 1) - 1).is_positive
    assert equal(sp.expand(x * (x + a) + 1), x**2 + a * x + 1)
    # 1 + a/x + 1/x² = (x² + ax + 1)/x², and √(x² + ax + 1) = x √(1 + a/x + 1/x²) for x > |a|:
    # x √(…) is ≥ 0 and its square is x² + ax + 1.
    assert equal(1 + a / x + 1 / x**2, (x**2 + a * x + 1) / x**2)
    inner = 1 + a / pos + 1 / pos**2
    assert equal(sp.expand((pos * sp.sqrt(inner)) ** 2), pos**2 + a * pos + 1)
    for av in (-4, -7, 0, 6, sp.Rational(5, 2)):
        assert equal_on_domain(sp.sqrt(x**2 + av * x + 1), x * sp.sqrt(1 + av / x + 1 / x**2), x,
                               sp.Interval.open(abs(av), sp.oo))
    # The root after dividing by x tends to √1 = 1 (1 ≥ 0 and 1² = 1), for every real a.
    assert equal(sp.limit(1 + a / x + 1 / x**2, x, sp.oo), 1) and equal(sp.sqrt(1), 1)
    assert equal(sp.limit(sp.sqrt(1 + a / x + 1 / x**2), x, sp.oo), 1)

    # b must be 1: F/x = √(1 + a/x + 1/x²) − b → 1 − b; and F/x = F · (1/x) → (−2) · 0 = 0.
    assert equal_on_domain(F.subs({a: -4, b: 3}) / x, sp.sqrt(1 - 4 / x + 1 / x**2) - 3, x, sp.Interval.open(4, sp.oo))
    assert equal(sp.limit(F / x, x, sp.oo), 1 - b)
    assert equal(target * 0, 0)
    assert equal(sp.solveset(sp.Eq(1 - b, 0), b, sp.S.Reals), sp.FiniteSet(1))
    # Uniqueness of b, independently: if b ≠ 1, F → ∞ (b < 1) or −∞ (b > 1), so never −2.
    assert sp.limit(F.subs(b, 1 - pos), x, sp.oo) is sp.oo
    assert sp.limit(F.subs(b, 1 + pos), x, sp.oo) is -sp.oo
    rng = random.Random(14)
    for _ in range(10):
        av = sp.Rational(rng.randint(-50, 50), 7)
        for bv in (sp.Rational(rng.randint(-30, 29), 30), sp.Rational(rng.randint(31, 90), 30)):
            assert limit_is(F.subs({a: av, b: bv}), x, sp.oo, sp.oo if bv < 1 else -sp.oo)

    # a must be −4: with b = 1, √ + x > 0, and the rationalised chain gives F → a/2.
    F1 = F.subs(b, 1)
    rat1 = ((x**2 + a * x + 1) - x**2) / (sp.sqrt(x**2 + a * x + 1) + x)
    rat2 = (a + 1 / x) / (sp.sqrt(1 + a / x + 1 / x**2) + 1)
    for av in (-4, -7, 0, 6, sp.Rational(5, 2)):
        dom = sp.Interval.open(abs(av), sp.oo)
        assert equal(solved(sp.sqrt(x**2 + av * x + 1) + x <= 0, dom), sp.S.EmptySet)
        assert equal_on_domain(F1.subs(a, av), rat1.subs(a, av), x, dom)
        assert equal_on_domain(rat1.subs(a, av), rat2.subs(a, av), x, dom)
    assert equal(sp.limit(a + 1 / x, x, sp.oo), a) and equal(sp.limit(rat2, x, sp.oo), a / 2)
    assert equal(sp.limit(F1, x, sp.oo), a / 2)
    # a/2 = −2 has exactly one solution; for b = 1 and any other a the limit is not −2.
    assert equal(sp.solveset(sp.Eq(a / 2, target), a, sp.S.Reals), sp.FiniteSet(-4))
    for av in (-5, sp.Rational(-41, 10), sp.Rational(-39, 10), -3, 0, 6):
        assert not equal(sp.limit(F1.subs(a, av), x, sp.oo), target)
    # The system 1 − b = 0, a/2 = −2 has exactly one solution.
    solutions = sp.solve([sp.Eq(1 - b, 0), sp.Eq(a / 2, target)], [a, b], dict=True)
    assert len(solutions) == 1
    pair = (solutions[0][a], solutions[0][b])
    # The pair works (two routes: the a/2 formula and limit_is), and √(x² − 4x + 1) approaches
    # the line y = x − 2.
    assert equal(pair[0] / 2, target)
    assert limit_is(F.subs({a: pair[0], b: pair[1]}), x, sp.oo, target)
    assert equal(F.subs({a: pair[0], b: pair[1]}) + x, sp.sqrt(x**2 - 4 * x + 1))
    assert limit_is(sp.sqrt(x**2 - 4 * x + 1) - (x - 2), x, sp.oo, 0)
    assert equal(answer("exr-calc-limits-review-root-parameters"), pair)


# ── Chapter summary (not labelled exercises; tested all the same) ───────────────────────────


def test_chapter_summary_limits():
    assert limit_is(sp.sin(x) / x, x, 0, 1)
    assert limit_is((1 - sp.cos(x)) / x, x, 0, 0)
    # The square-root law as the summary now states it: a positive limit (√(x + 3) → 2 at 1), or
    # the limit 0 with f ≥ 0 near a (√(x²) → 0 at 0). Without f ≥ 0 the root need not be defined
    # near a: −x² → 0 at 0, but −x² < 0 at every x ≠ 0.
    assert limit_is(sp.sqrt(x + 3), x, 1, 2)
    assert equal(solved(x**2 < 0, sp.S.Reals), sp.S.EmptySet) and limit_is(sp.sqrt(x**2), x, 0, 0)
    assert limit_is(-x**2, x, 0, 0) and equal(solved(-x**2 >= 0, sp.S.Reals), sp.FiniteSet(0))
