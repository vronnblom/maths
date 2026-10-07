#!/usr/bin/env bash
# SessionStart hook (docs/plan/10 §10.6): makes `npm run all` work in a Claude Code cloud
# session. It installs exactly what README.md's setup installs (`npm ci && uv sync`) and fetches
# the pinned site theme (scripts/fetch_theme.sh, 05 §5.5).
#
# - Cloud sessions only: on a laptop ($CLAUDE_CODE_REMOTE unset) it exits at once and touches
#   nothing. Run it by hand with CLAUDE_CODE_REMOTE=true to get the same setup locally.
# - Idempotent and quick when everything is installed: `npm ci` (which deletes node_modules/)
#   runs only when node_modules/ was not installed from the current package-lock.json by this
#   Node version (a stamp file records both); `uv sync --frozen` is a no-op on a synced .venv;
#   fetch_theme.sh is a no-op when the theme is there.
# - Fails loudly: any failing step stops the hook with exit code 2 and a message naming the
#   step, which Claude Code shows to the user. Nothing is half-installed silently: the stamp is
#   written only after `npm ci` succeeded, so the next session retries.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

step="start"
fail() {
  {
    echo "SessionStart hook (.claude/hooks/session-start.sh) FAILED at: $step"
    echo "The repository is NOT set up, so npm run check/verify/build will fail."
    echo "Fix the cause above, then run: CLAUDE_CODE_REMOTE=true bash .claude/hooks/session-start.sh"
  } >&2
  exit 2
}
trap fail ERR

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"
start=$SECONDS

step="checking the tools (node ≥ 22, npm, uv, git)"
for tool in node npm uv git; do
  command -v "$tool" >/dev/null || { echo "$tool is not installed" >&2; false; }
done
want=$(tr -dc '0-9' < .nvmrc)
have=$(node -p 'process.versions.node.split(".")[0]')
[ "$have" -ge "$want" ] || { echo "Node $have is too old: .nvmrc asks for $want" >&2; false; }

step="npm ci"
stamp=node_modules/.session-start-stamp
key="$(sha256sum package-lock.json | cut -d' ' -f1) node-$(node -v)"
if [ -f "$stamp" ] && [ "$(cat "$stamp")" = "$key" ] && [ -x node_modules/.bin/myst ]; then
  npm_state="up to date"
else
  npm ci --no-audit --no-fund --loglevel=error >&2
  echo "$key" > "$stamp"
  npm_state="installed"
fi

step="uv sync --frozen"
uv sync --frozen --quiet >&2

step="fetching the pinned theme (scripts/fetch_theme.sh)"
bash scripts/fetch_theme.sh >&2

# Exit 0: stdout goes into Claude's context.
echo "SessionStart hook: node_modules $npm_state, Python environment synced, site theme present ($((SECONDS - start)) s). npm run all is ready to run."
