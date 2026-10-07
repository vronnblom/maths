---
title: Absolute Value and Inequalities
label: calc-absolute-value-inequalities
description: >-
  The absolute value as a distance, how to turn statements about distance into intervals,
  how to solve linear, quadratic and absolute-value inequalities, and the triangle inequality.
tags: [preliminaries, inequalities]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 2
  est_minutes: 25
  prerequisites: [calc-real-numbers]
  objectives:
    - Solve linear, quadratic and absolute-value inequalities.
    - Translate $\lvert x-a\rvert<\delta$ into an interval.
    - Apply the triangle inequality.
  verify: verify/calculus/preliminaries/test_absolute_value_and_inequalities.py
  widgets: []
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

A bolt is specified as $20$ mm long, with a tolerance of $0.05$ mm. Which lengths are
acceptable? A length $x$ (in mm) is acceptable when its distance from $20$ is at most $0.05$.
We write that distance as $\abs{x - 20}$, so the condition is $\abs{x - 20} \le 0.05$, and
this is the same as $19.95 \le x \le 20.05$.

Calculus is full of statements of this kind: "$x$ is close to $a$", "$f(x)$ is within a
tolerance of $L$". The absolute value turns "close" into an inequality, and the rules of this
page turn that inequality into an interval that you can draw on the number line. The precise
definition of a limit, in the Limits chapter, is written entirely in this language.

## Absolute value as distance

% TODO link: calc-real-numbers once calc-real-numbers is merged
We use the interval notation of the page Real Numbers and Intervals throughout.

:::{proof:definition} Absolute value
:label: def-calc-absolute-value

The **absolute value** of a real number $x$ is
$$
\abs{x} :=
\begin{cases}
x & \text{if } x \ge 0,\\
-x & \text{if } x < 0.
\end{cases}
$$
For real numbers $x$ and $a$, the number $\abs{x - a}$ is called the **distance** between $x$
and $a$.
:::

**In words.** $\abs{x}$ is the distance from $x$ to $0$ on the number line, so it is never
negative. More generally, $\abs{x - a}$ is how far apart $x$ and $a$ are, whichever of the
two is larger.

**Example.** $\abs{-3} = -(-3) = 3$, and the distance between $-1$ and $4$ is
$\abs{-1 - 4} = \abs{-5} = 5$.

**Non-example.** $\abs{x}$ does not mean "delete the minus sign". For $x = -2$ we get
$\abs{-x} = \abs{2} = 2$, which is $-x$, not $x$: the formula $\abs{-x} = x$ fails for every
negative $x$.

:::{proof:remark} Basic properties
:label: rem-calc-absolute-value-properties

For all real numbers $x$ and $y$:

1. $\abs{x} \ge 0$, and $\abs{x} = 0$ only when $x = 0$;
2. $\abs{-x} = \abs{x}$;
3. $\abs{x}$ is the larger of $x$ and $-x$, that is, $\abs{x} = \max\{x, -x\}$; in particular
   $-\abs{x} \le x \le \abs{x}$;
4. $\abs{xy} = \abs{x}\,\abs{y}$, and $\abs{x / y} = \abs{x} / \abs{y}$ when $y \ne 0$;
5. $\abs{x}^2 = x^2$ and $\sqrt{x^2} = \abs{x}$;
6. if $x \ge 0$ and $y \ge 0$, then $x < y$ if and only if $x^2 < y^2$, and $x = y$ if and
   only if $x^2 = y^2$.

Properties 1–4 and the first half of 5 follow from the definition by checking the cases
$x \ge 0$ and $x < 0$ (for 4, the four combinations of signs of $x$ and $y$). For 3: if
$x \ge 0$ then $\abs{x} = x \ge -x$, and if $x < 0$ then $\abs{x} = -x > x$. In both cases
$\abs{x}$ is the larger of the two numbers.

% TODO link: rem-calc-square-roots once vronnblom/maths#8 is merged
Properties 5 and 6 rest on the remark on square roots in Real Numbers and Intervals: every
$y \ge 0$ has exactly one square root $\sqrt{y} \ge 0$, and the proof of that uniqueness shows
that for $0 \le s < t$ we have $s^2 < t^2$. For 5: $\abs{x} \ge 0$ and $\abs{x}^2 = x^2$, so
$\abs{x}$ is the one non-negative square root of $x^2$. For 6: if $x < y$ then $x^2 < y^2$ by
that fact. If instead $x \ge y$, then $x^2 \ge y^2$ (by the same fact when $x > y$), so
$x^2 < y^2$ fails. The second half of 6 is the uniqueness itself: $x$ and $y$ are both
non-negative square roots of $x^2 = y^2$.
:::

### Working with inequalities

% TODO link: calc-real-numbers once calc-real-numbers is merged
We use the order properties of the real numbers from Real Numbers and Intervals, in this form.
For all real numbers $u$, $v$, $w$, $s$, $t$ and $c$:

- **trichotomy:** exactly one of $u < v$, $u = v$ and $u > v$ holds; so "$u \le v$" fails
  exactly when $u > v$, and "$u < v$" fails exactly when $u \ge v$;
- **transitivity:** $u < v$ and $v < w$ imply $u < w$; the same holds when one of the two
  inequalities is $\le$ (for example $u \le v < w$ implies $u < w$), and $u \le v \le w$
  implies $u \le w$;
- **adding the same number** to both sides keeps an inequality: $u < v$ implies
  $u + c < v + c$;
- **adding two inequalities:** $u \le v$ and $s \le t$ imply $u + s \le v + t$, and the sum is
  strict, $u + s < v + t$, if at least one of the two is strict;
- **multiplying** both sides by a positive number keeps an inequality, and multiplying by a
  negative number reverses it: if $u < v$ and $c > 0$ then $cu < cv$, but if $c < 0$ then
  $cu > cv$;
- **multiplying by a number that may be zero:** if $u \le v$ and $c \ge 0$ then $cu \le cv$.
  This holds in particular when $u < v$, but the result is then only $\le$: for $c = 0$ both
  sides are $0$;
- **signs:** a product or a quotient of two non-zero numbers is positive when they have the
  same sign, and negative when their signs differ.

Every rule stated with $<$ also holds with $\le$ in place of $<$ (and $\ge$ in place of $>$);
for example, $u \le v$ and $c < 0$ give $cu \ge cv$.

To solve a quadratic or rational inequality, we factor it and make a **sign table**. A factor
$x - r$ is negative for $x < r$ and positive for $x > r$, so it changes sign only at $r$. The
zeros of the factors split the number line into intervals, and on each interval every factor,
and hence the whole expression, keeps one sign.

## Main results

The first result is the translation between distances and intervals that the rest of
calculus uses.

:::{proof:proposition} Distance inequalities as intervals
:label: prop-calc-abs-interval

Let $a$ and $\delta$ be real numbers. For every real number $x$,
$$
\begin{aligned}
&\text{(a)} && \abs{x - a} < \delta && \iff\quad a - \delta < x < a + \delta,\\
&\text{(b)} && \abs{x - a} \le \delta && \iff\quad a - \delta \le x \le a + \delta,\\
&\text{(c)} && \abs{x - a} > \delta && \iff\quad x < a - \delta \ \text{ or } \ x > a + \delta,\\
&\text{(d)} && \abs{x - a} \ge \delta && \iff\quad x \le a - \delta \ \text{ or } \ x \ge a + \delta,\\
&\text{(e)} && 0 < \abs{x - a} < \delta && \iff\quad a - \delta < x < a \ \text{ or } \ a < x < a + \delta.
\end{aligned}
$$
% TODO link: def-calc-interval once calc-real-numbers is merged
In particular, when $\delta > 0$, (a) says that $x$ lies in the open interval
$(a - \delta, a + \delta)$, (b) that $x$ lies in the closed interval
$[a - \delta, a + \delta]$, and (e) that $x$ lies in the set
$$
(a - \delta, a) \cup (a, a + \delta),
$$
the open interval $(a - \delta, a + \delta)$ with its centre $a$ removed. This set is called
the **punctured neighbourhood** of $a$ of radius $\delta$.
:::

:::{proof:proof}
:enumerated: false
We first treat a number $y$ in place of $x - a$, using that $\abs{y}$ is the larger of $y$ and
$-y$, and then shift by $a$.

By property 3 of [](#rem-calc-absolute-value-properties), $\abs{y} = \max\{y, -y\}$. The larger of two numbers is less than
$\delta$ if and only if both of them are, so
$$
\abs{y} < \delta
\iff y < \delta \text{ and } -y < \delta
\iff y < \delta \text{ and } y > -\delta
\iff -\delta < y < \delta .
$$
The middle step multiplies $-y < \delta$ by $-1$, which reverses the inequality, and
multiplying $y > -\delta$ by $-1$ takes us back. The same argument, with the $\le$ forms of the
same rules, gives $\abs{y} \le \delta \iff -\delta \le y \le \delta$.

Now put $y = x - a$. Adding the same number $a$ to all three parts of
$-\delta < x - a < \delta$ gives $a - \delta < x < a + \delta$, and adding $-a$ undoes this, so
the two are equivalent. This proves (a), and (b) follows in the same way with $\le$.

Part (c) is the negation of (b): by trichotomy, $\abs{x - a} > \delta$ says exactly that
$\abs{x - a} \le \delta$ fails, and "$a - \delta \le x \le a + \delta$" fails exactly when
$x < a - \delta$ or $x > a + \delta$. In the same way, (d) is the negation of (a).

For (e), the condition $0 < \abs{x - a}$ says that $x \ne a$: by property 1 of
[](#rem-calc-absolute-value-properties), $\abs{x - a}$ is never negative and is $0$ only when
$x - a = 0$. So by (a), $0 < \abs{x - a} < \delta$ holds if and only if
$a - \delta < x < a + \delta$ and $x \ne a$. By trichotomy, $x \ne a$ means $x < a$ or $x > a$,
which splits the double inequality into $a - \delta < x < a$ or $a < x < a + \delta$.
:::

[](#fig-calc-absolute-value-inequalities-neighbourhood) shows parts (a) and (e).

:::{figure} ./img/distance-interval.svg
:label: fig-calc-absolute-value-inequalities-neighbourhood
:alt: Two number lines, each with the points a minus delta, a and a plus delta marked. On the top line, a thick segment runs from a minus delta to a plus delta, with hollow dots at both ends. A point x inside the segment is marked, and a bracket above the line from a to x is labelled with the distance, the absolute value of x minus a. On the bottom line, the same segment has a third hollow dot at its centre a.

Top: the $x$ with $\abs{x - a} < \delta$ form the open interval $(a - \delta, a + \delta)$;
the bracket marks the distance $\abs{x - a}$ from $a$ to one such $x$. Bottom: the $x$ with
$0 < \abs{x - a} < \delta$ form the punctured neighbourhood
$(a - \delta, a) \cup (a, a + \delta)$; the hollow dot at $a$ shows that $a$ is left out.
:::

The case $a = 0$ is used so often that it is worth stating on its own:
$\abs{y} < \delta$ if and only if $-\delta < y < \delta$, and
$\abs{y} \le \delta$ if and only if $-\delta \le y \le \delta$.

The second result says that the size of a sum is at most the sum of the sizes. Part (b) is the
form for distances: going from $x$ to $y$ by way of $z$ is never shorter than going directly.

:::{proof:theorem} Triangle inequality
:label: thm-calc-triangle-inequality

For all real numbers $x$, $y$ and $z$,
$$
\begin{aligned}
&\text{(a)} && \abs{x + y} \le \abs{x} + \abs{y},\\
&\text{(b)} && \abs{x - y} \le \abs{x - z} + \abs{z - y},\\
&\text{(c)} && \abs{\abs{x} - \abs{y}} \le \abs{x - y}.
\end{aligned}
$$
:::

:::{proof:proof}
:enumerated: false
For (a) we bound $x + y$ and $-(x + y)$ separately, then use that $\abs{x + y}$ is the larger
of the two.

(a) By property 3 of [](#rem-calc-absolute-value-properties), $x \le \abs{x}$ and $-x \le \abs{x}$, and likewise
$y \le \abs{y}$ and $-y \le \abs{y}$. Adding two inequalities (the $\le$ form),
$$
x + y \le \abs{x} + \abs{y}
\qquad\text{and}\qquad
-(x + y) = (-x) + (-y) \le \abs{x} + \abs{y}.
$$
Since $\abs{x + y} = \max\{x + y, -(x + y)\}$, again by property 3 of [](#rem-calc-absolute-value-properties), and the larger of two
numbers is at most $\abs{x} + \abs{y}$ when both of them are, it follows that
$\abs{x + y} \le \abs{x} + \abs{y}$.

(b) Write $x - y = (x - z) + (z - y)$ and apply (a) to the numbers $x - z$ and $z - y$.

(c) By (a) applied to $x - y$ and $y$, and then adding the same number $-\abs{y}$ to both
sides,
$$
\abs{x} = \abs{(x - y) + y} \le \abs{x - y} + \abs{y},
\qquad\text{so}\qquad
\abs{x} - \abs{y} \le \abs{x - y}.
$$
Exchanging the roles of $x$ and $y$ gives $\abs{y} - \abs{x} \le \abs{y - x}$, and
$\abs{y - x} = \abs{x - y}$ by property 2 of [](#rem-calc-absolute-value-properties). So both
$\abs{x} - \abs{y}$ and its negative are at most $\abs{x - y}$, and so is the larger of the two.
That larger number is $\abs{\abs{x} - \abs{y}}$ by property 3 of
[](#rem-calc-absolute-value-properties), which proves (c).
:::

## Worked examples

:::{proof:example} A linear inequality: solve $3 - 2x < 7$
:label: eg-calc-absolute-value-inequalities-linear

1. Subtract $3$ from both sides: $-2x < 4$.
2. Divide both sides by $-2$. The number is negative, so the inequality reverses: $x > -2$.

$$
\boxed{(-2, \infty)}
$$

**Check.** $x = 0$ is in the set, and $3 - 0 = 3 < 7$. ✓ The endpoint $x = -2$ gives
$3 + 4 = 7$, which is not less than $7$, so it is rightly excluded. ✓ $x = -3$ gives
$9 < 7$, which is false. ✓
:::

:::{proof:example} A quadratic inequality: solve $x^2 - x - 6 \le 0$
:label: eg-calc-absolute-value-inequalities-quadratic

1. Factor: $x^2 - x - 6 = (x + 2)(x - 3)$. The zeros are $-2$ and $3$.
2. Make the sign table.

   | | $x < -2$ | $-2 < x < 3$ | $x > 3$ |
   |---|---|---|---|
   | $x + 2$ | $-$ | $+$ | $+$ |
   | $x - 3$ | $-$ | $-$ | $+$ |
   | $(x + 2)(x - 3)$ | $+$ | $-$ | $+$ |

3. The product is negative on $(-2, 3)$ and zero at $-2$ and $3$. The inequality allows
   equality, so both zeros belong to the solution set.

$$
\boxed{[-2, 3]}
$$

**Check.** $x = 0$: $-6 \le 0$. ✓ $x = 4$: $16 - 4 - 6 = 6$, which is positive, so $4$ is
rightly excluded. ✓ $x = -2$: $4 + 2 - 6 = 0 \le 0$. ✓
:::

:::{proof:example} A strict absolute-value inequality: solve $\abs{2x - 5} < 3$
:label: eg-calc-absolute-value-inequalities-abs-less

1. By [](#prop-calc-abs-interval) (a) with $a = 0$, applied to $y = 2x - 5$:
   $-3 < 2x - 5 < 3$.
2. Add $5$ to all three parts: $2 < 2x < 8$.
3. Divide by $2$, which is positive: $1 < x < 4$.

$$
\boxed{(1, 4)}
$$

The distance reading gives the same set: $\abs{2x - 5} = 2\abs{x - \tfrac{5}{2}}$, so the
inequality says that $x$ is within $\tfrac{3}{2}$ of $\tfrac{5}{2}$. The interval
$(1, 4)$ has midpoint $\tfrac{5}{2}$ and half-width $\tfrac{3}{2}$.

**Check.** $x = 2$: $\abs{-1} = 1 < 3$. ✓ The endpoint $x = 1$ gives $\abs{-3} = 3$, which is
not less than $3$. ✓ $x = 5$: $\abs{5} = 5$, outside. ✓
:::

:::{proof:example} An "outside" inequality: solve $\abs{x + 1} \ge 2$
:label: eg-calc-absolute-value-inequalities-abs-greater

1. Write $x + 1 = x - (-1)$: the inequality says that the distance from $x$ to $-1$ is at
   least $2$.
2. By [](#prop-calc-abs-interval) (d) with $a = -1$ and $\delta = 2$:
   $x \le -3$ or $x \ge 1$.

$$
\boxed{(-\infty, -3] \cup [1, \infty)}
$$

**Check.** $x = 0$: $\abs{1} = 1$, which is less than $2$, so $0$ is rightly excluded. ✓
$x = 1$: $\abs{2} = 2 \ge 2$. ✓ $x = -4$: $\abs{-3} = 3 \ge 2$. ✓
:::

:::{proof:example} An interval with its centre removed
:label: eg-calc-absolute-value-inequalities-punctured

Describe the set of all $x$ with $0 < \abs{x - 2} < 0.1$.

1. This is [](#prop-calc-abs-interval) (e) with $a = 2$ and $\delta = 0.1$:
   $1.9 < x < 2$ or $2 < x < 2.1$.
2. So the set is the punctured neighbourhood of $2$ of radius $0.1$: the interval $(1.9, 2.1)$
   with its centre $2$ removed.

$$
\boxed{(1.9, 2) \cup (2, 2.1)}
$$

**Check.** $x = 2$ gives $\abs{0} = 0$, which is not greater than $0$. ✓ $x = 2.05$ gives
$0 < 0.05 < 0.1$. ✓ $x = 2.1$ gives $\abs{0.1} = 0.1$, not less than $0.1$. ✓
:::

:::{admonition} Looking ahead
:class: looking-ahead
The definition of a limit, in the Limits chapter, only looks at $x$ in a punctured
neighbourhood of $a$: what happens at $a$ itself does not matter.
:::

:::{proof:example} Bounding with the triangle inequality
:label: eg-calc-absolute-value-inequalities-triangle-bound

Show that if $\abs{x - 2} < 1$, then $\abs{x + 2} < 5$ and $\abs{x^2 - 4} \le 5\abs{x - 2}$.

1. Write $x + 2$ in terms of the distance to $2$: $x + 2 = (x - 2) + 4$.
2. By [](#thm-calc-triangle-inequality) (a), and adding $4$ to both sides of
   $\abs{x - 2} < 1$,
   $$
   \abs{x + 2} \le \abs{x - 2} + \abs{4} = \abs{x - 2} + 4 < 1 + 4 = 5 .
   $$
   A $\le$ followed by a $<$ gives $<$ (transitivity), so $\abs{x + 2} < 5$.
3. Factor and use property 4 of [](#rem-calc-absolute-value-properties):
   $\abs{x^2 - 4} = \abs{(x - 2)(x + 2)} = \abs{x - 2}\,\abs{x + 2}$.
4. Multiply $\abs{x + 2} < 5$ by $\abs{x - 2}$. This number is $\ge 0$ (property 1 of
   [](#rem-calc-absolute-value-properties)), but it may be $0$: it is $0$ at $x = 2$. So
   multiplying keeps the inequality only in the form $\le$:
   $$
   \abs{x^2 - 4} = \abs{x - 2}\,\abs{x + 2} \le 5\abs{x - 2} ,
   $$
   with equality at $x = 2$, where both sides are $0$.

$$
\boxed{\abs{x + 2} < 5 \quad\text{and}\quad \abs{x^2 - 4} \le 5\abs{x - 2}}
$$

**Check.** $x = 2.9$: $\abs{4.9} = 4.9 < 5$ ✓, and $\abs{2.9^2 - 4} = 4.41 \le 5 \cdot 0.9 = 4.5$. ✓
:::

## Common mistakes

:::{warning} Forgetting to reverse the inequality
✗ **Wrong:** "$-2x < 4$, so $x < -2$."

**Why:** dividing by the negative number $-2$ reverses the inequality. The value $x = 0$
satisfies $-2x < 4$ but not $x < -2$.

✓ **Right:** $-2x < 4$ gives $x > -2$.
:::

:::{warning} Treating the absolute value as additive
✗ **Wrong:** "$\abs{x + y} = \abs{x} + \abs{y}$."

**Why:** $\abs{3 + (-3)} = 0$, but $\abs{3} + \abs{-3} = 6$.

✓ **Right:** only the inequality $\abs{x + y} \le \abs{x} + \abs{y}$ holds in general
([](#thm-calc-triangle-inequality)). It is an equality exactly when $x$ and $y$ do not have
opposite signs (see the rigorous track).
:::

:::{warning} Writing an "or" as a chain
✗ **Wrong:** "$\abs{x - 3} > 2$, so $-2 > x - 3 > 2$."

**Why:** no number is both less than $-2$ and greater than $2$, so the chain has no solutions
at all. An "outside" condition is an *or* of two inequalities.

✓ **Right:** by [](#prop-calc-abs-interval) (c), $x - 3 < -2$ or $x - 3 > 2$, so the solution
set is $(-\infty, 1) \cup (5, \infty)$.
:::

:::{warning} Dividing by an unknown
✗ **Wrong:** "$x^2 > 3x$; divide by $x$: $x > 3$."

**Why:** the direction of the inequality after dividing by $x$ depends on the sign of $x$,
which we do not know. The value $x = -1$ satisfies $1 > -3$ but not $x > 3$.

✓ **Right:** $x^2 - 3x = x(x - 3) > 0$, and a sign table gives $(-\infty, 0) \cup (3, \infty)$.
:::

## Rigorous track

:::{admonition} When is the triangle inequality an equality?
:class: dropdown rigor
We show that $\abs{x + y} = \abs{x} + \abs{y}$ if and only if $xy \ge 0$.

Both sides are non-negative, so by property 6 of [](#rem-calc-absolute-value-properties) they
are equal if and only if their squares are. By property 5 and property 4 of
[](#rem-calc-absolute-value-properties),
$$
\abs{x + y}^2 = x^2 + 2xy + y^2,
\qquad
\bigl(\abs{x} + \abs{y}\bigr)^2 = x^2 + 2\abs{xy} + y^2 .
$$
These are equal if and only if $xy = \abs{xy}$, that is, if and only if $xy \ge 0$.
:::

:::{admonition} No condition on $\delta$ is needed
:class: dropdown rigor
The proof of [](#prop-calc-abs-interval) never used the sign of $\delta$, so the proposition
holds for every real $\delta$. For $\delta < 0$ both sides of (a), (b) and (e) are false for
every $x$. For $\delta = 0$, (a) and (e) have no solutions, and (b) says that
$\abs{x - a} \le 0$ if and only if $x = a$. Later pages use the proposition with $\delta > 0$,
where both sides describe a genuine interval or punctured neighbourhood.
:::

## Summary

- $\abs{x} = x$ for $x \ge 0$ and $\abs{x} = -x$ for $x < 0$; $\abs{x - a}$ is the distance
  between $x$ and $a$.
- $\abs{x - a} < \delta$ if and only if $a - \delta < x < a + \delta$, and likewise with $\le$
  ([](#prop-calc-abs-interval)).
- "Outside" conditions, $\abs{x - a} > \delta$, become an *or*: $x < a - \delta$ or
  $x > a + \delta$.
- $0 < \abs{x - a} < \delta$ describes the punctured neighbourhood
  $(a - \delta, a) \cup (a, a + \delta)$: the interval $(a - \delta, a + \delta)$ without its
  centre $a$ ([](#prop-calc-abs-interval) (e)).
- Triangle inequality: $\abs{x + y} \le \abs{x} + \abs{y}$, and
  $\abs{x - y} \le \abs{x - z} + \abs{z - y}$ ([](#thm-calc-triangle-inequality)).
- To solve a quadratic or rational inequality, factor, make a sign table, and check the
  endpoints; never divide by a quantity whose sign you do not know.

## Exercises

::::{exercise} Evaluating absolute values
:label: exr-calc-absolute-value-inequalities-evaluate
:class: tier-a

Compute $\abs{-7} + \abs{3 - 8} - \abs{(-2) \cdot 4}$.

:::{admonition} Answer
:class: dropdown answer
$4$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-evaluate
:label: sol-calc-absolute-value-inequalities-evaluate
:class: dropdown
By [](#def-calc-absolute-value), $\abs{-7} = 7$, $\abs{3 - 8} = \abs{-5} = 5$ and
$\abs{(-2) \cdot 4} = \abs{-8} = 8$. So the expression is $7 + 5 - 8 = 4$.
::::

::::{exercise} A linear inequality
:label: exr-calc-absolute-value-inequalities-linear
:class: tier-a

Solve $5 - 3x \ge 11$. Give the solution set as an interval.

:::{admonition} Hint 1
:class: dropdown hint
What happens to the inequality when you divide by a negative number?
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, -2]$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-linear
:label: sol-calc-absolute-value-inequalities-linear
:class: dropdown
Subtracting $5$ gives $-3x \ge 6$. Dividing by $-3$, which is negative, reverses the
inequality: $x \le -2$. The solution set is $(-\infty, -2]$.
::::

::::{exercise} From a distance to an interval
:label: exr-calc-absolute-value-inequalities-abs-to-interval
:class: tier-a

Write the set of all $x$ with $\abs{x - 4} < 0.5$ as an interval.

:::{admonition} Answer
:class: dropdown answer set
$(3.5, 4.5)$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-abs-to-interval
:label: sol-calc-absolute-value-inequalities-abs-to-interval
:class: dropdown
By [](#prop-calc-abs-interval) (a) with $a = 4$ and $\delta = 0.5$,
$\abs{x - 4} < 0.5$ if and only if $3.5 < x < 4.5$. The set is $(3.5, 4.5)$.
::::

::::{exercise} A closed absolute-value inequality
:label: exr-calc-absolute-value-inequalities-abs-closed
:class: tier-a

Solve $\abs{3x + 1} \le 5$.

:::{admonition} Hint 1
:class: dropdown hint
Use [](#prop-calc-abs-interval) (b) with $a = 0$ to remove the absolute value, then solve the
double inequality.
:::

:::{admonition} Answer
:class: dropdown answer set
$[-2, \frac{4}{3}]$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-abs-closed
:label: sol-calc-absolute-value-inequalities-abs-closed
:class: dropdown
By [](#prop-calc-abs-interval) (b) with $a = 0$, the inequality is equivalent to
$-5 \le 3x + 1 \le 5$. Subtracting $1$ from all three parts gives $-6 \le 3x \le 4$, and
dividing by $3$ gives $-2 \le x \le \frac{4}{3}$. The solution set is $[-2, \frac{4}{3}]$.
::::

::::{exercise} From an interval to a distance
:label: exr-calc-absolute-value-inequalities-interval-to-abs
:class: tier-a

The interval $(-1, 5)$ is the set of all $x$ with $\abs{x - a} < \delta$, for exactly one
choice of $a$ and $\delta > 0$. Find (a) the centre $a$ and (b) the half-width $\delta$.

:::{admonition} Hint 1
:class: dropdown hint
The centre is the midpoint of the interval.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $2$ (b) $3$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-interval-to-abs
:label: sol-calc-absolute-value-inequalities-interval-to-abs
:class: dropdown
By [](#prop-calc-abs-interval) (a), the set of $x$ with $\abs{x - a} < \delta$ is
$(a - \delta, a + \delta)$, so we need $a - \delta = -1$ and $a + \delta = 5$. Adding the two
equations gives $2a = 4$, so $a = 2$; subtracting them gives $2\delta = 6$, so $\delta = 3$.
Check: $2 - 3 = -1$ and $2 + 3 = 5$.
::::

::::{exercise} An "outside" inequality
:label: exr-calc-absolute-value-inequalities-abs-outside
:class: tier-b

Solve $\abs{2x - 3} > 5$. Give the solution set as a union of intervals.

:::{admonition} Hint 1
:class: dropdown hint
The condition is an *or* of two inequalities, not a chain.
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, -1), (4, \infty)$ (the union of these two intervals)
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-abs-outside
:label: sol-calc-absolute-value-inequalities-abs-outside
:class: dropdown
By [](#prop-calc-abs-interval) (c) with $a = 0$ and $\delta = 5$, applied to $y = 2x - 3$:
$2x - 3 < -5$ or $2x - 3 > 5$. The first gives $2x < -2$, so $x < -1$; the second gives
$2x > 8$, so $x > 4$. The solution set is $(-\infty, -1) \cup (4, \infty)$.
::::

::::{exercise} A quadratic inequality
:label: exr-calc-absolute-value-inequalities-quadratic
:class: tier-b

Solve $x^2 + 2x - 8 < 0$.

:::{admonition} Hint 1
:class: dropdown hint
Factor the quadratic and make a sign table.
:::

:::{admonition} Answer
:class: dropdown answer set
$(-4, 2)$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-quadratic
:label: sol-calc-absolute-value-inequalities-quadratic
:class: dropdown
$x^2 + 2x - 8 = (x + 4)(x - 2)$, with zeros $-4$ and $2$. For $x < -4$ both factors are
negative and the product is positive; for $-4 < x < 2$ the factors have opposite signs and the
product is negative; for $x > 2$ both are positive. The inequality is strict, so the zeros are
excluded. The solution set is $(-4, 2)$.
::::

::::{exercise} Do not divide by $x$
:label: exr-calc-absolute-value-inequalities-cubic
:class: tier-b

Solve $x^3 \ge 4x$. Give the solution set as a union of intervals.

:::{admonition} Hint 1
:class: dropdown hint
Bring everything to one side and factor completely: there are three linear factors.
:::

:::{admonition} Answer
:class: dropdown answer set
$[-2, 0], [2, \infty)$ (the union of these two intervals)
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-cubic
:label: sol-calc-absolute-value-inequalities-cubic
:class: dropdown
The inequality is $x^3 - 4x \ge 0$, and $x^3 - 4x = x(x^2 - 4) = (x + 2)\,x\,(x - 2)$, with
zeros $-2$, $0$ and $2$. The sign table:

| | $x < -2$ | $-2 < x < 0$ | $0 < x < 2$ | $x > 2$ |
|---|---|---|---|---|
| $x + 2$ | $-$ | $+$ | $+$ | $+$ |
| $x$ | $-$ | $-$ | $+$ | $+$ |
| $x - 2$ | $-$ | $-$ | $-$ | $+$ |
| product | $-$ | $+$ | $-$ | $+$ |

The product is positive on $(-2, 0)$ and $(2, \infty)$, and zero at the three zeros, which the
inequality allows. The solution set is $[-2, 0] \cup [2, \infty)$. Dividing by $x$ at the start
would have lost the interval $[-2, 0]$.
::::

::::{exercise} A rational inequality
:label: exr-calc-absolute-value-inequalities-rational
:class: tier-b

Solve $\dfrac{x - 1}{x + 2} \le 0$.

:::{admonition} Hint 1
:class: dropdown hint
A quotient has the same sign as a product. Which endpoint can never belong to the solution set?
:::

:::{admonition} Answer
:class: dropdown answer set
$(-2, 1]$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-rational
:label: sol-calc-absolute-value-inequalities-rational
:class: dropdown
The quotient is undefined at $x = -2$ and zero at $x = 1$. For $x < -2$ both $x - 1$ and
$x + 2$ are negative, so the quotient is positive. For $-2 < x < 1$ the numerator is negative
and the denominator positive, so the quotient is negative. For $x > 1$ both are positive. The
quotient is $\le 0$ on $(-2, 1)$ and at $x = 1$, and $x = -2$ is excluded because the quotient
is not defined there. The solution set is $(-2, 1]$.
::::

::::{exercise} A punctured neighbourhood
:label: exr-calc-absolute-value-inequalities-punctured
:class: tier-b

Write the set of all $x$ with $0 < \abs{x + 1} < \frac{1}{2}$ as a union of two intervals.

:::{admonition} Hint 1
:class: dropdown hint
Write $x + 1$ as $x - a$ for a suitable $a$. What does the condition $0 < \abs{x + 1}$ exclude?
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\frac{3}{2}, -1), (-1, -\frac{1}{2})$ (the union of these two intervals)
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-punctured
:label: sol-calc-absolute-value-inequalities-punctured
:class: dropdown
Here $x + 1 = x - (-1)$, so $a = -1$ and $\delta = \frac{1}{2}$. By
[](#prop-calc-abs-interval) (e), $0 < \abs{x + 1} < \frac{1}{2}$ means
$-\frac{3}{2} < x < -1$ or $-1 < x < -\frac{1}{2}$: the interval
$(-\frac{3}{2}, -\frac{1}{2})$ with its centre $-1$ removed. The set is
$(-\frac{3}{2}, -1) \cup (-1, -\frac{1}{2})$.
::::

::::{exercise} True or false?
:label: exr-calc-absolute-value-inequalities-difference-bound
:class: tier-b

True or false: $\abs{x - y} \le \abs{x} + \abs{y}$ for all real numbers $x$ and $y$.

:::{admonition} Hint 1
:class: dropdown hint
Write $x - y$ as a sum.
:::

:::{admonition} Answer
:class: dropdown answer bool
True
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-difference-bound
:label: sol-calc-absolute-value-inequalities-difference-bound
:class: dropdown
True. Write $x - y = x + (-y)$. By [](#thm-calc-triangle-inequality) (a) and property 2 of
[](#rem-calc-absolute-value-properties),
$\abs{x - y} \le \abs{x} + \abs{-y} = \abs{x} + \abs{y}$.
::::

::::{exercise} Closer to $1$ than to $-3$
:label: exr-calc-absolute-value-inequalities-compare-distances
:class: tier-c

Solve $\abs{x - 1} < \abs{x + 3}$.

:::{admonition} Hint 1
:class: dropdown hint
Read both sides as distances: which points of the number line are closer to $1$ than to $-3$?
:::

:::{admonition} Hint 2
:class: dropdown hint
For an algebraic proof, both sides are non-negative, so you may compare their squares.
:::

:::{admonition} Answer
:class: dropdown answer set
$(-1, \infty)$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-compare-distances
:label: sol-calc-absolute-value-inequalities-compare-distances
:class: dropdown
Both sides are non-negative, so by property 6 of [](#rem-calc-absolute-value-properties) the
inequality holds if and only if $\abs{x - 1}^2 < \abs{x + 3}^2$. By property 5, this is
$(x - 1)^2 < (x + 3)^2$, that is, $x^2 - 2x + 1 < x^2 + 6x + 9$. This
simplifies to $-8 < 8x$, so $x > -1$. The solution set is $(-1, \infty)$.

This matches the picture: the point halfway between $-3$ and $1$ is $-1$, and the points
closer to $1$ are those to the right of it.
::::

::::{exercise} Two points close to a third
:label: exr-calc-absolute-value-inequalities-close-points
:class: tier-c rigor

Let $a$ and $\delta$ be real numbers. Prove that, for all real numbers $x$ and $y$, if
$\abs{x - a} < \frac{\delta}{2}$ and $\abs{y - a} < \frac{\delta}{2}$, then
$\abs{x - y} < \delta$.

:::{admonition} Hint 1
:class: dropdown hint
Go from $x$ to $y$ by way of $a$.
:::

:::{admonition} Answer
:class: dropdown answer manual
Use the triangle inequality with the intermediate point $a$.
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-close-points
:label: sol-calc-absolute-value-inequalities-close-points
:class: dropdown
Let $x$ and $y$ be real numbers with $\abs{x - a} < \frac{\delta}{2}$ and
$\abs{y - a} < \frac{\delta}{2}$. By [](#thm-calc-triangle-inequality) (b) with $z = a$, and
since $\abs{a - y} = \abs{y - a}$ (property 2 of [](#rem-calc-absolute-value-properties)),
$$
\abs{x - y} \le \abs{x - a} + \abs{a - y} = \abs{x - a} + \abs{y - a}
< \frac{\delta}{2} + \frac{\delta}{2} = \delta .
$$
The $<$ comes from adding the two strict inequalities, and a $\le$ followed by a $<$ gives $<$.

The proof never uses the sign of $\delta$. If $\delta \le 0$, no $x$ satisfies
$\abs{x - a} < \frac{\delta}{2}$, so there is nothing to prove; the statement has content only
for $\delta > 0$, which is how it is used in the Limits chapter.
::::

::::{exercise} How close is close enough?
:label: exr-calc-absolute-value-inequalities-largest-delta
:class: tier-c

Find the largest $\delta > 0$ such that every $x$ with $\abs{x - 2} < \delta$ satisfies
$\abs{x^2 - 4} < 1$.

:::{admonition} Hint 1
:class: dropdown hint
First solve $\abs{x^2 - 4} < 1$ and find the interval of solutions that contains $2$.
:::

:::{admonition} Hint 2
:class: dropdown hint
The interval $(2 - \delta, 2 + \delta)$ must fit inside that interval. Which end is closer to $2$?
:::

:::{admonition} Answer
:class: dropdown answer
$\sqrt{5} - 2$
:::
::::

::::{solution} exr-calc-absolute-value-inequalities-largest-delta
:label: sol-calc-absolute-value-inequalities-largest-delta
:class: dropdown
By [](#prop-calc-abs-interval) (a) with $a = 0$, $\abs{x^2 - 4} < 1$ means $-1 < x^2 - 4 < 1$,
that is, $3 < x^2 < 5$. For $x > 0$ this says $\sqrt{3} < x < \sqrt{5}$, by property 6 of
[](#rem-calc-absolute-value-properties) (as $3 = (\sqrt{3})^2$ and $5 = (\sqrt{5})^2$), so near
$2$ the solutions form the interval $(\sqrt{3}, \sqrt{5})$.

By [](#prop-calc-abs-interval) (a) again, the $x$ with $\abs{x - 2} < \delta$ form
$(2 - \delta, 2 + \delta)$. This interval lies inside $(\sqrt{3}, \sqrt{5})$ exactly when
$2 - \delta \ge \sqrt{3}$ and $2 + \delta \le \sqrt{5}$, that is, when
$\delta \le 2 - \sqrt{3}$ and $\delta \le \sqrt{5} - 2$.

The second bound is the smaller one: $\sqrt{5} - 2 < 2 - \sqrt{3}$ is equivalent to
$\sqrt{5} + \sqrt{3} < 4$. By property 6 of [](#rem-calc-absolute-value-properties), applied to
non-negative numbers, it is enough to compare squares: $\sqrt{15} < 4$ because $15 < 16 = 4^2$,
so $(\sqrt{5} + \sqrt{3})^2 = 8 + 2\sqrt{15} < 8 + 2 \cdot 4 = 16 = 4^2$. So every
$\delta \le \sqrt{5} - 2$ works. If $\delta > \sqrt{5} - 2$, then $2 + \delta > \sqrt{5}$, and
any $x$ with $\sqrt{5} \le x < 2 + \delta$ satisfies $\abs{x - 2} < \delta$ but $x^2 \ge 5$
(property 6 again),
so $\abs{x^2 - 4} \ge 1$. The largest $\delta$ is therefore $\sqrt{5} - 2$, which is $0.236$
to three decimal places.
::::

## Where this leads

:::{where-this-leads}
:::
