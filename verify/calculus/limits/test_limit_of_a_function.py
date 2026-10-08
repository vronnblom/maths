"""Verification tests for content/calculus/limits/limit-of-a-function.md (calc-limit).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps; the answers are read
with answer(label), as printed on the page.

The ε–δ checks follow the template: each displayed step is asserted, the chosen δ is checked
symbolically (|f(x) − L| is bounded on the window by a quantity that is at most ε, on each branch
of a min), and the implication 0 < |x − a| < δ ⇒ |f(x) − L| < ε is tested on exact rational
(ε, x) pairs up to the edge of the window. Floats could hide a failure at the edge, so the sampled
arithmetic is exact (fractions.Fraction, or SymPy where a square root is involved).
"""

import math
import random
from fractions import Fraction as Q

import pytest
import sympy as sp

from mathcheck import ManualAnswer, answer, answer_type, covers, equal, equal_on_domain, h, limit_is, n, x

eps = sp.Symbol("epsilon", positive=True)
delta = sp.Symbol("delta", positive=True)
L = sp.Symbol("L", real=True)
N = 10**6


def eps_samples(seed, count=300, breaks=()):
    """Exact rational tolerances: tiny, moderate and huge ones, each break of a min (the ε where
    the branches meet) and its immediate neighbours, and random ones."""
    rng = random.Random(seed)
    fixed = [Q(1, 10**9), Q(1, 10**6), Q(1, 1000), Q(1, 100), Q(1, 10), Q(1, 2), Q(1), Q(3), Q(100), Q(10**6)]
    for b in breaks:
        fixed += [Q(b), Q(b) - Q(1, 10**9), Q(b) + Q(1, 10**9)]
    return fixed + [Q(rng.randint(1, 20 * N), N) for _ in range(count)]


def window(a, d, rng, count=40):
    """Exact rational points x with 0 < |x − a| < d, on both sides: right next to a, right at the
    edge of the window (within 10⁻⁹ of d), and random ones in between."""
    fractions = [Q(1, 10**9), Q(1, N), Q(N - 1, N), Q(10**9 - 1, 10**9)]
    fractions += [Q(rng.randint(1, N - 1), N) for _ in range(count)]
    for fr in fractions:
        t = d * fr
        yield a + t
        yield a - t


def implication_holds(f, a, lim, choose_delta, samples, seed=0, count=40):
    """0 < |x − a| < δ ⇒ |f(x) − L| < ε at every sampled (ε, x) pair, all in exact arithmetic."""
    rng = random.Random(seed)
    for e in samples:
        d = choose_delta(e)
        assert d > 0
        for xv in window(a, d, rng, count):
            assert abs(f(xv) - lim) < e, f"ε = {e}, δ = {d}, x = {xv}: |f(x) − L| = {abs(f(xv) - lim)}"
    return True


def empty_on(condition, var, domain):
    """The set of `var` in `domain` where `condition` holds (an inequality, or an And of them),
    compared with the empty set."""
    parts = condition.args if isinstance(condition, sp.And) else (condition,)
    solved = sp.Intersection(*(sp.solveset(c, var, domain) for c in parts))
    return equal(solved, sp.S.EmptySet)


def round_down_sig(v, digits=6):
    """The exact positive number v rounded down to `digits` significant digits (the widget's
    promise for the δ it reports), as an exact rational."""
    e = sp.floor(sp.log(sp.N(v, 50), 10)) - digits + 1
    return sp.floor(v / sp.Integer(10) ** e) * sp.Integer(10) ** e


# ── Examples ──────────────────────────────────────────────────────────────────


@covers("eg-calc-limit-linear-eps-delta")
def test_eg_calc_limit_linear_eps_delta():
    f = 2 * x - 1
    # Step 1: |(2x − 1) − 5| = |2x − 6| = 2|x − 3|
    assert equal(sp.Abs(f - 5), sp.Abs(2 * x - 6))
    assert equal(sp.Abs(2 * x - 6), 2 * sp.Abs(x - 3))
    # Step 2/3: with δ = ε/2, sup over the window of |f − 5| = 2δ, which must be ≤ ε (it is = ε).
    d = eps / 2
    assert equal(2 * d, eps)
    # The implication itself, exactly, up to the edge of the window.
    assert implication_holds(lambda v: 2 * v - 1, 3, 5, lambda e: e / 2, eps_samples(1))
    # δ = ε/2 is the largest: any larger window contains x = 3 + ε/2, where |f − 5| = ε exactly.
    assert equal(sp.Abs(f.subs(x, 3 + eps / 2) - 5), eps)
    # Check: ε = 0.1 gives δ = 0.05; x = 3.04 gives 0.08 < 0.1; x = 3.05 gives exactly 0.1.
    e = sp.Rational(1, 10)
    assert equal(d.subs(eps, e), sp.Rational(5, 100))
    assert equal(sp.Abs(2 * sp.Rational(304, 100) - 1 - 5), sp.Rational(8, 100))
    assert sp.Rational(8, 100) < e
    assert equal(sp.Abs(2 * sp.Rational(305, 100) - 1 - 5), e)
    # Independent cross-check of the limit.
    assert limit_is(f, x, 3, 5)


@covers("eg-calc-limit-average-speed")
def test_eg_calc_limit_average_speed():
    v = (5 * (1 + h) ** 2 - 5) / h
    # Step 1: the two displayed rewritings, and v(h) = 10 + 5h for h ≠ 0.
    assert equal(v, (5 * (1 + 2 * h + h**2) - 5) / h)
    assert equal((5 * (1 + 2 * h + h**2) - 5) / h, (10 * h + 5 * h**2) / h)
    assert equal((10 * h + 5 * h**2) / h, 10 + 5 * h)
    # v is undefined only at h = 0 (so the definition applies on every punctured window).
    assert equal(sp.calculus.util.continuous_domain(v, h, sp.S.Reals), sp.S.Reals - sp.FiniteSet(0))
    # Step 2: |v(h) − 10| = 5|h|
    assert equal(sp.Abs(sp.cancel(v) - 10), 5 * sp.Abs(h))
    # Step 3: δ = ε/5; sup of 5|h| on the window is 5δ = ε.
    assert equal(5 * (eps / 5), eps)
    assert implication_holds(lambda t: (5 * (1 + t) ** 2 - 5) / t, 0, 10, lambda e: e / 5, eps_samples(2))
    assert limit_is(v, h, 0, 10)
    # Step 4: |v(h) − 10| < 0.01 exactly when 0 < |h| < 0.002 (solved from the raw formula).
    tol = sp.Rational(1, 100)
    good = sp.solveset(sp.Abs(v - 10) < tol, h, sp.S.Reals)
    assert equal(good, sp.Union(sp.Interval.open(-sp.Rational(2, 1000), 0), sp.Interval.open(0, sp.Rational(2, 1000))))
    # ... and at |h| = 0.002 the difference is exactly 0.01, on both sides.
    for hv in (sp.Rational(2, 1000), -sp.Rational(2, 1000)):
        assert equal(sp.Abs(v.subs(h, hv) - 10), tol)
    # Check: 1.002001 = (1.001)², v(0.001) = 10.005; v(0.01) = 10.05 = 10 + 5(0.01).
    assert equal(sp.Rational(1001, 1000) ** 2, sp.Rational(1002001, 10**6))
    assert equal(v.subs(h, sp.Rational(1, 1000)), (5 * sp.Rational(1002001, 10**6) - 5) / sp.Rational(1, 1000))
    assert equal(v.subs(h, sp.Rational(1, 1000)), sp.Rational(10005, 1000))
    assert sp.Abs(v.subs(h, sp.Rational(1, 1000)) - 10) < tol
    assert equal(v.subs(h, sp.Rational(1, 100)), sp.Rational(1005, 100))
    assert equal(v.subs(h, sp.Rational(1, 100)), 10 + 5 * sp.Rational(1, 100))


@covers("eg-calc-limit-jump")
def test_eg_calc_limit_jump():
    f = sp.Abs(x) / x
    pos, neg = sp.Symbol("p", positive=True), sp.Symbol("q", negative=True)
    # f = 1 for x > 0 and −1 for x < 0.
    assert equal(f.subs(x, pos), 1)
    assert equal(f.subs(x, neg), -1)
    # The witnesses ±δ/2 are in every window 0 < |x| < δ, with the values 1 and −1.
    assert equal(sp.Abs(delta / 2), delta / 2) and (delta / 2 < delta) is sp.true
    assert equal(f.subs(x, delta / 2), 1)
    assert equal(f.subs(x, -delta / 2), -1)
    # No L is within ε = 1 of both values: {L : |1 − L| < 1 and |−1 − L| < 1} is empty.
    assert empty_on(sp.And(sp.Abs(1 - L) < 1, sp.Abs(-1 - L) < 1), L, sp.S.Reals)
    # The symmetry step (property 2): |L − (−1)| = |−1 − L|.
    assert equal(sp.Abs(L - (-1)), sp.Abs(-1 - L))
    # The triangle-inequality step: |1 − L| + |L + 1| ≥ 2 = |1 − (−1)| for every L.
    assert equal(sp.Abs(1 - (-1)), 2)
    rng = random.Random(19)
    for lv in [Q(0), Q(1), Q(-1)] + [Q(rng.randint(-10**7, 10**7), 10**5) for _ in range(500)]:
        assert abs(1 - lv) + abs(lv + 1) >= 2
    # Independent cross-check: the one-sided limits differ, so the two-sided one does not exist.
    assert limit_is(f, x, 0, 1, dir="+")
    assert limit_is(f, x, 0, -1, dir="-")
    with pytest.raises(ValueError):
        sp.limit(f, x, 0, "+-")
    # Check: f(0.001) = 1, f(−0.001) = −1; f(0) is undefined.
    assert equal(f.subs(x, sp.Rational(1, 1000)), 1)
    assert equal(f.subs(x, -sp.Rational(1, 1000)), -1)
    assert f.subs(x, 0) is sp.nan


@covers("eg-calc-limit-sin-1-over-x")
def test_eg_calc_limit_sin_1_over_x():
    f = sp.sin(1 / x)
    m = sp.Symbol("m", integer=True, positive=True)
    p = 1 / (2 * sp.pi * m)
    q = 1 / (2 * sp.pi * m + sp.pi / 2)
    # f(p_n) = sin(2πn) = 0 and f(q_n) = sin(2πn + π/2) = 1, for every integer n ≥ 1.
    assert equal(f.subs(x, p), sp.sin(2 * sp.pi * m))
    assert equal(sp.sin(2 * sp.pi * m), 0)
    assert equal(f.subs(x, q), sp.sin(2 * sp.pi * m + sp.pi / 2))
    assert equal(sp.sin(2 * sp.pi * m + sp.pi / 2), 1)
    # 0 < q_n < p_n.
    gap = (sp.pi / 2) / ((2 * sp.pi * m) * (2 * sp.pi * m + sp.pi / 2))
    assert equal(p - q, gap)
    assert q.is_positive and gap.is_positive
    # Both sequences tend to 0.
    assert limit_is(1 / (2 * sp.pi * n), n, sp.oo, 0)
    assert limit_is(1 / (2 * sp.pi * n + sp.pi / 2), n, sp.oo, 0)
    # The step "n > 1/(2πδ) ⇒ p_n < δ": for many exact δ, the least such n puts both points in
    # the window, with values 0 and 1.
    rng = random.Random(3)
    deltas = [sp.Rational(1, 10**k) for k in range(0, 9)] + [sp.Rational(rng.randint(1, N), N) for _ in range(200)]
    for d in deltas:
        k = sp.floor(1 / (2 * sp.pi * d)) + 1
        assert k >= 1 and (k > 1 / (2 * sp.pi * d)) is sp.true
        pk, qk = p.subs(m, k), q.subs(m, k)
        assert (0 < qk) is sp.true and (qk < pk) is sp.true and (pk < d) is sp.true
        assert equal(f.subs(x, pk), 0)
        assert equal(f.subs(x, qk), 1)
    # The symmetry step (property 2): |L − 0| = |0 − L|.
    assert equal(sp.Abs(L - 0), sp.Abs(0 - L))
    # No L is within ½ of both 0 and 1, and |1 − 0| = 1 = ½ + ½.
    assert empty_on(sp.And(sp.Abs(0 - L) < sp.Rational(1, 2), sp.Abs(1 - L) < sp.Rational(1, 2)), L, sp.S.Reals)
    for lv in [Q(0), Q(1), Q(1, 2)] + [Q(rng.randint(-10**7, 10**7), 10**5) for _ in range(500)]:
        assert abs(1 - lv) + abs(lv - 0) >= 1
    # Check: n = 50. p ≈ 0.003183, q ≈ 0.003167, less than 0.0001 apart, values 1 apart.
    p50, q50 = p.subs(m, 50), q.subs(m, 50)
    assert equal(p50, 1 / (100 * sp.pi)) and equal(q50, 1 / (100 * sp.pi + sp.pi / 2))
    assert abs(sp.N(p50, 30) - sp.Rational(3183, 10**6)) < sp.Rational(5, 10**7)
    assert abs(sp.N(q50, 30) - sp.Rational(3167, 10**6)) < sp.Rational(5, 10**7)
    assert (p50 - q50 < sp.Rational(1, 10**4)) is sp.true
    assert equal(f.subs(x, q50) - f.subs(x, p50), 1)
    # Independent cross-check: SymPy finds no limit, only the bounds [−1, 1] (evidence of
    # oscillation, not itself a pass).
    assert sp.limit(f, x, 0, "+") == sp.AccumBounds(-1, 1)


@covers("eg-calc-limit-unbounded")
def test_eg_calc_limit_unbounded():
    f = 1 / x**2
    # f(0.01) = 10 000, f(0.001) = 1 000 000.
    assert equal(f.subs(x, sp.Rational(1, 100)), 10**4)
    assert equal(f.subs(x, sp.Rational(1, 1000)), 10**6)
    # For 0 < x < 1: x² < x, so 1/x² > 1/x (1/x² − 1/x = (1 − x)/x² > 0).
    u = sp.Symbol("u", positive=True)
    assert equal(1 / u**2 - 1 / u, (1 - u) / u**2)
    assert empty_on(u**2 >= u, u, sp.Interval.open(0, 1))
    # 1/(|L| + 2) ≤ ½ for every real L.
    assert equal(sp.maximum(1 / (sp.Abs(L) + 2), L, sp.S.Reals), sp.Rational(1, 2))
    # The proof's witness x = min(δ/2, 1/(|L| + 2)) on many exact (L, δ): in the window, and
    # f(x) − L > 2, so |f(x) − L| > 1 = ε.
    rng = random.Random(4)
    Ls = [Q(0), Q(1), Q(-1), Q(100), Q(-100), Q(10**6), Q(-10**6)] + [Q(rng.randint(-10**8, 10**8), 1000) for _ in range(300)]
    ds = [Q(10**6), Q(1), Q(1, 10**9)] + [Q(rng.randint(1, 10**9), 10**6) for _ in range(30)]
    for lv in Ls:
        for d in ds:
            xv = min(d / 2, 1 / (abs(lv) + 2))
            assert 0 < xv < d
            assert xv <= Q(1, 2)
            assert xv * xv < xv
            fx = 1 / (xv * xv)
            assert fx > 1 / xv >= abs(lv) + 2
            assert fx - lv >= fx - abs(lv) > 2
            assert abs(fx - lv) > 1
    # Check: L = 100: x ≤ 1/102 gives f(x) ≥ 102² = 10 404.
    assert equal(1 / (sp.Abs(100) + 2), sp.Rational(1, 102))
    assert equal(f.subs(x, sp.Rational(1, 102)), 10404)
    assert empty_on(f < 10404, x, sp.Interval.Lopen(0, sp.Rational(1, 102)))
    # Independent cross-check: the limit is +∞, so no real number is the limit.
    assert limit_is(f, x, 0, sp.oo)


@covers("eg-calc-limit-quadratic-eps-delta")
def test_eg_calc_limit_quadratic_eps_delta():
    # Step 1: |x² − 4| = |x − 2| |x + 2|
    assert equal(sp.Abs(x**2 - 4), sp.Abs(x - 2) * sp.Abs(x + 2))
    # Step 2: |x − 2| < 1 ⟺ 1 < x < 3, and then 3 < x + 2 < 5, so |x + 2| < 5.
    assert equal(sp.solveset(sp.Abs(x - 2) < 1, x, sp.S.Reals), sp.Interval.open(1, 3))
    assert equal(sp.imageset(sp.Lambda(x, x + 2), sp.Interval.open(1, 3)), sp.Interval.open(3, 5))
    assert empty_on(sp.Abs(x + 2) >= 5, x, sp.Interval.open(1, 3))
    # So |x² − 4| ≤ 5|x − 2| on the capped window (strict for x ≠ 2).
    assert empty_on(sp.Abs(x**2 - 4) >= 5 * sp.Abs(x - 2), x, sp.Interval.open(1, 3) - sp.FiniteSet(2))
    # Symbolic check of δ = min(1, ε/5), branch by branch. On a window of half-width d ≤ 1,
    # x² − 4 is increasing (2x > 0 on [1, 3]), so |x² − 4| < max((2 + d)² − 4, 4 − (2 − d)²)
    # = 4d + d²; the implication holds iff 4d + d² ≤ ε.
    assert equal(sp.minimum(2 * x, x, sp.Interval(1, 3)), 2)
    assert equal((2 + delta) ** 2 - 4, 4 * delta + delta**2)
    assert equal(4 - (2 - delta) ** 2, 4 * delta - delta**2)   # smaller, since δ² > 0
    sup = lambda d: 4 * d + d**2  # noqa: E731
    assert empty_on(sup(eps / 5) > eps, eps, sp.Interval.Lopen(0, 5))   # branch ε ≤ 5: δ = ε/5
    assert empty_on(sup(1) > eps, eps, sp.Interval(5, sp.oo))          # branch ε ≥ 5: δ = 1
    assert equal(sp.Min(1, eps / 5).subs(eps, 5), 1) and equal((eps / 5).subs(eps, 5), 1)
    # The implication on exact pairs, both branches and the break ε = 5.
    assert implication_holds(lambda v: v * v, 2, 4, lambda e: min(Q(1), e / 5), eps_samples(5, breaks=[5]))
    # Why the 1: δ = ε/5 alone fails for ε = 100 at x = 21.
    assert equal((eps / 5).subs(eps, 100), 20)
    assert (0 < sp.Abs(21 - 2)) is sp.true and (sp.Abs(21 - 2) < 20) is sp.true
    assert equal(sp.Abs(21**2 - 4), 437) and sp.Integer(437) > 100
    # A cap of ½ gives |x + 2| < 4.5, and δ = min(½, ε/4.5) works too.
    assert empty_on(sp.Abs(x + 2) >= sp.Rational(9, 2), x, sp.Interval.open(sp.Rational(3, 2), sp.Rational(5, 2)))
    assert empty_on(sup(eps * 2 / 9) > eps, eps, sp.Interval.Lopen(0, sp.Rational(9, 4)))
    assert empty_on(sup(sp.Rational(1, 2)) > eps, eps, sp.Interval(sp.Rational(9, 4), sp.oo))
    assert implication_holds(lambda v: v * v, 2, 4, lambda e: min(Q(1, 2), e * 2 / 9), eps_samples(6, breaks=[Q(9, 4)]))
    # Check: ε = 0.5 gives δ = 0.1, below the exact largest δ for both sides, √4.5 − 2 (≈ 0.12132).
    e = sp.Rational(1, 2)
    assert equal(sp.Min(1, e / 5), sp.Rational(1, 10))
    right = sp.sqrt(4 + e) - 2
    assert equal(round_down_sig(right), sp.Rational(121320, 10**6))
    assert (sp.Rational(1, 10) < right) is sp.true
    assert equal(sp.Abs(sp.Rational(209, 100) ** 2 - 4), sp.Rational(3681, 10**4))
    assert sp.Rational(3681, 10**4) < e
    # And for ε = 0.1 the page says δ = min(1, ε/5) = 0.02.
    assert equal(sp.Min(1, sp.Rational(1, 10) / 5), sp.Rational(2, 100))
    assert limit_is(x**2, x, 2, 4)


# ── Exercises ─────────────────────────────────────────────────────────────────


@covers("exr-calc-limit-table-estimate")
def test_exr_calc_limit_table_estimate():
    g = (sp.sqrt(1 + x) - 1) / x
    # The limit, from SymPy on both sides, and every point of the table is in the domain x ≥ −1.
    exact = sp.limit(g, x, 0)
    assert limit_is(g, x, 0, exact)
    assert limit_is(g, x, 0, exact, dir="+") and limit_is(g, x, 0, exact, dir="-")
    # Looking ahead: for x ≠ 0, x ≥ −1, multiplying by √(1 + x) + 1 gives 1/(√(1 + x) + 1), which
    # is defined at 0, where it equals the limit.
    rationalised = 1 / (sp.sqrt(1 + x) + 1)
    assert equal_on_domain(g, rationalised, x, sp.Interval.Ropen(-1, 0))
    assert equal_on_domain(g, rationalised, x, sp.Interval.open(0, sp.oo))
    assert equal(g.subs(x, -1), rationalised.subs(x, -1))            # the endpoint x = −1 too
    assert equal(rationalised.subs(x, 0), exact)
    assert equal(exact, sp.Rational(1, 2))
    # The table the exercise asks for: from the right the values increase towards the limit, from
    # the left they decrease towards it, and at ±0.001 both round to the limit's two decimals.
    pts = [sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)]
    right = [g.subs(x, p) for p in pts]
    left = [g.subs(x, -p) for p in pts]
    chain = [right[0], right[1], right[2], exact, left[2], left[1], left[0]]
    assert all((lo < hi) is sp.true for lo, hi in zip(chain, chain[1:]))

    def rounded(v, places):
        """v rounded to the nearest multiple of 10^−places, exactly (no float ties)."""
        scale = sp.Integer(10) ** places
        return sp.floor(v * scale + sp.Rational(1, 2)) / scale

    two_dp = rounded(exact, 2)
    assert equal(rounded(right[2], 2), two_dp) and equal(rounded(left[2], 2), two_dp)
    # The solution's printed six-decimal table, against the values computed here.
    printed = {sp.Rational(1, 10): "0.488088", sp.Rational(1, 100): "0.498756", sp.Rational(1, 1000): "0.499875",
               -sp.Rational(1, 1000): "0.500125", -sp.Rational(1, 100): "0.501256", -sp.Rational(1, 10): "0.513167"}
    for p, shown in printed.items():
        assert equal(rounded(g.subs(x, p), 6), sp.Rational(shown)), (p, shown)
    # The answer: within its tolerance (5·10⁻³) of the exact limit, and the correctly rounded value.
    value = answer("exr-calc-limit-table-estimate")
    assert answer_type("exr-calc-limit-table-estimate") == "numeric-5e-3"
    assert (sp.Abs(value - exact) <= sp.Rational(5, 1000)) is sp.true
    assert equal(value, two_dp)


@covers("exr-calc-limit-value-at-a")
def test_exr_calc_limit_value_at_a():
    g = sp.Piecewise((0, sp.Eq(x, 2)), (2 * x + 1, True))
    value = g.subs(x, 2)
    # The limit uses only x ≠ 2, where g = 2x + 1. (sp.limit cannot be given g itself: SymPy
    # 1.14 evaluates the Piecewise at x = 2 and returns 0, a SymPy bug, not the page's.)
    assert equal(g.subs(x, sp.Rational(201, 100)), 2 * sp.Rational(201, 100) + 1)
    lim = sp.limit(2 * x + 1, x, 2)
    assert limit_is(2 * x + 1, x, 2, lim)
    # The solution: |g(x) − L| = 2|x − 2| for x ≠ 2, so δ = ε/2 works.
    assert equal(sp.Abs(2 * x + 1 - lim), 2 * sp.Abs(x - 2))
    assert implication_holds(lambda v: 2 * v + 1 if v != 2 else 0, 2, int(lim), lambda e: e / 2, eps_samples(7, count=50))
    a_part, b_part = answer("exr-calc-limit-value-at-a")
    assert equal(a_part, value)
    assert equal(b_part, lim)
    assert not equal(value, lim)  # the point of the exercise: g(2) is not the limit


@covers("exr-calc-limit-largest-delta-linear")
def test_exr_calc_limit_largest_delta_linear():
    f, a, lim, e = 5 * x + 2, 1, 7, sp.Rational(1, 100)
    good = sp.solveset(sp.Abs(f - lim) < e, x, sp.S.Reals)
    assert isinstance(good, sp.Interval) and good.contains(a) is sp.true
    largest = sp.Min(good.sup - a, a - good.inf)   # the widest window around a inside `good`
    assert equal(sp.Abs(f - lim), 5 * sp.Abs(x - 1))
    got = answer("exr-calc-limit-largest-delta-linear")
    assert equal(got, largest)
    # It works (exactly, up to the edge) ...
    assert implication_holds(lambda v: 5 * v + 2, 1, 7, lambda _: Q(str(got)), [Q(1, 100)], count=2000)
    # ... and no larger δ does: x = 1 + δ is in every larger window, and there |f − 7| = 0.01.
    assert equal(sp.Abs(f.subs(x, a + got) - lim), e)


@covers("exr-calc-limit-large-values")
def test_exr_calc_limit_large_values():
    f, bound = 1 / x**2, 10**4
    good = sp.solveset(f > bound, x, sp.S.Reals)
    # The good set is a punctured interval around 0; the largest δ is its half-width.
    largest = good.sup
    assert equal(good, sp.Interval.open(-largest, largest) - sp.FiniteSet(0))
    got = answer("exr-calc-limit-large-values")
    assert equal(got, largest)
    # The solution's steps: for x ≠ 0, 1/x² > 10 000 ⟺ x² < 1/10 000 (multiplying by x²/10 000 > 0);
    # x² = |x|²; 1/10 000 = (1/100)²; and for non-negative numbers, |x|² < (1/100)² ⟺ |x| < 1/100.
    nonzero = sp.S.Reals - sp.FiniteSet(0)
    assert equal(good, sp.solveset(x**2 < sp.Rational(1, bound), x, nonzero))
    assert equal(x**2, sp.Abs(x) ** 2)
    assert equal(sp.Rational(1, bound), sp.Rational(1, 100) ** 2)
    assert equal(sp.solveset(sp.Abs(x) ** 2 < sp.Rational(1, 100) ** 2, x, nonzero),
                 sp.solveset(sp.Abs(x) < sp.Rational(1, 100), x, nonzero))
    rng = random.Random(8)
    d = Q(str(got))
    for xv in window(0, d, rng, count=2000):
        assert 1 / (xv * xv) > bound
    # A larger δ lets in x = δ_answer, where f = 10 000, not greater.
    assert equal(f.subs(x, got), bound)


@covers("exr-calc-limit-widget-largest-delta")
def test_exr_calc_limit_widget_largest_delta():
    e, a = sp.Rational(1, 10), 2
    good = sp.solveset(sp.Abs(x**2 - 4) < e, x, sp.S.Reals)
    # The component of the good set around a = 2 (the other one is around −2).
    component = good.intersect(sp.Interval.open(0, sp.oo))
    assert isinstance(component, sp.Interval) and component.contains(a) is sp.true
    right = component.sup - a
    left = a - component.inf
    both = sp.Min(left, right)
    assert equal(right, sp.sqrt(sp.Rational(41, 10)) - 2)
    assert equal(left, 2 - sp.sqrt(sp.Rational(39, 10)))
    assert (right < left) is sp.true
    got = answer("exr-calc-limit-widget-largest-delta")
    assert equal(got, (right, left, both))
    r41, r39 = sp.sqrt(sp.Rational(41, 10)), sp.sqrt(sp.Rational(39, 10))
    # The solution's set-up: |x² − 4| < 0.1 ⟺ 3.9 < x² < 4.1, and for x > 0 that is √3.9 < x < √4.1.
    band = sp.Intersection(sp.solveset(x**2 > 4 - e, x, sp.S.Reals), sp.solveset(x**2 < 4 + e, x, sp.S.Reals))
    assert equal(good, band)
    assert equal(component, sp.Interval.open(r39, r41))
    assert equal(r39**2, sp.Rational(39, 10)) and equal(r41**2, sp.Rational(41, 10))
    # (a), (b): √3.9 < 2 because 3.9 < 4 = 2², and 2 < √4.1 because 2² = 4 < 4.1.
    assert sp.Rational(39, 10) < 4 < sp.Rational(41, 10)
    assert (r39 < 2) is sp.true and (2 < r41) is sp.true
    # (c), comparing squares (F4): (√4.1·√3.9)² = 4.1·3.9 = 15.99 < 16 = 4², so √4.1·√3.9 < 4; then
    # (√4.1 + √3.9)² = 4.1 + 2√4.1·√3.9 + 3.9 < 8 + 2·4 = 16 = 4², so √4.1 + √3.9 < 4.
    prod = r41 * r39
    assert equal(prod**2, sp.Rational(41, 10) * sp.Rational(39, 10))
    assert equal(sp.Rational(41, 10) * sp.Rational(39, 10), sp.Rational(1599, 100))
    assert sp.Rational(1599, 100) < 16 and (prod < 4) is sp.true
    s = r41 + r39
    assert equal(s**2, sp.Rational(41, 10) + 2 * prod + sp.Rational(39, 10))
    assert equal(sp.Rational(41, 10) + sp.Rational(39, 10), 8)
    assert (s**2 < 16) is sp.true and (s < 4) is sp.true
    # ... which is the comparison √4.1 − 2 < 2 − √3.9 that picks (c).
    assert equal((2 - r39) - (r41 - 2), 4 - s)
    # F10: √4.1 = √410/10 and √3.9 = √390/10 (non-negative, with squares 4.1 and 3.9).
    for root, radicand, value in ((sp.sqrt(410) / 10, 410, sp.Rational(41, 10)), (sp.sqrt(390) / 10, 390, sp.Rational(39, 10))):
        assert root.is_nonnegative
        assert equal(root**2, sp.Rational(radicand, 100)) and equal(root**2, value)
        assert equal(root, sp.sqrt(value))
    # The numbers the widget reports (Try this, step 1, and the solution) are the exact values
    # rounded down to six significant digits.
    assert equal(round_down_sig(right), sp.Rational(248456, 10**7))
    assert equal(round_down_sig(left), sp.Rational(251582, 10**7))
    # The solution's "≈ 0.0248457" and "≈ 0.0251582" (nearest rounding).
    assert abs(sp.N(right, 30) - sp.Rational(248457, 10**7)) < sp.Rational(5, 10**8)
    assert abs(sp.N(left, 30) - sp.Rational(251582, 10**7)) < sp.Rational(5, 10**8)
    # F6: "may be smaller than the exact value by about 10⁻⁵ of that value": here the reported
    # numbers are below the exact ones by less than 10⁻⁵ (relative).
    for exact_v, reported in ((right, sp.Rational(248456, 10**7)), (left, sp.Rational(251582, 10**7))):
        assert (reported <= exact_v) is sp.true
        assert ((exact_v - reported) / exact_v < sp.Rational(1, 10**5)) is sp.true
    # Each δ works on its side, exactly up to the edge.
    rng = random.Random(9)
    for side, d in ((1, right), (-1, left)):
        for k in [1, N - 1, 10**9 - 1] + [rng.randint(1, N - 1) for _ in range(200)]:
            t = d * sp.Rational(k, 10**9 if k == 10**9 - 1 else N)
            assert (sp.Abs((a + side * t) ** 2 - 4) < e) is sp.true


@covers("exr-calc-limit-average-speed")
def test_exr_calc_limit_average_speed():
    s = lambda t: 5 * t**2  # noqa: E731
    v = (s(2 + h) - s(2)) / h
    lim = sp.limit(v, h, 0)
    assert limit_is(v, h, 0, lim)
    # The solution's steps: v(h) = (5(4 + 4h + h²) − 20)/h = (20h + 5h²)/h = 20 + 5h.
    assert equal(v, (5 * (4 + 4 * h + h**2) - 20) / h)
    assert equal((5 * (4 + 4 * h + h**2) - 20) / h, (20 * h + 5 * h**2) / h)
    assert equal((20 * h + 5 * h**2) / h, 20 + 5 * h)
    # (a) the proof's δ = ε/5, exactly up to the edge.
    assert implication_holds(lambda t: (5 * (2 + t) ** 2 - 20) / t, 0, int(lim), lambda e: e / 5, eps_samples(10, count=100))
    # (b) the good set for the tolerance 0.1, solved from the raw quotient: a punctured interval.
    tol = sp.Rational(1, 10)
    good = sp.solveset(sp.Abs(v - lim) < tol, h, sp.S.Reals)
    largest = good.sup
    assert equal(good, sp.Interval.open(-largest, largest) - sp.FiniteSet(0))
    assert equal(sp.Abs(v.subs(h, largest) - lim), tol)   # no larger δ: equality at h = δ
    a_part, b_part = answer("exr-calc-limit-average-speed")
    assert equal(a_part, lim)
    assert equal(b_part, largest)


@covers("exr-calc-limit-eps-delta-linear")
def test_exr_calc_limit_eps_delta_linear():
    # A manual answer (a proof): its key claims are checked here; it counts as covered only
    # through a reviewer's note in maths.manual_checked.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limit-eps-delta-linear")
    f = 4 - 3 * x
    assert equal(f.subs(x, -1), 7) and limit_is(f, x, -1, 7)
    # Scratch work: |(4 − 3x) − 7| = |−3x − 3| = 3|x + 1| = 3|x − (−1)|
    assert equal(sp.Abs(f - 7), sp.Abs(-3 * x - 3))
    assert equal(sp.Abs(-3 * x - 3), 3 * sp.Abs(x + 1))
    # δ = ε/3: the sup of 3|x + 1| on the window is 3δ = ε.
    assert equal(3 * (eps / 3), eps)
    assert implication_holds(lambda v: 4 - 3 * v, -1, 7, lambda e: e / 3, eps_samples(11))


@covers("exr-calc-limit-jump-which-eps")
def test_exr_calc_limit_jump_which_eps():
    H = sp.Heaviside(x, 1)   # 0 for x < 0, 1 for x ≥ 0 (a Piecewise trips a SymPy 1.14 limit bug)
    assert equal(H.subs(x, 0), 1)
    half = sp.Rational(1, 2)
    neg, pos = sp.Symbol("q", negative=True), sp.Symbol("p", positive=True)
    # On every punctured window both sides occur, with these distances from ½.
    dist_left, dist_right = sp.Abs(H.subs(x, neg) - half), sp.Abs(H.subs(x, pos) - half)
    assert equal(dist_left, half) and equal(dist_right, half)
    # Since |H − ½| is constant on each side, a δ exists for ε iff each distance is < ε.
    expected = sp.Intersection(sp.solveset(dist_left < eps, eps, sp.Interval.open(0, sp.oo)),
                               sp.solveset(dist_right < eps, eps, sp.Interval.open(0, sp.oo)))
    got = answer("exr-calc-limit-jump-which-eps")
    assert equal(got, expected)
    # Evidence for the claim's failure: ε = ½ is a positive tolerance outside the set, and the
    # one-sided limits are 0 and 1.
    assert expected.contains(half) is sp.false
    assert limit_is(H, x, 0, 0, dir="-")
    assert limit_is(H, x, 0, 1, dir="+")
    # Spot-check the set: for ε in it every window works, for ε ≤ ½ the point δ/2 fails.
    rng = random.Random(12)
    for e in eps_samples(12, count=100, breaks=[half]):
        d = Q(rng.randint(1, N), N)
        works = all(abs((0 if xv < 0 else 1) - Q(1, 2)) < e for xv in window(0, d, rng, count=10))
        assert works == (sp.Rational(e.numerator, e.denominator) in expected)


@covers("exr-calc-limit-sin-pi-over-x")
def test_exr_calc_limit_sin_pi_over_x():
    f = sp.sin(sp.pi / x)
    m = sp.Symbol("m", integer=True, positive=True)
    # The claim "lim sin(π/x) = 0" fails for ε = ½ if every window holds a point with f = 1.
    # Points with π/x = 2πm + π/2:
    xm = sp.solve(sp.Eq(sp.pi / x, 2 * sp.pi * m + sp.pi / 2), x)[0]
    assert equal(f.subs(x, xm), 1)
    assert limit_is(xm.subs(m, n), n, sp.oo, 0)
    # For many exact δ, a point x_m < δ with |f(x_m) − 0| = 1 ≥ ½: the claim is false.
    rng = random.Random(13)
    claim_holds = True
    for d in [sp.Rational(1, 10**k) for k in range(0, 9)] + [sp.Rational(rng.randint(1, N), N) for _ in range(200)]:
        k = sp.ceiling(1 / (2 * d)) + 1          # the solution's n > 1/(2δ)
        point = xm.subs(m, k)
        assert (0 < point) is sp.true and (point < d) is sp.true
        assert equal(sp.Abs(f.subs(x, point) - 0), 1)
        if sp.Abs(f.subs(x, point)) >= sp.Rational(1, 2):
            claim_holds = False
    got = answer("exr-calc-limit-sin-pi-over-x")
    assert equal(got, sp.true if claim_holds else sp.false)
    # Independent cross-check: SymPy finds only the bounds [−1, 1] (evidence, not a pass).
    assert sp.limit(f, x, 0, "+") == sp.AccumBounds(-1, 1)
    # The solution: x_m = 2/(4m + 1), and the table's last rows are x_6, x_31, x_156; the
    # points 1/m give sin(mπ) = 0.
    assert equal(xm, 2 / (4 * m + 1))
    for k, shown in ((6, "0.08"), (31, "0.016"), (156, "0.0032")):
        assert equal(xm.subs(m, k), sp.Rational(shown))
    assert equal(f.subs(x, 1 / m), 0)


@covers("exr-calc-limit-eps-delta-quadratic")
def test_exr_calc_limit_eps_delta_quadratic():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limit-eps-delta-quadratic")
    assert limit_is(x**2, x, 3, 9)
    # Scratch work: |x² − 9| = |x − 3||x + 3|; |x − 3| < 1 gives 2 < x < 4, 5 < x + 3 < 7.
    assert equal(sp.Abs(x**2 - 9), sp.Abs(x - 3) * sp.Abs(x + 3))
    assert equal(sp.solveset(sp.Abs(x - 3) < 1, x, sp.S.Reals), sp.Interval.open(2, 4))
    assert equal(sp.imageset(sp.Lambda(x, x + 3), sp.Interval.open(2, 4)), sp.Interval.open(5, 7))
    assert empty_on(sp.Abs(x**2 - 9) >= 7 * sp.Abs(x - 3), x, sp.Interval.open(2, 4) - sp.FiniteSet(3))
    # δ = min(1, ε/7), branch by branch: on a window of half-width d ≤ 1, x² is increasing, so
    # |x² − 9| < (3 + d)² − 9 = 6d + d²; the implication holds iff 6d + d² ≤ ε.
    assert equal((3 + delta) ** 2 - 9, 6 * delta + delta**2)
    assert equal(9 - (3 - delta) ** 2, 6 * delta - delta**2)   # smaller, since δ² > 0
    sup = lambda d: 6 * d + d**2  # noqa: E731
    assert empty_on(sup(eps / 7) > eps, eps, sp.Interval.Lopen(0, 7))
    assert empty_on(sup(1) > eps, eps, sp.Interval(7, sp.oo))
    assert implication_holds(lambda v: v * v, 3, 9, lambda e: min(Q(1), e / 7), eps_samples(14, breaks=[7]))


@covers("exr-calc-limit-eps-delta-sqrt")
def test_exr_calc_limit_eps_delta_sqrt():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limit-eps-delta-sqrt")
    u = sp.Symbol("u", nonnegative=True)
    assert limit_is(sp.sqrt(x), x, 4, 2)
    # (√x − 2)(√x + 2) = x − 4, because (√x)² = x, and √x + 2 ≥ 2 > 0, because √x ≥ 0 (x ≥ 0);
    # so |√x − 2| = |x − 4|/(√x + 2) ≤ |x − 4|/2.
    assert equal(sp.sqrt(u) ** 2, u) and sp.sqrt(u).is_nonnegative
    assert equal((sp.sqrt(u) - 2) * (sp.sqrt(u) + 2), u - 4)
    # Property 4, |p/q| = |p|/|q|, with q = √x + 2 = |√x + 2| > 0, applied to √x − 2 = (x − 4)/(√x + 2).
    assert equal(sp.Abs(sp.sqrt(u) + 2), sp.sqrt(u) + 2) and (sp.sqrt(u) + 2).is_positive
    assert equal(sp.Abs((u - 4) / (sp.sqrt(u) + 2)), sp.Abs(u - 4) / sp.Abs(sp.sqrt(u) + 2))
    assert equal(sp.minimum(sp.sqrt(x) + 2, x, sp.Interval(0, sp.oo)), 2)
    assert equal((u - 4) / (sp.sqrt(u) + 2), sp.sqrt(u) - 2)   # so |√x − 2| = |x − 4|/(√x + 2)
    assert empty_on(sp.Abs(sp.sqrt(x) - 2) > sp.Abs(x - 4) / 2, x, sp.Interval(0, sp.oo))
    # |x − 4| < 4 gives 0 < x < 8, inside the domain [0, ∞), which contains (0, 8) around 4.
    assert equal(sp.solveset(sp.Abs(x - 4) < 4, x, sp.S.Reals), sp.Interval.open(0, 8))
    # δ = min(4, 2ε), branch by branch: √x is increasing, so on a window of half-width d ≤ 4
    # |√x − 2| < max(√(4 + d) − 2, 2 − √(4 − d)) = 2 − √(4 − d); it must be ≤ ε.
    d_ = sp.Symbol("d", positive=True)
    assert empty_on(sp.sqrt(4 + d_) - 2 > 2 - sp.sqrt(4 - d_), d_, sp.Interval.Lopen(0, 4))
    assert empty_on(2 - sp.sqrt(4 - 2 * eps) > eps, eps, sp.Interval.Lopen(0, 2))   # branch ε ≤ 2: δ = 2ε
    assert empty_on(2 - sp.sqrt(4 - 4) > eps, eps, sp.Interval(2, sp.oo))           # branch ε ≥ 2: δ = 4
    # The implication on exact pairs (SymPy decides each comparison exactly), both branches.
    rng = random.Random(15)
    for e in eps_samples(15, count=40, breaks=[2]):
        d = min(Q(4), 2 * e)
        er = sp.Rational(e.numerator, e.denominator)
        for xv in window(Q(4), d, rng, count=8):
            xr = sp.Rational(xv.numerator, xv.denominator)
            assert xr > 0                                   # in the domain
            assert (sp.Abs(sp.sqrt(xr) - 2) < er) is sp.true, (e, xv)
    # Without the cap: ε = 3 gives δ = 6, and x = −1 is in the window, where √x is not real.
    assert (0 < sp.Abs(-1 - 4)) is sp.true and (sp.Abs(-1 - 4) < 2 * 3) is sp.true
    assert sp.sqrt(sp.Integer(-1)).is_real is False


# ── Unlabelled claims: the definition's examples, the remark, the theorem, the figures ──────


def test_definition_example_and_non_example():
    # lim_{x→a} x = a with δ = ε.
    assert implication_holds(lambda v: v, Q(7, 3), Q(7, 3), lambda e: e, eps_samples(16, count=50))
    # 1.5 is not lim_{x→1} x: for ε = 0.25 and every δ, x = 1 + d with d = ½ min(δ, 0.25) is in
    # the window and |x − 1.5| = 0.5 − d ≥ 0.375.
    rng = random.Random(17)
    for dv in [Q(10**6), Q(1), Q(1, 4), Q(1, 10**9)] + [Q(rng.randint(1, 10**7), N) for _ in range(300)]:
        d = min(dv, Q(1, 4)) / 2
        assert 0 < d < dv
        assert abs((1 + d) - Q(3, 2)) == Q(1, 2) - d >= Q(3, 8)
        assert not abs((1 + d) - Q(3, 2)) < Q(1, 4)
    # The ∃δ∀ε order fails for f(x) = x at a = 0 with L = 0: for each δ > 0, the point x = 3δ/4 is
    # in the window 0 < |x − 0| < δ, and there |f(x) − 0| = 3δ/4 ≥ δ/2 = ε.
    w = 3 * delta / 4
    assert (0 < sp.Abs(w - 0)) is sp.true and (sp.Abs(w - 0) < delta) is sp.true
    assert equal(sp.Abs(w - 0), 3 * delta / 4)
    assert (sp.Abs(w - 0) >= delta / 2) is sp.true
    # "Why f must be defined near a": for √x at −1 and δ ≤ 1, no x of the domain [0, ∞) has
    # 0 < |x + 1| < δ (checked at δ = 1, the widest such window).
    assert empty_on(sp.Abs(x + 1) < 1, x, sp.Interval(0, sp.oo))


def test_remark_value_irrelevant():
    g = (x**2 - 1) / (x - 1)
    assert g.subs(x, 1) is sp.nan
    assert equal(g, (x - 1) * (x + 1) / (x - 1))
    assert equal(sp.cancel(g), x + 1)
    assert equal(sp.Abs(sp.cancel(g) - 2), sp.Abs(x - 1))
    assert limit_is(g, x, 1, 2)
    hh = sp.Piecewise((5, sp.Eq(x, 1)), (x + 1, True))
    assert equal(hh.subs(x, 1), 5)
    assert equal(hh.subs(x, sp.Rational(99, 100)), sp.Rational(199, 100))
    assert limit_is(x + 1, x, 1, 2)   # h = x + 1 on x ≠ 1 (sp.limit mishandles the Piecewise)


def test_thm_calc_limit_unique_computable_claims():
    # The proof's computable claims: ε = ½|L − M| > 0 when L ≠ M, ε + ε = |L − M|, x = a + δ/2
    # lies in the window, and no number w is within ε of both L and M (so the triangle
    # inequality |L − M| ≤ |L − w| + |w − M| gives |L − M| < |L − M|).
    gap = sp.Symbol("g", positive=True)            # |L − M| with M = L + g (the case M < L is symmetric)
    M = L + gap
    e = sp.Abs(L - M) / 2
    assert e.is_positive
    assert equal(e + e, sp.Abs(L - M))
    assert (0 < sp.Abs(delta / 2)) is sp.true and (delta / 2 < delta) is sp.true
    # Write w = L + g·s: |w − L| = g|s|, |w − M| = g|s − 1|, ε = g/2, so w is within ε of both
    # iff |s| < ½ and |s − 1| < ½, which no s satisfies.
    sv = sp.Symbol("s", real=True)
    assert equal(sp.Abs((L + gap * sv) - L), gap * sp.Abs(sv))
    assert equal(sp.Abs((L + gap * sv) - M), gap * sp.Abs(sv - 1))
    assert equal(e, gap / 2)
    # The symmetry step (property 2), |L − f(x)| = |f(x) − L|, with a symbol for f(x).
    fx = sp.Symbol("f_x", real=True)
    assert equal(sp.Abs(L - fx), sp.Abs(fx - L))
    assert empty_on(sp.And(sp.Abs(sv) < sp.Rational(1, 2), sp.Abs(sv - 1) < sp.Rational(1, 2)), sv, sp.S.Reals)
    # The triangle inequality in the form used, on exact random triples.
    rng = random.Random(18)
    for _ in range(2000):
        uu, vv, ww = (Q(rng.randint(-10**6, 10**6), 997) for _ in range(3))
        assert abs(uu - vv) <= abs(uu - ww) + abs(ww - vv)
    # And numerically for many (L, M) pairs, the open ε-intervals never meet.
    for _ in range(500):
        lv, mv = Q(rng.randint(-10**6, 10**6), 1000), Q(rng.randint(-10**6, 10**6), 1000)
        if lv == mv:
            continue
        ev = abs(lv - mv) / 2
        assert max(lv, mv) - ev >= min(lv, mv) + ev


def test_figure_average_speed():
    # Caption: the table values at h = ±0.1, ±0.01, ±0.001, and the limit 10.
    v = (5 * (1 + h) ** 2 - 5) / h
    shown = {sp.Rational(1, 10): "10.5", sp.Rational(1, 100): "10.05", sp.Rational(1, 1000): "10.005",
             -sp.Rational(1, 1000): "9.995", -sp.Rational(1, 100): "9.95", -sp.Rational(1, 10): "9.5"}
    for hv, value in shown.items():
        assert equal(v.subs(h, hv), sp.Rational(value))
    assert limit_is(v, h, 0, 10)


def test_figure_misleading_table():
    f = sp.sin(sp.pi / x)
    # sin(10π) = sin(100π) = sin(1000π) = 0 at x = 0.1, 0.01, 0.001.
    for xv, k in ((sp.Rational(1, 10), 10), (sp.Rational(1, 100), 100), (sp.Rational(1, 1000), 1000)):
        assert equal(sp.pi / xv, k * sp.pi)
        assert equal(f.subs(x, xv), 0)
    # sin(12.5π) = sin(62.5π) = sin(312.5π) = 1 at x = 0.08, 0.016, 0.0032.
    for xv, k in ((sp.Rational(8, 100), sp.Rational(25, 2)), (sp.Rational(16, 1000), sp.Rational(125, 2)),
                  (sp.Rational(32, 10**4), sp.Rational(625, 2))):
        assert equal(sp.pi / xv, k * sp.pi)
        assert equal(f.subs(x, xv), 1)
    # "The computer shows tiny numbers such as −1.2 × 10⁻¹⁵": IEEE doubles, as in the browser.
    tiny = [math.sin(math.pi / v) for v in (0.1, 0.01, 0.001)]
    assert all(0 < abs(t) < 1e-12 for t in tiny)
    assert f"{tiny[0]:.1e}" == "-1.2e-15"
    # "It stays between −1 and 1. Near x = 0 it rises to height 1 and falls back through 0 again
    # and again": the values lie in [−1, 1], and between consecutive zeros 1/(2m + 1) < 1/(2m) lies
    # x_m = 2/(4m + 1), where the value is 1, for every integer m ≥ 1.
    # (sin takes values in [−1, 1] on all of ℝ, and π/x is real for x ≠ 0.)
    tt = sp.Symbol("t", real=True)
    assert equal(sp.calculus.util.function_range(sp.sin(tt), tt, sp.S.Reals), sp.Interval(-1, 1))
    assert (sp.pi / sp.Symbol("x_nz", real=True, nonzero=True)).is_real
    m = sp.Symbol("m", integer=True, positive=True)
    xm = 2 / (4 * m + 1)
    assert equal(f.subs(x, 1 / (2 * m)), 0) and equal(f.subs(x, 1 / (2 * m + 1)), 0)
    assert equal(f.subs(x, xm), 1)
    assert equal(1 / (2 * m) - xm, 1 / (2 * m * (4 * m + 1))) and equal(xm - 1 / (2 * m + 1), 1 / ((4 * m + 1) * (2 * m + 1)))
    assert (1 / (2 * m * (4 * m + 1))).is_positive and (1 / ((4 * m + 1) * (2 * m + 1))).is_positive


def test_facts_from_school():
    # The box "Facts from school used on this page", each fact symbolically (k an integer, any
    # sign; t real), in radians.
    kk = sp.Symbol("k", integer=True)
    tt = sp.Symbol("t", real=True)
    assert equal(sp.sin(kk * sp.pi), 0)
    assert equal(sp.sin(sp.pi / 2 + 2 * kk * sp.pi), 1)
    assert equal(sp.calculus.util.function_range(sp.sin(tt), tt, sp.S.Reals), sp.Interval(-1, 1))
    # Every use on the page is an instance of the first two facts, with an integer k:
    # the figure's 10π, 100π, 1000π (k = 10, 100, 1000) and 12.5π, 62.5π, 312.5π (k = 6, 31, 156);
    for multiple in (10, 100, 1000):
        assert equal(sp.sin(multiple * sp.pi), sp.sin(kk * sp.pi).subs(kk, multiple))
    for value, k_ in ((sp.Rational(25, 2), 6), (sp.Rational(125, 2), 31), (sp.Rational(625, 2), 156)):
        assert equal(value * sp.pi, sp.pi / 2 + 2 * k_ * sp.pi)
    # p_n, q_n: sin(2πn) (k = 2n) and sin(2πn + π/2) (k = n); the n = 50 Check: sin(100π) and
    # sin(100π + π/2); sin(π/x) solution: sin(nπ) at x = 1/n and π/x_n = 2πn + π/2.
    nn = sp.Symbol("n", integer=True, positive=True)
    assert equal(sp.sin(2 * sp.pi * nn), sp.sin(kk * sp.pi).subs(kk, 2 * nn))
    assert equal(sp.sin(2 * sp.pi * nn + sp.pi / 2), sp.sin(sp.pi / 2 + 2 * kk * sp.pi).subs(kk, nn))
    assert equal(sp.sin(100 * sp.pi + sp.pi / 2), 1)
    assert equal(sp.pi / (2 / (4 * nn + 1)), 2 * sp.pi * nn + sp.pi / 2)
    # In the sin(1/x) intro, 1/x passes through every multiple kπ (k ≥ 1) at x = 1/(kπ) and through
    # every π/2 + 2kπ (k ≥ 0) at x = 1/(π/2 + 2kπ), points that tend to 0.
    assert limit_is(1 / (nn * sp.pi), nn, sp.oo, 0)
    assert limit_is(1 / (sp.pi / 2 + 2 * nn * sp.pi), nn, sp.oo, 0)


def test_figure_epsilon_delta_and_try_this():
    a_, lim = 2, 4

    def largest(e):
        right = sp.sqrt(lim + e) - a_
        left = a_ - sp.sqrt(lim - e)
        return left, right

    # Caption, ε = 0.5: left 2 − √3.5 ≈ 0.129171, right √4.5 − 2 ≈ 0.121320; the widget reports
    # them rounded down to six significant digits, 0.129171 and 0.12132.
    left, right = largest(sp.Rational(1, 2))
    assert equal(left, 2 - sp.sqrt(sp.Rational(7, 2))) and equal(right, sp.sqrt(sp.Rational(9, 2)) - 2)
    assert equal(round_down_sig(left), sp.Rational(129171, 10**6))
    assert equal(round_down_sig(right), sp.Rational(121320, 10**6))
    # Sliders: ε from 0.05 to 1.5 in steps of 0.05, starting at 0.5; eight presses of ← give 0.1.
    assert equal(sp.Rational(1, 2) - 8 * sp.Rational(5, 100), sp.Rational(1, 10))
    # δ slider: the step is a thousandth of the distance from a to the nearer end of xRange [1, 3].
    step = sp.Rational(min(a_ - 1, 3 - a_), 1000)
    assert equal(step, sp.Rational(1, 1000))
    # Try this, step 1: ε = 0.1 → 0.0251582 (left) and 0.0248456 (right).
    e = sp.Rational(1, 10)
    left, right = largest(e)
    assert equal(round_down_sig(left), sp.Rational(251582, 10**7))
    assert equal(round_down_sig(right), sp.Rational(248456, 10**7))
    # Step 3: the largest slider value ≤ the found δ is 0.024; one step up is 0.025, which fails:
    # its (open) window 0 < |x − 2| < 0.025 contains points right of √4.1, e.g. x = 2.0249, where
    # x² = 4.10022001 ≥ 4.1. (x = 2.025 itself is the window's edge, not in it.)
    found = round_down_sig(right)
    on_slider = sp.floor(found / step) * step
    assert equal(on_slider, sp.Rational(24, 1000))
    assert (on_slider < right) is sp.true            # δ = 0.024 really works
    up = on_slider + step
    assert equal(up, sp.Rational(25, 1000))
    assert (up > right) is sp.true                   # δ = 0.025 does not
    probe = sp.Rational(20249, 10**4)
    assert (0 < probe - a_) and (probe - a_ < up)
    assert equal(probe**2, sp.Rational(410022001, 10**8)) and probe**2 >= lim + e
    # "Why the smaller one" (F7): a δ larger than √4.1 − 2 ≈ 0.024846 lets in points right of √4.1,
    # where x² ≥ 4.1 (at x = 2.025, outside the band: x² = 4.100625; x = 2.025 is right of √4.1 and
    # in the window of every δ > 0.025); the left side tolerates up to 2 − √3.9 ≈ 0.025158.
    r41, r39 = sp.sqrt(lim + e), sp.sqrt(lim - e)
    assert equal(right, r41 - 2) and equal(left, 2 - r39)
    assert equal(sp.floor(right * 10**6 + sp.Rational(1, 2)), 24846)
    assert equal(sp.floor(left * 10**6 + sp.Rational(1, 2)), 25158)
    assert equal(sp.Rational(2025, 1000) ** 2, sp.Rational(4100625, 10**6))
    assert sp.Rational(4100625, 10**6) >= lim + e
    assert (sp.Rational(2025, 1000) > r41) is sp.true
    # Any δ above √4.1 − 2 fails: its window contains a point of (√4.1, 2 + δ), outside the band.
    for d_over in (sp.Rational(1, 10**9), sp.Rational(1, 10**6), sp.Rational(1, 1000)):
        xv = a_ + right + d_over / 2                  # in the window of δ = right + d_over
        assert (0 < xv - a_) is sp.true and (xv - a_ < right + d_over) is sp.true
        assert (sp.Abs(xv**2 - lim) >= e) is sp.true
    # Within the left tolerance the left side is fine: every x in (2 − (2 − √3.9), 2) has x² > 3.9.
    assert empty_on(x**2 <= lim - e, x, sp.Interval.open(a_ - left, a_))
    # Step 4 and "as ε shrinks, so does the window": the both-sides δ increases with ε.
    deltas = [sp.Min(*largest(sp.Rational(k, 100))) for k in (5, 10, 50, 100, 150)]
    assert all((p < q) is sp.true for p, q in zip(deltas, deltas[1:]))
    # And for ε = 0.1 the proof's δ = min(1, ε/5) = 0.02 is smaller than the largest.
    assert (sp.Min(1, e / 5) < sp.Min(left, right)) is sp.true
