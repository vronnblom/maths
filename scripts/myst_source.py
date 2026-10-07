"""A small parser for the MyST Markdown that our pages use (docs/plan/03 §3.4, templates/).

The `checks` CI job does not build the site, so the label and notation checks read the
Markdown source. This is deliberately not a full MyST parser: it understands the front
matter, colon- and backtick-fenced directives with their `:option:` lines and nesting,
`(label)=` targets before headings, `$$ … $$ (label)` equations, MyST `%` comments, inline
code and math, and `[text](#label)` references. Anything else that would affect labels or
references (an unknown directive, a YAML option block, `{ref}` roles, …) is a ParseError, so
the checks fail loudly instead of guessing. `tests/test_parser_ast.py` compares the labels
found here with mystmd's own AST for templates/topic.md, so drift shows up as a failing test.
"""

from __future__ import annotations

import bisect
import re
from dataclasses import dataclass, field

# Directives whose body is Markdown (parsed recursively) …
PROOF_KINDS = {
    "proof:definition": "def",
    "proof:theorem": "thm",
    "proof:lemma": "lem",
    "proof:corollary": "cor",
    "proof:proposition": "prop",
    "proof:axiom": "ax",
    "proof:proof": "prf",
    "proof:example": "eg",
    "proof:remark": "rem",
}
ADMONITIONS = {
    "admonition", "note", "warning", "tip", "important", "hint", "caution", "attention",
    "danger", "error", "seealso",
}
PLUGIN_DIRECTIVES = {"topic-header", "where-this-leads"}  # plugins/topic-header.mjs (stage 3)
MARKDOWN_BODY = set(PROOF_KINDS) | ADMONITIONS | PLUGIN_DIRECTIVES | {
    "exercise", "solution", "figure", "table", "list-table",
}
# … and directives whose body is not Markdown (skipped).
RAW_BODY = {"anywidget", "math", "code", "code-block", "mermaid", "include"}
KNOWN_DIRECTIVES = MARKDOWN_BODY | RAW_BODY

# The label kinds each directive may carry (docs/plan/02 §2.4, 03 §3.4).
DIRECTIVE_KINDS = {
    **{name: (kind,) for name, kind in PROOF_KINDS.items()},
    **{name: ("rem",) for name in ADMONITIONS},
    "exercise": ("exr",),
    "solution": ("sol",),
    "figure": ("fig", "wdg"),
    "table": ("tbl",),
    "list-table": ("tbl",),
    "math": ("eq",),
}
LABEL_REQUIRED = {
    "proof:definition", "proof:theorem", "proof:lemma", "proof:corollary",
    "proof:proposition", "proof:axiom", "proof:example", "exercise", "solution",
}
STATEMENTS = {"proof:theorem", "proof:lemma", "proof:corollary", "proof:proposition"}
# Directives whose argument is a label or a path, not inline Markdown.
ARG_NOT_TEXT = {"solution", "figure", "include", "anywidget", "code", "code-block", "math", "mermaid"}
# Roles that are cross-references: we use [](#label) only (CLAUDE.md, 02 §2.4).
REF_ROLES = {"ref", "numref", "eq", "doc", "prf:ref", "term", "cite", "cite:p", "cite:t"}


class ParseError(Exception):
    def __init__(self, line: int, message: str):
        super().__init__(f"line {line}: {message}")
        self.line = line
        self.message = message


# ── Nodes ────────────────────────────────────────────────────────────────────


@dataclass
class Node:
    line: int
    parent: "Directive | None" = field(default=None, repr=False)

    def ancestors(self):
        p = self.parent
        while p is not None:
            yield p
            p = p.parent


@dataclass
class Directive(Node):
    name: str = ""
    arg: str = ""
    options: dict = field(default_factory=dict)
    option_lines: dict = field(default_factory=dict)
    end: int = 0
    fence: str = ":::"
    children: list = field(default_factory=list)
    raw: list = field(default_factory=list)  # [(line, text)] of a raw body ({math}, {code}, …)

    @property
    def label(self) -> str | None:
        return self.options.get("label") or None

    @property
    def classes(self) -> list[str]:
        return self.options.get("class", "").split()

    def option_line(self, key: str) -> int:
        return self.option_lines.get(key, self.line)


@dataclass
class Heading(Node):
    level: int = 0
    text: str = ""
    target: str | None = None
    target_line: int = 0


@dataclass
class Target(Node):
    label: str = ""


@dataclass
class DisplayMath(Node):
    text: str = ""
    label: str | None = None
    end: int = 0


@dataclass
class Paragraph(Node):
    lines: list = field(default_factory=list)  # [(line number, text)]


@dataclass
class Comment(Node):
    text: str = ""


@dataclass
class Rule(Node):
    """A thematic break (---)."""


@dataclass
class Code(Node):
    info: str = ""
    end: int = 0


# ── Inline content ───────────────────────────────────────────────────────────


@dataclass
class Inline:
    """The pieces of a run of inline Markdown, each with its source line."""

    math: list = field(default_factory=list)  # [(line, latex)]
    prose: list = field(default_factory=list)  # [(line, text with code and math blanked)]
    refs: list = field(default_factory=list)  # [(line, label, link text)]
    problems: list = field(default_factory=list)  # [(line, message)]


REF_RE = re.compile(r"\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)\s]*)\)")
ROLE_BEFORE = re.compile(r"\{([A-Za-z][\w:-]*)\}$")


def scan_inline(lines: list[tuple[int, str]]) -> Inline:
    """Split inline Markdown into prose, math and references, keeping line numbers."""
    out = Inline()
    if not lines:
        return out
    text = "\n".join(t for _, t in lines)
    starts, pos = [], 0
    for _, t in lines:
        starts.append(pos)
        pos += len(t) + 1
    numbers = [n for n, _ in lines]

    def line_at(offset):
        return numbers[bisect.bisect_right(starts, offset) - 1]

    code_masked = list(text)  # code blanked: for references
    prose = list(text)  # code and math blanked: for prose rules
    i, n = 0, len(text)

    def blank(buf, a, b):
        for k in range(a, b):
            if buf[k] != "\n":
                buf[k] = " "

    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            i += 2
            continue
        if c == "`":
            j = i
            while j < n and text[j] == "`":
                j += 1
            ticks = text[i:j]
            close = re.compile(r"(?<!`)" + re.escape(ticks) + r"(?!`)")
            m = close.search(text, j)
            if not m:
                i = j
                continue
            role = ROLE_BEFORE.search(text[:i])
            body = text[j : m.start()]
            if role:
                name = role.group(1)
                if name in REF_ROLES:
                    out.problems.append(
                        (line_at(i), f"{{{name}}} role: write cross-references as [text](#label)")
                    )
                if name == "math":
                    out.math.append((line_at(j), body))
                a = role.start()
            else:
                a = i
            blank(code_masked, a, m.end())
            blank(prose, a, m.end())
            i = m.end()
            continue
        if c == "$":
            if text.startswith("$$", i):
                k = text.find("$$", i + 2)
                if k < 0:
                    i += 2
                    continue
                out.math.append((line_at(i), text[i + 2 : k]))
                blank(prose, i, k + 2)
                i = k + 2
                continue
            k = i + 1
            while k < n and not (text[k] == "$" and text[k - 1] != "\\"):
                k += 1
            if k >= n:
                i += 1
                continue
            out.math.append((line_at(i), text[i + 1 : k]))
            blank(prose, i, k + 1)
            i = k + 1
            continue
        i += 1

    masked = "".join(code_masked)
    for m in REF_RE.finditer(masked):
        target = m.group(2)
        if target.startswith("#"):
            out.refs.append((line_at(m.start()), target[1:], m.group(1)))
        elif target.startswith(("project:", "xref:")) or target.endswith(".md") or ".md#" in target:
            out.problems.append(
                (line_at(m.start()), f"link to {target!r}: link to a label instead, [text](#label)")
            )
    prose_text = "".join(prose)
    for k, t in enumerate(prose_text.split("\n")):
        out.prose.append((numbers[k], t))
    return out


# ── Blocks ───────────────────────────────────────────────────────────────────

COLON_OPEN = re.compile(r"^(\s*)(:{3,})\{([^}\s]+)\}\s*(.*?)\s*$")
COLON_PLAIN = re.compile(r"^(\s*)(:{3,})\s*(\S.*)?$")
TICK_OPEN = re.compile(r"^(\s*)(`{3,}|~{3,})\s*(.*?)\s*$")
OPTION = re.compile(r"^\s*:([A-Za-z0-9_-]+):(?:\s+(.*?))?\s*$")
TARGET = re.compile(r"^\s*\(([^()\s]+)\)=\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
EQ_LABEL = re.compile(r"^\$\$\s*\(([^()\s]+)\)\s*$")


@dataclass
class Document:
    frontmatter_end: int  # line of the closing --- (0 if none)
    children: list
    comments: list  # every Comment, in order

    def walk(self):
        """Every node, depth first, in document order."""
        def rec(nodes):
            for nd in nodes:
                yield nd
                if isinstance(nd, Directive):
                    yield from rec(nd.children)
        yield from rec(self.children)

    def directives(self):
        return [n for n in self.walk() if isinstance(n, Directive)]

    def inline_runs(self):
        """(node, Inline) for every run of inline Markdown: paragraphs, headings and the
        titles of directives."""
        for nd in self.walk():
            if isinstance(nd, Paragraph):
                yield nd, scan_inline(nd.lines)
            elif isinstance(nd, Heading):
                yield nd, scan_inline([(nd.line, nd.text)])
            elif isinstance(nd, Directive) and nd.arg and nd.name not in ARG_NOT_TEXT:
                yield nd, scan_inline([(nd.line, nd.arg)])

    def display_math(self):
        """(line, latex) of every display: $$ blocks and {math} directives."""
        for nd in self.walk():
            if isinstance(nd, DisplayMath):
                yield nd.line, nd.text
            elif isinstance(nd, Directive) and nd.name == "math" and nd.raw:
                yield nd.raw[0][0], "\n".join(t for _, t in nd.raw)


def parse(text: str) -> Document:
    lines = text.split("\n")
    start = 0
    fm_end = 0
    if lines and lines[0].rstrip() == "---":
        for i in range(1, len(lines)):
            if lines[i].rstrip() == "---":
                fm_end = i + 1
                start = i + 1
                break
        else:
            raise ParseError(1, "front matter has no closing ---")
    comments: list[Comment] = []
    children = _parse_blocks(lines, start, len(lines), None, comments)
    return Document(frontmatter_end=fm_end, children=children, comments=comments)


def _parse_blocks(lines, start, end, parent, comments):
    nodes: list[Node] = []
    para: Paragraph | None = None
    pending_target: Target | None = None
    i = start

    def flush():
        nonlocal para
        if para is not None:
            nodes.append(para)
            para = None

    while i < end:
        raw = lines[i]
        ln = i + 1
        s = raw.strip()
        if not s:
            flush()
            i += 1
            continue
        if s.startswith("%"):
            flush()
            c = Comment(line=ln, parent=parent, text=s[1:].strip())
            nodes.append(c)
            comments.append(c)
            i += 1
            continue
        if s.startswith("<!--"):
            flush()
            j = i
            while j < end and "-->" not in lines[j]:
                j += 1
            if j >= end:
                raise ParseError(ln, "unclosed HTML comment")
            c = Comment(line=ln, parent=parent, text=s)
            nodes.append(c)
            comments.append(c)
            i = j + 1
            continue
        m = COLON_OPEN.match(raw)
        if m:
            flush()
            if pending_target:
                raise ParseError(pending_target.line, "a (label)= target must come before a heading; label a directive with :label:")
            d, i = _parse_directive(lines, i, end, parent, comments, m.group(2), m.group(3), m.group(4))
            nodes.append(d)
            continue
        if COLON_PLAIN.match(raw):
            raise ParseError(ln, f"stray colon fence {s!r} (no directive open here, or too many colons)")
        m = TICK_OPEN.match(raw)
        if m:
            flush()
            if pending_target:
                raise ParseError(pending_target.line, "a (label)= target must come before a heading; label a directive with :label:")
            fence, info = m.group(2), m.group(3)
            dm = re.match(r"^\{([^}\s]+)\}\s*(.*)$", info)
            if dm:
                d, i = _parse_directive(lines, i, end, parent, comments, fence, dm.group(1), dm.group(2))
                nodes.append(d)
            else:
                j = _find_close(lines, i + 1, end, fence)
                if j is None:
                    raise ParseError(ln, f"unclosed code fence {fence}")
                nodes.append(Code(line=ln, parent=parent, info=info, end=j + 1))
                i = j + 1
            continue
        m = TARGET.match(raw)
        if m:
            flush()
            if pending_target:
                raise ParseError(pending_target.line, "two (label)= targets in a row")
            pending_target = Target(line=ln, parent=parent, label=m.group(1))
            nodes.append(pending_target)
            i += 1
            continue
        m = HEADING.match(raw)
        if m:
            flush()
            h = Heading(line=ln, parent=parent, level=len(m.group(1)), text=m.group(2))
            if pending_target:
                h.target, h.target_line = pending_target.label, pending_target.line
                pending_target = None
            nodes.append(h)
            i += 1
            continue
        if pending_target:
            raise ParseError(pending_target.line, "a (label)= target must come directly before a heading; label a directive with :label:")
        if s.startswith("$$"):  # a display interrupts a paragraph, as in markdown-it
            flush()
            j, body, label = _parse_display_math(lines, i, end)
            nodes.append(DisplayMath(line=ln, parent=parent, text=body, label=label, end=j + 1))
            i = j + 1
            continue
        if s == "---" and para is None:
            nodes.append(Rule(line=ln, parent=parent))
            i += 1
            continue
        if para is None:
            para = Paragraph(line=ln, parent=parent)
        para.lines.append((ln, raw))
        i += 1
    flush()
    if pending_target:
        raise ParseError(pending_target.line, "a (label)= target must come before a heading")
    return nodes


def _find_close(lines, i, end, fence):
    ch, n = fence[0], len(fence)
    pat = re.compile(r"^\s*" + re.escape(ch) + "{" + str(n) + r",}\s*$")
    for j in range(i, end):
        if pat.match(lines[j]):
            return j
    return None


def _parse_display_math(lines, i, end):
    s = lines[i].strip()
    rest = s[2:]
    k = rest.find("$$")
    if k >= 0:  # $$ … $$ on one line, maybe with (label)
        after = rest[k + 2 :].strip()
        label = None
        if after:
            m = re.match(r"^\(([^()\s]+)\)$", after)
            if not m:
                raise ParseError(i + 1, f"text after a one-line $$ … $$: {after!r}")
            label = m.group(1)
        return i, rest[:k], label
    body = [rest]
    for j in range(i + 1, end):
        t = lines[j].strip()
        if t.startswith("$$") or t.endswith("$$"):
            if t.endswith("$$") and not t.startswith("$$"):
                body.append(t[:-2])
                return j, "\n".join(body), None
            m = EQ_LABEL.match(t)
            if m:
                return j, "\n".join(body), m.group(1)
            if t == "$$":
                return j, "\n".join(body), None
            raise ParseError(j + 1, f"unexpected text after $$: {t!r}")
        body.append(lines[j])
    raise ParseError(i + 1, "unclosed $$ display")


def _parse_directive(lines, i, end, parent, comments, fence, name, arg):
    ln = i + 1
    if name not in KNOWN_DIRECTIVES:
        raise ParseError(
            ln,
            f"unknown directive {{{name}}}: scripts/myst_source.py does not know it. Use a "
            f"directive from templates/blocks.md, or teach the parser in a tooling PR",
        )
    if fence[0] == ":" and parent is not None and parent.fence[0] == ":" and len(fence) >= len(parent.fence):
        raise ParseError(
            ln,
            f"{{{name}}} opens with {len(fence)} colons inside {{{parent.name}}} with "
            f"{len(parent.fence)}: the outer directive needs more colons than the inner one",
        )
    d = Directive(line=ln, parent=parent, name=name, arg=arg.strip(), fence=fence)
    j = i + 1
    if j < end and lines[j].strip() == "---":
        raise ParseError(j + 1, f"YAML option block in {{{name}}}: write options as :key: value lines")
    while j < end:
        m = OPTION.match(lines[j])
        if not m:
            break
        key, val = m.group(1), (m.group(2) or "").strip()
        if key in d.options:
            raise ParseError(j + 1, f"option :{key}: given twice")
        d.options[key] = val
        d.option_lines[key] = j + 1
        j += 1
    close = _find_close(lines, j, end, fence)
    if close is None:
        raise ParseError(ln, f"{{{name}}} opened with {fence} is never closed")
    d.end = close + 1
    if name in MARKDOWN_BODY:
        d.children = _parse_blocks(lines, j, close, d, comments)
    else:
        d.raw = [(k + 1, lines[k]) for k in range(j, close)]
    return d, close + 1


# ── Labels ───────────────────────────────────────────────────────────────────


@dataclass
class LabelSite:
    label: str
    line: int
    kinds: tuple  # the label kinds this site may carry
    node: Node
    where: str  # a description, e.g. "{proof:theorem}"


def label_sites(doc: Document) -> list[LabelSite]:
    """Every block label in the document (not the page label), in document order."""
    sites = []
    for nd in doc.walk():
        if isinstance(nd, Directive) and nd.label:
            sites.append(LabelSite(nd.label, nd.option_line("label"), DIRECTIVE_KINDS.get(nd.name, ()), nd, f"{{{nd.name}}}"))
        elif isinstance(nd, Heading) and nd.target:
            sites.append(LabelSite(nd.target, nd.target_line, ("sec",), nd, "a heading target"))
        elif isinstance(nd, DisplayMath) and nd.label:
            sites.append(LabelSite(nd.label, nd.end, ("eq",), nd, "a $$ equation"))
    return sites


def previous_sibling(node: Node, doc: Document):
    """The block before `node` at the same level, skipping comments."""
    siblings = node.parent.children if node.parent is not None else doc.children
    k = next(i for i, s in enumerate(siblings) if s is node)
    for s in reversed(siblings[:k]):
        if not isinstance(s, Comment):
            return s
    return None
