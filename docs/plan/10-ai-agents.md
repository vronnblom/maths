# 10. Working with AI agents

The repository is designed so that most content can be **drafted by AI agents and verified
by machines and the owner**. Agents follow `CLAUDE.md` at the repo root (v1 since Phase 0
stage 5). This document explains the workflow behind it.

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

### The role prompts: the skills in `.claude/skills/`

The three role prompts live in one place only, the Claude Code skills that run them (built in
Phase 0 stage 5; `docs/agents/README.md` is the index):

| Role | Skill | What it does |
|---|---|---|
| Author | `/new-topic <label>` ([`.claude/skills/new-topic/SKILL.md`](../../.claude/skills/new-topic/SKILL.md)) | scaffolds the page, the verify file (`@covers` stubs only) and the toc entry with `scripts/new_topic.py`, then writes the page and walks the "How to add a topic" checklist; never computes expected values |
| Verifier | `/verify-topic <path>` ([`.claude/skills/verify-topic/SKILL.md`](../../.claude/skills/verify-topic/SKILL.md)) | writes the SymPy tests from the statements only, reads answers with `answer(label)`, never edits the page, reports disagreements with evidence |
| Reviewer | `/review-math <path>` ([`.claude/skills/review-math/SKILL.md`](../../.claude/skills/review-math/SKILL.md)) | reviews against the 06 §6.3 checklist and the 08 §8.3 circularity table, tries counterexamples, checks proof policies, ranks findings by severity, never rewrites the page |

A person or an agent without Claude Code reads the same files as prompts. Change a role by
changing its skill; this section only says which skill holds it.

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
  mechanical, and PR descriptions follow a fixed template
  (`.github/pull_request_template.md`: summary of mathematical content,
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
- Never mark `status: reviewed`/`verified`; never add yourself to `reviewed_by`; never add a
  `maths.manual_checked` entry (the reviewer's note for a `manual` answer, 06 §6.6).
- Never weaken a test to make it pass; report the disagreement instead.
- Never add dependencies, new front-matter keys or new directive kinds without a `tooling` PR.
- Never copy text, exercises or figures from non-compatible sources ([07 §7.4](07-exercises.md));
  record every adapted source in `maths.sources`.
- Never use L'Hôpital, derivatives or series to prove a fact the curriculum uses to *build*
  them (see the circularity table).
- When unsure about a mathematical convention, follow `content/about/notation.md`. If it
  doesn't say, ask in the PR rather than inventing one.

## 10.6 Repository support for agents (built in Phase 0)

- **`CLAUDE.md`**: conventions, commands, procedures and "don'ts" (v1 since Phase 0 stage 5).
- **SessionStart hook** (`.claude/settings.json` → `.claude/hooks/session-start.sh`): in a
  cloud session only (`CLAUDE_CODE_REMOTE=true`; on a laptop it exits at once), it runs
  `npm ci` (skipped when `node_modules/` was installed from the current lockfile by the same
  Node version), `uv sync --frozen` and `scripts/fetch_theme.sh`, so `npm run all` works
  immediately. The theme comes with `git fetch`, which cloud sessions allow (05 §5.5), so no
  network-settings change is needed. A failing step stops it with exit code 2 and a message
  naming the step. It is synchronous, so the session starts with everything installed.
- **Skill `/new-topic <label>`** (`.claude/skills/new-topic/SKILL.md`): the Author. Runs
  `scripts/new_topic.py`, which scaffolds the page (front matter, every result with its
  proof-policy blocks), the verify file and the toc entry from the curriculum entry, refusing
  labels outside the curriculum and pages that exist; then walks the author checklist.
- **Skill `/verify-topic <path>`**: the Verifier.
- **Skill `/review-math <path>`**: the Reviewer.
- **`docs/agents/README.md`**: the index of the roles and their skills.
- **`.github/pull_request_template.md`**: the fixed PR description of §10.4 (11 §11.5).
