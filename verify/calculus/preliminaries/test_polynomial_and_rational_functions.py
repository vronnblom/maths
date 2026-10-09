"""Verification tests for content/calculus/preliminaries/polynomial-and-rational-functions.md (calc-polynomial-rational).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Expected values are
derived independently of the page's answers and solutions:

- quotients and remainders come from sp.div, and each one is checked three ways: f = g q + r
  after expanding, r is zero or of lower degree than g, and the quotient and remainder printed
  on the page agree with sp.div's;
- factorisations are checked by expanding the page's product back (sp.expand) and against
  sp.factor; root sets come from sp.roots (with multiplicities) and are cross-checked with
  solveset over the reals; no polynomial is credited with more distinct roots than its degree;
- the factor theorem is checked as "p(a) = 0 exactly when the remainder of p divided by x - a is
  0", with the remainder from sp.rem, a different route from substituting a;
- domains are R minus the real zeros of the denominator as written, before any cancellation
  (sp.fraction of the unsimplified expression, which SymPy does not cancel on construction);
- every sign statement is checked against solveset of f > 0 and f < 0 over the domain, and
  pointwise, with exact arithmetic, at each marked number, just either side of it (± 10^-6), at
  a point inside each interval, and on a grid: a point is in the printed set exactly when the
  inequality holds there. That catches an open/closed endpoint mix-up even if solveset were
  wrong.
"""

import itertools
import random

import pytest
import sympy as sp

from mathcheck import ManualAnswer, answer, answer_type, covers, equal, limit_is, t, x

R = sp.S.Reals
oo = sp.oo
EPS = sp.Rational(1, 10**6)
GRID = [sp.Rational(k, 8) for k in range(-80, 81)]  # -10 … 10 in steps of 1/8


# ── Helpers ───────────────────────────────────────────────────────────────────


def poly(expr, var=x):
    return sp.Poly(sp.expand(expr), var)


def check_division(f, g, q_page, r_page, var=x):
    """sp.div gives the quotient and remainder of f by g; the page's q and r must be the same,
    f = g q + r must hold after expanding, and r must be zero or of lower degree than g."""
    q, r = sp.div(sp.expand(f), sp.expand(g), var)
    assert equal(sp.expand(q - q_page), 0), f"quotient: SymPy {q}, page {q_page}"
    assert equal(sp.expand(r - r_page), 0), f"remainder: SymPy {r}, page {r_page}"
    assert equal(sp.expand(g * q_page + r_page - f), 0)
    if sp.expand(r_page) != 0:
        assert poly(r_page, var).degree() < poly(g, var).degree()


def factor_theorem_iff(p, a, var=x):
    """p(a) = 0 exactly when x - a divides p. The left side by substitution, the right by the
    remainder of sp.rem (a different computation). Returns whether a is a root."""
    is_root = sp.expand(p).subs(var, a) == 0
    divides = sp.rem(sp.expand(p), var - a, var) == 0
    assert is_root == divides, f"p = {p}, a = {a}: p(a) = 0 is {is_root}, (x - a) | p is {divides}"
    return is_root


def real_roots(p, var=x):
    """The real roots of p with their multiplicities, from sp.roots, cross-checked against
    solveset over R (same set of distinct roots) and against the degree bound."""
    P = poly(p, var)
    rts = {r_: m for r_, m in sp.roots(P).items() if r_.is_real}
    assert sum(sp.roots(P).values()) == P.degree(), f"sp.roots did not find every root of {p}"
    assert equal(sp.FiniteSet(*rts), sp.solveset(sp.expand(p), var, R))
    assert len(rts) <= P.degree()  # thm-calc-polynomial-roots-bound
    return rts


def domain(f, var=x):
    """R minus the real zeros of the denominator of f as written (no cancellation)."""
    _num, den = sp.fraction(f)
    return sp.Complement(R, sp.solveset(den, var, R))


def value(f, v, var=x):
    """f(v) exactly, or None where f is undefined (a zero denominator in f as written)."""
    _num, den = sp.fraction(f)
    if den.subs(var, v) == 0:
        return None
    return sp.nsimplify(f.subs(var, v))


def holds(rel, v, var=x):
    """The relation holds at v; where a side is undefined it does not."""
    lhs, rhs = value(rel.lhs, v, var), value(rel.rhs, v, var)
    if lhs is None or rhs is None:
        return False
    return bool(rel.func(lhs, rhs))


def marked_points(S, extra=()):
    extra = [sp.sympify(e) for e in extra]
    pts = set(GRID) | set(extra)
    for e in list(S.boundary) + extra:
        if e.is_finite:
            pts |= {e, e - EPS, e + EPS}
    return pts


def spot_check(S, rel, var=x, extra=()):
    """Pointwise: at each endpoint of S, ± 10^-6 either side, the extra points and the grid, v is
    in S exactly when rel holds at v."""
    for v in marked_points(S, extra):
        assert bool(S.contains(v)) == holds(rel, v, var), (
            f"{var} = {v}: the set says {'in' if S.contains(v) else 'out'}, {rel} "
            f"{'holds' if holds(rel, v, var) else 'fails'}")


def solve_ineq(rel, var=x, over=R):
    """solveset over `over`, intersected with the domain of both sides as written."""
    S = sp.solveset(rel, var, over)
    assert not S.has(sp.ConditionSet), f"SymPy cannot solve {rel}"
    return sp.Intersection(S, domain(rel.lhs, var), domain(rel.rhs, var))


def check_sign_chart(f, positive, negative, zeros, undefined, cuts, var=x):
    """The page's sign statements for f, against solveset and pointwise. `cuts` are the marked
    numbers; a point inside each open interval between them is checked too."""
    assert equal(domain(f, var), sp.Complement(R, sp.FiniteSet(*undefined)))
    S_pos = solve_ineq(sp.StrictGreaterThan(f, 0), var)
    S_neg = solve_ineq(sp.StrictLessThan(f, 0), var)
    S_zero = sp.Intersection(sp.solveset(sp.fraction(f)[0], var, R), domain(f, var))
    assert equal(S_pos, positive), f"f > 0: SymPy {S_pos}, page {positive}"
    assert equal(S_neg, negative), f"f < 0: SymPy {S_neg}, page {negative}"
    assert equal(S_zero, sp.FiniteSet(*zeros))
    cuts = sorted(sp.sympify(v) for v in cuts)
    inside = [cuts[0] - 1, cuts[-1] + 1] + [(p + q) / 2 for p, q in zip(cuts, cuts[1:])]
    spot_check(positive, sp.StrictGreaterThan(f, 0), var, extra=inside + cuts)
    spot_check(negative, sp.StrictLessThan(f, 0), var, extra=inside + cuts)
    for v in cuts:
        val = value(f, v, var)
        if v in undefined:
            assert val is None
        else:
            assert val is not None and (val == 0) == (v in zeros)


def negatives_at(factors, v, var=x):
    """How many of the factors are negative at v."""
    return sum(1 for fac in factors if sp.sympify(fac).subs(var, v) < 0)


# ── Unlabelled claims in the text (not coverage, but checked) ────────────────


def test_why_this_matters():
    # x^3 - 8 = (x - 2)(x^2 + 2x + 4), and the average rate (x^3 - 8)/(x - 2) is 0/0 at 2.
    assert equal(sp.expand((x - 2) * (x**2 + 2 * x + 4)), x**3 - 8)
    assert factor_theorem_iff(x**3 - 8, 2)
    check_division(x**3 - 8, x - 2, x**2 + 2 * x + 4, 0)
    # For x != 2 it equals x^2 + 2x + 4, which is 12 at 2; and the limit at 2 is 12.
    assert equal(sp.cancel((x**3 - 8) / (x - 2)), x**2 + 2 * x + 4)
    assert equal((x**2 + 2 * x + 4).subs(x, 2), 12)
    assert limit_is((x**3 - 8) / (x - 2), x, 2, 12)
    # The page's example after the factor theorem: for p = x^3, a = 2, the proof's q_3 is this.
    a_ = sp.Integer(2)
    assert equal(sp.expand(x**2 + x * a_ + a_**2), x**2 + 2 * x + 4)


def test_definition_examples():
    p = 3 * x**4 - x + 7
    P = poly(p)
    assert P.degree() == 4 and P.LC() == 3 and P.coeff_monomial(1) == 7
    assert equal(sp.expand((x - 1) * (x + 2)), x**2 + x - 2)
    assert poly(x**2 + x - 2).degree() == 2
    assert real_roots(x**2 + x - 2) == {1: 1, -2: 1}
    assert real_roots(x**2 - 2) == {sp.sqrt(2): 1, -sp.sqrt(2): 1}
    # Non-example: 1/x is undefined at 0 (a polynomial is defined there), sqrt(x) has domain [0, oo).
    assert value(1 / x, 0) is None
    assert equal(sp.calculus.util.continuous_domain(sp.sqrt(x), x, R), sp.Interval(0, oo))
    # Rational-function example: (x + 1)/(x^2 - 4), x^2 - 4 = (x - 2)(x + 2), domain R \ {-2, 2}.
    assert equal(sp.expand((x - 2) * (x + 2)), x**2 - 4)
    assert equal(domain((x + 1) / (x**2 - 4)),
                 sp.Union(sp.Interval.open(-oo, -2), sp.Interval.open(-2, 2), sp.Interval.open(2, oo)))
    # Non-example: sqrt(x)/(x + 1) has natural domain [0, oo), which leaves out infinitely many numbers.
    assert equal(sp.calculus.util.continuous_domain(sp.sqrt(x) / (x + 1), x, R), sp.Interval(0, oo))


def test_degree_of_a_product():
    # Degree m times degree k gives degree m + k, with leading coefficient ab, on random exact
    # examples (a sampled check, not a proof).
    rng = random.Random(1)
    for _ in range(200):
        m, k = rng.randint(0, 5), rng.randint(0, 5)
        cf = [sp.Rational(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(m + k + 2)]
        a_, b_ = rng.choice([-3, -1, 2, sp.Rational(1, 2)]), rng.choice([-2, 1, 5, sp.Rational(-3, 7)])
        f = a_ * x**m + sum(cf[i] * x**i for i in range(m))
        g = b_ * x**k + sum(cf[m + 1 + i] * x**i for i in range(k))
        Pfg = poly(f * g)
        assert Pfg.degree() == m + k and Pfg.LC() == a_ * b_
        assert sp.expand(f * g) != 0  # "a product of two non-zero polynomials is not zero"
    # The proof: among 0 <= i <= m, 0 <= j <= k, only (i, j) = (m, k) has i + j = m + k.
    for m in range(6):
        for k in range(6):
            top = [(i, j) for i in range(m + 1) for j in range(k + 1) if i + j >= m + k]
            assert top == [(m, k)]
    # "In words": (3x^2 + 1)(x - 5) has degree 3 and leading coefficient 3.
    P = poly((3 * x**2 + 1) * (x - 5))
    assert P.degree() == 3 and P.LC() == 3


def test_factor_theorem_statement():
    # (a) on exact examples: x - a divides p(x) - p(a), the quotient has degree n - 1 and the
    # leading coefficient of p; and the proof's construction q = sum c_k q_k gives that quotient.
    a_ = sp.Symbol("a", real=True)
    for k_ in range(1, 9):
        qk = sum(x**j * a_**(k_ - 1 - j) for j in range(k_))
        assert equal(sp.expand((x - a_) * qk), x**k_ - a_**k_)
    rng = random.Random(2)
    for _ in range(100):
        n_ = rng.randint(1, 6)
        cs = [sp.Integer(rng.randint(-9, 9)) for _ in range(n_)] + [sp.Integer(rng.choice([-4, -1, 1, 3, 7]))]
        p = sum(cs[i] * x**i for i in range(n_ + 1))
        av = sp.Rational(rng.randint(-12, 12), rng.randint(1, 3))
        q, rem = sp.div(p - p.subs(x, av), x - av, x)
        assert rem == 0
        Q = poly(q)
        assert Q.degree() == n_ - 1 and Q.LC() == cs[n_]
        construction = sum(cs[k_] * sum(x**j * av**(k_ - 1 - j) for j in range(k_)) for k_ in range(1, n_ + 1))
        assert equal(sp.expand(construction - q), 0)
        # (a), the quotient form: (p(x) - p(a))/(x - a) = q(x) for x != a. Symbolically by
        # cancelling, and exactly at rational x != a, including x close to a; at x = a the
        # quotient has the denominator 0.
        dq = (p - p.subs(x, av)) / (x - av)
        assert equal(sp.cancel(dq) - q, 0)
        for xv in (av - 1, av + sp.Rational(1, 7), av - EPS, av + EPS, sp.Integer(0), sp.Integer(5)):
            if xv != av:
                assert equal(dq.subs(x, xv), q.subs(x, xv))
        assert (x - av).subs(x, av) == 0
        # (b): p(a) = 0 exactly when x - a divides p, on a root and a non-root.
        factor_theorem_iff(p, av)
        assert factor_theorem_iff(p - p.subs(x, av), av)
    # The remainder on division by x - a is p(a) (the "In words" after the division theorem).
    for p in (x**5 - 3 * x + 2, 2 * x**3 - 5 * x + 1, x**4 - 3 * x**3 + x + 6):
        for av in (-2, -1, 0, sp.Rational(1, 2), 3):
            assert equal(sp.rem(p, x - av, x), p.subs(x, av))


def test_roots_bound_and_zero_polynomial():
    # Distinct real roots never exceed the degree, on examples with repeated and non-real roots.
    for p in ((x - 1)**2 * (x + 2), x**2 + 1, (x - 1)**2, x**3 - 3 * x, x**4 - 5 * x**2 + 4,
              (x - 1)**3 * (x**2 + 1), x**5 - x):
        real_roots(p)
    # The zero polynomial: every real number is a root (sampled).
    for v in GRID:
        assert sp.Integer(0).subs(x, v) == 0


def test_cor_calc_polynomial_identity():
    # Two polynomials of degree <= n agreeing at n + 1 points have the same coefficients:
    # the coefficients solving the n + 1 interpolation equations are unique (Vandermonde
    # determinant non-zero for distinct nodes), checked for n = 0 … 5 on random distinct nodes.
    rng = random.Random(3)
    for n_ in range(6):
        nodes = rng.sample(range(-10, 11), n_ + 1)
        V = sp.Matrix([[sp.Integer(xi)**j for j in range(n_ + 1)] for xi in nodes])
        assert V.det() != 0
        cs = sp.symbols(f"c0:{n_ + 1}")
        target = [sp.Integer(rng.randint(-9, 9)) for _ in nodes]
        sol = sp.solve([sum(cs[j] * xi**j for j in range(n_ + 1)) - yv for xi, yv in zip(nodes, target)],
                       cs, dict=True)
        assert len(sol) == 1 and all(sol[0][c_].is_number for c_ in cs)
    # Agreement at only n points is not enough: p and p + (x - x_1)…(x - x_n) agree at x_1 … x_n
    # and differ elsewhere (why the corollary asks for n + 1).
    p = x**2 + 1
    p2 = p + (x - 1) * (x - 2)
    assert p.subs(x, 1) == p2.subs(x, 1) and p.subs(x, 2) == p2.subs(x, 2)
    assert p.subs(x, 0) != p2.subs(x, 0)
    # "Compare coefficients": ax^2 + bx + c = 2x^2 - 5 for every x gives a = 2, b = 0, c = -5,
    # here from the values at three points only.
    A, B, C = sp.symbols("A B C")
    sol = sp.solve([A * v**2 + B * v + C - (2 * v**2 - 5) for v in (-1, 0, 1)], [A, B, C], dict=True)
    assert sol == [{A: 2, B: 0, C: -5}]


def test_prop_calc_sign_rules():
    rng = random.Random(4)
    vals = [sp.Rational(rng.randint(-50, 50), rng.randint(1, 7)) for _ in range(60)] + [sp.Integer(0)]
    # The part letters follow the statement as it now is: (a) zero product and zero quotient,
    # (b) the sign of x - t, (c) two non-zero numbers, (d) counting negative factors.
    for u_, v_ in itertools.product(vals, repeat=2):
        prod = u_ * v_
        # (a): uv = 0 exactly when u = 0 or v = 0; for v != 0, u/v = 0 exactly when u = 0.
        assert (prod == 0) == (u_ == 0 or v_ == 0)
        if v_ != 0:
            assert (u_ / v_ == 0) == (u_ == 0)
        # (b), with x = u, t = v.
        assert sp.sign(u_ - v_) == (-1 if u_ < v_ else 0 if u_ == v_ else 1)
        # (c): for u, v != 0, uv and u/v are positive for equal signs, negative otherwise;
        # 1/v has the sign of v.
        if u_ != 0 and v_ != 0:
            same = (u_ > 0) == (v_ > 0)
            assert (prod > 0) == same and (prod < 0) == (not same)
            assert (u_ / v_ > 0) == same and (u_ / v_ < 0) == (not same)
            assert sp.sign(1 / v_) == sp.sign(v_)
            # The proof's step for v < 0: 1/(-v) > 0 and 1/(-v) + 1/v = 0.
            if v_ < 0:
                assert 1 / (-v_) > 0 and 1 / (-v_) + 1 / v_ == 0
    # (c), "in particular": u^2 > 0 for u != 0, u^2 >= 0 for every u, and 1 > 0. Sampled on the
    # values above, and symbolically: u^2 < 0 has no real solution, u^2 = 0 only u = 0.
    for u_ in vals:
        assert u_**2 >= 0 and (u_**2 > 0) == (u_ != 0)
    assert equal(sp.solveset(x**2 < 0, x, R), sp.S.EmptySet)
    assert equal(sp.solveset(sp.Eq(x**2, 0), x, R), sp.FiniteSet(0))
    assert sp.Integer(1) == sp.Integer(1)**2 and sp.Integer(1) > 0
    # (a) symbolically: uv = 0 exactly when u = 0, for fixed v != 0 (solveset in u).
    for v_ in (-3, sp.Rational(1, 2), 7):
        assert equal(sp.solveset(x * v_, x, R), sp.FiniteSet(0))
    # (d): products and quotients of non-zero numbers, sign = (-1)^(number of negative factors);
    # and the proof's last step, N/D has the sign of N·D.
    nonzero = [v_ for v_ in vals if v_ != 0]
    for _ in range(500):
        num = rng.sample(nonzero, rng.randint(1, 5))
        den = rng.sample(nonzero, rng.randint(0, 4))
        N, D = sp.Mul(*num), sp.Mul(*den)
        q = N / D
        negs = sum(1 for v_ in num + den if v_ < 0)
        assert sp.sign(q) == (-1) ** negs
        assert sp.sign(q) == sp.sign(N * D)


def test_prop_calc_rational_domain():
    examples = [
        ((x + 1), x**2 - 4),
        (x**2 - 1, x**2 - x - 6),
        (x + 3, x**2 + x - 6),
        (x**2 - 9, x**2 + 2 * x - 3),
        (x**2 - 4, x**2 - 3 * x + 2),
        (x, x**2 + 1),
        (1, (x - 1)**2 * (x + 5) * (x**2 + 2)),
        (x**3, sp.Integer(7)),
    ]
    for p, q in examples:
        f = p / q
        m = poly(q).degree()
        # (a): dom f = R minus the roots of q, and at most m numbers are left out.
        roots_q = sp.solveset(q, x, R)
        assert equal(domain(f), sp.Complement(R, roots_q))
        assert len(roots_q) <= m
        # (b): the proof's interval (alpha, beta) around a, for several a, has no root of q
        # other than a.
        rq = sorted(roots_q)
        for a_ in list(rq) + [sp.Integer(0), sp.Rational(5, 2), sp.Integer(-7)]:
            below, above = [r_ for r_ in rq if r_ < a_], [r_ for r_ in rq if r_ > a_]
            al = max(below) if below else a_ - 1
            be = min(above) if above else a_ + 1
            assert al < a_ < be
            assert all(not (al < r_ < be) for r_ in rq if r_ != a_)
            if q.subs(x, a_) != 0:
                assert a_ in domain(f)
        # (c): zeros of f = roots of p that are not roots of q.
        zeros = sp.Complement(sp.solveset(p, x, R), roots_q)
        for z_ in zeros:
            assert value(f, z_) == 0
        for z_ in sp.solveset(p, x, R):
            if z_ in roots_q:
                assert value(f, z_) is None
    # The counterexample in Common mistakes: (x^2 - 4)/(x^2 - 3x + 2): numerator roots {2, -2},
    # but 2 is a root of the denominator, so the only zero is -2, and f(-2) = 0/12.
    f = (x**2 - 4) / (x**2 - 3 * x + 2)
    assert equal(sp.solveset(x**2 - 4, x, R), sp.FiniteSet(-2, 2))
    assert equal(sp.expand((x - 1) * (x - 2)), x**2 - 3 * x + 2)
    assert 2 not in domain(f)
    assert equal(sp.Complement(sp.solveset(x**2 - 4, x, R), sp.solveset(x**2 - 3 * x + 2, x, R)),
                 sp.FiniteSet(-2))
    assert equal((x**2 - 3 * x + 2).subs(x, -2), 12) and value(f, -2) == 0
    # x^2 + 1 >= 1 > 0 at every real x: nothing satisfies x^2 + 1 < 1.
    assert equal(sp.solveset(x**2 + 1 < 1, x, R), sp.S.EmptySet)
    assert equal(sp.solveset(x**2 + 1 > 0, x, R), R)


def test_prop_calc_rational_sign():
    # f = K N P / (D Q): on each open interval between the marked numbers, f is defined, non-zero,
    # of one sign, and that sign is (-1)^(negative factors among K, x - r_i, x - s_j) at any point.
    cases = [
        (1, [1, -1], [3, -2], 1, 1),
        (-1, [5], [1], 1, 1),
        (2, [1, 1], [0], x**2 + 1, 1),
        (-3, [2, 2, -4], [], 1, x**2 - x + 2),
        (sp.Rational(1, 2), [0, 0, 0], [1, 1], x**4 + 3, x**2 + 1),
        (1, [], [-1, 1], x**2 - x + 2, 1),
    ]
    for K, rs, ss, P, Q in cases:
        f = K * sp.Mul(*[(x - r_) for r_ in rs]) * P / (sp.Mul(*[(x - s_) for s_ in ss]) * Q)
        assert equal(sp.solveset(P <= 0, x, R) if P != 1 else sp.S.EmptySet, sp.S.EmptySet)
        assert equal(sp.solveset(Q <= 0, x, R) if Q != 1 else sp.S.EmptySet, sp.S.EmptySet)
        cuts = sorted(sp.sympify(v) for v in set(rs) | set(ss))
        S_pos = solve_ineq(sp.StrictGreaterThan(f, 0))
        S_neg = solve_ineq(sp.StrictLessThan(f, 0))
        bounds = [-oo] + cuts + [oo]
        for lo, hi in zip(bounds, bounds[1:]):
            I_ = sp.Interval.open(lo, hi)
            pt = (lo + hi) / 2 if lo.is_finite and hi.is_finite else (hi - 1 if lo is -oo else lo + 1)
            negs = negatives_at([K] + [x - r_ for r_ in rs] + [x - s_ for s_ in ss], pt)
            predicted = S_pos if negs % 2 == 0 else S_neg
            assert I_.is_subset(predicted), f"{f} on {I_}: parity predicts {'+' if negs % 2 == 0 else '-'}"
            assert I_.is_subset(domain(f))
            for v in (pt, lo + EPS if lo.is_finite else pt - 100, hi - EPS if hi.is_finite else pt + 100):
                val = value(f, v)
                assert val is not None and val != 0 and sp.sign(val) == (-1) ** negs


def test_figure_cubic_roots():
    c_ = sp.Symbol("c", real=True)
    f = x**3 - 3 * x + c_
    # c = 0: roots -sqrt(3), 0, sqrt(3), all inside the view [-3, 3]; x^3 - 3x = x(x^2 - 3).
    assert equal(sp.expand(x * (x**2 - 3)), x**3 - 3 * x)
    r0 = real_roots(f.subs(c_, 0))
    assert set(r0) == {-sp.sqrt(3), 0, sp.sqrt(3)} and all(-3 <= r_ <= 3 for r_ in r0)
    # c = 2: x^3 - 3x + 2 = (x - 1)^2 (x + 2), roots -2 (simple) and 1 (double); it touches at 1
    # without crossing: the same sign either side of 1, while it changes sign at -2.
    assert equal(sp.expand((x - 1)**2 * (x + 2)), x**3 - 3 * x + 2)
    assert real_roots(f.subs(c_, 2)) == {1: 2, -2: 1}
    f2 = f.subs(c_, 2)
    for d in (sp.Rational(1, 10), sp.Rational(1, 1000)):
        assert f2.subs(x, 1 - d) > 0 and f2.subs(x, 1 + d) > 0
        assert f2.subs(x, -2 - d) < 0 and f2.subs(x, -2 + d) > 0
    # Every slider value c = -4, -3.5, …, 4: degree 3, at most three real roots.
    for k_ in range(-8, 9):
        p = f.subs(c_, sp.Rational(k_, 2))
        assert poly(p).degree() == 3
        # Exact real roots as CRootOf (radicals hit casus irreducibilis here, where solveset
        # cannot decide), cross-checked against count_roots (Sturm), which counts distinct roots.
        distinct = set(poly(p).real_roots())
        assert len(distinct) == poly(p).count_roots() <= 3


def test_figure_sign_chart_table():
    f = (x**2 - 1) / (x**2 - x - 6)
    table = {-3: sp.Rational(4, 3), sp.Rational(-3, 2): sp.Rational(-5, 9), 0: sp.Rational(1, 6),
             2: sp.Rational(-3, 4), 4: sp.Rational(5, 2)}
    intervals = [sp.Interval.open(-oo, -2), sp.Interval.open(-2, -1), sp.Interval.open(-1, 1),
                 sp.Interval.open(1, 3), sp.Interval.open(3, oo)]
    for (pt, val), I_ in zip(table.items(), intervals):
        assert equal(value(f, pt), val)
        assert pt in I_  # one point in each interval of the sign chart, in order
    assert [sp.sign(v) for v in table.values()] == [1, -1, 1, -1, 1]
    # Gaps at -2 and 3, zeros at -1 and 1, all inside the view [-5, 6].
    assert value(f, -2) is None and value(f, 3) is None
    assert value(f, -1) == 0 and value(f, 1) == 0


def test_integer_division_analogy():
    assert 17 == 5 * 3 + 2 and 0 <= 2 < 3


def test_division_uniqueness_rigorous_track():
    # Uniqueness on exact examples: with unknown coefficients for q (degree k - m) and r (degree
    # < m), f = g q + r has exactly one solution, the one sp.div finds.
    for f, g in ((2 * x**3 - 3 * x**2 + 4 * x - 1, x**2 + 1), (x**4 + 2 * x**2 - x + 3, x**2 - x + 1),
                 (x**5 - 1, 3 * x**2 + x), (x**3 - 12 * x + 16, x - 2)):
        k_, m = poly(f).degree(), poly(g).degree()
        qs = sp.symbols(f"q0:{k_ - m + 1}")
        rs = sp.symbols(f"r0:{m}")
        qx = sum(qs[i] * x**i for i in range(len(qs)))
        rx = sum(rs[i] * x**i for i in range(len(rs)))
        eqs = poly(g * qx + rx - f).all_coeffs()
        sol = sp.solve(eqs, list(qs) + list(rs), dict=True)
        assert len(sol) == 1
        q, r = sp.div(f, g, x)
        assert equal(sp.expand(qx.subs(sol[0]) - q), 0) and equal(sp.expand(rx.subs(sol[0]) - r), 0)


def test_common_mistakes():
    # 1. (x + 3)/(x - 1) < 2: the wrong answer x > 5 misses x = 0, where the left side is -3.
    lhs = (x + 3) / (x - 1)
    S = solve_ineq(lhs < 2)
    assert equal(S, sp.Union(sp.Interval.open(-oo, 1), sp.Interval.open(5, oo)))
    spot_check(S, lhs < 2, extra=[1, 5])
    assert equal(value(lhs, 0), -3) and 0 in S and 0 not in sp.Interval.open(5, oo)
    assert equal(sp.cancel(lhs - 2 - (5 - x) / (x - 1)), 0)
    assert equal(sp.expand((-1) * (x - 5)), 5 - x)
    S2 = solve_ineq((5 - x) / (x - 1) < 0)
    assert equal(S2, sp.Union(sp.Interval.open(-oo, 1), sp.Interval.open(5, oo)))
    # 2. (x - 1)^2 (x + 2): positive on (-2, 1) and on (1, oo), p(2) = 4.
    p = (x - 1)**2 * (x + 2)
    pos = solve_ineq(p > 0)
    assert sp.Interval.open(-2, 1).is_subset(pos) and sp.Interval.open(1, oo).is_subset(pos)
    assert equal(pos, sp.Union(sp.Interval.open(-2, 1), sp.Interval.open(1, oo)))
    assert equal(p.subs(x, 2), 4)
    assert negatives_at([x - 1, x - 1, x + 2], 2) == 0
    # 3. x^2 + 1 has no real roots, (x - 1)^2 only the root 1.
    assert real_roots(x**2 + 1) == {}
    assert real_roots((x - 1)**2) == {1: 2}
    # 4. is in test_prop_calc_rational_domain (the counterexample (x^2 - 4)/(x^2 - 3x + 2)).


# ── Worked examples ──────────────────────────────────────────────────────────


@covers("eg-calc-polynomial-rational-division")
def test_eg_calc_polynomial_rational_division():
    f = 2 * x**3 - 3 * x**2 + 4 * x - 1
    g = x**2 + 1
    # Step 1: 2x^3 / x^2 = 2x; 2x g = 2x^3 + 2x; f - 2x g = -3x^2 + 2x - 1.
    assert equal(sp.cancel(2 * x**3 / x**2), 2 * x)
    assert equal(sp.expand(2 * x * g), 2 * x**3 + 2 * x)
    assert equal(sp.expand(f - 2 * x * g), -3 * x**2 + 2 * x - 1)
    # Step 2: -3x^2 / x^2 = -3; -3 g = -3x^2 - 3; leaves 2x + 2.
    assert equal(sp.expand(-3 * g), -3 * x**2 - 3)
    assert equal(sp.expand(-3 * x**2 + 2 * x - 1 - (-3 * g)), 2 * x + 2)
    # Step 3 and the box: q = 2x - 3, r = 2x + 2 (degree 1 < 2), against sp.div.
    check_division(f, g, 2 * x - 3, 2 * x + 2)
    # Check line: x = 1 gives 2 on both sides, x = 0 gives -1; (x^2 + 1)(2x - 3) multiplied out.
    rhs = g * (2 * x - 3) + (2 * x + 2)
    assert equal(f.subs(x, 1), 2) and equal(rhs.subs(x, 1), 2)
    assert equal(sp.Integer(2) * (-1) + 4, 2)
    assert equal(f.subs(x, 0), -1) and equal(rhs.subs(x, 0), -1)
    assert equal(sp.expand(g * (2 * x - 3)), 2 * x**3 - 3 * x**2 + 2 * x - 3)


@covers("eg-calc-polynomial-rational-factor-cubic")
def test_eg_calc_polynomial_rational_factor_cubic():
    p = x**3 - 2 * x**2 - 5 * x + 6
    # Step 1: p(1) = 0, so x - 1 is a factor (the factor theorem, checked both ways).
    assert equal(p.subs(x, 1), 0) and equal(sp.Integer(1) - 2 - 5 + 6, 0)
    assert factor_theorem_iff(p, 1)
    # Step 1's aside: an integer root divides 6, so only the divisors of 6 need trying; the
    # integer roots are among them.
    divisors = {d * s_ for d in sp.divisors(6) for s_ in (1, -1)}
    int_roots = {r_ for r_ in real_roots(p) if r_.is_integer}
    assert int_roots <= divisors
    # Step 2: the three subtractions, and the quotient by sp.div.
    s1 = sp.expand(p - x**2 * (x - 1))
    assert equal(s1, -x**2 - 5 * x + 6)
    s2 = sp.expand(s1 - (-x) * (x - 1))
    assert equal(s2, -6 * x + 6)
    assert equal(sp.expand(s2 - (-6) * (x - 1)), 0)
    check_division(p, x - 1, x**2 - x - 6, 0)
    Q = poly(x**2 - x - 6)
    assert Q.degree() == 2 and Q.LC() == 1
    # Step 3: -3 and 2 have product -6 and sum -1; x^2 - x - 6 = (x - 3)(x + 2).
    assert (-3) * 2 == -6 and -3 + 2 == -1
    assert equal(sp.expand((x - 3) * (x + 2)), x**2 - x - 6)
    # The box and step 4: p = (x - 1)(x - 3)(x + 2), roots 1, 3, -2, each simple; no more than 3.
    assert equal(sp.expand((x - 1) * (x - 3) * (x + 2)), p)
    assert equal(sp.factor(p), (x - 1) * (x - 3) * (x + 2))
    assert real_roots(p) == {1: 1, 3: 1, -2: 1}
    # Check line: p(3) and p(-2), term by term as printed; constant term (-1)(-3)(2) = 6.
    assert equal(sp.Integer(27) - 18 - 15 + 6, 0) and equal(p.subs(x, 3), 0)
    assert equal(sp.Integer(-8) - 8 + 10 + 6, 0) and equal(p.subs(x, -2), 0)
    assert equal(sp.Integer(-1) * (-3) * 2, 6) and poly(p).coeff_monomial(1) == 6


@covers("eg-calc-polynomial-rational-difference-quotient")
def test_eg_calc_polynomial_rational_difference_quotient():
    p = 2 * x**3 - 5 * x + 1
    # Step 1: p(1) = -2; p(x) - p(1) = 2x^3 - 5x + 3 = 2(x^3 - 1) - 5(x - 1).
    assert equal(p.subs(x, 1), -2)
    d = sp.expand(p - p.subs(x, 1))
    assert equal(d, 2 * x**3 - 5 * x + 3)
    assert equal(sp.expand(2 * (x**3 - 1) - 5 * (x - 1)), d)
    # Step 2: x^3 - 1 = (x - 1)(x^2 + x + 1), and d = (x - 1)(2x^2 + 2x - 3), against sp.div.
    assert equal(sp.expand((x - 1) * (x**2 + x + 1)), x**3 - 1)
    assert equal(sp.expand(2 * (x - 1) * (x**2 + x + 1) - 5 * (x - 1)), d)
    check_division(d, x - 1, 2 * x**2 + 2 * x - 3, 0)
    Q = poly(2 * x**2 + 2 * x - 3)
    assert Q.degree() == 2 and Q.LC() == 2
    # The proof's construction: q = 2 q_3 - 5 q_1 with a = 1.
    assert equal(sp.expand(2 * (x**2 + x + 1) - 5 * 1), 2 * x**2 + 2 * x - 3)
    # Step 3: for x != 1 the difference quotient equals q, and q(1) = 1.
    assert equal(sp.cancel(d / (x - 1)), 2 * x**2 + 2 * x - 3)
    assert equal((2 * x**2 + 2 * x - 3).subs(x, 1), 1)
    assert limit_is(d / (x - 1), x, 1, 1)
    # Check line: at 0, p(0) - p(1) = 3 = (0 - 1)(-3); at 2, p(2) = 7, 9 = (1)(9).
    assert equal(d.subs(x, 0), 3) and equal(sp.Integer(0 - 1) * (0 + 0 - 3), 3)
    assert equal(p.subs(x, 2), 7) and equal(d.subs(x, 2), 9) and equal(sp.Integer(2 - 1) * (8 + 4 - 3), 9)
    # Looking ahead: q(1) = 1 is the slope of the tangent at 1, i.e. p'(1).
    assert equal(sp.diff(p, x).subs(x, 1), 1)


@covers("eg-calc-polynomial-rational-sign-chart")
def test_eg_calc_polynomial_rational_sign_chart():
    f = (x**2 - 1) / (x**2 - x - 6)
    # Step 1: the factorisations.
    assert equal(sp.expand((x - 1) * (x + 1)), x**2 - 1)
    assert equal(sp.expand((x - 3) * (x + 2)), x**2 - x - 6)
    assert equal(sp.factor(x**2 - x - 6), (x - 3) * (x + 2))
    # Steps 2–3 and the Result: domain from the unsimplified denominator, zeros, signs.
    dom = sp.Union(sp.Interval.open(-oo, -2), sp.Interval.open(-2, 3), sp.Interval.open(3, oo))
    assert equal(domain(f), dom)
    positive = sp.Union(sp.Interval.open(-oo, -2), sp.Interval.open(-1, 1), sp.Interval.open(3, oo))
    negative = sp.Union(sp.Interval.open(-2, -1), sp.Interval.open(1, 3))
    check_sign_chart(f, positive, negative, zeros=[-1, 1], undefined=[-2, 3], cuts=[-2, -1, 1, 3])
    # Step 4: the table, row by row: each factor's sign at a point of the interval, and the
    # parity rule (four, two, zero negatives give +; three, one give -).
    factors = [x + 2, x + 1, x - 1, x - 3]
    rows = [
        (sp.Interval.open(-oo, -2), "----", 1),
        (sp.Interval.open(-2, -1), "+---", -1),
        (sp.Interval.open(-1, 1), "++--", 1),
        (sp.Interval.open(1, 3), "+++-", -1),
        (sp.Interval.open(3, oo), "++++", 1),
    ]
    for I_, signs, fsign in rows:
        pt = (I_.start + I_.end) / 2 if I_.start.is_finite and I_.end.is_finite else (
            I_.end - 1 if I_.start is -oo else I_.start + 1)
        for fac, sg in zip(factors, signs):
            assert sp.sign(fac.subs(x, pt)) == (1 if sg == "+" else -1)
            # one sign on the whole interval: the factor's own zero is not inside it
            assert sp.solveset(fac, x, I_) == sp.S.EmptySet
        assert (-1) ** signs.count("-") == fsign
        assert I_.is_subset(positive if fsign == 1 else negative)
    assert [r[1].count("-") for r in rows] == [4, 3, 2, 1, 0]
    # Check line: f(0) = 1/6, f(2) = -3/4 (printed 3/(-4)), f(4) = 15/6.
    assert equal(value(f, 0), sp.Rational(1, 6)) and equal(sp.Rational(-1, -6), sp.Rational(1, 6))
    assert equal(value(f, 2), sp.Rational(3, -4))
    assert equal(value(f, 4), sp.Rational(15, 6))


@covers("eg-calc-polynomial-rational-box")
def test_eg_calc_polynomial_rational_box():
    hx = 4 / x**2
    # Step 1: volume x^2 h = 4; area = base + four sides xh = 4/x, so S = x^2 + 16/x.
    assert equal(x**2 * hx, 4)
    assert equal(x * hx, 4 / x)
    S = x**2 + 4 * x * hx
    assert equal(S, x**2 + 16 / x)
    # Step 2: S - 12 = (x^3 - 12x + 16)/x.
    assert equal(sp.together(S - 12) - (x**3 - 12 * x + 16) / x, 0)
    num = x**3 - 12 * x + 16
    # Step 3: the root 2 and the division, step by step.
    assert equal(num.subs(x, 2), 0) and equal(sp.Integer(8) - 24 + 16, 0)
    assert factor_theorem_iff(num, 2)
    s1 = sp.expand(num - x**2 * (x - 2))
    assert equal(s1, 2 * x**2 - 12 * x + 16)
    s2 = sp.expand(s1 - 2 * x * (x - 2))
    assert equal(s2, -8 * x + 16)
    assert equal(sp.expand(s2 - (-8) * (x - 2)), 0)
    check_division(num, x - 2, x**2 + 2 * x - 8, 0)
    assert equal(sp.expand((x - 2) * (x + 4)), x**2 + 2 * x - 8)
    # Step 4 and the box: (x - 2)^2 (x + 4)/x on (0, oo) is > 0 except at 2, where it is 0.
    assert equal(sp.factor(num), (x - 2)**2 * (x + 4))
    assert real_roots(num) == {2: 2, -4: 1}
    pos = sp.Interval.open(0, oo)
    assert equal(sp.solveset(S - 12 < 0, x, pos), sp.S.EmptySet)
    assert equal(sp.solveset(sp.Eq(S, 12), x, pos), sp.FiniteSet(2))
    assert equal(sp.solveset(S - 12 > 0, x, pos), sp.Union(sp.Interval.open(0, 2), sp.Interval.open(2, oo)))
    for v in [sp.Rational(k_, 16) for k_ in range(1, 161)] + [2 - EPS, 2 + EPS, EPS]:
        assert S.subs(x, v) >= 12 and (S.subs(x, v) == 12) == (v == 2)
    # On (0, 2) both factors x - 2 are negative, on (2, oo) both positive; x, x + 4 positive.
    for v, n_neg in ((1, 2), (3, 0)):
        assert negatives_at([x - 2, x - 2, x + 4, x], v) == n_neg
    # The box with x = 2: h = 1, volume 4; check line S(1) = 17, S(2) = 12, S(4) = 20.
    assert equal(hx.subs(x, 2), 1) and equal(sp.Integer(2)**2 * 1, 4)
    assert equal(S.subs(x, 1), 17) and equal(S.subs(x, 2), 12) and equal(S.subs(x, 4), 20)


# ── Exercises ────────────────────────────────────────────────────────────────


@covers("exr-calc-polynomial-rational-degree")
def test_exr_calc_polynomial_rational_degree():
    p = (2 * x - 1) * (x**2 + 3) - 2 * x**3
    P = poly(p)
    deg, lc = answer("exr-calc-polynomial-rational-degree")
    assert equal(deg, P.degree())
    assert equal(lc, P.LC())
    # The product alone has degree 3 (the subtraction cancels its leading term).
    assert poly((2 * x - 1) * (x**2 + 3)).degree() == 3


@covers("exr-calc-polynomial-rational-factor-check")
def test_exr_calc_polynomial_rational_factor_check():
    p = x**4 - 3 * x**3 + x + 6
    expected = sp.true if factor_theorem_iff(p, 2) else sp.false
    assert equal(answer("exr-calc-polynomial-rational-factor-check"), expected)
    # The solution's quotient.
    check_division(p, x - 2, x**3 - x**2 - 2 * x - 3, 0)


@covers("exr-calc-polynomial-rational-domain")
def test_exr_calc_polynomial_rational_domain():
    f = (x + 3) / (x**2 + x - 6)  # SymPy does not cancel on construction
    assert sp.fraction(f) == (x + 3, x**2 + x - 6)
    expected = domain(f)
    printed = answer("exr-calc-polynomial-rational-domain")
    assert equal(printed, expected)
    # Pointwise: v is in the printed domain exactly when the unsimplified denominator is non-zero.
    for v in marked_points(printed, extra=[-3, 2]):
        assert bool(printed.contains(v)) == ((x**2 + x - 6).subs(x, v) != 0)
    # Cancelling first would give a larger domain (it would put -3 back), the trap the hint names.
    cancelled = sp.cancel(f)
    assert equal(cancelled, 1 / (x - 2))
    assert -3 in domain(cancelled) and -3 not in printed
    # -3 gives 0/0 in f as written.
    assert (x + 3).subs(x, -3) == 0 and (x**2 + x - 6).subs(x, -3) == 0
    assert equal(sp.expand((x + 3) * (x - 2)), x**2 + x - 6)


@covers("exr-calc-polynomial-rational-zeros")
def test_exr_calc_polynomial_rational_zeros():
    f = (x**2 - 9) / (x**2 + 2 * x - 3)
    num, den = sp.fraction(f)
    expected = sp.Complement(sp.solveset(num, x, R), sp.solveset(den, x, R))
    printed = answer("exr-calc-polynomial-rational-zeros")
    assert equal(printed, expected)
    # Second route: f evaluated exactly at every root of the numerator.
    for z_ in sp.solveset(num, x, R):
        assert (value(f, z_) == 0) == (z_ in printed)
    assert equal(sp.expand((x + 3) * (x - 1)), x**2 + 2 * x - 3)
    assert equal(sp.expand((x - 3) * (x + 3)), x**2 - 9)
    assert equal(den.subs(x, 3), 12)


@covers("exr-calc-polynomial-rational-division")
def test_exr_calc_polynomial_rational_division():
    f = x**4 + 2 * x**2 - x + 3
    g = x**2 - x + 1
    q, r = sp.div(f, g, x)
    q_page, r_page = answer("exr-calc-polynomial-rational-division")
    assert equal(q_page, q) and equal(r_page, r)
    check_division(f, g, q_page, r_page)
    # The solution's steps.
    assert equal(sp.expand(x**2 * g), x**4 - x**3 + x**2)
    s1 = sp.expand(f - x**2 * g)
    assert equal(s1, x**3 + x**2 - x + 3)
    assert equal(sp.expand(x * g), x**3 - x**2 + x)
    s2 = sp.expand(s1 - x * g)
    assert equal(s2, 2 * x**2 - 2 * x + 3)
    assert equal(sp.expand(2 * g), 2 * x**2 - 2 * x + 2)
    assert equal(sp.expand(s2 - 2 * g), 1)
    assert equal(f.subs(x, 1), 5) and equal(g.subs(x, 1) * q.subs(x, 1) + r, 5)


@covers("exr-calc-polynomial-rational-factor-cubic")
def test_exr_calc_polynomial_rational_factor_cubic():
    p = 2 * x**3 - 3 * x**2 - 11 * x + 6
    assert equal(p.subs(x, 3), 0) and factor_theorem_iff(p, 3)
    printed = answer("exr-calc-polynomial-rational-factor-cubic")
    # The printed product is p, and it is a product of linear factors (a constant times
    # factors of degree 1 in x).
    assert equal(sp.expand(printed - p), 0)
    assert isinstance(printed, sp.Mul)
    for fac in printed.args:
        assert fac.is_number or poly(fac).degree() == 1, f"{fac} is not linear"
    # Independently: sp.factor gives the same factorisation up to constants, and the roots.
    assert equal(sp.expand(sp.factor(p) - printed), 0)
    assert real_roots(p) == {3: 1, sp.Rational(1, 2): 1, -2: 1}
    # The solution's steps and quotient.
    assert equal(sp.Integer(54) - 27 - 33 + 6, 0)
    s1 = sp.expand(p - 2 * x**2 * (x - 3))
    assert equal(s1, 3 * x**2 - 11 * x + 6)
    s2 = sp.expand(s1 - 3 * x * (x - 3))
    assert equal(s2, -2 * x + 6)
    assert equal(sp.expand(s2 - (-2) * (x - 3)), 0)
    check_division(p, x - 3, 2 * x**2 + 3 * x - 2, 0)
    assert equal(sp.expand((2 * x - 1) * (x + 2)), 2 * x**2 + 3 * x - 2)


@covers("exr-calc-polynomial-rational-difference-quotient")
def test_exr_calc_polynomial_rational_difference_quotient():
    p = x**3 - 2 * x
    a_ = -1
    q, rem = sp.div(sp.expand(p - p.subs(x, a_)), x - a_, x)
    assert rem == 0
    q_page, q_at = answer("exr-calc-polynomial-rational-difference-quotient")
    assert equal(q_page, q)
    assert equal(q_at, q.subs(x, a_))
    # Second route: the difference quotient cancels to q, and its limit at -1 is q(-1) = p'(-1).
    assert equal(sp.cancel((p - p.subs(x, a_)) / (x - a_)), q_page)
    assert equal(sp.diff(p, x).subs(x, a_), q_at)
    Q = poly(q_page)
    assert Q.degree() == 2 and Q.LC() == 1
    # The solution's steps.
    assert equal(p.subs(x, -1), 1)
    assert equal(sp.expand((x**3 - (-1)**3) - 2 * (x - (-1))), x**3 - 2 * x - 1)
    assert equal(sp.expand((x + 1) * (x**2 - x + 1)), x**3 + 1)


@covers("exr-calc-polynomial-rational-remainder")
def test_exr_calc_polynomial_rational_remainder():
    p = x**100 - 2 * x + 1
    r = sp.rem(p, x - 1, x)
    assert equal(answer("exr-calc-polynomial-rational-remainder"), r)
    # Second route: the factor theorem's remainder p(1).
    assert equal(p.subs(x, 1), r)
    assert factor_theorem_iff(p, 1)


@covers("exr-calc-polynomial-rational-inequality")
def test_exr_calc_polynomial_rational_inequality():
    rel = (2 * x - 1) / (x + 1) < 1
    expected = solve_ineq(rel)
    printed = answer("exr-calc-polynomial-rational-inequality")
    assert equal(printed, expected)
    spot_check(printed, rel, extra=[-1, 2])
    # The solution's reduction: (2x - 1)/(x + 1) - 1 = (x - 2)/(x + 1), and its sign chart.
    assert equal(sp.cancel((2 * x - 1) / (x + 1) - 1 - (x - 2) / (x + 1)), 0)
    check_sign_chart((x - 2) / (x + 1),
                     positive=sp.Union(sp.Interval.open(-oo, -1), sp.Interval.open(2, oo)),
                     negative=sp.Interval.open(-1, 2), zeros=[2], undefined=[-1], cuts=[-1, 2])
    # Its examples: x = 0 gives -1 < 1; x = -2 gives 5.
    assert equal(value(rel.lhs, 0), -1) and equal(value(rel.lhs, -2), 5)


@covers("exr-calc-polynomial-rational-concentration")
def test_exr_calc_polynomial_rational_concentration():
    c_ = 5 * t / (t**2 + 4)
    rel = c_ > 1
    expected = sp.Intersection(sp.solveset(rel, t, R), sp.Interval(0, oo))
    printed = answer("exr-calc-polynomial-rational-concentration")
    assert equal(printed, expected)
    spot_check(printed, rel, var=t, extra=[0, 1, 4])
    # The denominator is positive everywhere; the reduction to t^2 - 5t + 4 < 0 = (t - 1)(t - 4).
    assert equal(sp.solveset(t**2 + 4 <= 0, t, R), sp.S.EmptySet)
    assert equal(sp.solveset(t**2 + 4 < 4, t, R), sp.S.EmptySet)  # t^2 + 4 >= 4 for every t
    assert equal(sp.solveset(t**2 - 5 * t + 4 < 0, t, R), expected)
    assert equal(sp.expand((t - 1) * (t - 4)), t**2 - 5 * t + 4)
    # The check values: c(2) = 10/8 = 1.25, c(1) = 1.
    assert equal(c_.subs(t, 2), sp.Rational(5, 4)) and equal(c_.subs(t, 1), 1)


@covers("exr-calc-polynomial-rational-from-roots")
def test_exr_calc_polynomial_rational_from_roots():
    # Independently: the general cubic with these roots is K(x + 1)(x - 1)(x - 2) (three applications
    # of the factor theorem, or: the cubic is determined by K and its roots); K from p(0) = 4.
    K = sp.Symbol("K")
    general = K * (x + 1) * (x - 1) * (x - 2)
    Kv = sp.solve(sp.Eq(general.subs(x, 0), 4), K)
    assert len(Kv) == 1
    expected = general.subs(K, Kv[0])
    printed = answer("exr-calc-polynomial-rational-from-roots")
    assert equal(sp.expand(printed - expected), 0)
    # Second route: the printed polynomial has degree 3, exactly the roots -1, 1, 2, and p(0) = 4.
    assert poly(printed).degree() == 3
    assert set(real_roots(printed)) == {-1, 1, 2}
    assert equal(printed.subs(x, 0), 4)
    # Uniqueness: the coefficients of a cubic c3 x^3 + … + c0 satisfying the four conditions are
    # unique (cor-calc-polynomial-identity's "values determine coefficients", for n = 3).
    cs = sp.symbols("c0:4")
    cubic = sum(cs[i] * x**i for i in range(4))
    sol = sp.solve([cubic.subs(x, -1), cubic.subs(x, 1), cubic.subs(x, 2), cubic.subs(x, 0) - 4], cs, dict=True)
    assert len(sol) == 1 and equal(sp.expand(cubic.subs(sol[0]) - printed), 0)
    # The solution's K is the leading coefficient of p.
    assert equal(poly(expected).LC(), Kv[0])
    # The solution's values: (x + 1) at 1 is 2; (x + 1)(x - 1) at 2 is 3 · 1; at 0, (1)(-1)(-2) = 2.
    assert (x + 1).subs(x, 1) == 2 and (x + 1).subs(x, 2) == 3 and (x - 1).subs(x, 2) == 1
    assert ((x + 1) * (x - 1) * (x - 2)).subs(x, 0) == 2


@covers("exr-calc-polynomial-rational-inequality-hard")
def test_exr_calc_polynomial_rational_inequality_hard():
    rel = x / (x - 1) >= 2 / (x + 1)
    expected = solve_ineq(rel)
    # Second route: solveset of the one-sided form, over the domain of both sides.
    one_sided = solve_ineq(sp.together(x / (x - 1) - 2 / (x + 1)) >= 0)
    assert equal(expected, one_sided)
    printed = answer("exr-calc-polynomial-rational-inequality-hard")
    assert equal(printed, expected)
    spot_check(printed, rel, extra=[-1, 1, 0, sp.Rational(1, 2)])
    # The solution's numerator: x(x + 1) - 2(x - 1) = x^2 - x + 2 = (x - 1/2)^2 + 7/4, never 0.
    assert equal(sp.expand(x * (x + 1) - 2 * (x - 1)), x**2 - x + 2)
    assert equal(sp.expand((x - sp.Rational(1, 2))**2 + sp.Rational(7, 4)), x**2 - x + 2)
    assert equal(sp.solveset(x**2 - x + 2 < sp.Rational(7, 4), x, R), sp.S.EmptySet)
    assert real_roots(x**2 - x + 2) == {}
    # Its examples: x = 2 gives 2 >= 2/3; x = 0 gives 0 >= 2, false.
    assert equal(value(x / (x - 1), 2), 2) and equal(value(2 / (x + 1), 2), sp.Rational(2, 3))
    assert not holds(rel, 0) and equal(value(2 / (x + 1), 0), 2)


@covers("exr-calc-polynomial-rational-integer-root")
def test_exr_calc_polynomial_rational_integer_root():
    # The answer is a proof: answer() has nothing to read, so this test cannot cover the label
    # (only the reviewer's maths.manual_checked note can). Check the key claims anyway.
    assert answer_type("exr-calc-polynomial-rational-integer-root") == "manual"
    with pytest.raises(ManualAnswer):
        answer("exr-calc-polynomial-rational-integer-root")
    # The identity behind the proof, symbolically for n = 1 … 6: if p(r) = 0 then
    # c_0 = r * k with k = -(c_n r^(n-1) + … + c_1).
    r_ = sp.Symbol("r")
    for n_ in range(1, 7):
        cs = sp.symbols(f"c0:{n_ + 1}")
        p_r = sum(cs[i] * r_**i for i in range(n_ + 1))
        k_ = -sum(cs[i] * r_**(i - 1) for i in range(1, n_ + 1))
        assert equal(sp.expand(cs[0] - r_ * k_ - p_r), 0)  # c0 - r k = p(r), which is 0
    # Sampled: integer polynomials with a known integer root r != 0; r divides the constant term.
    rng = random.Random(5)
    for _ in range(300):
        root = rng.choice([v for v in range(-9, 10) if v != 0])
        cofactor = sum(rng.randint(-6, 6) * x**i for i in range(rng.randint(1, 4)))
        p = sp.expand((x - root) * cofactor)
        if p == 0:
            continue
        assert p.subs(x, root) == 0
        assert poly(p).coeff_monomial(1) % root == 0
    # The example: x^3 + x^2 - 7x + 2. Its integer roots, from all its roots, are {2}; and the
    # candidates ±1, ±2 give -3, 9, 0, 12.
    p = x**3 + x**2 - 7 * x + 2
    rts = real_roots(p)
    assert {r for r in rts if r.is_integer} == {2}
    for v, val in ((1, -3), (-1, 9), (2, 0), (-2, 12)):
        assert equal(p.subs(x, v), val)
    assert set(d * s_ for d in sp.divisors(2) for s_ in (1, -1)) == {1, -1, 2, -2}
    # The solution's proof that the integers dividing 2 are ±1, ±2. Exhaustively over
    # |r|, |k| <= 60 (a sampled check, not a proof): 2 = rk only for r in {±1, ±2}, and never
    # with r = 0 or k = 0.
    pairs = [(r, k) for r in range(-60, 61) for k in range(-60, 61) if r * k == 2]
    assert {r for r, _ in pairs} == {1, -1, 2, -2}
    assert all(r != 0 and k != 0 for r, k in pairs)
    # Its steps, on the same range: for r >= 3, k >= 1 gives rk >= r >= 3 and k <= -1 gives
    # rk <= -r <= -3; for r <= -3, 2 = rk is 2 = (-r)(-k) with -r >= 3.
    for r in range(3, 61):
        for k in range(-60, 61):
            if k >= 1:
                assert r * k >= r >= 3
            if k <= -1:
                assert r * k <= -r <= -3
    for r in range(-60, -2):
        for k in range(-60, 61):
            assert r * k == (-r) * (-k) and -r >= 3
