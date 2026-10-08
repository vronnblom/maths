# maths

An open, interactive and verified body of university mathematics: definitions, theorems,
proofs, worked examples and exercises, published as a website. Calculus is the first subject.

**Status:** Phase 0 (the repository, its checks and the site) is done, and the site is live
at <https://vronnblom.github.io/maths/>. The checks run in CI, the plugin renders page
headers, the first interactive widget (`function-plot`) is on the "How to read this site"
page, and the SymPy verification harness checks worked examples and exercise answers (read
from the built pages) and gates each page's status on the coverage it reaches. The curriculum
is planned (`content/calculus/curriculum.yml`); the first topic pages come next (Phase 1a).
Start with [PLAN.md](PLAN.md). To contribute, read [CONTRIBUTING.md](CONTRIBUTING.md); agents
read [CLAUDE.md](CLAUDE.md).

## Building the site

You need [Node.js 22](https://nodejs.org/) (see `.nvmrc`), [uv](https://docs.astral.sh/uv/)
(it installs Python 3.12+ if needed) and `git`, with network access to the npm registry, PyPI
and github.com.

```bash
git clone https://github.com/vronnblom/maths.git && cd maths
npm ci && uv sync     # install mystmd (pinned) and the Python tooling, from the lockfiles
npm run all           # everything CI runs: check, verify, test:widgets, then build
```

`npm run all` takes a few minutes and ends with the site in `content/_build/html`. Its parts:

```bash
npm run check         # the repository checks: front matter, labels, prerequisite graph, toc,
                      # notation lint, widgets, spelling, and the checkers' own tests
npm run verify        # the mathematics: build the AST, extract every exercise's answer,
                      # run the SymPy tests in verify/, then the coverage gate
npm run test:widgets  # the widgets' mathematics (against SymPy) and the plugin's logic
npm run build         # build the site into content/_build/html; fails on any error or warning
npm run dev           # live-reloading site at http://localhost:3000
```

`build` and `dev` first run `npm run generate`, which writes the prerequisite maps and the
status table from the curriculum and the pages (into git-ignored `_generated/` folders).
`uv run python scripts/graph.py ready calc` lists the topics that are ready to be written, and
`uv run python scripts/new_topic.py <label>` scaffolds one.

The first build fetches the site theme (a pinned commit of
[book-theme](https://github.com/myst-templates/book-theme)) with `git` into
`content/_build/templates/` (`scripts/fetch_theme.sh`); later builds reuse it.

To look at a built site, serve it from its root, for example
`npx serve content/_build/html`, rather than opening the files directly. The same applies
to the `site` artifact that CI attaches to every pull request.

In a Claude Code cloud session, the SessionStart hook (`.claude/hooks/session-start.sh`) runs
the installation and fetches the theme before the session starts.

## Layout

```
content/          the MyST project: myst.yml, the pages, curriculum.yml, tags.yml, _static/
plugins/          the MyST plugin: {topic-header}, {where-this-leads}, {chapter-topics}
widgets/          interactive widgets (anywidget modules using JSXGraph), _lib/, _tests/;
                  the catalogue is widgets/README.md
verify/           SymPy verification tests, the mathcheck helpers and their own tests
scripts/          the checks (check_all.py), graph.py, generate.py, write_redirects.py,
                  build_site.sh (the gated build), myst_gate.sh, fetch_theme.sh,
                  extract_answers.py, check_coverage.py, check_verified_edits.py,
                  new_topic.py (scaffolds a topic), links_report.sh
schema/           JSON Schemas for page front matter, curriculum.yml and widget configs
labels.lock       every label ever published (labels are permanent)
tests/            the checkers' tests, with one broken fixture project per check
docs/plan/        the plan; docs/decisions/ for later architecture decisions
docs/agents/      the agent roles (Author, Verifier, Reviewer) and their skills
templates/        page and test templates
.claude/          the SessionStart hook and the skills /new-topic, /verify-topic, /review-math,
                  /recheck-topic
.github/          workflows: ci.yml (checks, verify, build), guard.yml (the verified-page edit
                  guard on pull requests), deploy.yml (GitHub Pages), links.yml (weekly
                  external-link check); the PR template, issue forms, CODEOWNERS, Dependabot
```

## Licences

The content (everything under `content/`) is licensed under CC BY-SA 4.0
([LICENSE-CONTENT.md](LICENSE-CONTENT.md)); the code under MIT ([LICENSE](LICENSE)). See
[docs/plan/11-governance.md](docs/plan/11-governance.md).
