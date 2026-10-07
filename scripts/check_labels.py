"""Labels and cross-references in every page of the toc (docs/plan/02 §2.4–2.5, 06 §6.4, 06 §6.7).

Checks: the label grammar and kind prefix (`thm-` on {proof:theorem}, …); required labels;
duplicates across all pages; examples, exercises and solutions prefixed by their topic; every
exercise has a tier class, exactly one Answer admonition and exactly one solution after it;
every proof directly follows its statement or is paired with it by label (prf-<slug>);
references point to existing labels with the [text](#label) syntax; every label is in
labels.lock and no locked label disappears without a tombstone.

    check_labels.py                  the checks above
    check_labels.py --forward-refs   also the forward-reference rules (02 §2.5): warnings, errors
                                     on verified pages
    check_labels.py --update-lock    add new labels to labels.lock (sorted, with their page) and
                                     update the page of moved ones; then check
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import myst_source as ms
from project import SUBJECTS, Page, Project, Reporter, add_root_argument, display_path

CHARSET = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KINDS = ("def", "thm", "lem", "cor", "prop", "ax", "prf", "eg", "exr", "sol", "rem", "eq", "fig", "tbl", "sec", "wdg")
BLOCK = re.compile(r"^(" + "|".join(KINDS) + r")-([a-z0-9]+)-[a-z0-9]+(-[a-z0-9]+)*$")
TIERS = ("tier-a", "tier-b", "tier-c")
SEE_ALSO_CLASSES = ("see-also", "looking-ahead")
LOCK_HEADER = """\
# labels.lock: every label ever merged to main (docs/plan/02 §2.4, 06 §6.7).
# One line per label: `<label>  <page, relative to content/>`, sorted. New labels are added by
#   uv run python scripts/check_labels.py --update-lock
# which also updates the page of a moved label. Never delete a line: a label that is removed
# from the content keeps a tombstone instead, `<label> → <replacement label, or the reason>`.
"""


@dataclass
class Site:
    label: str
    page: Page
    line: int
    node: object  # a myst_source node, or None for the page label


@dataclass
class LockEntry:
    label: str
    line: int
    page: str | None = None  # live entry
    tombstone: str | None = None  # tombstone text


def lock_path(project: Project) -> Path:
    return project.repo / "labels.lock"


def read_lock(path: Path, rep: Reporter) -> dict[str, LockEntry] | None:
    if not path.exists():
        return None
    entries: dict[str, LockEntry] = {}
    for n, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), start=1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"^(\S+)\s*(?:→|->)\s*(.+)$", s)
        if m:
            e = LockEntry(m.group(1), n, tombstone=m.group(2).strip())
        else:
            parts = s.split()
            if len(parts) != 2:
                rep.error(path, n, f"cannot read this line: expected `<label>  <page>` or `<label> → <reason>`")
                continue
            e = LockEntry(parts[0], n, page=parts[1])
        if e.label in entries:
            rep.error(path, n, f"{e.label} is listed twice (first at line {entries[e.label].line})")
            continue
        entries[e.label] = e
    return entries


def write_lock(path: Path, entries: dict[str, LockEntry]) -> None:
    lines = []
    for label in sorted(entries):
        e = entries[label]
        lines.append(f"{label} → {e.tombstone}" if e.tombstone is not None else f"{label}  {e.page}")
    path.write_text(LOCK_HEADER + "\n".join(lines) + "\n", encoding="utf-8")


def _expected_prefix(page: Page, kind: str) -> str | None:
    """eg-/exr-/sol- labels start with their topic (or chapter) slug (02 §2.4)."""
    if kind not in ("eg", "exr", "sol") or not page.label:
        return None
    if page.kind == "topic":
        return f"{kind}-{page.label}-"
    if page.kind == "chapter" and page.subject and page.label.endswith("-chapter"):
        return f"{kind}-{page.label[: -len('-chapter')]}-"
    return None


class LabelChecker:
    def __init__(self, project: Project, rep: Reporter):
        self.project = project
        self.rep = rep
        self.docs: dict[str, ms.Document] = {}
        self.sites: dict[str, Site] = {}  # first occurrence of each label
        self.proves: dict[int, ms.Directive] = {}  # id(proof) → the statement it proves

    def err(self, page, line, msg):
        self.rep.error(page.path, line, msg)

    def run(self, forward_refs=False, update_lock=False):
        for page in self.project.pages:
            try:
                self.docs[page.rel] = ms.parse(page.text)
            except ms.ParseError as e:
                self.err(page, e.line, e.message)
        for page in self.project.pages:
            self._collect(page)
        for page in self.project.pages:
            doc = self.docs.get(page.rel)
            if doc is not None:
                self._check_page(page, doc)
        self._check_lock(update_lock)
        if forward_refs:
            self._check_forward_refs()

    # ── collection and per-label rules ──

    def _add(self, label, page, line, node):
        if label in self.sites:
            first = self.sites[label]
            self.err(page, line, f"duplicate label {label}: already used at {display_path(first.page.path)}:{first.line}")
            return
        self.sites[label] = Site(label, page, line, node)

    def _collect(self, page: Page):
        if page.label:
            self._add(page.label, page, page.line("label"), None)
        doc = self.docs.get(page.rel)
        if doc is None:
            return
        subj = "site" if page.kind == "meta" else page.subject
        for s in ms.label_sites(doc):
            label = s.label
            if not CHARSET.match(label):
                self.err(page, s.line, f"label {label!r} may use only lowercase letters, digits and single hyphens [a-z0-9-] (docs/plan/02 §2.4)")
                continue
            m = BLOCK.match(label)
            if not m:
                self.err(page, s.line, f"label {label} does not fit <kind>-<subject>-<slug> with kind one of {' '.join(KINDS)} (docs/plan/02 §2.4)")
                continue
            kind, lsubj = m.group(1), m.group(2)
            if lsubj not in SUBJECTS + ("site",):
                self.err(page, s.line, f"label {label}: {lsubj} is not a subject code (docs/plan/02 §2.4)")
            elif subj and lsubj != subj:
                self.err(page, s.line, f"label {label} on a {subj} page should be {kind}-{subj}-…")
            if s.kinds and kind not in s.kinds:
                self.err(page, s.line, f"label {label} on {s.where}: the kind prefix should be {' or '.join(k + '-' for k in s.kinds)}")
            elif not s.kinds:
                self.err(page, s.line, f"{s.where} cannot carry a label")
            prefix = _expected_prefix(page, kind)
            if prefix and not label.startswith(prefix):
                self.err(page, s.line, f"label {label}: examples, exercises and solutions start with their page's slug, {prefix}… (docs/plan/02 §2.4)")
            self._add(label, page, s.line, s.node)

    def _check_page(self, page: Page, doc: ms.Document):
        directives = doc.directives()
        for d in directives:
            if d.name in ms.LABEL_REQUIRED and not d.label:
                self.err(page, d.line, f"{{{d.name}}} needs a :label: (docs/plan/03 §3.4)")
        # Exercises and solutions.
        exercises = [d for d in directives if d.name == "exercise"]
        solutions = [d for d in directives if d.name == "solution"]
        by_target: dict[str, list] = {}
        for s in solutions:
            by_target.setdefault(s.arg, []).append(s)
            if s.arg not in {e.label for e in exercises if e.label}:
                self.err(page, s.line, f"{{solution}} {s.arg or '(no exercise label)'}: no such exercise on this page")
        for e in exercises:
            if not e.label:
                continue
            tiers = [c for c in e.classes if c in TIERS]
            if len(tiers) != 1:
                self.err(page, e.option_line("class"), f"exercise {e.label} needs exactly one tier class ({', '.join(TIERS)}) in :class: (docs/plan/07)")
            answers = [c for c in e.children if isinstance(c, ms.Directive) and c.name == "admonition" and "answer" in c.classes]
            if len(answers) != 1:
                self.err(page, e.line, f"exercise {e.label} needs exactly one Answer admonition (:class: dropdown answer), found {len(answers)}")
            sols = by_target.get(e.label, [])
            if len(sols) != 1:
                self.err(page, e.line, f"exercise {e.label} needs exactly one {{solution}} {e.label}, found {len(sols)}")
            for s in sols:
                want = "sol-" + e.label[len("exr-"):] if e.label.startswith("exr-") else None
                if s.line < e.end:
                    self.err(page, s.line, f"the solution of {e.label} comes before the exercise ends")
                if want and s.label and s.label != want:
                    self.err(page, s.option_line("label"), f"the solution of {e.label} is labelled {want}, not {s.label}")
        # Proofs.
        statements = {d.label: d for d in directives if d.name in ms.STATEMENTS and d.label}
        for d in directives:
            if d.name != "proof:proof":
                continue
            if d.label and d.label.startswith("prf-"):
                slug = d.label[len("prf-"):]
                target = next((statements[f"{k}-{slug}"] for k in ("thm", "lem", "cor", "prop") if f"{k}-{slug}" in statements), None)
                if target is None:
                    self.err(page, d.option_line("label"), f"proof {d.label} has no statement thm-/lem-/cor-/prop-{slug} on this page to prove")
                else:
                    self.proves[id(d)] = target
                continue
            prev = ms.previous_sibling(d, doc)
            if isinstance(prev, ms.Directive) and prev.name in ms.STATEMENTS:
                self.proves[id(d)] = prev
            else:
                self.err(page, d.line, "orphan proof: a {proof:proof} directly follows the statement it proves, or carries the label prf-<slug> of that statement (docs/plan/02 §2.5)")
        # Inline syntax and references.
        for node, inl in doc.inline_runs():
            for line, msg in inl.problems:
                self.err(page, line, msg)
            for line, label, _text in inl.refs:
                if label not in self.sites:
                    self.err(page, line, f"reference to unknown label #{label} (no page or block in the toc has it)")

    # ── labels.lock ──

    def _check_lock(self, update: bool):
        path = lock_path(self.project)
        entries = read_lock(path, self.rep)
        if entries is None:
            if not update:
                self.rep.error(path, 1, "labels.lock does not exist: create it with uv run python scripts/check_labels.py --update-lock")
                return
            entries = {}
        if update:
            for label, site in self.sites.items():
                e = entries.get(label)
                if e is None:
                    entries[label] = LockEntry(label, 0, page=site.page.rel)
                elif e.tombstone is None:
                    e.page = site.page.rel
            write_lock(path, entries)
            print(f"updated {display_path(path)} ({len(entries)} labels)", file=sys.stderr)
            entries = read_lock(path, self.rep)
        for label, site in self.sites.items():
            e = entries.get(label)
            if e is None:
                self.err(site.page, site.line, f"label {label} is not in labels.lock: run uv run python scripts/check_labels.py --update-lock (docs/plan/06 §6.7)")
            elif e.tombstone is not None:
                self.err(site.page, site.line, f"label {label} was removed (labels.lock:{e.line}: → {e.tombstone}); labels are never reused")
            elif e.page != site.page.rel:
                self.err(site.page, site.line, f"labels.lock records {label} on {e.page}; it is now on {site.page.rel}: run --update-lock")
        unparsed = {p.rel for p in self.project.pages if p.rel not in self.docs}
        for label, e in entries.items():
            if e.page in unparsed:
                continue  # its page has a parse error, reported above; don't bury it
            if e.tombstone is None and label not in self.sites:
                self.rep.error(path, e.line, f"label {label} (on {e.page}) is no longer in the content: restore it, or replace "
                                             f"this line with a tombstone `{label} → <replacement or reason>` (docs/plan/06 §6.7)")

    # ── forward references (02 §2.5) ──

    def _check_forward_refs(self):
        from graph import Graph

        graph = Graph(self.project)
        for page in self.project.pages:
            doc = self.docs.get(page.rel)
            if doc is None or page.kind == "meta" or not page.label:
                continue  # meta pages document the site; they cite freely
            severity = "error" if page.status == "verified" else "warning"
            closure = graph.closure(page.label)
            for node, inl in doc.inline_runs():
                ancestors = list(node.ancestors()) + ([node] if isinstance(node, ms.Directive) else [])
                if any(isinstance(a, ms.Directive) and (a.name == "seealso" or set(a.classes) & set(SEE_ALSO_CLASSES)) for a in ancestors):
                    continue
                proof = next((a for a in ancestors if isinstance(a, ms.Directive) and a.name == "proof:proof"), None)
                solution = next((a for a in ancestors if isinstance(a, ms.Directive) and a.name == "solution"), None)
                for line, label, _text in inl.refs:
                    site = self.sites.get(label)
                    if site is None:
                        continue  # reported above
                    target = site.page
                    if target.kind == "meta":
                        continue
                    if target is not page:
                        if target.label not in closure:
                            self.rep.report(severity, page.path, line,
                                            f"cites {label} on {target.rel}, which is not in the prerequisite closure of "
                                            f"{page.label}; cite it in a looking-ahead admonition, or add the prerequisite (docs/plan/02 §2.5)")
                        continue
                    if proof is not None:
                        stmt = self.proves.get(id(proof))
                        if stmt is not None and site.line >= stmt.line:
                            self.rep.report(severity, page.path, line,
                                            f"the proof of {stmt.label} cites {label}, which is not stated before {stmt.label} (docs/plan/02 §2.5)")
                    elif solution is not None and site.line >= line:
                        self.rep.report(severity, page.path, line,
                                        f"the solution {solution.label or solution.arg} cites {label}, which comes later on the page (docs/plan/02 §2.5)")


def check(project: Project, rep: Reporter, forward_refs: bool = False, update_lock: bool = False) -> LabelChecker:
    c = LabelChecker(project, rep)
    c.run(forward_refs=forward_refs, update_lock=update_lock)
    return c


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    ap.add_argument("--forward-refs", action="store_true", help="also check forward references (02 §2.5)")
    ap.add_argument("--update-lock", action="store_true", help="add new labels to labels.lock, then check")
    args = ap.parse_args(argv)
    rep = Reporter()
    check(Project(args.root), rep, forward_refs=args.forward_refs, update_lock=args.update_lock)
    print(f"check_labels.py: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)", file=sys.stderr)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
