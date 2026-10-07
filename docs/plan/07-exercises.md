# 7. Exercises

## 7.1 Goals
- Every topic page ends with **6–15 exercises** in increasing difficulty, and every chapter
  index has **6–12 mixed review exercises**, where choosing the method is part of the task.
- Every exercise has **hints → final answer → full solution**, each revealed separately, so
  a student can get unstuck without being handed the solution.
- Every computational answer is **machine-verified** ([06](06-quality-assurance.md)).
- Interactivity comes in stages: static first (Phases 1–4), then answer checking and
  randomised practice (Phase 5), then retrofitted to earlier chapters.

## 7.2 Difficulty tiers

| Tier | Class | Name shown | Purpose | Typical share | Example (Limits chapter) |
|---|---|---|---|---|---|
| A | `tier-a` | **Check** | Direct application of one definition or rule; a 2–5 minute confidence check | ~40 % | $\lim_{x\to 2}(3x^2 - x + 1)$ |
| B | `tier-b` | **Practice** | Multi-step, combines 2–3 ideas, needs choosing an approach | ~40 % | $\lim_{x\to 0}\frac{\sqrt{x+4}-2}{x}$ |
| C | `tier-c` | **Challenge** | Proofs, ε–δ, "why does the hypothesis matter", or a novel application | ~20 % | Prove from the definition that $\lim_{x\to 3}(2x-1) = 5$ |

Orthogonal flags (extra classes):
- `rigor`: requires the rigorous track (ε–δ, completeness). Shown with a "Rigorous" tag,
  so engineering students know they can skip it.
- `applied`: a modelling/physics/economics context.
- `widget`: solved with or explored via a widget on the page.

The tier is shown as a coloured tag via CSS on the class (`content/_static/custom.css`).

## 7.3 Structure of one exercise

````markdown
::::{exercise} Rationalising the numerator
:label: exr-calc-computing-limits-conjugate
:class: tier-b

Compute $\displaystyle \lim_{x \to 0} \frac{\sqrt{x+1} - 1}{x}$.

:::{admonition} Hint 1
:class: dropdown hint
Direct substitution gives $\tfrac{0}{0}$. What algebraic trick removes a square root from a difference?
:::

:::{admonition} Hint 2
:class: dropdown hint
Multiply numerator and denominator by the conjugate $\sqrt{x+1} + 1$.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{2}$
:::
::::

::::{solution} exr-calc-computing-limits-conjugate
:label: sol-calc-computing-limits-conjugate
:class: dropdown

For $x \ne 0$ (and $x \ge -1$),
$$
\frac{\sqrt{x+1}-1}{x} \cdot \frac{\sqrt{x+1}+1}{\sqrt{x+1}+1}
= \frac{(x+1) - 1}{x\,(\sqrt{x+1}+1)}
= \frac{1}{\sqrt{x+1}+1}.
$$
The two sides agree for every $x \ne 0$ near $0$, so by [](#lem-calc-limit-agree-except-point)
they have the same limit. By the [limit laws](#thm-calc-limit-laws) (root, sum and quotient
laws), that limit is $\frac{1}{\sqrt{0+1}+1} = \frac{1}{2}$.
::::
````

This exact structure was validated in the PoC (see 05 §5.3). It lives on
`calc-computing-limits`, where the curriculum puts rationalising and the "agree except at a
point" lemma (08), so the solution cites only that page and its prerequisite closure.

Rules:
- **Hints**: 0–3, each a nudge, not a step of the solution. Tier A may have none. Tier C
  should have at least one.
- **Answer**: final result only, in the machine-checkable subset
  ([04 §4.3](04-notation-and-style.md)). Several parts are listed as `(a) … (b) …`, each in
  its own math span. Non-expression answers ("does not exist", a proof) use
  `:class: dropdown answer manual`.
- **Answer types** (an extra class on the answer admonition, so the checker knows how to
  compare): `expr` (default; a bracketed pair `(a, b)` is a point), `antiderivative`
  (compare up to a constant), `set` (solution sets/intervals: only here are brackets read as
  intervals), `bool` (true/false questions), `numeric` (with tolerance, e.g.
  `numeric-1e-4`), `manual`. An answer asked "to $n$ decimal places" uses the tolerance
  $\tfrac12 \cdot 10^{-n}$ (`numeric-5e-3` for two places), and its test compares the
  printed value with the correctly rounded one, so a wrongly rounded answer fails.
- **Solution**: complete, at the level of a worked example. It cites earlier results by link
  and uses only methods from the page's prerequisite closure. Solutions live **inline,
  directly after their exercise, collapsed**. Since output is website only, there is no reason
  to separate them into a solutions file, and inline keeps exercise and solution in one diff.
- Exercise labels are semantic: `exr-<subj>-<topic-slug>-<what-it-is-about>`. Display numbers
  ("Exercise 7") come from MyST and may change when exercises are reordered; labels don't.

## 7.4 Sources and licensing of exercises

- Original exercises are preferred. Classic exercises ("compute $\lim \frac{\sin 3x}{x}$")
  are mathematical facts and can be used freely.
- Exercises adapted from openly licensed books must be **licence-compatible with CC BY-SA
  4.0**, which means the source is CC BY or CC BY-SA. Any *NonCommercial* (NC) licence is
  incompatible. Adapted sources are listed in `maths.sources`, and the licence of each
  source is checked when it is first used. Current assessment (to re-check at the time of use):

  | Source | Licence | Usable? |
  |---|---|---|
  | Active Calculus (Boelkins), 2018+ editions | CC BY-SA 4.0 | ✔ with attribution |
  | Active Calculus, editions up to 2015 | CC BY-NC-SA 3.0 | ✗ |
  | OpenStax Calculus Vol. 1–3 | CC BY-NC-SA 4.0 | ✗ (inspiration only, no copying) |
  | APEX Calculus | CC BY-NC 4.0 | ✗ |
  | CLP Calculus (UBC) | CC BY-NC-SA 4.0 | ✗ |
- No exercises from proprietary textbooks (Stewart, Adams, Persson & Böiers, …), not even
  paraphrased.

## 7.5 Verification of exercises

- Every `exr-*` label must be covered by a test (`@covers`) or have a `manual` answer (with a
  reviewer note in the PR) before the page can be `verified`.
- The test reproduces the answer independently (§6.1). For tier C proofs the "test" may check
  the key computational claims in the solution, e.g. that $\delta = \min(1, \eps/7)$ really
  works for $x^2$ near 3, by verifying the inequality chain symbolically.

## 7.6 Phase 5: interactive exercises (designed now, built later)

### Answer-check widget
- `widgets/answer-check.mjs` adds an input box under exercises that opt in
  (`:class: tier-a check`). The student types an expression in a forgiving plain-math syntax
  (`sqrt(3)/2`, `1/2*ln(2)`, `pi/4`). An optional MathLive input can be evaluated then.
- Checking runs **in the browser**, so no server is needed. The candidate engine is the
  [Cortex Compute Engine](https://cortexjs.io/compute-engine/) (MIT), which parses and tests
  symbolic equivalence. Fallback: numeric spot-checking at random points (robust for most
  calculus answers), possibly with `math.js`.
- The expected answer comes from the same extracted `_answers.json` that the SymPy tests check,
  so the widget never disagrees with the verified answer.
- Feedback is "correct", "not equivalent", or "equivalent but not simplified" (where detectable).
  Solutions remain available regardless.

### Randomised practice banks
- `practice/<topic>.py` generators (Python + SymPy) produce, for example, 200 instances of
  "differentiate $a x^n \sin(bx)$" with **answers computed by SymPy at build time**.
  Generators run in CI and write `content/<subject>/<chapter>/_practice/<topic>.json`. The
  JSON is committed (reproducible with a fixed seed), so reviewers can read the diff.
- `widgets/practice.mjs` draws a random instance, accepts an answer via the answer-check
  engine, and reveals the SymPy-derived worked steps where the generator provides them
  (step templates).
- Each generator has quality filters: no trivial instances, bounded coefficient sizes, "nice"
  answers where wanted, and no duplicates.
- Every generator ships with a test that a sample of its instances satisfies the claimed
  property, e.g. the derivative of the instance equals the stored answer.

### In-browser Python (Phase 5)
- "Compute it" sections on selected pages let students run SymPy themselves (Pyodide).
  First evaluate MyST's built-in JupyterLite execution (`project.jupyter.lite: true`, beta).
  If it's not stable enough, write a small `widgets/python-cell.mjs` that lazy-loads Pyodide
  from its CDN only when the reader clicks *Run*, so no page pays the ~10 MB cost up front.
- Python cells are enrichment only; no core explanation depends on running code.

## 7.7 What we will not do
- Graded quizzes, accounts or progress tracking (that needs a server and personal data).
  A per-browser "done" checkbox using `localStorage` is acceptable later.
- Hidden solutions "for instructors only". Everything is open.
