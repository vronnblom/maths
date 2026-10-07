"""Regenerate tests/fixtures/ast/topic.json: mystmd's AST of templates/topic.md.

tests/test_parser.py compares the labels and references that scripts/myst_source.py finds in
templates/topic.md with this AST, so parser drift (or a template change that the parser reads
differently from mystmd) shows up as a failing test. Run this after changing templates/topic.md
or upgrading mystmd, and commit the result:

    npm ci && bash scripts/fetch_theme.sh && uv run python tests/make_ast_fixture.py

It builds a one-page scratch project with `myst build --site`, using the theme that
fetch_theme.sh put in content/_build/templates (the site build needs a template, but nothing is
downloaded). The unknown {topic-header} directives and missing widget modules are reported by
mystmd as errors but don't stop it from writing the AST.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "tests" / "fixtures" / "ast" / "topic.json"


def strip(node):
    """Drop rendered HTML and keys that churn between builds; keep types, labels and positions."""
    if isinstance(node, dict):
        return {k: strip(v) for k, v in node.items() if k not in ("html", "key")}
    if isinstance(node, list):
        return [strip(v) for v in node]
    return node


def main() -> int:
    myst_yml = (REPO / "content" / "myst.yml").read_text(encoding="utf-8")
    math = re.search(r"^  math:\n(?:    .*\n)+", myst_yml, re.M).group(0)
    themes = sorted((REPO / "content" / "_build" / "templates" / "site").glob("*/template.yml"))
    if not themes:
        print("no theme in content/_build/templates: run bash scripts/fetch_theme.sh first", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        page = proj / "calculus" / "limits" / "limit-of-a-function.md"
        page.parent.mkdir(parents=True)
        page.write_text((REPO / "templates" / "topic.md").read_text(encoding="utf-8"), encoding="utf-8")
        (proj / "myst.yml").write_text(
            "version: 1\nproject:\n  title: AST fixture\n" + math
            + "  numbering: { title: false, headings: false }\n"
            + "  toc:\n    - file: calculus/limits/limit-of-a-function.md\n"
            + f"site:\n  template: {themes[0].parent}\n",
            encoding="utf-8",
        )
        myst = REPO / "node_modules" / ".bin" / "myst"
        subprocess.run([str(myst), "build", "--site", "--ci"], cwd=proj, check=True)
        data = json.loads((proj / "_build" / "site" / "content" / "index.json").read_text(encoding="utf-8"))
    out = {"mystmd": json.loads((REPO / "node_modules" / "mystmd" / "package.json").read_text())["version"],
           "frontmatter": {"label": data["frontmatter"].get("label")},
           "mdast": strip(data["mdast"])}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
