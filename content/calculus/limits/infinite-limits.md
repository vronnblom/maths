---
title: Infinite Limits and Vertical Asymptotes
label: calc-infinite-limits
description: >-
  Functions whose values grow without bound near a point: what it means for a one-sided limit
  to be infinity or minus infinity, why such a limit does not exist as a real number, how a sign
  analysis decides between the two, and how the result locates vertical asymptotes.
tags: [limits, epsilon-delta]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 3
  est_minutes: 45
  prerequisites: [calc-one-sided-limits, calc-polynomial-rational]
  objectives:
    - Determine infinite one-sided limits via sign analysis.
    - Locate vertical asymptotes.
    - Explain why "$=\infty$" means the limit does not exist in ℝ.
  verify: verify/calculus/limits/test_infinite_limits.py
  widgets: []
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

A magnifying glass has a focal length of $10$ cm. Put a small object $u$ centimetres in front
of it. The thin-lens equation $\frac{1}{u} + \frac{1}{v} = \frac{1}{10}$ says where the lens
forms the sharp image of the object: at distance
$$
v(u) = \frac{10u}{u - 10}
$$
behind the lens, for every $u \ne 10$, in centimetres. (A negative $v$ means that the image is
on the same side as the object: the enlarged *virtual* image you see when you look through the
glass.) What happens as the object moves towards the focal point, $u = 10$?

| $u$ | $11$ | $10.1$ | $10.01$ | $9.99$ | $9.9$ |
|---|---|---|---|---|---|
| $v(u)$ | $110$ | $1010$ | $10\,010$ | ${-9990}$ | ${-990}$ |

From the right, the image runs away behind the lens: $10.01$ cm gives an image 100 metres
away. From the left, the virtual image runs away just as fast on the other side. So $v(u)$
approaches no number as $u$ approaches $10$ from either side. On the page
[The Limit of a Function](#calc-limit) such behaviour was one of the ways a limit can fail to
exist (compare [its example of unbounded values](#eg-calc-limit-unbounded), $\frac{1}{x^2}$
near $0$). But "does not exist" throws away what we see in the table: on the right the values
grow beyond every bound, and on the left they fall below every bound.

This page gives that behaviour a notation, $\lim_{u \to 10^{+}} v(u) = \infty$ and
$\lim_{u \to 10^{-}} v(u) = -\infty$, and a precise meaning. The notation does not make $\infty$
a number: we prove that such a limit does not exist as a real number. Then we find infinite
limits of rational functions by a sign analysis, and the lines they create in the graph, the
vertical asymptotes. [](#eg-calc-infinite-limits-lens) proves the two limits of the table, and
finds how close to $10$ cm the object must be for the image to be more than 10 metres away.

## Limits that are infinite

Informally, $\lim_{x \to a^{+}} f(x) = \infty$ means that $f(x)$ is as large as we like for all
$x$ close enough to $a$ and greater than $a$. The game of
[the definition of one-sided limits](#def-calc-one-sided-limit) changes in one place: instead of
a band of half-width $\eps$ around a number $L$, the challenger names a height $M$, and the
values of $f$ on the half-window must lie **above** it.

:::{figure} ./img/reciprocal-powers-asymptote.svg
:label: fig-calc-infinite-limits-reciprocal-powers
:alt: Two graphs side by side, each for x from 0 to 4, with a dashed vertical line at x = 2. Left, the graph of y = 1/(x − 2): to the right of the dashed line it rises steeply out of view as x approaches 2, and to the left of the line it falls steeply out of view. Right, the graph of y = 1/(x − 2) squared: on both sides of the dashed line it rises steeply out of view.

Left: $y = \frac{1}{x - 2}$ climbs beyond every height as $x$ approaches $2$ from the right, and
falls below every height as $x$ approaches $2$ from the left. Right: $y = \frac{1}{(x - 2)^2}$
climbs beyond every height from both sides. The dashed line $x = 2$ is a vertical asymptote of
both graphs. A drawing shows finitely many points; [](#prop-calc-reciprocal-power-limits)
proves what it suggests.
:::

:::{proof:definition} Infinite limits
:label: def-calc-infinite-limit

Let $a$ be a real number.

(a) Let $f$ be a function that is defined at every point of an open interval $(a, a + r)$, for
some $r > 0$. We say that **$f(x)$ tends to $\infty$ as $x$ approaches $a$ from the right**, and
write
$$
\lim_{x \to a^{+}} f(x) = \infty,
$$
if, whatever height $M > 0$ is named, $f(x) > M$ for all $x > a$ that are close enough to $a$.
We say that **$f(x)$ tends to $-\infty$** as $x \to a^{+}$, and write
$\lim_{x \to a^{+}} f(x) = -\infty$, if, whatever $M > 0$ is named, $f(x) < -M$ for all $x > a$
that are close enough to $a$.

(b) Let $f$ be a function that is defined at every point of an open interval $(a - r, a)$, for
some $r > 0$. The statements $\lim_{x \to a^{-}} f(x) = \infty$ and
$\lim_{x \to a^{-}} f(x) = -\infty$ say the same for all $x < a$ that are close enough to $a$.

(c) Let $f$ be a function that is defined at every point of $(a - r, a)$ and of $(a, a + r)$,
for some $r > 0$. We write $\lim_{x \to a} f(x) = \infty$ if both
$\lim_{x \to a^{-}} f(x) = \infty$ and $\lim_{x \to a^{+}} f(x) = \infty$, and
$\lim_{x \to a} f(x) = -\infty$ if both one-sided limits are $-\infty$.

These are **infinite limits**. We also write $f(x) \to \infty$ as $x \to a^{+}$, and so on.
:::

"Close enough" means the same as in [the definition of one-sided
limits](#def-calc-one-sided-limit): there is a half-window $a < x < a + \delta$ (or
$a - \delta < x < a$) on which it holds. The rigorous track states this precisely, in the
dropdown below; the proofs on this page use that version.

:::{proof:definition} Infinite limits, precisely (rigorous track)
:label: def-calc-infinite-limit-precise
:class: dropdown

Let $a$ be a real number.

(a) Let $f$ be as in part (a) of [](#def-calc-infinite-limit). Then
$\lim_{x \to a^{+}} f(x) = \infty$ means: for every $M > 0$ there is a $\delta > 0$ such that $f$
is defined at every $x$ with $a < x < a + \delta$, and
$$
\begin{aligned}
&a < x < a + \delta \\
&\quad\text{implies}\quad f(x) > M .
\end{aligned}
$$
And $\lim_{x \to a^{+}} f(x) = -\infty$ means the same with $f(x) < -M$ in place of $f(x) > M$.

(b) Let $f$ be as in part (b) of [](#def-calc-infinite-limit). The statements
$\lim_{x \to a^{-}} f(x) = \infty$ and $\lim_{x \to a^{-}} f(x) = -\infty$ mean the same as in
(a), with the half-window $a - \delta < x < a$ in place of $a < x < a + \delta$.

Part (c) of [](#def-calc-infinite-limit) is defined through (a) and (b), so it needs no
precise version of its own.
:::

**In words.** A challenger names a height $M > 0$; you reply with a half-window of width
$\delta$ next to $a$; you win the round if $f$ is defined at every $x$ of the half-window and
every such $f(x)$ is above $M$. The limit is $\infty$ when you can win *every* round. Three
points to notice:

- $\delta$ is chosen after $M$, so it may depend on $M$ (and on $a$), but not on $x$. A higher
  $M$ usually needs a narrower half-window. If a $\delta$ wins a round, so does every smaller
  $\delta > 0$, and it wins every lower height too.
- Neither half-window contains $a$. The value $f(a)$, and whether it exists, plays no part.
- "$= \infty$" is notation, not an equation between numbers: $\infty$ is not a real number,
  and there is no band around it. It says *how* $f(x)$ fails to approach a number.
  [](#prop-calc-infinite-limit-no-real-limit) below proves that it does fail.

**Example.** $\lim_{x \to 0^{+}} \frac{1}{x} = \infty$. The function $\frac{1}{x}$ is defined
at every $x \ne 0$. Given $M > 0$, take $\delta = \frac{1}{M}$, which is positive by
[property 6 of the order rules](#rem-calc-order-rules). If $0 < x < \frac{1}{M}$, then by the
same property 6 ($0 < u < v$ implies $\frac{1}{v} < \frac{1}{u}$, with $u = x$ and
$v = \frac{1}{M}$), $M = \frac{1}{1/M} < \frac{1}{x}$.

**Non-example.** $\lim_{x \to 0^{-}} \frac{1}{x}$ is not $\infty$. Take $M = 1$. For $x < 0$,
$\frac{1}{x}$ has the sign of $x$ ([part (c) of the sign rules](#prop-calc-sign-rules)), so
$\frac{1}{x} < 0 < 1$. So *every* point of every half-window $-\delta < x < 0$ fails the round
$M = 1$, and no $\delta$ wins it. (From the left, $\frac{1}{x}$ tends to $-\infty$:
[](#prop-calc-reciprocal-power-limits) below.)

An infinite limit at $a$ shows in the graph of $f$ as a vertical line that the graph climbs or
falls along without bound, as the line $x = 2$ in
[](#fig-calc-infinite-limits-reciprocal-powers).

:::{proof:definition} Vertical asymptote
:label: def-calc-vertical-asymptote

Let $a$ be a real number and $f$ a function. The line $x = a$ is a **vertical asymptote** of the
graph of $f$ if at least one of the following holds:

- $\lim_{x \to a^{+}} f(x) = \infty$ or $\lim_{x \to a^{+}} f(x) = -\infty$;
- $\lim_{x \to a^{-}} f(x) = \infty$ or $\lim_{x \to a^{-}} f(x) = -\infty$.
:::

**In words.** On at least one side of the line $x = a$, the graph of $f$ climbs beyond every
height or falls below every height as $x$ approaches $a$. One side is enough, and the two sides
may go in different directions. As with every limit, the value $f(a)$ plays no part: $f$ may be
defined at $a$ and still have the vertical asymptote $x = a$. For example,
$F(x) = \frac{1}{x} + 1$ for $x > 0$ and $F(x) = 0$ for $x \le 0$ is defined at $0$, and
$\lim_{x \to 0^{+}} F(x) = \infty$: for $x > 0$, adding $\frac{1}{x}$ to $0 < 1$ gives
$\frac{1}{x} < F(x)$ ([property 3 of the order rules](#rem-calc-order-rules)), so by
transitivity (property 2) the $\delta = \frac{1}{M}$ of the example above wins every round $M$
for $F$ too.

**Example.** The line $x = 0$ is a vertical asymptote of the graph of $\frac{1}{x}$, by the
example after [](#def-calc-infinite-limit-precise).

**Non-example.** Let $g(x) = \dfrac{x^2 - 1}{x - 1}$ for $x \ne 1$. Although $g$ is undefined at
$1$, the line $x = 1$ is not a vertical asymptote of its graph. For $x \ne 1$ we may cancel the
non-zero factor $x - 1$, so $g(x) = x + 1$. If $0 < x < 2$, adding $1$ keeps both inequalities
([property 3 of the order rules](#rem-calc-order-rules)): $1 < g(x) < 3$ for every $x \ne 1$ in
$(0, 2)$. Take $M = 3$. Every half-window $1 < x < 1 + \delta$ contains the point
$x = 1 + \frac12 \min(\delta, 1)$, which lies in $(1, 2)$, so $g(x) < 3 = M$ there: no $\delta$
wins the round $M = 3$, and $\lim_{x \to 1^{+}} g(x) \ne \infty$. At the same point
$g(x) > 1 > -3$, so $\lim_{x \to 1^{+}} g(x) \ne -\infty$ either, and the point
$x = 1 - \frac12 \min(\delta, 1)$ of the left half-window does the same from the left. A
function that stays between two numbers near $a$ has no vertical asymptote at $a$.

:::{admonition} Looking ahead
:class: looking-ahead
Here $a$ is always a real number. The page Limits at Infinity and Horizontal Asymptotes lets $x$
itself grow without bound: there $\lim_{x \to \infty} \frac{1}{x} = 0$, a *horizontal*
asymptote, and $\lim_{x \to \infty} x^2 = \infty$, an infinite limit at infinity.
:::

## Main results

### An infinite limit is not a real limit

If $f(x)$ is above every height near $a$, it cannot also stay within $1$ of a fixed number
$L$, because $L + 1$ is one of the heights.

:::{proof:proposition} An infinite limit is not a real limit
:label: prop-calc-infinite-limit-no-real-limit

Let $a$ be a real number.

(a) Let $f$ be as in part (a) of [](#def-calc-infinite-limit). If
$\lim_{x \to a^{+}} f(x) = \infty$ or $\lim_{x \to a^{+}} f(x) = -\infty$, then there is no real
number $L$ with $\lim_{x \to a^{+}} f(x) = L$: the right-hand limit of $f$ at $a$ does not exist.
The same holds for left-hand limits, with $f$ as in part (b) of [](#def-calc-infinite-limit).

(b) Let $f$ be defined at every point of $(a - r, a)$ and of $(a, a + r)$, for some $r > 0$. If
at least one of the one-sided limits of $f$ at $a$ is $\infty$ or $-\infty$, then
$\lim_{x \to a} f(x)$ does not exist. In particular, it does not exist if
$\lim_{x \to a} f(x) = \infty$ or $\lim_{x \to a} f(x) = -\infty$.
:::

:::{proof:proof}
:enumerated: false
For (a) we argue by contradiction: a real limit $L$ keeps $f(x)$ below $L + 1$ on a
half-window, an infinite limit pushes it above $\abs{L} + 1 \ge L + 1$ on another, and one point
lies in both. Part (b) then follows from the corollary on one-sided limits.

(a) First let $\lim_{x \to a^{+}} f(x) = \infty$, and suppose that also
$\lim_{x \to a^{+}} f(x) = L$ for a real number $L$. By part (a) of
[](#def-calc-one-sided-limit), with $\eps = 1$, there is a $\delta_1 > 0$ such that $f$ is
defined and $\abs{f(x) - L} < 1$ at every $x$ with $a < x < a + \delta_1$. By
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval), with $f(x)$,
$L$ and $1$ in place of $x$, $a$ and $\delta$, every such $x$ has $L - 1 < f(x) < L + 1$.

Let $M = \abs{L} + 1$. Since $\abs{L} \ge 0$
([property 1 of the absolute value](#rem-calc-absolute-value-properties)), adding $1$ gives
$M \ge 1$ ([property 3 of the order rules](#rem-calc-order-rules)), and $1 > 0$
([part (c) of the sign rules](#prop-calc-sign-rules)), so $M > 0$ by transitivity
([property 2](#rem-calc-order-rules)). By part (a) of [](#def-calc-infinite-limit-precise),
there is a $\delta_2 > 0$ such that $f(x) > M$ at every $x$ with $a < x < a + \delta_2$.

Let $\delta = \min(\delta_1, \delta_2)$, which is positive, and $x = a + \frac{\delta}{2}$.
Multiplying $0 < \delta$ by the positive number $\frac12$ keeps the inequality
([property 5(a)](#rem-calc-order-rules)), so $0 < \frac{\delta}{2}$; adding $\frac{\delta}{2}$
to both sides (property 3) gives $\frac{\delta}{2} < \delta$. Adding $a$ (property 3):
$a < x < a + \delta$. Since $\delta \le \delta_1$, adding $a$ gives $a + \delta \le a + \delta_1$,
so $a < x < a + \delta_1$ (property 2); in the same way $a < x < a + \delta_2$. So $x$ lies in
both half-windows, and
$$
\begin{aligned}
f(x) &< L + 1 \le \abs{L} + 1 \\
&= M < f(x) .
\end{aligned}
$$
Here $L \le \abs{L}$ is [property 3 of the absolute
value](#rem-calc-absolute-value-properties), and adding $1$ keeps it (property 3 of the order
rules). By transitivity (property 2), $f(x) < f(x)$, which trichotomy
([property 1](#rem-calc-order-rules)) forbids. So no such $L$ exists.

If instead $\lim_{x \to a^{+}} f(x) = -\infty$, take the same $M$ and a $\delta_2 > 0$ with
$f(x) < -M$ for $a < x < a + \delta_2$. Property 3 of the absolute value also gives
$-\abs{L} \le L$, and adding $-1$ keeps it, so at the same point $x$
$$
\begin{aligned}
-M &= -\abs{L} - 1 \le L - 1 \\
&< f(x) < -M ,
\end{aligned}
$$
and again $-M < -M$, which is impossible.

For left-hand limits, use the point $x = a - \frac{\delta}{2}$ of the half-windows
$a - \delta_1 < x < a$ and $a - \delta_2 < x < a$. Multiplying $0 < \frac{\delta}{2} < \delta$
by the negative number ${-1}$ reverses both inequalities ([property 5(c)](#rem-calc-order-rules)),
and adding $a$ keeps them: $a - \delta < x < a$. Multiplying $\delta \le \delta_1$ by ${-1}$
and adding $a$ gives $a - \delta_1 \le a - \delta$, so $x$ lies in the half-window of
$\delta_1$, and in the same way in that of $\delta_2$. The rest is unchanged.

(b) Since $r > 0$, adding $a$ and $a - r$ gives $a - r < a < a + r$ (property 3), so
$(a - r, a + r)$ is an [open interval](#def-calc-interval) containing $a$, and $f$ is defined at
every point of it except possibly at $a$: $f$ and $a$ are as in [the definition of the
limit](#def-calc-limit). By (a), the one-sided limit that is $\infty$ or $-\infty$ does not
exist. By [part (b) of the corollary on differing one-sided
limits](#cor-calc-one-sided-limits-differ), $\lim_{x \to a} f(x)$ does not exist. If
$\lim_{x \to a} f(x) = \infty$ or $-\infty$, then by part (c) of [](#def-calc-infinite-limit)
both one-sided limits are, so this applies.
:::

**In words.** "$\lim_{x \to a} f(x) = \infty$" is a precise way of saying that the limit does
**not** exist: it records the reason. The converse is false. A limit can fail to exist without
being $\infty$ or $-\infty$: at a jump, such as $\frac{\abs{x}}{x}$ at $0$, or when the two sides
go to different infinities, as $\frac{1}{x}$ does at $0$ ([](#prop-calc-reciprocal-power-limits)
below), so that $\lim_{x \to 0} \frac{1}{x}$ is neither $\infty$ nor $-\infty$, by part (c) of
[](#def-calc-infinite-limit).

### Reciprocal powers

The simplest infinite limits are those of $\frac{1}{(x - a)^n}$. Their sign depends on the side
and on whether $n$ is even or odd ([](#fig-calc-infinite-limits-reciprocal-powers)).

:::{proof:proposition} Reciprocal powers
:label: prop-calc-reciprocal-power-limits

Let $a$ be a real number and $n \ge 1$ an integer, and let $g(x) = \dfrac{1}{(x - a)^n}$ for
$x \ne a$.

(a) $\lim_{x \to a^{+}} g(x) = \infty$.

(b) If $n$ is even, $\lim_{x \to a^{-}} g(x) = \infty$, and so $\lim_{x \to a} g(x) = \infty$.

(c) If $n$ is odd, $\lim_{x \to a^{-}} g(x) = -\infty$.

For $a = 0$: as $x \to 0^{+}$, $\frac{1}{x^n}$ tends to $\infty$; as $x \to 0^{-}$, it tends to
$\infty$ if $n$ is even and to $-\infty$ if $n$ is odd.
:::

:::{proof:proof}
:enumerated: false
Let $t = \abs{x - a}$ be the distance from $x$ to $a$. For $0 < t \le 1$, the power $t^n$ is at
most $t$, so $\frac{1}{t^n} \ge \frac{1}{t}$, which is above $M$ when $t < \frac{1}{M}$: the
half-windows of width $\delta = \min\bigl(1, \frac{1}{M}\bigr)$ win the round $M$. The sign of
$(x - a)^n$ then decides between $\infty$ and $-\infty$.

**The domain.** For $x \ne a$, each of the $n$ factors of $(x - a)^n$ is non-zero, so the
product is non-zero, by [part (a) of the sign rules](#prop-calc-sign-rules) applied to one factor
after another. So $g$ is defined at every $x \ne a$, in particular at every point of
$(a - 1, a)$ and of $(a, a + 1)$.

**Step 1: powers of a number in $(0, 1]$.** Let $0 < t \le 1$. We show that $0 < t^k \le t$
for every integer $k \ge 1$. For $k = 1$ this says $0 < t \le t$. Suppose it holds for some
$k$. Then $t^{k+1} = t^k \cdot t$ is a product of two positive numbers, so it is positive
([part (c) of the sign rules](#prop-calc-sign-rules)); and multiplying $t \le 1$ by the positive
number $t^k$ gives $t^{k+1} \le t^k$ ([property 5(b) of the order rules](#rem-calc-order-rules)),
so $t^{k+1} \le t^k \le t$ by transitivity (property 2). So the claim passes from each $k$ to
$k + 1$, and therefore holds for every $k \ge 1$. (If it failed for some $k$, the set of
integers $k \ge 1$ at which it fails would be a non-empty set of positive integers, so it would
have a smallest element $k$, by [the well-ordering principle](#rem-calc-well-ordering). The claim
holds for $1$, so $k \ge 2$. Then $k - 1 \ge 1$ is smaller than the smallest failure, so the
claim holds for $k - 1$, and the step above gives it for $k$: a contradiction.)

**Step 2: the size and the sign of $(x - a)^n$.** Let $x \ne a$ and $t = \abs{x - a}$. By
[property 4 of the absolute value](#rem-calc-absolute-value-properties),
$\abs{uv} = \abs{u}\,\abs{v}$, applied to one factor after another,
$\abs{(x - a)^n} = t^n$. If $x > a$, each factor $x - a$ is positive
([part (b) of the sign rules](#prop-calc-sign-rules)), and so is the product. If $x < a$, all
$n$ factors are negative, and by [part (d) of the sign rules](#prop-calc-sign-rules) the product
is positive if $n$ is even and negative if $n$ is odd. By [the definition of the absolute
value](#def-calc-absolute-value), a positive number equals its absolute value and a negative one
equals minus its absolute value. So $(x - a)^n = t^n$ if $x > a$, or if $x < a$ and $n$ is
even, and $(x - a)^n = -t^n$ if $x < a$ and $n$ is odd.

**Step 3: the height $M$.** Let $M > 0$ and $\delta = \min\bigl(1, \frac{1}{M}\bigr)$, which is
positive, because $\frac{1}{M} > 0$ ([property 6 of the order rules](#rem-calc-order-rules)).
Let $0 < t < \delta$. Then $t < 1$, so step 1 gives $0 < t^n \le t$; and $t < \frac{1}{M}$, so
$0 < t^n < \frac{1}{M}$ (property 2). By property 6 ($0 < u < v$ implies
$\frac{1}{v} < \frac{1}{u}$), with $u = t^n$ and $v = \frac{1}{M}$,
$$
M = \frac{1}{1/M} < \frac{1}{t^n} .
$$

(a) Let $a < x < a + \delta$. Adding $-a$ (property 3) gives $0 < x - a < \delta$, so
$t = x - a$ satisfies $0 < t < \delta$. By step 2, $(x - a)^n = t^n$, so $g(x)$ is defined and,
by step 3, $g(x) = \frac{1}{t^n} > M$. So $\delta$ wins the round $M$, and since $M > 0$ was
arbitrary, $\lim_{x \to a^{+}} g(x) = \infty$ by part (a) of
[](#def-calc-infinite-limit-precise).

(b) and (c). Let $a - \delta < x < a$. Then $t = \abs{x - a} = a - x$, because $x - a < 0$
([the definition of the absolute value](#def-calc-absolute-value)). Adding $-x$ to $x < a$
gives $0 < a - x$, and adding $\delta - x$ to $a - \delta < x$ gives $a - x < \delta$
(property 3), so $0 < t < \delta$, and step 3 gives $\frac{1}{t^n} > M$.

- If $n$ is even, $(x - a)^n = t^n$ by step 2, so $g(x) = \frac{1}{t^n} > M$. So
  $\lim_{x \to a^{-}} g(x) = \infty$, by part (b) of [](#def-calc-infinite-limit-precise). With
  (a), both one-sided limits are $\infty$, and $g$ is defined on $(a - 1, a)$ and on
  $(a, a + 1)$, so $\lim_{x \to a} g(x) = \infty$ by part (c) of [](#def-calc-infinite-limit).
- If $n$ is odd, $(x - a)^n = -t^n$ by step 2, so $g(x) = -\frac{1}{t^n}$. Multiplying
  $M < \frac{1}{t^n}$ by the negative number ${-1}$ reverses it
  ([property 5(c)](#rem-calc-order-rules)): $g(x) = -\frac{1}{t^n} < -M$. So
  $\lim_{x \to a^{-}} g(x) = -\infty$.
:::

So for every $n \ge 1$ the line $x = a$ is a vertical asymptote of the graph of
$\frac{1}{(x - a)^n}$. For odd $n$ the one-sided limits are $\infty$ and $-\infty$, and
$\lim_{x \to a} \frac{1}{(x - a)^n}$ is neither, by part (c) of [](#def-calc-infinite-limit).

### Sign analysis: a factor that stays away from $0$

Near a zero $a$ of its denominator, after cancelling common factors, a rational function is a
reciprocal power $\frac{1}{(x - a)^k}$ times a factor $h(x)$ that does not vanish at $a$. If $h$ keeps one sign
and stays a fixed distance away from $0$ near $a$, it cannot stop the reciprocal power from
growing; it can only flip its sign.

:::{proof:proposition} A factor that stays away from $0$
:label: prop-calc-infinite-limit-product

Let $a$ be a real number and $r > 0$, and let $f$, $g$ and $h$ be functions that are defined at
every point of $(a, a + r)$, with $f(x) = h(x)\, g(x)$ for every $x$ in $(a, a + r)$. Suppose
that $\lim_{x \to a^{+}} g(x)$ is $\infty$ or $-\infty$.

(a) If there is a number $m > 0$ with $h(x) \ge m$ for every $x$ in $(a, a + r)$, then
$\lim_{x \to a^{+}} f(x)$ is $\infty$ if $\lim_{x \to a^{+}} g(x) = \infty$, and $-\infty$ if
$\lim_{x \to a^{+}} g(x) = -\infty$.

(b) If there is a number $m > 0$ with $h(x) \le -m$ for every $x$ in $(a, a + r)$, then
$\lim_{x \to a^{+}} f(x)$ is $-\infty$ if $\lim_{x \to a^{+}} g(x) = \infty$, and $\infty$ if
$\lim_{x \to a^{+}} g(x) = -\infty$.

(c) If $\lim_{x \to a^{+}} h(x) = L$ for a real number $L \ne 0$, then the conclusion of (a)
holds if $L > 0$, and that of (b) if $L < 0$.

The same holds for left-hand limits, with $(a - r, a)$ in place of $(a, a + r)$.
:::

:::{proof:proof}
:enumerated: false
To push $f(x) = h(x)\,g(x)$ above a height $M$, we ask $g$ for the height $\frac{M}{m}$: then
$h(x)\,g(x) \ge m\,g(x) > M$. Changing the sign of $h$ or of $g$ changes the sign of the
conclusion, and a limit $L \ne 0$ of $h$ keeps $h$ a fixed distance from $0$.

**Changing sign.** For a function $F$ defined on $(a, a + r)$, $\lim_{x \to a^{+}} F(x) = -\infty$
exactly when $\lim_{x \to a^{+}} \bigl(-F(x)\bigr) = \infty$: multiplying by the negative number
${-1}$ reverses an inequality ([property 5(c) of the order rules](#rem-calc-order-rules)), so
$F(x) < -M$ exactly when $-F(x) > M$, and the same $\delta$ wins the same rounds in
[](#def-calc-infinite-limit-precise). $(\ast)$

(a) First let $\lim_{x \to a^{+}} g(x) = \infty$, and let $M > 0$. The number $\frac{M}{m}$ is a
quotient of two positive numbers, so it is positive ([part (c) of the sign
rules](#prop-calc-sign-rules)). By part (a) of [](#def-calc-infinite-limit-precise), with the
height $\frac{M}{m}$, there is a $\delta_1 > 0$ such that $g(x) > \frac{M}{m}$ at every $x$ with
$a < x < a + \delta_1$. Let $\delta = \min(\delta_1, r)$, which is positive, and let
$a < x < a + \delta$. Since $\delta \le \delta_1$ and $\delta \le r$, adding $a$
([property 3](#rem-calc-order-rules)) and transitivity ([property 2](#rem-calc-order-rules))
give $x < a + \delta_1$ and $x < a + r$. So $x$ lies in $(a, a + r)$: $f(x)$ is defined,
$f(x) = h(x)\,g(x)$ and $h(x) \ge m$; and $g(x) > \frac{M}{m} > 0$. Multiplying $h(x) \ge m$ by
the positive number $g(x)$ gives $h(x)\,g(x) \ge m\,g(x)$ ([property 5(b)](#rem-calc-order-rules)),
and multiplying $g(x) > \frac{M}{m}$ by the positive number $m$ gives $m\,g(x) > M$
([property 5(a)](#rem-calc-order-rules)). By property 2,
$$
f(x) = h(x)\,g(x) \ge m\,g(x) > M ,
$$
so $f(x) > M$. So $\delta$ wins the round $M$, and $\lim_{x \to a^{+}} f(x) = \infty$.

Now let $\lim_{x \to a^{+}} g(x) = -\infty$. By $(\ast)$, $-g$ tends to $\infty$, so by the case
just proved $h \cdot (-g) = -f$ tends to $\infty$, and by $(\ast)$ again $f$ tends to $-\infty$.

(b) If $h(x) \le -m$, then $-h(x) \ge m$ (property 5(c)), and $f = (-h) \cdot (-g)$. If $g$
tends to $\infty$, then $-g$ tends to $-\infty$ by $(\ast)$, and (a), applied to $-h$ and $-g$,
gives $\lim_{x \to a^{+}} f(x) = -\infty$. If $g$ tends to $-\infty$, then $-g$ tends to $\infty$,
and (a) gives $\lim_{x \to a^{+}} f(x) = \infty$.

(c) Let $L > 0$. Then $\frac{L}{2} > 0$ (property 5(a)). By part (a) of
[](#def-calc-one-sided-limit), with $\eps = \frac{L}{2}$, there is a $\delta_0 > 0$ such that $h$
is defined and $\abs{h(x) - L} < \frac{L}{2}$ at every $x$ with $a < x < a + \delta_0$. By
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval), each such $x$
has $h(x) > L - \frac{L}{2} = \frac{L}{2}$. Let $r' = \min(r, \delta_0)$, which is positive. Every
$x$ in $(a, a + r')$ lies in $(a, a + r)$ and in the half-window of $\delta_0$, as in (a), so
$h(x) \ge \frac{L}{2}$ and $f(x) = h(x)\,g(x)$ there. So (a) applies with $r'$ in place of $r$ and
$m = \frac{L}{2}$. If $L < 0$, take $\eps = -\frac{L}{2}$, which is positive (property 5(c)); now
each $x$ of the half-window has $h(x) < L + \bigl(-\frac{L}{2}\bigr) = \frac{L}{2}$, so
$h(x) \le -m$ with $m = -\frac{L}{2} > 0$, and (b) applies.

For left-hand limits, use the half-windows $a - \delta < x < a$ throughout. Multiplying
$\delta \le \delta_1$ and $\delta \le r$ by ${-1}$ reverses them (property 5(c)), and adding $a$
keeps them, so $a - \delta_1 \le a - \delta < x$ and $a - r \le a - \delta < x$: $x$ lies in
$(a - r, a)$ and in the half-window of $\delta_1$. The rest is unchanged.
:::

**In words: how to find the one-sided limits of a rational function at a zero $a$ of its
denominator.**

1. **Factor** the numerator and the denominator. If the numerator is also $0$ at $a$, cancel the
   common factor $x - a$ first: for $x \ne a$ the two expressions are the same number. What is
   left may have a finite limit at $a$ ([](#eg-calc-infinite-limits-hole)).
2. **Sign.** By [the proposition on the sign of a factored rational
   function](#prop-calc-rational-sign), $f$ has one sign on the interval just to the right of $a$
   and one just to the left (up to the next number of a linear factor). These signs tell you which
   of $\infty$ and $-\infty$ to expect on each side.
3. **Split.** On a window around $a$, write $f(x) = h(x) \cdot \frac{1}{(x - a)^k}$, where $k$ is
   the number of factors $x - a$ in the denominator. This is algebra at each point $x \ne a$ of
   the window, not a statement about limits.
4. **Bound.** Choose the window so small that it contains no other number of a linear factor,
   and find an $m > 0$ with $h(x) \ge m$ (or $h(x) \le -m$) at every point of it, with
   [the order rules](#rem-calc-order-rules).
5. **Conclude** with [](#prop-calc-reciprocal-power-limits), for $\frac{1}{(x - a)^k}$, and
   [](#prop-calc-infinite-limit-product).

:::{admonition} Looking ahead
:class: looking-ahead
Step 4 avoids computing the limit of $h$ at $a$, because the limit laws, which make such
limits routine, come on the page Limit Laws, outside the prerequisites of this page. Once they
are available, $\lim_{x \to a} h(x) = h(a) \ne 0$ is immediate for a rational $h$ defined at $a$,
and part (c) of [](#prop-calc-infinite-limit-product) replaces the bound. The same laws show
that at a point where its denominator is not $0$, a rational function has a finite limit, so its
graph has no vertical asymptote there. That is why this page examines only the zeros of the
denominator.
:::

## Worked examples

### One-sided limits at a zero of the denominator

:::{proof:example} The one-sided limits of $\frac{x + 1}{x - 2}$ at $2$
:label: eg-calc-infinite-limits-simple-pole

Let $f(x) = \dfrac{x + 1}{x - 2}$ for $x \ne 2$. Find both one-sided limits of $f$ at $2$, decide
whether the line $x = 2$ is a vertical asymptote, and whether $\lim_{x \to 2} f(x)$ exists.

1. **Domain.** The denominator $x - 2$ is $0$ only at $x = 2$
   ([part (b) of the sign rules](#prop-calc-sign-rules)), so $f$ is defined at every point of
   $(1, 2)$ and of $(2, 3)$.
2. **Sign.** By [](#prop-calc-rational-sign) (with $K = 1$ and the numbers ${-1}$ and $2$), $f$
   has one sign on $(-1, 2)$ and one on $(2, \infty)$. At $x = 3$ both factors $x + 1$ and
   $x - 2$ are positive, so $f > 0$ on $(2, \infty)$; at $x = 0$ only $x - 2$ is negative, so
   $f < 0$ on $(-1, 2)$. We expect $\infty$ on the right and $-\infty$ on the left.
3. **Split.** For $x \ne 2$, $f(x) = h(x)\,g(x)$ with $h(x) = x + 1$ and
   $g(x) = \frac{1}{x - 2}$.
4. **Bound.** If $1 < x < 3$, adding $1$ keeps both inequalities
   ([property 3 of the order rules](#rem-calc-order-rules)): $2 < x + 1 < 4$. So $h(x) \ge 2$ at
   every point of $(1, 2)$ and of $(2, 3)$; take $m = 2$.
5. **From the right.** By [part (a) of the proposition on reciprocal
   powers](#prop-calc-reciprocal-power-limits), with $a = 2$ and $n = 1$,
   $\lim_{x \to 2^{+}} g(x) = \infty$. By part (a) of [](#prop-calc-infinite-limit-product), on
   $(2, 3)$, $\lim_{x \to 2^{+}} f(x) = \infty$.
6. **From the left.** By part (c) of [](#prop-calc-reciprocal-power-limits) ($n = 1$ is odd),
   $\lim_{x \to 2^{-}} g(x) = -\infty$. By the left-hand version of part (a) of
   [](#prop-calc-infinite-limit-product), on $(1, 2)$, $\lim_{x \to 2^{-}} f(x) = -\infty$.
7. **Conclusions.** The line $x = 2$ is a vertical asymptote
   ([](#def-calc-vertical-asymptote)). By part (b) of
   [](#prop-calc-infinite-limit-no-real-limit), $\lim_{x \to 2} f(x)$ does not exist; and it is
   neither $\infty$ nor $-\infty$, because the two one-sided limits differ (part (c) of
   [](#def-calc-infinite-limit)).

$$
\boxed{
\begin{aligned}
\lim_{x \to 2^{-}} \frac{x + 1}{x - 2} &= -\infty, \\
\lim_{x \to 2^{+}} \frac{x + 1}{x - 2} &= \infty
\end{aligned}
}
$$

**Check.** $f(2.001) = \frac{3.001}{0.001} = 3001$ and $f(1.999) = \frac{2.999}{-0.001} = -2999$:
large, with the signs of step 2. ✓ For $M = 1000$, the proof of
[](#prop-calc-infinite-limit-product) asks $g$ for the height $\frac{M}{m} = 500$, and the proof
of [](#prop-calc-reciprocal-power-limits) answers with $\delta = \min\bigl(1, \frac{1}{500}\bigr)
= 0.002$. The point $x = 2.0019$ of that half-window gives $f(x) = \frac{3.0019}{0.0019} \approx
1579.9 > 1000$. ✓
:::

:::{proof:example} A sign analysis at two zeros of the denominator
:label: eg-calc-infinite-limits-sign-analysis

Let $f(x) = \dfrac{x - 3}{x^3 - x^2}$. Find the one-sided limits of $f$ at each zero of its
denominator.

1. **Factor.** $x^3 - x^2 = x \cdot x \cdot (x - 1)$, which is $0$ exactly when $x = 0$ or
   $x = 1$ ([part (a) of the sign rules](#prop-calc-sign-rules)). The numerator $x - 3$ is not
   $0$ at either. So $f$ is defined at every $x \ne 0, 1$.
2. **Sign.** The numbers $0$, $1$ and $3$ of the linear factors cut $\R$ into four open
   intervals, and on each of them $f$ has one sign ([](#prop-calc-rational-sign), $K = 1$). We
   count the negative factors among $x - 3$, $x$, $x$ and $x - 1$ at one point of each:

   | Interval | point | negative factors | $f$ |
   |---|---|---|---|
   | $(-\infty, 0)$ | ${-1}$ | $4$ | $+$ |
   | $(0, 1)$ | $\frac12$ | $2$ | $+$ |
   | $(1, 3)$ | $2$ | $1$ | $-$ |
   | $(3, \infty)$ | $4$ | $0$ | $+$ |

   So we expect $\infty$ on both sides of $0$, $\infty$ on the left of $1$, and $-\infty$ on the
   right of $1$.
3. **At $0$: split and bound.** For $x \ne 0, 1$,
   $f(x) = h_0(x) \cdot \frac{1}{x^2}$ with $h_0(x) = \frac{x - 3}{x - 1} = \frac{3 - x}{1 - x}$.
   Let $-\frac12 < x < \frac12$. Multiplying by ${-1}$ reverses both inequalities
   ([property 5(c) of the order rules](#rem-calc-order-rules)), and adding $3$, or $1$, keeps
   them (property 3): $\frac52 < 3 - x < \frac72$ and $\frac12 < 1 - x < \frac32$. Since
   $0 < \frac12 < 1 - x$, the number $1 - x$ is positive (transitivity, property 2), and
   [property 6](#rem-calc-order-rules) gives $\frac{1}{1 - x} > \frac23$. Multiplying
   $3 - x > \frac52$ by the positive number $\frac{1}{1 - x}$, and then
   $\frac{1}{1 - x} > \frac23$ by the positive number $\frac52$, keeps both
   ([property 5(a)](#rem-calc-order-rules)):
   $$
   \begin{aligned}
   h_0(x) &= (3 - x) \cdot \frac{1}{1 - x} \\
   &> \frac52 \cdot \frac{1}{1 - x} \\
   &> \frac52 \cdot \frac23 = \frac53 .
   \end{aligned}
   $$
   So $h_0(x) \ge \frac53$ on $\bigl(-\frac12, 0\bigr)$ and on $\bigl(0, \frac12\bigr)$.
4. **At $0$: conclude.** By [part (b) of the proposition on reciprocal
   powers](#prop-calc-reciprocal-power-limits) ($a = 0$, $n = 2$), $\frac{1}{x^2}$ tends to
   $\infty$ from both sides. By part (a) of [](#prop-calc-infinite-limit-product) and its
   left-hand version, $f(x) \to \infty$ as $x \to 0^{+}$ and as $x \to 0^{-}$, so
   $\lim_{x \to 0} f(x) = \infty$ (part (c) of [](#def-calc-infinite-limit)).
5. **At $1$: split and bound.** For $x \ne 0, 1$, $f(x) = h_1(x) \cdot \frac{1}{x - 1}$ with
   $h_1(x) = \frac{x - 3}{x^2}$. Let $\frac12 < x < \frac32$. Adding $-3$ gives
   $x - 3 < -\frac32$ (property 3). Since $x > 0$, multiplying $x < \frac32$ by the positive
   number $x$, and then by the positive number $\frac32$, gives
   $x^2 < \frac32 x < \frac94$ (property 5(a)), and $x^2 > 0$
   ([part (c) of the sign rules](#prop-calc-sign-rules)); so $\frac{1}{x^2} > \frac49$ by
   property 6. Multiplying $x - 3 < -\frac32$ by the positive number $\frac{1}{x^2}$ keeps the
   inequality (property 5(a)), and multiplying $\frac{1}{x^2} > \frac49$ by the negative number
   $-\frac32$ reverses it (property 5(c)):
   $$
   \begin{aligned}
   h_1(x) &= (x - 3) \cdot \frac{1}{x^2} \\
   &< -\frac32 \cdot \frac{1}{x^2} \\
   &< -\frac32 \cdot \frac49 = -\frac23 .
   \end{aligned}
   $$
   So $h_1(x) \le -\frac23$ on $\bigl(\frac12, 1\bigr)$ and on $\bigl(1, \frac32\bigr)$.
6. **At $1$: conclude.** By parts (a) and (c) of [](#prop-calc-reciprocal-power-limits)
   ($a = 1$, $n = 1$), $\frac{1}{x - 1}$ tends to $\infty$ from the right and to $-\infty$ from
   the left. By part (b) of [](#prop-calc-infinite-limit-product), which flips the sign,
   $f(x) \to -\infty$ as $x \to 1^{+}$ and $f(x) \to \infty$ as $x \to 1^{-}$.

Both lines $x = 0$ and $x = 1$ are vertical asymptotes, and the signs agree with step 2.

$$
\boxed{
\begin{aligned}
\lim_{x \to 0} f(x) &= \infty, \\
\lim_{x \to 1^{-}} f(x) &= \infty, \\
\lim_{x \to 1^{+}} f(x) &= -\infty
\end{aligned}
}
$$

**Check.** $f(0.01) = \frac{-2.99}{0.000001 - 0.0001} \approx 30\,202$,
$f(0.99) = \frac{-2.01}{0.970299 - 0.9801} \approx 205.08$ and
$f(1.01) = \frac{-1.99}{1.030301 - 1.0201} \approx -195.08$. ✓ The bound of step 5 at
$x = 1.01$: $h_1(1.01) = \frac{-1.99}{1.0201} \approx -1.95 \le -\frac23$. ✓
:::

### A zero of the denominator that is not an asymptote

:::{proof:example} A hole and an asymptote: $\frac{x^2 - 1}{x^2 - 3x + 2}$
:label: eg-calc-infinite-limits-hole

Let $f(x) = \dfrac{x^2 - 1}{x^2 - 3x + 2}$. Which zeros $a$ of the denominator give a vertical
asymptote $x = a$ of its graph?

1. **Factor.** $x^2 - 1 = (x - 1)(x + 1)$ and $x^2 - 3x + 2 = (x - 1)(x - 2)$. The denominator
   is $0$ exactly at $x = 1$ and $x = 2$ ([part (a) of the sign rules](#prop-calc-sign-rules)),
   so $f$ is defined at every $x \ne 1, 2$. We examine these two zeros of the denominator.
2. **Cancel.** At every $x \ne 1, 2$ the factor $x - 1$ is not $0$, so we may cancel it:
   $$
   f(x) = \frac{x + 1}{x - 2} \qquad (x \ne 1, 2).
   $$
   This is an equation between two numbers at each such $x$, not a statement about limits.
3. **At $1$: a finite limit.** $f$ is defined at every point of the open interval $(0, 2)$
   except at $1$, so [the definition of the limit](#def-calc-limit) applies. We show
   $\lim_{x \to 1} f(x) = -2$. For $x \ne 1, 2$, by step 2,
   $$
   \begin{aligned}
   f(x) + 2 &= \frac{x + 1 + 2(x - 2)}{x - 2} \\
   &= \frac{3(x - 1)}{x - 2},
   \end{aligned}
   $$
   so $\abs{f(x) + 2} = \frac{3\abs{x - 1}}{\abs{x - 2}}$
   ([property 4 of the absolute value](#rem-calc-absolute-value-properties)). If
   $\abs{x - 1} < \frac12$, then $\frac12 < x < \frac32$
   ([part (a) of the proposition on distance inequalities](#prop-calc-abs-interval)), so
   $x - 2 < -\frac12$ (adding $-2$, property 3). Multiplying by ${-1}$ reverses this
   ([property 5(c) of the order rules](#rem-calc-order-rules)): $2 - x > \frac12$. So
   $\abs{x - 2} = 2 - x > \frac12$
   ([the definition of the absolute value](#def-calc-absolute-value)); by
   [property 6 of the order rules](#rem-calc-order-rules), $\frac{1}{\abs{x - 2}} < 2$. Let
   $\eps > 0$, $\delta = \min\bigl(\frac12, \frac{\eps}{6}\bigr)$, and
   $0 < \abs{x - 1} < \delta$. Then $x \ne 1$ and $\frac12 < x < \frac32$, so $x \ne 2$ and
   $f(x)$ is defined. Multiplying $\frac{1}{\abs{x - 2}} < 2$ by the positive number
   $3\abs{x - 1}$ keeps it ([property 5(a)](#rem-calc-order-rules)); and multiplying
   $\abs{x - 1} < \frac{\eps}{6}$ by the positive number $6$ keeps it too (property 5(a)):
   $$
   \begin{aligned}
   \abs{f(x) - (-2)} &< 6\abs{x - 1} \\
   &< 6 \cdot \frac{\eps}{6} = \eps .
   \end{aligned}
   $$
   So $\lim_{x \to 1} f(x) = -2$, and by [the theorem on a limit and its one-sided
   limits](#thm-calc-limit-iff-one-sided) both one-sided limits at $1$ are $-2$. If one of them
   were $\infty$ or $-\infty$, it would not exist, by part (a) of
   [](#prop-calc-infinite-limit-no-real-limit); but it is $-2$. So neither one-sided limit is
   infinite, and the line $x = 1$ is **not** a vertical asymptote. The graph has a *hole* at
   $(1, -2)$.
4. **At $2$: an asymptote.** For $x$ in $\bigl(\frac32, \frac52\bigr)$ with $x \ne 2$, step 2
   gives $f(x) = (x + 1) \cdot \frac{1}{x - 2}$, and adding $1$ gives $x + 1 > \frac52$
   ([property 3](#rem-calc-order-rules)). By parts (a) and (c) of
   [](#prop-calc-reciprocal-power-limits) and part (a) of
   [](#prop-calc-infinite-limit-product) with $m = \frac52$, as in
   [](#eg-calc-infinite-limits-simple-pole): $f(x) \to \infty$ as $x \to 2^{+}$ and
   $f(x) \to -\infty$ as $x \to 2^{-}$.

$$
\boxed{
\begin{aligned}
&x = 2 \text{ is a vertical asymptote,} \\
&\lim_{x \to 1} f(x) = -2
\end{aligned}
}
$$

**Check.** $f(1.001) = \frac{0.002001}{-0.000999} \approx -2.003$, close to ${-2}$. ✓
$f(2.001) = \frac{3.004001}{0.001001} \approx 3001$. ✓ For $\eps = 0.06$: $\delta = 0.01$, and
$x = 1.009$ gives $\abs{f(x) + 2} = \frac{3 \cdot 0.009}{0.991} \approx 0.0272 < 0.06$. ✓
:::

### An applied example

:::{proof:example} The image of an object near the focal point
:label: eg-calc-infinite-limits-lens

For the lens of Why this matters, $v(u) = \dfrac{10u}{u - 10}$ (in centimetres) for $u \ne 10$.
(a) Find $\lim_{u \to 10^{+}} v(u)$ and $\lim_{u \to 10^{-}} v(u)$. (b) Find the largest
$\delta > 0$ such that every object distance $u$ with $10 < u < 10 + \delta$ puts the image more
than 10 metres behind the lens.

1. **Split and bound.** For $u \ne 10$, $v(u) = 10u \cdot \frac{1}{u - 10}$. If $9 < u < 11$,
   multiplying by the positive number $10$ keeps both inequalities
   ([property 5(a) of the order rules](#rem-calc-order-rules)): $10u > 90$. So $h(u) = 10u$
   satisfies $h(u) \ge 90$ on $(9, 10)$ and on $(10, 11)$.
2. **(a)** By parts (a) and (c) of [](#prop-calc-reciprocal-power-limits) ($a = 10$, $n = 1$),
   $\frac{1}{u - 10}$ tends to $\infty$ from the right and to $-\infty$ from the left. By part
   (a) of [](#prop-calc-infinite-limit-product) and its left-hand version,
   $\lim_{u \to 10^{+}} v(u) = \infty$ and $\lim_{u \to 10^{-}} v(u) = -\infty$, as the table
   suggested.
3. **(b) Solve the inequality.** Ten metres are $1000$ cm. For $u > 10$, the number $u - 10$ is
   positive, and so is its reciprocal $\frac{1}{u - 10}$ ([property 6](#rem-calc-order-rules));
   so multiplying by either keeps an inequality (property 5(a)):
   $v(u) > 1000$ exactly when $10u > 1000(u - 10) = 1000u - 10\,000$. Adding
   $10\,000 - 10u$ to both sides (property 3), this says $10\,000 > 990u$, and multiplying by the
   positive number $\frac{1}{990}$, $u < \frac{1000}{99}$.
4. **The largest $\delta$.** So $v(u) > 1000$ at every $u$ with
   $10 < u < \frac{1000}{99}$, and $\delta = \frac{1000}{99} - 10 = \frac{10}{99}$ works. A larger
   $\delta$ does not: its half-window contains $u = \frac{1000}{99}$, where
   $v(u) = \frac{10\,000/99}{10/99} = 1000$, which is not more than $1000$.

$$
\boxed{
\begin{aligned}
\lim_{u \to 10^{+}} v(u) &= \infty, \\
\lim_{u \to 10^{-}} v(u) &= -\infty, \\
\delta &= \frac{10}{99}
\end{aligned}
}
$$

The object must be less than $\frac{10}{99} \approx 0.101$ cm, about a millimetre, beyond the
focal point.

**Check.** $u = 10.1$ lies in the half-window ($10.1 < 10.10101\ldots$), and
$v(10.1) = \frac{101}{0.1} = 1010 > 1000$. ✓ The table in Why this matters: $v(10.01) = 10\,010$
and $v(9.99) = -9990$. ✓ Units: $v$ and $u$ in centimetres, $\delta$ in centimetres. ✓
:::

## Common mistakes

:::{warning} "The limit is $\infty$, so the limit exists"
✗ **Wrong:** "$\lim_{x \to 0} \frac{1}{x^2} = \infty$, so $\frac{1}{x^2}$ has a limit at $0$."

**Why:** $\infty$ is not a real number. "$= \infty$" says that the values grow beyond every
height, and then there is no real number $L$ that is the limit
([](#prop-calc-infinite-limit-no-real-limit)).

✓ **Right:** "$\lim_{x \to 0} \frac{1}{x^2} = \infty$: the limit does not exist, and the values
grow without bound."
:::

:::{warning} Arithmetic with $\infty$
✗ **Wrong:** "$\frac{1}{x} \to \infty$ and $\frac{1}{x^2} \to \infty$ as $x \to 0^{+}$, so
$\frac{1}{x} - \frac{1}{x^2} \to \infty - \infty = 0$."

**Why:** $\infty - \infty$ is not a number, and the two terms may grow at different rates. Here
the second one wins.

✓ **Right:** combine first: $\frac{1}{x} - \frac{1}{x^2} = (x - 1) \cdot \frac{1}{x^2}$ for
$x \ne 0$. On $\bigl(0, \frac12\bigr)$, $x - 1 < -\frac12$, so part (b) of
[](#prop-calc-infinite-limit-product) and [](#prop-calc-reciprocal-power-limits) give
$\frac{1}{x} - \frac{1}{x^2} \to -\infty$ as $x \to 0^{+}$
([](#exr-calc-infinite-limits-difference) has more).
:::

:::{warning} "$\frac{3}{0} = \infty$"
✗ **Wrong:** "Substituting $x = 2$ gives $\frac{3}{0} = \infty$, so
$\lim_{x \to 2} \frac{x + 1}{x - 2} = \infty$."

**Why:** division by $0$ is not defined, so $\frac{3}{0}$ is not anything. The sign of the
denominator near $2$ matters: it is negative to the left of $2$ and positive to the right.

✓ **Right:** find the two one-sided limits separately, with a sign analysis:
$-\infty$ from the left and $\infty$ from the right ([](#eg-calc-infinite-limits-simple-pole)).
The two-sided limit is neither $\infty$ nor $-\infty$.
:::

:::{warning} "Every zero of the denominator is a vertical asymptote"
✗ **Wrong:** "$x^2 - 3x + 2$ is $0$ at $1$ and $2$, so the graph of
$\frac{x^2 - 1}{x^2 - 3x + 2}$ has the vertical asymptotes $x = 1$ and $x = 2$."

**Why:** at $x = 1$ the numerator is $0$ too. After cancelling $x - 1$, the function has the
finite limit ${-2}$ at $1$: a hole, not an asymptote ([](#eg-calc-infinite-limits-hole)).

✓ **Right:** check each zero $a$ of the denominator. Where the numerator is not $0$, bound the
cofactor and conclude as in the five steps after [](#prop-calc-infinite-limit-product). Where it
is $0$ too, cancel and look again.
:::

:::{admonition} Looking ahead
:class: looking-ahead
With the limit laws (the page Limit Laws) and part (c) of [](#prop-calc-infinite-limit-product),
the general fact becomes a theorem: after cancelling common factors, every zero of the
denominator at which the numerator is not $0$ gives a vertical asymptote.
:::

## Rigorous track

:::{admonition} Why the factor must stay away from $0$
:class: dropdown rigor
[](#prop-calc-infinite-limit-product) asks for $h(x) \ge m$ with a fixed $m > 0$, not only
$h(x) > 0$. That is needed. Let $h(x) = x^2$ and $g(x) = \frac{1}{x}$ for $0 < x < 1$. Then
$h(x) > 0$ and $\lim_{x \to 0^{+}} g(x) = \infty$, but $h(x)\,g(x) = x$ is less than $1$ at every
point of $(0, 1)$, so no $\delta$ wins the round $M = 1$ for it, and it does not tend to $\infty$.
The values of $h$ come arbitrarily close to $0$, and they beat the growth of $g$. In the same way,
part (c) needs $L \ne 0$: with $h(x) = x$, which tends to $0$, the product $h(x)\,g(x) = 1$ is
constant.
:::

:::{admonition} Unbounded is not the same as tending to $\infty$
:class: dropdown rigor
A function can take values beyond every height in every half-window, and still not tend to
$\infty$. For $x > 0$, let $k(x)$ be [the integer part](#rem-calc-integer-part) of $\frac{1}{x}$,
and let $f(x) = \frac{1}{x}$ if $k(x)$ is even and $f(x) = 0$ if $k(x)$ is odd.

Let $\delta > 0$. By [the Archimedean property](#rem-calc-naturals-unbounded) there is an
integer $n \ge 1$ with $n > \frac{1}{\delta}$, and then the even integer $2n$ and the odd
integer $2n + 1$ are both greater than $\frac{1}{\delta}$. For an integer $j > \frac{1}{\delta}$,
the point $x = \frac{1}{j}$ satisfies $0 < x < \delta$, by
[property 6 of the order rules](#rem-calc-order-rules), and $\frac{1}{x} = j$, whose integer
part is $j$ itself (as $j \le j < j + 1$). So:

- at $x = \frac{1}{2n + 1}$, $f(x) = 0 < 1$: every half-window contains a point that fails the
  round $M = 1$, and $f$ does not tend to $\infty$ as $x \to 0^{+}$;
- at $x = \frac{1}{2n}$, $f(x) = 2n$, and choosing $n$ also greater than a given $M$ makes
  $f(x) > M$: the values of $f$ in every half-window are not bounded above.

Nor does $f$ tend to $-\infty$: its values are never negative, so every point fails the round
$M = 1$. Nor does it have a real right-hand limit $L$: with $\eps = 1$, that would give a
half-window on which $f(x) < L + 1$ ([part (a) of the proposition on distance
inequalities](#prop-calc-abs-interval)), but that half-window contains points $\frac{1}{2n}$ with
$2n > L + 1$, where $f$ is $2n$. So $\lim_{x \to 0^{+}} f(x)$ fails to exist in a way
that "$= \infty$" does not describe.
:::

:::{admonition} The definition in symbols, and its negation
:class: dropdown rigor
With quantifiers, $\lim_{x \to a^{+}} f(x) = \infty$ says
$$
\begin{aligned}
&\forall M > 0 \ \ \exists \delta > 0 \ \ \forall x \colon \\
&\quad a < x < a + \delta \implies \\
&\qquad x \in \dom f \\
&\qquad \text{and } f(x) > M .
\end{aligned}
$$
To negate, each $\forall$ becomes $\exists$ and each $\exists$ becomes $\forall$, the implication
$P \implies Q$ becomes "$P$ and not $Q$", and "not $(u > v)$" becomes "$u \le v$"
([property 7 of the order rules](#rem-calc-order-rules)). So $f$ does **not** tend to $\infty$
as $x \to a^{+}$ when
$$
\begin{aligned}
&\exists M > 0 \ \ \forall \delta > 0 \ \ \exists x \colon \\
&\quad a < x < a + \delta \ \text{ and} \\
&\qquad \bigl(x \notin \dom f \\
&\qquad\quad \text{or } f(x) \le M\bigr).
\end{aligned}
$$
This is the pattern of the non-example after [](#def-calc-infinite-limit-precise) (in its
left-hand version, with the half-windows $a - \delta < x < a$), with $M = 1$, and of the function above, where the points $\frac{1}{2n + 1}$ fail the round $M = 1$.
:::

## Summary

- $\lim_{x \to a^{+}} f(x) = \infty$ ([](#def-calc-infinite-limit)): $f(x)$ is above every
  height for $x > a$ close enough to $a$. Precisely
  ([](#def-calc-infinite-limit-precise)): for every $M > 0$ there is a $\delta > 0$ such that
  $$
  \boxed{
  \begin{aligned}
  &a < x < a + \delta \\
  &\quad \implies f(x) > M ;
  \end{aligned}
  }
  $$
  for $-\infty$, $f(x) < -M$; from the left, $a - \delta < x < a$. The two-sided
  $\lim_{x \to a} f(x) = \infty$ means that both one-sided limits are $\infty$.
- "$= \infty$" is notation: the limit does not exist as a real number
  ([](#prop-calc-infinite-limit-no-real-limit)).
- $\frac{1}{(x - a)^n} \to \infty$ as $x \to a^{+}$; as $x \to a^{-}$ it tends to $\infty$ for
  even $n$ and to $-\infty$ for odd $n$ ([](#prop-calc-reciprocal-power-limits)).
- A factor that stays at least $m > 0$ away from $0$, with one sign, keeps an infinite limit
  infinite and decides its sign ([](#prop-calc-infinite-limit-product)). For a rational function
  at a zero of the denominator: factor, read the signs, bound the other factor, conclude.
- The line $x = a$ is a vertical asymptote if at least one one-sided limit at $a$ is $\infty$ or
  $-\infty$ ([](#def-calc-vertical-asymptote)). A zero of the denominator where the numerator is
  also $0$ may be a hole instead.

## Exercises

::::{exercise} Reciprocal powers
:label: exr-calc-infinite-limits-reciprocal-powers
:class: tier-a

Find (a) $\displaystyle \lim_{x \to 3^{-}} \frac{1}{x - 3}$,
(b) $\displaystyle \lim_{x \to -1^{-}} \frac{1}{(x + 1)^4}$ and
(c) $\displaystyle \lim_{x \to 0^{-}} \frac{1}{x^5}$.

:::{admonition} Hint 1
:class: dropdown hint
Write each as $\frac{1}{(x - a)^n}$. What are $a$ and $n$, and is $n$ even or odd?
:::

:::{admonition} Answer
:class: dropdown answer
(a) $-\infty$ (b) $\infty$ (c) $-\infty$
:::
::::

::::{solution} exr-calc-infinite-limits-reciprocal-powers
:label: sol-calc-infinite-limits-reciprocal-powers
:class: dropdown

All three are left-hand limits of $\frac{1}{(x - a)^n}$, so [](#prop-calc-reciprocal-power-limits)
gives them: $\infty$ for even $n$ (part (b)) and $-\infty$ for odd $n$ (part (c)).

(a) $a = 3$ and $n = 1$, which is odd: $-\infty$.

(b) $x + 1 = x - (-1)$, so $a = -1$ and $n = 4$, which is even: $\infty$.

(c) $a = 0$ and $n = 5$, which is odd: $-\infty$.

In each case the line $x = a$ is a vertical asymptote.
::::

::::{exercise} The sign of a quotient
:label: exr-calc-infinite-limits-quotient-sign
:class: tier-a

Let $f(x) = \dfrac{x - 5}{x - 3}$. Find (a) $\displaystyle \lim_{x \to 3^{-}} f(x)$ and
(b) $\displaystyle \lim_{x \to 3^{+}} f(x)$.

:::{admonition} Hint 1
:class: dropdown hint
Write $f(x) = (x - 5) \cdot \frac{1}{x - 3}$. What sign does $x - 5$ have near $3$, and how far
from $0$ does it stay on $(2, 4)$?
:::

:::{admonition} Answer
:class: dropdown answer
(a) $\infty$ (b) $-\infty$
:::
::::

::::{solution} exr-calc-infinite-limits-quotient-sign
:label: sol-calc-infinite-limits-quotient-sign
:class: dropdown

For $x \ne 3$, $f(x) = h(x) \cdot \frac{1}{x - 3}$ with $h(x) = x - 5$. If $2 < x < 4$, adding
$-5$ gives $x - 5 < -1$ ([property 3 of the order rules](#rem-calc-order-rules)), so
$h(x) \le -1$ on $(2, 3)$ and on $(3, 4)$: take $m = 1$ in part (b) of
[](#prop-calc-infinite-limit-product).

(a) By part (c) of [](#prop-calc-reciprocal-power-limits) ($a = 3$, $n = 1$),
$\frac{1}{x - 3} \to -\infty$ as $x \to 3^{-}$. A negative factor flips the sign: by the
left-hand version of part (b) of [](#prop-calc-infinite-limit-product),
$\lim_{x \to 3^{-}} f(x) = \infty$.

(b) By part (a) of [](#prop-calc-reciprocal-power-limits), $\frac{1}{x - 3} \to \infty$ as
$x \to 3^{+}$, and part (b) of [](#prop-calc-infinite-limit-product) gives
$\lim_{x \to 3^{+}} f(x) = -\infty$.

A sign chart agrees: on $(3, 5)$ the factor $x - 5$ is negative and $x - 3$ positive, so
$f < 0$; on $(-\infty, 3)$ both are negative, so $f > 0$ ([](#prop-calc-rational-sign)).
::::

::::{exercise} Locating vertical asymptotes
:label: exr-calc-infinite-limits-asymptotes
:class: tier-a

Let $f(x) = \dfrac{x + 5}{x^2 - 9}$. Find every zero $a$ of the denominator for which the line
$x = a$ is a vertical asymptote of the graph of $f$. Give them in increasing order.

:::{admonition} Hint 1
:class: dropdown hint
Factor the denominator. At each of its zeros, is the numerator $0$?
:::

:::{admonition} Hint 2
:class: dropdown hint
One infinite one-sided limit at $a$ is enough. Near $3$, write
$f(x) = \frac{x + 5}{x + 3} \cdot \frac{1}{x - 3}$, and bound the first factor on $(2, 4)$.
:::

:::{admonition} Answer
:class: dropdown answer
${-3}, 3$
:::
::::

::::{solution} exr-calc-infinite-limits-asymptotes
:label: sol-calc-infinite-limits-asymptotes
:class: dropdown

$x^2 - 9 = (x - 3)(x + 3)$, which is $0$ exactly when $x = 3$ or $x = -3$
([part (a) of the sign rules](#prop-calc-sign-rules)). The numerator is $8$ at $3$ and $2$ at
${-3}$, not $0$.

**At $3$.** For $x \ne \pm 3$, $f(x) = h(x) \cdot \frac{1}{x - 3}$ with
$h(x) = \frac{x + 5}{x + 3}$. If $3 < x < 4$, then $x + 5 > 8$ and $6 < x + 3 < 7$
([property 3 of the order rules](#rem-calc-order-rules)), so $\frac{1}{x + 3} > \frac17$
([property 6](#rem-calc-order-rules)). Multiplying $x + 5 > 8$ by the positive number
$\frac{1}{x + 3}$, and $\frac{1}{x + 3} > \frac17$ by the positive number $8$
([property 5(a)](#rem-calc-order-rules)), gives $h(x) > 8 \cdot \frac17 = \frac87$. By part (a)
of [](#prop-calc-reciprocal-power-limits) and part (a) of [](#prop-calc-infinite-limit-product)
(with $m = \frac87$ on $(3, 4)$), $\lim_{x \to 3^{+}} f(x) = \infty$. So $x = 3$ is a vertical
asymptote.

**At ${-3}$.** For $x \ne \pm 3$, $f(x) = k(x) \cdot \frac{1}{x + 3}$ with
$k(x) = \frac{x + 5}{x - 3} = -\frac{x + 5}{3 - x}$. If $-3 < x < -2$, then $2 < x + 5 < 3$ and,
multiplying by ${-1}$ (property 5(c)) and adding $3$, $5 < 3 - x < 6$; so
$\frac{1}{3 - x} > \frac16$ (property 6) and
$\frac{x + 5}{3 - x} > 2 \cdot \frac16 = \frac13$, as at $3$. Multiplying by ${-1}$,
$k(x) < -\frac13$. By part (a) of [](#prop-calc-reciprocal-power-limits) ($a = -3$) and part (b)
of [](#prop-calc-infinite-limit-product) (with $m = \frac13$ on $(-3, -2)$),
$\lim_{x \to -3^{+}} f(x) = -\infty$. So $x = -3$ is a vertical asymptote.
::::

::::{exercise} Is $\infty$ a limit?
:label: exr-calc-infinite-limits-not-a-number
:class: tier-a

True or false: if $f$ is defined at every point of $(a - r, a)$ and of $(a, a + r)$, for some
$r > 0$, and $\lim_{x \to a} f(x) = \infty$, then there is a real number $L$ with
$\lim_{x \to a} f(x) = L$.

:::{admonition} Hint 1
:class: dropdown hint
What does [](#prop-calc-infinite-limit-no-real-limit) say?
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-infinite-limits-not-a-number
:label: sol-calc-infinite-limits-not-a-number
:class: dropdown

It is false; in fact it never happens. By part (b) of
[](#prop-calc-infinite-limit-no-real-limit), if $\lim_{x \to a} f(x) = \infty$, then
$\lim_{x \to a} f(x)$ does not exist: there is no such real $L$. For example,
$\lim_{x \to 0} \frac{1}{x^2} = \infty$ (part (b) of [](#prop-calc-reciprocal-power-limits)),
and no real number is the limit of $\frac{1}{x^2}$ at $0$. The notation "$= \infty$" names the
way in which the limit fails to exist.
::::

::::{exercise} How close is close enough?
:label: exr-calc-infinite-limits-largest-delta
:class: tier-b

Find the largest $\delta > 0$ such that every $x$ with $0 < x < \delta$ has
$\dfrac{1}{x^3} > 1000$.

:::{admonition} Hint 1
:class: dropdown hint
$1000 = \frac{1}{(1/10)^3}$. Compare $x^3$ with $\bigl(\frac{1}{10}\bigr)^3$ by multiplying
inequalities between positive numbers.
:::

:::{admonition} Hint 2
:class: dropdown hint
For a larger $\delta$, look at the point $x = \frac{1}{10}$.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{10}$
:::
::::

::::{solution} exr-calc-infinite-limits-largest-delta
:label: sol-calc-infinite-limits-largest-delta
:class: dropdown

**$\delta = \frac{1}{10}$ works.** Let $0 < x < \frac{1}{10}$. Multiplying $x < \frac{1}{10}$
by the positive number $x$ gives $x^2 < \frac{x}{10}$, and multiplying it by the positive number
$\frac{1}{10}$ gives $\frac{x}{10} < \frac{1}{100}$
([property 5(a) of the order rules](#rem-calc-order-rules)); so $x^2 < \frac{1}{100}$ by
transitivity (property 2). In the same way, multiplying $x^2 < \frac{1}{100}$ by $x > 0$ and
$x < \frac{1}{10}$ by $\frac{1}{100} > 0$ gives $x^3 < \frac{x}{100} < \frac{1}{1000}$. Since
$x^3 > 0$ ([part (c) of the sign rules](#prop-calc-sign-rules)), property 6 of the order rules,
with $x^3$ and $\frac{1}{1000}$, gives $\frac{1}{x^3} > 1000$.

**No larger $\delta$ works.** If $\delta > \frac{1}{10}$, the half-window $0 < x < \delta$
contains $x = \frac{1}{10}$, where $\frac{1}{x^3} = 1000$, which is not greater than $1000$.

So the largest $\delta$ is $\frac{1}{10}$. This is one round, $M = 1000$, of
$\lim_{x \to 0^{+}} \frac{1}{x^3} = \infty$. The proof of
[](#prop-calc-reciprocal-power-limits) answers this round with the smaller
$\delta = \min\bigl(1, \frac{1}{1000}\bigr) = \frac{1}{1000}$: a proof needs *some* $\delta$
that works, not the largest one.
::::

::::{exercise} Two zeros of the denominator
:label: exr-calc-infinite-limits-two-poles
:class: tier-b

Let $f(x) = \dfrac{x - 2}{x^2 + x}$. Find (a) $\displaystyle \lim_{x \to -1^{-}} f(x)$,
(b) $\displaystyle \lim_{x \to -1^{+}} f(x)$, (c) $\displaystyle \lim_{x \to 0^{-}} f(x)$ and
(d) $\displaystyle \lim_{x \to 0^{+}} f(x)$.

:::{admonition} Hint 1
:class: dropdown hint
$x^2 + x = x(x + 1)$. Make a sign chart with the numbers ${-1}$, $0$ and $2$.
:::

:::{admonition} Hint 2
:class: dropdown hint
Near ${-1}$, write $f(x) = \frac{x - 2}{x} \cdot \frac{1}{x + 1}$ and bound the first factor on
$\bigl(-\frac32, -\frac12\bigr)$. Near $0$, write $f(x) = \frac{x - 2}{x + 1} \cdot \frac{1}{x}$
and bound the first factor on $\bigl(-\frac12, \frac12\bigr)$.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $-\infty$ (b) $\infty$ (c) $\infty$ (d) $-\infty$
:::
::::

::::{solution} exr-calc-infinite-limits-two-poles
:label: sol-calc-infinite-limits-two-poles
:class: dropdown

$x^2 + x = x(x + 1)$ is $0$ exactly at $x = 0$ and $x = -1$
([part (a) of the sign rules](#prop-calc-sign-rules)), and the numerator $x - 2$ is not $0$ at
either. We follow [](#eg-calc-infinite-limits-sign-analysis).

**Sign.** By [](#prop-calc-rational-sign), counting the negative factors among $x - 2$, $x$ and
$x + 1$: on $(-\infty, -1)$ all three are negative, so $f < 0$; on $(-1, 0)$ two are, so $f > 0$;
on $(0, 2)$ one is, so $f < 0$. So we expect (a) $-\infty$, (b) $\infty$, (c) $\infty$,
(d) $-\infty$.

**Near ${-1}$.** For $x \ne 0, -1$, $f(x) = h(x) \cdot \frac{1}{x + 1}$ with
$h(x) = \frac{x - 2}{x} = \frac{2 - x}{-x}$. Let $-\frac32 < x < -\frac12$. Multiplying by ${-1}$
reverses both inequalities ([property 5(c) of the order rules](#rem-calc-order-rules)):
$\frac12 < -x < \frac32$, and adding $2$ (property 3), $\frac52 < 2 - x < \frac72$. By
property 6, $\frac{1}{-x} > \frac23$. Multiplying $2 - x > \frac52$ by the positive number
$\frac{1}{-x}$, and $\frac{1}{-x} > \frac23$ by the positive number $\frac52$ (property 5(a)),
gives $h(x) > \frac53$. With $\frac{1}{x + 1} \to \infty$ as $x \to -1^{+}$ and $-\infty$ as
$x \to -1^{-}$ ([](#prop-calc-reciprocal-power-limits), $n = 1$), part (a) of
[](#prop-calc-infinite-limit-product) and its left-hand version give (a) $-\infty$ and
(b) $\infty$.

**Near $0$.** For $x \ne 0, -1$, $f(x) = k(x) \cdot \frac{1}{x}$ with
$k(x) = \frac{x - 2}{x + 1}$. Let $-\frac12 < x < \frac12$. Adding $-2$ and $1$ (property 3):
$x - 2 < -\frac32$ and $\frac12 < x + 1 < \frac32$, so $\frac{1}{x + 1} > \frac23$
(property 6). Multiplying $x - 2 < -\frac32$ by the positive number $\frac{1}{x + 1}$ keeps it,
and multiplying $\frac{1}{x + 1} > \frac23$ by the negative number $-\frac32$ reverses it
(property 5(c)): $k(x) < -\frac32 \cdot \frac{1}{x + 1} < -\frac32 \cdot \frac23 = -1$. With
$\frac{1}{x} \to -\infty$ as $x \to 0^{-}$ and $\infty$ as $x \to 0^{+}$, part (b) of
[](#prop-calc-infinite-limit-product), which flips the sign, gives (c) $\infty$ and
(d) $-\infty$.

All four agree with the sign chart. Both lines $x = -1$ and $x = 0$ are vertical asymptotes.
::::

::::{exercise} Cancel first
:label: exr-calc-infinite-limits-hole
:class: tier-b

Let $f(x) = \dfrac{x^2 - 4}{x^2 - x - 2}$. Find every zero $a$ of the denominator for which the
line $x = a$ is a vertical asymptote of the graph of $f$.

:::{admonition} Hint 1
:class: dropdown hint
Both the numerator and the denominator are $0$ at one of the zeros of the denominator. Cancel
the common factor, and follow [](#eg-calc-infinite-limits-hole).
:::

:::{admonition} Hint 2
:class: dropdown hint
At the hole, show from [the definition of the limit](#def-calc-limit) that the limit is finite.
If $\abs{x - 2} < 1$, how small can $\abs{x + 1}$ be?
:::

:::{admonition} Answer
:class: dropdown answer
${-1}$
:::
::::

::::{solution} exr-calc-infinite-limits-hole
:label: sol-calc-infinite-limits-hole
:class: dropdown

**Factor.** $x^2 - 4 = (x - 2)(x + 2)$ and $x^2 - x - 2 = (x - 2)(x + 1)$. The denominator is $0$
exactly at $x = 2$ and $x = -1$ ([part (a) of the sign rules](#prop-calc-sign-rules)). At every
$x \ne 2, -1$ we may cancel the non-zero factor $x - 2$: $f(x) = \frac{x + 2}{x + 1}$.

**At ${-1}$: an asymptote.** For $x \ne 2, -1$, $f(x) = (x + 2) \cdot \frac{1}{x + 1}$. If
$-\frac32 < x < -\frac12$, adding $2$ gives $x + 2 > \frac12$
([property 3 of the order rules](#rem-calc-order-rules)). By part (a) of
[](#prop-calc-reciprocal-power-limits) ($a = -1$, $n = 1$) and part (a) of
[](#prop-calc-infinite-limit-product) with $m = \frac12$ on $\bigl(-1, -\frac12\bigr)$,
$\lim_{x \to -1^{+}} f(x) = \infty$. So $x = -1$ is a vertical asymptote.

**At $2$: a finite limit.** $f$ is defined at every point of $(1, 3)$ except $2$. For
$x \ne 2, -1$,
$$
\begin{aligned}
f(x) - \frac43 &= \frac{3(x + 2) - 4(x + 1)}{3(x + 1)} \\
&= \frac{2 - x}{3(x + 1)},
\end{aligned}
$$
so $\abs{f(x) - \frac43} = \frac{\abs{x - 2}}{3\abs{x + 1}}$, by
[properties 2 and 4 of the absolute value](#rem-calc-absolute-value-properties). If
$\abs{x - 2} < 1$, then $1 < x < 3$
([part (a) of the proposition on distance inequalities](#prop-calc-abs-interval)), so
$x + 1 > 2$ (adding $1$, [property 3 of the order rules](#rem-calc-order-rules)) and
$\abs{x + 1} = x + 1$ ([the definition of the absolute value](#def-calc-absolute-value)).
Multiplying $x + 1 > 2$ by the positive number $3$ keeps it (property 5(a)), so
$3\abs{x + 1} > 6$, and property 6 gives $\frac{1}{3\abs{x + 1}} < \frac16$. Let $\eps > 0$,
$\delta = \min(1, 6\eps)$ and $0 < \abs{x - 2} < \delta$. Then $f(x)$ is defined, and
multiplying $\frac{1}{3\abs{x + 1}} < \frac16$ by the positive number $\abs{x - 2}$ keeps it
(property 5(a)):
$$
\abs{f(x) - \tfrac43} < \frac{\abs{x - 2}}{6} < \frac{6\eps}{6} = \eps .
$$
So $\lim_{x \to 2} f(x) = \frac43$. By [the theorem on a limit and its one-sided
limits](#thm-calc-limit-iff-one-sided), both one-sided limits at $2$ are $\frac43$, so by part
(a) of [](#prop-calc-infinite-limit-no-real-limit) neither is $\infty$ or $-\infty$. The line
$x = 2$ is not a vertical asymptote; the graph has a hole at $\bigl(2, \frac43\bigr)$.

So only the zero ${-1}$ of the denominator gives a vertical asymptote.
::::

::::{exercise} The cost of a cleaner river
:label: exr-calc-infinite-limits-pollution
:class: tier-b applied

A town estimates that removing $p$ per cent of the pollution from its river costs
$C(p) = \dfrac{50p}{100 - p}$ thousand pounds, for $0 \le p < 100$. (a) Find
$\displaystyle \lim_{p \to 100^{-}} C(p)$. (b) Find the largest $\delta > 0$ such that every $p$
with $100 - \delta < p < 100$ has a cost of more than $4950$ thousand pounds.

:::{admonition} Hint 1
:class: dropdown hint
$\frac{1}{100 - p} = -\frac{1}{p - 100}$. What does $\frac{1}{p - 100}$ do as $p \to 100^{-}$,
and what sign does $-50p$ have near $100$?
:::

:::{admonition} Hint 2
:class: dropdown hint
For $p < 100$, the number $100 - p$ is positive, so you may multiply the inequality
$C(p) > 4950$ by it.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $\infty$ (b) $1$
:::
::::

::::{solution} exr-calc-infinite-limits-pollution
:label: sol-calc-infinite-limits-pollution
:class: dropdown

(a) For $p \ne 100$, $C(p) = (-50p) \cdot \frac{1}{p - 100}$. If $99 < p < 100$, multiplying
$p > 99$ by the negative number ${-50}$ reverses it
([property 5(c) of the order rules](#rem-calc-order-rules)): $-50p < -4950$. So $h(p) = -50p$
satisfies $h(p) \le -4950$ on $(99, 100)$. By part (c) of
[](#prop-calc-reciprocal-power-limits) ($a = 100$, $n = 1$), $\frac{1}{p - 100} \to -\infty$ as
$p \to 100^{-}$, and by the left-hand version of part (b) of
[](#prop-calc-infinite-limit-product), with $m = 4950$, $\lim_{p \to 100^{-}} C(p) = \infty$.
Removing nearly all the pollution costs more than any budget.

(b) For $p < 100$, $100 - p > 0$, so multiplying by it, or by its reciprocal, keeps an
inequality (property 5(a)): $C(p) > 4950$ exactly when $50p > 4950(100 - p) = 495\,000 - 4950p$.
Adding $4950p$ (property 3), this says $5000p > 495\,000$, and multiplying by the positive
number $\frac{1}{5000}$, $p > 99$. So $\delta = 1$ works: every $p$ with $99 < p < 100$ costs
more than $4950$ thousand pounds. A larger $\delta$ does not: its half-window contains $p = 99$,
where $C(99) = \frac{4950}{1} = 4950$, which is not more than $4950$. The largest $\delta$ is
$1$: removing more than $99$ per cent costs more than £4.95 million.
::::

::::{exercise} Infinity minus infinity
:label: exr-calc-infinite-limits-difference
:class: tier-b

True or false: if $f$ and $g$ are defined at every point of $(a, a + r)$, for some $r > 0$, and
$\lim_{x \to a^{+}} f(x) = \infty$ and $\lim_{x \to a^{+}} g(x) = \infty$, then
$\lim_{x \to a^{+}} \bigl(f(x) - g(x)\bigr) = 0$.

:::{admonition} Hint 1
:class: dropdown hint
Try $g(x) = \frac{1}{x}$ at $a = 0$, and $f(x) = g(x) + 1$.
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-infinite-limits-difference
:label: sol-calc-infinite-limits-difference
:class: dropdown

It is false. Let $a = 0$, $g(x) = \frac{1}{x}$ and $f(x) = \frac{1}{x} + 1$ for $x > 0$.

- $\lim_{x \to 0^{+}} g(x) = \infty$, by part (a) of [](#prop-calc-reciprocal-power-limits).
- For $x > 0$, $f(x) = (1 + x) \cdot \frac{1}{x}$, and on $(0, 1)$, $1 + x > 1$
  ([property 3 of the order rules](#rem-calc-order-rules)). By part (a) of
  [](#prop-calc-infinite-limit-product) with $m = 1$, $\lim_{x \to 0^{+}} f(x) = \infty$.
- But $f(x) - g(x) = 1$ for every $x > 0$. For $\eps = \frac12$, every point $x$ of every
  half-window has $\abs{f(x) - g(x) - 0} = 1 \ge \frac12$, so $0$ is not the right-hand limit of
  $f - g$. (The right-hand limit is $1$: every $\delta$ works, because
  $\abs{1 - 1} = 0 < \eps$.)

Other choices give other answers: $f(x) = \frac{2}{x}$ gives $f(x) - g(x) = \frac{1}{x} \to \infty$,
and $f(x) = \frac{1}{x}$, $g(x) = \frac{1}{x^2}$ give $-\infty$ (Common mistakes, "Arithmetic
with $\infty$"). That is why "$\infty - \infty$" has no value. The function
$F(x) = \frac{1}{x} + 1$ for $x > 0$ and $F(x) = 0$ for $x \le 0$ also shows that a vertical
asymptote can sit where the function is defined: $F(0) = 0$, yet $x = 0$ is a vertical
asymptote of its graph, because $F(x) = (1 + x) \cdot \frac{1}{x}$ on $(0, 1)$, so
$\lim_{x \to 0^{+}} F(x) = \infty$ by the same argument as for $f$.
::::

::::{exercise} Straight from the definition
:label: exr-calc-infinite-limits-from-definition
:class: tier-c rigor

Prove from [the precise definition](#def-calc-infinite-limit-precise), without using the
propositions of this page, that $\displaystyle \lim_{x \to 1^{+}} \frac{x}{x - 1} = \infty$.

:::{admonition} Hint 1
:class: dropdown hint
For $x > 1$, $\frac{x}{x - 1} = x \cdot \frac{1}{x - 1}$, and $x > 1$. When is
$\frac{1}{x - 1} > M$?
:::

:::{admonition} Answer
:class: dropdown answer manual
$\delta = \frac{1}{M}$ works.
:::
::::

::::{solution} exr-calc-infinite-limits-from-definition
:label: sol-calc-infinite-limits-from-definition
:class: dropdown

The function $\frac{x}{x - 1}$ is defined at every $x \ne 1$, so at every point of $(1, 2)$, and
part (a) of [](#def-calc-infinite-limit) applies.

**Scratch work.** For $x > 1$, $x - 1 > 0$. If $x - 1 < \frac{1}{M}$, then
$\frac{1}{x - 1} > M$ ([property 6 of the order rules](#rem-calc-order-rules)), and the factor
$x > 1$ can only help.

**Proof.** Let $M > 0$ and $\delta = \frac{1}{M}$, which is positive (property 6). Let
$1 < x < 1 + \delta$. Adding $-1$ (property 3) gives $0 < x - 1 < \frac{1}{M}$, so $x \ne 1$,
the function is defined at $x$, and by property 6 ($0 < a < b$ implies
$\frac{1}{b} < \frac{1}{a}$, with $a = x - 1$ and $b = \frac{1}{M}$), $\frac{1}{x - 1} > M$. In
particular $\frac{1}{x - 1}$ is positive (property 2, as $M > 0$). Multiplying $x > 1$ by the
positive number $\frac{1}{x - 1}$ keeps it ([property 5(a)](#rem-calc-order-rules)):
$$
\frac{x}{x - 1} = x \cdot \frac{1}{x - 1} > \frac{1}{x - 1} > M .
$$
By transitivity (property 2), $\frac{x}{x - 1} > M$. So $\delta$ wins the round $M$, and since
$M > 0$ was arbitrary, $\lim_{x \to 1^{+}} \frac{x}{x - 1} = \infty$.
::::

::::{exercise} The reciprocal of an infinite limit
:label: exr-calc-infinite-limits-reciprocal
:class: tier-c rigor

Let $f$ be defined at every point of $(a, a + r)$, for some $r > 0$, with
$\lim_{x \to a^{+}} f(x) = \infty$. Prove that there is an $s > 0$ such that $f(x) > 0$ for every
$x$ in $(a, a + s)$, and that $\displaystyle \lim_{x \to a^{+}} \frac{1}{f(x)} = 0$.

:::{admonition} Hint 1
:class: dropdown hint
For the first part, play one round of [](#def-calc-infinite-limit-precise), with $M = 1$.
:::

:::{admonition} Hint 2
:class: dropdown hint
Given $\eps > 0$, which height $M$ makes $f(x) > M$ imply $\frac{1}{f(x)} < \eps$?
:::

:::{admonition} Answer
:class: dropdown answer manual
Given $\eps > 0$, a $\delta$ that wins the round $M = \frac{1}{\eps}$ works.
:::
::::

::::{solution} exr-calc-infinite-limits-reciprocal
:label: sol-calc-infinite-limits-reciprocal
:class: dropdown

**$f$ is positive near $a$.** By part (a) of [](#def-calc-infinite-limit-precise) with $M = 1$,
there is an $s > 0$ such that $f$ is defined and $f(x) > 1$ at every $x$ with $a < x < a + s$.
Since $1 > 0$ ([part (c) of the sign rules](#prop-calc-sign-rules)), $f(x) > 0$ there
([property 2 of the order rules](#rem-calc-order-rules)). So $\frac{1}{f}$ is defined at every
point of $(a, a + s)$, and part (a) of [](#def-calc-one-sided-limit) applies to it.

**The limit.** Let $\eps > 0$. The number $\frac{1}{\eps}$ is positive
([property 6](#rem-calc-order-rules)), so there is a $\delta_1 > 0$ such that $f(x) > \frac{1}{\eps}$
at every $x$ with $a < x < a + \delta_1$. Let $\delta = \min(\delta_1, s)$, which is positive, and
let $a < x < a + \delta$. Since $\delta \le \delta_1$ and $\delta \le s$, adding $a$
(property 3) and transitivity give $x < a + \delta_1$ and $x < a + s$. So $\frac{1}{f(x)}$ is
defined and $0 < \frac{1}{\eps} < f(x)$. By property 6 ($0 < u < v$ implies
$\frac{1}{v} < \frac{1}{u}$, with $u = \frac{1}{\eps}$ and $v = f(x)$),
$\frac{1}{f(x)} < \frac{1}{1/\eps} = \eps$; and $\frac{1}{f(x)} > 0$ (property 6), so
$\abs{\frac{1}{f(x)} - 0} = \frac{1}{f(x)} < \eps$ ([the definition of the absolute
value](#def-calc-absolute-value)). So $\delta$ wins the round $\eps$, and since $\eps > 0$ was
arbitrary, $\lim_{x \to a^{+}} \frac{1}{f(x)} = 0$.

The converse fails: $\frac{1}{g(x)} \to 0$ does not make $g(x) \to \infty$. For
$g(x) = -\frac{1}{x}$, $\frac{1}{g(x)} = -x \to 0$ as $x \to 0^{+}$, but $g(x) \to -\infty$ (part
(b) of [](#prop-calc-infinite-limit-product), with $h(x) = -1$).
::::

::::{exercise} One asymptote or two?
:label: exr-calc-infinite-limits-parameter
:class: tier-c

Let $c$ be a real number and $f(x) = \dfrac{x - c}{x^2 - 4x + 3}$. Find every $c$ for which
exactly one of the two zeros of the denominator gives a vertical asymptote of the graph of $f$.
Give them in increasing order.

:::{admonition} Hint 1
:class: dropdown hint
$x^2 - 4x + 3 = (x - 1)(x - 3)$. For which $c$ is the numerator $0$ at one of these zeros?
:::

:::{admonition} Hint 2
:class: dropdown hint
Write $f(x) = (x - c) \cdot g(x)$ with $g(x) = \frac{1}{(x - 1)(x - 3)}$. Find the one-sided limits
of $g$ first, and of $x - c$ (from the definition). Then use part (c) of
[](#prop-calc-infinite-limit-product).
:::

:::{admonition} Answer
:class: dropdown answer
$1, 3$
:::
::::

::::{solution} exr-calc-infinite-limits-parameter
:label: sol-calc-infinite-limits-parameter
:class: dropdown

The denominator $(x - 1)(x - 3)$ is $0$ exactly at $1$ and $3$
([part (a) of the sign rules](#prop-calc-sign-rules)). Let $g(x) = \frac{1}{(x - 1)(x - 3)}$ for $x \ne 1, 3$; then
$f(x) = (x - c)\, g(x)$ at every such $x$.

**The one-sided limits of $g$ at $1$.** On $\bigl(\frac12, \frac32\bigr)$, $g(x) =
\frac{1}{x - 3} \cdot \frac{1}{x - 1}$ for $x \ne 1$. There $\frac32 < 3 - x < \frac52$
(multiplying by ${-1}$ and adding $3$, [properties 5(c) and 3 of the order
rules](#rem-calc-order-rules)), so $\frac{1}{3 - x} > \frac25$ (property 6) and, multiplying by
${-1}$, $\frac{1}{x - 3} < -\frac25$. With [](#prop-calc-reciprocal-power-limits) ($n = 1$) and
part (b) of [](#prop-calc-infinite-limit-product) ($m = \frac25$): $g(x) \to -\infty$ as
$x \to 1^{+}$ and $g(x) \to \infty$ as $x \to 1^{-}$.

**The one-sided limits of $g$ at $3$.** On $\bigl(\frac52, \frac72\bigr)$,
$g(x) = \frac{1}{x - 1} \cdot \frac{1}{x - 3}$ for $x \ne 3$, and $\frac32 < x - 1 < \frac52$, so
$\frac{1}{x - 1} > \frac25$. By part (a) of [](#prop-calc-infinite-limit-product):
$g(x) \to \infty$ as $x \to 3^{+}$ and $g(x) \to -\infty$ as $x \to 3^{-}$.

**If $c \ne 1$, then $x = 1$ is an asymptote.** For every real $b$, $\lim_{x \to b} (x - c) = b - c$,
since $\abs{(x - c) - (b - c)} = \abs{x - b}$ and $\delta = \eps$ works; by [the theorem on a
limit and its one-sided limits](#thm-calc-limit-iff-one-sided), both one-sided limits are
$b - c$ too. With $b = 1$, the limit $1 - c$ is not $0$, so part (c) of
[](#prop-calc-infinite-limit-product) (on $\bigl(1, \frac32\bigr)$, with $h(x) = x - c$) shows
that $\lim_{x \to 1^{+}} f(x)$ is $\infty$ or $-\infty$. In the same way, if $c \ne 3$, then
$x = 3$ is an asymptote. So for $c \ne 1, 3$ there are two.

**If $c = 1$.** Then $x = 3$ is an asymptote, as $c \ne 3$. At every $x \ne 1, 3$ we may cancel
$x - 1$: $f(x) = \frac{1}{x - 3}$. We show $\lim_{x \to 1} f(x) = -\frac12$. For $x \ne 1, 3$,
$f(x) + \frac12 = \frac{x - 1}{2(x - 3)}$, so
$\abs{f(x) + \frac12} = \frac{\abs{x - 1}}{2\abs{x - 3}}$
([property 4 of the absolute value](#rem-calc-absolute-value-properties)). If
$\abs{x - 1} < 1$, then $0 < x < 2$
([part (a) of the proposition on distance inequalities](#prop-calc-abs-interval)). Multiplying
$x < 2$ by ${-1}$ reverses it ([property 5(c) of the order rules](#rem-calc-order-rules)), and
adding $3$ keeps it (property 3), so $3 - x > 1$. So $x - 3 < 0$ and $\abs{x - 3} = 3 - x$
([the definition of the absolute value](#def-calc-absolute-value)); multiplying $3 - x > 1$ by
the positive number $2$ keeps it (property 5(a)), and property 6 gives
$\frac{1}{2\abs{x - 3}} < \frac12$. For $\eps > 0$,
$\delta = \min(1, 2\eps)$ and $0 < \abs{x - 1} < \delta$, $f(x)$ is defined and
$\abs{f(x) + \frac12} < \frac{\abs{x - 1}}{2} < \eps$. So both one-sided limits at $1$ are the
real number $-\frac12$ (by [the theorem](#thm-calc-limit-iff-one-sided)), neither is infinite (part
(a) of [](#prop-calc-infinite-limit-no-real-limit)), and $x = 1$ is not an asymptote: exactly
one asymptote.

**If $c = 3$.** In the same way, $x = 1$ is an asymptote, and for $x \ne 1, 3$,
$f(x) = \frac{1}{x - 1}$ and $f(x) - \frac12 = \frac{3 - x}{2(x - 1)}$, so
$\abs{f(x) - \frac12} = \frac{\abs{x - 3}}{2\abs{x - 1}}$ ([properties 4 and 2 of the absolute
value](#rem-calc-absolute-value-properties), as $\abs{3 - x} = \abs{-(x - 3)} = \abs{x - 3}$). If
$\abs{x - 3} < 1$, then $2 < x < 4$ and $\abs{x - 1} = x - 1 > 1$, so $\delta = \min(1, 2\eps)$
works again: $\lim_{x \to 3} f(x) = \frac12$, and $x = 3$ is not an asymptote. Exactly one
asymptote.

So exactly one of the two zeros gives a vertical asymptote when $c = 1$ or $c = 3$.
::::

## Where this leads

:::{where-this-leads}
:::

Infinite limits at a point describe the vertical lines of a graph. The next page of the chapter
lets $x$ itself grow without bound, which gives the horizontal ones.
