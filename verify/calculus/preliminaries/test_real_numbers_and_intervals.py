"""Verification tests for content/calculus/preliminaries/real-numbers-and-intervals.md (calc-real-numbers).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-real-numbers-set-to-interval")
def test_eg_calc_real_numbers_set_to_interval():
    pytest.skip("for the verifier")


@covers("eg-calc-real-numbers-intersection-union")
def test_eg_calc_real_numbers_intersection_union():
    pytest.skip("for the verifier")


@covers("eg-calc-real-numbers-repeating-decimal")
def test_eg_calc_real_numbers_repeating_decimal():
    pytest.skip("for the verifier")


@covers("eg-calc-real-numbers-tolerance")
def test_eg_calc_real_numbers_tolerance():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-to-interval")
def test_exr_calc_real_numbers_to_interval():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-integers-in-interval")
def test_exr_calc_real_numbers_integers_in_interval():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-integers-rational")
def test_exr_calc_real_numbers_integers_rational():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-intersection")
def test_exr_calc_real_numbers_intersection():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-union")
def test_exr_calc_real_numbers_union():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-complement")
def test_exr_calc_real_numbers_complement():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-repeating-decimal")
def test_exr_calc_real_numbers_repeating_decimal():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-delayed-repeat")
def test_exr_calc_real_numbers_delayed_repeat():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-sqrt3-irrational")
def test_exr_calc_real_numbers_sqrt3_irrational():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-supremum")
def test_exr_calc_real_numbers_supremum():
    pytest.skip("for the verifier")


@covers("exr-calc-real-numbers-rational-between")
def test_exr_calc_real_numbers_rational_between():
    pytest.skip("for the verifier")
