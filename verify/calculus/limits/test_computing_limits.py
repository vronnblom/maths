"""Verification tests for content/calculus/limits/computing-limits.md (calc-computing-limits).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-computing-limits-factor")
def test_eg_calc_computing_limits_factor():
    pytest.skip("for the verifier")


@covers("eg-calc-computing-limits-conjugate")
def test_eg_calc_computing_limits_conjugate():
    pytest.skip("for the verifier")


@covers("eg-calc-computing-limits-same-form")
def test_eg_calc_computing_limits_same_form():
    pytest.skip("for the verifier")


@covers("eg-calc-computing-limits-resistors")
def test_eg_calc_computing_limits_resistors():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-factor-quadratic")
def test_exr_calc_computing_limits_factor_quadratic():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-factor-both")
def test_exr_calc_computing_limits_factor_both():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-conjugate")
def test_exr_calc_computing_limits_conjugate():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-compound")
def test_exr_calc_computing_limits_compound():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-factor-twice")
def test_exr_calc_computing_limits_factor_twice():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-root-denominator")
def test_exr_calc_computing_limits_root_denominator():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-abs-sqrt")
def test_exr_calc_computing_limits_abs_sqrt():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-abs-denominator")
def test_exr_calc_computing_limits_abs_denominator():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-lens")
def test_exr_calc_computing_limits_lens():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-power")
def test_exr_calc_computing_limits_power():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-numerator-zero")
def test_exr_calc_computing_limits_numerator_zero():
    pytest.skip("for the verifier")


@covers("exr-calc-computing-limits-find-constant")
def test_exr_calc_computing_limits_find_constant():
    pytest.skip("for the verifier")
