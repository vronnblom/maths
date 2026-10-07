"""Front matter of every page in the toc (docs/plan/03 §3.3, 06 §6.4, 06 §6.6).

- validates against schema/page.schema.json (fields, label grammar per kind, required fields by
  kind and status);
- tags come from content/tags.yml; the label's subject prefix matches maths.subject; the kind
  matches the path (03 §3.1); a page in a subject folder has that folder's subject;
- status ≥ reviewed: the maths.verify file exists, and every prerequisite page exists and is at
  least reviewed (the prerequisite-status gate). The coverage-based preconditions are checked by
  check_coverage.py in the verify job (stage 4).
"""

from __future__ import annotations

import argparse
import json
import sys

import jsonschema

from project import REPO, STATUS_RANK, Page, Project, Reporter, add_root_argument

KIND_PATHS = {
    "meta": "content/index.md or content/about/<page>.md",
    "subject": "content/<subject>/index.md",
    "chapter": "content/<subject>/<chapter>/index.md",
    "topic": "content/<subject>/<chapter>/<topic>.md",
}


def _kind_of_path(rel: str) -> str:
    parts = rel.split("/")
    if rel == "index.md" or (parts[0] == "about" and len(parts) == 2):
        return "meta"
    if len(parts) == 2 and parts[1] == "index.md":
        return "subject"
    if len(parts) == 3:
        return "chapter" if parts[2] == "index.md" else "topic"
    return "?"


def _schema_message(e: jsonschema.ValidationError, page: Page) -> str:
    path = ".".join(str(p) for p in e.absolute_path)
    where = path or "front matter"
    if e.validator == "propertyNames":
        return f"maths.{e.instance}: not allowed on a {page.kind} page (docs/plan/03 §3.3)"
    if e.validator == "additionalProperties":
        return f"{where}: {e.message} (docs/plan/03 §3.3)"
    if e.validator == "pattern" and path.startswith("maths.objectives"):
        return f"{where}: an objective starts with an observable verb (state, compute, prove, …), never understand or know: {e.instance!r}"
    if e.validator == "pattern" and path == "label":
        return f"label {e.instance!r} does not fit the grammar for a {page.kind} page (docs/plan/02 §2.4)"
    if e.validator == "not" and path == "label":
        return f"label {e.instance!r} does not fit the grammar for a {page.kind} page (docs/plan/02 §2.4)"
    if e.validator == "minItems" and path == "maths.reviewed_by":
        return "maths.reviewed_by: a reviewed or verified page needs at least one reviewer"
    if e.validator == "required" and "verify" in e.message:
        return "maths.verify: a reviewed or verified page needs its verification test file"
    return f"{where}: {e.message}"


def check(project: Project, rep: Reporter) -> None:
    schema = json.loads((REPO / "schema" / "page.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    tags, tag_error = project.load_tags()
    if tag_error:
        rep.error(project.root / "tags.yml", 1, tag_error)

    for page in project.pages:
        if page.fm_error:
            rep.error(page.path, page.fm_error_line, page.fm_error)
            continue
        if page.fm is None:
            rep.error(page.path, 1, "no front matter (docs/plan/03 §3.3)")
            continue
        errors = sorted(validator.iter_errors(page.fm), key=lambda e: list(map(str, e.absolute_path)))
        seen = set()
        for e in errors:
            msg = _schema_message(e, page)
            if msg in seen:
                continue
            seen.add(msg)
            rep.error(page.path, page.line(*e.absolute_path), msg)
        if errors:
            continue  # the rules below assume a valid shape
        m = page.maths
        kind = m["kind"]

        expected = _kind_of_path(page.rel)
        if expected != kind:
            rep.error(page.path, page.line("maths", "kind"), f"a {kind} page lives at {KIND_PATHS[kind]}, not content/{page.rel}")
        if kind != "meta":
            if not page.label.startswith(m["subject"] + "-"):
                rep.error(page.path, page.line("label"), f"label {page.label} does not start with its subject, {m['subject']}-")
            cur = project.curriculum_for_folder(page.rel.split("/")[0])
            if cur is not None and cur.subject and cur.subject != m["subject"]:
                rep.error(page.path, page.line("maths", "subject"),
                          f"maths.subject is {m['subject']}, but content/{cur.folder}/ is subject {cur.subject}")

        if tags is not None:
            for k, t in enumerate(page.fm.get("tags") or []):
                if t not in tags:
                    rep.error(page.path, page.line("tags", k), f"tag {t!r} is not in content/tags.yml")

        status = m["status"]
        if STATUS_RANK[status] >= STATUS_RANK["reviewed"]:
            v = m.get("verify")
            if v and not (project.repo / v).is_file():
                rep.error(page.path, page.line("maths", "verify"), f"maths.verify: {v} does not exist")
            for k, p in enumerate(m.get("prerequisites") or []):
                pre = project.page_by_label.get(p)
                line = page.line("maths", "prerequisites", k)
                if pre is None:
                    rep.error(page.path, line, f"status {status} needs every prerequisite written and at least "
                                               f"reviewed: {p} has no page yet (docs/plan/06 §6.6)")
                elif STATUS_RANK[pre.status] < STATUS_RANK["reviewed"]:
                    rep.error(page.path, line, f"status {status} needs every prerequisite at least reviewed: "
                                               f"{p} is {pre.status} (docs/plan/06 §6.6)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    args = ap.parse_args(argv)
    rep = Reporter()
    check(Project(args.root), rep)
    print(f"check_frontmatter.py: {len(rep.errors)} error(s)", file=sys.stderr)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
