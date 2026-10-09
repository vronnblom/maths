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
- **Chapter**: 3–12 topic pages that are taught together. It has an `index.md` overview
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
│   ├── tags.yml                 # the controlled vocabulary for `tags` (03 §3.3)
│   ├── about/
│   │   ├── how-to-read.md       # core vs rigorous track, statuses, exercise tiers
│   │   ├── notation.md          # published notation guide (from 04-notation-and-style)
│   │   ├── status.md            # dashboard: pages by status (includes a generated table)
│   │   └── errata.md            # public log of corrected errors in verified pages
│   ├── calculus/
│   │   ├── index.md             # subject landing: overview, chapter list, prerequisite map
│   │   ├── _generated/          # prereq-map.md, written by scripts/generate.py (git-ignored)
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
│   ├── _lib/                    # shared helpers + pure maths modules (published via static_files)
│   ├── _tests/                  # node --test against SymPy-computed fixtures (make_fixtures.py)
│   └── README.md                # widget catalogue: purpose + JSON config schema per widget
├── plugins/                     # the MyST plugin (03 §3.6), registered in myst.yml
│   ├── topic-header.mjs         # {topic-header}, {where-this-leads}, {chapter-topics}
│   ├── _lib/header.mjs          # its logic: front matter → AST nodes (pure)
│   └── _tests/                  # node --test, run by `npm run test:widgets`
├── verify/                      # SymPy/pytest verification, mirrors content/ (06 §6.1)
│   ├── conftest.py              # loads _answers.json (refuses a stale one), records coverage
│   ├── mathcheck/               # helper package: @covers registry, LaTeX→SymPy, equality checks
│   ├── test_mathcheck.py        # the harness's own tests; fixtures/ holds its AST fixture
│   └── calculus/
│       └── limits/
│           └── test_limit_of_a_function.py
├── schema/
│   ├── page.schema.json         # front-matter schema for all pages
│   ├── curriculum.schema.json   # the shape of content/<subject>/curriculum.yml
│   └── widgets/*.schema.json    # one JSON schema per widget config
├── labels.lock                  # every label ever merged (§2.4, 06 §6.7)
├── tests/                       # the checkers' tests; fixtures/ holds one broken project per check
├── scripts/                     # repository checks (Python, stdlib + pyyaml/jsonschema)
│   ├── check_all.py             # runs every check below; used by CI and `npm run check`
│   ├── check_frontmatter.py
│   ├── check_labels.py
│   ├── graph.py                 # prerequisite graph: validate, render Mermaid, list ready topics
│   ├── check_toc.py
│   ├── check_coverage.py        # verification coverage (recorded by the pytest run) vs status
│   ├── check_verified_edits.py  # PR guard for edits to verified pages (06 §6.6)
│   ├── extract_answers.py       # exercise answers from MyST AST → JSON for verify/
│   ├── generate.py              # generated includes: prerequisite maps, status table
│   ├── write_redirects.py       # redirect pages for old URLs (§2.3), run by build_site.sh
│   ├── project.py               # shared: the toc, front matter with line numbers, curricula, diagnostics
│   ├── myst_source.py           # the small MyST source parser the label and notation checks use
│   ├── notation_lint.py         # the notation lint, run by check_all.py
│   ├── check_widgets.py         # widget figures, files and configs, run by check_all.py
│   ├── build_site.sh            # the gated site build (05 §5.5)
│   ├── myst_gate.sh             # the ⛔️/⚠️ log gate around `myst build`, used by build_site.sh and tests/
│   └── fetch_theme.sh           # the pinned book-theme via git, for cloud sessions (05 §5.5)
├── templates/                   # copy these to start a page; see 03-content-model
├── docs/
│   └── plan/                    # this plan
└── .github/
    ├── workflows/ci.yml
    ├── workflows/guard.yml      # verified-page edit guard, the only workflow that runs on label changes
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
Only that one file is copied, so the shared `widgets/_lib/` is published separately
(05 §5.8).

## 2.3 Naming rules

| Thing | Rule | Example |
|---|---|---|
| Subject folder | kebab-case English noun phrase | `calculus`, `linear-algebra`, `multivariable-calculus` |
| Chapter folder | kebab-case, **no number prefix** | `limits`, `derivative-applications` |
| Topic file | kebab-case, describes the concept, **no number prefix** | `limit-of-a-function.md`, `chain-rule.md` |
| Widget file | kebab-case, describes the widget's function | `epsilon-delta.mjs` |
| Verify file | `test_<topic_file_with_underscores>.py`, mirroring the path (basenames may repeat, e.g. every chapter's `test_index.py`; pytest runs in `importlib` mode, 05 §5.5) | `verify/calculus/limits/test_limit_laws.py` |

**Order is defined only in the `toc` of `content/myst.yml`**, never in file names, so
reordering chapters never changes a URL. The page **label** never changes, but moving a page
to another folder changes its URL. mystmd 1.11 has no redirect feature (an `aliases:`
front-matter key is ignored with a warning), so a moved page lists its old paths in
`maths.aliases: [/calculus/limits/limit-laws]`. After every site build (`scripts/build_site.sh`,
so locally, in CI and on deploy), `scripts/write_redirects.py` writes a small `index.html` at
each old path, with a `<meta http-equiv="refresh">` and a canonical link to the new URL. Both
paths are prefixed with `BASE_URL` (`/maths` on deploy), the same variable mystmd uses. The
script fails if an old path collides with a live page, so a collision fails the PR, not the
deploy.

## 2.4 Stable IDs (labels)

All labels share **one global namespace** across the site, because a MyST project resolves
`[](#label)` across all its pages. Labels:

- use only `[a-z0-9-]`, which has been tested to round-trip through MyST unchanged;
- are **semantic, never positional** (`thm-calc-squeeze`, not `thm-2-3-1`);
- are **permanent**: never renamed or reused once merged to `main`. The committed
  `labels.lock` lists every label ever merged. CI fails if a label in the content is missing
  from the lock (authors add new ones with `check_labels.py --update-lock`) and if a locked
  label disappears. Deleting a block requires an explicit tombstone entry (a redirect note)
  in the lock file (06 §6.7).

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
              |  site-<slug>                           site-notation         (meta pages: content/index.md, about/*)
block label  :=  <kind>-<subj>-<slug>                  thm-calc-squeeze
                                                       exr-calc-computing-limits-conjugate
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
  self-locating: `eg-calc-computing-limits-factor`, `exr-calc-chain-rule-nested-trig`.
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

This is the machine-readable form of [08](08-calculus-curriculum.md); since Phase 0 stage 2
it is the source, and 08 the commentary. It is the **plan**, while the page front matter is
the **truth** for written pages. `graph.py check` fails if a written topic page disagrees with
its entry (label, file, title, level, prerequisites), or if a topic page is not in the
curriculum at all. Its shape is `schema/curriculum.schema.json`.

```yaml
# content/calculus/curriculum.yml
subject: calc
chapters:
  - slug: limits
    title: Limits
    topics:
      - label: calc-limit
        file: limits/limit-of-a-function.md      # relative to content/calculus/
        title: The Limit of a Function
        level: core                              # core | extension
        prerequisites: [calc-functions, calc-absolute-value-inequalities]
        objectives:
          - Estimate limits from tables and graphs and explain how this can mislead.
          - …
        widgets: [epsilon-delta, function-plot]
        results:                                 # labels to write, with the proof policy (08 §8.2)
          - {label: def-calc-limit, note: "precise definition, in core with intuitive unpacking"}
          - {label: thm-calc-limit-unique, policy: R}
          - …
        notes: [gold-standard page, …]
      - label: calc-limit-laws
        file: limits/limit-laws.md
        title: Limit Laws
        level: core
        prerequisites: [calc-limit]
        objectives: […]
        results:
          - {label: thm-calc-limit-laws, policy: F+R+S, note: "sum F as the model ε/2 proof; product, quotient R; power, root S"}
```

A result's `policy` is one letter or a combination such as `S+R` (a sketch in the core, the
full proof in the rigorous track) or `S+D` (a sketch here, the proof deferred). With `D`,
`deferred_to` names a later topic, another subject's code, or `out-of-scope`; `graph.py check`
rejects a target that is in the topic's own prerequisite closure.

### What `scripts/graph.py` does

| Command | Purpose |
|---|---|
| `graph.py check` | `curriculum.yml` matches its schema; every prerequisite resolves (to a page or a planned topic); no cycles (stdlib `graphlib.TopologicalSorter`); cross-subject edges respect `depends_on`; written pages agree with the curriculum; warns about redundant transitive edges |
| `graph.py mermaid calc` | writes `content/calculus/_generated/prereq-map.md`, included on the subject landing page (MyST renders Mermaid natively): a flowchart of the chapters, then one flowchart per chapter with its topics and their prerequisites from other chapters. (One flowchart of all 82 topics was tried in stage 2: scaled to the page width it is unreadable.) Planned topics are dashed; written ones are coloured by status and link to their page. Run before every build by `scripts/generate.py` (05 §5.7). |
| `graph.py ready calc` | lists planned (not yet written) topics whose prerequisites are all written and have `status ≥ reviewed`. This is the queue for parallel authoring ([10](10-ai-agents.md)). |
| `graph.py closure calc-mean-value-theorem` | prints all transitive prerequisites; used by the forward-reference check |

### Forward-reference check (`check_labels.py --forward-refs`)

For every cross-reference on page P to a block on page Q, one of these must hold:
- Q is in P's transitive prerequisite closure;
- Q is P itself, and the reference is **not** inside a proof or a solution;
- Q is P itself, the reference is inside a **proof**, and the target block comes earlier on
  the page than the **statement that proof proves**. Comparing with the position of the
  citation is not enough: policy-R proofs may sit in the `## Rigorous track` section, below
  several statements, and two such proofs could then cite each other's theorems;
- Q is P itself, the reference is inside a **proof**, and the target is **exactly the
  statement that proof proves** (e.g. `prf-calc-limit-laws` linking to
  `thm-calc-limit-laws`, so that a rigorous-track proof can say what it proves). Every
  other block from that statement on stays forbidden;
- Q is P itself, the reference is inside a **solution**, and the target block comes earlier
  on the page than the reference;
- the reference sits inside an admonition with class `see-also` / `looking-ahead` (or a
  `{seealso}` admonition);
- Q is a meta page (`site-…`: notation, how to read, …). Meta pages document the site, so
  they are also exempt as P.

A reference to a label that no page in the toc has is always an error (the build would fail
on it too).

**Which statement a proof proves.** A proof directly after a statement block proves that
statement. A proof anywhere else (in practice, in the Rigorous track section) must carry the
label `prf-<slug>` of the statement `<kind>-<slug>` it proves, e.g. `prf-calc-limit-unique`
for `thm-calc-limit-unique`. `check_labels.py` fails on a proof that is neither directly
after a statement nor paired by label.

Anything else is a warning, and an error on pages with `status: verified`. This is how "no
circular reasoning" is enforced mechanically, across pages and within a page.

**Chapter index pages** are read after the chapter's topics, and their review exercises
cite those topics' results (07 §7.3). So the closure of a chapter `index.md` is its listed
prerequisites **plus every topic of the chapter** (from `curriculum.yml`) and their closures.
The same holds for a subject `index.md` and its chapters.

### Rendering the graph to readers
- On each topic page, a **"Before you start"** box lists direct prerequisites as links (with
  hover previews), and a **"Where this leads"** section lists pages that depend on this one.
  Both come from the graph, not hand-maintained lists (see 03 §3.3).
- On each subject page, a Mermaid map of chapters and topics.
- Later (Phase 7), an interactive graph widget (`widgets/prereq-graph.mjs`) reading a
  generated `graph.json`, so a learner can click a topic and see everything it needs.

## 2.6 Adding a new subject (the scale test)

1. Pick a subject code and add it to the table in §2.4, and to the subject lists in
   `schema/page.schema.json` (the `subject` enum and the label patterns),
   `schema/curriculum.schema.json` and `SUBJECTS` in `scripts/project.py`.
2. Create `content/<subject>/` from `templates/subject-index.md` (as `index.md`) and
   `templates/chapter-index.md` (one per chapter folder), plus `curriculum.yml`.
3. Write `curriculum.yml` (chapters, topics, prerequisites, proof policies) and get it
   reviewed in its own PR. Cross-subject edges go here too.
4. Add the subject block to the `toc` in `content/myst.yml`.
5. Author topics exactly as for Calculus. Every script, check, widget and template applies
   unchanged.

Nothing else changes: no new tooling, no new config schema, no restructuring.
