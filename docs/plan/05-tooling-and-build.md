# 5. Tooling and build

## 5.1 Requirements recap

Website only, highly interactive (sliders, interactive plots, in-browser Python later), heavy
LaTeX, theorem-style environments with cross-page references, search, free hosting on GitHub
Pages, authored by one maintainer plus AI agents in plain text, maintained for years. **PDF is
not a requirement.**

## 5.2 Options compared

Scale: ●●● excellent · ●● adequate · ● weak/DIY · ✗ not available

| Criterion | **MyST (mystmd / Jupyter Book 2)** | Quarto (website) | Material for MkDocs + KaTeX | Jupyter Book 1 (Sphinx) | Astro Starlight / Docusaurus | PreTeXt | Plain LaTeX (+ tex4ht/lwarp) |
|---|---|---|---|---|---|---|---|
| Math rendering quality/speed | ●●● KaTeX, macros in config | ●●● MathJax/KaTeX | ●● KaTeX/MathJax via arithmatex | ●● MathJax | ●● remark-math + rehype-katex | ●●● MathJax | ●●● print / ● web |
| Theorem/definition/proof envs | ●●● built-in `proof:*` + `{proof}`, dropdown option | ●●● built-in | ● admonitions only | ●● sphinx-proof extension | ✗ (custom MDX components) | ●●● native, semantic | ●●● amsthm |
| Numbering + cross-refs **across pages** | ●●● cross-page, **hover previews** | ● theorem refs across pages work in *books*, not websites; previews same-page only | ● manual anchors | ●●● | ● DIY | ●●● within one book | ●●● print / ● web |
| Exercises + hidden solutions | ●●● `{exercise}` / `{solution}`, dropdown | ●● via callouts | ● | ●● sphinx-exercise | ● DIY | ●●● incl. WeBWorK | ●● (exsheets etc.) |
| Interactive plots/widgets | ●●● `{anywidget}` (ES module + JSON state, no kernel), iframes, Mermaid | ●●● Observable JS built in; Pyodide via `quarto-live` | ●● raw HTML/JS | ●● | ●●● (it's a JS framework) | ●●● Desmos/GeoGebra/JSXGraph interactives | ✗ |
| In-browser Python | ●● JupyterLite/Thebe (**beta**) or a custom Pyodide widget | ●●● quarto-live | ● DIY | ●● Thebe | ● DIY | ●● Sage cells | ✗ |
| PDF export (not required) | ●● LaTeX/Typst | ●●● | ● | ●● | ✗ | ●●● | ●●● |
| Search | ●●● built-in client-side | ●●● | ●●● | ●● | ●●● (Pagefind/Algolia) | ●● | ✗ |
| Authoring by humans | ●●● Markdown | ●●● Markdown | ●●● Markdown | ●● MyST/rST | ●● MDX (JSX in Markdown) | ● XML | ●● LaTeX |
| Authoring by AI agents | ●●● well-known syntax, strict build warnings | ●●● | ●●● | ●● | ●● | ●● (verbose XML, schema-validated) | ●●● |
| GitHub Pages | ●●● static `myst build --html` | ●●● | ●●● | ●●● | ●●● | ●●● | ● |
| Long-term maintenance | ●● active (2i2c, Curvenote; v1.11.0 released 2026-09-21); younger project, frequent releases | ●●● Posit-backed, mature | ✗ **maintenance mode since Nov 2025** (successor Zensical) | ✗ superseded by JB2 | ●●● (big JS ecosystems, but more custom code for us) | ●●● stable academic community | ●●● |
| Fit for a cross-linked knowledge graph | **●●●** | ●● | ● | ●● | ● | ●● (one document per build) | ● |

### Decision: **MyST Markdown, built with `mystmd`** (the engine of Jupyter Book 2)

Reasons, in order of weight:
1. **Cross-page references with hover previews** for every labelled block. In a body of
   knowledge where definitions are cited everywhere, hovering "[continuous](#def-calc-continuity)"
   to see the definition is the single most valuable reader feature. Quarto websites can't do
   this for theorems, and the others need custom code.
2. **Math semantics built in**: definitions, theorems, proofs, examples, remarks, exercises
   and solutions, all numbered, labelled and collapsible, in standard MyST syntax (shared
   with Sphinx/Jupyter Book, so the content outlives any one tool).
3. **Interactivity without a server**: `{anywidget}` takes a plain ES module plus a JSON
   body. Content authors (and agents) write *configuration*, not JavaScript.
4. **Extensible in small doses**: a 100-line JS plugin renders our front-matter metadata
   (proved in the PoC).
5. Plain Markdown, static output, free hosting, client-side search.

**Runner-up: Quarto**, if cross-page hover previews didn't matter. It has more mature
interactivity (OJS) and corporate backing. **PreTeXt** would win if print/PDF were a primary
output.

**Accepted downsides and mitigations**
- *Younger tool, frequent releases*: pin the exact version, upgrade deliberately in a
  dedicated PR (weekly Dependabot), and gate upgrades on the full CI and a visual check
  of the exemplar pages.
- *In-page Python execution is beta*: not on the critical path (Phase 5). We can ship our
  own small Pyodide widget instead.
- *Theme customisation is limited* (React theme): we use the stock `book-theme` plus CSS
  only. Forking the theme is explicitly out of scope.

## 5.3 Proof of concept (2026-10-07, mystmd 1.11.0)

A throwaway two-page project was built in the sandbox (not committed). Findings:

| Question | Result |
|---|---|
| `proof:definition`, `proof:theorem`, `proof:example`, `{proof}` with `:class: dropdown` | ✔ build, labels kept, per-kind numbering per page |
| Cross-page `[](#label)`, `[{name}](#label)`, `[Theorem {number}](#label)` | ✔ resolved |
| Broken reference | reported as `⚠️ No target for internal reference "#…"` |
| Labels with `[a-z0-9-]` | ✔ unchanged in the AST and as HTML ids |
| `::::{exercise}` with nested `:::{admonition}` hint/answer dropdowns, `:class: tier-a` | ✔ classes `dropdown hint`, `dropdown answer`, `tier-a` preserved in the AST |
| `{solution} exr-…` | ✔ links to its exercise; labelled equations inside work |
| Unknown front-matter key `maths:` | one warning per page: `'frontmatter' extra key ignored: maths`; the key is dropped from MyST's output (we read it ourselves) |
| URLs with `site.options.folders: true` | nested URLs mirror the folders relative to `myst.yml`, so `myst.yml` lives in `content/` → `/calculus/limits/limit-laws` |
| `{anywidget} ../../../widgets/x.mjs` (outside the project root) + JSON body | ✔ module copied to `public/` with a content hash; the JSON body becomes the widget model |
| MyST JS plugin directive reading `vfile.path` and emitting `crossReference` nodes | ✔ MyST resolved them to page titles and URLs (so they get hover previews) |
| `myst build --strict` | the flag exists ("exit non-zero on any errors"). Whether extra-key warnings count could not be isolated, because the HTML theme download (`api.mystmd.org`) is blocked in the sandbox. CI therefore uses the log filter in §5.7. |
| SymPy 1.14 `parse_latex` | the `lark` backend **fails on `\pi`** → use the `antlr` backend (`antlr4-python3-runtime==4.11.*`), which handled every test answer. Normalise `e` → `E`. |

**Still to validate in Phase 0** (needs the real HTML build, which runs in GitHub Actions):
the rendered look of dropdown proofs and exercises, KaTeX macros with arguments, anywidget
rendering on the built site, search quality on math-heavy pages, and the build time with
about 100 pages.

## 5.4 Dependencies (each justified)

| Dependency | Version policy | Why | Alternative rejected |
|---|---|---|---|
| **Node.js 22 LTS** | `.nvmrc` | runtime for mystmd | – |
| **mystmd** | exact pin (`1.11.0`), lockfile | the site engine | `jupyter-book` 2 on PyPI wraps the same engine but adds a layer; we need npm for the plugin anyway |
| **yaml** (npm) | caret, lockfile | the plugin parses front matter properly | a hand-rolled regex (fragile) |
| **katex** (npm, dev) | exact, matching the theme's KaTeX | `scripts/check_katex.mjs` fails CI on math that would render as red error text (mystmd is a single bundled package, so KaTeX isn't otherwise importable) | relying on visual inspection |
| **JSXGraph** | exact version in the widget import URL; vendored copy as fallback | interactive geometry/plots: sliders, gliders, function graphs, keyboard support, small (≈ 300 kB), MIT/LGPL dual licence, maintained since 2008 by a university group | Plotly (heavy, data-viz oriented), D3 (too low-level), Desmos API (licence/API key for production, not version-controlled), GeoGebra (heavy, external) |
| **Python ≥ 3.12 + uv** | `uv.lock` | reproducible env for verification and checks; uv is fast and handles the lockfile | pip + requirements.txt (no lock), poetry (slower, heavier) |
| **sympy** | lock | symbolic verification of every computation | – |
| **antlr4-python3-runtime 4.11.x** | pinned (SymPy requires this exact minor) | SymPy's LaTeX parser backend (lark fails on `\pi`) | lark backend |
| **pytest** | lock | test runner, parametrisation, clear failure output | unittest (more boilerplate) |
| **pyyaml** | lock | front matter parsing in scripts | ruamel (round-trip not needed) |
| **jsonschema** | lock | front matter and widget config validation | hand-written validation |
| **codespell** | lock | spelling: few false positives on math-heavy text because it only flags *known* misspellings | cspell (needs a large allowlist for math tokens) |
| **lychee** (GitHub Action) | pinned action SHA | weekly external-link check | `myst build --check-links` (also usable; lychee gives a nicer report and runs on a schedule) |
| GitHub Actions: `actions/checkout`, `setup-node`, `astral-sh/setup-uv`, `upload-pages-artifact`, `deploy-pages` | pinned by SHA, Dependabot | CI and deploy | – |

Not used, on purpose: a CSS framework, a bundler (unless the JSXGraph CDN import proves
unreliable, then **esbuild** bundles widgets), a Markdown linter (the MyST build plus our
schema checks cover structure), and Jupyter kernels (pages are `.md`, not notebooks, so
nothing is executed at build time).

## 5.5 Repository skeleton (Phase 0 deliverable)

See [02 §2.2](02-information-architecture.md#22-repository-layout) for the full tree. Key
config files:

### `content/myst.yml`

```yaml
version: 1
project:
  id: 5c1b0f4e-…                     # generated once by `myst init`, never changed
  title: Maths: an open, verified university mathematics reference
  description: Definitions, theorems, proofs, worked examples and exercises — interactive and verified.
  github: https://github.com/vronnblom/maths
  license:
    content: CC-BY-SA-4.0
    code: MIT
  plugins:
    - ../plugins/topic-header.mjs
  math:
    '\R': '\mathbb{R}'
    # … full list in 04-notation-and-style §4.1
  numbering:
    title: false
    headings: false                   # numbering is per kind, per page (default)
  toc:
    - file: index.md
    - title: About
      children:
        - file: about/how-to-read.md
        - file: about/notation.md
        - file: about/status.md
        - file: about/errata.md
    - title: Calculus
      file: calculus/index.md
      children:
        - title: Preliminaries
          file: calculus/preliminaries/index.md
          children:
            - file: calculus/preliminaries/real-numbers-and-intervals.md
            # …
        - title: Limits
          file: calculus/limits/index.md
          children:
            - file: calculus/limits/limit-of-a-function.md
            - file: calculus/limits/limit-laws.md
            # …
site:
  template: book-theme
  options:
    folders: true                      # URLs mirror folders
    logo_text: Maths
    favicon: _static/favicon.svg
    style: _static/custom.css          # tier/status badges, rigor dropdown styling
  nav: []
  actions:
    - title: Report an error
      url: https://github.com/vronnblom/maths/issues/new?template=erratum.yml
```

If the toc grows unwieldy (more than about 300 lines), split it per subject with MyST's
`extends:` mechanism. Check first whether `extends` merges `toc` entries; otherwise
`scripts/check_toc.py` can generate the toc from `curriculum.yml` files. That is deferred
until it's needed.

### `package.json`

```json
{
  "name": "maths",
  "private": true,
  "type": "module",
  "engines": { "node": ">=22" },
  "scripts": {
    "dev": "cd content && myst start",
    "build": "cd content && myst build --html --strict --ci",
    "check": "uv run python scripts/check_all.py",
    "verify": "uv run pytest verify -q",
    "all": "npm run check && npm run verify && npm run build"
  },
  "dependencies": { "mystmd": "1.11.0", "yaml": "^2.8.0" },
  "devDependencies": { "katex": "<pinned to the theme's version>" }
}
```

### `pyproject.toml`

```toml
[project]
name = "maths-tooling"
version = "0"
requires-python = ">=3.12"
dependencies = [
  "sympy>=1.14,<2",
  "antlr4-python3-runtime==4.11.*",
  "pytest>=8",
  "pyyaml>=6",
  "jsonschema>=4.23",
  "codespell>=2.3",
]

[tool.pytest.ini_options]
testpaths = ["verify"]
addopts = "-ra --strict-markers"

[tool.codespell]
skip = "*.lock,*.json,_build,node_modules"
ignore-words = ".codespell-ignore"
```

## 5.6 Local development workflow

```bash
# one-time
nvm use && npm ci          # mystmd + yaml
uv sync                    # Python env for checks and verification

# while writing
npm run dev                # live-reloading site at http://localhost:3000
uv run pytest verify/calculus/limits -q   # verify the topic you are working on

# before pushing (the same as CI)
npm run all
```

`myst start` rebuilds on save and shows warnings (broken refs, unknown directives) in the
terminal. Agents in Claude Code cloud sessions get the same environment through a
SessionStart hook (Phase 0) that runs `npm ci && uv sync`.

## 5.7 CI and deployment

### `.github/workflows/ci.yml` (on every PR and on push to `main`)

```yaml
name: CI
on:
  pull_request:
  push: { branches: [main] }
concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: astral-sh/setup-uv@<sha>
      - run: uv sync --frozen
      - name: Front matter, labels, graph, toc, coverage
        run: uv run python scripts/check_all.py --format github   # emits ::error file=…,line=…:: annotations
      - name: Spelling
        run: uv run codespell content docs templates

  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: astral-sh/setup-uv@<sha>
      - run: uv sync --frozen
      - uses: actions/setup-node@<sha>
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - name: Build AST (needed for answer extraction)
        run: cd content && npx myst build --site --ci
      - run: uv run python scripts/extract_answers.py content/_build/site/content > verify/_answers.json
      - run: uv run pytest verify -q

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: actions/setup-node@<sha>
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - name: Build site (warnings are errors, except the whitelisted one)
        env: { BASE_URL: /maths }
        run: |
          cd content
          # Actions' default bash runs with -o pipefail, so a non-zero myst exit fails the step.
          # Phase 0: if --strict turns out to count the whitelisted `maths` warning as an error,
          # drop --strict; the grep filter below is the real gate either way.
          npx myst build --html --strict --ci 2>&1 | tee build.log
          # fail on any warning except the expected `maths` front-matter key
          if grep '⚠️' build.log | grep -v "extra key ignored: maths"; then
            echo "::error::MyST build produced warnings"; exit 1; fi
      - uses: actions/upload-artifact@<sha>          # downloadable preview of the PR's site
        with: { name: site, path: content/_build/html, retention-days: 7 }
```

### `.github/workflows/deploy.yml` (on push to `main`)

```yaml
name: Deploy
on: { push: { branches: [main] }, workflow_dispatch: {} }
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: false }
jobs:
  deploy:
    environment: { name: github-pages, url: '${{ steps.d.outputs.page_url }}' }
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: actions/setup-node@<sha>
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - run: cd content && npx myst build --html --ci
        env: { BASE_URL: /maths }
      - uses: actions/upload-pages-artifact@<sha>
        with: { path: content/_build/html }
      - id: d
        uses: actions/deploy-pages@<sha>
```

Branch protection on `main`: require `checks`, `verify` and `build`; require one approving
review (the owner); linear history (squash merge).

### `.github/workflows/links.yml`

This runs weekly (cron) plus manual dispatch. It runs lychee over the built HTML and opens or
updates an issue "External links report" if anything is broken. It never blocks PRs, because
external sites flake.

### PR previews

Phase 0 uses the `site` build artifact (download, unzip, open). If reviewing widgets that way
proves painful, add free Cloudflare Pages or Netlify PR previews. This is an open question
in [12](12-risks-and-open-questions.md).

## 5.8 Widgets

- Every widget is one ES module in `widgets/` exporting `{ render({ model, el }) }` (the
  anywidget contract). It imports JSXGraph from a pinned URL:
  `import JXG from "https://cdn.jsdelivr.net/npm/jsxgraph@<exact>/distrib/jsxgraphcore.mjs"`.
- **Configuration is JSON only**, so authors never write JS:

  ````markdown
  ```{anywidget} ../../../widgets/epsilon-delta.mjs
  {
    "id": "wdg-calc-limit-eps-delta",
    "f": "x^2", "a": 2, "L": 4,
    "eps": 0.5, "epsRange": [0.05, 1.5],
    "xRange": [0, 3.5], "yRange": [0, 9],
    "description": "Graph of y = x² near x = 2 with a horizontal band of half-width ε around y = 4 and a vertical band of half-width δ around x = 2. Dragging ε shrinks the band; the widget shows the largest δ that keeps the graph inside the band."
  }
  ```
  ````
- Expressions (`"f": "x^2"`) are compiled with JSXGraph's built-in JessieCode parser, so
  there is no `eval` and no extra dependency.
- Each widget has a JSON Schema (`schema/widgets/<name>.schema.json`); `check_all.py`
  validates every widget block in the content.
- Shared helpers in `widgets/_lib/` handle board creation, theme-aware colours (light/dark),
  keyboard-operable sliders, and rendering `description` as visually-hidden text plus a
  `<noscript>` fallback.
- **Catalogue** (built as the curriculum needs them, see 08): `function-plot` (graphs plus
  parameter sliders), `epsilon-delta`, `secant-tangent`, `zoom-to-linear`, `riemann-sum`,
  `area-accumulation` (FTC), `taylor`, `partial-sums`, `slope-field`, `newton-method`,
  `solid-of-revolution` (JSXGraph 3D), `prereq-graph` (Phase 7).
- Desmos/GeoGebra are allowed **only** as optional "explore further" links, never as core
  content: they are not version-controlled, may change or vanish, and have their own terms.
- A widget's *mathematics* is verified too: the δ that `epsilon-delta` reports is computed in
  JS, and a small Node test (`widgets/_tests/*.test.mjs`, run with `node --test`, no extra
  dependency) checks it against known values.
