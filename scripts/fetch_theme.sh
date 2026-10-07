#!/usr/bin/env bash
# Puts the book-theme commit pinned in content/myst.yml into mystmd's template cache, using
# git instead of mystmd's zip download (05 §5.5, "The theme is a dependency too").
#
# mystmd 1.11 keeps a URL template in content/_build/templates/site/<sha256 of the URL>/ and
# skips the download when template.yml is already there (it then runs `npm ci` in that folder
# once, if node_modules/ is missing). Claude Code cloud sessions can't download github.com
# archives, but can `git fetch` public repositories, so this works everywhere. A fetch by
# commit SHA is content-addressed, so it gets exactly the pinned files.
set -euo pipefail
cd "$(dirname "$0")/../content"

url=$(grep -m1 -oE 'https://github\.com/myst-templates/book-theme/archive/[0-9a-f]{40}\.zip' myst.yml) || {
  echo "::error::no pinned book-theme URL in content/myst.yml" >&2; exit 1; }
sha=$(basename "$url" .zip)
hash=$(node -e 'process.stdout.write(require("crypto").createHash("sha256").update(process.argv[1]).digest("hex"))' "$url")
dir="_build/templates/site/$hash"
[ -f "$dir/template.yml" ] && exit 0

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git -C "$tmp" init -q
git -C "$tmp" fetch -q --depth 1 https://github.com/myst-templates/book-theme "$sha"
mkdir -p "$tmp/theme"
git -C "$tmp" archive FETCH_HEAD | tar -x -C "$tmp/theme"
rm -rf "$dir"                       # a partial download left by mystmd, if any
mkdir -p "$(dirname "$dir")"
mv "$tmp/theme" "$dir"
echo "Fetched book-theme $sha into content/$dir"
