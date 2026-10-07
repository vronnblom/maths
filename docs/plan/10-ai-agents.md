# 10. Working with AI agents

The repository is designed so that most content can be **drafted by AI agents and verified
by machines and the owner**. Agents follow `CLAUDE.md` at the repo root (draft v0 committed
alongside this plan). This document explains the workflow behind it.

## 10.1 Principles

1. **Agents draft, machines check, the owner approves.** No agent marks its own work
   `reviewed` or `verified`.
2. **Separate the author from the verifier.** The agent that writes a page is never the one
   that writes its verification test or performs the adversarial review. Independent
   derivation is what makes verification meaningful.
3. **Small, independent units.** One topic page per PR. Each PR can be reviewed in under an
   hour and merged without waiting for any other open PR.
4. **The graph is the scheduler.** `scripts/graph.py ready calc` lists topics whose
   prerequisites are all `reviewed` or better, and those can be worked on in parallel.
5. **Everything an agent needs is in the repo**: templates, the curriculum entry (objectives,
   results, proof policies), the notation guide and the exemplar page. Prompts reference
   files; they don't restate conventions.

## 10.2 Unit of work and PR types

| PR type | Scope | Branch name | Typical author |
|---|---|---|---|
| `topic` | one topic page + its verify test + widget configs | `topic/calc-limit-laws` | author agent → verifier agent pushes the test to the same branch |
| `chapter-index` | one chapter `index.md` + review exercises | `chapter/calc-limits-chapter` | author agent, after all chapter topics are `reviewed` |
| `widget` | one widget module + schema + tests + catalogue entry | `widget/riemann-sum` | agent or owner |
| `curriculum` | changes to `curriculum.yml` / 08 (add, split or reorder topics, change prerequisites) | `curriculum/…` | owner (agents may propose) |
| `tooling` | scripts, CI, plugin, templates | `tooling/…` | agent or owner |
| `erratum` | fix a reported error (+ regression test) | `erratum/<issue>` | agent or owner |

Rules: topic PRs never modify other topic pages, except to add a link *to* the new page in
a "Where this leads" or "see also" section (and the plugin does most of that automatically).
Needing to change another page's mathematics means a separate PR.

## 10.3 The pipeline for one topic

```
graph.py ready ──► [1 Author agent] ──► draft page (status: draft), CI structural checks green
                         │
                         ▼
                  [2 Verifier agent] ──► verify/…/test_<topic>.py written *from the statements only*,
                         │               then run against the page; disagreements reported, not "fixed" silently
                         ▼
                  [3 Reviewer agent] ──► adversarial review with the 06 §6.3 checklist + 08 §8.3 circularity table;
                         │               posts findings as PR review comments
                         ▼
                  [1 Author agent] ──► addresses findings (or argues back in the thread)
                         │
                         ▼
                     Owner review ──► approves; status → reviewed (or verified if 100 % coverage + both checklists)
```

### Prompt templates (stored in `docs/agents/` in Phase 0)

**Author**
> Write the topic page `<label>` for the subject `<subject>`.
> Inputs: its entry in `content/<subject>/curriculum.yml` (title, prerequisites, objectives,
> results with proof policies, widgets), `templates/topic.md`, `templates/blocks.md`,
> `content/about/notation.md`, and the exemplar `content/calculus/limits/limit-of-a-function.md`
> as the quality bar. Read the pages of the direct prerequisites so you use their labels and
> don't redefine anything. Cite earlier results only via `[name](#label)`.
> Output: the page with `status: draft`, the new labels added to `labels.lock`
> (`check_labels.py --update-lock`), and a
> `verify/<subject>/<chapter>/test_<topic>.py` containing only the `@covers` skeleton: one
> `pytest.skip("for the verifier")` stub per `eg-` and `exr-` label (stubs count as uncovered).
> Run `npm run all` and fix every error and warning.
> Do **not** compute expected values in the test file.

**Verifier**
> For the page `<path>`, write the SymPy tests in `<test path>`. Derive every expected value
> **independently**: read the problem statements and displayed steps, but do not copy numbers
> from answers or solutions into the test. Use `answer(label)` to read the page's answers.
> For worked examples, assert each displayed equality. If a test fails, do **not** edit the
> page: report the label, the page's claim, your result and the SymPy evidence in the PR.

**Reviewer**
> Review `<path>` adversarially against `docs/plan/06-quality-assurance.md` §6.3 and the
> circularity table in `docs/plan/08-calculus-curriculum.md` §8.3. For every theorem, try to
> find a counterexample to the statement as written. For every proof, check each step and
> name the hypothesis it uses. Check that the proof policy (F/R/S/D) matches the curriculum.
> Report findings as review comments ranked by severity: wrong mathematics > missing
> hypothesis > gap in proof > unclear > style. Do not rewrite the page.

## 10.4 Running work in parallel

- **Waves from the graph**: after Phase 1a (which also brings `calc-limit`'s three
  Preliminaries prerequisites to `reviewed`), `graph.py ready calc` returns e.g.
  `{calc-one-sided-limits, calc-limit-laws, calc-tangents-rates, calc-function-operations,
  calc-polynomial-rational, calc-trig-functions, calc-sigma-notation}`.
  Each is an independent topic PR, run as one agent session per topic (cloud sessions or
  worktrees).
- **Drafting ahead**: topics whose prerequisites are still `draft` (or not yet written) may be
  drafted (they only need prerequisite *labels* to exist in the curriculum), but they can't
  move to `reviewed` until every prerequisite page exists and is `reviewed` (CI-enforced). This keeps agents busy without breaking the quality order.
- **The owner is the bottleneck**, so pace work to review capacity, about 3–6 topic PRs open
  at a time. Planned mitigations: agent review absorbs the first pass, CI absorbs everything
  mechanical, and PR descriptions follow a fixed template (summary of mathematical content,
  list of theorems with policies, verification coverage, checklist), so review is reading
  mathematics rather than hunting for context.
- **Conflicts** only arise in shared files: `content/myst.yml` (toc) and `labels.lock`.
  Both are append-mostly (`check_labels.py --update-lock` keeps the lock sorted, so
  conflicts are usually trivial). Agents rebase, re-run `--update-lock` and `npm run check`
  before requesting review.
  If toc conflicts become frequent, generate the toc from `curriculum.yml`
  ([05 §5.5](05-tooling-and-build.md)).

## 10.5 Guardrails for agents (summarised in `CLAUDE.md`)

- Never rename or delete a label; never change another page's mathematics in a topic PR.
- Never mark `status: reviewed`/`verified`; never add yourself to `reviewed_by`.
- Never weaken a test to make it pass; report the disagreement instead.
- Never add dependencies, new front-matter keys or new directive kinds without a `tooling` PR.
- Never copy text, exercises or figures from non-compatible sources ([07 §7.4](07-exercises.md));
  record every adapted source in `maths.sources`.
- Never use L'Hôpital, derivatives or series to prove a fact the curriculum uses to *build*
  them (see the circularity table).
- When unsure about a mathematical convention, follow `content/about/notation.md`. If it
  doesn't say, ask in the PR rather than inventing one.

## 10.6 Repository support for agents (built in Phase 0)

- **`CLAUDE.md`**: conventions, commands, procedures and "don'ts" (draft v0 is in the repo now).
- **SessionStart hook** (`.claude/settings.json`): runs `npm ci && uv sync` in cloud sessions
  so `npm run all` works immediately. This also needs the pinned theme to be reachable from
  the session (allowed in the environment's network settings, or vendored; 05 §5.5);
  Phase 0's definition of done checks it in a real cloud session.
- **Skill `/new-topic <label>`** (`.claude/skills/new-topic/SKILL.md`): scaffolds the page and
  verify file from templates and the curriculum entry, then walks the author checklist.
- **Skill `/verify-topic <path>`**: the verifier role as a reusable skill.
- **Skill `/review-math <path>`**: the reviewer role as a reusable skill.
- **`docs/agents/`**: the three prompt templates above and the PR description template.
