"""plugins/topic-header.mjs through mystmd: a project assembled from templates/topic.md and
templates/chapter-index.md, built through the gate (scripts/myst_gate.sh), with assertions on
the resolved AST (docs/plan/03 §3.6).

The `checks` job has no theme, so the project names a stub site template (a `template.yml`
only): `myst build --site` then writes every page's AST to _build/site/content/ in about a
second, without a download, and resolves the cross-references. plugins/_tests/ unit-tests the
same logic without mystmd.

The project (the real curriculum.yml, so calc-absolute-value-inequalities is planned but
unwritten):
    index.md                                   a home page (the first toc entry is the site root)
    calculus/preliminaries/functions.md        calc-functions, written (a prerequisite of calc-limit)
    calculus/limits/index.md                   templates/chapter-index.md, verbatim
    calculus/limits/limit-of-a-function.md     templates/topic.md, verbatim
    calculus/limits/limit-laws.md              calc-limit-laws, written (it builds on calc-limit)

`uv run python tests/test_plugin_build.py <dir>` writes the project to <dir>, to build it with
the real theme and look at it.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from project import REPO  # noqa: E402

MYST_BIN = REPO / "node_modules" / ".bin"


def topic_page(label, title, prerequisites, difficulty=2, minutes=30, status="draft"):
    return f"""---
title: {title}
label: {label}
description: A minimal page for the plugin build test.
maths:
  kind: topic
  subject: calc
  status: {status}
  level: core
  difficulty: {difficulty}
  est_minutes: {minutes}
  prerequisites: [{', '.join(prerequisites)}]
  objectives:
    - State what this page is about, with $x^2$ in it.
    - Use it.
---

:::{{topic-header}}
:::

## Where this leads

:::{{where-this-leads}}
:::
"""


def make_project(dest: Path, site_template: str | None = None) -> Path:
    """Write the project to dest; returns its content/ folder. `site_template` replaces the
    stub (e.g. the pinned book-theme URL, for an HTML build)."""
    content = dest / "content"
    (dest / "site-template").mkdir(parents=True, exist_ok=True)
    (dest / "site-template" / "template.yml").write_text("jtex: v1\ntitle: AST only (tests/test_plugin_build.py)\n", encoding="utf-8")
    shutil.copytree(REPO / "widgets", dest / "widgets", ignore=shutil.ignore_patterns("_tests", "README.md"), dirs_exist_ok=True)
    pages = {
        "index.md": "---\ntitle: Home\nlabel: site-home\nmaths:\n  kind: meta\n  status: draft\n---\n\nThe plugin fixture.\n",
        "calculus/preliminaries/functions.md": topic_page("calc-functions", "Functions and Their Graphs", ["calc-real-numbers"]),
        "calculus/limits/index.md": (REPO / "templates" / "chapter-index.md").read_text(encoding="utf-8"),
        "calculus/limits/limit-of-a-function.md": (REPO / "templates" / "topic.md").read_text(encoding="utf-8"),
        "calculus/limits/limit-laws.md": topic_page("calc-limit-laws", "Limit Laws", ["calc-limit"], difficulty=3, minutes=35, status="reviewed"),
    }
    for rel, text in pages.items():
        (content / rel).parent.mkdir(parents=True, exist_ok=True)
        (content / rel).write_text(text, encoding="utf-8")
    shutil.copy(REPO / "content" / "calculus" / "curriculum.yml", content / "calculus" / "curriculum.yml")
    template = site_template or "../site-template"
    style = ""
    if site_template:  # the real theme: also the site's CSS (the stub template has no `style` option)
        shutil.copytree(REPO / "content" / "_static", content / "_static", dirs_exist_ok=True)
        style = "\n    style: _static/custom.css"
    (content / "myst.yml").write_text(f"""version: 1
project:
  id: 7d0b5c52-3e43-4c49-9a39-5d1e1c1b0a11
  title: Plugin fixture
  github: https://github.com/vronnblom/maths
  plugins:
    - {(REPO / 'plugins' / 'topic-header.mjs').as_posix()}
  static_files:
    - ../widgets/_lib
  math:
    '\\abs': '\\left\\lvert #1 \\right\\rvert'
    '\\eps': '\\varepsilon'
  toc:
    - file: index.md                                 # mystmd: the first toc item is a file, the site root
    - title: Preliminaries
      children:
        - file: calculus/preliminaries/functions.md
    - title: Limits
      file: calculus/limits/index.md
      children:
        - file: calculus/limits/limit-of-a-function.md
        - file: calculus/limits/limit-laws.md
site:
  template: {template}
  options:
    folders: true{style}
""", encoding="utf-8")
    return content


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    if not (MYST_BIN / "myst").exists():
        pytest.fail("mystmd is not installed: run npm ci (the checks job does)")
    content = make_project(tmp_path_factory.mktemp("plugin"))
    env = {**os.environ, "PATH": f"{MYST_BIN}{os.pathsep}{os.environ.get('PATH', '')}"}
    r = subprocess.run(["bash", str(REPO / "scripts" / "myst_gate.sh"), "--site"], cwd=content, env=env,
                       capture_output=True, text=True, timeout=180)
    pages = {}
    for f in (content / "_build" / "site" / "content").glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        pages[data["frontmatter"].get("label")] = data["mdast"]
    return r, pages


def walk(node):
    yield node
    for c in node.get("children") or []:
        yield from walk(c)


def text(node) -> str:
    return "".join(n.get("value", "") for n in walk(node) if n["type"] in ("text", "inlineMath"))


def with_class(tree, cls):
    return [n for n in walk(tree) if cls in (n.get("class") or "").split()]


def links(tree):
    return [(n["url"], text(n)) for n in walk(tree) if n["type"] == "link" and n.get("internal")]


def test_the_build_passes_the_gate(built):
    r, pages = built
    assert r.returncode == 0, r.stdout + r.stderr
    assert {"calc-functions", "calc-limits-chapter", "calc-limit", "calc-limit-laws"} <= set(pages)


def test_topic_header(built):
    _, pages = built
    tree = pages["calc-limit"]
    banner, = with_class(tree, "maths-draft-banner")
    assert banner["type"] == "admonition" and text(banner).startswith("Draft — may contain errors")
    header, = with_class(tree, "maths-topic-header")
    # A written prerequisite: a crossReference, which MyST resolved to the page's title and URL.
    assert links(header) == [("/calculus/preliminaries/functions", "Functions and Their Graphs")]
    # A planned one without a page: its curriculum title, "coming soon".
    assert "Absolute Value and Inequalities (coming soon)" in text(header)
    assert "About 40 minutes · Difficulty ●●○○○ (2 of 5)" in text(header)
    badge, = with_class(header, "maths-badge")
    assert badge["class"] == "maths-badge maths-status-draft" and text(badge) == "Draft"
    objectives = next(n for n in walk(header) if n["type"] == "list")
    assert len(objectives["children"]) == 4
    assert text(objectives["children"][1]).startswith("State the precise (ε–δ) definition")


def test_objectives_render_their_math(built):
    _, pages = built
    header, = with_class(pages["calc-functions"], "maths-topic-header")
    assert any(n["type"] == "inlineMath" and n["value"] == "x^2" for n in walk(header))


def test_reviewed_page_has_no_banner(built):
    _, pages = built
    assert not with_class(pages["calc-limit-laws"], "maths-draft-banner")
    badge, = with_class(pages["calc-limit-laws"], "maths-badge")
    assert badge["class"] == "maths-badge maths-status-reviewed"


def test_where_this_leads(built):
    _, pages = built
    tree = pages["calc-limit"]
    after = text(tree).split("Where this leads", 1)[1]
    # Written dependants are links; planned ones (from the real curriculum) are "coming soon".
    assert ("/calculus/limits/limit-laws", "Limit Laws") in links(tree)
    assert "One-Sided Limits (coming soon)" in after
    assert "Limit Laws" in after.split("One-Sided Limits")[0], "written dependants come first"
    # And the reverse edge from the other side: functions.md is built on by calc-limit.
    assert ("/calculus/limits/limit-of-a-function", "The Limit of a Function") in links(pages["calc-functions"])


def test_chapter_topics_table(built):
    _, pages = built
    tree = pages["calc-limits-chapter"]
    table, = [n for n in walk(tree) if n["type"] == "table"]
    rows = [[text(c) for c in row["children"]] for row in table["children"]]
    assert rows[0] == ["Topic", "Time", "Difficulty", "Status"]
    assert rows[1] == ["The Limit of a Function", "40 min", "●●○○○ (2 of 5)", "Draft"]
    assert rows[2] == ["One-Sided Limits", "–", "–", "coming soon"]
    assert rows[3] == ["Limit Laws", "35 min", "●●●○○ (3 of 5)", "Reviewed"]
    assert len(rows) == 1 + 7, "every topic of the Limits chapter in curriculum.yml"
    assert links(table) == [("/calculus/limits/limit-of-a-function", "The Limit of a Function"),
                            ("/calculus/limits/limit-laws", "Limit Laws")]
    # The chapter page's own header: prerequisites, no time or difficulty.
    header, = with_class(tree, "maths-topic-header")
    assert links(header) == [("/calculus/preliminaries/functions", "Functions and Their Graphs")]
    assert "minutes" not in text(header)


def test_the_widgets_reach_the_ast(built):
    _, pages = built
    plot, eps_delta = [n for n in walk(pages["calc-limit"]) if n["type"] == "anywidget"]
    assert plot["esm"].endswith(".mjs") and "function-plot" in plot["esm"]
    assert plot["model"]["hole"] == {"x": 0} and plot["model"]["variable"] == "h"
    assert eps_delta["esm"].endswith(".mjs") and "epsilon-delta" in eps_delta["esm"]
    assert eps_delta["model"]["a"] == 2 and eps_delta["model"]["epsStep"] == 0.05


def test_malformed_front_matter_fails_the_build(tmp_path):
    content = make_project(tmp_path)
    page = content / "calculus" / "limits" / "limit-of-a-function.md"
    page.write_text(page.read_text(encoding="utf-8").replace("difficulty: 2", "difficulty: seven"), encoding="utf-8")
    env = {**os.environ, "PATH": f"{MYST_BIN}{os.pathsep}{os.environ.get('PATH', '')}"}
    r = subprocess.run(["bash", str(REPO / "scripts" / "myst_gate.sh"), "--site"], cwd=content, env=env,
                       capture_output=True, text=True, timeout=180)
    assert r.returncode == 1
    assert "{topic-header}: calculus/limits/limit-of-a-function.md: maths.difficulty must be a whole number from 1 to 5" in r.stdout
    assert "::error::MyST build produced errors or warnings" in r.stdout


if __name__ == "__main__":
    out = make_project(Path(sys.argv[1]), *(sys.argv[2:3]))
    print(f"wrote {out}")
