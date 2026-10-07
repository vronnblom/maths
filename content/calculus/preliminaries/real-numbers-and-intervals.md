---
title: Real Numbers and Intervals
label: calc-real-numbers
description: >-
  The number systems from the natural numbers to the real numbers, interval and set-builder
  notation for sets of real numbers, a proof that the square root of 2 is irrational, and,
  in the rigorous track, suprema and the completeness axiom.
tags: [preliminaries, proofs]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 1
  est_minutes: 35
  prerequisites: []
  objectives:
    - Use interval and set-builder notation.
    - Distinguish ℕ, ℤ, ℚ, ℝ.
    - State what "bounded above" and "supremum" mean (rigorous track).
  verify: verify/calculus/preliminaries/test_real_numbers_and_intervals.py
  widgets: []
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

Calculus is about quantities that change without jumps: the position of a car, the
temperature of a cup of coffee, the area under a curve. To describe them we need a number
system with no gaps, and fractions are not enough.

Draw a square whose sides have length $1$. By Pythagoras' theorem its diagonal $d$ satisfies
$d^2 = 1^2 + 1^2 = 2$. Is $d$ a fraction? We prove below that it is not: no fraction squares to
$2$. Yet the diagonal certainly has a length, and swinging it down onto the number line marks
a definite point on it. The **real numbers** are the number system in which every point of the
line is a number, and so every length is one.

:::{figure} ./img/sqrt2-diagonal.svg
:label: fig-calc-real-numbers-diagonal
:alt: A unit square standing on the number line between 0 and 1, with its diagonal drawn from 0. A dashed arc of radius equal to the diagonal swings it down onto the line, where it lands at a point between 1 and 2.

The diagonal of the unit square has length $\sqrt{2}$. Swung down onto the number line, it
marks a point between $1$ and $2$ that no fraction reaches.
:::

The second half of this page is a language for **sets** of real numbers. Calculus keeps asking
*for which* $x$ something holds: $\sqrt{x - 1}$ is defined exactly when $x \ge 1$, and a
function may increase only for $x$ between two values. Intervals and set-builder notation say
such things briefly and precisely.

## The number systems

We use four number systems, each contained in the next:

- the **natural numbers** $\N = \{0, 1, 2, 3, \dots\}$, for counting. On this site $\N$
  contains $0$; when we mean the positive integers we write "$n \ge 1$";
- the **integers** $\Z = \{\dots, -2, -1, 0, 1, 2, \dots\}$;
- the **rational numbers** $\Q$, the fractions $\frac{p}{q}$ with $p$ and $q$ integers and
  $q \ne 0$. The same rational number has many such forms: $\frac{1}{2} = \frac{2}{4} = \frac{-3}{-6}$;
- the **real numbers** $\R$, the points of the number line. A real number that is not rational
  is called **irrational**.

$$
\N \subset \Z \subset \Q \subset \R .
$$

Every integer $n$ is rational, because $n = \frac{n}{1}$. The number $\sqrt{2}$ is irrational
([](#thm-calc-sqrt2-irrational) below), and so is $\pi$, although that proof is harder and we
do not need it.

**Decimals.** Every real number has a decimal expansion, such as $\frac{1}{4} = 0.25$,
$\frac{1}{3} = 0.333\ldots$ or $\sqrt{2} = 1.41421\ldots$. A bar marks a block of digits that
repeats for ever: $0.\overline{3} = 0.333\ldots$ and $0.1\overline{25} = 0.1252525\ldots$. The
decimals tell rational and irrational numbers apart:

- The decimal expansion of a rational number $\frac{p}{q}$ terminates or eventually repeats.
  When we divide $p$ by $q$ by long division, each remainder is one of $0, 1, \dots, q - 1$, so
  after at most $q$ steps a remainder comes back, and from then on the digits repeat.
- Conversely, a decimal that terminates or eventually repeats is rational:
  [](#eg-calc-real-numbers-repeating-decimal) shows the method.

So the irrational numbers are exactly the real numbers whose decimals go on for ever without
repeating. A decimal approximation such as $\sqrt{2} \approx 1.4142$ is a rational number close
to $\sqrt{2}$, never $\sqrt{2}$ itself.

**Order.** For any two real numbers $a$ and $b$, exactly one of $a < b$, $a = b$ and $a > b$
holds; on the number line, $a < b$ means that $a$ lies to the left of $b$. We write $a \le b$
for "$a < b$ or $a = b$".

## Sets and intervals

A **set** is a collection of objects, its **elements**. We write $x \in A$ for "$x$ is an
element of $A$" and $x \notin A$ for its negation. A small set can be listed in braces, as in
$\{1, 2, 3\}$. Most sets in calculus are described by a condition instead, in **set-builder
notation**:
$$
\{x \in \R : x > 0\}
$$
is read "the set of all real numbers $x$ such that $x > 0$". The **empty set** $\emptyset$ has
no elements. For sets $A$ and $B$:

| Notation | Read as | Its elements |
|---|---|---|
| $A \subseteq B$ | $A$ is a subset of $B$ | every element of $A$ is an element of $B$ |
| $A \cap B$ | $A$ intersect $B$ | the $x$ with $x \in A$ **and** $x \in B$ |
| $A \cup B$ | $A$ union $B$ | the $x$ with $x \in A$ **or** $x \in B$ (or both) |
| $A \setminus B$ | $A$ minus $B$ | the $x$ with $x \in A$ and $x \notin B$ |

The sets of real numbers that calculus uses most are intervals: all the numbers between two
endpoints, or all the numbers on one side of a point.

:::{proof:definition} Interval
:label: def-calc-interval

Let $a$ and $b$ be real numbers with $a < b$. The **bounded intervals** with **endpoints** $a$
and $b$ are
$$
\begin{aligned}
[a, b] &= \{x \in \R : a \le x \le b\}, & (a, b) &= \{x \in \R : a < x < b\}, \\
[a, b) &= \{x \in \R : a \le x < b\}, & (a, b] &= \{x \in \R : a < x \le b\}.
\end{aligned}
$$
For a real number $c$, the **unbounded intervals** are
$$
\begin{aligned}
[c, \infty) &= \{x \in \R : x \ge c\}, & (c, \infty) &= \{x \in \R : x > c\}, \\
(-\infty, c] &= \{x \in \R : x \le c\}, & (-\infty, c) &= \{x \in \R : x < c\},
\end{aligned}
$$
and $(-\infty, \infty) = \R$. An **interval** is a set of one of these nine forms. The
intervals $(a, b)$, $(c, \infty)$, $(-\infty, c)$ and $\R$ are called **open**, and $[a, b]$ is
called a **closed interval**.
:::

**In words.** A square bracket means that the endpoint belongs to the interval, a round bracket
that it does not. The symbols $\infty$ and $-\infty$ are not real numbers: they only say that
the interval has no end on that side, so they always get a round bracket. We ask for $a < b$ so
that every interval contains more than one number.

**Example.** $\{x \in \R : -1 \le x < 3\} = [-1, 3)$ contains ${-1}$, $0$, $2.9$ and $\sqrt{2}$,
but not $3$. On the number line we draw the included endpoint as a filled dot and the excluded
one as a hollow dot ([](#fig-calc-real-numbers-intervals)).

:::{figure} ./img/intervals-number-line.svg
:label: fig-calc-real-numbers-intervals
:alt: Two number lines marked from −2 to 4. On the first, a thick segment runs from −1, drawn as a filled dot, to 3, drawn as a hollow dot. On the second, a thick ray starts at a hollow dot at 2 and continues past 4 with an arrow.

The interval $[-1, 3)$ (top): the filled dot shows that ${-1}$ belongs to it, the hollow dot that
$3$ does not. The interval $(2, \infty)$ (bottom) starts just after $2$ and has no right end.
:::

**Non-example.** An interval has no gaps: if two numbers lie in an interval, so does every
number between them. The set $\{x \in \R : x \ne 0\}$ is therefore not an interval: it contains
${-1}$ and $1$ but not $0$, which lies between them. It is the union $(-\infty, 0) \cup (0, \infty)$
of two intervals. The set $\Z$ of integers is not an interval either: it contains $1$ and $2$ but
not $1.5$.

## Main results

We use square roots throughout calculus, and the next pages cite this fact about them.

:::{proof:remark} Square roots
:label: rem-calc-square-roots

For every real number $y \ge 0$ there is exactly one real number $s \ge 0$ with $s^2 = y$. It is
called the **square root** of $y$ and written $\sqrt{y}$. For example $\sqrt{9} = 3$ (and not
${-3}$, although $(-3)^2 = 9$ too), $\sqrt{0} = 0$ and $\sqrt{2} = 1.41421\ldots$. A negative
number has no real square root, because $s^2 \ge 0$ for every real number $s$.
:::

The proof below uses two facts about whole numbers:

- every integer is either **even**, of the form $2m$ with $m \in \Z$, or **odd**, of the form
  $2m + 1$ with $m \in \Z$, and not both;
- every non-empty set of positive integers has a smallest element (the **well-ordering
  principle**).

:::{proof:theorem} The square root of 2 is irrational
:label: thm-calc-sqrt2-irrational

There is no rational number $r$ with $r^2 = 2$. In particular, $\sqrt{2}$ is irrational.
:::

:::{proof:proof}
:enumerated: false
We argue by contradiction: we assume that some rational number squares to $2$ and deduce
something impossible.

Suppose that $r$ is rational and $r^2 = 2$. Then $r \ne 0$, and $(-r)^2 = r^2 = 2$ as well, so
we may assume that $r > 0$ (otherwise we replace $r$ by $-r$). Then $r = \frac{p}{q}$ with
positive integers $p$ and $q$. Among all such ways of writing $r$, we choose one with the
smallest possible denominator $q$; there is one, by the well-ordering principle.

1. From $\frac{p^2}{q^2} = 2$ we get $p^2 = 2q^2$, so $p^2$ is even.
2. Then $p$ is even. Otherwise $p$ is odd, $p = 2m + 1$ with $m \in \Z$, and
   $p^2 = 4m^2 + 4m + 1 = 2(2m^2 + 2m) + 1$ is odd, which contradicts step 1.
3. So $p = 2k$ with $k$ a positive integer. Then $4k^2 = 2q^2$, that is $q^2 = 2k^2$, so $q^2$
   is even, and the argument of step 2 shows that $q$ is even: $q = 2l$ with $l$ a positive
   integer.
4. Now $r = \frac{p}{q} = \frac{2k}{2l} = \frac{k}{l}$ with positive integers $k$ and $l$, and
   the denominator $l = \frac{q}{2}$ is smaller than $q$. This contradicts the choice of $q$ as
   the smallest possible denominator.

So no rational number squares to $2$. Since $\sqrt{2}$ is the positive real number whose square
is $2$, it is not rational.
:::

:::{proof:remark} Why the proof does not show that $\sqrt{4}$ is irrational
:label: rem-calc-sqrt4-rational

The same steps for $p^2 = 4q^2$ give $p = 2k$, and then $4k^2 = 4q^2$, that is $k = q$: no
contradiction, and indeed $\sqrt{4} = 2 = \frac{2}{1}$. For $2$, the factor $2$ comes back in
step 3 ($q^2 = 2k^2$) and makes $q$ even; for $4$ it cancels completely. The same idea proves
that $\sqrt{3}$ is irrational ([](#exr-calc-real-numbers-sqrt3-irrational)).
:::

Here, as in [](#rem-calc-square-roots), we have taken from school that $\sqrt{2}$ exists: that
there is a positive real number whose square is $2$. The rigorous track shows that this is
exactly what the **completeness** of $\R$ guarantees, and what $\Q$ lacks, and proves
[](#rem-calc-square-roots) for every $y \ge 0$.

## Worked examples

:::{proof:example} Write $\{x \in \R : x > -1 \text{ and } x \le 3\}$ as an interval
:label: eg-calc-real-numbers-set-to-interval

**Goal.** Find the interval whose elements are exactly the real numbers that satisfy both
conditions.

1. The two conditions together say $-1 < x \le 3$.
2. The left endpoint ${-1}$ is excluded ($x > -1$ is strict), so it gets a round bracket.
3. The right endpoint $3$ is included ($x \le 3$), so it gets a square bracket.

$$
\boxed{(-1, 3]}
$$

**Check.** $x = 3$ satisfies both conditions and lies in $(-1, 3]$; $x = -1$ fails $x > -1$
and is not in $(-1, 3]$; $x = 0$ is in both. ✓
:::

:::{proof:example} Find $A \cap B$ and $A \cup B$ for $A = [-2, 3)$ and $B = (1, 5]$
:label: eg-calc-real-numbers-intersection-union

**Goal.** Describe the numbers in both intervals, and the numbers in at least one of them.

1. $x \in A$ means $-2 \le x < 3$, and $x \in B$ means $1 < x \le 5$.
2. **Intersection.** Both hold when $x$ is larger than ${-2}$ and $1$, the larger left endpoint,
   and smaller than $3$ and $5$, the smaller right endpoint: $1 < x < 3$. The endpoint $1$ is
   excluded because $1 \notin B$, and $3$ because $3 \notin A$.
3. **Union.** The intervals overlap (on $(1, 3)$), so together they leave no gap: their union
   runs from the left end of $A$ to the right end of $B$. Since $-2 \in A$ and $5 \in B$, both
   endpoints are included.

$$
\boxed{A \cap B = (1, 3), \qquad A \cup B = [-2, 5]}
$$

**Check.** $x = 2$ lies in $A$ and in $B$, and in $(1, 3)$. $x = 4$ lies in $B$ only, so it is in
the union but not the intersection. $x = 3$ is in $B$ (so in the union) but not in $A$ (so not in
the intersection). ✓
:::

:::{proof:example} Write $0.\overline{36}$ as a fraction
:label: eg-calc-real-numbers-repeating-decimal

**Goal.** Find integers $p$ and $q$ with $0.\overline{36} = 0.363636\ldots = \frac{p}{q}$.

1. Let $x = 0.363636\ldots$. The repeating block has two digits, so we multiply by $10^2 = 100$:
   $100x = 36.363636\ldots$.
2. Subtracting, the repeating tails cancel: $100x - x = 36.3636\ldots - 0.3636\ldots = 36$, so
   $99x = 36$.
3. Hence $x = \frac{36}{99} = \frac{4}{11}$, dividing numerator and denominator by $9$.

$$
\boxed{0.\overline{36} = \frac{4}{11}}
$$

**Check.** Long division of $4$ by $11$: $40 = 3 \cdot 11 + 7$, $70 = 6 \cdot 11 + 4$, and the
remainder $4$ is back, so $\frac{4}{11} = 0.3636\ldots$. ✓
:::

:::{proof:example} The acceptable lengths of a bolt
:label: eg-calc-real-numbers-tolerance

**Goal.** A bolt must be $40\,\text{mm}$ long, with a tolerance of $0.5\,\text{mm}$: it is
accepted if its length differs from $40\,\text{mm}$ by at most $0.5\,\text{mm}$. Write the set
of acceptable lengths as an interval.

1. Let $L$ be the length in millimetres. "Differs by at most $0.5$" means
   $40 - 0.5 \le L \le 40 + 0.5$, that is $39.5 \le L \le 40.5$.
2. Both endpoints are accepted ("at most"), so both get square brackets.

$$
\boxed{L \in [39.5, 40.5] \text{ (in mm)}}
$$

**Check.** A bolt of $40.3\,\text{mm}$ differs from $40\,\text{mm}$ by $0.3\,\text{mm}$ and is
accepted; one of $40.6\,\text{mm}$ differs by $0.6\,\text{mm}$ and is rejected, and indeed
$40.6 \notin [39.5, 40.5]$. The interval has length $1\,\text{mm}$, twice the tolerance. ✓
:::

## Common mistakes

:::{warning} A square bracket at infinity
✗ **Wrong:** "$\{x \in \R : x \ge 3\} = [3, \infty]$."

**Why:** $\infty$ is not a real number, so it cannot be an element of a set of real numbers. The
symbol only says that the interval has no right end.

✓ **Right:** $\{x \in \R : x \ge 3\} = [3, \infty)$, with a round bracket at $\infty$, always.
:::

:::{warning} Reading an interval as a list of whole numbers
✗ **Wrong:** "The interval $(2, 5)$ contains $3$ and $4$." (as if these were all its elements)

**Why:** an interval contains *every* real number between its endpoints, not only the integers:
$2.5$, $\sqrt{5}$ and $\pi$ are in $(2, 5)$ too. The set $\{3, 4\}$, in braces, has only two
elements.

✓ **Right:** $(2, 5) = \{x \in \R : 2 < x < 5\}$, and the integers in it are $3$ and $4$.
:::

:::{warning} Treating a decimal approximation as the number
✗ **Wrong:** "$\sqrt{2} = 1.4142$."

**Why:** $1.4142 = \frac{14142}{10000}$ is rational, and $\sqrt{2}$ is not
([](#thm-calc-sqrt2-irrational)). Indeed $1.4142^2 = 1.99996164 \ne 2$.

✓ **Right:** $\sqrt{2} \approx 1.4142$ (to $4$ decimal places), or keep the exact value
$\sqrt{2}$.
:::

## Rigorous track

What makes $\R$ different from $\Q$? Both allow the four arithmetic operations, and both are
ordered. The difference is that $\R$ has no gaps, and to say this precisely we need upper bounds
and suprema.

:::{proof:definition} Upper bound, bounded above
:label: def-calc-bounded-above

Let $S$ be a subset of $\R$. A real number $u$ is an **upper bound** of $S$ if $s \le u$ for
every $s \in S$. The set $S$ is **bounded above** if it has an upper bound.
:::

**In words.** An upper bound lies on or to the right of every element of $S$. For example $1$,
$2$ and $100$ are upper bounds of $[0, 1)$, and $0.9$ is not, because $0.95 \in [0, 1)$. *Lower
bounds* and *bounded below* are defined in the same way with $s \ge u$, and a set is *bounded*
if it is bounded above and below.

:::{proof:definition} Supremum
:label: def-calc-supremum

Let $S$ be a subset of $\R$. A real number $s$ is a **supremum** (or **least upper bound**) of
$S$ if

1. $s$ is an upper bound of $S$, and
2. $s \le u$ for every upper bound $u$ of $S$.

A set has at most one supremum: if $s$ and $s'$ are both suprema, then condition 2 gives
$s \le s'$ and $s' \le s$, so $s = s'$. We write it $\sup S$.
:::

**In words.** The supremum is the smallest upper bound. It need not belong to $S$:
$\sup\, [0, 1) = 1$, because $1$ is an upper bound and every number $u < 1$ fails to be one (the
number $\max\bigl(0, \frac{u + 1}{2}\bigr)$ lies in $[0, 1)$ and is larger than $u$). A useful
consequence: if $s = \sup S$ and $\eps > 0$, then $s - \eps$ is smaller than $s$, so it is not an
upper bound, and some element $x \in S$ satisfies $x > s - \eps$.

:::{proof:axiom} Completeness of $\R$
:label: ax-calc-completeness

Every non-empty subset of $\R$ that is bounded above has a supremum in $\R$.
:::

**Why "non-empty".** Every real number is an upper bound of the empty set, since $\emptyset$ has
no element to check. So $\emptyset$ is bounded above, but its upper bounds are all of $\R$, which
has no smallest element: $\emptyset$ has no supremum. A set that is not bounded above, such as
$\R$ itself, has no upper bound at all, so no supremum either.

:::{proof:remark} Why an axiom, and where it comes from
:label: rem-calc-completeness-origin

We do not prove the completeness axiom: we take it, together with the rules of arithmetic and of
inequalities, as one of the defining properties of $\R$. The rational numbers satisfy all the
other properties, but not this one: below we find a non-empty set of rationals, bounded above,
with no least upper bound among the rationals.

*Sketch of where it comes from.* The real numbers can be constructed from the rationals. In one
construction (Dedekind cuts) a real number is a way of cutting $\Q$ into a lower and an upper
part, and the supremum of a non-empty set of cuts that is bounded above is the cut whose lower
part is the union of theirs, so completeness becomes a theorem. This sketch leaves out the
definitions of the arithmetic operations on cuts and the proofs of their rules; they belong to
Real Analysis (`ana`), which does not exist yet.
:::

Two first consequences of completeness. The first, that $\N$ is not bounded above, is the
**Archimedean property** of $\R$; later pages cite it by that name.

:::{proof:remark} The Archimedean property: $\N$ is not bounded above
:label: rem-calc-naturals-unbounded

For every real number $u$ there is an integer $n \ge 1$ with $n > u$.

*Reason.* First, $\N$ is not bounded above. Suppose it were. It is non-empty, so by
[](#ax-calc-completeness) it has a supremum $s$. Then $s - 1 < s$ is not an upper bound of $\N$,
so some $m \in \N$ has $m > s - 1$. But then $m + 1 \in \N$ and $m + 1 > s$, which contradicts
$s$ being an upper bound. So a real number $u$ is never an upper bound of $\N$: some $m \in \N$
has $m > u$, and then $n = m + 1$ is an integer with $n \ge 1$ and $n > u$.
:::

:::{admonition} Completeness gives $\sqrt{2}$
:class: dropdown rigor

Let $S = \{x \in \R : x \ge 0 \text{ and } x^2 < 2\}$. It is non-empty ($1 \in S$) and bounded
above by $2$ (if $x \ge 2$ then $x^2 \ge 4$). By [](#ax-calc-completeness) it has a supremum
$s$, and $1 \le s \le 2$. We show that $s^2 = 2$ by ruling out the other two cases.

- **If $s^2 < 2$:** let $h = \frac{2 - s^2}{2s + 2}$. Then $0 < h < 1$, because
  $0 < 2 - s^2 < 2 < 2s + 2$ (the first by the case we are in, the others because $s \ge 1$).
  So $h^2 < h$ and $(s + h)^2 = s^2 + 2sh + h^2 < s^2 + h(2s + 2) = 2$. So $s + h \in S$,
  although $s + h > s$: this contradicts $s$ being an upper bound.
- **If $s^2 > 2$:** let $h = \frac{s^2 - 2}{2s}$. Then $h > 0$, $s - h = \frac{s^2 + 2}{2s} > 0$
  and $(s - h)^2 = s^2 - 2sh + h^2 = 2 + h^2 > 2$. Every $x \in S$ has $x^2 < 2 < (s - h)^2$,
  so $x < s - h$ (both are non-negative). So $s - h$ is an upper bound of $S$ smaller than $s$:
  this contradicts condition 2 of [](#def-calc-supremum).

Hence $s^2 = 2$: the supremum $s$ is the positive square root of $2$.

**The gap in $\Q$.** The set $S_\Q = \{x \in \Q : x \ge 0 \text{ and } x^2 < 2\}$ is non-empty
and bounded above, but no rational number $u$ is its least upper bound among the rationals.
Suppose one were. Then $u \ge 1$ (because $1 \in S_\Q$), and $u^2 \ne 2$ by
[](#thm-calc-sqrt2-irrational). If $u^2 < 2$, the first case above with $s = u$ gives a rational
$h$ and an element $u + h$ of $S_\Q$ larger than $u$. If $u^2 > 2$, the second case gives the
rational upper bound $u - h = \frac{u^2 + 2}{2u}$ of $S_\Q$, smaller than $u$. Both contradict
the choice of $u$. So the argument that produced $\sqrt{2}$ in $\R$ fails in $\Q$ at its very
first step: there, the supremum need not exist.
:::

:::{admonition} Completeness gives every square root
:class: dropdown rigor

We prove [](#rem-calc-square-roots): every $y \ge 0$ has exactly one non-negative square root.

*Uniqueness.* If $0 \le s < t$, then $s^2 < t^2$: multiplying $s < t$ by $s \ge 0$ gives
$s^2 \le st$, and multiplying it by $t > 0$ gives $st < t^2$. So two different non-negative
numbers have different squares, and $y$ has at most one non-negative square root. In the same
way, if $0 \le s \le t$ then $s^2 \le t^2$.

*Existence (sketch).* For $y = 0$, take $s = 0$. For $y > 0$, we repeat the argument for
$\sqrt{2}$ with $y$ in place of $2$. The set $S_y = \{x \in \R : x \ge 0 \text{ and } x^2 < y\}$
is non-empty ($0 \in S_y$) and bounded above by $1 + y$ (if $x \ge 1 + y$, then $x \ge 1$, so
$x^2 \ge x > y$). By [](#ax-calc-completeness) it has a supremum $s \ge 0$.

- **If $s^2 < y$:** let $h$ be the smaller of $\frac{1}{2}$ and $\frac{y - s^2}{2s + 1}$. Then
  $0 < h < 1$, so $h^2 < h$ and $(s + h)^2 < s^2 + h(2s + 1) \le y$. So $s + h \in S_y$, although
  $s + h > s$.
- **If $s^2 > y$:** then $s > 0$ (as $s \ge 0$ and $s^2 > 0$); let $h = \frac{s^2 - y}{2s}$.
  As for $\sqrt{2}$, $h > 0$, $s - h = \frac{s^2 + y}{2s} > 0$ and $(s - h)^2 = y + h^2 > y$.
  Every $x \in S_y$ has $x^2 < y < (s - h)^2$, so $x < s - h$ (if $x \ge s - h \ge 0$, the
  uniqueness step would give $x^2 \ge (s - h)^2$). So $s - h$ is an upper bound of $S_y$ smaller
  than $s$.

Both cases contradict $s = \sup S_y$, so $s^2 = y$.
:::

## Summary

- $\N \subset \Z \subset \Q \subset \R$. The real numbers are the points of the number line; the
  irrational ones are those whose decimals neither terminate nor repeat.
- $\sqrt{2}$ is irrational: no fraction squares to $2$ ([](#thm-calc-sqrt2-irrational)).
- Set-builder notation $\{x \in \R : \text{condition}\}$ describes a set by a condition.
- Intervals: a square bracket includes the endpoint, a round one excludes it, and $\pm\infty$
  always gets a round bracket:
  $$
  [a, b) = \{x \in \R : a \le x < b\}, \qquad (c, \infty) = \{x \in \R : x > c\}.
  $$
- Rigorous track: $\sup S$ is the least upper bound of $S$, and the completeness axiom says that
  every non-empty set of reals that is bounded above has one.

## Exercises

::::{exercise} From conditions to intervals
:label: exr-calc-real-numbers-to-interval
:class: tier-a

Write each set as an interval.

(a) $\{x \in \R : -2 < x \le 5\}$  (b) $\{x \in \R : x \ge 3\}$  (c) $\{x \in \R : x < 0\}$

:::{admonition} Hint 1
:class: dropdown hint
For each endpoint, ask whether it satisfies the condition.
:::

:::{admonition} Answer
:class: dropdown answer set
(a) $(-2, 5]$ (b) $[3, \infty)$ (c) $(-\infty, 0)$
:::
::::

::::{solution} exr-calc-real-numbers-to-interval
:label: sol-calc-real-numbers-to-interval
:class: dropdown

(a) ${-2}$ does not satisfy $-2 < x$, so it is excluded; $5$ satisfies $x \le 5$, so it is
included: $(-2, 5]$.

(b) The numbers $x \ge 3$ start at $3$, which is included, and have no right end: $[3, \infty)$.

(c) The numbers $x < 0$ have no left end and stop just before $0$, which is excluded:
$(-\infty, 0)$.
::::

::::{exercise} The integers in an interval
:label: exr-calc-real-numbers-integers-in-interval
:class: tier-a

List all the integers that lie in the interval $(-2, 3]$.

:::{admonition} Answer
:class: dropdown answer set
$-1, 0, 1, 2, 3$
:::
::::

::::{solution} exr-calc-real-numbers-integers-in-interval
:label: sol-calc-real-numbers-integers-in-interval
:class: dropdown

The interval $(-2, 3]$ is $\{x \in \R : -2 < x \le 3\}$. The integer ${-2}$ is excluded (the
bracket is round) and $3$ is included (the bracket is square), so the integers in it are
${-1}$, $0$, $1$, $2$ and $3$.
::::

::::{exercise} Integers and fractions
:label: exr-calc-real-numbers-integers-rational
:class: tier-a

True or false: every integer is a rational number.

:::{admonition} Answer
:class: dropdown answer bool
True
:::
::::

::::{solution} exr-calc-real-numbers-integers-rational
:label: sol-calc-real-numbers-integers-rational
:class: dropdown

True. An integer $n$ can be written as the fraction $\frac{n}{1}$, whose numerator and
denominator are integers and whose denominator is not $0$. So $\Z \subseteq \Q$.
::::

::::{exercise} An intersection
:label: exr-calc-real-numbers-intersection
:class: tier-a

Write $[-1, 4) \cap (2, 6]$ as an interval.

:::{admonition} Hint 1
:class: dropdown hint
Draw both intervals on one number line and look where they overlap.
:::

:::{admonition} Answer
:class: dropdown answer set
$(2, 4)$
:::
::::

::::{solution} exr-calc-real-numbers-intersection
:label: sol-calc-real-numbers-intersection
:class: dropdown

A number lies in both intervals when $-1 \le x < 4$ and $2 < x \le 6$. The larger left endpoint
is $2$ and the smaller right endpoint is $4$, so the conditions together say $2 < x < 4$. The
endpoint $2$ is excluded because $2 \notin (2, 6]$, and $4$ because $4 \notin [-1, 4)$. So the
intersection is $(2, 4)$, as in [](#eg-calc-real-numbers-intersection-union).
::::

::::{exercise} A union
:label: exr-calc-real-numbers-union
:class: tier-b

Write $[0, 2] \cup (1, 5)$ as an interval.

:::{admonition} Hint 1
:class: dropdown hint
Do the two intervals overlap? If they do, the union has no gap.
:::

:::{admonition} Answer
:class: dropdown answer set
$[0, 5)$
:::
::::

::::{solution} exr-calc-real-numbers-union
:label: sol-calc-real-numbers-union
:class: dropdown

The intervals overlap on $(1, 2]$, so their union has no gap: it runs from the left end of
$[0, 2]$ to the right end of $(1, 5)$. The left endpoint $0$ belongs to $[0, 2]$, so it is
included; the right endpoint $5$ belongs to neither interval, so it is excluded. The union is
$[0, 5)$.
::::

::::{exercise} The complement of an interval
:label: exr-calc-real-numbers-complement
:class: tier-b

The set $\R \setminus [1, 3)$ is the union of two intervals. Find them, the left one first.

:::{admonition} Hint 1
:class: dropdown hint
A real number $x$ is *not* in $[1, 3)$ when $x < 1$ or $x \ge 3$.
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, 1)$ and $[3, \infty)$
:::
::::

::::{solution} exr-calc-real-numbers-complement
:label: sol-calc-real-numbers-complement
:class: dropdown

The interval $[1, 3)$ is $\{x \in \R : 1 \le x < 3\}$. A real number fails this condition when
$x < 1$ or when $x \ge 3$. The first condition gives $(-\infty, 1)$, without $1$ (which is in
$[1, 3)$), and the second gives $[3, \infty)$, with $3$ (which is not in $[1, 3)$). So
$\R \setminus [1, 3) = (-\infty, 1) \cup [3, \infty)$.
::::

::::{exercise} A repeating decimal
:label: exr-calc-real-numbers-repeating-decimal
:class: tier-b

Write $0.\overline{27} = 0.272727\ldots$ as a fraction in lowest terms.

:::{admonition} Hint 1
:class: dropdown hint
The repeating block has two digits. Follow [](#eg-calc-real-numbers-repeating-decimal).
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{3}{11}$
:::
::::

::::{solution} exr-calc-real-numbers-repeating-decimal
:label: sol-calc-real-numbers-repeating-decimal
:class: dropdown

Let $x = 0.272727\ldots$. Then $100x = 27.272727\ldots$, and subtracting,
$100x - x = 27$, so $99x = 27$ and $x = \frac{27}{99} = \frac{3}{11}$ (dividing by $9$).
::::

::::{exercise} A decimal that repeats after a delay
:label: exr-calc-real-numbers-delayed-repeat
:class: tier-b

Write $1.2\overline{3} = 1.2333\ldots$ as a fraction in lowest terms.

:::{admonition} Hint 1
:class: dropdown hint
Multiply by $10$ and by $100$: the two results have the same digits after the decimal point.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{37}{30}$
:::
::::

::::{solution} exr-calc-real-numbers-delayed-repeat
:label: sol-calc-real-numbers-delayed-repeat
:class: dropdown

Let $x = 1.2333\ldots$. Then $10x = 12.333\ldots$ and $100x = 123.333\ldots$ have the same tail,
so $100x - 10x = 123 - 12 = 111$, that is $90x = 111$, and $x = \frac{111}{90} = \frac{37}{30}$
(dividing by $3$).
::::

::::{exercise} The square root of 3
:label: exr-calc-real-numbers-sqrt3-irrational
:class: tier-c

Prove that $\sqrt{3}$ is irrational.

:::{admonition} Hint 1
:class: dropdown hint
Follow the proof of [](#thm-calc-sqrt2-irrational), with "divisible by $3$" in place of "even".
:::

:::{admonition} Hint 2
:class: dropdown hint
Every integer has one of the forms $3m$, $3m + 1$ or $3m + 2$ with $m \in \Z$. Square the last
two.
:::

:::{admonition} Answer
:class: dropdown answer manual
If $\sqrt{3} = \frac{p}{q}$ with the smallest possible positive denominator $q$, then $3$
divides $p$ and then $q$, so a smaller denominator exists: a contradiction.
:::
::::

::::{solution} exr-calc-real-numbers-sqrt3-irrational
:label: sol-calc-real-numbers-sqrt3-irrational
:class: dropdown

We argue by contradiction, as in the proof of [](#thm-calc-sqrt2-irrational).

We use division with remainder by $3$: every integer is of exactly one of the forms $3m$,
$3m + 1$ and $3m + 2$ with $m \in \Z$, and $3$ divides it exactly when it is of the form $3m$.

First, if $3$ does not divide an integer $p$, then it does not divide $p^2$. Indeed, then
$p = 3m + 1$ or $p = 3m + 2$ with $m \in \Z$, and
$$
(3m + 1)^2 = 3(3m^2 + 2m) + 1, \qquad (3m + 2)^2 = 3(3m^2 + 4m + 1) + 1,
$$
which are both of the form $3j + 1$ with $j \in \Z$, so neither is of the form $3m$.

Suppose now that $\sqrt{3} = \frac{p}{q}$ with positive integers $p$ and $q$, and choose $q$ as
small as possible. Then $p^2 = 3q^2$, so $3$ divides $p^2$, and by the first paragraph $3$
divides $p$: $p = 3k$ with $k$ a positive integer. Then $9k^2 = 3q^2$, that is $q^2 = 3k^2$, so
$3$ divides $q^2$ and therefore $q$: $q = 3l$ with $l$ a positive integer. Now
$\sqrt{3} = \frac{3k}{3l} = \frac{k}{l}$ with $l < q$, which contradicts the choice of $q$. So
$\sqrt{3}$ is irrational.
::::

::::{exercise} Two suprema
:label: exr-calc-real-numbers-supremum
:class: tier-c rigor

Find (a) $\sup\, \{1 - \frac{1}{n} : n \text{ an integer}, n \ge 1\}$ and
(b) $\sup\, \{x \in \R : x^2 < 2\}$, and prove that your answers are the suprema, using
[](#def-calc-supremum).

:::{admonition} Hint 1
:class: dropdown hint
For each set, show first that your candidate is an upper bound, and then that no smaller number
is one.
:::

:::{admonition} Hint 2
:class: dropdown hint
In (a), a number $u < 1$ is exceeded by $1 - \frac{1}{n}$ once $\frac{1}{n} < 1 - u$. Use
[the Archimedean property](#rem-calc-naturals-unbounded).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $1$ (b) $\sqrt{2}$
:::
::::

::::{solution} exr-calc-real-numbers-supremum
:label: sol-calc-real-numbers-supremum
:class: dropdown

(a) Let $S = \{1 - \frac{1}{n} : n \text{ an integer}, n \ge 1\}$. Every element satisfies
$1 - \frac{1}{n} < 1$, so $1$ is an upper bound. Now let $u < 1$. By
[the Archimedean property](#rem-calc-naturals-unbounded) there is an integer $n \ge 1$ with
$n > \frac{1}{1 - u}$, and since $1 - u > 0$ this gives $\frac{1}{n} < 1 - u$, that is
$1 - \frac{1}{n} > u$. So $u$ is not an upper bound, and every upper bound is at least $1$:
$\sup S = 1$. Note that $1 \notin S$, so $S$ has no largest element.

(b) Let $T = \{x \in \R : x^2 < 2\}$. If $x \ge \sqrt{2}$, then $x > 0$, and multiplying
$x \ge \sqrt{2}$ by $x$ and by $\sqrt{2}$, both positive, gives
$x^2 \ge \sqrt{2}\, x \ge \sqrt{2} \cdot \sqrt{2} = 2$, so $x \notin T$; hence every element of
$T$ is less than $\sqrt{2}$, and $\sqrt{2}$ is an upper bound. Now let $u < \sqrt{2}$ be any
upper bound of $T$. Since $0 \in T$, we have $u \ge 0$. The number $x = \frac{u + \sqrt{2}}{2}$
satisfies $0 \le u < x < \sqrt{2}$. Multiplying $x < \sqrt{2}$ by $x > 0$ and by $\sqrt{2} > 0$
gives $x^2 < \sqrt{2}\, x < 2$, so $x \in T$; but $x > u$, which contradicts $u$ being an upper
bound. So no number below $\sqrt{2}$ is an upper bound: $\sup T = \sqrt{2}$.
::::

::::{exercise} A rational number between any two reals
:label: exr-calc-real-numbers-rational-between
:class: tier-c rigor

Let $a < b$ be real numbers. Prove that there is a rational number $r$ with $a < r < b$.

:::{admonition} Hint 1
:class: dropdown hint
Use [the Archimedean property](#rem-calc-naturals-unbounded) to find an integer $n \ge 1$ with
$\frac{1}{n} < b - a$.
:::

:::{admonition} Hint 2
:class: dropdown hint
The fractions $\frac{m}{n}$ with $m \in \Z$ are spaced $\frac{1}{n}$ apart. Take the first one
to the right of $a$.
:::

:::{admonition} Answer
:class: dropdown answer manual
With $n > \frac{1}{b - a}$ and $m$ the smallest integer greater than $na$, the number
$r = \frac{m}{n}$ works.
:::
::::

::::{solution} exr-calc-real-numbers-rational-between
:label: sol-calc-real-numbers-rational-between
:class: dropdown

Since $b - a > 0$, [the Archimedean property](#rem-calc-naturals-unbounded) gives an integer
$n \ge 1$ with $n > \frac{1}{b - a}$, that is $nb - na > 1$.

Next, let $A$ be the set of integers greater than $na$. It is non-empty: by the Archimedean
property again, some integer exceeds $na$. It has a smallest element, which we find with the
well-ordering principle (stated before [](#thm-calc-sqrt2-irrational)). The elements of $A$ need
not be positive, so we first shift $A$ into the positive integers: the Archimedean property gives
an integer $k \ge 1$ with $k > -na$, and then every $j \in A$ has $j + k > na + k > 0$. So the
numbers $j + k$ with $j \in A$ form a non-empty set of positive integers, which by the
well-ordering principle has a smallest element $m + k$ with $m \in A$; then $m$ is the smallest
element of $A$. Since $m$ is the smallest, $m - 1$ is not greater than $na$, so
$$
na < m \le na + 1 < na + (nb - na) = nb .
$$
Dividing by $n > 0$ gives $a < \frac{m}{n} < b$, so $r = \frac{m}{n}$ is a rational number
between $a$ and $b$.
::::

## Where this leads

:::{where-this-leads}
:::
