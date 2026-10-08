"""Verification tests for content/calculus/preliminaries/functions.md (calc-functions).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. Every expected value
is derived here from the statements (natural domains with `continuous_domain` and, independently,
from the conditions "radicand ≥ 0" and "denominator ≠ 0"; ranges with `function_range`; even/odd
by def-calc-even-odd, which (since e7202c0) asks for a symmetric domain as part of both
definitions: S = −S is checked with `imageset`, separately from and before the identity
f(−x) = ±f(x); monotonicity from the definition, i.e. the sign of f(x₂) − f(x₁)).
Answers are read with answer(label). The tests at the end, without @covers, check claims in the
prose (definitions, figures, common mistakes, Summary) that no eg-/exr- label owns.

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


def parity(f, dom):
    """def-calc-even-odd: the subset of {"even", "odd"} that f, on dom, satisfies. The domain is
    checked first: if it is not symmetric about 0, f is neither, whatever its formula does."""
    if not is_symmetric(dom):
        return set()
    kinds = set()
    if equal(f.subs(x, -x), f):
        kinds.add("even")
    if equal(f.subs(x, -x), -f):
        kinds.add("odd")
    return kinds


def monotone_kinds(f, S):
    """def-calc-monotone on a finite set S, pair by pair: which of the four properties hold."""
    pairs = [(a, b) for a in S for b in S if a < b]
    return {
        name
        for name, ok in (
            ("increasing", lambda u, v: u <= v),
            ("strictly increasing", lambda u, v: u < v),
            ("decreasing", lambda u, v: u >= v),
            ("strictly decreasing", lambda u, v: u > v),
        )
        if all(bool(ok(f(a), f(b))) for a, b in pairs)
    }


ALL_FOUR = {"increasing", "strictly increasing", "decreasing", "strictly decreasing"}


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
    # 1. f(x) = x³ − x: domain ℝ (symmetric), f(−x) = −x³ + x = −f(x): odd.
    f = x**3 - x
    dom_f = continuous_domain(f, x, R)
    assert equal(dom_f, R) and is_symmetric(dom_f)
    assert equal(f.subs(x, -x), -x**3 + x)
    assert equal(f.subs(x, -x), -f)
    assert not equal(f.subs(x, -x), f)  # and not even (so the answer "odd" is the only one)
    assert parity(f, dom_f) == {"odd"}
    # 2. g(x) = 1/(x² − 1): domain ℝ \ {±1}, symmetric; g(−x) = g(x): even.
    g = 1 / (x**2 - 1)
    dom_g = continuous_domain(g, x, R)
    assert equal(dom_g, R - sp.FiniteSet(-1, 1))
    assert is_symmetric(dom_g)
    assert equal(g.subs(x, -x), g)
    assert parity(g, dom_g) == {"even"}
    # 3. h(x) = x² + x: domain ℝ (symmetric), but h(1) = 2, h(−1) = 0, so neither.
    h = x**2 + x
    assert is_symmetric(continuous_domain(h, x, R))
    assert equal(h.subs(x, 1), 2)
    assert equal(h.subs(x, -1), 0)
    assert not equal(h.subs(x, -1), h.subs(x, 1))
    assert not equal(h.subs(x, -1), -h.subs(x, 1))
    assert parity(h, R) == set()
    # 4. k = x² on [−1, 2]. The formula alone passes the even test (k(−x) = k(x) as formulas),
    # but 2 ∈ dom k and −2 ∉ dom k, so the domain is not symmetric, and the definition (which
    # asks for a symmetric domain for both) makes k neither even nor odd.
    k = x**2
    dom_k = sp.Interval(-1, 2)
    assert equal(k.subs(x, -x), k)
    assert dom_k.contains(2) is sp.true and dom_k.contains(-2) is sp.false
    assert not is_symmetric(dom_k)
    assert equal(reflect(dom_k), sp.Interval(-2, 1))  # −[−1, 2] = [−2, 1] ≠ [−1, 2]
    assert parity(k, dom_k) == set()
    # Restricted to a symmetric part of the domain the same formula is even: the domain decides.
    assert parity(k, sp.Interval(-1, 1)) == {"even"}
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
    # The recalled fact: each u ≥ 0 has exactly one square root s ≥ 0, and (√u)² = u.
    u = sp.Symbol("u", nonnegative=True)
    s = sp.Symbol("s", real=True)
    # The real solutions of s² = u are ±√u; −√u ≤ 0, and −√u ≥ 0 only when u = 0 (where the two
    # coincide), so √u is the only one ≥ 0.
    assert equal(sp.solveset(sp.Eq(s**2, u), s, R), sp.FiniteSet(-sp.sqrt(u), sp.sqrt(u)))
    assert sp.sqrt(u).is_nonnegative and (-sp.sqrt(u)).is_nonpositive
    assert equal(sp.solveset(sp.Eq(sp.sqrt(u), 0), u, sp.Interval(0, oo)), sp.FiniteSet(0))
    assert equal(sp.sqrt(u) ** 2, u)
    # The new step: x₂ > 0 gives √x₂ > 0, because √x₂ = 0 would give x₂ = 0² = 0. The only
    # u ≥ 0 with √u = 0 is u = 0, and x₂ = x₁ + d > 0.
    assert x2.is_positive
    assert equal(sp.solveset(sp.Eq(sp.sqrt(u), 0), u, sp.Interval(0, oo)), sp.FiniteSet(0))
    assert sp.sqrt(x2).is_positive
    assert sp.sqrt(x1).is_nonnegative
    # The edge case x₁ = 0 (where √x₁ = 0 and only √x₂ keeps the denominator positive).
    assert equal(lhs.subs(x1, 0), sp.sqrt(d)) and sp.sqrt(d).is_positive
    assert (sp.sqrt(x2) + sp.sqrt(x1)).subs(x1, 0).is_positive


@covers("exr-calc-functions-odd-at-zero")
def test_exr_calc_functions_odd_at_zero():
    # Manual answer (a proof): no answer() call; a reviewer's note covers it. Its key claims:
    # f(0) = −f(0) forces f(0) = 0, and x³ + 1 is 1 ≠ 0 at 0 (so it is not odd).
    v = sp.Symbol("v", real=True)  # v = f(0)
    assert equal(-sp.S.Zero, 0)  # −0 = 0, so the condition at x = 0 reads f(0) = −f(0)
    assert equal(sp.solveset(sp.Eq(v, -v), v, R), sp.FiniteSet(0))
    # The hypothesis 0 ∈ dom f is needed: 1/x is odd on its symmetric domain ℝ \ {0}, which
    # does not contain 0.
    recip_dom = continuous_domain(1 / x, x, R)
    assert equal(recip_dom, R - sp.FiniteSet(0))
    assert parity(1 / x, recip_dom) == {"odd"}
    assert recip_dom.contains(0) is sp.false
    # Second part: x³ + 1 has domain ℝ, symmetric and containing 0, and its value there is 1 ≠ 0.
    g = x**3 + 1
    dom_g = continuous_domain(g, x, R)
    assert equal(dom_g, R) and is_symmetric(dom_g) and dom_g.contains(0) is sp.true
    assert equal(g.subs(x, 0), 1)
    assert not equal(g.subs(x, 0), 0)
    assert not equal(g.subs(x, -x), -g)
    assert "odd" not in parity(g, dom_g)


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

    # Left piece: for x < 0, −x > 0, and each y > 0 is taken at x = −y < 0.
    pos = sp.Symbol("pos", positive=True)
    assert (-x).subs(x, -pos).is_positive and (-pos).is_negative
    assert equal(function_range(left, x, dom_left), sp.Interval.open(0, oo))

    # Right piece, with t = x − 1. From 0 ≤ x ≤ 3: −1 ≤ t ≤ 2.
    t = sp.Symbol("t", real=True)
    assert equal(sp.imageset(sp.Lambda(x, x - 1), dom_right), sp.Interval(-1, 2))
    assert equal(right, (x - 1) ** 2 - 1)
    # Why term-by-term squaring fails: it would give 1 ≤ t², false at t = 0 (x = 1).
    assert not equal(sp.solveset(t**2 < 1, t, sp.Interval(-1, 2)), sp.S.EmptySet)
    # Case t ≥ 0: t ≤ 2 times t ≥ 0 gives t² ≤ 2t; t ≤ 2 times 2 gives 2t ≤ 4. No t in [0, 2]
    # breaks either step.
    case1 = sp.Interval(0, 2)
    assert equal(sp.solveset(t**2 > 2 * t, t, case1), sp.S.EmptySet)
    assert equal(sp.solveset(2 * t > 4, t, case1), sp.S.EmptySet)
    # Case t < 0: −1 ≤ t times the negative t reverses to t² ≤ −t; −1 ≤ t times −1 gives
    # −t ≤ 1. No t in [−1, 0) breaks either step, so t² ≤ 1 ≤ 4.
    case2 = sp.Interval.Ropen(-1, 0)
    assert equal(sp.solveset(t**2 > -t, t, case2), sp.S.EmptySet)
    assert equal(sp.solveset(-t > 1, t, case2), sp.S.EmptySet)
    assert equal(sp.Union(case1, case2), sp.Interval(-1, 2))  # the two cases cover every t
    # In both cases 0 ≤ t² ≤ 4, so −1 ≤ f(x) = t² − 1 ≤ 3 (and these bounds are attained).
    assert equal(function_range(t**2, t, sp.Interval(-1, 2)), sp.Interval(0, 4))
    assert equal(function_range(right, x, dom_right), sp.Interval(-1, 3))

    # Converse: for y ∈ [−1, 3], s = √(y + 1) ≥ 0 and s ≤ 2.
    Y = sp.Interval(-1, 3)
    s = sp.sqrt(y + 1)
    assert equal(function_range(s, y, Y), sp.Interval(0, 2))
    # The page's argument for s ≤ 2: if s > 2 then s² > 2s > 4 (write s = 2 + e, e > 0).
    e = sp.Symbol("e", positive=True)
    big = 2 + e
    assert equal(big**2 - 2 * big, e * (e + 2))  # s² − 2s = s(s − 2), with s > 0 and s − 2 > 0
    assert sp.factor(big**2 - 2 * big).is_positive  # s² > 2s
    assert sp.factor(2 * big - 4).is_positive  # 2s > 4
    assert equal(sp.solveset(y + 1 > 4, y, Y), sp.S.EmptySet)  # but s² = y + 1 ≤ 4 on [−1, 3]
    # x = 1 + s lies in [1, 3] ⊆ [0, 3] and f(1 + s) = s² − 1 = y.
    assert equal(function_range(1 + s, y, Y), sp.Interval(1, 3))
    assert equal_on_domain(right.subs(x, 1 + s), y, y, Y)


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
    # The new definition also asks for a symmetric domain: the common domain ℝ is one (this is
    # also what lets the uniqueness part evaluate f, g, h at −x for every x).
    assert is_symmetric(R)
    # The example f(x) = x² + x + 1: g(x) = x² + 1 and h(x) = x, derived from the formulas.
    f = x**2 + x + 1
    ge = (f + f.subs(x, -x)) / 2
    he = (f - f.subs(x, -x)) / 2
    assert equal(ge.subs(x, -x), ge)
    assert equal(he.subs(x, -x), -he)
    assert equal(ge + he, f)
    assert parity(ge, R) == {"even"} and parity(he, R) == {"odd"}
    assert equal(ge, x**2 + 1)
    assert equal(he, x)


# ---------------------------------------------------------------------------------------------
# Claims in the prose that no eg-/exr- label owns (not counted for coverage).


def test_def_calc_monotone_constant_functions():
    """A constant function on a set with at least two points is increasing and decreasing but
    neither strictly; on a one-point set every function is all four (vacuously)."""
    const = lambda v: 7  # noqa: E731
    # Two points.
    assert monotone_kinds(const, [0, 1]) == {"increasing", "decreasing"}
    # Any S with at least two points: some x₁ < x₂ = x₁ + d, and f(x₂) − f(x₁) = 0, which is
    # ≤ 0 and ≥ 0 but neither < 0 nor > 0.
    c, x1 = sp.symbols("c x1", real=True)
    diff = sp.Lambda(x, c)(x1 + d) - sp.Lambda(x, c)(x1)
    assert equal(diff, 0)
    assert diff.is_nonnegative and diff.is_nonpositive
    assert diff.is_positive is False and diff.is_negative is False
    # One point: there are no x₁ < x₂ to compare, so all four hold, for any function there.
    assert monotone_kinds(const, [5]) == ALL_FOUR
    assert monotone_kinds(lambda v: v**3 - v, [sp.Rational(1, 2)]) == ALL_FOUR
    # (and with three points a constant is still only weakly monotone)
    assert monotone_kinds(const, [-1, 0, 2]) == {"increasing", "decreasing"}


def test_increasing_not_strictly_example_and_figure():
    """g = 0 on x < 0, x on x ≥ 0 is increasing on ℝ but not strictly (g(−2) = g(−1) = 0); the
    example and the left half of fig-calc-functions-increasing-vs-strictly."""
    g = sp.Piecewise((0, x < 0), (x, True))
    assert equal(g.subs(x, -2), 0) and equal(g.subs(x, -1), 0)
    # From the definition, by where x₁ < x₂ lie (p, d > 0 and q ≥ 0):
    q = sp.Symbol("q", nonnegative=True)
    # both < 0 (x₁ = −p − d < x₂ = −p): both values are 0;
    assert equal(g.subs(x, -p) - g.subs(x, -p - d), 0)
    # x₁ = −p < 0 ≤ x₂ = q: g(x₂) − g(x₁) = q ≥ 0;
    assert equal(g.subs(x, q) - g.subs(x, -p), q) and q.is_nonnegative
    # 0 ≤ x₁ = q < x₂ = q + d: g(x₂) − g(x₁) = d > 0.
    assert equal(g.subs(x, q + d) - g.subs(x, q), d)
    assert monotone_kinds(lambda v: g.subs(x, v), [-3, -2, -1, 0, 1, 2, 3]) == {"increasing"}


def test_def_calc_domain_range_example_and_shadows_figure():
    """f(x) = √(x − 1): dom f = [1, ∞), ran f = [0, ∞), each y ≥ 0 is the value at y² + 1;
    the figure's point (5, 2)."""
    f = sp.sqrt(x - 1)
    assert equal(natural_domain([x - 1]), sp.Interval(1, oo))
    assert equal(continuous_domain(f, x, R), sp.Interval(1, oo))
    assert equal(function_range(f, x, sp.Interval(1, oo)), sp.Interval(0, oo))
    assert equal_on_domain(f.subs(x, y**2 + 1), y, y, sp.Interval(0, oo))
    assert equal(f.subs(x, 5), 2)
    # Non-example: x² on ℝ has range [0, ∞), and −1 is not a value.
    assert equal(function_range(x**2, x, R), sp.Interval(0, oo))
    assert equal(sp.solveset(sp.Eq(x**2, -1), x, R), sp.S.EmptySet)


def test_vertical_line_test_figure_and_sketching_example():
    """x = 1.5 meets y = x² once; x = 2.5 meets y² = x twice. The step function's heights at 0
    differ (0 from the left formula, 1 from the right), so no segment joins (−1, 0) to (0, 1)."""
    assert equal(sp.solveset(sp.Eq(y, sp.Rational(3, 2) ** 2), y, R), sp.FiniteSet(sp.Rational(9, 4)))
    two = sp.solveset(sp.Eq(y**2, sp.Rational(5, 2)), y, R)
    assert equal(two, sp.FiniteSet(-sp.sqrt(sp.Rational(5, 2)), sp.sqrt(sp.Rational(5, 2))))
    step_left, step_right = sp.S.Zero, sp.S.One
    assert not equal(step_left, step_right)


def test_def_calc_even_odd_examples_mistake_and_summary():
    """Under def-calc-even-odd (symmetric domain + identity): the examples, the non-example,
    the third common mistake and the Summary's "a function whose domain is not symmetric is
    neither"."""
    # Examples and non-example (domain ℝ).
    assert parity(x**4 - 3 * x**2, R) == {"even"}
    assert parity(x**3, R) == {"odd"}
    nonex = x**2 + x
    assert equal(nonex.subs(x, 1), 2) and equal(nonex.subs(x, -1), 0)
    assert parity(nonex, R) == set()
    # The third common mistake: x³ + 1 on ℝ. The domain is symmetric, f(−1) = 0, −f(1) = −2,
    # f(1) = 2: not odd and not even.
    f = x**3 + 1
    assert is_symmetric(continuous_domain(f, x, R))
    assert equal(f.subs(x, -1), 0) and equal(-f.subs(x, 1), -2) and equal(f.subs(x, 1), 2)
    assert parity(f, R) == set()
    # Summary: a non-symmetric domain makes a function neither, even when its formula is even
    # or odd elsewhere.
    for formula, dom in [
        (x**2, sp.Interval(-1, 2)),
        (x**3, sp.Interval.Ropen(-1, 1)),
        (sp.sqrt(x), continuous_domain(sp.sqrt(x), x, R)),
        (x**2 - x**2, sp.Interval(0, 1)),  # the zero function: both on ℝ, neither on [0, 1]
    ]:
        assert not is_symmetric(dom)
        assert parity(formula, dom) == set()
    assert parity(sp.S.Zero * x, R) == {"even", "odd"}
