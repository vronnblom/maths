"""Verification tests for content/calculus/limits/index.md (calc-limits-chapter).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("exr-calc-limits-review-substitute-or-simplify")
def test_exr_calc_limits_review_substitute_or_simplify():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-sine-over-quadratic")
def test_exr_calc_limits_review_sine_over_quadratic():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-abs-quotient")
def test_exr_calc_limits_review_abs_quotient():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-asymptotes")
def test_exr_calc_limits_review_asymptotes():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-root-and-factor")
def test_exr_calc_limits_review_root_and_factor():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-oscillation-over-sine")
def test_exr_calc_limits_review_oscillation_over_sine():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-brine-tank")
def test_exr_calc_limits_review_brine_tank():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-root-over-line")
def test_exr_calc_limits_review_root_over_line():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-positive-over-square")
def test_exr_calc_limits_review_positive_over_square():
    pytest.skip("for the verifier")


@covers("exr-calc-limits-review-root-parameters")
def test_exr_calc_limits_review_root_parameters():
    pytest.skip("for the verifier")
