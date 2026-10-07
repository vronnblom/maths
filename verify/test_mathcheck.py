"""Tests of mathcheck itself (docs/plan/06 §6.1): the answer parser's golden cases, the known
SymPy traps, the equality helpers, the coverage bookkeeping, and the AST fixture.

The golden cases cover every item of the answer LaTeX subset (docs/plan/04 §4.3) and the
examples of 06 §6.1. **Every expected value is written by hand**, as SymPy constructors of the
mathematics (`sp.pi / 4`, `sp.Rational(69, 100)`, `sp.Interval.Ropen(0, 1)`), never by running
parse_answer. They are compared **structurally** (`same`, via `sp.srepr`) on purpose: a golden
test pins the exact canonical object, e.g. `sp.pi` and not a symbol called pi, or `Rational(1, 2)`
and not an unevaluated `Pow(2, -1)`. The harness itself compares values with `equal`, never `==`.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import sympy as sp
import yaml
from sympy.parsing.latex import parse_latex

import mathcheck
from mathcheck import (
    AnswerParseError, ManualAnswer, Undecidable, b, covers, equal, equal_on_domain, equal_up_to_constant,
    limit_is, n, numeric_spot_check, series_converges_to, solves_ode, x,
)
from mathcheck.latex import parse_answer, project_macros

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
oo = sp.oo


def same(got, want):
    """Structural identity: the same SymPy tree (and Python type), not just an equal value."""
    assert type(got) is type(want), f"{got!r} is a {type(got).__name__}, expected a {type(want).__name__} ({want!r})"
    assert sp.srepr(got) == sp.srepr(want), f"{sp.srepr(got)} != {sp.srepr(want)}"


# ── Golden cases: every item of 04 §4.3, and the examples of 06 §6.1 ────────

GOLDEN = [
    # numbers (a decimal is exact: 0.69 is 69/100, so rounding tests compare exactly)
    ("3", "expr", sp.Integer(3)),
    ("-3", "expr", sp.Integer(-3)),
    ("+5", "expr", sp.Integer(5)),
    ("0.69", "numeric-5e-3", sp.Rational(69, 100)),
    ("2.5", "expr", sp.Rational(5, 2)),
    ("-0.05", "expr", sp.Rational(-1, 20)),
    # \frac{}{}
    (r"\frac{3}{4}", "expr", sp.Rational(3, 4)),
    (r"\frac{x}{2}", "expr", sp.Mul(sp.Rational(1, 2), x)),
    # \sqrt{} and \sqrt[n]{}
    (r"\sqrt{2}", "expr", sp.Pow(2, sp.Rational(1, 2))),
    (r"\sqrt[3]{2}", "expr", sp.Pow(2, sp.Rational(1, 3))),
    (r"\sqrt[3]{8}", "expr", sp.Integer(2)),
    # ^{}
    (r"2^{10}", "expr", sp.Integer(1024)),
    (r"x^{3}", "expr", sp.Pow(x, 3)),
    # \pi (06 §6.1: \frac{\pi}{4})
    (r"\pi", "expr", sp.pi),
    (r"\frac{\pi}{4}", "expr", sp.Mul(sp.Rational(1, 4), sp.pi)),
    # e (06 §6.1: e^{2})
    ("e", "expr", sp.E),
    ("e^{2}", "expr", sp.exp(2)),
    (r"e^{-x}", "expr", sp.exp(-x)),
    # \infty, -\infty
    (r"\infty", "expr", sp.oo),
    (r"-\infty", "expr", -sp.oo),
    # \sin \cos \tan
    (r"\sin x", "expr", sp.sin(x)),
    (r"\cos(\pi)", "expr", sp.Integer(-1)),
    (r"\tan{\frac{\pi}{4}}", "expr", sp.Integer(1)),
    # \arcsin \arccos \arctan
    (r"\arcsin{\frac{1}{2}}", "expr", sp.Mul(sp.Rational(1, 6), sp.pi)),
    (r"\arccos(0)", "expr", sp.Mul(sp.Rational(1, 2), sp.pi)),
    (r"\arctan x", "expr", sp.atan(x)),
    # \ln and \log_{b} (06 §6.1)
    (r"\ln 2", "expr", sp.log(2)),
    (r"\ln x", "expr", sp.log(x)),
    (r"\log_{2} 8", "expr", sp.Integer(3)),
    (r"\log_{b} x", "expr", sp.Mul(sp.Pow(sp.log(b), -1), sp.log(x))),
    # \abs{} and |x| (06 §6.1: \abs{x})
    (r"\abs{x}", "expr", sp.Abs(x)),
    (r"|x - 1|", "expr", sp.Abs(sp.Add(x, -1))),
    (r"\abs{-3}", "expr", sp.Integer(3)),
    # +C for antiderivatives (06 §6.1)
    (r"\frac{x^{2}}{2} + C", "antiderivative", sp.Mul(sp.Rational(1, 2), sp.Pow(x, 2))),
    (r"\ln|x| + C", "antiderivative", sp.log(sp.Abs(x))),
    # several answers as a comma-separated list (06 §6.1: -2, 4 is two elements)
    ("-2, 4", "expr", (sp.Integer(-2), sp.Integer(4))),
    (r"\frac{1}{2}, \sqrt{2}, \pi", "expr", (sp.Rational(1, 2), sp.Pow(2, sp.Rational(1, 2)), sp.pi)),
    # intervals with the set type (06 §6.1: [0, 1) as set); without it (a, b) is a point
    ("[0, 1)", "set", sp.Interval.Ropen(0, 1)),
    (r"(-\infty, 2]", "set", sp.Interval(-oo, 2, left_open=True, right_open=False)),
    ("[-1, 1]", "set", sp.Interval(-1, 1)),
    (r"(-\infty, 0), (1, \infty)", "set", sp.Union(sp.Interval.open(-oo, 0), sp.Interval.open(1, oo))),
    ("-2, 4", "set", sp.FiniteSet(-2, 4)),
    ("(1, -2)", "expr", (sp.Integer(1), sp.Integer(-2))),
    # 2x (06 §6.1): implicit multiplication, with mathcheck's real x
    ("2x", "expr", sp.Mul(2, x)),
    (r"x \cdot 3", "expr", sp.Mul(3, x)),
    # normalised (but not to be used): \mathrm{e} and \dfrac
    (r"\mathrm{e}^{2}", "expr", sp.exp(2)),
    (r"\dfrac{1}{2}", "expr", sp.Rational(1, 2)),
    # other normalisation: \left/\right, thin spaces, \lvert…\rvert, a Unicode minus
    (r"\left( x + 1 \right)^{2}", "expr", sp.Pow(sp.Add(x, 1), 2)),
    (r"2 \, x", "expr", sp.Mul(2, x)),
    (r"\lvert x \rvert", "expr", sp.Abs(x)),
    ("−3", "expr", sp.Integer(-3)),
    # bool answers (07 §7.3)
    ("True", "bool", sp.true),
    ("false", "bool", sp.false),
]


@pytest.mark.parametrize("latex, answer_type, want", GOLDEN, ids=[f"{t}:{s}" for s, t, _ in GOLDEN])
def test_golden(latex, answer_type, want):
    same(parse_answer(latex, answer_type), want)


def test_every_subset_item_has_a_golden_case():
    """04 §4.3 lists these; each must appear in GOLDEN."""
    used = " ".join(s for s, _, _ in GOLDEN)
    for item in [r"\frac", r"\sqrt{", r"\sqrt[", "^{", r"\pi", "e^", r"\infty", r"-\infty", r"\sin", r"\cos",
                 r"\tan", r"\arcsin", r"\arccos", r"\arctan", r"\ln", r"\log_{", r"\abs{", "|x", "+ C", ", "]:
        assert item in used, item
    types = {t for _, t, _ in GOLDEN}
    assert {"expr", "antiderivative", "set", "bool", "numeric-5e-3"} <= types


def test_symbols_are_mathchecks():
    """Free symbols become mathcheck's own objects, so 2x on the page equals a test's 2*x."""
    got = parse_answer("2x")
    assert got.free_symbols == {x} and next(iter(got.free_symbols)) is mathcheck.x
    assert mathcheck.x.is_real and mathcheck.n.is_integer
    assert equal(parse_answer("2x"), 2 * x)


# ── The known SymPy traps, each shown to exist and to be handled ─────────────


def test_trap_pi_and_e_are_plain_symbols_in_sympy():
    raw_pi, raw_e = parse_latex(r"\pi", backend="antlr"), parse_latex("e", backend="antlr")
    assert isinstance(raw_pi, sp.Symbol) and isinstance(raw_e, sp.Symbol)
    assert parse_answer(r"\pi") is sp.pi and parse_answer("e") is sp.E


def test_trap_list_truncated_at_the_first_comma():
    assert parse_latex("-2, 4", backend="antlr") == -2  # the rest is silently dropped
    with pytest.raises(Exception):
        parse_latex("-2, 4", backend="antlr", strict=True)
    same(parse_answer("-2, 4"), (sp.Integer(-2), sp.Integer(4)))


def test_trap_unevaluated_half():
    raw = parse_latex(r"\frac{1}{2}", backend="antlr")
    assert not isinstance(raw, sp.Rational)
    same(parse_answer(r"\frac{1}{2}"), sp.Rational(1, 2))


def test_trap_unknown_commands_read_as_symbols():
    """antlr reads \\approx as a symbol named approx: an answer outside the subset would 'parse'."""
    raw = parse_latex(r"\approx 0.69", backend="antlr")
    assert sp.Symbol("approx") in raw.free_symbols
    with pytest.raises(AnswerParseError, match=r"\\approx is not in the answer subset"):
        parse_answer(r"\approx 0.69")


def test_trap_bare_log_is_natural_log_in_sympy():
    assert parse_latex(r"\log x", backend="antlr").doit() == sp.log(sp.Symbol("x"))
    with pytest.raises(AnswerParseError, match="bare"):
        parse_answer(r"\log x")


# ── Parse failures: the message says what to do ──────────────────────────────

FAILURES = [
    (r"\text{does not exist}", "expr", r"\\text is not in the answer subset"),
    (r"\approx 0.69", "expr", r"\\approx is not in the answer subset"),
    (r"\frac{1}{", "expr", "unbalanced"),
    (r"\abs", "expr", r"the macro \\abs is missing an argument"),
    ("x = 2", "expr", "not a value"),
    ("x + C", "expr", "needs the type `antiderivative`"),
    (r"\frac{x^{2}}{2}", "antiderivative", r"ends with \+ C"),
    ("[0, 1]", "expr", "need the answer type `set`"),
    ("[1, 0]", "set", "empty"),
    ("x", "numeric-5e-3", "must be a number"),
    ("yes", "bool", "True or False"),
    ("", "expr", "empty"),
    ("1, , 2", "expr", "empty item"),
]


@pytest.mark.parametrize("latex, answer_type, problem", FAILURES, ids=[f"{t}:{s}" for s, t, _ in FAILURES])
def test_parse_failure_tells_the_author_what_to_do(latex, answer_type, problem):
    with pytest.raises(AnswerParseError, match=problem) as e:
        parse_answer(latex, answer_type)
    assert "docs/plan/04 §4.3" in str(e.value) and "manual" in str(e.value)


def test_multi_letter_symbols_are_rejected():
    """The backstop behind the command allowlist: antlr turns an unknown command into a symbol
    with that name, and such a name is never a variable of ours."""
    from mathcheck.latex import _post_process

    with pytest.raises(AnswerParseError, match="multi-letter name"):
        _post_process(sp.Symbol("approx") * sp.Rational(69, 100), r"\approx 0.69", "expr")
    same(parse_answer("abc"), sp.Mul(mathcheck.a, b, mathcheck.c))  # single letters: a product


def test_unknown_answer_type():
    with pytest.raises(ValueError, match="unknown answer type"):
        parse_answer("1", "numeric")  # a numeric answer needs its tolerance


def test_macros_come_from_myst_yml():
    """Expanded from content/myst.yml itself (read here independently), not from a copy."""
    math = yaml.safe_load((REPO / "content" / "myst.yml").read_text(encoding="utf-8"))["project"]["math"]
    assert {k: v[0] for k, v in project_macros().items()} == math
    assert project_macros()[r"\abs"] == (math[r"\abs"], 1)
    same(parse_answer(r"\half x", macros={r"\half": (r"\frac{1}{2}", 0)}), sp.Mul(sp.Rational(1, 2), x))


# ── Equality helpers ─────────────────────────────────────────────────────────


def test_equal():
    assert equal(sp.sqrt(x**2), sp.Abs(x))  # x is real
    assert equal(sp.sin(x) ** 2 + sp.cos(x) ** 2, 1)
    assert equal(sp.Rational(1, 2), 0.5)
    assert not equal(sp.Rational(1, 3), sp.Rational(333, 1000))
    assert equal((1, sp.sqrt(4)), (1, 2)) and not equal((1, 2), (1, 2, 3)) and not equal((1, 2), 1)
    assert equal(sp.Interval.Ropen(0, 1), sp.Interval(0, 1) - sp.FiniteSet(1))
    assert not equal(sp.Interval(0, 1), sp.Interval.Ropen(0, 1))
    assert equal(sp.true, sp.true) and not equal(sp.true, sp.false)
    assert equal(sp.oo, sp.oo) and not equal(sp.oo, -sp.oo) and not equal(sp.oo, 10**100)


def test_equal_never_passes_when_undecidable():
    f, g = sp.Function("f"), sp.Function("g")
    with pytest.raises(Undecidable):
        equal(f(x), g(x))
    for undefined in (sp.nan, sp.zoo):
        with pytest.raises(Undecidable, match="undefined"):
            equal(undefined, undefined)
    assert isinstance(Undecidable("x"), AssertionError)  # so it fails a test, never skips it


def test_equal_rejects_foreign_symbols():
    with pytest.raises(Undecidable, match="mathcheck's symbols"):
        equal(sp.Symbol("x"), x)


def test_equal_up_to_constant():
    assert equal_up_to_constant(x**2 / 2 + 7, x, x)
    # d/dx ln|x| = 1/x only for x ≠ 0 (at 0 SymPy's derivative is undefined), so state the domain
    assert not equal_up_to_constant(sp.log(sp.Abs(x)), 1 / x, x)
    assert equal_up_to_constant(sp.log(sp.Abs(x)), 1 / x, x, domain=(0, oo))
    assert equal_up_to_constant(sp.log(sp.Abs(x)), 1 / x, x, domain=(-oo, 0))
    assert not equal_up_to_constant(x**2, x, x)


def test_equal_on_domain():
    assert equal_on_domain(sp.sqrt(x**2), x, x, sp.Interval(0, oo))
    assert not equal_on_domain(sp.sqrt(x**2), x, x, sp.Interval(-oo, 0, right_open=True))
    assert equal_on_domain(sp.sqrt(x**2), -x, x, (-5, 0))


def test_numeric_spot_check():
    assert numeric_spot_check(sp.sin(2 * x), 2 * sp.sin(x) * sp.cos(x), x, (-10, 10))
    assert not numeric_spot_check(sp.sin(2 * x), 2 * sp.sin(x), x, (-10, 10))
    with pytest.raises(Undecidable, match="only 0 of 50 points"):
        numeric_spot_check(1 / sp.floor(x), 1, x, (sp.Rational(1, 10), sp.Rational(9, 10)))


def test_limit_is():
    assert limit_is(sp.sin(x) / x, x, 0, 1)
    assert not limit_is(sp.sin(x) / x, x, 0, 2)
    assert limit_is(1 / x, x, 0, oo, "+") and limit_is(1 / x, x, 0, -oo, "-")
    assert limit_is((1 + 1 / x) ** x, x, oo, sp.E)
    assert limit_is(1 / sp.log(x), x, 0, 0, "+")  # slow, but the table still settles


def test_limit_is_cross_checks_sympy_numerically(monkeypatch):
    monkeypatch.setattr(sp, "limit", lambda *args: sp.Integer(2))  # a wrong symbolic answer
    with pytest.raises(AssertionError, match="do not settle"):
        limit_is(sp.sin(x) / x, x, 0, 2)


def test_series_converges_to():
    assert series_converges_to(1 / n**2, n, sp.pi**2 / 6)
    assert not series_converges_to(1 / n**2, n, 2)
    assert series_converges_to(sp.Rational(1, 2) ** n, n, 1)
    assert series_converges_to(sp.Rational(1, 2) ** n, n, 2, start=0)


def test_solves_ode():
    f = sp.Function("f")
    ode = sp.Eq(f(x).diff(x), 2 * f(x))
    assert solves_ode(sp.Eq(f(x), 5 * sp.exp(2 * x)), ode)
    assert not solves_ode(sp.Eq(f(x), sp.exp(3 * x)), ode)


# ── Coverage bookkeeping ─────────────────────────────────────────────────────


def test_only_true_results_count_as_assertions():
    state = mathcheck._state
    saved = (state.test, state.assertions, set(state.answers))
    state.begin("probe")
    try:
        assert equal(1, 1)
        assert not equal(1, 2)  # a False result is not an assertion of the page's claim
        assert limit_is(sp.sin(x) / x, x, 0, 1)
        assert state.end() == (2, set())
    finally:
        state.test, state.assertions, state.answers = saved


def test_covers_validates_and_accumulates():
    @covers("eg-calc-limit-one")
    @covers("exr-calc-limit-two", "exr-calc-limit-three")
    def t():
        pass

    assert set(t.__mathcheck_covers__) == {"eg-calc-limit-one", "exr-calc-limit-two", "exr-calc-limit-three"}
    for bad in ["", "exr-Calc-x", "calc-limit", "exr_calc_limit_x"]:
        with pytest.raises(ValueError):
            covers(bad)
    with pytest.raises(ValueError):
        covers()


def test_answer_reads_the_page_and_records_the_call(monkeypatch):
    monkeypatch.setattr(mathcheck._state, "data", {
        "exr-calc-a-half": {"latex": [r"\frac{1}{2}"], "manual": False, "type": "expr", "page": "p.md"},
        "exr-calc-a-parts": {"latex": ["-3", "[0, 1)"], "manual": False, "type": "set", "page": "p.md"},
        "exr-calc-a-proof": {"latex": [r"\delta = \eps / 3"], "manual": True, "type": "manual", "page": "p.md"},
    })
    state = mathcheck._state
    saved = (state.test, state.assertions, set(state.answers))
    state.begin("probe")
    try:
        same(mathcheck.answer("exr-calc-a-half"), sp.Rational(1, 2))
        same(mathcheck.answer("exr-calc-a-parts"), (sp.FiniteSet(-3), sp.Interval.Ropen(0, 1)))
        assert mathcheck.answer_type("exr-calc-a-parts") == "set"
        with pytest.raises(ManualAnswer, match="manual_checked"):
            mathcheck.answer("exr-calc-a-proof")
        with pytest.raises(KeyError, match="no Answer"):
            mathcheck.answer("exr-calc-a-missing")
        assert state.end()[1] == {"exr-calc-a-half", "exr-calc-a-parts", "exr-calc-a-proof", "exr-calc-a-missing"}
    finally:
        state.test, state.assertions, state.answers = saved


# ── The AST fixture: a mystmd upgrade that changes an answer's shape fails here ──

FIXTURE = HERE / "fixtures" / "answers-ast.json"


def _fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _exercise(mdast, label):
    def walk(node):
        yield node
        for c in node.get("children") or []:
            yield from walk(c)

    ex = next(node for node in walk(mdast) if node.get("type") == "exercise" and node.get("label") == label)
    adm = next(c for c in ex["children"] if c.get("type") == "admonition" and "answer" in c.get("class", "").split())
    return [c for c in adm["children"] if c["type"] != "admonitionTitle"]


def test_ast_fixture_matches_the_pinned_mystmd():
    pinned = json.loads((REPO / "package.json").read_text())["dependencies"]["mystmd"]
    assert _fixture()["mystmd"] == pinned, "regenerate with uv run python verify/fixtures/make_answers_ast.py"
    spec = importlib.util.spec_from_file_location("make_answers_ast", HERE / "fixtures" / "make_answers_ast.py")
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    assert _fixture()["page"] == gen.PAGE, "the generator's page changed: regenerate the fixture"


def test_ast_fixture_shapes():
    """The three shapes that extract_answers.py reads (06 §6.1)."""
    mdast = _fixture()["mdast"]
    (para,) = _exercise(mdast, "exr-calc-shapes-symbolic")
    assert [(c["type"], c.get("value")) for c in para["children"]] == [("inlineMath", r"\frac{1}{2}")]
    (para,) = _exercise(mdast, "exr-calc-shapes-numeric")
    assert [(c["type"], c.get("value")) for c in para["children"]] == [("text", "0.69")]
    (para,) = _exercise(mdast, "exr-calc-shapes-power")
    (span,) = para["children"]
    assert span["type"] == "span"
    assert [c["type"] for c in span["children"]] == ["text", "superscript"]
    assert span["children"][0]["value"] == "2"
    assert [(c["type"], c.get("value")) for c in span["children"][1]["children"]] == [("text", "10")]


def test_ast_fixture_extracts_and_parses():
    from extract_answers import Extractor  # scripts/ is on pytest's pythonpath
    from project import Reporter

    rep, answers = Reporter(quiet=True), {}
    Extractor(rep).page("index.md", Path("index.md"), _fixture()["mdast"], answers, {})
    assert not rep.diagnostics
    latex = {label: (a["type"], a["latex"]) for label, a in answers.items()}
    assert latex == {
        "exr-calc-shapes-symbolic": ("expr", [r"\frac{1}{2}"]),
        "exr-calc-shapes-numeric": ("numeric-5e-3", ["0.69"]),
        "exr-calc-shapes-power": ("expr", ["2^{10}"]),
        "exr-calc-shapes-parts": ("expr", ["-3", "10^{-3}", r"\sqrt{2}, \pi"]),
        "exr-calc-shapes-set": ("set", ["[0, 1)"]),
        "exr-calc-shapes-manual": ("manual", [r"\delta = \eps / 3"]),
    }
    assert answers["exr-calc-shapes-manual"]["manual"] is True
    same(parse_answer(r"\frac{1}{2}"), sp.Rational(1, 2))
    same(parse_answer("0.69", "numeric-5e-3"), sp.Rational(69, 100))
    same(parse_answer("2^{10}"), sp.Integer(1024))
    parts = tuple(parse_answer(s) for s in latex["exr-calc-shapes-parts"][1])
    same(parts, (sp.Integer(-3), sp.Rational(1, 1000), (sp.Pow(2, sp.Rational(1, 2)), sp.pi)))
    same(parse_answer("[0, 1)", "set"), sp.Interval.Ropen(0, 1))
