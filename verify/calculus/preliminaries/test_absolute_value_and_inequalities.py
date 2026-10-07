"""Verification tests for content/calculus/preliminaries/absolute-value-and-inequalities.md (calc-absolute-value-inequalities).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Expected values are
derived independently: every solution set comes from SymPy's solveset over the reals (or, for
a conjunction, the intersection of the solvesets of its parts), and the page's printed answer
is read with answer(label). Each solution set is also checked pointwise, with exact arithmetic,
at its endpoints, just either side of them, and on a grid: a point is in the printed set
exactly when it satisfies the inequality. That catches an open/closed endpoint mix-up even if
solveset were wrong.

Claims about all real x and y (the triangle inequality and its relatives) are reduced to one
variable: both sides are positively homogeneous of degree 1 (scaling x and y by c > 0 scales
both by c, asserted below), so a claim for all (x, y) follows from the claim for y in
{-1, 0, 1} and every real x, and solveset decides that over the whole real line.
"""

import random

import pytest
import sympy as sp

from mathcheck import ManualAnswer, a, answer, answer_type, covers, equal, numeric_spot_check, x, y, z

R = sp.S.Reals
oo = sp.oo
EPS = sp.Rational(1, 10**6)
GRID = [sp.Rational(k, 8) for k in range(-80, 81)]  # -10 … 10 in steps of 1/8
c = sp.Symbol("c", positive=True)


def solve_one(cond):
    """The real solution set of one condition in x. solveset cannot handle some inequalities with
    several absolute values (it returns a ConditionSet); then we rewrite each |u| by its two
    cases (u >= 0, u < 0), which is the definition on the page, and solve that."""
    if isinstance(cond, sp.logic.boolalg.BooleanAtom):  # e.g. |x - a| < -2 evaluates to False
        return R if cond else sp.S.EmptySet
    S = sp.solveset(cond, x, R)
    if isinstance(S, sp.ConditionSet):
        cases = sp.piecewise_fold(cond.lhs.rewrite(sp.Piecewise) - cond.rhs.rewrite(sp.Piecewise))
        S = sp.solveset(cond.func(cases, 0), x, R)
    assert not S.has(sp.ConditionSet), f"SymPy cannot solve {cond}"
    return S


def solve(*conditions):
    """The real solution set of the conjunction of `conditions` (relationals in x)."""
    return sp.Intersection(*(solve_one(cond) for cond in conditions)) if len(conditions) > 1 \
        else solve_one(conditions[0])


def holds(conditions, v) -> bool:
    """Every condition holds at x = v, computed exactly. Where a side is undefined (a zero
    denominator), the inequality is not satisfied."""
    for cond in conditions:
        if isinstance(cond, sp.logic.boolalg.BooleanAtom):
            if not cond:
                return False
            continue
        lhs, rhs = cond.lhs.subs(x, v), cond.rhs.subs(x, v)
        if lhs.has(sp.zoo, sp.nan, sp.oo, -sp.oo) or rhs.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
            return False
        if not bool(cond.func(lhs, rhs)):
            return False
    return True


def spot_check(S, *conditions):
    """Pointwise check of a printed solution set S: at each finite endpoint, at endpoint ± 10^-6
    and on the grid, v is in S exactly when the conditions hold at v."""
    points = list(GRID)
    for e in S.boundary:
        if e.is_finite:
            points += [e, e - EPS, e + EPS]
    for v in points:
        assert bool(S.contains(v)) == holds(conditions, v), (
            f"x = {v}: the printed set says {'in' if S.contains(v) else 'out'}, the inequality says "
            f"{'holds' if holds(conditions, v) else 'fails'}")


def check_solution_set(printed, *conditions) -> bool:
    """The printed set equals the solveset of the conditions and passes the pointwise check."""
    spot_check(printed, *conditions)
    return equal(printed, solve(*conditions))


def for_all_x_and_y(violation) -> bool:
    """`violation(x, y)` (a relational, homogeneous of degree 1) has no real solution x for
    y = -1, 0, 1, hence (by homogeneity) for no real x, y."""
    return all(solve(violation(x, yv)) is sp.S.EmptySet for yv in (-1, 0, 1))


# ── The page's results (no @covers: they are not eg-/exr- blocks) ─────────────


def test_absolute_value_definition_and_remark():
    # Definition: the two cases.
    p, q = sp.Symbol("p", positive=True), sp.Symbol("q", negative=True)
    assert equal(sp.Abs(p), p) and equal(sp.Abs(q), -q) and equal(sp.Abs(0), 0)
    # "Example": |-3| = 3 and the distance between -1 and 4 is 5.
    assert equal(sp.Abs(-3), 3) and equal(sp.Abs(-1 - 4), 5)
    # "Non-example": at x = -2, |-x| = 2 = -x and not x; |-x| = x fails for every x < 0.
    assert equal(sp.Abs(2), 2) and equal(sp.Abs(-(-2)), -(-2)) and not equal(sp.Abs(-(-2)), -2)
    assert equal(solve(sp.Eq(sp.Abs(-x), x)), sp.Interval(0, oo))
    # Properties 1-5, case by case.
    assert equal(solve(sp.Abs(x) < 0), sp.S.EmptySet) and equal(solve(sp.Eq(sp.Abs(x), 0)), sp.FiniteSet(0))
    assert equal(sp.Abs(-x), sp.Abs(x))
    for v in (p, q, sp.S.Zero):
        assert equal(sp.Abs(v), sp.Max(v, -v))
    assert equal(solve(x > sp.Abs(x)), sp.S.EmptySet) and equal(solve(-sp.Abs(x) > x), sp.S.EmptySet)
    for xv, yv in ((p, p), (p, q), (q, p), (q, q)):
        assert equal(sp.Abs(xv * yv), sp.Abs(xv) * sp.Abs(yv))
        assert equal(sp.Abs(xv / yv), sp.Abs(xv) / sp.Abs(yv))
    assert equal(sp.Abs(x) ** 2, x**2) and equal(sp.sqrt(x**2), sp.Abs(x))


def test_prop_abs_interval():
    # (a)-(d) against solveset for a grid of centres a and half-widths delta, including delta = 0
    # and delta < 0 (the rigorous track says the proposition holds for every real delta).
    for av in (sp.Integer(-3), sp.Integer(0), sp.Rational(5, 2), sp.Integer(7)):
        for dv in (sp.Integer(-2), sp.Integer(0), sp.Rational(1, 10), sp.Integer(1), sp.Integer(4)):
            lo, hi = av - dv, av + dv
            cases = [
                (sp.Abs(x - av) < dv, sp.Interval.open(lo, hi)),
                (sp.Abs(x - av) <= dv, sp.Interval(lo, hi)),
                (sp.Abs(x - av) > dv, sp.Union(sp.Interval.open(-oo, lo), sp.Interval.open(hi, oo))),
                (sp.Abs(x - av) >= dv, sp.Union(sp.Interval(-oo, lo), sp.Interval(hi, oo))),
            ]
            for cond, rhs in cases:
                assert check_solution_set(rhs, cond), (av, dv, cond)
            # Rigorous track: delta < 0 makes (a) and (b) empty; delta = 0 makes (a) empty and (b) {a}.
            if dv < 0:
                assert equal(solve(cases[0][0]), sp.S.EmptySet) and equal(solve(cases[1][0]), sp.S.EmptySet)
            if dv == 0:
                assert equal(solve(cases[0][0]), sp.S.EmptySet) and equal(solve(cases[1][0]), sp.FiniteSet(av))
    # The proof's key step: the larger of y and -y is < delta iff both are, for y on either side of 0.
    for dv in (-1, 0, 2):
        assert equal(solve(sp.Max(x, -x) < dv), solve(x < dv, -x < dv))


def test_thm_triangle_inequality():
    # Homogeneity: scaling x, y by c > 0 scales every side by c, so y in {-1, 0, 1} suffices.
    assert equal(sp.Abs(c * x + c * y), c * sp.Abs(x + y))
    assert equal(sp.Abs(sp.Abs(c * x) - sp.Abs(c * y)), c * sp.Abs(sp.Abs(x) - sp.Abs(y)))
    # (a) |x + y| <= |x| + |y|
    assert for_all_x_and_y(lambda u, v: sp.Abs(u + v) > sp.Abs(u) + sp.Abs(v))
    # (b) is (a) for x - z and z - y: (x - z) + (z - y) = x - y. Translating all three by t
    # changes nothing, so z = 0 suffices, and then (b) is |x - y| <= |x| + |y|.
    assert equal((x - z) + (z - y), x - y)
    assert for_all_x_and_y(lambda u, v: sp.Abs(u - v) > sp.Abs(u) + sp.Abs(v))
    # (c) ||x| - |y|| <= |x - y|
    assert for_all_x_and_y(lambda u, v: sp.Abs(sp.Abs(u) - sp.Abs(v)) > sp.Abs(u - v))
    # The proof of (c): |x| - |y| <= |x - y| for all x, y, and |y - x| = |x - y|.
    assert for_all_x_and_y(lambda u, v: sp.Abs(u) - sp.Abs(v) > sp.Abs(u - v))
    assert equal(sp.Abs(y - x), sp.Abs(x - y))
    # Exact random spot check of all three, independent of the reduction above.
    rng = random.Random(0)
    for _ in range(300):
        xv, yv, zv = (sp.Rational(rng.randint(-10**4, 10**4), rng.randint(1, 100)) for _ in range(3))
        assert sp.Abs(xv + yv) <= sp.Abs(xv) + sp.Abs(yv)
        assert sp.Abs(xv - yv) <= sp.Abs(xv - zv) + sp.Abs(zv - yv)
        assert sp.Abs(sp.Abs(xv) - sp.Abs(yv)) <= sp.Abs(xv - yv)


def test_rigorous_track_equality_case():
    # |x + y| = |x| + |y| iff xy >= 0: for y = 1 that is x >= 0, for y = -1 x <= 0, for y = 0 all x.
    eq = lambda v: sp.Eq(sp.Abs(x + v), sp.Abs(x) + sp.Abs(v))  # noqa: E731
    assert equal(solve(eq(1)), solve(x * 1 >= 0))
    assert equal(solve(eq(-1)), solve(x * -1 >= 0))
    assert equal(solve(eq(0)), R)
    # The displayed squares.
    assert equal(sp.Abs(x + y) ** 2, x**2 + 2 * x * y + y**2)
    assert equal((sp.Abs(x) + sp.Abs(y)) ** 2, x**2 + 2 * sp.Abs(x * y) + y**2)


def test_why_this_matters_and_common_mistakes():
    # |x - 20| <= 0.05 iff 19.95 <= x <= 20.05
    assert equal(solve(sp.Abs(x - 20) <= sp.Rational(5, 100)), sp.Interval(sp.Rational(1995, 100), sp.Rational(2005, 100)))
    # Forgetting to reverse: -2x < 4 gives x > -2; x = 0 satisfies -2x < 4 but not x < -2.
    assert equal(solve(-2 * x < 4), sp.Interval.open(-2, oo))
    assert holds([-2 * x < 4], 0) and not holds([x < -2], 0)
    # Not additive: |3 + (-3)| = 0, |3| + |-3| = 6.
    assert equal(sp.Abs(3 + (-3)), 0) and equal(sp.Abs(3) + sp.Abs(-3), 6)
    # An "or" as a chain: -2 > x - 3 > 2 has no solutions; |x - 3| > 2 is (-oo, 1) U (5, oo).
    assert equal(solve(-2 > x - 3, x - 3 > 2), sp.S.EmptySet)
    assert check_solution_set(sp.Union(sp.Interval.open(-oo, 1), sp.Interval.open(5, oo)), sp.Abs(x - 3) > 2)
    # Dividing by an unknown: x = -1 satisfies x^2 > 3x but not x > 3; x(x - 3) > 0 is (-oo, 0) U (3, oo).
    assert holds([x**2 > 3 * x], -1) and not holds([x > 3], -1)
    assert equal(x**2 - 3 * x, x * (x - 3))
    assert check_solution_set(sp.Union(sp.Interval.open(-oo, 0), sp.Interval.open(3, oo)), x**2 > 3 * x)


# ── Worked examples ──────────────────────────────────────────────────────────


@covers("eg-calc-absolute-value-inequalities-linear")
def test_eg_calc_absolute_value_inequalities_linear():
    original = 3 - 2 * x < 7
    # Step 1: subtract 3 from both sides: -2x < 4 (same solution set).
    assert equal((3 - 2 * x) - 3, -2 * x) and equal(7 - 3, 4)
    assert equal(solve(-2 * x < 4), solve(original))
    # Step 2: divide by -2 and reverse: x > -2.
    assert equal(solve(x > -2), solve(original))
    # Boxed: (-2, oo).
    assert check_solution_set(sp.Interval.open(-2, oo), original)
    # Check line: x = 0 gives 3 < 7; x = -2 gives 7, not < 7; x = -3 gives 9 < 7, false.
    assert equal(3 - 2 * 0, 3) and holds([original], 0)
    assert equal(3 - 2 * (-2), 7) and not holds([original], -2)
    assert equal(3 - 2 * (-3), 9) and not holds([original], -3)


@covers("eg-calc-absolute-value-inequalities-quadratic")
def test_eg_calc_absolute_value_inequalities_quadratic():
    p = x**2 - x - 6
    original = p <= 0
    # Step 1: factor; the zeros are -2 and 3.
    assert equal(sp.factor(p), (x + 2) * (x - 3))
    assert equal(sp.solveset(p, x, R), sp.FiniteSet(-2, 3))
    # Step 2: the sign table, row by row, at a point of each interval (x < -2, -2 < x < 3, x > 3).
    table = {x + 2: (-1, 1, 1), x - 3: (-1, -1, 1), (x + 2) * (x - 3): (1, -1, 1)}
    for f, signs in table.items():
        for (lo, hi), sign in zip(((-oo, -2), (-2, 3), (3, oo)), signs):
            interval = sp.Interval.open(lo, hi)
            # one sign on the whole interval: f has no zero inside it, and the sign at a point
            assert sp.solveset(f, x, interval) is sp.S.EmptySet
            assert equal(sp.sign(f.subs(x, interval.inf + 1 if interval.inf.is_finite else interval.sup - 1)), sign)
    # Step 3: negative on (-2, 3), zero at -2 and 3.
    assert equal(solve(p < 0), sp.Interval.open(-2, 3))
    # Boxed: [-2, 3].
    assert check_solution_set(sp.Interval(-2, 3), original)
    # Check line: x = 0 gives -6; x = 4 gives 6 (excluded); x = -2 gives 0.
    assert equal(p.subs(x, 0), -6) and equal(p.subs(x, 4), 6) and equal(p.subs(x, -2), 0)
    assert equal(16 - 4 - 6, p.subs(x, 4)) and equal(4 + 2 - 6, p.subs(x, -2))


@covers("eg-calc-absolute-value-inequalities-abs-less")
def test_eg_calc_absolute_value_inequalities_abs_less():
    original = sp.Abs(2 * x - 5) < 3
    S = solve(original)
    # Step 1: -3 < 2x - 5 < 3.
    assert equal(solve(-3 < 2 * x - 5, 2 * x - 5 < 3), S)
    # Step 2: add 5: 2 < 2x < 8.
    assert equal(-3 + 5, 2) and equal(3 + 5, 8)
    assert equal(solve(2 < 2 * x, 2 * x < 8), S)
    # Step 3: divide by 2: 1 < x < 4.
    assert equal(solve(1 < x, x < 4), S)
    # Boxed: (1, 4).
    assert check_solution_set(sp.Interval.open(1, 4), original)
    # Distance reading: |2x - 5| = 2|x - 5/2|; within 3/2 of 5/2; (1, 4) has midpoint 5/2, half-width 3/2.
    assert equal(sp.Abs(2 * x - 5), 2 * sp.Abs(x - sp.Rational(5, 2)))
    assert equal(solve(sp.Abs(x - sp.Rational(5, 2)) < sp.Rational(3, 2)), S)
    assert equal((S.inf + S.sup) / 2, sp.Rational(5, 2)) and equal((S.sup - S.inf) / 2, sp.Rational(3, 2))
    # Check line: x = 2 gives |-1| = 1; x = 1 gives |-3| = 3, not < 3; x = 5 gives 5.
    assert equal(sp.Abs(2 * 2 - 5), 1) and holds([original], 2)
    assert equal(sp.Abs(2 * 1 - 5), 3) and not holds([original], 1)
    assert equal(sp.Abs(2 * 5 - 5), 5) and not holds([original], 5)


@covers("eg-calc-absolute-value-inequalities-abs-greater")
def test_eg_calc_absolute_value_inequalities_abs_greater():
    original = sp.Abs(x + 1) >= 2
    # Step 1: x + 1 = x - (-1).
    assert equal(x + 1, x - (-1))
    # Step 2: proposition (d) with a = -1, delta = 2: x <= a - delta = -3 or x >= a + delta = 1.
    assert equal(-1 - 2, -3) and equal(-1 + 2, 1)
    assert equal(sp.Union(solve(x <= -3), solve(x >= 1)), solve(original))
    # Boxed: (-oo, -3] U [1, oo).
    assert check_solution_set(sp.Union(sp.Interval(-oo, -3), sp.Interval(1, oo)), original)
    # Check line: x = 0 gives 1 (excluded); x = 1 gives 2; x = -4 gives |-3| = 3.
    assert equal(sp.Abs(0 + 1), 1) and not holds([original], 0)
    assert equal(sp.Abs(1 + 1), 2) and holds([original], 1)
    assert equal(sp.Abs(-4 + 1), 3) and holds([original], -4)


@covers("eg-calc-absolute-value-inequalities-punctured")
def test_eg_calc_absolute_value_inequalities_punctured():
    tenth = sp.Rational(1, 10)
    conditions = (0 < sp.Abs(x - 2), sp.Abs(x - 2) < tenth)
    # Step 1: |x - 2| < 0.1 iff 1.9 < x < 2.1.
    assert equal(solve(conditions[1]), sp.Interval.open(sp.Rational(19, 10), sp.Rational(21, 10)))
    # Step 2: 0 < |x - 2| iff x != 2.
    assert equal(solve(conditions[0]), R - sp.FiniteSet(2))
    # Step 3 and boxed: (1.9, 2) U (2, 2.1).
    boxed = sp.Union(sp.Interval.open(sp.Rational(19, 10), 2), sp.Interval.open(2, sp.Rational(21, 10)))
    assert equal(boxed, sp.Interval.open(sp.Rational(19, 10), sp.Rational(21, 10)) - sp.FiniteSet(2))
    assert check_solution_set(boxed, *conditions)
    # In general, for delta > 0: 0 < |x - a| < delta iff x in (a - delta, a) U (a, a + delta).
    for av in (sp.Integer(-1), sp.Integer(0), sp.Rational(7, 3)):
        for dv in (sp.Rational(1, 100), sp.Integer(1), sp.Integer(5)):
            punctured = sp.Union(sp.Interval.open(av - dv, av), sp.Interval.open(av, av + dv))
            assert check_solution_set(punctured, 0 < sp.Abs(x - av), sp.Abs(x - av) < dv)
    # Check line: x = 2 gives 0, not > 0; x = 2.05 gives 0 < 0.05 < 0.1; x = 2.1 gives 0.1, not < 0.1.
    assert equal(sp.Abs(2 - 2), 0) and not holds(conditions, 2)
    assert equal(sp.Abs(sp.Rational(205, 100) - 2), sp.Rational(5, 100)) and holds(conditions, sp.Rational(205, 100))
    assert equal(sp.Abs(sp.Rational(21, 10) - 2), tenth) and not holds(conditions, sp.Rational(21, 10))


@covers("eg-calc-absolute-value-inequalities-triangle-bound")
def test_eg_calc_absolute_value_inequalities_triangle_bound():
    near = solve(sp.Abs(x - 2) < 1)  # the hypothesis |x - 2| < 1
    # Step 1: x + 2 = (x - 2) + 4.
    assert equal(x + 2, (x - 2) + 4)
    # Step 2: |x + 2| <= |x - 2| + |4| = |x - 2| + 4 for every x (no violation), and < 1 + 4 = 5
    # whenever |x - 2| < 1.
    assert equal(sp.Abs(4), 4) and equal(1 + 4, 5)
    assert equal(solve(sp.Abs(x + 2) > sp.Abs(x - 2) + 4), sp.S.EmptySet)
    assert near.is_subset(solve(sp.Abs(x + 2) < 5)) is True
    assert equal(sp.Intersection(near, solve(sp.Abs(x + 2) >= 5)), sp.S.EmptySet)
    # Step 3: |x^2 - 4| = |(x - 2)(x + 2)| = |x - 2||x + 2| <= 5|x - 2| when |x - 2| < 1.
    assert equal(sp.factor(x**2 - 4), (x - 2) * (x + 2))
    assert equal(sp.Abs((x - 2) * (x + 2)), sp.Abs(x - 2) * sp.Abs(x + 2))
    assert numeric_spot_check(sp.Abs(x**2 - 4), sp.Abs(x - 2) * sp.Abs(x + 2), x, (-10, 10))
    assert equal(sp.Intersection(near, solve(sp.Abs(x**2 - 4) > 5 * sp.Abs(x - 2))), sp.S.EmptySet)
    # Check line: x = 2.9: |4.9| = 4.9 < 5, and |2.9^2 - 4| = 4.41 <= 5 * 0.9 = 4.5.
    xv = sp.Rational(29, 10)
    assert near.contains(xv) is sp.true
    assert equal(sp.Abs(xv + 2), sp.Rational(49, 10)) and sp.Rational(49, 10) < 5
    assert equal(sp.Abs(xv**2 - 4), sp.Rational(441, 100))
    assert equal(5 * sp.Abs(xv - 2), sp.Rational(45, 10)) and sp.Rational(441, 100) <= sp.Rational(45, 10)


# ── Exercises ────────────────────────────────────────────────────────────────


@covers("exr-calc-absolute-value-inequalities-evaluate")
def test_exr_calc_absolute_value_inequalities_evaluate():
    expected = sp.Abs(-7) + sp.Abs(3 - 8) - sp.Abs((-2) * 4)
    assert equal(answer("exr-calc-absolute-value-inequalities-evaluate"), expected)


@covers("exr-calc-absolute-value-inequalities-linear")
def test_exr_calc_absolute_value_inequalities_linear():
    printed = answer("exr-calc-absolute-value-inequalities-linear")
    assert check_solution_set(printed, 5 - 3 * x >= 11)


@covers("exr-calc-absolute-value-inequalities-abs-to-interval")
def test_exr_calc_absolute_value_inequalities_abs_to_interval():
    printed = answer("exr-calc-absolute-value-inequalities-abs-to-interval")
    assert check_solution_set(printed, sp.Abs(x - 4) < sp.Rational(1, 2))


@covers("exr-calc-absolute-value-inequalities-abs-closed")
def test_exr_calc_absolute_value_inequalities_abs_closed():
    printed = answer("exr-calc-absolute-value-inequalities-abs-closed")
    assert check_solution_set(printed, sp.Abs(3 * x + 1) <= 5)


@covers("exr-calc-absolute-value-inequalities-interval-to-abs")
def test_exr_calc_absolute_value_inequalities_interval_to_abs():
    centre, half_width = answer("exr-calc-absolute-value-inequalities-interval-to-abs")
    # Independently: (a - d, a + d) = (-1, 5) has exactly one solution with d > 0.
    A, D = sp.symbols("A D", real=True)
    solutions = sp.solve([sp.Eq(A - D, -1), sp.Eq(A + D, 5)], [A, D], dict=True)
    assert len(solutions) == 1 and solutions[0][D] > 0
    assert equal((centre, half_width), (solutions[0][A], solutions[0][D]))
    # And the printed pair really describes the interval.
    assert check_solution_set(sp.Interval.open(-1, 5), sp.Abs(x - centre) < half_width)


@covers("exr-calc-absolute-value-inequalities-abs-outside")
def test_exr_calc_absolute_value_inequalities_abs_outside():
    printed = answer("exr-calc-absolute-value-inequalities-abs-outside")
    assert check_solution_set(printed, sp.Abs(2 * x - 3) > 5)


@covers("exr-calc-absolute-value-inequalities-quadratic")
def test_exr_calc_absolute_value_inequalities_quadratic():
    printed = answer("exr-calc-absolute-value-inequalities-quadratic")
    assert check_solution_set(printed, x**2 + 2 * x - 8 < 0)


@covers("exr-calc-absolute-value-inequalities-cubic")
def test_exr_calc_absolute_value_inequalities_cubic():
    printed = answer("exr-calc-absolute-value-inequalities-cubic")
    assert check_solution_set(printed, x**3 >= 4 * x)
    # The solution's claim: dividing by x would have lost part of the set (x <= 0 there).
    divided = solve(x**2 >= 4, x > 0)  # what is left if one divides by x as if it were positive
    assert not equal(divided, printed)


@covers("exr-calc-absolute-value-inequalities-rational")
def test_exr_calc_absolute_value_inequalities_rational():
    printed = answer("exr-calc-absolute-value-inequalities-rational")
    assert check_solution_set(printed, (x - 1) / (x + 2) <= 0)
    # The excluded endpoint is where the quotient is undefined.
    assert ((x - 1) / (x + 2)).subs(x, -2).has(sp.zoo)


@covers("exr-calc-absolute-value-inequalities-punctured")
def test_exr_calc_absolute_value_inequalities_punctured():
    printed = answer("exr-calc-absolute-value-inequalities-punctured")
    assert check_solution_set(printed, 0 < sp.Abs(x + 1), sp.Abs(x + 1) < sp.Rational(1, 2))


@covers("exr-calc-absolute-value-inequalities-difference-bound")
def test_exr_calc_absolute_value_inequalities_difference_bound():
    # Decide the claim: |x - y| > |x| + |y| has no real solution (homogeneity, see the module docstring).
    assert equal(sp.Abs(c * x - c * y), c * sp.Abs(x - y))
    holds_for_all = for_all_x_and_y(lambda u, v: sp.Abs(u - v) > sp.Abs(u) + sp.Abs(v))
    assert equal(answer("exr-calc-absolute-value-inequalities-difference-bound"), sp.true if holds_for_all else sp.false)


@covers("exr-calc-absolute-value-inequalities-compare-distances")
def test_exr_calc_absolute_value_inequalities_compare_distances():
    original = sp.Abs(x - 1) < sp.Abs(x + 3)
    printed = answer("exr-calc-absolute-value-inequalities-compare-distances")
    assert check_solution_set(printed, original)
    # The solution's steps: squaring is an equivalence here, and (x + 3)^2 - (x - 1)^2 = 8x + 8.
    assert equal(solve((x - 1) ** 2 < (x + 3) ** 2), solve(original))
    assert equal(sp.expand((x + 3) ** 2 - (x - 1) ** 2), 8 * x + 8)
    # The picture: the midpoint of -3 and 1 is -1.
    assert equal(sp.Rational(-3 + 1, 2), -1)


@covers("exr-calc-absolute-value-inequalities-close-points")
def test_exr_calc_absolute_value_inequalities_close_points():
    # The answer is a proof: answer() has nothing to read, so this test cannot cover the label
    # (only the reviewer's maths.manual_checked note can). Check the key claims anyway.
    assert answer_type("exr-calc-absolute-value-inequalities-close-points") == "manual"
    with pytest.raises(ManualAnswer):
        answer("exr-calc-absolute-value-inequalities-close-points")
    # Triangle inequality (b) with z = a, and |a - y| = |y - a|.
    assert equal((x - a) + (a - y), x - y) and equal(sp.Abs(a - y), sp.Abs(y - a))
    # The claim itself, reduced to u = x - a, v = y - a and (by scaling) delta = 2: if |u| < 1
    # and |v| < 1 then |u - v| < 2. For each v, no u in (-1, 1) violates it; plus random exact points.
    u = sp.Symbol("u", real=True)
    for v in [sp.Rational(k, 16) for k in range(-15, 16)]:
        assert sp.solveset(sp.Abs(u - v) >= 2, u, sp.Interval.open(-1, 1)) is sp.S.EmptySet
    rng = random.Random(1)
    for _ in range(500):
        av = sp.Rational(rng.randint(-1000, 1000), 10)
        dv = sp.Rational(rng.randint(1, 10**4), 100)
        xv = av + dv / 2 * sp.Rational(rng.randint(-999, 999), 1000)
        yv = av + dv / 2 * sp.Rational(rng.randint(-999, 999), 1000)
        assert sp.Abs(xv - yv) < dv


@covers("exr-calc-absolute-value-inequalities-largest-delta")
def test_exr_calc_absolute_value_inequalities_largest_delta():
    printed = answer("exr-calc-absolute-value-inequalities-largest-delta")
    good = solve(sp.Abs(x**2 - 4) < 1)
    # The component of the solution set that contains 2, and the distance from 2 to its ends.
    component = next(i for i in (good.args if isinstance(good, sp.Union) else (good,)) if i.contains(2))
    expected = sp.Min(2 - component.inf, component.sup - 2)
    assert equal(printed, expected)
    # The printed delta works, and no larger one does.
    assert printed > 0
    assert sp.Interval.open(2 - printed, 2 + printed).is_subset(good) is True
    for extra in (sp.Rational(1, 10**9), sp.Rational(1, 1000), sp.Rational(1, 10)):
        assert sp.Interval.open(2 - printed - extra, 2 + printed + extra).is_subset(good) is False
    # The solution's comparison: sqrt(5) - 2 < 2 - sqrt(3), via (sqrt 5 + sqrt 3)^2 = 8 + 2 sqrt 15 < 16.
    assert equal(sp.expand((sp.sqrt(5) + sp.sqrt(3)) ** 2), 8 + 2 * sp.sqrt(15))
    assert sp.sqrt(5) - 2 < 2 - sp.sqrt(3)
