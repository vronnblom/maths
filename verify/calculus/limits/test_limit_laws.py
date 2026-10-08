"""Verification tests for content/calculus/limits/limit-laws.md (calc-limit-laws).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps; the answers are read
with answer(label), as printed on the page.

- The ε–δ checks follow verify/calculus/limits/test_limit_of_a_function.py: each displayed step is
  asserted, a δ is found symbolically (solveset) where the page says "exactly when", and the
  implication 0 < |x − a| < δ ⇒ |F(x) − L| < ε is tested on exact rational (ε, x) pairs up to the
  edge of the window (fractions.Fraction; floats could hide a failure at the edge).
- Direct substitution: every polynomial or rational limit on the page is compared with sp.limit
  AND with the value at the point, after checking that the denominator is non-zero there.
- "When the laws do not apply": each case is checked to be what the page says it is at the point
  (numerator and denominator both → 0, denominator → 0, a part with no limit, a function not
  defined on any punctured interval), without resolving the 0/0 limits on the next page's behalf.
"""

import random
from fractions import Fraction as Q

import pytest
import sympy as sp

from mathcheck import ManualAnswer, answer, c, covers, equal, limit_is, symbol, t, u, x

eps = sp.Symbol("epsilon", positive=True)   # ε > 0 for derivations
EPS_PAGE = symbol("varepsilon")             # the symbol answer() reads \eps as (real)
N = 10**6


def page_eps(expr):
    """An answer containing \\eps, with the page's real ε replaced by the positive ε used here."""
    return expr.subs(EPS_PAGE, eps)


def eps_samples(seed, count=200, breaks=()):
    """Exact rational tolerances: tiny, moderate and huge ones, each break of a min (the ε where
    the branches meet) and its immediate neighbours, and random ones."""
    rng = random.Random(seed)
    fixed = [Q(1, 10**9), Q(1, 10**6), Q(1, 1000), Q(1, 100), Q(1, 10), Q(1, 2), Q(1), Q(3), Q(100), Q(10**6)]
    for b in breaks:
        fixed += [Q(b), Q(b) - Q(1, 10**9), Q(b) + Q(1, 10**9)]
    return fixed + [Q(rng.randint(1, 20 * N), N) for _ in range(count)]


def window(a, d, rng, count=30):
    """Exact rational points x with 0 < |x − a| < d, on both sides: right next to a, right at the
    edge of the window (within 10⁻⁹ of d), and random ones in between."""
    fractions = [Q(1, 10**9), Q(1, N), Q(N - 1, N), Q(10**9 - 1, 10**9)]
    fractions += [Q(rng.randint(1, N - 1), N) for _ in range(count)]
    for fr in fractions:
        yield a + d * fr
        yield a - d * fr


def implication_holds(F, a, lim, choose_delta, samples, seed=0, count=30):
    """0 < |x − a| < δ ⇒ |F(x) − L| < ε at every sampled (ε, x) pair, all in exact arithmetic."""
    rng = random.Random(seed)
    for e in samples:
        d = choose_delta(e)
        assert d > 0
        for xv in window(a, d, rng, count):
            assert abs(F(xv) - lim) < e, f"ε = {e}, δ = {d}, x = {xv}: |F(x) − L| = {abs(F(xv) - lim)}"
    return True


def half_width(good, a):
    """The good set {x : |F(x) − L| < ε} must be (a − d, a + d) or (a − d, a + d) minus {a};
    returns d (the largest δ, read off the set itself)."""
    hull = sp.Interval(good.inf, good.sup, left_open=True, right_open=True)
    assert equal(hull - good, sp.S.EmptySet) or equal(hull - good, sp.FiniteSet(a))
    d = a - good.inf
    assert equal(good.sup - a, d)
    return d


def substitution_agrees(expr, var, a, value):
    """Direct substitution for a polynomial or rational expr at a: the denominator is non-zero at
    a, and sp.limit, the value at a and `value` all agree."""
    num, den = sp.fraction(sp.together(expr))
    assert num.is_polynomial(var) and den.is_polynomial(var)
    assert den.subs(var, a) != 0, f"the denominator {den} is 0 at {a}"
    direct = expr.subs(var, a)
    assert equal(direct, num.subs(var, a) / den.subs(var, a))
    assert equal(sp.limit(expr, var, a), direct)
    if expr.free_symbols - {var}:   # a parameter (c): no table of values, sp.limit only
        return equal(direct, value)
    return equal(direct, value) and limit_is(expr, var, a, value)


def rounds_to(exact, shown):
    """`shown` (a decimal string) is `exact` correctly rounded to the digits shown."""
    places = len(shown.split(".")[1]) if "." in shown else 0
    return abs(sp.nsimplify(exact) - sp.Rational(shown)) <= sp.Rational(1, 2 * 10**places)


def no_two_sided_limit(expr, var, a):
    """The one-sided limits at a are +∞ and −∞ (SymPy, with a table of values as a second
    route through limit_is), so there is no real two-sided limit."""
    return limit_is(expr, var, a, sp.oo, dir="+") and limit_is(expr, var, a, -sp.oo, dir="-")


# ── The sum law's proof (F) and part (a) ─────────────────────────────────────────


def test_thm_calc_limit_laws_part_a_and_sum_proof():
    # (a) constants: δ = 1 works for every ε (|c − c| = 0); the identity: δ = ε.
    for cv in (Q(0), Q(-7, 3), Q(5)):
        assert implication_holds(lambda v: cv, Q(2, 3), cv, lambda e: Q(1), eps_samples(1, count=40))
    assert implication_holds(lambda v: v, Q(-5, 7), Q(-5, 7), lambda e: e, eps_samples(2, count=60))

    # The displayed chain, with symbols for f(x), g(x), L, M:
    fx, gx, Lm, Mm = sp.symbols("f_x g_x L M", real=True)
    # line 1: (f + g) − (L + M) = (f − L) + (g − M)
    assert equal((fx + gx) - (Lm + Mm), (fx - Lm) + (gx - Mm))
    # ε/2 + ε/2 = ε, and ε/2 > 0
    assert equal(eps / 2 + eps / 2, eps) and (eps / 2).is_positive
    # the difference: (f − g) − (L − M) = (f − L) + (−(g − M)), and |−(g − M)| = |g − M|
    assert equal((fx - gx) - (Lm - Mm), (fx - Lm) + (-(gx - Mm)))
    assert equal(sp.Abs(-(gx - Mm)), sp.Abs(gx - Mm))
    # line 2, the triangle inequality |p + q| ≤ |p| + |q|, on exact random pairs; and adding two
    # strict inequalities p < r, q < s gives p + q < r + s.
    rng = random.Random(3)
    for _ in range(2000):
        p, q, r_, s_ = (Q(rng.randint(-10**6, 10**6), 997) for _ in range(4))
        assert abs(p + q) <= abs(p) + abs(q)
        if p < r_ and q < s_:
            assert p + q < r_ + s_

    # The whole proof on concrete pairs (f, g, a, L, M) with known δ's for the tolerance τ: each
    # δ_i is first checked for f and g with the tolerance ε/2, then δ = min(δ1, δ2) for f + g and
    # f − g with ε, and each displayed inequality is checked at every sampled point.
    third = Q(1, 3)
    cases = [
        # f = 2x − 1, g = 4x at 3: |f − 5| = 2|x − 3|, |g − 12| = 4|x − 3|.
        (lambda v: 2 * v - 1, lambda v: 4 * v, Q(3), Q(5), Q(12), lambda tau: tau / 2, lambda tau: tau / 4),
        # f = x² at 2 (δ = min(1, τ/5): |x + 2| < 5 on |x − 2| < 1), g = 1/x at 2 (δ = min(1, 2τ):
        # |1/x − ½| = |x − 2|/(2|x|) < |x − 2|/2 on |x − 2| < 1, where x > 1).
        (lambda v: v * v, lambda v: 1 / v, Q(2), Q(4), Q(1, 2),
         lambda tau: min(Q(1), tau / 5), lambda tau: min(Q(1), 2 * tau)),
        # f = 1/x at 1/3 (|1/x − 3| = 3|x − ⅓|/x < 18|x − ⅓| on |x − ⅓| < 1/6, where x > 1/6),
        # g = 3x − 2 at 1/3.
        (lambda v: 1 / v, lambda v: 3 * v - 2, third, Q(3), Q(-1),
         lambda tau: min(Q(1, 6), tau / 18), lambda tau: tau / 3),
    ]
    for i, (f, g, a, Lv, Mv, d1, d2) in enumerate(cases):
        # The known δ's, for the tolerance ε/2.
        assert implication_holds(f, a, Lv, lambda e: d1(e / 2), eps_samples(10 + i, count=60), seed=i)
        assert implication_holds(g, a, Mv, lambda e: d2(e / 2), eps_samples(20 + i, count=60), seed=i)
        choose = lambda e: min(d1(e / 2), d2(e / 2))  # noqa: E731  (the proof's δ)
        assert implication_holds(lambda v: f(v) + g(v), a, Lv + Mv, choose, eps_samples(30 + i), seed=i)
        assert implication_holds(lambda v: f(v) - g(v), a, Lv - Mv, choose, eps_samples(40 + i), seed=i)
        # Each line of the display, at each sampled point.
        rng = random.Random(50 + i)
        for e in eps_samples(50 + i, count=40, breaks=(2,)):
            d = choose(e)
            for xv in window(a, d, rng, count=10):
                ef, eg = f(xv) - Lv, g(xv) - Mv
                assert abs(xv - a) < d1(e / 2) and abs(xv - a) < d2(e / 2)   # in both windows
                assert abs((f(xv) + g(xv)) - (Lv + Mv)) == abs(ef + eg)
                assert abs(ef + eg) <= abs(ef) + abs(eg)
                assert abs(ef) < e / 2 and abs(eg) < e / 2
                assert abs(ef) + abs(eg) < e
                assert abs((f(xv) - g(xv)) - (Lv - Mv)) == abs(ef + (-eg)) <= abs(ef) + abs(-eg) < e
    # Cross-check of the three pairs' limits by SymPy.
    assert limit_is(x**2 + 1 / x, x, 2, sp.Rational(9, 2)) and limit_is(x**2 - 1 / x, x, 2, sp.Rational(7, 2))
    assert limit_is(1 / x + 3 * x - 2, x, sp.Rational(1, 3), 2)


def test_combining_functions_example_and_non_example():
    # Example: δ = ε/2 for 2x − 1 → 5 and ε/4 for 4x → 12 at 3; the sum law gives 17.
    assert equal(sp.Abs((2 * x - 1) - 5), 2 * sp.Abs(x - 3))
    assert equal(sp.Abs(4 * x - 12), 4 * sp.Abs(x - 3))
    assert implication_holds(lambda v: 2 * v - 1, Q(3), Q(5), lambda e: e / 2, eps_samples(60, count=60))
    assert implication_holds(lambda v: 4 * v, Q(3), Q(12), lambda e: e / 4, eps_samples(61, count=60))
    assert equal((2 * x - 1) + 4 * x, 6 * x - 1)
    assert limit_is(6 * x - 1, x, 3, 5 + 12)
    # Non-example: x · (1/x) = 1 for x ≠ 0 (limit 1), and 1/x has no limit at 0.
    assert equal(sp.cancel(x * (1 / x)), 1)
    assert limit_is(x * (1 / x), x, 0, 1)
    assert no_two_sided_limit(1 / x, x, 0)
    # "Why the laws should hold": errors of 0.01 each add up to at most 0.02.
    assert equal(sp.Rational(1, 100) + sp.Rational(1, 100), sp.Rational(2, 100))


def test_power_and_root_sketches():
    # (e): f² = f·f and f³ = f²·f, so L·L = L² and L²·L = L³.
    fx, Lm = sp.symbols("f_x L", real=True)
    assert equal(fx * fx, fx**2) and equal(fx**2 * fx, fx**3)
    # (f), L > 0: (√f − √L)(√f + √L) = f − L for f ≥ 0, and √f + √L ≥ √L > 0.
    fy = sp.Symbol("f_y", nonnegative=True)
    Lp = sp.Symbol("L_p", positive=True)
    assert equal((sp.sqrt(fy) - sp.sqrt(Lp)) * (sp.sqrt(fy) + sp.sqrt(Lp)), fy - Lp)
    assert sp.sqrt(Lp).is_positive and (sp.sqrt(fy) + sp.sqrt(Lp) - sp.sqrt(Lp)).is_nonnegative
    # |√f − √L| = |f − L|/(√f + √L) ≤ |f − L|/√L.
    # (dividing the identity by the positive factor; property 4, |p/q| = |p|/|q|, with |q| = q)
    q_ = sp.sqrt(fy) + sp.sqrt(Lp)
    assert equal((fy - Lp) / q_, sp.sqrt(fy) - sp.sqrt(Lp))
    assert equal(sp.Abs(q_), q_) and equal(sp.Abs((fy - Lp) / q_), sp.Abs(fy - Lp) / sp.Abs(q_))
    gap = sp.Abs(fy - Lp) / sp.sqrt(Lp) - sp.Abs(fy - Lp) / q_
    assert equal(gap, sp.Abs(fy - Lp) * sp.sqrt(fy) / (sp.sqrt(Lp) * q_))
    assert (sp.Abs(fy - Lp) * sp.sqrt(fy) / (sp.sqrt(Lp) * q_)).is_nonnegative
    # |f − L| < L gives f > 0: the set {f : |f − L| < L} is (0, 2L).
    fr = sp.Symbol("f_r", real=True)
    assert equal(sp.solveset(sp.Abs(fr - 4) < 4, fr, sp.S.Reals), sp.Interval.open(0, 8))
    # The sketch's δ on a concrete case: f = x + 3 at 1 (L = 4, δ_f(τ) = τ). The tolerance L gives
    # δ = 4; |f − 4| < ε√4 = 2ε gives δ = 2ε; the full proof takes min(4, 2ε). Exact comparisons
    # (SymPy decides each square root comparison exactly).
    rng = random.Random(70)
    for e in eps_samples(70, count=25, breaks=(2,)):
        d = min(Q(4), 2 * e)
        for xv in window(Q(1), d, rng, count=5):
            xr = sp.Rational(xv.numerator, xv.denominator)
            assert xr + 3 > 0
            assert (sp.Abs(sp.sqrt(xr + 3) - 2) < sp.Rational(e.numerator, e.denominator)) is sp.true
    # (f), L = 0: 0 ≤ f < ε² gives √f < ε. With s = √f ≥ 0 (so f = s²): s² < ε² exactly when
    # 0 ≤ s < ε.
    # 0 ≤ s < ε (the solution set over ℝ is (−ε, ε); SymPy cannot simplify its meet with [0, ∞)).
    sq = sp.Symbol("s_q", nonnegative=True)
    sr = sp.Symbol("s_r", real=True)
    assert equal(sp.sqrt(sq**2), sq)
    assert equal(sp.solveset(sr**2 < eps**2, sr, sp.S.Reals), sp.Interval.open(-eps, eps))
    # Looking ahead: the cube root of −8 is −2.
    assert equal(sp.real_root(-8, 3), -2) and equal((-2) ** 3, -8)


def test_prf_calc_limit_laws_key_claims():
    # The rigorous track (policy R) on a concrete pair: its δ's composed exactly as written.
    fx, gx, Lm, Mm = sp.symbols("f_x g_x L M", real=True)
    # (c) the identity f g − LM = f(g − M) + M(f − L).
    assert equal(fx * gx - Lm * Mm, fx * (gx - Mm) + Mm * (fx - Lm))
    # (d) 1/g − 1/M = (M − g)/(g M); and |g − M| < |M|/2 gives |g| > |M|/2.
    assert equal(1 / gx - 1 / Mm, (Mm - gx) / (gx * Mm))
    g_ = sp.Symbol("g", real=True)
    for Mv in (sp.Integer(12), sp.Rational(-3, 2)):
        near = sp.solveset(sp.Abs(g_ - Mv) < sp.Abs(Mv) / 2, g_, sp.S.Reals)
        assert equal(near - sp.solveset(sp.Abs(g_) > sp.Abs(Mv) / 2, g_, sp.S.Reals), sp.S.EmptySet)
    # Concrete: f = 2x − 1 → 5, g = 4x → 12 at 3, with δ_f(τ) = τ/2, δ_g(τ) = τ/4.
    a, Lv, Mv = Q(3), Q(5), Q(12)
    df, dg = lambda tau: tau / 2, lambda tau: tau / 4

    def product_delta(da, db, La, Mb):
        K, Nn = abs(La) + 1, abs(Mb) + 1
        return lambda e: min(da(Q(1)), db(e / (2 * K)), da(e / (2 * Nn)))

    assert implication_holds(lambda v: (2 * v - 1) * 4 * v, a, Lv * Mv, product_delta(df, dg, Lv, Mv), eps_samples(80))
    # 1/g → 1/M with δ = min(δ4, δ5), δ4 for the tolerance |M|/2, δ5 for ε|M|²/2.
    dinv = lambda e: min(dg(abs(Mv) / 2), dg(e * Mv * Mv / 2))  # noqa: E731
    assert implication_holds(lambda v: 1 / (4 * v), a, 1 / Mv, dinv, eps_samples(81))
    rng = random.Random(82)
    for xv in window(a, dg(abs(Mv) / 2), rng):
        assert abs(4 * xv) > abs(Mv) / 2                          # g stays away from 0
    # f/g = f · (1/g) → L/M, with the product law's δ for f and 1/g.
    assert implication_holds(lambda v: (2 * v - 1) / (4 * v), a, Lv / Mv, product_delta(df, dinv, Lv, 1 / Mv),
                             eps_samples(83))
    assert limit_is((2 * x - 1) / (4 * x), x, 3, sp.Rational(5, 12))


# ── Direct substitution ──────────────────────────────────────────────────────────


def test_cor_calc_direct_substitution_every_example():
    # Every polynomial or rational limit the page states (value as on the page), each against
    # sp.limit and the value at the point, with the denominator checked non-zero there.
    claims = [
        (6 * x - 1, x, 3, 17),                                  # Combining functions, Example
        (x**2 + 3, x, 2, 7), (x**3 - 1, x, 2, 7),               # eg-rational, steps 1 and 3
        ((x**3 - 1) / (x**2 + 3), x, 2, 1),                     # eg-rational
        (x + 3, x, 1, 4), (x**2 + 1, x, 1, 2),                  # eg-root-quotient, steps 1 and 3
        (3 * t / (3 + t), t, 6, 2),                             # eg-resistors
        (x**2 - 1, x, 1, 0), (x - 1, x, 1, 0),                  # eg-hypotheses (i)
        (x - 2, x, 2, 0),                                       # eg-hypotheses (iii)
        (x + 1, x, 1, 2),                                       # common mistake, h
        (x - 1, x, 0, -1),                                      # not apply, root with L < 0
        (x**2 + x**4, x, 0, 0),                                 # exr root-zero
        (x**2 + 9, x, 4, 25),                                   # exr roots
        (x + 1, x, 0, 1), (x, x, 0, 0),                         # not apply, (x + 1)/x
        (x + 2, x, 2, 4), (x**2 - 4, x, 2, 0),                  # exr where-substitution, at 2
        (x + 2, x, -2, 0), (x**2 - 4, x, -2, 0),                # ... at −2
        (5 * u, u, 5, 25), (u - 5, u, 5, 0),                    # exr lens, at the focal point
        (5 * u / (u - 5), u, 15, sp.Rational(15, 2)),           # exr lens (its answer is read below)
        (c * x - x**2, x, 2, 2 * c - 4),                        # exr root-domain
    ]
    for expr, var, a, value in claims:
        assert substitution_agrees(expr, var, a, value), (expr, a)
    # The h of the remark is not rational: h(1) = 5, but its limit at 1 is that of x + 1.
    hh = sp.Piecewise((5, sp.Eq(x, 1)), (x + 1, True))
    assert equal(hh.subs(x, 1), 5)
    assert limit_is(x + 1, x, 1, 2)   # h = x + 1 on x ≠ 1 (sp.limit mishandles the Piecewise)


# ── When the laws do not apply ───────────────────────────────────────────────────


def test_sec_calc_limit_laws_not_apply():
    # A part has no limit: 1/x at 0 (one-sided limits +∞ and −∞); the page's argument: x·(1/x) = 1
    # has the limit 1, while the product law would give 0·M = 0.
    assert no_two_sided_limit(1 / x, x, 0)
    assert equal(sp.cancel(x * (1 / x)), 1) and limit_is(x * (1 / x), x, 0, 1)
    M = sp.Symbol("M", real=True)
    assert equal(0 * M, 0)
    # Quotient with M = 0, L ≠ 0: 1/x and (x + 1)/x = 1 + 1/x; numerator → 1, denominator → 0.
    assert equal((x + 1) / x, 1 + 1 / x)
    assert limit_is(x + 1, x, 0, 1) and limit_is(x, x, 0, 0)
    assert no_two_sided_limit((x + 1) / x, x, 0)
    assert equal((x + 1) / x - 1, 1 / x)
    # Quotient with M = 0, L = 0: x² + cx and x both → 0 at 0, for every c; the quotient is
    # undefined at 0. (Its limit is not resolved here.)
    assert equal((x**2 + c * x).subs(x, 0), 0) and equal(sp.limit(x**2 + c * x, x, 0), 0)
    assert ((x**2 + c * x) / x).subs(x, 0) is sp.nan
    # The stone's speed (5(1 + h)² − 5)/h: numerator and denominator both → 0 at 0.
    hs = symbol("h")
    assert equal(sp.limit(5 * (1 + hs) ** 2 - 5, hs, 0), 0) and equal(sp.limit(hs, hs, 0), 0)
    # Power n = −1: (f(x))^{−1} = 1/f(x); for f = x at 0, no limit.
    assert equal(x ** (-1), 1 / x)
    # Root with L < 0: x − 1 → −1 at 0, and x − 1 < 0 exactly for x < 1, a set containing a whole
    # interval around 0, so √(x − 1) is real on no punctured interval around 0.
    assert limit_is(x - 1, x, 0, -1)
    assert equal(sp.solveset(x - 1 < 0, x, sp.S.Reals), sp.Interval.open(-sp.oo, 1))
    assert sp.sqrt(sp.Rational(-1, 2) - 1).is_real is False
    # Root with L = 0 but f < 0 near 0: f = x, undefined for x < 0 (the point −δ/2 of every window).
    d = sp.Symbol("delta", positive=True)
    assert sp.sqrt(-d / 2).is_real is False
    # With the sign condition: √(x²) = |x| → 0, and x² ≥ 0 everywhere.
    assert equal(sp.solveset(x**2 < 0, x, sp.S.Reals), sp.S.EmptySet)
    assert equal(sp.sqrt(x**2), sp.Abs(x)) and limit_is(sp.sqrt(x**2), x, 0, 0)


def test_figure_zero_over_zero_and_try_this():
    F = (x**2 + c * x) / x
    # "For every c the graph is a straight line with a hole": F = x + c at every x ≠ 0.
    assert equal(sp.cancel(F), x + c)
    assert F.subs({c: 1, x: 0}) is sp.nan
    # Slider: −2 to 2 in steps of 0.5 (9 values) includes −2, 0, 1 and 1.5; on [−1, 1] the lines
    # stay within [−3, 3], inside yRange [−3.5, 3.5].
    steps = [sp.Integer(-2) + k * sp.Rational(1, 2) for k in range(9)]
    assert equal(steps[-1], 2)
    assert all(any(equal(s, v) for s in steps) for v in (-2, 0, 1, sp.Rational(3, 2)))
    assert equal(sp.Max(*[abs(v + s) for s in steps for v in (-1, 1)]), 3)
    # Table values for c = 1 and c = 1.5, exactly as listed.
    points = ["0.1", "0.01", "0.001", "-0.001", "-0.01", "-0.1"]
    shown = {1: ["1.1", "1.01", "1.001", "0.999", "0.99", "0.9"],
             sp.Rational(3, 2): ["1.6", "1.51", "1.501", "1.499", "1.49", "1.4"]}
    for cv, values in shown.items():
        for p, v in zip(points, values):
            assert equal(F.subs({c: cv, x: sp.Rational(p)}), sp.Rational(v))
        # "which approach c": the distance to c is |x|, which shrinks down the table on each side.
        dist = [abs(sp.Rational(v) - cv) for v in values]
        assert dist[0] > dist[1] > dist[2] and dist[5] > dist[4] > dist[3]
    # Try this: for c = −2, 0, 1.5 the numerator and the denominator both approach 0.
    for cv in (-2, 0, sp.Rational(3, 2)):
        assert equal(sp.limit((x**2 + c * x).subs(c, cv), x, 0), 0)


def test_common_mistakes():
    # "Zero times anything": x · (1/x) = 1, not 0.
    assert limit_is(x * (1 / x), x, 0, 1)
    # √x at the edge of its domain: undefined at every x < 0, real for x ≥ 0.
    assert equal(sp.solveset(x < 0, x, sp.S.Reals), sp.Interval.open(-sp.oo, 0))
    assert sp.sqrt(sp.Rational(-1, 10**6)).is_real is False
    assert limit_is(sp.sqrt(x), x, 0, 0, dir="+")   # the one-sided limit the page points to


# ── Examples ─────────────────────────────────────────────────────────────────────


@covers("eg-calc-limit-laws-sum-delta")
def test_eg_calc_limit_laws_sum_delta():
    f, g = 2 * x - 1, 4 * x
    assert limit_is(f, x, 3, 5) and limit_is(g, x, 3, 12) and limit_is(f + g, x, 3, 17)
    # Step 1: |f − 5| = |2x − 6| = 2|x − 3|; |f − 5| < ε/2 exactly when |x − 3| < ε/4.
    assert equal(sp.Abs(f - 5), sp.Abs(2 * x - 6)) and equal(sp.Abs(2 * x - 6), 2 * sp.Abs(x - 3))
    d1 = half_width(sp.solveset(sp.Abs(f - 5) < eps / 2, x, sp.S.Reals), 3)
    assert equal(d1, eps / 4)
    # Step 2: |g − 12| = 4|x − 3|; < ε/2 exactly when |x − 3| < ε/8.
    assert equal(sp.Abs(g - 12), 4 * sp.Abs(x - 3))
    d2 = half_width(sp.solveset(sp.Abs(g - 12) < eps / 2, x, sp.S.Reals), 3)
    assert equal(d2, eps / 8)
    # Step 3: min(ε/4, ε/8) = ε/8.
    assert equal(sp.Min(d1, d2), eps / 8) and (eps / 8 < eps / 4) is sp.true
    # Step 4: f + g = 6x − 1, |(6x − 1) − 17| = 6|x − 3|, < ε exactly when |x − 3| < ε/6; at
    # x = 3 + ε/6 the distance is exactly ε.
    assert equal(f + g, 6 * x - 1) and equal(sp.Abs((6 * x - 1) - 17), 6 * sp.Abs(x - 3))
    largest = half_width(sp.solveset(sp.Abs((6 * x - 1) - 17) < eps, x, sp.S.Reals), 3)
    assert equal(largest, eps / 6)
    assert equal(sp.Abs((6 * x - 1).subs(x, 3 + eps / 6) - 17), eps)
    # The boxed δ = ε/8 works (exact pairs up to the edge), and is smaller than ε/6.
    assert implication_holds(lambda v: 6 * v - 1, Q(3), Q(17), lambda e: e / 8, eps_samples(90))
    assert (eps / 8 < eps / 6) is sp.true
    # On the window of the largest δ, ε/6, f uses at most 2·ε/6 = ε/3 of the tolerance (less than
    # half) and g up to 4·ε/6 = 2ε/3 (more than half). See the report on the sentence
    # "g needs less than half".
    assert equal(2 * largest, eps / 3) and (eps / 3 < eps / 2) is sp.true
    assert equal(4 * largest, 2 * eps / 3) and (2 * eps / 3 > eps / 2) is sp.true
    # Check: ε = 0.6 gives δ = 0.075; x = 3.07 is in the window and |6(3.07) − 18| = 0.42 < 0.6.
    e = sp.Rational(6, 10)
    assert equal((eps / 8).subs(eps, e), sp.Rational(75, 1000))
    xv = sp.Rational(307, 100)
    assert 0 < abs(xv - 3) < sp.Rational(75, 1000)
    assert equal(sp.Abs(6 * xv - 1 - 17), sp.Rational(42, 100)) and sp.Rational(42, 100) < e

    # The rigour admonition "Sharing the tolerance in other ways": 2ε/3 to f and ε/3 to g give
    # min(ε/3, ε/12) = ε/12; ε/3 to f and 2ε/3 to g give min(ε/6, ε/6) = ε/6, the largest.
    def split_delta(ef, eg):
        a1 = half_width(sp.solveset(sp.Abs(f - 5) < ef, x, sp.S.Reals), 3)
        a2 = half_width(sp.solveset(sp.Abs(g - 12) < eg, x, sp.S.Reals), 3)
        return a1, a2

    a1, a2 = split_delta(2 * eps / 3, eps / 3)
    assert equal(a1, eps / 3) and equal(a2, eps / 12) and equal(sp.Min(a1, a2), eps / 12)
    a1, a2 = split_delta(eps / 3, 2 * eps / 3)
    assert equal(a1, eps / 6) and equal(a2, eps / 6) and equal(sp.Min(a1, a2), largest)
    assert implication_holds(lambda v: 6 * v - 1, Q(3), Q(17), lambda e: e / 12, eps_samples(91, count=60))


@covers("eg-calc-limit-laws-rational")
def test_eg_calc_limit_laws_rational():
    F = (x**3 - 1) / (x**2 + 3)
    # Step 1: x → 2, x² → 4, 3 → 3, x² + 3 → 7.
    assert limit_is(x, x, 2, 2) and limit_is(x**2, x, 2, 4) and limit_is(sp.Integer(3) + 0 * x, x, 2, 3)
    assert limit_is(x**2 + 3, x, 2, 4 + 3)
    # Step 2: 7 ≠ 0.  Step 3: x³ → 2³ = 8, x³ − 1 → 7.
    assert equal(sp.Integer(2) ** 3, 8) and limit_is(x**3, x, 2, 8) and limit_is(x**3 - 1, x, 2, 8 - 1)
    # Step 4 and the box: 7/7 = 1, by sp.limit and by direct substitution (denominator 7 ≠ 0).
    assert equal(sp.Rational(7, 7), 1)
    assert substitution_agrees(F, x, 2, 1)
    # "Why this matters": numerator and denominator are both 7 at 2.
    assert equal((x**3 - 1).subs(x, 2), 7) and equal((x**2 + 3).subs(x, 2), 7)
    # Check: at 2.001, 7.012006001/7.004001 ≈ 1.001143.
    xv = sp.Rational("2.001")
    assert equal(xv**3 - 1, sp.Rational("7.012006001")) and equal(xv**2 + 3, sp.Rational("7.004001"))
    assert rounds_to(F.subs(x, xv), "1.001143")
    # The figure wdg-calc-limit-laws-rational: the table at six points, rounded to six places;
    # f(0) ≈ −0.33, f(4) ≈ 3.3, rising on [0, 4] (f' ≥ 0 there, zero only at 0), approaching 1
    # from below on the left and from above on the right.
    table = {"1.9": "0.886384", "1.99": "0.988578", "1.999": "0.998857",
             "2.001": "1.001143", "2.01": "1.011435", "2.1": "1.114845"}
    for p, v in table.items():
        assert rounds_to(F.subs(x, sp.Rational(p)), v), (p, sp.N(F.subs(x, sp.Rational(p)), 12))
        assert (F.subs(x, sp.Rational(p)) < 1) == (sp.Rational(p) < 2)
    assert rounds_to(F.subs(x, 0), "-0.33") and rounds_to(F.subs(x, 4), "3.3")
    dF = sp.factor(sp.diff(F, x))
    assert equal(dF, x * (x**3 + 9 * x + 2) / (x**2 + 3) ** 2)
    assert equal(sp.solveset(dF < 0, x, sp.Interval(0, 4)), sp.S.EmptySet)
    assert equal(sp.solveset(sp.Eq(dF, 0), x, sp.Interval(0, 4)), sp.FiniteSet(0))
    # yRange [−1, 4] contains the graph on [0, 4] (its range is [f(0), f(4)]).
    assert -1 < F.subs(x, 0) and F.subs(x, 4) < 4


@covers("eg-calc-limit-laws-root-quotient")
def test_eg_calc_limit_laws_root_quotient():
    F = (x + sp.sqrt(x + 3)) / (x**2 + 1)
    # Step 1: x + 3 → 4 > 0, so √(x + 3) → √4 = 2; defined for every x ≥ −3.
    assert substitution_agrees(x + 3, x, 1, 4)
    assert equal(sp.sqrt(4), 2) and limit_is(sp.sqrt(x + 3), x, 1, 2)
    assert equal(sp.solveset(x + 3 >= 0, x, sp.S.Reals), sp.Interval(-3, sp.oo))
    # Step 2: numerator → 1 + 2 = 3.  Step 3: x² + 1 → 2 ≠ 0.
    assert limit_is(x + sp.sqrt(x + 3), x, 1, 1 + 2)
    assert substitution_agrees(x**2 + 1, x, 1, 2)
    # Step 4 and the box: 3/2, by sp.limit (with a table) and by the value at 1.
    assert limit_is(F, x, 1, sp.Rational(3, 2))
    assert equal(F.subs(x, 1), sp.Rational(3, 2))
    # Check: √4.01 ≈ 2.002498, so ≈ 3.012498/2.0201 ≈ 1.491262.
    xv = sp.Rational("1.01")
    assert rounds_to(sp.sqrt(xv + 3), "2.002498")
    assert equal(xv + sp.Rational("2.002498"), sp.Rational("3.012498"))
    assert equal(xv**2 + 1, sp.Rational("2.0201"))
    assert rounds_to(F.subs(x, xv), "1.491262")


@covers("eg-calc-limit-laws-resistors")
def test_eg_calc_limit_laws_resistors():
    R = 3 * t / (3 + t)
    # Step 1: defined for every t > 0 (the denominator vanishes only at t = −3).
    assert equal(sp.solveset(sp.Eq(3 + t, 0), t, sp.S.Reals), sp.FiniteSet(-3))
    # Step 2: 3 + 6 = 9 ≠ 0.  Step 3: R(6) = 18/9 = 2, by sp.limit and by substitution.
    assert equal((3 + t).subs(t, 6), 9)
    assert equal((3 * t).subs(t, 6), 18) and equal(sp.Rational(18, 9), 2)
    assert substitution_agrees(R, t, 6, 2)
    # Check: R(6.01) = 18.03/9.01 ≈ 2.00111.
    tv = sp.Rational("6.01")
    assert equal(R.subs(t, tv), sp.Rational("18.03") / sp.Rational("9.01"))
    assert rounds_to(R.subs(t, tv), "2.00111")
    # A parallel combination is smaller than each resistor: R(t) < 3 and R(t) < t for t > 0.
    pos = sp.Interval.open(0, sp.oo)
    assert equal(sp.solveset(R >= 3, t, pos), sp.S.EmptySet)
    assert equal(sp.solveset(R >= t, t, pos), sp.S.EmptySet)


@covers("eg-calc-limit-laws-hypotheses")
def test_eg_calc_limit_laws_hypotheses():
    # (i) numerator and denominator both → 0 at 1 (a genuine 0/0; the quotient is undefined at 1).
    assert substitution_agrees(x**2 - 1, x, 1, 0)
    assert substitution_agrees(x - 1, x, 1, 0)
    assert ((x**2 - 1) / (x - 1)).subs(x, 1) is sp.nan
    # (ii) 1/x has no limit at 0; x · (1/x) = 1 at every x ≠ 0, with the limit 1.
    assert no_two_sided_limit(1 / x, x, 0)
    assert limit_is(x * (1 / x), x, 0, 1)
    # (iii) x − 2 → 0, negative exactly for x < 2, so √(x − 2) is real on no interval left of 2.
    assert substitution_agrees(x - 2, x, 2, 0)
    assert equal(sp.solveset(x - 2 < 0, x, sp.S.Reals), sp.Interval.open(-sp.oo, 2))
    assert equal(sp.calculus.util.continuous_domain(sp.sqrt(x - 2), x, sp.S.Reals), sp.Interval(2, sp.oo))
    # Check: at 1.001, numerator 0.002001 and denominator 0.001; 0.001 · 1000 = 1; at 1.99,
    # x − 2 = −0.01, which has no real square root.
    xv = sp.Rational("1.001")
    assert equal(xv**2 - 1, sp.Rational("0.002001")) and equal(xv - 1, sp.Rational("0.001"))
    assert equal(sp.Rational("0.001") * 1000, 1)
    assert equal(sp.Rational("1.99") - 2, sp.Rational("-0.01")) and sp.sqrt(sp.Rational("-0.01")).is_real is False


# ── Exercises ────────────────────────────────────────────────────────────────────


@covers("exr-calc-limit-laws-given-limits")
def test_exr_calc_limit_laws_given_limits():
    Lf, Mg = sp.Integer(3), sp.Integer(-2)
    # The laws: (a) 2L − M, (b) L·M², (c) L/(M + 5) with M + 5 ≠ 0, (d) √(L + 1) with L + 1 > 0.
    assert Mg + 5 != 0 and Lf + 1 > 0
    expected = (2 * Lf - Mg, Lf * Mg**2, Lf / (Mg + 5), sp.sqrt(Lf + 1))
    # Second route: concrete f → 3, g → −2 at a = 1 (f = x + 2, g = x² − 3), by sp.limit.
    f, g = x + 2, x**2 - 3
    assert limit_is(f, x, 1, 3) and limit_is(g, x, 1, -2)
    concrete = (2 * f - g, f * g**2, f / (g + 5), sp.sqrt(f + 1))
    for expr, value in zip(concrete, expected):
        assert limit_is(expr, x, 1, value)
    assert equal(answer("exr-calc-limit-laws-given-limits"), expected)


@covers("exr-calc-limit-laws-polynomial")
def test_exr_calc_limit_laws_polynomial():
    p = 2 * x**3 - x + 4
    ans = answer("exr-calc-limit-laws-polynomial")
    assert substitution_agrees(p, x, -1, ans)
    assert equal(ans, p.subs(x, -1))


@covers("exr-calc-limit-laws-rational")
def test_exr_calc_limit_laws_rational():
    r_ = (x**2 + 1) / (x - 3)
    assert (x - 3).subs(x, 2) != 0
    ans = answer("exr-calc-limit-laws-rational")
    assert substitution_agrees(r_, x, 2, ans)
    assert equal(ans, sp.limit(r_, x, 2))


@covers("exr-calc-limit-laws-where-substitution")
def test_exr_calc_limit_laws_where_substitution():
    num, den = x + 2, x**2 - 4
    # The corollary applies exactly where the denominator is non-zero.
    expected = sp.Complement(sp.S.Reals, sp.solveset(sp.Eq(den, 0), x, sp.S.Reals))
    assert equal(sp.solveset(sp.Eq(den, 0), x, sp.S.Reals), sp.FiniteSet(-2, 2))
    got = answer("exr-calc-limit-laws-where-substitution")
    assert equal(got, expected)
    # At sample points of the set, substitution agrees with sp.limit.
    for a in (-5, sp.Rational(-21, 10), 0, sp.Rational(19, 10), sp.Rational(21, 10), 7):
        assert got.contains(a) is sp.true
        assert substitution_agrees(num / den, x, a, (num / den).subs(x, a))
    # The solution's remark on the excluded points: at 2 the numerator → 4 and the denominator → 0;
    # at −2 both → 0. (Not resolved here.)
    assert equal(num.subs(x, 2), 4) and equal(den.subs(x, 2), 0)
    assert equal(num.subs(x, -2), 0) and equal(den.subs(x, -2), 0)


@covers("exr-calc-limit-laws-roots")
def test_exr_calc_limit_laws_roots():
    F = (sp.sqrt(x) + x) / sp.sqrt(x**2 + 9)
    # x → 4 > 0, √x → 2; x² + 9 → 25 > 0, √(x² + 9) → 5 ≠ 0.
    assert limit_is(x, x, 4, 4) and limit_is(sp.sqrt(x), x, 4, 2)
    assert substitution_agrees(x**2 + 9, x, 4, 25) and limit_is(sp.sqrt(x**2 + 9), x, 4, 5)
    expected = (2 + 4) / sp.Integer(5)
    ans = answer("exr-calc-limit-laws-roots")
    assert equal(ans, expected)
    assert limit_is(F, x, 4, ans) and equal(F.subs(x, 4), ans)


@covers("exr-calc-limit-laws-lens")
def test_exr_calc_limit_laws_lens():
    vv = 5 * u / (u - 5)
    assert equal((u - 5).subs(u, 15), 10)
    ans = answer("exr-calc-limit-laws-lens")
    assert substitution_agrees(vv, u, 15, ans)
    assert equal(ans, sp.limit(vv, u, 15))
    # "7.5 cm", and at the focal point the numerator → 25, the denominator → 0.
    assert equal(ans, sp.Rational("7.5"))
    assert equal(sp.limit(5 * u, u, 5), 25) and equal(sp.limit(u - 5, u, 5), 0)


@covers("exr-calc-limit-laws-sum-delta")
def test_exr_calc_limit_laws_sum_delta():
    f, g = 3 * x - 2, 5 - x
    assert limit_is(f, x, 2, 4) and limit_is(g, x, 2, 3) and limit_is(f + g, x, 2, 7)
    # (a) the largest δ for f and for g with the tolerance ε/2, read off the good sets.
    assert equal(sp.Abs(f - 4), 3 * sp.Abs(x - 2)) and equal(sp.Abs(g - 3), sp.Abs(x - 2))
    d1 = half_width(sp.solveset(sp.Abs(f - 4) < eps / 2, x, sp.S.Reals), 2)
    d2 = half_width(sp.solveset(sp.Abs(g - 3) < eps / 2, x, sp.S.Reals), 2)
    proof_delta = sp.Min(d1, d2)
    # (b) the largest δ for f + g with ε.
    assert equal(f + g, 2 * x + 3)
    largest = half_width(sp.solveset(sp.Abs((f + g) - 7) < eps, x, sp.S.Reals), 2)
    assert equal(sp.Abs((f + g).subs(x, 2 + largest) - 7), eps)        # equality at the edge
    a_part, b_part = answer("exr-calc-limit-laws-sum-delta")
    assert equal(page_eps(a_part), proof_delta)
    assert equal(page_eps(b_part), largest)
    # The proof's δ works (exact pairs), and "three times smaller".
    assert implication_holds(lambda v: (3 * v - 2) + (5 - v), Q(2), Q(7), lambda e: e / 6, eps_samples(100))
    assert equal(largest / proof_delta, 3)
    # The solution's edge claim for f: at x = 2 + ε/6, |f − 4| = ε/2 exactly.
    assert equal(sp.Abs(f.subs(x, 2 + d1) - 4), eps / 2)


@covers("exr-calc-limit-laws-sum-part")
def test_exr_calc_limit_laws_sum_part():
    # g = (f + g) − f wherever both are defined, so the difference law gives lim g = K − L.
    fx, gx = sp.symbols("f_x g_x", real=True)
    assert equal((fx + gx) - fx, gx)
    # A concrete instance where g alone looks unruly but f + g and f have limits: f = 1/x² + x,
    # g = 2 − 1/x², at 1, where (f + g) − f is g again.
    f, g = 1 / x**2 + x, 2 - 1 / x**2
    assert limit_is(f, x, 1, 2) and limit_is(f + g, x, 1, 3) and limit_is(g, x, 1, 1)
    assert equal(sp.cancel((f + g) - f), g)
    # No counterexample exists: the claim follows from the difference law and the identity.
    expected = sp.true
    assert equal(answer("exr-calc-limit-laws-sum-part"), expected)


@covers("exr-calc-limit-laws-product-part")
def test_exr_calc_limit_laws_product_part():
    # Counterexample: f = x, g = 1/x at 0: lim f = 0, lim fg = 1, and g has no limit.
    f, g = x, 1 / x
    assert limit_is(f, x, 0, 0)
    assert equal(sp.cancel(f * g), 1) and limit_is(f * g, x, 0, 1)
    assert no_two_sided_limit(g, x, 0)
    claim_holds = False   # the hypotheses hold and the conclusion fails
    assert equal(answer("exr-calc-limit-laws-product-part"), sp.true if claim_holds else sp.false)
    # The page's argument: lim g = M would give lim fg = 0·M = 0 ≠ 1; and g = fg/f, but lim f = 0.
    M = sp.Symbol("M", real=True)
    assert equal(0 * M, 0)
    assert equal(sp.cancel((f * g) / f), g)


@covers("exr-calc-limit-laws-root-zero")
def test_exr_calc_limit_laws_root_zero():
    inner = x**2 + x**4
    assert substitution_agrees(inner, x, 0, 0)
    # The sign condition: x² + x⁴ = x²(1 + x²) ≥ 0 for every real x.
    assert equal(inner, x**2 * (1 + x**2))
    assert equal(sp.solveset(inner < 0, x, sp.S.Reals), sp.S.EmptySet)
    assert equal(sp.solveset(1 + x**2 < 1, x, sp.S.Reals), sp.S.EmptySet)
    ans = answer("exr-calc-limit-laws-root-zero")
    assert limit_is(sp.sqrt(inner), x, 0, ans)
    assert equal(ans, sp.sqrt(inner.subs(x, 0)))


@covers("exr-calc-limit-laws-root-domain")
def test_exr_calc_limit_laws_root_domain():
    # {x : cx − x² ≥ 0} = [min(0, c), max(0, c)] (checked on sample c); √(cx − x²) is defined on a
    # punctured open interval around 2 exactly when 2 lies inside this interval, not at an end.
    rng = random.Random(110)
    samples = [sp.Integer(v) for v in (-3, -1, 0, 1, 2, 3, 10)] + [sp.Rational(201, 100), sp.Rational(199, 100)]
    samples += [sp.Rational(rng.randint(-5000, 5000), 1000) for _ in range(30)]
    for cv in samples:
        S = sp.solveset(cv * x - x**2 >= 0, x, sp.S.Reals)
        assert equal(S, sp.Interval(sp.Min(0, cv), sp.Max(0, cv)))
        assert (S.interior.contains(2) is sp.true) == (cv > 2)
    # Symbolically: for c ≥ 0 the interior is (0, c), so 2 is inside iff c > 2; for c < 0 the
    # interior (c, 0) never contains 2.
    expected = sp.Union(sp.solveset(c > 2, c, sp.Interval(0, sp.oo)),
                        sp.solveset(sp.And(c < 2, 2 < 0), c, sp.Interval.open(-sp.oo, 0)))
    got = answer("exr-calc-limit-laws-root-domain")
    assert equal(got, expected)
    # For c > 2: cx − x² > 0 on (1, c), the limit under the root is 2c − 4 > 0, and the limit is
    # √(2c − 4) (the solution's value; the Answer prints only the set).
    for cv in (sp.Rational(5, 2), 3, 10):
        assert equal(sp.solveset(cv * x - x**2 <= 0, x, sp.Interval.open(1, cv)), sp.S.EmptySet)
        assert limit_is(sp.sqrt(cv * x - x**2), x, 2, sp.sqrt(2 * cv - 4))
    # c = 2: the limit under the root is 0, but 2x − x² < 0 just right of 2 (the solution's
    # x between 2 and 3).
    assert equal(sp.limit(2 * x - x**2, x, 2), 0)
    assert equal(sp.solveset(2 * x - x**2 < 0, x, sp.Interval.open(2, 3)), sp.Interval.open(2, 3))


@covers("exr-calc-limit-laws-constant-multiple")
def test_exr_calc_limit_laws_constant_multiple():
    # A manual answer (a proof): its key claims are checked here; it counts as covered only
    # through a reviewer's note in maths.manual_checked.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limit-laws-constant-multiple")
    fx, Lm, cr = sp.symbols("f_x L c_r", real=True)
    cn = sp.Symbol("c_n", real=True, nonzero=True)
    # |cf − cL| = |c||f − L|, and |c| · ε/|c| = ε for c ≠ 0, with ε/|c| > 0.
    assert equal(sp.Abs(cr * fx - cr * Lm), sp.Abs(cr) * sp.Abs(fx - Lm))
    assert equal(sp.Abs(cn) * (eps / sp.Abs(cn)), eps) and (eps / sp.Abs(cn)).is_positive
    # c = 0: 0·f − 0·L = 0 < ε.
    assert equal(0 * fx - 0 * Lm, 0)
    # The answer's δ on a concrete f: f = x² at 2 (δ_f(τ) = min(1, τ/5)), c ∈ {−3, ½, 7}: the δ for
    # the tolerance ε/|c| works for cf; for c = 0 any δ (here δ_f(1)) works.
    for i, cv in enumerate((Q(-3), Q(1, 2), Q(7))):
        assert implication_holds(lambda v: cv * v * v, Q(2), 4 * cv, lambda e: min(Q(1), e / abs(cv) / 5),
                                 eps_samples(120 + i), seed=i)
    assert implication_holds(lambda v: 0 * v * v, Q(2), Q(0), lambda e: Q(1), eps_samples(123, count=40))
    assert limit_is(-3 * x**2, x, 2, -12)


@covers("exr-calc-limit-laws-absolute-value")
def test_exr_calc_limit_laws_absolute_value():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limit-laws-absolute-value")
    # Part (c) of the triangle inequality, ||p| − |q|| ≤ |p − q|, on exact random pairs.
    rng = random.Random(130)
    for _ in range(3000):
        p, q = (Q(rng.randint(-10**6, 10**6), 991) for _ in range(2))
        assert abs(abs(p) - abs(q)) <= abs(p - q)
    # The answer's δ (the one for f with the tolerance ε) works for |f|, on concrete f with a
    # negative, a zero and a positive limit: f = x² − 4 at 1 (L = −3, δ = min(1, ε/3)), f = 2x − 6
    # at 3 (L = 0, δ = ε/2), f = 1/x at ½ (L = 2, δ = min(¼, ε/8): |1/x − 2| = 2|x − ½|/x < 8|x − ½|
    # on |x − ½| < ¼, where x > ¼).
    cases = [(lambda v: v * v - 4, Q(1), Q(-3), lambda e: min(Q(1), e / 3)),
             (lambda v: 2 * v - 6, Q(3), Q(0), lambda e: e / 2),
             (lambda v: 1 / v, Q(1, 2), Q(2), lambda e: min(Q(1, 4), e / 8))]
    for i, (f, a, Lv, d) in enumerate(cases):
        assert implication_holds(f, a, Lv, d, eps_samples(131 + i), seed=i)
        assert implication_holds(lambda v: abs(f(v)), a, abs(Lv), d, eps_samples(131 + i), seed=i)
    assert limit_is(sp.Abs(x**2 - 4), x, 1, 3)
