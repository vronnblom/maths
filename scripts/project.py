"""Shared loading for the repository checks: the toc, page front matter, curricula, diagnostics.

Every checker takes a project root (the folder with `myst.yml`, default `content/`); the
repository root is its parent (`labels.lock`, `verify/`, `schema/` live there). The page list
always comes from the toc in `myst.yml`, never from a glob, so the stale copies that every
build writes into `content/_build/` are never read (docs/plan/06 §6.4).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO / "content"

# Subject codes (docs/plan/02 §2.4). `site` is the pseudo-subject of meta pages.
SUBJECTS = ("calc", "linalg", "mvc", "found", "disc", "prob", "ana", "ode", "cplx")
STATUS_RANK = {"draft": 0, "reviewed": 1, "verified": 2}


# ── Diagnostics ──────────────────────────────────────────────────────────────


@dataclass
class Diagnostic:
    severity: str  # "error" | "warning"
    path: Path
    line: int
    message: str

    def location(self) -> str:
        return f"{display_path(self.path)}:{self.line}"

    def __str__(self) -> str:
        return f"{self.location()}: {self.severity}: {self.message}"


def display_path(path: Path) -> str:
    """The path relative to the working directory when it is inside it (clickable, and what
    GitHub annotations expect when run from the repository root)."""
    path = Path(path)
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _escape_data(s: str) -> str:
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _escape_property(s: str) -> str:
    return _escape_data(s).replace(":", "%3A").replace(",", "%2C")


class Reporter:
    """Collects diagnostics and prints them as `file:line: severity: message`, plus a GitHub
    `::error file=…,line=…::` annotation when `GITHUB_ACTIONS` is set."""

    def __init__(self, stream=None, annotate: bool | None = None, quiet: bool = False):
        self.stream = stream
        self.annotate = bool(os.environ.get("GITHUB_ACTIONS")) if annotate is None else annotate
        self.quiet = quiet
        self.diagnostics: list[Diagnostic] = []

    def error(self, path, line, message):
        self._add("error", path, line, message)

    def warning(self, path, line, message):
        self._add("warning", path, line, message)

    def report(self, severity, path, line, message):
        self._add(severity, path, line, message)

    def _add(self, severity, path, line, message):
        d = Diagnostic(severity, Path(path), max(int(line or 1), 1), message)
        self.diagnostics.append(d)
        if self.quiet:
            return
        out = self.stream or sys.stdout
        print(d, file=out)
        if self.annotate:
            print(
                f"::{severity} file={_escape_property(display_path(d.path))},line={d.line}::"
                f"{_escape_data(message)}",
                file=out,
            )

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == "error"]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == "warning"]


# ── YAML with line numbers ───────────────────────────────────────────────────


def yaml_lines(text: str, first_line: int = 1) -> dict[tuple, int]:
    """Map every key path in a YAML document (tuples of keys and list indices) to the 1-based
    line where its value starts; the empty tuple maps to the document start."""
    lines: dict[tuple, int] = {}
    node = yaml.compose(text, Loader=yaml.SafeLoader)
    if node is None:
        return {(): first_line}

    def walk(n, path):
        lines.setdefault(path, n.start_mark.line + first_line)
        if isinstance(n, yaml.MappingNode):
            for k, v in n.value:
                key = k.value
                lines[path + (key,)] = k.start_mark.line + first_line
                walk(v, path + (key,))
                lines[path + (key,)] = k.start_mark.line + first_line
        elif isinstance(n, yaml.SequenceNode):
            for i, v in enumerate(n.value):
                walk(v, path + (i,))

    walk(node, ())
    return lines


def line_of(lines: dict[tuple, int], path) -> int:
    """The line of the deepest prefix of `path` that has one."""
    path = tuple(path)
    while path and path not in lines:
        path = path[:-1]
    return lines.get(path, 1)


# ── Pages ────────────────────────────────────────────────────────────────────


@dataclass
class Page:
    root: Path
    rel: str  # posix path relative to the project root, e.g. "calculus/limits/limit-laws.md"
    toc_line: int
    text: str = ""
    fm: dict | None = None
    fm_error: str | None = None
    fm_error_line: int = 1
    fm_lines: dict = field(default_factory=dict)
    fm_end: int = 0  # the line of the closing `---` (0 when there is no front matter)

    @property
    def path(self) -> Path:
        return self.root / self.rel

    @property
    def maths(self) -> dict:
        m = (self.fm or {}).get("maths")
        return m if isinstance(m, dict) else {}

    @property
    def label(self) -> str | None:
        v = (self.fm or {}).get("label")
        return v if isinstance(v, str) else None

    @property
    def kind(self) -> str | None:
        return self.maths.get("kind")

    @property
    def subject(self) -> str | None:
        return self.maths.get("subject")

    @property
    def status(self) -> str:
        s = self.maths.get("status")
        return s if s in STATUS_RANK else "draft"

    @property
    def title(self) -> str | None:
        return (self.fm or {}).get("title")

    @property
    def prerequisites(self) -> list[str]:
        p = self.maths.get("prerequisites") or []
        return [x for x in p if isinstance(x, str)] if isinstance(p, list) else []

    def line(self, *keys) -> int:
        """The line of a front-matter key path, e.g. page.line("maths", "status")."""
        return line_of(self.fm_lines, keys) if self.fm_lines else 1

    @property
    def url(self) -> str:
        """The site path of the page (site.options.folders: true), without BASE_URL."""
        stem = self.rel[: -len(".md")] if self.rel.endswith(".md") else self.rel
        if stem == "index":
            return "/"
        if stem.endswith("/index"):
            stem = stem[: -len("/index")]
        return "/" + stem


def read_page(root: Path, rel: str, toc_line: int = 1) -> Page:
    page = Page(root=root, rel=rel, toc_line=toc_line)
    page.text = (root / rel).read_text(encoding="utf-8")
    lines = page.text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return page
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            page.fm_end = i + 1
            raw = "\n".join(lines[1:i])
            try:
                data = yaml.safe_load(raw)
                page.fm_lines = yaml_lines(raw, first_line=2)
            except yaml.YAMLError as e:
                page.fm_error = f"front matter is not valid YAML: {getattr(e, 'problem', None) or e}"
                mark = getattr(e, "problem_mark", None)
                page.fm_error_line = (mark.line + 2) if mark else 2
                return page
            if data is None:
                data = {}
            if not isinstance(data, dict):
                page.fm_error = "front matter is not a mapping"
                page.fm_error_line = 2
                return page
            page.fm = data
            return page
    page.fm_error = "front matter has no closing ---"
    return page


# ── The toc ──────────────────────────────────────────────────────────────────


@dataclass
class TocEntry:
    file: str | None
    line: int
    title: str | None = None
    keys: tuple = ()


TOC_KEYS = {"file", "title", "children"}


def load_myst(root: Path):
    """(data, line map) of myst.yml, or raises FileNotFoundError / yaml.YAMLError."""
    text = (root / "myst.yml").read_text(encoding="utf-8")
    return yaml.safe_load(text) or {}, yaml_lines(text)


def toc_entries(root: Path) -> tuple[list[TocEntry], list[tuple[int, str]]]:
    """Flatten the toc of myst.yml. Returns (entries, problems), problems as (line, message)."""
    problems: list[tuple[int, str]] = []
    try:
        data, lines = load_myst(root)
    except FileNotFoundError:
        return [], [(1, "no myst.yml")]
    except yaml.YAMLError as e:
        return [], [(1, f"myst.yml is not valid YAML: {e}")]
    toc = (data.get("project") or {}).get("toc")
    if not isinstance(toc, list):
        return [], [(line_of(lines, ("project",)), "myst.yml has no project.toc list")]
    entries: list[TocEntry] = []

    def walk(items, path):
        for i, item in enumerate(items):
            p = path + (i,)
            ln = line_of(lines, p)
            if not isinstance(item, dict):
                problems.append((ln, f"toc entry is not a mapping: {item!r}"))
                continue
            unknown = set(item) - TOC_KEYS
            if unknown:
                problems.append(
                    (ln, f"toc entry uses {', '.join(sorted(unknown))}; the checks understand only "
                         f"file, title and children")
                )
            f = item.get("file")
            if f is None and "children" not in item:
                problems.append((ln, "toc entry has neither file nor children"))
            entries.append(TocEntry(file=f, line=ln, title=item.get("title"), keys=tuple(item)))
            if isinstance(item.get("children"), list):
                walk(item["children"], p + ("children",))
            elif "children" in item:
                problems.append((ln, "toc children is not a list"))

    walk(toc, ("project", "toc"))
    return entries, problems


# ── Curricula ────────────────────────────────────────────────────────────────


@dataclass
class PlannedTopic:
    label: str
    file: str  # relative to the project root, e.g. "calculus/limits/limit-laws.md"
    title: str
    level: str
    prerequisites: list[str]
    chapter: str
    line: int
    curriculum: "Curriculum"
    data: dict


@dataclass
class Curriculum:
    path: Path
    folder: str  # the subject folder, relative to the project root, e.g. "calculus"
    data: dict
    lines: dict
    subject: str | None = None
    topics: dict = field(default_factory=dict)  # label -> PlannedTopic
    chapters: list = field(default_factory=list)  # (slug, title, [labels], line)
    error: str | None = None

    def line(self, *keys) -> int:
        return line_of(self.lines, keys)


def load_curriculum(path: Path, root: Path) -> Curriculum:
    folder = path.parent.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text) or {}
        lines = yaml_lines(text)
    except yaml.YAMLError as e:
        return Curriculum(path=path, folder=folder, data={}, lines={}, error=f"not valid YAML: {e}")
    cur = Curriculum(path=path, folder=folder, data=data if isinstance(data, dict) else {}, lines=lines)
    if not isinstance(data, dict):
        cur.error = "not a mapping"
        return cur
    cur.subject = data.get("subject")
    for ci, ch in enumerate(data.get("chapters") or []):
        if not isinstance(ch, dict):
            continue
        labels = []
        for ti, t in enumerate(ch.get("topics") or []):
            if not isinstance(t, dict) or not isinstance(t.get("label"), str):
                continue
            pre = t.get("prerequisites") or []
            topic = PlannedTopic(
                label=t["label"],
                file=f"{folder}/{t.get('file')}",
                title=t.get("title"),
                level=t.get("level"),
                prerequisites=[p for p in pre if isinstance(p, str)] if isinstance(pre, list) else [],
                chapter=ch.get("slug"),
                line=line_of(lines, ("chapters", ci, "topics", ti)),
                curriculum=cur,
                data=t,
            )
            labels.append(topic.label)
            cur.topics.setdefault(topic.label, topic)
        cur.chapters.append((ch.get("slug"), ch.get("title"), labels, line_of(lines, ("chapters", ci))))
    return cur


# ── The project ──────────────────────────────────────────────────────────────


class Project:
    def __init__(self, root: Path | str = DEFAULT_ROOT):
        self.root = Path(root).resolve()
        self.repo = self.root.parent
        self.myst_path = self.root / "myst.yml"
        self.toc, self.toc_problems = toc_entries(self.root)
        self.pages: list[Page] = []
        seen = set()
        for e in self.toc:
            if not isinstance(e.file, str) or not e.file.endswith(".md") or e.file in seen:
                continue
            p = (self.root / e.file).resolve()
            if not p.is_file() or not p.is_relative_to(self.root):
                continue
            seen.add(e.file)
            self.pages.append(read_page(self.root, Path(e.file).as_posix(), e.line))
        self.page_by_rel = {p.rel: p for p in self.pages}
        self.page_by_label: dict[str, Page] = {}
        for p in self.pages:
            if p.label and p.label not in self.page_by_label:
                self.page_by_label[p.label] = p
        self.curricula: list[Curriculum] = []
        for path in sorted(self.root.glob("*/curriculum.yml")):
            if path.parent.name.startswith(("_", ".")):
                continue
            self.curricula.append(load_curriculum(path, self.root))
        self.planned: dict[str, PlannedTopic] = {}
        for c in self.curricula:
            for label, t in c.topics.items():
                self.planned.setdefault(label, t)

    def curriculum_for_subject(self, subject: str) -> Curriculum | None:
        for c in self.curricula:
            if c.subject == subject:
                return c
        return None

    def curriculum_for_folder(self, folder: str) -> Curriculum | None:
        for c in self.curricula:
            if c.folder == folder:
                return c
        return None

    def subject_page(self, subject: str) -> Page | None:
        p = self.page_by_label.get(f"{subject}-subject")
        return p if p is not None and p.kind == "subject" else None

    def load_tags(self) -> tuple[set[str] | None, str | None]:
        path = self.root / "tags.yml"
        if not path.exists():
            return None, None
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            return None, f"tags.yml is not valid YAML: {e}"
        tags = data.get("tags") if isinstance(data, dict) else None
        if not isinstance(tags, dict):
            return None, "tags.yml has no `tags:` mapping"
        return set(tags), None


def add_root_argument(parser):
    parser.add_argument(
        "--root",
        default=str(DEFAULT_ROOT),
        help="the MyST project root (the folder with myst.yml); default: content/",
    )
