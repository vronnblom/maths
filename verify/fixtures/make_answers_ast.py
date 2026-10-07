"""Regenerate verify/fixtures/answers-ast.json: mystmd's AST of three exercises whose Answers
take the three shapes that scripts/extract_answers.py reads (docs/plan/06 §6.1):

- a symbolic answer, `$\\frac{1}{2}$` → an `inlineMath` node;
- a numeric answer, `$0.69$` → a plain `text` node (mystmd turns number-only math into text);
- a power of numbers, `$2^{10}$` → a `span` of text "2" and a `superscript` "10";

plus a multi-part answer that mixes them, a `set` answer and a `manual` one.

verify/test_mathcheck.py runs the extractor over this AST and checks the node shapes, so a
mystmd upgrade that changes any of them fails one clear test. Run it after upgrading mystmd
(a test fails until you do) and commit the result:

    npm ci && uv run python verify/fixtures/make_answers_ast.py

It builds a one-page scratch project with `myst build --site` and a stub site template (a
`template.yml` only), as tests/test_plugin_build.py does: no theme, no network.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "answers-ast.json"

PAGE = """\
---
title: Answer shapes
---

::::{exercise} A symbolic answer
:label: exr-calc-shapes-symbolic
:class: tier-a

Compute something.

:::{admonition} Answer
:class: dropdown answer
$\\frac{1}{2}$
:::
::::

::::{exercise} A numeric answer
:label: exr-calc-shapes-numeric
:class: tier-a

Estimate something to two decimal places.

:::{admonition} Answer
:class: dropdown answer numeric-5e-3
$0.69$
:::
::::

::::{exercise} A power of numbers
:label: exr-calc-shapes-power
:class: tier-a

How many subsets does a set of ten elements have?

:::{admonition} Answer
:class: dropdown answer
$2^{10}$
:::
::::

::::{exercise} Three parts
:label: exr-calc-shapes-parts
:class: tier-b

Three things.

:::{admonition} Answer
:class: dropdown answer
(a) $-3$ (b) $10^{-3}$ (c) $\\sqrt{2}, \\pi$
:::
::::

::::{exercise} A solution set
:label: exr-calc-shapes-set
:class: tier-a

Solve an inequality.

:::{admonition} Answer
:class: dropdown answer set
$[0, 1)$
:::
::::

::::{exercise} A proof
:label: exr-calc-shapes-manual
:class: tier-c

Prove something.

:::{admonition} Answer
:class: dropdown answer manual
$\\delta = \\eps / 3$ works.
:::
::::
"""


def strip(node):
    """Drop rendered HTML and keys that churn between builds."""
    if isinstance(node, dict):
        return {k: strip(v) for k, v in node.items() if k not in ("html", "key")}
    if isinstance(node, list):
        return [strip(v) for v in node]
    return node


def main() -> int:
    myst = REPO / "node_modules" / ".bin" / "myst"
    if not myst.exists():
        print("mystmd is not installed: run npm ci", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        proj = Path(tmp)
        (proj / "stub").mkdir()
        (proj / "stub" / "template.yml").write_text("jtex: v1\ntitle: AST only\n", encoding="utf-8")
        (proj / "index.md").write_text(PAGE, encoding="utf-8")
        (proj / "myst.yml").write_text(
            "version: 1\nproject:\n  title: Answer shapes\n  math:\n    '\\eps': '\\varepsilon'\n"
            "  toc:\n    - file: index.md\nsite:\n  template: stub\n", encoding="utf-8")
        subprocess.run([str(myst), "build", "--site", "--ci"], cwd=proj, check=True, capture_output=True)
        data = json.loads((proj / "_build" / "site" / "content" / "index.json").read_text(encoding="utf-8"))
    out = {"mystmd": json.loads((REPO / "node_modules" / "mystmd" / "package.json").read_text())["version"],
           "location": data["location"], "page": PAGE, "mdast": strip(data["mdast"])}
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
