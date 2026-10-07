#!/usr/bin/env bash
# The one site build: `npm run build` (after `npm run generate`), CI and deploy (05 §5.5).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
bash "$here/fetch_theme.sh"           # the pinned theme, via git (no-op when cached)
cd "$here/../content"
bash "$here/myst_gate.sh" --html      # errors and warnings fail, except the whitelisted one
# Redirect pages for moved pages (02 §2.3). Run here, not only on deploy, so a redirect that
# collides with a live page fails the PR. Reads BASE_URL (/maths on deploy) like mystmd.
uv run python "$here/write_redirects.py" _build/html
