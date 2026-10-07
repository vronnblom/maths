"""Loads verify/_answers.json for mathcheck.answer() and records verification coverage
(docs/plan/06 §6.1).

- `verify/_answers.json` is written by `scripts/extract_answers.py` (`npm run verify` runs it
  after building the AST). If it is missing or **stale**, i.e. a page in the toc changed, appeared
  or went away since it was written, the run stops with a usage error before any test runs, so
  a test can never check an answer that is no longer on the page.
- The coverage plugin records, for every test, its outcome, its `@covers` labels, the mathcheck
  assertions it made and the answers it read. A label is covered only if a test declaring it
  **passed** (skipped, xfailed, xpassed and failed tests count as uncovered), no test declaring it
  failed, and, for an `exr-` label, that test called `answer(label)`; for an `eg-` label, it made
  at least one mathcheck assertion. The result goes to `verify/_coverage.json`, which
  `scripts/check_coverage.py` compares with each page's labels and status.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

import mathcheck

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
ANSWERS = HERE / "_answers.json"
COVERAGE = HERE / "_coverage.json"
FORMAT = 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def toc_pages(root: Path) -> list[str]:
    """The pages in the toc of root/myst.yml (the same list every check uses)."""
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        from project import Project
    finally:
        sys.path.pop(0)
    return [p.rel for p in Project(root).pages]


def stale_reasons(data: dict) -> list[str]:
    root = REPO / data["root"]
    recorded = data["pages"]
    reasons = []
    for rel, digest in sorted(recorded.items()):
        path = root / rel
        if not path.is_file():
            reasons.append(f"{data['root']}/{rel} no longer exists")
        elif sha256(path) != digest:
            reasons.append(f"{data['root']}/{rel} changed")
    toc = toc_pages(root)
    for rel in toc:
        if rel not in recorded:
            reasons.append(f"{data['root']}/{rel} is new in the toc")
    for rel in sorted(set(recorded) - set(toc)):
        reasons.append(f"{data['root']}/{rel} left the toc")
    return reasons


def load_answers() -> dict:
    rerun = "run `npm run verify` (it builds the AST and extracts the answers before running the tests)"
    if not ANSWERS.is_file():
        raise pytest.UsageError(f"verify/_answers.json is missing: {rerun}")
    try:
        data = json.loads(ANSWERS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise pytest.UsageError(f"verify/_answers.json is not valid JSON ({e}): {rerun}") from None
    if data.get("format") != FORMAT or not isinstance(data.get("answers"), dict) or not isinstance(data.get("pages"), dict):
        raise pytest.UsageError(f"verify/_answers.json has an unknown format: {rerun}")
    reasons = stale_reasons(data)
    if reasons:
        shown = "; ".join(reasons[:5]) + (f"; and {len(reasons) - 5} more" if len(reasons) > 5 else "")
        raise pytest.UsageError(f"verify/_answers.json is stale ({shown}): {rerun}")
    return data


class CoveragePlugin:
    def __init__(self, data: dict):
        self.data = data
        self.tests: dict[str, dict] = {}

    def _record(self, item) -> dict:
        rec = self.tests.get(item.nodeid)
        if rec is None:
            path = Path(str(item.path)).resolve()
            try:
                file = path.relative_to(REPO).as_posix()
            except ValueError:
                file = path.as_posix()
            rec = {"file": file, "covers": list(getattr(item.obj, "__mathcheck_covers__", ())),
                   "outcome": "not run", "assertions": 0, "answers": []}
            self.tests[item.nodeid] = rec
        return rec

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        self._record(item)
        mathcheck._state.begin(item.nodeid)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        rec = self._record(item)
        if report.when == "call":
            assertions, answers = mathcheck._state.end()
            rec["assertions"] = assertions
            rec["answers"] = sorted(answers)
        xfail = hasattr(report, "wasxfail")
        if report.failed:
            rec["outcome"] = "failed"
        elif rec["outcome"] == "failed":
            pass  # a failure in any phase is final
        elif report.skipped or xfail:
            rec["outcome"] = "xfailed" if xfail else "skipped"
        elif report.when == "call" and report.passed and rec["outcome"] == "not run":
            rec["outcome"] = "passed"

    def pytest_runtest_teardown(self, item):
        if mathcheck._state.test == item.nodeid:  # the call phase never ran (setup failed or skipped)
            mathcheck._state.end()

    def labels(self) -> dict:
        out: dict[str, dict] = {}
        for nodeid, rec in sorted(self.tests.items()):
            for label in rec["covers"]:
                entry = out.setdefault(label, {"covered": False, "tests": [], "reasons": []})
                entry["tests"].append(nodeid)
                why = None
                if rec["outcome"] != "passed":
                    why = rec["outcome"]
                elif label.startswith("exr-") and label not in rec["answers"]:
                    why = f'passed, but never called answer("{label}")'
                elif label.startswith("eg-") and rec["assertions"] < 1:
                    why = "passed, but made no mathcheck assertion (equal, limit_is, …)"
                if why is None:
                    entry.setdefault("passing", []).append({"test": nodeid, "file": rec["file"]})
                else:
                    entry["reasons"].append(f"{nodeid}: {why}")
                if rec["outcome"] == "failed":
                    entry["failed"] = True
        for entry in out.values():
            entry["covered"] = bool(entry.get("passing")) and not entry.get("failed")
        return out

    @staticmethod
    def partial(config) -> list[str]:
        """Why this run is not the whole of verify/ (a filtered run can't certify coverage: it
        may leave out a failing test of a label that another, passing test declares)."""
        o = config.option
        why = [f"{flag} {value}" for flag, value in (("-k", getattr(o, "keyword", "")), ("-m", getattr(o, "markexpr", "")))
               if value]
        if getattr(o, "lf", False):
            why.append("--last-failed")
        if getattr(o, "deselect", None):
            why.append("--deselect")
        if getattr(o, "maxfail", 0):
            why.append("-x/--maxfail")
        start = Path(str(config.invocation_params.dir))
        paths = {(start / a.split("::")[0]).resolve() for a in config.args}
        if HERE not in paths:
            why.append(f"only {', '.join(config.args)}")
        return why

    def pytest_sessionfinish(self, session, exitstatus):
        files = {p.relative_to(REPO).as_posix(): sha256(p)
                 for p in sorted(HERE.rglob("test_*.py")) if "fixtures" not in p.relative_to(HERE).parts}
        COVERAGE.write_text(json.dumps({
            "format": FORMAT,
            "exitstatus": int(exitstatus),
            "partial": self.partial(session.config),
            "root": self.data["root"],
            "pages": self.data["pages"],
            "test_files": files,
            "tests": self.tests,
            "labels": self.labels(),
        }, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def pytest_configure(config):
    if COVERAGE.exists():
        COVERAGE.unlink()  # never leave the coverage of an earlier run behind
    data = load_answers()
    mathcheck._install_answers(data["answers"])
    config.pluginmanager.register(CoveragePlugin(data), "mathcheck-coverage")
