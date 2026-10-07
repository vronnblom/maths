"""Extract every exercise's Answer from mystmd's AST into verify/_answers.json (docs/plan/06 §6.1).

    extract_answers.py content/_build/site/content -o verify/_answers.json [--root content]

`npm run verify` runs it after `npm run ast` (`myst build --site`). For each page in the toc it
reads `<AST dir>/<slug>.json`, checks that the AST was built from the source as it is now (mystmd
stores the source's sha256), and walks the exercises in document order:

    exercise{label} > admonition{class contains "answer"} > paragraph > (inlineMath | text | span)

From each Answer it collects one LaTeX string per math span, in document order (so the parts
of `(a) … (b) …` keep their order):
- `inlineMath` and `math` nodes: their value;
- `text` nodes whose whole value is a number: mystmd turns number-only math (`$0.69$`, `$-3$`)
  into plain text;
- `span` nodes that mystmd builds from simple powers and indices (`$2^{10}$` → text "2" +
  superscript "10"), rebuilt as `2^{10}`.

The answer type and `manual` come from the admonition's class (docs/plan/07 §7.3). A `bool`
answer is the word True or False in plain text. Errors (an exercise with no Answer or two, an
unknown answer class, an Answer with no math, math that KaTeX rejected, a stale AST) are printed
as `file:line: error: message`; then nothing is written and an existing output file is
**deleted**, so the tests can never read answers from an earlier build.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from project import DEFAULT_ROOT, REPO, Project, Reporter, add_root_argument, display_path

FORMAT = 1  # verify/conftest.py checks it
NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$")
TYPE_CLASSES = re.compile(r"^(expr|antiderivative|set|bool|manual|numeric-(?:\d+(?:\.\d*)?|\.\d+)(?:e-?\d+)?)$")
LAYOUT_CLASSES = {"dropdown", "answer"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_of(node) -> int:
    """The source line of a node, or of its first descendant that has one (mystmd gives an
    admonition no position of its own)."""
    for n in walk(node):
        line = ((n.get("position") or {}).get("start") or {}).get("line")
        if line:
            return line
    return 1


def walk(node):
    yield node
    for c in node.get("children") or []:
        yield from walk(c)


class Extractor:
    def __init__(self, rep: Reporter):
        self.rep = rep

    def span_latex(self, node, path, line) -> str | None:
        """`2^{10}` from span > (text "2", superscript > text "10")."""
        out = []
        for c in node.get("children") or []:
            t = c.get("type")
            if t == "text":
                out.append(c.get("value", ""))
            elif t in ("superscript", "subscript"):
                inner = self.span_latex(c, path, line)
                if inner is None:
                    return None
                out.append(("^{" if t == "superscript" else "_{") + inner + "}")
            else:
                self.rep.error(path, line, f"an Answer contains a {t} inside a span, which extract_answers.py "
                                           f"does not know how to read back as LaTeX")
                return None
        return "".join(out)

    def answer_parts(self, adm, path) -> list[str]:
        parts = []

        def visit(node):
            t = node.get("type")
            if t == "admonitionTitle":
                return
            if t in ("inlineMath", "math"):
                if node.get("error"):
                    self.rep.error(path, line_of(node), f"KaTeX cannot render the answer ${node.get('value')}$: "
                                                        f"{node.get('message', 'error')}")
                parts.append(node.get("value", ""))
                return
            if t == "text":
                if NUMBER.match(node.get("value", "")):
                    parts.append(node["value"])
                return
            if t == "span" and any(c.get("type") in ("superscript", "subscript") for c in node.get("children") or []):
                s = self.span_latex(node, path, line_of(adm))
                if s is not None:
                    parts.append(s)
                return
            for c in node.get("children") or []:
                visit(c)

        for c in adm.get("children") or []:
            visit(c)
        return parts

    @staticmethod
    def plain_text(adm) -> str:
        return "".join(n.get("value", "") for c in adm.get("children") or [] if c.get("type") != "admonitionTitle"
                       for n in walk(c) if n.get("type") == "text").strip()

    def page(self, rel: str, path: Path, mdast: dict, answers: dict, seen: dict) -> None:
        for ex in walk(mdast):
            if ex.get("type") != "exercise":
                continue
            label = ex.get("label") or ex.get("identifier")
            line = line_of(ex)
            if not label:
                self.rep.error(path, line, "an exercise without a label (docs/plan/07 §7.3)")
                continue
            adms = [c for c in ex.get("children") or []
                    if c.get("type") == "admonition" and "answer" in (c.get("class") or "").split()]
            if len(adms) != 1:
                self.rep.error(path, line, f"exercise {label} needs exactly one Answer admonition "
                                           f"(:class: dropdown answer), found {len(adms)}")
                continue
            adm = adms[0]
            classes = (adm.get("class") or "").split()
            types = [c for c in classes if c not in LAYOUT_CLASSES]
            bad = [c for c in types if not TYPE_CLASSES.match(c)]
            if bad:
                self.rep.error(path, line_of(adm), f"the Answer of {label} has the class {bad[0]!r}, which is not an "
                                                   f"answer type: expr, antiderivative, set, bool, numeric-<tolerance>, "
                                                   f"manual (docs/plan/07 §7.3)")
                continue
            if len(types) > 1:
                self.rep.error(path, line_of(adm), f"the Answer of {label} has two answer types: {' '.join(types)}")
                continue
            kind = types[0] if types else "expr"
            manual = kind == "manual"
            if kind == "bool":
                text = self.plain_text(adm)
                parts = [text] if text else []
            else:
                parts = self.answer_parts(adm, path)
            if not parts and not manual:
                self.rep.error(path, line_of(adm), f"the Answer of {label} contains no math: write it as $…$ in the "
                                                   f"answer subset (docs/plan/04 §4.3), or mark it manual")
                continue
            if label in seen:
                self.rep.error(path, line, f"exercise {label} also appears on {seen[label]}")
                continue
            seen[label] = rel
            answers[label] = {"latex": parts, "manual": manual, "page": rel, "type": kind, "line": line_of(adm)}


def extract(ast_dir: Path, root: Path, rep: Reporter, repo: Path = REPO) -> dict:
    """`repo` is the repository the output belongs to (the parent of its verify/ folder);
    verify/conftest.py resolves the recorded root against it."""
    project = Project(root)
    try:
        root_rel = project.root.relative_to(repo.resolve()).as_posix()
    except ValueError:
        root_rel = project.root.as_posix()
    data = {"format": FORMAT, "root": root_rel, "pages": {}, "answers": {}}
    ex = Extractor(rep)
    seen: dict[str, str] = {}
    # mystmd names each file after the page's slug; its `location` is the source path.
    by_location: dict[str, tuple[Path, dict]] = {}
    for f in sorted(ast_dir.glob("*.json")):
        ast = json.loads(f.read_text(encoding="utf-8"))
        by_location[(ast.get("location") or "").lstrip("/")] = (f, ast)
    for page in project.pages:
        if page.rel not in by_location:
            rep.error(page.path, 1, f"no AST for this page in {display_path(ast_dir)}: run npm run ast first")
            continue
        f, ast = by_location[page.rel]
        digest = sha256(page.path)
        if ast.get("sha256") != digest:
            rep.error(page.path, 1, f"the AST in {display_path(f)} was built from an older version of this page: "
                                    f"rebuild it (npm run ast, or npm run verify)")
            continue
        data["pages"][page.rel] = digest
        ex.page(page.rel, page.path, ast.get("mdast") or {}, data["answers"], seen)
    # Pages that changed after the build are already errors; also record the hashes of every
    # page in the toc, so verify/conftest.py notices any later edit.
    return data


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ast_dir", nargs="?", default=str(DEFAULT_ROOT / "_build" / "site" / "content"),
                    help="mystmd's page JSON (default: content/_build/site/content)")
    ap.add_argument("-o", "--output", default=str(REPO / "verify" / "_answers.json"), help="default: verify/_answers.json")
    add_root_argument(ap)
    args = ap.parse_args(argv)
    out = Path(args.output)
    if out.exists():
        out.unlink()  # never leave answers from an earlier build behind, even if this run fails
    rep = Reporter()
    data = extract(Path(args.ast_dir), Path(args.root), rep, repo=out.resolve().parent.parent)
    if rep.errors:
        print(f"extract_answers.py: {len(rep.errors)} error(s); {display_path(out)} not written", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    manual = sum(1 for a in data["answers"].values() if a["manual"])
    print(f"extract_answers.py: {len(data['answers'])} answers ({manual} manual) from {len(data['pages'])} pages "
          f"→ {display_path(out)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
