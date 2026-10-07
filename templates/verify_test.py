"""Verification tests for <page path>.

TEMPLATE: copy to verify/<subject>/<chapter>/test_<topic_with_underscores>.py
Rules: docs/plan/06-quality-assurance.md §6.1.

- One test (or more) per `eg-*` and `exr-*` label, declared with @covers.
- Derive expected values INDEPENDENTLY; never copy numbers from the page's answers or solutions.
- For worked examples, assert every displayed equality (or mark it `# prose step, reviewed manually`).
- `answer(label)` returns the page's own Answer, parsed by SymPy, so the printed answer is what gets checked.
  Compare it with `equal(...)`, never `==`.
- Coverage counts only tests that PASS (and, for `exr-*`, call `answer(label)`). The author's
  skeleton uses `pytest.skip("for the verifier")` stubs, which count as uncovered.
"""

import random

import sympy as sp

from mathcheck import (
    answer,             # answer("exr-…") -> SymPy expression parsed from the page
    covers,             # @covers("eg-…", "exr-…")
    equal,              # symbolic equality; fails (never passes) if undecidable
    equal_up_to_constant,
    limit_is,
    numeric_spot_check,
    x,                  # mathcheck's canonical real symbols: the same objects answer() uses
)

h = sp.symbols("h", real=True)
eps = sp.symbols("epsilon", positive=True)


@covers("eg-calc-limit-linear-eps-delta")
def test_linear_eps_delta_example():
    # Step 1 on the page: |(2x - 1) - 5| = 2|x - 3|
    assert equal(sp.Abs((2 * x - 1) - 5), 2 * sp.Abs(x - 3))
    # Step 3: with the page's delta = eps/2, 0 < |x - 3| < delta implies |f(x) - 5| < eps.
    # By step 1, |f(x) - 5| = 2t with t = |x - 3|, which increases with t, so the implication
    # holds exactly when 2 * delta <= eps.
    delta = eps / 2
    assert sp.simplify(2 * delta - eps) <= 0
    # And test the implication itself on random points, independently of the algebra above.
    rng = random.Random(0)
    for _ in range(1000):
        e = rng.uniform(1e-6, 2)
        d = float(delta.subs(eps, e))
        xv = 3 + rng.choice([-1, 1]) * rng.uniform(1e-12, d) * (1 - 1e-12)
        assert abs((2 * xv - 1) - 5) < e
    # Check line: eps = 0.1, x = 3.04
    assert sp.Abs(2 * sp.Rational(304, 100) - 1 - 5) < sp.Rational(1, 10)


@covers("exr-calc-limit-table-estimate")
def test_table_estimate():
    exact = sp.limit((2**x - 1) / x, x, 0)          # = ln 2, derived independently
    assert equal(exact, sp.log(2))
    # "to two decimal places": the printed value must be the correctly rounded one
    # (0.69), so a wrongly rounded 0.70 fails. A tolerance of 1e-2 would accept it.
    printed = float(answer("exr-calc-limit-table-estimate"))
    assert abs(printed - round(float(exact), 2)) < 1e-9


@covers("exr-calc-limit-eps-delta-linear")
def test_eps_delta_exercise_key_claim():
    # The answer is `manual` (a proof), but the key claim is still checkable:
    # |(4 - 3x) - 7| = 3|x + 1|, so delta = eps/3 works.
    assert equal(sp.Abs((4 - 3 * x) - 7), 3 * sp.Abs(x + 1))


def test_motivating_widget_limit():
    # Not a labelled block, but the "Why this matters" claim is checked too.
    assert limit_is((5 * (1 + h) ** 2 - 5) / h, h, 0, 10)
