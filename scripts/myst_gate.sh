#!/usr/bin/env bash
# The build gate (docs/plan/05 §5.5): runs `myst build <args> --strict --ci` in the current
# directory and fails on any ⛔️ error or ⚠️ warning except the one expected warning about our
# `maths` front-matter key. --strict exits non-zero only on errors, and mystmd 1.11 prints some
# errors (e.g. an unknown directive) with ⛔️ even with exit code 0, hence the log filter.
# Used by build_site.sh (`--html`) and by tests/test_build_gate.py on fixture projects.
set -euo pipefail            # pipefail: a non-zero myst exit survives the pipe into tee
myst build "$@" --strict --ci 2>&1 | tee build.log
if grep -E '⛔️|⚠️' build.log | grep -v "extra key ignored: maths"; then
  echo "::error::MyST build produced errors or warnings"; exit 1
fi
