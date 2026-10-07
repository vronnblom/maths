"""Verification tests for content/calculus/preliminaries/absolute-value-and-inequalities.md (calc-absolute-value-inequalities).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-absolute-value-inequalities-linear")
def test_eg_calc_absolute_value_inequalities_linear():
    pytest.skip("for the verifier")


@covers("eg-calc-absolute-value-inequalities-quadratic")
def test_eg_calc_absolute_value_inequalities_quadratic():
    pytest.skip("for the verifier")


@covers("eg-calc-absolute-value-inequalities-abs-less")
def test_eg_calc_absolute_value_inequalities_abs_less():
    pytest.skip("for the verifier")


@covers("eg-calc-absolute-value-inequalities-abs-greater")
def test_eg_calc_absolute_value_inequalities_abs_greater():
    pytest.skip("for the verifier")


@covers("eg-calc-absolute-value-inequalities-punctured")
def test_eg_calc_absolute_value_inequalities_punctured():
    pytest.skip("for the verifier")


@covers("eg-calc-absolute-value-inequalities-triangle-bound")
def test_eg_calc_absolute_value_inequalities_triangle_bound():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-evaluate")
def test_exr_calc_absolute_value_inequalities_evaluate():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-linear")
def test_exr_calc_absolute_value_inequalities_linear():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-abs-to-interval")
def test_exr_calc_absolute_value_inequalities_abs_to_interval():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-abs-closed")
def test_exr_calc_absolute_value_inequalities_abs_closed():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-interval-to-abs")
def test_exr_calc_absolute_value_inequalities_interval_to_abs():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-abs-outside")
def test_exr_calc_absolute_value_inequalities_abs_outside():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-quadratic")
def test_exr_calc_absolute_value_inequalities_quadratic():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-cubic")
def test_exr_calc_absolute_value_inequalities_cubic():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-rational")
def test_exr_calc_absolute_value_inequalities_rational():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-punctured")
def test_exr_calc_absolute_value_inequalities_punctured():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-difference-bound")
def test_exr_calc_absolute_value_inequalities_difference_bound():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-compare-distances")
def test_exr_calc_absolute_value_inequalities_compare_distances():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-close-points")
def test_exr_calc_absolute_value_inequalities_close_points():
    pytest.skip("for the verifier")


@covers("exr-calc-absolute-value-inequalities-largest-delta")
def test_exr_calc_absolute_value_inequalities_largest_delta():
    pytest.skip("for the verifier")
