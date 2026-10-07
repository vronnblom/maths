"""parse_answer(): an exercise's Answer, as printed on the page, to a SymPy object (docs/plan/06 §6.1).

The answer LaTeX subset is docs/plan/04 §4.3. SymPy's antlr backend reads it, but it is far too
forgiving to be trusted on its own (checked with SymPy 1.14 and antlr4-python3-runtime 4.11):

- it returns `\\pi` and `e` as plain symbols, and leaves `\\frac{1}{2}` as an unevaluated
  `Pow(2, -1)`;
- without `strict=True` it drops everything after the first comma, so `-2, 4` reads as `-2`;
- it reads an unknown command as a symbol of that name: `\\approx 0.69` is `approx*0.69`,
  `\\text{True}` is the product of the letters, `\\lvert x \\rvert` is `lvert*rvert*x`;
- a bare `\\log` is the natural logarithm (the notation guide rejects a bare `\\log`).

So parse_answer() works in four steps:

1. normalise: Unicode minus, `\\dfrac`/`\\tfrac` → `\\frac`, the project's macros expanded from
   content/myst.yml (so `\\abs{x}` → `\\left\\lvert x \\right\\rvert`), `\\left`/`\\right` and
   spacing dropped, `\\lvert`/`\\rvert` → `|`, `\\mathrm{e}` → `e`, decimals → exact fractions
   (`0.69` → `\\frac{69}{100}`); then every remaining command must be in the subset;
2. split a top-level comma-separated list ourselves; brackets are intervals only with the `set`
   type, otherwise `(a, b)` is a point (a tuple);
3. parse each element with `parse_latex(…, backend="antlr", strict=True)`;
4. post-process: `pi`/`e`/`E` → `sp.pi`/`sp.E`, `oo`, `.doit()`, every free symbol → the
   canonical mathcheck symbol of that name; a multi-letter name is an unknown command, an error.

Anything that cannot be read raises AnswerParseError, whose message tells the author to use the
subset or mark the answer `manual`. It never guesses.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import sympy as sp
import yaml

REPO = Path(__file__).resolve().parents[2]
MYST_YML = REPO / "content" / "myst.yml"

SUBSET = "docs/plan/04 §4.3"
HOW_TO_FIX = (f"Rewrite the answer in the answer LaTeX subset ({SUBSET}), or mark it "
              f"`:class: dropdown answer manual` if it is not an expression.")

# ── The canonical symbols ────────────────────────────────────────────────────
# Every free symbol in a parsed answer is replaced by the symbol of the same name from here, and
# tests import the same objects (`from mathcheck import x`), so `2x` on the page equals `2*x` in
# a test. All are real; `n` (an index in sequences and series) is an integer.

INTEGER_NAMES = frozenset({"n"})
_SYMBOLS: dict[str, sp.Symbol] = {}


def symbol(name: str) -> sp.Symbol:
    """The canonical symbol called `name`: real, or integer for n."""
    s = _SYMBOLS.get(name)
    if s is None:
        s = sp.Symbol(name, integer=True) if name in INTEGER_NAMES else sp.Symbol(name, real=True)
        _SYMBOLS[name] = s
    return s


GREEK = frozenset({
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta", "vartheta",
    "iota", "kappa", "lambda", "mu", "nu", "xi", "rho", "sigma", "tau", "upsilon", "phi", "varphi",
    "chi", "psi", "omega",
})

# ── Errors ───────────────────────────────────────────────────────────────────


class AnswerParseError(ValueError):
    """An answer outside the subset. The message says what and how to fix it."""

    def __init__(self, latex: str, problem: str):
        super().__init__(f"cannot read the answer {latex!r}: {problem}. {HOW_TO_FIX}")
        self.latex = latex
        self.problem = problem


# ── Answer types (docs/plan/07 §7.3) ─────────────────────────────────────────

TYPES = ("expr", "antiderivative", "set", "bool", "numeric", "manual")
NUMERIC = re.compile(r"^numeric-((?:\d+(?:\.\d*)?|\.\d+)(?:e-?\d+)?)$")


def parse_type(answer_type: str) -> tuple[str, float | None]:
    """'numeric-5e-3' → ('numeric', 0.005); 'set' → ('set', None). Raises ValueError."""
    m = NUMERIC.match(answer_type)
    if m:
        tol = float(m.group(1))
        if not tol > 0:
            raise ValueError(f"answer type {answer_type}: the tolerance must be positive")
        return "numeric", tol
    if answer_type in TYPES and answer_type != "numeric":
        return answer_type, None
    raise ValueError(f"unknown answer type {answer_type!r}: one of expr, antiderivative, set, bool, "
                     f"numeric-<tolerance> (e.g. numeric-5e-3), manual (docs/plan/07 §7.3)")


# ── Step 1: normalise ────────────────────────────────────────────────────────

TOKEN = re.compile(r"\\[A-Za-z]+|\\.|.", re.S)


@lru_cache(maxsize=None)
def project_macros(path: Path = MYST_YML) -> dict[str, tuple[str, int]]:
    """{'\\abs': ('\\left\\lvert #1 \\right\\rvert', 1), …} from project.math in myst.yml."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    math = (data.get("project") or {}).get("math") or {}
    out = {}
    for name, body in math.items():
        nargs = max((int(k) for k in re.findall(r"#([1-9])", body)), default=0)
        out[name] = (body, nargs)
    return out


def _read_argument(s: str, i: int, latex: str, name: str) -> tuple[str, int]:
    """A macro argument at s[i:]: a {…} group (without the braces) or one token."""
    while i < len(s) and s[i] == " ":
        i += 1
    if i >= len(s) or s[i] == "}":
        raise AnswerParseError(latex, f"the macro {name} is missing an argument")
    if s[i] != "{":
        tok = TOKEN.match(s, i).group(0)
        return tok, i + len(tok)
    depth, j = 0, i
    while j < len(s):
        tok = TOKEN.match(s, j).group(0)
        if tok == "{":
            depth += 1
        elif tok == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
        j += len(tok)
    raise AnswerParseError(latex, f"unbalanced braces in the argument of {name}")


def expand_macros(s: str, latex: str, macros: dict[str, tuple[str, int]]) -> str:
    for _ in range(50):  # macros may use macros; 50 rounds is far more than any real nesting
        out, i, changed = [], 0, False
        while i < len(s):
            tok = TOKEN.match(s, i).group(0)
            if tok in macros:
                body, nargs = macros[tok]
                j = i + len(tok)
                args = []
                for _k in range(nargs):
                    arg, j = _read_argument(s, j, latex, tok)
                    args.append(arg)
                for k, arg in enumerate(args, start=1):
                    body = body.replace(f"#{k}", arg)
                out.append(" " + body + " ")
                i, changed = j, True
                continue
            out.append(tok)
            i += len(tok)
        s = "".join(out)
        if not changed:
            return s
    raise AnswerParseError(latex, "the project macros expand without end")


# Commands of the subset (after normalisation), and Greek letters as variables.
ALLOWED_COMMANDS = frozenset({
    "frac", "sqrt", "pi", "infty", "sin", "cos", "tan", "arcsin", "arccos", "arctan", "ln", "log",
    "cdot", "times",
}) | GREEK
DROPPED = {"\\left", "\\right", "\\displaystyle", "\\textstyle", "\\,", "\\;", "\\:", "\\!", "\\ ", "~"}
BARS = {"\\lvert", "\\rvert", "\\vert", "\\mid"}
DECIMAL = re.compile(r"(?<![\d.])(\d*)\.(\d+)(?![\d.])")


def normalise(latex: str, macros: dict | None = None) -> str:
    """Step 1. Raises AnswerParseError on a command outside the subset."""
    s = latex.replace("\u2212", "-").replace("\u00a0", " ").strip()
    s = expand_macros(s, latex, project_macros() if macros is None else macros)
    s = re.sub(r"\\[dt]frac(?![A-Za-z])", r"\\frac", s)
    s = re.sub(r"\\mathrm\s*\{\s*e\s*\}", "e", s)
    out = []
    for tok in TOKEN.findall(s):
        if tok in DROPPED:
            out.append(" ")
        elif tok in BARS:
            out.append("|")
        else:
            out.append(tok)
    s = "".join(out)
    s = DECIMAL.sub(lambda m: f"\\frac{{{int((m.group(1) or '0') + m.group(2))}}}{{{10 ** len(m.group(2))}}}", s)
    s = re.sub(r"\s+", " ", s).strip()
    for tok in TOKEN.findall(s):
        if tok.startswith("\\") and len(tok) > 1:
            name = tok[1:]
            if name not in ALLOWED_COMMANDS:
                raise AnswerParseError(latex, f"{tok} is not in the answer subset")
    if re.search(r"\\log(?!\s*_)", s):
        raise AnswerParseError(latex, "a bare \\log is ambiguous: write \\ln, or \\log_{b} with its base")
    if not s:
        raise AnswerParseError(latex, "the answer is empty")
    return s


# ── Step 2: split lists and brackets ─────────────────────────────────────────

OPEN, CLOSE = "([{", ")]}"


def _depth_changes(s: str):
    """(index, depth after it) for every character, counting (, [ and { against ), ] and }."""
    depth = 0
    for i, ch in enumerate(s):
        if ch in OPEN and not (i > 0 and s[i - 1] == "\\"):
            depth += 1
        elif ch in CLOSE and not (i > 0 and s[i - 1] == "\\"):
            depth -= 1
        yield i, ch, depth


def split_top_level(s: str, latex: str) -> list[str]:
    """Split at commas outside every bracket and outside |…|."""
    parts, start, bars = [], 0, 0
    depth = 0
    for i, ch, depth in _depth_changes(s):
        if depth < 0:
            raise AnswerParseError(latex, "unbalanced brackets")
        if ch == "|" and depth == 0:
            bars ^= 1
        if ch == "," and depth == 0 and not bars:
            parts.append(s[start:i].strip())
            start = i + 1
    if depth != 0:
        raise AnswerParseError(latex, "unbalanced brackets")
    parts.append(s[start:].strip())
    if any(not p for p in parts):
        raise AnswerParseError(latex, "an empty item in a comma-separated list")
    return parts


def _bracket_group(s: str):
    """(opener, inner, closer) if s is one bracketed group with (or [ … ) or ], else None."""
    if len(s) < 2 or s[0] not in "([" or s[-1] not in ")]":
        return None
    for i, _ch, depth in _depth_changes(s):
        if depth == 0 and i < len(s) - 1:
            return None
    return s[0], s[1:-1], s[-1]


# ── Steps 3 and 4: parse and post-process ────────────────────────────────────


def _parse_one(s: str, latex: str, answer_type: str):
    from sympy.parsing.latex import parse_latex  # imports antlr; slow, so only when needed

    try:
        expr = parse_latex(s, backend="antlr", strict=True)
    except Exception as e:  # LaTeXParsingError, and antlr errors on odd input
        raise AnswerParseError(latex, f"SymPy cannot parse {s!r} ({type(e).__name__}: {str(e).splitlines()[0]})") from None
    return _post_process(expr, latex, answer_type)


def _post_process(expr, latex: str, answer_type: str):
    if not isinstance(expr, sp.Expr):
        raise AnswerParseError(latex, f"{expr} is not a value (an equation or inequality?); an answer is "
                                      f"the value itself, e.g. 2 rather than x = 2")
    constants = {}
    for sym in expr.free_symbols:
        if sym.name == "pi":
            constants[sym] = sp.pi
        elif sym.name in ("e", "E"):
            constants[sym] = sp.E
        elif sym.name in ("oo", "infty"):
            constants[sym] = sp.oo
    expr = expr.xreplace(constants).doit()
    mapping = {}
    for sym in expr.free_symbols:
        name = sym.name
        base = re.sub(r"_\{?[A-Za-z0-9]+\}?$", "", name)
        if not (len(base) == 1 and base.isalpha() or base in GREEK):
            raise AnswerParseError(latex, f"{name!r} reads as a variable with a multi-letter name; "
                                          f"it is probably a command or text outside the subset")
        if name == "C" and answer_type != "antiderivative":
            raise AnswerParseError(latex, "a constant C: an antiderivative answer needs the type `antiderivative`")
        mapping[sym] = symbol(name)
    expr = expr.xreplace(mapping)
    # A substitution can make a function evaluable (cos(pi) → -1); doit() once more is cheap.
    return expr.doit()


def _strip_constant(s: str, latex: str) -> str:
    m = re.search(r"\+\s*C\s*$", s)
    if not m:
        raise AnswerParseError(latex, "an antiderivative answer ends with + C")
    rest = s[: m.start()].strip()
    if not rest:
        raise AnswerParseError(latex, "the antiderivative is empty")
    return rest


def parse_answer(latex: str, answer_type: str = "expr", macros: dict | None = None):
    """The SymPy value of one answer span.

    - `expr` (default): an expression; a comma-separated list → a tuple; `(a, b)` → a point (a
      tuple); `[a, b]` is an error (brackets are intervals: use the `set` type).
    - `antiderivative`: `F(x) + C` → F(x) (compare with equal_up_to_constant).
    - `set`: `(a, b)`, `[a, b)`, … → sp.Interval, a number → a one-point set, a list → their union.
    - `bool`: True/False (case-insensitive) → sp.true/sp.false.
    - `numeric-<tol>`: a number (exact: `0.69` → 69/100).
    - `manual`: not machine-readable; raises AnswerParseError.
    """
    kind, _tol = parse_type(answer_type)
    if kind == "manual":
        raise AnswerParseError(latex, "the answer is marked manual, so it has no machine-readable value")
    if kind == "bool":
        word = latex.strip().rstrip(".").strip()
        if word.lower() in ("true", "false"):
            return sp.true if word.lower() == "true" else sp.false
        raise AnswerParseError(latex, "a bool answer is the word True or False")
    s = normalise(latex, macros)
    if kind == "antiderivative":
        s = _strip_constant(s, latex)
    items = split_top_level(s, latex)
    values = [_parse_item(item, latex, kind, answer_type) for item in items]
    if kind == "set":
        return sp.Union(*values) if len(values) > 1 else values[0]
    if kind == "numeric":
        for v in values:
            if not (isinstance(v, sp.Expr) and v.is_number):
                raise AnswerParseError(latex, f"a numeric answer must be a number, not {v}")
    return values[0] if len(values) == 1 else tuple(values)


def _parse_item(item: str, latex: str, kind: str, answer_type: str):
    group = _bracket_group(item)
    if group is not None:
        opener, inner, closer = group
        parts = split_top_level(inner, latex) if inner.strip() else []
        if len(parts) >= 2:
            if kind == "set":
                if len(parts) != 2:
                    raise AnswerParseError(latex, f"an interval has two endpoints: {item}")
                lo, hi = (_parse_one(p, latex, answer_type) for p in parts)
                interval = sp.Interval(lo, hi, left_open=opener == "(", right_open=closer == ")")
                if interval.is_empty is not False:
                    raise AnswerParseError(latex, f"the interval {item} is empty or its endpoints are not real numbers")
                return interval
            if opener == "[" or closer == "]":
                raise AnswerParseError(latex, f"{item}: square brackets are intervals, which need the answer type `set`")
            return tuple(_parse_one(p, latex, answer_type) for p in parts)
    value = _parse_one(item, latex, answer_type)
    if kind == "set":
        return sp.FiniteSet(value)
    return value
