"""Verification tests for content/calculus/limits/squeeze-theorem.md (calc-squeeze-theorem).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-squeeze-theorem-oscillating")
def test_eg_calc_squeeze_theorem_oscillating():
    pytest.skip("for the verifier")


@covers("eg-calc-squeeze-theorem-sin-3x")
def test_eg_calc_squeeze_theorem_sin_3x():
    pytest.skip("for the verifier")


@covers("eg-calc-squeeze-theorem-small-angle")
def test_eg_calc_squeeze_theorem_small_angle():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-sin-2x")
def test_exr_calc_squeeze_theorem_sin_2x():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-x2-cos")
def test_exr_calc_squeeze_theorem_x2_cos():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-tan")
def test_exr_calc_squeeze_theorem_tan():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-one-minus-cos-x2")
def test_exr_calc_squeeze_theorem_one_minus_cos_x2():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-sqrt-sin")
def test_exr_calc_squeeze_theorem_sqrt_sin():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-pendulum")
def test_exr_calc_squeeze_theorem_pendulum():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-different-limits")
def test_exr_calc_squeeze_theorem_different_limits():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-direct-cor")
def test_exr_calc_squeeze_theorem_direct_cor():
    pytest.skip("for the verifier")


@covers("exr-calc-squeeze-theorem-parabola")
def test_exr_calc_squeeze_theorem_parabola():
    pytest.skip("for the verifier")
