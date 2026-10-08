---
title: The Limit of a Function
short_title: Limit of a function
label: calc-limit
description: >-
  What it means for f(x) to approach L as x approaches a: from tables and graphs, which can
  mislead, to the precise definition with epsilon and delta, and the ways a limit can fail to
  exist.
tags: [limits, epsilon-delta, proofs]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 3
  est_minutes: 45
  prerequisites: [calc-functions, calc-absolute-value-inequalities]
  objectives:
    - Estimate limits from tables and graphs and explain how this can mislead.
    - State the precise (ε–δ) definition and interpret it as an ε–δ game.
    - Prove limits of linear and quadratic functions from the definition.
    - Recognise when a limit does not exist.
  verify: verify/calculus/limits/test_limit_of_a_function.py
  widgets: [epsilon-delta, function-plot]
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

You drop a stone from a bridge. How fast is it falling exactly one second later? A
speedometer would need to measure a speed at a single instant, but speed is distance divided
by time, and in a single instant the stone covers no distance in no time.

What we *can* compute are average speeds. Near the Earth's surface the stone has fallen about
$s(t) = 5t^2$ metres after $t$ seconds. Over the time interval from $1$ to $1 + h$ seconds it
falls $s(1 + h) - s(1)$ metres, so its average speed is
$$
\frac{s(1 + h) - s(1)}{h} = \frac{5(1+h)^2 - 5}{h} \quad\text{metres per second.}
$$
(For $h < 0$ this is the average over the interval from $1 + h$ to $1$.) We cannot put $h = 0$:
that gives $\frac{0}{0}$. But we can make $h$ small.

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
$h = 0$, where the formula is undefined, and a point on the graph that a slider for $h$ moves.
A table lists the values for $h = \pm 0.1, \pm 0.01, \pm 0.001$: $10.5$, $10.05$, $10.005$ and
$9.995$, $9.95$, $9.5$. They approach $10$ from both sides.
::::

**Try this:** move $h$ towards $0$ from both sides. Which number do the average speeds
approach? What happens when you try to put $h = 0$ in the formula?

The average speeds approach $10$, so the stone's speed at $t = 1$ should be $10$ metres per
second. This page makes "approach" precise. That matters, because tables and pictures can
mislead. The sine function appears in the next figure and the paragraph after it, the worked
example on $\sin(1/x)$, the common mistake "Checking one $\eps$, or a few points", and the
exercise on $\sin(\pi/x)$ (its statement, hints and solution). They use only the facts about it
in the box below.

:::{admonition} Facts from school used on this page
:label: rem-calc-limit-school-facts

With $t$ in radians:

- $\sin(k\pi) = 0$ for every integer $k$;
- $\sin\bigl(\frac{\pi}{2} + 2k\pi\bigr) = 1$ for every integer $k$;
- $-1 \le \sin t \le 1$ for every real number $t$.

These are the only facts about $\sin$ that this page uses. The page Trigonometric Functions, in
the Preliminaries chapter, defines $\sin$ and proves them.
:::

::::{figure}
:label: wdg-calc-limit-misleading-table

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "sin(pi/x)",
  "xRange": [-1, 1],
  "yRange": [-1.5, 1.5],
  "table": { "points": [0.1, 0.01, 0.001, 0.08, 0.016, 0.0032] },
  "zoom": false
}
```

Graph of $y = \sin(\pi / x)$ for $-1 \le x \le 1$, $x \ne 0$. It stays between $-1$ and $1$.
Near $x = 0$ it rises to height $1$ and falls back through $0$ again and again, faster and
faster, too fast to draw: the plotted curve joins finitely many computed points, so close to $0$ it is a jumble of lines that misses most of the swings, with
even a short flat piece at height $0$, an artefact of the drawing. A table lists the values at
$x = 0.1, 0.01, 0.001$, where the exact values are $\sin(10\pi) = \sin(100\pi) = \sin(1000\pi) = 0$ (the
computer shows tiny numbers such as $-1.2 \times 10^{-15}$ instead, because it rounds
$\pi$), and at $x = 0.08, 0.016, 0.0032$, where the values are
$\sin(12.5\pi) = \sin(62.5\pi) = \sin(312.5\pi) = 1$.
::::

**Try this:** cover the last three rows of the table. What limit at $0$ do the first three
suggest? Now look at the last three. Does the graph near $0$ settle near one height?

Both halves of the table are correct, and they suggest different answers. A table checks
finitely many points, and a graph is drawn through finitely many points, so neither can tell
us what happens at *every* point near $0$. We need a definition that speaks about all of
them. With it, we will show that the average speeds really do approach $10$
([](#eg-calc-limit-average-speed)) and that $\sin(\pi/x)$ approaches no number at all
([](#exr-calc-limit-sin-pi-over-x)).

:::{admonition} Looking ahead
:class: looking-ahead
The number that the average speeds approach is the stone's *instantaneous* speed. The
Derivatives chapter turns this idea into the derivative, starting from the page Tangent Lines
and Rates of Change. Like the average speed at $h = 0$, every difference quotient that defines
a derivative is undefined at the point where its limit is taken, which is why a limit must
ignore that point.
:::

## What a limit is

Informally, $\lim_{x \to a} f(x) = L$ means that $f(x)$ is as close to $L$ as we like for all
$x$ close enough to $a$, but not equal to $a$. "As close as we like" is a tolerance, which we
call $\eps$, and "close enough" is a distance, which we call $\delta$.

We measure closeness with distances: $\abs{f(x) - L}$ is
[the distance](#def-calc-absolute-value) from $f(x)$ to $L$, and $\abs{x - a}$ the distance
from $x$ to $a$. The set of $x$ with $0 < \abs{x - a} < \delta$ is the
[open interval](#def-calc-interval) $(a - \delta, a + \delta)$ with its centre $a$ removed, the
*punctured neighbourhood* of $a$ of radius $\delta$, by
[part (e) of the proposition on distance inequalities](#prop-calc-abs-interval).

:::{proof:definition} Limit of a function
:label: def-calc-limit

Let $a$ be a real number, and let $f$ be a function that is defined at every point of an open
interval containing $a$, except possibly at $a$ itself. We say that **the limit of $f(x)$ as
$x$ approaches $a$ is $L$**, where $L$ is a real number, and write
$$
\lim_{x \to a} f(x) = L,
$$
if for every $\eps > 0$ there is a $\delta > 0$ such that $f$ is defined at every $x$ with
$0 < \abs{x - a} < \delta$, and
$$
0 < \abs{x - a} < \delta \quad\text{implies}\quad \abs{f(x) - L} < \eps .
$$
We also write $f(x) \to L$ as $x \to a$.
:::

**In words.** Whatever tolerance $\eps$ someone demands around $L$, you can answer with a
window of half-width $\delta$ around $a$ such that every $x$ in that window, other than $a$
itself, has $f(x)$ within the tolerance. Think of it as a game. A challenger names an
$\eps > 0$; you reply with a $\delta > 0$; you win the round if every $x$ in your window passes.
The limit is $L$ when you can win *every* round. Three points to notice:

- $\delta$ is chosen after $\eps$, so it may depend on $\eps$ (and on $a$), but it is one
  number for the whole window: it may not depend on $x$.
- The window leaves out $x = a$. The value $f(a)$, and whether it exists, plays no part.
- If a $\delta$ wins a round, so does every smaller $\delta > 0$: a smaller window has fewer
  points to check. Since $f$ is defined on an open interval around $a$ (except at $a$), a
  small enough window lies inside that interval, so the requirement that $f$ be defined in the
  window only rules out windows that are too wide.

**Example.** $\lim_{x \to a} x = a$ for every real $a$. Given $\eps > 0$, take
$\delta = \eps$. If $0 < \abs{x - a} < \delta$, then $\abs{f(x) - a} = \abs{x - a} < \eps$.

**Non-example.** $\lim_{x \to 1} x$ is not $1.5$. Take $\eps = 0.25$. Whatever $\delta > 0$
is offered, the window contains the point $x = 1 + d$ with $d = \frac12 \min(\delta, 0.25)$,
and for it $\abs{f(x) - 1.5} = \abs{d - 0.5} = 0.5 - d \ge 0.375$, which is not less than
$0.25$. So no $\delta$ wins the round $\eps = 0.25$, and $1.5$ is not the limit. One round
that cannot be won is enough.

The game is easiest to understand by playing it. In the figure, the claim is
$\lim_{x \to 2} x^2 = 4$.

::::{figure}
:label: wdg-calc-limit-eps-delta

```{anywidget} ../../../widgets/epsilon-delta.mjs
{
  "f": "x^2", "a": 2, "L": 4,
  "eps": 0.5, "epsRange": [0.05, 1.5], "epsStep": 0.05,
  "xRange": [1, 3], "yRange": [0, 9]
}
```

Graph of $y = x^2$ for $1 \le x \le 3$, with a horizontal band of half-width $\eps$ around
$y = 4$ (translucent, dashed edges) and a vertical window $0 < \abs{x - 2} < \delta$
(translucent, solid edges; the dotted line $x = 2$ itself is left out). A slider sets $\eps$
from $0.05$ to $1.5$ in steps of $0.05$, starting at $0.5$. For each $\eps$ the widget states
the largest $\delta$ it found on each side of $2$, and how many points it checked, and then
the smaller of the two as the largest $\delta$ it found for both sides. For $\eps = 0.5$ it
reports $0.129171$ on the left and $0.12132$ on the right; the exact values are
$2 - \sqrt{3.5} \approx 0.129171$ and $\sqrt{4.5} - 2 \approx 0.121320$. A second slider sets
your own $\delta$, from $0.001$ to $1$ in steps of $0.001$, and a button sets it to the largest
value on that slider that is at most the $\delta$ the widget found. Points of the graph inside
the window but outside the band are marked with crosses, and a sentence says whether your
$\delta$ passed the widget's check at the points it tested, or names a point where it fails.
::::

**Try this: play the ε–δ game.**

1. Select the $\eps$ slider and press ← eight times, to $\eps = 0.1$. Read the largest
   $\delta$ the widget found on the left of $2$ and on the right. (It reports $0.0251582$ on
   the left and $0.0248456$ on the right.)
2. You must answer with *one* $\delta$. Which of the two numbers can you use, and why not the
   other?
3. Press **Set δ to the largest on the slider** ($\delta = 0.024$), then select the $\delta$
   slider and press → once ($\delta = 0.025$). Where does the widget see your $\delta$ fail?
4. Try $\eps = 0.05$ and $\eps = 1$. What happens to the $\delta$ the widget finds as $\eps$
   shrinks?

**Why the smaller one.** The window $0 < \abs{x - 2} < \delta$ reaches the same distance
$\delta$ on both sides of $2$, so one $\delta$ has to work on the left and on the right at
once. For $\eps = 0.1$, a $\delta$ larger than $\sqrt{4.1} - 2 \approx 0.024846$ (the widget
found $0.0248456$) lets in points just to the right of $\sqrt{4.1}$, where $x^2$ is already
outside the band (at $x = 2.025$, $x^2 = 4.100625$); the left side would tolerate up to
$2 - \sqrt{3.9} \approx 0.025158$, but that does not help. So the $\delta$ for both sides is
the smaller of the two, here the right side's, because $x^2$ grows faster to the right of $2$
than it falls to the left. As $\eps$ shrinks, the band narrows and so does the
window.

The widget's numbers are observations: it checks finitely many points, so it cannot prove that
its $\delta$ works for every $x$ in the window, or that a $\delta$ exists for every $\eps$.
Exercise [](#exr-calc-limit-widget-largest-delta) finds the exact largest $\delta$ for
$\eps = 0.1$, and the rigorous track proves, in [](#eg-calc-limit-quadratic-eps-delta), that
$\delta = \min(1, \eps/5)$ works for every $\eps > 0$. That $\delta$ is smaller than the
largest one (for $\eps = 0.1$ it is $0.02$): a proof only needs *some* $\delta$ that works.

:::{proof:remark} The value at $a$ does not matter
:label: rem-calc-limit-value-irrelevant

The definition only looks at $x$ with $0 < \abs{x - a}$, that is, at $x \ne a$. So
$\lim_{x \to a} f(x)$ depends only on the values of $f$ near $a$: changing $f(a)$, or leaving
$f(a)$ undefined, does not change the limit or whether it exists.

**Example.** $g(x) = \dfrac{x^2 - 1}{x - 1}$ is not defined at $x = 1$, but
$\lim_{x \to 1} g(x) = 2$. For $x \ne 1$ we may cancel $x - 1 \ne 0$:
$g(x) = \dfrac{(x - 1)(x + 1)}{x - 1} = x + 1$, so $\abs{g(x) - 2} = \abs{x - 1}$, and
$\delta = \eps$ works.

**Non-example.** The limit need not be the value at $a$. Let $h(x) = x + 1$ for $x \ne 1$ and
$h(1) = 5$. For $x \ne 1$, $h(x) = g(x)$, and only those $x$ enter the definition, so again
$\delta = \eps$ works and $\lim_{x \to 1} h(x) = 2$, although $h(1) = 5$. Putting $x = 1$ into
$h$ gives the wrong number.
:::

## Main results

Could a function have two different limits at the same point? The game suggests not: if
$f(x)$ is within any tolerance of $L$ for all $x$ close enough to $a$, it cannot also be
within every tolerance of a different number $M$, because $L$ and $M$ are a fixed distance
apart.

:::{proof:theorem} Uniqueness of limits
:label: thm-calc-limit-unique

Let $f$ and $a$ be as in [](#def-calc-limit). If $\lim_{x \to a} f(x) = L$ and
$\lim_{x \to a} f(x) = M$, then $L = M$.
:::

:::{proof:proof} Rigorous track
:label: prf-calc-limit-unique
:enumerated: false
:class: dropdown
We argue by contradiction: if $L \ne M$, we take a tolerance of half their distance and find one
$x$ whose value $f(x)$ would have to be within that tolerance of both, which the triangle
inequality forbids.

Suppose $L \ne M$, and let $\eps = \frac{1}{2}\abs{L - M}$, which is positive. Since
$\lim_{x \to a} f(x) = L$, there is a $\delta_1 > 0$ such that $f$ is defined and
$\abs{f(x) - L} < \eps$ for every $x$ with $0 < \abs{x - a} < \delta_1$. Since
$\lim_{x \to a} f(x) = M$, there is a $\delta_2 > 0$ such that $f$ is defined and
$\abs{f(x) - M} < \eps$ for every $x$ with $0 < \abs{x - a} < \delta_2$.

Let $\delta = \min(\delta_1, \delta_2)$ and $x = a + \frac{\delta}{2}$. Then
$0 < \abs{x - a} = \frac{\delta}{2} < \delta$, so $x$ lies in both windows: $f(x)$ is defined,
and $\abs{f(x) - L} < \eps$ and $\abs{f(x) - M} < \eps$. The first of these says also that
$\abs{L - f(x)} < \eps$, because $\abs{L - f(x)} = \abs{f(x) - L}$ by
[property 2 of the absolute value](#rem-calc-absolute-value-properties). By
[part (b) of the triangle inequality](#thm-calc-triangle-inequality),
$\abs{u - v} \le \abs{u - w} + \abs{w - v}$, with $u = L$, $v = M$ and $w = f(x)$,
$$
\abs{L - M} \le \abs{L - f(x)} + \abs{f(x) - M} < \eps + \eps = \abs{L - M},
$$
that is, $\abs{L - M} < \abs{L - M}$, which is impossible. So $L = M$.
:::

Because of [](#thm-calc-limit-unique), we may speak of *the* limit of $f(x)$ as $x \to a$,
when there is one. If there is none, we say that **the limit does not exist**. The proof used
the requirement in [](#def-calc-limit) that $f$ be defined at every point of the window; the
rigorous track shows that if the definition dropped its requirements on the domain of $f$,
uniqueness would fail.

## Worked examples

### Proving a limit from the definition

Each proof has the same shape. We start from $\abs{f(x) - L}$ and rewrite it in terms of
$\abs{x - a}$ (the scratch work); this tells us which $\delta$ to choose; then we check that
this $\delta$ works.

:::{proof:example} Prove $\lim_{x \to 3} (2x - 1) = 5$ from the definition
:label: eg-calc-limit-linear-eps-delta

**Goal.** Given $\eps > 0$, find $\delta > 0$ such that $0 < \abs{x - 3} < \delta$ implies
$\abs{(2x - 1) - 5} < \eps$. The function $2x - 1$ is defined for every $x$, so every window
lies in its domain.

1. **Scratch work.** $\abs{(2x - 1) - 5} = \abs{2x - 6} = 2\abs{x - 3}$.
2. **Choose $\delta$.** We need $2\abs{x - 3} < \eps$, that is, $\abs{x - 3} < \frac{\eps}{2}$.
   So take $\delta = \frac{\eps}{2}$. It depends on $\eps$ only, not on $x$.
3. **Proof.** Let $\eps > 0$ and $\delta = \frac{\eps}{2}$. If $0 < \abs{x - 3} < \delta$, then
   $$
   \abs{(2x - 1) - 5} = 2\abs{x - 3} < 2 \cdot \frac{\eps}{2} = \eps .
   $$
   So for every $\eps > 0$ this $\delta$ works, and $\lim_{x \to 3} (2x - 1) = 5$.

$$
\boxed{\delta = \frac{\eps}{2}}
$$

**Check.** For $\eps = 0.1$: $\delta = 0.05$, and $x = 3.04$ gives
$\abs{2(3.04) - 1 - 5} = 0.08 < 0.1$. ✓ The point $x = 3.05$, just outside the window, gives
exactly $0.1$: with this function $\delta = \frac{\eps}{2}$ is the largest $\delta$ that works.
:::

:::{proof:example} The stone's speed at $t = 1$
:label: eg-calc-limit-average-speed

Show that the average speeds $v(h) = \dfrac{5(1+h)^2 - 5}{h}$ of [Why this matters](#wdg-calc-limit-average-speed)
satisfy $\lim_{h \to 0} v(h) = 10$, and find how small $\abs{h}$ must be for $v(h)$ to be
within $0.01$ m/s of $10$ m/s.

1. **Simplify.** $v$ is defined for every $h \ne 0$, which is all the definition looks at. For
   $h \ne 0$,
   $$
   v(h) = \frac{5(1 + 2h + h^2) - 5}{h} = \frac{10h + 5h^2}{h} = 10 + 5h .
   $$
2. **Scratch work.** $\abs{v(h) - 10} = \abs{5h} = 5\abs{h}$.
3. **Choose $\delta$ and prove.** Let $\eps > 0$ and $\delta = \frac{\eps}{5}$. If
   $0 < \abs{h} < \delta$, then $\abs{v(h) - 10} = 5\abs{h} < 5 \cdot \frac{\eps}{5} = \eps$.
   So $\lim_{h \to 0} v(h) = 10$.
4. **The tolerance $0.01$ m/s.** By step 2, $\abs{v(h) - 10} < 0.01$ exactly when
   $5\abs{h} < 0.01$, that is, when $\abs{h} < 0.002$. So every time interval shorter than
   $0.002$ s (on either side of $t = 1$) gives an average speed within $0.01$ m/s of $10$ m/s,
   and no longer one does: at $\abs{h} = 0.002$ the difference is exactly $0.01$.

$$
\boxed{\lim_{h \to 0} v(h) = 10 \text{ m/s}, \quad \abs{h} < 0.002 \text{ s}}
$$

**Check.** $h = 0.001$: $v(0.001) = \frac{5 \cdot 1.002001 - 5}{0.001} = 10.005$, within
$0.01$ of $10$. ✓ The table in the figure shows $v(0.01) = 10.05 = 10 + 5(0.01)$. ✓ Units:
metres divided by seconds. ✓
:::

### When a limit does not exist

To show that a number $L$ is *not* the limit, one round of the game that cannot be won is
enough: one $\eps > 0$ such that every window $0 < \abs{x - a} < \delta$, however small,
contains a point $x$ with $\abs{f(x) - L} \ge \eps$ (or where $f$ is undefined). To show that
the limit does not exist, we must do this for *every* real number $L$. The next three examples
show the three typical ways this happens: a jump, oscillation, and unbounded values. Each proof
uses the same tool: two points of one window whose values are too far apart to be close to the
same number $L$.

:::{proof:example} A jump: $\lim_{x \to 0} \frac{\abs{x}}{x}$ does not exist
:label: eg-calc-limit-jump

Let $f(x) = \dfrac{\abs{x}}{x}$ for $x \ne 0$. Then $f(x) = 1$ for $x > 0$ and $f(x) = -1$ for
$x < 0$: the graph jumps from height $-1$ to height $1$ at $0$.

1. **Strategy.** Every window around $0$ contains points on both sides of $0$, where the values
   are $-1$ and $1$, a distance $2$ apart. No number is within $1$ of both.
2. **Proof.** Let $L$ be any real number, and suppose that $\delta > 0$ works for $\eps = 1$.
   The points $x = \frac{\delta}{2}$ and $x = -\frac{\delta}{2}$ are in the window, so
   $\abs{1 - L} < 1$ and $\abs{-1 - L} < 1$, and $\abs{L - (-1)} = \abs{-1 - L}$ by
   [property 2 of the absolute value](#rem-calc-absolute-value-properties). By
   [part (b) of the triangle inequality](#thm-calc-triangle-inequality),
   $$
   2 = \abs{1 - (-1)} \le \abs{1 - L} + \abs{L - (-1)} < 1 + 1 = 2,
   $$
   which is impossible. So no $\delta$ works for $\eps = 1$, and $L$ is not the limit.
3. Since $L$ was arbitrary, no real number is the limit.

$$
\boxed{\lim_{x \to 0} \frac{\abs{x}}{x} \text{ does not exist}}
$$

**Check.** $f(0.001) = 1$ and $f(-0.001) = -1$: arbitrarily close to $0$ the values are
still $2$ apart. ✓ The proof never used $f(0)$, which is undefined. ✓
:::

:::{proof:example} Oscillation: $\lim_{x \to 0} \sin(1/x)$ does not exist
:label: eg-calc-limit-sin-1-over-x

Let $f(x) = \sin(1/x)$ for $x \ne 0$. As $x$ decreases to $0$, $1/x$ increases without bound,
so it passes again and again through multiples of $\pi$, where $\sin$ is $0$, and through
numbers $\frac{\pi}{2} + 2k\pi$, where $\sin$ is $1$, by
[the facts from school](#rem-calc-limit-school-facts).

1. **Strategy.** In every window around $0$ we find a point where $\sin(1/x) = 0$ and a point
   where $\sin(1/x) = 1$. No number is within $\frac12$ of both.
2. **The points.** For an integer $n \ge 1$, let
   $$
   p_n = \frac{1}{2\pi n} \qquad\text{and}\qquad q_n = \frac{1}{2\pi n + \frac{\pi}{2}} .
   $$
   Then $f(p_n) = \sin(2\pi n) = 0$ and $f(q_n) = \sin\bigl(2\pi n + \frac{\pi}{2}\bigr) = 1$,
   and $0 < q_n < p_n$.
3. **Proof.** Let $L$ be any real number, and suppose that $\delta > 0$ works for
   $\eps = \frac12$. By [the Archimedean property](#rem-calc-naturals-unbounded), there is
   an integer $n \ge 1$ with $n > \frac{1}{2\pi\delta}$. Then $2\pi n > \frac{1}{\delta}$, so
   $0 < q_n < p_n = \frac{1}{2\pi n} < \delta$: both points are in the window. Hence
   $\abs{0 - L} < \frac12$ and $\abs{1 - L} < \frac12$, and $\abs{L - 0} = \abs{0 - L}$ by
   [property 2 of the absolute value](#rem-calc-absolute-value-properties). By
   [part (b) of the triangle inequality](#thm-calc-triangle-inequality),
   $$
   1 = \abs{1 - 0} \le \abs{1 - L} + \abs{L - 0} < \tfrac12 + \tfrac12 = 1,
   $$
   which is impossible. So $L$ is not the limit, for any real $L$.

$$
\boxed{\lim_{x \to 0} \sin(1/x) \text{ does not exist}}
$$

**Check.** For $n = 50$: $p_{50} = \frac{1}{100\pi} \approx 0.003183$ gives
$\sin(100\pi) = 0$, and $q_{50} = \frac{1}{100\pi + \pi/2} \approx 0.003167$ gives
$\sin\bigl(100\pi + \frac{\pi}{2}\bigr) = 1$. Two points less than $0.0001$ apart, values
$1$ apart. ✓
:::

:::{proof:example} Unbounded values: $\lim_{x \to 0} \frac{1}{x^2}$ does not exist
:label: eg-calc-limit-unbounded

Let $f(x) = \dfrac{1}{x^2}$ for $x \ne 0$. Close to $0$ the values are huge:
$f(0.01) = 10\,000$ and $f(0.001) = 1\,000\,000$.

1. **Strategy.** Whatever $L$ is proposed, every window around $0$ contains a point where
   $f(x)$ is more than $1$ above $L$.
2. **Proof.** Let $L$ be any real number, and suppose that $\delta > 0$ works for $\eps = 1$.
   Let $x = \min\bigl(\frac{\delta}{2}, \frac{1}{\abs{L} + 2}\bigr)$. Then $0 < x < \delta$,
   so $x$ is in the window. Also $x \le \frac{1}{\abs{L} + 2} \le \frac12 < 1$; multiplying
   $x < 1$ by $x > 0$ gives $x^2 < x$, and so
   $$
   f(x) = \frac{1}{x^2} > \frac{1}{x} \ge \abs{L} + 2 .
   $$
   Then $f(x) - L \ge f(x) - \abs{L} > 2$, so $\abs{f(x) - L} > 2 > 1 = \eps$, a contradiction.
   So $L$ is not the limit, for any real $L$.

$$
\boxed{\lim_{x \to 0} \frac{1}{x^2} \text{ does not exist}}
$$

**Check.** For $L = 100$ the proof takes $x \le \frac{1}{102}$, where
$f(x) \ge 102^2 = 10\,404$, far more than $1$ away from $100$. ✓
:::

:::{admonition} Looking ahead
:class: looking-ahead
The three ways to fail are treated separately later in the Limits chapter. A jump is
described by the two one-sided limits, on the page One-Sided Limits. Values that grow without
bound are written $\lim_{x \to 0} \frac{1}{x^2} = \infty$ on the page Infinite Limits and
Vertical Asymptotes; even then the limit does not exist as a real number.
:::

## Common mistakes

:::{warning} "The limit is just $f(a)$"
✗ **Wrong:** "$h(1) = 5$, so $\lim_{x \to 1} h(x) = 5$", for the function $h$ of
[](#rem-calc-limit-value-irrelevant), with $h(x) = x + 1$ for $x \ne 1$ and $h(1) = 5$.

**Why:** the definition only looks at $x \ne a$. The value $f(a)$ may be different from the
limit, or not be defined at all, as for $\frac{x^2 - 1}{x - 1}$ at $1$.

✓ **Right:** $\lim_{x \to 1} h(x) = 2$, because $\abs{h(x) - 2} = \abs{x - 1}$ for $x \ne 1$,
so $\delta = \eps$ works. Substituting $x = a$ gives the limit only for functions that are
known to behave well at $a$, and that is something to prove, not assume.
:::

:::{warning} Letting $\delta$ depend on $x$
✗ **Wrong:** "To prove $\lim_{x \to 2} x^2 = 4$: we need $\abs{x - 2}\,\abs{x + 2} < \eps$,
so take $\delta = \dfrac{\eps}{\abs{x + 2}}$."

**Why:** $\delta$ describes the whole window, so it must be chosen before any $x$ in it, from
$\eps$ (and $a$) alone. A "$\delta$" that changes with $x$ is not a window at all: there is no
single interval of $x$ that it describes.

✓ **Right:** first bound the troublesome factor on a fixed window. If $\abs{x - 2} < 1$, then
$\abs{x + 2} < 5$, so $\delta = \min\bigl(1, \frac{\eps}{5}\bigr)$ works
([](#eg-calc-limit-quadratic-eps-delta)).
:::

:::{warning} Checking one $\eps$, or a few points
✗ **Wrong:** "For $\eps = 0.1$ the widget found $\delta = 0.0248$, so $\lim_{x \to 2} x^2 = 4$."
Or: "$\sin(\pi/x)$ is $0$ at $x = 0.1, 0.01, 0.001$, so its limit at $0$ is $0$."

**Why:** the definition says *for every* $\eps > 0$, and *every* $x$ in the window. One
$\eps$, or finitely many points, is evidence, not a proof. The table of $\sin(\pi/x)$ in
[Why this matters](#wdg-calc-limit-misleading-table) is correct and still misleading: the limit
does not exist ([](#exr-calc-limit-sin-pi-over-x)).

✓ **Right:** prove the inequality for an arbitrary $\eps > 0$ and an arbitrary $x$ in the
window, as in [](#eg-calc-limit-linear-eps-delta). Use tables and the widget to *guess* the
limit and the $\delta$, then prove the guess.
:::

:::{warning} Reading "$\frac{0}{0}$" as the value of a limit
✗ **Wrong:** "$\lim_{h \to 0} \dfrac{5(1+h)^2 - 5}{h} = \dfrac{0}{0}$, so the limit does not
exist."

**Why:** $\frac{0}{0}$ is not a number; it only says that substituting $h = 0$ tells us
nothing. The definition never substitutes $h = 0$.

✓ **Right:** simplify for $h \ne 0$ first, then find the limit: here
$\frac{5(1+h)^2 - 5}{h} = 10 + 5h$ for $h \ne 0$, and the limit is $10$
([](#eg-calc-limit-average-speed)).
:::

## Rigorous track

:::{proof:example} Prove $\lim_{x \to 2} x^2 = 4$ from the definition
:label: eg-calc-limit-quadratic-eps-delta
:class: dropdown

**Goal.** Given $\eps > 0$, find $\delta > 0$ such that $0 < \abs{x - 2} < \delta$ implies
$\abs{x^2 - 4} < \eps$. The function $x^2$ is defined for every $x$.

1. **Scratch work.** $\abs{x^2 - 4} = \abs{x - 2}\,\abs{x + 2}$. The first factor is the one
   that $\delta$ controls. The second, $\abs{x + 2}$, changes with $x$, so we first bound it on a
   fixed window.
2. **Bound the other factor.** If $\abs{x - 2} < 1$, then $1 < x < 3$, by
   [part (a) of the proposition on distance inequalities](#prop-calc-abs-interval), so
   $3 < x + 2 < 5$ and $\abs{x + 2} < 5$.
3. **Choose $\delta$.** On that window, $\abs{x^2 - 4} < 5\abs{x - 2}$, which is less than
   $\eps$ when $\abs{x - 2} < \frac{\eps}{5}$. Both conditions hold if
   $\delta = \min\bigl(1, \frac{\eps}{5}\bigr)$.
4. **Proof.** Let $\eps > 0$ and $\delta = \min\bigl(1, \frac{\eps}{5}\bigr)$, and let
   $0 < \abs{x - 2} < \delta$. Since $\delta \le 1$, step 2 gives $\abs{x + 2} < 5$. Since
   $\delta \le \frac{\eps}{5}$ and $\abs{x - 2} > 0$,
   $$
   \abs{x^2 - 4} = \abs{x - 2}\,\abs{x + 2} < 5\abs{x - 2} < 5 \cdot \frac{\eps}{5} = \eps .
   $$
   (The first $<$ multiplies $\abs{x + 2} < 5$ by the positive number $\abs{x - 2}$.) So
   $\lim_{x \to 2} x^2 = 4$.

$$
\boxed{\delta = \min\Bigl(1, \frac{\eps}{5}\Bigr)}
$$

**Why the $1$?** It caps the window, and that is what makes $\abs{x + 2} < 5$ true. Without it,
$\delta = \frac{\eps}{5}$ fails for large $\eps$: for $\eps = 100$ it gives $\delta = 20$, and
$x = 21$ is in the window but $\abs{21^2 - 4} = 437 > 100$. Any fixed cap would do; a cap of
$\frac12$ gives $\abs{x + 2} < 4.5$ and $\delta = \min\bigl(\frac12, \frac{\eps}{4.5}\bigr)$.

**Check.** For $\eps = 0.5$: $\delta = \min(1, 0.1) = 0.1$, below the largest $\delta$ that the
[ε–δ figure](#wdg-calc-limit-eps-delta) reports for both sides, $0.12132$. ✓ The point
$x = 2.09$ gives $\abs{2.09^2 - 4} = 0.3681 < 0.5$. ✓
:::

:::{admonition} The definition in symbols, and its negation
:class: dropdown rigor
With quantifiers, $\lim_{x \to a} f(x) = L$ says
$$
\forall \eps > 0 \ \ \exists \delta > 0 \ \ \forall x \colon \quad
0 < \abs{x - a} < \delta \implies \bigl(x \in \dom f \text{ and } \abs{f(x) - L} < \eps\bigr).
$$
Here $\dom f$ is [the domain](#def-calc-domain-range) of $f$. The order matters.
"$\exists \delta > 0 \ \forall \eps > 0$" would ask for one window that works for every
tolerance at once. For $f(x) = x$ at $a = 0$, with $L = 0$, that is false: for each
$\delta > 0$, the tolerance $\eps = \frac{\delta}{2}$ fails at the point $x = \frac{3\delta}{4}$
of the window, where $\abs{f(x) - 0} = \frac{3\delta}{4} \ge \frac{\delta}{2}$.

To negate, each $\forall$ becomes $\exists$ and each $\exists$ becomes $\forall$, the
implication $P \implies Q$ becomes "$P$ and not $Q$", and, by De Morgan's law,
"not ($A$ and $B$)" becomes "(not $A$) or (not $B$)". So $L$ is **not** the limit when
$$
\exists \eps > 0 \ \ \forall \delta > 0 \ \ \exists x \colon \quad
0 < \abs{x - a} < \delta \ \text{ and } \ \bigl(x \notin \dom f \text{ or } \abs{f(x) - L} \ge \eps\bigr).
$$
This is the pattern of the three non-existence examples: one $\eps$, and for each $\delta$ a
point $x$ that fails.
:::

:::{admonition} Why "$0 < \abs{x - a}$"?
:class: dropdown rigor
The condition $0 < \abs{x - a}$ removes $x = a$ from every window. Without it, the
definition would demand $\abs{f(a) - L} < \eps$ for every $\eps > 0$, that is, $f(a) = L$, and
it would not apply at all where $f(a)$ is undefined. Both are exactly the cases we need
limits for: the average speed $\frac{5(1+h)^2 - 5}{h}$ is undefined at $h = 0$. The
definition is built to describe how $f$ behaves *near* $a$, which is information that $f(a)$
cannot give.
:::

:::{admonition} Why $f$ must be defined near $a$
:class: dropdown rigor
[](#def-calc-limit) asks for $f$ to be defined on an open interval around $a$ (except
possibly at $a$), and, in its domain clause, for $f$ to be defined at every point of the
window. The proof of [](#thm-calc-limit-unique) rests on that clause of the definition: it picks
a point $x = a + \frac{\delta}{2}$ in the window and uses $f(x)$.

Suppose the definition dropped both requirements, the open interval and the domain clause,
and only asked that "$x \in \dom f$ and $0 < \abs{x - a} < \delta$ imply
$\abs{f(x) - L} < \eps$". Take $f(x) = \sqrt{x}$ and $a = -1$. For $\delta \le 1$ no $x$ in the
domain $[0, \infty)$ satisfies $0 < \abs{x + 1} < \delta$, so the condition holds for *every*
$L$, and every real number would be "the limit" of $\sqrt{x}$ at $-1$. Uniqueness fails, so
that version of the definition needs a further hypothesis.

Many analysis books use such a domain-relative definition, with the hypothesis that every
window around $a$ contains points of the domain other than $a$ ($a$ is a *limit point* of the
domain). It agrees with ours whenever $f$ is defined on an open interval around $a$ (except
possibly at $a$), and it also allows endpoints: it gives $\lim_{x \to 0} \sqrt{x} = 0$, where
our definition does not apply, because $\sqrt{x}$ is undefined to the left of $0$.
:::

:::{admonition} Looking ahead
:class: looking-ahead
At an endpoint such as $0$ for $\sqrt{x}$, our course uses one-sided limits instead
($\lim_{x \to 0^{+}} \sqrt{x} = 0$), on the page One-Sided Limits.
:::

## Summary

- $\lim_{x \to a} f(x) = L$ is about the values of $f$ **near** $a$, never **at** $a$: $f(a)$
  may differ from the limit or be undefined ([](#rem-calc-limit-value-irrelevant)).
- Precisely ([](#def-calc-limit)): for every $\eps > 0$ there is a $\delta > 0$ such that
  $$
  \boxed{0 < \abs{x - a} < \delta \implies \abs{f(x) - L} < \eps .}
  $$
- The $\delta$ may depend on $\eps$ and $a$, never on $x$. To prove a limit, rewrite
  $\abs{f(x) - L}$ in terms of $\abs{x - a}$, choose $\delta$, then check it; for a quadratic,
  cap the window first, as in $\delta = \min\bigl(1, \frac{\eps}{5}\bigr)$.
- A limit, if it exists, is unique ([](#thm-calc-limit-unique)).
- A limit fails to exist when, for every $L$, some $\eps$ defeats every $\delta$: typically a
  jump, oscillation, or unbounded values.
- Tables, graphs and the ε–δ widget suggest limits and $\delta$s; only a proof establishes
  them.

## Exercises

::::{exercise} Reading a limit from a table
:label: exr-calc-limit-table-estimate
:class: tier-a

Use a table of values with $x = 0.1, 0.01, 0.001$ (and the negatives) to estimate
$\displaystyle \lim_{x \to 0} \frac{\sqrt{1 + x} - 1}{x}$ to two decimal places.

:::{admonition} Hint 1
:class: dropdown hint
Evaluate on both sides of $0$ with a calculator. Do the values settle as $x$ shrinks?
:::

:::{admonition} Answer
:class: dropdown answer numeric-5e-3
$0.50$
:::
::::

::::{solution} exr-calc-limit-table-estimate
:label: sol-calc-limit-table-estimate
:class: dropdown

To six decimal places:

| $x$ | $0.1$ | $0.01$ | $0.001$ | $-0.001$ | $-0.01$ | $-0.1$ |
|---|---|---|---|---|---|---|
| $\frac{\sqrt{1 + x} - 1}{x}$ | $0.488088$ | $0.498756$ | $0.499875$ | $0.500125$ | $0.501256$ | $0.513167$ |

As $x$ approaches $0$, the values seem to approach $\frac12$: those from the right increase
towards it and those from the left decrease towards it. At $x = \pm 0.001$ they agree to two
decimal places, $0.50$. So we estimate the limit as $0.50$. This is an
estimate, not a proof: a table checks only finitely many points
([Why this matters](#wdg-calc-limit-misleading-table)).

:::{admonition} Looking ahead
:class: looking-ahead
The exact value is $\frac12$. For $x \ne 0$ (and $x \ge -1$), multiplying the numerator and
the denominator by $\sqrt{1 + x} + 1$ gives $\frac{1}{\sqrt{1 + x} + 1}$, which is defined at
$x = 0$ and equals $\frac12$ there. The page Computing Limits Algebraically shows why such a
step gives the limit; rationalising is one of its methods.
:::
::::

::::{exercise} The value at the point
:label: exr-calc-limit-value-at-a
:class: tier-a

Let $g(x) = 2x + 1$ for $x \ne 2$, and $g(2) = 0$. Find (a) $g(2)$ and (b)
$\displaystyle \lim_{x \to 2} g(x)$.

:::{admonition} Hint 1
:class: dropdown hint
Which values of $g$ does the definition of the limit look at?
:::

:::{admonition} Answer
:class: dropdown answer
(a) $0$ (b) $5$
:::
::::

::::{solution} exr-calc-limit-value-at-a
:label: sol-calc-limit-value-at-a
:class: dropdown

(a) By its definition, $g(2) = 0$.

(b) The definition of the limit only uses $x \ne 2$ ([](#rem-calc-limit-value-irrelevant)), and
there $g(x) = 2x + 1$. For $x \ne 2$,
$$
\abs{g(x) - 5} = \abs{2x - 4} = 2\abs{x - 2},
$$
so for $\eps > 0$ the choice $\delta = \frac{\eps}{2}$ works, as in
[](#eg-calc-limit-linear-eps-delta): $0 < \abs{x - 2} < \frac{\eps}{2}$ implies
$\abs{g(x) - 5} < \eps$. Hence $\lim_{x \to 2} g(x) = 5$, although $g(2) = 0$.
::::

::::{exercise} The largest δ for a line
:label: exr-calc-limit-largest-delta-linear
:class: tier-a

For $f(x) = 5x + 2$, $a = 1$ and $L = 7$, find the largest $\delta > 0$ such that
$0 < \abs{x - 1} < \delta$ implies $\abs{f(x) - 7} < 0.01$.

:::{admonition} Hint 1
:class: dropdown hint
Write $\abs{f(x) - 7}$ as a multiple of $\abs{x - 1}$.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{500}$
:::
::::

::::{solution} exr-calc-limit-largest-delta-linear
:label: sol-calc-limit-largest-delta-linear
:class: dropdown

$\abs{f(x) - 7} = \abs{5x - 5} = 5\abs{x - 1}$, so $\abs{f(x) - 7} < 0.01$ exactly when
$\abs{x - 1} < 0.002$. Hence every $\delta \le 0.002$ works. A larger $\delta$ does not: its
window contains $x = 1.002$, where $\abs{f(x) - 7} = 0.01$, which is not less than $0.01$.
The largest $\delta$ is $0.002 = \frac{1}{500}$.
::::

::::{exercise} How close is close enough?
:label: exr-calc-limit-large-values
:class: tier-a

Let $f(x) = \dfrac{1}{x^2}$ for $x \ne 0$. Find the largest $\delta > 0$ such that every $x$
with $0 < \abs{x} < \delta$ has $f(x) > 10\,000$.

:::{admonition} Hint 1
:class: dropdown hint
For $x \ne 0$, both $x^2$ and $10\,000$ are positive. When is $\frac{1}{x^2} > 10\,000$?
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{100}$
:::
::::

::::{solution} exr-calc-limit-large-values
:label: sol-calc-limit-large-values
:class: dropdown

For $x \ne 0$, $x^2 > 0$, so multiplying by the positive number $\frac{x^2}{10\,000}$ shows
that $\frac{1}{x^2} > 10\,000$ exactly when $x^2 < \frac{1}{10\,000}$. Now $x^2 = \abs{x}^2$, by
[property 5 of the absolute value](#rem-calc-absolute-value-properties), and
$\frac{1}{10\,000} = \bigl(\frac{1}{100}\bigr)^2$. Both $\abs{x}$ and $\frac{1}{100}$ are
non-negative, so by the order part of [the square-root remark](#rem-calc-square-roots), which is
also [property 6 of the absolute value](#rem-calc-absolute-value-properties), this holds exactly
when $\abs{x} < \frac{1}{100}$.
So $\delta = \frac{1}{100}$ works. A larger $\delta$ does not: its window contains
$x = \frac{1}{100}$, where $f(x) = 10\,000$, which is not greater than $10\,000$.

The same argument works for any bound in place of $10\,000$, which is why no number $L$ can be
the limit ([](#eg-calc-limit-unbounded)).
::::

::::{exercise} The exact δ in the ε–δ figure
:label: exr-calc-limit-widget-largest-delta
:class: tier-b widget

In [the ε–δ figure](#wdg-calc-limit-eps-delta), $f(x) = x^2$, $a = 2$ and $L = 4$. For
$\eps = 0.1$, find exactly the largest $\delta > 0$ such that $\abs{x^2 - 4} < 0.1$ for every
$x$ in the window (a) on the right, $2 < x < 2 + \delta$; (b) on the left,
$2 - \delta < x < 2$; (c) on both sides, $0 < \abs{x - 2} < \delta$. Then compare with the
numbers the widget reports.

:::{admonition} Hint 1
:class: dropdown hint
$\abs{x^2 - 4} < 0.1$ means $3.9 < x^2 < 4.1$. For $x > 0$, take square roots.
:::

:::{admonition} Hint 2
:class: dropdown hint
For (c), the window must fit inside the allowed region on both sides at once.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $\frac{\sqrt{410}}{10} - 2$ (b) $2 - \frac{\sqrt{390}}{10}$ (c) $\frac{\sqrt{410}}{10} - 2$
:::
::::

::::{solution} exr-calc-limit-widget-largest-delta
:label: sol-calc-limit-widget-largest-delta
:class: dropdown

By [part (a) of the proposition on distance inequalities](#prop-calc-abs-interval), applied to
$x^2$ with $a = 4$ and $\delta = 0.1$, $\abs{x^2 - 4} < 0.1$ means $3.9 < x^2 < 4.1$. For
$x > 0$, this means $\sqrt{3.9} < x < \sqrt{4.1}$, by the order part of
[the square-root remark](#rem-calc-square-roots): for $s, t \ge 0$, $s < t$ exactly when
$s^2 < t^2$, and here $(\sqrt{3.9})^2 = 3.9$ and $(\sqrt{4.1})^2 = 4.1$. Every window below
lies in $x > 0$.

(a) For $x > 2$ the condition $x > \sqrt{3.9}$ holds automatically ($\sqrt{3.9} < 2$, by the
same order part, since $3.9 < 4 = 2^2$), so we need $x < \sqrt{4.1}$ for every $x$ in
$(2, 2 + \delta)$. That holds exactly when $2 + \delta \le \sqrt{4.1}$. The largest $\delta$
is $\sqrt{4.1} - 2 \approx 0.0248457$.

(b) For $x < 2$ the condition $x < \sqrt{4.1}$ holds automatically ($2 < \sqrt{4.1}$, since
$2^2 = 4 < 4.1$), so we need $x > \sqrt{3.9}$ for every $x$ in $(2 - \delta, 2)$, that is,
$2 - \delta \ge \sqrt{3.9}$. The largest $\delta$ is $2 - \sqrt{3.9} \approx 0.0251582$.

(c) The window works on both sides exactly when $\delta$ is at most both numbers, so the largest
is the smaller one. To compare them without a calculator: $\sqrt{4.1} - 2 < 2 - \sqrt{3.9}$
means $\sqrt{4.1} + \sqrt{3.9} < 4$. We compare squares, using the order part of
[the square-root remark](#rem-calc-square-roots) for non-negative numbers. First,
$\bigl(\sqrt{4.1}\,\sqrt{3.9}\bigr)^2 = 4.1 \cdot 3.9 = 15.99 < 16 = 4^2$, so
$\sqrt{4.1}\,\sqrt{3.9} < 4$. Then
$$
\bigl(\sqrt{4.1} + \sqrt{3.9}\bigr)^2 = 4.1 + 2\sqrt{4.1}\,\sqrt{3.9} + 3.9
< 8 + 2 \cdot 4 = 16 = 4^2,
$$
so $\sqrt{4.1} + \sqrt{3.9} < 4$. So the right side's value $\sqrt{4.1} - 2$ is the smaller
one, and it is the answer to (c).

The widget reports $0.0248456$ and $0.0251582$: here, these are the exact values rounded down to
six significant digits. Its method promises less: the $\delta$ it reports passed at every point
it checked and lies below every point where it saw the check fail, and it may be smaller than
the exact value by about $10^{-5}$ of that value.

In the answer, the square roots are written with whole numbers under the root:
$\sqrt{4.1} = \frac{\sqrt{410}}{10}$, because $\frac{\sqrt{410}}{10} \ge 0$ and
$\bigl(\frac{\sqrt{410}}{10}\bigr)^2 = \frac{410}{100} = 4.1$, and the square root is unique
([the square-root remark](#rem-calc-square-roots)). In the same way,
$\sqrt{3.9} = \frac{\sqrt{390}}{10}$.
::::

::::{exercise} The stone at $t = 2$
:label: exr-calc-limit-average-speed
:class: tier-b applied

The stone of Why this matters has fallen $s(t) = 5t^2$ metres after $t$ seconds. Its average
speed between $t = 2$ and $t = 2 + h$ is $v(h) = \dfrac{s(2 + h) - s(2)}{h}$ for $h \ne 0$.
(a) Find $\displaystyle \lim_{h \to 0} v(h)$, in m/s, and prove it from the definition.
(b) Find the largest $\delta > 0$ (in seconds) such that $0 < \abs{h} < \delta$ guarantees that
$v(h)$ is within $0.1$ m/s of that limit.

:::{admonition} Hint 1
:class: dropdown hint
Expand $5(2 + h)^2$ and simplify $v(h)$ for $h \ne 0$, as in [](#eg-calc-limit-average-speed).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $20$ (b) $\frac{1}{50}$
:::
::::

::::{solution} exr-calc-limit-average-speed
:label: sol-calc-limit-average-speed
:class: dropdown

(a) For $h \ne 0$,
$$
v(h) = \frac{5(4 + 4h + h^2) - 20}{h} = \frac{20h + 5h^2}{h} = 20 + 5h,
$$
so $\abs{v(h) - 20} = 5\abs{h}$. Given $\eps > 0$, let $\delta = \frac{\eps}{5}$: if
$0 < \abs{h} < \delta$, then $\abs{v(h) - 20} = 5\abs{h} < \eps$. So
$\lim_{h \to 0} v(h) = 20$ m/s.

(b) $\abs{v(h) - 20} < 0.1$ exactly when $5\abs{h} < 0.1$, that is, $\abs{h} < 0.02$. So
$\delta = 0.02$ s $= \frac{1}{50}$ s works, and no larger $\delta$ does: at $h = 0.02$ the
difference is exactly $0.1$ m/s.
::::

::::{exercise} An ε–δ proof
:label: exr-calc-limit-eps-delta-linear
:class: tier-b

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

**Scratch work.** $\abs{(4 - 3x) - 7} = \abs{-3x - 3} = 3\abs{x + 1} = 3\abs{x - (-1)}$.

**Choose $\delta$.** We need $3\abs{x + 1} < \eps$, that is, $\abs{x + 1} < \frac{\eps}{3}$, so
we take $\delta = \frac{\eps}{3}$.

**Proof.** The function $4 - 3x$ is defined for every $x$. Let $\eps > 0$ and
$\delta = \frac{\eps}{3}$. If $0 < \abs{x + 1} < \delta$, then
$$
\abs{(4 - 3x) - 7} = 3\abs{x + 1} < 3 \cdot \frac{\eps}{3} = \eps .
$$
Hence $\lim_{x \to -1} (4 - 3x) = 7$.
::::

::::{exercise} One tolerance at a jump
:label: exr-calc-limit-jump-which-eps
:class: tier-b

Let $H(x) = 0$ for $x < 0$ and $H(x) = 1$ for $x \ge 0$. Someone claims that
$\lim_{x \to 0} H(x) = \frac12$. For which $\eps > 0$ is there a $\delta > 0$ such that
$0 < \abs{x} < \delta$ implies $\abs{H(x) - \frac12} < \eps$? Give the set of all such $\eps$.
What does your answer say about the claim?

:::{admonition} Hint 1
:class: dropdown hint
Compute $\abs{H(x) - \frac12}$ for $x < 0$ and for $x > 0$.
:::

:::{admonition} Answer
:class: dropdown answer set
$(\frac{1}{2}, \infty)$
:::
::::

::::{solution} exr-calc-limit-jump-which-eps
:label: sol-calc-limit-jump-which-eps
:class: dropdown

For $x < 0$, $\abs{H(x) - \frac12} = \abs{0 - \frac12} = \frac12$, and for $x > 0$,
$\abs{H(x) - \frac12} = \abs{1 - \frac12} = \frac12$. So at every $x \ne 0$ the distance from
$H(x)$ to $\frac12$ is exactly $\frac12$.

- If $\eps > \frac12$, every $\delta > 0$ works, because $\frac12 < \eps$ at every point of
  every window.
- If $0 < \eps \le \frac12$, no $\delta$ works: every window contains, for example,
  $x = \frac{\delta}{2}$, where the distance is $\frac12 \ge \eps$.

So the set is $(\frac12, \infty)$. The claim fails: the definition needs a $\delta$ for *every*
$\eps > 0$, and already $\eps = \frac12$ has none. So $\frac12$ is not the limit. (No other
number is either: the argument of [](#eg-calc-limit-jump) works for $H$ with the values $0$ and
$1$ and $\eps = \frac12$.)
::::

::::{exercise} The misleading table, settled
:label: exr-calc-limit-sin-pi-over-x
:class: tier-c

The first three rows of the table in
[Why this matters](#wdg-calc-limit-misleading-table) suggest that
$\displaystyle \lim_{x \to 0} \sin\Bigl(\frac{\pi}{x}\Bigr) = 0$. Is this true? Prove your
answer from [the definition](#def-calc-limit).

:::{admonition} Hint 1
:class: dropdown hint
Look at the last three rows. For which $x$ is $\sin(\pi/x) = 1$?
:::

:::{admonition} Hint 2
:class: dropdown hint
$\sin\bigl(2\pi n + \frac{\pi}{2}\bigr) = 1$ for every integer $n$. Which $x$ gives
$\frac{\pi}{x} = 2\pi n + \frac{\pi}{2}$?
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-limit-sin-pi-over-x
:label: sol-calc-limit-sin-pi-over-x
:class: dropdown

It is false. We show that $0$ is not the limit by finding one $\eps$ that no $\delta$ can
answer: $\eps = \frac12$.

For an integer $n \ge 1$ let $x_n = \frac{2}{4n + 1}$. Then $\frac{\pi}{x_n} = 2\pi n +
\frac{\pi}{2}$, so $\sin\bigl(\frac{\pi}{x_n}\bigr) = 1$. (The last three rows of the table are
$x_n$ for $n = 6, 31, 156$.)

Let $\delta > 0$. By [the Archimedean property](#rem-calc-naturals-unbounded), there is an
integer $n \ge 1$ with $n > \frac{1}{2\delta}$. Then $4n + 1 > 4n > \frac{2}{\delta}$, so
$0 < x_n = \frac{2}{4n + 1} < \delta$: the point $x_n$ is in the window. There
$\abs{\sin(\pi/x_n) - 0} = 1 \ge \frac12$. So every window contains a point that fails, no
$\delta$ works for $\eps = \frac12$, and $\lim_{x \to 0} \sin(\pi/x) \ne 0$.

In fact the limit does not exist at all. The points $\frac{1}{n}$ give
$\sin(n\pi) = 0$ and the points $x_n$ give $1$, and both kinds lie in every window, so the
argument of [](#eg-calc-limit-sin-1-over-x) applies with these points.
::::

::::{exercise} A quadratic ε–δ proof
:label: exr-calc-limit-eps-delta-quadratic
:class: tier-c rigor

Prove from [the definition](#def-calc-limit) that $\lim_{x \to 3} x^2 = 9$.

:::{admonition} Hint 1
:class: dropdown hint
Factor $x^2 - 9$. One factor is controlled by $\delta$; bound the other on the window
$\abs{x - 3} < 1$.
:::

:::{admonition} Hint 2
:class: dropdown hint
If $\abs{x - 3} < 1$, then $2 < x < 4$, by
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval). How large can
$\abs{x + 3}$ be?
:::

:::{admonition} Answer
:class: dropdown answer manual
$\delta = \min(1, \eps/7)$ works.
:::
::::

::::{solution} exr-calc-limit-eps-delta-quadratic
:label: sol-calc-limit-eps-delta-quadratic
:class: dropdown

We follow [](#eg-calc-limit-quadratic-eps-delta).

**Scratch work.** $\abs{x^2 - 9} = \abs{x - 3}\,\abs{x + 3}$. If $\abs{x - 3} < 1$, then
$2 < x < 4$, by [part (a) of the proposition on distance inequalities](#prop-calc-abs-interval),
so $5 < x + 3 < 7$ and $\abs{x + 3} < 7$. Then $\abs{x^2 - 9} < 7\abs{x - 3}$,
which is less than $\eps$ when $\abs{x - 3} < \frac{\eps}{7}$.

**Proof.** $x^2$ is defined for every $x$. Let $\eps > 0$ and
$\delta = \min\bigl(1, \frac{\eps}{7}\bigr)$, and let $0 < \abs{x - 3} < \delta$. Since
$\delta \le 1$, $\abs{x + 3} < 7$. Since $\abs{x - 3} > 0$ and $\delta \le \frac{\eps}{7}$,
$$
\abs{x^2 - 9} = \abs{x - 3}\,\abs{x + 3} < 7\abs{x - 3} < 7 \cdot \frac{\eps}{7} = \eps .
$$
Hence $\lim_{x \to 3} x^2 = 9$.
::::

::::{exercise} A square root, and the domain
:label: exr-calc-limit-eps-delta-sqrt
:class: tier-c rigor

Prove from [the definition](#def-calc-limit) that $\lim_{x \to 4} \sqrt{x} = 2$. Make sure
that your $\delta$ keeps the window inside the domain of $\sqrt{x}$.

:::{admonition} Hint 1
:class: dropdown hint
Multiply $\sqrt{x} - 2$ by $\frac{\sqrt{x} + 2}{\sqrt{x} + 2}$.
:::

:::{admonition} Hint 2
:class: dropdown hint
$\sqrt{x} + 2 \ge 2$ wherever $\sqrt{x}$ is defined. Which $\delta$ keeps $x \ge 0$?
:::

:::{admonition} Answer
:class: dropdown answer manual
$\delta = \min(4, 2\eps)$ works.
:::
::::

::::{solution} exr-calc-limit-eps-delta-sqrt
:label: sol-calc-limit-eps-delta-sqrt
:class: dropdown

The domain of $\sqrt{x}$ is $[0, \infty)$, which contains the open interval $(0, 8)$ around
$4$, so [](#def-calc-limit) applies.

**Scratch work.** For $x \ge 0$, $(\sqrt{x} - 2)(\sqrt{x} + 2) = x - 4$, because
$(\sqrt{x})^2 = x$, and $\sqrt{x} + 2 \ge 2 > 0$, because $\sqrt{x} \ge 0$
([the square-root remark](#rem-calc-square-roots)). So, by
[property 4 of the absolute value](#rem-calc-absolute-value-properties),
$$
\abs{\sqrt{x} - 2} = \frac{\abs{x - 4}}{\sqrt{x} + 2} \le \frac{\abs{x - 4}}{2}.
$$
This is less than $\eps$ when $\abs{x - 4} < 2\eps$. The window must also lie in the domain:
$\abs{x - 4} < 4$ gives $0 < x < 8$, by
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval).

**Proof.** Let $\eps > 0$ and $\delta = \min(4, 2\eps)$. If $0 < \abs{x - 4} < \delta$, then
$0 < x < 8$, so $\sqrt{x}$ is defined, and
$$
\abs{\sqrt{x} - 2} \le \frac{\abs{x - 4}}{2} < \frac{2\eps}{2} = \eps .
$$
Hence $\lim_{x \to 4} \sqrt{x} = 2$.

Without the cap $4$, the proof breaks for $\eps > 2$: $\delta = 2\eps > 4$ would put negative
$x$ in the window, where $\sqrt{x}$ is undefined.
::::

## Where this leads

:::{where-this-leads}
:::

Every page of the Limits chapter plays the ε–δ game of this page: the limit laws are proved
with it, once, so that later limits can be computed without it.
