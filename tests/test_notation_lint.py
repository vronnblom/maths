"""The notation lint: what it must catch, and the code, math and prose it must leave alone."""

from __future__ import annotations

import textwrap

import pytest

import myst_source as ms
import notation_lint
from project import REPO, Project, Reporter, read_page

SUBJECT = """\
---
title: Calculus
label: calc-subject
description: x
maths:
  kind: subject
  subject: calc
  status: draft
---

{body}
"""
META = SUBJECT.replace("label: calc-subject", "label: site-x").replace("  kind: subject\n  subject: calc\n", "  kind: meta\n")


def lint(tmp_path, body, template=SUBJECT):
    (tmp_path / "index.md").write_text(template.format(body=body), encoding="utf-8")
    page = read_page(tmp_path, "index.md")
    rep = Reporter(quiet=True)
    notation_lint.lint_page(page, ms.parse(page.text), rep)
    return [d.message for d in rep.errors]


@pytest.mark.parametrize(
    "body, rule",
    [
        ("$\\log x$", "log"),
        ("$$\n\\log(x)\n$$", "log"),
        ("$\\cos^{-1} x$", "sin-inverse"),
        ("$\\tan^-1 x$", "sin-inverse"),
        ("$\\int f(x)\\,dx$", "raw-d"),
        ("$\\int_D f \\, dA$", "raw-d"),
        ("$\\int_0^1 x \\, \\mathrm{d}x$", "raw-d"),
        (":::{math}\n\\int_0^1 t \\, dt\n:::", "raw-d"),
        ("$x \\in ]a, b]$", "reversed-interval"),
        ("$e = \\mathrm{e}^1$", "mathrm-e"),
        ("An angle of 30°.", "degrees"),
        ("$\\pi = 180^{\\circ}$", "degrees"),
        ("It is Obviously true.", "filler"),
        (":::{proof:theorem} Clearly true\n:label: thm-calc-a-b\nx\n:::", "filler"),
    ],
)
def test_hits(tmp_path, body, rule):
    errors = lint(tmp_path, body)
    assert len(errors) == 1 and errors[0].startswith(f"[{rule}]"), errors


@pytest.mark.parametrize(
    "body",
    [
        "$\\ln x$, $\\log_{10} x$, $\\log_2 x$, $\\log_b x$",
        "`\\log x` in code, and in a block:\n\n```latex\n\\log x \\sin^{-1} ]a, b[ \\mathrm{e}\n```",
        "$\\arcsin x$, $\\sin^2 x$, $f^{-1}(x)$",
        "$\\int_0^1 x^2 \\dd x$, $\\int_c^d x \\dd x$, $\\dv{y}{x}$, $\\frac{d}{dx}$ outside an integral",
        "$[a, b] \\cup [c, d]$, $(0, 1] \\times [0, 1]$, $[a, b)$",
        "$e^x$, $\\exp(x)$, $\\operatorname{e}$ is not checked",
        'We never write "clearly", nor ‘obviously’ or “trivially”: quoted mentions are not uses.',
        "% a comment: clearly $\\log x$",
        "% notation-lint: off (shows what not to write)\n\n$\\log x$, $]a, b[$, clearly\n\n% notation-lint: on",
    ],
)
def test_no_false_positives(tmp_path, body):
    assert lint(tmp_path, body) == []


def test_emphasised_filler_is_still_filler(tmp_path):
    # Only a quoted mention is exempt; *obviously* in italics is a use.
    assert lint(tmp_path, "This is *obviously* true.")[0].startswith("[filler]")


def test_degrees_only_on_calculus_pages(tmp_path):
    assert lint(tmp_path, "An angle of 30°.", template=META) == []


def test_unclosed_off_region_is_an_error(tmp_path):
    errors = lint(tmp_path, "% notation-lint: off\n\n$\\log x$\n")
    # An unclosed region is an error, and it switches nothing off.
    assert errors[0] == "notation-lint: off is never switched back on"
    assert errors[1].startswith("[log]")


@pytest.mark.parametrize("path", sorted((REPO / "templates").glob("*.md")) + [REPO / "content" / "about" / "notation.md"])
def test_templates_and_notation_page_are_clean(path, tmp_path):
    """The templates and the notation guide (which shows what not to write) pass the lint."""
    page = read_page(path.parent, path.name)
    rep = Reporter(quiet=True)
    if path.name == "blocks.md":  # snippets inside ```markdown fences: lint each as a page
        import re
        for _f, snippet in re.findall(r"^(`{3,})markdown\n(.*?)^\1\s*$", page.text, re.M | re.S):
            (tmp_path / "s.md").write_text(SUBJECT.format(body=snippet), encoding="utf-8")
            p = read_page(tmp_path, "s.md")
            notation_lint.lint_page(p, ms.parse(p.text), rep)
    else:
        notation_lint.lint_page(page, ms.parse(page.text), rep)
    assert not rep.diagnostics, "\n".join(map(str, rep.diagnostics))
