"""scripts/myst_source.py against mystmd's own AST, and its loud failures on unknown syntax."""

from __future__ import annotations

import json
import re

import pytest

import myst_source as ms
from project import REPO

AST = REPO / "tests" / "fixtures" / "ast" / "topic.json"
TOPIC = REPO / "templates" / "topic.md"


def ast_labels_and_refs():
    data = json.loads(AST.read_text(encoding="utf-8"))
    labels, refs = set(), set()

    def walk(n):
        if isinstance(n, dict):
            t = n.get("type")
            if t == "crossReference":
                pos = n.get("position")
                refs.add((n["identifier"], pos["start"]["line"] if pos else None))
            elif n.get("label") and t != "captionNumber" and not n.get("implicit"):
                labels.add(n["label"])
            for c in n.get("children", []):
                walk(c)

    walk(data["mdast"])
    return data, labels, refs


def test_labels_match_the_mystmd_ast():
    """Regenerate the AST with tests/make_ast_fixture.py after changing templates/topic.md."""
    data, ast_labels, ast_refs = ast_labels_and_refs()
    doc = ms.parse(TOPIC.read_text(encoding="utf-8"))
    ours = {s.label for s in ms.label_sites(doc)}
    assert ours == ast_labels
    assert data["frontmatter"]["label"] == "calc-limit"
    # References written as [text](#label) carry a position; solution → exercise links don't.
    ours_refs = {(label, line) for _n, inl in doc.inline_runs() for line, label, _t in inl.refs}
    assert ours_refs == {r for r in ast_refs if r[1] is not None}
    solutions = {d.arg for d in doc.directives() if d.name == "solution"}
    assert solutions == {label for label, line in ast_refs if line is None}


def test_ast_fixture_matches_the_pinned_mystmd():
    pinned = json.loads((REPO / "package.json").read_text())["dependencies"]["mystmd"]
    assert json.loads(AST.read_text(encoding="utf-8"))["mystmd"] == pinned, "regenerate with tests/make_ast_fixture.py"


def test_kinds_of_the_template_blocks():
    doc = ms.parse(TOPIC.read_text(encoding="utf-8"))
    kinds = {s.label: s.kinds for s in ms.label_sites(doc)}
    assert kinds["thm-calc-limit-unique"] == ("thm",)
    assert kinds["prf-calc-limit-unique"] == ("prf",)
    assert kinds["wdg-calc-limit-eps-delta"] == ("fig", "wdg")
    assert kinds["sol-calc-limit-table-estimate"] == ("sol",)


def snippets(path):
    """The ```markdown blocks of templates/blocks.md (snippets, not a page)."""
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^(`{3,})markdown\n(.*?)^\1\s*$", text, re.M | re.S)


@pytest.mark.parametrize("snippet", [s for _f, s in snippets(REPO / "templates" / "blocks.md")])
def test_every_block_snippet_parses(snippet):
    doc = ms.parse(snippet)
    for _n, inl in doc.inline_runs():
        assert not inl.problems


def test_blocks_md_has_snippets():
    assert len(snippets(REPO / "templates" / "blocks.md")) >= 15


@pytest.mark.parametrize(
    "text, message",
    [
        (":::{nosuch} x\n:::\n", "unknown directive {nosuch}"),
        ("::::{exercise}\n:label: exr-calc-a-b\n::::{admonition} Hint\nx\n::::\n::::\n", "the outer directive needs more colons"),
        (":::{proof:theorem} T\n---\nlabel: thm-calc-a-b\n---\nx\n:::\n", "YAML option block"),
        (":::{note}\nnever closed\n", "is never closed"),
        ("(sec-calc-a-b)=\nA paragraph.\n", "target must come directly before a heading"),
        ("```python\nx = 1\n", "unclosed code fence"),
        ("$$\nx^2\n", "unclosed $$ display"),
        (":::\n", "stray colon fence"),
    ],
)
def test_unknown_syntax_fails_loudly(text, message):
    with pytest.raises(ms.ParseError) as e:
        ms.parse(text)
    assert message in e.value.message


@pytest.mark.parametrize(
    "text, message",
    [
        ("See {ref}`thm-calc-squeeze`.", "{ref} role: write cross-references as [text](#label)"),
        ("See {numref}`thm-calc-squeeze`.", "{numref} role"),
        ("See [the page](limit-laws.md).", "link to a label instead"),
    ],
)
def test_other_reference_syntax_is_reported(text, message):
    doc = ms.parse(text + "\n")
    problems = [p for _n, inl in doc.inline_runs() for p in inl.problems]
    assert problems and message in problems[0][1]


def test_inline_scanning():
    doc = ms.parse(
        "A [named link with $x^2$](#thm-calc-a-b), `code [](#not-a-ref)`, "
        "$[a, b]$ and [](#def-calc-c-d).\n% a comment with [](#calc-not-a-ref)\n"
    )
    refs = [label for _n, inl in doc.inline_runs() for _l, label, _t in inl.refs]
    assert refs == ["thm-calc-a-b", "def-calc-c-d"]
    maths = [m for _n, inl in doc.inline_runs() for _l, m in inl.math]
    assert maths == ["x^2", "[a, b]"]


def test_display_math_and_equation_labels():
    doc = ms.parse("Text\n$$\nf(x) \\approx f(a)\n$$ (eq-calc-a-b)\n\n$$x$$\n")
    sites = ms.label_sites(doc)
    assert [(s.label, s.kinds) for s in sites] == [("eq-calc-a-b", ("eq",))]
    assert [t for _l, t in doc.display_math()] == ["\nf(x) \\approx f(a)", "x"]


def test_proof_adjacency_skips_comments_only():
    doc = ms.parse(":::{proof:theorem} T\n:label: thm-calc-a-b\nx\n:::\n\n% a comment\n\n:::{proof:proof}\n:enumerated: false\ny\n:::\n")
    proof = [d for d in doc.directives() if d.name == "proof:proof"][0]
    assert ms.previous_sibling(proof, doc).name == "proof:theorem"
    doc = ms.parse(":::{proof:theorem} T\n:label: thm-calc-a-b\nx\n:::\n\nProse.\n\n:::{proof:proof}\ny\n:::\n")
    proof = [d for d in doc.directives() if d.name == "proof:proof"][0]
    assert isinstance(ms.previous_sibling(proof, doc), ms.Paragraph)
