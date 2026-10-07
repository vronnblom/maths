"""The toc of content/myst.yml against the Markdown files on disk (docs/plan/06 §6.4).

Every toc entry names an existing .md file inside the project, at most once; every .md file
under the project root is in the toc. This is the one check that globs the disk, and the glob
skips `_build/` (stale page copies from every build) and `_generated/` (included fragments,
not pages).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project import Project, Reporter, add_root_argument

SKIP_DIRS = {"_build", "_generated", "node_modules"}


def markdown_files(root: Path) -> list[str]:
    out = []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]):
            continue
        out.append(rel.as_posix())
    return out


def check(project: Project, rep: Reporter) -> None:
    myst = project.myst_path
    for line, msg in project.toc_problems:
        rep.error(myst, line, msg)
    seen: dict[str, int] = {}
    for e in project.toc:
        if e.file is None:
            continue
        if not isinstance(e.file, str):
            rep.error(myst, e.line, f"toc file is not a string: {e.file!r}")
            continue
        if not e.file.endswith(".md"):
            rep.error(myst, e.line, f"toc entry {e.file}: pages are .md files")
            continue
        path = (project.root / e.file).resolve()
        if not path.is_relative_to(project.root):
            rep.error(myst, e.line, f"toc entry {e.file} is outside the project root")
            continue
        rel = path.relative_to(project.root).as_posix()
        if rel in seen:
            rep.error(myst, e.line, f"toc entry {e.file} is listed twice (first at line {seen[rel]})")
            continue
        seen[rel] = e.line
        if not path.is_file():
            rep.error(myst, e.line, f"toc entry {e.file}: the file does not exist")
    for rel in markdown_files(project.root):
        if rel not in seen:
            rep.error(project.root / rel, 1, f"{rel} is not in the toc of myst.yml: add it there (order lives only in the toc) or delete it")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    args = ap.parse_args(argv)
    rep = Reporter()
    check(Project(args.root), rep)
    print(f"check_toc.py: {len(rep.errors)} error(s)", file=sys.stderr)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
