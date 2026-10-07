"""The prerequisite graph (docs/plan/02 §2.5).

    graph.py check                 validate curricula and front matter edges: everything resolves,
                                   no cycles, cross-subject edges respect depends_on, written pages
                                   agree with curriculum.yml; redundant transitive edges are warnings
    graph.py mermaid <subj>        write content/<subject>/_generated/prereq-map.md (-o - for stdout)
    graph.py ready <subj>          planned topics whose prerequisites are all written and ≥ reviewed
    graph.py closure <label>       every transitive prerequisite of a page or planned topic

Nodes are topic pages: a written page (front matter is the truth) or a planned topic from a
curriculum.yml. Chapter and subject index pages are nodes too. Their closure also contains every
topic of the chapter (subject), because they are read after them (02 §2.5).
"""

from __future__ import annotations

import argparse
import graphlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import jsonschema

from project import REPO, STATUS_RANK, SUBJECTS, Page, Project, Reporter, add_root_argument

LABEL_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESULT_KINDS = ("def", "thm", "lem", "cor", "prop", "ax", "eg", "rem")
POLICY_REQUIRED = ("thm", "lem", "cor", "prop")


@dataclass
class GNode:
    label: str
    kind: str  # topic | chapter | subject
    subject: str | None
    page: Page | None = None
    planned: object = None  # PlannedTopic
    prereqs: list = field(default_factory=list)  # declared (direct) prerequisites
    implicit: list = field(default_factory=list)  # chapter/subject index → its topics/chapters

    @property
    def written(self) -> bool:
        return self.page is not None

    @property
    def status(self) -> str | None:
        return self.page.status if self.page else None

    @property
    def title(self) -> str:
        if self.page and self.page.title:
            return self.page.title
        return self.planned.title if self.planned else self.label

    def source(self):
        """(path, line) where the prerequisites are declared."""
        if self.page:
            return self.page.path, self.page.line("maths", "prerequisites")
        return self.planned.curriculum.path, self.planned.line


class Graph:
    def __init__(self, project: Project):
        self.project = project
        self.nodes: dict[str, GNode] = {}
        for label, t in project.planned.items():
            self.nodes[label] = GNode(label, "topic", t.curriculum.subject, planned=t, prereqs=list(t.prerequisites))
        for page in project.pages:
            if page.kind not in ("topic", "chapter", "subject") or not page.label:
                continue
            node = self.nodes.get(page.label)
            if node is not None and node.page is not None:
                continue  # a duplicate label: check_labels.py reports it
            if node is None:
                node = self.nodes[page.label] = GNode(page.label, page.kind, page.subject)
            node.page, node.kind, node.subject = page, page.kind, page.subject
            node.prereqs = list(page.prerequisites)
        # Chapter and subject index pages: their topics (and chapters) count as read before them.
        for cur in project.curricula:
            subj = cur.subject
            chapter_labels = []
            for slug, _title, topics, _line in cur.chapters:
                ch_label = f"{subj}-{slug}-chapter"
                chapter_labels.append(ch_label)
                if ch_label in self.nodes:
                    self.nodes[ch_label].implicit = list(topics)
            sl = f"{subj}-subject"
            if sl in self.nodes:
                self.nodes[sl].implicit = [c for c in chapter_labels if c in self.nodes] + list(cur.topics)
        self._closure: dict[str, frozenset] = {}

    def edges(self, label) -> list[str]:
        n = self.nodes.get(label)
        if n is None:
            return []
        return [p for p in n.prereqs + n.implicit if p in self.nodes]

    def closure(self, label: str) -> frozenset:
        """All transitive prerequisites (plus, for index pages, their topics); not the node itself."""
        if label in self._closure:
            return self._closure[label]
        seen: set[str] = set()
        stack = list(self.edges(label))
        while stack:
            x = stack.pop()
            if x in seen or x == label:
                continue
            seen.add(x)
            stack.extend(self.edges(x))
        self._closure[label] = frozenset(seen)
        return self._closure[label]


# ── check ────────────────────────────────────────────────────────────────────


def _load_schema():
    return json.loads((REPO / "schema" / "curriculum.schema.json").read_text(encoding="utf-8"))


def check(project: Project, rep: Reporter) -> Graph:
    validator = jsonschema.Draft202012Validator(_load_schema())
    known_results: dict[str, tuple] = {}
    known_topics: dict[str, tuple] = {}
    for cur in project.curricula:
        if cur.error:
            rep.error(cur.path, 1, cur.error)
            continue
        for e in sorted(validator.iter_errors(cur.data), key=lambda e: list(map(str, e.absolute_path))):
            where = ".".join(str(p) for p in e.absolute_path) or "curriculum"
            rep.error(cur.path, cur.line(*e.absolute_path), f"{where}: {e.message}")
        subj = cur.subject
        if subj not in SUBJECTS:
            continue
        files: dict[str, int] = {}
        for ci, ch in enumerate(cur.data.get("chapters") or []):
            for ti, t in enumerate(ch.get("topics") or []):
                if not isinstance(t, dict):
                    continue
                path = ("chapters", ci, "topics", ti)
                label, line = t.get("label"), cur.line(*path)
                if not isinstance(label, str):
                    continue
                if label in known_topics:
                    rep.error(cur.path, line, f"topic {label} is listed twice (first at line {known_topics[label][1]})")
                known_topics.setdefault(label, (cur.path, line))
                if not label.startswith(f"{subj}-") or label.endswith(("-chapter", "-subject")):
                    rep.error(cur.path, line, f"topic label {label} must be {subj}-<topic-slug> (docs/plan/02 §2.4)")
                f = t.get("file")
                if isinstance(f, str):
                    if f in files:
                        rep.error(cur.path, line, f"file {f} is used by two topics")
                    files[f] = line
                    if f.split("/")[0] != ch.get("slug"):
                        rep.error(cur.path, cur.line(*path, "file"), f"file {f} is not in the chapter folder {ch.get('slug')}/")
                for ri, r in enumerate(t.get("results") or []):
                    if not isinstance(r, dict) or not isinstance(r.get("label"), str):
                        continue
                    rl, rline = r["label"], cur.line(*path, "results", ri)
                    kind = rl.split("-")[0]
                    if rl in known_results:
                        rep.error(cur.path, rline, f"result {rl} is listed twice (first at line {known_results[rl][1]})")
                    known_results.setdefault(rl, (cur.path, rline))
                    if kind in RESULT_KINDS and not rl.startswith(f"{kind}-{subj}-"):
                        rep.error(cur.path, rline, f"result label {rl} must be {kind}-{subj}-<slug>")
                    pol = r.get("policy") or ""
                    if kind in POLICY_REQUIRED and not pol:
                        rep.error(cur.path, rline, f"{rl} needs a proof policy (F, R, S or D; docs/plan/08 §8.2)")
                    if "D" in pol.split("+") and not r.get("deferred_to"):
                        rep.error(cur.path, rline, f"{rl} has policy D but no deferred_to")
                    if r.get("deferred_to") and "D" not in pol.split("+"):
                        rep.error(cur.path, rline, f"{rl} has deferred_to but no D in its policy")

    graph = Graph(project)

    # deferred_to targets: a later topic, another subject, or out-of-scope.
    for cur in project.curricula:
        for t in cur.topics.values():
            for ri, r in enumerate(t.data.get("results") or []):
                if not isinstance(r, dict) or not r.get("deferred_to"):
                    continue
                tgt = r["deferred_to"]
                line = cur.line(*_topic_path(cur, t.label), "results", ri)
                if tgt == "out-of-scope" or (tgt in SUBJECTS and tgt != cur.subject):
                    continue
                if tgt not in project.planned:
                    rep.error(cur.path, line, f"{r['label']} is deferred to {tgt}, which is neither a planned "
                                              f"topic, another subject's code, nor out-of-scope")
                elif tgt == t.label or tgt in graph.closure(t.label):
                    rep.error(cur.path, line, f"{r['label']} is deferred to {tgt}, which comes before {t.label} "
                                              f"(it is in its prerequisite closure)")

    # Every declared prerequisite resolves to a topic, written or planned.
    for node in graph.nodes.values():
        path, line = node.source()
        for p in node.prereqs:
            target = graph.nodes.get(p)
            if target is None:
                rep.error(path, line, f"{node.label}: unknown prerequisite {p} (not a page and not in any curriculum.yml)")
            elif target.kind != "topic":
                rep.error(path, line, f"{node.label}: prerequisite {p} is a {target.kind} page; list topics")
            elif p == node.label:
                rep.error(path, line, f"{node.label} lists itself as a prerequisite")

    # Cycles.
    ts = graphlib.TopologicalSorter({label: set(graph.edges(label)) for label in graph.nodes})
    try:
        ts.prepare()
    except graphlib.CycleError as e:
        cycle = e.args[1]
        first = graph.nodes[cycle[0]]
        path, line = first.source()
        rep.error(path, line, "prerequisite cycle: " + " → ".join(cycle) + " (each is a prerequisite of the next)")

    # Redundant transitive edges (only direct prerequisites are listed, 02 §2.5).
    else:
        for node in graph.nodes.values():
            for p in node.prereqs:
                via = [q for q in node.prereqs if q != p and p in graph.closure(q)]
                if via:
                    path, line = node.source()
                    rep.warning(path, line, f"{node.label}: prerequisite {p} is already implied by {via[0]}; list direct prerequisites only")

    # Cross-subject edges need depends_on on the subject page.
    for node in graph.nodes.values():
        for p in node.prereqs:
            target = graph.nodes.get(p)
            if target is None or not node.subject or not target.subject or target.subject == node.subject:
                continue
            path, line = node.source()
            sp = project.subject_page(node.subject)
            deps = (sp.maths.get("depends_on") or []) if sp else []
            if target.subject not in deps:
                rep.error(path, line, f"{node.label}: prerequisite {p} is in subject {target.subject}, which "
                                      f"{node.subject}-subject does not list in maths.depends_on")

    _check_agreement(project, graph, rep)
    return graph


def _topic_path(cur, label):
    for ci, ch in enumerate(cur.data.get("chapters") or []):
        for ti, t in enumerate(ch.get("topics") or []):
            if isinstance(t, dict) and t.get("label") == label:
                return ("chapters", ci, "topics", ti)
    return ()


def _check_agreement(project: Project, graph: Graph, rep: Reporter):
    """A written page must agree with its curriculum entry (02 §2.5)."""
    by_file = {t.file: t for t in project.planned.values()}
    for page in project.pages:
        if page.fm is None or not page.label:
            continue
        folder = page.rel.split("/")[0]
        cur = project.curriculum_for_folder(folder)
        if page.kind == "chapter" and cur is not None:
            slug = page.rel.split("/")[1] if page.rel.count("/") == 2 else None
            slugs = [c[0] for c in cur.chapters]
            if slug not in slugs:
                rep.error(page.path, page.line("label"), f"chapter folder {slug}/ is not a chapter of {cur.path.name}")
            elif page.label != f"{cur.subject}-{slug}-chapter":
                rep.error(page.path, page.line("label"), f"a chapter index has the label {cur.subject}-{slug}-chapter, not {page.label}")
        if page.kind != "topic":
            continue
        planned = project.planned.get(page.label)
        at_file = by_file.get(page.rel)
        if planned is None:
            if cur is not None:
                rep.error(page.path, page.line("label"), f"topic {page.label} is not in {display(cur.path)}; "
                                                         f"add it to the curriculum (its own PR) before writing the page")
            if at_file is not None:
                rep.error(page.path, page.line("label"), f"the curriculum puts {at_file.label} at this path, not {page.label}")
            continue
        where = f"{display(planned.curriculum.path)}:{planned.line}"
        if planned.file != page.rel:
            rep.error(page.path, page.line("label"), f"{page.label} is planned at {planned.file} ({where}), not here")
        if page.title != planned.title:
            rep.error(page.path, page.line("title"), f"title {page.title!r} differs from the curriculum's {planned.title!r} ({where})")
        level = page.maths.get("level")
        if level and level != planned.level:
            rep.error(page.path, page.line("maths", "level"), f"level {level} differs from the curriculum's {planned.level} ({where})")
        if set(page.prerequisites) != set(planned.prerequisites):
            missing = sorted(set(planned.prerequisites) - set(page.prerequisites))
            extra = sorted(set(page.prerequisites) - set(planned.prerequisites))
            parts = ([f"missing {', '.join(missing)}"] if missing else []) + ([f"extra {', '.join(extra)}"] if extra else [])
            rep.error(page.path, page.line("maths", "prerequisites"),
                      f"prerequisites differ from the curriculum ({where}): {'; '.join(parts)}")


def display(path):
    from project import display_path
    return display_path(path)


# ── mermaid, ready, closure ──────────────────────────────────────────────────


def _mid(label: str) -> str:
    return label.replace("-", "_")


def _mtext(s: str) -> str:
    return s.replace('"', "#quot;")


CLASSES = [
    "  classDef planned fill:#f6f8fa,stroke:#8c959f,stroke-dasharray:4 3,color:#57606a",
    "  classDef draft fill:#fff8c5,stroke:#9a6700,color:#3b2300",
    "  classDef reviewed fill:#ddf4ff,stroke:#0b5cad,color:#0a3069",
    "  classDef verified fill:#dafbe1,stroke:#1a7f37,color:#0f3d1e",
    "  classDef outside fill:#ffffff,stroke:#8c959f,color:#57606a",
]


def _reduce(edges: set) -> set:
    """Transitive reduction of a DAG given as {(a, b)}: drop a → c when a → … → c otherwise."""
    succ: dict = {}
    for a, b in edges:
        succ.setdefault(a, set()).add(b)

    def reach(a, skip):
        seen, stack = set(), [x for x in succ.get(a, ()) if (a, x) != skip]
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack.extend(succ.get(x, ()))
        return seen

    return {(a, b) for a, b in edges if b not in reach(a, (a, b))}


def mermaid(project: Project, subject: str, base_url: str | None = None) -> str:
    """The prerequisite map of a subject as a MyST fragment: an overview of the chapters, then one
    {mermaid} flowchart per chapter (one diagram of every topic is too wide to read)."""
    cur = project.curriculum_for_subject(subject)
    if cur is None:
        raise SystemExit(f"no curriculum.yml for subject {subject!r}")
    graph = Graph(project)
    base = (os.environ.get("BASE_URL", "") if base_url is None else base_url).rstrip("/")
    chapter_of = {}
    number = {}
    for k, (slug, title, topics, _line) in enumerate(cur.chapters, start=1):
        number[slug] = k
        for t in topics:
            chapter_of[t] = slug

    def node_line(label, indent="  "):
        node = graph.nodes[label]
        ext = " (extension)" if node.planned is not None and node.planned.level == "extension" else ""
        return f'{indent}{_mid(label)}["{_mtext(node.title + ext)}"]'

    def style_lines(labels):
        out = []
        for label in labels:
            node = graph.nodes[label]
            if node.written:
                out.append(f'  click {_mid(label)} "{base}{node.page.url}"')
                out.append(f"  class {_mid(label)} {node.status}")
            else:
                out.append(f"  class {_mid(label)} planned")
        return out

    n_total = len(chapter_of)
    n_written = sum(graph.nodes[t].written for t in chapter_of)
    out = [
        "% Generated by scripts/generate.py (graph.py mermaid) from curriculum.yml and the pages'",
        "% front matter. Do not edit; it is rewritten before every build.",
        "",
        f"Arrows point from a topic to the topics that build on it. Dashed boxes are planned topics "
        f"that have not been written yet ({n_total - n_written} of {n_total}); a written topic is "
        f"coloured by its status and links to its page.",
        "",
        "**The chapters.** An arrow means that the later chapter builds on the earlier one (an arrow "
        "that a longer path already implies is left out).",
        "",
        "```{mermaid}",
        "flowchart TB",
    ]
    ch_edges = set()
    for t, slug in chapter_of.items():
        for p in graph.nodes[t].prereqs:
            ps = chapter_of.get(p)
            if ps and ps != slug:
                ch_edges.add((ps, slug))
    for slug, title, _topics, _line in cur.chapters:
        out.append(f'  chapter_{_mid(slug)}["{number[slug]}. {_mtext(title)}"]')
    for a, b in sorted(_reduce(ch_edges), key=lambda e: (number[e[0]], number[e[1]])):
        out.append(f"  chapter_{_mid(a)} --> chapter_{_mid(b)}")
    out += ["```", ""]

    for slug, title, topics, _line in cur.chapters:
        k = number[slug]
        outside = []
        edges = []
        for t in topics:
            for p in graph.nodes[t].prereqs:
                if p not in graph.nodes:
                    continue
                if chapter_of.get(p) != slug and p not in outside:
                    outside.append(p)
                edges.append(f"  {_mid(p)} --> {_mid(t)}")
        out += [f"**{k}. {title}.**" + (" Rounded boxes are prerequisites from other chapters." if outside else ""), "",
                "```{mermaid}", "flowchart TB"] + CLASSES
        for p in outside:
            pn = graph.nodes[p]
            where = f"{number[chapter_of[p]]}. " if p in chapter_of else f"{pn.subject}: "
            out.append(f'  {_mid(p)}(["{_mtext(where + pn.title)}"])')
            out.append(f"  class {_mid(p)} outside")
        out += [node_line(t) for t in topics] + edges + style_lines(topics) + ["```", ""]
    return "\n".join(out)


def ready(project: Project, subject: str) -> list[tuple[str, str, str]]:
    cur = project.curriculum_for_subject(subject)
    if cur is None:
        raise SystemExit(f"no curriculum.yml for subject {subject!r}")
    graph = Graph(project)
    out = []
    for _slug, _title, topics, _line in cur.chapters:
        for label in topics:
            node = graph.nodes[label]
            if node.written:
                continue
            pre = [graph.nodes.get(p) for p in node.prereqs]
            if all(p is not None and p.written and STATUS_RANK[p.status] >= STATUS_RANK["reviewed"] for p in pre):
                out.append((label, node.planned.file, node.title))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    m = sub.add_parser("mermaid")
    m.add_argument("subject")
    m.add_argument("-o", "--output", help="output file (default content/<subject folder>/_generated/prereq-map.md; - for stdout)")
    r = sub.add_parser("ready")
    r.add_argument("subject")
    c = sub.add_parser("closure")
    c.add_argument("label")
    args = ap.parse_args(argv)
    project = Project(args.root)

    if args.cmd == "check":
        rep = Reporter()
        check(project, rep)
        print(f"graph.py check: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)", file=sys.stderr)
        return 1 if rep.errors else 0
    if args.cmd == "mermaid":
        text = mermaid(project, args.subject)
        if args.output == "-":
            sys.stdout.write(text)
            return 0
        cur = project.curriculum_for_subject(args.subject)
        out = Path(args.output) if args.output else project.root / cur.folder / "_generated" / "prereq-map.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"wrote {display(out)}")
        return 0
    if args.cmd == "ready":
        rows = ready(project, args.subject)
        width = max((len(r[0]) for r in rows), default=0)
        for label, _file, title in rows:
            print(f"{label.ljust(width)}  {title}")
        return 0
    if args.cmd == "closure":
        graph = Graph(project)
        if args.label not in graph.nodes:
            print(f"unknown label {args.label} (not a page or planned topic)", file=sys.stderr)
            return 2
        for label in sorted(graph.closure(args.label)):
            print(label)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
