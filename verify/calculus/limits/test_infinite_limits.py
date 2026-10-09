"""Verification tests for content/calculus/limits/infinite-limits.md (calc-infinite-limits).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps; the answers are read
with answer(label), as printed on the page (`\\infty` is read as sp.oo).

The checks follow verify/calculus/limits/test_one_sided_limits.py, with a height M in place of a
tolerance ε: each displayed step is asserted, a chosen δ is checked symbolically on each branch of
a min, and the implication "x in the half-window of δ(M) ⇒ f(x) > M" (or "< −M") is tested on exact
rational (M, x) pairs up to the edge of the half-window. Floats could hide a failure at the edge, so
the sampled arithmetic is exact (fractions.Fraction). The Python functions raise outside the domain
the page gives, so a sampled point outside it fails the test.

Infinite one-sided limits are computed twice: with sp.limit(…, dir='+' / '-') through limit_is
(which also checks a table of values approaching the point), and from the propositions of the page,
with the δ their proofs build. Signs on an interval are read twice too: by counting the negative
factors at one point (the rule of prop-calc-rational-sign), and by solveset of f > 0 / f < 0 on the
whole interval.
"""

import random
from fractions import Fraction as Q

import pytest
import sympy as sp

from mathcheck import ManualAnswer, answer, c, covers, equal, limit_is, t, u, x

eps = sp.Symbol("epsilon", positive=True)
M = sp.Symbol("M", positive=True)
pos = sp.Symbol("p", positive=True)         # a positive number (a branch of a min, x − a > 0)
nonneg = sp.Symbol("q", nonnegative=True)
P = sp.Symbol("P", real=True)                # the pollution percentage p of exr-…-pollution
N = 10**6


def m_samples(seed, count=150, breaks=()):
    """Exact rational heights M > 0: tiny, moderate and huge ones, each break of a min (the M where
    the branches meet) and its immediate neighbours, and random ones."""
    rng = random.Random(seed)
    fixed = [Q(1, 10**9), Q(1, 1000), Q(1, 10), Q(1, 2), Q(1), Q(2), Q(3), Q(1000), Q(10**6), Q(10**9)]
    for b in breaks:
        fixed += [Q(b), Q(b) - Q(1, 10**9), Q(b) + Q(1, 10**9)]
    return fixed + [Q(rng.randint(1, 10**4 * N), N) for _ in range(count)]


def eps_samples(seed, count=150, breaks=()):
    """Exact rational tolerances ε > 0, as in test_one_sided_limits.py."""
    rng = random.Random(seed)
    fixed = [Q(1, 10**9), Q(1, 10**6), Q(1, 1000), Q(1, 100), Q(1, 10), Q(1, 2), Q(1), Q(3), Q(100), Q(10**6)]
    for b in breaks:
        fixed += [Q(b), Q(b) - Q(1, 10**9), Q(b) + Q(1, 10**9)]
    return fixed + [Q(rng.randint(1, 20 * N), N) for _ in range(count)]


def half_window(a, d, side, rng, count=40):
    """Exact rational points of a < x < a + d (side = +1) or a − d < x < a (side = −1): right next
    to a, within 10⁻⁹·d of the far edge, and random ones in between."""
    fractions = [Q(1, 10**9), Q(1, N), Q(N - 1, N), Q(10**9 - 1, 10**9)]
    fractions += [Q(rng.randint(1, N - 1), N) for _ in range(count)]
    for fr in fractions:
        yield a + side * d * fr


def window(a, d, rng, count=40):
    """Exact rational points of 0 < |x − a| < d, on both sides."""
    yield from half_window(a, d, 1, rng, count)
    yield from half_window(a, d, -1, rng, count)


def infinite_holds(f, a, choose_delta, heights, side, sign, seed=0, count=40):
    """x in the half-window of δ = choose_delta(M) ⇒ sign·f(x) > M, at every sampled (M, x):
    sign = +1 for the limit ∞, −1 for −∞ (f(x) < −M)."""
    rng = random.Random(seed)
    for mv in heights:
        d = choose_delta(mv)
        assert d > 0
        for xv in half_window(a, d, side, rng, count):
            assert (xv > a) if side > 0 else (xv < a)      # a is never in a half-window
            assert sign * f(xv) > mv, f"side {side:+d}, M = {mv}, δ = {d}, x = {xv}: f(x) = {f(xv)}"
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


def rational_sign(K, roots, point):
    """The sign prop-calc-rational-sign gives on an interval, read at one point of it: +1 if an
    even number of K, point − r (r over every root of the numerator and of the denominator, with
    repetition) are negative, −1 if an odd number are. Also returns that number."""
    negatives = sum(1 for v in [K] + [point - r for r in roots] if v < 0)
    return (1 if negatives % 2 == 0 else -1), negatives


def sign_on(expr, interval):
    """The sign of expr on the whole interval, by solveset: +1 if expr > 0 at every point, −1 if
    expr < 0 at every point; anything else fails."""
    if equal(sp.solveset(expr > 0, x, interval), interval):
        return 1
    if equal(sp.solveset(expr < 0, x, interval), interval):
        return -1
    raise AssertionError(f"{expr} changes sign on {interval}")


def reciprocal_power_delta(mv, m=Q(1), r=None):
    """The δ the page's proofs give for (h · 1/(x − a)ⁿ) at the height M: the proof of
    prop-calc-infinite-limit-product asks 1/(x − a)ⁿ for the height M/m, the proof of
    prop-calc-reciprocal-power-limits answers min(1, 1/(M/m)), and the product proof takes
    min(δ₁, r). With m = 1 and r = None, it is the reciprocal-power δ itself."""
    d1 = min(Q(1), 1 / (mv / m))
    return d1 if r is None else min(d1, r)


def undefined(*_):
    raise ValueError("outside the domain the page gives")


# ── Definitions and propositions (unlabelled for coverage, tested all the same) ─────────────


def test_definition_example_and_non_example():
    # Example: 1/x > M on 0 < x < 1/M, at exact points up to the edge; at the edge x = 1/M itself
    # 1/x = M, so this δ is the largest (a claim the page doesn't make, but its "M = 1/(1/M)").
    assert infinite_holds(lambda v: 1 / v, 0, lambda mv: 1 / mv, m_samples(1), 1, 1)
    assert equal(1 / (1 / M), M) and (1 / M).is_positive
    # Non-example: for x < 0, 1/x < 0 < 1, so every point of every left half-window fails M = 1.
    assert empty_on(1 / x >= 0, x, sp.Interval.open(-sp.oo, 0))
    assert limit_is(1 / x, x, 0, -sp.oo, dir="-")
    # The figure: 1/(x − 2) → ∞ from the right and −∞ from the left; 1/(x − 2)² → ∞ from both.
    assert limit_is(1 / (x - 2), x, 2, sp.oo, dir="+") and limit_is(1 / (x - 2), x, 2, -sp.oo, dir="-")
    assert limit_is(1 / (x - 2) ** 2, x, 2, sp.oo, dir="+") and limit_is(1 / (x - 2) ** 2, x, 2, sp.oo, dir="-")
    # The looking-ahead admonition: 1/x → 0 and x² → ∞ as x → ∞.
    assert limit_is(1 / x, x, sp.oo, 0) and limit_is(x**2, x, sp.oo, sp.oo)


def test_vertical_asymptote_non_example():
    # g = (x² − 1)/(x − 1) = x + 1 for x ≠ 1; on (0, 2) minus 1, 1 < g < 3.
    g_expr = (x**2 - 1) / (x - 1)
    assert equal(sp.cancel(g_expr), x + 1)
    punctured = sp.Union(sp.Interval.open(0, 1), sp.Interval.open(1, 2))
    assert empty_on(g_expr <= 1, x, punctured) and empty_on(g_expr >= 3, x, punctured)
    assert limit_is(g_expr, x, 1, 2)          # a finite limit, so no asymptote (second route)

    def g(v):
        if v == 1:
            undefined()
        return (v * v - 1) / (v - 1)

    # The points 1 ± ½·min(δ, 1) lie in (1, 2) and (0, 1), and there −3 < 1 < g < 3: they fail
    # the rounds M = 3 of ∞ and of −∞, for every sampled δ.
    rng = random.Random(2)
    for d in [Q(10**6), Q(2), Q(1), Q(1, 2), Q(1, 10**9)] + [Q(rng.randint(1, 10**9), N) for _ in range(300)]:
        for side in (1, -1):
            xv = 1 + side * min(d, Q(1)) / 2
            assert 0 < side * (xv - 1) < d and 0 < xv < 2
            assert -3 < g(xv) < 3


def test_prop_calc_reciprocal_power_limits():
    # Step 1: 0 < tⁿ ≤ t on (0, 1], for n = 1, …, 9 (SymPy, on the whole interval).
    unit = sp.Interval.Lopen(0, 1)
    for nv in range(1, 10):
        assert empty_on(t**nv > t, t, unit) and empty_on(t**nv <= 0, t, unit)
    # Step 2: with x − a = p > 0, (x − a)ⁿ = pⁿ = |x − a|ⁿ; with x − a = −p < 0, (−p)ⁿ is pⁿ for
    # even n and −pⁿ for odd n.
    for nv in range(1, 10):
        assert equal(pos**nv, sp.Abs(pos) ** nv)
        assert equal((-pos) ** nv, pos**nv if nv % 2 == 0 else -(pos**nv))
        assert equal(sp.Abs((-pos) ** nv), pos**nv)
    # Step 3, δ = min(1, 1/M), branch by branch. M ≤ 1 (M = 1/(1 + q)): δ = 1 ≤ 1/M, so t < δ gives
    # t < 1 and t < 1/M. M > 1 (M = 1 + p): δ = 1/M < 1. On each branch δ ≤ 1 and δ ≤ 1/M.
    m_low, m_high = 1 / (1 + nonneg), 1 + pos
    assert equal(sp.Min(1, 1 / m_low), 1) and (1 / m_low - 1).is_nonnegative
    assert equal(sp.Min(1, 1 / m_high), 1 / m_high) and sp.together(1 - 1 / m_high).is_positive
    # Then tⁿ ≤ t < 1/M and 1/(1/M) = M < 1/tⁿ: on each branch, M·δⁿ ≤ 1 (so M·tⁿ < 1 for t < δ),
    # by solveset over the branch's M: M ≤ 1 with δ = 1, M > 1 with δ = 1/M.
    m_real = sp.Symbol("m_real", real=True)
    for nv in range(1, 10):
        assert empty_on(m_real * 1**nv > 1, m_real, sp.Interval.Lopen(0, 1))
        assert empty_on(m_real * (1 / m_real) ** nv > 1, m_real, sp.Interval.open(1, sp.oo))
    # The implication itself, on exact (M, x), for n = 1, …, 8, several a, both sides: g(x) > M on
    # the right; on the left g(x) > M for even n and g(x) < −M for odd n.
    for nv in range(1, 9):
        for i, av in enumerate((Q(0), Q(2), Q(-1), Q(10), Q(3, 7))):
            def g(v, av=av, nv=nv):
                if v == av:
                    undefined()
                return 1 / (v - av) ** nv
            assert infinite_holds(g, av, reciprocal_power_delta, m_samples(10 * nv + i, breaks=(1,)), 1, 1,
                                  seed=nv, count=15)
            left_sign = 1 if nv % 2 == 0 else -1
            assert infinite_holds(g, av, reciprocal_power_delta, m_samples(10 * nv + i, breaks=(1,)), -1, left_sign,
                                  seed=nv, count=15)
    # SymPy's limits agree (a second route), at a = 0 and a = 2.
    for nv in range(1, 7):
        for av in (0, 2):
            assert limit_is(1 / (x - av) ** nv, x, av, sp.oo, dir="+")
            assert limit_is(1 / (x - av) ** nv, x, av, sp.oo if nv % 2 == 0 else -sp.oo, dir="-")


def test_prop_calc_infinite_limit_no_real_limit():
    # M = |L| + 1 ≥ 1 > 0, and L + 1 ≤ |L| + 1 = M and −M = −|L| − 1 ≤ L − 1, for every real L
    # (|L| − L ≥ 0 and |L| + L ≥ 0, on each sign of L).
    for lv in (pos, -pos, sp.Integer(0)):
        assert (sp.Abs(lv) + 1 - 1).is_nonnegative
        assert (sp.Abs(lv) - lv).is_nonnegative and (sp.Abs(lv) + lv).is_nonnegative
    # The midpoint x = a ± δ/2, δ = min(δ₁, δ₂), lies in both half-windows, on exact pairs.
    rng = random.Random(3)
    ds = [Q(1, 10**9), Q(1), Q(10**6)] + [Q(rng.randint(1, 10**9), N) for _ in range(60)]
    for d1 in ds:
        for d2 in ds[:20]:
            d = min(d1, d2)
            for av in (Q(0), Q(-5, 3)):
                xr, xl = av + d / 2, av - d / 2
                assert av < xr < av + d1 and av < xr < av + d2
                assert av - d1 < xl < av and av - d2 < xl < av
    # The argument on concrete f: with ε = 1 against M = |L| + 1, the δ₂ that wins the round M
    # (from the proof of the reciprocal powers) leaves, in every half-window of every δ₁, a point
    # where f(x) > M ≥ L + 1 (or f(x) < −M ≤ L − 1), so no δ₁ wins the round ε = 1 for L.
    Ls = [Q(0), Q(1), Q(-1), Q(10**6), Q(-10**6)] + [Q(rng.randint(-10**8, 10**8), 1000) for _ in range(200)]
    cases = [(lambda v: 1 / v, 1, 1), (lambda v: 1 / v, -1, -1), (lambda v: 1 / v**2, -1, 1), (lambda v: 1 / v**3, 1, 1)]
    for f, side, sign in cases:
        for lv in Ls:
            mv = abs(lv) + 1
            assert mv >= 1 > 0 and lv + 1 <= mv and -mv <= lv - 1
            d2 = reciprocal_power_delta(mv)
            for d1 in ds[:10]:
                xv = side * min(d1, d2) / 2
                assert sign * f(xv) > mv
                assert abs(f(xv) - lv) >= 1
    # (b): a one-sided limit ±∞ makes the two-sided limit fail; SymPy: no finite two-sided limit of
    # 1/x² at 0 (it is ∞), and 1/x has different one-sided limits.
    assert limit_is(1 / x**2, x, 0, sp.oo)
    assert limit_is(1 / x, x, 0, sp.oo, dir="+") and limit_is(1 / x, x, 0, -sp.oo, dir="-")
    # "In words": |x|/x has the one-sided limits 1 and −1 at 0 (a jump).
    assert limit_is(-x / x, x, 0, -1, dir="-") and equal(sp.Abs(-pos) / (-pos), -1) and equal(sp.Abs(pos) / pos, 1)


def test_prop_calc_infinite_limit_product():
    # (∗): F < −M exactly when −F > M.
    F = sp.Symbol("F", real=True)
    assert equal(sp.solveset(F < -M, F, sp.S.Reals), sp.solveset(-F > M, F, sp.S.Reals))
    # (a): M/m > 0, and h ≥ m, g > M/m > 0 give hg ≥ mg > M: with h = m + q (q ≥ 0) and
    # g = M/m + p (p > 0), hg − M = q·g + m·p > 0.
    mm = sp.Symbol("m", positive=True)
    hh, gg = mm + nonneg, M / mm + pos
    assert (M / mm).is_positive
    assert equal(hh * gg - mm * gg, nonneg * gg) and (nonneg * gg).is_nonnegative
    assert equal(mm * gg - M, mm * pos) and (mm * pos).is_positive
    # (c): |h − L| < L/2 gives h > L/2 for L > 0; |h − L| < −L/2 gives h < L/2 for L < 0.
    # (SymPy cannot intersect the intervals for a symbolic L, so for many exact L of each sign.)
    H = sp.Symbol("H", real=True)
    for lv in [sp.Rational(1, 1000), sp.Rational(1, 2), 1, sp.Rational(7, 3), 90, 10**6]:
        assert empty_on(sp.And(sp.Abs(H - lv) < lv / 2, H <= lv / 2), H, sp.S.Reals)
        assert empty_on(sp.And(sp.Abs(H + lv) < lv / 2, H >= -lv / 2), H, sp.S.Reals)
    # The proof's δ = min(δ₁, r) with δ₁ the reciprocal-power δ for the height M/m, on the
    # examples' windows and bounds m (and the left-hand versions), including the flipped sign of
    # (b). Each row: f, a, m, r, side, sign of the limit.
    rows = [
        (lambda v: (v + 1) / (v - 2), Q(2), Q(2), Q(1), 1, 1),                        # eg simple pole
        (lambda v: (v + 1) / (v - 2), Q(2), Q(2), Q(1), -1, -1),
        (lambda v: (v - 3) / (v**3 - v**2), Q(0), Q(5, 3), Q(1, 2), 1, 1),           # eg sign analysis
        (lambda v: (v - 3) / (v**3 - v**2), Q(0), Q(5, 3), Q(1, 2), -1, 1),
        (lambda v: (v - 3) / (v**3 - v**2), Q(1), Q(2, 3), Q(1, 2), 1, -1),
        (lambda v: (v - 3) / (v**3 - v**2), Q(1), Q(2, 3), Q(1, 2), -1, 1),
        (lambda v: (v * v - 1) / (v * v - 3 * v + 2), Q(2), Q(5, 2), Q(1, 2), 1, 1),  # eg hole, at 2
        (lambda v: (v * v - 1) / (v * v - 3 * v + 2), Q(2), Q(5, 2), Q(1, 2), -1, -1),
        (lambda v: 10 * v / (v - 10), Q(10), Q(90), Q(1), 1, 1),                    # eg lens
        (lambda v: 10 * v / (v - 10), Q(10), Q(90), Q(1), -1, -1),
        (lambda v: (1 / v - 1 / v**2), Q(0), Q(1, 2), Q(1, 2), 1, -1),               # common mistake
    ]
    for i, (f, av, mv_, rv, side, sign) in enumerate(rows):
        def choose(mv, mv_=mv_, rv=rv):
            return reciprocal_power_delta(mv, mv_, rv)
        assert infinite_holds(f, av, choose, m_samples(100 + i, breaks=(mv_, mv_ / rv)), side, sign, seed=i)
    # Rigorous track: h = x², g = 1/x on (0, 1): h > 0 and g → ∞, but hg = x < 1 there, so every
    # half-window has a point (x = ½·min(δ, 1)) that fails the round M = 1; and hg → 0.
    assert empty_on(x**2 <= 0, x, sp.Interval.open(0, 1)) and limit_is(1 / x, x, 0, sp.oo, dir="+")
    assert equal(x**2 * (1 / x), x) and empty_on(x >= 1, x, sp.Interval.open(0, 1))
    assert limit_is(x**2 * (1 / x), x, 0, 0, dir="+") and limit_is(x**2, x, 0, 0, dir="+")
    for d in [Q(10**6), Q(1), Q(1, 10**9)] + [Q(k, 997) for k in range(1, 2000, 37)]:
        xv = min(d, Q(1)) / 2
        assert 0 < xv < d and xv**2 * (1 / xv) < 1
    # h(x) = x → 0 and hg = 1, constant.
    assert limit_is(x, x, 0, 0, dir="+") and equal(x * (1 / x), 1)


# ── Examples ────────────────────────────────────────────────────────────────────


@covers("eg-calc-infinite-limits-simple-pole")
def test_eg_calc_infinite_limits_simple_pole():
    f_expr = (x + 1) / (x - 2)

    def f(v):
        if v == 2:
            undefined()
        return (v + 1) / (v - 2)

    # 1. Domain: the denominator vanishes only at 2.
    assert equal(sp.solveset(x - 2, x, sp.S.Reals), sp.FiniteSet(2))
    # 2. Sign (prop-calc-rational-sign, K = 1, numbers −1 and 2): at 3 no factor is negative, at 0
    # only x − 2; solveset agrees on the whole intervals.
    assert rational_sign(1, [-1, 2], 3) == (1, 0) and rational_sign(1, [-1, 2], 0) == (-1, 1)
    assert sign_on(f_expr, sp.Interval.open(2, sp.oo)) == 1 and sign_on(f_expr, sp.Interval.open(-1, 2)) == -1
    # 3. Split: f = (x + 1)·1/(x − 2).
    assert equal(f_expr, (x + 1) * (1 / (x - 2)))
    # 4. Bound: on (1, 3), 2 < x + 1 < 4, so h ≥ 2.
    assert equal(sp.imageset(sp.Lambda(x, x + 1), sp.Interval.open(1, 3)), sp.Interval.open(2, 4))
    # 5–6. The limits (SymPy and its table) and the boxed answer.
    assert limit_is(f_expr, x, 2, sp.oo, dir="+") and limit_is(f_expr, x, 2, -sp.oo, dir="-")
    # The same, with the δ of the proofs (min(δ₁, r), δ₁ = min(1, m/M), m = 2, r = 1).
    assert infinite_holds(f, 2, lambda mv: reciprocal_power_delta(mv, Q(2), Q(1)), m_samples(11, breaks=(2,)), 1, 1)
    assert infinite_holds(f, 2, lambda mv: reciprocal_power_delta(mv, Q(2), Q(1)), m_samples(12, breaks=(2,)), -1, -1)
    # 7. The two-sided limit: the one-sided limits differ (∞ against −∞), so it is neither.
    assert not equal(sp.limit(f_expr, x, 2, "+"), sp.limit(f_expr, x, 2, "-"))
    # Check: f(2.001) = 3001, f(1.999) = −2999.
    assert f(Q("2.001")) == 3001 and f(Q("1.999")) == -2999
    assert equal(sp.Rational("3.001") / sp.Rational("0.001"), 3001)
    # M = 1000: M/m = 500, δ = min(1, 1/500) = 0.002; x = 2.0019 lies in (2, 2.002) and
    # f(2.0019) = 3.0019/0.0019 ≈ 1579.9 > 1000.
    mv = Q(1000)
    assert mv / 2 == 500 and reciprocal_power_delta(mv, Q(2)) == Q("0.002")
    assert reciprocal_power_delta(mv, Q(2), Q(1)) == Q("0.002")
    xv = Q("2.0019")
    assert 2 < xv < 2 + Q("0.002")
    assert f(xv) == Q("3.0019") / Q("0.0019") and round(float(f(xv)), 1) == 1579.9 and f(xv) > 1000


@covers("eg-calc-infinite-limits-sign-analysis")
def test_eg_calc_infinite_limits_sign_analysis():
    f_expr = (x - 3) / (x**3 - x**2)

    def f(v):
        if v in (0, 1):
            undefined()
        return (v - 3) / (v**3 - v**2)

    # 1. Factor: x³ − x² = x·x·(x − 1), zero exactly at 0 and 1; the numerator is not 0 there.
    assert equal(x**3 - x**2, x * x * (x - 1))
    assert equal(sp.solveset(x**3 - x**2, x, sp.S.Reals), sp.FiniteSet(0, 1))
    assert not equal((x - 3).subs(x, 0), 0) and not equal((x - 3).subs(x, 1), 0)
    # 2. The sign chart: negative factors among x − 3, x, x, x − 1 at −1, ½, 2, 4, and the sign of
    # f on each whole interval by solveset.
    chart = [(sp.Interval.open(-sp.oo, 0), Q(-1), 4, 1), (sp.Interval.open(0, 1), Q(1, 2), 2, 1),
             (sp.Interval.open(1, 3), Q(2), 1, -1), (sp.Interval.open(3, sp.oo), Q(4), 0, 1)]
    for interval, point, page_count, page_sign in chart:
        assert sp.sympify(point) in interval
        sign, count = rational_sign(1, [3, 0, 0, 1], point)
        assert (sign, count) == (page_sign, page_count)
        assert sign_on(f_expr, interval) == page_sign
    # 3. At 0: f = h₀·1/x², h₀ = (x − 3)/(x − 1) = (3 − x)/(1 − x). On (−½, ½): 5/2 < 3 − x < 7/2,
    # ½ < 1 − x < 3/2, 1/(1 − x) > 2/3, and h₀ > 5/2·1/(1 − x) > 5/2·2/3 = 5/3.
    h0 = (x - 3) / (x - 1)
    assert equal(f_expr, h0 * (1 / x**2)) and equal(h0, (3 - x) / (1 - x))
    near0 = sp.Interval.open(-sp.Rational(1, 2), sp.Rational(1, 2))
    assert equal(sp.imageset(sp.Lambda(x, 3 - x), near0), sp.Interval.open(sp.Rational(5, 2), sp.Rational(7, 2)))
    assert equal(sp.imageset(sp.Lambda(x, 1 - x), near0), sp.Interval.open(sp.Rational(1, 2), sp.Rational(3, 2)))
    assert empty_on(1 / (1 - x) <= sp.Rational(2, 3), x, near0)
    assert empty_on(h0 <= sp.Rational(5, 2) / (1 - x), x, near0)
    assert equal(sp.Rational(5, 2) * sp.Rational(2, 3), sp.Rational(5, 3))
    assert empty_on(h0 <= sp.Rational(5, 3), x, near0)
    # 4. Limits at 0: ∞ from both sides, so the two-sided limit is ∞.
    assert limit_is(f_expr, x, 0, sp.oo, dir="+") and limit_is(f_expr, x, 0, sp.oo, dir="-")
    assert limit_is(f_expr, x, 0, sp.oo)
    # 5. At 1: f = h₁·1/(x − 1), h₁ = (x − 3)/x². On (½, 3/2): x − 3 < −3/2, x² < (3/2)x < 9/4,
    # 1/x² > 4/9, h₁ < −3/2·1/x² < −3/2·4/9 = −2/3.
    h1 = (x - 3) / x**2
    assert equal(f_expr, h1 * (1 / (x - 1)))
    near1 = sp.Interval.open(sp.Rational(1, 2), sp.Rational(3, 2))
    assert empty_on(x - 3 >= -sp.Rational(3, 2), x, near1)
    assert empty_on(x**2 >= sp.Rational(3, 2) * x, x, near1) and empty_on(sp.Rational(3, 2) * x >= sp.Rational(9, 4), x, near1)
    assert empty_on(1 / x**2 <= sp.Rational(4, 9), x, near1)
    assert empty_on(h1 >= -sp.Rational(3, 2) / x**2, x, near1)
    assert equal(-sp.Rational(3, 2) * sp.Rational(4, 9), -sp.Rational(2, 3))
    assert empty_on(h1 >= -sp.Rational(2, 3), x, near1)
    # 6. Limits at 1.
    assert limit_is(f_expr, x, 1, -sp.oo, dir="+") and limit_is(f_expr, x, 1, sp.oo, dir="-")
    # With the proofs' δ on the half-windows (m = 5/3 at 0, 2/3 at 1, r = ½).
    for side, sign, av, mv_ in ((1, 1, 0, Q(5, 3)), (-1, 1, 0, Q(5, 3)), (1, -1, 1, Q(2, 3)), (-1, 1, 1, Q(2, 3))):
        assert infinite_holds(f, av, lambda mv, mv_=mv_: reciprocal_power_delta(mv, mv_, Q(1, 2)),
                              m_samples(20 + side + 3 * av, breaks=(mv_, 2 * mv_)), side, sign)
    # Check: f(0.01) ≈ 30 202, f(0.99) ≈ 205.08, f(1.01) ≈ −195.08; h₁(1.01) ≈ −1.95 ≤ −2/3.
    assert Q("0.01") ** 3 - Q("0.01") ** 2 == Q("0.000001") - Q("0.0001")
    assert Q("0.99") ** 3 == Q("0.970299") and Q("0.99") ** 2 == Q("0.9801")
    assert Q("1.01") ** 3 == Q("1.030301") and Q("1.01") ** 2 == Q("1.0201")
    assert round(float(f(Q("0.01")))) == 30202
    assert round(float(f(Q("0.99"))), 2) == 205.08 and round(float(f(Q("1.01"))), 2) == -195.08
    h1v = (Q("1.01") - 3) / Q("1.01") ** 2
    assert h1v == Q("-1.99") / Q("1.0201") and round(float(h1v), 2) == -1.95 and h1v <= Q(-2, 3)


@covers("eg-calc-infinite-limits-hole")
def test_eg_calc_infinite_limits_hole():
    f_expr = (x**2 - 1) / (x**2 - 3 * x + 2)

    def f(v):
        if v in (1, 2):
            undefined()
        return (v * v - 1) / (v * v - 3 * v + 2)

    # 1. Factor; the denominator is zero exactly at 1 and 2.
    assert equal(x**2 - 1, (x - 1) * (x + 1)) and equal(x**2 - 3 * x + 2, (x - 1) * (x - 2))
    assert equal(sp.solveset(x**2 - 3 * x + 2, x, sp.S.Reals), sp.FiniteSet(1, 2))
    # 2. Cancel: f = (x + 1)/(x − 2) for x ≠ 1, 2.
    assert equal(sp.cancel(f_expr), (x + 1) / (x - 2))
    # 3. At 1: f + 2 = (x + 1 + 2(x − 2))/(x − 2) = 3(x − 1)/(x − 2).
    assert equal((x + 1) / (x - 2) + 2, (x + 1 + 2 * (x - 2)) / (x - 2))
    assert equal(x + 1 + 2 * (x - 2), 3 * (x - 1))
    # |x − 1| < ½ gives ½ < x < 3/2, x − 2 < −½, |x − 2| = 2 − x > ½ and 1/|x − 2| < 2.
    near1 = sp.Interval.open(sp.Rational(1, 2), sp.Rational(3, 2))
    assert equal(sp.solveset(sp.Abs(x - 1) < sp.Rational(1, 2), x, sp.S.Reals), near1)
    assert empty_on(x - 2 >= -sp.Rational(1, 2), x, near1)
    assert empty_on(1 / (2 - x) >= 2, x, near1)
    # δ = min(½, ε/6), branch by branch: ε ≤ 3 gives δ = ε/6 ≤ ½, ε > 3 gives δ = ½ < ε/6; on both,
    # δ ≤ ½ and 6δ ≤ ε (solveset over each branch's ε).
    ev = sp.Symbol("e_real", real=True)
    assert empty_on(ev / 6 > sp.Rational(1, 2), ev, sp.Interval.Lopen(0, 3))
    assert empty_on(6 * sp.Rational(1, 2) > ev, ev, sp.Interval.open(3, sp.oo))
    # The implication on exact (ε, x), both sides, up to the edge.
    assert two_sided_holds(f, 1, -2, lambda e: min(Q(1, 2), e / 6), eps_samples(30, breaks=(3,)))
    assert limit_is(f_expr, x, 1, -2)
    # Both one-sided limits are −2: no asymptote at 1.
    assert limit_is(f_expr, x, 1, -2, dir="+") and limit_is(f_expr, x, 1, -2, dir="-")
    # 4. At 2: on (3/2, 5/2), x + 1 > 5/2; the limits.
    assert equal(sp.imageset(sp.Lambda(x, x + 1), sp.Interval.open(sp.Rational(3, 2), sp.Rational(5, 2))),
                 sp.Interval.open(sp.Rational(5, 2), sp.Rational(7, 2)))
    assert limit_is(f_expr, x, 2, sp.oo, dir="+") and limit_is(f_expr, x, 2, -sp.oo, dir="-")
    # Check: f(1.001) ≈ −2.003 (0.002001 over −0.000999), f(2.001) ≈ 3001 (3.004001 over 0.001001).
    a1 = Q("1.001")
    assert a1 * a1 - 1 == Q("0.002001") and a1 * a1 - 3 * a1 + 2 == Q("-0.000999")
    assert round(float(f(a1)), 3) == -2.003
    a2 = Q("2.001")
    assert a2 * a2 - 1 == Q("3.004001") and a2 * a2 - 3 * a2 + 2 == Q("0.001001")
    assert round(float(f(a2))) == 3001
    # ε = 0.06: δ = min(½, 0.01) = 0.01; x = 1.009 gives |f + 2| = 3·0.009/0.991 ≈ 0.0272 < 0.06.
    e = Q("0.06")
    assert min(Q(1, 2), e / 6) == Q("0.01")
    xv = Q("1.009")
    assert 0 < abs(xv - 1) < Q("0.01")
    assert abs(f(xv) + 2) == 3 * Q("0.009") / Q("0.991") and round(float(abs(f(xv) + 2)), 4) == 0.0272 < 0.06


@covers("eg-calc-infinite-limits-lens")
def test_eg_calc_infinite_limits_lens():
    v_expr = 10 * u / (u - 10)

    def v(w):
        if w == 10:
            undefined()
        return 10 * w / (w - 10)

    # The thin-lens equation: 1/u + 1/v = 1/10 solved for v.
    vv = sp.Symbol("v", real=True)
    solved = sp.solve(sp.Eq(1 / u + 1 / vv, sp.Rational(1, 10)), vv)
    assert len(solved) == 1 and equal(solved[0], v_expr)
    # The table of Why this matters, and "10.01 cm gives an image 100 metres away" (10 010 cm).
    table = {"11": 110, "10.1": 1010, "10.01": 10010, "9.99": -9990, "9.9": -990}
    for w, value in table.items():
        assert v(Q(w)) == value
    assert round(v(Q("10.01")) / 100) == 100
    # 1. Split and bound: v = 10u·1/(u − 10); on (9, 11), 10u > 90.
    assert equal(v_expr, 10 * u * (1 / (u - 10)))
    assert empty_on(10 * u <= 90, u, sp.Interval.open(9, 11))
    # 2. (a) The limits, by SymPy and with the proofs' δ (m = 90, r = 1).
    assert limit_is(v_expr, u, 10, sp.oo, dir="+") and limit_is(v_expr, u, 10, -sp.oo, dir="-")
    assert infinite_holds(v, 10, lambda mv: reciprocal_power_delta(mv, Q(90), Q(1)), m_samples(40, breaks=(90,)), 1, 1)
    assert infinite_holds(v, 10, lambda mv: reciprocal_power_delta(mv, Q(90), Q(1)), m_samples(41, breaks=(90,)), -1, -1)
    # 3. (b) For u > 10: v > 1000 exactly when 10u > 1000u − 10 000, i.e. 10 000 > 990u, i.e.
    # u < 1000/99. SymPy solves v > 1000 on u > 10 directly.
    right = sp.Interval.open(10, sp.oo)
    good = sp.solveset(v_expr > 1000, u, right)
    assert equal(good, sp.solveset(10 * u > 1000 * u - 10000, u, right))
    assert equal(good, sp.solveset(10000 > 990 * u, u, right))
    assert equal(good.inf, 10)
    largest = good.sup - 10
    # 4. The largest δ is 10/99 (derived: sup of the good set minus 10).
    assert equal(largest, sp.Rational(10, 99)) and equal(good.sup, sp.Rational(1000, 99))
    # It works (exactly, up to the edge), and at u = 1000/99 = 10 + δ the image is at exactly 1000.
    d = Q(10, 99)
    assert infinite_holds(v, 10, lambda _: d, [Q(1000)], 1, 1, count=3000)
    assert v(Q(1000, 99)) == 1000
    assert equal(v_expr.subs(u, sp.Rational(1000, 99)), sp.Rational(10000, 99) / sp.Rational(10, 99))
    # Any larger δ contains 1000/99 (sampled: 10 + δ' > 1000/99 for δ' slightly above 10/99).
    for extra in (Q(1, 10**12), Q(1, 1000), Q(1)):
        assert 10 < Q(1000, 99) < 10 + d + extra
    # 10/99 ≈ 0.101 cm, about a millimetre.
    assert round(float(d), 3) == 0.101 and round(float(d) * 10) == 1
    # Check: 10.1 < 1000/99 = 10.1010…, v(10.1) = 101/0.1 = 1010 > 1000.
    assert Q("10.1") < Q(1000, 99) and v(Q("10.1")) == Q(101) / Q("0.1") == 1010


# ── Exercises ───────────────────────────────────────────────────────────────────


@covers("exr-calc-infinite-limits-reciprocal-powers")
def test_exr_calc_infinite_limits_reciprocal_powers():
    # Each as 1/(x − a)ⁿ from the left: (a) a = 3, n = 1; (b) a = −1, n = 4; (c) a = 0, n = 5.
    cases = [(1 / (x - 3), 3, 1), (1 / (x + 1) ** 4, -1, 4), (1 / x**5, 0, 5)]
    expected = []
    for expr, av, nv in cases:
        assert equal(expr, 1 / (x - av) ** nv)
        by_parity = sp.oo if nv % 2 == 0 else -sp.oo           # prop-calc-reciprocal-power-limits
        by_sympy = sp.limit(expr, x, av, "-")
        assert equal(by_parity, by_sympy) and limit_is(expr, x, av, by_parity, dir="-")
        expected.append(by_parity)
    got = answer("exr-calc-infinite-limits-reciprocal-powers")
    assert equal(got, tuple(expected))


@covers("exr-calc-infinite-limits-quotient-sign")
def test_exr_calc_infinite_limits_quotient_sign():
    f_expr = (x - 5) / (x - 3)

    def f(v):
        if v == 3:
            undefined()
        return (v - 5) / (v - 3)

    left, right = sp.limit(f_expr, x, 3, "-"), sp.limit(f_expr, x, 3, "+")
    assert limit_is(f_expr, x, 3, left, dir="-") and limit_is(f_expr, x, 3, right, dir="+")
    got = answer("exr-calc-infinite-limits-quotient-sign")
    assert equal(got, (left, right))
    # The solution: h = x − 5 ≤ −1 on (2, 4); the proofs' δ with m = 1, r = 1, sign flipped.
    assert empty_on(x - 5 > -1, x, sp.Interval.open(2, 4))
    assert infinite_holds(f, 3, lambda mv: reciprocal_power_delta(mv, Q(1), Q(1)), m_samples(50, breaks=(1,)), -1, 1)
    assert infinite_holds(f, 3, lambda mv: reciprocal_power_delta(mv, Q(1), Q(1)), m_samples(51, breaks=(1,)), 1, -1)
    # The sign chart: positive on (−∞, 3) (two negative factors), negative on (3, 5) (one).
    assert rational_sign(1, [5, 3], 0) == (1, 2) and rational_sign(1, [5, 3], 4) == (-1, 1)
    assert sign_on(f_expr, sp.Interval.open(-sp.oo, 3)) == 1 and sign_on(f_expr, sp.Interval.open(3, 5)) == -1


@covers("exr-calc-infinite-limits-asymptotes")
def test_exr_calc_infinite_limits_asymptotes():
    f_expr = (x + 5) / (x**2 - 9)
    zeros = sorted(sp.solveset(x**2 - 9, x, sp.S.Reals))
    asymptotes = []
    for av in zeros:
        one_sided = [sp.limit(f_expr, x, av, d) for d in ("-", "+")]
        if any(lim in (sp.oo, -sp.oo) for lim in one_sided):
            asymptotes.append(av)
            for d, lim in zip(("-", "+"), one_sided):
                assert limit_is(f_expr, x, av, lim, dir=d)
    got = answer("exr-calc-infinite-limits-asymptotes")
    assert equal(got, tuple(asymptotes))
    # The solution's claims: the numerator is 8 at 3 and 2 at −3; h = (x + 5)/(x + 3) > 8/7 on (3, 4);
    # k = (x + 5)/(x − 3) < −1/3 on (−3, −2); the limits it names.
    assert equal((x + 5).subs(x, 3), 8) and equal((x + 5).subs(x, -3), 2)
    assert empty_on((x + 5) / (x + 3) <= sp.Rational(8, 7), x, sp.Interval.open(3, 4))
    assert equal((x + 5) / (x - 3), -(x + 5) / (3 - x))
    assert empty_on((x + 5) / (3 - x) <= sp.Rational(1, 3), x, sp.Interval.open(-3, -2))
    assert empty_on((x + 5) / (x - 3) >= -sp.Rational(1, 3), x, sp.Interval.open(-3, -2))
    assert limit_is(f_expr, x, 3, sp.oo, dir="+") and limit_is(f_expr, x, -3, -sp.oo, dir="+")


@covers("exr-calc-infinite-limits-not-a-number")
def test_exr_calc_infinite_limits_not_a_number():
    # The hypothesis holds for f = 1/x² at 0 (and 1/x⁴): lim = ∞ from both sides. For every sampled
    # candidate L, ε = 1 against M = |L| + 1 leaves a point of every punctured window (the
    # reciprocal-power δ for M, halved) where |f − L| ≥ 1: no real L is the limit.
    rng = random.Random(60)
    Ls = [Q(0), Q(1), Q(-1), Q(10**6)] + [Q(rng.randint(-10**8, 10**8), 1000) for _ in range(200)]
    ds = [Q(1, 10**9), Q(1), Q(10**6)] + [Q(rng.randint(1, 10**9), N) for _ in range(10)]
    some_L_works = False
    for nv in (2, 4):
        assert limit_is(1 / x**nv, x, 0, sp.oo)
        for lv in Ls:
            d2 = reciprocal_power_delta(abs(lv) + 1)
            fails = all(abs(1 / (s * min(d1, d2) / 2) ** nv - lv) >= 1 for d1 in ds for s in (1, -1))
            if not fails:
                some_L_works = True
    got = answer("exr-calc-infinite-limits-not-a-number")
    assert equal(got, sp.true if some_L_works else sp.false)


@covers("exr-calc-infinite-limits-largest-delta")
def test_exr_calc_infinite_limits_largest_delta():
    right = sp.Interval.open(0, sp.oo)
    good = sp.solveset(1 / x**3 > 1000, x, right)
    # A second route: on x > 0, 1/x³ > 1000 exactly when x³ < 1/1000.
    assert equal(good, sp.solveset(x**3 < sp.Rational(1, 1000), x, right))
    assert equal(good.inf, 0)
    largest = good.sup
    got = answer("exr-calc-infinite-limits-largest-delta")
    assert equal(got, largest)
    # It works, exactly up to the edge; at the edge itself 1/x³ = 1000 (so no larger δ).
    d = Q(1, 10)
    assert equal(largest, sp.Rational(1, 10))
    assert infinite_holds(lambda v: 1 / v**3, 0, lambda _: d, [Q(1000)], 1, 1, count=3000)
    assert 1 / d**3 == 1000
    # The solution: 1000 = 1/(1/10)³, and the proof's δ = min(1, 1/1000) = 1/1000 is smaller.
    assert reciprocal_power_delta(Q(1000)) == Q(1, 1000) < d


@covers("exr-calc-infinite-limits-two-poles")
def test_exr_calc_infinite_limits_two_poles():
    f_expr = (x - 2) / (x**2 + x)
    points = [(-1, "-"), (-1, "+"), (0, "-"), (0, "+")]
    limits = []
    for av, d in points:
        lim = sp.limit(f_expr, x, av, d)
        assert limit_is(f_expr, x, av, lim, dir=d)
        limits.append(lim)
    got = answer("exr-calc-infinite-limits-two-poles")
    assert equal(got, tuple(limits))
    # The sign chart (numbers −1, 0, 2): negatives 3, 2, 1 on (−∞, −1), (−1, 0), (0, 2).
    for interval, point, count in ((sp.Interval.open(-sp.oo, -1), -2, 3), (sp.Interval.open(-1, 0), Q(-1, 2), 2),
                                   (sp.Interval.open(0, 2), 1, 1)):
        sign, cnt = rational_sign(1, [2, 0, -1], point)
        assert cnt == count and sign_on(f_expr, interval) == sign
    # The bounds: h = (x − 2)/x = (2 − x)/(−x) > 5/3 on (−3/2, −1/2); k = (x − 2)/(x + 1) < −1 on (−½, ½).
    assert equal(f_expr, (x - 2) / x * (1 / (x + 1))) and equal((x - 2) / x, (2 - x) / (-x))
    assert empty_on((x - 2) / x <= sp.Rational(5, 3), x, sp.Interval.open(-sp.Rational(3, 2), -sp.Rational(1, 2)))
    assert empty_on((x - 2) / (x + 1) >= -1, x, sp.Interval.open(-sp.Rational(1, 2), sp.Rational(1, 2)))
    assert equal(-sp.Rational(3, 2) * sp.Rational(2, 3), -1)


@covers("exr-calc-infinite-limits-hole")
def test_exr_calc_infinite_limits_hole():
    f_expr = (x**2 - 4) / (x**2 - x - 2)
    zeros = sorted(sp.solveset(x**2 - x - 2, x, sp.S.Reals))
    asymptotes = []
    for av in zeros:
        one_sided = [sp.limit(f_expr, x, av, d) for d in ("-", "+")]
        if any(lim in (sp.oo, -sp.oo) for lim in one_sided):
            asymptotes.append(av)
    got = answer("exr-calc-infinite-limits-hole")
    assert equal(got, asymptotes[0] if len(asymptotes) == 1 else tuple(asymptotes))
    # The solution: cancel x − 2; at −1 the limit from the right is ∞ (x + 2 > ½ on (−3/2, −½));
    # at 2 the limit is 4/3, with δ = min(1, 6ε).
    assert equal(sp.cancel(f_expr), (x + 2) / (x + 1))
    assert empty_on(x + 2 <= sp.Rational(1, 2), x, sp.Interval.open(-sp.Rational(3, 2), -sp.Rational(1, 2)))
    assert limit_is(f_expr, x, -1, sp.oo, dir="+") and limit_is(f_expr, x, -1, -sp.oo, dir="-")
    assert limit_is(f_expr, x, 2, sp.Rational(4, 3))
    assert equal((x + 2) / (x + 1) - sp.Rational(4, 3), (2 - x) / (3 * (x + 1)))
    assert empty_on(1 / (3 * (x + 1)) >= sp.Rational(1, 6), x, sp.Interval.open(1, 3))

    def f(v):
        if v in (2, -1):
            undefined()
        return (v * v - 4) / (v * v - v - 2)

    assert two_sided_holds(f, 2, Q(4, 3), lambda e: min(Q(1), 6 * e), eps_samples(70, breaks=(Q(1, 6),)))


@covers("exr-calc-infinite-limits-pollution")
def test_exr_calc_infinite_limits_pollution():
    C = 50 * P / (100 - P)

    def cost(pv):
        if not 0 <= pv < 100:
            undefined()
        return 50 * pv / (100 - pv)

    lim = sp.limit(C, P, 100, "-")
    assert limit_is(C, P, 100, lim, dir="-")
    domain = sp.Interval.Ropen(0, 100)
    good = sp.solveset(C > 4950, P, domain)
    assert equal(good.sup, 100)
    largest = 100 - good.inf
    got = answer("exr-calc-infinite-limits-pollution")
    assert equal(got, (lim, largest))
    # δ = 1 works exactly up to the edge, and C(99) = 4950 is not more than 4950.
    assert infinite_holds(cost, 100, lambda _: Q(1), [Q(4950)], -1, 1, count=3000)
    assert cost(Q(99)) == 4950
    # The solution's (a): C = (−50p)·1/(p − 100), −50p < −4950 on (99, 100), and the proofs' δ
    # with m = 4950, r = 1 on the left (the sign flipped twice).
    assert equal(C, (-50 * P) * (1 / (P - 100)))
    assert empty_on(-50 * P >= -4950, P, sp.Interval.open(99, 100))
    assert infinite_holds(cost, 100, lambda mv: reciprocal_power_delta(mv, Q(4950), Q(1)),
                          m_samples(80, breaks=(4950,)), -1, 1)
    # (b): 50p > 4950(100 − p) ⇔ 5000p > 495 000 ⇔ p > 99; 4950 thousand pounds = £4.95 million.
    assert equal(sp.expand(4950 * (100 - P)), 495000 - 4950 * P)
    assert equal(good, sp.solveset(5000 * P > 495000, P, domain))
    assert Q(4950 * 1000, 10**6) == Q("4.95")


@covers("exr-calc-infinite-limits-difference")
def test_exr_calc_infinite_limits_difference():
    # The statement's hypotheses hold for f = 1/x + 1, g = 1/x at 0, and f − g → 1, not 0: a
    # counterexample, so the statement is false.
    f_expr, g_expr = 1 / x + 1, 1 / x
    assert limit_is(f_expr, x, 0, sp.oo, dir="+") and limit_is(g_expr, x, 0, sp.oo, dir="+")
    diff_lim = sp.limit(f_expr - g_expr, x, 0, "+")
    assert equal(f_expr - g_expr, 1) and equal(diff_lim, 1)
    is_counterexample = not equal(diff_lim, 0)
    got = answer("exr-calc-infinite-limits-difference")
    assert equal(got, sp.false if is_counterexample else sp.true)
    # The solution: f = (1 + x)·1/x with 1 + x > 1 on (0, 1); the proofs' δ (m = 1, r = 1).
    assert equal(f_expr, (1 + x) * (1 / x)) and empty_on(1 + x <= 1, x, sp.Interval.open(0, 1))
    assert infinite_holds(lambda v: 1 / v + 1, 0, lambda mv: reciprocal_power_delta(mv, Q(1), Q(1)),
                          m_samples(90, breaks=(1,)), 1, 1)
    # Other choices: 2/x − 1/x = 1/x → ∞; 1/x − 1/x² → −∞.
    assert limit_is(2 / x - 1 / x, x, 0, sp.oo, dir="+") and limit_is(1 / x - 1 / x**2, x, 0, -sp.oo, dir="+")
    assert equal(1 / x - 1 / x**2, (x - 1) * (1 / x**2))
    # F = 1/x + 1 for x > 0, F = 0 for x ≤ 0: F(0) = 0 and F → ∞ as x → 0+ (from the formula of the
    # right side, as SymPy mis-evaluates limits of Piecewise).
    F = sp.Piecewise((1 / x + 1, x > 0), (0, True))
    assert equal(F.subs(x, 0), 0) and limit_is(1 / x + 1, x, 0, sp.oo, dir="+")


@covers("exr-calc-infinite-limits-from-definition")
def test_exr_calc_infinite_limits_from_definition():
    # A manual answer (a proof): its key claims are checked here; it counts as covered only
    # through a reviewer's note in maths.manual_checked.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-infinite-limits-from-definition")
    f_expr = x / (x - 1)
    assert limit_is(f_expr, x, 1, sp.oo, dir="+")
    # x/(x − 1) = x·1/(x − 1), and x/(x − 1) − 1/(x − 1) = 1 > 0 (the factor x > 1 helps).
    assert equal(f_expr, x * (1 / (x - 1))) and equal(f_expr - 1 / (x - 1), 1)
    # The answer's δ = 1/M, on exact (M, x) up to the edge.
    assert infinite_holds(lambda v: v / (v - 1), 1, lambda mv: 1 / mv, m_samples(100), 1, 1)


@covers("exr-calc-infinite-limits-reciprocal")
def test_exr_calc_infinite_limits_reciprocal():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-infinite-limits-reciprocal")
    # f > M = 1/ε > 0 gives 0 < 1/f < ε: with f = 1/ε + p, ε − 1/f > 0.
    fv = 1 / eps + pos
    assert (1 / eps).is_positive and (1 / fv).is_positive and sp.simplify(eps - 1 / fv).is_positive
    # The answer's δ (one that wins the round M = 1/ε for f) works for 1/f with ε, on concrete f
    # with the reciprocal-power δ (and s = 1, from the round M = 1): f = 1/x, 1/x², x/(x − 1) at 1.
    rng = random.Random(110)
    cases = [(lambda v: 1 / v, Q(0), reciprocal_power_delta), (lambda v: 1 / v**2, Q(0), reciprocal_power_delta),
             (lambda v: v / (v - 1), Q(1), lambda mv: 1 / mv)]
    for f, av, choose in cases:
        s = choose(Q(1))
        for e in eps_samples(111):
            d = min(choose(1 / e), s)
            for xv in half_window(av, d, 1, rng, 10):
                assert f(xv) > 0 and abs(1 / f(xv) - 0) < e
    assert limit_is(x, x, 0, 0, dir="+") and limit_is(1 / (1 / x**2), x, 0, 0, dir="+")
    # The converse fails: g = −1/x, 1/g = −x → 0, but g → −∞.
    assert equal(1 / (-1 / x), -x) and limit_is(-x, x, 0, 0, dir="+") and limit_is(-1 / x, x, 0, -sp.oo, dir="+")


@covers("exr-calc-infinite-limits-parameter")
def test_exr_calc_infinite_limits_parameter():
    den = x**2 - 4 * x + 3
    zeros = sorted(sp.solveset(den, x, sp.S.Reals))
    assert equal(den, (x - 1) * (x - 3)) and equal(tuple(zeros), (1, 3))
    # Each zero is simple, so it gives an asymptote unless the numerator x − c is 0 there: the c
    # that cancel a zero are the solutions of a − c = 0, for a = 1 and a = 3. Exactly one asymptote
    # iff exactly one zero is cancelled; no c cancels both (1 ≠ 3).
    cancelling = sorted(set().union(*(sp.solveset(av - c, c, sp.S.Reals) for av in zeros)))
    assert len(cancelling) == 2
    # Checked with SymPy's limits for those c and for other c (where both zeros are asymptotes).
    for cv in cancelling + [0, 2, -5, sp.Rational(7, 3), 1 + sp.Rational(1, 1000)]:
        f_expr = (x - cv) / den
        count = sum(1 for av in zeros if sp.limit(f_expr, x, av, "+") in (sp.oo, -sp.oo)
                    or sp.limit(f_expr, x, av, "-") in (sp.oo, -sp.oo))
        assert count == (1 if cv in cancelling else 2)
    got = answer("exr-calc-infinite-limits-parameter")
    assert equal(got, tuple(cancelling))
    # The solution's claims: g = 1/((x − 1)(x − 3)) → −∞ at 1⁺, ∞ at 1⁻, ∞ at 3⁺, −∞ at 3⁻; the
    # bounds 1/(x − 3) < −2/5 on (½, 3/2) and 1/(x − 1) > 2/5 on (5/2, 7/2).
    g_expr = 1 / den
    for av, d, lim in ((1, "+", -sp.oo), (1, "-", sp.oo), (3, "+", sp.oo), (3, "-", -sp.oo)):
        assert limit_is(g_expr, x, av, lim, dir=d)
    assert empty_on(1 / (x - 3) >= -sp.Rational(2, 5), x, sp.Interval.open(sp.Rational(1, 2), sp.Rational(3, 2)))
    assert empty_on(1 / (x - 1) <= sp.Rational(2, 5), x, sp.Interval.open(sp.Rational(5, 2), sp.Rational(7, 2)))
    # c = 1: f = 1/(x − 3) → −½ at 1, δ = min(1, 2ε); c = 3: f = 1/(x − 1) → ½ at 3, the same δ.
    assert equal(sp.cancel((x - 1) / den), 1 / (x - 3)) and equal(sp.cancel((x - 3) / den), 1 / (x - 1))
    assert limit_is((x - 1) / den, x, 1, -sp.Rational(1, 2)) and limit_is((x - 3) / den, x, 3, sp.Rational(1, 2))
    assert equal(1 / (x - 3) + sp.Rational(1, 2), (x - 1) / (2 * (x - 3)))
    assert equal(1 / (x - 1) - sp.Rational(1, 2), -(x - 3) / (2 * (x - 1)))

    def f1(v):
        if v in (1, 3):
            undefined()
        return (v - 1) / ((v - 1) * (v - 3))

    def f3(v):
        if v in (1, 3):
            undefined()
        return (v - 3) / ((v - 1) * (v - 3))

    assert two_sided_holds(f1, 1, Q(-1, 2), lambda e: min(Q(1), 2 * e), eps_samples(120, breaks=(Q(1, 2),)))
    assert two_sided_holds(f3, 3, Q(1, 2), lambda e: min(Q(1), 2 * e), eps_samples(121, breaks=(Q(1, 2),)))


# ── Rigorous track and common mistakes ──────────────────────────────────────────


def test_rigorous_track_unbounded_not_infinite():
    def k(v):
        return v.numerator // v.denominator if isinstance(v, Q) else int(v)  # ⌊v⌋ for v > 0

    def f(v):
        assert v > 0
        r_ = 1 / v
        return r_ if k(r_) % 2 == 0 else 0

    rng = random.Random(130)
    deltas = [Q(10**6), Q(1), Q(1, 2), Q(1, 10**9)] + [Q(rng.randint(1, 10**9), N) for _ in range(300)]
    for d in deltas:
        # An integer n ≥ 1 with n > 1/δ (Archimedes); then 2n and 2n + 1 are > 1/δ.
        nv = max(1, k(1 / d) + 1)
        assert nv > 1 / d and 2 * nv > 1 / d and 2 * nv + 1 > 1 / d
        for j in (2 * nv, 2 * nv + 1):
            xv = Q(1, j)
            assert 0 < xv < d and 1 / xv == j and k(Q(j)) == j
        # x = 1/(2n + 1): f = 0 < 1, fails the round M = 1 of ∞.
        assert f(Q(1, 2 * nv + 1)) == 0
        # x = 1/(2n): f = 2n; for n also > M, f > M.
        for mv in (Q(1), Q(1000), Q(10**6)):
            n2 = max(nv, k(mv) + 1)
            assert Q(1, 2 * n2) < d and f(Q(1, 2 * n2)) == 2 * n2 > mv
    # Never negative (so never below −M = −1), on many points of (0, 2).
    for _ in range(2000):
        xv = Q(rng.randint(1, 2 * N), N)
        assert f(xv) >= 0
    # No real right-hand limit L: for ε = 1, every window has a point 1/(2n) with 2n > L + 1.
    for lv in [Q(0), Q(-5), Q(10**6)] + [Q(rng.randint(-10**6, 10**6), 7) for _ in range(100)]:
        for d in deltas[:20]:
            nv = max(1, k(1 / d) + 1, k(max(lv + 1, Q(0))) + 1)
            assert Q(1, 2 * nv) < d and abs(f(Q(1, 2 * nv)) - lv) >= 1
    # A mathcheck assertion for the record: 1/x has no bound above on (0, 1) (its limit at 0+ is ∞).
    assert limit_is(1 / x, x, 0, sp.oo, dir="+")


def test_common_mistakes():
    # "The limit is ∞, so the limit exists": 1/x² → ∞ at 0 (and has no real limit, tested above).
    assert limit_is(1 / x**2, x, 0, sp.oo)
    # Arithmetic with ∞: 1/x − 1/x² = (x − 1)/x², x − 1 < −½ on (0, ½), → −∞ as x → 0+.
    assert equal(1 / x - 1 / x**2, (x - 1) * (1 / x**2))
    assert empty_on(x - 1 >= -sp.Rational(1, 2), x, sp.Interval.open(0, sp.Rational(1, 2)))
    assert limit_is(1 / x - 1 / x**2, x, 0, -sp.oo, dir="+")
    # "3/0 = ∞": (x + 1)/(x − 2) is negative left of 2 (on (−1, 2)) and positive right of it.
    assert equal((x + 1).subs(x, 2), 3)
    assert sign_on((x + 1) / (x - 2), sp.Interval.open(-1, 2)) == -1 and sign_on((x + 1) / (x - 2), sp.Interval.open(2, sp.oo)) == 1
    # "Every zero of the denominator is an asymptote": the numerator is 0 at 1 too, limit −2 there.
    assert equal((x**2 - 1).subs(x, 1), 0) and limit_is((x**2 - 1) / (x**2 - 3 * x + 2), x, 1, -2)
