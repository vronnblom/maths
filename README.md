# maths

An open, interactive and verified body of university mathematics: definitions, theorems,
proofs, worked examples and exercises, published as a website. Calculus is the first subject.

**Status:** Phase 0 (setting up the repository). The site skeleton builds and deploys, the
repository checks run in CI, the plugin that renders page headers works, and the first
interactive widget (`function-plot`) is on the "How to read this site" page. The curriculum is
planned (`content/calculus/curriculum.yml`), but there is no topic content yet. Start with [PLAN.md](PLAN.md). Agents should read [CLAUDE.md](CLAUDE.md).

## Building the site

You need [Node.js 22](https://nodejs.org/) (see `.nvmrc`), [uv](https://docs.astral.sh/uv/)
(it installs Python 3.12+ if needed) and `git`.

```bash
npm ci && uv sync     # install mystmd (pinned) and the Python tooling
npm run check         # the repository checks: front matter, labels, prerequisite graph, toc,
                      # notation lint, widgets, spelling, and the checkers' own tests
npm run test:widgets  # the widgets' mathematics (against SymPy) and the plugin's logic
npm run build         # build the site into content/_build/html; fails on any error or warning
npm run dev           # live-reloading site at http://localhost:3000
npm run all           # everything CI runs: check, test:widgets, then build
```

`build` and `dev` first run `npm run generate`, which writes the prerequisite maps and the
status table from the curriculum and the pages (into git-ignored `_generated/` folders).
`uv run python scripts/graph.py ready calc` lists the topics that are ready to be written.

The first build fetches the site theme (a pinned commit of
[book-theme](https://github.com/myst-templates/book-theme)) with `git` into
`content/_build/templates/` (`scripts/fetch_theme.sh`); later builds reuse it.

To look at a built site, serve it from its root, for example
`npx serve content/_build/html`, rather than opening the files directly. The same applies
to the `site` artifact that CI attaches to every pull request.

## Layout

```
content/          the MyST project: myst.yml, the pages, curriculum.yml, tags.yml, _static/
plugins/          the MyST plugin: {topic-header}, {where-this-leads}, {chapter-topics}
widgets/          interactive widgets (anywidget modules using JSXGraph), _lib/, _tests/;
                  the catalogue is widgets/README.md
scripts/          the checks (check_all.py), graph.py, generate.py, write_redirects.py,
                  build_site.sh (the gated build), myst_gate.sh, fetch_theme.sh
schema/           JSON Schemas for page front matter, curriculum.yml and widget configs
labels.lock       every label ever published (labels are permanent)
tests/            the checkers' tests, with one broken fixture project per check
docs/plan/        the plan
templates/        page and test templates
.github/workflows ci.yml (checks, build), deploy.yml (GitHub Pages)
```

## Licences

The content (everything under `content/`) is licensed under CC BY-SA 4.0
([LICENSE-CONTENT.md](LICENSE-CONTENT.md)); the code under MIT ([LICENSE](LICENSE)). See
[docs/plan/11-governance.md](docs/plan/11-governance.md).
