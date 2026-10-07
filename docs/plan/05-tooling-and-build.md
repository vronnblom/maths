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
| Theorem/definition/proof envs | ●●● built-in `proof:*` (incl. `proof:proof`), dropdown option | ●●● built-in | ● admonitions only | ●● sphinx-proof extension | ✗ (custom MDX components) | ●●● native, semantic | ●●● amsthm |
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
| `proof:definition`, `proof:theorem`, `proof:example`, `{proof}` with `:class: dropdown` | ✔ build, labels kept, per-kind numbering per page. Found in review: a bare `{proof}` has no kind, so the theme heads it with just a number ("1 (Rigorous proof)"). We use `{proof:proof}` + `:enumerated: false`, which renders "Proof" / "Proof (Rigorous track)". The theme draws no ∎. |
| Cross-page `[](#label)`, `[{name}](#label)`, `[Theorem {number}](#label)` | ✔ resolved |
| Broken reference | reported as `⚠️ No target for internal reference "#…"` |
| Labels with `[a-z0-9-]` | ✔ unchanged in the AST and as HTML ids |
| `::::{exercise}` with nested `:::{admonition}` hint/answer dropdowns, `:class: tier-a` | ✔ classes `dropdown hint`, `dropdown answer`, `tier-a` preserved in the AST |
| `{solution} exr-…` | ✔ links to its exercise; labelled equations inside work |
| Unknown front-matter key `maths:` | one warning per page: `'frontmatter' extra key ignored: maths`; the key is dropped from MyST's output (we read it ourselves) |
| URLs with `site.options.folders: true` | nested URLs mirror the folders relative to `myst.yml`, so `myst.yml` lives in `content/` → `/calculus/limits/limit-laws` |
| `{anywidget} ../../../widgets/x.mjs` (outside the project root) + JSON body | ✔ module copied to `public/` with a content hash; the JSON body becomes the widget model. Found in review: **only that one file** is copied (its imports are not followed), and a JSON `"id"` is not a label; see §5.8. |
| MyST JS plugin directive reading `vfile.path` and emitting `crossReference` nodes | ✔ MyST resolved them to page titles and URLs (so they get hover previews) |
| `myst build --strict` | the flag exists. Found in review: it exits non-zero only on errors (logged with ⛔️), not on warnings (⚠️), and some errors (an unknown directive) still exit 0. Hence the log filter in `scripts/build_site.sh` (§5.5). |
| Theme download | blocked in the sandbox. Found in review: `api.mystmd.org` answers; the denied host is github.com, where `book-theme` resolves to `main.zip`. Hence the pinned theme (§5.5). Resolved in Phase 0 stage 1 with a git fetch of the pinned commit (§5.5). |
| SymPy 1.14 `parse_latex` | the `lark` backend **fails on `\pi`** → use the `antlr` backend (`antlr4-python3-runtime==4.11.*`). Found in review: it returns `\pi` and `e` as free symbols, drops list items after the first comma, and leaves `\frac{1}{2}` unevaluated, so `parse_answer` post-processes its output (06 §6.1). |
| Number-only inline math | found in review: mystmd turns `$0.69$`, `$6$`, `$-3$` into plain text nodes in the AST (always on). `extract_answers.py` handles this (06 §6.1). |

**Validated in Phase 0 stage 1** (2026-10-07, mystmd 1.11.0, book-theme v1.4.1 at the pinned
commit). The real `myst build --html` ran in a Claude Code cloud session, with the theme
fetched by git (§5.5), and the pages were inspected with Playwright (Chromium, light and
dark colour schemes):

| Question | Result |
|---|---|
| KaTeX macros with arguments | ✔ every macro of 04 §4.1 renders on `about/notation.md` (114 formulas, 0 `.katex-error` nodes, no console errors), including `\dv`, `\dvn`, `\pdv`, `\abs`, `\norm` and `\vb`, inline, in table cells and in displays (where `\abs` and `\norm` grow with their contents). |
| How math is rendered | mystmd renders every formula **at build time** with its own bundled KaTeX **0.15.6** (the theme bundles the same 0.15.6 and loads `katex@0.15.2` CSS from jsDelivr; Mermaid has its own 0.16.47). A parse error is logged as `⛔️ <file>:<line> <KaTeX message>` and `--strict` exits 1, so `build_site.sh` already fails on red KaTeX (tested with `$\frac{1}{$`). |
| Dropdowns | ✔ (on a scratch page, not committed) `{proof:proof} Rigorous track` + `:class: dropdown` renders as a collapsed `<details>` headed "Proof (Rigorous track)"; hint, answer and solution dropdowns inside and after an `{exercise}` collapse and open; custom classes (`tier-b`, `rigor`, `hint`, `answer`) reach the HTML. `custom.css` tier tags and the ∎ after proofs work. |
| Search | ✔ Ctrl+K opens it; "interval", "arsinh" and "errata" find the right headings and table rows. It indexes the **LaTeX source** of formulas (a hit shows `\int_0^1 x^2 \dd x`), so searching for a symbol works by its command name only. |
| Equation numbers | Every display `$$ … $$` is numbered, labelled or not (the notation page shows (1)–(4)). |
| Favicon, actions, licences | ✔ the SVG favicon is served as `/favicon.ico`; "Report an error" sits in the header; the CC BY-SA and MIT badges and the GitHub link show on every page. |
| Build time | about 10 s for 6 pages, including the one-off `npm ci` of the theme (3 s). |

A `BASE_URL=/maths` build prefixes every link and asset in the HTML, the favicon included.

**Validated in Phase 0 stage 3** (2026-10-07, the `function-plot` widget on
`about/how-to-read.md` and a fixture project built from the templates; Playwright, Chromium):

| Question | Result |
|---|---|
| anywidget rendering | ✔ The theme's AnyRenderer `import()`s the hashed module (`/build/function-plot-<hash>.mjs`), attaches an **open shadow root** to the figure's `<div class="myst-anywidget">`, and calls `render({ model, el })` with `el` inside it; `model.get(key)` returns the keys of the JSON body. Page CSS does not reach into the shadow root (inherited properties such as the text colour and the font do), so a widget brings its own `<style>`. |
| `render()` lifecycle | The theme calls `render()` **more than once** while the page hydrates, and awaits it; it calls the returned cleanup on unmount, but a render still awaiting JSXGraph at that moment never gets its cleanup. So `render()` replaces `el`'s content, returns early if `el` is no longer connected after the `await`, and returns a cleanup. |
| `_lib/` next to the hashed module | ✔ `project.static_files: [../widgets/_lib]` publishes it at `/_lib/` **and** `/build/_lib/`, so `./_lib/x.mjs` from `/build/function-plot-<hash>.mjs` resolves (all 200). |
| JSXGraph from jsDelivr | ✔ `await import("https://cdn.jsdelivr.net/npm/jsxgraph@1.14.0/distrib/jsxgraphcore.mjs")` inside `render()`; the board draws inside the shadow root. |
| Text fallback | ✔ With the JSXGraph URL blocked, the module and `_lib/` still load, the widget says "The interactive figure could not be loaded. The caption describes it.", and the caption reads normally. With **all** of jsDelivr blocked the caption is still there, but its formulas show twice (as MathML and as HTML), because the theme loads KaTeX's CSS from jsDelivr too (§5.3 stage 1, 12 R8). |
| Keyboard | ✔ Tab reaches each slider and button; ArrowRight moves a slider by its step, and `aria-valuetext` announces "a = 1.5". |
| Colour schemes | ✔ Light and dark (the theme's `html.dark`/`html.light` class, else `prefers-color-scheme`), also when switched while the page is open; phone width (375 px) works. |
| Under `/maths/` | ✔ A `BASE_URL=/maths` build served under `/maths/` loads `/maths/build/function-plot-<hash>.mjs`, `/maths/build/_lib/*.mjs` and JSXGraph, and the widget works as above. |
| Plugin | ✔ `vfile.message(…)` with `fatal = true` logs `⛔️ <file>:<line> …` (a thrown error also logs ⛔️, without the line). `ctx.parseMyst()` parses inline Markdown and math. A `span` or `div` node with a `class`, and `admonition` with `class`, reach the HTML. |

**Validated in Phase 0 stage 4** (2026-10-07, mystmd 1.11.0, SymPy 1.14.0,
antlr4-python3-runtime 4.11.1):

| Question | Result |
|---|---|
| Deployed site | ✔ Once the owner enabled Pages, Deploy run 4 on `main` succeeded. `https://vronnblom.github.io/maths/` serves every page. On `/maths/about/how-to-read/` (Playwright, Chromium) the hashed `function-plot` module, all six `/maths/build/_lib/*.mjs` and JSXGraph load (200), the widget draws its board in the shadow root with its 4 sliders, its table shows 0, 0.479426, 0.841471, 0.997495, 0.909297 (the SymPy fixture), and there are no console errors. |
| Is a KaTeX check needed besides the build gate? | **No.** Through `myst_gate.sh`, in `--md` and in `--html` with the real theme, each of these is a `⛔️ <file>:<line> <KaTeX message>` error that fails the build: an unknown macro (`\foo{x}`), a command KaTeX does not support (`\bbox[5px]{x}`, `\mathbbm{1}`), a project macro missing an argument (`\dv{x}`, `\abs` alone), an unclosed `\frac{1}{`. The same holds inline, in displays, in a `{math}` directive, in a heading, in a directive title, in a figure caption, in an exercise's Answer and in an objective rendered by the plugin. mystmd also marks the node `"error": true` in the AST. So `scripts/check_katex.mjs` and the `katex` devDependency are dropped (06 §6.4); the `gate-katex-*` fixtures in `tests/` keep the evidence. |
| Math in front-matter `title`/`description` | Not rendered at all: the theme shows `$\foo$` literally, in the page heading and the `<title>`, and the build reports nothing (it is not math to KaTeX). No check could catch a KaTeX error there, and none is needed; titles simply carry no math (the curriculum's titles have none). |
| How answers look in the AST | Number-only inline math is a `text` node (`$-3$`, `$0.69$`, `$+5$`, `$-0.5$`). A power of plain numbers is a `span` of `text` + `superscript` (`$2^{10}$`, `$10^{-3}$`, `$2^{-1}$`); anything with a letter stays `inlineMath` (`$x^2$`, `$e^{2}$`, `$2^x$`, `$x_1$`). `verify/fixtures/answers-ast.json` pins these shapes. |
| SymPy's `parse_latex(…, backend="antlr")` | It takes `strict=True` (without it, `-2, 4` reads as `-2`), but it is **far more forgiving** than 06 assumed: an unknown command becomes a symbol of that name (`\approx 0.69` → `approx·0.69`; `\text{True}` → a product of letters; `\lvert x \rvert` → `lvert·rvert·x`), a bare `\log` is the natural logarithm, a decimal is a 15-digit float, `\pi`/`e` are symbols, and `\frac{1}{2}` stays `Pow(2, -1)`. So `parse_answer` allowlists commands and rejects multi-letter names (06 §6.1). |

**Still to validate**: search quality on math-heavy topic pages, and the build time with
about 100 pages.

## 5.4 Dependencies (each justified)

| Dependency | Version policy | Why | Alternative rejected |
|---|---|---|---|
| **Node.js 22 LTS** | `.nvmrc` | runtime for mystmd | – |
| **mystmd** | exact pin (`1.11.0`), lockfile | the site engine | `jupyter-book` 2 on PyPI wraps the same engine but adds a layer; we need npm for the plugin anyway |
| **yaml** (npm) | caret, lockfile | the plugin parses front matter properly | a hand-rolled regex (fragile) |
| **book-theme** (site theme, downloaded by mystmd) | commit SHA in `site.template` (§5.5) | the stock MyST web theme | an unpinned `template: book-theme` (follows the theme's `main`) |
| ~~**katex** (npm, dev)~~ | **dropped in stage 4** | It was for `scripts/check_katex.mjs`, a check for math that would render as red error text. Stage 4 showed that every kind of KaTeX error is a `⛔️` error in mystmd's own build-time rendering (bundled KaTeX 0.15.6), which the gated build already fails on (§5.3), so neither the script nor the dependency is needed. The `verify` job's `--site` build is not gated, but the `build` job's is, on the same pages | – |
| **JSXGraph** | exact version (**1.14.0**) in the URL that widgets `import()` at render time (`widgets/_lib/jsxgraph.mjs`); vendored copy as a manual fallback | interactive geometry/plots: sliders, gliders, function graphs, keyboard support, small (≈ 300 kB), MIT/LGPL dual licence, maintained since 2008 by a university group | Plotly (heavy, data-viz oriented), D3 (too low-level), Desmos API (licence/API key for production, not version-controlled), GeoGebra (heavy, external) |
| **jsxgraph** (npm, dev) | exact, the **same** version as the URL above (a test checks it) | the widget tests run expressions through JSXGraph's JessieCode, the evaluator the browser uses (§5.8). Checked in stage 3: the package's `distrib/jsxgraphcore.mjs` (the file jsDelivr serves) imports in Node 22 and compiles JessieCode on a board with JSXGraph's `NoRenderer`, no DOM needed. It is never published or imported by the site | a second, hand-written evaluator for the tests (the tests would then not check what readers see) |
| **Python ≥ 3.12 + uv** | `uv.lock` | reproducible env for verification and checks; uv is fast and handles the lockfile | pip + requirements.txt (no lock), poetry (slower, heavier) |
| **sympy** | lock | symbolic verification of every computation | – |
| **antlr4-python3-runtime 4.11.x** | pinned (SymPy requires this exact minor) | SymPy's LaTeX parser backend (lark fails on `\pi`) | lark backend |
| **pytest** | lock | test runner, parametrisation, clear failure output | unittest (more boilerplate) |
| **pyyaml** | lock | front matter parsing in scripts | ruamel (round-trip not needed) |
| **jsonschema** | lock | front matter and widget config validation | hand-written validation |
| **codespell** | lock | spelling: few false positives on math-heavy text because it only flags *known* misspellings | cspell (needs a large allowlist for math tokens) |
| **lychee** (GitHub Action) | pinned action SHA (`lycheeverse/lychee-action` v2.9.0, which pins lychee 0.24.2) | weekly external-link check (`links.yml`, §5.7) | `myst build --check-links` (also usable; lychee gives a nicer report and runs on a schedule) |
| GitHub Actions: `actions/checkout`, `setup-node`, `astral-sh/setup-uv`, `upload-pages-artifact`, `deploy-pages` | pinned by SHA, Dependabot | CI and deploy | – |

**Dependabot** (`.github/dependabot.yml`, stage 5) opens weekly PRs for three ecosystems:
- `github-actions`: every action is pinned by SHA with the tag in a comment; Dependabot updates
  both, grouped into one PR;
- `npm`: everything except **mystmd** and **jsxgraph**, which it ignores. mystmd is pinned
  exactly and moves only together with the theme pin, in one hand-made upgrade PR with the
  visual check (§5.5); Dependabot doesn't know the theme pin, so a mystmd bump alone would
  pair a new engine with an old theme. jsxgraph must equal the version in the widgets' import
  URL (a widget test checks it), so it also moves by hand, both at once;
- `uv`: Dependabot supports `uv.lock` (since March 2025).
  `versioning-strategy: lockfile-only` keeps it to lockfile updates within `pyproject.toml`'s
  ranges. The default strategy would raise the lower bounds in `pyproject.toml`, and a range
  such as `antlr4-python3-runtime==4.11.*` (which SymPy requires) must only change by hand.
  The updates are grouped into one PR.

The theme pin itself is outside every ecosystem Dependabot knows (§5.5).

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
  title: 'Maths: an open, verified university mathematics reference'   # quoted: contains ": "
  description: Definitions, theorems, proofs, worked examples and exercises — interactive and verified.
  github: https://github.com/vronnblom/maths
  license:
    content: CC-BY-SA-4.0
    code: MIT
  plugins:
    - ../plugins/topic-header.mjs
  static_files:                       # mystmd publishes only the .mjs named in {anywidget};
    - ../widgets/_lib                 # helpers it imports must be copied explicitly (§5.8)
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
  # Pinned to a commit (the theme repo has no tags). `template: book-theme` would fetch the
  # theme's `main` branch on every fresh runner, outside the version pin (see below).
  template: https://github.com/myst-templates/book-theme/archive/<commit-sha>.zip   # stage 1: 23f2df5… (v1.4.1)
  options:
    folders: true                      # URLs mirror folders
    logo_text: Maths
    favicon: _static/favicon.svg
    style: _static/custom.css          # tier/status badges, `rigor` dropdowns, a ∎ after proofs
  nav: []
  actions:
    - title: Report an error
      url: https://github.com/vronnblom/maths/issues/new?template=erratum.yml
```

**The theme is a dependency too.** mystmd downloads the site theme at build time; it is not
an npm package, so neither the mystmd pin, the lockfile nor Dependabot covers it. The
`<commit-sha>` above is the pin. It is bumped only in the same dedicated upgrade PRs as
mystmd (with the visual check of the exemplar pages). CI and deploy cache `content/_build/templates` keyed on the
SHA alone, which a step greps from `myst.yml` (keying on a hash of the whole `myst.yml`
would miss on every toc change, i.e. on almost every topic PR).

**The pinned theme (Phase 0 stage 1).** `23f2df5493e23dfb1d9433c8aa64c87beb4232a3` is
book-theme's `main` on 2026-10-07: the commit "🚀 v1.4.1", published on 2026-09-21 together
with mystmd 1.11.0. It is a *built* template (`template.yml`, `server.js`, `build/`,
`public/`), and the site builds with it under mystmd 1.11.0. Its KaTeX is 0.15.6 (§5.3).

**How the theme reaches cloud sessions.** Claude Code cloud sessions get HTTP 403 from
github.com for the archive zip, but `git fetch` of a public repository works. mystmd 1.11
resolves a URL template to `content/_build/templates/site/<sha256 of the URL>/` and
**skips the download when `template.yml` exists there**; it then runs the template's install
command (`npm ci --ignore-scripts`, from the npm registry) once, if that folder has no
`node_modules/`. So `scripts/fetch_theme.sh` reads the URL from `myst.yml`, `git fetch`es
that commit (`--depth 1`) and extracts it with `git archive` into exactly that folder. It is
a no-op when the folder is already populated (e.g. restored from the CI cache).
`build_site.sh` and `npm run dev` call it first, so every environment (local, CI, deploy,
cloud sessions) gets the theme the same way, and the zip URL stays in `myst.yml` as the pin
and as mystmd's fallback for a bare `myst build`. A fetch by commit SHA is
content-addressed, so it cannot drift from the pin. Neither a network-settings change nor a
vendored theme is needed.

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
    "generate": "uv run python scripts/generate.py",
    "dev": "npm run generate && bash scripts/fetch_theme.sh && cd content && myst start",
    "check": "uv run python scripts/check_all.py && uv run codespell content docs templates && uv run pytest tests -q",
    "ast": "npm run generate && bash scripts/fetch_theme.sh && cd content && myst build --site --ci",
    "verify": "npm run ast && uv run python scripts/extract_answers.py content/_build/site/content -o verify/_answers.json && uv run pytest verify -q && uv run python scripts/check_coverage.py",
    "test:widgets": "node --test \"widgets/_tests/*.test.mjs\" \"plugins/_tests/*.test.mjs\"",
    "build": "npm run generate && bash scripts/build_site.sh",
    "all": "npm run check && npm run verify && npm run test:widgets && npm run build"
  },
  "dependencies": { "mystmd": "1.11.0", "yaml": "^2.8.0" },
  "devDependencies": { "jsxgraph": "1.14.0" }
}
```

The npm scripts are the **only** definition of each step: CI calls the same scripts, so
`npm run all` really is "everything CI runs".
This is `package.json` since stage 4, the end state of Phase 0 (stage 4 dropped the planned
`katex` devDependency and the KaTeX step of `verify`, §5.3).
- `ast` fetches the pinned theme first (`--site` needs it, like `--html`), so `npm run verify`
  works from a clean checkout.
- `test:widgets` also runs the plugin's tests (`plugins/_tests/`), whose logic is the same kind
  of pure module (03 §3.6); stage 3 added that second glob.
- `generate` writes the generated includes (§5.7, "Generated content") before any build.
- `verify` always rebuilds the AST and re-extracts the answers, so tests never read a stale
  `verify/_answers.json`. Run alone, `pytest verify` refuses a missing or stale one (06 §6.1).
- `check_coverage.py` reads the coverage that the pytest run just recorded (06 §6.1), so it
  runs after `pytest`.
- `node --test` is given a glob. A bare directory argument is treated as a module on Node 22
  and fails with "Cannot find module".

### `scripts/build_site.sh` (the one site build, used by `npm run build`, CI and deploy, redirects included)

```bash
#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
bash "$here/fetch_theme.sh"           # the pinned theme, via git (no-op when cached)
cd "$here/../content"
bash "$here/myst_gate.sh" --html      # errors and warnings fail, except the whitelisted one
# Redirect pages for moved pages (02 §2.3). Run here, not only on deploy, so a redirect that
# collides with a live page fails the PR. Reads BASE_URL (/maths on deploy) like mystmd.
uv run python "$here/write_redirects.py" _build/html
```

The gate itself is `scripts/myst_gate.sh`, so that `tests/test_build_gate.py` can run it on
fixture projects (a broken reference, an unknown directive) in the `checks` job:

```bash
#!/usr/bin/env bash
set -euo pipefail            # pipefail: a non-zero myst exit survives the pipe into tee
myst build "$@" --strict --ci 2>&1 | tee build.log
# --strict exits non-zero only on errors. mystmd 1.11 prints errors with ⛔️ (some, e.g. an
# unknown directive, even with exit code 0) and warnings with ⚠️. Both fail the build, except
# the one expected warning about our `maths` front-matter key.
if grep -E '⛔️|⚠️' build.log | grep -v "extra key ignored: maths"; then
  echo "::error::MyST build produced errors or warnings"; exit 1
fi
```

The fixture tests can't use `--html` (no theme in `checks`). Found in stage 2: a bare
`myst build`, or `--site` without a site config, reports an unknown directive but not a broken
reference, because references are resolved only for an export. `myst build <page> --md --force`
resolves them and logs the same ⛔️/⚠️ lines in about a second without a theme, so the
tests use that.

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
testpaths = ["verify", "tests"]          # verify/: mathematics; tests/: the checkers' fixture tests
pythonpath = ["verify", "scripts"]       # `import mathcheck`, and the checkers for tests/
# importlib mode: test files may share a basename (every chapter has a verify/…/test_index.py)
addopts = "-ra --strict-markers --import-mode=importlib"

[tool.codespell]
skip = "*.lock,*.json,*.css,_build,_generated,node_modules,build.log"   # CSS is code (property names are US English); _generated/ is rebuilt
ignore-words = ".codespell-ignore"       # allowlist, seeded with `crossreference` (a MyST node type)
builtin = "clear,rare"
# Our US→GB list first, then "-" (codespell's default dictionary). The default dictionaries
# accept US spellings, and the built-in en-GB_to_en-US flags the British ones, so en-GB is
# enforced by a curated list (normalize->normalise, behavior->behaviour, color->colour, …).
# Words that are also class names or code identifiers stay out of the list: `rigor`, `center`,
# `license` (the LICENSE file, `license:` in myst.yml and package.json), and GitHub's
# `labeled`, `synchronize`, `artifact`.
dictionary = ".codespell-en-gb.txt,-"
```

`.codespell-en-gb.txt` has one `us->gb` pair per line and nothing else: codespell reads every
line as a pair, so the file can't hold comments.

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
SessionStart hook (`.claude/hooks/session-start.sh`, 10 §10.6) that runs `npm ci` (only
when `node_modules/` doesn't match the lockfile), `uv sync --frozen` and `fetch_theme.sh`, so
the theme is there before the first build (see "How the theme reaches cloud sessions" in §5.5).

## 5.7 CI and deployment

### `.github/workflows/ci.yml` (on every PR and on push to `main`)

Every job calls the npm scripts from §5.5, so CI and `npm run all` cannot drift apart (the
PR-only label guard is a separate workflow, `guard.yml`, below). A
`run:` step without `shell:` runs as `bash -e {0}`, with no pipefail. That is why pipelines
live in `scripts/build_site.sh` (`set -euo pipefail`), not inline in the YAML.

```yaml
name: CI
on:
  pull_request:                                 # default types: label changes don't re-run CI
  push:
    branches: [main]
concurrency:
  group: 'ci-${{ github.ref }}'
  cancel-in-progress: true

jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: astral-sh/setup-uv@<sha>
      - run: uv sync --frozen
      - uses: actions/setup-node@<sha>               # tests/test_build_gate.py runs myst on fixtures
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - name: Front matter, labels, graph, toc, notation lint, widgets, spelling, checker fixture tests
        run: npm run check                           # check_all.py emits ::error file=…,line=…:: annotations

  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: astral-sh/setup-uv@<sha>
      - run: uv sync --frozen
      - uses: actions/setup-node@<sha>
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - id: theme                                    # the pinned theme commit from myst.yml (§5.5)
        run: echo "sha=$(grep -oE 'book-theme/archive/[0-9a-f]{40}' content/myst.yml | cut -d/ -f3)" >> "$GITHUB_OUTPUT"
      - uses: actions/cache@<sha>                    # the pinned theme; --site needs it too
        with: { path: content/_build/templates, key: 'theme-${{ steps.theme.outputs.sha }}' }
      - name: AST, answers, SymPy verification, coverage gate
        run: npm run verify
      - name: Widget maths
        run: npm run test:widgets

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: astral-sh/setup-uv@<sha>                # `generate` (the prerequisite map, status table) is Python
      - run: uv sync --frozen
      - uses: actions/setup-node@<sha>
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - id: theme                                    # the pinned theme commit from myst.yml (§5.5)
        run: echo "sha=$(grep -oE 'book-theme/archive/[0-9a-f]{40}' content/myst.yml | cut -d/ -f3)" >> "$GITHUB_OUTPUT"
      - uses: actions/cache@<sha>                    # keyed on that commit only, so toc edits still hit
        with: { path: content/_build/templates, key: 'theme-${{ steps.theme.outputs.sha }}' }
      - name: Build site (errors and warnings fail, except the whitelisted one)
        run: npm run build                           # no BASE_URL: the preview is served from its root
      - uses: actions/upload-artifact@<sha>          # downloadable preview of the PR's site
        with: { name: site, path: content/_build/html, retention-days: 7, if-no-files-found: error }
```

### `.github/workflows/guard.yml` (the verified-page edit guard, PRs only)

The one check that reads PR labels (06 §6.6). It is a workflow of its own so that it alone
re-runs when a label is added or removed: adding `typo-only` turns it green without a new
push, while labelling a PR for triage doesn't re-run the full CI.

```yaml
name: Guard
on:
  pull_request:
    types: [opened, synchronize, reopened, labeled, unlabeled]
concurrency:
  group: 'guard-${{ github.ref }}'
  cancel-in-progress: true

jobs:
  verified-edits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
        with: { fetch-depth: 0 }                     # diffs against the base commit
      - uses: astral-sh/setup-uv@<sha>
      - run: uv sync --frozen
      - name: Verified-page edit guard
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          PR_LABELS: ${{ toJSON(github.event.pull_request.labels.*.name) }}
        run: uv run python scripts/check_verified_edits.py --base "$BASE_SHA" --labels "$PR_LABELS"
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
      - uses: astral-sh/setup-uv@<sha>
      - run: uv sync --frozen
      - uses: actions/setup-node@<sha>
        with: { node-version-file: .nvmrc, cache: npm }
      - run: npm ci
      - id: theme                                    # the pinned theme commit from myst.yml (§5.5)
        run: echo "sha=$(grep -oE 'book-theme/archive/[0-9a-f]{40}' content/myst.yml | cut -d/ -f3)" >> "$GITHUB_OUTPUT"
      - uses: actions/cache@<sha>                    # keyed on that commit only, so toc edits still hit
        with: { path: content/_build/templates, key: 'theme-${{ steps.theme.outputs.sha }}' }
      - run: npm run build                           # the same gated build as CI, redirects included
        env: { BASE_URL: /maths }
      - uses: actions/upload-pages-artifact@<sha>
        with: { path: content/_build/html }
      - id: d
        uses: actions/deploy-pages@<sha>
```

Branch protection on `main`: require `checks`, `verify`, `build` (ci.yml) and `verified-edits`
(guard.yml); require one approving review (the owner); linear history (squash merge).

### `.github/workflows/links.yml`

This runs weekly (cron, Monday morning UTC) plus manual dispatch, never on pull requests, so it
never blocks one: external sites flake. It builds the site with `npm run build` and runs lychee
over the HTML. `--root-dir` turns root-relative links into `file://` links, which
`--scheme https --scheme http` leaves out, so only external links are checked (internal ones
are the build gate's job); a 429 counts as fine. Then `scripts/links_report.sh` keeps one issue,
"External links report", in step: opened or updated with lychee's report when links are
broken, closed when they all pass again. Only runs on `main` touch the issue (a dispatch on a
branch writes just the job summary). The workflow has `permissions: {}` and its one job
`contents: read` and `issues: write`. A lychee error that isn't a broken link (bad arguments,
no input) fails the run.

Stage 5 ran lychee 0.24.2 locally on the build with the same arguments: 43 external links
fine and 12 redirected; the only errors were the 19 links to github.com (the repository,
`issues/new`, the theme's `edit/main/…` links), because cloud sessions get 403/404 for
github.com web pages. Those are checked for real on the runner.

### PR previews

Phase 0 uses the `site` build artifact. The CI build has no `BASE_URL`, so the site's links
and assets are root-absolute (`/build/…`, `/calculus/…`). It cannot be opened from `file://`;
serve it from its root instead: download, unzip, run `npx serve <unzipped folder>`, then
open `http://localhost:3000`. (The deploy build uses `BASE_URL=/maths`.) If reviewing
widgets that way proves painful, add free Cloudflare Pages or Netlify PR previews. This is
an open question in [12](12-risks-and-open-questions.md).

### Generated content

`scripts/generate.py` writes everything the site includes but nobody edits by hand:
`content/<subject>/_generated/prereq-map.md` (via `graph.py mermaid`) and
`content/about/_generated/status-table.md`, the dashboard table that `about/status.md`
includes. It runs before every build (`npm run generate`, called by `dev`, `ast` and
`build`), so the deployed map and dashboard always match the front matter. `_generated/` is
git-ignored, so stale copies can't be committed.

## 5.8 Widgets

- Every widget is one ES module in `widgets/` exporting `{ render({ model, el }) }` (the
  anywidget contract).
- **How mystmd publishes a widget** (checked with 1.11.0): it copies *only* the `.mjs` file
  named in `{anywidget}` into the build, renamed with a content hash, and does not follow its
  imports. So:
  - shared helpers live in `widgets/_lib/` and are published with `project.static_files`
    (§5.5). A widget imports them with a relative path (`./_lib/board.mjs`), which then
    resolves next to the hashed module (confirmed in stage 3: mystmd publishes the folder at
    `/build/_lib/`, beside `/build/<widget>-<hash>.mjs`, §5.3);
  - JSXGraph is loaded **inside** `render()` with a dynamic import of a pinned URL:
    `const { default: JXG } = await import("https://cdn.jsdelivr.net/npm/jsxgraph@<exact>/distrib/jsxgraphcore.mjs")`.
    No module has a static `https:` import, because Node refuses those
    (`ERR_UNSUPPORTED_ESM_URL_SCHEME`) and the widget tests could not import the module. The
    URL and its version live in one place, `widgets/_lib/jsxgraph.mjs`;
  - the mathematics a widget computes (the δ in `epsilon-delta`, Riemann sums, …) lives in
    pure modules in `widgets/_lib/` with no JSXGraph or DOM, so `node --test` can import it.
- **Configuration is JSON only**, so authors never write JS. Every widget sits alone inside a
  labelled `{figure}`. The `wdg-` label goes on the figure (the only way to give a widget a
  stable, linkable anchor: an `"id"` in the JSON is not a MyST label, and `{anywidget}`
  accepts no `:label:`). The figure's caption is the widget's text description:

  `````markdown
  ::::{figure}
  :label: wdg-calc-limit-eps-delta

  ```{anywidget} ../../../widgets/epsilon-delta.mjs
  {
    "f": "x^2", "a": 2, "L": 4,
    "eps": 0.5, "epsRange": [0.05, 1.5],
    "xRange": [0, 3.5], "yRange": [0, 9]
  }
  ```

  Graph of $y = x^2$ near $x = 2$ with a horizontal band of half-width $\eps$ around $y = 4$
  and a vertical band of half-width $\delta$ around $x = 2$. Dragging $\eps$ shrinks the band;
  the widget shows the largest $\delta$ that keeps the graph inside the band.
  ::::
  `````
- **The caption is the text fallback.** The theme renders an anywidget as an empty `<div>`
  and draws it only after the module loads, inside a shadow root. Text produced by the
  widget's own JS (a `<noscript>`, visually-hidden text) therefore never shows when it is
  needed: with JavaScript off, a CDN outage or a broken module. The caption is static HTML,
  so it always shows. Widgets are numbered as figures ("Figure 2"); cross-page links name
  them as usual.
- Expressions (`"f": "x^2"`) are compiled with JSXGraph's built-in JessieCode parser, so
  there is no `eval` of config strings and no extra runtime dependency. Found in stage 3:
  JessieCode alone is too forgiving for author input (an unknown function returns its
  argument, so `sec(x)` is x; an unknown name is `undefined`; `2x` compiles to a function that
  does nothing; it accepts `;`, `==`, `?:` and property access). So `widgets/_lib/expression.mjs`
  first tokenizes the expression against an allowlist (numbers, the variable, the parameters,
  `+ - * / ^ ( )`, `pi`, `e`, and 17 functions; `ln`, never `log`; multiplication always
  written), with clear messages, and only then hands it to JessieCode. The allowlist is in the
  widget's schema (`$defs`), so `check_widgets.py` applies the same rules in CI.
  JessieCode needs a board, not a DOM: `new JXG.Board(…, new JXG.NoRenderer(), …)` compiles
  in Node too, so the widget tests evaluate through the browser's evaluator, from the pinned
  `jsxgraph` dev dependency (§5.4). That board must have its events switched off, or in a
  browser it listens for window resizes it cannot handle.
- Each widget has a JSON Schema (`schema/widgets/<name>.schema.json`, `additionalProperties:
  false` at every level, so a typo is an error); `check_all.py` (`scripts/check_widgets.py`)
  validates every widget block in the content, plus the rules a schema cannot express (ranges
  increasing, values inside them, the names in an expression; the widget's `_lib/` has the
  same rules, and one shared table of cases tests both). It also checks that every
  `{anywidget}` is the only content of a `{figure}` with a `wdg-` label and a non-empty
  caption, that the widget exists, and that every `maths.widgets` id is a widget.
- Shared helpers in `widgets/_lib/` handle board creation, theme-aware colours (light/dark,
  with a contrast test: ≥ 3:1 for lines and points, ≥ 4.5:1 for text) and keyboard-operable
  sliders (native `<input type="range">`), buttons and value tables (real `<table>`s).
- The theme renders a widget inside a shadow root and may call `render()` several times while
  the page hydrates (§5.3), so `render()` replaces its element's content and returns a cleanup.
- **Catalogue** (built as the curriculum needs them, see 08; `widgets/README.md` documents
  each built widget's keys): `function-plot` (built in stage 3: a graph, parameter sliders, a
  table of values, a hole, a traced point, zoom; its other modes come with their pages), `epsilon-delta`, `secant-tangent`, `zoom-to-linear`, `riemann-sum`,
  `area-accumulation` (FTC), `taylor`, `partial-sums`, `slope-field`, `newton-method`,
  `solid-of-revolution` (JSXGraph 3D), `prereq-graph` (Phase 7).
- Desmos/GeoGebra are allowed **only** as optional "explore further" links, never as core
  content: they are not version-controlled, may change or vanish, and have their own terms.
- A widget's *mathematics* is verified too: the δ that `epsilon-delta` reports is computed in
  JS (in a pure `_lib/` module), and a small Node test (`widgets/_tests/*.test.mjs`, run by
  `npm run test:widgets` locally and in CI, no test framework) checks it against values that
  SymPy precomputed (`widgets/_tests/make_fixtures.py` writes them; a pytest fails if they are
  stale). For `function-plot`: JessieCode's values, the table of every `function-plot` figure
  on the site, the value at a hole (the limit, from both sides), and where the sampled graph
  breaks (poles and jumps, against SymPy's singularities).
