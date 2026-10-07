"""Verification tests for content/calculus/preliminaries/functions.md (calc-functions).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
is derived here from the statements (natural domains with `continuous_domain` and, independently,
from the conditions "radicand ≥ 0" and "denominator ≠ 0"; ranges with `function_range`; even/odd
from f(−x) against ±f(x); monotonicity from the definition, i.e. the sign of f(x₂) − f(x₁)).
Answers are read with answer(label).

Monotonicity: the page proves every claim from the definition (def-calc-monotone), and derivatives
come later in the course (its "Looking ahead" admonition). The tests check the definition directly;
where they also look at the sign of the derivative, that is only an independent cross-check on
SymPy's side, not a step the page uses.
"""

import sympy as sp
from sympy.calculus.util import continuous_domain, function_range

from mathcheck import answer, covers, equal, equal_on_domain, x, y

R = sp.S.Reals
oo = sp.oo

# x₁ < x₂ written as x₂ = x₁ + d with d > 0; the bounds on x₁ come from each claim.
d = sp.Symbol("d", positive=True)
p = sp.Symbol("p", positive=True)


def natural_domain(radicands=(), denominators=()):
    """{x real : every radicand ≥ 0 and every denominator ≠ 0}, from the conditions themselves."""
    dom = R
    for q in radicands:
        dom = dom.intersect(sp.solveset(q >= 0, x, R))
    for q in denominators:
        dom = dom - sp.solveset(sp.Eq(q, 0), x, R)
    return dom


def reflect(S):
    """{−x : x ∈ S}."""
    return sp.imageset(sp.Lambda(x, -x), S)


def is_symmetric(S):
    """S = −S (equal() raises if SymPy cannot decide, so `not is_symmetric` is never vacuous)."""
    return equal(S, reflect(S))


@covers("eg-calc-functions-natural-domain")
def test_eg_calc_functions_natural_domain():
    f = sp.sqrt(x + 2) / (x - 3)
    # Step 1: √(x + 2) is real iff x ≥ −2.
    assert equal(sp.solveset(x + 2 >= 0, x, R), sp.Interval(-2, oo))
    # Step 2: x − 3 ≠ 0 iff x ≠ 3.
    assert equal(sp.solveset(sp.Eq(x - 3, 0), x, R), sp.FiniteSet(3))
    # Step 3 (boxed): both conditions, computed two ways.
    boxed = sp.Union(sp.Interval.Ropen(-2, 3), sp.Interval.open(3, oo))
    assert equal(natural_domain([x + 2], [x - 3]), boxed)
    assert equal(continuous_domain(f, x, R), boxed)
    # Check line: f(−2) = 0/(−5) = 0; x = −3 needs √(−1) (not real); x = 3 divides by zero.
    assert equal(f.subs(x, -2), 0)
    assert f.subs(x, -3).is_real is False
    assert f.subs(x, 3).has(sp.zoo)


@covers("eg-calc-functions-range-quadratic")
def test_eg_calc_functions_range_quadratic():
    f = x**2 - 4 * x + 5
    # Step 1: completing the square.
    assert equal(f, (x - 2) ** 2 + 1)
    # Step 2: f(x) − 1 = (x − 2)² ≥ 0 for every real x.
    assert sp.factor(f - 1).is_nonnegative
    # Step 3: x = 2 + √(y − 1) has f(x) = y for every y ≥ 1.
    assert equal_on_domain(f.subs(x, 2 + sp.sqrt(y - 1)), y, y, sp.Interval(1, oo))
    # Step 4 (boxed): the range, from SymPy.
    assert equal(function_range(f, x, R), sp.Interval(1, oo))
    # Check line: y = 10 gives x = 5, f(5) = 10; the smallest value is f(2) = 1.
    assert equal(2 + sp.sqrt(10 - 1), 5)
    assert equal(f.subs(x, 5), 10)
    assert equal(f.subs(x, 2), 1)


@covers("eg-calc-functions-even-odd")
def test_eg_calc_functions_even_odd():
    # 1. f(x) = x³ − x: domain ℝ, f(−x) = −x³ + x = −f(x): odd.
    f = x**3 - x
    assert equal(f.subs(x, -x), -x**3 + x)
    assert equal(f.subs(x, -x), -f)
    assert not equal(f.subs(x, -x), f)  # and not even (so the answer "odd" is the only one)
    # 2. g(x) = 1/(x² − 1): domain ℝ \ {±1}, symmetric; g(−x) = g(x): even.
    g = 1 / (x**2 - 1)
    dom_g = continuous_domain(g, x, R)
    assert equal(dom_g, R - sp.FiniteSet(-1, 1))
    assert is_symmetric(dom_g)
    assert equal(g.subs(x, -x), g)
    # 3. h(x) = x² + x: h(1) = 2, h(−1) = 0, so neither even nor odd.
    h = x**2 + x
    assert equal(h.subs(x, 1), 2)
    assert equal(h.subs(x, -1), 0)
    assert not equal(h.subs(x, -1), h.subs(x, 1))
    assert not equal(h.subs(x, -1), -h.subs(x, 1))
    # 4. k = x² on [−1, 2]: 2 ∈ dom k but −2 ∉ dom k, so the domain is not symmetric.
    dom_k = sp.Interval(-1, 2)
    assert dom_k.contains(2) is sp.true and dom_k.contains(-2) is sp.false
    assert not is_symmetric(dom_k)
    # Check line: f(2) = 6, f(−2) = −6; g(3) = 1/8 = g(−3).
    assert equal(f.subs(x, 2), 6)
    assert equal(f.subs(x, -2), -6)
    assert equal(g.subs(x, 3), sp.Rational(1, 8))
    assert equal(g.subs(x, -3), sp.Rational(1, 8))


@covers("eg-calc-functions-monotone")
def test_eg_calc_functions_monotone():
    f = x / (x + 1)
    x1, x2 = sp.symbols("x1 x2", real=True)
    # Step 1: both displayed forms of f(x₂) − f(x₁).
    diff = f.subs(x, x2) - f.subs(x, x1)
    assert equal(diff, (x2 * (x1 + 1) - x1 * (x2 + 1)) / ((x1 + 1) * (x2 + 1)))
    assert equal(diff, (x2 - x1) / ((x1 + 1) * (x2 + 1)))
    # Step 2: on (−1, ∞), x₁ = −1 + p, x₂ = x₁ + d with p, d > 0: the difference is positive.
    on_right = sp.simplify(diff.subs({x1: -1 + p, x2: -1 + p + d}))
    assert on_right.is_positive
    # Step 3: dom f = (−∞, −1) ∪ (−1, ∞).
    dom = R - sp.FiniteSet(-1)
    assert equal(natural_domain(denominators=[x + 1]), dom)
    assert equal(continuous_domain(f, x, R), dom)
    # On (−∞, −1): x₂ = −1 − p, x₁ = x₂ − d; the difference is positive there too.
    on_left = sp.simplify(diff.subs({x2: -1 - p, x1: -1 - p - d}))
    assert on_left.is_positive
    # Not increasing on dom f: −2 < 0 but f(−2) = 2 > 0 = f(0).
    assert equal(f.subs(x, -2), 2)
    assert equal(f.subs(x, 0), 0)
    assert f.subs(x, -2) > f.subs(x, 0)
    # Cross-check only (the page does not use derivatives): f'(x) = 1/(x + 1)² > 0 on each piece.
    # (sp.is_increasing(f, dom) says True on the whole union, because it only looks at the sign
    # of f': exactly the page's point that the definition compares any two points of dom f.)
    assert sp.is_strictly_increasing(f, sp.Interval.open(-1, oo))
    assert sp.is_strictly_increasing(f, sp.Interval.open(-oo, -1))
    # Check line: f(0) = 0, f(1) = 1/2, f(3) = 3/4.
    assert equal(f.subs(x, 1), sp.Rational(1, 2))
    assert equal(f.subs(x, 3), sp.Rational(3, 4))


@covers("eg-calc-functions-pen")
def test_eg_calc_functions_pen():
    # Step 1, the model: two sides of x m meet the wall, so the third side is 40 − 2x m.
    third = 40 - 2 * x
    assert equal(2 * x + third, 40)
    A = x * third
    assert equal(A, x * (40 - 2 * x))
    # Step 2: a pen needs x > 0 and 40 − 2x > 0.
    dom = sp.And(x > 0, third > 0).as_set()
    assert equal(dom, sp.Interval.open(0, 20))
    # Step 3: completing the square, and the range on (0, 20).
    assert equal(A, 40 * x - 2 * x**2)
    assert equal(A, 200 - 2 * (x - 10) ** 2)
    assert equal(function_range((x - 10) ** 2, x, dom), sp.Interval.Ropen(0, 100))
    assert equal(function_range(A, x, dom), sp.Interval.Lopen(0, 200))
    # Converse: for 0 < a ≤ 200, x = 10 − √((200 − a)/2) lies in (0, 10] and A(x) = a.
    a = sp.Symbol("a", real=True)
    xa = 10 - sp.sqrt((200 - a) / 2)
    assert equal(function_range(xa, a, sp.Interval.Lopen(0, 200)), sp.Interval.Lopen(0, 10))
    assert equal_on_domain(A.subs(x, xa), a, a, sp.Interval.Lopen(0, 200))
    # The largest pen: 200 m² at x = 10.
    assert equal(sp.maximum(A, x, dom), 200)
    assert equal(sp.solveset(sp.Eq(A, 200), x, dom), sp.FiniteSet(10))
    # The natural domain of x(40 − 2x) is all of ℝ.
    assert equal(continuous_domain(A, x, R), R)
    # Check line: A(10) = 200, A(5) = 150 = 200 − 2·5².
    assert equal(A.subs(x, 10), 200)
    assert equal(A.subs(x, 5), 150)
    assert equal(A.subs(x, 5), 200 - 2 * 5**2)


@covers("exr-calc-functions-domain-root")
def test_exr_calc_functions_domain_root():
    f = sp.sqrt(6 - 2 * x)
    expected = natural_domain([6 - 2 * x])
    assert equal(continuous_domain(f, x, R), expected)
    assert equal(answer("exr-calc-functions-domain-root"), expected)


@covers("exr-calc-functions-domain-rational")
def test_exr_calc_functions_domain_rational():
    g = (x + 1) / (x**2 - 4)
    expected = natural_domain(denominators=[x**2 - 4])
    assert equal(continuous_domain(g, x, R), expected)
    assert equal(answer("exr-calc-functions-domain-rational"), expected)


@covers("exr-calc-functions-odd-check")
def test_exr_calc_functions_odd_check():
    f = x**5 - x**3 + 1
    # Domain ℝ (symmetric); odd iff f(−x) + f(x) is identically 0.
    residual = sp.expand(f.subs(x, -x) + f)
    is_odd = residual.is_zero
    assert is_odd is not None
    assert equal(answer("exr-calc-functions-odd-check"), sp.true if is_odd else sp.false)


@covers("exr-calc-functions-vertical-line")
def test_exr_calc_functions_vertical_line():
    # A curve is the graph of a function of x iff no vertical line x = c meets it twice.
    # For each c, the heights on x = c are the real solutions y of c² + y² = 1.
    c = sp.Symbol("c", real=True)
    heights = sp.solveset(c**2 + y**2 - 1, y, R)
    # Find the c with two heights: c ∈ (−1, 1) gives y = ±√(1 − c²), two different numbers.
    two = sp.solveset(1 - c**2 > 0, c, R)
    assert equal(two, sp.Interval.open(-1, 1))
    at_zero = heights.subs(c, 0)
    assert equal(at_zero, sp.FiniteSet(-1, 1))
    is_graph = len(at_zero) <= 1
    assert equal(answer("exr-calc-functions-vertical-line"), sp.true if is_graph else sp.false)


@covers("exr-calc-functions-box-domain")
def test_exr_calc_functions_box_domain():
    # Height x > 0 and base side 30 − 2x > 0.
    expected = sp.And(x > 0, 30 - 2 * x > 0).as_set()
    assert equal(answer("exr-calc-functions-box-domain"), expected)


@covers("exr-calc-functions-box-volume")
def test_exr_calc_functions_box_volume():
    # Base: a square of side 30 − 2x; height x.
    base_side, height = 30 - 2 * x, x
    expected = base_side**2 * height
    assert equal(answer("exr-calc-functions-box-volume"), expected)
    # The solution's example: x = 5 gives 20 × 20 × 5 = 2000 cm³.
    assert equal(expected.subs(x, 5), 20 * 20 * 5)


@covers("exr-calc-functions-range-reciprocal")
def test_exr_calc_functions_range_reciprocal():
    f = 1 / (x**2 + 1)
    dom = continuous_domain(f, x, R)
    assert equal(dom, R)
    expected = function_range(f, x, dom)
    # Cross-check: the y with a real solution of f(x) = y are those with 1/y − 1 ≥ 0, y ≠ 0.
    yy = sp.Symbol("yy", real=True)
    reachable = sp.solveset(1 / yy - 1 >= 0, yy, R - sp.FiniteSet(0))
    assert equal(expected, reachable)
    assert equal(answer("exr-calc-functions-range-reciprocal"), expected)


@covers("exr-calc-functions-range-quotient")
def test_exr_calc_functions_range_quotient():
    g = (2 * x + 1) / (x - 1)
    dom = continuous_domain(g, x, R)
    assert equal(dom, R - sp.FiniteSet(1))
    expected = function_range(g, x, dom)
    # Cross-check: y is a value iff g(x) = y has a solution x in the domain.
    sols = sp.solve(sp.Eq(g, y), x)
    assert len(sols) == 1
    inverse = sols[0]
    bad_y = sp.solveset(sp.denom(sp.together(inverse)), y, R)  # where that solution is undefined
    assert equal(sp.solveset(sp.Eq(g, bad_y.args[0]), x, dom), sp.S.EmptySet)  # no solution there
    assert equal(sp.solveset(sp.Eq(inverse, 1), y, R), sp.S.EmptySet)  # the solution is never x = 1
    assert equal(expected, R - bad_y)
    assert equal(answer("exr-calc-functions-range-quotient"), expected)


@covers("exr-calc-functions-monotone-parabola")
def test_exr_calc_functions_monotone_parabola():
    f = x**2 - 2 * x
    S = sp.Interval(0, oo)
    # From the definition: f is increasing on S iff no x₁ < x₂ in S has f(x₁) > f(x₂).
    # With x₁ = 0, the x₂ > 0 where f(x₂) < f(0) form a non-empty set, so f is not increasing on S.
    below = sp.solveset(f < f.subs(x, 0), x, sp.Interval.open(0, oo))
    assert equal(below, sp.Interval.open(0, 2))
    is_increasing = below.is_empty
    # Cross-check only (the page does not use derivatives): f'(x) = 2x − 2 < 0 on [0, 1).
    assert not sp.is_increasing(f, S)
    assert equal(answer("exr-calc-functions-monotone-parabola"), sp.true if is_increasing else sp.false)
    # The solution's full picture: f = (x − 1)² − 1, strictly decreasing on [0, 1], strictly
    # increasing on [1, ∞). From the definition: f(x₂) − f(x₁) = (x₂ − x₁)(x₁ + x₂ − 2).
    assert equal(f, (x - 1) ** 2 - 1)
    x1, x2 = sp.symbols("x1 x2", real=True)
    q = sp.Symbol("q", nonnegative=True)
    diff = f.subs(x, x2) - f.subs(x, x1)
    assert equal(diff, (x2 - x1) * (x1 + x2 - 2))
    # On [0, 1]: x₂ = 1 − q, x₁ = x₂ − d (q ≥ 0, d > 0; x₁ ≥ 0 only shrinks the set).
    assert sp.factor(diff.subs({x2: 1 - q, x1: 1 - q - d})).is_negative
    # On [1, ∞): x₁ = 1 + q, x₂ = x₁ + d.
    assert sp.factor(diff.subs({x1: 1 + q, x2: 1 + q + d})).is_positive


@covers("exr-calc-functions-sqrt-increasing")
def test_exr_calc_functions_sqrt_increasing():
    # Manual answer (a proof): no answer() call; a reviewer's note covers it. Its key claims:
    # for 0 ≤ x₁ < x₂ (x₂ = x₁ + d, d > 0), √x₂ − √x₁ = (x₂ − x₁)/(√x₂ + √x₁) > 0.
    x1 = sp.Symbol("x1", nonnegative=True)
    x2 = x1 + d
    lhs = sp.sqrt(x2) - sp.sqrt(x1)
    rhs = (x2 - x1) / (sp.sqrt(x2) + sp.sqrt(x1))
    assert equal(lhs * (sp.sqrt(x2) + sp.sqrt(x1)), x2 - x1)
    assert (sp.sqrt(x2) + sp.sqrt(x1)).is_positive
    assert rhs.is_positive
    assert equal(lhs, rhs)


@covers("exr-calc-functions-odd-at-zero")
def test_exr_calc_functions_odd_at_zero():
    # Manual answer (a proof): no answer() call; a reviewer's note covers it. Its key claims:
    # f(0) = −f(0) forces f(0) = 0, and x³ + 1 is 1 ≠ 0 at 0 (so it is not odd).
    v = sp.Symbol("v", real=True)  # v = f(0)
    assert equal(sp.solveset(sp.Eq(v, -v), v, R), sp.FiniteSet(0))
    g = x**3 + 1
    assert equal(g.subs(x, 0), 1)
    assert not equal(g.subs(x, 0), 0)
    assert not equal(g.subs(x, -x), -g)


@covers("exr-calc-functions-piecewise-range")
def test_exr_calc_functions_piecewise_range():
    left, right = -x, x**2 - 2 * x
    dom_left, dom_right = sp.Interval.open(-oo, 0), sp.Interval(0, 3)
    assert equal(sp.Union(dom_left, dom_right), sp.Interval(-oo, 3))
    expected = sp.Union(function_range(left, x, dom_left), function_range(right, x, dom_right))
    # The same pieces as images of their intervals, as a cross-check (function_range does not
    # take a Piecewise).
    assert equal(sp.Union(sp.imageset(sp.Lambda(x, left), dom_left),
                          sp.imageset(sp.Lambda(x, right), dom_right)), expected)
    assert equal(answer("exr-calc-functions-piecewise-range"), expected)
    # The sketch: the pieces meet at the origin; lowest point (1, −1); right end (3, 3).
    assert equal(sp.limit(left, x, 0, "-"), right.subs(x, 0))
    assert equal(right.subs(x, 1), -1)
    assert equal(right.subs(x, 3), 3)


@covers("exr-calc-functions-cube-increasing")
def test_exr_calc_functions_cube_increasing():
    # Manual answer (a proof): no answer() call; a reviewer's note covers it. Its key claims:
    # the factorisation, the completed square, and that the second factor is positive when
    # x₁ < x₂ (it is a positive definite quadratic form, zero only at x₁ = x₂ = 0).
    x1, x2 = sp.symbols("x1 x2", real=True)
    second = x2**2 + x1 * x2 + x1**2
    assert equal(x2**3 - x1**3, (x2 - x1) * second)
    assert equal(second, (x1 + x2 / 2) ** 2 + sp.Rational(3, 4) * x2**2)
    zeros = sp.solve([x1 + x2 / 2, x2], [x1, x2], dict=True)
    assert len(zeros) == 1 and equal((zeros[0][x1], zeros[0][x2]), (0, 0))
    # Directly: with x₂ = x₁ + d, d > 0, x₂³ − x₁³ = d(3x₁² + 3x₁d + d²), and the bracket has
    # discriminant 9d² − 12d² = −3d² < 0 in x₁, so it is positive for every real x₁.
    cubic = sp.expand((x1 + d) ** 3 - x1**3)
    assert equal(cubic, d * (3 * x1**2 + 3 * x1 * d + d**2))
    assert equal(sp.discriminant(3 * x1**2 + 3 * x1 * d + d**2, x1), -3 * d**2)


@covers("exr-calc-functions-even-odd-decomposition")
def test_exr_calc_functions_even_odd_decomposition():
    # Manual answer (a proof): no answer() call; a reviewer's note covers it. Its key claims.
    F = sp.Function("f")
    G, H = sp.symbols("G H")  # g(x), h(x) as unknowns
    # Uniqueness: f(x) = G + H and f(−x) = G − H (g even, h odd) has exactly one solution.
    sol = sp.solve([sp.Eq(F(x), G + H), sp.Eq(F(-x), G - H)], [G, H], dict=True)
    assert len(sol) == 1
    g, h = sol[0][G], sol[0][H]
    assert equal(g, (F(x) + F(-x)) / 2)
    assert equal(h, (F(x) - F(-x)) / 2)
    # Existence: g is even, h is odd, g + h = f, for an arbitrary f.
    assert equal(g.subs(x, -x), g)
    assert equal(h.subs(x, -x), -h)
    assert equal(g + h, F(x))
    # The example f(x) = x² + x + 1: g(x) = x² + 1 and h(x) = x, derived from the formulas.
    f = x**2 + x + 1
    ge = (f + f.subs(x, -x)) / 2
    he = (f - f.subs(x, -x)) / 2
    assert equal(ge.subs(x, -x), ge)
    assert equal(he.subs(x, -x), -he)
    assert equal(ge + he, f)
    assert equal(ge, x**2 + 1)
    assert equal(he, x)
