"""Redirect pages for moved pages (docs/plan/02 §2.3). Run by scripts/build_site.sh after the build.

mystmd 1.11 has no redirects, so a page that moved lists its old URL paths in
`maths.aliases: [/calculus/limits/limit-laws]`. For each one this writes
`<html dir>/<old path>/index.html` with a meta refresh and a canonical link to the page's
current URL. Both are prefixed with BASE_URL (`/maths` on deploy), as mystmd's own links are.
It fails, writing nothing, if an old path is a live page (or any file the build wrote), or if
two pages claim the same old path, so a collision fails the PR rather than the deploy.

    write_redirects.py content/_build/html [--root content]
"""

from __future__ import annotations

import argparse
import html
import os
import sys
from pathlib import Path

from project import Project, Reporter, add_root_argument, display_path

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to {title}</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<meta name="robots" content="noindex">
</head>
<body>
<p>This page has moved to <a href="{url}">{title}</a>.</p>
</body>
</html>
"""


def plan(project: Project, html_dir: Path, rep: Reporter, base_url: str) -> list[tuple[Path, str, str]]:
    """[(file to write, new URL, title)]; reports collisions."""
    live = {p.url: p for p in project.pages}
    claimed: dict[str, object] = {}
    out = []
    for page in project.pages:
        aliases = page.maths.get("aliases") or []
        if not isinstance(aliases, list):
            continue
        for k, alias in enumerate(aliases):
            line = page.line("maths", "aliases", k)
            if not isinstance(alias, str) or not alias.startswith("/") or ".." in alias.split("/"):
                rep.error(page.path, line, f"alias {alias!r} is not an absolute URL path like /calculus/limits/limit-laws")
                continue
            old = "/" + alias.strip("/")
            if old in live:
                rep.error(page.path, line, f"alias {old} collides with the live page {live[old].rel}")
                continue
            if old in claimed:
                rep.error(page.path, line, f"alias {old} is also claimed by {claimed[old].rel}")
                continue
            claimed[old] = page
            target = html_dir / old.lstrip("/")
            if target.is_file() or (target / "index.html").exists():
                rep.error(page.path, line, f"alias {old} collides with {display_path(target)} in the built site")
                continue
            out.append((target / "index.html", f"{base_url}{page.url}", page.title or page.url))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html_dir", help="the built site, e.g. content/_build/html")
    add_root_argument(ap)
    args = ap.parse_args(argv)
    html_dir = Path(args.html_dir)
    if not html_dir.is_dir():
        print(f"write_redirects.py: {html_dir} is not a directory (build the site first)", file=sys.stderr)
        return 2
    base_url = os.environ.get("BASE_URL", "").rstrip("/")
    rep = Reporter()
    todo = plan(Project(args.root), html_dir, rep, base_url)
    if rep.errors:
        print(f"write_redirects.py: {len(rep.errors)} collision(s); no redirects written", file=sys.stderr)
        return 1
    for path, url, title in todo:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(TEMPLATE.format(url=html.escape(url, quote=True), title=html.escape(title)), encoding="utf-8")
    print(f"write_redirects.py: {len(todo)} redirect(s) written", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
