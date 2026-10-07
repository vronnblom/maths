# CLAUDE.md

> **Status: Phase 0, stage 1 done (site skeleton, build, Pages deploy).** What exists now:
> `content/` (home, about pages, the empty Calculus subject page), `scripts/build_site.sh`,
> `scripts/fetch_theme.sh`, `ci.yml` (build job) and `deploy.yml`. Everything else below is
> specified in `docs/plan/` and arrives in the later stages of Phase 0
> (`docs/plan/09-roadmap.md`): **stage 2** checks, schema, `curriculum.yml`, `graph.py`,
> `generate.py`, `labels.lock`, codespell; **stage 3** the plugin and the first widget;
> **stage 4** `verify/`; **stage 5** the SessionStart hook, `CONTRIBUTING.md`, templates for
> PRs and issues. Items marked *(stage N)* don't exist yet. Update this file in the PR that
> lands each piece; it must always describe the repo as it is.

## What this repo is

An open, interactive, **verified** body of university mathematics, published as a MyST
website on GitHub Pages. Subjects live in `content/<subject>/`; Calculus (`calc`) is first.
The aim is correctness first and intuition before formalism, with layered rigour: core text
plus a collapsible "rigorous track". Read `PLAN.md` for the decisions and `docs/plan/` for
the details.

## Commands

```bash
npm ci && uv sync                 # install (Node 22 + mystmd 1.11.0; Python 3.12+ via uv)
npm run dev                       # live site at http://localhost:3000 (myst start in content/)
npm run build                     # scripts/build_site.sh: myst build, fails on any error or warning
npm run all                       # everything CI runs (CI calls these same scripts). Run before every push.
```

Both `dev` and `build` first run `scripts/fetch_theme.sh`, which git-fetches the book-theme
commit pinned in `content/myst.yml` into `content/_build/templates/` (cloud sessions can't
download github.com archives; see `docs/plan/05-tooling-and-build.md` §5.5). Bump the theme
only together with mystmd. mystmd renders every formula with KaTeX at build time, so a
KaTeX error (red text on the page) is a `⛔️` build error and fails `npm run build`.

Coming later (and then part of `npm run all`):

```bash
npm run check                     # (stage 2) front matter, labels, graph, toc, notation lint, spelling, checker tests
npm run verify                    # (stage 4) AST → answers → SymPy tests (pytest verify/) → coverage → KaTeX
npm run test:widgets              # (stage 3) widget maths (node --test)
uv run python scripts/graph.py ready calc   # (stage 2) topics whose prerequisites are done
```

## Layout

```
content/myst.yml                       MyST project (toc, KaTeX macros, theme pin, site options)
content/index.md, content/about/*.md   home and meta pages (labels site-<slug>)
content/_static/                       custom.css, favicon.svg
content/<subject>/index.md             subject landing page (calc-subject)
content/<subject>/curriculum.yml       (stage 2) planned topics, prerequisites, proof policies
content/<subject>/<chapter>/<topic>.md one topic page (the unit of work)
widgets/*.mjs                          (stage 3) interactive widgets (anywidget ES modules, JSON-configured)
plugins/topic-header.mjs               (stage 3) renders front matter (prerequisites, objectives, status)
verify/<subject>/<chapter>/test_*.py   (stage 4) SymPy tests, @covers("<label>")
scripts/                               build_site.sh, fetch_theme.sh; (stage 2) the checks
schema/                                (stage 2) JSON Schemas (front matter, widget configs)
templates/                             copy these to start a page or test
docs/plan/                             the plan (architecture decisions)
```

## Conventions (the short version)

- **Labels** are global, permanent and `[a-z0-9-]` only.
  - Page: `calc-limit-laws`. Block: `<kind>-<subj>-<slug>`, e.g. `thm-calc-squeeze`,
    `def-calc-continuity`, `eg-calc-computing-limits-factor`, `exr-calc-chain-rule-nested`,
    `sol-…` mirrors `exr-…`.
  - Kinds: `def thm lem cor prop ax prf eg exr sol rem eq fig sec wdg`.
  - Meta pages (`content/index.md`, `content/about/*`) use `site-<slug>`.
  - **Never rename or delete a label.** Every label is recorded in `labels.lock` *(stage 2)*. Details:
    `docs/plan/02-information-architecture.md` §2.4.
- **Front matter**: native MyST keys (`title`, `label`, `description`, `tags`) plus our
  `maths:` block (`kind, subject, status, level, difficulty, est_minutes, prerequisites,
  objectives, verify, widgets, reviewed_by, sources`). The MyST warning
  `'frontmatter' extra key ignored: maths` is expected and is the only allowed build warning.
- **Page structure** is fixed: `{topic-header}` → Why this matters → definitions → results →
  Worked examples → Common mistakes → Rigorous track → Summary → Exercises → Where this leads.
  See `templates/topic.md`.
- **Proofs** use `{proof:proof}` with `:enumerated: false` (a bare `{proof}` renders without
  the word "Proof"). Proof policies come from the curriculum: **F** full proof in core,
  **R** `{proof:proof} Rigorous track` with `:class: dropdown`, **S** `{proof:proof} Sketch`,
  **D** deferred (name the target).
- **Cross-references**: use `[](#label)` on the same page. On other pages always name the
  link: `[the squeeze theorem](#thm-calc-squeeze)`. Numbers restart on every page.
- **Notation**: follow `content/about/notation.md` (source: `docs/plan/04-notation-and-style.md`).
  Use the macros: `\R \N \Z \Q \C \dd \dv \dvn \pdv \abs \norm \vb \eps \sgn \arsinh \dom \ran`. Write `\ln` (never a bare
  `\log`), `\arcsin` (not `\sin^{-1}`), `\int_a^b f(x) \dd x`, intervals `[a, b)`, radians.
- **Exercises**: tier class `tier-a|tier-b|tier-c` (+ `rigor`, `applied`). Hints are
  `:class: dropdown hint`. One `Answer` admonition with `:class: dropdown answer` in the
  machine-checkable LaTeX subset (`\frac`, `\sqrt`, `\pi`, `e`, `\ln`, `\infty`, …), or
  `answer manual` for proofs. A `{solution}` follows each exercise, collapsed.
- **Writing**: en-GB spelling, "we" for reasoning, "you" for instructions. No "clearly" or
  "obviously". Alt text on every figure. Every widget sits alone in a `{figure}` labelled
  `wdg-…`, whose caption is its text description (`templates/blocks.md`).

## How to add a topic

Not possible yet: steps 1, 5 and 7 need stages 2–4, and `{topic-header}` needs the stage 3
plugin (the build fails on an unknown directive). The procedure, once they exist:

1. Pick a topic from `uv run python scripts/graph.py ready <subject>` (or as assigned).
   Branch: `topic/<label>`.
2. Copy `templates/topic.md` to the path in `curriculum.yml`. Fill in the front matter from
   the curriculum entry (prerequisites, objectives, results, proof policies, widgets).
   Keep `status: draft`.
3. Read the direct prerequisite pages, reuse their labels, and don't redefine anything.
   Read the exemplar `content/calculus/limits/limit-of-a-function.md` for the quality bar.
4. Write the page. ≥ 3 worked examples, ≥ 1 common mistake, 6–15 exercises across tiers,
   each with an answer and a solution.
5. Create `verify/<subject>/<chapter>/test_<topic>.py` from `templates/verify_test.py`
   with an `@covers` stub (`pytest.skip("for the verifier")`) for every `eg-`/`exr-` label.
   Stubs count as uncovered. **If you are the author, leave the expected values to the
   verifier.**
6. Add the page to the toc in `content/myst.yml`.
7. Run `uv run python scripts/check_labels.py --update-lock` and commit `labels.lock`.
8. Run `npm run all` and fix every error and warning.
9. Open a PR using the template. One topic per PR.

## How to verify mathematics

The harness (`verify/mathcheck/`) arrives in stage 4.

- Every displayed step in a worked example and every exercise answer gets a SymPy check in
  `verify/`, using `mathcheck` helpers (`equal`, `equal_up_to_constant`, `limit_is`,
  `numeric_spot_check`, `answer(label)`).
- `answer(label)` parses the answer **as printed on the page**, so never duplicate it in
  Python. Compare with `equal(...)`, never `==`.
- Derive expected values independently, and **never weaken a test to make it pass**. If the
  page and SymPy disagree, report it in the PR with the evidence.
- Proofs: go through `docs/plan/06-quality-assurance.md` §6.3, including the circularity
  table in `docs/plan/08-calculus-curriculum.md` §8.3.

## Don't

- Don't rename, delete or reuse labels. Don't move a page without listing its old path in
  `maths.aliases` (mystmd has no `aliases:` key; `scripts/write_redirects.py` *(stage 2)* makes the redirect).
- Don't set `status: reviewed`/`verified` or add yourself to `reviewed_by`; the owner does that.
- Don't edit another page's mathematics in a topic PR (open a separate PR).
- Don't add dependencies, front-matter keys, directive kinds or widget types without a
  `tooling` PR.
- Don't prove a result with a tool that depends on it (e.g. L'Hôpital or $(\sin x)'$ for
  $\lim \frac{\sin x}{x}$; Taylor series for Taylor's theorem).
- Don't cite results outside the page's prerequisite closure, except in a `looking-ahead`
  admonition. A proof may cite a same-page result only if it is stated before the result being
  proved; a solution, only results earlier than the solution. A proof that is not directly
  after its statement carries the matching label (`prf-calc-x` proves `thm-calc-x`).
- Don't copy from non-compatible sources (anything NC or proprietary; see
  `docs/plan/07-exercises.md` §7.4). List adapted CC BY / CC BY-SA sources in `maths.sources`.
- Don't embed Desmos/GeoGebra as core content (only as "explore further" links).
- Don't edit generated files (`content/**/_generated/`, `verify/_answers.json`,
  `verify/_coverage.json`).
