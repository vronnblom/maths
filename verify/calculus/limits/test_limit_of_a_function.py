"""Verification tests for content/calculus/limits/limit-of-a-function.md (calc-limit).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-limit-linear-eps-delta")
def test_eg_calc_limit_linear_eps_delta():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-quadratic-eps-delta")
def test_eg_calc_limit_quadratic_eps_delta():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-sin-1-over-x")
def test_eg_calc_limit_sin_1_over_x():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-average-speed")
def test_eg_calc_limit_average_speed():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-jump")
def test_eg_calc_limit_jump():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-unbounded")
def test_eg_calc_limit_unbounded():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-table-estimate")
def test_exr_calc_limit_table_estimate():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-value-at-a")
def test_exr_calc_limit_value_at_a():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-largest-delta-linear")
def test_exr_calc_limit_largest_delta_linear():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-large-values")
def test_exr_calc_limit_large_values():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-widget-largest-delta")
def test_exr_calc_limit_widget_largest_delta():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-average-speed")
def test_exr_calc_limit_average_speed():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-eps-delta-linear")
def test_exr_calc_limit_eps_delta_linear():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-jump-which-eps")
def test_exr_calc_limit_jump_which_eps():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-sin-pi-over-x")
def test_exr_calc_limit_sin_pi_over_x():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-eps-delta-quadratic")
def test_exr_calc_limit_eps_delta_quadratic():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-eps-delta-sqrt")
def test_exr_calc_limit_eps_delta_sqrt():
    pytest.skip("for the verifier")
