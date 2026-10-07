"""scripts/check_widgets.py beyond its four fixtures (test_checkers.py): every part of the figure
rule, paths, JSON, the schema's strictness, the rules shared with widgets/_lib (one table,
widgets/_tests/fixtures/function-plot-invalid.json, run by both), and the freshness of the
SymPy fixtures that the widget tests read.
"""

from __future__ import annotations

import importlib.util
import json
import shutil

import jsonschema
import pytest

import check_widgets
from project import REPO, Project, Reporter

CLEAN = REPO / "tests" / "fixtures" / "clean"
PAGE = "content/calculus/limits/limit-of-a-function.md"
SCHEMA = check_widgets.load_schema("function-plot")
EPS_SCHEMA = check_widgets.load_schema("epsilon-delta")
FIGURE_START = "::::{figure}\n:label: wdg-calc-limit-average-speed\n"


def check(tmp_path, old, new):
    shutil.copytree(CLEAN, tmp_path / "f")
    page = tmp_path / "f" / PAGE
    text = page.read_text(encoding="utf-8")
    assert old in text
    page.write_text(text.replace(old, new, 1), encoding="utf-8")
    rep = Reporter(quiet=True)
    check_widgets.check(Project(tmp_path / "f" / "content"), rep)
    return [(d.line, d.message) for d in rep.errors]


def test_clean_template_passes(tmp_path):
    assert check(tmp_path, "", "") == []


@pytest.mark.parametrize("old, new, line, message", [
    # not in a figure at all
    (FIGURE_START, "::::{admonition} A box\n", 49, "{anywidget} must be the only content of a {figure} labelled wdg-…"),
    # something else in the figure before the widget
    (FIGURE_START, FIGURE_START + "\nAn intro paragraph.\n", 47, "a widget figure holds only the {anywidget}, then its caption"),
    # a figure label that is not wdg-
    (":label: wdg-calc-limit-average-speed\n", ":label: fig-calc-limit-average-speed\n", 48, "a widget figure needs a wdg- label, not fig-calc-limit-average-speed"),
    # the path does not point into widgets/
    ("../../../widgets/function-plot.mjs", "../../widgets/function-plot.mjs", 50, "point it at widgets/<name>.mjs; from this page, ../../../widgets/<name>.mjs"),
    ("../../../widgets/function-plot.mjs", "../../../widgets/_lib/plot.mjs", 50, "point it at widgets/<name>.mjs"),
    # the body is not JSON
    ('  "variable": "h",', "  'variable': 'h',", 53, "the body is not valid JSON"),
    # a typo inside a nested object is rejected too
    ('"hole": { "x": 0 }', '"hole": { "x": 0, "radius": 2 }', 57, "hole: Additional properties are not allowed ('radius' was unexpected)"),
    ('"trace": { "x": 0.5 }', '"trace": { "x": "0.5" }', 58, "trace.x: '0.5' is not of type 'number'"),
    # a rule JSON Schema cannot express
    ('"xRange": [-1, 1]', '"xRange": [1, -1]', 54, "widget function-plot: xRange: the first number must be smaller than the second"),
    ('"f": "(5*(1+h)^2 - 5)/h"', '"f": "(5(1+h)^2 - 5)/h"', 52, "widget function-plot: f: missing * after 5: write 5*( (at position 2)"),
    # epsilon-delta: its schema, and the rules it cannot express
    ('"f": "x^2", "a": 2, "L": 4,', '"f": "x^2", "a": 2, "L": 4, "limit": 4,', 102, "widget epsilon-delta: config: Additional properties are not allowed ('limit' was unexpected)"),
    ('"f": "x^2", "a": 2, "L": 4,', '"f": "x^2", "L": 4,', 101, "widget epsilon-delta: config: 'a' is a required property"),
    ('"eps": 0.5, "epsRange": [0.05, 1.5]', '"eps": 0.5, "epsRange": [0, 1.5]', 103, "widget epsilon-delta: epsRange.0: 0 is less than or equal to the minimum of 0"),
    ('"eps": 0.5, "epsRange": [0.05, 1.5]', '"eps": 0.01, "epsRange": [0.05, 1.5]', 103, "widget epsilon-delta: eps: must lie inside epsRange"),
    ('"f": "x^2", "a": 2, "L": 4,', '"f": "x^2", "a": 3.5, "L": 4,', 102, "widget epsilon-delta: a: must lie strictly inside xRange"),
    ('"f": "x^2", "a": 2, "L": 4,', '"f": "x^2", "a": 2, "L": 12,', 102, "widget epsilon-delta: L: must lie inside yRange"),
    ('"f": "x^2", "a": 2, "L": 4,', '"f": "x*x(1)", "a": 2, "L": 4,', 102, "widget epsilon-delta: f: x is not a function"),
])
def test_figure_and_config_rules(tmp_path, old, new, line, message):
    errors = check(tmp_path, old, new)
    assert any(message in m for _, m in errors), errors
    assert [ln for ln, m in errors if message in m][0] == line, errors


def test_wdg_figure_without_a_widget(tmp_path):
    errors = check(tmp_path, "## Main results\n", "## Main results\n\n:::{figure} ./x.svg\n:label: wdg-calc-limit-static\n\nA picture.\n:::\n")
    assert any("a wdg- label is for a figure that holds a widget" in m for _, m in errors), errors


@pytest.mark.parametrize("case", json.loads((REPO / "widgets/_tests/fixtures/function-plot-invalid.json").read_text(encoding="utf-8"))["cases"])
def test_rules_shared_with_widgets_lib(case):
    """The same table as widgets/_tests/plot.test.mjs: both implementations report each problem."""
    config = case["config"]
    assert not list(jsonschema.Draft202012Validator(SCHEMA).iter_errors(config)), "the cases must be schema-valid"
    problems = check_widgets.function_plot_problems(config, SCHEMA)
    if case["problem"] is None:
        assert problems == []
    else:
        assert any(case["problem"] in p for p in problems), problems


@pytest.mark.parametrize("config, where", [
    ({"f": "x", "xRange": [0, 1]}, "'yRange' is a required property"),
    ({"f": "x", "xRange": [0, 1], "yRange": [0, 1], "colour": "red"}, "'colour' was unexpected"),
    ({"f": "x", "xRange": [0, 1], "yRange": [0, 1], "parameters": {"a": {"value": 1, "min": 0, "max": 2, "stpe": 1}}}, "'stpe' was unexpected"),
    ({"f": "x", "xRange": [0, 1], "yRange": [0, 1], "parameters": {"e": {"value": 1, "min": 0, "max": 2}}}, "'e' does not match"),
    ({"f": "x", "variable": "xx", "xRange": [0, 1], "yRange": [0, 1]}, "'xx' does not match"),
    ({"f": "x", "xRange": [0, 1, 2], "yRange": [0, 1]}, "is too long"),
    ({"f": "x", "xRange": [0, 1], "yRange": [0, 1], "table": {"points": []}}, "should be non-empty"),
])
def test_schema_rejects_typos_and_bad_shapes(config, where):
    messages = [e.message for e in jsonschema.Draft202012Validator(SCHEMA).iter_errors(config)]
    assert any(where in m for m in messages), messages


@pytest.mark.parametrize("case", json.loads((REPO / "widgets/_tests/fixtures/epsilon-delta-invalid.json").read_text(encoding="utf-8"))["cases"])
def test_epsilon_delta_rules_shared_with_widgets_lib(case):
    """The same table as widgets/_tests/epsdelta.test.mjs: both implementations report each problem."""
    config = case["config"]
    assert not list(jsonschema.Draft202012Validator(EPS_SCHEMA).iter_errors(config)), "the cases must be schema-valid"
    problems = check_widgets.epsilon_delta_problems(config, EPS_SCHEMA)
    if case["problem"] is None:
        assert problems == []
    else:
        assert any(case["problem"] in p for p in problems), problems


@pytest.mark.parametrize("config, where", [
    ({"f": "x", "a": 0, "L": 0, "eps": 0.5, "epsRange": [0.1, 1], "xRange": [-1, 1]}, "'yRange' is a required property"),
    ({"f": "x", "a": 0, "L": 0, "eps": 0, "epsRange": [0.1, 1], "xRange": [-1, 1], "yRange": [-1, 1]}, "0 is less than or equal to the minimum of 0"),
    ({"f": "x", "a": 0, "L": 0, "eps": 0.5, "epsRange": [0.1, 1], "delta": -1, "xRange": [-1, 1], "yRange": [-1, 1]}, "-1 is less than or equal to the minimum of 0"),
    ({"f": "x", "a": 0, "L": 0, "eps": 0.5, "epsRange": [0.1, 1, 2], "xRange": [-1, 1], "yRange": [-1, 1]}, "is too long"),
    ({"f": "x", "a": 0, "L": 0, "eps": 0.5, "epsRange": [0.1, 1], "xRange": [-1, 1], "yRange": [-1, 1], "variable": "t"}, "'variable' was unexpected"),
])
def test_epsilon_delta_schema_rejects_typos_and_bad_shapes(config, where):
    messages = [e.message for e in jsonschema.Draft202012Validator(EPS_SCHEMA).iter_errors(config)]
    assert any(where in m for m in messages), messages


def load_make_fixtures():
    spec = importlib.util.spec_from_file_location("make_fixtures", REPO / "widgets" / "_tests" / "make_fixtures.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_widget_fixtures_are_fresh():
    """widgets/_tests/fixtures/function-plot.json and epsilon-delta.json are exactly what
    make_fixtures.py writes now."""
    mod = load_make_fixtures()
    for path, data in mod.outputs().items():
        committed = path.read_text(encoding="utf-8")
        assert committed == mod.render(data), f"{path.name}: run uv run python widgets/_tests/make_fixtures.py and commit the result"


def test_every_site_widget_table_is_in_the_fixtures():
    """The widget tests check the table of every function-plot figure on the site."""
    data = json.loads((REPO / "widgets" / "_tests" / "fixtures" / "function-plot.json").read_text(encoding="utf-8"))
    sources = {t["source"].split(":")[0] for t in data["tables"]}
    assert {"about/how-to-read.md", "templates/topic.md"} <= sources


def test_epsilon_delta_fixtures_refuse_a_wrong_solveset():
    """SymPy 1.14 solves |abs(x) − 1/2| < 13/10 on (1/2, 3) as the whole interval (it is
    (1/2, 1.8)); make_fixtures.py checks SymPy's interval and refuses it instead of writing
    δ₊ = 5/2. Its correct answers still pass: δ₊ = 1/10 for ε = 1/10."""
    mod = load_make_fixtures()
    with pytest.raises(ValueError, match="does not check out"):
        mod.epsilon_delta_case("test", "abs", "abs(x)", 0.5, 0.5, [-1.5, 3], 1.3)
    case = mod.epsilon_delta_case("test", "abs", "abs(x)", 0.5, 0.5, [-1.5, 3], 0.1)
    assert case["right"]["sympy"] == "1/10" and case["left"]["sympy"] == "1/10"
