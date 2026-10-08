---
name: new-topic
description: The Author role (docs/plan/10 §10.3). Scaffold a topic page from its curriculum.yml entry with scripts/new_topic.py, then write it and walk the "How to add a topic" checklist of CLAUDE.md. Use for /new-topic <label>, or when asked to write or start a topic page.
argument-hint: <label>
---

# /new-topic: write a topic page (the Author)

You are the **Author** of the topic page `$ARGUMENTS`. You write the page and leave its
mathematics to be checked by others: a Verifier (`/verify-topic`, a different session) writes
the tests, a Reviewer (`/review-math`) reviews the proofs, and the owner approves.

If no label was given, run `uv run python scripts/graph.py ready calc` and ask which topic
to write. One topic per PR, on the branch `topic/<label>` (in a cloud session, the branch
you were assigned).

## 1. Scaffold

```bash
uv run python scripts/new_topic.py <label>
```

It writes the page at its `curriculum.yml` path (front matter from the entry, a statement and
the proof blocks its policy asks for, for every result in `results`), the verify file
`verify/<subject>/<chapter>/test_<topic>.py`, and the toc entry in `content/myst.yml`, then
runs `check_labels.py --update-lock`. Everything left to write is marked `TODO`.

**If it refuses** (exit code 2), stop and report its message. Never write the page by hand
to get round a refusal: a label that isn't in the curriculum needs a `curriculum` PR first,
and an existing page means the topic is already being written. If it prints "not ready",
you may draft ahead (10 §10.4), but say so in the PR: cite each result of an unmerged
prerequisite in plain text, followed by a `% TODO link: <label> once vronnblom/maths#<n> is
merged` comment, and list those lines in the PR body (they are the only lines `grep -n TODO`
may print while the prerequisite is open). When it merges, merge `main` into your branch,
turn every `% TODO link` into a named link, and check that the target's **merged statement**
says what your step uses; if it doesn't, ask for it on that page (a separate PR).

## 2. Read before writing

- the topic's entry in `content/<subject>/curriculum.yml`: title, prerequisites, objectives,
  results with proof policies (F/R/S/D, legend in `docs/plan/08-calculus-curriculum.md` §8.2),
  widgets, notes;
- `templates/topic.md` (structure) and `templates/blocks.md` (every block);
- `content/about/notation.md`, and `docs/plan/04-notation-and-style.md` §4.3 for the answer
  LaTeX subset;
- the pages of the direct prerequisites: reuse their labels, don't redefine anything;
- the exemplar `content/calculus/limits/limit-of-a-function.md`: the quality bar, and the
  model for every block (`docs/exemplar-review.md` is the rubric it was judged by);
- `uv run python scripts/graph.py closure <label>`: the only pages you may cite, except in a
  `looking-ahead` admonition.

## 3. Write the page

Follow CLAUDE.md (Conventions, Don't) and replace every `TODO`:
- the fixed structure: Why this matters → definitions → results → Worked examples → Common
  mistakes → Rigorous track → Summary → Exercises → Where this leads;
- every result of the entry, with its label and the proof its policy asks for; keep the
  scaffold's proof blocks (an R proof that isn't first carries `prf-<slug>`);
- ≥ 3 worked examples, each ending with a **Check**; ≥ 1 common mistake;
- 6–15 exercises across tiers, each with hints, exactly one Answer in the machine-checkable
  subset (or `answer manual` for a proof) and a collapsed `{solution}`;
- cite earlier results only as `[name](#label)`, naming the part or property you use
  (`[part (b) of the triangle inequality](#thm-calc-triangle-inequality)`), and only what the
  cited **statement** says; no "clearly", en-GB spelling;
- every step says what it rests on (a hypothesis, a definition clause, a cited result), and
  before multiplying or dividing an inequality, state the sign of the factor and name the order
  rule (`templates/blocks.md`, "Steps that say what they rest on"). These two were the most
  frequent findings of the Phase 1a reviews;
- only what the prerequisite closure provides. If the page needs a few school facts from
  outside it (values of $\sin$, say), ask the owner in the PR: either a `curriculum` PR adds the
  prerequisite, or the owner rules them allowed and you add the labelled "Facts from school
  used on this page" box (`templates/blocks.md`). Replace anything the closure can replace;
- displays that fit a phone: units in the sentence, long chains split with `aligned`, lists of
  facts as bulleted lists (CLAUDE.md, "Displays on a phone");
- the `function-plot` widget where the entry plans it (its figure, caption and **Try this:**;
  after adding a `table`, run `uv run python widgets/_tests/make_fixtures.py`, and again after
  any edit that moves lines on the page: the fixtures record line numbers). Planned widgets
  that aren't built stay out of `maths.widgets`. Captions and prose report what a widget
  observed, never "the limit is (not) $L$" or "the largest $\delta$ is" (CLAUDE.md, "Widget
  wording").

Keep `status: draft`.

## 4. The verify file: stubs only

```bash
uv run python scripts/new_topic.py --stubs <label>
```

This adds one `@covers` stub with `pytest.skip("for the verifier")` for every `eg-`/`exr-`
label on the page that has none yet. Stubs count as uncovered. **Do not compute expected
values or write real tests**: the Verifier derives them independently, and that independence is
what makes verification mean something (06 §6.1, 10 §10.1).

## 5. Finish

```bash
uv run python scripts/check_labels.py --update-lock   # your new eg-/exr-/sol-/prf- labels
grep -n TODO content/<subject>/<chapter>/<topic>.md    # must print nothing
npm run all                                           # fix every error and warning
```

Then open the PR with `.github/pull_request_template.md` (type `topic`): the summary of the
mathematics, every result with its policy, and the coverage table that `check_coverage.py`
printed in `npm run verify` (0 % is expected before the Verifier).

## 6. After a review

Answer every thread: fix it and reply with the commit, or argue back. Then post one comment
for the Verifier that lists **every** change to mathematical content (answers, displayed steps,
claims in prose, captions), separately from wording and link changes, so the second pass
(`/recheck-topic`) knows what to re-test. Never edit the tests.

If `main` has moved, merge it (a merge commit, never a rebase). Conflicts in `content/myst.yml`
and `labels.lock`: keep both sides, with the toc in `curriculum.yml` order, then run
`uv run python scripts/check_labels.py --update-lock` and `npm run check`.

## Never

These are the guardrails of 10 §10.5 and CLAUDE.md:
- set `status: reviewed` or `verified`, add anyone to `maths.reviewed_by`, or add a
  `maths.manual_checked` entry;
- write expected values in the verify file;
- rename or delete a label, or change another page's mathematics (that is a separate PR);
- add dependencies, front-matter keys, directive kinds or widget types;
- copy from non-compatible sources (07 §7.4); list adapted CC BY / CC BY-SA sources in
  `maths.sources`;
- prove a result with a tool that depends on it (08 §8.3).

If a mathematical convention is unclear and `content/about/notation.md` doesn't settle it, ask
in the PR rather than inventing one.
