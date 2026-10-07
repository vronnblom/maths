"""The coverage gate: each page's status against the verification coverage that the last pytest
run actually achieved (docs/plan/06 §6.1, §6.6). `npm run verify` runs it after `pytest verify`.

    check_coverage.py [--root content] [--coverage verify/_coverage.json]

A page's `eg-` and `exr-` labels (from its Markdown, via myst_source.py) are each:
- **covered**: verify/_coverage.json says a test declaring it passed (and called `answer(label)`
  for an exercise, made a mathcheck assertion for an example), no test declaring it failed, and
  a passing test is in the page's `maths.verify` file;
- **manual**: an exercise whose Answer is `manual` and whose page lists it in
  `maths.manual_checked` with a reviewer from `maths.reviewed_by` (the reviewer's note: a proof
  or a sketch that no test can read, checked by hand);
- otherwise **uncovered**, with the reason.

Thresholds (06 §6.6): `reviewed` needs the verify file and at least 50 % covered or manual;
`verified` needs 100 %. Draft pages are reported, never failed. Every page with examples or
exercises is printed with its coverage, the numbers the PR template asks for.

Errors: a missing or stale _coverage.json (a page or a test file changed since the pytest run),
a page below its threshold, and an `@covers` label that is on no page (a typo would otherwise
leave the intended label silently uncovered).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import myst_source as ms
from project import STATUS_RANK, Page, Project, Reporter, add_root_argument, display_path

FORMAT = 1
THRESHOLD = {"reviewed": 0.5, "verified": 1.0}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class Block:
    label: str
    line: int
    manual: bool = False  # an exercise whose Answer is `manual`


@dataclass
class PageCoverage:
    page: Page
    blocks: list = field(default_factory=list)
    covered: dict = field(default_factory=dict)  # label → test
    manual: dict = field(default_factory=dict)  # label → reviewer
    uncovered: dict = field(default_factory=dict)  # label → reason

    @property
    def total(self) -> int:
        return len(self.blocks)

    @property
    def done(self) -> int:
        return len(self.covered) + len(self.manual)

    @property
    def fraction(self) -> float:
        return self.done / self.total if self.total else 1.0


def page_blocks(doc: ms.Document) -> list[Block]:
    """The eg-/exr- labels of a page, in order, with whether each exercise's Answer is manual."""
    out = []
    for d in doc.directives():
        if not d.label:
            continue
        if d.name == "proof:example" and d.label.startswith("eg-"):
            out.append(Block(d.label, d.option_line("label")))
        elif d.name == "exercise" and d.label.startswith("exr-"):
            answers = [c for c in d.children if isinstance(c, ms.Directive) and c.name == "admonition" and "answer" in c.classes]
            manual = len(answers) == 1 and "manual" in answers[0].classes
            out.append(Block(d.label, d.option_line("label"), manual=manual))
    return out


def load_coverage(path: Path, project: Project, rep: Reporter) -> dict | None:
    rerun = "run npm run verify (it rebuilds the answers and reruns pytest verify)"
    if not path.is_file():
        rep.error(path, 1, f"{display_path(path)} does not exist: {rerun}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        rep.error(path, 1, f"not valid JSON ({e}): {rerun}")
        return None
    if data.get("format") != FORMAT:
        rep.error(path, 1, f"unknown format: {rerun}")
        return None
    stale = []
    for page in project.pages:
        recorded = data["pages"].get(page.rel)
        if recorded is None:
            stale.append(f"{page.rel} is new in the toc")
        elif recorded != sha256(page.path):
            stale.append(f"{page.rel} changed")
    verify_dir = project.repo / "verify"
    now = {p.relative_to(project.repo).as_posix(): sha256(p)
           for p in sorted(verify_dir.rglob("test_*.py")) if "fixtures" not in p.relative_to(verify_dir).parts}
    for f in sorted(set(now) | set(data.get("test_files", {}))):
        if now.get(f) != data.get("test_files", {}).get(f):
            stale.append(f"{f} changed" if f in now and f in data["test_files"] else f"{f} is {'new' if f in now else 'gone'}")
    if stale:
        rep.error(path, 1, f"{display_path(path)} is stale ({'; '.join(stale[:5])}{'; …' if len(stale) > 5 else ''}): {rerun}")
        return None
    if data.get("partial"):
        rep.error(path, 1, f"{display_path(path)} comes from a partial pytest run ({'; '.join(data['partial'])}), "
                           f"which cannot certify coverage: {rerun}")
        return None
    if data.get("exitstatus"):
        rep.warning(path, 1, f"the pytest run that wrote this failed (exit status {data['exitstatus']}); "
                             f"only its passing tests count")
    return data


def assess(project: Project, data: dict, rep: Reporter) -> list[PageCoverage]:
    labels = data.get("labels", {})
    results = []
    on_pages: set[str] = set()
    for page in project.pages:
        try:
            doc = ms.parse(page.text)
        except ms.ParseError as e:
            rep.error(page.path, e.line, e.message)
            continue
        cov = PageCoverage(page, page_blocks(doc))
        verify_file = page.maths.get("verify")
        notes = page.maths.get("manual_checked") or {}
        reviewers = set(page.maths.get("reviewed_by") or [])
        for b in cov.blocks:
            on_pages.add(b.label)
            if b.manual:
                who = notes.get(b.label) if isinstance(notes, dict) else None
                if who and who in reviewers:
                    cov.manual[b.label] = who
                else:
                    cov.uncovered[b.label] = ("manual answer without a reviewer's note: a reviewer adds "
                                              f"`{b.label}: <their handle>` to maths.manual_checked")
                continue
            entry = labels.get(b.label)
            if entry is None:
                cov.uncovered[b.label] = "no test declares it (@covers)"
                continue
            passing = entry.get("passing") or []
            here = [p for p in passing if not verify_file or p["file"] == verify_file]
            if entry.get("covered") and here:
                cov.covered[b.label] = here[0]["test"]
            elif entry.get("covered"):
                cov.uncovered[b.label] = (f"covered only by tests outside the page's maths.verify ({verify_file}): "
                                          + ", ".join(p["test"] for p in passing))
            else:
                cov.uncovered[b.label] = "; ".join(entry.get("reasons") or ["not covered"])
        results.append(cov)
    for label, entry in sorted(labels.items()):
        if label.startswith(("eg-", "exr-")) and label not in on_pages:
            test = entry["tests"][0]
            rep.error(project.repo / test.split("::")[0], 1,
                      f"{test} declares @covers(\"{label}\"), but no page in the toc has that label")
    return results


def gate(results: list[PageCoverage], rep: Reporter) -> None:
    for cov in results:
        status = cov.page.status
        if STATUS_RANK[status] < STATUS_RANK["reviewed"]:
            continue
        need = THRESHOLD[status]
        line = cov.page.line("maths", "status")
        v = cov.page.maths.get("verify")
        if cov.page.kind in ("topic", "chapter") and not (v and (cov.page.root.parent / v).is_file()):
            rep.error(cov.page.path, line, f"status {status} needs the page's verification file (maths.verify)")
        if cov.fraction < need:
            missing = "; ".join(f"{label}: {why}" for label, why in cov.uncovered.items())
            rep.error(cov.page.path, line,
                      f"status {status} needs {'all' if need == 1 else f'at least {need:.0%}'} of the examples and "
                      f"exercises verified, but {cov.done} of {cov.total} are ({cov.fraction:.0%}). Uncovered: {missing} "
                      f"(docs/plan/06 §6.6)")


def report(results: list[PageCoverage], out) -> None:
    rows = [c for c in results if c.total]
    print("Verification coverage (eg-/exr- labels covered by passing tests, or manual with a reviewer's note):", file=out)
    if not rows:
        print("  no page has examples or exercises yet", file=out)
    for c in rows:
        eg = [b for b in c.blocks if b.label.startswith("eg-")]
        exr = [b for b in c.blocks if b.label.startswith("exr-")]

        def n_done(bs):
            return sum(1 for b in bs if b.label in c.covered or b.label in c.manual)

        print(f"  {c.page.rel}  [{c.page.status}]  {c.done}/{c.total} ({c.fraction:.0%}):  "
              f"examples {n_done(eg)}/{len(eg)}, exercises {n_done(exr)}/{len(exr)}"
              f"{f' ({len(c.manual)} manual)' if c.manual else ''}", file=out)
        for b in c.blocks:
            if b.label in c.covered:
                print(f"    ✓ {b.label}  {c.covered[b.label]}", file=out)
            elif b.label in c.manual:
                print(f"    ✓ {b.label}  manual, checked by {c.manual[b.label]}", file=out)
            else:
                print(f"    ✗ {b.label}  {c.uncovered[b.label]}", file=out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    ap.add_argument("--coverage", help="default: verify/_coverage.json next to the project root")
    args = ap.parse_args(argv)
    project = Project(args.root)
    path = Path(args.coverage) if args.coverage else project.repo / "verify" / "_coverage.json"
    rep = Reporter()
    data = load_coverage(path, project, rep)
    if data is not None:
        results = assess(project, data, rep)
        report(results, sys.stdout)
        gate(results, rep)
    print(f"check_coverage.py: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)", file=sys.stderr)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
