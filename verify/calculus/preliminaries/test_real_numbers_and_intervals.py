"""Verification tests for content/calculus/preliminaries/real-numbers-and-intervals.md (calc-real-numbers).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
is derived here from the statement (the set's defining conditions, the decimal as a series), not
copied from the page's answers or solutions; the page's answers are read with answer(label).
"""

import random

import pytest
import sympy as sp

from mathcheck import (
    ManualAnswer,
    a,
    answer,
    b,
    covers,
    equal,
    k,
    limit_is,
    n,
    s,
    series_converges_to,
    symbol,
    x,
)

R = sp.S.Reals
m = symbol("m")  # real; the parity identities below are polynomial identities, true for all m
q = symbol("q")
L = symbol("L")
oo = sp.oo


def solve(condition, var=x):
    """The set of real var satisfying `condition`, as SymPy finds it (an And is the
    intersection of its parts' sets: solveset does not take And)."""
    if isinstance(condition, sp.And):
        return sp.Intersection(*(solve(c, var) for c in condition.args))
    return sp.solveset(condition, var, R)


def contains(S, value) -> sp.Basic:
    """S ∋ value as sp.true/sp.false, so that equal() can assert it (and count it)."""
    return sp.sympify(S.contains(value))


def decimal_digits(fraction: sp.Rational, count: int) -> list[int]:
    """The first `count` digits after the decimal point, by exact arithmetic."""
    return [int(sp.floor(fraction * 10**i)) % 10 for i in range(1, count + 1)]


# ── Worked examples ──────────────────────────────────────────────────────────


@covers("eg-calc-real-numbers-set-to-interval")
def test_eg_calc_real_numbers_set_to_interval():
    # The set {x ∈ ℝ : x > -1 and x ≤ 3}, solved from its two conditions.
    S = solve(x > -1).intersect(solve(x <= 3))
    # Step 1: the two conditions together say -1 < x ≤ 3.
    assert equal(S, solve(sp.And(-1 < x, x <= 3)))
    # Step 2: -1 is excluded; step 3: 3 is included.
    assert equal(contains(S, -1), sp.false)
    assert equal(contains(S, 3), sp.true)
    # The boxed result (-1, 3].
    assert equal(S, sp.Interval.Lopen(-1, 3))
    # Check line: 3 in, -1 out, 0 in.
    assert equal(contains(sp.Interval.Lopen(-1, 3), 3), sp.true)
    assert equal(contains(sp.Interval.Lopen(-1, 3), -1), sp.false)
    assert equal(contains(S, 0), sp.true)


@covers("eg-calc-real-numbers-intersection-union")
def test_eg_calc_real_numbers_intersection_union():
    # Step 1: A and B from their conditions -2 ≤ x < 3 and 1 < x ≤ 5.
    A = solve(sp.And(-2 <= x, x < 3))
    B = solve(sp.And(1 < x, x <= 5))
    assert equal(A, sp.Interval.Ropen(-2, 3))
    assert equal(B, sp.Interval.Lopen(1, 5))
    # Step 2: the intersection is 1 < x < 3; 1 ∉ B and 3 ∉ A.
    assert equal(A.intersect(B), solve(sp.And(1 < x, x < 3)))
    assert equal(contains(B, 1), sp.false)
    assert equal(contains(A, 3), sp.false)
    # Step 3: they overlap on (1, 3); -2 ∈ A and 5 ∈ B.
    assert equal(A.intersect(B), sp.Interval.open(1, 3))
    assert equal(contains(A, -2), sp.true)
    assert equal(contains(B, 5), sp.true)
    # The boxed results.
    assert equal(A.intersect(B), sp.Interval.open(1, 3))
    assert equal(A.union(B), sp.Interval(-2, 5))
    # Check line: 2 in both; 4 in B only; 3 in B, not in A.
    assert equal(contains(A, 2), sp.true) and equal(contains(B, 2), sp.true)
    assert equal(contains(A, 4), sp.false) and equal(contains(B, 4), sp.true)
    assert equal(contains(A.union(B), 4), sp.true) and equal(contains(A.intersect(B), 4), sp.false)
    assert equal(contains(A.union(B), 3), sp.true) and equal(contains(A.intersect(B), 3), sp.false)


@covers("eg-calc-real-numbers-repeating-decimal")
def test_eg_calc_real_numbers_repeating_decimal():
    # 0.363636… = sum over j ≥ 1 of 36/100^j, derived from the digits.
    value = sp.summation(sp.Rational(36) / 100**n, (n, 1, oo))
    assert series_converges_to(sp.Rational(36) / 100**n, n, value, start=1)
    # Step 1: 100x = 36.3636…, i.e. 100x = 36 + x.
    assert equal(100 * value, 36 + value)
    # Step 2: 100x - x = 36, so 99x = 36.
    assert equal(100 * value - value, 36)
    assert equal(99 * value, 36)
    # Step 3: x = 36/99 = 4/11, dividing by 9 = gcd(36, 99).
    assert equal(value, sp.Rational(36, 99))
    assert sp.gcd(36, 99) == 9
    assert equal(sp.Rational(36, 99), sp.Rational(4, 11))
    assert equal(value, sp.Rational(4, 11))
    # Check line: long division of 4 by 11.
    assert equal(sp.Integer(40), 3 * 11 + 7)
    assert equal(sp.Integer(70), 6 * 11 + 4)
    assert decimal_digits(sp.Rational(4, 11), 8) == [3, 6] * 4


@covers("eg-calc-real-numbers-tolerance")
def test_eg_calc_real_numbers_tolerance():
    tol = sp.Rational(1, 2)
    # Step 1: "differs from 40 by at most 0.5" is |L - 40| ≤ 0.5.
    accepted = solve(sp.Abs(L - 40) <= tol, L)
    assert equal(accepted, solve(sp.And(40 - tol <= L, L <= 40 + tol), L))
    assert equal(40 - tol, sp.Rational(395, 10)) and equal(40 + tol, sp.Rational(405, 10))
    # Step 2 and the boxed result: [39.5, 40.5], both endpoints in.
    assert equal(accepted, sp.Interval(sp.Rational(395, 10), sp.Rational(405, 10)))
    # Check line: 40.3 differs by 0.3 and is accepted; 40.6 differs by 0.6 and is rejected.
    assert equal(sp.Abs(sp.Rational(403, 10) - 40), sp.Rational(3, 10))
    assert equal(contains(accepted, sp.Rational(403, 10)), sp.true)
    assert equal(sp.Abs(sp.Rational(406, 10) - 40), sp.Rational(6, 10))
    assert equal(contains(accepted, sp.Rational(406, 10)), sp.false)
    # The interval has length 1 mm, twice the tolerance.
    assert equal(accepted.measure, 1) and equal(accepted.measure, 2 * tol)


# ── Exercises ────────────────────────────────────────────────────────────────


@covers("exr-calc-real-numbers-to-interval")
def test_exr_calc_real_numbers_to_interval():
    expected = (
        solve(sp.And(-2 < x, x <= 5)),  # (a)
        solve(x >= 3),                  # (b)
        solve(x < 0),                   # (c)
    )
    assert equal(answer("exr-calc-real-numbers-to-interval"), expected)


@covers("exr-calc-real-numbers-integers-in-interval")
def test_exr_calc_real_numbers_integers_in_interval():
    interval = solve(sp.And(-2 < x, x <= 3))  # (-2, 3]
    integers = sp.FiniteSet(*interval.intersect(sp.S.Integers))
    assert equal(answer("exr-calc-real-numbers-integers-in-interval"), integers)


@covers("exr-calc-real-numbers-integers-rational")
def test_exr_calc_real_numbers_integers_rational():
    # Z ⊆ Q, by SymPy's sets and by n = n/1 for a symbolic integer n.
    assert sp.S.Integers.is_subset(sp.S.Rationals) is True
    assert n.is_rational is True
    assert equal(answer("exr-calc-real-numbers-integers-rational"), sp.S.Integers.is_subset(sp.S.Rationals))


@covers("exr-calc-real-numbers-intersection")
def test_exr_calc_real_numbers_intersection():
    expected = solve(sp.And(-1 <= x, x < 4)).intersect(solve(sp.And(2 < x, x <= 6)))
    got = answer("exr-calc-real-numbers-intersection")
    assert equal(got, expected)
    assert isinstance(got, sp.Interval)  # "as an interval"


@covers("exr-calc-real-numbers-union")
def test_exr_calc_real_numbers_union():
    expected = solve(sp.And(0 <= x, x <= 2)).union(solve(sp.And(1 < x, x < 5)))
    got = answer("exr-calc-real-numbers-union")
    assert equal(got, expected)
    assert isinstance(got, sp.Interval)  # "as an interval"


@covers("exr-calc-real-numbers-complement")
def test_exr_calc_real_numbers_complement():
    complement = R - solve(sp.And(1 <= x, x < 3))
    # SymPy's complement is a union of two intervals; order them left to right.
    assert isinstance(complement, sp.Union) and len(complement.args) == 2
    expected = tuple(sorted(complement.args, key=lambda I: I.inf))
    assert all(isinstance(I, sp.Interval) for I in expected)
    assert equal(answer("exr-calc-real-numbers-complement"), expected)


@covers("exr-calc-real-numbers-repeating-decimal")
def test_exr_calc_real_numbers_repeating_decimal():
    # 0.272727… = sum over j ≥ 1 of 27/100^j.
    term = sp.Rational(27) / 100**n
    value = sp.summation(term, (n, 1, oo))
    assert series_converges_to(term, n, value, start=1)
    got = answer("exr-calc-real-numbers-repeating-decimal")
    assert equal(got, value)
    assert decimal_digits(sp.nsimplify(got), 8) == [2, 7] * 4
    # "In lowest terms": SymPy reduces fractions when it parses them, so the printed form
    # (\frac{3}{11}) is reviewed manually.


@covers("exr-calc-real-numbers-delayed-repeat")
def test_exr_calc_real_numbers_delayed_repeat():
    # 1.2333… = 1 + 2/10 + sum over j ≥ 2 of 3/10^j.
    value = 1 + sp.Rational(2, 10) + sp.summation(sp.Rational(3) / 10**n, (n, 2, oo))
    got = answer("exr-calc-real-numbers-delayed-repeat")
    assert equal(got, value)
    assert equal(sp.floor(got), 1)
    assert decimal_digits(sp.nsimplify(got), 8) == [2] + [3] * 7
    # The hint's method: 10x and 100x have the same tail.
    assert equal(100 * value - 10 * value, sp.floor(100 * value) - sp.floor(10 * value))


@covers("exr-calc-real-numbers-sqrt3-irrational")
def test_exr_calc_real_numbers_sqrt3_irrational_key_claims():
    # The answer is manual (a proof); its key claims are checked here, and the proof itself is
    # covered only by a reviewer's note.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-real-numbers-sqrt3-irrational")
    # A non-multiple of 3 squares to a non-multiple of 3: the two expansions in the solution.
    assert equal((3 * m + 1) ** 2, 3 * (3 * m**2 + 2 * m) + 1)
    assert equal((3 * m + 2) ** 2, 3 * (3 * m**2 + 4 * m + 1) + 1)
    # The same claim by brute force over residues: 3 | p² exactly when 3 | p.
    assert all((p * p % 3 == 0) == (p % 3 == 0) for p in range(-300, 301))
    # p = 3k in p² = 3q² gives q² = 3k².
    assert equal(sp.solve(sp.Eq((3 * k) ** 2, 3 * q**2), q**2)[0], 3 * k**2)
    # The conclusion, and no fraction p/q with q ≤ 2000 squares to 3.
    assert sp.sqrt(3).is_rational is False
    assert not any(sp.sqrt(3 * qq * qq).is_integer for qq in range(1, 2001))


@covers("exr-calc-real-numbers-supremum")
def test_exr_calc_real_numbers_supremum():
    # (a) The terms 1 - 1/n increase with n (their differences are positive) and tend to their
    # limit, so the supremum of the set is that limit.
    term = 1 - 1 / n
    assert equal(sp.simplify(term.subs(n, n + 1) - term), 1 / (n * (n + 1)))
    assert all(term.subs(n, j + 1) > term.subs(n, j) for j in range(1, 200))
    sup_a = sp.limit(term, n, oo)
    assert limit_is(1 - 1 / x, x, oo, sup_a)
    # (b) The set {x ∈ ℝ : x² < 2} from its condition.
    T = solve(x**2 < 2)
    sup_b = T.sup
    got = answer("exr-calc-real-numbers-supremum")
    assert equal(got, (sup_a, sup_b))
    # The solution's key steps. (a) n > 1/(1 - u) gives 1 - 1/n > u, for u < 1 (spot check).
    rng = random.Random(0)
    for _ in range(200):
        u_ = sp.Rational(rng.randint(-10**6, 10**6 - 1), 10**6)
        n_ = sp.floor(1 / (1 - u_)) + 1
        assert n_ >= 1 and 1 - sp.Rational(1, n_) > u_
    # (b) the supremum is not in T; for 0 ≤ u < √2, x = (u + √2)/2 lies in T and exceeds u.
    assert equal(contains(T, sup_b), sp.false)
    for _ in range(200):
        u_ = sp.Rational(rng.randint(0, 14142), 10**4)
        xv = (u_ + sp.sqrt(2)) / 2
        assert (u_ < xv) is sp.true and equal(contains(T, xv), sp.true)


@covers("exr-calc-real-numbers-rational-between")
def test_exr_calc_real_numbers_rational_between_key_claims():
    # Manual answer (a proof): check its construction, which the reviewer's note covers.
    with pytest.raises(ManualAnswer):
        answer("exr-calc-real-numbers-rational-between")
    # n > 1/(b - a) is nb - na > 1, for b > a and n > 0.
    nn = symbol("N")
    d = sp.Symbol("d", positive=True)  # d = b - a
    assert equal(sp.expand(nn * (a + d) - nn * a), nn * d)
    # The construction: n the first integer above 1/(b - a), m the smallest integer above na.
    # Exact arithmetic, with close pairs and irrational endpoints.
    rng = random.Random(1)
    pairs = [(sp.sqrt(2), sp.sqrt(2) + sp.Rational(1, 1000)), (-sp.pi, -sp.pi + sp.Rational(1, 10**6)),
             (sp.Integer(0), sp.Rational(1, 7)), (sp.Integer(-3), sp.Integer(-2))]
    for _ in range(200):
        lo = sp.Rational(rng.randint(-10**6, 10**6), rng.randint(1, 1000))
        pairs.append((lo, lo + sp.Rational(rng.randint(1, 1000), 10**rng.randint(1, 6))))
    for av, bv in pairs:
        n_ = sp.floor(1 / (bv - av)) + 1
        m_ = sp.floor(n_ * av) + 1
        assert n_ * bv - n_ * av > 1
        assert n_ * av < m_ <= n_ * av + 1 < n_ * bv
        r_ = sp.Rational(m_, n_)
        assert r_.is_rational and (av < r_) is sp.true and (r_ < bv) is sp.true


# ── Statements outside the labelled blocks ───────────────────────────────────


def test_thm_sqrt2_irrational_checkable_steps():
    # thm-calc-sqrt2-irrational (policy F): the proof is reviewed, its computations are checked.
    # Why this matters: the diagonal of the unit square has d² = 1² + 1² = 2.
    assert equal(1**2 + 1**2, 2)
    # Step 2: an odd p = 2m + 1 has p² = 4m² + 4m + 1 = 2(2m² + 2m) + 1, odd.
    assert equal((2 * m + 1) ** 2, 4 * m**2 + 4 * m + 1)
    assert equal(4 * m**2 + 4 * m + 1, 2 * (2 * m**2 + 2 * m) + 1)
    assert all((p * p % 2 == 0) == (p % 2 == 0) for p in range(-500, 501))
    # Step 3: p = 2k in p² = 2q² gives q² = 2k².
    assert equal(sp.solve(sp.Eq((2 * k) ** 2, 2 * q**2), q**2)[0], 2 * k**2)
    # Step 4: 2k/2l = k/l, with l = q/2 < q for q > 0.
    ll = sp.Symbol("l", positive=True)
    assert equal((2 * k) / (2 * ll), k / ll)
    qp = sp.Symbol("qp", positive=True)
    assert (qp / 2 < qp) is sp.true
    # The theorem: no p/q with q ≤ 2000 squares to 2, and SymPy agrees that √2 is irrational.
    assert not any(sp.sqrt(2 * qq * qq).is_integer for qq in range(1, 2001))
    assert sp.sqrt(2).is_rational is False
    # rem-calc-sqrt4-rational: p = 2k in p² = 4q² gives k² = q², so k = q for positive k, q.
    kp = sp.Symbol("kp", positive=True)
    assert sp.solve(sp.Eq((2 * kp) ** 2, 4 * qp**2), kp) == [qp]
    assert equal(sp.sqrt(4), 2)


def test_decimals_and_approximations():
    # The number systems: 1/2 = 2/4 = -3/-6; 1/4 = 0.25; 1/3 = 0.333…; √2 = 1.41421…
    assert equal(sp.Rational(1, 2), sp.Rational(2, 4)) and equal(sp.Rational(1, 2), sp.Rational(-3, -6))
    assert equal(sp.Rational(1, 4), sp.Rational(25, 100))
    assert decimal_digits(sp.Rational(1, 3), 6) == [3] * 6
    assert sp.floor(sp.sqrt(2) * 10**5) == 141421
    # 0.1\overline{25} = 0.1252525…: digits of 1/10 + (25/1000)/(1 - 1/100).
    v = sp.Rational(1, 10) + sp.summation(sp.Rational(25) / (10 * 100**n), (n, 1, oo))
    assert decimal_digits(v, 9) == [1, 2, 5, 2, 5, 2, 5, 2, 5]
    # Long division of p by q: the remainders lie in 0 … q - 1, so a remainder repeats within
    # q steps (checked for every p/q with q ≤ 60).
    for qq in range(1, 61):
        for pp in range(qq):
            seen, rem_ = set(), pp
            for _ in range(qq + 1):
                if rem_ in seen:
                    break
                seen.add(rem_)
                rem_ = 10 * rem_ % qq
            else:
                raise AssertionError(f"no repeated remainder for {pp}/{qq}")
            assert len(seen) <= qq
    # Common mistake: 1.4142 = 14142/10000, and 1.4142² = 1.99996164 ≠ 2.
    approx = sp.Rational(14142, 10000)
    assert equal(approx**2, sp.Rational(199996164, 10**8))
    assert not equal(approx**2, 2)


def test_interval_examples():
    # Example: [-1, 3) contains -1, 0, 2.9 and √2 but not 3.
    I = solve(sp.And(-1 <= x, x < 3))
    for v in (-1, 0, sp.Rational(29, 10), sp.sqrt(2)):
        assert equal(contains(I, v), sp.true)
    assert equal(contains(I, 3), sp.false)
    # Non-example: {x : x ≠ 0} = (-∞, 0) ∪ (0, ∞).
    assert equal(solve(sp.Ne(x, 0)), sp.Union(sp.Interval.open(-oo, 0), sp.Interval.open(0, oo)))
    # Common mistakes: {x : x ≥ 3} = [3, ∞); 2.5, √5 and π lie in (2, 5); its integers are 3, 4.
    assert equal(solve(x >= 3), sp.Interval(3, oo))
    J = solve(sp.And(2 < x, x < 5))
    for v in (sp.Rational(5, 2), sp.sqrt(5), sp.pi):
        assert equal(contains(J, v), sp.true)
    assert equal(sp.FiniteSet(*J.intersect(sp.S.Integers)), sp.FiniteSet(3, 4))


def test_rigorous_track_claims():
    # Upper bounds of [0, 1): 1, 2, 100 are; 0.9 is not, because 0.95 ∈ [0, 1).
    I = sp.Interval.Ropen(0, 1)
    for ub in (1, 2, 100):
        assert I.sup <= ub
    assert equal(contains(I, sp.Rational(95, 100)), sp.true) and sp.Rational(95, 100) > sp.Rational(9, 10)
    # sup [0, 1) = 1: for u < 1, max(0, (u + 1)/2) lies in [0, 1) and exceeds u.
    assert equal(I.sup, 1)
    rng = random.Random(2)
    for _ in range(300):
        u_ = sp.Rational(rng.randint(-10**6, 10**6 - 1), 10**6)
        w_ = sp.Max(0, (u_ + 1) / 2)
        assert equal(contains(I, w_), sp.true) and w_ > u_
    # Completeness gives √2: S = {x ≥ 0 : x² < 2} has 1 ∈ S, is bounded by 2, and sup S = √2.
    S = solve(sp.And(x >= 0, x**2 < 2))
    assert equal(contains(S, 1), sp.true) and S.sup <= 2
    assert equal(S.sup, sp.sqrt(2))
    # Case s² < 2: h = (2 - s²)/(2s + 2) gives s² + h(2s + 2) = 2, and 0 < h < 1 on 1 ≤ s < √2.
    h1 = (2 - s**2) / (2 * s + 2)
    assert equal(s**2 + h1 * (2 * s + 2), 2)
    assert equal((s + h1) ** 2, s**2 + 2 * s * h1 + h1**2)
    hs = sp.Interval.Ropen(1, sp.sqrt(2))
    assert sp.maximum(h1, s, hs) < 1 and sp.minimum(h1, s, hs) >= 0
    assert equal(contains(sp.solveset(h1 > 0, s, hs), 1), sp.true)
    # Case s² > 2: h = (s² - 2)/(2s) gives s - h = (s² + 2)/(2s) and (s - h)² = 2 + h².
    h2 = (s**2 - 2) / (2 * s)
    assert equal(s - h2, (s**2 + 2) / (2 * s))
    assert equal((s - h2) ** 2, 2 + h2**2)
    # Both h are rational when s is: the gap in Q.
    # In Q: for rational u, both h are rational; u + h1 ∈ S_Q when u² < 2, and u - h2 is a smaller
    # positive rational upper bound when u² > 2.
    for u_ in (sp.Rational(7, 5), sp.Rational(141, 100), sp.Rational(3, 2), sp.Rational(142, 100)):
        if u_**2 < 2:
            v_ = u_ + h1.subs(s, u_)
            assert v_.is_rational and v_ > u_ and v_**2 < 2
        else:
            v_ = u_ - h2.subs(s, u_)
            assert v_.is_rational and 0 < v_ < u_ and v_**2 > 2
