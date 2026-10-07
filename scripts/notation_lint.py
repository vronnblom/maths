"""The mechanical part of the notation and style rules (docs/plan/04 §4.2, §4.4; 06 §6.3–6.4).

Math rules look only inside math ($…$, $$…$$, {math}); the prose rule only outside math, code
and comments. A page that has to show what we do *not* write (the notation guide, the
inverse-trigonometric page mentioning sin^{-1}) wraps that part in MyST comments:

    % notation-lint: off (why)
    …
    % notation-lint: on
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import myst_source as ms
from project import Page, Reporter


@dataclass(frozen=True)
class Rule:
    id: str
    pattern: re.Pattern
    message: str
    where: str = "math"  # math | prose | both
    calc_only: bool = False
    integrals_only: bool = False


RULES = [
    Rule("log", re.compile(r"\\log(?![A-Za-z])(?!\s*_)"),
         r"bare \log: write \ln for the natural logarithm, or give the base, \log_{10} x (docs/plan/04 §4.2)"),
    Rule("sin-inverse", re.compile(r"\\(?:sin|cos|tan|sec|csc|cot)\s*\^\s*(?:\{\s*-\s*1\s*\}|-\s*1)"),
         r"\sin^{-1} and friends: write \arcsin, \arccos, \arctan (docs/plan/04 §4.2)"),
    Rule("raw-d", re.compile(r"(?<![\\A-Za-z^_])d\s*[A-Za-z](?![A-Za-z])|\\mathrm\s*\{\s*d\s*\}"),
         r"raw differential in an integral: write \dd x (docs/plan/04 §4.1)", integrals_only=True),
    Rule("reversed-interval", re.compile(r"(?:^|(?<=[\s=(,{]))\][^\[\]\s,][^\[\],]*,[^\[\],]*[^\[\]\s,]\s*[\[\]]"),
         r"reversed-bracket interval ]a, b[: write (a, b) (docs/plan/04 §4.2)"),
    Rule("mathrm-e", re.compile(r"\\mathrm\s*\{\s*e\s*\}"),
         r"\mathrm{e}: write an italic e (docs/plan/04 §4.2)"),
    Rule("degrees", re.compile(r"\^\s*\{?\s*\\circ(?![A-Za-z])|\\degree(?![A-Za-z])|°"),
         "degrees in a calculus page: angles are in radians (docs/plan/04 §4.2)", where="both", calc_only=True),
    Rule("filler", re.compile(r"(?<![\"“'‘\w])(?:clearly|obviously|trivially)(?![\"”'’\w])", re.IGNORECASE),
         'no "clearly", "obviously" or "trivially": give the short reason instead (docs/plan/04 §4.4)', where="prose"),
]

OFF = re.compile(r"^notation-lint:\s*off\b")
ON = re.compile(r"^notation-lint:\s*on\b")


def _disabled_ranges(doc: ms.Document, page: Page, rep: Reporter) -> list[tuple[int, int]]:
    ranges, start = [], None
    for c in doc.comments:
        if OFF.match(c.text):
            if start is not None:
                rep.error(page.path, c.line, "notation-lint: off while already off")
            start = c.line
        elif ON.match(c.text):
            if start is None:
                rep.error(page.path, c.line, "notation-lint: on without a matching off")
            else:
                ranges.append((start, c.line))
                start = None
    if start is not None:
        rep.error(page.path, start, "notation-lint: off is never switched back on")
    return ranges


def _hits(rule: Rule, text: str, first_line: int):
    for m in rule.pattern.finditer(text):
        yield first_line + text.count("\n", 0, m.start()), m.group(0)


def lint_page(page: Page, doc: ms.Document, rep: Reporter) -> None:
    disabled = _disabled_ranges(doc, page, rep)

    def report(rule, line, found):
        if any(a <= line <= b for a, b in disabled):
            return
        rep.error(page.path, line, f"[{rule.id}] `{found.strip()}`: {rule.message}")

    calc = page.subject == "calc"
    maths = list(doc.display_math())
    prose = []
    for _node, inl in doc.inline_runs():
        maths += inl.math
        prose += inl.prose
    for rule in RULES:
        if rule.calc_only and not calc:
            continue
        if rule.where in ("math", "both"):
            for line, tex in maths:
                if rule.integrals_only and "\\int" not in tex:
                    continue
                for ln, found in _hits(rule, tex, line):
                    report(rule, ln, found)
        if rule.where in ("prose", "both"):
            for line, text in prose:
                for ln, found in _hits(rule, text, line):
                    report(rule, ln, found)


def check(project, rep: Reporter, docs: dict | None = None) -> None:
    for page in project.pages:
        doc = (docs or {}).get(page.rel)
        if doc is None:
            try:
                doc = ms.parse(page.text)
            except ms.ParseError as e:
                rep.error(page.path, e.line, e.message)
                continue
        lint_page(page, doc, rep)
