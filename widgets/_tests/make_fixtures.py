"""Write widgets/_tests/fixtures/function-plot.json: the values that widgets/_tests/*.test.mjs
expect from widgets/_lib/, computed by SymPy (docs/plan/06 §6.2). Never edit the JSON by hand;
change the cases here and run

    uv run python widgets/_tests/make_fixtures.py

tests/test_widget_checks.py fails if the committed JSON differs from what this writes, so the
fixtures cannot go stale. The table cases are read from every function-plot figure on the pages
in the toc and in templates/topic.md, so a new figure gets its table checked automatically.

Expressions are translated token by token (scripts/check_widgets.py tokenizes them exactly as
widgets/_lib/expression.mjs does) into SymPy: decimals become exact rationals, `^` becomes
`**`, ln is log, cbrt is the real cube root, pi and e are SymPy's.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import check_widgets  # noqa: E402
import myst_source as ms  # noqa: E402
from project import Project  # noqa: E402

OUT = REPO / "widgets" / "_tests" / "fixtures" / "function-plot.json"
SCHEMA = check_widgets.load_schema("function-plot")
FUNCTIONS = SCHEMA["$defs"]["functions"]["enum"]
CONSTANTS = SCHEMA["$defs"]["constants"]["enum"]

SYMPY_FUNCTIONS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh, "exp": sp.exp, "ln": sp.log, "sqrt": sp.sqrt,
    "cbrt": lambda z: sp.real_root(z, 3), "abs": sp.Abs, "floor": sp.floor, "ceil": sp.ceiling, "sign": sp.sign,
}
assert set(SYMPY_FUNCTIONS) == set(FUNCTIONS), "keep SYMPY_FUNCTIONS in step with the schema"


def to_sympy(src: str, variable: str, params: list[str]) -> tuple[sp.Expr, sp.Symbol, dict]:
    names = [variable, *params]
    tokens = check_widgets.check_expression(src, names, FUNCTIONS, CONSTANTS)
    symbols = {n: sp.Symbol(n, real=True) for n in names}
    local = {**{f"F_{k}": v for k, v in SYMPY_FUNCTIONS.items()}, **{f"S_{k}": v for k, v in symbols.items()},
             "pi": sp.pi, "E": sp.E, "R": sp.Rational}
    out = []
    for kind, value, _ in tokens:
        if kind == "num":
            out.append(f"R('{value}')")
        elif kind == "name":
            out.append(f"F_{value}" if value in FUNCTIONS else "pi" if value == "pi" else "E" if value == "e" else f"S_{value}")
        else:
            out.append("**" if value == "^" else value)
    expr = sp.sympify(" ".join(out), locals=local, evaluate=True)
    return expr, symbols[variable], symbols


def exact(x) -> sp.Rational:
    return sp.Rational(repr(float(x))) if not isinstance(x, sp.Basic) else x


def value_at(expr, var, x, subs=None) -> float | None:
    """f(x) as a float, or None where it is undefined or not real."""
    v = expr.subs({**(subs or {}), var: exact(x)})
    v = sp.N(v, 30)
    if v.has(sp.zoo, sp.oo, -sp.oo, sp.nan) or not v.is_real:
        return None
    return float(v)


def param_subs(symbols, params: dict) -> dict:
    return {symbols[k]: exact(v) for k, v in params.items()}


# ── Cases ────────────────────────────────────────────────────────────────────

EXPRESSIONS = [
    # (f, variable, params, points): every function, constant and operator rule, and undefined values
    ("sin(x) + cos(x) + tan(x)", "x", {}, [-1.2, 0, 0.5, 1]),
    ("asin(x) + acos(x) + atan(x)", "x", {}, [-1, -0.3, 0, 0.7, 1, 1.5]),
    ("sinh(x) - cosh(x) + tanh(x)", "x", {}, [-2, 0, 0.5, 3]),
    ("exp(x) + ln(x)", "x", {}, [-1, 0, 0.1, 1, 2.5]),
    ("sqrt(x) + cbrt(x)", "x", {}, [-8, -1, 0, 2, 27]),
    ("abs(x) + floor(x) + ceil(x) + sign(x)", "x", {}, [-2.5, -1, 0, 0.5, 3]),
    ("pi*x + e", "x", {}, [0, 1, -0.25]),
    ("2^3^x", "x", {}, [0, 1, 2]),
    ("-x^2 + 2*-x", "x", {}, [-1, 3]),
    ("1/x", "x", {}, [-0.5, 0, 4]),
    ("1.5e-2*t^2 + .5", "t", {}, [0, 10]),
    ("a*sin(b*(x - c)) + d", "x", {"a": 2, "b": 0.5, "c": 1, "d": -1}, [-3, 0, 1, 2.5]),
]

HOLES = [
    # (f, variable, x, scale): SymPy decides the limit, or that there is none to draw
    ("(5*(1+h)^2 - 5)/h", "h", 0, 2),
    ("sin(x)/x", "x", 0, 8),
    ("(x^2 - 1)/(x - 1)", "x", 1, 4),
    ("(1 - cos(x))/x^2", "x", 0, 6),
    ("(sqrt(x + 4) - 2)/x", "x", 0, 4),
    ("(exp(x) - 1)/x", "x", 0, 4),
    ("(x^3 - 8)/(x - 2)", "x", 2, 6),
    ("abs(x)/x", "x", 0, 4),
    ("1/x^2", "x", 0, 4),
    ("sin(1/x)", "x", 0, 2),
]

SAMPLES = [
    # (f, a, b, n, jump): the grid values, and where SymPy says the graph breaks
    ("x^3 - x", -2, 2, 40, 0.2),
    ("1/x", -1, 1, 40, 0.2),
    ("1/x", -1, 1.05, 40, 0.2),
    ("tan(x)", -2, 2, 40, 0.2),
    ("1/(x^2 - 1)", -3, 3, 60, 0.3),
    ("floor(x)", -2.05, 2.05, 40, 0.2),
    ("sign(x)", -1, 1.05, 40, 0.1),
    ("20*x^3", -1, 1, 40, 2),
    ("sqrt(1 - x^2)", -1.5, 1.5, 30, 0.1),
]


def limit_case(f, variable, x0, scale):
    expr, var, _ = to_sympy(f, variable, [])
    a = sp.Rational(repr(float(x0)))
    left, right = sp.limit(expr, var, a, "-"), sp.limit(expr, var, a, "+")
    case = {"f": f, "variable": variable, "x": x0, "scale": scale}
    finite = all(v.is_finite and v.is_real for v in (left, right))
    if finite and sp.simplify(left - right) == 0:
        case["y"] = float(sp.N(left, 30))
    else:
        case["error"] = True
        case["sympy"] = f"left {left}, right {right}"
    return case


def breaks(expr, var, a, b) -> list[float]:
    """The points of (a, b) where expr is not continuous: singularities, and the jumps of
    floor, ceiling and sign (where their argument crosses an integer, or zero)."""
    interval = sp.Interval.open(exact(a), exact(b))
    points = set(sp.singularities(expr, var, interval))
    for node in sp.preorder_traversal(expr):
        if isinstance(node, (sp.floor, sp.ceiling)):
            g = node.args[0]
            lo, hi = sp.floor(sp.minimum(g, var, interval)), sp.ceiling(sp.maximum(g, var, interval))
            for k in range(int(lo), int(hi) + 1):
                points |= set(sp.solveset(sp.Eq(g, k), var, interval))
        elif isinstance(node, sp.sign):
            points |= set(sp.solveset(sp.Eq(node.args[0], 0), var, interval))
    return sorted(float(p) for p in points)


def sample_case(f, a, b, n, jump):
    expr, var, _ = to_sympy(f, "x", [])
    grid = [exact(a) + (exact(b) - exact(a)) * sp.Rational(i, n) for i in range(n + 1)]
    return {
        "f": f, "a": a, "b": b, "n": n, "jump": jump,
        "values": [value_at(expr, var, x) for x in grid],
        "breaks": breaks(expr, var, a, b),
    }


def site_configs():
    """(where, config) of every function-plot figure in the toc pages and templates/topic.md."""
    project = Project(REPO / "content")
    sources = [(p.rel, p.text) for p in project.pages]
    sources.append(("templates/topic.md", (REPO / "templates" / "topic.md").read_text(encoding="utf-8")))
    for where, text in sources:
        for d in ms.parse(text).directives():
            if d.name == "anywidget" and d.arg.endswith("/function-plot.mjs"):
                yield f"{where}:{d.line}", json.loads("\n".join(t for _, t in d.raw))


def table_cases():
    cases = []
    for where, config in site_configs():
        if "table" not in config:
            continue
        variable = config.get("variable", "x")
        specs = config.get("parameters") or {}
        expr, var, symbols = to_sympy(config["f"], variable, list(specs))
        settings = [("defaults", {k: p["value"] for k, p in specs.items()})]
        if specs:  # one step up on the first slider, as a reader pressing → once
            first, p = next(iter(specs.items()))
            step = p.get("step", (p["max"] - p["min"]) / 100)
            settings.append((f"{first} one step up", {**settings[0][1], first: min(p["value"] + step, p["max"])}))
        hole_x = config.get("hole", {}).get("x")
        for label, params in settings:
            subs = param_subs(symbols, params)
            cases.append({
                "source": where, "setting": label, "f": config["f"], "variable": variable, "params": params,
                "holeX": hole_x, "points": config["table"]["points"],
                "values": [None if x == hole_x else value_at(expr, var, x, subs) for x in config["table"]["points"]],
            })
    return cases


def build() -> dict:
    expressions = []
    for f, variable, params, points in EXPRESSIONS:
        expr, var, symbols = to_sympy(f, variable, list(params))
        subs = param_subs(symbols, params)
        expressions.append({"f": f, "variable": variable, "params": params, "points": points,
                            "values": [value_at(expr, var, x, subs) for x in points]})
    return {
        "_comment": "Written by widgets/_tests/make_fixtures.py from SymPy; do not edit by hand.",
        "sympy": sp.__version__,
        "expressions": expressions,
        "holes": [limit_case(*c) for c in HOLES],
        "samples": [sample_case(*c) for c in SAMPLES],
        "tables": table_cases(),
    }


def render(data: dict) -> str:
    return json.dumps(data, indent=1, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(build()), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
