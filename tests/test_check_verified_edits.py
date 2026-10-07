"""scripts/check_verified_edits.py on temporary git repositories (docs/plan/06 §6.6).

The base commit has templates/topic.md as a **verified** page with its test file, and a draft
page. Each test commits one change on top and runs the guard against the base.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import check_verified_edits as guard
from project import REPO, Reporter

PAGE = "content/calculus/limits/limit-of-a-function.md"
TEST = "verify/calculus/limits/test_limit_of_a_function.py"
DRAFT = "content/calculus/limits/limit-laws.md"
VERIFIED = [("  status: draft\n", "  status: verified\n"), ("  reviewed_by: []\n", "  reviewed_by: [vronnblom]\n")]
EXAMPLE_STEP = "1. **Scratch work.** $\\abs{(2x - 1) - 5} = \\abs{2x - 6} = 2\\abs{x - 3}$."


def sh(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false",
                           *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def write(repo: Path, rel: str, text: str):
    (repo / rel).parent.mkdir(parents=True, exist_ok=True)
    (repo / rel).write_text(text, encoding="utf-8")


def replace(repo: Path, rel: str, old: str, new: str):
    text = (repo / rel).read_text(encoding="utf-8")
    assert text.count(old) == 1, old
    write(repo, rel, text.replace(old, new))


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    page = (REPO / "templates" / "topic.md").read_text(encoding="utf-8")
    for old, new in VERIFIED:
        page = page.replace(old, new)
    write(r, PAGE, page)
    write(r, DRAFT, (REPO / "tests" / "fixtures" / "clean" / "content" / "calculus" / "limits" / "limit-of-a-function.md")
          .read_text(encoding="utf-8").replace("label: calc-limit\n", "label: calc-limit-laws\n"))
    write(r, TEST, (REPO / "templates" / "verify_test.py").read_text(encoding="utf-8"))
    write(r, "content/myst.yml", "version: 1\nproject:\n  toc:\n    - file: calculus/limits/limit-of-a-function.md\n"
                                 "    - file: calculus/limits/limit-laws.md\n")
    sh(r, "init", "-q", "-b", "main")
    sh(r, "add", "-A")
    sh(r, "commit", "-q", "-m", "base")
    return r


def check(repo: Path, labels=()):
    base = sh(repo, "rev-parse", "HEAD~1")
    rep = Reporter(quiet=True)
    notes = guard.check(repo, repo / "content", base, "HEAD", set(labels), rep)
    return rep, notes


def commit(repo: Path):
    sh(repo, "add", "-A")
    sh(repo, "commit", "-q", "-m", "change")


def test_edited_verified_page_fails(repo):
    replace(repo, PAGE, EXAMPLE_STEP, EXAMPLE_STEP.replace("2\\abs{x - 3}", "3\\abs{x - 3}"))
    commit(repo)
    rep, _ = check(repo)
    (e,) = rep.errors
    assert e.path == repo / PAGE and e.line == 139  # the {proof:example} line
    assert e.message.startswith("eg-calc-limit-linear-eps-delta changed on a verified page, but "
                                "verify/calculus/limits/test_limit_of_a_function.py did not change.")
    assert "set maths.status to reviewed" in e.message and "typo-only" in e.message


def test_edited_answer_fails(repo):
    replace(repo, PAGE, "\n$0.69$\n", "\n$0.70$\n")
    commit(repo)
    rep, _ = check(repo)
    assert [e.message.split(" on a verified page")[0] for e in rep.errors] == ["exr-calc-limit-table-estimate changed"]


def test_added_block_fails(repo):
    replace(repo, PAGE, "## Common mistakes\n", ":::{proof:example} Another\n:label: eg-calc-limit-another\n"
                                                 "$\\lim_{x \\to 0} x = 0$\n:::\n\n## Common mistakes\n")
    commit(repo)
    rep, _ = check(repo)
    assert [e.message.split(" on a verified page")[0] for e in rep.errors] == ["eg-calc-limit-another was added"]


def test_edited_with_the_test_passes(repo):
    replace(repo, PAGE, EXAMPLE_STEP, EXAMPLE_STEP.replace("2\\abs{x - 3}", "3\\abs{x - 3}"))
    replace(repo, TEST, "# Step 1 on the page", "# Step 1 on the page (re-checked)")
    commit(repo)
    rep, notes = check(repo)
    assert not rep.errors and "1 block(s) changed, and verify/calculus/limits/test_limit_of_a_function.py changed too" in notes[0]


def test_status_lowered_passes(repo):
    replace(repo, PAGE, EXAMPLE_STEP, EXAMPLE_STEP.replace("2\\abs{x - 3}", "3\\abs{x - 3}"))
    replace(repo, PAGE, "  status: verified\n", "  status: reviewed\n")
    commit(repo)
    rep, notes = check(repo)
    assert not rep.errors and notes == [f"{PAGE}: verified → reviewed, lowered in this PR"]


def test_typo_only_label_passes(repo):
    replace(repo, PAGE, "Prove $\\lim_{x \\to 3}", "Prove that $\\lim_{x \\to 3}")
    commit(repo)
    assert check(repo)[0].errors
    rep, notes = check(repo, labels={"typo-only", "documentation"})
    assert not rep.errors and "passed because the PR is labelled typo-only" in notes[0]


def test_draft_page_edited_passes(repo):
    replace(repo, DRAFT, EXAMPLE_STEP, EXAMPLE_STEP.replace("2\\abs{x - 3}", "3\\abs{x - 3}"))
    commit(repo)
    rep, notes = check(repo)
    assert not rep.errors and not notes


def test_prose_outside_blocks_passes(repo):
    replace(repo, PAGE, "**In words.** Whatever", "**In words.** Whichever")
    commit(repo)
    assert not check(repo)[0].errors


def test_moved_verified_page_is_still_guarded(repo):
    replace(repo, PAGE, EXAMPLE_STEP, EXAMPLE_STEP.replace("2\\abs{x - 3}", "3\\abs{x - 3}"))
    sh(repo, "mv", PAGE, "content/calculus/limits/the-limit.md")
    commit(repo)
    rep, _ = check(repo)
    assert len(rep.errors) == 1 and rep.errors[0].path == repo / "content/calculus/limits/the-limit.md"


def test_unreadable_status_fails(repo):
    replace(repo, PAGE, "  status: verified\n", "  status: [verified\n")
    commit(repo)
    rep, _ = check(repo)
    assert "its maths.status can no longer be read" in rep.errors[0].message


def test_labels_from_guard_yml():
    assert guard.parse_labels('["typo-only", "x"]') == {"typo-only", "x"}
    assert guard.parse_labels("[]") == set() and guard.parse_labels("") == set()
    assert guard.parse_labels("typo-only, x") == {"typo-only", "x"}


def test_cli(repo, capsys):
    replace(repo, PAGE, "\n$0.69$\n", "\n$0.70$\n")
    commit(repo)
    base = sh(repo, "rev-parse", "HEAD~1")
    root = str(repo / "content")
    assert guard.main(["--base", base, "--root", root]) == 1
    assert guard.main(["--base", base, "--root", root, "--labels", '["typo-only"]']) == 0
    assert "exr-calc-limit-table-estimate changed on a verified page" in capsys.readouterr().out


def test_unknown_base_fails_clearly(repo):
    rep = Reporter(quiet=True)
    guard.check(repo, repo / "content", "0" * 40, "HEAD", set(), rep)
    assert "the job needs the full history (fetch-depth: 0)" in rep.errors[0].message
