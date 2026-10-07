---
# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATE: topic page.  Copy to content/<subject>/<chapter>/<topic>.md
# This sample is the skeleton of the gold-standard page `calc-limit`.
# Lines starting with `%` are MyST comments (not rendered) — delete them when done.
# Rules: docs/plan/03-content-model.md · Notation: content/about/notation.md
# ─────────────────────────────────────────────────────────────────────────────
title: The Limit of a Function
short_title: Limit of a function
label: calc-limit
description: >-
  What it means for f(x) to approach L as x approaches a: intuitively, graphically,
  and precisely with ε and δ.
tags: [limits, epsilon-delta]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 2
  est_minutes: 40
  prerequisites:
    - calc-functions
    - calc-absolute-value-inequalities
  objectives:
    - Estimate a limit from a table of values and from a graph, and explain why such estimates can mislead.
    - State the precise (ε–δ) definition of a limit and interpret it as a game between ε and δ.
    - Prove limits of linear functions directly from the definition.
    - Recognise when a limit does not exist (jump, oscillation, unboundedness).
  verify: verify/calculus/limits/test_limit_of_a_function.py
  widgets: [function-plot, epsilon-delta]
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

% 1–3 paragraphs. Start from a concrete question, not a definition.
% Example: a ball's position is s(t) = 5t²; what is its speed at exactly t = 1?
% Average speeds over [1, 1+h] approach a number as h shrinks — that "approach" is a limit.

% A widget sits alone in a {figure}: the figure carries the wdg- label, and its caption is
% the text description (shown even when the widget can't load). See docs/plan/05 §5.8.
::::{figure}
:label: wdg-calc-limit-average-speed

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "(5*(1+h)^2 - 5)/h",
  "variable": "h",
  "xRange": [-1, 1],
  "yRange": [5, 15],
  "table": { "points": [0.1, 0.01, 0.001, -0.001, -0.01, -0.1] },
  "hole": { "x": 0 },
  "trace": { "x": 0.5 }
}
```

Graph of the average speed $\frac{5(1+h)^2 - 5}{h}$ for $-1 \le h \le 1$, with a hole at
$h = 0$, and a point on the graph that a slider for $h$ moves. A table lists the values for
$h = \pm 0.1, \pm 0.01, \pm 0.001$; they approach $10$.
::::

**Try this:** move $h$ towards $0$ from both sides. Which number do the average speeds
approach? Why can't you simply put $h = 0$?

## What a limit is

% Intuitive description first (no new symbols), then a precise definition.

Informally, $\lim_{x \to a} f(x) = L$ means that $f(x)$ can be made as close to $L$ as we
like by taking $x$ close enough to $a$, but not equal to $a$.

:::{proof:definition} Limit of a function
:label: def-calc-limit

Let $f$ be defined on an open interval containing $a$, except possibly at $a$ itself. We say
that **the limit of $f(x)$ as $x$ approaches $a$ is $L$**, and write
$$
\lim_{x \to a} f(x) = L,
$$
if for every $\eps > 0$ there exists $\delta > 0$ such that
$$
0 < \abs{x - a} < \delta \quad\text{implies}\quad \abs{f(x) - L} < \eps .
$$
:::

**In words.** Whatever tolerance $\eps$ someone demands around $L$, you can answer with a
window of half-width $\delta$ around $a$ such that every $x$ in that window (other than $a$)
has $f(x)$ within the tolerance.

% The ε–δ game (widgets/README.md, `epsilon-delta`): the reader sets ε and sees the largest δ on
% each side; then picks their own δ and sees where it fails. The caption is the text description.
::::{figure}
:label: wdg-calc-limit-eps-delta

```{anywidget} ../../../widgets/epsilon-delta.mjs
{
  "f": "x^2", "a": 2, "L": 4,
  "eps": 2, "epsRange": [0.05, 1.5], "epsStep": 0.05,
  "xRange": [-0.5, 3.5], "yRange": [-1, 9]
}
```

Graph of $y = x^2$ near $x = 2$, with a horizontal band of half-width $\eps$ around $y = 4$
(dashed edges) and a vertical window $0 < \abs{x - 2} < \delta$ (solid edges; the dotted line
$x = 2$ itself is left out). A slider sets $\eps$ from $0.05$ to $1.5$, and the widget states the
largest $\delta$ on each side of $2$: for $\eps = 0.5$ it is $2 - \sqrt{3.5} \approx 0.129$ on the
left and $\sqrt{4.5} - 2 \approx 0.121$ on the right. A second slider sets your own $\delta$;
points of the graph inside the window but outside the band are marked with crosses, and a
sentence says whether your $\delta$ works.
::::

**Try this:** set $\eps = 0.1$. What is the largest $\delta$ that works? Is it the same on both
sides of $a = 2$, and which one must you take? Then make $\delta$ a little larger and find
where it fails.

:::{proof:remark} The value at $a$ does not matter
:label: rem-calc-limit-value-irrelevant
% Example and non-example: f(x) = (x²−1)/(x−1) is undefined at 1 but has limit 2.
:::

## Main results

:::{proof:theorem} Uniqueness of limits
:label: thm-calc-limit-unique
If $\lim_{x\to a} f(x) = L$ and $\lim_{x\to a} f(x) = M$, then $L = M$.
:::

:::{proof:proof} Rigorous track
:label: prf-calc-limit-unique
:enumerated: false
:class: dropdown
% Policy R (docs/plan/08). Strategy sentence first: "Suppose L ≠ M and take ε = |L − M|/2 …"
:::

## Worked examples

:::{proof:example} Prove $\lim_{x \to 3} (2x - 1) = 5$ from the definition
:label: eg-calc-limit-linear-eps-delta

**Goal.** Given $\eps > 0$, find $\delta > 0$ with $0 < \abs{x-3} < \delta \implies \abs{(2x-1) - 5} < \eps$.

1. **Scratch work.** $\abs{(2x - 1) - 5} = \abs{2x - 6} = 2\abs{x - 3}$.
2. **Choose $\delta$.** We need $2\abs{x-3} < \eps$, so take $\delta = \eps/2$.
3. **Proof.** If $0 < \abs{x - 3} < \delta = \eps/2$, then
   $\abs{(2x-1) - 5} = 2\abs{x-3} < 2 \cdot \tfrac{\eps}{2} = \eps$.

$$
\boxed{\delta = \tfrac{\eps}{2}}
$$

**Check.** For $\eps = 0.1$: $\delta = 0.05$, and $x = 3.04$ gives $\abs{2(3.04) - 1 - 5} = 0.08 < 0.1$. ✓
:::

% Add 2–6 more examples: the typical, the edge case, an applied one; non-existence examples.

## Common mistakes

:::{warning} "The limit is just $f(a)$"
% ✗ wrong — why — ✓ right. Use the (x²−1)/(x−1) example: f(1) is undefined, the limit is 2.
:::

:::{warning} Letting $\delta$ depend on $x$
% ✗ "take δ = |x − 3|" — δ must depend only on ε (and a), chosen before x.
:::

## Rigorous track

:::{admonition} Why "$0 < \abs{x - a}$"?
:class: dropdown rigor
% Explain that excluding x = a is what makes limits useful for derivatives (0/0).
:::

## Summary

- $\lim_{x\to a} f(x) = L$ is about values of $f$ **near** $a$, never **at** $a$.
- Precisely: for every $\eps > 0$ there is $\delta > 0$ such that $0<\abs{x-a}<\delta \implies \abs{f(x)-L}<\eps$.
- Tables and graphs suggest limits but cannot prove them.
- A limit, if it exists, is unique ([](#thm-calc-limit-unique)).

## Exercises

% Tiers: A (check) ~40 %, B (practice) ~40 %, C (challenge) ~20 %. See docs/plan/07-exercises.md.
% Every exercise: label, tier class, optional hints, an Answer (machine-checkable LaTeX), and a solution.

::::{exercise} Reading a limit from a table
:label: exr-calc-limit-table-estimate
:class: tier-a

Use a table of values with $x = 0.1, 0.01, 0.001$ (and the negatives) to estimate
$\displaystyle \lim_{x \to 0} \frac{2^x - 1}{x}$ to two decimal places.

:::{admonition} Hint 1
:class: dropdown hint
Evaluate on both sides of $0$. Do the values settle as $x$ shrinks?
:::

:::{admonition} Answer
:class: dropdown answer numeric-5e-3
$0.69$
:::
::::

::::{solution} exr-calc-limit-table-estimate
:label: sol-calc-limit-table-estimate
:class: dropdown
% Full table, then the estimate 0.69. Do not cite the exact value here: it is ln 2, but the
% pages that show it are outside this page's prerequisite closure. Mention it, if at all,
% in a looking-ahead admonition (templates/blocks.md), e.g. "The exact value is ln 2; see
% [Derivatives of Exponential and Logarithmic Functions](#calc-derivatives-exp-log)."
::::

::::{exercise} An ε–δ proof
:label: exr-calc-limit-eps-delta-linear
:class: tier-c rigor

Prove from [the definition](#def-calc-limit) that $\lim_{x \to -1} (4 - 3x) = 7$.

:::{admonition} Hint 1
:class: dropdown hint
Start from $\abs{(4 - 3x) - 7}$ and factor out a constant.
:::

:::{admonition} Answer
:class: dropdown answer manual
$\delta = \eps / 3$ works.
:::
::::

::::{solution} exr-calc-limit-eps-delta-linear
:label: sol-calc-limit-eps-delta-linear
:class: dropdown
% Mirror the structure of the worked example: scratch work, choice of δ, proof.
::::

## Where this leads

:::{where-this-leads}
:::

% Optional, hand-written:
% - See also: …
% - Further reading: Active Calculus 2.0 §1.7 (CC BY-SA 4.0)
