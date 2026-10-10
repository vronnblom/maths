"""Verification tests for content/calculus/limits/limits-at-infinity.md (calc-limits-at-infinity).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps; the answers are read
with answer(label), as printed on the page.

The ε–N checks follow the ε–δ pattern of test_limit_of_a_function.py: each displayed step is
asserted, the chosen threshold is checked symbolically (on each branch of a max), and the
implication x > N ⇒ |f(x) − L| < ε (or f(x) > B) is tested on exact rational (ε, x) pairs right up
to the threshold. Floats could hide a failure at the edge, so the sampled arithmetic is exact
(fractions.Fraction, or SymPy where a square root is involved).

Limits are checked with limit_is, which takes SymPy's limit and cross-checks it against a table of
values at ±10³ … ±10¹² (60 digits): two routes for every limit.
"""

import random
import re
from decimal import ROUND_HALF_EVEN, Decimal
from fractions import Fraction as Q
from pathlib import Path

import pytest
import sympy as sp

from mathcheck import ManualAnswer, answer, covers, equal, equal_on_domain, limit_is, t, x

eps = sp.Symbol("epsilon", positive=True)
B = sp.Symbol("B", real=True)
p = sp.Symbol("p", positive=True)   # a positive x
q = sp.Symbol("q", negative=True)   # a negative x
s = sp.Symbol("s", positive=True)   # a positive step beyond a threshold
oo = sp.oo
M = 10**6

FIGURE = Path(__file__).resolve().parents[3] / "content/calculus/limits/img/limit-at-infinity-band.svg"


def eps_samples(seed, count=200, breaks=()):
    """Exact rational tolerances: tiny, moderate and huge ones, each break of a max (the ε where
    the branches meet) and its immediate neighbours, and random ones."""
    rng = random.Random(seed)
    fixed = [Q(1, 10**9), Q(1, 10**6), Q(1, 1000), Q(1, 100), Q(1, 10), Q(1, 2), Q(1), Q(3), Q(100), Q(10**6)]
    for b_ in breaks:
        fixed += [Q(b_), Q(b_) - Q(1, 10**9), Q(b_) + Q(1, 10**9)]
    return fixed + [Q(rng.randint(1, 20 * M), M) for _ in range(count)]


def ray(threshold, rng, count=30):
    """Exact rational points x > threshold: right next to it (10⁻⁹ beyond), moderately and very far
    beyond it, and random ones in between."""
    steps = [Q(1, 10**9), Q(1, M), Q(1, 1000), Q(1), Q(10), Q(1000), Q(10**9)]
    steps += [Q(rng.randint(1, 100 * M), M) for _ in range(count)]
    for d in steps:
        yield threshold + d


def eps_n_holds(f, lim, choose_n, samples, seed=0):
    """x > N ⇒ |f(x) − L| < ε at every sampled (ε, x) pair, in exact arithmetic."""
    rng = random.Random(seed)
    for e in samples:
        n_ = choose_n(e)
        for xv in ray(n_, rng):
            assert abs(f(xv) - lim) < e, f"ε = {e}, N = {n_}, x = {xv}: |f(x) − L| = {abs(f(xv) - lim)}"
    return True


def rounded(value, places):
    """The exact value correctly rounded to `places` decimal places, as an exact rational."""
    d = Decimal(str(sp.N(value, 60))).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN)
    return sp.Rational(str(d))


def _sign_is(expr, attr):
    """SymPy's sign assumption on expr after `together` and `factor` (True only if it is proved)."""
    return getattr(sp.factor(sp.together(sp.sympify(expr))), attr) is True


def positive(expr):
    return _sign_is(expr, "is_positive")


def nonnegative(expr):
    return _sign_is(expr, "is_nonnegative")


def negative(expr):
    return _sign_is(expr, "is_negative")


def leading(expr, var=x):
    """(degree, leading coefficient) of a polynomial, read by sp.Poly."""
    poly = sp.Poly(expr, var)
    return poly.degree(), poly.LC()


# ── Why this matters, the definition, the remark ──────────────────────────────


def test_why_this_matters_resistors():
    R = 3 * t / (3 + t)
    # The four rounded values: 2.3077, 2.9126, 2.9910 (4 places) and 2.999991 (6 places).
    for tv, places, shown in ((10, 4, "2.3077"), (100, 4, "2.9126"), (1000, 4, "2.9910"), (10**6, 6, "2.999991")):
        assert equal(rounded(R.subs(t, tv), places), sp.Rational(shown))
    # 3 − R(t) = (3(3 + t) − 3t)/(3 + t) = 9/(3 + t), positive for t > 0.
    assert equal(3 - R, (3 * (3 + t) - 3 * t) / (3 + t))
    assert equal((3 * (3 + t) - 3 * t) / (3 + t), 9 / (3 + t))
    assert positive(9 / (3 + p))
    # 9/(3 + t) < 0.001 exactly when t > 8997, on t > 0.
    assert equal(sp.solveset(9 / (3 + t) < sp.Rational(1, 1000), t, sp.Interval.open(0, oo)), sp.Interval.open(8997, oo))
    assert limit_is(R, t, oo, 3)


def test_definition_examples():
    rng = random.Random(10)
    # 1/x → 0 with N = 1/ε: if x > 1/ε > 0 then 0 < 1/x < ε (x = 1/ε + s, s > 0).
    assert positive(eps - 1 / (1 / eps + s)) and positive(1 / (1 / eps + s))
    assert eps_n_holds(lambda v: 1 / v, 0, lambda e: 1 / e, eps_samples(11))
    assert limit_is(1 / x, x, oo, 0)
    # x² → ∞ with N = max(1, B): x > N ⇒ x² > x > B, on both branches of the max, exactly.
    for b_ in [Q(-10**6), Q(-1), Q(0), Q(1, 2), Q(1) - Q(1, 10**9), Q(1), Q(1) + Q(1, 10**9), Q(7), Q(10**6)] + \
            [Q(rng.randint(-10 * M, 10 * M), M) for _ in range(100)]:
        n_ = max(Q(1), b_)
        for xv in ray(n_, rng):
            assert xv * xv > xv > b_
    # x² − x = x(x − 1) > 0 for x > 1 (x = 1 + s).
    assert positive(sp.expand((1 + s) ** 2 - (1 + s)))
    assert limit_is(x**2, x, oo, oo)
    # Non-example: with ε = 1 and any N, L, the point x = 1 + max(N, |L| + 1) has x > N and
    # |x² − L| > 1.
    for _ in range(500):
        n_, lv = Q(rng.randint(-10**4 * M, 10**4 * M), M), Q(rng.randint(-10**4 * M, 10**4 * M), M)
        xv = 1 + max(n_, abs(lv) + 1)
        assert xv > n_ and xv**2 - lv > 1 and abs(xv**2 - lv) > 1
    # |L| − L ≥ 0 for every real L: it is 0 for L ≥ 0 and −2L > 0 for L < 0.
    assert equal(sp.Abs(p) - p, 0) and equal(sp.Abs(sp.S.Zero) - 0, 0)
    assert equal(sp.Abs(q) - q, -2 * q) and positive(-2 * q)


def test_definition_heights_m_positive():
    # The fourth "In words" bullet: Infinite Limits uses heights M > 0 (and −M for −∞); a
    # threshold that wins the height max(B, 1) wins B, and one that wins −max(−B, 1) wins B with
    # "<". Each of max(B, 1) and max(−B, 1) is a height M > 0 there, on both branches of the max.
    w, u = sp.Symbol("w", nonnegative=True), sp.Symbol("u", positive=True)
    # B ≤ 1 (B = 1 − w): max(B, 1) = 1 > 0, and 1 ≥ B. B > 1 (B = 1 + u): max(B, 1) = B > 0.
    assert equal(sp.Max(1 - w, 1), 1) and nonnegative(1 - (1 - w))
    assert equal(sp.Max(1 + u, 1), 1 + u) and positive(1 + u)
    # −∞: B ≥ −1 (B = −1 + w): max(−B, 1) = 1 and −1 ≤ B. B < −1 (B = −1 − u): max(−B, 1) = −B,
    # so −max(−B, 1) = B.
    assert equal(sp.Max(-(-1 + w), 1), 1) and nonnegative((-1 + w) - (-1))
    assert equal(-sp.Max(-(-1 - u), 1), -1 - u) and positive(1 + u)
    # Exactly, on sampled heights B (both signs, and the breaks ±1 with their neighbours) and
    # values f(x) just beyond the height M: f(x) > M ⇒ f(x) > B, and f(x) < −M ⇒ f(x) < B.
    rng = random.Random(30)
    heights = [Q(-10**6), Q(-1) - Q(1, 10**9), Q(-1), Q(-1) + Q(1, 10**9), Q(0), Q(1, 2),
               Q(1) - Q(1, 10**9), Q(1), Q(1) + Q(1, 10**9), Q(10**6)]
    heights += [Q(rng.randint(-10 * M, 10 * M), M) for _ in range(100)]
    for b_ in heights:
        m_up, m_down = max(b_, Q(1)), max(-b_, Q(1))
        assert m_up > 0 and m_down > 0 and m_up >= b_ and -m_down <= b_
        for fv in ray(m_up, rng, 10):
            assert fv > b_
        for d in ray(Q(0), rng, 10):
            assert -m_down - d < b_


def test_remark_reflection():
    # Property 3: g(t) = f(−t); t > −c exactly when −t < c; lim_{x→−∞} f = lim_{t→∞} g.
    c_ = sp.Symbol("c", real=True)
    assert equal(sp.solveset(t > -c_, t, sp.S.Reals), sp.solveset(-t < c_, t, sp.S.Reals))
    cases = [(x**2, oo), (1 / x, 0), (x**3, -oo), ((x + 4) / (x**2 + 1), 0), ((x**3 - 2 * x) / (4 * x**2 + 1), -oo),
             (x / sp.sqrt(x**2 + 1), -1), ((2 * x - 1) / sp.sqrt(x**2 + 3), -2)]
    for f, value in cases:
        g = f.subs(x, -t)
        assert limit_is(f, x, -oo, value)
        assert limit_is(g, t, oo, value)
    # The non-example of the horizontal asymptotes: g(t) = (−t)² = t².
    assert equal((x**2).subs(x, -t), t**2)
    # A threshold −N for g matches N for f: t > −N ⇔ −t < N, and x < −N ⇔ −x > N.
    n_ = sp.Symbol("N", real=True)
    assert equal(sp.solveset(t > -n_, t, sp.S.Reals), sp.solveset(-t < n_, t, sp.S.Reals))
    assert equal(sp.solveset(x < -n_, x, sp.S.Reals), sp.solveset(-x > n_, x, sp.S.Reals))


def test_horizontal_asymptote_examples():
    # 1/x has y = 0 as x → ∞; x² has no horizontal asymptote (∞ in both directions).
    assert limit_is(1 / x, x, oo, 0) and limit_is(1 / x, x, -oo, 0)
    assert limit_is(x**2, x, oo, oo) and limit_is(x**2, x, -oo, oo)
    # 1/x grows without bound near 0 (from the right +∞, from the left −∞).
    assert limit_is(1 / x, x, 0, oo, dir="+") and limit_is(1 / x, x, 0, -oo, dir="-")


def test_laws_do_not_apply_examples():
    c_ = sp.Symbol("c", real=True)
    # (x + c) − x = c; 2x/x = 2 and x²/x = x for x > 0, with the limits 2 and ∞.
    assert equal((x + c_) - x, c_)
    assert equal_on_domain(2 * x / x, 2, x, (0, oo)) and equal_on_domain(x**2 / x, x, x, (0, oo))
    assert limit_is(2 * x / x, x, oo, 2) and limit_is(x**2 / x, x, oo, oo)
    # The sum proof: ε/2 + ε/2 = ε.
    assert equal(eps / 2 + eps / 2, eps)


# ── prop-calc-rational-at-infinity ────────────────────────────────────────────


def test_prop_part_a_eps_n():
    # Step 1: x ≤ x^j for every x ≥ 1, j = 1, …, 12: with x = 1 + y, y ≥ 0, the difference
    # (1 + y)^j − (1 + y) is a polynomial in y with non-negative coefficients.
    y = sp.Symbol("y", nonnegative=True)
    jj = sp.Symbol("j", integer=True, positive=True)
    # Step 1, the induction, for a symbolic integer j ≥ 1 and x = 1 + y ≥ 1: x^j > 0, and
    # x^(j+1) − x^j = x^j (x − 1) ≥ 0 (the step x^j ≤ x^(j+1)); the base case j = 1 is x ≤ x.
    assert positive((1 + y) ** jj)
    assert equal((1 + y) ** (jj + 1) - (1 + y) ** jj, (1 + y) ** jj * y)
    assert nonnegative((1 + y) ** jj * y)
    assert equal((1 + y) ** 1 - (1 + y), 0)
    # The induction run in exact arithmetic: from x ≤ x (j = 1), each step x^j ≤ x^(j+1) and
    # transitivity give x ≤ x^(j+1), up to j = 40, at x = 1 exactly and at x just above 1.
    rng = random.Random(41)
    for xv in [Q(1), Q(1) + Q(1, 10**9), Q(1) + Q(1, 1000), Q(3, 2), Q(2), Q(10**6)] + \
            [1 + Q(rng.randint(1, 10 * M), M) for _ in range(30)]:
        power = xv  # x^1
        assert xv <= power
        for _ in range(1, 40):
            nxt = power * xv
            assert power > 0 and power <= nxt  # x^j > 0 and x^j ≤ x^(j+1)
            assert xv <= nxt  # by transitivity, from x ≤ x^j
            power = nxt
    for j in range(1, 13):
        diff = sp.Poly(sp.expand((1 + y) ** j - (1 + y)), y)
        assert all(coef >= 0 for coef in diff.all_coeffs())
        assert nonnegative(sp.expand((1 + y) ** j - (1 + y)))
    # Step 2: N = max(1, 1/ε); x > N ⇒ 1/x^j < ε, on both branches of the max (ε ≤ 1 and ε > 1),
    # exactly, right up to the threshold, for j = 1, …, 6.
    for j in range(1, 7):
        assert eps_n_holds(lambda v, j=j: 1 / v**j, 0, lambda e: max(Q(1), 1 / e), eps_samples(20 + j, 60, breaks=(1,)), seed=j)
        assert limit_is(1 / x**j, x, oo, 0)
        assert limit_is(1 / x**j, x, -oo, 0)
        # As x → −∞: 1/(−t)^j = (−1)^j · 1/t^j, since (−1)^j (−1)^j = 1 gives 1/(−1)^j = (−1)^j.
        assert equal(1 / (-t) ** j, (-1) ** j / t**j)
        assert equal((-1) ** j * (-1) ** j, 1) and equal(sp.Rational(1, (-1) ** j), (-1) ** j)
    # The same for a symbolic integer j ≥ 1 (t > 0, written tp: SymPy's t is only real).
    tp = sp.Symbol("t_pos", positive=True)
    assert equal((-1) ** jj * (-1) ** jj, 1)
    assert equal(1 / (-1) ** jj, (-1) ** jj)
    assert equal((-tp) ** jj, (-1) ** jj * tp**jj)
    assert equal(1 / ((-1) ** jj * tp**jj), (-1) ** jj * (1 / tp**jj))
    assert limit_is((-1) ** 3 / t**3, t, oo, 0) and limit_is((-1) ** 4 / t**4, t, oo, 0)
    # Branch ε ≤ 1 (N = 1/ε ≥ 1): x = 1/ε + s gives x^j ≥ x > 1/ε. Branch ε > 1 (N = 1): x > 1
    # gives x^j ≥ x > 1 > 1/ε.
    assert positive(eps - 1 / (1 / eps + s))
    big = sp.Symbol("e_big", positive=True)
    assert positive(1 / (1 + big)) and positive(1 + big - 1 / (1 + big))


def _rule(m, k, a_, b_, direction):
    """The proposition's statement, (b)–(d), for one direction (+1 for ∞, −1 for −∞)."""
    if m < k:
        return sp.Integer(0)
    if m == k:
        return sp.Rational(a_, b_)
    sign = sp.Rational(a_, b_) * (1 if direction == 1 else (-1) ** (m - k))
    return oo if sign > 0 else -oo


def test_prop_parts_b_to_d_random():
    # Random rational functions (degrees 0–5, integer coefficients in [−9, 9], non-zero leading
    # coefficients), in both directions, against SymPy's limit and the table of values.
    rng = random.Random(2026)
    seen = set()
    for _ in range(120):
        m, k = rng.randint(0, 5), rng.randint(0, 5)
        a_ = rng.choice([v for v in range(-9, 10) if v != 0])
        b_ = rng.choice([v for v in range(-9, 10) if v != 0])
        num = a_ * x**m + sum(rng.randint(-9, 9) * x**i for i in range(m))
        den = b_ * x**k + sum(rng.randint(-9, 9) * x**i for i in range(k))
        assert leading(num) == (m, a_) and leading(den) == (k, b_)
        r = num / den
        for direction in (1, -1):
            assert limit_is(r, x, direction * oo, _rule(m, k, a_, b_, direction))
        seen.add((m < k, m == k, m > k, (-1) ** max(m - k, 0) * a_ * b_ > 0))
    # All three cases occurred, and in case (d) both signs of (−1)^(m−k)·a/b.
    assert len(seen) >= 4


def test_prop_specific_cases_and_steps():
    # In-words example and non-example: 3/2 both ways; (x² + 1)/x → ∞ and −∞.
    assert limit_is((3 * x**2 - x + 2) / (2 * x**2 + 5), x, oo, sp.Rational(3, 2))
    assert limit_is((3 * x**2 - x + 2) / (2 * x**2 + 5), x, -oo, sp.Rational(3, 2))
    assert limit_is((x**2 + 1) / x, x, oo, oo) and limit_is((x**2 + 1) / x, x, -oo, -oo)
    assert (-1) ** (2 - 1) * 1 < 0
    # Case (d) as x → −∞ with an even m − k keeps the sign: x³/x → ∞, −x³/x → −∞.
    assert limit_is(x**3 / x, x, -oo, oo) and limit_is(-x**3 / x, x, -oo, -oo)
    # Step 4: q(x)/x^k = b + b_{k−1}/x + … + b_0/x^k, for a generic cubic.
    b0, b1, b2, b3 = sp.symbols("b0:4", real=True)
    qq = b3 * x**3 + b2 * x**2 + b1 * x + b0
    assert equal(qq / x**3, b3 + b2 / x + b1 / x**2 + b0 / x**3)
    assert limit_is((2 * x**3 - x + 4) / x**3, x, oo, 2)
    # Step 6: x^(m−k)·S(x) = r(x) with S = (p/x^m)/(q/x^k).
    pp, qq2 = x**4 - x, 3 - 2 * x**3
    S = (pp / x**4) / (qq2 / x**3)
    assert equal(x ** (4 - 3) * S, pp / qq2)
    assert limit_is(S, x, oo, sp.Rational(1, -2))
    # Step 7: p(−t) has the coefficient (−1)^i a_i at t^i, so degree m and leading coefficient
    # (−1)^m a; and (−1)^m = (−1)^(m−k)(−1)^k.
    rng = random.Random(7)
    for _ in range(20):
        m = rng.randint(0, 6)
        coeffs = [rng.randint(-9, 9) for _ in range(m)] + [rng.choice([1, -1, 2, -3, 5])]
        poly = sum(cf * x**i for i, cf in enumerate(coeffs))
        flipped = sp.Poly(sp.expand(poly.subs(x, -t)), t)
        assert flipped.degree() == m
        assert all(equal(flipped.coeff_monomial(t**i), (-1) ** i * cf) for i, cf in enumerate(coeffs))
    mm, kk = sp.symbols("m k", integer=True)
    assert equal((-1) ** (mm - kk) * (-1) ** kk, (-1) ** mm)
    # Step 7, m = k: (−1)^m a / ((−1)^m b) = a/b.
    a_s, b_s = sp.symbols("a b", real=True, nonzero=True)
    assert equal((-1) ** mm * a_s / ((-1) ** mm * b_s), a_s / b_s)


def test_comparing_growth():
    # x^k/x^m = 1/x^(m−k) → 0 for m > k ≥ 0.
    for m in range(1, 6):
        for k_ in range(0, m):
            assert equal_on_domain(x**k_ / x**m, 1 / x ** (m - k_), x, (0, oo))
            assert limit_is(x**k_ / x**m, x, oo, 0)
    # 1000x² against x³: 100 000 against 1000 at x = 10; equal at 1000; x³ ten times larger at 10 000.
    assert equal((1000 * x**2).subs(x, 10), 100000) and equal((x**3).subs(x, 10), 1000)
    assert equal(sp.solveset(sp.Eq(x**3, 1000 * x**2), x, sp.Interval.open(0, oo)), sp.FiniteSet(1000))
    assert equal((x**3).subs(x, 10000), 10 * (1000 * x**2).subs(x, 10000))
    assert limit_is(1000 * x**2 / x**3, x, oo, 0)
    # p(x)/(a x^m) → 1.
    assert limit_is((3 * x**4 - 7 * x**3 + x - 2) / (3 * x**4), x, oo, 1)
    assert limit_is((3 * x**4 - 7 * x**3 + x - 2) / (3 * x**4), x, -oo, 1)


# ── The figure ────────────────────────────────────────────────────────────────


def test_figure_band_caption():
    f = (2 * x**2 + x) / (x**2 + 1)
    e = sp.Rational(1, 10)
    assert limit_is(f, x, oo, 2)
    # f − 2 = (x − 2)/(x² + 1); the graph meets y = 2 only at x = 2.
    assert equal(f - 2, (x - 2) / (x**2 + 1))
    assert equal(sp.solveset(sp.Eq(f, 2), x, sp.S.Reals), sp.FiniteSet(2))
    # It is in the band 1.9 < y < 2.1 exactly on (−∞, −5 − 2√11) ∪ (−5 + 2√11, 3) ∪ (7, ∞): it leaves
    # through the upper edge at x = 3 and comes back at x = 7. (Second route: f − 2 < 1/10 ⇔
    # (x − 3)(x − 7) > 0 and f − 2 > −1/10 ⇔ x² + 10x − 19 > 0, by the positive denominator.)
    band = sp.solveset(sp.Abs(f - 2) < e, x, sp.S.Reals)
    r11 = 2 * sp.sqrt(11)
    expected = sp.Union(sp.Interval.open(-oo, -5 - r11), sp.Interval.open(-5 + r11, 3), sp.Interval.open(7, oo))
    assert equal(band, expected)
    assert equal(sp.expand(10 * (x**2 + 1) * (e - (f - 2))), sp.expand((x - 3) * (x - 7)))
    assert equal(sp.expand(10 * (x**2 + 1) * ((f - 2) + e)), x**2 + 10 * x - 19)
    assert equal(f.subs(x, 3), 2 + e) and equal(f.subs(x, 7), 2 + e)
    # Above the band on (3, 7), and above y = 2 for every x > 2 ("from above").
    assert equal(sp.solveset(f > 2 + e, x, sp.S.Reals), sp.Interval.open(3, 7))
    assert equal(sp.solveset(f > 2, x, sp.S.Reals), sp.Interval.open(2, oo))
    # The peak is at x = 2 + √5 ≈ 4.24 ("near x = 4"), with the height 2 + √5/(10 + 4√5) ≈ 2.118,
    # just above the band and below the top of the shown range, 2.15.
    crit = sp.solveset(sp.diff(f, x), x, sp.S.Reals)
    assert equal(crit, sp.FiniteSet(2 - sp.sqrt(5), 2 + sp.sqrt(5)))
    peak = f.subs(x, 2 + sp.sqrt(5))
    assert equal(peak, 2 + sp.sqrt(5) / (10 + 4 * sp.sqrt(5)))
    assert 2 + e < peak < sp.Rational(215, 100)
    assert 4 < 2 + sp.sqrt(5) < sp.Rational(45, 10)
    # The plotted piece starts at x = 1.25, at a height just above 1.7 (inside the shown range).
    assert sp.Rational(17, 10) < f.subs(x, sp.Rational(5, 4)) < sp.Rational(18, 10)


def test_figure_band_svg():
    # The SVG's polyline lies on the graph, with the mapping stated in the file:
    # X = 50 + 28.125x on [0, 16], Y = 260 − (240/0.45)(y − 1.7) on [1.7, 2.15]; coordinates are
    # rounded to 0.1, so each point may be off by 0.05 in X and Y.
    svg = FIGURE.read_text()
    assert "x maps to 50 + 28.125 x on [0, 16]; y maps to 260 - 533.3 (y - 1.7) on [1.7, 2.15]" in svg
    fx = sp.lambdify(x, (2 * x**2 + x) / (x**2 + 1))
    dfx = sp.lambdify(x, sp.diff((2 * x**2 + x) / (x**2 + 1), x))
    to_x = lambda X: (X - 50) / 28.125  # noqa: E731
    to_Y = lambda yv: 260 - (240 / 0.45) * (yv - 1.7)  # noqa: E731
    points = [tuple(map(float, pt.split(","))) for pt in re.search(r'<polyline[^>]*points="([^"]+)"', svg).group(1).split()]
    assert len(points) > 100
    assert abs(to_x(points[0][0]) - 1.25) < 0.01 and abs(to_x(points[-1][0]) - 16) < 0.01
    for X, Y in points:
        slope = abs(dfx(to_x(X))) * (240 / 0.45) / 28.125
        assert abs(Y - to_Y(fx(to_x(X)))) <= 0.05 + 0.05 * slope + 1e-6, (X, Y)
    # The band edges, the asymptote and the threshold line are at y = 1.9, 2.1, 2 and x = 7.
    for yv, shown in ((1.9, "153.3"), (2.1, "46.7"), (2.0, "100.0")):
        assert f"{to_Y(yv):.1f}" == shown and f'y1="{shown}" x2="500" y2="{shown}"' in svg
    assert f"{50 + 28.125 * 7:.1f}" == "246.9" and 'x1="246.9" y1="20" x2="246.9" y2="260"' in svg
    # To the right of N = 7 every plotted point is inside the band; between 3 and 7 some are above it.
    assert all(46.7 <= Y <= 153.3 for X, Y in points if to_x(X) > 7)
    assert any(Y < 46.7 for X, Y in points if 3 < to_x(X) < 7)


# ── Worked examples ───────────────────────────────────────────────────────────


@covers("eg-calc-limits-at-infinity-eps-n")
def test_eg_calc_limits_at_infinity_eps_n():
    f = 2 * x / (x + 1)
    # f is defined at every x ≠ −1.
    assert equal(sp.calculus.util.continuous_domain(f, x, sp.S.Reals), sp.S.Reals - sp.FiniteSet(-1))
    # Step 1: f − 2 = (2x − 2(x + 1))/(x + 1) = −2/(x + 1); |f − 2| = 2/(x + 1) for x > −1.
    assert equal(f - 2, (2 * x - 2 * (x + 1)) / (x + 1))
    assert equal((2 * x - 2 * (x + 1)) / (x + 1), -2 / (x + 1))
    # (on x > −1, written x = −1 + p with p > 0, where SymPy can resolve the absolute value)
    assert equal(sp.Abs(f - 2).subs(x, -1 + p), (2 / (x + 1)).subs(x, -1 + p))
    assert equal((2 / (x + 1)).subs(x, -1 + p), 2 / p)
    # Step 2: on x > −1, 2/(x + 1) < ε exactly when x > 2/ε − 1 (exact ε, solved from the raw
    # formula), and N = 2/ε − 1 > −1.
    for e in (sp.Rational(1, 10), sp.Rational(1, 1000), sp.Rational(1), sp.Rational(5), sp.Rational(3, 7)):
        good = sp.solveset(sp.Abs(f - 2) < e, x, sp.Interval.open(-1, oo))
        assert equal(good, sp.Interval.open(2 / e - 1, oo))
    assert positive((2 / eps - 1) - (-1))
    # Step 3: x = N + s, s > 0, gives x + 1 = 2/ε + s and 2/(x + 1) < ε.
    xs = 2 / eps - 1 + s
    assert equal(xs + 1, 2 / eps + s)
    assert positive(eps - 2 / (xs + 1))
    assert equal(2 * (eps / 2), eps)
    # The implication, exactly, right up to the threshold.
    assert eps_n_holds(lambda v: 2 * v / (v + 1), 2, lambda e: 2 / e - 1, eps_samples(1))
    # No smaller threshold: at x = 2/ε − 1, |f − 2| = ε.
    assert equal(sp.Abs(f.subs(x, 2 / eps - 1) - 2), eps)
    # Check: ε = 0.1 gives N = 19; f(20) = 40/21 ≈ 1.904762, 2/21 ≈ 0.095 < 0.1 from 2.
    e = sp.Rational(1, 10)
    assert equal(2 / e - 1, 19)
    assert equal(f.subs(x, 20), sp.Rational(40, 21))
    assert equal(rounded(sp.Rational(40, 21), 6), sp.Rational("1.904762"))
    assert equal(2 - sp.Rational(40, 21), sp.Rational(2, 21))
    assert equal(rounded(sp.Rational(2, 21), 3), sp.Rational("0.095")) and sp.Rational(2, 21) < e
    assert limit_is(f, x, oo, 2)


@covers("eg-calc-limits-at-infinity-rational")
def test_eg_calc_limits_at_infinity_rational():
    f1 = (3 * x**2 - x + 2) / (2 * x**2 + 5)
    f2 = (x + 4) / (x**2 + 1)
    f3 = (x**3 - 2 * x) / (4 * x**2 + 1)
    # (i): m = k = 2, a = 3, b = 2; the divided form; numerator → 3, denominator → 2; limit 3/2.
    assert leading(3 * x**2 - x + 2) == (2, 3) and leading(2 * x**2 + 5) == (2, 2)
    assert equal(f1, (3 - 1 / x + 2 / x**2) / (2 + 5 / x**2))
    assert limit_is(3 - 1 / x + 2 / x**2, x, oo, 3) and limit_is(2 + 5 / x**2, x, oo, 2)
    assert limit_is(f1, x, oo, sp.Rational(3, 2))
    # (ii): m = 1 < k = 2; limit 0 as x → −∞.
    assert leading(x + 4) == (1, 1) and leading(x**2 + 1) == (2, 1)
    assert limit_is(f2, x, -oo, 0)
    # (iii): m = 3 > k = 2, a = 1, b = 4; (−1)^(3−2)·(1/4) = −1/4 < 0; limit −∞. x³/(4x²) = x/4.
    assert leading(x**3 - 2 * x) == (3, 1) and leading(4 * x**2 + 1) == (2, 4)
    assert equal((-1) ** (3 - 2) * sp.Rational(1, 4), -sp.Rational(1, 4))
    assert equal_on_domain(x**3 / (4 * x**2), x / 4, x, (-oo, 0))
    assert limit_is(f3, x, -oo, -oo)
    # Asymptotes: (i) y = 3/2 in both directions, (ii) y = 0 in both, (iii) none (±∞).
    assert limit_is(f1, x, -oo, sp.Rational(3, 2))
    assert limit_is(f2, x, oo, 0)
    assert limit_is(f3, x, oo, oo)
    # Check: (i) at 1000 it is 2 999 002/2 000 005 ≈ 1.499497; (ii) at −1000 ≈ −0.000996;
    # (iii) at −100 ≈ −24.99.
    assert equal(f1.subs(x, 1000), sp.Rational(2999002, 2000005))
    assert equal(rounded(f1.subs(x, 1000), 6), sp.Rational("1.499497"))
    assert equal(rounded(f2.subs(x, -1000), 6), sp.Rational("-0.000996"))
    assert equal(rounded(f3.subs(x, -100), 2), sp.Rational("-24.99"))
    # (iii) at −1000 ≈ −250.00: the value is −999 998 000/4 000 001 = −249.99944…, which rounds
    # to −250.00 at two places (and to −249.9994 at four), and is not −250 itself: hence "about".
    # (The page said "about −249.99" before 99f79da; that assertion went with the claim.)
    v = f3.subs(x, -1000)
    assert equal(v, sp.Rational(-999998000, 4000001))
    assert equal(rounded(v, 2), sp.Rational("-250.00"))
    assert equal(rounded(v, 4), sp.Rational("-249.9994"))
    assert not equal(v, -250) and positive(v + 250)


@covers("eg-calc-limits-at-infinity-conjugate")
def test_eg_calc_limits_at_infinity_conjugate():
    root = sp.sqrt(x**2 + 1)
    # Step 2: |x|² = x² < x² + 1, both |x| and √(x² + 1) non-negative, so |x| < √(x² + 1);
    # −x ≤ |x|; hence √(x² + 1) + x > 0 for every real x.
    assert equal(sp.Abs(x) ** 2, x**2)
    assert equal(root**2 - sp.Abs(x) ** 2, 1)
    assert nonnegative(sp.Abs(x)) and root.is_nonnegative
    assert equal(sp.Abs(p) + p, 2 * p) and equal(sp.Abs(q) + q, 0)  # −x ≤ |x|, on each sign of x
    assert equal(sp.solveset(root + x <= 0, x, sp.S.Reals), sp.S.EmptySet)
    # The conjugate identity, at every real x, as displayed since 99f79da: the product
    # (√(x² + 1) − x)(√(x² + 1) + x) = (x² + 1) − x² = 1, and dividing it by √(x² + 1) + x > 0.
    assert equal(sp.expand((root - x) * (root + x)), (x**2 + 1) - x**2)
    assert equal((x**2 + 1) - x**2, 1)
    assert equal((root - x) * (root + x) / (root + x), root - x)
    assert equal(root - x, 1 / (root + x))
    assert equal(sp.sqrt(p) ** 2, p)
    # Step 3: for x > 0, x√(1 + 1/x²) ≥ 0 with square x² + 1, so it is √(x² + 1); divided by x.
    assert nonnegative(p * sp.sqrt(1 + 1 / p**2))
    assert equal(sp.expand((p * sp.sqrt(1 + 1 / p**2)) ** 2), p**2 + 1)
    assert equal(p * sp.sqrt(1 + 1 / p**2), sp.sqrt(p**2 + 1))
    assert equal(1 / (sp.sqrt(p**2 + 1) + p), (1 / p) / (sp.sqrt(1 + 1 / p**2) + 1))
    # Step 4: 1/x² → 0, 1 + 1/x² → 1, √(1 + 1/x²) → 1, denominator → 2, numerator → 0; limit 0.
    assert limit_is(1 / x**2, x, oo, 0)
    assert limit_is(sp.sqrt(1 + 1 / x**2), x, oo, 1)
    assert limit_is(sp.sqrt(1 + 1 / x**2) + 1, x, oo, 2)
    assert limit_is((1 / x) / (sp.sqrt(1 + 1 / x**2) + 1), x, oo, 0)
    assert limit_is(root - x, x, oo, 0)
    # Check at x = 1000: √1 000 001 − 1000 ≈ 0.0005, and 1/(√1 000 001 + 1000) ≈ 1/2000.
    v = (root - x).subs(x, 1000)
    assert equal(rounded(v, 4), sp.Rational("0.0005"))
    assert sp.Abs(v - sp.Rational(1, 2000)) < sp.Rational(1, 10**9)


@covers("eg-calc-limits-at-infinity-two-asymptotes")
def test_eg_calc_limits_at_infinity_two_asymptotes():
    f = x / sp.sqrt(x**2 + 1)
    # Step 1: x² + 1 ≥ 1 > 0, so f is defined on ℝ.
    assert nonnegative(x**2 + 1 - 1)
    assert equal(sp.calculus.util.continuous_domain(f, x, sp.S.Reals), sp.S.Reals)
    # Step 2: for x ≠ 0, |x|√(1 + 1/x²) ≥ 0 has square |x|²(1 + 1/x²) = x² + 1, so it is √(x² + 1):
    # on each side of 0.
    for z in (p, q):
        assert nonnegative(sp.Abs(z) * sp.sqrt(1 + 1 / z**2))
        assert equal(sp.expand(sp.Abs(z) ** 2 * (1 + 1 / z**2)), z**2 + 1)
        assert equal(sp.Abs(z) * sp.sqrt(1 + 1 / z**2), sp.sqrt(z**2 + 1))
    # √(x²) = |x|, which is −x for x < 0.
    assert equal(sp.sqrt(x**2), sp.Abs(x))
    assert equal(sp.Abs(q), -q) and equal(sp.sqrt(q**2), -q)
    # Steps 3 and 4: f = 1/√(1 + 1/x²) for x > 0, and f = x/(−x√(1 + 1/x²)) = −1/√(1 + 1/x²) for x < 0.
    assert equal(f.subs(x, p), 1 / sp.sqrt(1 + 1 / p**2))
    assert equal(f.subs(x, q), q / (-q * sp.sqrt(1 + 1 / q**2)))
    assert equal(q / (-q * sp.sqrt(1 + 1 / q**2)), -1 / sp.sqrt(1 + 1 / q**2))
    assert limit_is(1 / x**2, x, -oo, 0)
    assert limit_is(f, x, oo, 1)
    # Step 4 as written since 99f79da: as x → −∞, 1 + 1/x² → 1, √(1 + 1/x²) → 1 ≠ 0,
    # 1/√(1 + 1/x²) → 1, and the factor −1 gives −1; the formula holds at every x < 0.
    assert limit_is(1 + 1 / x**2, x, -oo, 1)
    assert limit_is(sp.sqrt(1 + 1 / x**2), x, -oo, 1)
    assert limit_is(1 / sp.sqrt(1 + 1 / x**2), x, -oo, 1)
    assert limit_is(-1 / sp.sqrt(1 + 1 / x**2), x, -oo, -1)
    assert equal_on_domain(f, -1 / sp.sqrt(1 + 1 / x**2), x, (-oo, 0))
    assert limit_is(f, x, -oo, -1)
    # Check: f(1000) ≈ 0.9999995, f(−1000) ≈ −0.9999995; f has the sign of x.
    assert equal(rounded(f.subs(x, 1000), 7), sp.Rational("0.9999995"))
    assert equal(rounded(f.subs(x, -1000), 7), sp.Rational("-0.9999995"))
    assert positive(f.subs(x, p)) and negative(f.subs(x, q))


@covers("eg-calc-limits-at-infinity-resistors")
def test_eg_calc_limits_at_infinity_resistors():
    R = 3 * t / (3 + t)
    # Step 1: R agrees with 3t/(t + 3), defined at every t ≠ −3.
    assert equal(R, 3 * t / (t + 3))
    assert equal(sp.calculus.util.continuous_domain(3 * t / (t + 3), t, sp.S.Reals), sp.S.Reals - sp.FiniteSet(-3))
    # Step 2: m = k = 1, a = 3, b = 1; the limit 3.
    assert leading(3 * t, t) == (1, 3) and leading(t + 3, t) == (1, 1)
    assert limit_is(R, t, oo, 3)
    # Step 3: for t > 0, |R − 3| = 3 − R = 9/(3 + t); < 0.01 exactly when 3 + t > 900, t > 897.
    assert equal_on_domain(sp.Abs(R - 3), 9 / (3 + t), t, (0, oo))
    assert equal(sp.solveset(9 / (3 + t) < sp.Rational(1, 100), t, sp.Interval.open(0, oo)), sp.Interval.open(897, oo))
    assert equal(sp.solveset(sp.Abs(R - 3) < sp.Rational(1, 100), t, sp.Interval.open(0, oo)), sp.Interval.open(897, oo))
    assert equal(sp.Rational(9) / sp.Rational(1, 100), 900)
    # Check: R(897) = 2691/900 = 2.99, exactly 0.01 below 3; R(898) = 2694/901 ≈ 2.990011.
    assert equal(R.subs(t, 897), sp.Rational(2691, 900)) and equal(sp.Rational(2691, 900), sp.Rational("2.99"))
    assert equal(3 - R.subs(t, 897), sp.Rational(1, 100))
    assert equal(R.subs(t, 898), sp.Rational(2694, 901))
    assert equal(rounded(sp.Rational(2694, 901), 6), sp.Rational("2.990011"))
    # R(t) < 3 and R(t) < t for t > 0 (a parallel pair is smaller than each resistor).
    assert positive(3 - R.subs(t, p))
    assert equal(p - R.subs(t, p), p**2 / (3 + p)) and positive(p**2 / (3 + p))


# ── Common mistakes ───────────────────────────────────────────────────────────


def test_common_mistakes():
    f = x / sp.sqrt(x**2 + 1)
    # √(x² + 1) = x√(1 + 1/x²) is false for x < 0: the wrong form is positive, f is not.
    wrong = 1 / sp.sqrt(1 + 1 / x**2)
    assert not equal(f.subs(x, -10), wrong.subs(x, -10))
    assert equal(rounded(f.subs(x, -10), 3), sp.Rational("-0.995"))
    assert limit_is(f, x, -oo, -1) and limit_is(wrong, x, -oo, 1)
    # "∞ − ∞": (x + c) − x = c; √(x² + x) − x = x/(√(x² + x) + x) = 1/(√(1 + 1/x) + 1) for x > 0,
    # with the limit 1/2; ≈ 0.49999 at x = 10 000.
    assert equal(sp.sqrt(p**2 + p), p * sp.sqrt(1 + 1 / p))
    assert equal(sp.sqrt(p**2 + p) - p, p / (sp.sqrt(p**2 + p) + p))
    assert equal(p / (sp.sqrt(p**2 + p) + p), 1 / (sp.sqrt(1 + 1 / p) + 1))
    assert limit_is(sp.sqrt(x**2 + x) - x, x, oo, sp.Rational(1, 2))
    assert equal(rounded((sp.sqrt(x**2 + x) - x).subs(x, 10000), 5), sp.Rational("0.49999"))
    # "∞/∞": (2x + 1)/(x + 5) → 2/1 = 2; ≈ 1.991 at x = 1000.
    assert leading(2 * x + 1) == (1, 2) and leading(x + 5) == (1, 1)
    assert limit_is((2 * x + 1) / (x + 5), x, oo, 2)
    assert equal(rounded(sp.Rational(2001, 1005), 3), sp.Rational("1.991"))
    # "A graph never crosses its asymptote": (2·4 + 2)/(4 + 1) = 2 at x = 2.
    g = (2 * x**2 + x) / (x**2 + 1)
    assert equal(g.subs(x, 2), sp.Rational(8 + 2, 4 + 1)) and equal(g.subs(x, 2), 2)


# ── Rigorous track ────────────────────────────────────────────────────────────


def test_rigorous_track_reciprocal_substitution():
    f = (2 * x**2 + x) / (x**2 + 1)
    # g(t) = f(1/t) = (2 + t)/(1 + t²) for t > 0 (multiplying by t²), and for t < 0 too.
    g = f.subs(x, 1 / t)
    assert equal(g, (2 + t) / (1 + t**2))
    assert equal(((2 / t**2 + 1 / t) * t**2), 2 + t) and equal(((1 / t**2 + 1) * t**2), 1 + t**2)
    # Direct substitution at 0 gives 2; the right-hand and the left-hand limits are 2.
    assert equal(((2 + t) / (1 + t**2)).subs(t, 0), 2)
    assert limit_is((2 + t) / (1 + t**2), t, 0, 2, dir="+")
    assert limit_is(g, t, 0, 2, dir="+") and limit_is(g, t, 0, 2, dir="-")
    assert limit_is(f, x, oo, 2) and limit_is(f, x, -oo, 2)
    # The key fact: for positive t and δ, t < δ exactly when 1/t > 1/δ.
    d = sp.Symbol("delta", positive=True)
    # 1/t − 1/δ = (δ − t)/(tδ), and tδ > 0, so the two differences have the same sign.
    tp = sp.Symbol("t_pos", positive=True)
    assert equal(1 / tp - 1 / d, (d - tp) / (tp * d)) and positive(tp * d)
    for dv in (sp.Rational(1, 10), sp.Rational(3), sp.Rational(7, 1000)):
        assert equal(sp.solveset(t < dv, t, sp.Interval.open(0, oo)), sp.solveset(1 / t > 1 / dv, t, sp.Interval.open(0, oo)))
    # Thresholds: δ = 1/N' with N' = max(N, 1): 0 < t < δ gives 1/t > N'; and N = 1/δ: x > N gives
    # 0 < 1/x < δ (x = 1/δ + s).
    assert positive(d - 1 / (1 / d + s)) and positive(1 / (1 / d + s))
    nn = sp.Symbol("Nprime", positive=True)
    tt = 1 / (nn + s)  # every t in (0, 1/N') is 1/(N' + s) for some s > 0
    assert positive(1 / nn - tt) and positive(1 / tt - nn)
    # Other examples: lim_{x→∞} f(x) = lim_{t→0⁺} f(1/t), and x → −∞ ↔ t → 0⁻.
    for h_, right, left in ((x / sp.sqrt(x**2 + 1), 1, -1), ((2 * x - 1) / sp.sqrt(x**2 + 3), 2, -2), (sp.sqrt(x**2 + 1) - x, 0, oo)):
        assert limit_is(h_.subs(x, 1 / t), t, 0, right, dir="+") and limit_is(h_, x, oo, right)
        assert limit_is(h_.subs(x, 1 / t), t, 0, left, dir="-") and limit_is(h_, x, -oo, left)


# ── Exercises ─────────────────────────────────────────────────────────────────


@covers("exr-calc-limits-at-infinity-equal-degree")
def test_exr_calc_limits_at_infinity_equal_degree():
    num, den = 4 * x**3 - x + 1, 2 * x**3 + 7 * x**2
    (m, a_), (k_, b_) = leading(num), leading(den)
    assert m == k_
    expected = sp.Rational(a_, b_)
    assert limit_is(num / den, x, oo, expected)
    assert equal(answer("exr-calc-limits-at-infinity-equal-degree"), expected)


@covers("exr-calc-limits-at-infinity-lower-degree")
def test_exr_calc_limits_at_infinity_lower_degree():
    f = (5 * x + 2) / (x**2 - 3)
    assert leading(5 * x + 2)[0] < leading(x**2 - 3)[0]
    value = answer("exr-calc-limits-at-infinity-lower-degree")
    assert limit_is(f, x, -oo, value)
    assert equal(value, 0)
    # The solution's aside: also 0 as x → ∞.
    assert limit_is(f, x, oo, 0)


@covers("exr-calc-limits-at-infinity-higher-degree")
def test_exr_calc_limits_at_infinity_higher_degree():
    num, den = x**4 - x, 3 - 2 * x**3
    (m, a_), (k_, b_) = leading(num), leading(den)
    assert (m, a_, k_, b_) == (4, 1, 3, -2)
    assert equal((-1) ** (m - k_) * sp.Rational(a_, b_), sp.Rational(1, 2))
    value = answer("exr-calc-limits-at-infinity-higher-degree")
    assert equal(value, oo)
    assert limit_is(num / den, x, -oo, value)
    # Far to the left it behaves like x⁴/(−2x³) = −x/2; at x = −10 it is 10 010/2003 ≈ 5.0.
    assert equal_on_domain(x**4 / (-2 * x**3), -x / 2, x, (-oo, 0))
    assert equal((num / den).subs(x, -10), sp.Rational(10010, 2003))
    assert equal(rounded(sp.Rational(10010, 2003), 1), sp.Rational("5.0"))


@covers("exr-calc-limits-at-infinity-asymptote")
def test_exr_calc_limits_at_infinity_asymptote():
    f = (1 - 4 * x**2) / (x**2 + x + 1)
    # The denominator is (x + 1/2)² + 3/4 ≥ 3/4, never 0: f is defined on ℝ.
    assert equal(x**2 + x + 1, (x + sp.Rational(1, 2)) ** 2 + sp.Rational(3, 4))
    assert equal(sp.solveset(x**2 + x + 1, x, sp.S.Reals), sp.S.EmptySet)
    assert leading(1 - 4 * x**2) == (2, -4) and leading(x**2 + x + 1) == (2, 1)
    value = answer("exr-calc-limits-at-infinity-asymptote")
    # Exactly one horizontal asymptote: both limits are the same number L.
    assert limit_is(f, x, oo, value) and limit_is(f, x, -oo, value)
    assert equal(value, sp.limit(f, x, oo)) and equal(value, -4)


@covers("exr-calc-limits-at-infinity-figure-threshold")
def test_exr_calc_limits_at_infinity_figure_threshold():
    f = (2 * x**2 + x) / (x**2 + 1)
    e = sp.Rational(1, 10)
    assert limit_is(f, x, oo, 2)
    # The smallest N with |f − 2| < 0.1 at every x > N is the supremum of the set where it fails.
    bad = sp.S.Reals - sp.solveset(sp.Abs(f - 2) < e, x, sp.S.Reals)
    n_min = bad.sup
    assert equal(n_min, 7)
    # Second route: f − 2 = (x − 2)/(x² + 1) > 0 for x > 2, and f − 2 < 1/10 ⇔ (x − 3)(x − 7) > 0;
    # at x = 7 the distance is exactly 1/10, and every x > 7 is inside.
    assert equal(f - 2, (x - 2) / (x**2 + 1))
    assert equal(x**2 - 10 * x + 21, (x - 3) * (x - 7))
    assert equal(sp.Abs(f.subs(x, 7) - 2), e)
    assert positive(((x - 3) * (x - 7)).subs(x, 7 + s)) and positive((7 + s - 2) / ((7 + s) ** 2 + 1))
    rng = random.Random(5)
    for xv in ray(Q(7), rng, 200):
        assert abs((2 * xv**2 + xv) / (xv**2 + 1) - 2) < Q(1, 10)
    # Every N < 7 fails at x = 7; between 3 and 7 the graph is above the band.
    assert equal(sp.solveset(f - 2 >= e, x, sp.S.Reals), sp.Interval(3, 7))
    assert equal(answer("exr-calc-limits-at-infinity-figure-threshold"), n_min)


@covers("exr-calc-limits-at-infinity-conjugate")
def test_exr_calc_limits_at_infinity_conjugate():
    f = sp.sqrt(x**2 + 6 * x) - x
    # For x > 0: x² + 6x = x(x + 6) > 0; the conjugate step; x√(1 + 6/x) = √(x² + 6x); divided by x.
    assert equal(p**2 + 6 * p, p * (p + 6)) and positive(p * (p + 6))
    assert equal(sp.expand((sp.sqrt(p**2 + 6 * p) - p) * (sp.sqrt(p**2 + 6 * p) + p)), 6 * p)
    assert equal(sp.sqrt(p**2 + 6 * p) - p, 6 * p / (sp.sqrt(p**2 + 6 * p) + p))
    assert equal(p * sp.sqrt(1 + 6 / p), sp.sqrt(p**2 + 6 * p))
    assert equal(6 * p / (sp.sqrt(p**2 + 6 * p) + p), 6 / (sp.sqrt(1 + 6 / p) + 1))
    assert limit_is(sp.sqrt(1 + 6 / x), x, oo, 1)
    value = answer("exr-calc-limits-at-infinity-conjugate")
    assert limit_is(f, x, oo, value)
    assert equal(value, 3)


@covers("exr-calc-limits-at-infinity-sqrt-minus-infinity")
def test_exr_calc_limits_at_infinity_sqrt_minus_infinity():
    f = (2 * x - 1) / sp.sqrt(x**2 + 3)
    assert equal(sp.calculus.util.continuous_domain(f, x, sp.S.Reals), sp.S.Reals)
    # For x < 0: −x√(1 + 3/x²) ≥ 0 has square x² + 3, so it is √(x² + 3); the divided form.
    assert nonnegative(-q * sp.sqrt(1 + 3 / q**2))
    assert equal(sp.expand((-q * sp.sqrt(1 + 3 / q**2)) ** 2), q**2 + 3)
    assert equal(-q * sp.sqrt(1 + 3 / q**2), sp.sqrt(q**2 + 3))
    assert equal(f.subs(x, q), (2 * q - 1) / (-q * sp.sqrt(1 + 3 / q**2)))
    assert equal((2 * q - 1) / (-q * sp.sqrt(1 + 3 / q**2)), -(2 - 1 / q) / sp.sqrt(1 + 3 / q**2))
    assert limit_is(2 - 1 / x, x, -oo, 2) and limit_is(sp.sqrt(1 + 3 / x**2), x, -oo, 1)
    value = answer("exr-calc-limits-at-infinity-sqrt-minus-infinity")
    assert limit_is(f, x, -oo, value)
    assert equal(value, -2)
    # The aside: 2 as x → ∞.
    assert limit_is(f, x, oo, 2)


@covers("exr-calc-limits-at-infinity-root-over-linear")
def test_exr_calc_limits_at_infinity_root_over_linear():
    f = sp.sqrt(x) / (x + 1)
    # For x > 0: √x > 0, √(1/x) = 1/√x, √x/x = 1/√x, and the divided form.
    assert positive(sp.sqrt(p))
    assert equal(sp.sqrt(1 / p), 1 / sp.sqrt(p)) and equal((1 / sp.sqrt(p)) ** 2, 1 / p)
    assert equal(sp.sqrt(p) * sp.sqrt(p), p) and equal(sp.sqrt(p) / p, 1 / sp.sqrt(p))
    assert equal(f.subs(x, p), sp.sqrt(1 / p) / (1 + 1 / p))
    # 1/x ≥ 0 for x > 0 (the hypothesis of part (f) with L = 0, K = 0); √(1/x) → 0, 1 + 1/x → 1.
    assert nonnegative(1 / p)
    assert limit_is(sp.sqrt(1 / x), x, oo, 0) and limit_is(1 + 1 / x, x, oo, 1)
    value = answer("exr-calc-limits-at-infinity-root-over-linear")
    assert limit_is(f, x, oo, value)
    assert equal(value, 0)


@covers("exr-calc-limits-at-infinity-average-cost")
def test_exr_calc_limits_at_infinity_average_cost():
    A = (2000 + 45 * x) / x
    assert leading(45 * x + 2000) == (1, 45) and leading(x) == (1, 1)
    value = answer("exr-calc-limits-at-infinity-average-cost")
    assert limit_is(A, x, oo, value)
    assert equal(value, 45)
    # A − 45 = 2000/x; for x > 0, A < 50 exactly when x > 400.
    assert equal(A - 45, 2000 / x)
    assert equal(sp.solveset(A < 50, x, sp.Interval.open(0, oo)), sp.Interval.open(400, oo))
    assert equal(A.subs(x, 400), 50)


@covers("exr-calc-limits-at-infinity-difference")
def test_exr_calc_limits_at_infinity_difference():
    # The counterexample f = x + 1, g = x: both → ∞, f − g = 1 → 1 ≠ 0. So the claim is false.
    f, g = x + 1, x
    assert limit_is(f, x, oo, oo) and limit_is(g, x, oo, oo)
    assert equal(f - g, 1)
    assert limit_is(f - g, x, oo, 1)
    # N = B − 1 wins the round B for f: x = B − 1 + s gives x + 1 = B + s > B.
    assert positive((B - 1 + s) + 1 - B)
    # Other pairs: (x + c) − x → c for every c; x² − x → ∞; x − x² → −∞.
    assert limit_is(x**2 - x, x, oo, oo) and limit_is(x - x**2, x, oo, -oo)
    claim_holds = sp.limit(f - g, x, oo) == 0
    assert equal(answer("exr-calc-limits-at-infinity-difference"), sp.true if claim_holds else sp.false)


@covers("exr-calc-limits-at-infinity-oblique")
def test_exr_calc_limits_at_infinity_oblique():
    f = (x**2 + 1) / (x + 1)
    # Independently: m = lim f(x)/x, c = lim (f(x) − m x).
    m = sp.limit(f / x, x, oo)
    assert limit_is(f / x, x, oo, m)
    c_ = sp.limit(f - m * x, x, oo)
    assert limit_is(f - m * x, x, oo, c_)
    assert limit_is(f - (m * x + c_), x, oo, 0)
    # The solution's division: (x + 1)(x − 1) + 2 = x² + 1; quotient x − 1, remainder 2;
    # f = x − 1 + 2/(x + 1) for x ≠ −1, and 2/(x + 1) → 0.
    assert equal(sp.expand((x + 1) * (x - 1) + 2), x**2 + 1)
    assert sp.div(x**2 + 1, x + 1, x) == (x - 1, 2)
    assert equal(f, x - 1 + 2 / (x + 1))
    assert limit_is(2 / (x + 1), x, oo, 0)
    # Uniqueness: (m' − m)x + (c' − c) → ±∞ when m' ≠ m, and → c' − c when m' = m.
    for dm, dc in ((1, 0), (-2, 5), (sp.Rational(1, 3), -1)):
        assert limit_is(dm * x + dc, x, oo, oo if dm > 0 else -oo)
    for dc in (1, -3, sp.Rational(1, 7)):
        assert limit_is(f - (m * x + c_ + dc), x, oo, -dc)
    assert equal(answer("exr-calc-limits-at-infinity-oblique"), (m, c_))


@covers("exr-calc-limits-at-infinity-reciprocal")
def test_exr_calc_limits_at_infinity_reciprocal():
    # A manual answer (a proof): its key claims are checked here; it counts as covered only
    # through a reviewer's note in maths.manual_checked.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limits-at-infinity-reciprocal")
    # The round B = 1/ε: if f(x) > 1/ε > 0, then 0 < 1/f(x) < ε (f(x) = 1/ε + s, s > 0).
    fx = 1 / eps + s
    assert positive(1 / eps)
    assert positive(1 / fx) and positive(eps - 1 / fx)
    assert equal(1 / (1 / eps), eps)
    # The domain: f(x) > 1 > 0 makes 1/f(x) defined.
    assert positive(1 + s)
    # Exactly, on sampled (ε, f(x)) pairs right above the height 1/ε.
    rng = random.Random(3)
    for e in eps_samples(4):
        for fv in ray(1 / e, rng, 10):
            assert 0 < 1 / fv < e
    # Instances: f = x, x², x + 1, √x, x³ − x all → ∞, and their reciprocals → 0.
    for f in (x, x**2, x + 1, sp.sqrt(x), x**3 - x):
        assert limit_is(f, x, oo, oo) and limit_is(1 / f, x, oo, 0)


@covers("exr-calc-limits-at-infinity-sqrt-unbounded")
def test_exr_calc_limits_at_infinity_sqrt_unbounded():
    # A manual answer (a proof): its key claims are checked here; the reviewer's note covers it.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-limits-at-infinity-sqrt-unbounded")
    assert limit_is(sp.sqrt(x), x, oo, oo)
    # B > 0, N = B²: x = B² + s gives √x > B (squares of non-negative numbers compared).
    bp = sp.Symbol("B_pos", positive=True)
    # (√(B² + s))² − B² = s > 0, both roots non-negative, so √(B² + s) > √(B²) = B.
    assert equal(sp.sqrt(bp**2 + s) ** 2 - sp.sqrt(bp**2) ** 2, s)
    assert nonnegative(sp.sqrt(bp**2 + s)) and nonnegative(bp)
    assert equal(sp.sqrt(bp**2), bp)
    assert equal(sp.solveset(sp.sqrt(x) > 3, x, sp.Interval(0, oo)), sp.Interval.open(9, oo))
    # B ≤ 0, N = 0: x > 0 gives √x > 0 ≥ B.
    assert positive(sp.sqrt(p))
    # Exactly, on sampled B (both signs) and x right above the threshold.
    rng = random.Random(8)
    heights = [Q(-10**6), Q(-1), Q(0), Q(1, 10**9), Q(1, 1000), Q(1), Q(7, 3), Q(10**4)]
    heights += [Q(rng.randint(-10 * M, 10 * M), M) for _ in range(60)]
    for b_ in heights:
        n_ = b_**2 if b_ > 0 else Q(0)
        for xv in ray(n_, rng, 5):
            assert sp.sqrt(sp.Rational(xv.numerator, xv.denominator)) > sp.Rational(b_.numerator, b_.denominator)
        # For B > 0 no smaller threshold works: at x = B², √x = B.
        if b_ > 0:
            assert equal(sp.sqrt(sp.Rational(b_.numerator, b_.denominator) ** 2), sp.Rational(b_.numerator, b_.denominator))
