"""Each checker fails on its fixture with the intended message, and nothing else fails there;
every checker passes on the clean fixture (templates/topic.md, verbatim) and on the real tree.

A fixture is a tiny repository: tests/fixtures/<name>/{content/myst.yml, content/…, labels.lock}.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import check_all
import check_frontmatter
import check_labels
import check_toc
import check_widgets
import graph
import notation_lint
from project import REPO, Project, Reporter

FIXTURES = REPO / "tests" / "fixtures"

CHECKERS = {
    "check_toc": check_toc.check,
    "check_frontmatter": check_frontmatter.check,
    "check_labels": lambda p, r: check_labels.check(p, r, forward_refs=True),
    "graph": graph.check,
    "notation_lint": notation_lint.check,
    "check_widgets": check_widgets.check,
}

# fixture → (checker, file the error is in, line, a substring of the message)
DEFECTS = {
    "bad-label": ("check_labels", "limit-of-a-function.md", 21, "label 'def-calc-Limit' may use only lowercase letters"),
    "duplicate-label": ("check_labels", "limit-laws.md", 21, "duplicate label def-calc-limit: already used at"),
    "label-missing-from-lock": ("check_labels", "limit-of-a-function.md", 21, "label def-calc-limit is not in labels.lock"),
    "removed-label-without-tombstone": ("check_labels", "labels.lock", 4, "label thm-calc-limit-old (on calculus/limits/limit-of-a-function.md) is no longer in the content"),
    "kind-prefix-mismatch": ("check_labels", "limit-of-a-function.md", 26, "label thm-calc-limit-unique on {proof:lemma}: the kind prefix should be lem-"),
    "exercise-without-solution": ("check_labels", "limit-of-a-function.md", 27, "exercise exr-calc-limit-first needs exactly one {solution} exr-calc-limit-first, found 0"),
    "exercise-without-answer": ("check_labels", "limit-of-a-function.md", 27, "exercise exr-calc-limit-first needs exactly one Answer admonition"),
    "orphan-proof": ("check_labels", "limit-of-a-function.md", 34, "orphan proof"),
    "forward-reference-outside-closure": ("check_labels", "limit-of-a-function.md", 27, "cites thm-calc-limit-laws on calculus/limits/limit-laws.md, which is not in the prerequisite closure of calc-limit"),
    "forward-citation-in-proof": ("check_labels", "limit-of-a-function.md", 50, "the proof of thm-calc-limit-unique cites lem-calc-limit-local, which is not stated before thm-calc-limit-unique"),
    "proof-cites-later-theorem": ("check_labels", "limit-of-a-function.md", 50, "the proof of thm-calc-limit-unique cites thm-calc-limit-local, which is not stated before thm-calc-limit-unique"),
    "prerequisite-cycle": ("graph", "curriculum.yml", 31, "prerequisite cycle: calc-limit → calc-functions → calc-limit"),
    "unknown-prerequisite": ("graph", "curriculum.yml", 21, "unknown prerequisite calc-no-such-topic"),
    "reviewed-with-draft-prerequisite": ("check_frontmatter", "limit-of-a-function.md", 12, "status reviewed needs every prerequisite at least reviewed: calc-functions is draft"),
    "schema-violation": ("check_frontmatter", "limit-of-a-function.md", 10, "maths.difficulty: 7 is greater than the maximum of 5"),
    "toc-mismatch": ("check_toc", "orphan.md", 1, "about/orphan.md is not in the toc of myst.yml"),
    "lint-bare-log": ("notation_lint", "index.md", 13, "[log] `\\log`: bare \\log"),
    "lint-sin-inverse": ("notation_lint", "index.md", 13, "[sin-inverse] `\\sin^{-1}`"),
    "lint-raw-dx": ("notation_lint", "index.md", 13, "[raw-d] `dx`: raw differential in an integral"),
    "lint-reversed-interval": ("notation_lint", "index.md", 13, "[reversed-interval] `]0, 1[`"),
    "lint-mathrm-e": ("notation_lint", "index.md", 13, "[mathrm-e] `\\mathrm{e}`"),
    "lint-degrees": ("notation_lint", "index.md", 13, "[degrees] `^\\circ`: degrees in a calculus page"),
    "lint-filler": ("notation_lint", "index.md", 13, "[filler] `clearly`"),
    "widget-schema-violation": ("check_widgets", "limit-of-a-function.md", 56, "widget function-plot: config: Additional properties are not allowed ('tabel' was unexpected)"),
    "widget-missing-file": ("check_widgets", "limit-of-a-function.md", 50, "{anywidget}: widget no-such-widget does not exist"),
    "widget-figure-without-caption": ("check_widgets", "limit-of-a-function.md", 47, "widget figure wdg-calc-limit-average-speed: the caption (the widget's text description) is missing"),
    "widget-unknown-id": ("check_widgets", "limit-of-a-function.md", 31, "maths.widgets: no-such-widget is not a widget"),
    "widget-epsilon-delta-out-of-range": ("check_widgets", "limit-of-a-function.md", 103, "widget epsilon-delta: eps: must lie inside epsRange"),
}


def run(name_or_root, checker=None):
    root = name_or_root if isinstance(name_or_root, Path) else FIXTURES / name_or_root / "content"
    rep = Reporter(quiet=True)
    project = Project(root)
    if checker is None:
        check_all.run(project, rep)
    else:
        CHECKERS[checker](project, rep)
    return rep


def fmt(rep):
    return "\n".join(str(d) for d in rep.diagnostics)


def test_every_fixture_is_listed():
    projects = {p.parent.parent.name for p in FIXTURES.glob("*/content/myst.yml")}
    other = {"clean", "us-spelling", "redirects", "redirect-collision", "proof-cites-own-statement"}
    gate = {p for p in projects if p.startswith("gate-")}  # tests/test_build_gate.py
    assert projects == set(DEFECTS) | other | gate


@pytest.mark.parametrize("name", sorted(DEFECTS))
def test_checker_fails_on_its_fixture(name):
    checker, filename, line, message = DEFECTS[name]
    rep = run(name, checker)
    hits = [d for d in rep.errors if message in d.message]
    assert hits, f"{checker} did not report {message!r} on {name}:\n{fmt(rep)}"
    assert (hits[0].path.name, hits[0].line) == (filename, line), fmt(rep)


@pytest.mark.parametrize("name", sorted(DEFECTS))
def test_fixture_has_exactly_one_defect(name):
    rep = run(name)
    assert len(rep.errors) == 1 and not rep.warnings, f"{name} should fail only its own check:\n{fmt(rep)}"
    assert DEFECTS[name][3] in rep.errors[0].message


@pytest.mark.parametrize("checker", sorted(CHECKERS))
@pytest.mark.parametrize("where", ["clean", "real tree"])
def test_checker_passes(checker, where):
    root = FIXTURES / "clean" / "content" if where == "clean" else REPO / "content"
    rep = run(root, checker)
    assert not rep.diagnostics, fmt(rep)


def test_clean_fixture_is_the_topic_template():
    page = FIXTURES / "clean" / "content" / "calculus" / "limits" / "limit-of-a-function.md"
    template = REPO / "templates" / "topic.md"
    assert page.read_bytes() == template.read_bytes(), "copy templates/topic.md into the clean fixture (and re-run --update-lock there)"


def test_clean_lock_accepts_a_tombstone():
    assert "→" in (FIXTURES / "clean" / "labels.lock").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", ["forward-reference-outside-closure", "forward-citation-in-proof"])
def test_forward_references_warn_on_unverified_pages(name, tmp_path):
    """The same forward reference is a warning on a draft page, an error only on a verified one."""
    shutil.copytree(FIXTURES / name, tmp_path / name)
    page = tmp_path / name / "content" / "calculus" / "limits" / "limit-of-a-function.md"
    page.write_text(page.read_text(encoding="utf-8").replace("status: verified", "status: draft"), encoding="utf-8")
    rep = run(tmp_path / name / "content")
    assert not rep.errors, fmt(rep)
    assert len(rep.warnings) == 1 and DEFECTS[name][3] in rep.warnings[0].message, fmt(rep)


def test_a_proof_may_cite_the_statement_it_proves():
    """Directly after its statement or paired by prf-<slug>, a proof may cite that statement (02 §2.5)."""
    assert not run("proof-cites-own-statement").diagnostics


def test_looking_ahead_admonition_allows_a_forward_reference(tmp_path):
    name = "forward-reference-outside-closure"
    shutil.copytree(FIXTURES / name, tmp_path / name)
    page = tmp_path / name / "content" / "calculus" / "limits" / "limit-of-a-function.md"
    text = page.read_text(encoding="utf-8").replace(
        "For sums of limits, see [the limit laws](#thm-calc-limit-laws).",
        ":::{admonition} Looking ahead\n:class: looking-ahead\nFor sums of limits, see [the limit laws](#thm-calc-limit-laws).\n:::",
    )
    page.write_text(text, encoding="utf-8")
    assert not run(tmp_path / name / "content").diagnostics


def test_checks_ignore_build_and_generated_copies(tmp_path):
    """Pages come from the toc, and check_toc's glob skips _build/ and _generated/ (06 §6.4)."""
    shutil.copytree(FIXTURES / "clean", tmp_path / "clean")
    content = tmp_path / "clean" / "content"
    stale = (FIXTURES / "duplicate-label" / "content" / "calculus" / "limits" / "limit-laws.md").read_text(encoding="utf-8")
    for rel in ("_build/site/calculus/limits/limit-laws.md", "calculus/_generated/prereq-map.md", "about/_generated/x.md"):
        (content / rel).parent.mkdir(parents=True, exist_ok=True)
        (content / rel).write_text(stale + "\nclearly $\\log x$\n", encoding="utf-8")
    assert not run(content).diagnostics


def test_update_lock_adds_missing_labels_sorted(tmp_path):
    shutil.copytree(FIXTURES / "label-missing-from-lock", tmp_path / "f")
    rep = Reporter(quiet=True)
    check_labels.check(Project(tmp_path / "f" / "content"), rep, update_lock=True)
    assert not rep.diagnostics, fmt(rep)
    lines = [l for l in (tmp_path / "f" / "labels.lock").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    assert lines == sorted(lines)
    assert "def-calc-limit  calculus/limits/limit-of-a-function.md" in lines


def test_update_lock_never_drops_a_removed_label(tmp_path):
    shutil.copytree(FIXTURES / "removed-label-without-tombstone", tmp_path / "f")
    rep = Reporter(quiet=True)
    check_labels.check(Project(tmp_path / "f" / "content"), rep, update_lock=True)
    assert any("thm-calc-limit-old" in d.message for d in rep.errors)
    assert "thm-calc-limit-old" in (tmp_path / "f" / "labels.lock").read_text(encoding="utf-8")


def test_github_annotations(capsys, monkeypatch):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    rep = Reporter()
    check_toc.check(Project(FIXTURES / "toc-mismatch" / "content"), rep)
    out = capsys.readouterr().out
    assert ":1: error: about/orphan.md is not in the toc" in out
    assert "::error file=" in out and "orphan.md,line=1::about/orphan.md is not in the toc" in out


def test_check_all_cli_exit_codes():
    assert check_all.main(["--root", str(FIXTURES / "clean" / "content")]) == 0
    assert check_all.main(["--root", str(FIXTURES / "orphan-proof" / "content")]) == 1


# ── maths.verify and maths.manual_checked (check_frontmatter.py, docs/plan/06 §6.6) ──

PAGE_REL = Path("calculus") / "limits" / "limit-of-a-function.md"
NOTE = "  reviewed_by: [vronnblom]\n  manual_checked:\n    {label}: {who}\n"

FRONTMATTER_CASES = {
    "note-on-a-computed-answer": ("  reviewed_by: []\n", NOTE.format(label="exr-calc-limit-table-estimate", who="vronnblom"), 34,
                                  "maths.manual_checked: exr-calc-limit-table-estimate has a machine-checkable Answer, so it needs a test"),
    "note-by-someone-not-a-reviewer": ("  reviewed_by: []\n", NOTE.format(label="exr-calc-limit-eps-delta-linear", who="someone"), 34,
                                       "maths.manual_checked: exr-calc-limit-eps-delta-linear names someone, who is not in maths.reviewed_by"),
    "note-on-an-unknown-exercise": ("  reviewed_by: []\n", NOTE.format(label="exr-calc-limit-nothing", who="vronnblom"), 34,
                                    "maths.manual_checked: exr-calc-limit-nothing is not an exercise on this page"),
    "note-on-an-example": ("  reviewed_by: []\n", NOTE.format(label="eg-calc-limit-linear-eps-delta", who="vronnblom"), 33,
                           "maths.manual_checked: eg-calc-limit-linear-eps-delta is not an exercise label"),
    "verify-path-of-another-page": ("verify/calculus/limits/test_limit_of_a_function.py", "verify/calculus/limits/test_limits.py", 30,
                                    "maths.verify is verify/calculus/limits/test_limits.py, but this page's test file is "
                                    "verify/calculus/limits/test_limit_of_a_function.py"),
}


def _edited_clean(tmp_path, old, new) -> Path:
    shutil.copytree(FIXTURES / "clean", tmp_path / "clean")
    page = tmp_path / "clean" / "content" / PAGE_REL
    text = page.read_text(encoding="utf-8")
    assert text.count(old) == 1
    page.write_text(text.replace(old, new), encoding="utf-8")
    return tmp_path / "clean" / "content"


@pytest.mark.parametrize("name", sorted(FRONTMATTER_CASES))
def test_frontmatter_rejects(name, tmp_path):
    old, new, line, message = FRONTMATTER_CASES[name]
    rep = run(_edited_clean(tmp_path, old, new), "check_frontmatter")
    hits = [d for d in rep.errors if message in d.message]
    assert hits, fmt(rep)
    assert (hits[0].path.name, hits[0].line) == ("limit-of-a-function.md", line), fmt(rep)


def test_frontmatter_accepts_a_reviewers_note(tmp_path):
    root = _edited_clean(tmp_path, "  reviewed_by: []\n", NOTE.format(label="exr-calc-limit-eps-delta-linear", who="vronnblom"))
    rep = run(root)
    assert not rep.diagnostics, fmt(rep)
