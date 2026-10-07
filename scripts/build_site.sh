#!/usr/bin/env bash
set -euo pipefail            # pipefail: a non-zero myst exit survives the pipe into tee
bash "$(dirname "$0")/fetch_theme.sh"   # the pinned theme, via git (no-op when cached)
cd "$(dirname "$0")/../content"
myst build --html --strict --ci 2>&1 | tee build.log
# --strict exits non-zero only on errors. mystmd 1.11 prints errors with ⛔️ (some, e.g. an
# unknown directive, even with exit code 0) and warnings with ⚠️. Both fail the build, except
# the one expected warning about our `maths` front-matter key.
if grep -E '⛔️|⚠️' build.log | grep -v "extra key ignored: maths"; then
  echo "::error::MyST build produced errors or warnings"; exit 1
fi
