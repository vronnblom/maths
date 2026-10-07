#!/usr/bin/env bash
# Keeps one open issue, "External links report", in step with the last lychee run
# (.github/workflows/links.yml, 05 §5.7). Reads EXIT_CODE (lychee's: 0 all links fine,
# 2 some broken), RUN_URL and lychee/out.md; needs GH_TOKEN and GH_REPO for the gh CLI.
set -euo pipefail
title="External links report"
number=$(gh issue list --state open --search "\"$title\" in:title" --json number,title \
  --jq ".[] | select(.title == \"$title\") | .number" | head -n 1)

if [ "$EXIT_CODE" = 2 ]; then
  {
    echo "The weekly link check found broken external links ([run]($RUN_URL))."
    echo "External sites flake: recheck before editing a page. Fix real breakages in a PR;"
    echo "this issue is updated every week and closed when all links pass."
    echo
    head -c 60000 lychee/out.md      # an issue body holds at most 65536 characters
  } > body.md
  if [ -n "$number" ]; then
    gh issue edit "$number" --body-file body.md
    echo "Updated #$number"
  else
    gh issue create --title "$title" --body-file body.md
  fi
elif [ -n "$number" ]; then
  gh issue close "$number" --comment "All external links pass again ([run]($RUN_URL))."
  echo "Closed #$number"
fi
