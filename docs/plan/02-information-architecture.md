# 2. Information architecture

## 2.1 Hierarchy

```
Site
└── Subject            e.g. Calculus                     → folder   content/calculus/
    └── Chapter        e.g. Limits                       → folder   content/calculus/limits/
        └── Topic page e.g. The Limit of a Function      → file     content/calculus/limits/limit-of-a-function.md
            └── Block  definition / theorem / proof / example / exercise / solution / remark / widget
                                                         → labelled MyST directive inside the page
```

- **Subject**: a coherent university course area with its own landing page and subject code.
- **Chapter**: 3–10 topic pages that are taught together. It has an `index.md` overview
  (chapter map, objectives, mixed review problems).
- **Topic page**: the unit of authoring, review, status and prerequisites. It takes roughly
  **20–45 minutes of reading** and holds 1–4 definitions, 1–5 main results, 3–8 worked
  examples and 6–15 exercises. If a page grows past that, split it.
- **Block**: the *atomic unit of knowledge*. Blocks are not separate files. They are labelled
  directives inside topic pages. MyST gives every labelled block a URL anchor, cross-page
  links and a **hover preview**, so blocks can be addressed individually without the
  overhead of one file per theorem.

> **Why not one file per theorem?** It gives tiny pages with no narrative, hundreds of
> navigation entries, and lost context ("why do we care?"). Hover previews give us
> addressability without fragmenting the reading experience.

## 2.2 Repository layout

```
maths/
├── PLAN.md                      # entry point to this plan
├── README.md                    # what the project is, how to build, links (Phase 0)
├── CLAUDE.md                    # instructions for AI agents (and a good summary for humans)
├── CONTRIBUTING.md              # Phase 0
├── LICENSE                      # MIT (code: scripts, widgets, plugins, config)
├── LICENSE-CONTENT.md           # CC BY-SA 4.0 (everything under content/)
├── package.json                 # pins mystmd; npm scripts are the task runner
├── package-lock.json
├── pyproject.toml               # Python tooling (verification + checks), managed by uv
├── uv.lock
├── content/                     # ← the MyST project root (myst.yml lives here)
│   ├── myst.yml                 # project + site config, toc, KaTeX macros
│   ├── index.md                 # site home: subject cards, how to use the site
│   ├── about/
│   │   ├── how-to-read.md       # core vs rigorous track, statuses, exercise tiers
│   │   ├── notation.md          # published notation guide (from 04-notation-and-style)
│   │   ├── status.md            # dashboard: pages by status (generated table)
│   │   └── errata.md            # public log of corrected errors in verified pages
│   ├── calculus/
│   │   ├── index.md             # subject landing: overview, chapter list, prerequisite map
│   │   ├── preliminaries/
│   │   │   ├── index.md
│   │   │   ├── real-numbers-and-intervals.md
│   │   │   └── …
│   │   ├── limits/
│   │   │   ├── index.md
│   │   │   ├── limit-of-a-function.md
│   │   │   ├── limit-laws.md
│   │   │   └── …
│   │   └── …                    # one folder per chapter (see 08)
│   ├── linear-algebra/          # future subject: same shape
│   └── multivariable-calculus/  # future subject: same shape
├── widgets/                     # reusable interactive widgets (anywidget ES modules)
│   ├── function-plot.mjs
│   ├── epsilon-delta.mjs
│   ├── _lib/                    # shared helpers (board setup, sliders, a11y text)
│   └── README.md                # widget catalogue: purpose + JSON config schema per widget
├── verify/                      # SymPy/pytest verification, mirrors content/
│   ├── conftest.py
│   ├── mathcheck/               # helper package: @covers registry, LaTeX→SymPy, equality checks
│   └── calculus/
│       └── limits/
│           └── test_limit_of_a_function.py
├── schema/
│   ├── page.schema.json         # front-matter schema for all pages
│   └── widgets/*.schema.json    # one JSON schema per widget config
├── scripts/                     # repository checks (Python, stdlib + pyyaml/jsonschema)
│   ├── check_all.py             # runs every check below; used by CI and `npm run check`
│   ├── check_frontmatter.py
│   ├── check_labels.py
│   ├── graph.py                 # prerequisite graph: validate, render Mermaid, list ready topics
│   ├── check_toc.py
│   ├── check_coverage.py        # verification coverage vs status
│   └── extract_answers.py       # exercise answers from MyST AST → JSON for verify/
├── templates/                   # copy these to start a page; see 03-content-model
├── docs/
│   └── plan/                    # this plan
└── .github/
    ├── workflows/ci.yml
    ├── workflows/deploy.yml
    ├── workflows/links.yml      # weekly external link check
    ├── ISSUE_TEMPLATE/{erratum,new-topic,widget}.yml
    ├── pull_request_template.md
    └── CODEOWNERS
```

### Why the MyST project root is `content/`

The PoC (see [05](05-tooling-and-build.md) §5.3) showed that with
`site.options.folders: true`, URLs mirror the folder tree *relative to `myst.yml`*. With
`myst.yml` in `content/`, the URL is `/calculus/limits/limit-laws`, not
`/content/calculus/limits/limit-laws`. Widgets outside the project root
(`../../../widgets/x.mjs`) still resolve and are copied, with a content hash, into the build.

## 2.3 Naming rules

| Thing | Rule | Example |
|---|---|---|
| Subject folder | kebab-case English noun phrase | `calculus`, `linear-algebra`, `multivariable-calculus` |
| Chapter folder | kebab-case, **no number prefix** | `limits`, `derivative-applications` |
| Topic file | kebab-case, describes the concept, **no number prefix** | `limit-of-a-function.md`, `chain-rule.md` |
| Widget file | kebab-case, describes the widget's function | `epsilon-delta.mjs` |
| Verify file | `test_<topic_file_with_underscores>.py`, mirroring the path | `verify/calculus/limits/test_limit_laws.py` |

**Order is defined only in the `toc` of `content/myst.yml`**, never in file names, so
reordering chapters never changes a URL. A renamed or moved page keeps its old URL as a
MyST `aliases:` entry in its front matter, but the page **label** never changes.

## 2.4 Stable IDs (labels)

All labels share **one global namespace** across the site, because a MyST project resolves
`[](#label)` across all its pages. Labels:

- use only `[a-z0-9-]`, which has been tested to round-trip through MyST unchanged;
- are **semantic, never positional** (`thm-calc-squeeze`, not `thm-2-3-1`);
- are **permanent**: never renamed or reused once merged to `main`. CI keeps a
  `labels.lock` file of every label ever published and fails if one disappears. Deleting a
  block requires an explicit tombstone entry (a redirect note) in the lock file.

### Subject codes

| Code | Subject | Status |
|---|---|---|
| `calc` | Calculus (single variable, series, intro ODE) | first implementation |
| `linalg` | Linear Algebra | next |
| `mvc` | Multivariable Calculus | after linalg |
| `found` | Foundations (logic, sets, proof techniques) | small, could start early (see 12) |
| `disc` | Discrete Mathematics | later |
| `prob` | Probability & Statistics | later |
| `ana` | Real Analysis | later (target for "D" proofs) |
| `ode` | Differential Equations | later |
| `cplx` | Complex Analysis | later |

### Label grammar

```
page label   :=  <subj>-<topic-slug>                   calc-limit-laws
              |  <subj>-<chapter-slug>-chapter         calc-limits-chapter   (chapter index.md)
              |  <subj>-subject                        calc-subject          (subject index.md)
block label  :=  <kind>-<subj>-<slug>                  thm-calc-squeeze
                                                       exr-calc-limit-laws-conjugate
kind         :=  def | thm | lem | cor | prop | ax     (statements)
              |  prf                                   (a proof, when referenced on its own)
              |  eg                                    (worked example; "ex" is avoided: ambiguous)
              |  exr | sol                             (exercise / its solution)
              |  rem                                   (remark, common mistake, note)
              |  eq | fig | tbl | sec | wdg            (equation, figure, table, section, widget)
```

Rules for the slug:
- Statements are named after the mathematics: `thm-calc-mvt`, `def-calc-continuity`,
  `thm-calc-ftc-1`.
- Examples and exercises are prefixed by their topic slug, which keeps them unique and
  self-locating: `eg-calc-limit-laws-rational`, `exr-calc-chain-rule-nested-trig`.
- Solutions mirror their exercise: `exr-calc-x-y` → `sol-calc-x-y`.
- Page labels match the file name where possible: `limit-laws.md` → `calc-limit-laws`.
  (Exception: the exemplar `limit-of-a-function.md` uses the shorter `calc-limit`.)

### Referencing conventions

| Situation | Syntax | Renders as |
|---|---|---|
| Same page | `[](#thm-calc-squeeze)` | "Theorem 2" (page-local number) |
| Another page | `[the squeeze theorem](#thm-calc-squeeze)` | named link with hover preview |
| Name only | `[{name}](#thm-calc-squeeze)` | the block title |
| Page | `[](#calc-limit-laws)` | the page title |

**Rule:** cross-page references must use explicit link text or `{name}`. Numbers restart on
every page, so a bare "Theorem 2" pointing to another page is ambiguous.

## 2.5 Prerequisite / dependency graph

### Nodes and edges
- **Nodes are topic pages** (page labels). Blocks are not graph nodes, because block-level
  graphs are too fine-grained to maintain by hand.
- **Edges** are declared on the dependent page:
  `maths.prerequisites: [calc-limit, calc-functions]`. An edge means "you should be able to
  do this before reading this page".
- Only **direct** prerequisites are listed. CI warns if a listed prerequisite is already
  implied transitively, which keeps the lists short.
- **Edges may cross subjects**: `mvc-partial-derivatives` lists `calc-derivative`;
  `mvc-jacobian` lists `linalg-determinant`. Subjects also declare subject-level
  dependencies in their `index.md` (`maths.depends_on: [calc, linalg]`), and CI checks that
  every cross-subject edge points into a declared dependency subject.
- An edge may point to a topic that is *planned but not written*, if that topic is listed in
  the subject's curriculum file `content/<subject>/curriculum.yml`. It then renders as an
  unlinked "coming soon" item. This lets authors work in parallel.

### `curriculum.yml` (one per subject)

This is the machine-readable form of [08](08-calculus-curriculum.md). It is the **plan**,
while the page front matter is the **truth** for written pages. CI checks that the two
agree once a page exists.

```yaml
# content/calculus/curriculum.yml
subject: calc
chapters:
  - slug: limits
    title: Limits
    topics:
      - label: calc-limit
        file: limits/limit-of-a-function.md
        title: The Limit of a Function
        prerequisites: [calc-functions, calc-absolute-value-inequalities]
        widgets: [epsilon-delta, function-plot]
      - label: calc-limit-laws
        file: limits/limit-laws.md
        title: Limit Laws
        prerequisites: [calc-limit]
```

### What `scripts/graph.py` does

| Command | Purpose |
|---|---|
| `graph.py check` | every prerequisite resolves (to a page or a planned topic); no cycles (stdlib `graphlib.TopologicalSorter`); cross-subject edges respect `depends_on`; warns about redundant transitive edges |
| `graph.py mermaid calc` | writes `content/calculus/_generated/prereq-map.md`, a Mermaid `flowchart` included on the subject landing page (MyST renders Mermaid natively) |
| `graph.py ready calc` | lists planned topics whose prerequisites all have `status ≥ reviewed`. This is the queue for parallel authoring ([10](10-ai-agents.md)). |
| `graph.py closure calc-mean-value-theorem` | prints all transitive prerequisites; used by the forward-reference check |

### Forward-reference check (`check_labels.py --forward-refs`)

For every cross-reference on page P to a block on page Q, Q must be P itself, in P's
transitive prerequisite closure, or the reference must sit inside an admonition with
class `see-also` / `looking-ahead`. Anything else is a warning, and an error on pages with
`status: verified`. This is how "no circular reasoning" is enforced mechanically across
pages.

### Rendering the graph to readers
- On each topic page, a **"Before you start"** box lists direct prerequisites as links (with
  hover previews), and a **"Where this leads"** section lists pages that depend on this one.
  Both come from the graph, not hand-maintained lists (see 03 §3.3).
- On each subject page, a Mermaid map of chapters and topics.
- Later (Phase 7), an interactive graph widget (`widgets/prereq-graph.mjs`) reading a
  generated `graph.json`, so a learner can click a topic and see everything it needs.

## 2.6 Adding a new subject (the scale test)

1. Pick a subject code and add it to the table in §2.4 (and to `schema/page.schema.json`'s
   `subject` enum).
2. Create `content/<subject>/` from `templates/subject-index.md` (as `index.md`) and
   `templates/chapter-index.md` (one per chapter folder), plus `curriculum.yml`.
3. Write `curriculum.yml` (chapters, topics, prerequisites, proof policies) and get it
   reviewed in its own PR. Cross-subject edges go here too.
4. Add the subject block to the `toc` in `content/myst.yml`.
5. Author topics exactly as for Calculus. Every script, check, widget and template applies
   unchanged.

Nothing else changes: no new tooling, no new config schema, no restructuring.
