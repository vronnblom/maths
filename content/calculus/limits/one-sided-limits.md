---
title: One-Sided Limits
label: calc-one-sided-limits
description: >-
  Limits from the left and from the right: their precise definition, how to compute them for
  piecewise functions and at an endpoint such as 0 for the square root, and how they decide
  whether a limit exists.
tags: [limits, epsilon-delta]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 2
  est_minutes: 40
  prerequisites: [calc-limit]
  objectives:
    - Compute left and right limits, including for piecewise functions.
    - Decide existence of a limit from the one-sided limits.
  verify: verify/calculus/limits/test_one_sided_limits.py
  widgets: [epsilon-delta]
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

A courier charges £3 for a parcel of up to 2 kg, and £5 for a parcel over 2 kg and up to
10 kg. For a parcel of $w$ kilograms, where $0 < w \le 10$, the price in pounds is
$$
P(w) =
\begin{cases}
3 & \text{if } 0 < w \le 2,\\
5 & \text{if } 2 < w \le 10.
\end{cases}
$$
What does the price do near 2 kg? A parcel of 1.999 kg costs £3 and one of 2.001 kg costs £5,
and however close to 2 kg the two weights are, the two prices stay £2 apart. So $P(w)$
approaches no single number as $w$ approaches $2$: $\lim_{w \to 2} P(w)$ does not exist, as we
prove in [](#eg-calc-one-sided-limits-parcel). But "does not exist" throws away what we
know. Just below 2 kg the price is £3, and just above it is £5. We would like to say that
$P(w)$ approaches $3$ as $w$ approaches $2$ from the left, approaches $5$ from the right, and so
jumps by £2 at 2 kg.

A second situation has the same cure. [The definition of the limit](#def-calc-limit) asks for
$f$ to be defined on an open interval around $a$, except possibly at $a$. The square root
$\sqrt{x}$ is defined for no $x < 0$, because a negative number has no real square root
([the square-root remark](#rem-calc-square-roots)), so that definition says nothing about
$\sqrt{x}$ at $0$. Yet $\sqrt{x}$ is as small as we like when $x > 0$ is small enough:
$\sqrt{0.0001} = 0.01$.

A **one-sided limit** looks at one side of $a$ only. It describes the jump of the price, and
the square root at $0$, and it gives a practical test for whether a limit exists: look at the
two sides separately, then compare.

:::{admonition} Looking ahead
:class: looking-ahead
The page Infinite Limits and Vertical Asymptotes uses one-sided limits to describe functions
such as $\frac{1}{x}$, whose values near $0$ grow without bound in one direction on the right
of $0$ and in the other on the left.
:::

## Limits from one side

Informally, $\lim_{x \to a^{+}} f(x) = L$ means that $f(x)$ is as close to $L$ as we like for
all $x$ close enough to $a$ and **greater than** $a$. The window of the ε–δ game becomes the
right half of the window of [the definition of the limit](#def-calc-limit): the punctured
neighbourhood $0 < \abs{x - a} < \delta$ is the set $(a - \delta, a) \cup (a, a + \delta)$, by
[part (e) of the proposition on distance inequalities](#prop-calc-abs-interval), and a
one-sided limit keeps only one of the two intervals.

:::{proof:definition} One-sided limits
:label: def-calc-one-sided-limit

Let $a$ and $L$ be real numbers.

(a) Let $f$ be a function that is defined at every point of an open interval $(a, a + r)$, for
some $r > 0$. We say that **the limit of $f(x)$ as $x$ approaches $a$ from the right is $L$**,
and write
$$
\lim_{x \to a^{+}} f(x) = L,
$$
if for every $\eps > 0$ there is a $\delta > 0$ such that $f$ is defined at every $x$ with
$a < x < a + \delta$, and
$$
\begin{aligned}
&a < x < a + \delta \\
&\quad\text{implies}\quad \abs{f(x) - L} < \eps .
\end{aligned}
$$

(b) Let $f$ be a function that is defined at every point of an open interval $(a - r, a)$, for
some $r > 0$. We say that **the limit of $f(x)$ as $x$ approaches $a$ from the left is $L$**,
and write
$$
\lim_{x \to a^{-}} f(x) = L,
$$
if for every $\eps > 0$ there is a $\delta > 0$ such that $f$ is defined at every $x$ with
$a - \delta < x < a$, and
$$
\begin{aligned}
&a - \delta < x < a \\
&\quad\text{implies}\quad \abs{f(x) - L} < \eps .
\end{aligned}
$$

These are the **right-hand** and the **left-hand limit**, together the **one-sided limits**. We
also write $f(x) \to L$ as $x \to a^{+}$ (or $x \to a^{-}$).
:::

**In words.** The right-hand limit is [the definition of the limit](#def-calc-limit) with its
window $0 < \abs{x - a} < \delta$ replaced by the right half, $a < x < a + \delta$; the
left-hand limit keeps the left half, $a - \delta < x < a$. The game is the same: a challenger
names $\eps > 0$, you reply with $\delta > 0$, and you win the round if every $x$ in your
half-window has $f(x)$ within $\eps$ of $L$. Three points to notice:

- Neither half-window contains $a$. The value $f(a)$, and whether it exists, plays no part, for
  the same reason as in [the remark that the value at $a$ does not
  matter](#rem-calc-limit-value-irrelevant).
- The values of $f$ on the other side of $a$ play no part either. For the right-hand limit, $f$
  need not even be defined to the left of $a$: that is what makes $\lim_{x \to 0^{+}} \sqrt{x}$
  meaningful.
- As before, if a $\delta$ wins a round, so does every smaller $\delta > 0$. Since $f$ is
  defined on $(a, a + r)$ (in part (a)), every $\delta \le r$ gives a half-window inside that
  interval, so the requirement that $f$ be defined in the window only rules out windows that
  are too wide.

**Example.** Let $g(x) = x$ for $x \le 0$ and $g(x) = x + 1$ for $x > 0$. Then
$\lim_{x \to 0^{+}} g(x) = 1$. Given $\eps > 0$, take $\delta = \eps$. If $0 < x < \delta$, then
$g(x) = x + 1$, so $\abs{g(x) - 1} = \abs{x} = x < \eps$, where $\abs{x} = x$ because $x > 0$
([the definition of the absolute value](#def-calc-absolute-value)).

**Non-example.** $\lim_{x \to 0^{+}} g(x)$ is not $0$, although $g(0) = 0$. Take
$\eps = \frac12$. Whatever $\delta > 0$ is offered, the half-window $0 < x < \delta$ contains
$x = d$ with $d = \frac12 \min\bigl(\delta, 1\bigr)$, which is positive, and there
$\abs{g(d) - 0} = d + 1 > 1 > \frac12$. So no $\delta$ wins the round $\eps = \frac12$. (From
the left, $g(x) = x$, and $\lim_{x \to 0^{-}} g(x) = 0$, with $\delta = \eps$ as in the
example.)

The figure plays the game for the parcel price of Why this matters, with
the claim $\lim_{w \to 2^{+}} P(w) = 5$. The widget treats the two sides of $2$ separately,
which is exactly what a one-sided limit does.

::::{figure}
:label: wdg-calc-one-sided-limits-parcel

```{anywidget} ../../../widgets/epsilon-delta.mjs
{
  "f": "4 + sign(x - 2)", "a": 2, "L": 5,
  "eps": 0.5, "epsRange": [0.1, 2.5], "epsStep": 0.1,
  "xRange": [1, 3], "yRange": [2, 6]
}
```

Graph of the parcel price for weights from 1 kg to 3 kg: height $3$ to the left of $2$ and
height $5$ to the right, with a horizontal band of half-width $\eps$ around $y = 5$
(translucent, dashed edges) and a vertical window $0 < \abs{x - 2} < \delta$ (translucent, solid
edges; the dotted line $x = 2$ itself is left out, so the widget never uses the price at
exactly 2 kg). A slider sets $\eps$ from $0.1$ to $2.5$ in steps of $0.1$, starting at $0.5$.
For each $\eps$ the widget states, separately for the left and the right of $2$, the largest
$\delta$ it found or that it observed none. For $\eps = 0.5$ it reports on the right that the
values stayed in the band at every point it checked, out to the edge of the view ($\delta = 1$),
and on the left that it observed no $\delta$: the values leave the band at points as close to
$2$ as it checks. A second slider sets your own $\delta$; points of the graph inside the window
but outside the band are marked with crosses, and a sentence says whether your $\delta$ passed
the widget's check at the points it tested, or names a point where it fails.
::::

**Try this:**

1. At $\eps = 0.5$, read what the widget reports on each side of $2$. Which side's values are
   within $\eps$ of $5$?
2. Select the $\eps$ slider and raise $\eps$ one step at a time. At which $\eps$ does the widget
   first find a $\delta$ on the left? Why there, and not one step earlier?
3. Now the widget finds a $\delta$ on both sides. Does that make $5$ the limit of $P(w)$ as
   $w \to 2$? (The definition asks for a $\delta$ for *every* $\eps > 0$.)

The widget checks finitely many points, so what it reports are observations. The proofs are
on this page: [](#eg-calc-one-sided-limits-parcel) proves that the right-hand limit is $5$ and
the left-hand limit is $3$, and exercise [](#exr-calc-one-sided-limits-widget-eps) finds
exactly the $\eps$ for which some $\delta$ works on the left.

Could a function have two different right-hand limits at the same point? No, by the argument
that shows that a limit is unique, now with a point taken in the half-window.

:::{proof:remark} One-sided limits are unique
:label: rem-calc-one-sided-limit-unique

Let $f$ and $a$ be as in part (a) of [](#def-calc-one-sided-limit). If
$\lim_{x \to a^{+}} f(x) = L$ and $\lim_{x \to a^{+}} f(x) = M$, then $L = M$. The same holds
for left-hand limits, with $f$ and $a$ as in part (b).

*Reason.* Suppose $L \ne M$, and let $\eps = \frac12 \abs{L - M}$, which is positive by
[property 1 of the absolute value](#rem-calc-absolute-value-properties), since $L - M \ne 0$.
By part (a) of the definition, applied to $L$ and to $M$, there are $\delta_1 > 0$ and
$\delta_2 > 0$ such that $f$ is defined at every $x$ with $a < x < a + \delta_1$ and has
$\abs{f(x) - L} < \eps$ there, and is defined at every $x$ with $a < x < a + \delta_2$ and has
$\abs{f(x) - M} < \eps$ there. Let $\delta = \min(\delta_1, \delta_2)$ and
$x = a + \frac{\delta}{2}$. Then $a < x < a + \delta$, so $x$ lies in both half-windows:
$f(x)$ is defined, $\abs{f(x) - L} < \eps$ and $\abs{f(x) - M} < \eps$. By
[property 2 of the absolute value](#rem-calc-absolute-value-properties),
$\abs{L - f(x)} = \abs{f(x) - L}$. By
[part (b) of the triangle inequality](#thm-calc-triangle-inequality),
$\abs{u - v} \le \abs{u - w} + \abs{w - v}$, with $u = L$, $v = M$ and $w = f(x)$,
$$
\begin{aligned}
\abs{L - M} &\le \abs{L - f(x)} \\
&\quad + \abs{f(x) - M} \\
&< \eps + \eps = \abs{L - M},
\end{aligned}
$$
which is impossible. So $L = M$. For left-hand limits, take $x = a - \frac{\delta}{2}$
instead, which satisfies $a - \delta < x < a$.
:::

So we may speak of *the* right-hand limit and *the* left-hand limit, when they exist.

## Main results

The two half-windows together make up the punctured neighbourhood $0 < \abs{x - a} < \delta$.
So a limit should exist exactly when $f(x)$ settles near the same number on both sides.

:::{proof:theorem} A limit and its one-sided limits
:label: thm-calc-limit-iff-one-sided

Let $f$ and $a$ be as in [the definition of the limit](#def-calc-limit), and let $L$ be a real
number. Then
$$
\lim_{x \to a} f(x) = L
$$
if and only if both $\lim_{x \to a^{-}} f(x) = L$ and $\lim_{x \to a^{+}} f(x) = L$.
:::

:::{proof:proof} Rigorous track
:label: prf-calc-limit-iff-one-sided
:enumerated: false
:class: dropdown
By [part (e) of the proposition on distance inequalities](#prop-calc-abs-interval), the window
$0 < \abs{x - a} < \delta$ is made of the two half-windows $a - \delta < x < a$ and
$a < x < a + \delta$. So a $\delta$ that works for the limit works on each side, and
conversely the smaller of a $\delta$ for each side works for the limit.

**The one-sided limits make sense.** By hypothesis, $f$ is defined at every point of an open
interval $I$ containing $a$, except possibly at $a$. By
[the definition of an interval](#def-calc-interval), $I$ is $(c, d)$, $(c, \infty)$,
$(-\infty, d)$ or $\R$, and since $a \in I$, we have $c < a$ whenever $I$ has a left endpoint
$c$, and $a < d$ whenever it has a right endpoint $d$. Let $r$ be the smaller of the numbers
$a - c$ and $d - a$ that occur (one of them, if $I$ has only one endpoint), and $r = 1$ if
$I = \R$. Then $r > 0$, and every $x$ with $a - r < x < a + r$ lies in $I$: $r \le a - c$ gives
$c \le a - r < x$, and $r \le d - a$ gives $x < a + r \le d$. So $f$ is defined at every point
of $(a - r, a)$ and of $(a, a + r)$, as parts (b) and (a) of [](#def-calc-one-sided-limit)
require.

**If the limit is $L$, so are both one-sided limits.** Let $\eps > 0$. Since
$\lim_{x \to a} f(x) = L$, there is a $\delta > 0$ such that $f$ is defined at every $x$ with
$0 < \abs{x - a} < \delta$, and $\abs{f(x) - L} < \eps$ for each such $x$. If
$a < x < a + \delta$, then $0 < \abs{x - a} < \delta$, by part (e) of the proposition, read from
right to left. So $f(x)$ is defined and $\abs{f(x) - L} < \eps$: this $\delta$ wins the round
$\eps$ for the right-hand limit. In the same way, $a - \delta < x < a$ implies
$0 < \abs{x - a} < \delta$, so the same $\delta$ wins the round for the left-hand limit. Since
$\eps > 0$ was arbitrary, $\lim_{x \to a^{+}} f(x) = L$ and $\lim_{x \to a^{-}} f(x) = L$.

**If both one-sided limits are $L$, so is the limit.** Let $\eps > 0$. By part (b) of the
definition there is a $\delta_1 > 0$ such that $f$ is defined and $\abs{f(x) - L} < \eps$ at
every $x$ with $a - \delta_1 < x < a$; by part (a) there is a $\delta_2 > 0$ such that the same
holds at every $x$ with $a < x < a + \delta_2$. Let $\delta = \min(\delta_1, \delta_2)$, which
is positive, and let $0 < \abs{x - a} < \delta$. By part (e) of the proposition, read from left
to right, either $a - \delta < x < a$ or $a < x < a + \delta$.

- In the first case, multiplying $\delta \le \delta_1$ by the negative number ${-1}$ reverses
  it, $-\delta_1 \le -\delta$, and adding $a$ keeps it: $a - \delta_1 \le a - \delta < x < a$.
  So $x$ is in the half-window of $\delta_1$.
- In the second case, adding $a$ to $\delta \le \delta_2$ gives
  $a < x < a + \delta \le a + \delta_2$, so $x$ is in the half-window of $\delta_2$.

Either way, $f(x)$ is defined and $\abs{f(x) - L} < \eps$. So $\delta$ wins the round $\eps$
for the limit; since $\eps > 0$ was arbitrary, $\lim_{x \to a} f(x) = L$.
:::

**How to use it.** Let $f$ and $a$ be as in [the definition of the limit](#def-calc-limit).

1. If both one-sided limits exist and are equal, the limit exists and has that value: this is
   the "if" part of [](#thm-calc-limit-iff-one-sided).
2. If both one-sided limits exist but are different, say $L \ne M$, the limit does not exist.
   For if $\lim_{x \to a} f(x) = N$ for some real number $N$, the "only if" part of the theorem
   gives $\lim_{x \to a^{-}} f(x) = N$ and $\lim_{x \to a^{+}} f(x) = N$, and then
   [](#rem-calc-one-sided-limit-unique) gives $N = L$ and $N = M$, so $L = M$, which is false.
3. If one of the one-sided limits does not exist, the limit does not exist: by the "only if"
   part, a limit $N$ would be a one-sided limit on both sides.

The **jump** of $f$ at $a$ is then the difference $\lim_{x \to a^{+}} f(x) - \lim_{x \to a^{-}} f(x)$,
when both exist: it is $0$ exactly when they are equal.

## Worked examples

### Piecewise functions

A function given by different formulas on the two sides of $a$ is made for one-sided limits:
each half-window sees only one formula. The value at $a$ itself, whichever formula or special
value gives it, plays no part.

:::{proof:example} Two formulas that meet, and a value that does not
:label: eg-calc-one-sided-limits-agree

Let
$$
f(x) =
\begin{cases}
x^2 & \text{if } x < 2,\\
0 & \text{if } x = 2,\\
2x & \text{if } x > 2.
\end{cases}
$$
Find $\lim_{x \to 2^{-}} f(x)$ and $\lim_{x \to 2^{+}} f(x)$, and decide whether
$\lim_{x \to 2} f(x)$ exists.

1. **The value at $2$.** $f(2) = 0$, given by the middle line. Neither half-window contains
   $2$, so this value plays no part in either one-sided limit. The function is defined at every
   real number.
2. **From the left: scratch work.** For $x < 2$, $f(x) = x^2$, and
   $\abs{x^2 - 4} = \abs{x - 2}\,\abs{x + 2}$ by
   [property 4 of the absolute value](#rem-calc-absolute-value-properties). The factor
   $\abs{x + 2}$ changes with $x$, so we bound it on a fixed half-window: if $1 < x < 2$, then
   adding $2$ keeps the inequalities, $3 < x + 2 < 4$, so $x + 2$ is positive and
   $\abs{x + 2} = x + 2 < 4$ ([the definition of the absolute value](#def-calc-absolute-value)).
   On that half-window $\abs{x^2 - 4} < 4\abs{x - 2}$, which is less than $\eps$ when $\abs{x - 2} < \frac{\eps}{4}$. Both conditions hold if
   $\delta = \min\bigl(1, \frac{\eps}{4}\bigr)$.
3. **From the left: proof.** Let $\eps > 0$, $\delta = \min\bigl(1, \frac{\eps}{4}\bigr)$, and
   $2 - \delta < x < 2$. Since $\delta \le 1$, multiplying by ${-1}$ reverses the inequality and
   adding $2$ keeps it, so $2 - \delta \ge 1$ and $1 < x < 2$; by step 2, $\abs{x + 2} < 4$.
   Since $x < 2$, $\abs{x - 2} = 2 - x$, which is positive and less than
   $\delta \le \frac{\eps}{4}$. Multiplying $\abs{x + 2} < 4$ by the positive number
   $\abs{x - 2}$, and then $\abs{x - 2} < \frac{\eps}{4}$ by the positive number $4$, keeps
   both strict inequalities:
   $$
   \begin{aligned}
   \abs{f(x) - 4} &= \abs{x - 2}\,\abs{x + 2} \\
   &< 4\abs{x - 2} \\
   &< 4 \cdot \frac{\eps}{4} = \eps .
   \end{aligned}
   $$
   So $\lim_{x \to 2^{-}} f(x) = 4$.
4. **From the right.** For $x > 2$, $f(x) = 2x$, and $\abs{2x - 4} = 2\abs{x - 2} = 2(x - 2)$,
   by [property 4 of the absolute value](#rem-calc-absolute-value-properties) and because
   $x - 2 > 0$. Let $\eps > 0$ and $\delta = \frac{\eps}{2}$. If $2 < x < 2 + \delta$,
   then $0 < x - 2 < \frac{\eps}{2}$, and multiplying by the positive number $2$ keeps the
   inequality: $\abs{f(x) - 4} = 2(x - 2) < \eps$. So $\lim_{x \to 2^{+}} f(x) = 4$.
5. **The limit.** $f$ is defined on the open interval $\R$ around $2$, and both one-sided limits
   are $4$. By [](#thm-calc-limit-iff-one-sided), $\lim_{x \to 2} f(x) = 4$, although
   $f(2) = 0$.

$$
\boxed{
\begin{aligned}
\lim_{x \to 2^{-}} f(x) &= \lim_{x \to 2^{+}} f(x) = 4, \\
\lim_{x \to 2} f(x) &= 4
\end{aligned}
}
$$

**Check.** For $\eps = 0.4$, the left $\delta$ is $\min(1, 0.1) = 0.1$, and $x = 1.95$ gives
$\abs{1.95^2 - 4} = \abs{3.8025 - 4} = 0.1975 < 0.4$. ✓ The right $\delta$ is $0.2$, and
$x = 2.15$ gives $\abs{4.3 - 4} = 0.3 < 0.4$. ✓ Neither check used $f(2)$. ✓ On the left the
cap $\delta \le 1$ gives the bound $\abs{x + 2} < 4$; the two-sided window
$0 < \abs{x - 2} < 1$ would only give $\abs{x + 2} < 5$, as in [the quadratic ε–δ
example](#eg-calc-limit-quadratic-eps-delta). ✓
:::

:::{proof:example} The parcel price at 2 kg
:label: eg-calc-one-sided-limits-parcel

For the price $P(w)$ of Why this matters, find the one-sided limits at
$w = 2$, decide whether $\lim_{w \to 2} P(w)$ exists, and find the jump in price.

1. **The value at $2$.** $P(2) = 3$, from the first line of the price list ($0 < w \le 2$). It
   plays no part in either one-sided limit, because neither half-window contains $2$. $P$ is
   defined on the open interval $(0, 10)$, which contains $2$.
2. **From the left.** For $1 < w < 2$, $P(w) = 3$ (first line). Let $\eps > 0$ and
   $\delta = 1$. If $2 - \delta < w < 2$, that is, $1 < w < 2$, then
   $\abs{P(w) - 3} = 0 < \eps$. So $\lim_{w \to 2^{-}} P(w) = 3$. This $3$ comes from the
   prices of parcels lighter than 2 kg; that $P(2)$ is also $3$ is a coincidence of the price
   list, and the limit would be the same if the first line read $0 < w < 2$.
3. **From the right.** For $2 < w < 3$, $P(w) = 5$ (second line). Let $\eps > 0$ and
   $\delta = 1$. If $2 < w < 2 + \delta$, then $\abs{P(w) - 5} = 0 < \eps$. So
   $\lim_{w \to 2^{+}} P(w) = 5$.
4. **The limit.** The one-sided limits exist and are different, $3 \ne 5$. By point 2 of "How
   to use it" (after [](#thm-calc-limit-iff-one-sided)), $\lim_{w \to 2} P(w)$ does not exist.
5. **The jump.** $\lim_{w \to 2^{+}} P(w) - \lim_{w \to 2^{-}} P(w) = 5 - 3 = 2$: the price
   jumps by £2 at 2 kg.

$$
\boxed{
\begin{aligned}
\lim_{w \to 2^{-}} P(w) &= 3, \\
\lim_{w \to 2^{+}} P(w) &= 5, \\
\text{jump} &= 2
\end{aligned}
}
$$

**Check.** $P(1.999) = 3$ and $P(2.001) = 5$, in pounds: the prices on the two sides stay $2$
apart however close to 2 kg the weights are. ✓ The widget in
[the figure](#wdg-calc-one-sided-limits-parcel) found a $\delta$ on the right for $\eps = 0.5$, and observed none on the left, where every value
is $3$, at distance $2$ from $5$. ✓ Units: pounds throughout. ✓
:::

### An endpoint

:::{proof:example} $\lim_{x \to 0^{+}} \sqrt{x} = 0$
:label: eg-calc-one-sided-limits-sqrt

The square root is defined on $[0, \infty)$ and on no negative number
([the square-root remark](#rem-calc-square-roots)). So [the definition of the
limit](#def-calc-limit) does not apply at $0$, but part (a) of
[](#def-calc-one-sided-limit) does: $\sqrt{x}$ is defined at every point of the open interval
$(0, 1)$, and every half-window $0 < x < \delta$ lies in its domain.

**Goal.** Given $\eps > 0$, find $\delta > 0$ such that $0 < x < \delta$ implies
$\abs{\sqrt{x} - 0} < \eps$.

1. **Scratch work.** For $x > 0$, $\sqrt{x} \ge 0$, so $\abs{\sqrt{x} - 0} = \sqrt{x}$
   ([the definition of the absolute value](#def-calc-absolute-value)). Both $\sqrt{x}$ and
   $\eps$ are non-negative, so by the order part of
   [the square-root remark](#rem-calc-square-roots), $\sqrt{x} < \eps$ exactly when
   $(\sqrt{x})^2 < \eps^2$, that is, when $x < \eps^2$.
2. **Choose $\delta$.** Take $\delta = \eps^2$, which is positive.
3. **Proof.** Let $\eps > 0$ and $\delta = \eps^2$. If $0 < x < \delta$, then $\sqrt{x}$ is
   defined and $(\sqrt{x})^2 = x < \eps^2$, so $\sqrt{x} < \eps$ by step 1, and
   $\abs{\sqrt{x} - 0} = \sqrt{x} < \eps$. So $\lim_{x \to 0^{+}} \sqrt{x} = 0$.
4. **The other side.** $\sqrt{x}$ is defined at no point of any interval $(-r, 0)$, so part (b)
   of the definition does not apply: $\lim_{x \to 0^{-}} \sqrt{x}$ is not defined, and neither is
   $\lim_{x \to 0} \sqrt{x}$. [](#thm-calc-limit-iff-one-sided) does not apply either: its
   hypothesis asks for $f$ to be defined on both sides of $a$.

$$
\boxed{\delta = \eps^2}
$$

**Check.** For $\eps = 0.1$: $\delta = 0.01$, and $x = 0.0081$ gives $\sqrt{x} = 0.09 < 0.1$. ✓
The point $x = 0.01$, just outside the half-window, gives exactly $0.1$: no larger $\delta$
works, because every larger half-window contains $x = \eps^2$, where $\sqrt{x} = \eps$. ✓
:::

The jump of $\frac{\abs{x}}{x}$ at $0$, the first of the three ways a limit can fail to exist
in [The Limit of a Function](#calc-limit), fits the same pattern: its one-sided limits are
${-1}$ and $1$ (exercise [](#exr-calc-one-sided-limits-abs-over-x)), so point 2 of "How to use
it" gives again what [the jump example](#eg-calc-limit-jump) proved there with the triangle
inequality.

## Common mistakes

:::{warning} "The one-sided limit is the value at $a$"
✗ **Wrong:** "$g(0) = 0$, so $\lim_{x \to 0^{+}} g(x) = 0$", for the function $g$ after
[](#def-calc-one-sided-limit), with $g(x) = x$ for $x \le 0$ and $g(x) = x + 1$ for $x > 0$.

**Why:** the half-window $0 < x < \delta$ leaves out $x = 0$. Here $g(0)$ comes from the formula
for $x \le 0$, which says nothing about $x > 0$.

✓ **Right:** for $x > 0$, $g(x) = x + 1$, so $\lim_{x \to 0^{+}} g(x) = 1$. For a piecewise
function, find the formula that holds on the half-window, and ignore the value at $a$.
:::

:::{warning} "Both one-sided limits exist, so the limit exists"
✗ **Wrong:** "$\lim_{w \to 2^{-}} P(w) = 3$ and $\lim_{w \to 2^{+}} P(w) = 5$ both exist, so
$\lim_{w \to 2} P(w)$ exists", for the parcel price.

**Why:** [](#thm-calc-limit-iff-one-sided) asks for the two one-sided limits to be **equal**.
When they differ, the limit does not exist ([](#eg-calc-one-sided-limits-parcel)).

✓ **Right:** first find both one-sided limits, then compare them. Equal: the limit is their
common value. Different, or one missing: there is no limit.
:::

:::{warning} Writing $\lim_{x \to 0} \sqrt{x} = 0$
✗ **Wrong:** "$\sqrt{x}$ is small near $0$, so $\lim_{x \to 0} \sqrt{x} = 0$."

**Why:** [the definition of the limit](#def-calc-limit) needs $f$ to be defined on an open
interval around $0$, except possibly at $0$, and $\sqrt{x}$ is undefined for every $x < 0$.

✓ **Right:** $\lim_{x \to 0^{+}} \sqrt{x} = 0$ ([](#eg-calc-one-sided-limits-sqrt)). At an
endpoint of the domain, use the one-sided limit from the side where $f$ is defined.
:::

## Rigorous track

:::{admonition} One-sided limits in symbols, and the negation
:class: dropdown rigor
With quantifiers, $\lim_{x \to a^{+}} f(x) = L$ says
$$
\begin{aligned}
&\forall \eps > 0 \ \ \exists \delta > 0 \ \ \forall x \colon \\
&\quad a < x < a + \delta \implies \\
&\qquad x \in \dom f \\
&\qquad \text{and } \abs{f(x) - L} < \eps .
\end{aligned}
$$
Here $\dom f$ is [the domain](#def-calc-domain-range) of $f$. To negate, each $\forall$
becomes $\exists$ and each $\exists$ becomes $\forall$, the implication $P \implies Q$ becomes
"$P$ and not $Q$", and "not ($A$ and $B$)" becomes "(not $A$) or (not $B$)". So $L$ is **not**
the right-hand limit when
$$
\begin{aligned}
&\exists \eps > 0 \ \ \forall \delta > 0 \ \ \exists x \colon \\
&\quad a < x < a + \delta \ \text{ and} \\
&\qquad \bigl(x \notin \dom f \\
&\qquad\quad \text{or } \abs{f(x) - L} \ge \eps\bigr).
\end{aligned}
$$
This is the pattern of the non-example after [](#def-calc-one-sided-limit): $\eps = \frac12$,
and for each $\delta$ the point $x = \frac12 \min(\delta, 1)$. For the left-hand limit, replace
$a < x < a + \delta$ by $a - \delta < x < a$.
:::

:::{admonition} Why $f$ must be defined on one side of $a$
:class: dropdown rigor
Part (a) of [](#def-calc-one-sided-limit) asks for $f$ to be defined on an interval
$(a, a + r)$, and, in its domain clause, at every point of the half-window. The reason in
[](#rem-calc-one-sided-limit-unique) rests on that clause: it picks the point
$x = a + \frac{\delta}{2}$ of the half-window and uses $f(x)$.

Suppose the definition dropped both requirements, and only asked that "$x \in \dom f$ and
$a < x < a + \delta$ imply $\abs{f(x) - L} < \eps$". Take $f(x) = \sqrt{-x}$, which is defined
exactly for $x \le 0$, and $a = 0$. No $x$ in its domain satisfies $0 < x < \delta$, so the
condition holds for *every* $L$, and every real number would be "the right-hand limit" of
$\sqrt{-x}$ at $0$. Our definition does not apply there: $\sqrt{-x}$ is defined on no interval
$(0, r)$. It does apply from the left, where $\lim_{x \to 0^{-}} \sqrt{-x} = 0$, by the argument
of [](#eg-calc-one-sided-limits-sqrt) with $-x$ in place of $x$.
:::

## Summary

- $\lim_{x \to a^{+}} f(x) = L$ ([](#def-calc-one-sided-limit)): for every $\eps > 0$ there is a
  $\delta > 0$ such that
  $$
  \boxed{
  \begin{aligned}
  &a < x < a + \delta \\
  &\quad \implies \abs{f(x) - L} < \eps ,
  \end{aligned}
  }
  $$
  and the left-hand limit uses $a - \delta < x < a$. The value $f(a)$ and the values on the
  other side play no part.
- One-sided limits are unique ([](#rem-calc-one-sided-limit-unique)).
- $\lim_{x \to a} f(x) = L$ exactly when both one-sided limits are $L$
  ([](#thm-calc-limit-iff-one-sided)). If they differ, or one does not exist, the limit does
  not exist.
- For a piecewise function, each half-window sees one formula; the value at $a$ never matters.
- At an endpoint of the domain, such as $0$ for $\sqrt{x}$, only one one-sided limit is
  defined: $\lim_{x \to 0^{+}} \sqrt{x} = 0$.

## Exercises

::::{exercise} The jump of $\abs{x}/x$, side by side
:label: exr-calc-one-sided-limits-abs-over-x
:class: tier-a

Let $f(x) = \dfrac{\abs{x}}{x}$ for $x \ne 0$. Find (a) $\displaystyle \lim_{x \to 0^{-}} f(x)$
and (b) $\displaystyle \lim_{x \to 0^{+}} f(x)$.

:::{admonition} Hint 1
:class: dropdown hint
What is $\abs{x}$ for $x > 0$, and for $x < 0$?
:::

:::{admonition} Answer
:class: dropdown answer
(a) ${-1}$ (b) $1$
:::
::::

::::{solution} exr-calc-one-sided-limits-abs-over-x
:label: sol-calc-one-sided-limits-abs-over-x
:class: dropdown

$f$ is defined at every point of $(-1, 0)$ and of $(0, 1)$, so both parts of
[](#def-calc-one-sided-limit) apply.

(a) For $x < 0$, $\abs{x} = -x$ ([the definition of the absolute value](#def-calc-absolute-value)),
so $f(x) = \frac{-x}{x} = -1$. Given $\eps > 0$, let $\delta = 1$: if $-1 < x < 0$, then
$\abs{f(x) - (-1)} = 0 < \eps$. So $\lim_{x \to 0^{-}} f(x) = -1$.

(b) For $x > 0$, $\abs{x} = x$, so $f(x) = \frac{x}{x} = 1$, and $\delta = 1$ works in the same
way: $\lim_{x \to 0^{+}} f(x) = 1$.

The two one-sided limits differ, so by point 2 of "How to use it" (after
[](#thm-calc-limit-iff-one-sided)), $\lim_{x \to 0} f(x)$ does not exist, as
[the jump example](#eg-calc-limit-jump) proved directly from the definition. The jump is
$1 - (-1) = 2$.
::::

::::{exercise} Reading a piecewise function
:label: exr-calc-one-sided-limits-piecewise
:class: tier-a

Let $f(x) = 2x + 1$ for $x < 1$, $f(1) = 0$, and $f(x) = 4 - x$ for $x > 1$. Find
(a) $\displaystyle \lim_{x \to 1^{-}} f(x)$, (b) $\displaystyle \lim_{x \to 1^{+}} f(x)$,
(c) $f(1)$ and (d) $\displaystyle \lim_{x \to 1} f(x)$.

:::{admonition} Hint 1
:class: dropdown hint
On the half-window $1 - \delta < x < 1$, only the formula $2x + 1$ is used. Write
$\abs{(2x + 1) - L}$ as a multiple of $\abs{x - 1}$ for the right $L$.
:::

:::{admonition} Hint 2
:class: dropdown hint
For (d), compare (a) and (b), and use [](#thm-calc-limit-iff-one-sided).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $3$ (b) $3$ (c) $0$ (d) $3$
:::
::::

::::{solution} exr-calc-one-sided-limits-piecewise
:label: sol-calc-one-sided-limits-piecewise
:class: dropdown

$f$ is defined at every real number, and $f(1) = 0$ plays no part in (a), (b) or (d), because
no window contains $1$.

(a) For $x < 1$, $\abs{(2x + 1) - 3} = \abs{2x - 2} = 2\abs{x - 1}$. Given $\eps > 0$, let
$\delta = \frac{\eps}{2}$. If $1 - \delta < x < 1$, then $0 < \abs{x - 1} = 1 - x < \frac{\eps}{2}$,
and multiplying by the positive number $2$ keeps the inequality: $\abs{f(x) - 3} < \eps$. So
$\lim_{x \to 1^{-}} f(x) = 3$.

(b) For $x > 1$, $\abs{(4 - x) - 3} = \abs{1 - x} = \abs{x - 1} = x - 1$, by
[property 2 of the absolute value](#rem-calc-absolute-value-properties) and because $x - 1 > 0$. Given $\eps > 0$, let
$\delta = \eps$: if $1 < x < 1 + \eps$, then $\abs{f(x) - 3} = x - 1 < \eps$. So
$\lim_{x \to 1^{+}} f(x) = 3$.

(c) $f(1) = 0$, by the definition of $f$.

(d) Both one-sided limits are $3$, so $\lim_{x \to 1} f(x) = 3$ by
[](#thm-calc-limit-iff-one-sided), although $f(1) = 0$.
::::

::::{exercise} A square root at its endpoint
:label: exr-calc-one-sided-limits-sqrt-shift
:class: tier-a

Find the largest $\delta > 0$ such that $3 < x < 3 + \delta$ implies $\sqrt{x - 3} < 0.1$.

:::{admonition} Hint 1
:class: dropdown hint
Both $\sqrt{x - 3}$ and $0.1$ are non-negative, so you may compare their squares. Follow
[](#eg-calc-one-sided-limits-sqrt).
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{100}$
:::
::::

::::{solution} exr-calc-one-sided-limits-sqrt-shift
:label: sol-calc-one-sided-limits-sqrt-shift
:class: dropdown

For $x > 3$, $\sqrt{x - 3}$ is defined and non-negative. By the order part of
[the square-root remark](#rem-calc-square-roots), for the non-negative numbers $\sqrt{x - 3}$
and $0.1$, $\sqrt{x - 3} < 0.1$ exactly when $(\sqrt{x - 3})^2 < 0.1^2$, that is,
$x - 3 < 0.01$. So every $\delta \le 0.01$ works. A larger $\delta$ does not: its half-window
contains $x = 3.01$, where $\sqrt{x - 3} = 0.1$, which is not less than $0.1$. The largest
$\delta$ is $0.01 = \frac{1}{100}$.

This is the round $\eps = 0.1$ of $\lim_{x \to 3^{+}} \sqrt{x - 3} = 0$. Only the right-hand
limit is defined here: $\sqrt{x - 3}$ is undefined for every $x < 3$.
::::

::::{exercise} The value from one side
:label: exr-calc-one-sided-limits-claim
:class: tier-a

True or false: if $f$ is defined at every point of an open interval containing $a$ (including
$a$), and $\lim_{x \to a^{+}} f(x) = f(a)$, then $\lim_{x \to a} f(x) = f(a)$.

:::{admonition} Hint 1
:class: dropdown hint
Look for a function whose value at $a$ is given by the formula on the right of $a$, but whose
values on the left of $a$ are far from it.
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-one-sided-limits-claim
:label: sol-calc-one-sided-limits-claim
:class: dropdown

It is false. Let $H(x) = 0$ for $x < 0$ and $H(x) = 1$ for $x \ge 0$, and $a = 0$, so $H$ is
defined at every real number and $H(0) = 1$.

For $x > 0$, $H(x) = 1$, so $\abs{H(x) - 1} = 0 < \eps$ for every $\eps > 0$ (with $\delta = 1$,
say): $\lim_{x \to 0^{+}} H(x) = 1 = H(0)$. For $x < 0$, $H(x) = 0$, and in the same way
$\lim_{x \to 0^{-}} H(x) = 0$. The one-sided limits differ, so by point 2 of "How to use it"
(after [](#thm-calc-limit-iff-one-sided)), $\lim_{x \to 0} H(x)$ does not exist; in particular it
is not $H(0)$. A right-hand limit says nothing about the left of $a$.
::::

::::{exercise} The largest δ on each side
:label: exr-calc-one-sided-limits-largest-delta
:class: tier-b

Let $g(x) = x + 3$ for $x < 2$ and $g(x) = 3x - 1$ for $x \ge 2$, and let $\eps = 0.03$. Find
the largest $\delta > 0$ such that $\abs{g(x) - 5} < 0.03$ for every $x$ (a) with
$2 < x < 2 + \delta$, (b) with $2 - \delta < x < 2$, (c) with $0 < \abs{x - 2} < \delta$.

:::{admonition} Hint 1
:class: dropdown hint
On each side, write $\abs{g(x) - 5}$ as a multiple of $\abs{x - 2}$.
:::

:::{admonition} Hint 2
:class: dropdown hint
For (c), the window $0 < \abs{x - 2} < \delta$ is made of the two half-windows of (a) and (b)
([part (e) of the proposition on distance inequalities](#prop-calc-abs-interval)).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $\frac{1}{100}$ (b) $\frac{3}{100}$ (c) $\frac{1}{100}$
:::
::::

::::{solution} exr-calc-one-sided-limits-largest-delta
:label: sol-calc-one-sided-limits-largest-delta
:class: dropdown

(a) For $x > 2$, $\abs{g(x) - 5} = \abs{3x - 6} = 3(x - 2)$, because $x - 2 > 0$. Dividing by
the positive number $3$ keeps the inequality, so $3(x - 2) < 0.03$ exactly when $x - 2 < 0.01$.
So every $\delta \le 0.01$ works, and a larger one does not: its half-window contains
$x = 2.01$, where $\abs{g(x) - 5} = 0.03$. The largest is $0.01 = \frac{1}{100}$.

(b) For $x < 2$, $\abs{g(x) - 5} = \abs{x - 2} = 2 - x$, which is less than $0.03$ exactly when
$x > 1.97$. So every $\delta \le 0.03$ works, and a larger one does not: its half-window
contains $x = 1.97$, where $\abs{g(x) - 5} = 0.03$. The largest is $0.03 = \frac{3}{100}$.

(c) By [part (e) of the proposition on distance inequalities](#prop-calc-abs-interval),
$0 < \abs{x - 2} < \delta$ means $2 - \delta < x < 2$ or $2 < x < 2 + \delta$. So $\delta$ works
for the window exactly when it works for both half-windows, that is, when $\delta \le 0.01$ and
$\delta \le 0.03$. The largest is the smaller number, $\frac{1}{100}$: the choice
$\delta = \min(\delta_1, \delta_2)$ of the proof of [](#thm-calc-limit-iff-one-sided).
::::

::::{exercise} The price of parking
:label: exr-calc-one-sided-limits-parking
:class: tier-b applied

A car park charges £2 for each hour or part of an hour. For a stay of $t$ hours, with
$0 < t \le 3$, the charge in pounds is $C(t) = 2$ for $0 < t \le 1$, $C(t) = 4$ for
$1 < t \le 2$, and $C(t) = 6$ for $2 < t \le 3$. Find (a) $\displaystyle \lim_{t \to 1^{-}} C(t)$,
(b) $\displaystyle \lim_{t \to 1^{+}} C(t)$, and (c) the jump in the charge at one hour, in
pounds.

:::{admonition} Hint 1
:class: dropdown hint
On a short enough half-window on each side of $1$, $C$ is constant. Which constant?
:::

:::{admonition} Answer
:class: dropdown answer
(a) $2$ (b) $4$ (c) $2$
:::
::::

::::{solution} exr-calc-one-sided-limits-parking
:label: sol-calc-one-sided-limits-parking
:class: dropdown

$C(1) = 2$, from the first line, but it plays no part in either one-sided limit.

(a) For $0 < t < 1$, $C(t) = 2$. Given $\eps > 0$, $\delta = 1$ works: if $0 < t < 1$, then
$\abs{C(t) - 2} = 0 < \eps$. So $\lim_{t \to 1^{-}} C(t) = 2$.

(b) For $1 < t < 2$, $C(t) = 4$, and $\delta = 1$ works in the same way:
$\lim_{t \to 1^{+}} C(t) = 4$.

(c) The jump is $4 - 2 = 2$: a stay just over an hour costs £2 more than one just under. Since
the one-sided limits differ, $\lim_{t \to 1} C(t)$ does not exist, by point 2 of "How to use
it" (after [](#thm-calc-limit-iff-one-sided)).
::::

::::{exercise} Making the two sides meet
:label: exr-calc-one-sided-limits-parameter
:class: tier-b

Let $c$ be a real number, and let $f(x) = cx + 1$ for $x < 1$, $f(1) = 7$, and
$f(x) = 5 - 2x$ for $x > 1$. Find the value of $c$ for which $\lim_{x \to 1} f(x)$ exists.

:::{admonition} Hint 1
:class: dropdown hint
Find both one-sided limits at $1$. The left-hand one depends on $c$.
:::

:::{admonition} Hint 2
:class: dropdown hint
$\abs{(cx + 1) - (c + 1)} = \abs{c}\,\abs{x - 1}$. Treat $c = 0$ separately.
:::

:::{admonition} Answer
:class: dropdown answer
$2$
:::
::::

::::{solution} exr-calc-one-sided-limits-parameter
:label: sol-calc-one-sided-limits-parameter
:class: dropdown

$f$ is defined at every real number; $f(1) = 7$ plays no part.

**From the right.** For $x > 1$, $\abs{(5 - 2x) - 3} = \abs{2 - 2x} = 2\abs{x - 1}$. Given
$\eps > 0$, let $\delta = \frac{\eps}{2}$: if $1 < x < 1 + \delta$, then
$0 < \abs{x - 1} < \frac{\eps}{2}$, and multiplying by the positive number $2$ keeps the
inequality, so $\abs{f(x) - 3} < \eps$. So $\lim_{x \to 1^{+}} f(x) = 3$.

**From the left.** For $x < 1$, $\abs{(cx + 1) - (c + 1)} = \abs{c(x - 1)} = \abs{c}\,\abs{x - 1}$,
by [property 4 of the absolute value](#rem-calc-absolute-value-properties). If $c = 0$, this is
$0 < \eps$ for every $x$, and any $\delta$ works. If $c \ne 0$, then $\abs{c} > 0$; let
$\delta = \frac{\eps}{\abs{c}}$. If $1 - \delta < x < 1$, then $\abs{x - 1} < \frac{\eps}{\abs{c}}$,
and multiplying by the positive number $\abs{c}$ gives $\abs{f(x) - (c + 1)} < \eps$. Either
way, $\lim_{x \to 1^{-}} f(x) = c + 1$.

**The limit.** If $c + 1 = 3$, that is, $c = 2$, both one-sided limits are $3$, and
$\lim_{x \to 1} f(x) = 3$ by [](#thm-calc-limit-iff-one-sided). If $c \ne 2$, the one-sided
limits $c + 1$ and $3$ differ, and the limit does not exist, by point 2 of "How to use it". So
the limit exists exactly when $c = 2$.
::::

::::{exercise} Which tolerances the left side can meet
:label: exr-calc-one-sided-limits-widget-eps
:class: tier-b widget

In [the figure](#wdg-calc-one-sided-limits-parcel), the claim is that the parcel price has the
limit $5$, and on the left of $2$ the widget observes no $\delta$ for small $\eps$. Find the set
of all $\eps > 0$ for which there is a $\delta > 0$ such that $2 - \delta < w < 2$ implies
$\abs{P(w) - 5} < \eps$. Compare with what the widget reports as you move the $\eps$ slider.

:::{admonition} Hint 1
:class: dropdown hint
Compute $\abs{P(w) - 5}$ for $1 < w < 2$.
:::

:::{admonition} Answer
:class: dropdown answer set
$(2, \infty)$
:::
::::

::::{solution} exr-calc-one-sided-limits-widget-eps
:label: sol-calc-one-sided-limits-widget-eps
:class: dropdown

For $0 < w < 2$, $P(w) = 3$, so $\abs{P(w) - 5} = 2$ at every point of every half-window
$2 - \delta < w < 2$ with $\delta \le 2$.

- If $\eps > 2$, then $\delta = 1$ works, because $\abs{P(w) - 5} = 2 < \eps$ for $1 < w < 2$.
- If $0 < \eps \le 2$, no $\delta$ works: every half-window contains the point
  $w = 2 - \frac12 \min(\delta, 1)$, which lies in $(1, 2)$, and there
  $\abs{P(w) - 5} = 2 \ge \eps$.

So the set is $(2, \infty)$. On the slider, whose values are $0.1, 0.2, \ldots, 2.5$, the widget
observes no $\delta$ on the left up to $\eps = 2$ and finds one from $\eps = 2.1$ on. Since the
definition needs a $\delta$ for every $\eps > 0$, and already $\eps = 2$ has none,
$\lim_{w \to 2^{-}} P(w) \ne 5$: from the left, the limit is $3$
([](#eg-calc-one-sided-limits-parcel)).
::::

::::{exercise} The reciprocal from the right
:label: exr-calc-one-sided-limits-reciprocal
:class: tier-c rigor

True or false: there is a real number $L$ with $\displaystyle \lim_{x \to 0^{+}} \frac{1}{x} = L$.
Prove your answer from [](#def-calc-one-sided-limit).

:::{admonition} Hint 1
:class: dropdown hint
Close to $0$ on the right, $\frac{1}{x}$ is huge. Given $L$ and $\delta$, find a point $x$ of
the half-window with $\frac{1}{x} \ge \abs{L} + 2$.
:::

:::{admonition} Hint 2
:class: dropdown hint
Try $x = \min\bigl(\frac{\delta}{2}, \frac{1}{\abs{L} + 2}\bigr)$ and $\eps = 1$.
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-one-sided-limits-reciprocal
:label: sol-calc-one-sided-limits-reciprocal
:class: dropdown

It is false. The function $\frac{1}{x}$ is defined at every point of $(0, 1)$, so part (a) of
[](#def-calc-one-sided-limit) applies. Let $L$ be any real number. We show that no $\delta$ wins
the round $\eps = 1$.

Let $\delta > 0$, and let $x = \min\bigl(\frac{\delta}{2}, \frac{1}{\abs{L} + 2}\bigr)$. Both
numbers are positive, so $0 < x \le \frac{\delta}{2} < \delta$: the point $x$ is in the
half-window. Also $0 < x \le \frac{1}{\abs{L} + 2}$. Multiplying this inequality by the
positive number $\frac{\abs{L} + 2}{x}$ keeps it: $\abs{L} + 2 \le \frac{1}{x}$. By
[property 3 of the absolute value](#rem-calc-absolute-value-properties), $L \le \abs{L}$;
multiplying by ${-1}$ reverses this, $-L \ge -\abs{L}$, and adding $\frac{1}{x}$ keeps it.
Adding $-\abs{L}$ to $\abs{L} + 2 \le \frac{1}{x}$ gives $\frac{1}{x} - \abs{L} \ge 2$. So
$$
\frac{1}{x} - L \ge \frac{1}{x} - \abs{L} \ge 2 .
$$
So $\frac{1}{x} - L$ is positive and, by [the definition of the absolute
value](#def-calc-absolute-value), $\abs{\frac{1}{x} - L} = \frac{1}{x} - L \ge 2 > 1$. The
point $x$ fails the round, so no $\delta$ works for $\eps = 1$, and $L$ is not the right-hand
limit. Since $L$ was arbitrary, the right-hand limit does not exist.
::::

::::{exercise} A reciprocal from the left, with a bound
:label: exr-calc-one-sided-limits-reciprocal-left
:class: tier-c rigor

Prove from [](#def-calc-one-sided-limit) that $\displaystyle \lim_{x \to 1^{-}} \frac{1}{x} = 1$.

:::{admonition} Hint 1
:class: dropdown hint
For $x > 0$, $\frac{1}{x} - 1 = \frac{1 - x}{x}$. The numerator is controlled by $\delta$; bound
the denominator from below on a fixed half-window, such as $\frac12 < x < 1$.
:::

:::{admonition} Hint 2
:class: dropdown hint
If $\frac12 < x < 1$, then $\frac{1}{x} < 2$.
:::

:::{admonition} Answer
:class: dropdown answer manual
$\delta = \min(\frac{1}{2}, \frac{\eps}{2})$ works.
:::
::::

::::{solution} exr-calc-one-sided-limits-reciprocal-left
:label: sol-calc-one-sided-limits-reciprocal-left
:class: dropdown

The function $\frac{1}{x}$ is defined at every point of $(0, 1)$, so part (b) of
[](#def-calc-one-sided-limit) applies at $a = 1$.

**Scratch work.** For $0 < x < 1$, $\frac{1}{x} - 1 = \frac{1 - x}{x}$, a quotient of two
positive numbers, so it is positive and $\abs{\frac{1}{x} - 1} = \frac{1 - x}{x}$. If
$\frac12 < x$, multiplying by the positive number $\frac{2}{x}$ keeps the inequality:
$\frac{1}{x} < 2$. Then multiplying by the positive number $1 - x$ gives
$\frac{1 - x}{x} < 2(1 - x)$, which is less than $\eps$ when $1 - x < \frac{\eps}{2}$.

**Proof.** Let $\eps > 0$ and $\delta = \min\bigl(\frac12, \frac{\eps}{2}\bigr)$, and let
$1 - \delta < x < 1$. Since $\delta \le \frac12$, multiplying by ${-1}$ reverses the inequality
and adding $1$ keeps it, so $1 - \delta \ge \frac12$ and $\frac12 < x < 1$. Then $\frac{1}{x}$ is
defined, $\frac{1}{x} < 2$, and $0 < 1 - x < \delta \le \frac{\eps}{2}$, so, by the scratch work,
$$
\begin{aligned}
\abs{\frac{1}{x} - 1} &= \frac{1 - x}{x} < 2(1 - x) \\
&< 2 \cdot \frac{\eps}{2} = \eps ,
\end{aligned}
$$
where the last step multiplies $1 - x < \frac{\eps}{2}$ by the positive number $2$. Hence
$\lim_{x \to 1^{-}} \frac{1}{x} = 1$.

The cap $\frac12$ keeps the half-window away from $0$, where $\frac{1}{x}$ is undefined and
grows without bound ([](#exr-calc-one-sided-limits-reciprocal)).
::::

## Where this leads

:::{where-this-leads}
:::

The theorem of this page is the usual way to show that a limit does not exist: find the two
one-sided limits and compare them.
