# 12. Risks and open questions

## 12.1 Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | **Plausible-but-wrong mathematics from AI drafting** (the biggest risk to a "trustworthy" resource) | high | high | Author/verifier/reviewer separation; SymPy verification of every displayed step; proof checklist with a circularity table; owner review; status banners; public errata |
| R2 | **mystmd breaking changes** (young, fast-moving tool; v1.11 in Sept 2026) | medium | medium | Exact version pin; upgrades only in dedicated PRs with full CI and a visual check of exemplar pages; content uses standard MyST syntax (portable to Jupyter Book / Sphinx); our custom code is small (one plugin, widgets as plain ES modules) |
| R3 | MyST behaviour on custom front matter changes (e.g. the extra-key warning becomes an error) | low | medium | One namespaced key (`maths:`), so the fallback is mechanical: a sidecar `<page>.meta.yml` read by the same scripts and plugin (a one-script migration) |
| R4 | `{anywidget}` support or theme rendering regresses | low | medium | Widgets are anywidget-standard modules (also usable in Jupyter); a widget's `description` provides a text fallback |
| R5 | Owner review becomes the bottleneck | high | medium | Cap open PRs (3–6); agent pre-review; machine checks; fixed PR template; later per-subject reviewers |
| R6 | SymPy's LaTeX parser can't read some answers, or misparses them | medium | low | Restricted answer subset (04 §4.3); golden tests for the parser; parse failures *fail* rather than pass; `manual` escape hatch with a reviewer note; numeric spot-checks |
| R7 | Verification tests that copy the page's numbers (verifying nothing) | medium | high | Verifier prompt forbids it; reviewer checks that tests compute rather than restate; coverage counts labels, and the reviewer samples test quality |
| R8 | CDN dependency for JSXGraph (outage, URL change) | low | medium | Exact-version URL; vendored copy in `widgets/vendor/` as fallback; esbuild bundling if needed |
| R9 | Scope creep (too many widgets or extension pages before core is done) | medium | medium | Roadmap order; extension pages are marked and come after core; the widget catalogue only grows when a curriculum page needs it |
| R10 | Inconsistent notation across many agent sessions | medium | medium | Macros; notation lint in CI; notation page as the single reference; exemplar page |
| R11 | Licence contamination (copying from NC or proprietary textbooks) | medium | high | Explicit allow/deny list (07 §7.4); `maths.sources` required; PR checkbox; reviewer agent spot-checks unusual exercises with web search |
| R12 | Accessibility of interactive content | medium | medium | Keyboard-operable sliders, text descriptions, no colour-only encoding, Lighthouse ≥ 95 on exemplar pages |
| R13 | Translation drift (if a Swedish edition is added) | later | medium | Labels are shared; a translation records the source commit it was translated from, and CI flags pages whose English source changed since (see Q2) |
| R14 | Build time grows with hundreds of pages and widgets | low | low | MyST builds pages in tens of ms (PoC); measure in Phase 0 and Phase 4 |

## 12.2 Open questions (with recommended defaults)

| # | Question | Recommended default | Decide by |
|---|---|---|---|
| Q1 | **Custom domain?** (e.g. `maths.<something>`) | Start on `vronnblom.github.io/maths`; a domain can be added later without breaking labels (a MyST `BASE_URL` change only) | any time |
| Q2 | **How will translations work?** | A separate MyST project per language: `i18n/sv/myst.yml` mirrors `content/` with the *same labels and file names*, built to `/sv/`; each translated page records `maths.translated_from: <commit>`. Notation differences (decimal comma, `]a,b[`) live in the translation's notation page. No translation before Calculus 1.0. | after Phase 7 |
| Q3 | **Where do logic, sets and proof techniques live?** | A small `found` subject (5–8 pages: logic and quantifiers, sets and functions, proof techniques, induction) written **during Phase 2**, so the rigorous track can link to it instead of explaining in place. Alternative: keep explanations inline and defer `found`. | start of Phase 2 |
| Q4 | **Complex numbers: calculus preliminaries or linear algebra/`found`?** | Extension page in calculus preliminaries (needed by second-order ODEs); move or duplicate-link it when `linalg` needs more | Phase 2 |
| Q5 | **PR previews for reviewing widgets?** | Artifact download in Phase 0; add Cloudflare Pages/Netlify previews (free) if reviewing widgets from artifacts proves painful | end of Phase 1a |
| Q6 | **In-browser answer checking engine** | Spike in Phase 5: Cortex Compute Engine (symbolic) vs numeric spot-checking; probably a combination (symbolic first, numeric fallback) | Phase 5 |
| Q7 | **In-browser Python** | MyST JupyterLite if it has left beta by Phase 5; otherwise own lazy-loading Pyodide widget | Phase 5 |
| Q8 | **Parametric and polar curves** | Extension chapter in `calc` if Phase 6 has capacity, else into `mvc` | Phase 6 |
| Q9 | **Link Lean/Mathlib statements?** (e.g. "formal statement: `Real.exists_deriv_eq_slope`") | Not now. Optional remark field per theorem later; no formal proofs in scope | after Calculus 1.0 |
| Q10 | **Analytics?** | None (privacy, no cookie banner). Use GitHub traffic stats and errata/issue volume as signals | – |
| Q11 | **Per-browser progress tracking** ("mark as done") | `localStorage`-only checkboxes in Phase 7 if wanted; never accounts | Phase 7 |
| Q12 | **Number of exercises per page**: is 6–15 right? | Keep 6–15 on topic pages plus chapter review sets; practice banks (Phase 5) provide volume | after Phase 1b retrospective |
| Q13 | **Which existing course should paths align with?** (e.g. a specific Swedish university syllabus) | Generic paths (08 §8.6) now; add named course maps later as pages listing labels in order (cheap, since labels are stable) | any time |
| Q14 | **`ℕ` includes 0?** | Yes (ISO 80000-2), with explicit ranges in statements | settled unless objected to |
| Q15 | **Italic $e$, $\mathrm{d}$?** | Italic $e$, upright d via `\dd` (04) | settled unless objected to |
