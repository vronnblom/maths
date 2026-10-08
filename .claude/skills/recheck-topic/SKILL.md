---
name: recheck-topic
description: The second pass (docs/plan/10 §10.3) - Verifier and Reviewer again, in one session, after the Author has answered the first review. Re-test what changed, re-review the page against the first review's findings, push test changes only, and post one review with a per-finding table, the manual-exercise verdicts, the coverage and a verdict. Use for /recheck-topic <path>, or when asked for the second pass, re-check or re-verify of a page.
argument-hint: <content/…/page.md>
---

# /recheck-topic: the second pass (Verifier and Reviewer again)

You are the **second pass** on `$ARGUMENTS`, after its first review and the Author's round of
fixes. You play both checking roles in one session: you update the tests (the Verifier) and you
re-review the page (the Reviewer). The owner waived the separation of those two roles for this
pass (it ran this way on vronnblom/maths#7, #8, #9 and #11); the separation from the Author
stays. If this session wrote the page, or any of the Author's fixes, stop and say that a
different session has to do the second pass (10 §10.1).

## Read first

- the first review (its findings table and every inline thread) and the first verifier report;
- every Author reply, and the Author's comment that lists the changes to mathematical content;
- the page in full, as it is now, and its verify file (`maths.verify`);
- the statements the page cites on its prerequisite pages, as merged on `main`;
- the skills `/verify-topic` and `/review-math`: their rules all apply here;
- `uv run python scripts/graph.py closure <page label>`.

## 1. Verify (test changes only)

- Re-test every changed claim from the Author's list: new or changed answers, displayed steps,
  claims in prose, captions, tables and **Try this** numbers. Derive every expected value
  independently, as `/verify-topic` says.
- Remove an assertion only when the page no longer prints its claim, and replace it with a test
  of what the page now says. Never weaken a test; say what you removed and why.
- Fix any mistake in your predecessors' tests or comments, and say so.
- Run `npm run verify` (and `npm run all` before pushing). Push a commit that changes files
  under `verify/` only; never the page, its front matter or its status.

## 2. Re-review

- Each finding of the first review: resolved, partly resolved or not, with the evidence (the
  line, the new wording, the test).
- Everything new or changed, reviewed as if for the first time, with the `/review-math`
  checklist and its list of what the Phase 1a reviews kept finding (the sign of each factor,
  what each step rests on, exact citations of parts and properties, the closure and any "Facts
  from school" box, `% TODO link` targets, widget wording, displays on a phone).
- The closure: every cited label is in `graph.py closure` or earlier on the page; anything
  used without a label is in the closure too, or in a "Facts from school" box.
- Consistency with the pages that cite this one, and with open PRs that will.
- New findings are inline review comments on their lines when they need a change; minor ones
  may stay in the review body.

## 3. Post one review

One PR review (event `COMMENT`), with these sections in this order:

1. **Verification**: the test commit, "Disagreements: none" or each disagreement (label, the
   page's claim, your result, the SymPy evidence), what each new test derives, and what was
   removed or fixed.
2. **The first review's findings**, a table: `| # | Verdict | Evidence |`, one row per finding
   (✅ resolved, ⚠️ partly, ❌ not), owner's rulings marked as such.
3. **New findings**, a table: `| # | Severity | Where | Finding |` (N1, N2, …, ranked as
   `/review-math` ranks them), or "none".
4. **The manual exercises**: for each `manual` Answer, "correct and complete" or what is
   missing, step by step, for the owner's `maths.manual_checked` note. You never add the note.
5. **Coverage**: the block that `check_coverage.py` printed, verbatim.
6. **The 06 §6.3 checklist**, re-walked for the new and changed material; for an exemplar page,
   the 09 §9.1 rubric (`docs/exemplar-review.md`).
7. **Verdict**: "ready for the owner", with the owner's remaining steps (CLAUDE.md, "Owner
   sign-off"), or "another author round", with the findings it needs.

## Never

- edit the page, its front matter or its status, add anyone to `maths.reviewed_by`, or add a
  `maths.manual_checked` entry (10 §10.5);
- push anything outside `verify/`;
- copy expected values from the page, or weaken a test to make it pass;
- soften a finding because the tests pass.
