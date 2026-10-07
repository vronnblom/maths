---
name: review-math
description: The Reviewer role (docs/plan/10 §10.3). Review a topic page adversarially with the proof checklist of docs/plan/06 §6.3 and the circularity table of docs/plan/08 §8.3, try counterexamples, check the proof policies, and report findings ranked by severity without rewriting the page. Use for /review-math <path>, or when asked to review a page's mathematics.
argument-hint: <content/…/page.md>
---

# /review-math: review a page's mathematics (the Reviewer)

You are the **Reviewer** of `$ARGUMENTS`. You must not be its author or its verifier: if this
session wrote the page or its tests, stop and say that a different session has to review it
(10 §10.1).

## Read first

```bash
sed -n '/^## 6.3/,/^## 6.4/p' docs/plan/06-quality-assurance.md    # the proof checklist
sed -n '/^## 8.3/,/^## 8.4/p' docs/plan/08-calculus-curriculum.md  # the circularity map and table
uv run python scripts/graph.py closure <page label>               # what the page may cite
```

and the page's entry in `content/<subject>/curriculum.yml` (results and their proof policies,
legend in 08 §8.2), its verify file (`maths.verify`) and the pages it cites.

## The task

Review the page adversarially against the 06 §6.3 checklist and the circularity table in
08 §8.3. For every theorem, try to find a counterexample to the statement as written. For
every proof, check each step and name the hypothesis it uses. Check that the proof policy
(F/R/S/D) matches the curriculum.

Also:
- walk the whole 06 §6.3 checklist (statements, proofs, examples and exercises, pedagogy), and
  say which items you checked;
- for every "fact now, proof later" item of the 08 §8.3 table that the page touches, check it is
  stated as such and not proved with a tool built on it;
- check that each cited result is in the closure above, or earlier on the same page;
- for solutions, check that they use only methods available at this point in the graph;
- recompute a sample of the examples and solutions yourself (SymPy via `uv run python` is fine).

## Report

Findings ranked by severity: **wrong mathematics > missing hypothesis > gap in proof >
unclear > style**. Each one names the label and the line, quotes the claim, says what is
wrong, and gives the evidence (a counterexample, the step that fails, the hypothesis that
isn't used). Post them as PR review comments on the lines concerned when there is a PR, else
report them here. End with the checklist, item by item: ✔, ✘ (with the finding) or n/a.

## Never

- rewrite the page or push changes to it: the Author addresses your findings;
- set `status`, add anyone to `maths.reviewed_by`, or add a `maths.manual_checked` entry: the
  owner does that when approving (10 §10.5, 06 §6.6);
- soften a finding because the tests pass: tests don't check proofs.
