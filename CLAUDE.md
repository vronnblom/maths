# CLAUDE.md

> **v1, Phase 0 done** (2026-10-07). Phase 1a is under way: `calc-real-numbers` (the first
> topic page, a draft), then `calc-functions` and `calc-absolute-value-inequalities`, then the
> exemplar `calc-limit` (`docs/plan/09-roadmap.md`). This file must always describe the repo as it is: update it in
> the PR that changes what it says.

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
npm run check                     # front matter, labels, graph, toc, notation lint, widgets, spelling, checker tests
npm run verify                    # AST → answers → SymPy tests (pytest verify/) → coverage gate
npm run test:widgets              # widget maths against SymPy fixtures, and the plugin's logic (node --test)
npm run build                     # generate, then scripts/build_site.sh: myst build (fails on any error or warning), redirects
npm run all                       # check + verify + test:widgets + build: everything CI runs (CI calls these same scripts). Run before every push.
uv run python scripts/graph.py ready calc        # planned topics whose prerequisites are all ≥ reviewed
uv run python scripts/graph.py closure calc-mean-value-theorem   # every transitive prerequisite
uv run python scripts/new_topic.py calc-real-numbers              # scaffold a topic: page, verify stubs, toc, labels.lock (/new-topic)
uv run python scripts/new_topic.py --stubs calc-real-numbers      # add @covers stubs for the page's new eg-/exr- labels
uv run python scripts/check_labels.py --update-lock               # add your new labels to labels.lock
uv run python widgets/_tests/make_fixtures.py                     # after adding a function-plot table: SymPy's expected values
uv run pytest verify/calculus/limits -q          # after npm run verify: rerun one chapter's tests while you work
```

`npm run check` = `scripts/check_all.py` (`check_toc`, `check_frontmatter`, `check_labels
--forward-refs`, `graph.py check`, the notation lint, `check_widgets`; errors fail, warnings
don't) + codespell + `pytest tests`. Every check prints `file:line: error: message`. Each script also runs alone
(`uv run python scripts/check_labels.py`) and takes `--root` (default `content/`).

`dev` and `build` first run `npm run generate` (`scripts/generate.py`), which writes the
git-ignored includes `content/calculus/_generated/prereq-map.md` (the Mermaid maps on the
subject page) and `content/about/_generated/status-table.md`. Never edit or commit them.
Both then run `scripts/fetch_theme.sh`, which git-fetches the book-theme
commit pinned in `content/myst.yml` into `content/_build/templates/` (cloud sessions can't
download github.com archives; see `docs/plan/05-tooling-and-build.md` §5.5). Bump the theme
only together with mystmd. mystmd renders every formula with KaTeX at build time, so a
KaTeX error (red text on the page) is a `⛔️` build error and fails `npm run build` (the
`gate-katex-*` fixtures prove it; there is no separate KaTeX check). Math in the front-matter
`title` and `description` is never rendered: it shows as literal `$…$`, so keep math out of them.

In a Claude Code cloud session the **SessionStart hook** (`.claude/settings.json` →
`.claude/hooks/session-start.sh`) has already run `npm ci` (skipped when `node_modules/` matches
the lockfile), `uv sync --frozen` and `fetch_theme.sh`; its one-line report is in your context.
If it failed, it said which step: fix that and rerun it with
`CLAUDE_CODE_REMOTE=true bash .claude/hooks/session-start.sh`. On a laptop it does nothing.

`npm run verify` = `npm run ast` (`myst build --site`, the AST only) →
`scripts/extract_answers.py` (every exercise's Answer, as printed, into the git-ignored
`verify/_answers.json`) → `pytest verify` (which refuses to run on a missing or stale
`_answers.json` and writes `verify/_coverage.json`) → `scripts/check_coverage.py` (each page's
status against the coverage that run achieved; it prints the per-page coverage for your PR).
On pull requests, `guard.yml` runs `check_verified_edits.py`: changing a block of a `verified`
page fails unless its `maths.verify` file changes too, the status is lowered, or the PR has the
`typo-only` label.

## Layout

```
content/myst.yml                       MyST project (toc, KaTeX macros, theme pin, site options)
content/index.md, content/about/*.md   home and meta pages (labels site-<slug>)
content/_static/                       custom.css, favicon.svg
content/tags.yml                       the controlled vocabulary for `tags`
content/<subject>/index.md             subject landing page (calc-subject)
content/<subject>/curriculum.yml       the plan: chapters, topics, prerequisites, objectives, results and proof policies
content/<subject>/<chapter>/<topic>.md one topic page (the unit of work)
widgets/*.mjs, widgets/README.md       interactive widgets (anywidget ES modules, JSON-configured) and their catalogue
widgets/_lib/, widgets/_tests/         shared helpers and pure maths modules; node tests against SymPy fixtures
plugins/topic-header.mjs               {topic-header}, {where-this-leads}, {chapter-topics}: rendered from front matter
                                       and curriculum.yml (logic in plugins/_lib/, tests in plugins/_tests/)
verify/<subject>/<chapter>/test_*.py   SymPy tests, @covers("<label>"); one file per page, at its maths.verify path
verify/mathcheck/                      covers, answer, the canonical symbols, equal…, limit_is…; latex.py (parse_answer)
verify/conftest.py, test_mathcheck.py  loads _answers.json, records coverage; the harness's own tests and AST fixture
scripts/                               the checks (check_all.py and the scripts it runs), graph.py, generate.py,
                                       write_redirects.py, build_site.sh, myst_gate.sh, fetch_theme.sh,
                                       extract_answers.py, check_coverage.py, check_verified_edits.py,
                                       new_topic.py (the /new-topic scaffolder), links_report.sh (links.yml)
schema/                                JSON Schemas: page front matter, curriculum.yml, widgets/<name>.schema.json
labels.lock                            every label ever merged (06 §6.7)
tests/                                 the checkers' tests; tests/fixtures/ has one broken project per check
templates/                             the page and test templates (new_topic.py builds on topic.md)
docs/plan/                             the plan (ADR 0000); docs/decisions/ holds later ADRs (11 §11.3)
docs/agents/README.md                  index of the agent roles and their skills
.claude/settings.json, .claude/hooks/  the SessionStart hook (cloud sessions only)
.claude/skills/                        /new-topic, /verify-topic, /review-math: the role prompts (their only copy)
.github/workflows/                     ci.yml (checks, verify, build), guard.yml (verified-edits, PRs only),
                                       deploy.yml (Pages), links.yml (weekly external links → one issue)
.github/                               pull_request_template.md, ISSUE_TEMPLATE/ (erratum, new-topic, widget),
                                       CODEOWNERS, dependabot.yml (actions, npm except mystmd/jsxgraph, uv)
CONTRIBUTING.md, CODE_OF_CONDUCT.md    for people; agents read this file
```

## Conventions (the short version)

- **Labels** are global, permanent and `[a-z0-9-]` only.
  - Page: `calc-limit-laws`. Block: `<kind>-<subj>-<slug>`, e.g. `thm-calc-squeeze`,
    `def-calc-continuity`, `eg-calc-computing-limits-factor`, `exr-calc-chain-rule-nested`,
    `sol-…` mirrors `exr-…`.
  - Kinds: `def thm lem cor prop ax prf eg exr sol rem eq fig sec wdg`.
  - Meta pages (`content/index.md`, `content/about/*`) use `site-<slug>`.
  - **Never rename or delete a label.** Every label is recorded in `labels.lock`. Details:
    `docs/plan/02-information-architecture.md` §2.4.
- **Front matter**: native MyST keys (`title`, `label`, `description`, `tags`) plus our
  `maths:` block (`kind, subject, status, level, difficulty, est_minutes, prerequisites,
  objectives, verify, widgets, reviewed_by, manual_checked, sources`), validated against
  `schema/page.schema.json`. Tags come from `content/tags.yml`. A topic page's label, file,
  title, level and prerequisites must match its `curriculum.yml` entry. The MyST warning
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
  The notation lint checks these (and `\mathrm{e}`, "clearly"). Where a page must *show* the
  wrong form (the notation guide, the inverse-trig page), wrap it in
  `% notation-lint: off (reason)` … `% notation-lint: on`.
- **Exercises**: tier class `tier-a|tier-b|tier-c` (+ `rigor`, `applied`). Hints are
  `:class: dropdown hint`. One `Answer` admonition with `:class: dropdown answer` in the
  machine-checkable LaTeX subset (`\frac`, `\sqrt`, `\pi`, `e`, `\ln`, `\infty`, …; 04 §4.3), or
  `answer manual` for proofs. An extra class gives the answer type: `expr` (default),
  `antiderivative` (ends `+ C`), `set` (brackets are intervals), `bool` (the word True or
  False), `numeric-<tol>` (`numeric-5e-3` for two decimal places). A `{solution}` follows
  each exercise, collapsed.
- **Writing**: en-GB spelling, "we" for reasoning, "you" for instructions. No "clearly" or
  "obviously". Alt text on every figure.
- **Widgets**: every widget sits alone in a `{figure}` labelled `wdg-…`, whose caption is its
  text description (shown when the widget can't load), followed by **Try this:**. Its JSON
  must validate against `schema/widgets/<name>.schema.json`, and its id goes in
  `maths.widgets`; `check_widgets.py` checks all of it. Keys and the expression language
  (`2*x`, `ln`, `pi`, `e`) are in `widgets/README.md`. Only built widgets may be used: today
  `function-plot`. After adding or changing a `function-plot` with a `table`, run
  `widgets/_tests/make_fixtures.py` (a test fails otherwise).

## Roles

Every topic goes through three roles, each a different session (`docs/plan/10-ai-agents.md`
§10.1–§10.3); each role's prompt is its skill, and only there:

- **Author**: `/new-topic <label>` (`.claude/skills/new-topic/SKILL.md`) writes the page and
  leaves `@covers` stubs. Never computes expected values.
- **Verifier**: `/verify-topic <path>` writes the SymPy tests from the statements, pushes them
  to the topic branch, and reports disagreements. Never edits the page.
- **Reviewer**: `/review-math <path>` reviews against the 06 §6.3 checklist and the 08 §8.3
  circularity table and posts findings ranked by severity. Never rewrites the page.

None of them sets a status, `reviewed_by` or `maths.manual_checked`: the owner does, when
approving. A session that wrote a page doesn't verify or review it.

## How to add a topic

`/new-topic <label>` walks these steps (`.claude/skills/new-topic/SKILL.md` has the detail):

1. Pick a topic from `uv run python scripts/graph.py ready <subject>` (or as assigned).
   Branch: `topic/<label>`. One topic per PR. To change the plan (a prerequisite, a title),
   change `curriculum.yml` first, in its own `curriculum` PR.
2. Scaffold it: `uv run python scripts/new_topic.py <label>`. From the `curriculum.yml` entry
   it writes the page (front matter, every result of `results` with the proof blocks its
   policy asks for, the sections of `templates/topic.md`), the verify file at `maths.verify`
   (`verify/<subject>/<chapter>/test_<topic>.py`, `-` → `_`), and the toc entry (under a
   chapter group until the chapter index exists), then runs `check_labels.py --update-lock`.
   It refuses a label that is in no curriculum and a page that exists. Keep `status: draft`.
3. Read the direct prerequisite pages, reuse their labels, and don't redefine anything.
   Read the exemplar `content/calculus/limits/limit-of-a-function.md` (once it exists) for the
   quality bar.
4. Write the page, replacing every `TODO`: ≥ 3 worked examples, ≥ 1 common mistake, 6–15
   exercises across tiers, each with an answer and a solution.
5. `uv run python scripts/new_topic.py --stubs <label>` adds an `@covers` stub
   (`pytest.skip("for the verifier")`) for every `eg-`/`exr-` label. Stubs count as uncovered.
   **If you are the author, leave the expected values to the verifier.**
6. Run `uv run python scripts/check_labels.py --update-lock` and commit `labels.lock`.
7. `grep -n TODO <page>` prints nothing; `npm run all` passes with no errors or warnings.
   `check_coverage.py` (in `npm run verify`) prints the page's coverage; copy it into the PR.
8. Open the PR with `.github/pull_request_template.md`: type, summary of the mathematics,
   results with policies, coverage, the proof checklist, sources.

## How to verify mathematics

Details: `docs/plan/06-quality-assurance.md` §6.1. The harness is `verify/mathcheck/`.

- Every displayed step in a worked example and every exercise answer gets a SymPy check in
  `verify/`, using `mathcheck` helpers (`equal`, `equal_up_to_constant`, `equal_on_domain`,
  `numeric_spot_check`, `limit_is`, `series_converges_to`, `solves_ode`, `answer(label)`).
  Import the symbols from `mathcheck` (`from mathcheck import x, n`): they are the ones
  `answer()` uses (real; `n` an integer), and `equal` rejects a foreign `sp.Symbol("x")`.
- `answer(label)` parses the answer **as printed on the page**, so never duplicate it in
  Python. Compare with `equal(...)`, never `==`. A multi-part answer comes back as a tuple of
  its parts, in order.
- What counts (06 §6.1): a label is covered only by a test that declares it with `@covers`
  and **passes**; an `exr-` test must call `answer(label)`; an `eg-` test must make at least one
  mathcheck assertion. A helper counts as an assertion only when it returns True, and a
  comparison SymPy cannot decide raises (it never passes). Skipped, xfailed and failed tests
  count for nothing. Thresholds: `reviewed` ≥ 50 %, `verified` 100 %.
- A `manual` answer (a proof, a sketch) has nothing for `answer()` to read; test its key claims
  anyway. It counts as covered only through the **reviewer's note**: the reviewer adds
  `<exr label>: <their handle>` under `maths.manual_checked`, and the handle must be in
  `maths.reviewed_by`. Authors and verifiers never add it.
- Derive expected values independently, and **never weaken a test to make it pass**. If the
  page and SymPy disagree, report it in the PR with the evidence.
- Proofs: go through `docs/plan/06-quality-assurance.md` §6.3, including the circularity
  table in `docs/plan/08-calculus-curriculum.md` §8.3.

## Don't

- Don't rename, delete or reuse labels. Don't move a page without listing its old path in
  `maths.aliases` (mystmd has no `aliases:` key; `scripts/write_redirects.py` makes the redirect).
- Don't set `status: reviewed`/`verified`, add yourself to `reviewed_by`, or add
  `maths.manual_checked` entries; the owner (or a human reviewer) does that.
- Don't edit another page's mathematics in a topic PR (open a separate PR).
- Don't add dependencies, front-matter keys, directive kinds or widget types without a
  `tooling` PR (the checks' parser, `scripts/myst_source.py`, fails on directives it doesn't
  know).
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
