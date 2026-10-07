# 3. Content model and templates

Ready-to-copy files are in [`templates/`](../../templates/):
[`topic.md`](../../templates/topic.md) (a complete sample page),
[`blocks.md`](../../templates/blocks.md) (one snippet per block type),
[`chapter-index.md`](../../templates/chapter-index.md),
[`subject-index.md`](../../templates/subject-index.md) and
[`verify_test.py`](../../templates/verify_test.py).
This document explains the *rules* those templates follow.

## 3.1 Page kinds

| `maths.kind` | File | Purpose |
|---|---|---|
| `subject` | `content/<subject>/index.md` | Landing page: overview, audience, chapter list, prerequisite map, subject-level dependencies |
| `chapter` | `content/<subject>/<chapter>/index.md` | Chapter overview: why this chapter, topic list with time estimates, chapter objectives, **mixed review exercises** (which cut across topics) |
| `topic` | `content/<subject>/<chapter>/<topic>.md` | The unit of learning (structure below) |
| `meta` | `content/about/*.md`, `content/index.md` | Site documentation: notation, how to read, status, errata. Labels `site-<slug>`, no `maths.subject` |

## 3.2 Standard structure of a topic page

Sections appear **in this order**. Headings are fixed so readers and agents always know where
things are. Optional sections are marked.

| # | Section (H2 heading) | Content | Required |
|---|---|---|---|
| 0 | *(no heading)* `:::{topic-header}` | Rendered by the plugin from front matter: "Before you start" (prerequisite links), learning objectives, estimated time, difficulty, status badge | ✔ |
| 1 | `## Why this matters` | 1–3 paragraphs plus a picture or widget: the question this topic answers and a concrete motivating example. No formal definitions yet. | ✔ |
| 2 | `## Definitions` (or a concept-named heading) | `proof:definition` blocks. Each is followed by a plain-language unpacking and at least one example/non-example. | ✔ if the page defines anything |
| 3 | `## Main results` (or concept-named headings) | `proof:theorem` / `lemma` / `corollary` / `proposition` with proofs according to the proof policy (F/R/S/D) | ✔ if the page has results |
| 4 | `## Worked examples` | `proof:example` blocks, each with a stated goal, numbered steps, a boxed result, and a "check" line (sanity check: units, sign, special case, graph) | ✔ (≥ 3) |
| 5 | `## Common mistakes` | `{warning}` admonitions, each showing the mistake, why it's wrong and the correct version | ✔ (≥ 1) |
| 6 | `## Rigorous track` | Dropdown admonitions: ε–δ proofs (policy R), subtle hypotheses, counterexamples showing why hypotheses are needed | optional |
| 7 | `## Summary` | 3–7 bullet key takeaways and a formula box | ✔ |
| 8 | `## Exercises` | Tier A → B → C, each with hints, an answer and a solution (see [07](07-exercises.md)) | ✔ (≥ 6) |
| 9 | `## Where this leads` | Rendered by the `{where-this-leads}` plugin directive (reverse prerequisite edges), plus optional hand-written "see also" and "further reading" | ✔ |

Section-level widgets go where they help, usually in §1 (motivation) and §2/§3 (exploring a
definition or theorem). Every widget is followed by a short "Try this:" prompt (what to drag
and what to notice).

## 3.3 Front matter schema

Front matter has **two layers**:

1. **Native MyST keys**, which MyST understands and renders: `title`, `short_title`,
   `label`, `description`, `tags`, `numbering`. (mystmd has no `aliases` key; old URLs go in
   `maths.aliases`, see below.)
2. **One namespaced key `maths:`**, our own metadata, which MyST ignores (with exactly one
   predictable warning, `'frontmatter' extra key ignored: maths`, which CI whitelists; see 05).
   It is read by `scripts/*.py` (validation, graph, coverage) and by the
   `plugins/topic-header.mjs` MyST plugin (rendering).

### Example: a topic page

```yaml
---
title: The Limit of a Function
short_title: Limit of a function
label: calc-limit
description: >-
  What it means for f(x) to approach L as x approaches a — intuitively, graphically,
  and precisely with ε and δ.
tags: [limits, epsilon-delta]
maths:
  kind: topic
  subject: calc
  status: draft                   # draft | reviewed | verified
  level: core                     # core | extension   (extension = whole page is optional)
  difficulty: 2                   # 1 (routine) … 5 (hard)
  est_minutes: 40
  prerequisites:
    - calc-functions
    - calc-absolute-value-inequalities
  objectives:
    - Estimate a limit from a table of values and from a graph, and explain why such estimates can mislead.
    - State the precise (ε–δ) definition of a limit and interpret it as a game between ε and δ.
    - Prove simple limits (linear, quadratic) directly from the definition.
    - Decide when a limit fails to exist (jump, oscillation, unboundedness).
  verify: verify/calculus/limits/test_limit_of_a_function.py
  widgets: [epsilon-delta, function-plot]
  reviewed_by: []                 # GitHub handles; required non-empty for status ≥ reviewed
  sources:                        # where facts/exercises were adapted from (licence-compatible only)
    - "Active Calculus 2.0, §1.7 (CC BY-SA 4.0)"
---
```

### Field reference (`schema/page.schema.json`)

| Field | Type | Required | Rule |
|---|---|---|---|
| `title` | string | ✔ | Title Case; ≤ 60 chars |
| `short_title` | string | | sidebar label, ≤ 30 chars |
| `label` | string | ✔ | `^(calc\|linalg\|mvc\|…\|site)-[a-z0-9]+(-[a-z0-9]+)*$`. By kind (02 §2.4): topic = its curriculum entry's label; chapter = `<subj>-<chapter-slug>-chapter`; subject = `<subj>-subject`; meta = `site-<slug>` |
| `description` | string | ✔ | 1–2 sentences; used in hover previews, search and social cards |
| `tags` | string[] | | from `content/tags.yml` (controlled vocabulary, avoids `limit`/`limits` drift) |
| `maths.kind` | enum | ✔ | `subject` · `chapter` · `topic` · `meta` |
| `maths.subject` | enum | ✔ (not meta) | subject code |
| `maths.status` | enum | ✔ | `draft` · `reviewed` · `verified` (see 06 §6.6) |
| `maths.level` | enum | ✔ topic | `core` · `extension` |
| `maths.difficulty` | int 1–5 | ✔ topic | |
| `maths.est_minutes` | int 5–90 | ✔ topic | reading + examples, excluding exercises |
| `maths.prerequisites` | label[] | ✔ topic, chapter | may be empty only for the first topic of a subject without dependencies. For a chapter, the earlier-chapter topics it builds on; its own topics are added to its closure automatically (02 §2.5) |
| `maths.objectives` | string[] 2–6 | ✔ topic | each starts with an observable verb (*state, compute, prove, decide, sketch, explain, apply, estimate, recognise, …*); never *understand* or *know* |
| `maths.verify` | path | ✔ if status ≥ reviewed | must exist |
| `maths.widgets` | widget id[] | | must exist in `widgets/` (a mode of a widget, e.g. bisection, is configuration, not a separate id) |
| `maths.aliases` | path[] | | old URL paths of a moved page; `write_redirects.py` turns each into a redirect (02 §2.3) |
| `maths.reviewed_by` | string[] | ✔ if status ≥ reviewed | |
| `maths.sources` | string[] | | attribution; required if anything was adapted |
| `maths.depends_on` | subject code[] | subject pages only | cross-subject dependencies |

There is no `id` field: `label` is the ID. There is no `date` or `author`: git history is the
record. There is no `version`: the status plus git history covers it.

## 3.4 Block templates

Every block is a MyST directive. Snippets are in [`templates/blocks.md`](../../templates/blocks.md).

| Block | Directive | Label | Title | Notes |
|---|---|---|---|---|
| Definition | `:::{proof:definition} <Term>` | `def-…` required | the term being defined | the defined term in **bold** inside the body; followed by "In words:" unpacking |
| Theorem | `:::{proof:theorem} <Name>` | `thm-…` required | conventional name ("Squeeze theorem") or a short descriptive one | hypotheses first ("Let… Suppose…"), then the conclusion; each hypothesis needed |
| Lemma / Corollary / Proposition | `proof:lemma` / `proof:corollary` / `proof:proposition` | `lem-` / `cor-` / `prop-` | | corollaries reference their parent theorem in the first line |
| Proof (core) | `:::{proof:proof}` + `:enumerated: false`, directly after the statement | `prf-…` optional | none | renders "Proof". First line names the strategy ("We use the squeeze theorem with…"); ends at the end of the directive. The theme draws no ∎; `custom.css` adds one |
| Proof (rigorous) | `:::{proof:proof} Rigorous track` + `:enumerated: false` + `:class: dropdown` | `prf-<slug>` of the statement it proves (required unless directly after it, 02 §2.5) | "Rigorous track" | renders "Proof (Rigorous track)" |
| Proof sketch | `:::{proof:proof} Sketch` + `:enumerated: false` | | "Sketch" | says what is missing; under policy D, also where it is proved |
| Worked example | `:::{proof:example} <Goal>` | `eg-…` required | goal in imperative form ("Find …") | numbered steps; final result in `\boxed{}`; ends with **Check:** |
| Remark | `:::{proof:remark} <Topic>` | `rem-…` if referenced | | |
| Common mistake | `:::{warning} <Mistake in a few words>` | `rem-…` if referenced | | three parts: ✗ wrong, why, ✓ right |
| Rigorous aside | `:::{admonition} <Title>` + `:class: dropdown rigor` | | | for counterexamples and subtleties outside a proof |
| Exercise | `::::{exercise} <optional short title>` + `:class: tier-a\|tier-b\|tier-c` | `exr-…` required | | contains hint and answer dropdowns; see 07 |
| Solution | `::::{solution} exr-…` + `:class: dropdown` | `sol-…` required | | full worked solution |
| Widget | `::::{figure}` containing only ```` ```{anywidget} ../../../widgets/<w>.mjs ```` + JSON body, then the caption | `wdg-…` on the figure | caption = the text description | JSON validated against `schema/widgets/<w>.schema.json`; followed by **Try this:**. See 05 §5.8 for why the label and description live on the figure |
| Figure (static) | `:::{figure} ./img/<file>.svg` | `fig-…` | caption | SVG preferred; alt text required |
| Displayed equation | `$$ … $$ (eq-…)` | `eq-…` if referenced | | |

All of these block types were validated with `mystmd 1.11.0` in the Phase-0 PoC (see 05 §5.3),
including exercises with nested hint/answer dropdowns, solutions referencing exercises,
labelled equations, dropdown theorems and the `{anywidget}` directive.

### Writing a proof (house style)
- Start with the strategy: "We prove the contrapositive." / "Apply the MVT on $[x, x+h]$."
- Say which hypothesis is used at each step, *by name*: "Since $f$ is continuous on
  $[a,b]$ (hypothesis 1), the [extreme value theorem](#thm-calc-evt) gives…".
- One idea per paragraph, with displayed equations for anything you would point at.
- No "clearly", "obviously" or "trivially". If it is obvious, a short reason costs nothing.
- End by restating what was shown if the proof is longer than ~10 lines.

## 3.5 Chapter and subject pages

**Chapter `index.md`** contains `:::{topic-header}` (chapter-level objectives), the chapter
storyline (1–2 paragraphs), a topic table (title, time, difficulty, status), `## Review
exercises` (6–12 mixed exercises that require choosing a method), and `## Chapter summary`
(a concept map or bullet summary).

**Subject `index.md`** contains what the subject covers and for whom, how it relates to
other subjects (`maths.depends_on`), the chapter list, the Mermaid prerequisite map
generated by `graph.py`, and a "suggested paths" table (e.g. "Engineering Calculus I:
chapters 1–6; Calculus II: 7–11").

## 3.6 Plugins (rendering front matter)

`plugins/topic-header.mjs` (≈ 150 lines, MIT) registers two directives.

- `{topic-header}` reads the current file's front matter (`vfile.path`, parsed with the
  `yaml` npm package) and emits a MyST admonition with: prerequisites as
  `crossReference` nodes (MyST resolves them to page titles with hover previews), the
  objectives list, `est_minutes`, the difficulty as dots, and a status badge. A planned
  but unwritten prerequisite is rendered as plain text "(coming soon)".
- `{where-this-leads}` reads the front matter of every page in the toc of `content/myst.yml`
  once per build (cached), computes reverse edges, and emits links to pages that list this
  page as a prerequisite. It does not glob `content/**/*.md`, which would also match the
  stale page copies under `content/_build/`.

The PoC proved the key mechanism: a plugin directive reading `vfile.path`, emitting
`crossReference` nodes that MyST resolved to the target page title and URL.
