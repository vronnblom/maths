"""Verification tests for <page path>.

TEMPLATE: copy to verify/<subject>/<chapter>/test_<topic_with_underscores>.py
Rules: docs/plan/06-quality-assurance.md §6.1.

- One test (or more) per `eg-*` and `exr-*` label, declared with @covers.
- Derive expected values INDEPENDENTLY; never copy numbers from the page's answers or solutions.
- For worked examples, assert every displayed equality (or mark it `# prose step, reviewed manually`).
- `answer(label)` returns the page's own Answer, parsed by SymPy, so the printed answer is what gets checked.
"""

import sympy as sp

from mathcheck import (
    answer,             # answer("exr-…") -> SymPy expression parsed from the page
    covers,             # @covers("eg-…", "exr-…")
    equal,              # symbolic equality; fails (never passes) if undecidable
    equal_up_to_constant,
    limit_is,
    numeric_spot_check,
)

x, h = sp.symbols("x h", real=True)
eps = sp.symbols("epsilon", positive=True)


@covers("eg-calc-limit-linear-eps-delta")
def test_linear_eps_delta_example():
    # Step 1 on the page: |(2x - 1) - 5| = 2|x - 3|
    assert equal(sp.Abs((2 * x - 1) - 5), 2 * sp.Abs(x - 3))
    # Step 3: with delta = eps/2, |x - 3| < delta implies |f(x) - 5| < eps.
    delta = eps / 2
    assert equal(2 * delta, eps)
    # Check line: eps = 0.1, x = 3.04
    assert sp.Abs(2 * sp.Rational(304, 100) - 1 - 5) < sp.Rational(1, 10)


@covers("exr-calc-limit-table-estimate")
def test_table_estimate():
    exact = sp.limit((2**x - 1) / x, x, 0)          # = ln 2, derived independently
    assert equal(exact, sp.log(2))
    assert abs(float(answer("exr-calc-limit-table-estimate")) - float(exact)) < 1e-2


@covers("exr-calc-limit-eps-delta-linear")
def test_eps_delta_exercise_key_claim():
    # The answer is `manual` (a proof), but the key claim is still checkable:
    # |(4 - 3x) - 7| = 3|x + 1|, so delta = eps/3 works.
    assert equal(sp.Abs((4 - 3 * x) - 7), 3 * sp.Abs(x + 1))


def test_motivating_widget_limit():
    # Not a labelled block, but the "Why this matters" claim is checked too.
    assert limit_is((5 * (1 + h) ** 2 - 5) / h, h, 0, 10)
