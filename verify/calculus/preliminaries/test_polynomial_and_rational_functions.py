"""Verification tests for content/calculus/preliminaries/polynomial-and-rational-functions.md (calc-polynomial-rational).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-polynomial-rational-division")
def test_eg_calc_polynomial_rational_division():
    pytest.skip("for the verifier")


@covers("eg-calc-polynomial-rational-factor-cubic")
def test_eg_calc_polynomial_rational_factor_cubic():
    pytest.skip("for the verifier")


@covers("eg-calc-polynomial-rational-difference-quotient")
def test_eg_calc_polynomial_rational_difference_quotient():
    pytest.skip("for the verifier")


@covers("eg-calc-polynomial-rational-sign-chart")
def test_eg_calc_polynomial_rational_sign_chart():
    pytest.skip("for the verifier")


@covers("eg-calc-polynomial-rational-box")
def test_eg_calc_polynomial_rational_box():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-degree")
def test_exr_calc_polynomial_rational_degree():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-factor-check")
def test_exr_calc_polynomial_rational_factor_check():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-domain")
def test_exr_calc_polynomial_rational_domain():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-zeros")
def test_exr_calc_polynomial_rational_zeros():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-division")
def test_exr_calc_polynomial_rational_division():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-factor-cubic")
def test_exr_calc_polynomial_rational_factor_cubic():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-difference-quotient")
def test_exr_calc_polynomial_rational_difference_quotient():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-remainder")
def test_exr_calc_polynomial_rational_remainder():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-inequality")
def test_exr_calc_polynomial_rational_inequality():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-concentration")
def test_exr_calc_polynomial_rational_concentration():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-from-roots")
def test_exr_calc_polynomial_rational_from_roots():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-inequality-hard")
def test_exr_calc_polynomial_rational_inequality_hard():
    pytest.skip("for the verifier")


@covers("exr-calc-polynomial-rational-integer-root")
def test_exr_calc_polynomial_rational_integer_root():
    pytest.skip("for the verifier")
