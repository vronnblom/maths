# Contributing

Thank you for helping. This repository is an open, verified body of university mathematics:
every computation is re-done by SymPy, every proof goes through a checklist, and every page
says how far it has got (`draft` → `reviewed` → `verified`). The rules below exist to keep
that true. The full reasoning is in [`PLAN.md`](PLAN.md) and [`docs/plan/`](docs/plan/).

## 1. Ways to help

- **Report an error.** This is the most valuable contribution: a wrong statement, a gap in a
  proof, an unclear step, a typo, a broken widget.
- **Suggest an exercise**, or a better example, in an issue.
- **Improve an explanation**: a pull request against one page.
- **Write a topic** from the curriculum (§5).
- **Build a widget** from the catalogue in [`widgets/README.md`](widgets/README.md), or propose
  one with the *Widget* issue form.

## 2. Reporting errors

Use the [*Erratum* issue form](https://github.com/vronnblom/maths/issues/new?template=erratum.yml).
The link at the foot of each topic page ("Found an error on this page? Report it") opens it
with the page filled in, and "Report an error" in the site's header opens it blank. Give the
label of the block if you can: it is the part after `#` in the block's link. We triage
within about a week; how errors are fixed, and when they are listed on the
[errata page](https://vronnblom.github.io/maths/about/errata/), is in
[11 §11.4](docs/plan/11-governance.md#114-errata-process).

## 3. Before you write

- Read [01](docs/plan/01-vision-and-scope.md) (the principles),
  [04](docs/plan/04-notation-and-style.md) (notation and style) and
  [03](docs/plan/03-content-model.md) (the page structure), then the exemplar page
  `content/calculus/limits/limit-of-a-function.md` once it exists (until then,
  [`templates/topic.md`](templates/topic.md)).
- Check [`content/calculus/curriculum.yml`](content/calculus/curriculum.yml) and the open
  issues and pull requests, so that two people don't write the same thing.
- For a topic that is not in the curriculum, open a *New topic* issue first: the curriculum
  changes in its own PR, approved by the maintainer.

## 4. Setup

You need [Node.js 22](https://nodejs.org/) (the version is in `.nvmrc`),
[uv](https://docs.astral.sh/uv/) (it installs Python 3.12 or later if you don't have it) and
`git`, plus network access to the npm registry, PyPI and github.com.

```bash
git clone https://github.com/vronnblom/maths.git
cd maths
npm ci && uv sync     # mystmd (pinned) and the Python tooling, from the lockfiles
npm run dev           # the live-reloading site at http://localhost:3000
npm run all           # everything CI runs; run it before every push
```

The first `npm run dev`, `verify` or `build` fetches the pinned site theme with `git` into
`content/_build/templates/`; later runs reuse it. `npm run all` takes a few minutes.
[`README.md`](README.md) lists what each npm script does.

In a Claude Code cloud session, the SessionStart hook (`.claude/hooks/session-start.sh`) does
the installation for you.

## 5. Writing a topic

The procedure is "How to add a topic" in [`CLAUDE.md`](CLAUDE.md); people follow it too.
In short:

1. Pick a topic from `uv run python scripts/graph.py ready calc` and work on a branch
   `topic/<label>`. **One topic per pull request.**
2. Scaffold it: `uv run python scripts/new_topic.py <label>` (in Claude Code, `/new-topic
   <label>`). This writes the page from [`templates/topic.md`](templates/topic.md) and the
   curriculum entry, the verify file and the toc entry. Replace every `TODO`.
3. Follow the fixed page structure, the curriculum's proof policies, and
   [`templates/blocks.md`](templates/blocks.md) for every block.
4. **Labels** (`def-calc-…`, `thm-calc-…`, `exr-calc-…`) are global and permanent: never
   rename or delete one. Run `uv run python scripts/check_labels.py --update-lock` to record
   new ones in `labels.lock`.
5. Keep `status: draft`. Only the maintainer sets `reviewed` or `verified`.

## 6. Verification

Every worked example and every exercise answer is checked by a SymPy test in
`verify/<subject>/<chapter>/test_<topic>.py` ([06 §6.1](docs/plan/06-quality-assurance.md)).

- The author of a page leaves one `pytest.skip("for the verifier")` stub per example and
  exercise (`scripts/new_topic.py --stubs <label>` adds them). **Someone else** writes the
  tests, deriving every expected value independently; that is what makes them a check.
- Tests read each answer from the built page with `answer(label)`, so the answer must be in
  the machine-checkable LaTeX subset ([04 §4.3](docs/plan/04-notation-and-style.md)), with an
  answer type class when it is not an expression (`set`, `bool`, `antiderivative`,
  `numeric-<tol>`).
- A proof has a `manual` answer. No test can read it, so it counts as covered only when a
  reviewer records that they checked it (`maths.manual_checked`).
- If a test and the page disagree, report it in the pull request with the evidence. Never
  weaken a test to make it pass.

`npm run verify` builds the pages, runs the tests and prints each page's coverage.

## 7. Pull requests

- Fill in the pull request template: the type of PR, the mathematics in a few sentences, the
  results with their proof policies, the coverage that `npm run verify` printed, and for
  topic PRs the proof checklist.
- CI must be green: `checks`, `verify`, `build` and the verified-page guard. `npm run all`
  runs the same checks locally.
- The maintainer reviews every PR: the statements, the proofs and a sample of solutions. Expect
  a first response within about a week (best effort). A page becomes `reviewed` in the PR
  that earns it.
- An AI reviewer may post findings first. Answer each one, or fix it.

## 8. Sources and licensing

Content is licensed under CC BY-SA 4.0 ([`LICENSE-CONTENT.md`](LICENSE-CONTENT.md)), code
under MIT ([`LICENSE`](LICENSE)), and contributions are accepted under the same licences.

- Write original material, or adapt material under **CC BY or CC BY-SA** only, and list every
  adapted source in the page's `maths.sources`.
- Nothing under a NonCommercial (NC) licence (OpenStax, APEX and CLP Calculus, for example),
  and nothing from proprietary textbooks, not even paraphrased ([07 §7.4](docs/plan/07-exercises.md)
  lists the sources checked so far). Classic exercises such as "compute
  $\lim \frac{\sin 3x}{x}$" are mathematical facts and can be used freely.
- AI-assisted contributions say so in a `Co-Authored-By:` trailer. The person who opens the PR
  is responsible for it.

## 9. Style

- en-GB spelling; "we" for reasoning and "you" for instructions; no "clearly" or "obviously".
- Notation as in [`content/about/notation.md`](content/about/notation.md), with the KaTeX
  macros (`\R`, `\dd`, `\abs{…}`, …); `npm run check` lints the mechanical part.
- Proofs: `{proof:proof}` with `:enumerated: false`, a first sentence that states the
  strategy, every hypothesis used, and the curriculum's policy (F in the core, R in the
  rigorous track, S a sketch, D deferred with its target named).
- Accessibility: alt text on every figure; every widget has a text description (its caption)
  and works with the keyboard alone; never rely on colour alone.

## 10. Code of conduct

Everyone taking part follows the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

## 11. For AI agents

Read [`CLAUDE.md`](CLAUDE.md). The roles (Author, Verifier, Reviewer) are the skills listed
in [`docs/agents/README.md`](docs/agents/README.md).
