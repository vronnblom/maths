"""Verification tests for content/calculus/limits/one-sided-limits.md (calc-one-sided-limits).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-one-sided-limits-agree")
def test_eg_calc_one_sided_limits_agree():
    pytest.skip("for the verifier")


@covers("eg-calc-one-sided-limits-parcel")
def test_eg_calc_one_sided_limits_parcel():
    pytest.skip("for the verifier")


@covers("eg-calc-one-sided-limits-sqrt")
def test_eg_calc_one_sided_limits_sqrt():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-abs-over-x")
def test_exr_calc_one_sided_limits_abs_over_x():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-piecewise")
def test_exr_calc_one_sided_limits_piecewise():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-sqrt-shift")
def test_exr_calc_one_sided_limits_sqrt_shift():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-claim")
def test_exr_calc_one_sided_limits_claim():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-largest-delta")
def test_exr_calc_one_sided_limits_largest_delta():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-parking")
def test_exr_calc_one_sided_limits_parking():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-parameter")
def test_exr_calc_one_sided_limits_parameter():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-widget-eps")
def test_exr_calc_one_sided_limits_widget_eps():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-reciprocal")
def test_exr_calc_one_sided_limits_reciprocal():
    pytest.skip("for the verifier")


@covers("exr-calc-one-sided-limits-reciprocal-left")
def test_exr_calc_one_sided_limits_reciprocal_left():
    pytest.skip("for the verifier")
