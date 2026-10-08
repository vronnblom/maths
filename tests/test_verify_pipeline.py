"""The verification pipeline end to end, as `npm run verify` runs it (docs/plan/06 §6.1, §6.6):
`myst build --site` → scripts/extract_answers.py → pytest with verify/conftest.py →
scripts/check_coverage.py.

The project is the one tests/test_plugin_build.py assembles: templates/topic.md (verbatim) with
the real curriculum. Its test is templates/verify_test.py, verbatim, at the page's maths.verify
path. Each defect below is that project with **one** edit, and must fail with its message.

The build uses a stub site template (no theme, no network), so this runs in the `checks` job.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_plugin_build import make_project  # noqa: E402

from project import REPO  # noqa: E402

MYST_BIN = REPO / "node_modules" / ".bin"
PAGE = "content/calculus/limits/limit-of-a-function.md"
TEST = "verify/calculus/limits/test_limit_of_a_function.py"
STATUS = "  status: draft\n"
REVIEWERS = "  reviewed_by: []\n"
# The page made verified, with the reviewer's note for its manual exercise (06 §6.6).
VERIFIED = [
    (PAGE, STATUS, "  status: verified\n"),
    (PAGE, REVIEWERS, "  reviewed_by: [vronnblom]\n  manual_checked:\n    exr-calc-limit-eps-delta-linear: vronnblom\n"),
]
EG_ASSERTION = "    assert equal(sp.Abs((2 * x - 1) - 5), 2 * sp.Abs(x - 3))\n"
EG_DEF = "def test_linear_eps_delta_example():\n"
EXR_DEF = "def test_table_estimate():\n"
ANSWER_CALL = '    printed = float(answer("exr-calc-limit-table-estimate"))\n'
TABLE_ANSWER = ":::{admonition} Answer\n:class: dropdown answer numeric-5e-3\n$0.50$\n:::\n"


class Run:
    def __init__(self, root: Path):
        self.root = root
        self.steps: dict[str, subprocess.CompletedProcess] = {}

    def output(self, step: str) -> str:
        r = self.steps[step]
        return r.stdout + r.stderr

    def failed_at(self) -> str | None:
        return next((name for name, r in self.steps.items() if r.returncode != 0), None)


def edit(root: Path, edits):
    for rel, old, new in edits:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        assert text.count(old) == 1, f"{old!r} must occur exactly once in {rel}"
        path.write_text(text.replace(old, new), encoding="utf-8")


def assemble(root: Path, edits=()) -> Path:
    if not (MYST_BIN / "myst").exists():
        pytest.fail("mystmd is not installed: run npm ci (the checks job does)")
    content = make_project(root)
    # The plugin fixture's limit-laws page is reviewed without a test file; that is not this test's subject.
    edit(root, [("content/calculus/limits/limit-laws.md", STATUS.replace("draft", "reviewed"), STATUS)])
    (root / TEST).parent.mkdir(parents=True)
    shutil.copy(REPO / "templates" / "verify_test.py", root / TEST)
    shutil.copy(REPO / "verify" / "conftest.py", root / "verify" / "conftest.py")
    edit(root, edits)
    return content


def run_step(run: Run, name: str, cmd, cwd: Path, env=None) -> bool:
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
    run.steps[name] = r
    return r.returncode == 0


def build(root: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "PATH": f"{MYST_BIN}{os.pathsep}{os.environ.get('PATH', '')}"}
    r = subprocess.run(["myst", "build", "--site", "--ci"], cwd=root / "content", env=env,
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stdout + r.stderr
    return r


def extract(run: Run) -> bool:
    root = run.root
    return run_step(run, "extract", [sys.executable, str(REPO / "scripts" / "extract_answers.py"),
                                     str(root / "content" / "_build" / "site" / "content"),
                                     "-o", str(root / "verify" / "_answers.json"), "--root", str(root / "content")], REPO)


def pytest_verify(run: Run) -> bool:
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(REPO / "verify"), str(REPO / "scripts")])}
    return run_step(run, "pytest", [sys.executable, "-m", "pytest", "verify", "-q", "-ra", "-p", "no:cacheprovider",
                                    "--import-mode=importlib", "--rootdir", str(run.root)], run.root, env)


def coverage(run: Run) -> bool:
    return run_step(run, "coverage", [sys.executable, str(REPO / "scripts" / "check_coverage.py"),
                                      "--root", str(run.root / "content")], REPO)


def pipeline(root: Path, edits=(), after_build=()) -> Run:
    """Assemble, build, then extract → pytest → coverage, stopping at the first failing step
    (as `npm run verify` does with &&). `after_build` edits are applied after the AST was built."""
    assemble(root, edits)
    build(root)
    edit(root, after_build)
    run = Run(root)
    if extract(run) and pytest_verify(run):
        coverage(run)
    return run


# ── The template, end to end ─────────────────────────────────────────────────

TEMPLATE_REPORT = """\
Verification coverage (eg-/exr- labels covered by passing tests, or manual with a reviewer's note):
  calculus/limits/limit-of-a-function.md  [draft]  2/3 (67%):  examples 1/1, exercises 1/2
    ✓ eg-calc-limit-linear-eps-delta  verify/calculus/limits/test_limit_of_a_function.py::test_linear_eps_delta_example
    ✓ exr-calc-limit-table-estimate  verify/calculus/limits/test_limit_of_a_function.py::test_table_estimate
    ✗ exr-calc-limit-eps-delta-linear  manual answer without a reviewer's note: a reviewer adds `exr-calc-limit-eps-delta-linear: <their handle>` to maths.manual_checked
"""


def test_the_template_end_to_end(tmp_path):
    """templates/topic.md → extract → templates/verify_test.py → check_coverage, both unchanged."""
    run = pipeline(tmp_path)
    assert run.failed_at() is None, {k: run.output(k) for k in run.steps}
    assert "2 answers (1 manual) from 5 pages" in run.output("extract")
    assert "4 passed" in run.output("pytest")
    assert run.steps["coverage"].stdout == TEMPLATE_REPORT


def test_the_template_verified_with_a_reviewers_note(tmp_path):
    """The base of the defects below: verified, 100 % (the manual exercise by the reviewer's note)."""
    run = pipeline(tmp_path, VERIFIED)
    assert run.failed_at() is None, {k: run.output(k) for k in run.steps}
    out = run.steps["coverage"].stdout
    assert "[verified]  3/3 (100%):  examples 1/1, exercises 2/2 (1 manual)" in out
    assert "✓ exr-calc-limit-eps-delta-linear  manual, checked by vronnblom" in out


# ── One defect each ──────────────────────────────────────────────────────────

STUB = '    pytest.skip("for the verifier")\n'

DEFECTS = {
    # name: (edits on top of VERIFIED, edits after the build, failing step, message)
    "covers-stub-on-verified-page": (
        [(TEST, EG_DEF, EG_DEF + STUB), (TEST, "import random\n", "import random\n\nimport pytest\n")], [],
        "coverage", "status verified needs all of the examples and exercises verified, but 2 of 3 are (67%). Uncovered: "
                    "eg-calc-limit-linear-eps-delta: verify/calculus/limits/test_limit_of_a_function.py::test_linear_eps_delta_example: skipped"),
    "eg-test-without-mathcheck-assertion": (
        [(TEST, EG_ASSERTION, "    assert sp.simplify(sp.Abs((2 * x - 1) - 5) - 2 * sp.Abs(x - 3)) == 0\n")], [],
        "coverage", "eg-calc-limit-linear-eps-delta: verify/calculus/limits/test_limit_of_a_function.py::test_linear_eps_delta_example: "
                    "passed, but made no mathcheck assertion (equal, limit_is, …)"),
    "exr-test-that-never-calls-answer": (
        [(TEST, ANSWER_CALL, "    printed = 0.50\n")], [],
        "coverage", 'exr-calc-limit-table-estimate: verify/calculus/limits/test_limit_of_a_function.py::test_table_estimate: '
                    'passed, but never called answer("exr-calc-limit-table-estimate")'),
    "failing-test": (
        [(TEST, EG_ASSERTION, EG_ASSERTION.replace("2 * sp.Abs(x - 3)", "3 * sp.Abs(x - 3)"))], [],
        "pytest", "FAILED verify/calculus/limits/test_limit_of_a_function.py::test_linear_eps_delta_example"),
    "reviewed-page-below-50-percent": (
        [(PAGE, "  status: verified\n", "  status: reviewed\n"), (TEST, EG_DEF, EG_DEF + STUB), (TEST, EXR_DEF, EXR_DEF + STUB),
         (TEST, "import random\n", "import random\n\nimport pytest\n")], [],
        "coverage", "status reviewed needs at least 50% of the examples and exercises verified, but 1 of 3 are (33%)"),
    "answer-outside-the-subset": (
        [(PAGE, "\n$0.50$\n", "\n$\\approx 0.50$\n")], [],
        "pytest", "cannot read the answer '\\\\approx 0.50': \\approx is not in the answer subset. Rewrite the answer in the "
                  "answer LaTeX subset (docs/plan/04 §4.3), or mark it `:class: dropdown answer manual`"),
    "wrongly-rounded-numeric-answer": (
        [(PAGE, "\n$0.50$\n", "\n$0.51$\n")], [],
        "pytest", "FAILED verify/calculus/limits/test_limit_of_a_function.py::test_table_estimate"),
    "exercise-without-an-answer": (
        [(PAGE, TABLE_ANSWER + "::::\n", "::::\n")], [],
        "extract", "exercise exr-calc-limit-table-estimate needs exactly one Answer admonition (:class: dropdown answer), found 0"),
    "exercise-with-two-answers": (
        [(PAGE, TABLE_ANSWER + "::::\n", TABLE_ANSWER + "\n" + TABLE_ANSWER + "::::\n")], [],
        "extract", "exercise exr-calc-limit-table-estimate needs exactly one Answer admonition (:class: dropdown answer), found 2"),
    "unknown-answer-type": (
        [(PAGE, ":class: dropdown answer numeric-5e-3\n", ":class: dropdown answer numerical\n")], [],
        "extract", "the Answer of exr-calc-limit-table-estimate has the class 'numerical', which is not an answer type"),
    "manual-answer-without-a-note-on-verified-page": (
        [(PAGE, "  manual_checked:\n    exr-calc-limit-eps-delta-linear: vronnblom\n", "")], [],
        "coverage", "exr-calc-limit-eps-delta-linear: manual answer without a reviewer's note"),
    "xfailed-test": (
        [(TEST, "@covers(\"eg-calc-limit-linear-eps-delta\")\n", "@pytest.mark.xfail(reason=\"probe\")\n@covers(\"eg-calc-limit-linear-eps-delta\")\n"),
         (TEST, "import random\n", "import random\n\nimport pytest\n"),
         (TEST, EG_ASSERTION, EG_ASSERTION + "    assert False\n")], [],
        "coverage", "test_linear_eps_delta_example: xfailed"),
    "covers-an-unknown-label": (
        [(TEST, '@covers("exr-calc-limit-eps-delta-linear")\n', '@covers("exr-calc-limit-eps-delta-linear", "eg-calc-limit-typo")\n')], [],
        "coverage", 'test_eps_delta_exercise_key_claim declares @covers("eg-calc-limit-typo"), but no page in the toc has that label'),
    "stale-ast": (
        [], [(PAGE, "\n$0.50$\n", "\n$0.51$\n")],
        "extract", "was built from an older version of this page: rebuild it (npm run ast, or npm run verify)"),
}


@pytest.mark.parametrize("name", sorted(DEFECTS))
def test_defect_fails_with_its_message(name, tmp_path):
    edits, after_build, step, message = DEFECTS[name]
    run = pipeline(tmp_path, VERIFIED + list(edits), after_build)
    assert run.failed_at() == step, {k: run.output(k) for k in run.steps}
    assert message in run.output(step), run.output(step)


def test_stale_answers_stop_pytest(tmp_path):
    assemble(tmp_path)
    build(tmp_path)
    run = Run(tmp_path)
    assert extract(run)
    edit(tmp_path, [(PAGE, "\n$0.50$\n", "\n$0.51$\n")])  # after the answers were extracted
    assert not pytest_verify(run)
    assert ("verify/_answers.json is stale (content/calculus/limits/limit-of-a-function.md changed): run `npm run verify`"
            in run.output("pytest"))


def test_missing_answers_stop_pytest(tmp_path):
    assemble(tmp_path)
    run = Run(tmp_path)
    assert not pytest_verify(run)
    assert "verify/_answers.json is missing: run `npm run verify`" in run.output("pytest")
    assert not (tmp_path / "verify" / "_coverage.json").exists()


def test_failed_extraction_deletes_old_answers(tmp_path):
    assemble(tmp_path)
    build(tmp_path)
    run = Run(tmp_path)
    assert extract(run)
    edit(tmp_path, [(PAGE, "\n$0.50$\n", "\n$0.51$\n")])  # now the AST is stale
    assert not extract(run)
    assert not (tmp_path / "verify" / "_answers.json").exists()


def test_stale_coverage_fails_the_gate(tmp_path):
    run = pipeline(tmp_path)
    assert run.failed_at() is None
    edit(tmp_path, [(TEST, "    printed = float(", "    printed = 0 + float(")])  # the test changed since the run
    assert not coverage(run)
    assert f"is stale ({TEST} changed)" in run.output("coverage")


def test_a_partial_run_cannot_certify_coverage(tmp_path):
    """A filtered run (here -k) could leave out a failing test of a label another test covers."""
    assemble(tmp_path)
    build(tmp_path)
    run = Run(tmp_path)
    assert extract(run)
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(REPO / "verify"), str(REPO / "scripts")])}
    assert run_step(run, "pytest", [sys.executable, "-m", "pytest", "verify", "-q", "-p", "no:cacheprovider",
                                    "--import-mode=importlib", "-k", "table"], tmp_path, env)
    assert not coverage(run)
    assert "comes from a partial pytest run (-k table), which cannot certify coverage" in run.output("coverage")


def test_a_test_outside_the_pages_verify_file_does_not_count(tmp_path):
    other = "verify/calculus/test_elsewhere.py"
    assemble(tmp_path, VERIFIED)
    shutil.move(tmp_path / TEST, tmp_path / other)
    (tmp_path / TEST).write_text('"""Empty."""\n', encoding="utf-8")
    build(tmp_path)
    run = Run(tmp_path)
    assert extract(run) and pytest_verify(run)
    assert not coverage(run)
    assert "covered only by tests outside the page's maths.verify (verify/calculus/limits/test_limit_of_a_function.py)" in run.output("coverage")
