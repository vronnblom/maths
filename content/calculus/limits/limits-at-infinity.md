---
title: Limits at Infinity and Horizontal Asymptotes
label: calc-limits-at-infinity
description: >-
  What it means for f(x) to approach a number, or to grow without bound, as x grows without
  bound in either direction; the limit laws at infinity; the limits of rational functions and of
  expressions with square roots; horizontal asymptotes; and how powers compare in growth.
tags: [limits, epsilon-delta, proofs]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 3
  est_minutes: 50
  prerequisites: [calc-limit-laws, calc-infinite-limits]
  objectives:
    - Compute limits at ±∞ of rational and root expressions.
    - Find horizontal asymptotes.
    - Compare growth informally.
  verify: verify/calculus/limits/test_limits_at_infinity.py
  widgets: []
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

On the page [Limit Laws](#calc-limit-laws) we met two resistors in parallel, of $3$ ohms and $t$
ohms, with the combined resistance
$$
R(t) = \frac{3t}{3 + t}
$$
ohms, for $t > 0$, and we found what it approaches as $t$ approaches $6$. Now replace the second
resistor by larger and larger ones. What happens to the combined resistance? Rounded, in ohms:

- $t = 10$ gives $R(10) \approx 2.3077$;
- $t = 100$ gives $R(100) \approx 2.9126$;
- $t = 1000$ gives $R(1000) \approx 2.9910$;
- $t = 1\,000\,000$ gives $R(1\,000\,000) \approx 2.999991$.

The values creep up towards $3$ and never reach it. Indeed, for every $t > 0$,
$$
3 - R(t) = \frac{3(3 + t) - 3t}{3 + t} = \frac{9}{3 + t},
$$
which is positive, and as small as we like when $t$ is large enough: it is less than $0.001$ as
soon as $t > 8997$. A huge resistor in parallel lets almost no current through, so the pair
behaves almost like the $3$-ohm resistor alone.

This is a new kind of limit. The variable $t$ does not approach a number $a$: it grows without
bound. We will write $\lim_{t \to \infty} R(t) = 3$, and say that the line $y = 3$ is a
horizontal asymptote of the graph of $R$. We also want to describe $x \to -\infty$, and values
that grow without bound themselves, as $x^2$ does when $x$ grows. This page defines all of
these precisely, carries the limit laws over to them, and uses the laws to find the limits of
every rational function and of some expressions with square roots.

## Limits as $x$ grows without bound

Informally, $\lim_{x \to \infty} f(x) = L$ means that $f(x)$ is as close to $L$ as we like for
**all** $x$ large enough. The ε–δ game of [the definition of the limit](#def-calc-limit) changes
in one place: the challenger still names a tolerance $\eps > 0$, but instead of a window
$0 < \abs{x - a} < \delta$ around a point $a$ you reply with a **threshold** $N$, and you win if
every $x > N$ has $f(x)$ within $\eps$ of $L$. The window is now the ray of all $x > N$. For
values that grow without bound, such as $x^2$, the challenger names a height $B$ instead, and
you win if $f(x) > B$ for every $x > N$. Values of $f$ at small $x$ play no part; $f$ only has to
be defined from some point on.

:::{proof:definition} Limits at infinity
:label: def-calc-limit-at-infinity

Let $f$ be a function and $L$ a real number.

(a) Let $f$ be defined at every point of an interval $(c, \infty)$, for some real number $c$. We
say that **the limit of $f(x)$ as $x$ tends to infinity is $L$**, and write
$$
\lim_{x \to \infty} f(x) = L,
$$
if for every $\eps > 0$ there is a real number $N$ such that $f$ is defined at every $x > N$, and
$$
x > N \quad\text{implies}\quad \abs{f(x) - L} < \eps .
$$

(b) Let $f$ be defined at every point of an interval $(-\infty, c)$, for some real number $c$.
We say that **the limit of $f(x)$ as $x$ tends to minus infinity is $L$**, and write
$\lim_{x \to -\infty} f(x) = L$, if for every $\eps > 0$ there is a real number $N$ such that
$f$ is defined at every $x < N$, and
$$
x < N \quad\text{implies}\quad \abs{f(x) - L} < \eps .
$$

(c) Let $f$ be as in (a). We write $\lim_{x \to \infty} f(x) = \infty$ if for every real number
$B$ there is a real number $N$ such that $f$ is defined at every $x > N$, and
$$
x > N \quad\text{implies}\quad f(x) > B ;
$$
and $\lim_{x \to \infty} f(x) = -\infty$ if the same holds with $f(x) < B$ in place of
$f(x) > B$.

(d) Let $f$ be as in (b). We write $\lim_{x \to -\infty} f(x) = \infty$, respectively
$\lim_{x \to -\infty} f(x) = -\infty$, if for every real number $B$ there is a real number $N$
such that $f$ is defined at every $x < N$, and $x < N$ implies $f(x) > B$, respectively
$f(x) < B$.

We also write $f(x) \to L$ as $x \to \infty$, and so on. These are the **limits at infinity**.
:::

**In words.** Parts (a) and (b) are the game of [the definition of the limit](#def-calc-limit)
with the punctured window $0 < \abs{x - a} < \delta$ replaced by the ray $x > N$, or $x < N$.
Parts (c) and (d) replace the tolerance band around $L$ by a height $B$ that the values must
stay above, or below, from the threshold on. Four points to notice:

- If a threshold $N$ wins a round, so does every larger one when $x \to \infty$ (every smaller
  one when $x \to -\infty$): if $N' \ge N$ and $x > N'$, then $x > N$ by transitivity
  ([property 2 of the order rules](#rem-calc-order-rules)). So $N$ may be taken as large as we
  like, and it depends on $\eps$ (or $B$), never on $x$.
- Since $f$ is defined on $(c, \infty)$ in (a), every $N \ge c$ meets the requirement that $f$
  be defined at every $x > N$. That requirement only rules out thresholds that are too small,
  as the window's domain clause in [the definition of the limit](#def-calc-limit) only rules
  out windows that are too wide.
- The symbols $\infty$ and $-\infty$ are not real numbers. "$\lim_{x \to \infty} f(x) = \infty$"
  does not say that a limit exists: it says how the limit fails to exist as a real number,
  because the values eventually exceed every real number (property 1 of [the remark
  below](#rem-calc-limit-at-infinity-facts) proves this). This is the convention that the page
  Infinite Limits and Vertical Asymptotes uses for infinite limits at a point $a$.
  % TODO link: prop-calc-infinite-limit-no-real-limit once vronnblom/maths#30 is merged
  When we say that a limit at infinity **exists**, we mean that it is a real number.
- On the page Infinite Limits and Vertical Asymptotes the heights are $M > 0$; that is the same
  condition, since a threshold that wins the height $\max(B, 1)$ also wins $B$: if
  $f(x) > \max(B, 1)$, then $f(x) > B$, by transitivity. (For $-\infty$, the heights there are
  $-M$ with $M > 0$, and the height $-\max(-B, 1)$ plays the same role.)

**Example.** $\lim_{x \to \infty} \frac{1}{x} = 0$, by part (a). The function is defined at
every $x > 0$, so on $(0, \infty)$. Let $\eps > 0$ and take $N = \frac{1}{\eps}$, which is
positive by [property 6 of the order rules](#rem-calc-order-rules). If $x > N$, then
$0 < \frac{1}{\eps} < x$, and property 6 gives $\frac{1}{x} < \frac{1}{1/\eps} = \eps$ and
$\frac{1}{x} > 0$. So $\abs{\frac{1}{x} - 0} = \frac{1}{x} < \eps$, by
[the definition of the absolute value](#def-calc-absolute-value).

**Example.** $\lim_{x \to \infty} x^2 = \infty$, by part (c). Let $B$ be a real number and take
$N$ to be the larger of $1$ and $B$. If $x > N$, then $x > 1$ and $x > B$. Multiplying $x > 1$ by
the positive number $x$ keeps the inequality ([property 5(a) of the order
rules](#rem-calc-order-rules)): $x^2 > x$. So $x^2 > x > B$, and $x^2 > B$ by transitivity.

**Non-example.** No real number $L$ is the limit of $x^2$ as $x \to \infty$. Take $\eps = 1$.
Whatever $N$ is offered, let $x$ be $1$ more than the larger of $N$ and $\abs{L} + 1$. Then
$x > N$, and $x > \abs{L} + 1 \ge 1$, so as in the example $x^2 > x > \abs{L} + 1$. Adding $-L$
to both sides ([property 3 of the order rules](#rem-calc-order-rules)), and using
$\abs{L} - L \ge 0$ ([property 3 of the absolute value](#rem-calc-absolute-value-properties)),
gives $x^2 - L > \abs{L} - L + 1 \ge 1$. So $x^2 - L$ is positive, and
$\abs{x^2 - L} = x^2 - L > 1 = \eps$: the threshold $N$ loses the round $\eps = 1$.

The figure shows one round of the game of part (a).

:::{figure} ./img/limit-at-infinity-band.svg
:label: fig-calc-limits-at-infinity-band
:alt: The graph of y equals (2x squared plus x) over (x squared plus 1) for x from about 1.25 to 16, shown for heights between 1.7 and 2.15 only. A horizontal band runs between the dashed lines y = 1.9 and y = 2.1, with the dotted line y = 2 in its middle. The graph rises steeply, crosses y = 2 at x = 2, leaves the band through its upper edge at x = 3, peaks just above it near x = 4, comes back to the upper edge at x = 7 and then stays inside the band, slowly approaching y = 2 from above. A dashed vertical line marks x = 7, labelled N = 7, and the region to its right is shaded.

The graph of $f(x) = \frac{2x^2 + x}{x^2 + 1}$, with the band $1.9 < y < 2.1$ of half-width
$\eps = 0.1$ around $y = 2$; the vertical axis shows only the heights from $1.7$ to $2.15$. The
graph crosses the line $y = 2$ at $x = 2$, leaves the band at $x = 3$ and returns to it at
$x = 7$. To the right of the threshold $N = 7$ (shaded) it stays inside the band.
:::

For this $\eps$, the threshold $N = 7$ wins the round, and no smaller threshold does
([](#exr-calc-limits-at-infinity-figure-threshold) proves both). A smaller $\eps$ needs a larger
$N$. The graph meets the line $y = 2$ and leaves the band before it settles: the definition does
not care what happens before the threshold.

Before we use the definition, three facts that make it easier to use. The first says that we may
speak of *the* limit at infinity.

:::{proof:remark} Three facts about limits at infinity
:label: rem-calc-limit-at-infinity-facts

1. **Uniqueness.** A function has at most one limit as $x \to \infty$, counting $\infty$ and
   $-\infty$: if $\lim_{x \to \infty} f(x) = L$ and $\lim_{x \to \infty} f(x) = M$, where each of
   $L$ and $M$ is a real number, $\infty$ or $-\infty$, then $L = M$. The same holds as
   $x \to -\infty$.
2. **Only the tail matters.** Let $f$ and $g$ be defined at every point of $(c, \infty)$, with
   $f(x) = g(x)$ at every $x > c$. Then, for $L$ a real number, $\infty$ or $-\infty$,
   $\lim_{x \to \infty} f(x) = L$ if and only if $\lim_{x \to \infty} g(x) = L$. The same holds
   as $x \to -\infty$, for $f$ and $g$ defined on $(-\infty, c)$ with $f(x) = g(x)$ at every
   $x < c$.
3. **Reflection.** Let $f$ be defined at every point of $(-\infty, c)$, and let $g(t) = f(-t)$.
   Then $g$ is defined at every point of $(-c, \infty)$, and, for $L$ a real number, $\infty$ or
   $-\infty$, $\lim_{x \to -\infty} f(x) = L$ if and only if $\lim_{t \to \infty} g(t) = L$.

*Reason.* **1.** Suppose $L \ne M$. In each case below we name a round for each of the two
limits; let $N_1$ and $N_2$ be thresholds that win them, and let $x$ be $1$ more than the larger
of $N_1$ and $N_2$. Then $x > N_1$ and $x > N_2$, so $f(x)$ is defined and satisfies both
inequalities.

- *$L$ and $M$ real.* Take the round $\eps = \frac12 \abs{L - M}$ for both, which is positive by
  [property 1 of the absolute value](#rem-calc-absolute-value-properties). By
  [part (b) of the triangle inequality](#thm-calc-triangle-inequality), applied to the numbers
  $L$, $M$ and $f(x)$ in the roles of $x$, $y$ and $z$ there, by property 2 of the absolute
  value, and by adding the two strict inequalities $\abs{f(x) - L} < \eps$ and
  $\abs{f(x) - M} < \eps$ ([property 4 of the order rules](#rem-calc-order-rules)),
  $\abs{L - M} \le \abs{f(x) - L} + \abs{f(x) - M} < 2\eps = \abs{L - M}$, which is impossible.
- *$L$ real and $M = \infty$.* Take $\eps = 1$ for $L$ and $B = L + 1$ for $M$. Then
  $\abs{f(x) - L} < 1$ gives $f(x) < L + 1$, by
  [part (a) of the proposition on distance inequalities](#prop-calc-abs-interval), while
  $f(x) > L + 1$: impossible, by trichotomy ([property 1 of the order
  rules](#rem-calc-order-rules)). For $M = -\infty$, take $B = L - 1$: then $f(x) > L - 1$ and
  $f(x) < L - 1$.
- *$L = \infty$ and $M = -\infty$.* Take $B = 0$ for both: then $f(x) > 0$ and $f(x) < 0$.

The cases with $L$ and $M$ exchanged are the same. As $x \to -\infty$, let $x$ be $1$ less than
the smaller of $N_1$ and $N_2$.

**2.** If a threshold $N$ wins a round for $f$, let $N'$ be the larger of $N$ and $c$. If
$x > N'$, then $x > N$ and $x > c$, so $g(x)$ is defined and equals $f(x)$, which satisfies the
round's inequality. So $N'$ wins the same round for $g$. Exchanging $f$ and $g$ gives the
converse. As $x \to -\infty$, take the smaller of $N$ and $c$.

**3.** Multiplying by the negative number ${-1}$ reverses an inequality ([property 5(c) of the
order rules](#rem-calc-order-rules)), so $t > -c$ exactly when $-t < c$: then $g(t) = f(-t)$ is
defined. If $N$ wins a round for $\lim_{x \to -\infty} f(x)$, then $-N$ wins the same round for
$\lim_{t \to \infty} g(t)$: if $t > -N$, then $-t < N$, so $g(t) = f(-t)$ is defined and
satisfies the round's inequality. Conversely, if $N$ wins a round for $g$, then $-N$ wins it for
$f$: if $x < -N$, then $-x > N$, and $f(x) = f(-(-x)) = g(-x)$.
:::

### Horizontal asymptotes

A limit at infinity describes the far ends of a graph. When the limit is a real number $L$, the
graph runs ever closer to the horizontal line $y = L$.

:::{proof:definition} Horizontal asymptote
:label: def-calc-horizontal-asymptote

Let $L$ be a real number. The line $y = L$ is a **horizontal asymptote** of the graph of a
function $f$ if
$$
\lim_{x \to \infty} f(x) = L \quad\text{or}\quad \lim_{x \to -\infty} f(x) = L .
$$
:::

**In words.** Far to the right, or far to the left, the graph comes as close to the line
$y = L$ as we like and stays that close.

**Example.** The line $y = 3$ is a horizontal asymptote of the graph of the combined resistance
$R$ of Why this matters, which is defined only for $t > 0$, so only the direction $t \to \infty$
is available ([](#eg-calc-limits-at-infinity-resistors) proves the limit). The line $y = 2$ is a
horizontal asymptote of the graph in [](#fig-calc-limits-at-infinity-band): as the figure shows,
a graph may cross its horizontal asymptote.

**Non-example.** The graph of $x^2$ has no horizontal asymptote. As $x \to \infty$ its limit is
$\infty$, so by [property 1 of the remark](#rem-calc-limit-at-infinity-facts) it is no real
number $L$. As $x \to -\infty$ the same holds, by property 3 of the remark: $g(t) = (-t)^2 = t^2$.

By property 1 of the remark, a graph has at most two horizontal asymptotes, one for each
direction. Each of the two directions may give the same line, a different one, or none.

**Horizontal and vertical asymptotes.** The page Infinite Limits and Vertical Asymptotes defines
a **vertical asymptote** $x = a$: a vertical line near which $f(x)$ tends to $\infty$ or to
$-\infty$ as $x$ approaches the number $a$ from at least one side.
% TODO link: def-calc-vertical-asymptote once vronnblom/maths#30 is merged
The roles of $x$ and $y$ are exchanged. At a vertical asymptote, $x$ approaches a number and
$f(x)$ grows or falls without bound; at a horizontal asymptote, $x$ grows without bound and $f(x)$
approaches a number. A graph may have many vertical asymptotes, but at most two horizontal ones;
and it meets a vertical line $x = a$ at most once, because $f$ has at most one value at $a$, while
it may cross a horizontal asymptote. The graph of $\frac{1}{x}$ has both kinds:
the line $y = 0$, as $x \to \infty$ by the example above, and the line $x = 0$, by the limits of
reciprocal powers on Infinite Limits and Vertical Asymptotes.
% TODO link: prop-calc-reciprocal-power-limits once vronnblom/maths#30 is merged

## Main results

### The limit laws at infinity

The limit laws of [Limit Laws](#calc-limit-laws) hold at infinity too, with the same hypotheses.
Part (a) differs: the function $x$ has no real limit as $x \to \infty$, so the identity law
becomes a statement about $\infty$.

:::{proof:theorem} Limit laws at infinity
:label: thm-calc-limit-laws-at-infinity

- **(a) Constants and the identity.** For every real number $c$,
  $\lim_{x \to \infty} c = c$ and $\lim_{x \to -\infty} c = c$. Also
  $\lim_{x \to \infty} x = \infty$ and $\lim_{x \to -\infty} x = -\infty$.

Now let $f$ and $g$ be functions, each defined at every point of an interval $(\alpha, \infty)$,
for some real number $\alpha$, such that $\lim_{x \to \infty} f(x) = L$ and $\lim_{x \to \infty} g(x) = M$,
where $L$ and $M$ are real numbers. Then, all limits being taken as $x \to \infty$:

- **(b) Sum and difference.** $\lim \bigl(f(x) + g(x)\bigr) = L + M$ and
  $\lim \bigl(f(x) - g(x)\bigr) = L - M$.
- **(c) Product.** $\lim f(x)\,g(x) = LM$. In particular, $\lim c\,f(x) = cL$ for every real
  number $c$.
- **(d) Quotient.** If $M \ne 0$, then $\lim \dfrac{f(x)}{g(x)} = \dfrac{L}{M}$.
- **(e) Power.** For every integer $n \ge 1$, $\lim \bigl(f(x)\bigr)^n = L^n$.
- **(f) Square root.** If $L > 0$, then $\lim \sqrt{f(x)} = \sqrt{L}$. If $L = 0$, and there is a
  real number $K$ such that $f(x) \ge 0$ for every $x > K$, then $\lim \sqrt{f(x)} = 0$.

In each of (b)–(f), the function whose limit is taken is defined at every point of some interval
$(\alpha', \infty)$, so that [](#def-calc-limit-at-infinity) applies to it. The same statements
hold as $x \to -\infty$, for $f$ and $g$ defined on an interval $(-\infty, \alpha)$, with "for
every $x < K$" in (f) and intervals $(-\infty, \alpha')$ in the conclusion.
:::

:::{proof:proof} Sketch
:enumerated: false
The proofs on the page [Limit Laws](#calc-limit-laws) carry over with rays in place of
windows, and the larger of two thresholds in place of the smaller of two window widths.

Those proofs use the window $0 < \abs{x - a} < \delta$ in only two ways. They take a window from
the definition of the limit for each function involved, one round each; and then they take a
window inside all of these, $\delta = \min(\delta_1, \delta_2)$, or the smallest of three. Every
inequality after that is about the numbers $f(x)$ and $g(x)$ at one $x$ in that window. At
infinity, [](#def-calc-limit-at-infinity) gives a threshold for each round instead, and the ray
$x > N$ with $N = \max(N_1, N_2)$ lies inside both rays $x > N_1$ and $x > N_2$: if $x > N$, then
$x > N_1$ and $x > N_2$, by transitivity, since $N \ge N_1$ and $N \ge N_2$. So each proof
carries over with $N = \max(N_1, N_2)$ in place of $\delta = \min(\delta_1, \delta_2)$, and with
its inequalities unchanged.

**(b), the sum, written out.** Let $\eps > 0$. There are thresholds $N_1$ and $N_2$ such that $f$
is defined and $\abs{f(x) - L} < \frac{\eps}{2}$ at every $x > N_1$, and $g$ is defined and
$\abs{g(x) - M} < \frac{\eps}{2}$ at every $x > N_2$. Let $N = \max(N_1, N_2)$ and $x > N$. Then
$f(x)$ and $g(x)$ are defined, and by [part (a) of the triangle
inequality](#thm-calc-triangle-inequality), then adding the two strict inequalities
([property 4 of the order rules](#rem-calc-order-rules)),
$$
\begin{aligned}
&\abs{\bigl(f(x) + g(x)\bigr) - (L + M)} \\
&\quad \le \abs{f(x) - L} + \abs{g(x) - M} \\
&\quad < \frac{\eps}{2} + \frac{\eps}{2} = \eps .
\end{aligned}
$$
So $f + g$ is defined at every $x > N$, and $N$ wins the round $\eps$.

**The other parts.** (a): for a constant, every $N$ wins every round, since $\abs{c - c} = 0$.
For the identity and a height $B$, the threshold $N = B$ wins: $x > N$ says that $x > B$ (and as
$x \to -\infty$, $x < N$ says that $x < B$). (c): the tolerance $1$ gives a threshold beyond
which $\abs{f(x)} < \abs{L} + 1$, and the two tolerances of [the product
proof](#prf-calc-limit-laws) on the Limit Laws page give two more; beyond the largest of the
three thresholds, that proof's inequalities hold word for word. (That proof names its constant
$N = \abs{M} + 1$; this is not our threshold.) (d): the tolerance $\frac{\abs{M}}{2}$ gives a
threshold beyond which $\abs{g(x)} > \frac{\abs{M}}{2}$, so $g(x) \ne 0$ there, and the rest is
as in [the quotient proof](#prf-calc-limit-laws) there. (e) is
the product law used repeatedly, as in [the sketches for the power and square-root
laws](#rem-calc-limit-laws-power-root-sketch). (f): the tolerance $L$ gives a threshold beyond
which $f(x) > 0$ when $L > 0$; when $L = 0$, the hypothesis gives $f(x) \ge 0$ beyond $K$; the
inequalities of those sketches then apply at each such $x$. As $x \to -\infty$, the rays are
$x < N$, and the smaller of two thresholds replaces the larger.

*What this sketch leaves out:* writing each of (c)–(f) out with thresholds, including the
bookkeeping of the domain, that each new function is defined at every $x$ beyond the final
threshold, so on an interval $(N, \infty)$; the induction in (e) and the details of (f) that the
Limit Laws page itself only sketches; and the versions for $x \to -\infty$.
:::

(If $f$ and $g$ are defined on two different intervals $(\alpha_1, \infty)$ and
$(\alpha_2, \infty)$, both are defined on the one whose left end is the larger of $\alpha_1$ and
$\alpha_2$, so one $\alpha$ is no restriction.)

**When the laws do not apply.** As on the Limit Laws page, the laws need the limits $L$ and $M$ of
the parts to be **real numbers**. If both parts tend to $\infty$, the laws say nothing about the
difference, "$\infty - \infty$", or the quotient, "$\frac{\infty}{\infty}$", and such limits can
be anything. For every real number $c$, the functions $x + c$ and $x$ both tend to $\infty$, yet
their difference is the constant $c$, whose limit is $c$. The quotients $\frac{2x}{x}$ and
$\frac{x^2}{x}$ are both "$\frac{\infty}{\infty}$"; they equal $2$ and $x$ at every $x > 0$, so by
[property 2 of the remark](#rem-calc-limit-at-infinity-facts) their limits are $2$ and $\infty$,
by part (a) of the theorem. Such forms are a signal to rewrite the function first, as the next
proof and the examples do.

### Rational functions

For a rational function, the leading terms decide everything: far out, $\frac{p(x)}{q(x)}$
behaves like the quotient of the leading terms. We first need that the reciprocal powers
$\frac{1}{x^j}$ tend to $0$.

:::{proof:proposition} Rational functions at infinity
:label: prop-calc-rational-at-infinity

(a) For every integer $j \ge 1$,
$$
\lim_{x \to \infty} \frac{1}{x^j} = 0 \quad\text{and}\quad \lim_{x \to -\infty} \frac{1}{x^j} = 0 .
$$

Now let $p$ be a polynomial of degree $m$ with leading coefficient $a$, let $q$ be a polynomial
of degree $k$ with leading coefficient $b$, and let $r(x) = \frac{p(x)}{q(x)}$. There is a real
number $c \ge 0$ such that $r$ is defined at every $x > c$ and at every $x < -c$, and:

(b) if $m < k$, then $\lim_{x \to \infty} r(x) = 0$ and $\lim_{x \to -\infty} r(x) = 0$;

(c) if $m = k$, then $\lim_{x \to \infty} r(x) = \frac{a}{b}$ and
$\lim_{x \to -\infty} r(x) = \frac{a}{b}$;

(d) if $m > k$, then $\lim_{x \to \infty} r(x)$ is $\infty$ if $\frac{a}{b} > 0$ and $-\infty$ if
$\frac{a}{b} < 0$; and $\lim_{x \to -\infty} r(x)$ is $\infty$ if $(-1)^{m - k} \frac{a}{b} > 0$
and $-\infty$ if $(-1)^{m - k} \frac{a}{b} < 0$.
:::

:::{proof:proof}
:enumerated: false
We divide the numerator and the denominator by the highest power of $x$ in the denominator, so
that every term except the leading ones becomes a constant times a reciprocal power, which tends
to $0$ by (a); the limit laws at infinity do the rest. The limits as $x \to -\infty$ follow by
reflection. Throughout, $a \ne 0$ and $b \ne 0$, since they are leading coefficients
([](#def-calc-polynomial)).

**Step 1: a power is at least its base.** Let $x \ge 1$. For each integer $i \ge 1$, $x^i$ is a
product of positive numbers, so it is positive ([part (d) of the sign
rules](#prop-calc-sign-rules)), and multiplying $1 \le x$ by the positive number $x^i$ gives
$x^i \le x^{i + 1}$ ([property 5(b) of the order rules](#rem-calc-order-rules)). We claim that,
for every integer $j \ge 1$,
$$
x \le x^j .
$$
For $j = 1$ this is $x \le x$; if $x \le x^j$, then $x^j \le x^{j + 1}$ (as above) gives
$x \le x^{j + 1}$ by transitivity (property 2), so by induction it holds for every $j \ge 1$.

**Step 2: part (a).** The function $\frac{1}{x^j}$ is defined at every $x \ne 0$, since
$x^j \ne 0$ there (part (a) of the sign rules). Let $\eps > 0$, and let $N$ be the larger of $1$
and $\frac{1}{\eps}$. If $x > N$, then $x > 1$ and $x > \frac{1}{\eps}$, and by Step 1,
$$
0 < \frac{1}{\eps} < x \le x^j .
$$
So $\frac{1}{\eps} < x^j$ by transitivity, and [property 6 of the order
rules](#rem-calc-order-rules) gives $0 < \frac{1}{x^j} < \eps$. So
$\abs{\frac{1}{x^j} - 0} = \frac{1}{x^j} < \eps$ ([the definition of the absolute
value](#def-calc-absolute-value)), and $N$ wins the round $\eps$. As $x \to -\infty$: by
[property 3 of the remark](#rem-calc-limit-at-infinity-facts) we need
$\lim_{t \to \infty} \frac{1}{(-t)^j} = 0$. Since $(-t)^j = (-1)^j t^j$, and
$\frac{1}{(-1)^j} = (-1)^j$ because $(-1)^j (-1)^j = 1$, this function is
$(-1)^j \cdot \frac{1}{t^j}$, and the "in particular" of [part (c) of the limit laws at
infinity](#thm-calc-limit-laws-at-infinity) gives the limit $(-1)^j \cdot 0 = 0$.

**Step 3: where $r$ is defined.** By [part (a) of the proposition on the
domain](#prop-calc-rational-domain), $r$ is defined at every real number except the roots of $q$,
of which there are at most $k$. Let $c$ be the largest of $0$ and the absolute values of these
roots ($c = 0$ if $q$ has none). If $x > c$ or $x < -c$, then $\abs{x} > c$, because $\abs{x}$ is
at least $x$ and at least $-x$ ([property 3 of the absolute
value](#rem-calc-absolute-value-properties)); so $x$ is not a root of $q$, and $x \ne 0$ since
$c \ge 0$. Hence $r$ is defined at $x$, and $x^k \ne 0$.

**Step 4: the denominator and the numerator, divided by a power.** Write
$q(x) = b x^k + b_{k-1} x^{k-1} + \dots + b_1 x + b_0$, and for $x \ne 0$ let
$$
\begin{aligned}
Q(x) &= \frac{q(x)}{x^k} \\
  &= b + b_{k-1} \cdot \frac{1}{x} + \dots + b_0 \cdot \frac{1}{x^k} .
\end{aligned}
$$
By (a) and the "in particular" of part (c) of the laws, each term $b_i \cdot \frac{1}{x^{k - i}}$
with $i < k$ tends to $b_i \cdot 0 = 0$ as $x \to \infty$; the constant $b$ tends to $b$, by part
(a) of the laws; and the sum law, part (b), applied once for each term added, gives
$\lim_{x \to \infty} Q(x) = b$. All these functions are defined on $(0, \infty)$. In the same way,
writing $p(x) = a x^m + a_{m-1} x^{m-1} + \dots + a_0$, the function $P(x) = \frac{p(x)}{x^k}$
tends to $a$ if $m = k$. If $m < k$, every term of $P(x)$ is $a_i \cdot \frac{1}{x^{k - i}}$ with
$k - i \ge k - m \ge 1$, so every term tends to $0$, and $\lim_{x \to \infty} P(x) = 0$.

**Step 5: parts (b) and (c) as $x \to \infty$.** Since $b \ne 0$, the quotient law, part (d) of
the laws, gives $\lim_{x \to \infty} \frac{P(x)}{Q(x)} = \frac{0}{b} = 0$ if $m < k$, and
$\frac{a}{b}$ if $m = k$. At every $x > c$, Step 3 gives $q(x) \ne 0$ and $x^k \ne 0$, so
$Q(x) \ne 0$ and, multiplying the numerator and the denominator by $x^k$,
$\frac{P(x)}{Q(x)} = \frac{p(x)}{q(x)} = r(x)$. By [property 2 of the
remark](#rem-calc-limit-at-infinity-facts), $r$ has the same limit as $\frac{P}{Q}$.

**Step 6: part (d) as $x \to \infty$.** Let $m > k$, and for $x > c$ let
$$
S(x) = \frac{p(x) / x^m}{q(x) / x^k} .
$$
Step 4 with $m$ in place of $k$ gives $\lim_{x \to \infty} \frac{p(x)}{x^m} = a$, so the quotient
law gives $\lim_{x \to \infty} S(x) = \frac{a}{b}$ (with property 2 of the remark, as $S$ is that
quotient at every $x > c$), and at every $x > c$,
$x^{m - k} S(x) = \frac{p(x)}{q(x)} = r(x)$.

Suppose first that $\frac{a}{b} > 0$, and let $h = \frac12 \cdot \frac{a}{b}$, which is positive.
With the tolerance $h$, there is a threshold $N_1$ such that $\abs{S(x) - \frac{a}{b}} < h$ at
every $x > N_1$, and then $S(x) > \frac{a}{b} - h = h$, by [part (a) of the proposition on
distance inequalities](#prop-calc-abs-interval). Let $B$ be a real number, let $N$ be the largest
of $N_1$, $c$, $1$ and $\frac{\abs{B}}{h}$, and let $x > N$. Then $r(x)$ is defined (Step 3),
$S(x) > h > 0$, and $x > 1$, so $x^{m - k} \ge x$ by Step 1, as $m - k \ge 1$. Multiplying
$x^{m - k} \ge x$ by the positive number $S(x)$, multiplying $S(x) > h$ by the positive number
$x$, and multiplying $x > \frac{\abs{B}}{h}$ by the positive number $h$
([property 5 of the order rules](#rem-calc-order-rules)) gives
$$
\begin{aligned}
r(x) = x^{m - k} S(x) &\ge x\,S(x) \\
  &> x h > \abs{B} \ge B ,
\end{aligned}
$$
where $\abs{B} \ge B$ is property 3 of the absolute value. So $r(x) > B$ by transitivity, and
$\lim_{x \to \infty} r(x) = \infty$.

If $\frac{a}{b} < 0$, apply this to $-p$, which has degree $m$ and leading coefficient $-a$, with
$\frac{-a}{b} > 0$: so $\lim_{x \to \infty} \bigl(-r(x)\bigr) = \infty$. Given a real number $B$,
a threshold that wins the round $-B$ for $-r$ wins the round $B$ for $r$ with "$<$": $-r(x) > -B$
gives $r(x) < B$, multiplying by the negative number ${-1}$, which reverses the inequality
([property 5(c) of the order rules](#rem-calc-order-rules)). So $\lim_{x \to \infty} r(x) = -\infty$.

**Step 7: the limits as $x \to -\infty$.** Let $\tilde p(t) = p(-t)$ and $\tilde q(t) = q(-t)$.
Since $(-t)^i = (-1)^i t^i$, the polynomial $\tilde p$ has the coefficient $(-1)^i a_i$ at $t^i$;
at $t^m$ this is $(-1)^m a$, which is not $0$ (part (a) of the sign rules), and there are no
higher powers. So $\tilde p$ has degree $m$ and leading coefficient $(-1)^m a$, and likewise
$\tilde q$ has degree $k$ and leading coefficient $(-1)^k b$. The rational function
$\tilde r = \frac{\tilde p}{\tilde q}$ has $\tilde r(t) = r(-t)$, and $r$ is defined at every
$x < -c$ (Step 3). By property 3 of the remark, $\lim_{x \to -\infty} r(x)$ is
$\lim_{t \to \infty} \tilde r(t)$, which Steps 5 and 6 give, with $(-1)^m a$ and $(-1)^k b$ in
place of $a$ and $b$. If $m < k$, it is $0$. If $m = k$, it is
$\frac{(-1)^m a}{(-1)^m b} = \frac{a}{b}$. If $m > k$, the sign that decides is that of
$$
\frac{(-1)^m a}{(-1)^k b} = (-1)^{m - k} \frac{a}{b},
$$
because $(-1)^m = (-1)^{m - k} (-1)^k$.
:::

**In words.** Compare the degrees. A higher degree in the denominator pulls the quotient to $0$;
equal degrees give the quotient $\frac{a}{b}$ of the leading coefficients; a higher degree in the
numerator sends the quotient to $\infty$ or $-\infty$, with the sign of
$\frac{a x^m}{b x^k} = \frac{a}{b} x^{m - k}$ far out on that side. So the graph of $r$ has the
horizontal asymptote $y = 0$ in case (b), $y = \frac{a}{b}$ in case (c), in both directions, and
none in case (d).

**Example.** $\frac{3x^2 - x + 2}{2x^2 + 5}$ has $m = k = 2$, so its limit in both directions is
$\frac{3}{2}$. **Non-example.** For $\frac{x^2 + 1}{x}$, $m = 2 > k = 1$ and $\frac{a}{b} = 1$:
the limit is $\infty$ as $x \to \infty$, and, since $(-1)^1 \cdot 1 < 0$, $-\infty$ as
$x \to -\infty$. There is no horizontal asymptote.

### Comparing growth

Limits at infinity let us say which of two functions grows faster. Informally, $f$ **grows faster
than** $g$ as $x \to \infty$ if $\frac{g(x)}{f(x)} \to 0$: eventually $g(x)$ is a tiny fraction of
$f(x)$.

- **Higher powers grow faster.** If $m > k \ge 0$, then $\frac{x^k}{x^m} = \frac{1}{x^{m - k}}$
  for $x \ne 0$, which tends to $0$ by [part (a) of the
  proposition](#prop-calc-rational-at-infinity). So $x^3$ grows faster than $1000 x^2$, although
  $1000 x^2$ is far larger for a long time: at $x = 10$ it is $100\,000$ against $1000$, at
  $x = 1000$ the two are equal, and at $x = 10\,000$, $x^3$ is ten times larger.
- **A polynomial grows like its leading term.** By [part (c) of the
  proposition](#prop-calc-rational-at-infinity), applied to $p(x)$ over its leading term
  $a x^m$, $\frac{p(x)}{a x^m} \to 1$: the other terms become negligible in comparison.
- **The square root grows, but more slowly than $x$.** $\sqrt{x}$ eventually exceeds every
  height ([](#exr-calc-limits-at-infinity-sqrt-unbounded)), yet
  $\frac{\sqrt{x}}{x + 1} \to 0$ ([](#exr-calc-limits-at-infinity-root-over-linear)).

:::{admonition} Looking ahead
:class: looking-ahead
Exponential functions, such as $2^x$, are introduced on the page Exponential Functions and the
Number e, and logarithms on the page Logarithms. Compared in the same way, every exponential
function with a base greater than $1$ grows faster than every power of $x$, and every logarithm
grows more slowly than every positive power of $x$. The page Indeterminate Forms and L'Hôpital's
Rule gives one way to prove such comparisons.
:::

## Worked examples

### From the definition

:::{proof:example} Prove $\lim_{x \to \infty} \frac{2x}{x + 1} = 2$ from the definition
:label: eg-calc-limits-at-infinity-eps-n

**Goal.** Given $\eps > 0$, find a threshold $N$ such that $x > N$ implies
$\abs{\frac{2x}{x + 1} - 2} < \eps$. The function $f(x) = \frac{2x}{x + 1}$ is defined at every
$x \ne -1$, so on $(-1, \infty)$, and part (a) of [](#def-calc-limit-at-infinity) applies.

1. **Scratch work.** For $x > -1$, $x + 1 > 0$, and
   $$
   \begin{aligned}
   f(x) - 2 &= \frac{2x - 2(x + 1)}{x + 1} \\
     &= \frac{-2}{x + 1} .
   \end{aligned}
   $$
   By [property 4 of the absolute value](#rem-calc-absolute-value-properties), and since
   $x + 1 > 0$, $\abs{f(x) - 2} = \frac{2}{x + 1}$.
2. **Choose $N$.** We need $\frac{2}{x + 1} < \eps$. Since $x + 1 > 0$, multiplying by
   $\frac{x + 1}{\eps} > 0$ shows this holds exactly when $x + 1 > \frac{2}{\eps}$, that is,
   $x > \frac{2}{\eps} - 1$. So take $N = \frac{2}{\eps} - 1$. It depends on $\eps$ only, and
   $N > -1$, so $f$ is defined at every $x > N$.
3. **Proof.** Let $\eps > 0$, $N = \frac{2}{\eps} - 1$ and $x > N$. Adding $1$ to both sides,
   $x + 1 > \frac{2}{\eps} > 0$. By [property 6 of the order rules](#rem-calc-order-rules),
   $\frac{1}{x + 1} < \frac{\eps}{2}$, and multiplying by the positive number $2$ keeps the
   inequality:
   $$
   \abs{f(x) - 2} = \frac{2}{x + 1} < 2 \cdot \frac{\eps}{2} = \eps .
   $$

$$
\boxed{N = \frac{2}{\eps} - 1}
$$

No smaller threshold wins: at $x = \frac{2}{\eps} - 1$ itself, $\abs{f(x) - 2} = \eps$, not less.

**Check.** For $\eps = 0.1$: $N = 19$, and $x = 20$ gives $f(20) = \frac{40}{21} \approx 1.904762$,
which is $\frac{2}{21} \approx 0.095 < 0.1$ from $2$. ✓
:::

### Rational functions

:::{proof:example} Three rational functions
:label: eg-calc-limits-at-infinity-rational

Find (i) $\displaystyle \lim_{x \to \infty} \frac{3x^2 - x + 2}{2x^2 + 5}$,
(ii) $\displaystyle \lim_{x \to -\infty} \frac{x + 4}{x^2 + 1}$ and
(iii) $\displaystyle \lim_{x \to -\infty} \frac{x^3 - 2x}{4x^2 + 1}$.

1. **(i)** The degrees are $m = k = 2$, and the leading coefficients $a = 3$ and $b = 2$. By part
   (c) of [](#prop-calc-rational-at-infinity), the limit is $\frac{3}{2}$. By hand, as in the
   proof: for $x \ne 0$, dividing the numerator and the denominator by $x^2$,
   $$
   \frac{3x^2 - x + 2}{2x^2 + 5} = \frac{3 - \frac{1}{x} + \frac{2}{x^2}}{2 + \frac{5}{x^2}},
   $$
   and by part (a) of the proposition and the laws of [](#thm-calc-limit-laws-at-infinity), the
   numerator tends to $3 - 0 + 2 \cdot 0 = 3$ and the denominator to $2 + 5 \cdot 0 = 2 \ne 0$.
2. **(ii)** Here $m = 1 < k = 2$. By part (b) of the proposition, the limit is $0$.
3. **(iii)** Here $m = 3 > k = 2$, $a = 1$ and $b = 4$, so $\frac{a}{b} = \frac{1}{4}$. As
   $x \to -\infty$, part (d) of the proposition looks at the sign of
   $(-1)^{3 - 2} \cdot \frac{1}{4} = -\frac{1}{4}$, which is negative. So the limit is $-\infty$.
   Far to the left the function behaves like $\frac{x^3}{4x^2} = \frac{x}{4}$, which is very
   negative there.

$$
\boxed{\text{(i) } \frac{3}{2} \qquad \text{(ii) } 0 \qquad \text{(iii) } -\infty}
$$

The graph of (i) has the horizontal asymptote $y = \frac{3}{2}$ in both directions, that of (ii)
the asymptote $y = 0$, and that of (iii) none.

**Check.** (i) At $x = 1000$ the function is $\frac{2\,999\,002}{2\,000\,005} \approx 1.499497$. ✓
(ii) At $x = -1000$ it is about ${-0.000996}$. ✓ (iii) At $x = -100$ it is about ${-24.99}$, and
at $x = -1000$ about ${-250.00}$. ✓
:::

### Square roots

:::{proof:example} A difference of two large numbers: $\lim_{x \to \infty} \bigl(\sqrt{x^2 + 1} - x\bigr)$
:label: eg-calc-limits-at-infinity-conjugate

1. **The laws do not apply directly.** $\sqrt{x^2 + 1}$ is defined for every $x$, since
   $x^2 + 1 > 0$. Both $\sqrt{x^2 + 1}$ and $x$ grow without bound, and the difference law needs
   real limits: this is "$\infty - \infty$".
2. **Multiply by the conjugate.** For every real $x$, $\abs{x}^2 = x^2 < x^2 + 1$
   ([property 5 of the absolute value](#rem-calc-absolute-value-properties)), and both $\abs{x}$
   and $\sqrt{x^2 + 1}$ are non-negative, so the order part of [the square-root
   remark](#rem-calc-square-roots) gives $\abs{x} < \sqrt{x^2 + 1}$. With $-x \le \abs{x}$
   (property 3 of the absolute value), $\sqrt{x^2 + 1} + x > 0$. So we may divide by it, at
   every $x$. Using $\bigl(\sqrt{y}\bigr)^2 = y$ for $y \ge 0$,
   $$
   \begin{aligned}
   &\bigl(\sqrt{x^2 + 1} - x\bigr)\bigl(\sqrt{x^2 + 1} + x\bigr) \\
   &\quad = (x^2 + 1) - x^2 = 1 ,
   \end{aligned}
   $$
   and dividing by $\sqrt{x^2 + 1} + x$,
   $$
   \sqrt{x^2 + 1} - x = \frac{1}{\sqrt{x^2 + 1} + x} .
   $$
   This is an identity at every $x$, not only near some point.
3. **Take out $x$ under the root.** For $x > 0$, the number $x\sqrt{1 + \frac{1}{x^2}}$ is
   non-negative, and its square is $x^2 \bigl(1 + \frac{1}{x^2}\bigr) = x^2 + 1$. By the
   uniqueness in [the square-root remark](#rem-calc-square-roots), it is $\sqrt{x^2 + 1}$.
   Dividing the numerator and the denominator by $x > 0$,
   $$
   \frac{1}{\sqrt{x^2 + 1} + x} = \frac{\frac{1}{x}}{\sqrt{1 + \frac{1}{x^2}} + 1} .
   $$
4. **The laws.** By part (a) of [](#prop-calc-rational-at-infinity), $\frac{1}{x^2} \to 0$, so
   $1 + \frac{1}{x^2} \to 1$ (parts (a) and (b) of [](#thm-calc-limit-laws-at-infinity)). Since
   $1 > 0$, part (f) gives $\sqrt{1 + \frac{1}{x^2}} \to \sqrt{1} = 1$, so the denominator tends
   to $2 \ne 0$. The numerator tends to $0$, by part (a) of the proposition, and the quotient law,
   part (d), gives the limit $\frac{0}{2} = 0$.
5. **Back to the function.** The last quotient equals $\sqrt{x^2 + 1} - x$ at every $x > 0$, so
   by [property 2 of the remark](#rem-calc-limit-at-infinity-facts) the two have the same limit.

$$
\boxed{\lim_{x \to \infty} \bigl(\sqrt{x^2 + 1} - x\bigr) = 0}
$$

**Check.** At $x = 1000$: $\sqrt{1\,000\,001} - 1000 \approx 0.0005$, and
$\frac{1}{\sqrt{1\,000\,001} + 1000} \approx \frac{1}{2000}$. ✓
:::

:::{proof:example} Two different horizontal asymptotes
:label: eg-calc-limits-at-infinity-two-asymptotes

Find the horizontal asymptotes of the graph of $f(x) = \dfrac{x}{\sqrt{x^2 + 1}}$.

1. **Domain.** $x^2 + 1 \ge 1 > 0$ for every $x$, so $\sqrt{x^2 + 1}$ is defined and positive,
   and $f$ is defined on $\R$.
2. **Take out $\abs{x}$ under the root.** For $x \ne 0$, the number
   $\abs{x}\sqrt{1 + \frac{1}{x^2}}$ is non-negative, and its square is
   $\abs{x}^2 \bigl(1 + \frac{1}{x^2}\bigr) = x^2 + 1$, by [property 5 of the absolute
   value](#rem-calc-absolute-value-properties). By the uniqueness in [the square-root
   remark](#rem-calc-square-roots),
   $$
   \sqrt{x^2 + 1} = \abs{x}\sqrt{1 + \frac{1}{x^2}} .
   $$
   It is $\abs{x}$, not $x$, that comes out.
3. **As $x \to \infty$.** For $x > 0$, $\abs{x} = x$, so $f(x) = \dfrac{1}{\sqrt{1 + 1/x^2}}$. By
   part (a) of [](#prop-calc-rational-at-infinity), $\frac{1}{x^2} \to 0$, so by parts (a), (b)
   and (f) of [](#thm-calc-limit-laws-at-infinity), $\sqrt{1 + \frac{1}{x^2}} \to \sqrt{1} = 1$,
   which is not $0$, and the quotient law gives the limit $\frac{1}{1} = 1$. By [property 2 of the
   remark](#rem-calc-limit-at-infinity-facts), $\lim_{x \to \infty} f(x) = 1$.
4. **As $x \to -\infty$.** For $x < 0$, $\abs{x} = -x$ ([the definition of the absolute
   value](#def-calc-absolute-value)), so
   $$
   \begin{aligned}
   f(x) &= \frac{x}{-x\sqrt{1 + 1/x^2}} \\
     &= -\frac{1}{\sqrt{1 + 1/x^2}} .
   \end{aligned}
   $$
   By part (a) of [](#prop-calc-rational-at-infinity), $\frac{1}{x^2} \to 0$ as $x \to -\infty$
   too. The laws as $x \to -\infty$ then work as in step 3: by parts (a), (b) and (f) of
   [](#thm-calc-limit-laws-at-infinity), $\sqrt{1 + \frac{1}{x^2}} \to 1$, which is not $0$; the
   quotient law gives $\frac{1}{\sqrt{1 + 1/x^2}} \to 1$; and the "in particular" of part (c),
   with the factor ${-1}$, gives the limit $-1$. The formula holds at every $x < 0$, so by
   [property 2 of the remark](#rem-calc-limit-at-infinity-facts), in its form for
   $x \to -\infty$, $\lim_{x \to -\infty} f(x) = -1$.

$$
\boxed{
\begin{aligned}
\lim_{x \to \infty} f(x) &= 1 \\
\lim_{x \to -\infty} f(x) &= -1
\end{aligned}
}
$$

So the graph has two horizontal asymptotes, $y = 1$ on the right and $y = -1$ on the left. This
cannot happen for a rational function: by [](#prop-calc-rational-at-infinity), its two limits,
when real, are equal.

**Check.** $f(1000) \approx 0.9999995$ and $f(-1000) \approx {-0.9999995}$. The sign is right:
$f(x)$ has the sign of $x$, since the denominator is positive. ✓
:::

### An application

:::{proof:example} A very large resistor in parallel
:label: eg-calc-limits-at-infinity-resistors

Find $\lim_{t \to \infty} R(t)$ for the combined resistance $R(t) = \frac{3t}{3 + t}$ ohms,
$t > 0$, of Why this matters, and how large the second resistor must be for $R(t)$ to be within
$0.01$ ohm of the limit.

1. **The function.** $R$ is defined on $(0, \infty)$, and it agrees there with the rational
   function $r(t) = \frac{3t}{t + 3}$, defined at every $t \ne -3$.
2. **The limit.** For $r$, the degrees are $m = k = 1$ and the leading coefficients $a = 3$ and
   $b = 1$, so by part (c) of [](#prop-calc-rational-at-infinity), $\lim_{t \to \infty} r(t) = 3$.
   By [property 2 of the remark](#rem-calc-limit-at-infinity-facts), with $c = 0$,
   $\lim_{t \to \infty} R(t) = 3$.
3. **How large?** For $t > 0$, $\abs{R(t) - 3} = 3 - R(t) = \frac{9}{3 + t}$, as in Why this
   matters. This is less than $0.01$ exactly when $3 + t > 900$ (multiply by the positive number
   $\frac{3 + t}{0.01}$, or divide by it, which keeps the inequality), that is, when $t > 897$.

$$
\boxed{\lim_{t \to \infty} R(t) = 3}
$$

The combined resistance approaches $3$ ohms, and it is within $0.01$ ohm of $3$ ohms exactly when
the second resistor has more than $897$ ohms: for $\eps = 0.01$, the threshold $N = 897$ wins.
The line $y = 3$ is a horizontal asymptote of the graph of $R$.

**Check.** $R(897) = \frac{2691}{900} = 2.99$, exactly $0.01$ below $3$, and
$R(898) = \frac{2694}{901} \approx 2.990011$. ✓ Units: ohms times ohms over ohms is ohms. ✓ A
parallel combination is smaller than each resistor, and $R(t) < 3$. ✓
:::

## Common mistakes

:::{warning} "$\sqrt{x^2} = x$", also as $x \to -\infty$
✗ **Wrong:** "$\dfrac{x}{\sqrt{x^2 + 1}} = \dfrac{x}{x\sqrt{1 + 1/x^2}} = \dfrac{1}{\sqrt{1 + 1/x^2}}$,
so the limit as $x \to -\infty$ is $1$."

**Why:** $\sqrt{x^2} = \abs{x}$ ([property 5 of the absolute
value](#rem-calc-absolute-value-properties)), and for $x < 0$ that is $-x$, not $x$. A square
root is never negative, so taking $x$ out of $\sqrt{x^2 + 1}$ for negative $x$ produces the
wrong sign. At $x = -10$ the function is about ${-0.995}$, nowhere near $1$.

✓ **Right:** $\sqrt{x^2 + 1} = \abs{x}\sqrt{1 + 1/x^2} = -x\sqrt{1 + 1/x^2}$ for $x < 0$, and the
limit as $x \to -\infty$ is ${-1}$ ([](#eg-calc-limits-at-infinity-two-asymptotes)). Treat
$x \to \infty$ and $x \to -\infty$ separately whenever a square root of $x^2$ appears.
:::

:::{warning} "$\infty - \infty = 0$"
✗ **Wrong:** "$\sqrt{x^2 + x}$ and $x$ both tend to $\infty$, so
$\lim_{x \to \infty} \bigl(\sqrt{x^2 + x} - x\bigr) = \infty - \infty = 0$."

**Why:** $\infty$ is not a number, and the difference law needs both limits to be real numbers.
"$\infty - \infty$" can hide any value: $(x + c) - x$ has the limit $c$, for every $c$.

✓ **Right:** multiply by the conjugate. For $x > 0$, $\sqrt{x^2 + x} = x\sqrt{1 + \frac{1}{x}}$,
and
$$
\begin{aligned}
\sqrt{x^2 + x} - x &= \frac{x}{\sqrt{x^2 + x} + x} \\
  &= \frac{1}{\sqrt{1 + \frac{1}{x}} + 1},
\end{aligned}
$$
which tends to $\frac{1}{2}$ by the laws, as in [](#eg-calc-limits-at-infinity-conjugate). At
$x = 10\,000$ the difference is about $0.49999$.
:::

:::{warning} "$\frac{\infty}{\infty} = 1$"
✗ **Wrong:** "In $\dfrac{2x + 1}{x + 5}$ the numerator and the denominator both tend to $\infty$,
so the quotient tends to $1$."

**Why:** the quotient law needs real limits, and "$\frac{\infty}{\infty}$", like "$\frac{0}{0}$",
says only that the law does not apply. How fast the two parts grow decides.

✓ **Right:** the degrees are equal, so by part (c) of [](#prop-calc-rational-at-infinity) the
limit is the quotient of the leading coefficients, $\frac{2}{1} = 2$. At $x = 1000$ the function
is about $1.991$.
:::

:::{warning} "A graph never crosses its asymptote"
✗ **Wrong:** "$y = 2$ is the horizontal asymptote of $\dfrac{2x^2 + x}{x^2 + 1}$, so the graph
never reaches the height $2$."

**Why:** the definition is about $x$ beyond a threshold only; before it, anything may happen. At
$x = 2$ the function is $\frac{8 + 2}{4 + 1} = 2$: the graph crosses its asymptote there, and then
approaches it from above ([](#fig-calc-limits-at-infinity-band)).

✓ **Right:** a horizontal asymptote says that the values approach $L$ far out. Whether the graph
meets the line is a separate question, answered by solving $f(x) = L$.
:::

## Rigorous track

:::{admonition} A limit at infinity is a one-sided limit at $0$
:class: dropdown rigor
The substitution $x = \frac{1}{t}$ turns $x \to \infty$ into $t \to 0^{+}$. Let $f$ be defined at
every point of $(c, \infty)$, let $g(t) = f\bigl(\frac{1}{t}\bigr)$ for $t > 0$, and let $L$ be a
real number. Then
$$
\lim_{x \to \infty} f(x) = L \iff \lim_{t \to 0^{+}} g(t) = L,
$$
with the right-hand limit of [the definition of one-sided limits](#def-calc-one-sided-limit). The
key fact: for positive numbers, $t < \delta$ exactly when $\frac{1}{t} > \frac{1}{\delta}$, by
[property 6 of the order rules](#rem-calc-order-rules) (applied in both directions).

*From left to right.* Let $c' = \max(c, 1) > 0$. For $0 < t < \frac{1}{c'}$, $\frac{1}{t} > c'$,
so $g$ is defined on $\bigl(0, \frac{1}{c'}\bigr)$. If $N$ wins the round $\eps$ for $f$, so does
$N' = \max(N, 1)$, which is positive; then $\delta = \frac{1}{N'}$ wins it for $g$: if
$0 < t < \delta$, then $\frac{1}{t} > N'$, so $g(t) = f\bigl(\frac{1}{t}\bigr)$ is defined and
within $\eps$ of $L$.

*From right to left.* If $g$ is defined on $(0, \rho)$, then $f(x) = g\bigl(\frac{1}{x}\bigr)$ for
$x > \frac{1}{\rho}$, since $0 < \frac{1}{x} < \rho$ there. If $\delta$ wins the round $\eps$ for
$g$, then $N = \frac{1}{\delta}$ wins it for $f$: if $x > N$, then $0 < \frac{1}{x} < \delta$, so
$f(x) = g\bigl(\frac{1}{x}\bigr)$ is defined and within $\eps$ of $L$.

**Example.** For $f(x) = \frac{2x^2 + x}{x^2 + 1}$ of [](#fig-calc-limits-at-infinity-band),
multiplying the numerator and the denominator by $t^2 > 0$ gives
$g(t) = \frac{2 + t}{1 + t^2}$ for $t > 0$. This rational function has the limit $\frac{2}{1} = 2$
at $0$, by [direct substitution](#cor-calc-direct-substitution), so its right-hand limit is $2$
too, by [the theorem on one-sided limits](#thm-calc-limit-iff-one-sided); the right-hand limit
uses only $t > 0$, where it agrees with $g$. So
$\lim_{x \to \infty} f(x) = 2$, as part (c) of [](#prop-calc-rational-at-infinity) says.

The same substitution turns $\lim_{x \to -\infty}$ into $\lim_{t \to 0^{-}}$. It shows why the
two kinds of limit behave alike, and it is how some books define limits at infinity.
:::

## Summary

- $\lim_{x \to \infty} f(x) = L$ means: for every $\eps > 0$ there is a threshold $N$ with
  $\abs{f(x) - L} < \eps$ for every $x > N$ ([](#def-calc-limit-at-infinity)). For $x \to -\infty$
  the ray is $x < N$; for the value $\infty$, a height $B$ replaces the tolerance.
- "$= \infty$" describes how a limit fails to exist as a real number; it is not a limit that
  exists.
- The limit laws hold at infinity, with $\max(N_1, N_2)$ in place of $\min(\delta_1, \delta_2)$
  ([](#thm-calc-limit-laws-at-infinity)); they need the limits of the parts to be real, so
  "$\infty - \infty$" and "$\frac{\infty}{\infty}$" call for rewriting first.
- For a rational function, compare degrees: lower over higher gives $0$, equal gives the quotient
  of the leading coefficients, higher over lower gives $\pm\infty$
  ([](#prop-calc-rational-at-infinity)).
- With square roots, multiply by the conjugate for "$\infty - \infty$", and remember
  $\sqrt{x^2} = \abs{x} = -x$ for $x < 0$.
- $y = L$ is a horizontal asymptote if $f(x) \to L$ as $x \to \infty$ or as $x \to -\infty$
  ([](#def-calc-horizontal-asymptote)); a graph has at most two, and may cross them.

## Exercises

::::{exercise} Equal degrees
:label: exr-calc-limits-at-infinity-equal-degree
:class: tier-a

Find $\displaystyle \lim_{x \to \infty} \frac{4x^3 - x + 1}{2x^3 + 7x^2}$.

:::{admonition} Hint 1
:class: dropdown hint
Compare the degrees of the numerator and the denominator.
:::

:::{admonition} Answer
:class: dropdown answer
$2$
:::
::::

::::{solution} exr-calc-limits-at-infinity-equal-degree
:label: sol-calc-limits-at-infinity-equal-degree
:class: dropdown

The numerator and the denominator both have degree $3$, with the leading coefficients $4$ and
$2$. By part (c) of [](#prop-calc-rational-at-infinity), the limit is $\frac{4}{2} = 2$.
::::

::::{exercise} A higher degree below
:label: exr-calc-limits-at-infinity-lower-degree
:class: tier-a

Find $\displaystyle \lim_{x \to -\infty} \frac{5x + 2}{x^2 - 3}$.

:::{admonition} Hint 1
:class: dropdown hint
Which has the higher degree, the numerator or the denominator?
:::

:::{admonition} Answer
:class: dropdown answer
$0$
:::
::::

::::{solution} exr-calc-limits-at-infinity-lower-degree
:label: sol-calc-limits-at-infinity-lower-degree
:class: dropdown

The numerator has degree $1$ and the denominator degree $2$. By part (b) of
[](#prop-calc-rational-at-infinity), the limit is $0$ as $x \to -\infty$ (and as $x \to \infty$).
::::

::::{exercise} A higher degree above
:label: exr-calc-limits-at-infinity-higher-degree
:class: tier-a

Find $\displaystyle \lim_{x \to -\infty} \frac{x^4 - x}{3 - 2x^3}$. Write $\infty$ or $-\infty$ if
the values grow without bound.

:::{admonition} Hint 1
:class: dropdown hint
Find the leading coefficient of the denominator: it is the coefficient of $x^3$. Then look at the
sign of $(-1)^{m - k} \frac{a}{b}$.
:::

:::{admonition} Answer
:class: dropdown answer
$\infty$
:::
::::

::::{solution} exr-calc-limits-at-infinity-higher-degree
:label: sol-calc-limits-at-infinity-higher-degree
:class: dropdown

The numerator $x^4 - x$ has degree $m = 4$ and leading coefficient $a = 1$. The denominator
$-2x^3 + 3$ has degree $k = 3$ and leading coefficient $b = -2$. So $m > k$ and
$\frac{a}{b} = -\frac{1}{2}$. As $x \to -\infty$, part (d) of [](#prop-calc-rational-at-infinity)
looks at the sign of
$$
(-1)^{4 - 3} \cdot \Bigl(-\frac{1}{2}\Bigr) = \frac{1}{2},
$$
which is positive. So the limit is $\infty$. (Far to the left the function behaves like
$\frac{x^4}{-2x^3} = -\frac{x}{2}$, which is large and positive there; at $x = -10$ it is about
$5.0$.)
::::

::::{exercise} The horizontal asymptote
:label: exr-calc-limits-at-infinity-asymptote
:class: tier-a

The graph of $f(x) = \dfrac{1 - 4x^2}{x^2 + x + 1}$ has exactly one horizontal asymptote, the line
$y = L$. Find $L$.

:::{admonition} Hint 1
:class: dropdown hint
Find both limits at infinity. Be careful with the leading coefficient of the numerator.
:::

:::{admonition} Answer
:class: dropdown answer
${-4}$
:::
::::

::::{solution} exr-calc-limits-at-infinity-asymptote
:label: sol-calc-limits-at-infinity-asymptote
:class: dropdown

The numerator $-4x^2 + 1$ has degree $2$ and leading coefficient ${-4}$; the denominator has
degree $2$ and leading coefficient $1$. (The denominator is never $0$:
$x^2 + x + 1 = \bigl(x + \frac12\bigr)^2 + \frac34$, where the square is $\ge 0$ by [part (c) of
the sign rules](#prop-calc-sign-rules), so it is at least $\frac34$, and $f$ is defined on $\R$.) By part (c) of [](#prop-calc-rational-at-infinity), both limits at infinity
are $\frac{-4}{1} = -4$, so $y = -4$ is the horizontal asymptote, in both directions, and there
is no other ([property 1 of the remark](#rem-calc-limit-at-infinity-facts)).
::::

::::{exercise} The threshold in the figure
:label: exr-calc-limits-at-infinity-figure-threshold
:class: tier-b

Let $f(x) = \dfrac{2x^2 + x}{x^2 + 1}$, the function of [](#fig-calc-limits-at-infinity-band),
whose limit as $x \to \infty$ is $2$. Show that $\abs{f(x) - 2} < 0.1$ at every $x > 7$, and find
the smallest number $N$ such that $\abs{f(x) - 2} < 0.1$ at every $x > N$.

:::{admonition} Hint 1
:class: dropdown hint
Simplify $f(x) - 2$ to a single fraction. What is its sign for $x > 2$?
:::

:::{admonition} Hint 2
:class: dropdown hint
For $x > 2$, the inequality $f(x) - 2 < 0.1$ becomes a quadratic inequality. Factor it.
:::

:::{admonition} Answer
:class: dropdown answer
$7$
:::
::::

::::{solution} exr-calc-limits-at-infinity-figure-threshold
:label: sol-calc-limits-at-infinity-figure-threshold
:class: dropdown

For every real $x$, $x^2 + 1 > 0$, and
$$
\begin{aligned}
f(x) - 2 &= \frac{2x^2 + x - 2(x^2 + 1)}{x^2 + 1} \\
  &= \frac{x - 2}{x^2 + 1} .
\end{aligned}
$$

**Every $x > 7$ works.** Let $x > 7$. Then $x - 2 > 0$, so $f(x) - 2$ is a quotient of two
positive numbers, positive by [part (c) of the sign rules](#prop-calc-sign-rules), and
$\abs{f(x) - 2} = f(x) - 2$. Multiplying by the positive number $10(x^2 + 1)$, the inequality
$f(x) - 2 < 0.1$ holds exactly when $10(x - 2) < x^2 + 1$, that is, when
$$
x^2 - 10x + 21 = (x - 3)(x - 7) > 0 .
$$
For $x > 7$ both factors are positive, so the product is positive. So $\abs{f(x) - 2} < 0.1$.

**No smaller $N$ works.** If $N < 7$, then $x = 7$ satisfies $x > N$, but
$f(7) - 2 = \frac{5}{50} = 0.1$, which is not less than $0.1$.

So the smallest such $N$ is $7$. (Between $3$ and $7$ the product $(x - 3)(x - 7)$ is negative:
there the graph is above the band, as the figure shows.)
::::

::::{exercise} The conjugate again
:label: exr-calc-limits-at-infinity-conjugate
:class: tier-b

Find $\displaystyle \lim_{x \to \infty} \bigl(\sqrt{x^2 + 6x} - x\bigr)$.

:::{admonition} Hint 1
:class: dropdown hint
This is "$\infty - \infty$". Multiply and divide by $\sqrt{x^2 + 6x} + x$, as in
[](#eg-calc-limits-at-infinity-conjugate).
:::

:::{admonition} Hint 2
:class: dropdown hint
For $x > 0$, $\sqrt{x^2 + 6x} = x\sqrt{1 + \frac{6}{x}}$.
:::

:::{admonition} Answer
:class: dropdown answer
$3$
:::
::::

::::{solution} exr-calc-limits-at-infinity-conjugate
:label: sol-calc-limits-at-infinity-conjugate
:class: dropdown

For $x > 0$, $x^2 + 6x = x(x + 6) > 0$, so the root is defined, and $\sqrt{x^2 + 6x} + x > 0$, as a
sum of a non-negative and a positive number. So, for $x > 0$,
$$
\begin{aligned}
\sqrt{x^2 + 6x} - x &= \frac{(x^2 + 6x) - x^2}{\sqrt{x^2 + 6x} + x} \\
  &= \frac{6x}{\sqrt{x^2 + 6x} + x} .
\end{aligned}
$$
For $x > 0$, $x\sqrt{1 + \frac{6}{x}}$ is non-negative and its square is $x^2 + 6x$, so it equals
$\sqrt{x^2 + 6x}$ by the uniqueness in [the square-root remark](#rem-calc-square-roots).
Dividing the numerator and the denominator by $x > 0$,
$$
\frac{6x}{\sqrt{x^2 + 6x} + x} = \frac{6}{\sqrt{1 + \frac{6}{x}} + 1} .
$$
By part (a) of [](#prop-calc-rational-at-infinity) and the laws of
[](#thm-calc-limit-laws-at-infinity), $1 + \frac{6}{x} \to 1 > 0$, so by part (f)
$\sqrt{1 + \frac{6}{x}} \to 1$, and by parts (b) and (d) the quotient tends to
$\frac{6}{1 + 1} = 3$. The quotient equals the original function at every $x > 0$, so by
[property 2 of the remark](#rem-calc-limit-at-infinity-facts) the limit is $3$.
::::

::::{exercise} A square root as $x \to -\infty$
:label: exr-calc-limits-at-infinity-sqrt-minus-infinity
:class: tier-b

Find $\displaystyle \lim_{x \to -\infty} \frac{2x - 1}{\sqrt{x^2 + 3}}$.

:::{admonition} Hint 1
:class: dropdown hint
For $x < 0$, what is $\sqrt{x^2}$? Take $\abs{x}$ out of the root, as in
[](#eg-calc-limits-at-infinity-two-asymptotes).
:::

:::{admonition} Answer
:class: dropdown answer
${-2}$
:::
::::

::::{solution} exr-calc-limits-at-infinity-sqrt-minus-infinity
:label: sol-calc-limits-at-infinity-sqrt-minus-infinity
:class: dropdown

The function is defined on $\R$, since $x^2 + 3 > 0$. For $x < 0$, the number
$-x\sqrt{1 + \frac{3}{x^2}}$ is non-negative, and its square is $x^2 + 3$, so it is
$\sqrt{x^2 + 3}$ ([the square-root remark](#rem-calc-square-roots)). Dividing the numerator and
the denominator by $-x > 0$,
$$
\begin{aligned}
\frac{2x - 1}{\sqrt{x^2 + 3}} &= \frac{2x - 1}{-x\sqrt{1 + \frac{3}{x^2}}} \\
  &= -\frac{2 - \frac{1}{x}}{\sqrt{1 + \frac{3}{x^2}}} .
\end{aligned}
$$
As $x \to -\infty$, $\frac{1}{x} \to 0$ and $\frac{1}{x^2} \to 0$ by part (a) of
[](#prop-calc-rational-at-infinity). By [](#thm-calc-limit-laws-at-infinity), as
$x \to -\infty$, the numerator $2 - \frac{1}{x}$ tends to $2$, and $1 + \frac{3}{x^2} \to 1 > 0$,
so the root tends to $1$ by part (f). By the quotient law and the "in particular" of part (c),
with $c = -1$, the limit is $-\frac{2}{1} = -2$; by [property 2 of the
remark](#rem-calc-limit-at-infinity-facts), so is that of the original function.

(As $x \to \infty$ the limit is $2$: the graph has two horizontal asymptotes, $y = 2$ and
$y = -2$.)
::::

::::{exercise} A square root over a line
:label: exr-calc-limits-at-infinity-root-over-linear
:class: tier-b

Find $\displaystyle \lim_{x \to \infty} \frac{\sqrt{x}}{x + 1}$.

:::{admonition} Hint 1
:class: dropdown hint
Divide the numerator and the denominator by $x$. For $x > 0$, what is $\frac{\sqrt{x}}{x}$?
:::

:::{admonition} Hint 2
:class: dropdown hint
$\frac{1}{\sqrt{x}} = \sqrt{\frac{1}{x}}$ for $x > 0$. The square-root law with $L = 0$ has an
extra hypothesis.
:::

:::{admonition} Answer
:class: dropdown answer
$0$
:::
::::

::::{solution} exr-calc-limits-at-infinity-root-over-linear
:label: sol-calc-limits-at-infinity-root-over-linear
:class: dropdown

For $x > 0$, $\sqrt{x} > 0$ (it is $\ge 0$, and not $0$, since $0^2 = 0 \ne x$), and
$\sqrt{\frac{1}{x}} = \frac{1}{\sqrt{x}}$: the right-hand side is non-negative, and its square is
$\frac{1}{x}$ ([the square-root remark](#rem-calc-square-roots)). Since $\sqrt{x} \cdot \sqrt{x} = x$,
$\frac{\sqrt{x}}{x} = \frac{1}{\sqrt{x}}$, and dividing the numerator and the denominator by $x$,
$$
\frac{\sqrt{x}}{x + 1} = \frac{\sqrt{1/x}}{1 + \frac{1}{x}} \quad\text{for } x > 0 .
$$
By part (a) of [](#prop-calc-rational-at-infinity), $\frac{1}{x} \to 0$, and $\frac{1}{x} \ge 0$
for every $x > 0$, so part (f) of [](#thm-calc-limit-laws-at-infinity), with $L = 0$ and $K = 0$,
gives $\sqrt{1/x} \to 0$. The denominator tends to $1 \ne 0$, so the quotient law gives
$\frac{0}{1} = 0$; by [property 2 of the remark](#rem-calc-limit-at-infinity-facts), so does the
original function. So $\sqrt{x}$ grows more slowly than $x + 1$.
::::

::::{exercise} The average cost of a chair
:label: exr-calc-limits-at-infinity-average-cost
:class: tier-b applied

A workshop pays £$2000$ for a set of moulds and then £$45$ in materials and labour for each chair.
Making $x$ chairs costs $2000 + 45x$ pounds, so the average cost per chair is
$$
A(x) = \frac{2000 + 45x}{x}
$$
pounds, for $x > 0$. Find $\lim_{x \to \infty} A(x)$, in pounds, and show that making more than
$400$ chairs brings the average cost below £$50$.

:::{admonition} Hint 1
:class: dropdown hint
$A$ agrees, for $x > 0$, with a rational function of equal degrees.
:::

:::{admonition} Answer
:class: dropdown answer
$45$
:::
::::

::::{solution} exr-calc-limits-at-infinity-average-cost
:label: sol-calc-limits-at-infinity-average-cost
:class: dropdown

For $x > 0$, $A(x)$ is the value of the rational function $\frac{45x + 2000}{x}$, whose numerator
and denominator have degree $1$ and leading coefficients $45$ and $1$. By part (c) of
[](#prop-calc-rational-at-infinity) and [property 2 of the
remark](#rem-calc-limit-at-infinity-facts), $\lim_{x \to \infty} A(x) = 45$.

The fixed cost is shared by more and more chairs, so the average cost approaches the cost of the
materials and labour for one chair, £$45$. Indeed $A(x) - 45 = \frac{2000}{x}$, which is less than
$5$ exactly when $x > 400$ (multiplying by the positive number $\frac{x}{5}$): more than $400$
chairs bring the average below £$50$.
::::

::::{exercise} Two functions that tend to $\infty$
:label: exr-calc-limits-at-infinity-difference
:class: tier-b

Let $f$ and $g$ be defined on an interval $(c, \infty)$. True or false: if
$\lim_{x \to \infty} f(x) = \infty$ and $\lim_{x \to \infty} g(x) = \infty$, then
$\lim_{x \to \infty} \bigl(f(x) - g(x)\bigr) = 0$.

:::{admonition} Hint 1
:class: dropdown hint
Try $f(x) = x + 1$ and $g(x) = x$.
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-limits-at-infinity-difference
:label: sol-calc-limits-at-infinity-difference
:class: dropdown

False. Take $f(x) = x + 1$ and $g(x) = x$, defined on $\R$. By part (a) of
[](#thm-calc-limit-laws-at-infinity), $\lim_{x \to \infty} g(x) = \infty$. For $f$, given a real
number $B$, the threshold $N = B - 1$ wins: if $x > B - 1$, then $x + 1 > B$, adding $1$
([property 3 of the order rules](#rem-calc-order-rules)). So $\lim_{x \to \infty} f(x) = \infty$.
But $f(x) - g(x) = 1$ at every $x$, and the constant $1$ has the limit $1$ (part (a)), not $0$: by
[property 1 of the remark](#rem-calc-limit-at-infinity-facts), a limit is unique.

"$\infty - \infty$" is not $0$; it is not a number at all.
::::

::::{exercise} The line that the graph approaches
:label: exr-calc-limits-at-infinity-oblique
:class: tier-c

There are real numbers $m$ and $c$ such that
$$
\lim_{x \to \infty} \Bigl(\frac{x^2 + 1}{x + 1} - (mx + c)\Bigr) = 0 .
$$
Find (a) $m$ and (b) $c$, and show that no other pair of numbers works.

:::{admonition} Hint 1
:class: dropdown hint
Divide $x^2 + 1$ by $x + 1$ with a remainder ([the division of
polynomials](#thm-calc-polynomial-division)).
:::

:::{admonition} Hint 2
:class: dropdown hint
For uniqueness: if two pairs work, subtract. What is the limit of $(m - m')x + (c - c')$ as
$x \to \infty$ when $m \ne m'$?
:::

:::{admonition} Answer
:class: dropdown answer
(a) $1$ (b) ${-1}$
:::
::::

::::{solution} exr-calc-limits-at-infinity-oblique
:label: sol-calc-limits-at-infinity-oblique
:class: dropdown

**Existence.** $(x + 1)(x - 1) + 2 = x^2 - 1 + 2 = x^2 + 1$ for every $x$, so dividing by
$x + 1$ gives the quotient $x - 1$ and the remainder $2$ ([](#thm-calc-polynomial-division)).
For $x \ne -1$,
$$
\frac{x^2 + 1}{x + 1} = x - 1 + \frac{2}{x + 1} .
$$
With $m = 1$ and $c = -1$, the difference is $\frac{2}{x + 1}$ at every $x > -1$. This rational
function has a numerator of degree $0$ and a denominator of degree $1$, so its limit is $0$ by
part (b) of [](#prop-calc-rational-at-infinity), and by [property 2 of the
remark](#rem-calc-limit-at-infinity-facts) so is that of the difference.

**Uniqueness.** Suppose $m'$ and $c'$ work too. By the difference law, part (b) of
[](#thm-calc-limit-laws-at-infinity), applied to the two differences,
$$
\begin{aligned}
&\lim_{x \to \infty} \bigl((m' - m)x + (c' - c)\bigr) \\
&\quad = 0 - 0 = 0 .
\end{aligned}
$$
If $m' \ne m$, then $(m' - m)x + (c' - c)$ is a polynomial of degree $1$, and by part (d) of the
proposition (with the denominator $1$, of degree $0$) its limit is $\infty$ or $-\infty$, which
contradicts the limit $0$ by [property 1 of the remark](#rem-calc-limit-at-infinity-facts). So
$m' = m$, and then the function is the constant $c' - c$, whose limit is $c' - c$ (part (a) of the
laws); uniqueness gives $c' - c = 0$. So $m = 1$ and $c = -1$ is the only pair.

The line $y = x - 1$ is not horizontal, but the graph approaches it far to the right.
:::{admonition} Looking ahead
:class: looking-ahead
Such a line is called an oblique asymptote; the page Curve Sketching uses them.
:::
::::

::::{exercise} The reciprocal of a function that tends to $\infty$
:label: exr-calc-limits-at-infinity-reciprocal
:class: tier-c rigor

Let $f$ be defined at every point of an interval $(c, \infty)$, with
$\lim_{x \to \infty} f(x) = \infty$. Prove from [](#def-calc-limit-at-infinity) that
$\lim_{x \to \infty} \frac{1}{f(x)} = 0$.

:::{admonition} Hint 1
:class: dropdown hint
To get $\frac{1}{f(x)}$ below $\eps$, which height $B$ should $f(x)$ exceed?
:::

:::{admonition} Hint 2
:class: dropdown hint
Do not forget the domain: where is $\frac{1}{f}$ defined?
:::

:::{admonition} Answer
:class: dropdown answer manual
A threshold that wins the round $B = \frac{1}{\eps}$ for $f$ wins the round $\eps$ for
$\frac{1}{f}$.
:::
::::

::::{solution} exr-calc-limits-at-infinity-reciprocal
:label: sol-calc-limits-at-infinity-reciprocal
:class: dropdown

**The domain.** With the height $B = 1$, there is a threshold $N_0$ such that $f$ is defined and
$f(x) > 1 > 0$ at every $x > N_0$. So $f(x) \ne 0$ there, and $\frac{1}{f}$ is defined at every
point of $(N_0, \infty)$, as part (a) of the definition requires.

**The rounds.** Let $\eps > 0$. Then $\frac{1}{\eps}$ is a real number, so there is a threshold
$N$ such that $f$ is defined and $f(x) > \frac{1}{\eps}$ at every $x > N$. Let $x > N$. Since
$\frac{1}{\eps} > 0$ ([property 6 of the order rules](#rem-calc-order-rules)), we have
$0 < \frac{1}{\eps} < f(x)$, and property 6 gives
$$
0 < \frac{1}{f(x)} < \frac{1}{1/\eps} = \eps .
$$
So $\frac{1}{f(x)}$ is defined, and $\abs{\frac{1}{f(x)} - 0} = \frac{1}{f(x)} < \eps$, by
[the definition of the absolute value](#def-calc-absolute-value). So $N$ wins the round $\eps$,
and since $\eps > 0$ was arbitrary, $\lim_{x \to \infty} \frac{1}{f(x)} = 0$.
::::

::::{exercise} The square root grows without bound
:label: exr-calc-limits-at-infinity-sqrt-unbounded
:class: tier-c rigor

Prove from [](#def-calc-limit-at-infinity) that $\lim_{x \to \infty} \sqrt{x} = \infty$.

:::{admonition} Hint 1
:class: dropdown hint
For a height $B > 0$, which $x$ have $\sqrt{x} > B$? Use the order part of [the square-root
remark](#rem-calc-square-roots). Treat $B \le 0$ separately.
:::

:::{admonition} Answer
:class: dropdown answer manual
For $B > 0$ the threshold $N = B^2$ works; for $B \le 0$, $N = 0$.
:::
::::

::::{solution} exr-calc-limits-at-infinity-sqrt-unbounded
:label: sol-calc-limits-at-infinity-sqrt-unbounded
:class: dropdown

The function $\sqrt{x}$ is defined at every $x \ge 0$ ([the square-root
remark](#rem-calc-square-roots)), so on $(0, \infty)$. Let $B$ be a real number.

**If $B \le 0$.** Take $N = 0$. If $x > 0$, then $\sqrt{x}$ is defined, $\sqrt{x} \ge 0$, and
$\sqrt{x} \ne 0$, because $0^2 = 0 \ne x$. So $\sqrt{x} > 0 \ge B$, and $\sqrt{x} > B$ by
transitivity ([property 2 of the order rules](#rem-calc-order-rules)).

**If $B > 0$.** Take $N = B^2$, which is $\ge 0$. If $x > B^2$, then $x > 0$, so $\sqrt{x}$ is
defined. The numbers $B$ and $\sqrt{x}$ are non-negative, and $B^2 < x = \bigl(\sqrt{x}\bigr)^2$,
so the order part of the square-root remark, with $s = B$ and $t = \sqrt{x}$, gives
$B < \sqrt{x}$.

In both cases $N$ wins the round $B$. Since $B$ was arbitrary, $\lim_{x \to \infty} \sqrt{x} =
\infty$.
::::

## Where this leads

:::{where-this-leads}
:::

Limits at infinity return wherever "in the long run" matters: in curve sketching, where horizontal
and oblique asymptotes describe the far ends of a graph; in L'Hôpital's rule, whose general form
covers "$\frac{\infty}{\infty}$" and $x \to \pm\infty$; in improper integrals over unbounded
intervals; and in sequences, where $n \to \infty$ runs through the integers only.
