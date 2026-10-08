# Plan: an open, verified university mathematics repository

**Status:** decision-ready plan, 2026-10-07. **Phase 0 is done**: stages 1 (site skeleton,
build, Pages deploy), 2 (checks, schema, curriculum and prerequisite graph), 3 (plugin and first
widget), 4 (verification harness, coverage gate, verified-page guard) and 5 (agent support and
governance) are in place, and the site is live at <https://vronnblom.github.io/maths/>. The
first Phase 1a session confirmed the last item of its definition of done: a brand-new cloud
session starts with the SessionStart hook (09). **Phase 1a** is under way: the three Preliminaries prerequisites of `calc-limit`, then `calc-limit` itself.
**First subject:** Calculus. **Architecture:** scales to any subject by adding a folder.

## Decisions at a glance

| Area | Decision | Details |
|---|---|---|
| Purpose | Reference **and** course: definitions, theorems, proofs, worked examples, exercises, widgets; every block permanently addressable | [01](docs/plan/01-vision-and-scope.md) |
| Language | English (en-GB) now; i18n-ready (language-neutral labels; translations as parallel MyST projects later) | [04](docs/plan/04-notation-and-style.md), [12 Q2](docs/plan/12-risks-and-open-questions.md) |
| Audience / rigour | First-year engineering/science core text **+ collapsible rigorous track** for math majors; per-theorem proof policy F/R/S/D | [01 §1.5](docs/plan/01-vision-and-scope.md) |
| Output | **Website only**, highly interactive (JSXGraph widgets now; answer checking, practice banks and in-browser Python in Phase 5). No PDF. | [05](docs/plan/05-tooling-and-build.md), [07](docs/plan/07-exercises.md) |
| Toolchain | **MyST Markdown + `mystmd` (Jupyter Book 2 engine)**, book-theme, GitHub Pages via Actions. Chosen for cross-page references **with hover previews**, built-in proof/exercise directives, and `{anywidget}`. Runner-up: Quarto. | [05 §5.2](docs/plan/05-tooling-and-build.md) |
| Structure | Subject → chapter → topic page → labelled blocks. Global permanent labels `<kind>-<subj>-<slug>`. Topic-level prerequisite graph across subjects, checked in CI. | [02](docs/plan/02-information-architecture.md) |
| Content model | Fixed page structure; native MyST front matter + one `maths:` metadata block (JSON Schema); a small MyST plugin renders prerequisites, objectives and status | [03](docs/plan/03-content-model.md) |
| Correctness | Every computation re-done by SymPy; exercise answers parsed **from the page itself**; proof checklist with a circularity table; author ≠ verifier ≠ reviewer; status draft → reviewed → verified | [06](docs/plan/06-quality-assurance.md) |
| Exercises | Tiers A/B/C (+ `rigor`/`applied` flags), hints → answer → solution inline and collapsed; staged interactivity | [07](docs/plan/07-exercises.md) |
| Calculus scope | Single variable + series + intro ODE: **11 chapters, 82 topic pages**. Multivariable is a **separate subject** (`mvc`, depends on `calc` + `linalg`). | [08](docs/plan/08-calculus-curriculum.md) |
| Exemplar | **Limits**: `calc-limit` "The Limit of a Function" to gold standard first (with the ε–δ widget), then the rest of the chapter | [09](docs/plan/09-roadmap.md) |
| AI agents | One topic per PR; graph-driven parallel waves; author/verifier/reviewer agent roles; `CLAUDE.md` | [10](docs/plan/10-ai-agents.md), [CLAUDE.md](CLAUDE.md) |
| Licences | Content **CC BY-SA 4.0**, code **MIT**; open to outside contributors later (DCO); public errata log | [11](docs/plan/11-governance.md) |

## Plan documents

1. [Vision and scope](docs/plan/01-vision-and-scope.md)
2. [Information architecture](docs/plan/02-information-architecture.md): folders, labels, prerequisite graph
3. [Content model](docs/plan/03-content-model.md): page structure, front-matter schema, block templates
4. [Notation and style](docs/plan/04-notation-and-style.md): notation table, KaTeX macros, answer LaTeX subset
5. [Tooling and build](docs/plan/05-tooling-and-build.md): comparison, PoC results, dependencies, CI/deploy YAML
6. [Quality assurance](docs/plan/06-quality-assurance.md): SymPy verification, proof checklist, CI checks, statuses
7. [Exercises](docs/plan/07-exercises.md): tiers, structure, sources, Phase 5 interactivity
8. [Calculus curriculum](docs/plan/08-calculus-curriculum.md): all 82 topics with prerequisites, objectives, results, proof policies
9. [Roadmap](docs/plan/09-roadmap.md): Phases 0–8 with deliverables and definitions of done
10. [Working with AI agents](docs/plan/10-ai-agents.md)
11. [Contribution, licensing and governance](docs/plan/11-governance.md)
12. [Risks and open questions](docs/plan/12-risks-and-open-questions.md)

Templates (used from Phase 0): [`templates/`](templates/): a complete sample topic page,
block snippets, chapter and subject index pages, and a verification test.

## Roadmap summary

| Phase | Output |
|---|---|
| 0 | Repo skeleton, checks, CI, Pages deploy, plugin, first widget, governance files |
| 1a | Gold-standard page `calc-limit` + `epsilon-delta` widget (+ its 3 Preliminaries prerequisites); template freeze |
| 1b | Rest of the Limits chapter (6 pages + chapter index, + 2 Preliminaries prerequisites) |
| 2 | Remaining Preliminaries (7) + Continuity (4) |
| 3 | Derivatives (10) + Applications of derivatives (10) |
| 4 | Integrals, techniques, applications, improper integrals (22) |
| 5 | Interactive exercises: answer checking, practice banks, Python cells |
| 6 | Sequences and series (11) + intro ODE (6) |
| 7 | Calculus 1.0: everything verified, release |
| 8 | Linear Algebra, then Multivariable Calculus, by the same templates |

## Next tasks (first implementation session)

1. **Phase 0 skeleton** (stage 1, built): `content/myst.yml` (toc, macros, `folders: true`, the book-theme
   pinned to a commit), home and about pages, `package.json`/lockfile pinning
   `mystmd@1.11.0`, `pyproject.toml`/`uv.lock`, licence files, `.gitignore`,
   `scripts/build_site.sh`, and `deploy.yml`. Done when the site is live on GitHub Pages and the
   remaining PoC items (rendered dropdowns, KaTeX macros with arguments, anywidget, search)
   are confirmed. Dropdowns, macros and search are confirmed on the HTML build (05 §5.3);
   anywidget is confirmed in item 3; the theme reaches cloud sessions via `scripts/fetch_theme.sh`.
   **The site is live** (2026-10-07, after the owner enabled Pages: Deploy run 4 on `main`
   succeeded, and `/maths/`, `/maths/about/how-to-read/` and `/maths/calculus/` serve).
2. **Checks and schema** (stage 2, built): `schema/page.schema.json`, `content/tags.yml`,
   `content/calculus/curriculum.yml` (imported once from 08, now the source), `scripts/check_*.py`,
   `graph.py`, `generate.py` (the Mermaid maps and the status table), `write_redirects.py`,
   `labels.lock`, codespell with the en-GB list, the `checks` CI job, and `tests/` with broken
   fixtures proving that each check fails.
3. **Plugin and first widget** (stage 3, built): `plugins/topic-header.mjs` (`{topic-header}`,
   `{where-this-leads}`, `{chapter-topics}`), `widgets/function-plot.mjs` with `_lib/`, its
   schema, the catalogue (`widgets/README.md`) and Node tests against SymPy fixtures,
   `check_widgets.py`, and the widget on `about/how-to-read.md`. anywidget rendering is
   confirmed on the HTML build and **on the deployed site** (05 §5.3).
4. **Verification harness** (stage 4, built): `verify/mathcheck/` (`covers`, `answer`, the
   canonical symbols, `equal`…, `limit_is`…, `parse_answer` with the antlr backend and its
   normalisation), `scripts/extract_answers.py`, `check_coverage.py` and the coverage-based
   status preconditions (with the reviewer's note for `manual` answers, `maths.manual_checked`),
   the `verify` CI job, and the verified-page edit guard (`check_verified_edits.py`,
   `guard.yml`). KaTeX errors already fail the gated build, so there is no `check_katex.mjs`
   (05 §5.3).
5. **Agent support and governance** (stage 5, built): the SessionStart hook
   (`.claude/hooks/session-start.sh`: `npm ci` when needed, `uv sync --frozen`, the theme; cloud
   sessions only), the skills `/new-topic` (with `scripts/new_topic.py`), `/verify-topic` and
   `/review-math` (the role prompts of 10 §10.3, now only there), `CONTRIBUTING.md`,
   `CODE_OF_CONDUCT.md`, `CODEOWNERS`, the PR template and issue forms, the pre-filled erratum
   link on every topic and chapter page, `docs/decisions/` (ADRs), Dependabot and `links.yml`.
   `CLAUDE.md` is v1.
6. **Phase 1a** (next): `calc-real-numbers`, then `calc-functions` and
   `calc-absolute-value-inequalities`, each `/new-topic <label>` in its own session and PR,
   verified and reviewed by other sessions; then `calc-limit` with the `epsilon-delta` widget
   (09).
