# 11. Contribution, licensing and governance

## 11.1 Licences

| What | Licence | File | Why |
|---|---|---|---|
| Content: everything under `content/` (text, math, figures, exercise text, widget JSON configs) | **CC BY-SA 4.0** | `LICENSE-CONTENT.md` | Share-alike keeps derivatives open; compatible with Wikipedia and Active Calculus (2018+), so we can reuse from and contribute to them |
| Code: `widgets/`, `plugins/`, `scripts/`, `verify/`, `schema/`, config, workflows | **MIT** | `LICENSE` | Lets anyone reuse widgets and tooling, including in non-open projects; standard for small JS/Python code |
| Third-party code (JSXGraph, KaTeX, mystmd) | their own (MIT/LGPL/MIT) | – | loaded or installed as dependencies, never copied into our tree without their licence header |

MyST shows both licences on every page via `project.license: {content: CC-BY-SA-4.0, code: MIT}`
in `myst.yml`.

**Inbound = outbound**: contributions are accepted under the same licences. No CLA. When
the repo opens to outside contributors, we add the **DCO** (`Signed-off-by:` trailer, enforced
by the DCO GitHub App). It is lightweight and makes provenance explicit. AI-generated
contributions are attributed in commit trailers (`Co-Authored-By:`), and the human who merges
them takes responsibility for their review.

## 11.2 `CONTRIBUTING.md` outline (written in Phase 0)

1. **Ways to help**: report an error (most valuable), suggest an exercise, improve an
   explanation, write a topic, build a widget.
2. **Reporting errors**: use the *Erratum* issue form (§11.4).
3. **Before you write**: read `docs/plan/01` (principles), `04` (notation), `03` (content
   model) and the exemplar page; check `curriculum.yml` and open issues to avoid duplicates;
   for a new topic, open a *New topic* issue first.
4. **Setup**: `npm ci && uv sync`, then `npm run dev`; `npm run all` before pushing.
5. **Writing a topic**: copy `templates/topic.md`; label rules; one topic per PR.
6. **Verification**: how to write `verify/` tests; the answer LaTeX subset; `manual` answers.
7. **Pull requests**: PR template checklist; CI must be green; review expectations and
   response times (best effort, typically within a week).
8. **Sources and licensing**: only original material or material under CC BY / CC BY-SA;
   list sources; never paste from proprietary textbooks.
9. **Style**: en-GB spelling, house style for proofs, accessibility rules.
10. **Code of conduct**: Contributor Covenant 2.1 (`CODE_OF_CONDUCT.md`).
11. **For AI agents**: see `CLAUDE.md`.

## 11.3 Roles and decision-making

| Role | Who (now) | Can |
|---|---|---|
| Maintainer | @vronnblom | merge; approve status changes; decide curriculum and architecture |
| AI agents | Claude Code sessions | draft, verify, review; open PRs; never merge |
| Contributors (later) | anyone | issues and PRs |
| Subject reviewers (later) | trusted contributors per subject | approve the mathematics in their subject (CODEOWNERS per `content/<subject>/`) |

- **CODEOWNERS** from day one: `* @vronnblom`. Per-subject owners are added as the project
  opens up.
- **Architecture decisions** (tooling, schema, label grammar, licence) are recorded as short
  ADRs in `docs/decisions/NNNN-title.md` (context, decision, consequences). The plan
  documents in `docs/plan/` serve as ADR 0000. Later changes get their own ADR, so the
  plan doesn't silently drift.
- **Curriculum changes** (adding, splitting or reordering topics, changing proof policies) go
  through a `curriculum` PR approved by the maintainer.

## 11.4 Errata process

**Report**: the site header has a "Report an error" action (configured in `myst.yml`) that
opens the erratum form, and every topic and chapter page ends with a pre-filled link to it:
the last line of `{where-this-leads}` (the plugin, 03 §3.6), "Found an error on this page?
Report it", built from `project.github`. It fills in the form's `page` field with the page's
label and source file (e.g. `calc-limit (content/calculus/limits/limit-of-a-function.md)`)
and the issue title. That pair identifies the page exactly, and unlike the page URL it does
not depend on the site's base URL (`/maths` on Pages, `/` in the CI preview), which the
plugin does not know. Meta pages and the subject page have only the header action (they have
no `{where-this-leads}`). The issue form `.github/ISSUE_TEMPLATE/erratum.yml` (stage 5) asks for:
- the page (pre-filled from the page's link) and the **label** of the block
  (definition/theorem/exercise) if known;
- type: *mathematical error* · *unclear/misleading* · *typo/formatting* · *broken widget/link*;
- what is wrong, and the suggested correction (optional);
- how they found it (optional; helps write a regression test).

**Triage** (target: within a week): labels `erratum` + `severity:math|clarity|typo|widget`;
assign; confirm or close with an explanation.

**Fix**:
1. Branch `erratum/<issue-number>`; fix the page.
2. For a computational error: **add a regression test first** (it must fail on the old
   content), then fix.
3. For a mathematical error in a `verified` page: the PR also adds an entry to
   `content/about/errata.md` (date, page, label, what was wrong, what changed, issue link).
   Transparency about corrected errors is part of being trustworthy.
4. Ask: *why did QA miss this?* If a checklist item or check would have caught it, update
   06 / the checker in the same or a follow-up `tooling` PR.

**Severity → status**: a confirmed *mathematical error* on a `verified` page immediately gets
a visible "Known issue: see #123" admonition (a one-line PR) until fixed. The status is not
downgraded unless the error shows systematic review failure on that page.

## 11.5 Issue and PR templates (Phase 0, built in stage 5)

- `ISSUE_TEMPLATE/erratum.yml` (above)
- `ISSUE_TEMPLATE/new-topic.yml`: label, subject, chapter, proposed prerequisites, objectives,
  and why the topic is needed
- `ISSUE_TEMPLATE/widget.yml`: purpose, the topic(s) it serves, interaction sketch, the
  mathematics it computes
- `ISSUE_TEMPLATE/config.yml`: the issue chooser, with links to `CONTRIBUTING.md` and the site
  (blank issues stay allowed)
- `pull_request_template.md`: type of PR; summary of the mathematics; theorems added with
  F/R/S/D; verification coverage (pasted from `check_coverage.py`); proof checklist (06 §6.3)
  for topic PRs; screenshots of new widgets; "I have not copied from incompatible sources" ✔.
  The proof checklist is a copy of 06 §6.3; `tests/test_github_templates.py` fails if the two
  drift apart (it also checks the erratum form's field ids, which the page links fill in).

## 11.6 Versioning and releases

- `main` is always deployable and deployed.
- Subject releases are tagged `calc-1.0`, `linalg-1.0`, … when a subject meets its definition
  of done. A release note lists pages, statuses and errata since the previous release.
- Labels are permanent across releases, so citing `…/calculus/limits/squeeze-theorem#thm-calc-squeeze`
  stays valid. If the page ever moves, its old path gets a redirect (02 §2.3).
