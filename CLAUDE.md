# CLAUDE.md

> **Status: v0 (planning stage).** The tooling described here (scripts, CI, plugin, widgets)
> is specified in `docs/plan/` and gets built in **Phase 0** (`docs/plan/09-roadmap.md`).
> Until then, only `docs/plan/` and `templates/` exist. Update this file in the PR that lands
> each piece; it must always describe the repo as it is.

## What this repo is

An open, interactive, **verified** body of university mathematics, published as a MyST
website on GitHub Pages. Subjects live in `content/<subject>/`; Calculus (`calc`) is first.
The aim is correctness first and intuition before formalism, with layered rigor: core text
plus a collapsible "rigorous track". Read `PLAN.md` for the decisions and `docs/plan/` for
the details.

## Commands

```bash
npm ci && uv sync                 # install (Node 22 + mystmd; Python 3.12+ via uv)
npm run dev                       # live site at http://localhost:3000 (myst start in content/)
npm run check                     # front matter, labels, graph, toc, coverage, notation lint
npm run verify                    # SymPy verification tests (pytest verify/)
npm run build                     # myst build --html --strict
npm run all                       # everything CI runs. Run before every push.
uv run python scripts/graph.py ready calc   # topics whose prerequisites are done
```

## Layout

```
content/myst.yml                       MyST project (toc, KaTeX macros, plugins)
content/<subject>/curriculum.yml       planned topics, prerequisites, proof policies
content/<subject>/<chapter>/<topic>.md one topic page (the unit of work)
widgets/*.mjs                          interactive widgets (anywidget ES modules, JSON-configured)
plugins/topic-header.mjs               renders front matter (prerequisites, objectives, status)
verify/<subject>/<chapter>/test_*.py   SymPy tests, @covers("<label>")
scripts/                               repository checks
schema/                                JSON Schemas (front matter, widget configs)
templates/                             copy these to start a page or test
docs/plan/                             the plan (architecture decisions)
```

## Conventions (the short version)

- **Labels** are global, permanent and `[a-z0-9-]` only.
  - Page: `calc-limit-laws`. Block: `<kind>-<subj>-<slug>`, e.g. `thm-calc-squeeze`,
    `def-calc-continuity`, `eg-calc-limit-laws-rational`, `exr-calc-chain-rule-nested`,
    `sol-…` mirrors `exr-…`.
  - Kinds: `def thm lem cor prop ax prf eg exr sol rem eq fig sec wdg`.
  - **Never rename or delete a label.** Details: `docs/plan/02-information-architecture.md` §2.4.
- **Front matter**: native MyST keys (`title`, `label`, `description`, `tags`) plus our
  `maths:` block (`kind, subject, status, level, difficulty, est_minutes, prerequisites,
  objectives, verify, widgets, reviewed_by, sources`). The MyST warning
  `'frontmatter' extra key ignored: maths` is expected and is the only allowed build warning.
- **Page structure** is fixed: `{topic-header}` → Why this matters → definitions → results →
  Worked examples → Common mistakes → Rigorous track → Summary → Exercises → Where this leads.
  See `templates/topic.md`.
- **Proof policies** come from the curriculum: **F** full proof in core, **R** `{proof}` with
  `:class: dropdown`, **S** sketch, **D** deferred (name the target).
- **Cross-references**: use `[](#label)` on the same page. On other pages always name the
  link: `[the squeeze theorem](#thm-calc-squeeze)`. Numbers restart on every page.
- **Notation**: follow `content/about/notation.md` (source: `docs/plan/04-notation-and-style.md`).
  Use the macros: `\R \N \Z \Q \C \dd \dv \abs \norm \vb \eps`. Write `\ln` (never a bare
  `\log`), `\arcsin` (not `\sin^{-1}`), `\int_a^b f(x) \dd x`, intervals `[a, b)`, radians.
- **Exercises**: tier class `tier-a|tier-b|tier-c` (+ `rigor`, `applied`). Hints are
  `:class: dropdown hint`. One `Answer` admonition with `:class: dropdown answer` in the
  machine-checkable LaTeX subset (`\frac`, `\sqrt`, `\pi`, `e`, `\ln`, `\infty`, …), or
  `answer manual` for proofs. A `{solution}` follows each exercise, collapsed.
- **Writing**: en-GB spelling, "we" for reasoning, "you" for instructions. No "clearly" or
  "obviously". Alt text on every figure; `description` on every widget.

## How to add a topic

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
   with an `@covers` stub for every `eg-`/`exr-` label. **If you are the author, leave the
   expected values to the verifier.**
6. Add the page to the toc in `content/myst.yml`.
7. Run `npm run all` and fix every error and warning.
8. Open a PR using the template. One topic per PR.

## How to verify mathematics

- Every displayed step in a worked example and every exercise answer gets a SymPy check in
  `verify/`, using `mathcheck` helpers (`equal`, `equal_up_to_constant`, `limit_is`,
  `numeric_spot_check`, `answer(label)`).
- `answer(label)` parses the answer **as printed on the page**, so never duplicate it in
  Python.
- Derive expected values independently, and **never weaken a test to make it pass**. If the
  page and SymPy disagree, report it in the PR with the evidence.
- Proofs: go through `docs/plan/06-quality-assurance.md` §6.3, including the circularity
  table in `docs/plan/08-calculus-curriculum.md` §8.3.

## Don't

- Don't rename, delete or reuse labels. Don't change URLs without adding `aliases:`.
- Don't set `status: reviewed`/`verified` or add yourself to `reviewed_by`; the owner does that.
- Don't edit another page's mathematics in a topic PR (open a separate PR).
- Don't add dependencies, front-matter keys, directive kinds or widget types without a
  `tooling` PR.
- Don't prove a result with a tool that depends on it (e.g. L'Hôpital or $(\sin x)'$ for
  $\lim \frac{\sin x}{x}$; Taylor series for Taylor's theorem).
- Don't cite results outside the page's prerequisite closure, except in a `looking-ahead`
  admonition.
- Don't copy from non-compatible sources (anything NC or proprietary; see
  `docs/plan/07-exercises.md` §7.4). List adapted CC BY / CC BY-SA sources in `maths.sources`.
- Don't embed Desmos/GeoGebra as core content (only as "explore further" links).
- Don't edit generated files (`content/**/_generated/`, `verify/_answers.json`).
