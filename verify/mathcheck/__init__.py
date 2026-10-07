"""mathcheck: what verification tests import (docs/plan/06 §6.1).

    from mathcheck import covers, answer, equal, x

- `@covers("eg-…", "exr-…")` declares the labelled blocks a test verifies. A declaration counts
  for nothing on its own: verify/conftest.py counts a label as covered only if a test declaring
  it **passed**, and, for an `exr-` label, called `answer(label)`; for an `eg-` label, made at
  least one mathcheck assertion.
- `answer(label)` returns the exercise's Answer as printed on the page, parsed by
  `latex.parse_answer` with the answer type from the page. Each call is recorded for the test
  that made it.
- The helpers (`equal`, `equal_up_to_constant`, `equal_on_domain`, `numeric_spot_check`,
  `limit_is`, `series_converges_to`, `solves_ode`) return True or False, and raise when SymPy
  cannot decide (an undecidable comparison fails). Each True result counts as one mathcheck
  assertion for the running test; write `assert equal(...)`.
- The canonical symbols (`x`, `t`, `n`, …) are the objects `answer()` puts into parsed answers:
  all real, `n` an integer.
"""

from __future__ import annotations

import functools
import re

import mpmath
import sympy as sp

from . import equality as _eq
from .equality import Undecidable
from .latex import AnswerParseError, parse_answer, parse_type, symbol

__all__ = [
    "covers", "answer", "answer_type", "equal", "equal_up_to_constant", "equal_on_domain",
    "numeric_spot_check", "limit_is", "series_converges_to", "solves_ode", "symbol",
    "Undecidable", "AnswerParseError", "ManualAnswer",
    "a", "b", "c", "h", "k", "r", "s", "t", "u", "v", "w", "x", "y", "z", "n", "theta",
]

a, b, c, h, k, r, s, t, u, v, w, x, y, z, n, theta = (
    symbol(name) for name in ("a", "b", "c", "h", "k", "r", "s", "t", "u", "v", "w", "x", "y", "z", "n", "theta")
)

# ── Per-test state, read by the coverage plugin in verify/conftest.py ────────

LABEL = re.compile(r"^(def|thm|lem|cor|prop|ax|prf|eg|exr|sol|rem|eq|fig|tbl|sec|wdg)-[a-z0-9]+(-[a-z0-9]+)+$")


class _State:
    def __init__(self):
        self.test: str | None = None
        self.assertions = 0
        self.answers: set[str] = set()
        self.data: dict | None = None  # verify/_answers.json["answers"], installed by conftest.py

    def begin(self, test: str):
        self.test, self.assertions, self.answers = test, 0, set()

    def end(self) -> tuple[int, set[str]]:
        result = (self.assertions, set(self.answers))
        self.test, self.assertions, self.answers = None, 0, set()
        return result


_state = _State()


def _install_answers(answers: dict) -> None:
    """Called by verify/conftest.py with verify/_answers.json["answers"]."""
    _state.data = answers


def covers(*labels: str):
    """Declare the labelled blocks (`eg-…`, `exr-…`) that the decorated test verifies."""
    if not labels:
        raise ValueError("@covers needs at least one label")
    for label in labels:
        if not isinstance(label, str) or not LABEL.match(label):
            raise ValueError(f"@covers({label!r}): not a block label (docs/plan/02 §2.4)")

    def mark(fn):
        fn.__mathcheck_covers__ = tuple(getattr(fn, "__mathcheck_covers__", ())) + labels
        return fn

    return mark


class ManualAnswer(Exception):
    """answer() on an exercise whose Answer is `manual`: there is nothing machine-readable."""


def _entry(label: str) -> dict:
    if _state.data is None:
        raise RuntimeError("no answers are loaded: run the tests with pytest from the repository "
                           "(verify/conftest.py loads verify/_answers.json; npm run verify writes it)")
    entry = _state.data.get(label)
    if entry is None:
        raise KeyError(f"{label} has no Answer in verify/_answers.json: is the label right, and is the "
                       f"exercise in the toc? (npm run verify rebuilds the file)")
    return entry


def answer_type(label: str) -> str:
    """The answer type of an exercise, as on the page: expr, set, numeric-5e-3, manual, …"""
    return _entry(label)["type"]


def answer(label: str):
    """The Answer of exercise `label` as printed on the page, parsed by SymPy.

    One math span gives one value (an expression, a tuple for a list or point, an Interval for
    the `set` type); a multi-part answer `(a) … (b) …` gives a tuple of the parts in order.
    """
    if _state.test is not None:
        _state.answers.add(label)
    entry = _entry(label)
    if entry.get("manual"):
        raise ManualAnswer(f"{label} has a manual answer (a proof or a sketch), so answer() has nothing to "
                           f"parse. Check its key claims without answer(); a reviewer records the manual check "
                           f"in the page's maths.manual_checked (docs/plan/06 §6.6)")
    values = [parse_answer(s, entry["type"]) for s in entry["latex"]]
    if not values:
        raise AnswerParseError("", f"{label}: the Answer has no math")
    return values[0] if len(values) == 1 else tuple(values)


def _counted(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        if result is True and _state.test is not None:
            _state.assertions += 1
        return result

    return wrapper


equal = _counted(_eq.equal)
equal_up_to_constant = _counted(_eq.equal_up_to_constant)
equal_on_domain = _counted(_eq.equal_on_domain)
numeric_spot_check = _counted(_eq.numeric_spot_check)

# ── Limits, series, ODEs ─────────────────────────────────────────────────────


def _approach_table(expr, var, point, side: str, steps=range(3, 13)):
    """Values of expr at points approaching `point` from `side` ('+' or '-'), with mpmath at
    60 digits (exact powers such as (1 + 10^-12)^(10^12) would never finish)."""
    f = sp.lambdify(var, expr, modules="mpmath")
    values = []
    with mpmath.workdps(60):
        for k_ in steps:
            if point is sp.S.Infinity or point is sp.S.NegativeInfinity:
                p = mpmath.mpf(10) ** k_ * (1 if point is sp.S.Infinity else -1)
            else:
                step = mpmath.mpf(10) ** -k_
                p = mpmath.mpmathify(sp.N(point, 60)) + (step if side == "+" else -step)
            try:
                values.append(mpmath.mpmathify(f(p)))
            except (ZeroDivisionError, ValueError, OverflowError, TypeError):
                values.append(mpmath.nan)
    return values


def _table_agrees(values, value) -> bool:
    finite = [v for v in values if isinstance(v, mpmath.mpf) and mpmath.isfinite(v)]
    if len(finite) < len(values) // 2:
        return False
    if value is sp.S.Infinity or value is sp.S.NegativeInfinity:
        sign = 1 if value is sp.S.Infinity else -1
        seq = [sign * v for v in finite]
        return all(q >= p for p, q in zip(seq, seq[1:])) and seq[-1] > seq[0] and seq[-1] > 0
    with mpmath.workdps(60):
        target = mpmath.mpmathify(sp.N(value, 60))
        errs = [abs(v - target) for v in finite]
        return errs[-1] <= errs[0] and errs[-1] < mpmath.mpf("0.1") * (1 + abs(target))


def _limit_is(expr, var, point, value, dir="+-") -> bool:
    """lim_{var → point} expr = value. dir is '+-' (two-sided, the default), '+' or '-'; point
    and value may be ±oo. sp.limit decides, and a table of values approaching the point (60
    digits, steps 10^-3 … 10^-12, or ±10^3 … ±10^12) must agree with it, or the check fails."""
    expr, point, value = sp.sympify(expr), sp.sympify(point), sp.sympify(value)
    if point is sp.S.Infinity or point is sp.S.NegativeInfinity:
        dirs = ["-" if point is sp.S.Infinity else "+"]
        computed = sp.limit(expr, var, point)
    else:
        dirs = ["+", "-"] if dir == "+-" else [dir]
        computed = sp.limit(expr, var, point, dir)
    if isinstance(computed, sp.Limit) or computed.has(sp.AccumBounds):
        raise Undecidable(f"SymPy cannot evaluate the limit of {expr} as {var} → {point} ({computed})")
    if not _eq.equal(computed, value):
        return False
    for side in dirs:
        table = _approach_table(expr, var, point, side)
        if not _table_agrees(table, value):
            shown = ", ".join(mpmath.nstr(v, 8) for v in table)
            raise AssertionError(f"SymPy says the limit of {expr} as {var} → {point}{side if len(dirs) > 1 else ''} is "
                                 f"{value}, but the values approaching it do not settle there: {shown}")
    return True


def _series_converges_to(term, var, value, start=1, tol=1e-6) -> bool:
    """sum_{var=start}^oo term = value. SymPy's summation if it finds a closed form; partial sums
    (N = 10^2 … 10^4, 50 digits) as a cross-check, or as the check itself, with the tolerance."""
    term, value = sp.sympify(term), sp.sympify(value)
    total = sp.summation(term, (var, start, sp.oo))
    f = sp.lambdify(var, term, modules="mpmath")
    with mpmath.workdps(50):
        target = mpmath.mpmathify(sp.N(value, 50))
        partial, errors, k_ = mpmath.mpf(0), [], int(start)
        for N in (100, 1000, 10000):
            while k_ <= N:
                partial += f(k_)
                k_ += 1
            errors.append(abs(partial - target))
    settles = errors[-1] <= errors[0] and errors[-1] < 1e-2 * (1 + abs(target))
    if isinstance(total, sp.Sum) or total.has(sp.Sum):
        if not settles or errors[-1] > tol:
            raise Undecidable(f"SymPy finds no closed form for the sum of {term}, and the partial sums are "
                              f"{float(errors[-1]):.3g} away from {value} at N = 10^4 (tolerance {tol})")
        return True
    if not _eq.equal(total, value):
        return False
    if not settles:
        raise AssertionError(f"SymPy sums {term} to {value}, but the partial sums do not approach it")
    return True


def _solves_ode(solution, ode, func=None) -> bool:
    """`solution` (an Eq(f(x), …) or the right-hand side, with `func`) solves `ode`."""
    ok, residual = sp.checkodesol(ode, solution, func=func) if func is not None else sp.checkodesol(ode, solution)
    if ok:
        return True
    return _eq.equal(residual, 0) if isinstance(residual, sp.Expr) else False


limit_is = _counted(_limit_is)
series_converges_to = _counted(_series_converges_to)
solves_ode = _counted(_solves_ode)

