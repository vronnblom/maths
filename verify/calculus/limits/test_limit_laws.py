"""Verification tests for content/calculus/limits/limit-laws.md (calc-limit-laws).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401


@covers("eg-calc-limit-laws-sum-delta")
def test_eg_calc_limit_laws_sum_delta():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-laws-rational")
def test_eg_calc_limit_laws_rational():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-laws-root-quotient")
def test_eg_calc_limit_laws_root_quotient():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-laws-resistors")
def test_eg_calc_limit_laws_resistors():
    pytest.skip("for the verifier")


@covers("eg-calc-limit-laws-hypotheses")
def test_eg_calc_limit_laws_hypotheses():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-given-limits")
def test_exr_calc_limit_laws_given_limits():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-polynomial")
def test_exr_calc_limit_laws_polynomial():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-rational")
def test_exr_calc_limit_laws_rational():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-where-substitution")
def test_exr_calc_limit_laws_where_substitution():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-roots")
def test_exr_calc_limit_laws_roots():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-lens")
def test_exr_calc_limit_laws_lens():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-sum-delta")
def test_exr_calc_limit_laws_sum_delta():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-sum-part")
def test_exr_calc_limit_laws_sum_part():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-product-part")
def test_exr_calc_limit_laws_product_part():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-root-zero")
def test_exr_calc_limit_laws_root_zero():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-root-domain")
def test_exr_calc_limit_laws_root_domain():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-constant-multiple")
def test_exr_calc_limit_laws_constant_multiple():
    pytest.skip("for the verifier")


@covers("exr-calc-limit-laws-absolute-value")
def test_exr_calc_limit_laws_absolute_value():
    pytest.skip("for the verifier")
