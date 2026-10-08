---
title: Functions and Their Graphs
label: calc-functions
description: >-
  What a function is, how to find its natural domain and its range, how to read both off a
  graph, and how to recognise even, odd, increasing and decreasing functions.
tags: [preliminaries, modelling]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 1
  est_minutes: 25
  prerequisites: [calc-real-numbers]
  objectives:
    - Determine the natural domain and the range.
    - Read and sketch graphs.
    - Recognise even/odd and increasing/decreasing functions.
    - Model a situation with a function.
  verify: verify/calculus/preliminaries/test_functions.py
  widgets: []
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

A farmer has 40 metres of fencing and wants a rectangular pen against a long wall, so only
three sides need fencing. How large can the pen be? Before we can answer, we need a precise
way to say *how the area depends on the width*. Each width gives exactly one area, some
widths make no sense at all (a negative width, or one that uses more than 40 metres of
fence), and only some areas can actually occur.

Those three ingredients — a rule, the inputs it accepts and the outputs it produces — are
what a function is. Almost everything in calculus is about functions: limits describe how
their values behave, derivatives measure how fast they change, and integrals add up their
values. This page fixes the vocabulary that the rest of the course uses, and in particular
the exact meaning of "increasing", which later results depend on.

## Functions and their graphs

Think of a function as a machine: you feed it an input, and it returns *exactly one*
output. The same input always gives the same output. Different inputs may give the same
output.

:::{proof:definition} Function and graph
:label: def-calc-function

Let $A$ and $B$ be sets. A **function** $f\colon A \to B$ is a rule that assigns to each
element $x \in A$ exactly one element $f(x) \in B$, called the **value** of $f$ at $x$. We
also write $x \mapsto f(x)$.

When $A$ and $B$ are subsets of $\R$, the **graph** of $f$ is the set of points
$$
\{(x, f(x)) : x \in A\}
$$
in the plane.
:::

**In words.** Every allowed input gets an output, and never more than one. The function is
$f$; the number $f(x)$ is its value at one input $x$. The graph is the curve $y = f(x)$: the
point above (or below) each input $x$ at height $f(x)$.

**Example.** $f\colon \R \to \R$, $f(x) = x^2$, is a function: each real $x$ has exactly one
square. Different inputs can share a value ($f(-2) = f(2) = 4$); that is allowed.

**Non-example.** Assign to each $x \in \R$ the real numbers $y$ with $y^2 = x$. This is not
a function from $\R$ to $\R$, and it fails in both ways: $x = 4$ gets two numbers, $2$ and
$-2$, and $x = -1$ gets none.

Because each $x$ has only one value, a vertical line $x = c$ meets the graph of a function at
most once: at the point $(c, f(c))$ if $c$ is an allowed input, and nowhere otherwise. This is
the **vertical line test**: a curve in the plane is the graph of a function of $x$ exactly when
no vertical line meets it twice ([](#fig-calc-functions-vertical-line-test)).

:::{figure} ./img/vertical-line-test.svg
:label: fig-calc-functions-vertical-line-test
:alt: Two coordinate planes side by side. On the left, the parabola y = x squared, with a dashed vertical line at x = 1.5 that meets it at exactly one point. On the right, the sideways parabola y squared = x, opening to the right, with a dashed vertical line at x = 2.5 that meets it at two points, one above and one below the x-axis.

The vertical line test. Left: the graph of $y = x^2$; every vertical line meets it exactly
once. Right: the curve $y^2 = x$ of the non-example; the vertical line $x = 2.5$ meets it twice,
so it is not the graph of a function of $x$.
:::

:::{proof:definition} Domain and range
:label: def-calc-domain-range

Let $f\colon A \to B$ be a function.

- The **domain** of $f$ is the set $\dom f := A$ of its inputs.
- The **range** of $f$ is the set of its values,
  $$
  \ran f := \{f(x) : x \in \dom f\}.
  $$
  It is a subset of $B$, which is called the **codomain**.

If a function is given only by a formula, its domain is understood to be its **natural
domain**: the set of all real numbers $x$ for which the formula defines a real number.
:::

The set $\{f(x) : x \in \dom f\}$ is written in set-builder notation, and most domains and
ranges below are [intervals](#def-calc-interval) or unions of intervals; both are introduced in
[Real Numbers and Intervals](#calc-real-numbers).

**In words.** The domain is what you may put in; the range is what actually comes out. The
codomain is only a set that is promised to contain every value, and it may be larger than
the range. To find the range you must show two things: every value $f(x)$ lies in the set
you claim, and every element of that set is a value $f(x)$ for some $x$.

:::{admonition} Range, image and codomain
:class: note
The range is also called the **image** of $f$. Some books use the word "range" for what we
call the codomain. On this site the range is always the set of values $\ran f$ of
[](#def-calc-domain-range).
:::

**Example.** For $f(x) = \sqrt{x - 1}$, the square root needs $x - 1 \ge 0$, so
$\dom f = [1, \infty)$. Every square root is $\ge 0$, and each $y \ge 0$ is the value at
$x = y^2 + 1$, because $\sqrt{y^2} = y$ for $y \ge 0$
(see [the remark on square roots](#rem-calc-square-roots)). So $\ran f = [0, \infty)$.

**Non-example.** For $g\colon \R \to \R$, $g(x) = x^2$, the codomain is $\R$, but the range is
not: $-1$ is not in $\ran g$, because no real $x$ has $x^2 = -1$. Here $\ran g = [0, \infty)$.

**Reading a graph.** The domain is the shadow of the graph on the $x$-axis: the set of $x$
that have a point of the graph directly above or below them. The range is the shadow on the
$y$-axis: the set of heights that the graph reaches
([](#fig-calc-functions-domain-range-shadows)). A sketch suggests the domain and range; the
algebra above confirms them.

:::{figure} ./img/domain-range-shadows.svg
:label: fig-calc-functions-domain-range-shadows
:alt: The graph of y = square root of (x minus 1): a curve that starts at the point (1, 0) and rises ever more slowly to the right. A shaded band on the x-axis runs from 1 to the right, and a shaded band on the y-axis runs from 0 upwards. Dashed lines join the point (5, 2) of the graph to 5 on the x-axis and to 2 on the y-axis.

Domain and range as shadows, for $f(x) = \sqrt{x - 1}$. The shadow of the graph on the
$x$-axis is $\dom f = [1, \infty)$, and its shadow on the $y$-axis is $\ran f = [0, \infty)$.
The point $(5, 2)$ of the graph casts $5$ into the domain and $2 = f(5)$ into the range.
:::

**Sketching a graph.** For a first sketch, find the domain, compute a few values (including
any points where the formula changes, and where the graph crosses an axis), plot them, and
join them in order of increasing $x$, leaving gaps where $x$ is not in the domain. Where the
formula changes, compare the heights that the two pieces give there before you join across
that point: if they differ, the graph jumps, and no segment is drawn across the jump. For
example, the function that is $0$ for $x < 0$ and $1$ for $x \ge 0$ has domain $\R$, but its
graph is two horizontal pieces, with no segment from $(-1, 0)$ to $(0, 1)$.

## Symmetry and monotonicity

Two kinds of shape recur throughout calculus. Some graphs look the same after a reflection:
the graph of $y = x^2$ is unchanged by reflection in the $y$-axis. Some functions only ever go
up (or only ever go down) as $x$ moves to the right. Both properties save work: a symmetric
graph needs to be sketched only for $x \ge 0$, and a function that always goes up (one that
is *strictly* increasing, in the words of the definition below) takes each value at most
once.

:::{proof:definition} Even and odd functions
:label: def-calc-even-odd

Let $f$ be a function. Its domain is **symmetric about $0$** if $-x \in \dom f$ whenever
$x \in \dom f$.

- $f$ is **even** if $\dom f$ is symmetric about $0$ and $f(-x) = f(x)$ for every
  $x \in \dom f$.
- $f$ is **odd** if $\dom f$ is symmetric about $0$ and $f(-x) = -f(x)$ for every
  $x \in \dom f$.
:::

**In words.** An even function takes the same value at $x$ and at $-x$, so its graph is
symmetric under reflection in the $y$-axis. An odd function takes opposite values at $x$ and
$-x$, so its graph is symmetric under a half-turn about the origin: if $(x, y)$ is on the
graph, so is $(-x, -y)$. Both need a domain that is symmetric about $0$, so a function whose
domain is not symmetric is neither even nor odd. The condition on the values must hold for
*every* $x$ in the domain; one $x$ where it fails is enough to show that a function is not
even (or not odd).

**Example.** $x \mapsto x^4 - 3x^2$ is even and $x \mapsto x^3$ is odd. The names come from
these examples: a polynomial with only even powers of $x$ is even, and one with only odd
powers is odd.

**Non-example.** $f(x) = x^2 + x$ is neither even nor odd: $f(1) = 2$ and $f(-1) = 0$, so
$f(-1) \ne f(1)$ and $f(-1) \ne -f(1)$. Most functions are neither even nor odd.

:::{proof:definition} Increasing, decreasing and monotone functions
:label: def-calc-monotone

Let $f$ be a function and let $S \subseteq \dom f$ (usually an interval). We say that $f$ is

- **increasing on $S$** if for all $x_1, x_2 \in S$ with $x_1 < x_2$ we have
  $f(x_1) \le f(x_2)$;
- **strictly increasing on $S$** if for all $x_1, x_2 \in S$ with $x_1 < x_2$ we have
  $f(x_1) < f(x_2)$;
- **decreasing on $S$** if for all $x_1, x_2 \in S$ with $x_1 < x_2$ we have
  $f(x_1) \ge f(x_2)$;
- **strictly decreasing on $S$** if for all $x_1, x_2 \in S$ with $x_1 < x_2$ we have
  $f(x_1) > f(x_2)$.

$f$ is **monotone on $S$** if it is increasing on $S$ or decreasing on $S$, and **strictly
monotone on $S$** if it is strictly increasing on $S$ or strictly decreasing on $S$. When
$S = \dom f$ we leave out "on $S$".
:::

**In words.** Increasing means "never goes down" as you move right through $S$; strictly
increasing means "always goes up". A strictly increasing function is increasing, but not
the other way round: a function that is increasing may stay level for a while. The
definition compares *any two* points of $S$, not just neighbouring ones.

**Example.** $f(x) = 2x + 1$ is strictly increasing on $\R$: if $x_1 < x_2$, then
$2x_1 + 1 < 2x_2 + 1$. A constant function on a set $S$ with at least two points is both
increasing and decreasing on $S$, but neither strictly increasing nor strictly decreasing on
$S$. (On a set with only one point there are no $x_1 < x_2$ to compare, so every function is
strictly increasing and strictly decreasing there.) The function
$$
g(x) =
\begin{cases}
0, & x < 0, \\
x, & x \ge 0,
\end{cases}
$$
is increasing on $\R$ but not strictly increasing, because $g(-2) = g(-1) = 0$
([](#fig-calc-functions-increasing-vs-strictly)).

:::{figure} ./img/increasing-vs-strictly.svg
:label: fig-calc-functions-increasing-vs-strictly
:alt: Two graphs side by side. On the left, a graph that runs along the x-axis at height 0 from x = -3 to x = 0 and then rises in a straight line to the point (3, 3). On the right, the cubic curve y = x cubed from x = -1.5 to x = 1.5, which rises everywhere and flattens out briefly near the origin without becoming level.

Left: the function $g$ above is increasing on $\R$ but not strictly increasing: it stays level
for $x < 0$. Right: $x \mapsto x^3$ is strictly increasing on $\R$
([](#exr-calc-functions-cube-increasing) proves it). Its graph is very flat near $0$, but no two
points of it are at the same height.
:::

**Non-example.** $h(x) = x^2$ is not monotone on $\R$: $-1 < 0$ with $h(-1) > h(0)$, but
$0 < 1$ with $h(0) < h(1)$. It is strictly decreasing on $(-\infty, 0]$ and strictly
increasing on $[0, \infty)$, which is why we always say *where* a function is increasing.

:::{admonition} Other books use other words
:class: note
Some books say "increasing" for what we call *strictly increasing*, and "non-decreasing" for
what we call *increasing*. On this site the words always mean exactly what
[](#def-calc-monotone) says: "increasing" allows level stretches, and "strictly increasing"
does not.
:::

## Worked examples

:::{proof:example} The natural domain of $\frac{\sqrt{x+2}}{x-3}$
:label: eg-calc-functions-natural-domain

Find the natural domain of $f(x) = \dfrac{\sqrt{x+2}}{x-3}$.

1. The square root is a real number only if $x + 2 \ge 0$, that is, $x \ge -2$.
2. The quotient is defined only if the denominator is not zero: $x - 3 \ne 0$, that is,
   $x \ne 3$.
3. Both conditions must hold, so the natural domain is the set of $x \ge -2$ with $x \ne 3$:

$$
\boxed{\dom f = [-2, 3) \cup (3, \infty)}
$$

**Check.** $f(-2) = \frac{0}{-5} = 0$ is defined, so $-2$ belongs to the domain. At $x = -3$ the
formula needs $\sqrt{-1}$, and at $x = 3$ it divides by zero; neither is in the domain. ✓
:::

:::{proof:example} The range of $x^2 - 4x + 5$
:label: eg-calc-functions-range-quadratic

Find the range of $f(x) = x^2 - 4x + 5$, whose domain is $\R$.

1. **Complete the square.** $x^2 - 4x + 5 = (x - 2)^2 + 1$.
2. **Every value is at least $1$.** A square is never negative, so
   $f(x) = (x-2)^2 + 1 \ge 1$ for every $x$. Hence $\ran f \subseteq [1, \infty)$.
3. **Every $y \ge 1$ is a value.** Given $y \ge 1$, the number $y - 1 \ge 0$ has a square
   root ([the remark on square roots](#rem-calc-square-roots)). Put $x = 2 + \sqrt{y - 1}$;
   then $f(x) = \bigl(\sqrt{y-1}\bigr)^2 + 1 = y$. Hence
   $[1, \infty) \subseteq \ran f$.
4. The two inclusions together give

$$
\boxed{\ran f = [1, \infty)}
$$

**Check.** For $y = 10$, step 3 gives $x = 2 + 3 = 5$, and indeed $f(5) = 25 - 20 + 5 = 10$.
The smallest value is $f(2) = 4 - 8 + 5 = 1$. ✓
:::

:::{proof:example} Even, odd or neither?
:label: eg-calc-functions-even-odd

Decide whether each function is even, odd or neither.

1. $f(x) = x^3 - x$. The domain $\R$ is symmetric, and
   $f(-x) = (-x)^3 - (-x) = -x^3 + x = -(x^3 - x) = -f(x)$, so $f$ is odd.
2. $g(x) = \dfrac{1}{x^2 - 1}$. The domain is all $x$ except $1$ and $-1$, which is
   symmetric about $0$, and $g(-x) = \dfrac{1}{(-x)^2 - 1} = \dfrac{1}{x^2 - 1} = g(x)$, so
   $g$ is even.
3. $h(x) = x^2 + x$. As in the non-example above, $h(1) = 2$ and $h(-1) = 0$, so $h$ is
   neither.
4. $k\colon [-1, 2] \to \R$, $k(x) = x^2$. The formula is the same as for an even function,
   but $2 \in \dom k$ while $-2 \notin \dom k$. The domain is not symmetric about $0$, and
   [](#def-calc-even-odd) asks for a symmetric domain both for even and for odd. So $k$ is
   neither even nor odd.

**Check.** $f(2) = 8 - 2 = 6$ and $f(-2) = -8 + 2 = -6 = -f(2)$; $g(3) = \frac{1}{8} = g(-3)$. ✓
:::

:::{proof:example} A function that is increasing on each piece of its domain
:label: eg-calc-functions-monotone

Show that $f(x) = \dfrac{x}{x + 1}$ is strictly increasing on $(-1, \infty)$, and decide whether
it is increasing on its whole domain.

1. **Compare two points.** Let $-1 < x_1 < x_2$. Over a common denominator,
   $$
   f(x_2) - f(x_1) = \frac{x_2 (x_1 + 1) - x_1 (x_2 + 1)}{(x_1 + 1)(x_2 + 1)}
   = \frac{x_2 - x_1}{(x_1 + 1)(x_2 + 1)}.
   $$
2. **Signs.** The numerator is positive because $x_1 < x_2$. Both factors of the denominator
   are positive because $x_1, x_2 > -1$. So $f(x_2) - f(x_1) > 0$, that is,
   $f(x_1) < f(x_2)$. Hence $f$ is strictly increasing on $(-1, \infty)$.
3. **The whole domain.** $\dom f = (-\infty, -1) \cup (-1, \infty)$. The same computation
   shows that $f$ is strictly increasing on $(-\infty, -1)$ as well (there both factors of the
   denominator are negative, so their product is positive). But $f$ is *not* increasing on
   its domain: $-2 < 0$, while $f(-2) = \frac{-2}{-1} = 2 > 0 = f(0)$.

$$
\boxed{\text{strictly increasing on } (-\infty, -1) \text{ and on } (-1, \infty), \text{ but not increasing on } \dom f}
$$

**Check.** $f(0) = 0$, $f(1) = \frac{1}{2}$, $f(3) = \frac{3}{4}$: the values grow, as they
should on $(-1, \infty)$. ✓
:::

:::{proof:example} The largest pen against a wall
:label: eg-calc-functions-pen

A rectangular pen is built against a long wall, with 40 m of fencing for the other three
sides. Express its area as a function of the width $x$ (in metres) of the two sides that meet
the wall, and find the domain and the range of that function.

1. **Model.** The two sides that meet the wall use $2x$ metres of fence, so the side parallel
   to the wall is $40 - 2x$ metres long. The area, in square metres, is
   $$
   A(x) = x(40 - 2x).
   $$
2. **Domain from the context.** The formula makes sense for every real $x$, but a pen needs
   $x > 0$ and $40 - 2x > 0$, that is, $x < 20$. So $\dom A = (0, 20)$.
3. **Range.** Completing the square, $A(x) = 40x - 2x^2 = 200 - 2(x - 10)^2$. Let
   $0 < x < 20$. A square is never negative, so $(x - 10)^2 \ge 0$. Also
   $(x - 10)^2 - 100 = x^2 - 20x = x(x - 20) < 0$, because $x > 0$ and $x - 20 < 0$. So
   $0 \le (x - 10)^2 < 100$, and $0 < A(x) \le 200$. Conversely, let $0 < a \le 200$. Then
   $0 \le \frac{200 - a}{2} < 100$, so $s = \sqrt{(200 - a)/2}$ is a real number with
   $s \ge 0$ and $s^2 < 100 = 10^2$. Squaring keeps the order of non-negative numbers
   ([the remark on square roots](#rem-calc-square-roots)), so $s < 10$. Hence
   $x = 10 - s$ lies in $(0, 10]$, and $A(x) = 200 - 2s^2 = 200 - (200 - a) = a$.
   So $\ran A = (0, 200]$.

$$
\boxed{A(x) = x(40 - 2x) \text{ m}^2, \quad \dom A = (0, 20), \quad \ran A = (0, 200]}
$$

So the largest possible pen has area $200$ m², when $x = 10$ m. Notice that the domain came
from the situation, not from the formula: the natural domain of $x(40 - 2x)$ is all of $\R$.

**Check.** $A(10) = 10 \cdot 20 = 200$, and $A(5) = 5 \cdot 30 = 150 = 200 - 2 \cdot 5^2$. ✓
:::

## Common mistakes

:::{warning} Simplifying before finding the domain
✗ **Wrong:** "$f(x) = \dfrac{x^2 - 1}{x - 1} = x + 1$, so $\dom f = \R$."

**Why:** the natural domain is read from the formula as it is given. At $x = 1$ that formula
is $\frac{0}{0}$, which is not a number. The equation $\frac{x^2-1}{x-1} = x + 1$ only holds for
$x \ne 1$.

✓ **Right:** $\dom f = (-\infty, 1) \cup (1, \infty)$, and $f(x) = x + 1$ for every $x$ in it.
The graph is the line $y = x + 1$ with the point $(1, 2)$ missing.
:::

:::{warning} Decreasing on each piece need not mean decreasing
✗ **Wrong:** "$f(x) = \dfrac{1}{x}$ is decreasing."

**Why:** [](#def-calc-monotone) compares *any* two points of the domain. Here $-1 < 1$, but
$f(-1) = -1 < 1 = f(1)$: the value went up.

✓ **Right:** $f$ is strictly decreasing on $(-\infty, 0)$ and strictly decreasing on
$(0, \infty)$, but it is not decreasing on its domain $(-\infty, 0) \cup (0, \infty)$.
:::

:::{warning} "Odd powers make an odd function"
✗ **Wrong:** "$f(x) = x^3 + 1$ is odd, because $3$ is odd." Or: "every function is either even
or odd."

**Why:** the constant term $1 = 1 \cdot x^0$ is an even power. Test the definition instead:
$f(-1) = 0$ but $-f(1) = -2$, so $f$ is not odd; and $f(-1) \ne f(1) = 2$, so it is not even
either. Most functions are neither.

✓ **Right:** check that the domain is symmetric about $0$, then check $f(-x) = f(x)$ or
$f(-x) = -f(x)$ for *every* $x$ in it; to rule one out, a single $x$ where it fails is
enough.
:::

## Rigorous track

:::{admonition} What a "rule" is
:class: dropdown rigor
[](#def-calc-function) speaks of a *rule*, which is not a precise mathematical object. The
standard way to make it precise is to identify a function with its graph. A function from
$A$ to $B$ is a subset $G \subseteq A \times B$ of ordered pairs such that
$$
\forall x \in A \ \ \exists!\, y \in B : (x, y) \in G,
$$
where $\exists!$ means "there exists exactly one". The value $f(x)$ is that unique $y$. With
this definition a function *is* its set of input–output pairs, and the vertical line test
is just the condition "exactly one $y$ for each $x$" drawn in the plane.
:::

:::{admonition} When are two functions equal?
:class: dropdown rigor
Two functions $f$ and $g$ are equal when $\dom f = \dom g$ and $f(x) = g(x)$ for every $x$ in
that common domain. The domain is part of the function, not an afterthought:

- $x \mapsto x + 1$ on $\R$ and $x \mapsto \frac{x^2 - 1}{x - 1}$ (natural domain) are
  different functions: one is defined at $1$ and the other is not.
- $x \mapsto x^2$ on $\R$ is not monotone, but the "same" formula on $[0, \infty)$ is strictly
  increasing. Restricting the domain in this way is how inverse functions such as $\sqrt{x}$
  are obtained later in the course.

Some books also count the codomain as part of a function, so that $x \mapsto x^2$ as a map
$\R \to \R$ and as a map $\R \to [0, \infty)$ are different. Nothing in this course depends on
that distinction.
:::

## Summary

- A function $f\colon A \to B$ assigns to each $x \in A$ *exactly one* value $f(x)$; its graph
  is the set of points $(x, f(x))$, and no vertical line meets it twice.
- $\dom f$ is the set of inputs; $\ran f = \{f(x) : x \in \dom f\}$ is the set of values. A
  formula with no stated domain has its natural domain. To find a range, show both inclusions.
- In a model, the domain comes from the situation, not only from the formula.
- *Even* means that $\dom f$ is symmetric about $0$ and $f(-x) = f(x)$ (mirror symmetry in
  the $y$-axis); *odd* means that $\dom f$ is symmetric about $0$ and $f(-x) = -f(x)$
  (half-turn symmetry about the origin). A function whose domain is not symmetric is
  neither.
- *Increasing* on $S$: $x_1 < x_2$ implies $f(x_1) \le f(x_2)$. *Strictly increasing*:
  $x_1 < x_2$ implies $f(x_1) < f(x_2)$. Always say on which set.

## Exercises

::::{exercise} The domain of a square root
:label: exr-calc-functions-domain-root
:class: tier-a

Find the natural domain of the function $f$ given by $f(x) = \sqrt{6 - 2x}$.

:::{admonition} Hint 1
:class: dropdown hint
A square root of a real number is defined only when that number is $\ge 0$.
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, 3]$
:::
::::

::::{solution} exr-calc-functions-domain-root
:label: sol-calc-functions-domain-root
:class: dropdown
We need $6 - 2x \ge 0$, that is, $2x \le 6$, that is, $x \le 3$. So
$\dom f = (-\infty, 3]$. At the endpoint, $f(3) = \sqrt{0} = 0$ is defined, so $3$ belongs to
the domain.
::::

::::{exercise} The domain of a quotient
:label: exr-calc-functions-domain-rational
:class: tier-a

Find the natural domain of the function $g$ given by $g(x) = \dfrac{x + 1}{x^2 - 4}$.

:::{admonition} Hint 1
:class: dropdown hint
Which values of $x$ make the denominator zero? Does a zero numerator cause any problem?
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, -2), (-2, 2), (2, \infty)$ (the union of these three intervals)
:::
::::

::::{solution} exr-calc-functions-domain-rational
:label: sol-calc-functions-domain-rational
:class: dropdown
The quotient is defined unless the denominator is zero. Since $x^2 - 4 = (x - 2)(x + 2)$, it
is zero exactly when $x = 2$ or $x = -2$. A zero numerator (at $x = -1$) is no problem:
$g(-1) = \frac{0}{-3} = 0$. So
$\dom g = (-\infty, -2) \cup (-2, 2) \cup (2, \infty)$, all real numbers except $\pm 2$.
::::

::::{exercise} Is it odd?
:label: exr-calc-functions-odd-check
:class: tier-a

True or false: the function $f$ given by $f(x) = x^5 - x^3 + 1$ is odd.

:::{admonition} Hint 1
:class: dropdown hint
Compare $f(-1)$ with $-f(1)$.
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-functions-odd-check
:label: sol-calc-functions-odd-check
:class: dropdown
The domain $\R$ is symmetric about $0$. We have $f(1) = 1 - 1 + 1 = 1$ and
$f(-1) = -1 + 1 + 1 = 1$, so $f(-1) = 1 \ne -1 = -f(1)$. The condition of
[](#def-calc-even-odd) fails at $x = 1$, so $f$ is not odd. (Without the constant term,
$x^5 - x^3$ would be odd.)
::::

::::{exercise} A circle and the vertical line test
:label: exr-calc-functions-vertical-line
:class: tier-a

True or false: the unit circle, the set of points $(x, y)$ with $x^2 + y^2 = 1$, is the graph
of a function of $x$.

:::{admonition} Hint 1
:class: dropdown hint
How many points of the circle lie on the vertical line $x = 0$?
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-functions-vertical-line
:label: sol-calc-functions-vertical-line
:class: dropdown
The vertical line $x = 0$ meets the circle at $(0, 1)$ and at $(0, -1)$, because both satisfy
$0^2 + y^2 = 1$. A function assigns only one value to $x = 0$, so the circle is not the graph
of a function of $x$. Its upper half is: it is the graph of $x \mapsto \sqrt{1 - x^2}$ on
$[-1, 1]$.
::::

::::{exercise} Which boxes can be made?
:label: exr-calc-functions-box-domain
:class: tier-a applied

An open box is made from a square sheet of card, 30 cm by 30 cm, by cutting a square of side
$x$ cm from each corner and folding up the four flaps. For which values of $x$ does this give
a box? Write the set of these $x$ as an interval.

:::{admonition} Hint 1
:class: dropdown hint
The height of the box is $x$ and each side of its base is $30 - 2x$. Both must be positive.
:::

:::{admonition} Answer
:class: dropdown answer set
$(0, 15)$
:::
::::

::::{solution} exr-calc-functions-box-domain
:label: sol-calc-functions-box-domain
:class: dropdown
Cutting a square of side $x$ from each corner leaves a base of side $30 - 2x$ cm, and the flaps
give a height of $x$ cm. A box needs $x > 0$ (otherwise nothing is folded up) and
$30 - 2x > 0$, that is, $x < 15$ (otherwise there is no base). So the possible values form the
interval $(0, 15)$.
::::

::::{exercise} The volume of the box
:label: exr-calc-functions-box-volume
:class: tier-b applied

For the box of [](#exr-calc-functions-box-domain), write the volume $V(x)$, in cubic
centimetres, as a function of $x$.

:::{admonition} Hint 1
:class: dropdown hint
Volume is the area of the base times the height.
:::

:::{admonition} Answer
:class: dropdown answer
$x \cdot (30 - 2x)^2$ (in cm³)
:::
::::

::::{solution} exr-calc-functions-box-volume
:label: sol-calc-functions-box-volume
:class: dropdown
The base is a square of side $30 - 2x$ cm, so its area is $(30 - 2x)^2$ cm², and the height is
$x$ cm. Hence $V(x) = x(30 - 2x)^2$ cm³, with domain $(0, 15)$ from
[](#exr-calc-functions-box-domain). For example, $x = 5$ gives a box $20$ cm by $20$ cm by
$5$ cm, of volume $V(5) = 5 \cdot 20^2 = 2000$ cm³.
::::

::::{exercise} The range of $\frac{1}{x^2 + 1}$
:label: exr-calc-functions-range-reciprocal
:class: tier-b

Find the range of the function $f$ given by $f(x) = \dfrac{1}{x^2 + 1}$.

:::{admonition} Hint 1
:class: dropdown hint
How small can $x^2 + 1$ be? What does that say about its reciprocal?
:::

:::{admonition} Hint 2
:class: dropdown hint
To show that a number $y$ is a value, solve $\frac{1}{x^2 + 1} = y$ for $x$.
:::

:::{admonition} Answer
:class: dropdown answer set
$(0, 1]$
:::
::::

::::{solution} exr-calc-functions-range-reciprocal
:label: sol-calc-functions-range-reciprocal
:class: dropdown
The denominator is never zero, so $\dom f = \R$.

*Every value lies in $(0, 1]$.* For every $x$, $x^2 + 1 \ge 1 > 0$. A positive number has a
positive reciprocal, and a number $\ge 1$ has a reciprocal $\le 1$, so $0 < f(x) \le 1$.

*Every $y \in (0, 1]$ is a value.* Given $0 < y \le 1$, we have $\frac{1}{y} \ge 1$, so
$x = \sqrt{\frac{1}{y} - 1}$ is a real number
([the remark on square roots](#rem-calc-square-roots)), and
$f(x) = \frac{1}{\left(\frac{1}{y} - 1\right) + 1} = \frac{1}{1/y} = y$.

So $\ran f = (0, 1]$. The value $1$ is taken at $x = 0$; the value $0$ is never taken.
::::

::::{exercise} The range of a quotient of linear functions
:label: exr-calc-functions-range-quotient
:class: tier-b

Find the range of the function $g$ given by $g(x) = \dfrac{2x + 1}{x - 1}$.

:::{admonition} Hint 1
:class: dropdown hint
Solve $y = \frac{2x + 1}{x - 1}$ for $x$. For which $y$ is there a solution in the domain?
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, 2), (2, \infty)$ (the union of these two intervals)
:::
::::

::::{solution} exr-calc-functions-range-quotient
:label: sol-calc-functions-range-quotient
:class: dropdown
The domain is all $x \ne 1$. A number $y$ is in $\ran g$ exactly when the equation
$\frac{2x + 1}{x - 1} = y$ has a solution $x \ne 1$. For $x \ne 1$ we may multiply by $x - 1$,
so the equation is equivalent to
$$
2x + 1 = y(x - 1) \iff (y - 2)\,x = y + 1 .
$$

- If $y = 2$, this reads $0 = 3$, which has no solution. So $2 \notin \ran g$.
- If $y \ne 2$, the solution is $x = \frac{y + 1}{y - 2}$. It is never $1$, because
  $\frac{y + 1}{y - 2} = 1$ would mean $y + 1 = y - 2$. So this $x$ is in the domain, and
  $g(x) = y$.

Hence $\ran g = (-\infty, 2) \cup (2, \infty)$: every real number except $2$.
::::

::::{exercise} Increasing on $[0, \infty)$?
:label: exr-calc-functions-monotone-parabola
:class: tier-b

True or false: the function $f$ given by $f(x) = x^2 - 2x$ is increasing on $[0, \infty)$.

:::{admonition} Hint 1
:class: dropdown hint
Complete the square, or compute $f(0)$ and $f(1)$.
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-functions-monotone-parabola
:label: sol-calc-functions-monotone-parabola
:class: dropdown
Take $x_1 = 0$ and $x_2 = 1$ in $[0, \infty)$. Then $x_1 < x_2$, but $f(0) = 0 > -1 = f(1)$,
so the condition of [](#def-calc-monotone) fails. Completing the square,
$f(x) = (x - 1)^2 - 1$, shows the full picture: $f$ is strictly decreasing on $[0, 1]$ and
strictly increasing on $[1, \infty)$.
::::

::::{exercise} Reading the range from a sketch
:label: exr-calc-functions-piecewise-range
:class: tier-b

Sketch the graph of
$$
f(x) =
\begin{cases}
-x, & x < 0, \\
x^2 - 2x, & 0 \le x \le 3,
\end{cases}
$$
and use it to find the range of $f$.

:::{admonition} Hint 1
:class: dropdown hint
The domain is $(-\infty, 3]$. Find the values of each piece separately, then combine them.
:::

:::{admonition} Hint 2
:class: dropdown hint
On $[0, 3]$, complete the square: $x^2 - 2x = (x - 1)^2 - 1$.
:::

:::{admonition} Answer
:class: dropdown answer set
$[-1, \infty)$
:::
::::

::::{solution} exr-calc-functions-piecewise-range
:label: sol-calc-functions-piecewise-range
:class: dropdown
**Sketch.** For $x < 0$ the graph is the line $y = -x$, rising to the left and approaching
the origin from the left. For $0 \le x \le 3$ it is the parabola
$y = (x - 1)^2 - 1$, from $(0, 0)$ down to its lowest point $(1, -1)$ and up to $(3, 3)$. The
two pieces meet at the origin.

**Left piece.** For $x < 0$ the values $-x$ are positive, and every $y > 0$ is taken (at
$x = -y$). So this piece contributes $(0, \infty)$.

**Right piece.** Let $0 \le x \le 3$, so that $-1 \le x - 1 \le 2$. A square is never
negative, so $(x - 1)^2 \ge 0$. For the upper bound we cannot square the two inequalities
term by term, because $x - 1$ may be negative; we split into two cases.

- If $x - 1 \ge 0$: multiplying $x - 1 \le 2$ by $x - 1 \ge 0$ gives
  $(x - 1)^2 \le 2(x - 1)$, and multiplying $x - 1 \le 2$ by $2 > 0$ gives
  $2(x - 1) \le 4$, so $(x - 1)^2 \le 4$.
- If $x - 1 < 0$: multiplying $-1 \le x - 1$ by the negative number $x - 1$ reverses the
  inequality and gives $(x - 1)^2 \le -(x - 1)$, and multiplying $-1 \le x - 1$ by $-1$
  gives $-(x - 1) \le 1$, so $(x - 1)^2 \le 1 \le 4$.

In both cases $0 \le (x - 1)^2 \le 4$, so $-1 \le f(x) \le 3$. Conversely, let
$y \in [-1, 3]$. Then $y + 1 \ge 0$ has a square root $s = \sqrt{y + 1} \ge 0$
([the remark on square roots](#rem-calc-square-roots)), and
$s \le 2$: if $s > 2$, then $s^2 > 2s > 4$, but $s^2 = y + 1 \le 4$. So $x = 1 + s$ lies in
$[1, 3]$, and $f(x) = s^2 - 1 = y$. So this piece contributes $[-1, 3]$.

**Together.** $\ran f = [-1, 3] \cup (0, \infty) = [-1, \infty)$, with the smallest value
$f(1) = -1$.
::::

::::{exercise} The square root is strictly increasing
:label: exr-calc-functions-sqrt-increasing
:class: tier-c

Show from [](#def-calc-monotone) that $x \mapsto \sqrt{x}$ is strictly increasing on
$[0, \infty)$.

:::{admonition} Hint 1
:class: dropdown hint
For $0 \le x_1 < x_2$, multiply $\sqrt{x_2} - \sqrt{x_1}$ by
$\frac{\sqrt{x_2} + \sqrt{x_1}}{\sqrt{x_2} + \sqrt{x_1}}$. Why is that denominator not zero?
:::

:::{admonition} Answer
:class: dropdown answer manual
For $0 \le x_1 < x_2$, $\sqrt{x_2} - \sqrt{x_1} = \dfrac{x_2 - x_1}{\sqrt{x_2} + \sqrt{x_1}} > 0$.
:::
::::

::::{solution} exr-calc-functions-sqrt-increasing
:label: sol-calc-functions-sqrt-increasing
:class: dropdown
We show that $\sqrt{x_2} - \sqrt{x_1} > 0$ by rationalising: multiplying and dividing by
$\sqrt{x_2} + \sqrt{x_1}$ turns the difference of the roots into $x_2 - x_1$. Recall that each
$x \ge 0$ has exactly one square root $\sqrt{x} \ge 0$, and $\bigl(\sqrt{x}\bigr)^2 = x$
([the remark on square roots](#rem-calc-square-roots)).

Let $0 \le x_1 < x_2$. Then $x_2 > 0$, so $\sqrt{x_2} > 0$ (since $\sqrt{x_2} = 0$ would give
$x_2 = 0^2 = 0$), and $\sqrt{x_1} \ge 0$; hence $\sqrt{x_2} + \sqrt{x_1} > 0$. Using $(a - b)(a + b) = a^2 - b^2$,
$$
\sqrt{x_2} - \sqrt{x_1}
= \frac{\bigl(\sqrt{x_2} - \sqrt{x_1}\bigr)\bigl(\sqrt{x_2} + \sqrt{x_1}\bigr)}{\sqrt{x_2} + \sqrt{x_1}}
= \frac{x_2 - x_1}{\sqrt{x_2} + \sqrt{x_1}} .
$$
The numerator and the denominator are both positive, so $\sqrt{x_1} < \sqrt{x_2}$. As
$x_1 < x_2$ in $[0, \infty)$ were arbitrary, the square root is strictly increasing on
$[0, \infty)$.
::::

::::{exercise} Odd functions vanish at zero
:label: exr-calc-functions-odd-at-zero
:class: tier-c

Let $f$ be an odd function with $0 \in \dom f$. Show that $f(0) = 0$. Use this to give a
second reason why $x \mapsto x^3 + 1$ is not odd.

:::{admonition} Hint 1
:class: dropdown hint
Put $x = 0$ in the condition $f(-x) = -f(x)$.
:::

:::{admonition} Answer
:class: dropdown answer manual
$f(0) = f(-0) = -f(0)$, so $2f(0) = 0$; and $0^3 + 1 = 1 \ne 0$.
:::
::::

::::{solution} exr-calc-functions-odd-at-zero
:label: sol-calc-functions-odd-at-zero
:class: dropdown
We put $x = 0$ in the condition that defines an odd function. Since $f$ is odd and
$0 \in \dom f$, the condition $f(-x) = -f(x)$ holds for $x = 0$. As
$-0 = 0$, it says $f(0) = -f(0)$, so $2 f(0) = 0$ and $f(0) = 0$.

The function $x \mapsto x^3 + 1$ has domain $\R$, which contains $0$, and its value there is
$0^3 + 1 = 1 \ne 0$. If it were odd, its value at $0$ would be $0$; so it is not odd.
::::

::::{exercise} The cube is strictly increasing
:label: exr-calc-functions-cube-increasing
:class: tier-c

Show from [](#def-calc-monotone) that $x \mapsto x^3$ is strictly increasing on $\R$.

:::{admonition} Hint 1
:class: dropdown hint
For $x_1 < x_2$, factor $x_2^3 - x_1^3 = (x_2 - x_1)\bigl(x_2^2 + x_1 x_2 + x_1^2\bigr)$.
:::

:::{admonition} Hint 2
:class: dropdown hint
Complete the square in the second factor:
$x_2^2 + x_1 x_2 + x_1^2 = \bigl(x_1 + \tfrac{1}{2} x_2\bigr)^2 + \tfrac{3}{4} x_2^2$. When
can this be zero?
:::

:::{admonition} Answer
:class: dropdown answer manual
$x_2^3 - x_1^3 = (x_2 - x_1)\bigl(\bigl(x_1 + \tfrac{1}{2}x_2\bigr)^2 + \tfrac{3}{4}x_2^2\bigr)$,
and both factors are positive when $x_1 < x_2$.
:::
::::

::::{solution} exr-calc-functions-cube-increasing
:label: sol-calc-functions-cube-increasing
:class: dropdown
We show that $x_2^3 - x_1^3 > 0$ whenever $x_1 < x_2$, by factoring. Let $x_1 < x_2$. Expanding
the right-hand side confirms
$$
x_2^3 - x_1^3 = (x_2 - x_1)\bigl(x_2^2 + x_1 x_2 + x_1^2\bigr),
\qquad
x_2^2 + x_1 x_2 + x_1^2 = \Bigl(x_1 + \frac{x_2}{2}\Bigr)^2 + \frac{3}{4} x_2^2 .
$$
The first factor is positive. The second is a sum of two squares, so it is $\ge 0$, and it is
$0$ only if both squares are $0$: $x_2 = 0$ and $x_1 = -\frac{x_2}{2} = 0$. That would give
$x_1 = x_2$, which is impossible. So the second factor is positive too, and
$x_2^3 - x_1^3 > 0$, that is, $x_1^3 < x_2^3$.
::::

::::{exercise} Every function is even plus odd
:label: exr-calc-functions-even-odd-decomposition
:class: tier-c

Let $f$ be any function with domain $\R$. Show that there are exactly one even function $g$
and exactly one odd function $h$, both with domain $\R$, such that $f(x) = g(x) + h(x)$ for
every $x$. Find $g$ and $h$ when $f(x) = x^2 + x + 1$.

:::{admonition} Hint 1
:class: dropdown hint
Suppose $f = g + h$ works. Write down $f(x)$ and $f(-x)$ in terms of $g(x)$ and $h(x)$.
:::

:::{admonition} Hint 2
:class: dropdown hint
Add and subtract the two equations of Hint 1 to find $g(x)$ and $h(x)$. Then check that the
functions you found really work.
:::

:::{admonition} Answer
:class: dropdown answer manual
$g(x) = \frac{f(x) + f(-x)}{2}$ and $h(x) = \frac{f(x) - f(-x)}{2}$; for
$f(x) = x^2 + x + 1$ these are $g(x) = x^2 + 1$ and $h(x) = x$.
:::
::::

::::{solution} exr-calc-functions-even-odd-decomposition
:label: sol-calc-functions-even-odd-decomposition
:class: dropdown
We first show that $g$ and $h$ are forced (so there is at most one pair), then that the forced
pair works.

*At most one pair.* Suppose $g$ is even, $h$ is odd and $f(x) = g(x) + h(x)$ for every $x$.
Applying this at $-x$ gives $f(-x) = g(-x) + h(-x) = g(x) - h(x)$. Adding and subtracting the
two equations,
$$
g(x) = \frac{f(x) + f(-x)}{2}, \qquad h(x) = \frac{f(x) - f(-x)}{2}
$$
for every $x$. So $g$ and $h$ are determined by $f$.

*This pair works.* Define $g$ and $h$ by these formulas. Then $g(x) + h(x) = f(x)$, their
common domain $\R$ is symmetric about $0$, and
$$
g(-x) = \frac{f(-x) + f(x)}{2} = g(x), \qquad h(-x) = \frac{f(-x) - f(x)}{2} = -h(x),
$$
so $g$ is even and $h$ is odd.

*The example.* For $f(x) = x^2 + x + 1$ we have $f(-x) = x^2 - x + 1$, so
$g(x) = \frac{2x^2 + 2}{2} = x^2 + 1$ and $h(x) = \frac{2x}{2} = x$.
::::

## Where this leads

:::{where-this-leads}
:::

:::{admonition} Looking ahead
:class: looking-ahead
Checking monotonicity from the definition, as in the worked examples, takes some algebra. The
page *Monotonicity and the First Derivative Test* shows that the sign of the derivative
decides it far more quickly. The page *Inverse Functions* shows that a strictly monotone
function never takes the same value twice, so it has an inverse.
:::
