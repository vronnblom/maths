"""Verification tests for content/calculus/limits/computing-limits.md (calc-computing-limits).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
here is derived independently from the statements and the displayed steps (by cancelling with
SymPy, by polynomial division, or by a second route such as a derivative); the answers are read
with answer(label), as printed on the page.

Limits are checked with limit_is, which needs sp.limit and a 60-digit table of values on both
sides to agree. The lemma's δ = min(δ₀, r) is checked on each branch of the min, and its
implication on exact rational (ε, x) pairs up to the edge of the window (fractions.Fraction), as
in test_limit_of_a_function.py: floats could hide a failure at the edge.
"""

import random
from fractions import Fraction as Q

import pytest
import sympy as sp

from mathcheck import (
    ManualAnswer, a, answer, answer_type, c, covers, equal, equal_on_domain, limit_is, n, t, u, x,
)

eps = sp.Symbol("epsilon", positive=True)
N = 10**6


def eps_samples(seed, count=200, breaks=()):
    """Exact rational tolerances: tiny, moderate and huge ones, each break of a min (the ε where
    the branches meet) and its immediate neighbours, and random ones."""
    rng = random.Random(seed)
    fixed = [Q(1, 10**9), Q(1, 10**6), Q(1, 1000), Q(1, 100), Q(1, 10), Q(1, 2), Q(1), Q(3), Q(100), Q(10**6)]
    for b in breaks:
        fixed += [Q(b), Q(b) - Q(1, 10**9), Q(b) + Q(1, 10**9)]
    return fixed + [Q(rng.randint(1, 20 * N), N) for _ in range(count)]


def window(a_, d, rng, count=30):
    """Exact rational points x with 0 < |x − a| < d, on both sides: right next to a, right at the
    edge of the window (within 10⁻⁹ of d), and random ones in between."""
    fractions = [Q(1, 10**9), Q(1, N), Q(N - 1, N), Q(10**9 - 1, 10**9)]
    fractions += [Q(rng.randint(1, N - 1), N) for _ in range(count)]
    for fr in fractions:
        yield a_ + d * fr
        yield a_ - d * fr


def implication_holds(F, a_, lim, choose_delta, samples, seed=0, count=30):
    """0 < |x − a| < δ ⇒ F is defined at x and |F(x) − L| < ε, at every sampled (ε, x) pair, in
    exact arithmetic. F returns None where it is undefined."""
    rng = random.Random(seed)
    for e in samples:
        d = choose_delta(e)
        assert d > 0
        for xv in window(a_, d, rng, count):
            fx = F(xv)
            assert fx is not None, f"ε = {e}, δ = {d}, x = {xv}: F is undefined there"
            assert abs(fx - lim) < e, f"ε = {e}, δ = {d}, x = {xv}: |F(x) − L| = {abs(fx - lim)}"
    return True


def rounds_to(exact, shown):
    """`shown` (a decimal string) is `exact` correctly rounded to the digits shown."""
    places = len(shown.split(".")[1]) if "." in shown else 0
    err = sp.Abs(sp.nsimplify(exact) - sp.Rational(shown)) if exact.is_Rational else \
        sp.Abs(sp.N(exact, 50) - sp.Rational(shown))
    return bool(err <= sp.Rational(1, 2 * 10**places))


def no_real_limit(expr, var, a_):
    """No real two-sided limit at a_: the one-sided limits are infinite (sp.limit, with a table of
    values through limit_is as the second route), or they differ."""
    right, left = sp.limit(expr, var, a_, "+"), sp.limit(expr, var, a_, "-")
    assert limit_is(expr, var, a_, right, dir="+") and limit_is(expr, var, a_, left, dir="-")
    return right.is_infinite or left.is_infinite or not equal(right, left)


def window_free_of(den, var, a_, r):
    """den has no root x with 0 < |x − a| < r (solved over the reals)."""
    roots = sp.solveset(sp.Eq(den, 0), var, sp.S.Reals)
    punctured = sp.Union(sp.Interval.open(a_ - r, a_), sp.Interval.open(a_, a_ + r))
    return equal(sp.Intersection(roots, punctured), sp.S.EmptySet)


def punctured_window_set(a_, r):
    return sp.Union(sp.Interval.open(a_ - r, a_), sp.Interval.open(a_, a_ + r))


def multiplicity_by_division(p, var, a_):
    """Divide p by (x − a) while the remainder is 0, as the factoring paragraph and the rigorous
    track do. Returns (number of steps, final quotient)."""
    steps, cur = 0, sp.Poly(p, var)
    while True:
        quo, rem = sp.div(cur, sp.Poly(var - a_, var))
        if not rem.is_zero:
            return steps, cur.as_expr()
        steps, cur = steps + 1, quo


# ── Why this matters: the cube and its figure ────────────────────────────────────


def test_why_this_matters_and_figure():
    A = (x**3 - 8) / (x - 2)
    g = x**2 + 2 * x + 4
    # The factorisation the page recalls, and A = g at every x ≠ 2 (and A is undefined at 2).
    assert equal(sp.expand((x - 2) * g), x**3 - 8)
    assert equal_on_domain(A, g, x, (-100, 2)) and equal_on_domain(A, g, x, (2, 100))
    assert A.subs(x, 2) is sp.nan
    # 2² + 2·2 + 4 = 12; the quotient law cannot apply (the denominator → 0).
    assert equal(g.subs(x, 2), 12) and equal(sp.limit(x - 2, x, 2), 0)
    assert limit_is(A, x, 2, 12)
    # Caption: rising from 4 at x = 0 to 28 at x = 4 (A = g there, and g' = 2x + 2 > 0 on [0, 4]).
    assert equal(A.subs(x, 0), 4) and equal(A.subs(x, 4), 28)
    assert equal(sp.solveset(sp.diff(g, x) <= 0, x, sp.Interval(0, 4)), sp.S.EmptySet)
    assert 0 <= 4 and 28 <= 30   # inside the figure's yRange [0, 30]
    # Caption table, exactly as listed, and "they approach 12 from both sides".
    table = {"1.9": "11.41", "1.99": "11.9401", "1.999": "11.994001",
             "2.001": "12.006001", "2.01": "12.0601", "2.1": "12.61"}
    for p, v in table.items():
        assert equal(A.subs(x, sp.Rational(p)), sp.Rational(v))
    left = [sp.Rational(table[p]) for p in ("1.9", "1.99", "1.999")]
    right = [sp.Rational(table[p]) for p in ("2.1", "2.01", "2.001")]
    assert left[0] < left[1] < left[2] < 12 < right[2] < right[1] < right[0]
    # Try this: x² + 2x + 4 at 1.99 is the table's value there, and at 2 it is 12.
    assert equal(g.subs(x, sp.Rational("1.99")), A.subs(x, sp.Rational("1.99")))
    assert equal(g.subs(x, 2), 12)


def test_zero_over_zero_definition_examples():
    # Example: x³ − 8 → 0 and x − 2 → 0 at 2, the quotient defined at every x ≠ 2.
    assert equal(sp.limit(x**3 - 8, x, 2), 0) and equal(sp.limit(x - 2, x, 2), 0)
    assert equal(sp.solveset(sp.Eq(x - 2, 0), x, sp.S.Reals), sp.FiniteSet(2))
    # Non-example: denominator → 4, the limit is 0/4 = 0.
    assert equal(sp.limit(x + 2, x, 2), 4) and limit_is((x**3 - 8) / (x + 2), x, 2, 0)
    # Non-example: 1/x, numerator → 1, no limit at 0.
    assert no_real_limit(1 / x, x, 0)


# ── The lemma (F): δ = min(δ₀, r) ────────────────────────────────────────────────


def test_lem_calc_limit_agree_except_point_delta_chain():
    d0, r = sp.symbols("delta_0 r", positive=True)
    s = sp.Symbol("s", nonnegative=True)
    # δ = min(δ₀, r) is positive, and on each branch of the min it is ≤ r and ≤ δ₀.
    delta = sp.Min(d0, r)
    assert delta.is_positive
    for branch, (dd0, rr, expected) in {"δ₀ ≤ r": (d0, d0 + s, d0), "r ≤ δ₀": (r + s, r, r)}.items():
        dv = sp.Min(dd0, rr)
        assert equal(dv, expected), branch
        assert dv.is_positive, branch
        assert (rr - dv).is_nonnegative, branch
        assert (dd0 - dv).is_nonnegative, branch
    # Transitivity in the form "u < v ≤ w ⇒ u < w", on exact samples.
    rng = random.Random(1)
    for _ in range(2000):
        vv = Q(rng.randint(1, N), 1000)
        uu = vv - Q(rng.randint(1, N), N)
        ww = vv + Q(rng.randint(0, N), N)
        assert uu < vv <= ww and uu < ww

    # The chain on concrete f and g. g(x) = x² + 2x + 4 at a = 2, L = 12:
    # |g − 12| = |x − 2||x + 4| ≤ 7|x − 2| when |x − 2| < 1, so δ₀(ε) = min(1, ε/7) works for g.
    gx = x**2 + 2 * x + 4
    assert equal(sp.factor(gx - 12), (x - 2) * (x + 4))
    assert equal(sp.Max(sp.Abs(1 + 4), sp.Abs(3 + 4)), 7)        # |x + 4| < 7 on (1, 3)

    def g(v):
        return v * v + 2 * v + 4

    def d_g(e):
        return min(Q(1), e / 7)

    assert implication_holds(g, Q(2), Q(12), d_g, eps_samples(2, breaks=(7,)), seed=2)

    # f agrees with g only on 0 < |x − 2| < r, is undefined at 2, and is g + 100 elsewhere.
    def make_f(rr):
        def f(v):
            if v == 2:
                return None
            return g(v) if abs(v - 2) < rr else g(v) + 100
        return f

    for i, rr in enumerate((Q(1, 1000), Q(1, 10), Q(1, 2), Q(1), Q(5))):
        f = make_f(rr)
        assert implication_holds(f, Q(2), Q(12), lambda e, rr=rr: min(d_g(e), rr),
                                 eps_samples(10 + i, breaks=(7, 7 * rr)), seed=10 + i)
    # The min with r is needed: with r = 1/10 and ε = 7, δ₀ = 1 alone lets in x = 2.5, where f
    # is far from 12.
    f = make_f(Q(1, 10))
    assert d_g(Q(7)) == 1 and abs(Q(5, 2) - 2) < 1 and abs(f(Q(5, 2)) - 12) >= 7

    # A second instance, with a rational g: g(t) = 1/(3 + t) at 6, L = 1/9. On |t − 6| < 1,
    # 3 + t > 8, so |g − 1/9| = |t − 6|/(9(3 + t)) < |t − 6|/72: δ₀(ε) = min(1, 72ε).
    assert equal(1 / (3 + t) - sp.Rational(1, 9), -(t - 6) / (9 * (3 + t)))

    def f2(v):
        if v == 6:
            return None
        return 1 / (3 + v) if abs(v - 6) < Q(1, 2) else Q(-50)

    assert implication_holds(f2, Q(6), Q(1, 9), lambda e: min(min(Q(1), 72 * e), Q(1, 2)),
                             eps_samples(20, breaks=(Q(1, 72), Q(1, 144))), seed=20)


def test_lemma_remarks_example_and_non_example():
    # A whole window is needed: |x|/x = 1 at every x > 0, but it has no limit at 0.
    pos = sp.Symbol("p", positive=True)
    assert equal((sp.Abs(x) / x).subs(x, pos), 1)
    assert equal((sp.Abs(x) / x).subs(x, -pos), -1)
    assert no_real_limit(sp.Abs(x) / x, x, 0)
    # Example: (x² − 1)/(x − 1) = x + 1 for x ≠ 1, both defined on 0 < |x − 1| < 1, limit 2.
    F = (x**2 - 1) / (x - 1)
    assert equal(sp.expand((x - 1) * (x + 1)), x**2 - 1)
    assert equal_on_domain(F, x + 1, x, (0, 1)) and equal_on_domain(F, x + 1, x, (1, 2))
    assert equal(sp.limit(x + 1, x, 1), 2) and limit_is(F, x, 1, 2)
    # Non-example: h(x) = x + 1 for x ≠ 0, h(0) = 0. h(0) = 0 is the value of x at 0, lim x = 0,
    # but lim h = 1 (through x + 1 and the lemma; tested exactly, not with sp.limit on a Piecewise).
    assert equal(sp.limit(x, x, 0), 0) and equal(sp.limit(x + 1, x, 0), 1)

    def h(v):
        return Q(0) if v == 0 else v + 1

    assert h(Q(0)) == 0
    assert implication_holds(h, Q(0), Q(1), lambda e: e, eps_samples(30), seed=30)


# ── The factoring paragraph and the general fact ─────────────────────────────────


def test_factoring_paragraph():
    # r = min(a − α, β − a) is positive when α < a < β, and α ≤ a − r, a + r ≤ β, on each branch.
    lo, hi = sp.symbols("l h_", positive=True)           # a − α = lo, β − a = hi
    s = sp.Symbol("s", nonnegative=True)
    for lo_, hi_ in ((lo, lo + s), (hi + s, hi)):
        rr = sp.Min(lo_, hi_)
        assert rr.is_positive
        alpha, beta = a - lo_, a + hi_
        assert ((a - rr) - alpha).is_nonnegative and (beta - (a + rr)).is_nonnegative

    # Concrete pairs p, q with p(a) = q(a) = 0: dividing by x − a leaves remainder 0, the
    # quotients have degree one less, and where q₁(a) ≠ 0 there is a window on which p/q and
    # p₁/q₁ agree, with limit p₁(a)/q₁(a).
    cases = [
        (x**3 - 8, x**2 - 4, 2),                                  # q₁ = x + 2, other root −2
        (x**2 - x - 2, (x - 2) * (x - 1) * (x + 1), 2),           # q₁ = x² − 1, roots ±1
        (x**3 + x**2 - x - 1, x**2 + 3 * x + 2, -1),              # p has the root −1 twice
        (2 * x**2 - 3 * x - 2, 3 * x**2 - 5 * x - 2, 2),
    ]
    for p, q, av in cases:
        p, q = sp.expand(p), sp.expand(q)
        assert equal(p.subs(x, av), 0) and equal(q.subs(x, av), 0)
        p1, rp = sp.div(p, x - av, x)
        q1, rq = sp.div(q, x - av, x)
        assert equal(rp, 0) and equal(rq, 0)
        assert sp.degree(p1, x) == sp.degree(p, x) - 1 and sp.degree(q1, x) == sp.degree(q, x) - 1
        assert equal(sp.expand((x - av) * p1), p) and equal(sp.expand((x - av) * q1), q)
        if q1.subs(x, av) == 0:
            continue
        roots = [rt for rt in sp.real_roots(q1) if rt != av]
        alpha = max([rt for rt in roots if rt < av], default=av - 10)
        beta = min([rt for rt in roots if rt > av], default=av + 10)
        rr = min(av - alpha, beta - av)
        assert rr > 0 and window_free_of(q, x, av, rr)
        for piece in (sp.Interval.open(av - rr, av), sp.Interval.open(av, av + rr)):
            assert equal_on_domain(p / q, p1 / q1, x, piece)
        assert limit_is(p / q, x, av, p1.subs(x, av) / q1.subs(x, av))


def test_general_fact_difference_quotient():
    # For a generic polynomial of degree d (symbolic coefficients, symbolic a): p(x) − p(a) is
    # divisible by x − a, and the quotient q has q(a) = p'(a) (the derivative is the second route).
    for d in range(0, 7):
        cs = sp.symbols(f"k0:{d + 1}", real=True)
        p = sum(ck * x**i for i, ck in enumerate(cs))
        num = sp.expand(p - p.subs(x, a))
        q, rem = sp.div(num, x - a, x)
        assert equal(rem, 0)
        assert equal(sp.expand((x - a) * q), num)
        assert equal(q.subs(x, a), sp.diff(p, x).subs(x, a))
    # The quotient is a polynomial, so the limit is q(a): concrete random polynomials.
    rng = random.Random(40)
    for _ in range(6):
        deg = rng.randint(1, 5)
        p = sum(rng.randint(-9, 9) * x**i for i in range(deg)) + rng.choice([-3, -1, 1, 2]) * x**deg
        av = sp.Rational(rng.randint(-20, 20), rng.randint(1, 4))
        q, rem = sp.div(sp.expand(p - p.subs(x, av)), x - av, x)
        assert equal(rem, 0)
        assert limit_is((p - p.subs(x, av)) / (x - av), x, av, q.subs(x, av))
    # The cube is the case p(x) = x³, a = 2: q(2) = 12.
    q, _ = sp.div(x**3 - 8, x - 2, x)
    assert equal(q.subs(x, 2), 12)


# ── The rationalising and compound-fraction paragraphs ───────────────────────────


def test_rationalising_paragraph():
    U, V = sp.symbols("U V", nonnegative=True)
    Up = sp.Symbol("U_p", positive=True)
    # (√u − √v)(√u + √v) = u − v for u, v ≥ 0, and (√u)² = u.
    assert equal(sp.expand((sp.sqrt(U) - sp.sqrt(V)) * (sp.sqrt(U) + sp.sqrt(V))), U - V)
    assert equal(sp.sqrt(U) ** 2, U)
    # The conjugate is positive for u > 0: √u ≥ 0, √u ≠ 0 (0² = 0 ≠ u), so √u > 0; plus √v ≥ 0.
    assert sp.sqrt(U).is_nonnegative and sp.sqrt(V).is_nonnegative
    assert sp.sqrt(Up).is_positive and (sp.sqrt(Up) + sp.sqrt(V)).is_positive
    # ... on exact samples too, and u > 0 is needed: u = v = 0 gives the conjugate 0.
    rng = random.Random(50)
    for _ in range(200):
        uv = sp.Rational(rng.randint(1, 10**6), rng.randint(1, 10**4))
        vv = sp.Rational(rng.randint(0, 10**6), rng.randint(1, 10**4))
        conj = sp.sqrt(uv) + sp.sqrt(vv)
        assert (conj > 0) is sp.true
        assert equal((sp.sqrt(uv) - sp.sqrt(vv)) * conj, uv - vv)
    assert equal(sp.sqrt(0) + sp.sqrt(0), 0)
    # Root law with L = 0 and the sign condition: |x| = √(x²) for every real x, x² ≥ 0 everywhere.
    assert equal(sp.sqrt(x**2), sp.Abs(x))
    assert equal(sp.solveset(x**2 < 0, x, sp.S.Reals), sp.S.EmptySet)
    assert equal(sp.limit(x**2, x, 0), 0) and limit_is(sp.Abs(x), x, 0, 0)
    # Without the sign condition: √x is undefined at every x < 0.
    neg = sp.Symbol("q", negative=True)
    assert sp.sqrt(neg).is_real is False


def test_compound_fraction_identity():
    c1, c2 = sp.symbols("c_1 c_2", real=True)
    b, d = sp.symbols("b d", real=True, nonzero=True)
    assert equal(c1 / b - c2 / d, (c1 * d - c2 * b) / (b * d))
    assert (b * d).is_nonzero


# ── Rigorous track ────────────────────────────────────────────────────────────────


def test_rigorous_track_factoring_always_ends():
    rng = random.Random(60)

    def rand_poly(deg, av):
        while True:
            P = sum(rng.randint(-6, 6) * x**i for i in range(deg)) + rng.choice([-2, -1, 1, 3]) * x**deg
            if P.subs(x, av) != 0:
                return sp.expand(P)

    seen = {"j>k": 0, "j=k": 0, "j<k": 0}
    for trial in range(30):
        av = sp.Rational(rng.randint(-6, 6), rng.choice([1, 2, 3]))
        j, k = rng.randint(0, 3), rng.randint(1, 3)
        P, Qp = rand_poly(rng.randint(0, 2), av), rand_poly(rng.randint(0, 2), av)
        p, q = sp.expand((x - av) ** j * P), sp.expand((x - av) ** k * Qp)
        m = sp.degree(q, x)
        # Repeated division ends after exactly k steps, 1 ≤ k ≤ m, with Q(a) ≠ 0; same for p, j.
        kk, Qd = multiplicity_by_division(q, x, av)
        jj, Pd = multiplicity_by_division(p, x, av)
        assert kk == k and 1 <= kk <= m and Qd.subs(x, av) != 0
        assert jj == j and Pd.subs(x, av) != 0
        assert equal(sp.expand((x - av) ** kk * Qd), q) and equal(sp.expand((x - av) ** jj * Pd), p)
        # The window: Q has no root on 0 < |x − a| < r, so neither has q.
        others = [abs(rt - av) for rt in sp.real_roots(sp.Poly(Qd, x))]
        rr = min(others + [sp.Integer(1)])
        assert rr > 0 and window_free_of(q, x, av, rr)
        f = p / q
        if j >= k:
            reduced = (x - av) ** (j - k) * Pd / Qd
            assert equal_on_domain(f, reduced, x, (av, av + rr))
            expected = 0 if j > k else Pd.subs(x, av) / Qd.subs(x, av)
            assert limit_is(f, x, av, expected)
            seen["j>k" if j > k else "j=k"] += 1
        else:
            # (x − a)^(k−j) → 0, and (x − a)^(k−j) f = P/Q on the window, with limit P(a)/Q(a) ≠ 0.
            assert equal(sp.limit((x - av) ** (k - j), x, av), 0)
            assert equal_on_domain((x - av) ** (k - j) * f, Pd / Qd, x, (av, av + rr))
            # (limit_is on the expanded product itself can trip over rounding noise when P/Q is
            # constant: its table error grows from exactly 0. So sp.limit on the product, and
            # limit_is on P/Q, which equals it on the window.)
            assert equal(sp.limit((x - av) ** (k - j) * f, x, av), Pd.subs(x, av) / Qd.subs(x, av))
            assert limit_is(Pd / Qd, x, av, Pd.subs(x, av) / Qd.subs(x, av))
            assert Pd.subs(x, av) / Qd.subs(x, av) != 0
            assert no_real_limit(f, x, av)
            seen["j<k"] += 1
    assert all(v > 0 for v in seen.values()), seen
    # The zero polynomial over q: 0 wherever defined, limit 0.
    assert limit_is(sp.Integer(0) * x / (x - 1), x, 1, 0)


def test_rigorous_track_one_sided_window():
    F = (x - 2) / sp.sqrt(x - 2)
    yp = sp.Symbol("y", positive=True)
    # For x > 2 (x − 2 = y > 0): y/√y = √y.
    assert equal(F.subs(x, 2 + yp), sp.sqrt(yp))
    # Neither function is real at any x < 2.
    assert sp.sqrt(-yp).is_real is False
    # The one-sided limit the page points to: from the right, √(x − 2) → 0.
    assert limit_is(sp.sqrt(x - 2), x, 2, 0, dir="+")


# ── Common mistakes ──────────────────────────────────────────────────────────────


def test_common_mistakes():
    # Cancelling without the lemma: (x² − 9)/(x − 3) is undefined at 3, = x + 3 elsewhere, limit 6.
    F = (x**2 - 9) / (x - 3)
    assert F.subs(x, 3) is sp.nan
    assert equal(sp.expand((x - 3) * (x + 3)), x**2 - 9)
    assert equal_on_domain(F, x + 3, x, (2, 3)) and equal_on_domain(F, x + 3, x, (3, 4))
    assert limit_is(F, x, 3, 6)
    # "0/0 = 1": x²/x → 0, and 3x/x → 3.
    assert limit_is(x**2 / x, x, 0, 0) and limit_is(3 * x / x, x, 0, 3)
    # "√(x²) = x": √(x²)/x is 1 for x > 0 and −1 for x < 0; no limit at 0.
    pos = sp.Symbol("p", positive=True)
    G = sp.sqrt(x**2) / x
    assert equal(G.subs(x, pos), 1) and equal(G.subs(x, -pos), -1)
    assert no_real_limit(G, x, 0)
    # Splitting: the two parts (1/x)/(x − 3) and (1/3)/(x − 3) have numerators → 1/3 and no limit.
    assert equal(sp.limit(1 / x, x, 3), sp.Rational(1, 3))
    assert no_real_limit((1 / x) / (x - 3), x, 3) and no_real_limit(sp.Rational(1, 3) / (x - 3), x, 3)
    # Right: 1/x − 1/3 = (3 − x)/(3x); the quotient is −1/(3x) for x ≠ 0, 3; window 0 < |x − 3| < 3
    # avoids 0; limit −1/9.
    H = (1 / x - sp.Rational(1, 3)) / (x - 3)
    assert equal(1 / x - sp.Rational(1, 3), (3 - x) / (3 * x))
    assert equal_on_domain(H, -1 / (3 * x), x, (0, 3)) and equal_on_domain(H, -1 / (3 * x), x, (3, 6))
    assert window_free_of(3 * x * (x - 3) / (x - 3), x, 3, 3)
    assert limit_is(H, x, 3, -sp.Rational(1, 9))


# ── Examples ─────────────────────────────────────────────────────────────────────


@covers("eg-calc-computing-limits-factor")
def test_eg_calc_computing_limits_factor():
    A = (x**3 - 8) / (x - 2)
    # Step 1: defined at every x ≠ 2; numerator → 0, denominator → 0.
    assert equal(sp.calculus.util.continuous_domain(A, x, sp.S.Reals), sp.S.Reals - sp.FiniteSet(2))
    assert equal(sp.Integer(2) ** 3 - 8, 0) and equal(sp.Integer(2) - 2, 0)
    # Step 2: p(2) = 0, and dividing by x − 2 gives a degree-2 quotient with leading coefficient 1,
    # which is x² + 2x + 4; the displayed multiplication, line by line.
    q, rem = sp.div(x**3 - 8, x - 2, x)
    assert equal(rem, 0) and equal(q, x**2 + 2 * x + 4)
    assert sp.degree(q, x) == 2 and sp.LC(q, x) == 1
    assert equal(sp.expand((x - 2) * (x**2 + 2 * x + 4)), x**3 + 2 * x**2 + 4 * x - 2 * x**2 - 4 * x - 8)
    assert equal(x**3 + 2 * x**2 + 4 * x - 2 * x**2 - 4 * x - 8, x**3 - 8)
    # Step 3: A = x² + 2x + 4 on 0 < |x − 2| < 1.
    g = x**2 + 2 * x + 4
    assert equal_on_domain(A, g, x, (1, 2)) and equal_on_domain(A, g, x, (2, 3))
    # Step 4: g(2) = 4 + 4 + 4 = 12.
    assert equal(g.subs(x, 2), 4 + 4 + 4) and equal(4 + 4 + 4, 12)
    # Step 5 / boxed result.
    assert limit_is(A, x, 2, 12)
    # The general fact with p(x) = x³, a = 2: q(2) = p'(2).
    assert equal(q.subs(x, 2), sp.diff(x**3, x).subs(x, 2))
    # Check: 2.001³ − 8 = 0.012006001, /0.001 = 12.006001.
    assert equal(sp.Rational("2.001") ** 3 - 8, sp.Rational("0.012006001"))
    assert equal(sp.Rational("0.012006001") / sp.Rational("0.001"), sp.Rational("12.006001"))


@covers("eg-calc-computing-limits-conjugate")
def test_eg_calc_computing_limits_conjugate():
    f = (sp.sqrt(1 + x) - 1) / x
    gx = 1 / (sp.sqrt(1 + x) + 1)
    # Step 1: 0 < |x| < 1 ⇒ 1 + x > 0.
    assert equal(sp.solveset(1 + x <= 0, x, sp.Interval.open(-1, 1)), sp.S.EmptySet)
    # Step 2: √(1 + x) → 1 (1 > 0), so the numerator → 0; the denominator → 0.
    assert limit_is(sp.sqrt(1 + x), x, 0, 1) and equal(sp.sqrt(1), 1)
    assert equal(sp.limit(sp.sqrt(1 + x) - 1, x, 0), 0)
    # Step 3: s = √(1 + x) ≥ 0, so s + 1 ≥ 1 > 0; (s − 1)(s + 1) = s² − 1 = x; f = 1/(s + 1).
    sv = sp.Symbol("s", nonnegative=True)
    assert (sv + 1 - 1).is_nonnegative and (sv + 1).is_positive
    assert equal(sp.expand((sv - 1) * (sv + 1)), sv**2 - 1)
    for piece in ((-1, 0), (0, 1)):
        assert equal_on_domain(sp.sqrt(1 + x) ** 2 - 1, x, x, piece)
        assert equal_on_domain(f, ((sp.sqrt(1 + x) - 1) * (sp.sqrt(1 + x) + 1)) / (x * (sp.sqrt(1 + x) + 1)),
                               x, piece)
        assert equal_on_domain(f, gx, x, piece)
    # Step 4: g is defined for x ≥ −1 (its denominator ≥ 1 there); the denominator → 2; g → 1/2.
    assert equal(sp.solveset(sp.sqrt(1 + x) + 1 < 1, x, sp.Interval(-1, sp.oo)), sp.S.EmptySet)
    assert limit_is(sp.sqrt(1 + x) + 1, x, 0, 2)
    assert limit_is(gx, x, 0, sp.Rational(1, 2))
    # Step 5 / boxed result.
    assert limit_is(f, x, 0, sp.Rational(1, 2))
    # The other page's table estimate 0.50 is 1/2 to two decimal places.
    assert rounds_to(sp.Rational(1, 2), "0.50")
    # Check: g(0.001) ≈ 0.499875.
    assert rounds_to(gx.subs(x, sp.Rational("0.001")), "0.499875")
    assert equal(gx.subs(x, sp.Rational("0.001")), f.subs(x, sp.Rational("0.001")))


@covers("eg-calc-computing-limits-same-form")
def test_eg_calc_computing_limits_same_form():
    f1, f2, f3 = x**2 / x, 3 * x / x, x / x**2
    # All three: numerator and denominator → 0.
    for num in (x**2, 3 * x, x):
        assert equal(sp.limit(num, x, 0), 0)
    assert equal(sp.limit(x**2, x, 0), 0)
    # (i) x²/x = x for x ≠ 0, limit 0. (ii) 3x/x = 3, limit 3.
    assert equal_on_domain(f1, x, x, (-1, 0)) and equal_on_domain(f1, x, x, (0, 1))
    assert limit_is(f1, x, 0, 0)
    assert equal_on_domain(f2, 3, x, (-1, 0)) and equal_on_domain(f2, 3, x, (0, 1))
    assert limit_is(f2, x, 0, 3)
    # (iii) x·f(x) = x²/x² = 1 for x ≠ 0, so its limit is 1, while x → 0; f has no limit.
    assert equal_on_domain(x * f3, 1, x, (-1, 0)) and equal_on_domain(x * f3, 1, x, (0, 1))
    assert equal(sp.limit(x, x, 0) * 0, 0)
    assert no_real_limit(f3, x, 0)
    # Replacing 3 by any c gives the limit c.
    assert equal(sp.limit(c * x / x, x, 0), c)
    # Check: at 0.01: 0.01, 3, 100; at 0.001, (iii) is 1000.
    h1 = sp.Rational("0.01")
    assert equal(f1.subs(x, h1), sp.Rational("0.0001") / h1) and equal(f1.subs(x, h1), sp.Rational("0.01"))
    assert equal(f2.subs(x, h1), sp.Rational("0.03") / h1) and equal(f2.subs(x, h1), 3)
    assert equal(f3.subs(x, h1), h1 / sp.Rational("0.0001")) and equal(f3.subs(x, h1), 100)
    assert equal(f3.subs(x, sp.Rational("0.001")), 1000)


@covers("eg-calc-computing-limits-resistors")
def test_eg_calc_computing_limits_resistors():
    R = 3 * t / (3 + t)
    f = (R - 2) / (t - 6)
    assert equal(R.subs(t, 6), sp.Rational(18, 9)) and equal(sp.Rational(18, 9), 2)
    # Step 1: 0 < |t − 6| < 6 ⇒ 0 < t < 12: inside t > 0.
    assert equal(sp.Interval.open(0, 12) - sp.FiniteSet(6), punctured_window_set(6, 6))
    # Step 2: R → 2 (denominator 9 ≠ 0 at 6), so the numerator → 0; the denominator → 0.
    assert equal((3 + t).subs(t, 6), 9) and limit_is(R, t, 6, 2)
    # Step 3: R − 2 = (3t − 2(3 + t))/(3 + t) = (t − 6)/(3 + t) for t > 0.
    assert equal_on_domain(R - 2, (3 * t - 2 * (3 + t)) / (3 + t), t, (0, 100))
    assert equal((3 * t - 2 * (3 + t)) / (3 + t), (t - 6) / (3 + t))
    # Step 4: f = 1/(3 + t) on the window.
    g = 1 / (3 + t)
    assert equal_on_domain(f, (t - 6) / ((3 + t) * (t - 6)), t, (0, 6))
    assert equal_on_domain(f, g, t, (0, 6)) and equal_on_domain(f, g, t, (6, 12))
    # Step 5 / 6 / boxed result.
    assert equal(g.subs(t, 6), sp.Rational(1, 9))
    assert limit_is(f, t, 6, sp.Rational(1, 9))
    # Check: R(6.01) = 18.03/9.01 ≈ 2.0011099; f(6.01) ≈ 0.110988 = g(6.01) = 1/9.01; 1/9 ≈ 0.111111.
    tv = sp.Rational("6.01")
    assert equal(R.subs(t, tv), sp.Rational("18.03") / sp.Rational("9.01"))
    assert rounds_to(R.subs(t, tv), "2.0011099")
    assert rounds_to(f.subs(t, tv), "0.110988") and equal(f.subs(t, tv), g.subs(t, tv))
    assert equal(g.subs(t, tv), 1 / sp.Rational("9.01"))
    assert rounds_to(sp.Rational(1, 9), "0.111111")


# ── Exercises ────────────────────────────────────────────────────────────────────


@covers("exr-calc-computing-limits-factor-quadratic")
def test_exr_calc_computing_limits_factor_quadratic():
    F = (x**2 + 5 * x + 6) / (x + 2)
    # The solution's steps: numerator 4 − 10 + 6 = 0 at −2; (x + 2)(x + 3); window r = 1.
    assert equal((x**2 + 5 * x + 6).subs(x, -2), 0)
    reduced, rem = sp.div(x**2 + 5 * x + 6, x + 2, x)
    assert equal(rem, 0) and equal(reduced, x + 3)
    assert equal_on_domain(F, reduced, x, (-3, -2)) and equal_on_domain(F, reduced, x, (-2, -1))
    expected = reduced.subs(x, -2)
    assert limit_is(F, x, -2, expected)
    assert equal(answer("exr-calc-computing-limits-factor-quadratic"), expected)


@covers("exr-calc-computing-limits-factor-both")
def test_exr_calc_computing_limits_factor_both():
    F = (x**2 - x - 2) / (x**2 - 4)
    assert equal(sp.expand((x - 2) * (x + 1)), x**2 - x - 2)
    assert equal(sp.expand((x - 2) * (x + 2)), x**2 - 4)
    # The denominator's roots are ±2; the window 0 < |x − 2| < 1 avoids −2.
    assert equal(sp.solveset(sp.Eq(x**2 - 4, 0), x, sp.S.Reals), sp.FiniteSet(-2, 2))
    assert window_free_of(x**2 - 4, x, 2, 1)
    G = (x + 1) / (x + 2)
    assert equal_on_domain(F, G, x, (1, 2)) and equal_on_domain(F, G, x, (2, 3))
    expected = G.subs(x, 2)
    assert limit_is(F, x, 2, expected)
    assert equal(answer("exr-calc-computing-limits-factor-both"), expected)


@covers("exr-calc-computing-limits-conjugate")
def test_exr_calc_computing_limits_conjugate():
    F = (sp.sqrt(x + 4) - 2) / x
    G = 1 / (sp.sqrt(x + 4) + 2)
    # Window r = 4: x + 4 > 0 there; (s − 2)(s + 2) = s² − 4 = x; F = G on the window.
    assert equal(sp.solveset(x + 4 <= 0, x, sp.Interval.open(-4, 4)), sp.S.EmptySet)
    assert equal_on_domain(sp.sqrt(x + 4) ** 2 - 4, x, x, (-4, 4))
    assert equal_on_domain(F, G, x, (-4, 0)) and equal_on_domain(F, G, x, (0, 4))
    assert limit_is(sp.sqrt(x + 4) + 2, x, 0, 4)
    expected = sp.limit(F, x, 0)
    assert equal(expected, G.subs(x, 0))           # second route: the rewritten g at 0
    assert limit_is(F, x, 0, expected)
    assert equal(answer("exr-calc-computing-limits-conjugate"), expected)


@covers("exr-calc-computing-limits-compound")
def test_exr_calc_computing_limits_compound():
    F = (1 / x - sp.Rational(1, 2)) / (x - 2)
    # 1/x − 1/2 = (2 − x)/(2x); F = −1/(2x) on 0 < |x − 2| < 2 (which avoids 0).
    assert equal(1 / x - sp.Rational(1, 2), (2 - x) / (2 * x))
    assert equal(sp.Interval.open(0, 4) - sp.FiniteSet(2), punctured_window_set(2, 2))
    G = -1 / (2 * x)
    assert equal_on_domain(F, G, x, (0, 2)) and equal_on_domain(F, G, x, (2, 4))
    expected = G.subs(x, 2)
    assert limit_is(F, x, 2, expected)
    # Second route: the derivative of 1/x at 2.
    assert equal(expected, sp.diff(1 / x, x).subs(x, 2))
    assert equal(answer("exr-calc-computing-limits-compound"), expected)


@covers("exr-calc-computing-limits-factor-twice")
def test_exr_calc_computing_limits_factor_twice():
    p, q = x**3 - 3 * x + 2, x**2 - 2 * x + 1
    # One division by x − 1 leaves the form 0/0; the second ends it (q = (x − 1)²).
    p1, r1 = sp.div(p, x - 1, x)
    assert equal(r1, 0) and equal(p1, x**2 + x - 2)
    assert equal(p1.subs(x, 1), 0)
    assert equal(sp.expand((x - 1) * (x + 2)), x**2 + x - 2)
    assert equal(sp.expand((x - 1) ** 2 * (x + 2)), p) and equal(sp.expand((x - 1) ** 2), q)
    j, P = multiplicity_by_division(p, x, 1)
    k, Qd = multiplicity_by_division(q, x, 1)
    assert j == k == 2 and equal(Qd, 1)
    assert equal_on_domain(p / q, x + 2, x, (0, 1)) and equal_on_domain(p / q, x + 2, x, (1, 2))
    expected = P.subs(x, 1) / Qd.subs(x, 1)
    assert limit_is(p / q, x, 1, expected)
    assert equal(answer("exr-calc-computing-limits-factor-twice"), expected)


@covers("exr-calc-computing-limits-root-denominator")
def test_exr_calc_computing_limits_root_denominator():
    F = (x - 9) / (sp.sqrt(x) - 3)
    # On the window 0 < |x − 9| < 9 (so 0 < x < 18): √x is defined, √x ≠ 3, and
    # x − 9 = (√x − 3)(√x + 3), so F = √x + 3.
    assert equal(sp.solveset(sp.Eq(sp.sqrt(x), 3), x, sp.Interval.open(0, 18)), sp.FiniteSet(9))
    assert equal_on_domain((sp.sqrt(x) - 3) * (sp.sqrt(x) + 3), x - 9, x, (0, 18))
    assert equal_on_domain(F, sp.sqrt(x) + 3, x, (0, 9)) and equal_on_domain(F, sp.sqrt(x) + 3, x, (9, 18))
    assert limit_is(sp.sqrt(x), x, 9, 3)
    expected = (sp.sqrt(x) + 3).subs(x, 9)
    assert limit_is(F, x, 9, expected)
    # Second route: 1/(d√x/dx at 9).
    assert equal(expected, 1 / sp.diff(sp.sqrt(x), x).subs(x, 9))
    assert equal(answer("exr-calc-computing-limits-root-denominator"), expected)


@covers("exr-calc-computing-limits-abs-sqrt")
def test_exr_calc_computing_limits_abs_sqrt():
    assert answer_type("exr-calc-computing-limits-abs-sqrt") == "bool"
    F = sp.sqrt(x**2) / x
    pos = sp.Symbol("p", positive=True)
    # √(x²) = |x|, so F = 1 for x > 0 and −1 for x < 0; the one-sided limits differ.
    assert equal(sp.sqrt(x**2), sp.Abs(x))
    assert equal(F.subs(x, pos), 1) and equal(F.subs(x, -pos), -1)
    assert limit_is(F, x, 0, 1, dir="+") and limit_is(F, x, 0, -1, dir="-")
    # No L within 1 of both 1 and −1: the solution's triangle-inequality step.
    L = sp.Symbol("L", real=True)
    good = sp.Intersection(sp.solveset(sp.Abs(1 - L) < 1, L, sp.S.Reals),
                           sp.solveset(sp.Abs(-1 - L) < 1, L, sp.S.Reals))
    assert equal(good, sp.S.EmptySet)
    assert equal(sp.Abs(L - (-1)), sp.Abs(-1 - L)) and equal(sp.Abs(1 - (-1)), 2)
    exists = sp.true if not no_real_limit(F, x, 0) else sp.false
    assert equal(answer("exr-calc-computing-limits-abs-sqrt"), exists)


@covers("exr-calc-computing-limits-abs-denominator")
def test_exr_calc_computing_limits_abs_denominator():
    F = (sp.sqrt(4 + x**2) - 2) / sp.Abs(x)
    G = sp.Abs(x) / (sp.sqrt(4 + x**2) + 2)
    # 4 + x² ≥ 4 > 0; (s − 2)(s + 2) = s² − 4 = x² = |x|²; F = G at every x ≠ 0.
    assert equal(sp.solveset(4 + x**2 < 4, x, sp.S.Reals), sp.S.EmptySet)
    assert equal(sp.expand((sp.sqrt(4 + x**2) - 2) * (sp.sqrt(4 + x**2) + 2)), x**2)
    assert equal(x**2, sp.Abs(x) ** 2)
    assert equal_on_domain(F, G, x, (-5, 0)) and equal_on_domain(F, G, x, (0, 5))
    # Where the sign condition is used: |x| = √(x²) → 0 with x² ≥ 0; the denominator → 4.
    assert limit_is(sp.Abs(x), x, 0, 0) and limit_is(sp.sqrt(4 + x**2) + 2, x, 0, 4)
    expected = sp.limit(G, x, 0)
    assert limit_is(F, x, 0, expected)
    assert equal(answer("exr-calc-computing-limits-abs-denominator"), expected)


@covers("exr-calc-computing-limits-lens")
def test_exr_calc_computing_limits_lens():
    v = 5 * u / (u - 5)
    assert equal(v.subs(u, 15), sp.Rational(15, 2))
    F = (v - sp.Rational(15, 2)) / (u - 15)
    # Window 0 < |u − 15| < 10, i.e. 5 < u < 25 without 15.
    assert equal(sp.Interval.open(5, 25) - sp.FiniteSet(15), punctured_window_set(15, 10))
    # The solution's displayed steps, for u > 5.
    assert equal_on_domain(v - sp.Rational(15, 2), (10 * u - 15 * (u - 5)) / (2 * (u - 5)), u, (5, 100))
    assert equal((10 * u - 15 * (u - 5)) / (2 * (u - 5)), (75 - 5 * u) / (2 * (u - 5)))
    assert equal((75 - 5 * u) / (2 * (u - 5)), -5 * (u - 15) / (2 * (u - 5)))
    G = -5 / (2 * (u - 5))
    assert equal_on_domain(F, G, u, (5, 15)) and equal_on_domain(F, G, u, (15, 25))
    expected = G.subs(u, 15)
    assert equal(expected, -sp.Rational(5, 20))
    assert limit_is(F, u, 15, expected)
    # Second route: v'(15).
    assert equal(expected, sp.diff(v, u).subs(u, 15))
    # "The image moves towards the lens": the rate is negative.
    assert expected < 0
    assert equal(answer("exr-calc-computing-limits-lens"), expected)


@covers("exr-calc-computing-limits-power")
def test_exr_calc_computing_limits_power():
    ans = answer("exr-calc-computing-limits-power")
    m = sp.Symbol("m", integer=True, positive=True)
    k = sp.Symbol("k", integer=True, nonnegative=True)
    # Symbolically, for a positive integer m: s(x) = Σ_{k=0}^{m−1} x^k has s(1) = m (m ones), and
    # (x − 1)s(x) = x^m − 1 (the telescoping sum: x·s − s), checked as Σ x^(k+1) − Σ x^k.
    s_sum = sp.Sum(x**k, (k, 0, m - 1))
    assert equal(s_sum.subs(x, 1).doit(), m)
    tele = sp.Sum(x ** (k + 1), (k, 0, m - 1)) - s_sum
    assert equal(sp.Sum(x ** (k + 1), (k, 0, m - 1)).doit().subs(x, 2) - s_sum.doit().subs(x, 2),
                 sp.Integer(2) ** m - 1)
    assert equal(tele.subs(x, 1).doit(), 0) and equal((x**m - 1).subs(x, 1), 0)
    # The limit, symbolically in m, by two routes: sp.limit, and the derivative of x^m at 1.
    lim_m = sp.limit((x**m - 1) / (x - 1), x, 1)
    assert equal(lim_m, m)
    assert equal(sp.diff(x**m, x).subs(x, 1), m)
    assert equal(ans.subs(n, m), lim_m)
    # For several n: the factorisation, the quotient, its value at 1, and the limit (limit_is).
    for nv in list(range(1, 13)) + [17, 25]:
        s_n = sum(x**i for i in range(nv))
        assert equal(sp.expand((x - 1) * s_n), x**nv - 1)
        quo, rem = sp.div(x**nv - 1, x - 1, x)
        assert equal(rem, 0) and equal(quo, s_n)
        assert equal(s_n.subs(x, 1), nv)
        assert limit_is((x**nv - 1) / (x - 1), x, 1, nv)
        assert equal(ans.subs(n, nv), nv)
    # n = 3: the limit of (x³ − 1)/(x − 1) is 3.
    assert limit_is((x**3 - 1) / (x - 1), x, 1, 3)


@covers("exr-calc-computing-limits-numerator-zero")
def test_exr_calc_computing_limits_numerator_zero():
    # A manual answer (a proof): its key claims are checked here; it counts as covered only
    # through a reviewer's note in maths.manual_checked.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-computing-limits-numerator-zero")
    fx = sp.Symbol("f_x", real=True)
    xa = sp.Symbol("xa", real=True, nonzero=True)          # x − a ≠ 0
    # (x − a)·(f(x)/(x − a)) = f(x) for x ≠ a, and x − a → 0, so the product law gives 0·M = 0.
    assert equal(xa * (fx / xa), fx)
    assert equal(sp.limit(x - a, x, a), 0)
    M = sp.Symbol("M", real=True)
    assert equal(0 * M, 0)
    # Instances: f/(x − a) has a limit, and f → 0.
    instances = [(x**2 - 4, 2), (sp.sqrt(1 + x) - 1, 0), (x**3 - 3 * x + 2, 1), (sp.Abs(x) * x, 0)]
    for fexpr, av in instances:
        assert sp.limit(fexpr / (x - av), x, av).is_finite
        assert limit_is(fexpr, x, av, 0)
    # The contrapositive ("of the form c/0 with c ≠ 0" has no limit): f → 1 or 1/3, no limit.
    assert equal(sp.limit(x**2 - 3, x, 2), 1) and no_real_limit((x**2 - 3) / (x - 2), x, 2)
    assert no_real_limit(1 / x, x, 0)
    # The window: where h = f/(x − a) is defined (x ≠ a), f is defined; e.g. f = √(1 + x), a = 0:
    # h is defined on 0 < |x| < 1 and so is f.
    assert equal(sp.solveset(1 + x < 0, x, sp.Interval.open(-1, 1)), sp.S.EmptySet)


@covers("exr-calc-computing-limits-find-constant")
def test_exr_calc_computing_limits_find_constant():
    p = x**2 + c * x - 10
    # (a) The limit can exist only if p(2) = 0 (the numerator-zero argument): p(2) = 2c − 6.
    assert equal(p.subs(x, 2), 2 * c - 6)
    cs = sp.solveset(sp.Eq(p.subs(x, 2), 0), c, sp.S.Reals)
    assert isinstance(cs, sp.FiniteSet) and len(cs) == 1
    (cv,) = cs
    # For other c the limit does not exist (sampled c, with p(2) ≠ 0).
    for other in (-5, 0, 1, sp.Rational(5, 2), sp.Rational(7, 2), 10):
        assert not equal(p.subs({c: other, x: 2}), 0)
        assert no_real_limit(p.subs(c, other) / (x - 2), x, 2)
    # And cv works: x² + cv·x − 10 = (x − 2)·quotient.
    pc = p.subs(c, cv)
    quo, rem = sp.div(pc, x - 2, x)
    assert equal(rem, 0)
    assert equal(sp.expand((x - 2) * (x + 5)), x**2 + 3 * x - 10)
    assert equal_on_domain(pc / (x - 2), quo, x, (1, 2)) and equal_on_domain(pc / (x - 2), quo, x, (2, 3))
    lim = quo.subs(x, 2)
    assert limit_is(pc / (x - 2), x, 2, lim)
    # Second route for (b): the derivative of the numerator at 2.
    assert equal(lim, sp.diff(pc, x).subs(x, 2))
    assert equal(answer("exr-calc-computing-limits-find-constant"), (cv, lim))
