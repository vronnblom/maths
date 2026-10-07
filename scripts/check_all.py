"""Every repository check over the pages in the toc (docs/plan/06 §6.4); `npm run check` and the
CI `checks` job run this, then codespell and the checkers' own tests (pytest tests).

    toc           check_toc.py            the toc against the files on disk
    front matter  check_frontmatter.py    schema, tags, status preconditions, prerequisite gate
    labels        check_labels.py         grammar, kinds, duplicates, exercises, proofs, labels.lock,
                                          forward references (warnings; errors on verified pages)
    graph         graph.py check          prerequisites resolve, no cycles, depends_on, curriculum agreement
    notation      notation_lint.py        bare \\log, \\sin^{-1}, raw dx, ]a, b[, \\mathrm{e}, degrees, "clearly"
    widgets       check_widgets.py        {anywidget} alone in a wdg- figure with a caption, the widget exists,
                                          its JSON against schema/widgets/, maths.widgets ids

Exits non-zero on any error. Warnings are printed but don't fail.
"""

from __future__ import annotations

import argparse
import sys

import check_frontmatter
import check_labels
import check_toc
import check_widgets
import graph
import notation_lint
from project import Project, Reporter, add_root_argument


def run(project: Project, rep: Reporter) -> None:
    check_toc.check(project, rep)
    check_frontmatter.check(project, rep)
    labels = check_labels.check(project, rep, forward_refs=True)
    graph.check(project, rep)
    notation_lint.check(project, rep, docs=labels.docs)
    check_widgets.check(project, rep, docs=labels.docs)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_root_argument(ap)
    args = ap.parse_args(argv)
    project = Project(args.root)
    rep = Reporter()
    run(project, rep)
    print(f"check_all.py: {len(project.pages)} pages, {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)",
          file=sys.stderr)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
