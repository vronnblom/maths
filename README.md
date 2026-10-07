# maths

An open, interactive and verified body of university mathematics: definitions, theorems,
proofs, worked examples and exercises, published as a website. Calculus is the first subject.

**Status:** Phase 0 (setting up the repository). The site skeleton builds and deploys; there
is no topic content yet. Start with [PLAN.md](PLAN.md). Agents should read [CLAUDE.md](CLAUDE.md).

## Building the site

You need [Node.js 22](https://nodejs.org/) (see `.nvmrc`), [uv](https://docs.astral.sh/uv/)
(it installs Python 3.12+ if needed) and `git`.

```bash
npm ci && uv sync     # install mystmd (pinned) and the Python tooling
npm run build         # build the site into content/_build/html; fails on any error or warning
npm run dev           # live-reloading site at http://localhost:3000
npm run all           # everything CI runs (for now, the build)
```

The first build fetches the site theme (a pinned commit of
[book-theme](https://github.com/myst-templates/book-theme)) with `git` into
`content/_build/templates/` (`scripts/fetch_theme.sh`); later builds reuse it.

To look at a built site, serve it from its root, for example
`npx serve content/_build/html`, rather than opening the files directly. The same applies
to the `site` artifact that CI attaches to every pull request.

## Layout

```
content/          the MyST project: myst.yml, the pages, _static/ (CSS, favicon)
scripts/          build_site.sh (the gated build), fetch_theme.sh
docs/plan/        the plan
templates/        page and test templates
.github/workflows ci.yml (build), deploy.yml (GitHub Pages)
```

## Licences

The content (everything under `content/`) is licensed under CC BY-SA 4.0
([LICENSE-CONTENT.md](LICENSE-CONTENT.md)); the code under MIT ([LICENSE](LICENSE)). See
[docs/plan/11-governance.md](docs/plan/11-governance.md).
