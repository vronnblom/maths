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
    ("|x| at 1/2: SymPy 1.14 solves the raw inequality wrongly (review F5)", "abs(x)", 0.5, 0.5, [-1.5, 3], [0.1, 1.3, 2.49]),
]

class OracleRefused(ValueError):
    """SymPy could not certify a case: make_fixtures.py writes nothing rather than a guess."""


def _resolved(s: sp.Set) -> bool:
    """Whether s is a finite union of intervals and points (what the oracle can certify)."""
    if s is sp.S.EmptySet or isinstance(s, sp.Interval):
        return True
    if isinstance(s, sp.FiniteSet):
        return all(v.is_real for v in s.args)
    return isinstance(s, sp.Union) and all(_resolved(t) for t in s.args)


_PIECEWISE = (sp.Abs, sp.sign, sp.floor, sp.ceiling)


def _breaks(expr, var, window: sp.Interval) -> list:
    """The points of the open window where an argument of abs, sign, floor or ceil crosses a
    break (0, or an integer) or has a singularity: between two of them each of these functions
    is a fixed formula."""
    points = set()
    for node in sp.preorder_traversal(expr):
        if isinstance(node, _PIECEWISE):
            g = node.args[0]
            points |= set(sp.singularities(g, var, window))
            if isinstance(node, (sp.floor, sp.ceiling)):
                lo, hi = sp.floor(sp.minimum(g, var, window)), sp.ceiling(sp.maximum(g, var, window))
                if not (lo.is_finite and hi.is_finite):
                    raise OracleRefused(f"{node} is unbounded on {window}")
                for k in range(int(lo), int(hi) + 1):
                    s = sp.solveset(sp.Eq(g, k), var, window)
                    if not (s is sp.S.EmptySet or isinstance(s, sp.FiniteSet)):
                        raise OracleRefused(f"SymPy cannot find where {g} = {k} on {window}")
                    points |= set(s)
            else:
                s = sp.solveset(sp.Eq(g, 0), var, window)
                if not (s is sp.S.EmptySet or isinstance(s, sp.FiniteSet)):
                    raise OracleRefused(f"SymPy cannot find where {g} = 0 on {window}")
                points |= set(s)
    return sorted(points, key=lambda p: sp.N(p, 30))


def _fixed(expr, var, at):
    """expr with each abs, sign, floor and ceil replaced by the formula it has near x = at."""
    if not expr.args:
        return expr
    args = [_fixed(arg, var, at) for arg in expr.args]
    if isinstance(expr, _PIECEWISE):
        g = args[0]
        v = g.subs(var, at)
        if isinstance(expr, sp.Abs):
            return g if v >= 0 else -g
        if isinstance(expr, sp.sign):
            return sp.sign(v)
        return sp.floor(v) if isinstance(expr, sp.floor) else sp.ceiling(v)
    return expr.func(*args)


def _at(expr, var, x):
    """f(x) exactly, or None where f is undefined (not a finite real number)."""
    v = sp.simplify(expr.subs(var, x))
    if v.has(sp.zoo, sp.oo, -sp.oo, sp.nan) or v.is_real is False or not v.is_finite:
        return None
    if v.is_real is None and sp.im(sp.N(v, 50)) != 0:
        return None
    return v


def _sign(v) -> int:
    """The sign of an exact real number, decided by SymPy or at 60 digits away from 0."""
    v = sp.nsimplify(v) if v.is_Float else v
    if v.is_zero:
        return 0
    if v.is_positive:
        return 1
    if v.is_negative:
        return -1
    n = sp.N(v, 60)
    if abs(n) > sp.Float("1e-45", 60):
        return 1 if n > 0 else -1
    raise OracleRefused(f"SymPy cannot decide the sign of {v}")


def _fails_at(expr, var, x, L, eps) -> bool:
    """Whether the band condition fails at x: f undefined there, or |f(x) − L| ≥ ε."""
    v = _at(expr, var, x)
    return v is None or _sign(sp.Abs(v - L) - eps) >= 0


def _bad_and_good(expr, var, window: sp.Interval, L, eps, split=True):
    """(B, G, U): where the band condition fails in the window (f undefined, or |f − L| ≥ ε),
    where it holds, each from its own solveset, and where f is undefined; without abs in the band inequality
    (L − ε < f < L + ε). With split, the window is cut at the breaks of abs, sign, floor and
    ceil, each piece is solved with their fixed formula, and the breaks are decided one by one."""
    points = _breaks(expr, var, window) if split else []
    ends = [window.left, *points, window.right]
    bad, good, undefined = [], [], []
    for lo, hi in zip(ends, ends[1:]):
        piece = sp.Interval.open(lo, hi)
        g = _fixed(expr, var, (lo + hi) / 2) if split else expr
        try:
            domain = sp.calculus.util.continuous_domain(g, var, piece)
        except NotImplementedError as e:
            raise OracleRefused(f"SymPy cannot find where {g} is defined on {piece}") from e
        undefined.append(sp.Complement(piece, domain))
        bad.append(sp.solveset(g - L >= eps, var, domain))
        bad.append(sp.solveset(g - L <= -eps, var, domain))
        good.append(sp.Intersection(sp.solveset(g - L < eps, var, domain), sp.solveset(g - L > -eps, var, domain)))
    for p in points:
        if _at(expr, var, p) is None:
            undefined.append(sp.FiniteSet(p))
        (bad if _fails_at(expr, var, p, L, eps) else good).append(sp.FiniteSet(p))
    undefined = sp.Union(*undefined)
    return sp.Union(*bad, undefined), sp.Union(*good), undefined


def _accumulates(expr, var, value, a, side) -> bool:
    """Whether f = value at points that accumulate at a from `side`: SymPy solves f = value as
    images n ↦ h(n) of the integers, and h(n) → a from that side as n → ±∞."""
    s = sp.solveset(sp.Eq(expr, value), var, sp.S.Reals)
    images = s.args if isinstance(s, sp.Union) else [s]
    for im in images:
        if not (isinstance(im, sp.ImageSet) and im.base_sets == (sp.S.Integers,)):
            continue
        n, = im.lamda.variables
        h = im.lamda.expr
        for end in (sp.oo, -sp.oo):
            if sp.limit(h, n, end) != a:
                continue
            far = 10**6 if end is sp.oo else -10**6
            if all(_sign(side * (h.subs(n, far * k) - a)) > 0 for k in (1, 2, 3)):
                return True
    return False


def _no_delta_by_limit(expr, var, a, L, eps, side):
    """A certificate that no δ exists on `side` when solveset cannot solve the inequality: the
    one-sided limit is infinite, or finite and farther than ε from L, or it oscillates
    (AccumBounds) and f takes a value farther than ε from L at points accumulating at a."""
    lim = sp.limit(expr, var, a, "+" if side > 0 else "-")
    if isinstance(lim, sp.AccumBounds):
        for value in (lim.min, lim.max):
            if _sign(sp.Abs(value - L) - eps) > 0 and _accumulates(expr, var, value, a, side):
                return f"f = {value} at points accumulating at a, and |{value} − L| > ε"
        return None
    if lim.is_infinite or lim in (sp.zoo, sp.oo, -sp.oo):
        return f"limit {lim}"
    if lim.is_finite and lim.is_real and _sign(sp.Abs(lim - L) - eps) > 0:
        return f"limit {lim}, |limit − L| > ε"
    return None


def exact_side(expr, var, a, L, eps, side: int, reach, split=True) -> dict:
    """The largest δ on one side (side −1 left, +1 right), exactly:
    sup{t ≤ reach : f defined and |f(x) − L| < ε for all x with 0 < ±(x − a) < t}.

    SymPy certifies it rather than sampling for it (review F5):
    - route A, from the complement: B = {x in the window : f undefined or |f(x) − L| ≥ ε};
      δ = inf B − a on the right (a − sup B on the left), "none" if that is 0, capped if B = ∅;
    - route B, from the inequality itself: G = {x in the window : L − ε < f(x) < L + ε}; δ is
      the length of the interval of G that starts at a, "none" if there is none;
    - the two must agree, and at a finite boundary b, |f(b) − L| = ε exactly, or b is where f
      stops being defined, or a break of sign, floor or ceil;
    - a capped δ is probed at exact points closing in on the end of the window;
    - where solveset cannot solve the inequality (sin(1/x)), "none" needs a certificate from the
      one-sided limit (_no_delta_by_limit), and "capped" needs the range of f inside the band.
    Anything else raises OracleRefused: the case is not written.
    """
    a, L, eps, reach = (exact(v) for v in (a, L, eps, reach))
    window = sp.Interval.open(a, a + reach) if side > 0 else sp.Interval.open(a - reach, a)
    bad, good, undefined = _bad_and_good(expr, var, window, L, eps, split)
    where = f"|{expr} − {L}| < {eps} on {window}"
    if not (_resolved(bad) and _resolved(good)):
        why = _no_delta_by_limit(expr, var, a, L, eps, side)
        if why:
            return {"none": True, "delta": 0, "capped": False, "sympy": why}
        rng = sp.calculus.util.function_range(expr, var, window)
        if isinstance(rng, sp.Interval) and rng.is_subset(sp.Interval.open(L - eps, L + eps)):
            return _capped(expr, var, a, L, eps, side, reach, where, f"the range {rng} lies inside the band")
        raise OracleRefused(f"SymPy cannot solve {where}")

    # Route A: the complement.
    if bad is sp.S.EmptySet:
        a_delta = reach
    else:
        a_delta = sp.simplify(bad.inf - a) if side > 0 else sp.simplify(a - bad.sup)
    # Route B: the interval of G that starts at a.
    parts = good.args if isinstance(good, sp.Union) else [good]
    touching = [i for i in parts if isinstance(i, sp.Interval) and (i.inf if side > 0 else i.sup) == a]
    b_delta = 0 if not touching else sp.simplify(touching[0].sup - a if side > 0 else a - touching[0].inf)
    if sp.simplify(a_delta - b_delta) != 0:
        raise OracleRefused(f"the two routes disagree for {where}: δ = {a_delta} from the complement, {b_delta} from the inequality; it does not check out")
    if a_delta == 0:
        assert _no_delta_by_limit(expr, var, a, L, eps, side) or not split, f"{where}: no δ, but the limit is within ε"
        return {"none": True, "delta": 0, "capped": False, "sympy": "the failures accumulate at a (inf of the complement is a)"}
    delta = sp.nsimplify(a_delta)
    if delta == reach:
        return _capped(expr, var, a, L, eps, side, reach, where, None)
    # The boundary: |f(b) − L| = ε, or f stops being defined there, or it is a break.
    b = a + side * delta
    v = _at(expr, var, b)
    edge = v is not None and sp.simplify(sp.Abs(v - L) - eps) == 0
    stops = v is None or b in undefined.boundary
    breaks = split and b in _breaks(expr, var, window)
    if not (edge or stops or breaks):
        raise OracleRefused(f"SymPy's δ = {delta} for {where} does not check out: f is within ε of L at its end {b}")
    _probe(expr, var, a, L, eps, side, delta, where)
    return {"none": False, "delta": float(sp.N(delta, 30)), "capped": False, "sympy": str(delta)}


def _probe(expr, var, a, L, eps, side, delta, where):
    """A sanity check of an interval that SymPy says is good: f inside the band at exact points
    spread over it, and closing in on its far end."""
    ks = [sp.Rational(k, 17) for k in range(1, 17)] + [1 - sp.Rational(1, 10**k) for k in range(1, 16)]
    for k in ks:
        x = a + side * delta * k
        if _fails_at(expr, var, x, L, eps):
            raise OracleRefused(f"SymPy's δ = {delta} for {where} does not check out: the band condition fails at x = {x}")


def _capped(expr, var, a, L, eps, side, reach, where, why):
    """A capped δ (the reach), probed near the cap (review F5: SymPy once missed a failing tail
    there)."""
    _probe(expr, var, a, L, eps, side, reach, where)
    return {"none": False, "delta": float(sp.N(reach, 30)), "capped": True, "sympy": why or str(sp.nsimplify(reach))}


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
