"""Scaffold a topic page from its curriculum entry: what `/new-topic <label>` runs
(.claude/skills/new-topic/SKILL.md; CLAUDE.md, "How to add a topic").

    new_topic.py <label>            write the page, its verify file and the toc entry, then
                                    run check_labels.py --update-lock
    new_topic.py --stubs <label>    add a @covers stub to the page's verify file for every eg-/exr-
                                    label on the page that the file doesn't declare yet

The page comes from the curriculum entry and the section order of templates/topic.md: the front
matter (title, label, level, prerequisites, objectives, the entry's widgets that are built), and
a statement for every result in `results`, with the proof blocks its policy asks for (F, R, S,
D, or a combination such as S+R; docs/plan/08 §8.2). Everything the author still has to write
is marked `TODO`. The verify file has one `pytest.skip("for the verifier")` stub per eg-/exr-
label (stubs count as uncovered); the author never writes expected values.

It refuses a label that is in no curriculum.yml, and a topic whose page, verify file or toc entry
already exists. A topic whose prerequisites are not all reviewed yet is scaffolded with a note:
drafting ahead is allowed (docs/plan/10 §10.4).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

import graph
import myst_source as ms
from check_frontmatter import _verify_path
from project import STATUS_RANK, Curriculum, PlannedTopic, Project, add_root_argument, display_path

STATEMENT_DIRECTIVE = {"thm": "theorem", "lem": "lemma", "cor": "corollary", "prop": "proposition"}
OTHER_DIRECTIVE = {"def": "definition", "ax": "axiom", "rem": "remark", "eg": "example"}


class Refusal(Exception):
    pass


# ── YAML scalars that round-trip ─────────────────────────────────────────────


def scalar(s: str) -> str:
    """`s` as a YAML scalar: plain if that reads back unchanged, else single-quoted."""
    for candidate in (s, "'" + s.replace("'", "''") + "'"):
        try:
            if yaml.safe_load(f"k: {candidate}") == {"k": s}:
                return candidate
        except yaml.YAMLError:
            pass
    raise ValueError(f"cannot write {s!r} as a YAML scalar")


def flow_list(items: list[str]) -> str:
    return "[" + ", ".join(scalar(i) for i in items) + "]"


# ── The page ─────────────────────────────────────────────────────────────────


def _slug(label: str) -> str:
    return label.split("-", 1)[1]


def _comment(text: str) -> list[str]:
    return [f"% {line}" if line else "%" for line in text.split("\n")]


def _result_blocks(r: dict, topic: PlannedTopic) -> list[str]:
    label, policy, note = r["label"], r.get("policy") or "", r.get("note")
    kind = label.split("-")[0]
    parts = [p for p in policy.split("+") if p]
    name = STATEMENT_DIRECTIVE.get(kind) or OTHER_DIRECTIVE.get(kind) or "remark"
    out = [f":::{{proof:{name}}}", f":label: {label}"]
    out += _comment(f"TODO: the title (after the directive name) and the {name}." + (f"\nCurriculum note: {note}" if note else ""))
    out += [":::", ""]
    if kind not in STATEMENT_DIRECTIVE:
        if parts:  # a definition, axiom, remark or example with a policy: no proof block
            out += _comment(f"TODO (policy {policy}): {_policy_hint(parts, r)}") + [""]
        return out
    # The first proof directly follows the statement (unlabelled); a rigorous-track proof that
    # is not first carries prf-<slug>, which pairs it with the statement (check_labels.py).
    proof_parts = [p for p in parts if p in "FRS"]
    for i, p in enumerate(proof_parts):
        labelled = i > 0
        if labelled and p != "R":
            out += _comment(f"TODO (policy {policy}, part {p}): {_policy_hint([p], r)}. Fold it into a proof "
                            f"above or a remark: only one proof can carry prf-{_slug(label)}.") + [""]
            continue
        title = {"F": "", "R": " Rigorous track", "S": " Sketch"}[p]
        out.append(f":::{{proof:proof}}{title}")
        if labelled:
            out.append(f":label: prf-{_slug(label)}")
        out.append(":enumerated: false")
        if p == "R":
            out.append(":class: dropdown")
        out += _comment(f"TODO (policy {p}): {_policy_hint([p], r)}")
        out += [":::", ""]
    if "D" in parts:
        out += _comment(f"TODO (policy D): {_policy_hint(['D'], r)}") + [""]
    return out


def _policy_hint(parts: list[str], r: dict) -> str:
    hints = {
        "F": "the full proof in the core, strategy sentence first",
        "R": "the full proof in the rigorous track (a dropdown), strategy sentence first",
        "S": "a sketch that says what it leaves out",
        "D": f"deferred to {r.get('deferred_to')}: say where the proof is (a link to a later page only "
             f"inside a looking-ahead admonition, templates/blocks.md)",
    }
    return "; ".join(hints[p] for p in parts if p in hints)


def page_text(project: Project, topic: PlannedTopic) -> str:
    d = topic.data
    subject = topic.curriculum.subject
    tags_known, _ = project.load_tags()
    tags = [topic.chapter] if tags_known and topic.chapter in tags_known else []
    widgets_planned = list(d.get("widgets") or [])
    built = [w for w in widgets_planned if (project.repo / "widgets" / f"{w}.mjs").is_file()]
    unbuilt = [w for w in widgets_planned if w not in built]
    results = [r for r in (d.get("results") or []) if isinstance(r, dict) and isinstance(r.get("label"), str)]

    fm = [
        "---",
        f"title: {scalar(topic.title)}",
        f"label: {topic.label}",
        "description: >-",
        "  TODO: one or two sentences on what the reader learns. No math: it is not rendered here.",
        f"tags: {flow_list(tags)}                # TODO: from content/tags.yml",
        "maths:",
        "  kind: topic",
        f"  subject: {subject}",
        "  status: draft",
        f"  level: {topic.level}",
        "  difficulty: 2                  # TODO: 1–5",
        "  est_minutes: 30                # TODO: reading time",
        f"  prerequisites: {flow_list(topic.prerequisites)}",
        "  objectives:",
        *[f"    - {scalar(o)}" for o in d.get("objectives") or []],
        f"  verify: {_verify_path(topic.file)}",
        f"  widgets: {flow_list(built)}" + (f"                # not built yet: {', '.join(unbuilt)}" if unbuilt else ""),
        "  reviewed_by: []",
        "  sources: []",
        "---",
        "",
    ]
    body = [
        ":::{topic-header}",
        ":::",
        "",
        "## Why this matters",
        "",
        *_comment("TODO: 1–3 paragraphs that start from a concrete question, not a definition."),
    ]
    if widgets_planned:
        body += _comment(f"TODO: the widgets planned for this topic: {', '.join(widgets_planned)}. Each sits alone in a\n"
                         "{figure} labelled wdg-…, whose caption is its text description, then **Try this:**\n"
                         "(templates/topic.md, widgets/README.md).")
    for note in d.get("notes") or []:
        body += _comment(f"Curriculum note: {note}")
    body.append("")

    defs = [r for r in results if r["label"].split("-")[0] in ("def", "ax")]
    stmts = [r for r in results if r["label"].split("-")[0] in (*STATEMENT_DIRECTIVE, "rem")]
    egs = [r for r in results if r["label"].split("-")[0] == "eg"]
    rigorous_egs = [r for r in egs if "R" in (r.get("policy") or "").split("+")]
    core_egs = [r for r in egs if r not in rigorous_egs]

    body += ["## TODO: the heading of the definitions section", ""]
    body += _comment("TODO: the intuition first, then each definition with an \"in words\" unpacking, an example\n"
                     "and a non-example (templates/blocks.md).") + [""]
    for r in defs:
        body += _result_blocks(r, topic)
    if stmts:
        body += ["## Main results", ""]
        for r in stmts:
            body += _result_blocks(r, topic)
    body += ["## Worked examples", ""]
    body += _comment("TODO: at least 3 worked examples (the typical, an edge case, an applied one), each ending\n"
                     "with a **Check**. Labels eg-<topic slug>-<name>.") + [""]
    for r in core_egs:
        body += _result_blocks(r, topic)
    body += ["## Common mistakes", ""]
    body += _comment("TODO: at least one {warning} drawn from real student errors (templates/blocks.md).") + [""]
    body += ["## Rigorous track", ""]
    body += _comment("TODO: the rigorous asides ({admonition} with :class: dropdown rigor), or delete this note.") + [""]
    for r in rigorous_egs:
        body += _result_blocks(r, topic)
    body += ["## Summary", ""]
    body += _comment("TODO: 3–6 bullet points.") + [""]
    body += ["## Exercises", ""]
    body += _comment("TODO: 6–15 exercises across tiers A/B/C, each with hints, one Answer and a {solution}\n"
                     "(templates/topic.md). Labels exr-<topic slug>-<name>. Then run\n"
                     f"  uv run python scripts/new_topic.py --stubs {topic.label}") + [""]
    body += ["## Where this leads", "", ":::{where-this-leads}", ":::", ""]
    return "\n".join(fm + body)


# ── The verify file ──────────────────────────────────────────────────────────

COVERS = re.compile(r"@covers\(([^)]*)\)")


def stub(label: str) -> str:
    name = label.replace("-", "_")  # eg_calc_… and exr_calc_…: unique, so no test shadows another
    return f'\n\n@covers("{label}")\ndef test_{name}():\n    pytest.skip("for the verifier")\n'


def verify_text(topic: PlannedTopic, labels: list[str]) -> str:
    head = f'''"""Verification tests for content/{topic.file} ({topic.label}).

Rules: docs/plan/06-quality-assurance.md §6.1 and templates/verify_test.py. The author leaves one
`pytest.skip("for the verifier")` stub per eg-/exr- label (stubs count as uncovered); the
verifier (/verify-topic) replaces them with tests whose expected values are derived
independently, reading answers with answer(label).
"""

import pytest
import sympy as sp  # noqa: F401  (for the verifier)

from mathcheck import answer, covers, equal, x  # noqa: F401
'''
    return head + "".join(stub(label) for label in labels)


def page_labels(path: Path) -> list[str]:
    doc = ms.parse(path.read_text(encoding="utf-8"))
    return [d.label for d in doc.directives()
            if d.label and ((d.name == "proof:example" and d.label.startswith("eg-"))
                            or (d.name == "exercise" and d.label.startswith("exr-")))]


def declared(text: str) -> set[str]:
    out = set()
    for m in COVERS.finditer(text):
        out.update(re.findall(r"""["']([a-z0-9-]+)["']""", m.group(1)))
    return out


# ── The toc ──────────────────────────────────────────────────────────────────


def _mapping_get(node, key):
    for k, v in node.value:
        if k.value == key:
            return k, v
    return None, None


def _end_line(node, lines: list[str]) -> int:
    """The 0-based index of the line after `node` (block style)."""
    end = node.end_mark  # where the next token starts, which may be indented on a later line
    if end.line >= len(lines) or not lines[end.line][: end.column].strip():
        return end.line
    return end.line + 1


def add_to_toc(project: Project, topic: PlannedTopic) -> None:
    """Insert the page into the toc, under its subject page and chapter, in curriculum order.
    The chapter gets a `title:` group until its chapter index page exists."""
    cur: Curriculum = topic.curriculum
    path = project.myst_path
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    root = yaml.compose(text)
    _, proj = _mapping_get(root, "project")
    _, toc = _mapping_get(proj, "toc")
    subject_file = f"{cur.folder}/index.md"

    def file_of(entry):
        _, f = _mapping_get(entry, "file")
        return f.value if f is not None else None

    subject = next((e for e in toc.value if file_of(e) == subject_file), None)
    if subject is None:
        raise Refusal(f"the toc has no entry for the subject page {subject_file}")
    order = [label for _slug, _t, labels, _l in cur.chapters for label in labels]
    files = {cur.topics[label].file: i for i, label in enumerate(order)}
    chapter_slugs = [c[0] for c in cur.chapters]
    chapter_title = next(t for s, t, _labels, _l in cur.chapters if s == topic.chapter)
    k = " " * subject.start_mark.column  # the column of the subject entry's keys

    def chapter_of(entry):
        f = file_of(entry)
        if f and f.startswith(f"{cur.folder}/"):
            return f.split("/")[1]
        _, t = _mapping_get(entry, "title")
        return next((s for s, ti, _labels, _l in cur.chapters if t is not None and ti == t.value), None)

    # In a block sequence of mappings, an item's keys sit two columns right of its dash.
    _, children = _mapping_get(subject, "children")
    if children is None:
        at = _end_line(subject, lines)
        new = [f"{k}children:", f"{k}  - title: {scalar(chapter_title)}", f"{k}    children:",
               f"{k}      - file: {topic.file}"]
    else:
        chapter = next((c for c in children.value if chapter_of(c) == topic.chapter), None)
        c = " " * children.value[0].start_mark.column
        if chapter is None:
            later = [e for e in children.value if chapter_of(e) in chapter_slugs
                     and chapter_slugs.index(chapter_of(e)) > chapter_slugs.index(topic.chapter)]
            at = later[0].start_mark.line if later else _end_line(children, lines)
            new = [f"{c[2:]}- title: {scalar(chapter_title)}", f"{c}children:", f"{c}  - file: {topic.file}"]
        else:
            _, topics = _mapping_get(chapter, "children")
            if topics is None:
                at = _end_line(chapter, lines)
                new = [f"{c}children:", f"{c}  - file: {topic.file}"]
            else:
                t = " " * topics.value[0].start_mark.column
                later = [e for e in topics.value if files.get(file_of(e), -1) > files[topic.file]]
                at = later[0].start_mark.line if later else _end_line(topics, lines)
                new = [f"{t[2:]}- file: {topic.file}"]
    lines[at:at] = new
    out = "\n".join(lines)
    try:
        ok = topic.file in [e.file for e in _flatten(yaml.safe_load(out)["project"]["toc"])]
    except (yaml.YAMLError, KeyError, TypeError):
        ok = False
    if not ok:
        raise Refusal(f"could not insert {topic.file} into the toc of {display_path(path)}: add it by hand")
    path.write_text(out, encoding="utf-8")


def _flatten(items):
    for item in items or []:
        yield argparse.Namespace(file=item.get("file"))
        yield from _flatten(item.get("children"))


# ── Main ─────────────────────────────────────────────────────────────────────


def find_topic(project: Project, label: str) -> PlannedTopic:
    topic = project.planned.get(label)
    if topic is None:
        raise Refusal(f"{label} is not a topic in any curriculum.yml. Pick one from "
                      f"`uv run python scripts/graph.py ready <subject>`, or add it to the curriculum first, "
                      f"in its own curriculum PR (CLAUDE.md, How to add a topic, step 2).")
    return topic


def scaffold(project: Project, label: str) -> list[Path]:
    topic = find_topic(project, label)
    page = project.root / topic.file
    verify = project.repo / _verify_path(topic.file)
    if page.exists():
        raise Refusal(f"{display_path(page)} already exists: {label} is being (or has been) written. "
                      f"Continue on its branch instead of scaffolding it again.")
    if verify.exists():
        raise Refusal(f"{display_path(verify)} already exists, but the page doesn't: remove the stray file first.")
    if any(e.file == topic.file for e in project.toc):
        raise Refusal(f"{topic.file} is already in the toc of {display_path(project.myst_path)}, but the page doesn't exist.")
    results = [r for r in (topic.data.get("results") or []) if isinstance(r, dict) and isinstance(r.get("label"), str)]
    page_src = page_text(project, topic)
    verify_src = verify_text(topic, [r["label"] for r in results if r["label"].startswith("eg-")])
    add_to_toc(project, topic)  # first: it refuses before anything is written
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(page_src, encoding="utf-8")
    verify.parent.mkdir(parents=True, exist_ok=True)
    verify.write_text(verify_src, encoding="utf-8")
    return [page, verify, project.myst_path]


def add_stubs(project: Project, label: str) -> list[str]:
    topic = find_topic(project, label)
    page = project.root / topic.file
    verify = project.repo / _verify_path(topic.file)
    if not page.is_file() or not verify.is_file():
        raise Refusal(f"scaffold {label} first: {display_path(page)} or {display_path(verify)} is missing")
    text = verify.read_text(encoding="utf-8")
    missing = [lab for lab in page_labels(page) if lab not in declared(text)]
    if missing:
        verify.write_text(text.rstrip("\n") + "\n" + "".join(stub(lab) for lab in missing), encoding="utf-8")
    return missing


def not_ready(project: Project, topic: PlannedTopic) -> list[str]:
    g = graph.Graph(project)
    out = []
    for p in topic.prerequisites:
        node = g.nodes.get(p)
        if node is None or not node.written or STATUS_RANK[node.status] < STATUS_RANK["reviewed"]:
            out.append(p)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    ap.add_argument("--stubs", action="store_true", help="add the missing @covers stubs to the verify file")
    ap.add_argument("label")
    args = ap.parse_args(argv)
    project = Project(args.root)
    try:
        if args.stubs:
            missing = add_stubs(project, args.label)
            print(f"added {len(missing)} stub(s): {', '.join(missing)}" if missing else "every eg-/exr- label already has a test")
            return 0
        written = scaffold(project, args.label)
    except Refusal as e:
        print(f"new_topic.py: refused: {e}", file=sys.stderr)
        return 2
    for p in written:
        print(f"wrote {display_path(p)}")
    waiting = not_ready(project, project.planned[args.label])
    if waiting:
        print(f"note: {args.label} is not ready ({', '.join(waiting)} not yet reviewed). Drafting ahead is fine, "
              f"but the page can't become reviewed before they are (docs/plan/10 §10.4).")
    lock = subprocess.run([sys.executable, str(Path(__file__).with_name("check_labels.py")), "--update-lock",
                           "--root", str(project.root)])
    return lock.returncode


if __name__ == "__main__":
    sys.exit(main())
