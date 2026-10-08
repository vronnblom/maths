"""Verification tests for content/calculus/preliminaries/trigonometric-functions.md (calc-trig-functions).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-trig-functions-radians")
def test_eg_calc_trig_functions_radians():
    pytest.skip("for the verifier")


@covers("eg-calc-trig-functions-special-values")
def test_eg_calc_trig_functions_special_values():
    pytest.skip("for the verifier")


@covers("eg-calc-trig-functions-other-angles")
def test_eg_calc_trig_functions_other_angles():
    pytest.skip("for the verifier")


@covers("eg-calc-trig-functions-sign")
def test_eg_calc_trig_functions_sign():
    pytest.skip("for the verifier")


@covers("eg-calc-trig-functions-addition")
def test_eg_calc_trig_functions_addition():
    pytest.skip("for the verifier")


@covers("eg-calc-trig-functions-ferris-wheel")
def test_eg_calc_trig_functions_ferris_wheel():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-degrees-to-radians")
def test_exr_calc_trig_functions_degrees_to_radians():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-arc-length")
def test_exr_calc_trig_functions_arc_length():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-multiples-of-pi")
def test_exr_calc_trig_functions_multiples_of_pi():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-exact-values")
def test_exr_calc_trig_functions_exact_values():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-from-cosine")
def test_exr_calc_trig_functions_from_cosine():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-addition")
def test_exr_calc_trig_functions_addition():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-solve-sine")
def test_exr_calc_trig_functions_solve_sine():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-widget-wave")
def test_exr_calc_trig_functions_widget_wave():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-ferris-times")
def test_exr_calc_trig_functions_ferris_times():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-cos-decreasing")
def test_exr_calc_trig_functions_cos_decreasing():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-tan-period")
def test_exr_calc_trig_functions_tan_period():
    pytest.skip("for the verifier")


@covers("exr-calc-trig-functions-sin-over-theta")
def test_exr_calc_trig_functions_sin_over_theta():
    pytest.skip("for the verifier")
