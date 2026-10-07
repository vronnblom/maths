"""Widgets in every page of the toc (docs/plan/05 §5.8, 06 §6.4).

- every ```{anywidget} is the only content of a {figure} with a `wdg-` label and a non-empty
  caption (the caption is the widget's text description), and a `wdg-` figure holds a widget;
- the {anywidget} path points to widgets/<name>.mjs, and that widget exists in the catalogue
  (widgets/*.mjs of this repository) with a schema, schema/widgets/<name>.schema.json;
- the JSON body is valid JSON and valid against that schema, and passes the rules a schema
  cannot express (function-plot: ranges increasing, values inside ranges, and the names and
  functions in `f`, mirroring widgets/_lib/plot.mjs and expression.mjs; epsilon-delta: ranges
  increasing, a strictly inside xRange, L inside yRange, eps inside epsRange, delta and epsStep
  small enough, and `f`, mirroring widgets/_lib/epsdelta.mjs);
- every id in `maths.widgets` is a widget of the catalogue.

The catalogue and the schemas are always this repository's, also for a fixture project under
tests/fixtures/ (its pages point into the fixture, but the widgets they name must be real).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema

import myst_source as ms
from project import REPO, Page, Project, Reporter, add_root_argument

WIDGETS = REPO / "widgets"
SCHEMAS = REPO / "schema" / "widgets"


def catalogue() -> set[str]:
    return {p.stem for p in WIDGETS.glob("*.mjs")}


def load_schema(name: str) -> dict | None:
    path = SCHEMAS / f"{name}.schema.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


# ── Expressions (the rules of widgets/_lib/expression.mjs) ───────────────────

TOKEN = re.compile(r"\s*(?:(\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|([-+*/^()]))")


class ExpressionError(ValueError):
    pass


def tokenize(src: str) -> list[tuple[str, str, int]]:
    """[(type, value, position)] with type num | name | op."""
    if not isinstance(src, str) or not src.strip():
        raise ExpressionError("the expression is empty")
    tokens, pos = [], 0
    while pos < len(src) and src[pos:].strip():
        m = TOKEN.match(src, pos)
        if not m:
            at = pos + len(src[pos:]) - len(src[pos:].lstrip())
            raise ExpressionError(f"unexpected character {json.dumps(src[at])} at position {at + 1}")
        kind = "num" if m.group(1) is not None else "name" if m.group(2) is not None else "op"
        value = m.group(1) or m.group(2) or m.group(3)
        tokens.append((kind, value, m.end() - len(value)))
        pos = m.end()
    return tokens


def check_expression(src: str, names: list[str], functions: list[str], constants: list[str]) -> list[tuple[str, str, int]]:
    """Raise ExpressionError if `src` breaks the expression rules; return its tokens."""
    tokens = tokenize(src)
    depth = 0

    def operand(t):
        return t is not None and (t[0] in ("num", "name") or t[1] == "(")

    for i, (kind, value, pos) in enumerate(tokens):
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        where = f"at position {pos + 1}"
        if kind == "name":
            if value in functions:
                if nxt is None or nxt[1] != "(":
                    raise ExpressionError(f"{value} needs parentheses: {value}(…) ({where})")
                continue
            if value == "log":
                raise ExpressionError(f"write ln for the natural logarithm, not log ({where})")
            if value not in names and value not in constants:
                raise ExpressionError(f"unknown name {value} ({where}): use the variable, a parameter, pi, e, or one of {', '.join(functions)}")
            if nxt is not None and nxt[1] == "(":
                raise ExpressionError(f"{value} is not a function: write {value}*(…) ({where})")
            if operand(nxt):
                raise ExpressionError(f"missing * after {value} ({where})")
        elif kind == "num":
            if operand(nxt):
                raise ExpressionError(f"missing * after {value}: write {value}*{nxt[1]} ({where})")
        else:
            if value == "(":
                depth += 1
            elif value == ")":
                depth -= 1
                if depth < 0:
                    raise ExpressionError(f"unmatched ) ({where})")
                if operand(nxt):
                    raise ExpressionError(f"missing * after ) ({where})")
    if depth > 0:
        raise ExpressionError("unmatched (")
    return tokens


def function_plot_problems(config: dict, schema: dict) -> list[str]:
    """The rules of configProblems() in widgets/_lib/plot.mjs, plus the expression rules."""
    problems = []
    variable = config.get("variable", "x")
    for key in ("xRange", "yRange"):
        r = config.get(key)
        if isinstance(r, list) and len(r) == 2 and not r[0] < r[1]:
            problems.append(f"{key}: the first number must be smaller than the second")
    x0, x1 = config.get("xRange", [float("-inf"), float("inf")])

    def inside(x):
        return x0 <= x <= x1

    params = config.get("parameters") or {}
    for name, p in params.items():
        if name == variable:
            problems.append(f"parameters.{name}: a parameter cannot have the name of the variable")
        if not p["min"] < p["max"]:
            problems.append(f"parameters.{name}: min must be smaller than max")
        elif not p["min"] <= p["value"] <= p["max"]:
            problems.append(f"parameters.{name}: value must lie between min and max")
    for x in (config.get("table") or {}).get("points", []):
        if not inside(x):
            problems.append(f"table.points: {_js_number(x)} lies outside xRange")
    for key in ("hole", "trace"):
        if key in config and not inside(config[key]["x"]):
            problems.append(f"{key}.x: {_js_number(config[key]['x'])} lies outside xRange")
    try:
        check_expression(config["f"], [variable, *params], schema["$defs"]["functions"]["enum"],
                         schema["$defs"]["constants"]["enum"])
    except ExpressionError as e:
        problems.append(f"f: {e}")
    return problems


def epsilon_delta_problems(config: dict, schema: dict) -> list[str]:
    """The rules of configProblems() in widgets/_lib/epsdelta.mjs, plus the expression rules."""
    problems = []

    def increasing(key):
        r = config.get(key)
        ok = not (isinstance(r, list) and len(r) == 2) or r[0] < r[1]
        if not ok:
            problems.append(f"{key}: the first number must be smaller than the second")
        return ok and isinstance(r, list)

    x_ok, y_ok, eps_ok = increasing("xRange"), increasing("yRange"), increasing("epsRange")
    a = config["a"]
    if x_ok:
        x0, x1 = config["xRange"]
        if not x0 < a < x1:
            problems.append("a: must lie strictly inside xRange, so that both sides of a show")
        if "delta" in config and not config["delta"] <= min(a - x0, x1 - a):
            problems.append("delta: must be at most the distance from a to the nearer end of xRange")
    if y_ok and not config["yRange"][0] <= config["L"] <= config["yRange"][1]:
        problems.append("L: must lie inside yRange")
    if eps_ok:
        e0, e1 = config["epsRange"]
        if not e0 <= config["eps"] <= e1:
            problems.append("eps: must lie inside epsRange")
        if "epsStep" in config and not config["epsStep"] <= e1 - e0:
            problems.append("epsStep: must be at most the width of epsRange")
    try:
        check_expression(config["f"], ["x"], schema["$defs"]["functions"]["enum"], schema["$defs"]["constants"]["enum"])
    except ExpressionError as e:
        problems.append(f"f: {e}")
    return problems


def _js_number(x) -> str:
    """A number as JavaScript prints it (so that both implementations give the same message)."""
    return str(int(x)) if float(x).is_integer() else repr(float(x))


SEMANTIC = {"function-plot": function_plot_problems, "epsilon-delta": epsilon_delta_problems}


# ── The checks ───────────────────────────────────────────────────────────────


def _json_line(d: ms.Directive, path) -> int:
    """The line of a key path (e.g. ["trace", "x"]) in the JSON body: each key is looked for after
    the line of the one before it. Falls back to the body's first line."""
    keys = [k for k in path if isinstance(k, str)]
    found = d.raw[0][0] if d.raw else d.line
    start = 0
    for key in keys:
        for i in range(start, len(d.raw)):
            if f'"{key}"' in d.raw[i][1]:
                found, start = d.raw[i][0], i
                break
        else:
            break
    return found


def _caption_text(nodes) -> str:
    return " ".join(t for n in nodes if isinstance(n, ms.Paragraph) for _, t in n.lines).strip()


def check_page(page: Page, doc: ms.Document, project: Project, rep: Reporter, known: set[str]) -> None:
    for d in doc.directives():
        if d.name == "figure":
            widgets = [c for c in d.children if isinstance(c, ms.Directive) and c.name == "anywidget"]
            if d.label and d.label.startswith("wdg-") and not widgets:
                rep.error(page.path, d.option_line("label"), f"figure {d.label}: a wdg- label is for a figure that holds a widget ({{anywidget}})")
            continue
        if d.name != "anywidget":
            continue
        fig = d.parent
        if fig is None or fig.name != "figure":
            rep.error(page.path, d.line, "{anywidget} must be the only content of a {figure} labelled wdg-…, whose caption describes the widget (docs/plan/05 §5.8)")
        else:
            others = [c for c in fig.children if not isinstance(c, ms.Comment) and c is not d]
            first = next(c for c in fig.children if not isinstance(c, ms.Comment))
            if first is not d or any(not isinstance(c, ms.Paragraph) for c in others):
                rep.error(page.path, fig.line, "a widget figure holds only the {anywidget}, then its caption (docs/plan/05 §5.8)")
            if not (fig.label or "").startswith("wdg-"):
                rep.error(page.path, fig.option_line("label"), f"a widget figure needs a wdg- label, not {fig.label or 'none'} (docs/plan/05 §5.8)")
            if not _caption_text(others):
                rep.error(page.path, fig.line, f"widget figure {fig.label or '(unlabelled)'}: the caption (the widget's text description) is missing; it is all that readers without the widget see (docs/plan/05 §5.8)")
        _check_widget(page, d, project, rep, known)
    widgets = page.maths.get("widgets")
    if isinstance(widgets, list):
        for k, w in enumerate(widgets):
            if isinstance(w, str) and w not in known:
                rep.error(page.path, page.line("maths", "widgets", k), f"maths.widgets: {w} is not a widget: there is no widgets/{w}.mjs (see widgets/README.md)")


def _check_widget(page: Page, d: ms.Directive, project: Project, rep: Reporter, known: set[str]) -> None:
    arg = d.arg.strip()
    name = Path(arg).stem if arg.endswith(".mjs") else None
    target = (page.path.parent / arg).resolve() if arg else None
    expected = (project.repo / "widgets" / f"{name}.mjs").resolve() if name else None
    if not name or target != expected:
        depth = "../" * (len(page.rel.split("/")))
        rep.error(page.path, d.line, f"{{anywidget}} {arg or '(no path)'}: point it at widgets/<name>.mjs; from this page, {depth}widgets/<name>.mjs")
        return
    if name not in known:
        rep.error(page.path, d.line, f"{{anywidget}}: widget {name} does not exist (no widgets/{name}.mjs; the catalogue is widgets/README.md)")
        return
    schema = load_schema(name)
    if schema is None:
        rep.error(page.path, d.line, f"widget {name} has no schema/widgets/{name}.schema.json")
        return
    body = "\n".join(t for _, t in d.raw)
    try:
        config = json.loads(body)
    except json.JSONDecodeError as e:
        line = d.raw[e.lineno - 1][0] if d.raw and e.lineno <= len(d.raw) else d.line
        rep.error(page.path, line, f"widget {name}: the body is not valid JSON: {e.msg}")
        return
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(config), key=lambda e: list(map(str, e.absolute_path)))
    for e in errors:
        where = ".".join(str(p) for p in e.absolute_path) or "config"
        path = list(e.absolute_path)
        if e.validator == "additionalProperties" and isinstance(e.instance, dict):  # point at the stray key
            path += sorted(set(e.instance) - set(e.schema.get("properties", {})))[:1]
        rep.error(page.path, _json_line(d, path), f"widget {name}: {where}: {e.message} (schema/widgets/{name}.schema.json)")
    if errors:
        return
    semantic = SEMANTIC.get(name)
    for problem in semantic(config, schema) if semantic else []:
        key = problem.split(":")[0].split(".")[0]
        rep.error(page.path, _json_line(d, [key]), f"widget {name}: {problem}")


def check(project: Project, rep: Reporter, docs: dict | None = None) -> None:
    known = catalogue()
    for page in project.pages:
        doc = (docs or {}).get(page.rel)
        if doc is None:
            try:
                doc = ms.parse(page.text)
            except ms.ParseError:
                continue  # check_labels reports it
        check_page(page, doc, project, rep, known)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    args = ap.parse_args(argv)
    rep = Reporter()
    check(Project(args.root), rep)
    print(f"check_widgets.py: {len(rep.errors)} error(s)", file=sys.stderr)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
