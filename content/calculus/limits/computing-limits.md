---
title: Computing Limits Algebraically
label: calc-computing-limits
description: >-
  Limits in which substituting the point gives zero over zero: why that is a form and not a
  value, and how factoring, rationalising and simplifying find the limit, each step justified
  by a lemma about functions that agree except at a point.
tags: [limits, proofs]
maths:
  kind: topic
  subject: calc
  status: reviewed
  level: core
  difficulty: 2
  est_minutes: 45
  prerequisites: [calc-limit-laws, calc-polynomial-rational]
  objectives:
    - Resolve 0/0 forms by factoring, rationalising and simplifying.
    - Justify each step with the "agree except at a point" lemma.
  verify: verify/calculus/limits/test_computing_limits.py
  widgets: [function-plot]
  reviewed_by: [vronnblom]
  manual_checked:
    exr-calc-computing-limits-numerator-zero: vronnblom
  sources: []
---

:::{topic-header}
:::

## Why this matters

A metal cube is heated and expands. On
[Polynomial and Rational Functions](#calc-polynomial-rational) we asked how fast its volume
grows when its side is exactly $2$ centimetres. As the side grows from $2$ to $x$, the volume
$x^3$ grows by $x^3 - 8$, so on average it grows by
$$
A(x) = \frac{x^3 - 8}{x - 2}
$$
cubic centimetres per centimetre of side. At $x = 2$ the formula gives $\frac{0}{0}$, which is
not a number.

::::{figure}
:label: wdg-calc-computing-limits-cube

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "(x^3 - 8)/(x - 2)",
  "xRange": [0, 4],
  "yRange": [0, 30],
  "table": { "points": [1.9, 1.99, 1.999, 2.001, 2.01, 2.1] },
  "hole": { "x": 2 },
  "trace": { "x": 1 }
}
```

Graph of the average rate $y = \frac{x^3 - 8}{x - 2}$ for $0 \le x \le 4$, rising from $4$ at
$x = 0$ to $28$ at $x = 4$, with an open circle at $x = 2$, where the formula is undefined. The
widget draws the circle at the height it estimates from the values on both sides of $2$. A
slider for $x$ moves a point along the graph. A table lists the values at
$x = 1.9, 1.99, 1.999$: $11.41$, $11.9401$, $11.994001$, and at $x = 2.001, 2.01, 2.1$:
$12.006001$, $12.0601$, $12.61$. They get closer to $12$ from both sides.
::::

**Try this:** move the point towards $x = 2$ from both sides and read the values. Then compute
$x^2 + 2x + 4$ at $x = 1.99$ and at $x = 2$. What do you notice?

On that page we factored the numerator, $x^3 - 8 = (x - 2)(x^2 + 2x + 4)$, cancelled the
non-zero number $x - 2$ for $x \ne 2$, and said that for $x$ close to $2$ the rate is close to
$2^2 + 2 \cdot 2 + 4 = 12$. The table agrees. But two questions remain.

- Is $12$ the **limit** of $A(x)$ as $x \to 2$? The quotient law, part (d) of
  [the limit laws](#thm-calc-limit-laws), cannot say: the denominator approaches $0$.
- Cancelling changed the function. $A$ is undefined at $2$, while $x^2 + 2x + 4$ is defined
  there. Why should the new function have the same limit as the old one?

This page answers both with one lemma: two functions that agree near $a$, except possibly at $a$
itself, have the same limit at $a$. With it, every limit of the form "$\frac{0}{0}$" on this
page follows the same plan: rewrite the function for $x \ne a$, by factoring, rationalising or
simplifying, until the limit laws apply, and let the lemma carry the limit back.

## Limits of the form $\frac{0}{0}$

On [Limit Laws](#calc-limit-laws) we met quotients whose numerator and denominator both
approach $0$. The quotient law needs the limit of the denominator to be non-zero, so it does not
apply to them.

Let $f$ and $g$ be functions, each defined at every point of an open interval containing $a$,
except possibly at $a$, with $\lim_{x \to a} f(x) = 0$ and $\lim_{x \to a} g(x) = 0$, and
suppose that $\frac{f}{g}$ is also defined at every point of an open interval containing $a$,
except possibly at $a$. We then say that $\lim_{x \to a} \frac{f(x)}{g(x)}$ is **of the form
$\frac{0}{0}$**.

**In words.** "Of the form $\frac{0}{0}$" describes the situation, not the answer: substituting
the limits of the parts gives the symbol $\frac{0}{0}$, which is not a number, because $0$ has
no reciprocal. Such a limit may be any number, or not exist at all, as
[the figure on Limit Laws](#wdg-calc-limit-laws-zero-over-zero) suggests and
[](#eg-calc-computing-limits-same-form) proves. The form says only that the quotient law gives
nothing, and that we must rewrite the function first.

**Example.** $\lim_{x \to 2} \frac{x^3 - 8}{x - 2}$ is of the form $\frac{0}{0}$: by
[part (a) of direct substitution](#cor-calc-direct-substitution), the numerator approaches
$2^3 - 8 = 0$ and the denominator $2 - 2 = 0$, and the quotient is defined at every $x \ne 2$.

**Non-example.** $\lim_{x \to 2} \frac{x^3 - 8}{x + 2}$ is not of the form $\frac{0}{0}$: the
denominator approaches $4 \ne 0$, so the quotient law applies, and the limit is
$\frac{0}{4} = 0$. Nor is $\lim_{x \to 0} \frac{1}{x}$, where the numerator approaches $1$: that
limit does not exist, as [Limit Laws](#sec-calc-limit-laws-not-apply) shows, and no rewriting
changes that.

## Main results

The lemma says that a limit only sees the values of a function on a small window around $a$,
with $a$ itself left out. The window is the set of $x$ with $0 < \abs{x - a} < r$, which by
[part (e) of the proposition on distance inequalities](#prop-calc-abs-interval) is the open
interval $(a - r, a + r)$ with its centre $a$ removed.

:::{proof:lemma} Functions that agree except at a point
:label: lem-calc-limit-agree-except-point

Let $a$ be a real number and $r > 0$. Let $f$ and $g$ be functions that are both defined at
every $x$ with $0 < \abs{x - a} < r$, and such that, for every $x$ with
$0 < \abs{x - a} < r$,
$$
f(x) = g(x) .
$$
If $\lim_{x \to a} g(x) = L$, where $L$ is a real number, then $\lim_{x \to a} f(x) = L$.
:::

:::{proof:proof}
:enumerated: false
A window that wins a round of the $\eps$–$\delta$ game for $g$, made small enough to lie in
the window where $f$ and $g$ agree, wins the same round for $f$, because on it $f$ has the same
values as $g$.

By hypothesis, $f$ is defined at every $x$ with $0 < \abs{x - a} < r$, which is the open
interval $(a - r, a + r)$ with $a$ removed, by
[part (e) of the proposition on distance inequalities](#prop-calc-abs-interval). So
[the definition of a limit](#def-calc-limit) applies to $f$.

Let $\eps > 0$. Since $\lim_{x \to a} g(x) = L$, the definition gives a $\delta_0 > 0$ such
that $g$ is defined and $\abs{g(x) - L} < \eps$ at every $x$ with $0 < \abs{x - a} < \delta_0$.
Let $\delta = \min(\delta_0, r)$. It is one of the two positive numbers $\delta_0$ and $r$, so
it is positive.

Let $0 < \abs{x - a} < \delta$. Since $\delta \le r$ and $\delta \le \delta_0$, transitivity
([property 2 of the order rules](#rem-calc-order-rules), in the form "$u < v \le w$ implies
$u < w$") gives $\abs{x - a} < r$ and $\abs{x - a} < \delta_0$. The first, with
$0 < \abs{x - a}$, says that $x$ is in the window of the hypothesis: $f$ is defined at $x$, and
$f(x) = g(x)$. The second says that $\abs{g(x) - L} < \eps$. So
$$
\abs{f(x) - L} = \abs{g(x) - L} < \eps .
$$
So $f$ is defined at every $x$ with $0 < \abs{x - a} < \delta$, and $\delta$ wins the round
$\eps$ for $f$. Since $\eps > 0$ was arbitrary, $\lim_{x \to a} f(x) = L$.
:::

**In words.** If two functions have the same values near $a$, except possibly at $a$, they
have the same limit at $a$. What they do at $a$ plays no part: $f(a)$ and $g(a)$ may be
different, or undefined. What they do far from $a$ plays no part either: only some window
around $a$, however small, matters.

- **Both directions.** The hypothesis is the same with $f$ and $g$ swapped. So if either
  function has a limit at $a$, the other has the same limit; and if one has no limit at $a$,
  neither has the other.
- **A whole window is needed.** Agreeing on one side of $a$ is not enough. The function
  $\frac{\abs{x}}{x}$ agrees with the constant $1$ at every $x > 0$, and the constant has the
  limit $1$, but $\frac{\abs{x}}{x}$ has no limit at $0$
  ([](#exr-calc-computing-limits-abs-sqrt)): every window around $0$ also contains points
  $x < 0$, where its value is ${-1}$.
- **What we already knew.** [The remark on the value at $a$](#rem-calc-limit-value-irrelevant)
  says that changing a function at the single point $a$, or leaving it undefined there, does
  not change its limit, and [part (c) of direct substitution](#cor-calc-direct-substitution)
  says that a rational function whose denominator is not $0$ at $a$, used only on an open
  interval around $a$, keeps its limit $\frac{p(a)}{q(a)}$. The lemma is the general form of
  both ideas. Unlike the remark, it asks $f$ and $g$ to agree only on a window around $a$, not
  at every $x \ne a$. Unlike part (c), it allows $g$ to be any function that has a limit at $a$,
  given by any formula, and $f$ need not be defined at $a$. This is what limits of the form
  $\frac{0}{0}$ need.

**Example.** For $x \ne 1$, $\frac{x^2 - 1}{x - 1} = \frac{(x - 1)(x + 1)}{x - 1} = x + 1$,
cancelling the non-zero number $x - 1$. Both functions are defined at every $x$ with
$0 < \abs{x - 1} < 1$ and agree there, and $\lim_{x \to 1} (x + 1) = 2$ by
[part (a) of direct substitution](#cor-calc-direct-substitution). By the lemma,
$\lim_{x \to 1} \frac{x^2 - 1}{x - 1} = 2$.

**Non-example.** Agreeing *at* $a$ is not the hypothesis, and it is not enough. Let $h(x) = x + 1$
for $x \ne 0$ and $h(0) = 0$. The functions $x$ and $h$ agree at $x = 0$. But
$\lim_{x \to 0} x = 0$ ([part (a) of the limit laws](#thm-calc-limit-laws)), while $h$ agrees
with $x + 1$ at every $x \ne 0$, so by the lemma and
[part (a) of direct substitution](#cor-calc-direct-substitution),
$\lim_{x \to 0} h(x) = 1$.

### The method for $\frac{0}{0}$

To find $\lim_{x \to a} f(x)$ for a quotient $f$:

1. **Substitute.** Find the limits of the numerator and the denominator with the limit laws or
   direct substitution. If the denominator's limit is not $0$, the quotient law gives the
   answer, and we are done. If both limits are $0$, the limit is of the form $\frac{0}{0}$:
   go on.
2. **Rewrite.** Find a function $g$ and a window $0 < \abs{x - a} < r$ on which $f$ and $g$ are
   both defined and $f(x) = g(x)$. The algebra may use $x \ne a$: on the window we may cancel a
   factor that is not $0$ there, such as $x - a$.
3. **Compute** $\lim_{x \to a} g(x)$ with the limit laws or direct substitution, checking the
   hypotheses of each law and naming its part.
4. **Conclude** with [](#lem-calc-limit-agree-except-point): $\lim_{x \to a} f(x)$ is the same
   number.

Step 2 is where the three techniques below come in. Each of them produces a $g$ to which the
laws apply.

### Three ways to rewrite

**Factoring.** Let $f = \frac{p}{q}$, with polynomials $p$ and $q$ such that $p(a) = 0$ and
$q(a) = 0$, and $p$ not the zero polynomial. (If $p$ is the zero polynomial, $f$ is $0$
wherever it is defined; the rigorous track treats this case.) A polynomial of degree $0$ is a
non-zero constant, which has no root, so $p$ has degree at least $1$. So has $q$, which is not
the zero polynomial, by [the definition of a rational function](#def-calc-rational-function).
By [part (b) of the factor theorem](#thm-calc-factor-theorem), for every real $x$,
$$
\begin{aligned}
p(x) &= (x - a)\, p_1(x), \\
q(x) &= (x - a)\, q_1(x),
\end{aligned}
$$
where $p_1$ and $q_1$ are polynomials whose degrees are one less than those
of $p$ and $q$ (part (a) of the theorem, for degree at least $1$). To find $p_1$, divide $p$ by
$x - a$: since $p(x) = (x - a)\, p_1(x) + 0$, the uniqueness in
[division of polynomials](#thm-calc-polynomial-division) says that $p_1$ is the quotient, with
the zero polynomial as the remainder. For a quadratic, a factorisation found by inspection is
just as good, once multiplying out confirms it.

At every $x \ne a$ the number $x - a$ is not $0$, so by
[part (a) of the sign rules](#prop-calc-sign-rules), $q(x) \ne 0$ exactly when
$q_1(x) \ne 0$. So $\frac{p}{q}$ and $\frac{p_1}{q_1}$ are defined at the same points
$x \ne a$, and at those points
$$
\frac{p(x)}{q(x)} = \frac{(x - a)\, p_1(x)}{(x - a)\, q_1(x)} = \frac{p_1(x)}{q_1(x)},
$$
cancelling the non-zero factor $x - a$. If $q_1(a) \ne 0$, then by
[part (b) of the proposition on the domain of a rational function](#prop-calc-rational-domain)
there is an open interval $(\alpha, \beta)$ containing $a$ at every point of which
$\frac{p_1}{q_1}$ is defined. Let $r$ be the smaller of $a - \alpha$ and $\beta - a$, which is
positive, since $\alpha < a < \beta$. If $0 < \abs{x - a} < r$, then $a - r < x < a + r$ by
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval), and
$\alpha \le a - r$ and $a + r \le \beta$ (add $\alpha - r$, or $a$, to both sides of
$r \le a - \alpha$, or of $r \le \beta - a$; [property 3 of the order rules](#rem-calc-order-rules)),
so $\alpha < x < \beta$ (property 2). So both functions are defined and agree on the window
$0 < \abs{x - a} < r$, [part (b) of direct substitution](#cor-calc-direct-substitution) gives
$\lim_{x \to a} \frac{p_1(x)}{q_1(x)} = \frac{p_1(a)}{q_1(a)}$, and the lemma gives the same
limit for $\frac{p}{q}$. If $q_1(a) = 0$ too, there are two cases.

- If $p_1(a) = 0$ as well, the limit is again of the form $\frac{0}{0}$, and we factor again
  ([](#exr-calc-computing-limits-factor-twice)).
- If $p_1(a) \ne 0$, the limit does not exist, as for $\frac{x}{x^2}$ at $0$ in
  [](#eg-calc-computing-limits-same-form) (iii), where $p_1(x) = 1$ and $q_1(x) = x$.

The rigorous track, "Factoring always ends", proves both cases: after finitely many steps,
factoring gives the limit or shows that there is none. In an example, the window is usually
found directly, from the roots of the denominator.

The cube of Why this matters is a special case of a general fact. For every polynomial $p$ and
every real $a$, [part (a) of the factor theorem](#thm-calc-factor-theorem) gives a polynomial
$q$ such that, for every real $x \ne a$,
$$
\frac{p(x) - p(a)}{x - a} = q(x) .
$$
Both sides are defined at every $x \ne a$ and agree there, so on every window around $a$. By
[part (a) of direct substitution](#cor-calc-direct-substitution),
$\lim_{x \to a} q(x) = q(a)$, and by the lemma
$$
\lim_{x \to a} \frac{p(x) - p(a)}{x - a} = q(a) .
$$

**Rationalising.** A difference of square roots becomes a difference of numbers when it is
multiplied by the sum. For real numbers $u, v \ge 0$, the numbers $\sqrt{u}$ and $\sqrt{v}$ are
defined, and $\bigl(\sqrt{u}\bigr)^2 = u$ and $\bigl(\sqrt{v}\bigr)^2 = v$, by
[the square-root remark](#rem-calc-square-roots). Multiplying out, the two middle terms cancel:
$$
\bigl(\sqrt{u} - \sqrt{v}\bigr)\bigl(\sqrt{u} + \sqrt{v}\bigr) = u - v .
$$
The **conjugate** $\sqrt{u} + \sqrt{v}$ is positive if $u > 0$: then $\sqrt{u} \ge 0$, and
$\sqrt{u} \ne 0$ because $0^2 = 0 \ne u$, so $\sqrt{u} > 0$; adding this to $\sqrt{v} \ge 0$
gives $\sqrt{u} + \sqrt{v} > 0$ ([property 4 of the order rules](#rem-calc-order-rules)). So we
may multiply the numerator and the denominator of a quotient by it without changing the value:
the quotient is the same number, now written with $u - v$ in place of $\sqrt{u} - \sqrt{v}$
([](#eg-calc-computing-limits-conjugate)).

After rationalising, the limit of a square root comes from
[part (f) of the limit laws](#thm-calc-limit-laws), the root law, and its hypotheses must be
checked. If $\lim_{x \to a} h(x) = L$ with $L > 0$, then $\lim_{x \to a} \sqrt{h(x)} = \sqrt{L}$.
If $L = 0$, the law needs more: an $r > 0$ such that $h(x) \ge 0$ at every $x$ with
$0 < \abs{x - a} < r$. For example, $\abs{x} = \sqrt{x^2}$ for every real $x$, by
[property 5 of the absolute value](#rem-calc-absolute-value-properties); here $h(x) = x^2$ has
the limit $0$ at $0$ ([part (a) of direct substitution](#cor-calc-direct-substitution)), and
$x^2 \ge 0$ for every real $x$, by [part (c) of the sign rules](#prop-calc-sign-rules). So the
root law gives
$$
\lim_{x \to 0} \abs{x} = \lim_{x \to 0} \sqrt{x^2} = 0 .
$$
Without the sign condition the law says nothing: $\sqrt{x}$ is undefined at every $x < 0$, so it
has no limit at $0$ in the sense of [the definition](#def-calc-limit), although $x \to 0$.

**Simplifying compound fractions.** A quotient whose numerator or denominator is itself a sum
of fractions is brought to a single fraction first. For numbers $b \ne 0$ and $d \ne 0$,
$$
\frac{c_1}{b} - \frac{c_2}{d} = \frac{c_1 d - c_2 b}{b d},
$$
and $bd \ne 0$ by [part (a) of the sign rules](#prop-calc-sign-rules). Then a factor $x - a$
usually appears in the new numerator and cancels ([](#eg-calc-computing-limits-resistors)).

## Worked examples

### Factoring

:::{proof:example} The cube from Why this matters
:label: eg-calc-computing-limits-factor

Find $\displaystyle \lim_{x \to 2} \frac{x^3 - 8}{x - 2}$, the rate at which the cube's volume
grows when its side is $2$ cm.

1. **Substitute.** The function $A(x) = \frac{x^3 - 8}{x - 2}$ is defined at every $x \ne 2$,
   since $x - 2 = 0$ only for $x = 2$. By
   [part (a) of direct substitution](#cor-calc-direct-substitution), the numerator approaches
   $2^3 - 8 = 0$ and the denominator $2 - 2 = 0$. The limit is of the form $\frac{0}{0}$, and the
   quotient law does not apply.
2. **Factor.** Let $p(x) = x^3 - 8$. Since $p(2) = 0$,
   [part (b) of the factor theorem](#thm-calc-factor-theorem) gives a polynomial $q$, of degree
   $2$ with leading coefficient $1$ (part (a)), such that $p(x) = (x - 2)\, q(x)$ for every
   real $x$. Multiplying out gives
   $$
   \begin{aligned}
   &(x - 2)(x^2 + 2x + 4) \\
   &\quad = x^3 + 2x^2 + 4x \\
   &\qquad - 2x^2 - 4x - 8 \\
   &\quad = x^3 - 8 .
   \end{aligned}
   $$
   So $p(x) = (x - 2)(x^2 + 2x + 4) + 0$ and $p(x) = (x - 2)\, q(x) + 0$ for every real $x$, and
   by the uniqueness of the quotient in [division of polynomials](#thm-calc-polynomial-division),
   dividing $p$ by $x - 2$, we get $q(x) = x^2 + 2x + 4$.
3. **Cancel.** For $x \ne 2$ the number $x - 2$ is not $0$, so
   $$
   \begin{aligned}
   A(x) &= \frac{(x - 2)(x^2 + 2x + 4)}{x - 2} \\
     &= x^2 + 2x + 4 .
   \end{aligned}
   $$
   So $A$ and $g(x) = x^2 + 2x + 4$ are both defined, and equal, at every $x$ with
   $0 < \abs{x - 2} < 1$ (any $r > 0$ would do).
4. **Compute.** $g$ is a polynomial, so by part (a) of direct substitution,
   $\lim_{x \to 2} g(x) = g(2) = 4 + 4 + 4 = 12$.
5. **Conclude.** By [](#lem-calc-limit-agree-except-point), with $f = A$, $a = 2$, $r = 1$ and
   $L = 12$, the limit of $A$ is $12$.

$$
\boxed{\lim_{x \to 2} \frac{x^3 - 8}{x - 2} = 12}
$$

So when the side is $2$ cm, the volume grows at $12$ cubic centimetres per centimetre of side.
This is the general fact of the factoring paragraph, with $p(x) = x^3$ and $a = 2$: the limit is
$q(2)$.

**Check.** At $x = 2.001$: $\frac{2.001^3 - 8}{0.001} = \frac{0.012006001}{0.001} = 12.006001$,
as in the table of [the figure](#wdg-calc-computing-limits-cube), and close to $12$. ✓ Units:
cubic centimetres divided by centimetres. ✓
:::

### Rationalising

:::{proof:example} A difference of square roots
:label: eg-calc-computing-limits-conjugate

Find $\displaystyle \lim_{x \to 0} \frac{\sqrt{1 + x} - 1}{x}$, the limit that a table
estimated as $0.50$ in [an exercise on The Limit of a Function](#exr-calc-limit-table-estimate).

1. **The window.** Let $f(x) = \frac{\sqrt{1 + x} - 1}{x}$. If $0 < \abs{x} < 1$, then
   $-1 < x < 1$ and $x \ne 0$, by
   [part (e) of the proposition on distance inequalities](#prop-calc-abs-interval), and adding
   $1$ to $-1 < x$ gives $1 + x > 0$ ([property 3 of the order rules](#rem-calc-order-rules)).
   So $\sqrt{1 + x}$ is defined ([the square-root remark](#rem-calc-square-roots)), and $f$ is
   defined at every $x$ with $0 < \abs{x} < 1$.
2. **Substitute.** By [part (a) of direct substitution](#cor-calc-direct-substitution),
   $\lim_{x \to 0} (1 + x) = 1$. Since $1 > 0$, the root law,
   [part (f) of the limit laws](#thm-calc-limit-laws), gives
   $\lim_{x \to 0} \sqrt{1 + x} = \sqrt{1} = 1$ (since $1 \ge 0$ and $1^2 = 1$). By parts (a)
   and (b), the numerator approaches $1 - 1 = 0$, and by part (a) the denominator $x$
   approaches $0$. The limit is of the form $\frac{0}{0}$.
3. **Rationalise.** Let $0 < \abs{x} < 1$, and $s = \sqrt{1 + x}$. Then $s \ge 0$, so
   $s + 1 \ge 1 > 0$ (adding $1$ to both sides, property 3), and we may multiply the numerator
   and the denominator by $s + 1$. Since $s^2 = 1 + x$,
   $$
   \begin{aligned}
   (s - 1)(s + 1) &= s^2 - 1 \\
     &= (1 + x) - 1 \\
     &= x .
   \end{aligned}
   $$
   So, cancelling the non-zero number $x$,
   $$
   \begin{aligned}
   f(x) &= \frac{(s - 1)(s + 1)}{x\,(s + 1)} \\
     &= \frac{x}{x\,(s + 1)} \\
     &= \frac{1}{\sqrt{1 + x} + 1} .
   \end{aligned}
   $$
4. **Compute.** Let $g(x) = \frac{1}{\sqrt{1 + x} + 1}$. It is defined at every $x \ge -1$, since
   its denominator is at least $1$ there, so it agrees with $f$ on the window
   $0 < \abs{x} < 1$. By step 2 and part (b) of the limit laws, the denominator approaches
   $1 + 1 = 2$, which is not $0$; by parts (a) and (d),
   $\lim_{x \to 0} g(x) = \frac{1}{2}$.
5. **Conclude.** By [](#lem-calc-limit-agree-except-point), with $a = 0$ and $r = 1$,
   $\lim_{x \to 0} f(x) = \frac{1}{2}$.

$$
\boxed{\lim_{x \to 0} \frac{\sqrt{1 + x} - 1}{x} = \frac{1}{2}}
$$

The table on The Limit of a Function suggested $0.50$; now we have a proof.

**Check.** At $x = 0.001$: $g(0.001) = \frac{1}{\sqrt{1.001} + 1} \approx 0.499875$, the value
in that table. ✓
:::

### The same form, different answers

:::{proof:example} Three limits of the form $\frac{0}{0}$
:label: eg-calc-computing-limits-same-form

Find each limit, or show that it does not exist:
(i) $\displaystyle \lim_{x \to 0} \frac{x^2}{x}$, (ii) $\displaystyle \lim_{x \to 0} \frac{3x}{x}$,
(iii) $\displaystyle \lim_{x \to 0} \frac{x}{x^2}$.

All three quotients are defined at every $x \ne 0$. By
[part (a) of direct substitution](#cor-calc-direct-substitution), each numerator and each
denominator approaches $0$, so all three limits are of the form $\frac{0}{0}$.

1. **(i)** For $x \ne 0$, cancelling the non-zero number $x$ gives $\frac{x^2}{x} = x$. Both
   functions are defined and agree at every $x$ with $0 < \abs{x} < 1$, and
   $\lim_{x \to 0} x = 0$ by [part (a) of the limit laws](#thm-calc-limit-laws). By
   [](#lem-calc-limit-agree-except-point), the limit is $0$.
2. **(ii)** For $x \ne 0$, $\frac{3x}{x} = 3$. The constant $3$ has the limit $3$, by part (a)
   of the limit laws, so by the lemma the limit is $3$.
3. **(iii)** Let $f(x) = \frac{x}{x^2}$, and suppose that $\lim_{x \to 0} f(x) = M$ for a real
   number $M$. Both $f$ and the function $x$ are defined at every $x \ne 0$, and
   $\lim_{x \to 0} x = 0$, so the product law, part (c) of the limit laws, gives
   $\lim_{x \to 0} x\,f(x) = 0 \cdot M = 0$. But for $x \ne 0$,
   $x\,f(x) = \frac{x^2}{x^2} = 1$, so $x\,f(x)$ agrees with the constant $1$ at every $x$ with
   $0 < \abs{x} < 1$, and by part (a) and the lemma its limit is $1$. Two different limits,
   $0$ and $1$, contradict [uniqueness of limits](#thm-calc-limit-unique). So $f$ has no limit
   at $0$.

**Conclusion.**

- (i) $\displaystyle \lim_{x \to 0} \frac{x^2}{x} = 0$;
- (ii) $\displaystyle \lim_{x \to 0} \frac{3x}{x} = 3$;
- (iii) $\displaystyle \lim_{x \to 0} \frac{x}{x^2}$ does not exist.

The same form $\frac{0}{0}$ gave $0$, $3$ and no limit at all. So $\frac{0}{0}$ is not a value;
replacing $3$ by any real number $c$ in (ii) gives the limit $c$.

**Check.** At $x = 0.01$: (i) $\frac{0.0001}{0.01} = 0.01$, close to $0$ ✓; (ii)
$\frac{0.03}{0.01} = 3$ ✓; (iii) $\frac{0.01}{0.0001} = 100$, and at $x = 0.001$ it is
$1000$: the values do not settle. ✓
:::

### Simplifying a compound fraction

:::{proof:example} Two resistors in parallel, again
:label: eg-calc-computing-limits-resistors

In [an example on Limit Laws](#eg-calc-limit-laws-resistors), two resistors in parallel, of $3$ ohms and $t$
ohms, have the combined resistance
$$
R(t) = \frac{3t}{3 + t}
$$
ohms, for $t > 0$, and $R(6) = \frac{18}{9} = 2$. As the second resistance passes $6$ ohms,
how fast does the combined resistance change? Find the limit of the average rate
$$
f(t) = \frac{R(t) - 2}{t - 6}
$$
as $t \to 6$, in ohms per ohm.

1. **The window.** $f$ is defined at every $t > 0$ with $t \ne 6$. If $0 < \abs{t - 6} < 6$,
   then $0 < t < 12$ and $t \ne 6$, by
   [part (e) of the proposition on distance inequalities](#prop-calc-abs-interval). So $f$ is
   defined at every $t$ with $0 < \abs{t - 6} < 6$.
2. **Substitute.** $R$ is the restriction of the rational function $\frac{3t}{3 + t}$ to the
   open interval $(0, \infty)$, which contains $6$, and the denominator is $9 \ne 0$ at $t = 6$.
   By [part (c) of direct substitution](#cor-calc-direct-substitution),
   $\lim_{t \to 6} R(t) = 2$, so the numerator approaches $2 - 2 = 0$
   ([parts (a) and (b) of the limit laws](#thm-calc-limit-laws)). The denominator approaches
   $0$. The limit is of the form $\frac{0}{0}$.
3. **One fraction.** For $t > 0$, adding $0 < 3$ and $0 < t$ gives $3 + t > 0$
   ([property 4 of the order rules](#rem-calc-order-rules)), so $3 + t \ne 0$, and
   $$
   \begin{aligned}
   R(t) - 2 &= \frac{3t - 2(3 + t)}{3 + t} \\
     &= \frac{t - 6}{3 + t} .
   \end{aligned}
   $$
4. **Cancel.** For $t > 0$ with $t \ne 6$, the number $t - 6$ is not $0$, so
   $$
   f(t) = \frac{t - 6}{(3 + t)(t - 6)} = \frac{1}{3 + t} .
   $$
   So $f$ and $g(t) = \frac{1}{3 + t}$ are both defined, and equal, at every $t$ with
   $0 < \abs{t - 6} < 6$.
5. **Compute.** $g$ is a rational function whose denominator is $9 \ne 0$ at $t = 6$, so by
   [part (b) of direct substitution](#cor-calc-direct-substitution),
   $\lim_{t \to 6} g(t) = \frac{1}{9}$.
6. **Conclude.** By [](#lem-calc-limit-agree-except-point), with $a = 6$ and $r = 6$,
   $\lim_{t \to 6} f(t) = \frac{1}{9}$.

$$
\boxed{\lim_{t \to 6} \frac{R(t) - 2}{t - 6} = \frac{1}{9}}
$$

So near $t = 6$, a small increase of the second resistance raises the combined resistance by
about one ninth of that increase: the rate is $\frac{1}{9}$ ohm per ohm.

**Check.** At $t = 6.01$: $R(6.01) = \frac{18.03}{9.01} \approx 2.0011099$, so
$f(6.01) \approx 0.110988$, and $g(6.01) = \frac{1}{9.01} \approx 0.110988$, close to
$\frac{1}{9} \approx 0.111111$. ✓ Units: ohms divided by ohms. ✓
:::

:::{admonition} Looking ahead
:class: looking-ahead
The limits in [](#eg-calc-computing-limits-factor) and [](#eg-calc-computing-limits-resistors)
are limits of average rates of change. The page Tangent Lines and Rates of Change calls such a
limit the rate of change at a point, and the Derivatives chapter computes it for every
polynomial at once, with the general fact of the factoring paragraph.
:::

## Common mistakes

:::{warning} Cancelling, then substituting, without the lemma
✗ **Wrong:** "$\frac{x^2 - 9}{x - 3} = x + 3$, so at $x = 3$ the function is $6$, and its limit
is $6$."

**Why:** the equality holds only for $x \ne 3$: the left-hand side is undefined at $3$, so it
has no value $6$ there. Two steps are missing. The functions $\frac{x^2 - 9}{x - 3}$ and $x + 3$
are different functions, and only [](#lem-calc-limit-agree-except-point) says that they have
the same limit. And "substituting $x = 3$" into $x + 3$ gives the limit only because $x + 3$ is
a polynomial ([part (a) of direct substitution](#cor-calc-direct-substitution)), not because
substituting always works.

✓ **Right:** for $x \ne 3$, $\frac{x^2 - 9}{x - 3} = \frac{(x - 3)(x + 3)}{x - 3} = x + 3$, so
the two functions are defined and agree on the window $0 < \abs{x - 3} < 1$. By part (a) of
direct substitution, $\lim_{x \to 3} (x + 3) = 6$, and by the lemma
$\lim_{x \to 3} \frac{x^2 - 9}{x - 3} = 6$.
:::

:::{warning} "$\frac{0}{0} = 1$"
✗ **Wrong:** "In $\lim_{x \to 0} \frac{x^2}{x}$, the numerator and the denominator both
approach $0$. A number divided by itself is $1$, so $\frac{0}{0} = 1$, and the limit is $1$."

**Why:** a number divided by itself is $1$ only when it is not $0$: $\frac{u}{u} = 1$ needs
$u \ne 0$, because $0$ has no reciprocal. $\frac{0}{0}$ is not a number at all. The numerator
and the denominator approach $0$ at different speeds: $x^2$ is much smaller than $x$ near $0$.

✓ **Right:** the limit is of the form $\frac{0}{0}$, which says only that the quotient law does
not apply. Rewriting gives $\frac{x^2}{x} = x$ for $x \ne 0$, and the limit is $0$
([](#eg-calc-computing-limits-same-form)). Nor is "$\frac{0}{0}$, so the limit does not exist"
right: in the same example, $\frac{3x}{x}$ has the limit $3$.
:::

:::{warning} "$\sqrt{x^2} = x$"
✗ **Wrong:** "$\displaystyle \lim_{x \to 0} \frac{\sqrt{x^2}}{x} = \lim_{x \to 0} \frac{x}{x} = 1$."

**Why:** $\sqrt{x^2}$ is the non-negative number whose square is $x^2$
([the square-root remark](#rem-calc-square-roots)), which is $\abs{x}$, by
[property 5 of the absolute value](#rem-calc-absolute-value-properties). For $x < 0$ that is
$-x$, not $x$. So $\frac{\sqrt{x^2}}{x}$ agrees with $1$ only on the right of $0$, and the lemma
needs a whole window.

✓ **Right:** $\frac{\sqrt{x^2}}{x} = \frac{\abs{x}}{x}$, which is $1$ for $x > 0$ and ${-1}$ for
$x < 0$. Its limit at $0$ does not exist ([](#exr-calc-computing-limits-abs-sqrt)). When a
square root is simplified, check the sign of what comes out.
:::

:::{warning} Splitting into parts that have no limit
✗ **Wrong:** "$\displaystyle \lim_{x \to 3} \frac{\frac{1}{x} - \frac{1}{3}}{x - 3} =
\lim_{x \to 3} \frac{1}{x(x - 3)} - \lim_{x \to 3} \frac{1}{3(x - 3)}$", followed by an attempt
to compute the two limits on the right.

**Why:** the difference law, part (b) of [the limit laws](#thm-calc-limit-laws), needs both
limits on the right to exist, as real numbers. Here neither does: the two functions are
$\frac{1/x}{x - 3}$ and $\frac{1/3}{x - 3}$, whose numerators approach $\frac{1}{3}$, not $0$,
while their denominators approach $0$. Such a quotient has no limit. If $\frac{1/x}{x - 3}$ had
a limit $M$, then, since $x - 3 \to 0$ (parts (a) and (b)), the product law, part (c), would
give $(x - 3) \cdot \frac{1/x}{x - 3} \to 0 \cdot M = 0$. But on the window
$0 < \abs{x - 3} < 3$ this product is $\frac{1}{x}$. Since $\frac{1}{x} \to \frac{1}{3}$ by
[part (b) of direct substitution](#cor-calc-direct-substitution), the lemma gives the product the
limit $\frac{1}{3}$, and $0 \ne \frac{1}{3}$ contradicts
[uniqueness of limits](#thm-calc-limit-unique). The same argument applies to
$\frac{1/3}{x - 3}$: there the product is the constant $\frac{1}{3}$, whose limit is
$\frac{1}{3}$ by part (a) of the limit laws
([](#exr-calc-computing-limits-numerator-zero) proves the general fact behind this). Splitting a
limit is a conclusion of the laws, never a step you may take before checking their hypotheses.

✓ **Right:** first bring the numerator to one fraction. For $x \ne 0$,
$\frac{1}{x} - \frac{1}{3} = \frac{3 - x}{3x}$, so for $x \ne 0$ and $x \ne 3$ the quotient is
$\frac{3 - x}{3x(x - 3)} = -\frac{1}{3x}$. On the window $0 < \abs{x - 3} < 3$, part (b) of
[direct substitution](#cor-calc-direct-substitution) and the lemma give the limit
$-\frac{1}{9}$.
:::

## Rigorous track

:::{admonition} Factoring always ends
:class: dropdown rigor
Let $f = \frac{p}{q}$ be a rational function, where $q$ has degree $m \ge 1$, and let $a$ be a
root of $q$. By [part (b) of the factor theorem](#thm-calc-factor-theorem),
$q(x) = (x - a)\, q_1(x)$ with $q_1$ of degree $m - 1$ (part (a)). If $q_1(a) = 0$, we factor
$q_1$ in the same way, and so on. Each step lowers the degree by one, and a polynomial of degree
$0$ is a non-zero constant, which is not $0$ at $a$. So after $k$ steps, for some $k$ with
$1 \le k \le m$, we reach a polynomial $Q$ with $Q(a) \ne 0$ such that, for every real $x$,
$$
q(x) = (x - a)^k\, Q(x) .
$$
In the same way, if $p$ is not the zero polynomial, $p(x) = (x - a)^j\, P(x)$ for every real
$x$, with $P(a) \ne 0$ and $j \ge 0$ ($j = 0$ when $p(a) \ne 0$). (If $p$ is the zero
polynomial, the limit is $0$. By
[part (b) of the proposition on the domain of a rational function](#prop-calc-rational-domain)
there is an open interval $(\alpha, \beta)$ containing $a$ such that $f$ is defined at every
point of it except possibly $a$; as in the factoring paragraph, it contains a window
$0 < \abs{x - a} < r$. There $f(x) = \frac{0}{q(x)} = 0$, so $f$ agrees with the constant $0$,
whose limit is $0$ by [part (a) of the limit laws](#thm-calc-limit-laws), and the lemma gives
$\lim_{x \to a} f(x) = 0$.) By
[part (b) of the proposition on the domain of a rational function](#prop-calc-rational-domain),
applied to $\frac{P}{Q}$, and as in the factoring paragraph of the main results, there is a window
$0 < \abs{x - a} < r$ on which $Q$ has no root; there $x - a \ne 0$ too, so
$q(x) = (x - a)^k\, Q(x) \ne 0$, by [part (a) of the sign rules](#prop-calc-sign-rules)
applied $k$ times, and $f$ is defined. On that window:

- **If $j \ge k$:** cancelling $(x - a)^k$ gives $f(x) = \frac{(x - a)^{j - k} P(x)}{Q(x)}$, a
  rational function whose denominator is not $0$ at $a$. By
  [part (b) of direct substitution](#cor-calc-direct-substitution) and
  [](#lem-calc-limit-agree-except-point), the limit is $0$ if $j > k$, and $\frac{P(a)}{Q(a)}$ if
  $j = k$.
- **If $j < k$:** the limit does not exist. Suppose $\lim_{x \to a} f(x) = L$. By
  [parts (a), (b) and (e) of the limit laws](#thm-calc-limit-laws),
  $\lim_{x \to a} (x - a)^{k - j} = 0$, so the product law, part (c), gives
  $\lim_{x \to a} (x - a)^{k - j} f(x) = 0 \cdot L = 0$. But on the window,
  $(x - a)^{k - j} f(x) = \frac{P(x)}{Q(x)}$, whose limit is $\frac{P(a)}{Q(a)} \ne 0$, by part (b)
  of direct substitution and the lemma. This contradicts
  [uniqueness of limits](#thm-calc-limit-unique).

So for a rational function, the method of this page always settles a limit of the form
$\frac{0}{0}$: after at most $m$ cancellations it gives the limit, or shows that there is none.
*What this leaves out:* "and so on" stands for an induction on the degree, as in the sketch of
the power law on Limit Laws.
:::

::::{admonition} When the window is one-sided
:class: dropdown rigor
The lemma needs a window on **both** sides of $a$. Consider
$\frac{x - 2}{\sqrt{x - 2}}$ at $a = 2$. It is defined only for $x > 2$, and there, with
$y = x - 2 > 0$, it equals $\frac{y}{\sqrt{y}} = \sqrt{y}$, since $y = \sqrt{y}\,\sqrt{y}$ and
$\sqrt{y} \ne 0$. It is tempting to write
$$
\lim_{x \to 2} \frac{x - 2}{\sqrt{x - 2}} = \lim_{x \to 2} \sqrt{x - 2} = 0 .
$$
But neither function is defined at any $x < 2$, so neither is defined on an open interval
containing $2$ (except at $2$), and [the definition of a limit](#def-calc-limit) applies to
neither. The root law agrees: with $L = 0$, its sign condition asks for $x - 2 \ge 0$ on both
sides of $2$, and it fails on the left. Rewriting cannot create a window that the function does
not have.

:::{admonition} Looking ahead
:class: looking-ahead
Approaching $2$ from the right only is a one-sided limit, the subject of the page One-Sided
Limits. The lemma has a one-sided version, with the same proof.
:::
::::

## Summary

- A limit is **of the form $\frac{0}{0}$** when the numerator and the denominator both approach
  $0$. That is a form, not a value: the quotient law does not apply, and the limit may be any
  number, or not exist.
- **The lemma** ([](#lem-calc-limit-agree-except-point)): if $f(x) = g(x)$ for every $x$ with
  $0 < \abs{x - a} < r$, and $\lim_{x \to a} g(x) = L$, then $\lim_{x \to a} f(x) = L$. The
  values at $a$ play no part.
- **The method:** substitute; if the form is $\frac{0}{0}$, rewrite $f$ for $x \ne a$ as a $g$
  to which the laws apply, compute $\lim g$ with the laws, naming each part, and conclude with
  the lemma.
- **Factoring:** a common root $a$ of numerator and denominator gives a common factor $x - a$
  ([the factor theorem](#thm-calc-factor-theorem)), which may be cancelled for $x \ne a$.
- **Rationalising:** $\bigl(\sqrt{u} - \sqrt{v}\bigr)\bigl(\sqrt{u} + \sqrt{v}\bigr) = u - v$
  for $u, v \ge 0$; then the root law, with $L > 0$, or $L = 0$ and the sign condition.
- **Compound fractions:** bring them to one fraction, then cancel.

## Exercises

::::{exercise} Factor and cancel
:label: exr-calc-computing-limits-factor-quadratic
:class: tier-a

Find $\displaystyle \lim_{x \to -2} \frac{x^2 + 5x + 6}{x + 2}$.

:::{admonition} Hint 1
:class: dropdown hint
Substituting gives $\frac{0}{0}$, so $x + 2 = x - (-2)$ is a factor of the numerator, by the
factor theorem. What is the other factor?
:::

:::{admonition} Answer
:class: dropdown answer
$1$
:::
::::

::::{solution} exr-calc-computing-limits-factor-quadratic
:label: sol-calc-computing-limits-factor-quadratic
:class: dropdown

By [part (a) of direct substitution](#cor-calc-direct-substitution), the numerator approaches
$4 - 10 + 6 = 0$ and the denominator $-2 + 2 = 0$: the form is $\frac{0}{0}$. The quotient is
defined at every $x \ne -2$. Multiplying out confirms $x^2 + 5x + 6 = (x + 2)(x + 3)$, so for
$x \ne -2$, cancelling the non-zero number $x + 2$,
$$
\frac{x^2 + 5x + 6}{x + 2} = x + 3 .
$$
The two functions are defined and agree at every $x$ with $0 < \abs{x + 2} < 1$. By part (a) of
direct substitution, $\lim_{x \to -2} (x + 3) = 1$, and by
[](#lem-calc-limit-agree-except-point) the limit is $1$.
::::

::::{exercise} Factor the numerator and the denominator
:label: exr-calc-computing-limits-factor-both
:class: tier-a

Find $\displaystyle \lim_{x \to 2} \frac{x^2 - x - 2}{x^2 - 4}$.

:::{admonition} Hint 1
:class: dropdown hint
Both the numerator and the denominator are $0$ at $x = 2$, so both have the factor $x - 2$.
:::

:::{admonition} Hint 2
:class: dropdown hint
The denominator has another root. Choose a window around $2$ that does not reach it.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{3}{4}$
:::
::::

::::{solution} exr-calc-computing-limits-factor-both
:label: sol-calc-computing-limits-factor-both
:class: dropdown

At $x = 2$ the numerator is $4 - 2 - 2 = 0$ and the denominator $4 - 4 = 0$, so by
[part (a) of direct substitution](#cor-calc-direct-substitution) the form is $\frac{0}{0}$.
Multiplying out confirms
$$
\begin{aligned}
x^2 - x - 2 &= (x - 2)(x + 1), \\
x^2 - 4 &= (x - 2)(x + 2) .
\end{aligned}
$$
By [part (a) of the sign rules](#prop-calc-sign-rules), the denominator is $0$ only at $x = 2$
and $x = -2$. If $0 < \abs{x - 2} < 1$, then $1 < x < 3$ and $x \ne 2$
([part (e) of the proposition on distance inequalities](#prop-calc-abs-interval)), so
$x + 2 > 3 > 0$ (adding $2$ to $1 < x$, [property 3 of the order rules](#rem-calc-order-rules),
then property 2) and $x - 2 \ne 0$. On this window, cancelling $x - 2$,
$$
\frac{x^2 - x - 2}{x^2 - 4} = \frac{x + 1}{x + 2} .
$$
The right-hand side is a rational function whose denominator is $4 \ne 0$ at $2$, so by
[part (b) of direct substitution](#cor-calc-direct-substitution) its limit is $\frac{3}{4}$, and
by [](#lem-calc-limit-agree-except-point) so is the limit of the left-hand side.
::::

::::{exercise} Rationalise the numerator
:label: exr-calc-computing-limits-conjugate
:class: tier-a

Find $\displaystyle \lim_{x \to 0} \frac{\sqrt{x + 4} - 2}{x}$.

:::{admonition} Hint 1
:class: dropdown hint
Multiply the numerator and the denominator by $\sqrt{x + 4} + 2$, as in
[](#eg-calc-computing-limits-conjugate).
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{4}$
:::
::::

::::{solution} exr-calc-computing-limits-conjugate
:label: sol-calc-computing-limits-conjugate
:class: dropdown

**The window.** If $0 < \abs{x} < 4$, then $-4 < x < 4$ and $x \ne 0$
([part (e) of the proposition on distance inequalities](#prop-calc-abs-interval)), so
$x + 4 > 0$ (adding $4$ to $-4 < x$, [property 3 of the order rules](#rem-calc-order-rules)) and
$\sqrt{x + 4}$ is defined ([the square-root remark](#rem-calc-square-roots)).

**The form.** By [part (a) of direct substitution](#cor-calc-direct-substitution),
$x + 4 \to 4$, and $4 > 0$, so the root law,
[part (f) of the limit laws](#thm-calc-limit-laws), gives $\sqrt{x + 4} \to \sqrt{4} = 2$ (since
$2 \ge 0$ and $2^2 = 4$). So the numerator approaches $0$ (part (b)), and so does the
denominator: the form is $\frac{0}{0}$.

**Rationalise.** On the window, $s = \sqrt{x + 4} \ge 0$, so $s + 2 \ge 2 > 0$, and
$(s - 2)(s + 2) = s^2 - 4 = x$. Cancelling the non-zero number $x$,
$$
\begin{aligned}
\frac{\sqrt{x + 4} - 2}{x} &= \frac{x}{x\,(\sqrt{x + 4} + 2)} \\
  &= \frac{1}{\sqrt{x + 4} + 2} .
\end{aligned}
$$

**Compute and conclude.** The right-hand side is defined at every $x \ge -4$. Its denominator
approaches $2 + 2 = 4 \ne 0$ (parts (a), (b) and (f)), so by part (d) it approaches
$\frac{1}{4}$. By [](#lem-calc-limit-agree-except-point), with $r = 4$, the limit is
$\frac{1}{4}$.
::::

::::{exercise} A compound fraction
:label: exr-calc-computing-limits-compound
:class: tier-a

Find $\displaystyle \lim_{x \to 2} \frac{\frac{1}{x} - \frac{1}{2}}{x - 2}$.

:::{admonition} Hint 1
:class: dropdown hint
Write $\frac{1}{x} - \frac{1}{2}$ as one fraction. Which factor appears in its numerator?
:::

:::{admonition} Answer
:class: dropdown answer
$-\frac{1}{4}$
:::
::::

::::{solution} exr-calc-computing-limits-compound
:label: sol-calc-computing-limits-compound
:class: dropdown

The quotient is defined at every $x$ other than $0$ and $2$. If $0 < \abs{x - 2} < 2$, then
$0 < x < 4$ and $x \ne 2$ ([part (e) of the proposition on distance
inequalities](#prop-calc-abs-interval)), so it is defined on that window. The numerator
approaches $\frac{1}{2} - \frac{1}{2} = 0$ and the denominator $0$
([part (b) of direct substitution](#cor-calc-direct-substitution) and
[part (b) of the limit laws](#thm-calc-limit-laws)): the form is $\frac{0}{0}$.

For $x \ne 0$, $\frac{1}{x} - \frac{1}{2} = \frac{2 - x}{2x}$. For $x \ne 0$ and $x \ne 2$,
since $2 - x = -(x - 2)$ and $x - 2 \ne 0$,
$$
\frac{\frac{1}{x} - \frac{1}{2}}{x - 2} = \frac{-(x - 2)}{2x\,(x - 2)} = -\frac{1}{2x} .
$$
The function $-\frac{1}{2x}$ is rational, with the denominator $4 \ne 0$ at $x = 2$, so by
part (b) of direct substitution its limit at $2$ is $-\frac{1}{4}$. By
[](#lem-calc-limit-agree-except-point), with $r = 2$, the limit is $-\frac{1}{4}$.
::::

::::{exercise} Factoring twice
:label: exr-calc-computing-limits-factor-twice
:class: tier-b

Find $\displaystyle \lim_{x \to 1} \frac{x^3 - 3x + 2}{x^2 - 2x + 1}$.

:::{admonition} Hint 1
:class: dropdown hint
Factor out $x - 1$ from the numerator and the denominator once. Is the new limit still of the
form $\frac{0}{0}$?
:::

:::{admonition} Hint 2
:class: dropdown hint
$x^2 - 2x + 1 = (x - 1)^2$. Divide $x^3 - 3x + 2$ by $x - 1$, and then the quotient by $x - 1$
again.
:::

:::{admonition} Answer
:class: dropdown answer
$3$
:::
::::

::::{solution} exr-calc-computing-limits-factor-twice
:label: sol-calc-computing-limits-factor-twice
:class: dropdown

At $x = 1$ the numerator is $1 - 3 + 2 = 0$ and the denominator $1 - 2 + 1 = 0$, so the form is
$\frac{0}{0}$ ([part (a) of direct substitution](#cor-calc-direct-substitution)).

By [part (b) of the factor theorem](#thm-calc-factor-theorem), $x - 1$ is a factor of both.
Dividing gives $x^3 - 3x + 2 = (x - 1)(x^2 + x - 2)$ and $x^2 - 2x + 1 = (x - 1)(x - 1)$, as
multiplying out confirms. Cancelling $x - 1$ for $x \ne 1$ leaves
$\frac{x^2 + x - 2}{x - 1}$, and at $x = 1$ its numerator $1 + 1 - 2$ and denominator are both
$0$ again. Since $1$ is a root of $x^2 + x - 2$, the factor theorem gives
$x^2 + x - 2 = (x - 1)(x + 2)$. So
$$
\begin{aligned}
x^3 - 3x + 2 &= (x - 1)^2 (x + 2), \\
x^2 - 2x + 1 &= (x - 1)^2 .
\end{aligned}
$$
For $x \ne 1$, $(x - 1)^2 \ne 0$ ([part (a) of the sign rules](#prop-calc-sign-rules)), so
$$
\frac{x^3 - 3x + 2}{x^2 - 2x + 1} = x + 2 .
$$
Both sides are defined and agree at every $x \ne 1$, so on the window $0 < \abs{x - 1} < 1$.
By part (a) of direct substitution, $\lim_{x \to 1} (x + 2) = 3$, and by
[](#lem-calc-limit-agree-except-point) the limit is $3$.
::::

::::{exercise} A square root in the denominator
:label: exr-calc-computing-limits-root-denominator
:class: tier-b

Find $\displaystyle \lim_{x \to 9} \frac{x - 9}{\sqrt{x} - 3}$.

:::{admonition} Hint 1
:class: dropdown hint
For $x \ge 0$, $x - 9 = \bigl(\sqrt{x}\bigr)^2 - 3^2$. Factor it as a difference of squares.
:::

:::{admonition} Answer
:class: dropdown answer
$6$
:::
::::

::::{solution} exr-calc-computing-limits-root-denominator
:label: sol-calc-computing-limits-root-denominator
:class: dropdown

**The window.** If $0 < \abs{x - 9} < 9$, then $0 < x < 18$ and $x \ne 9$
([part (e) of the proposition on distance inequalities](#prop-calc-abs-interval)). So $\sqrt{x}$
is defined there. Also $\sqrt{x} \ne 3$: if $\sqrt{x} = 3$, then $x = \bigl(\sqrt{x}\bigr)^2 = 9$
([the square-root remark](#rem-calc-square-roots)). So the quotient is defined on the window.

**The form.** By [part (a) of the limit laws](#thm-calc-limit-laws), $x \to 9$, and $9 > 0$, so
the root law, part (f), gives $\sqrt{x} \to \sqrt{9} = 3$. The numerator and the denominator
both approach $0$.

**Rewrite.** On the window, $\bigl(\sqrt{x}\bigr)^2 = x$, so
$x - 9 = \bigl(\sqrt{x} - 3\bigr)\bigl(\sqrt{x} + 3\bigr)$, and cancelling the non-zero number
$\sqrt{x} - 3$,
$$
\frac{x - 9}{\sqrt{x} - 3} = \sqrt{x} + 3 .
$$

**Compute and conclude.** By parts (a), (b) and (f), $\sqrt{x} + 3 \to 3 + 3 = 6$. By
[](#lem-calc-limit-agree-except-point), with $r = 9$, the limit is $6$.
::::

::::{exercise} A square root of a square
:label: exr-calc-computing-limits-abs-sqrt
:class: tier-b

True or false: $\displaystyle \lim_{x \to 0} \frac{\sqrt{x^2}}{x}$ exists.

:::{admonition} Hint 1
:class: dropdown hint
Is $\sqrt{x^2}$ equal to $x$ for every $x$? Use
[property 5 of the absolute value](#rem-calc-absolute-value-properties).
:::

:::{admonition} Hint 2
:class: dropdown hint
If the limit were $L$, every window around $0$ would contain a point where the quotient is $1$
and a point where it is ${-1}$. Can both be within $1$ of $L$?
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-computing-limits-abs-sqrt
:label: sol-calc-computing-limits-abs-sqrt
:class: dropdown

False. By [property 5 of the absolute value](#rem-calc-absolute-value-properties),
$\sqrt{x^2} = \abs{x}$, so the function is $f(x) = \frac{\abs{x}}{x}$, defined at every
$x \ne 0$. By [the definition of the absolute value](#def-calc-absolute-value), $f(x) = 1$ for
$x > 0$ and $f(x) = \frac{-x}{x} = -1$ for $x < 0$. (The limit is of the form $\frac{0}{0}$:
$\abs{x} \to 0$, as shown in the rationalising paragraph, and $x \to 0$.)

Suppose that $\lim_{x \to 0} f(x) = L$. For the tolerance $\eps = 1$,
[the definition of a limit](#def-calc-limit) gives a $\delta > 0$ such that
$\abs{f(x) - L} < 1$ at every $x$ with $0 < \abs{x} < \delta$. The points
$\frac{\delta}{2}$ and $-\frac{\delta}{2}$ are in this window, so $\abs{1 - L} < 1$ and
$\abs{-1 - L} < 1$, and $\abs{L - (-1)} = \abs{-1 - L}$ by
[property 2 of the absolute value](#rem-calc-absolute-value-properties). By
[part (b) of the triangle inequality](#thm-calc-triangle-inequality), with $x = 1$, $y = -1$
and $z = L$,
$$
\begin{aligned}
2 &= \abs{1 - (-1)} \\
  &\le \abs{1 - L} + \abs{L - (-1)} \\
  &< 1 + 1 = 2,
\end{aligned}
$$
which is impossible. So no real number $L$ is the limit: the limit does not exist.

The function agrees with the constant $1$ at every $x > 0$, but not on any whole window
around $0$, so [](#lem-calc-limit-agree-except-point) does not apply.
::::

::::{exercise} An absolute value in the denominator
:label: exr-calc-computing-limits-abs-denominator
:class: tier-b

Find $\displaystyle \lim_{x \to 0} \frac{\sqrt{4 + x^2} - 2}{\abs{x}}$, and say where you use
the sign condition of the root law.

:::{admonition} Hint 1
:class: dropdown hint
Rationalise the numerator, and use $x^2 = \abs{x}^2$
([property 5 of the absolute value](#rem-calc-absolute-value-properties)).
:::

:::{admonition} Hint 2
:class: dropdown hint
After cancelling, $\abs{x}$ is left in the numerator. Its limit at $0$ is in the rationalising
paragraph of the main results.
:::

:::{admonition} Answer
:class: dropdown answer
$0$
:::
::::

::::{solution} exr-calc-computing-limits-abs-denominator
:label: sol-calc-computing-limits-abs-denominator
:class: dropdown

The quotient is defined at every $x \ne 0$: $4 + x^2 \ge 4 > 0$, because $x^2 \ge 0$
([part (c) of the sign rules](#prop-calc-sign-rules)), and $\abs{x} \ne 0$ for $x \ne 0$
([property 1 of the absolute value](#rem-calc-absolute-value-properties)).

**The form.** By [part (a) of direct substitution](#cor-calc-direct-substitution),
$4 + x^2 \to 4 > 0$, so the root law, [part (f) of the limit laws](#thm-calc-limit-laws), gives
$\sqrt{4 + x^2} \to 2$, and the numerator approaches $0$. The denominator $\abs{x}$ approaches
$0$: it equals $\sqrt{x^2}$, and $x^2 \to 0$ with $x^2 \ge 0$ for every $x$, so the root law
with $L = 0$ applies, its sign condition holding on every window. The form is $\frac{0}{0}$.

**Rewrite.** For $x \ne 0$, let $s = \sqrt{4 + x^2}$. Then $s \ge 0$, so $s + 2 > 0$, and
$(s - 2)(s + 2) = s^2 - 4 = x^2 = \abs{x}^2$ ([the square-root remark](#rem-calc-square-roots)
and [property 5 of the absolute value](#rem-calc-absolute-value-properties)). Cancelling the
non-zero number $\abs{x}$,
$$
\begin{aligned}
\frac{\sqrt{4 + x^2} - 2}{\abs{x}} &= \frac{\abs{x}^2}{\abs{x}\,(s + 2)} \\
  &= \frac{\abs{x}}{\sqrt{4 + x^2} + 2} .
\end{aligned}
$$

**Compute and conclude.** The right-hand side is defined at every real $x$. Its numerator
approaches $0$, by the root law with $L = 0$ as above (this is where the sign condition is
used), and its denominator approaches $2 + 2 = 4 \ne 0$ (parts (a), (b) and (f)). By part (d),
it approaches $\frac{0}{4} = 0$. By [](#lem-calc-limit-agree-except-point), with $r = 1$, the
limit is $0$.
::::

::::{exercise} How fast the image moves
:label: exr-calc-computing-limits-lens
:class: tier-b applied

In [an exercise on Limit Laws](#exr-calc-limit-laws-lens), a thin lens of focal length $5$ cm forms the image
of an object at distance $u$ cm at the distance
$$
v(u) = \frac{5u}{u - 5}
$$
cm from the lens, for $u > 5$; at $u = 15$ the image is at $v(15) = \frac{15}{2}$ cm. Find
$$
\lim_{u \to 15} \frac{v(u) - \frac{15}{2}}{u - 15},
$$
the rate at which the image moves as the object passes $15$ cm, in cm per cm.

:::{admonition} Hint 1
:class: dropdown hint
Write $v(u) - \frac{15}{2}$ as one fraction, with the denominator $2(u - 5)$.
:::

:::{admonition} Answer
:class: dropdown answer
$-\frac{1}{4}$
:::
::::

::::{solution} exr-calc-computing-limits-lens
:label: sol-calc-computing-limits-lens
:class: dropdown

**The window.** If $0 < \abs{u - 15} < 10$, then $5 < u < 25$ and $u \ne 15$
([part (e) of the proposition on distance inequalities](#prop-calc-abs-interval)), so
$u - 5 > 0$ (adding ${-5}$ to $5 < u$, [property 3 of the order rules](#rem-calc-order-rules)),
$v(u)$ is defined, and so is the quotient.

**The form.** $v$ is the restriction of the rational function $\frac{5u}{u - 5}$ to
$(5, \infty)$, which contains $15$, and $15 - 5 = 10 \ne 0$. By
[part (c) of direct substitution](#cor-calc-direct-substitution), $v(u) \to \frac{15}{2}$, so
the numerator approaches $0$ ([part (b) of the limit laws](#thm-calc-limit-laws)), and so does
the denominator.

**One fraction.** For $u > 5$,
$$
\begin{aligned}
v(u) - \frac{15}{2} &= \frac{10u - 15(u - 5)}{2(u - 5)} \\
  &= \frac{75 - 5u}{2(u - 5)} \\
  &= \frac{-5(u - 15)}{2(u - 5)} .
\end{aligned}
$$
For $u \ne 15$, cancelling the non-zero number $u - 15$,
$$
\frac{v(u) - \frac{15}{2}}{u - 15} = -\frac{5}{2(u - 5)} .
$$

**Compute and conclude.** The right-hand side is a rational function whose denominator is
$20 \ne 0$ at $u = 15$, so by [part (b) of direct substitution](#cor-calc-direct-substitution)
its limit is $-\frac{5}{20} = -\frac{1}{4}$. By [](#lem-calc-limit-agree-except-point), with
$r = 10$, the limit is $-\frac{1}{4}$.

So as the object moves away from the lens through $15$ cm, the image moves towards the lens, by
about a quarter of the distance the object moves. Units: cm divided by cm.
::::

::::{exercise} A power minus one
:label: exr-calc-computing-limits-power
:class: tier-c

Let $n \ge 1$ be an integer. Find $\displaystyle \lim_{x \to 1} \frac{x^n - 1}{x - 1}$, in terms
of $n$.

:::{admonition} Hint 1
:class: dropdown hint
Show that $(x - 1)(x^{n-1} + x^{n-2} + \dots + x + 1) = x^n - 1$ by multiplying out: almost
every term cancels.
:::

:::{admonition} Hint 2
:class: dropdown hint
How many terms does $x^{n-1} + \dots + x + 1$ have, and what is each of them at $x = 1$?
:::

:::{admonition} Answer
:class: dropdown answer
$n$
:::
::::

::::{solution} exr-calc-computing-limits-power
:label: sol-calc-computing-limits-power
:class: dropdown

At $x = 1$ the numerator is $1 - 1 = 0$ and the denominator $0$, so the form is $\frac{0}{0}$
([part (a) of direct substitution](#cor-calc-direct-substitution)). The quotient is defined at
every $x \ne 1$.

Let $s(x) = x^{n-1} + x^{n-2} + \dots + x + 1$, the sum of the $n$ terms $x^k$ for
$k = 0, 1, \dots, n - 1$ (with $x^0 = 1$). Multiplying $s(x)$ by $x$ gives
$x^n + x^{n-1} + \dots + x$, and multiplying it by $-1$ gives $-x^{n-1} - \dots - x - 1$. In the
sum of the two, every term cancels except $x^n$ and ${-1}$, so, for every real $x$,
$$
(x - 1)\, s(x) = x^n - 1 .
$$
(For $n = 1$, $s(x) = 1$.) This is the factorisation that
[the factor theorem](#thm-calc-factor-theorem) promises, since $1^n - 1 = 0$. So for $x \ne 1$,
cancelling the non-zero number $x - 1$, $\frac{x^n - 1}{x - 1} = s(x)$, and the two functions
agree on the window $0 < \abs{x - 1} < 1$.

$s$ is a polynomial, so by part (a) of direct substitution
$\lim_{x \to 1} s(x) = s(1) = 1 + 1 + \dots + 1 = n$, a sum of $n$ ones. By
[](#lem-calc-limit-agree-except-point), the limit is $n$.

For $n = 3$ this is the limit $3$ of $\frac{x^3 - 1}{x - 1}$; compare the cube of
[](#eg-calc-computing-limits-factor), at $a = 2$ instead of $1$.
::::

::::{exercise} When the denominator approaches zero
:label: exr-calc-computing-limits-numerator-zero
:class: tier-c rigor

Let $a$ be a real number, and let $f$ be a function such that
$\lim_{x \to a} \frac{f(x)}{x - a}$ exists. Prove that $\lim_{x \to a} f(x) = 0$.

:::{admonition} Hint 1
:class: dropdown hint
For $x \ne a$ at which $f$ is defined, $f(x) = (x - a) \cdot \frac{f(x)}{x - a}$. Which law gives
the limit of the right-hand side?
:::

:::{admonition} Hint 2
:class: dropdown hint
You need a window on which $f$ is defined. Where does it come from?
:::

:::{admonition} Answer
:class: dropdown answer manual
With $h(x) = \frac{f(x)}{x - a}$: $f(x) = (x - a)\,h(x)$ for $x \ne a$, so the product law and
the lemma give $\lim_{x \to a} f(x) = 0 \cdot \lim_{x \to a} h(x) = 0$.
:::
::::

::::{solution} exr-calc-computing-limits-numerator-zero
:label: sol-calc-computing-limits-numerator-zero
:class: dropdown

Let $h(x) = \frac{f(x)}{x - a}$, which is defined at every $x \ne a$ at which $f$ is defined, and
let $M = \lim_{x \to a} h(x)$.

**A window.** By the domain clause of [the definition of a limit](#def-calc-limit), with the
tolerance $1$, there is an $r > 0$ such that $h$ is defined at every $x$ with
$0 < \abs{x - a} < r$. At each such $x$, $f(x)$ is defined, because $h(x)$ is.

**The product.** By [parts (a) and (b) of the limit laws](#thm-calc-limit-laws),
$\lim_{x \to a} (x - a) = a - a = 0$, and $x - a$ is defined for every $x$. Both $x - a$ and $h$
are defined at every point of the open interval $(a - r, a + r)$ except $a$
([part (e) of the proposition on distance inequalities](#prop-calc-abs-interval)), so the product
law, part (c), gives
$$
\lim_{x \to a} (x - a)\, h(x) = 0 \cdot M = 0 .
$$

**The lemma.** At every $x$ with $0 < \abs{x - a} < r$, the number $x - a$ is not $0$, and
$(x - a)\, h(x) = (x - a) \cdot \frac{f(x)}{x - a} = f(x)$. So $f$ and the product are both
defined and agree on this window, and by [](#lem-calc-limit-agree-except-point),
$\lim_{x \to a} f(x) = 0$.

In words: if the denominator of a quotient approaches $0$ and the quotient has a limit, then the
numerator approaches $0$. A limit "of the form $\frac{c}{0}$" with $c \ne 0$ does not exist,
which is what [Limit Laws](#sec-calc-limit-laws-not-apply) found for $\frac{1}{x}$.
::::

::::{exercise} Choosing a constant
:label: exr-calc-computing-limits-find-constant
:class: tier-c

Let $c$ be a real number. (a) Find the value of $c$ for which
$\displaystyle \lim_{x \to 2} \frac{x^2 + cx - 10}{x - 2}$ exists, and show that it is the only
one. (b) For that $c$, find the limit.

:::{admonition} Hint 1
:class: dropdown hint
If the limit exists, what must the numerator approach? Compare
[](#exr-calc-computing-limits-numerator-zero).
:::

:::{admonition} Hint 2
:class: dropdown hint
For that $c$, the numerator has the root $2$. Factor it.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $3$ (b) $7$
:::
::::

::::{solution} exr-calc-computing-limits-find-constant
:label: sol-calc-computing-limits-find-constant
:class: dropdown

Let $p(x) = x^2 + cx - 10$ and $h(x) = \frac{p(x)}{x - 2}$, defined at every $x \ne 2$.

(a) **Only $c = 3$ can work.** Suppose $\lim_{x \to 2} h(x) = M$. By
[parts (a) and (b) of the limit laws](#thm-calc-limit-laws), $\lim_{x \to 2} (x - 2) = 0$, and
the product law, part (c), gives $\lim_{x \to 2} (x - 2)\, h(x) = 0 \cdot M = 0$. For $x \ne 2$,
$(x - 2)\, h(x) = p(x)$, so the product and the polynomial $p$ agree at every $x$ with
$0 < \abs{x - 2} < 1$. By [part (a) of direct substitution](#cor-calc-direct-substitution),
$\lim_{x \to 2} p(x) = p(2) = 2c - 6$, and by [](#lem-calc-limit-agree-except-point), with $p$
in the role of $g$, the product has the limit $2c - 6$ too. By
[uniqueness of limits](#thm-calc-limit-unique), $2c - 6 = 0$, so $c = 3$. (This is the argument
of [](#exr-calc-computing-limits-numerator-zero), for this $f$.)

**And $c = 3$ works.** For $c = 3$, $p(2) = 4 + 6 - 10 = 0$, and multiplying out confirms
$x^2 + 3x - 10 = (x - 2)(x + 5)$. For $x \ne 2$, cancelling the non-zero number $x - 2$ gives
$h(x) = x + 5$; the two functions agree on the window $0 < \abs{x - 2} < 1$.

(b) By part (a) of direct substitution, $\lim_{x \to 2} (x + 5) = 7$, and by the lemma
$\lim_{x \to 2} h(x) = 7$.

For every other $c$, the limit does not exist, as (a) shows: the numerator then approaches
$2c - 6 \ne 0$ while the denominator approaches $0$.
::::

## Where this leads

:::{where-this-leads}
:::

The method of this page, rewrite and then let the lemma carry the limit back, is used again
whenever a limit is of the form $\frac{0}{0}$.

:::{admonition} Looking ahead
:class: looking-ahead
Some limits of the form $\frac{0}{0}$ resist every algebraic rewriting, because the function is
not built from polynomials and square roots. The page The Squeeze Theorem brings a new tool for
them: it traps a function between two others that have the same limit.
:::
