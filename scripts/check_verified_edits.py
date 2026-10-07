"""The verified-page edit guard (docs/plan/06 §6.6, 05 §5.7): run by .github/workflows/guard.yml
on pull requests only.

    check_verified_edits.py --base <sha> [--head HEAD] [--labels '["typo-only"]'] [--root content]

It diffs `head` against `base` and, for every page that was `verified` at `base`, compares its
blocks: every labelled directive or equation, and every unlabelled proof (keyed by the statement
it follows). If a block changed, was added or was removed, the PR must also change that page's
`maths.verify` file (the verifier re-establishes the verified status), or lower the page's
status in the same diff. Otherwise it fails. A PR labelled `typo-only` passes; guard.yml re-runs
on label changes, so adding the label turns the check green without a new push.

Pages that are not verified at `base` are never checked here (the coverage gate in the
`verify` job decides whether a page may become verified).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

import myst_source as ms
from project import DEFAULT_ROOT, STATUS_RANK, Reporter, add_root_argument

TYPO_ONLY = "typo-only"


class GitError(Exception):
    pass


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def show(repo: Path, rev: str, path: str) -> str | None:
    try:
        return git(repo, "show", f"{rev}:{path}")
    except GitError:
        return None


def changed_files(repo: Path, base: str, head: str) -> list[tuple[str, str, str]]:
    """(status, old path, new path) for every file that differs, renames detected."""
    out = git(repo, "diff", "--name-status", "-M", "-z", base, head)
    fields = out.split("\0")
    changes, i = [], 0
    while i < len(fields) and fields[i]:
        status = fields[i]
        if status[0] in "RC":
            changes.append((status[0], fields[i + 1], fields[i + 2]))
            i += 3
        else:
            changes.append((status[0], fields[i + 1], fields[i + 1]))
            i += 2
    return changes


def front_matter(text: str) -> dict:
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return {}
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:i])) or {}
            except yaml.YAMLError:
                return {}
            return data if isinstance(data, dict) else {}
    return {}


def maths(text: str | None) -> dict:
    m = front_matter(text or "").get("maths")
    return m if isinstance(m, dict) else {}


def blocks(text: str) -> dict[str, tuple[int, str]]:
    """{key: (line, source text)} of the page's blocks. Raises ms.ParseError."""
    doc = ms.parse(text)
    lines = text.split("\n")
    out: dict[str, tuple[int, str]] = {}
    counts: dict[str, int] = {}
    for nd in doc.walk():
        key = None
        if isinstance(nd, ms.Directive):
            if nd.label:
                key = nd.label
            elif nd.name == "proof:proof":
                prev = ms.previous_sibling(nd, doc)
                if isinstance(prev, ms.Directive) and prev.label:
                    key = f"the proof of {prev.label}"
            if key is not None:
                out[key] = (nd.line, "\n".join(lines[nd.line - 1 : nd.end]))
        elif isinstance(nd, ms.DisplayMath) and nd.label:
            out[nd.label] = (nd.line, "\n".join(lines[nd.line - 1 : nd.end]))
        if key is None and isinstance(nd, ms.Directive) and nd.name == "proof:proof":
            n = counts[nd.name] = counts.get(nd.name, 0) + 1
            out[f"unlabelled proof #{n}"] = (nd.line, "\n".join(lines[nd.line - 1 : nd.end]))
    return out


def parse_labels(value: str) -> set[str]:
    value = (value or "").strip()
    if not value:
        return set()
    if value.startswith("["):
        return {str(v) for v in json.loads(value)}
    return {v.strip() for v in value.split(",") if v.strip()}


def check(repo: Path, root: Path, base: str, head: str, labels: set[str], rep: Reporter) -> list[str]:
    """Returns notes (pages that passed for a reason); errors go to rep."""
    notes: list[str] = []
    root_rel = root.resolve().relative_to(repo.resolve()).as_posix()
    try:
        changes = changed_files(repo, base, head)
    except GitError as e:
        rep.error(repo, 1, f"cannot diff against the base commit ({e}); the job needs the full history (fetch-depth: 0)")
        return notes
    changed = {p for _, old, new in changes for p in (old, new)}
    for status, old, new in changes:
        if not (old.startswith(root_rel + "/") and old.endswith(".md")):
            continue
        before = show(repo, base, old)
        if maths(before).get("status") != "verified":
            continue
        after = None if status == "D" else show(repo, head, new)
        where = repo / (new if after is not None else old)
        if after is None:
            notes.append(f"{old}: a verified page was removed (labels.lock keeps its labels honest)")
            continue
        m_after = maths(after)
        if m_after.get("status") not in STATUS_RANK:
            rep.error(where, 1, "this page was verified, and its maths.status can no longer be read; "
                                "lower it explicitly (status: reviewed) or restore it")
            continue
        if STATUS_RANK[m_after["status"]] < STATUS_RANK["verified"]:
            notes.append(f"{new}: verified → {m_after.get('status')}, lowered in this PR")
            continue
        try:
            old_blocks, new_blocks = blocks(before), blocks(after)
        except ms.ParseError as e:
            rep.error(where, e.line, f"cannot compare the blocks of this verified page: {e.message}")
            continue
        diffs = []
        for key in sorted(set(old_blocks) | set(new_blocks), key=lambda k: new_blocks.get(k, old_blocks.get(k))[0]):
            if key not in new_blocks:
                diffs.append((1, f"{key} was removed"))
            elif key not in old_blocks:
                diffs.append((new_blocks[key][0], f"{key} was added"))
            elif old_blocks[key][1] != new_blocks[key][1]:
                diffs.append((new_blocks[key][0], f"{key} changed"))
        if not diffs:
            continue
        verify_files = {v for v in (maths(before).get("verify"), m_after.get("verify")) if v}
        if verify_files & changed:
            notes.append(f"{new}: {len(diffs)} block(s) changed, and {', '.join(sorted(verify_files & changed))} changed too")
            continue
        if TYPO_ONLY in labels:
            notes.append(f"{new}: {len(diffs)} block(s) changed; passed because the PR is labelled {TYPO_ONLY}")
            continue
        test = " or ".join(sorted(verify_files)) or "its verification file"
        for line, what in diffs:
            rep.error(where, line, f"{what} on a verified page, but {test} did not change. Update the test (the "
                                   f"verifier re-establishes verified), or set maths.status to reviewed in this PR; "
                                   f"a typo-only fix can add the {TYPO_ONLY} label instead (docs/plan/06 §6.6)")
    return notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="the PR's base commit")
    ap.add_argument("--head", default="HEAD", help="default: HEAD")
    ap.add_argument("--labels", default="", help="the PR's labels: a JSON list (guard.yml) or comma-separated")
    add_root_argument(ap)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    repo = Path(git(root, "rev-parse", "--show-toplevel").strip()) if root.exists() else DEFAULT_ROOT.parent
    rep = Reporter()
    for note in check(repo, root, args.base, args.head, parse_labels(args.labels), rep):
        print(f"note: {note}")
    print(f"check_verified_edits.py: {len(rep.errors)} error(s)", file=sys.stderr)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
