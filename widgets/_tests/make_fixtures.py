"""Write widgets/_tests/fixtures/function-plot.json and epsilon-delta.json: the values that
widgets/_tests/*.test.mjs expect from widgets/_lib/, computed by SymPy (docs/plan/06 §6.2).
Never edit the JSON by hand; change the cases here and run

    uv run python widgets/_tests/make_fixtures.py

tests/test_widget_checks.py fails if the committed JSON differs from what this writes, so the
fixtures cannot go stale. The table cases are read from every function-plot figure on the pages
in the toc and in templates/topic.md, so a new figure gets its table checked automatically; so
are the δ of every epsilon-delta figure, at its starting ε and at both ends of its ε slider.

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
OUT_EPSILON_DELTA = REPO / "widgets" / "_tests" / "fixtures" / "epsilon-delta.json"
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


def site_configs(widget: str = "function-plot"):
    """(where, config) of every `widget` figure in the toc pages and templates/topic.md."""
    project = Project(REPO / "content")
    sources = [(p.rel, p.text) for p in project.pages]
    sources.append(("templates/topic.md", (REPO / "templates" / "topic.md").read_text(encoding="utf-8")))
    for where, text in sources:
        for d in ms.parse(text).directives():
            if d.name == "anywidget" and d.arg.endswith(f"/{widget}.mjs"):
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


# ── epsilon-delta: the exact largest δ on each side ──────────────────────────

# The relative tolerance of the reported δ (widgets/_lib/epsdelta.mjs rounds down to 6
# significant digits): exact·(1 − TOLERANCE) ≤ reported ≤ exact.
EPSILON_DELTA_TOLERANCE = 2e-5

EPSILON_DELTA = [
    # (what the case shows, f, a, L, xRange, [ε, …])
    ("a linear f: δ = ε/2 on both sides", "2*x - 1", 3, 5, [0, 6], [0.1, 0.5]),
    ("x² at a = 2: the two sides differ", "x^2", 2, 4, [0, 3.5], [0.05, 0.1, 0.5, 1.5]),
    ("√x at a small a: on the left, f is undefined below 0", "sqrt(x)", 0.04, 0.2, [-0.1, 0.5], [0.1, 0.3]),
    ("1/x away from 0", "1/x", 1, 1, [0.2, 3], [0.1, 0.5]),
    ("a jump: no δ on the left while ε is below the gap", "x + sign(x)", 0, 1, [-2, 2], [0.5, 1.9, 2.5]),
    ("sin(1/x) at 0: no δ for ε < 1, any δ for ε > 1", "sin(1/x)", 0, 0, [-1, 1], [0.5, 0.9, 1.2]),
    ("an unbounded f: no δ", "1/x^2", 0, 1, [-1, 1], [0.5, 5]),
    ("a wrong L (4.5 for x² at 2): no δ while ε < 0.5", "x^2", 2, 4.5, [0, 3.5], [0.1, 0.4, 0.7]),
]


def _intervals(s: sp.Set) -> list[sp.Interval] | None:
    """The intervals of a union of intervals, or None if SymPy left it unsolved."""
    if s is sp.S.EmptySet:
        return []
    if isinstance(s, sp.Interval):
        return [s]
    if isinstance(s, sp.Union) and all(isinstance(t, sp.Interval) for t in s.args):
        return list(s.args)
    return None


def exact_side(expr, var, a, L, eps, side: int, reach) -> dict:
    """The largest δ on one side (side −1 left, +1 right), exactly:
    sup{t ≤ reach : |f(x) − L| < ε for all x with 0 < ±(x − a) < t}. SymPy solves
    |f(x) − L| < ε on (a, a + reach) (or (a − reach, a)), and δ is the length of the solution
    interval that starts at a; there is none when no interval starts there. Where SymPy cannot
    solve the inequality (sin(1/x)), the one-sided limit decides that no δ exists: its
    distance from L, or the largest distance of its accumulation bounds, exceeds ε."""
    a, L, eps, reach = (exact(v) for v in (a, L, eps, reach))
    lim = sp.limit(expr, var, a, "+" if side > 0 else "-")
    if isinstance(lim, sp.AccumBounds):
        gap = sp.Max(sp.Abs(lim.min - L), sp.Abs(lim.max - L))
    elif lim.is_finite and lim.is_real:
        gap = sp.Abs(lim - L)
    else:
        gap = sp.oo
    if gap == eps:
        raise ValueError(f"{expr} at {a}: ε = {eps} is exactly the gap {gap}; choose another ε")
    window = sp.Interval.open(a, a + reach) if side > 0 else sp.Interval.open(a - reach, a)
    good = _intervals(sp.solveset(sp.Abs(expr - L) < eps, var, window))
    if good is None:
        if gap > eps:
            return {"none": True, "delta": 0, "capped": False, "sympy": f"limit {lim}, |limit − L| > ε"}
        raise ValueError(f"SymPy cannot solve |{expr} − {L}| < {eps} on {window}")
    touching = [i for i in good if (i.inf if side > 0 else i.sup) == a]
    if not touching:
        assert gap > eps, f"{expr}: no solution interval at a, but the limit {lim} is within ε"
        return {"none": True, "delta": 0, "capped": False, "sympy": f"no solution interval starts at a; limit {lim}"}
    assert gap < eps, f"{expr}: a solution interval at a, but the limit {lim} is not within ε"
    delta = sp.nsimplify(touching[0].sup - a if side > 0 else a - touching[0].inf)
    return {"none": False, "delta": float(sp.N(delta, 30)), "capped": bool(delta == reach), "sympy": str(delta)}


def epsilon_delta_case(source, what, f, a, L, x_range, eps) -> dict:
    expr, var, _ = to_sympy(f, "x", [])
    reach = (exact(a) - exact(x_range[0]), exact(x_range[1]) - exact(a))
    return {
        "source": source, "case": what, "f": f, "a": a, "L": L, "xRange": x_range, "eps": eps,
        "left": exact_side(expr, var, a, L, eps, -1, reach[0]),
        "right": exact_side(expr, var, a, L, eps, 1, reach[1]),
    }


def epsilon_delta_cases() -> list[dict]:
    cases = [epsilon_delta_case("make_fixtures.py", what, f, a, L, xr, eps)
             for what, f, a, L, xr, epss in EPSILON_DELTA for eps in epss]
    for where, c in site_configs("epsilon-delta"):
        for eps in dict.fromkeys([c["eps"], *c["epsRange"]]):
            cases.append(epsilon_delta_case(where, "a figure on the site", c["f"], c["a"], c["L"], c["xRange"], eps))
    return cases


def build_epsilon_delta() -> dict:
    return {
        "_comment": "Written by widgets/_tests/make_fixtures.py from SymPy; do not edit by hand.",
        "sympy": sp.__version__,
        "tolerance": EPSILON_DELTA_TOLERANCE,
        "cases": epsilon_delta_cases(),
    }


def outputs() -> dict[Path, dict]:
    """Every fixture file and its contents."""
    return {OUT: build(), OUT_EPSILON_DELTA: build_epsilon_delta()}


def render(data: dict) -> str:
    return json.dumps(data, indent=1, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    for path, data in outputs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(data), encoding="utf-8")
        print(f"wrote {path.relative_to(REPO)}")
