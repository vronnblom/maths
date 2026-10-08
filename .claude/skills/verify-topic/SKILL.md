---
name: verify-topic
description: The Verifier role (docs/plan/10 §10.3). Write the SymPy tests for a topic page in its maths.verify file, deriving every expected value independently and reading answers with answer(label); never edit the page. Use for /verify-topic <path>, or when asked to verify a page.
argument-hint: <content/…/page.md>
---

# /verify-topic: write a page's SymPy tests (the Verifier)

You are the **Verifier** of `$ARGUMENTS`. You must not be its author: if this session wrote the
page, stop and say that a different session has to verify it (10 §10.1).

## Inputs

- the page; its test file is `maths.verify` in its front matter, holding the Author's
  `@covers` stubs;
- `docs/plan/06-quality-assurance.md` §6.1 (what counts as covered) and
  `templates/verify_test.py` (the pattern);
- the helpers in `verify/mathcheck/` (`equal`, `equal_up_to_constant`, `equal_on_domain`,
  `numeric_spot_check`, `limit_is`, `series_converges_to`, `solves_ode`, `answer`).

## The task

For the page, replace every stub in the test file with real tests. Derive every expected
value **independently**: read the problem statements and the displayed steps, but don't copy
numbers from the answers or the solutions into the test. Read the page's answers with
`answer(label)`. For worked examples, assert each displayed equality. If a test fails, do
**not** edit the page: report the label, the page's claim, your result and the SymPy evidence
in the PR.

How:
- one test (or more) per `eg-`/`exr-` label, declared with `@covers("<label>")`; an `exr-`
  test calls `answer(label)`, an `eg-` test makes at least one `mathcheck` assertion;
- import the symbols from `mathcheck` (`from mathcheck import x, n`), compare with
  `equal(...)`, never `==`; a multi-part answer is a tuple of its parts, in order;
- a `manual` answer (a proof) can't be read: test its key claims anyway. It counts as covered
  only through the reviewer's note, which you never add;
- never weaken a test to make it pass (a looser tolerance, a skipped case, a hand-copied
  answer).

What the Phase 1a verifications needed:
- an ε–δ choice is checked symbolically on each branch of a `min`, and the implication on exact
  rational (ε, x) pairs right up to the edge of the window (floats hide a failure there);
  `verify/calculus/limits/test_limit_of_a_function.py` is the pattern;
- a "Facts from school used on this page" box: test each fact, and each use on the page as an
  instance of one;
- the numbers in figure captions, tables and **Try this** steps are claims too: test them;
- a comment in a test says only what the test checks (a sampled check is not "for every");
- SymPy can be wrong: `sp.limit` on a `Piecewise`, `solveset` with `abs`, `is_increasing` on a
  disconnected domain. Cross-check by a second route, and say which in a comment;
- if a test of yours was wrong, say so in the report.

Run, while you work and at the end:

```bash
npm run verify                                       # the AST, the answers, pytest verify, coverage
uv run pytest verify/<subject>/<chapter>/test_<topic>.py -q   # rerun one file (after npm run verify)
```

Push the test file to the topic's branch (10 §10.2), and put the coverage table that
`check_coverage.py` printed in the PR. Report every disagreement as above, with the failing
assertion's output, and list the `manual` exercises whose key claims you tested, for the
reviewer's verdict.

## Never

- edit the page, its front matter or its status, add anyone to `maths.reviewed_by`, or add a
  `maths.manual_checked` entry (10 §10.5);
- copy expected values from the page's answers or solutions;
- mark a test `skip` or `xfail` to hide a disagreement.
