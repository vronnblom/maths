# 9. Phased roadmap

Phases are ordered by dependency, not by calendar. The effort column is a rough guide
assuming one maintainer reviewing plus AI agents drafting. **Every phase ends with the
site deployed and CI green on `main`.**

| Phase | Name | Main output | Rough effort |
|---|---|---|---|
| 0 | Skeleton and CI | buildable empty site, all checks, templates, governance files | 2–4 sessions |
| 1a | Gold-standard page | `calc-limit` finished to the highest standard (+ its 3 Preliminaries prerequisites), templates frozen | 3–4 sessions |
| 1b | Limits chapter | the remaining 6 Limits pages (+ 2 more Preliminaries prerequisites) + chapter index | 4–6 sessions |
| 2 | Foundations | the remaining 7 Preliminaries pages + Continuity (4) | 4–7 sessions |
| 3 | Differential calculus | Derivatives (10) + Applications (10) | 8–12 sessions |
| 4 | Integral calculus | Integrals (7) + Techniques (6) + Applications (6) + Improper (3) | 8–12 sessions |
| 5 | Interactive exercises | answer-check widget, practice banks, Python cells; retrofit chapters 2–5 | 4–6 sessions |
| 6 | Series and ODE | Sequences & series (11) + Differential equations (6); backlog decision | 8–10 sessions |
| 7 | Calculus 1.0 | full audit, all pages verified, release | 3–5 sessions |
| 8 | Next subject | Linear Algebra via the "add a subject" checklist | – |

Phases 3 and 4 can overlap: they share only the MVT/FTC boundary, and the graph
(`graph.py ready`) tells us which pages are unblocked.

---

## Phase 0: skeleton, CI, deployment

**Deliverables**
- `content/myst.yml`, `content/index.md`, `content/about/{how-to-read,notation,status,errata}.md`
  (notation from [04](04-notation-and-style.md)), `content/calculus/index.md`,
  `content/calculus/curriculum.yml` (imported from [08](08-calculus-curriculum.md) by a
  one-off script), `content/_static/custom.css`.
- `package.json` + lock, `.nvmrc`, `pyproject.toml` + `uv.lock`, `.codespell-ignore`
  (seeded with `crossreference`), `.codespell-en-gb.txt` (the US→GB list),
  `.gitignore` (`_build/`, `_generated/`, `build.log`, `node_modules/`, `.venv/`,
  `verify/_answers.json`, `verify/_coverage.json`).
- `site.template` pinned to a book-theme commit, and the theme reachable from cloud sessions
  (05 §5.5).
- `plugins/topic-header.mjs` (`{topic-header}`, `{where-this-leads}`, `{chapter-topics}`).
- `scripts/`: `check_all.py`, `check_frontmatter.py`, `check_labels.py` (+ `labels.lock`),
  `graph.py`, `check_toc.py`, `check_coverage.py`, `check_verified_edits.py`,
  `extract_answers.py`, `generate.py`, `write_redirects.py`, `check_widgets.py`,
  `build_site.sh`; `schema/page.schema.json`; `verify/mathcheck/` with its own tests and the
  runtime coverage plugin. (`check_katex.mjs` was dropped in stage 4: KaTeX errors already fail
  the gated build, 05 §5.3.)
- One widget end-to-end: `widgets/function-plot.mjs` + schema + `_lib/` (published with
  `static_files`, 05 §5.8) + a Node test, rendering on the deployed site.
- `.github/workflows/{ci,guard,deploy,links}.yml`; branch protection on `main`;
  `.github/{pull_request_template.md,CODEOWNERS,ISSUE_TEMPLATE/*}`; Dependabot config.
- `README.md`, `CONTRIBUTING.md`, `LICENSE` (MIT), `LICENSE-CONTENT.md` (CC BY-SA 4.0),
  `CLAUDE.md` updated from v0 to v1.
- `.claude/` SessionStart hook (`npm ci && uv sync`) and a `/new-topic` skill wrapping the
  "add a topic" procedure ([10](10-ai-agents.md)).
- `tests/fixtures/` with deliberately broken pages (bad label, cycle, missing answer, KaTeX
  error (`gate-katex-*`, through the build gate), broken ref, unknown directive) and a pytest in
  `tests/` that runs each checker on them (run by `npm run check`); the verification defects (a
  `@covers` stub on a `verified` page, a failing test, an answer outside the subset, …) are
  one-edit variants of the template project in `tests/test_verify_pipeline.py`.

**Definition of done**
- [x] `https://vronnblom.github.io/maths/` serves the site with a home page, the about pages and an empty Calculus subject page showing the Mermaid prerequisite map from `curriculum.yml` (2026-10-07: the 12 maps render, no console errors).
- [x] Each checker has been shown to **fail** on its fixture and pass on the clean tree (fixture tests in CI).
- [x] The remaining items in [05 §5.3](05-tooling-and-build.md) are validated on the real HTML build (dropdowns, KaTeX macros with arguments, anywidget rendering, search) and the results are recorded in 05; anywidget also on the deployed site.
- [ ] A fresh clone gets to a green `npm run all` by following only `README.md`, and so does a
      Claude Code cloud session after its SessionStart hook.

## Phase 1a: the gold-standard page `calc-limit`

**Deliverables**
- The three Preliminaries pages in `calc-limit`'s prerequisite closure, `calc-real-numbers`,
  `calc-functions` and `calc-absolute-value-inequalities`, to at least `reviewed`. A page may
  only be `reviewed` or `verified` once all its prerequisites are `reviewed` (CI-enforced,
  06 §6.4), so the exemplar can't be verified without them. They are short pages, written
  in the normal one-topic-per-PR flow before the exemplar is marked.
- `content/calculus/limits/limit-of-a-function.md`, complete per [03 §3.2](03-content-model.md),
  with:
  - motivation from velocity and instantaneous rate (a teaser for derivatives) and a
    table-of-values widget showing where tables mislead (e.g. $\sin(\pi/x)$);
  - the precise ε–δ definition in the core, with the **`epsilon-delta` widget** (the
    signature widget of the site) and a guided "Try this";
  - ε–δ proofs for a linear function (core, worked) and a quadratic (rigorous track);
  - non-existence examples (jump, oscillation, unbounded);
  - common mistakes, e.g. "the limit is $f(a)$", or choosing δ that depends on $x$;
  - 10–12 exercises (4 A, 4 B, 3 C including 2 `rigor`) with hints, answers and solutions;
  - `verify/calculus/limits/test_limit_of_a_function.py` with 100 % coverage.
- `widgets/epsilon-delta.mjs` + schema + Node tests.
- **Template freeze**: update `templates/` and `CLAUDE.md` with everything learnt; write
  `docs/exemplar-review.md`, the rubric the page was judged by (§9.1).

**Definition of done**
- [ ] `calc-real-numbers`, `calc-functions` and `calc-absolute-value-inequalities` at least `reviewed`.
- [ ] `calc-limit` at `status: verified`, with the proof checklist signed by the owner and the reviewer agent.
- [ ] Exemplar rubric (§9.1): every item ✔.
- [ ] Tested by a real reader (a student or colleague), and their feedback addressed.
- [ ] Mobile view checked (widgets usable on a phone, dropdowns readable).
- [ ] Lighthouse accessibility score ≥ 95 for the page.

## Phase 1b: the rest of the Limits chapter

**Deliverables**: `calc-one-sided-limits`, `calc-limit-laws`, `calc-computing-limits`,
`calc-squeeze-theorem`, `calc-infinite-limits`, `calc-limits-at-infinity`, and
`limits/index.md` with review exercises. Also the two remaining Preliminaries pages that the
chapter needs: `calc-polynomial-rational` (for `calc-computing-limits`) and
`calc-trig-functions` (for `calc-squeeze-theorem`), to at least `reviewed`. **One PR per
page**, produced in parallel by agents (see [10](10-ai-agents.md)) once Phase 1a is merged.

**Definition of done**: all 7 Limits pages `verified`, and the 5 Preliminaries pages they
need at least `reviewed`; chapter index with ≥ 8 review exercises; no forward-reference
warnings; a retrospective note on what the template missed, folded back into `templates/`.

**Note**: pages in later phases can be *drafted* before their prerequisites are reviewed, but
they cannot be marked `reviewed` until all their prerequisites exist and are at least
`reviewed` (CI-enforced by `check_frontmatter.py`, 06 §6.4). This keeps quality ordered
without blocking drafting. Every phase plans its pages so that its definition of done can be
met under this rule.

## Phase 2: Preliminaries and Continuity

**Deliverables**: the remaining 7 Preliminaries pages (short: 15–25 minutes each,
exercise-heavy; 5 were done in Phases 1a/1b) and 4 Continuity pages (incl. the bisection
mode of `function-plot`); 2 chapter indexes.
**Definition of done**: all 16 Preliminaries and Continuity pages at least `reviewed`, ≥ 75 % `verified`; Mermaid map for
chapters 1–3 correct; the notation page reviewed against the actual usage in chapters 1–3.

## Phase 3: Derivatives and Applications of Derivatives

**Deliverables**: 20 pages; widgets `secant-tangent`, `zoom-to-linear`, `newton-method`,
`taylor`.
**Definition of done**: all pages at least `reviewed`, ≥ 75 % `verified`; the circularity table
in [08 §8.3](08-calculus-curriculum.md) checked for these chapters (the reviewer agent gets
the table explicitly).

## Phase 4: Integral calculus

**Deliverables**: 22 pages (chapters 6–9) including the extension `calc-ln-integral`, which
closes the exponential/logarithm loop; widgets `riemann-sum`, `area-accumulation`,
`solid-of-revolution`.
**Definition of done**: as in Phase 3; plus `calc-ln-integral` verified (it carries the
"proved later" debt from chapters 1 and 4).

## Phase 5: interactive exercise layer

**Deliverables** (see [07 §7.6](07-exercises.md)):
- `widgets/answer-check.mjs` with the chosen in-browser equivalence engine (spike first:
  Compute Engine vs numeric spot-checking; record the decision in 05).
- `practice/` generators + `widgets/practice.mjs`, with practice banks for at least: limit
  laws, differentiation rules, chain rule, substitution, integration by parts.
- In-browser Python: evaluate MyST JupyterLite execution, else `widgets/python-cell.mjs`.
- Retrofit `check` answers onto all tier A exercises in chapters 2–5.

**Definition of done**: answer-check agrees with the SymPy-verified answer for 100 % of
retrofitted exercises (tested in CI by feeding each extracted answer into the engine's Node
build); practice generators tested; lazy-loading confirmed (no page loads Pyodide unless
asked).

## Phase 6: Sequences and series, intro ODE

**Deliverables**: 17 pages; widgets `partial-sums`, `slope-field`; decision on the
parametric/polar backlog chapter (add as extension or move to `mvc`).
**Definition of done**: as in Phase 3.

## Phase 7: Calculus 1.0

**Deliverables**
- Every page `verified`; the success criteria in [01 §1.6](01-vision-and-scope.md) met.
- Full-subject audit by a fresh reviewer agent per chapter (statement consistency, notation,
  cross-link density, "where this leads" sanity).
- `widgets/prereq-graph.mjs` (interactive graph on the subject page).
- A tagged release `calc-1.0` and a citation file (`CITATION.cff`) with a Zenodo DOI (optional).

**Definition of done**: the release is tagged; the errata process has handled at least one
real report end-to-end; and the "how to add a subject" checklist has been dry-run on a
dummy subject in a branch.

## Phase 8 onward: next subjects

**Order**: `linalg` (needed by `mvc`) → `mvc` → `found` (if not done earlier) → `prob` / `disc`
/ `ode` / `ana` by demand. For each:

1. **Curriculum PR**: `content/<subject>/curriculum.yml` + a planning doc
   `docs/plan/subjects/<subject>.md` (scope, chapter tree, proof policies, notation additions,
   widgets needed). Owner approves.
2. **Exemplar page** for the subject (one page, gold standard, using the same rubric), since
   each subject has its own style, e.g. matrix layouts in `linalg` and combinatorial proofs in `disc`.
3. Chapters in graph order, one topic per PR.
4. **Definition of done** per subject: as for Calculus 1.0.

Things that will likely be needed per subject and are already anticipated: notation
additions (vectors and matrices are reserved in 04), new widget types (2D/3D vector
widgets for `linalg`, probability simulators for `prob`), and new proof kinds (MyST supports
`proof:algorithm` and `proof:axiom` already).

## 9.1 Exemplar rubric (used in Phase 1a, then for every subject's exemplar)

| # | Criterion |
|---|---|
| 1 | Follows the page structure exactly; the topic header renders prerequisites, objectives, time and status |
| 2 | Opens with a concrete question; the first formula appears only after motivation |
| 3 | Every definition has an "in words" unpacking, an example and a non-example |
| 4 | Every theorem: hypotheses justified (counterexamples for the subtle ones), proof per policy, strategy sentence |
| 5 | ≥ 3 worked examples covering the typical, the edge case, and an applied case; each ends with a **Check** |
| 6 | Widgets: ≥ 1, each with a "Try this", a text description, and keyboard operability |
| 7 | Common mistakes are drawn from real student errors (≥ 2) |
| 8 | Exercises: ≥ 10, all tiers, hints/answer/solution complete, ≥ 1 `rigor` and ≥ 1 `applied` |
| 9 | 100 % verification coverage; every displayed step in examples checked or annotated |
| 10 | All cross-references named; prerequisites linked; "where this leads" non-empty |
| 11 | Notation lint clean; reads well aloud (no undefined symbols, no "clearly") |
| 12 | Renders well on mobile and in dark mode; accessibility ≥ 95 |
