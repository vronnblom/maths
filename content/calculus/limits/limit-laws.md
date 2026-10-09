---
title: Limit Laws
label: calc-limit-laws
description: >-
  Rules that give the limit of a sum, product, quotient, power or square root from the limits
  of its parts, proved once from the definition; why substituting the point gives the limit of
  a polynomial or a rational function; and what goes wrong when a hypothesis of a law fails.
tags: [limits, epsilon-delta, proofs]
maths:
  kind: topic
  subject: calc
  status: reviewed
  level: core
  difficulty: 3
  est_minutes: 50
  prerequisites: [calc-limit]
  objectives:
    - Evaluate limits with the sum, product, quotient, power and root laws.
    - Justify direct substitution for polynomials and rational functions.
    - Identify when the laws do not apply.
  verify: verify/calculus/limits/test_limit_laws.py
  widgets: [function-plot]
  reviewed_by: [vronnblom]
  manual_checked:
    exr-calc-limit-laws-constant-multiple: vronnblom
    exr-calc-limit-laws-absolute-value: vronnblom
  sources: []
---

:::{topic-header}
:::

## Why this matters

On the page [The Limit of a Function](#calc-limit) we proved that $\lim_{x \to 2} x^2 = 4$ from
[the definition](#def-calc-limit), and even that took some care: we had to cap the window and
bound a factor. Now consider
$$
\lim_{x \to 2} \frac{x^3 - 1}{x^2 + 3} .
$$
A table suggests an answer, but a direct proof with $\eps$ and $\delta$ would have to control the
numerator and the denominator at the same time, with a new choice of $\delta$ for this one
function. Doing that for every function we meet would be hopeless.

::::{figure}
:label: wdg-calc-limit-laws-rational

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "(x^3 - 1)/(x^2 + 3)",
  "xRange": [0, 4],
  "yRange": [-1, 4],
  "table": { "points": [1.9, 1.99, 1.999, 2.001, 2.01, 2.1] },
  "trace": { "x": 1 }
}
```

Graph of $y = \frac{x^3 - 1}{x^2 + 3}$ for $0 \le x \le 4$, rising from about ${-0.33}$ at
$x = 0$ to about $3.3$ at $x = 4$, with a point on the graph that a slider for $x$ moves. A
table lists the values, rounded to six decimal places, at $x = 1.9, 1.99, 1.999$: $0.886384$,
$0.988578$, $0.998857$, and at $x = 2.001, 2.01, 2.1$: $1.001143$, $1.011435$, $1.114845$. They
approach $1$ from both sides.
::::

**Try this:** move the point towards $x = 2$ from both sides and read $f(x)$. Then compute the
numerator and the denominator at $x = 2$ separately. What do you notice?

The table suggests that the limit is $1 = \frac{7}{7}$, the numerator's value at $2$ divided by
the denominator's. That is no accident. Instead of proving each limit from scratch, we prove a
few rules once, from the definition, that say how limits combine: the limit of a sum is the sum
of the limits, the limit of a quotient is the quotient of the limits, and so on. With these
**limit laws** the limit above takes a few lines ([](#eg-calc-limit-laws-rational)), and
for every polynomial the limit is its value at the point ([](#cor-calc-direct-substitution)).

Each law has hypotheses, and they matter. The stone's average speed on
[The Limit of a Function](#calc-limit), $\frac{5(1+h)^2 - 5}{h}$, is a quotient whose
denominator approaches $0$: the quotient law says nothing about it. The last part of the main
results is about such cases.

## Combining functions

Let $f$ and $g$ be functions. Their **sum** $f + g$, **difference** $f - g$ and **product**
$fg$ are the functions with

- $(f + g)(x) = f(x) + g(x)$,
- $(f - g)(x) = f(x) - g(x)$,
- $(fg)(x) = f(x)\,g(x)$,

defined at every $x$ at which both $f(x)$ and $g(x)$ are defined. Their **quotient** $f/g$,
with $(f/g)(x) = \frac{f(x)}{g(x)}$, is defined at every such $x$ at which, in addition,
$g(x) \ne 0$. For a real number $c$, the function $cf$ has $(cf)(x) = c\,f(x)$, and
$\sqrt{f}$ has the value $\sqrt{f(x)}$ at every $x$ at which $f(x)$ is defined and
$f(x) \ge 0$, by [the square-root remark](#rem-calc-square-roots).

**Why the laws should hold.** If $f(x)$ is close to $L$ and $g(x)$ is close to $M$, then
$f(x) + g(x)$ should be close to $L + M$. How close? The two errors can add up: if each of
$f(x)$ and $g(x)$ is within $0.01$ of its limit, then $f(x) + g(x)$ is within $0.02$ of
$L + M$, by the triangle inequality. So to get $f(x) + g(x)$ within a tolerance $\eps$ of
$L + M$, we demand $\frac{\eps}{2}$ from each of $f$ and $g$. The definition of the limit lets
us demand any tolerance, $\frac{\eps}{2}$ included. That is the whole idea of the proof of the
sum law below, and the other proofs refine it.

**Example.** From the definition, $\lim_{x \to 3} (2x - 1) = 5$ (the window
$\delta = \frac{\eps}{2}$ works, because $\abs{(2x - 1) - 5} = 2\abs{x - 3}$) and
$\lim_{x \to 3} 4x = 12$ ($\delta = \frac{\eps}{4}$ works, because
$\abs{4x - 12} = 4\abs{x - 3}$). The sum law gives $\lim_{x \to 3} (6x - 1) = 5 + 12 = 17$
without a new proof; [](#eg-calc-limit-laws-sum-delta) looks at the $\delta$ it produces.

**Non-example.** The laws need the limits of the parts to exist. For $f(x) = x$ and
$g(x) = \frac{1}{x}$, $x \ne 0$, the product $f(x)\,g(x) = 1$ has the limit $1$ at $0$, but the
product law cannot be used to find it, because $\frac{1}{x}$ has no limit at $0$ (we show this
in [When the laws do not apply](#sec-calc-limit-laws-not-apply)).

## Main results

The laws are stated for two functions $f$ and $g$ with limits $L$ and $M$ at the same point
$a$. Each of them comes with the conclusion that the new function is defined near $a$, so that
[the definition of a limit](#def-calc-limit) applies to it.

:::{proof:theorem} Limit laws
:label: thm-calc-limit-laws

Let $a$ be a real number.

- **(a) Constants and the identity.** For every real number $c$, $\lim_{x \to a} c = c$; and
  $\lim_{x \to a} x = a$.

Now let $f$ and $g$ be functions, each defined at every point of an open interval containing
$a$, except possibly at $a$ itself, such that $\lim_{x \to a} f(x) = L$ and
$\lim_{x \to a} g(x) = M$, where $L$ and $M$ are real numbers. Then:

- **(b) Sum and difference.** $\lim_{x \to a} \bigl(f(x) + g(x)\bigr) = L + M$ and
  $\lim_{x \to a} \bigl(f(x) - g(x)\bigr) = L - M$.
- **(c) Product.** $\lim_{x \to a} f(x)\,g(x) = LM$. In particular,
  $\lim_{x \to a} c\,f(x) = cL$ for every real number $c$.
- **(d) Quotient.** If $M \ne 0$, then $\lim_{x \to a} \dfrac{f(x)}{g(x)} = \dfrac{L}{M}$.
- **(e) Power.** For every integer $n \ge 1$, $\lim_{x \to a} \bigl(f(x)\bigr)^n = L^n$.
- **(f) Square root.** If $L > 0$, then $\lim_{x \to a} \sqrt{f(x)} = \sqrt{L}$. If $L = 0$, and
  there is an $r > 0$ such that $f(x) \ge 0$ for every $x$ with $0 < \abs{x - a} < r$, then
  $\lim_{x \to a} \sqrt{f(x)} = 0$.

In each of (b)–(f), the function whose limit is taken is defined at every point of some open
interval containing $a$, except possibly at $a$, so that
[the definition of a limit](#def-calc-limit) applies to it.
:::

:::{proof:proof}
:enumerated: false
We prove (a) and (b) here; (c) and (d) are proved in the rigorous track below, and (e) and (f)
are sketched in the remark after this proof. For the sum the idea is to share the tolerance:
we ask $f(x)$ to be within $\frac{\eps}{2}$ of $L$ and $g(x)$ within $\frac{\eps}{2}$ of $M$,
and the triangle inequality adds the two errors.

**(a)** The constant function $c$ is defined for every $x$. Let $\eps > 0$ and take
$\delta = 1$. For every $x$ with $0 < \abs{x - a} < 1$, $\abs{c - c} = 0 < \eps$. So
$\lim_{x \to a} c = c$. The function $x$ is also defined for every $x$. Let $\eps > 0$ and take
$\delta = \eps$. If $0 < \abs{x - a} < \delta$, then $\abs{x - a} < \eps$. So
$\lim_{x \to a} x = a$.

**(b), the sum.** Let $\eps > 0$. Then $\frac{\eps}{2} > 0$, so we may use it as the tolerance
in [the definition of a limit](#def-calc-limit). Since $\lim_{x \to a} f(x) = L$, there is a
$\delta_1 > 0$ such that $f$ is defined and $\abs{f(x) - L} < \frac{\eps}{2}$ at every $x$
with $0 < \abs{x - a} < \delta_1$. Since $\lim_{x \to a} g(x) = M$, there is a $\delta_2 > 0$
such that $g$ is defined and $\abs{g(x) - M} < \frac{\eps}{2}$ at every $x$ with
$0 < \abs{x - a} < \delta_2$.

Let $\delta = \min(\delta_1, \delta_2)$, which is positive, and let $0 < \abs{x - a} < \delta$.
Since $\delta \le \delta_1$ and $\delta \le \delta_2$, also $\abs{x - a} < \delta_1$ and
$\abs{x - a} < \delta_2$, so $x$ lies in both windows. Hence $f(x)$ and $g(x)$ are defined, and
so is $f(x) + g(x)$. By [part (a) of the triangle inequality](#thm-calc-triangle-inequality),
applied to the numbers $f(x) - L$ and $g(x) - M$,
$$
\begin{aligned}
\abs{\bigl(f(x) + g(x)\bigr) - (L + M)}
  &= \abs{\bigl(f(x) - L\bigr) + \bigl(g(x) - M\bigr)} \\
  &\le \abs{f(x) - L} + \abs{g(x) - M} \\
  &< \frac{\eps}{2} + \frac{\eps}{2} = \eps .
\end{aligned}
$$
The last step adds two strict inequalities, which gives a strict inequality.

So $f + g$ is defined at every $x$ with $0 < \abs{x - a} < \delta$, which by
[part (e) of the proposition on distance inequalities](#prop-calc-abs-interval) is the open
interval $(a - \delta, a + \delta)$ with $a$ removed; the definition applies to $f + g$, and the
display shows that $\delta$ wins the round $\eps$. Since $\eps > 0$ was arbitrary,
$\lim_{x \to a} \bigl(f(x) + g(x)\bigr) = L + M$.

**(b), the difference.** The same $\delta$ works. The only change is in the first line of the
display: $\bigl(f(x) - g(x)\bigr) - (L - M) = \bigl(f(x) - L\bigr) + \bigl(-(g(x) - M)\bigr)$,
and $\abs{-(g(x) - M)} = \abs{g(x) - M}$ by
[property 2 of the absolute value](#rem-calc-absolute-value-properties), so the same two bounds
apply.
:::

The power law is the product law used again and again, and the square-root law needs one
identity and a look at the domain. Both are sketched here; what a sketch leaves out is said in
it.

:::{proof:remark} Sketches for the power and square-root laws
:label: rem-calc-limit-laws-power-root-sketch

**(e) Power.** For $n = 1$ the law is the hypothesis $\lim_{x \to a} f(x) = L$. For $n = 2$,
$\bigl(f(x)\bigr)^2 = f(x)\,f(x)$, so [part (c)](#thm-calc-limit-laws) with $g = f$ gives the
limit $L \cdot L = L^2$. For $n = 3$, $\bigl(f(x)\bigr)^3 = \bigl(f(x)\bigr)^2 f(x)$, so part (c)
again gives $L^2 \cdot L = L^3$, and so on: each step multiplies by one more factor $f(x)$.
*What this leaves out:* "and so on" stands for a proof by induction on $n$, which shows that
if the law holds for $n$, it holds for $n + 1$.

**(f) Square root, $L > 0$.** At every $x$ with $f(x) \ge 0$, the number $\sqrt{f(x)}$ is
defined, and
$$
\bigl(\sqrt{f(x)} - \sqrt{L}\bigr)\bigl(\sqrt{f(x)} + \sqrt{L}\bigr) = f(x) - L,
$$
because $\bigl(\sqrt{y}\bigr)^2 = y$ for every $y \ge 0$
([the square-root remark](#rem-calc-square-roots)). The second factor is at least $\sqrt{L}$
(add $\sqrt{L}$ to both sides of $\sqrt{f(x)} \ge 0$), and $\sqrt{L}$ is positive:
$\sqrt{L} \ge 0$, and $\sqrt{L} \ne 0$ because $0^2 = 0 \ne L$. Dividing by the positive second
factor, and using [property 4 of the absolute value](#rem-calc-absolute-value-properties) and,
since the second factor is positive, [the definition](#def-calc-absolute-value) to drop the bars
around it,
$$
\abs{\sqrt{f(x)} - \sqrt{L}} = \frac{\abs{f(x) - L}}{\sqrt{f(x)} + \sqrt{L}}
\le \frac{\abs{f(x) - L}}{\sqrt{L}} .
$$
The inequality uses two of the order rules of
[Absolute Value and Inequalities](#calc-absolute-value-inequalities) ("Working with
inequalities"). Multiplying $\sqrt{L} \le \sqrt{f(x)} + \sqrt{L}$ by the positive number
$\frac{1}{\sqrt{L}\,(\sqrt{f(x)} + \sqrt{L})}$ keeps it, and gives
$\frac{1}{\sqrt{f(x)} + \sqrt{L}} \le \frac{1}{\sqrt{L}}$. Multiplying this by
$\abs{f(x) - L}$, which is $\ge 0$ and may be $0$, gives only $\le$. So a window in which
$\abs{f(x) - L} < \eps\sqrt{L}$ also has $\abs{\sqrt{f(x)} - \sqrt{L}} < \eps$: multiplying
$\abs{f(x) - L} < \eps\sqrt{L}$ by the positive number $\frac{1}{\sqrt{L}}$ keeps the strict
inequality, and $\le$ followed by $<$ gives $<$ (transitivity). *What this leaves out:* that
$\sqrt{f(x)}$ is defined in the window at all, that is, $f(x) \ge 0$ there. The tolerance $L$ in the definition of
$\lim_{x \to a} f(x) = L$ gives a window in which $\abs{f(x) - L} < L$, so $f(x) > 0$ by
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval); a full proof
takes the smaller of the two windows.

**(f) Square root, $L = 0$.** Here the hypothesis $f(x) \ge 0$ provides the domain, and by the
order part of [the square-root remark](#rem-calc-square-roots), $0 \le f(x) < \eps^2$ gives
$\sqrt{f(x)} < \eps$. So a window in which $\abs{f(x) - 0} < \eps^2$ and $f(x) \ge 0$ works.
*What this leaves out:* the bookkeeping of the windows, as above.
:::

:::{admonition} Looking ahead
:class: looking-ahead
Higher roots obey a root law too. For an odd $n$, such as the cube root, the $n$-th root of
$f(x)$ approaches the $n$-th root of $L$ for every real $L$, with no sign condition, because odd
roots of negative numbers exist (the cube root of ${-8}$ is ${-2}$). For an even $n$ the sign
condition of part (f) is needed, as for square roots. Roots other than the square root are
introduced with rational exponents on the page Exponential Functions and the Number e, and the
root law for them follows on the page Continuity of Elementary Functions.
:::

### Direct substitution

A **polynomial** is a function of the form $p(x) = c_n x^n + \dots + c_1 x + c_0$, where
$n \ge 0$ is an integer and $c_0, c_1, \dots, c_n$ are real numbers; it is defined for every
real $x$. A **rational function** is a quotient $\frac{p(x)}{q(x)}$ of two polynomials, defined
at every $x$ with $q(x) \ne 0$. For these functions the laws reduce every limit to a
substitution.

:::{proof:corollary} Direct substitution
:label: cor-calc-direct-substitution

Let $a$ be a real number.

- **(a) Polynomials.** If $p$ is a polynomial, then $\lim_{x \to a} p(x) = p(a)$.
- **(b) Rational functions.** If $r = \frac{p}{q}$ is a rational function, with polynomials
  $p$ and $q$ such that $q(a) \ne 0$, then $\lim_{x \to a} r(x) = r(a) = \frac{p(a)}{q(a)}$.
- **(c) Restrictions.** Let $r$ be as in (b), and let $I$ be an open interval containing $a$.
  If $s$ is the restriction of $r$ to $I$, that is, the function defined at the points of $I$ at
  which $r$ is defined, with $s(x) = r(x)$ there, then
  $\lim_{x \to a} s(x) = s(a) = \frac{p(a)}{q(a)}$.
:::

:::{proof:proof}
:enumerated: false
We build $p$ from constants and the function $x$ with the laws of [](#thm-calc-limit-laws),
one operation at a time.

(a) Write $p(x) = c_n x^n + \dots + c_1 x + c_0$. Every term is defined for every real $x$,
so each satisfies the hypothesis on the domain in [](#thm-calc-limit-laws). By part (a),
$\lim_{x \to a} x = a$. For each $k$ with $1 \le k \le n$, part (e) applied to the function $x$
gives $\lim_{x \to a} x^k = a^k$, and then the "in particular" of part (c) gives
$\lim_{x \to a} c_k x^k = c_k a^k$. By part (a), $\lim_{x \to a} c_0 = c_0$. The polynomial is
the sum of these $n + 1$ terms; applying the sum law, part (b), $n$ times, adding one term at a
time, gives
$$
\lim_{x \to a} p(x) = c_n a^n + \dots + c_1 a + c_0 = p(a) .
$$

(b) By (a), $\lim_{x \to a} p(x) = p(a)$ and $\lim_{x \to a} q(x) = q(a)$, and both
polynomials are defined for every real $x$. Since $q(a) \ne 0$, part (d) of
[](#thm-calc-limit-laws) applies, with $f = p$, $g = q$, $L = p(a)$ and $M = q(a)$, and gives
$\lim_{x \to a} \frac{p(x)}{q(x)} = \frac{p(a)}{q(a)}$. Since $r = \frac{p}{q}$, this is
$\lim_{x \to a} r(x)$; and since $q(a) \ne 0$, $r$ is defined at $a$, with
$r(a) = \frac{p(a)}{q(a)}$.

(c) Since $a$ is in $I$ and $r$ is defined at $a$, so is $s$, and $s(a) = r(a)$. We find a
window around $a$ that lies inside $I$. By [the definition of an interval](#def-calc-interval),
$I$ is $(\alpha, \beta)$, $(\alpha, \infty)$, $(-\infty, \beta)$ or $\R$. Since $a$ is in $I$,
$\alpha < a$ when $I$ has the left endpoint $\alpha$, and $a < \beta$ when it has the right
endpoint $\beta$. Let $\rho$ be the smaller of $a - \alpha$ and
$\beta - a$, or $a - \alpha$, or $\beta - a$, or $1$, in these four cases. Then $\rho > 0$,
$\rho \le a - \alpha$ when $I$ has the left endpoint $\alpha$, and $\rho \le \beta - a$ when it
has the right endpoint $\beta$.

Let $\eps > 0$. By (b), there is a $\delta_0 > 0$ such that $r$ is defined and
$\abs{r(x) - r(a)} < \eps$ at every $x$ with $0 < \abs{x - a} < \delta_0$. Let
$\delta = \min(\delta_0, \rho)$, which is positive, and let $0 < \abs{x - a} < \delta$. By
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval),
$a - \delta < x < a + \delta$. If $I$ has the left endpoint $\alpha$, then adding
$\alpha - \rho$ to both sides of $\rho \le a - \alpha$ gives $\alpha \le a - \rho$, and
$a - \rho \le a - \delta$ since $\delta \le \rho$, so $\alpha < x$. In the same way, if $I$ has
the right endpoint $\beta$, then $x < \beta$. So $x$ is in $I$. Since also
$\abs{x - a} < \delta_0$, $r$ is defined at $x$, so $s$ is defined there, and
$$
\abs{s(x) - s(a)} = \abs{r(x) - r(a)} < \eps .
$$
So $s$ is defined at every $x$ with $0 < \abs{x - a} < \delta$, which by part (e) of the
proposition on distance inequalities is the open interval $(a - \delta, a + \delta)$ with $a$
removed; [the definition of a limit](#def-calc-limit) applies to $s$, and $\delta$ wins the
round $\eps$. Since $\eps > 0$ was arbitrary, $\lim_{x \to a} s(x) = s(a)$.
:::

**In words.** For a polynomial, the limit at any point is the value there. For a rational
function, the same holds at every point where the denominator is not $0$, and part (c) says
that it still holds when the function is used only on an open interval around the point, as in
an application where only some inputs make sense ([](#eg-calc-limit-laws-resistors)). This is a
property of these particular functions, proved from the laws. It is not true of every function
given by a formula: the function $h$ of
[the remark on the value at $a$](#rem-calc-limit-value-irrelevant), with $h(x) = x + 1$ for
$x \ne 1$ and $h(1) = 5$, has the limit $2$ at $1$, not $h(1) = 5$.

Together with (e) and (f), the corollary handles many functions built from polynomials and
square roots: apply it to the parts, check each law's hypotheses, and combine
([](#eg-calc-limit-laws-root-quotient)).

(sec-calc-limit-laws-not-apply)=
### When the laws do not apply

Every law has hypotheses: the limits of the parts must exist, as real numbers; the quotient law
needs $M \ne 0$; the square-root law needs $L > 0$, or $L = 0$ and $f(x) \ge 0$ near $a$. When a
hypothesis fails, the law says nothing at all: neither that the limit exists, nor that it does
not. Each of the following shows a hypothesis failing.

- **A part has no limit.** The function $\frac{1}{x}$, $x \ne 0$, has no limit at $0$.
  Suppose it had a limit $M$. By part (a) of [](#thm-calc-limit-laws), $\lim_{x \to 0} x = 0$,
  so the product law would give $\lim_{x \to 0} x \cdot \frac{1}{x} = 0 \cdot M = 0$. But
  $x \cdot \frac{1}{x} = 1$ at every $x \ne 0$, and the constant $1$ is within every $\eps > 0$
  of $1$, so this limit is $1$. Two different limits contradict
  [uniqueness of limits](#thm-calc-limit-unique). So $\frac{1}{x}$ has no limit at $0$. In
  particular the product law does not apply to $x \cdot \frac{1}{x}$, although its limit
  exists.
- **The quotient law with $M = 0$ and $L \ne 0$.** For $\frac{1}{x}$ at $0$, the numerator has
  the limit $1$ and the denominator the limit $0$; the quotient has no limit, as we just saw.
  The same holds for $\frac{x + 1}{x}$, which is $1 + \frac{1}{x}$ for $x \ne 0$: if it had a
  limit, the difference law would give one for $\frac{1}{x} = \frac{x + 1}{x} - 1$.
- **The quotient law with $M = 0$ and $L = 0$.** Substituting gives "$\frac{0}{0}$", which is
  not a number. Such a limit may be any number, or not exist. In the next figure, the numerator
  $x^2 + cx$ and the denominator $x$ both have the limit $0$ at $0$
  ([](#cor-calc-direct-substitution)), for every value of $c$.
- **Negative powers when $L = 0$.** Part (e) is stated for $n \ge 1$. For $n = -1$,
  $\bigl(f(x)\bigr)^{-1} = \frac{1}{f(x)}$ is a quotient with numerator $1$, and when $L \ne 0$
  the quotient law gives it the limit $\frac{1}{L}$. What fails when $L = 0$ is the quotient
  law's hypothesis $M \ne 0$, here with $M = L$, not anything about $n$: for $f(x) = x$ at $0$
  there is no limit.
- **The square-root law without its sign condition.** If $L < 0$: $f(x) = x - 1$ has the limit
  ${-1}$ at $0$, and $\sqrt{x - 1}$ is undefined at every $x < 1$, so it is not defined on any
  open interval around $0$, and [the definition of a limit](#def-calc-limit) does not apply.
  If $L = 0$ but $f$ takes negative values arbitrarily close to $a$: $f(x) = x$ at $0$, where
  $\sqrt{x}$ is undefined at every $x < 0$, and again the definition does not apply. With the
  sign condition, $f(x) = x^2 \ge 0$, the law gives $\lim_{x \to 0} \sqrt{x^2} = 0$.

::::{figure}
:label: wdg-calc-limit-laws-zero-over-zero

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "(x^2 + c*x)/x",
  "xRange": [-1, 1],
  "yRange": [-3.5, 3.5],
  "parameters": { "c": { "value": 1, "min": -2, "max": 2, "step": 0.5 } },
  "table": { "points": [0.1, 0.01, 0.001, -0.001, -0.01, -0.1] },
  "hole": { "x": 0 }
}
```

Graph of $y = \frac{x^2 + cx}{x}$ for $-1 \le x \le 1$, $x \ne 0$, with a hole at $x = 0$, where
the formula is undefined. A slider sets $c$ from ${-2}$ to $2$ in steps of $0.5$, starting at
$c = 1$. For every $c$ the graph is a straight line with a hole. A table lists the values at
$x = 0.1, 0.01, 0.001, -0.001, -0.01, -0.1$; for $c = 1$ they are $1.1$, $1.01$, $1.001$,
$0.999$, $0.99$, $0.9$, which approach $1$, and for $c = 1.5$ they are $1.6$, $1.51$, $1.501$,
$1.499$, $1.49$, $1.4$, which approach $1.5$.
::::

**Try this:** set $c = -2$, $c = 0$ and $c = 1.5$. In each case, what do the numerator and the
denominator approach as $x \to 0$? Which number do the values in the table approach? What does
"$\frac{0}{0}$" tell you about the limit?

The figure shows the same "$\frac{0}{0}$" next to different values in the table, one for each
$c$. So a $\frac{0}{0}$ is not an answer: it says only that the quotient law does not apply,
and that more work is needed.

:::{admonition} Looking ahead
:class: looking-ahead
Limits that give $\frac{0}{0}$ are the subject of the next page, Computing Limits
Algebraically. There we rewrite the function, for $x \ne a$, as one to which the laws apply
(by factoring, rationalising or simplifying), and a lemma shows that this does not change the
limit. The stone's speed on [The Limit of a Function](#calc-limit) was found in exactly this
way.
:::

## Worked examples

### Using the laws

:::{proof:example} The $\delta$ that the proof of the sum law builds
:label: eg-calc-limit-laws-sum-delta

Let $f(x) = 2x - 1$ and $g(x) = 4x$, with $\lim_{x \to 3} f(x) = 5$ and
$\lim_{x \to 3} g(x) = 12$. Follow the proof of the sum law, part (b) of
[](#thm-calc-limit-laws), to find a $\delta$ for $\lim_{x \to 3} \bigl(f(x) + g(x)\bigr) = 17$,
and compare it with the largest $\delta$ that works.

1. **Tolerance $\frac{\eps}{2}$ for $f$.** $\abs{f(x) - 5} = \abs{2x - 6} = 2\abs{x - 3}$, so
   $\abs{f(x) - 5} < \frac{\eps}{2}$ exactly when $\abs{x - 3} < \frac{\eps}{4}$ (dividing by
   the positive number $2$ keeps the inequality). Take $\delta_1 = \frac{\eps}{4}$.
2. **Tolerance $\frac{\eps}{2}$ for $g$.** $\abs{g(x) - 12} = \abs{4x - 12} = 4\abs{x - 3}$, so
   $\abs{g(x) - 12} < \frac{\eps}{2}$ exactly when $\abs{x - 3} < \frac{\eps}{8}$ (dividing by
   the positive number $4$). Take $\delta_2 = \frac{\eps}{8}$.
3. **The proof's $\delta$.** $\delta = \min\bigl(\frac{\eps}{4}, \frac{\eps}{8}\bigr) =
   \frac{\eps}{8}$, since $\frac{\eps}{8} < \frac{\eps}{4}$ for $\eps > 0$.
4. **Directly.** $f(x) + g(x) = 6x - 1$, and $\abs{(6x - 1) - 17} = 6\abs{x - 3}$, which is
   less than $\eps$ exactly when $\abs{x - 3} < \frac{\eps}{6}$ (dividing by the positive
   number $6$). So $\frac{\eps}{6}$ is the largest $\delta$ that works: a larger window
   contains $x = 3 + \frac{\eps}{6}$, where the distance is exactly $\eps$.

The proof gives
$$
\boxed{\delta = \frac{\eps}{8}},
$$
and the largest $\delta$ that works is $\frac{\eps}{6}$. The proof's $\delta$ is smaller than
the largest one because the proof gives each function half of the tolerance, and $g$ needs more
than half. On the largest window, $\abs{x - 3} < \frac{\eps}{6}$, the error
$\abs{g(x) - 12} = 4\abs{x - 3}$ comes as close as we like to $\frac{2\eps}{3}$, while
$\abs{f(x) - 5} = 2\abs{x - 3}$ stays below $\frac{\eps}{3}$. Held to half of the tolerance,
$g$ allows only the smaller window $\delta_2 = \frac{\eps}{8}$. A proof only needs *some*
$\delta$ that works.

**Check.** For $\eps = 0.6$: $\delta = 0.075$, and $x = 3.07$ gives
$\abs{6(3.07) - 1 - 17} = 0.42 < 0.6$. ✓
:::

:::{proof:example} The limit from Why this matters
:label: eg-calc-limit-laws-rational

Find $\displaystyle \lim_{x \to 2} \frac{x^3 - 1}{x^2 + 3}$ with the laws of
[](#thm-calc-limit-laws), naming the law used at each step.

1. **The denominator.** By part (a), $\lim_{x \to 2} x = 2$, so by part (e),
   $\lim_{x \to 2} x^2 = 4$. By part (a), $\lim_{x \to 2} 3 = 3$. By part (b),
   $\lim_{x \to 2} (x^2 + 3) = 4 + 3 = 7$.
2. **The hypothesis of the quotient law.** The denominator's limit is $7 \ne 0$, so part (d)
   may be used.
3. **The numerator.** By part (e), $\lim_{x \to 2} x^3 = 2^3 = 8$, and by parts (a) and (b),
   $\lim_{x \to 2} (x^3 - 1) = 8 - 1 = 7$.
4. **The quotient.** By part (d), the limit is $\frac{7}{7} = 1$.

$$
\boxed{\lim_{x \to 2} \frac{x^3 - 1}{x^2 + 3} = 1}
$$

These steps are the proof of [](#cor-calc-direct-substitution) for this one function. From now
on we may cite the corollary instead: the function is rational, its denominator is $7 \ne 0$ at
$x = 2$, and its value there is $\frac{7}{7} = 1$.

**Check.** At $x = 2.001$ the function is $\frac{7.012006001}{7.004001} \approx 1.001143$, as
in the table of [Why this matters](#wdg-calc-limit-laws-rational). ✓
:::

:::{proof:example} A square root inside a quotient
:label: eg-calc-limit-laws-root-quotient

Find $\displaystyle \lim_{x \to 1} \frac{x + \sqrt{x + 3}}{x^2 + 1}$.

1. **The square root.** By [](#cor-calc-direct-substitution),
   $\lim_{x \to 1} (x + 3) = 4$. Since $4 > 0$, part (f) of [](#thm-calc-limit-laws) gives
   $\lim_{x \to 1} \sqrt{x + 3} = \sqrt{4} = 2$, and says that $\sqrt{x + 3}$ is defined near
   $1$ (it is defined for every $x \ge -3$).
2. **The numerator.** By parts (a) and (b), $\lim_{x \to 1} \bigl(x + \sqrt{x + 3}\bigr) =
   1 + 2 = 3$.
3. **The denominator.** By [](#cor-calc-direct-substitution),
   $\lim_{x \to 1} (x^2 + 1) = 2$, which is not $0$.
4. **The quotient.** By part (d), the limit is $\frac{3}{2}$.

$$
\boxed{\lim_{x \to 1} \frac{x + \sqrt{x + 3}}{x^2 + 1} = \frac{3}{2}}
$$

The corollary alone does not give this limit: the function is not rational, because of the
square root. The laws handle it one part at a time.

**Check.** At $x = 1.01$: $\sqrt{4.01} \approx 2.002498$, so the function is about
$\frac{3.012498}{2.0201} \approx 1.491262$, close to $1.5$. ✓
:::

:::{proof:example} Two resistors in parallel
:label: eg-calc-limit-laws-resistors

Two resistors in parallel, of $3$ ohms and $t$ ohms, have the combined resistance
$$
R(t) = \frac{3t}{3 + t}
$$
ohms, for $t > 0$. The second resistor warms up, and its resistance $t$ approaches $6$ ohms.
What does the combined resistance approach?

1. **The function.** Only $t > 0$ makes sense here, so $R$ is not itself a rational function: it
   is the restriction of the rational function $r(t) = \frac{3t}{3 + t}$, defined at every
   $t \ne -3$, to the open interval $(0, \infty)$. That interval contains $6$, and $R$ is
   defined at every point of it.
2. **The hypothesis.** The denominator at $t = 6$ is $3 + 6 = 9 \ne 0$.
3. **Substitute.** By part (c) of [](#cor-calc-direct-substitution), with $I = (0, \infty)$,
   $\lim_{t \to 6} R(t) = R(6) = \frac{18}{9} = 2$.

$$
\boxed{\lim_{t \to 6} R(t) = 2}
$$

So the combined resistance approaches $2$ ohms.

**Check.** At $t = 6.01$: $R(6.01) = \frac{18.03}{9.01} \approx 2.00111$, in ohms. ✓ Units:
ohms times ohms divided by ohms gives ohms. ✓ A parallel combination is smaller than each of its
resistors, and $2 < 3$. ✓
:::

### Checking the hypotheses

:::{proof:example} Do the laws apply?
:label: eg-calc-limit-laws-hypotheses

For each limit, decide whether the laws of [](#thm-calc-limit-laws) give it.

- (i) $\displaystyle \lim_{x \to 1} \frac{x^2 - 1}{x - 1}$
- (ii) $\displaystyle \lim_{x \to 0} x \cdot \frac{1}{x}$
- (iii) $\displaystyle \lim_{x \to 2} \sqrt{x - 2}$

1. **(i)** By [](#cor-calc-direct-substitution), the numerator and the denominator have the
   limits $1 - 1 = 0$ and $1 - 1 = 0$. The quotient law needs the denominator's limit to be
   non-zero, so it does not apply. The laws say nothing here: this is a "$\frac{0}{0}$", the
   subject of the next page.
2. **(ii)** The product law needs both factors to have limits, and $\frac{1}{x}$ has none at $0$
   ([](#sec-calc-limit-laws-not-apply)). So the law does not apply. The
   limit exists anyway: $x \cdot \frac{1}{x} = 1$ at every $x \ne 0$, so every $\delta > 0$
   wins every round, and the limit is $1$.
3. **(iii)** The inside $x - 2$ has the limit $0$, but it is negative at every $x < 2$, so the
   sign condition of part (f) fails, and $\sqrt{x - 2}$ is undefined at every $x < 2$. It is
   not defined on any open interval around $2$, so
   [the definition of a limit](#def-calc-limit) does not apply at all.

**Conclusion.** The laws give none of the three: (i) is a $\frac{0}{0}$; in (ii) a factor has
no limit, yet the limit is $1$; in (iii) the function is undefined to the left of $2$.

"The laws do not apply" is not "the limit does not exist": in (ii) the limit exists. When a law
does not apply, we need another argument.

**Check.** (i) At $x = 1.001$ the numerator is $0.002001$ and the denominator $0.001$: both are
close to $0$. ✓ (ii) At $x = 0.001$: $0.001 \cdot 1000 = 1$. ✓ (iii) At $x = 1.99$:
$x - 2 = {-0.01}$, which has no real square root. ✓
:::

## Common mistakes

:::{warning} "Zero times anything is zero"
✗ **Wrong:** "$\lim_{x \to 0} x \cdot \frac{1}{x} = 0$, because $\lim_{x \to 0} x = 0$, and
zero times anything is zero."

**Why:** the product law applies only when *both* factors have limits, and $\frac{1}{x}$ has
none at $0$ ([](#sec-calc-limit-laws-not-apply)). A factor that
approaches $0$ can be outweighed by one that grows without bound.

✓ **Right:** $x \cdot \frac{1}{x} = 1$ for every $x \ne 0$, so the limit is $1$
([](#eg-calc-limit-laws-hypotheses)). Before splitting a limit, check that every part has one.
:::

:::{warning} Using the quotient law when the denominator approaches $0$
✗ **Wrong:** "$\displaystyle \lim_{x \to 1} \frac{x^2 - 1}{x - 1} = \frac{0}{0}$, so the limit
does not exist." Or: "the numerator approaches $0$, so the quotient approaches $0$."

**Why:** the quotient law needs $M \ne 0$. With $M = 0$ it says nothing, and
"$\frac{0}{0}$" can hide any number, as [the figure](#wdg-calc-limit-laws-zero-over-zero) shows.

✓ **Right:** read "$\frac{0}{0}$" as "the quotient law does not apply here". The next page,
Computing Limits Algebraically, rewrites such a function first.
:::

:::{warning} Substituting into any formula
✗ **Wrong:** for the function $h$ of
[the remark on the value at $a$](#rem-calc-limit-value-irrelevant), with $h(x) = x + 1$ for
$x \ne 1$ and $h(1) = 5$: "by direct substitution, $\lim_{x \to 1} h(x) = h(1) = 5$."

**Why:** [](#cor-calc-direct-substitution) is about polynomials and rational functions. The
function $h$ is neither. By the ✓ part below, its limit at $1$ is $2$. If $h$ were a
polynomial, or a rational function (whose denominator is not $0$ at $1$, since $h(1)$ is
defined), the corollary would give the limit $h(1) = 5$, and two different limits contradict
[uniqueness of limits](#thm-calc-limit-unique).

✓ **Right:** $h$ is the polynomial $x + 1$ with its value at $1$ changed, and by
[the remark on the value at $a$](#rem-calc-limit-value-irrelevant) that does not change the
limit. So $\lim_{x \to 1} h(x) = \lim_{x \to 1} (x + 1) = 2$, by
[](#cor-calc-direct-substitution).
:::

:::{warning} The square-root law at the edge of the domain
✗ **Wrong:** "$\displaystyle \lim_{x \to 0} \sqrt{x} = \sqrt{0} = 0$ by the square-root law."

**Why:** with $L = 0$, part (f) of [](#thm-calc-limit-laws) needs $f(x) \ge 0$ on both sides of
$a$. Here $f(x) = x$ is negative at every $x < 0$, where $\sqrt{x}$ is undefined, so
[the definition of a limit](#def-calc-limit) does not apply at $0$.

✓ **Right:** only $x > 0$ comes near $0$ inside the domain of $\sqrt{x}$. Approaching $0$ from
the right is a one-sided limit, the subject of the page One-Sided Limits. Compare
$\lim_{x \to 0} \sqrt{x^2} = 0$, where the sign condition holds.
:::

## Rigorous track

The product and quotient laws need more than sharing the tolerance: in a product, the error in
one factor is multiplied by the other factor, and in a quotient we divide by $g(x)$, which must
stay away from $0$.

:::{proof:proof} Rigorous track
:label: prf-calc-limit-laws
:enumerated: false
:class: dropdown
This proves parts (c) and (d) of the limit laws, stated in Main results. For the product we split
$f(x)\,g(x) - LM$ into two terms, each a small error times a bounded factor; for the quotient we
first show that $\frac{1}{g(x)}$ approaches $\frac{1}{M}$ and then use the product law. Every
multiplication of an inequality below names the sign of the factor, by the order rules of
[Absolute Value and Inequalities](#calc-absolute-value-inequalities) ("Working with
inequalities").

**(c) Product.** The strategy rests on the identity
$$
f(x)\,g(x) - LM = f(x)\bigl(g(x) - M\bigr) + M\bigl(f(x) - L\bigr),
$$
which holds because the two middle terms, $-f(x)M$ and $+Mf(x)$, cancel. Let $\eps > 0$.

1. *$f$ is bounded near $a$.* The definition of $\lim_{x \to a} f(x) = L$, with the tolerance
   $1$, gives a $\delta_1 > 0$ such that $f$ is defined and $\abs{f(x) - L} < 1$ at every $x$
   with $0 < \abs{x - a} < \delta_1$. For such $x$, by
   [part (a) of the triangle inequality](#thm-calc-triangle-inequality), applied to the numbers
   $f(x) - L$ and $L$, and then adding $\abs{L}$ to both sides of $\abs{f(x) - L} < 1$,
   $$
   \abs{f(x)} = \abs{\bigl(f(x) - L\bigr) + L} \le \abs{f(x) - L} + \abs{L} < 1 + \abs{L} .
   $$
2. *The tolerances.* Let $K = \abs{L} + 1$ and $N = \abs{M} + 1$. Both are at least $1$, by
   [property 1 of the absolute value](#rem-calc-absolute-value-properties), so
   $\frac{\eps}{2K}$ and $\frac{\eps}{2N}$ are positive. So there are $\delta_2 > 0$ and
   $\delta_3 > 0$ such that $g$ is defined and $\abs{g(x) - M} < \frac{\eps}{2K}$ at every $x$
   with $0 < \abs{x - a} < \delta_2$, and $\abs{f(x) - L} < \frac{\eps}{2N}$ at every $x$ with
   $0 < \abs{x - a} < \delta_3$. (We use $N = \abs{M} + 1$ rather than $\abs{M}$ because $M$
   may be $0$, and we may not divide by $0$.)
3. *The proof.* Let $\delta = \min(\delta_1, \delta_2, \delta_3)$, which is positive, and let
   $0 < \abs{x - a} < \delta$. Then $x$ lies in all three windows, so $f(x)$, $g(x)$ and
   $f(x)\,g(x)$ are defined. By the identity, part (a) of the triangle inequality and
   [property 4 of the absolute value](#rem-calc-absolute-value-properties),
   $$
   \begin{aligned}
   \abs{f(x)\,g(x) - LM}
     &= \abs{f(x)\bigl(g(x) - M\bigr) + M\bigl(f(x) - L\bigr)} \\
     &\le \abs{f(x)}\,\abs{g(x) - M} + \abs{M}\,\abs{f(x) - L} .
   \end{aligned}
   $$
   *The first term.* By step 1, $\abs{f(x)} < K$. Multiplying by $\abs{g(x) - M}$, which is
   $\ge 0$ and may be $0$, gives only $\abs{f(x)}\,\abs{g(x) - M} \le K\abs{g(x) - M}$.
   Multiplying $\abs{g(x) - M} < \frac{\eps}{2K}$ by the positive number $K$ keeps the strict
   inequality: $K\abs{g(x) - M} < \frac{\eps}{2}$. So the first term is less than
   $\frac{\eps}{2}$.

   *The second term.* $\abs{M} < N$. Multiplying by $\abs{f(x) - L} \ge 0$ gives
   $\abs{M}\,\abs{f(x) - L} \le N\abs{f(x) - L}$, and multiplying
   $\abs{f(x) - L} < \frac{\eps}{2N}$ by the positive number $N$ gives
   $N\abs{f(x) - L} < \frac{\eps}{2}$. So the second term is less than $\frac{\eps}{2}$.

   Adding the two strict inequalities, $\abs{f(x)\,g(x) - LM} < \eps$.

The product $fg$ is defined at every $x$ with $0 < \abs{x - a} < \delta$, which by
[part (e) of the proposition on distance inequalities](#prop-calc-abs-interval) is the open
interval $(a - \delta, a + \delta)$ with $a$ removed, so the definition applies to it, and
$\lim_{x \to a} f(x)\,g(x) = LM$. For the "in particular", apply this to the constant function
$c$, which is defined everywhere and has the limit $c$ by part (a), and to $f$:
$\lim_{x \to a} c\,f(x) = cL$.

**(d) Quotient.** Suppose $M \ne 0$.

1. *$g$ stays away from $0$ near $a$.* By
   [property 1 of the absolute value](#rem-calc-absolute-value-properties), $\abs{M} > 0$, so
   $\frac{\abs{M}}{2}$ is a tolerance. The definition gives a $\delta_4 > 0$ such that $g$ is
   defined and $\abs{g(x) - M} < \frac{\abs{M}}{2}$ at every $x$ with
   $0 < \abs{x - a} < \delta_4$. For such $x$,
   $$
   \abs{M} - \abs{g(x)} \le \abs{\abs{M} - \abs{g(x)}} \le \abs{M - g(x)} < \frac{\abs{M}}{2},
   $$
   by [property 3 of the absolute value](#rem-calc-absolute-value-properties) ($u \le \abs{u}$),
   [part (c) of the triangle inequality](#thm-calc-triangle-inequality), and
   $\abs{M - g(x)} = \abs{g(x) - M}$
   ([property 2](#rem-calc-absolute-value-properties)). Adding
   $\abs{g(x)} - \frac{\abs{M}}{2}$ to both sides gives $\abs{g(x)} > \frac{\abs{M}}{2} > 0$.
   So $g(x) \ne 0$, since $\abs{0} = 0$ by [the definition](#def-calc-absolute-value). Hence
   $\frac{1}{g}$ is defined at every $x$ with $0 < \abs{x - a} < \delta_4$, which by part (e) of
   the proposition on distance inequalities is the open interval $(a - \delta_4, a + \delta_4)$
   with $a$ removed.
2. *$\frac{1}{g(x)}$ approaches $\frac{1}{M}$.* Let $\eps > 0$. The number
   $\frac{\eps\abs{M}^2}{2}$ is positive, so there is a $\delta_5 > 0$ such that
   $\abs{g(x) - M} < \frac{\eps\abs{M}^2}{2}$ at every $x$ with $0 < \abs{x - a} < \delta_5$.
   Let $\delta = \min(\delta_4, \delta_5)$ and $0 < \abs{x - a} < \delta$. Since
   $\frac{1}{g(x)} - \frac{1}{M} = \frac{M - g(x)}{g(x)\,M}$, properties 4 and 2 of the
   absolute value give
   $$
   \abs{\frac{1}{g(x)} - \frac{1}{M}} = \frac{\abs{g(x) - M}}{\abs{g(x)}\,\abs{M}} .
   $$
   Multiplying $\abs{g(x)} > \frac{\abs{M}}{2}$ (step 1) by the positive number $\abs{M}$ gives
   $\abs{g(x)}\,\abs{M} > \frac{\abs{M}^2}{2} > 0$. For positive numbers $u > v$, multiplying by
   the positive number $\frac{1}{uv}$ gives $\frac{1}{v} > \frac{1}{u}$; so
   $\frac{1}{\abs{g(x)}\,\abs{M}} < \frac{2}{\abs{M}^2}$. Multiplying this by
   $\abs{g(x) - M}$, which is $\ge 0$ and may be $0$, gives only $\le$, and then multiplying
   $\abs{g(x) - M} < \frac{\eps\abs{M}^2}{2}$ by the positive number $\frac{2}{\abs{M}^2}$
   keeps the strict inequality:
   $$
   \abs{\frac{1}{g(x)} - \frac{1}{M}} \le \frac{2\abs{g(x) - M}}{\abs{M}^2} < \eps .
   $$
   So $\lim_{x \to a} \frac{1}{g(x)} = \frac{1}{M}$.
3. *The quotient.* By step 1, $\frac{1}{g}$ satisfies the hypothesis on the domain in
   the theorem, and so does $f$. By step 2 and part (c), applied to $f$ and
   $\frac{1}{g}$,
   $$
   \lim_{x \to a} f(x) \cdot \frac{1}{g(x)} = L \cdot \frac{1}{M} = \frac{L}{M} .
   $$
   The functions $f \cdot \frac{1}{g}$ and $\frac{f}{g}$ are defined at the same $x$ (those
   where $f(x)$ and $g(x)$ are defined and $g(x) \ne 0$) and have the same values there, so
   they are the same function, and $\lim_{x \to a} \frac{f(x)}{g(x)} = \frac{L}{M}$.
:::

:::{admonition} Sharing the tolerance in other ways
:class: dropdown rigor
The proof of the sum law gives each function half of the tolerance, but any split works: if
$\abs{f(x) - L} < \eps_1$ and $\abs{g(x) - M} < \eps_2$ with $\eps_1 + \eps_2 = \eps$, the
same display gives $\abs{(f(x) + g(x)) - (L + M)} < \eps$. In
[](#eg-calc-limit-laws-sum-delta), giving $\frac{2\eps}{3}$ to $f$ and $\frac{\eps}{3}$ to
$g$ produces $\delta = \min\bigl(\frac{\eps}{3}, \frac{\eps}{12}\bigr) = \frac{\eps}{12}$, a
worse $\delta$, and giving $\frac{\eps}{3}$ to $f$ and $\frac{2\eps}{3}$ to $g$ produces
$\min\bigl(\frac{\eps}{6}, \frac{\eps}{6}\bigr) = \frac{\eps}{6}$, the largest one.

For a sum of three functions, give each $\frac{\eps}{3}$, or apply the law twice:
$f + g + h = (f + g) + h$. The proof of [](#cor-calc-direct-substitution) does the second,
once for each term of the polynomial.
:::

## Summary

- The limit laws ([](#thm-calc-limit-laws)) compute the limit of a sum, difference, product,
  quotient, power or square root from the limits of its parts, which must exist as real
  numbers.
- The sum law is proved by sharing the tolerance: $\frac{\eps}{2}$ for each part, and
  $\delta = \min(\delta_1, \delta_2)$.
- The quotient law needs $M \ne 0$; the square-root law needs $L > 0$, or $L = 0$ and
  $f(x) \ge 0$ near $a$.
- For a polynomial, and for a rational function at a point where its denominator is not $0$,
  the limit is the value at the point ([](#cor-calc-direct-substitution)); this still holds
  when the rational function is restricted to an open interval around the point.
- When a hypothesis fails, the law says nothing: "$\frac{0}{0}$" is a signal to do more work,
  not an answer, and "the laws do not apply" is not "the limit does not exist".

## Exercises

::::{exercise} Combining given limits
:label: exr-calc-limit-laws-given-limits
:class: tier-a

Let $f$ and $g$ be defined at every point of an open interval containing $a$, except possibly
at $a$, with $\lim_{x \to a} f(x) = 3$ and $\lim_{x \to a} g(x) = -2$. Find
(a) $\lim_{x \to a} \bigl(2f(x) - g(x)\bigr)$, (b) $\lim_{x \to a} f(x)\bigl(g(x)\bigr)^2$,
(c) $\lim_{x \to a} \dfrac{f(x)}{g(x) + 5}$, (d) $\lim_{x \to a} \sqrt{f(x) + 1}$.

:::{admonition} Hint 1
:class: dropdown hint
Name the law for each step, and check its hypothesis: in (c) the limit of the denominator, in
(d) the limit under the root.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $8$ (b) $12$ (c) $1$ (d) $2$
:::
::::

::::{solution} exr-calc-limit-laws-given-limits
:label: sol-calc-limit-laws-given-limits
:class: dropdown

All parts use [](#thm-calc-limit-laws).

(a) By the "in particular" of part (c), $\lim_{x \to a} 2f(x) = 2 \cdot 3 = 6$. By part (b), the
difference has the limit $6 - (-2) = 8$.

(b) By part (e) with $n = 2$, $\lim_{x \to a} \bigl(g(x)\bigr)^2 = (-2)^2 = 4$. By part (c),
the product has the limit $3 \cdot 4 = 12$.

(c) By parts (a) and (b), $\lim_{x \to a} \bigl(g(x) + 5\bigr) = -2 + 5 = 3$, which is not $0$.
So part (d) applies, and the limit is $\frac{3}{3} = 1$.

(d) By parts (a) and (b), $\lim_{x \to a} \bigl(f(x) + 1\bigr) = 4$, which is positive. So
part (f) applies, and the limit is $\sqrt{4} = 2$, because $2 \ge 0$ and $2^2 = 4$
([the square-root remark](#rem-calc-square-roots)).
::::

::::{exercise} A polynomial
:label: exr-calc-limit-laws-polynomial
:class: tier-a

Find $\displaystyle \lim_{x \to -1} \bigl(2x^3 - x + 4\bigr)$.

:::{admonition} Hint 1
:class: dropdown hint
Which result says that the limit of a polynomial is its value?
:::

:::{admonition} Answer
:class: dropdown answer
$3$
:::
::::

::::{solution} exr-calc-limit-laws-polynomial
:label: sol-calc-limit-laws-polynomial
:class: dropdown

The function is a polynomial, so by part (a) of [](#cor-calc-direct-substitution) the limit is
its value at ${-1}$:
$$
2(-1)^3 - (-1) + 4 = -2 + 1 + 4 = 3 .
$$
::::

::::{exercise} A rational function
:label: exr-calc-limit-laws-rational
:class: tier-a

Find $\displaystyle \lim_{x \to 2} \frac{x^2 + 1}{x - 3}$.

:::{admonition} Hint 1
:class: dropdown hint
Check the denominator at $x = 2$ before you substitute.
:::

:::{admonition} Answer
:class: dropdown answer
${-5}$
:::
::::

::::{solution} exr-calc-limit-laws-rational
:label: sol-calc-limit-laws-rational
:class: dropdown

The function is rational, with the denominator $q(x) = x - 3$, and $q(2) = -1 \ne 0$. By part
(b) of [](#cor-calc-direct-substitution), the limit is the value at $2$:
$$
\frac{2^2 + 1}{2 - 3} = \frac{5}{-1} = -5 .
$$
::::

::::{exercise} Where substitution works
:label: exr-calc-limit-laws-where-substitution
:class: tier-a

Let $r(x) = \dfrac{x + 2}{x^2 - 4}$. For which real numbers $a$ does
[](#cor-calc-direct-substitution) give $\lim_{x \to a} r(x)$? Give the set of all such $a$.

:::{admonition} Hint 1
:class: dropdown hint
The corollary needs the denominator to be non-zero at $a$. When is $a^2 - 4 = 0$?
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, -2), (-2, 2), (2, \infty)$
:::
::::

::::{solution} exr-calc-limit-laws-where-substitution
:label: sol-calc-limit-laws-where-substitution
:class: dropdown

The numerator $x + 2$ and the denominator $q(x) = x^2 - 4$ are polynomials, so part (b) of
[](#cor-calc-direct-substitution) applies exactly at the $a$ with $q(a) \ne 0$. Now
$a^2 - 4 = 0$ means $a^2 = 2^2$, that is, $\abs{a}^2 = 2^2$, by
[property 5 of the absolute value](#rem-calc-absolute-value-properties). Both $\abs{a}$ and $2$
are non-negative, so by [property 6](#rem-calc-absolute-value-properties) this holds exactly
when $\abs{a} = 2$, that is, when $a = 2$ or $a = -2$. So the corollary applies at every $a$
except $2$ and ${-2}$:
$$
(-\infty, -2) \cup (-2, 2) \cup (2, \infty) .
$$
At the two excluded points the laws are silent: at $2$ the numerator approaches $4$ and the
denominator $0$, and at ${-2}$ both approach $0$.
::::

::::{exercise} Roots in a quotient
:label: exr-calc-limit-laws-roots
:class: tier-b

Find $\displaystyle \lim_{x \to 4} \frac{\sqrt{x} + x}{\sqrt{x^2 + 9}}$, and say which law you
use at each step.

:::{admonition} Hint 1
:class: dropdown hint
Find the limits of $x$ and of $x^2 + 9$ first, then take square roots with part (f) of
[](#thm-calc-limit-laws). Check that each limit under a root is positive.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{6}{5}$
:::
::::

::::{solution} exr-calc-limit-laws-roots
:label: sol-calc-limit-laws-roots
:class: dropdown

We use [](#thm-calc-limit-laws) and [](#cor-calc-direct-substitution).

- By part (a), $\lim_{x \to 4} x = 4$, which is positive, so by part (f)
  $\lim_{x \to 4} \sqrt{x} = \sqrt{4} = 2$.
- By part (b), the numerator has the limit $2 + 4 = 6$.
- By the corollary, $\lim_{x \to 4} (x^2 + 9) = 25$, which is positive, so by part (f) the
  denominator has the limit $\sqrt{25} = 5$ (since $5 \ge 0$ and $5^2 = 25$,
  [the square-root remark](#rem-calc-square-roots)). It is not $0$.
- By part (d), the limit is $\frac{6}{5}$.
::::

::::{exercise} The image formed by a lens
:label: exr-calc-limit-laws-lens
:class: tier-b applied

A thin lens with focal length $5$ cm forms an image of an object at distance $u$ cm from the
lens at the distance
$$
v(u) = \frac{5u}{u - 5}
$$
cm from the lens, for $u > 5$. The object is moved towards the distance $15$ cm. Find
$\lim_{u \to 15} v(u)$, in cm.

:::{admonition} Hint 1
:class: dropdown hint
$v$ is a rational function of $u$, used only for $u > 5$. Which part of
[](#cor-calc-direct-substitution) covers that? Is the denominator $0$ at $u = 15$?
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{15}{2}$
:::
::::

::::{solution} exr-calc-limit-laws-lens
:label: sol-calc-limit-laws-lens
:class: dropdown

Since $v$ is used only for $u > 5$, it is the restriction of the rational function
$\frac{5u}{u - 5}$, defined at every $u \ne 5$, to the open interval $(5, \infty)$, which
contains $15$. The denominator $u - 5$ is $10 \ne 0$ at $u = 15$. By part (c) of
[](#cor-calc-direct-substitution), with $I = (5, \infty)$,
$$
\lim_{u \to 15} v(u) = v(15) = \frac{75}{10} = \frac{15}{2} .
$$
So the image approaches the distance $7.5$ cm from the lens.

As $u$ approaches $5$, the quotient law would not apply: the numerator approaches $25$ and the
denominator $0$. (Optically, an object at the focal point forms no image at a finite distance.)
::::

::::{exercise} The $\delta$ from the proof of the sum law
:label: exr-calc-limit-laws-sum-delta
:class: tier-b

Let $f(x) = 3x - 2$ and $g(x) = 5 - x$, so that $\lim_{x \to 2} f(x) = 4$ and
$\lim_{x \to 2} g(x) = 3$. Let $\eps > 0$.
(a) In the proof of the sum law, part (b) of [](#thm-calc-limit-laws), take for $\delta_1$
and $\delta_2$ the largest $\delta$ that works for $f$ and for $g$ with the tolerance
$\frac{\eps}{2}$. Which $\delta$ does the proof give for $f + g$?
(b) What is the largest $\delta$ that works for $\lim_{x \to 2} \bigl(f(x) + g(x)\bigr) = 7$
with the tolerance $\eps$?

:::{admonition} Hint 1
:class: dropdown hint
Write $\abs{f(x) - 4}$, $\abs{g(x) - 3}$ and $\abs{(f(x) + g(x)) - 7}$ as multiples of
$\abs{x - 2}$, as in [](#eg-calc-limit-laws-sum-delta).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $\frac{\eps}{6}$ (b) $\frac{\eps}{2}$
:::
::::

::::{solution} exr-calc-limit-laws-sum-delta
:label: sol-calc-limit-laws-sum-delta
:class: dropdown

(a) $\abs{f(x) - 4} = \abs{3x - 6} = 3\abs{x - 2}$, which is less than $\frac{\eps}{2}$ exactly
when $\abs{x - 2} < \frac{\eps}{6}$ (dividing by the positive number $3$). So the largest
$\delta_1$ is $\frac{\eps}{6}$: a larger window contains $x = 2 + \frac{\eps}{6}$, where the
distance is exactly $\frac{\eps}{2}$. Next,
$\abs{g(x) - 3} = \abs{2 - x} = \abs{x - 2}$, by
[property 2 of the absolute value](#rem-calc-absolute-value-properties), so the largest
$\delta_2$ is $\frac{\eps}{2}$. The proof takes
$\delta = \min\bigl(\frac{\eps}{6}, \frac{\eps}{2}\bigr) = \frac{\eps}{6}$.

(b) $f(x) + g(x) = 2x + 3$, and $\abs{(2x + 3) - 7} = 2\abs{x - 2}$, which is less than $\eps$
exactly when $\abs{x - 2} < \frac{\eps}{2}$. So $\frac{\eps}{2}$ works, and no larger
$\delta$ does: its window contains $x = 2 + \frac{\eps}{2}$, where the distance is exactly
$\eps$.

The proof's $\delta$ is three times smaller than the largest one, and still correct.
::::

::::{exercise} A sum and one of its parts
:label: exr-calc-limit-laws-sum-part
:class: tier-b

Let $f$ and $g$ be defined at every point of an open interval containing $a$, except possibly
at $a$. True or false: if $\lim_{x \to a} f(x)$ and $\lim_{x \to a} \bigl(f(x) + g(x)\bigr)$
both exist, then $\lim_{x \to a} g(x)$ exists.

:::{admonition} Hint 1
:class: dropdown hint
Write $g(x)$ as a difference of two functions whose limits you know.
:::

:::{admonition} Answer
:class: dropdown answer bool
True
:::
::::

::::{solution} exr-calc-limit-laws-sum-part
:label: sol-calc-limit-laws-sum-part
:class: dropdown

True. Let $\lim_{x \to a} f(x) = L$ and $\lim_{x \to a} \bigl(f(x) + g(x)\bigr) = K$. By the
difference law, part (b) of [](#thm-calc-limit-laws), applied to the functions $f + g$ and $f$,
$$
\lim_{x \to a} \Bigl(\bigl(f(x) + g(x)\bigr) - f(x)\Bigr) = K - L .
$$
This function is defined at every $x$ at which $f(x)$ and $g(x)$ are both defined, and there
its value is $g(x)$. Let $\eps > 0$, and let $\delta$ win the round $\eps$ for the difference.
By the domain clause of [the definition of a limit](#def-calc-limit), the difference is defined
at every $x$ with $0 < \abs{x - a} < \delta$, so $g(x)$ is defined there too and equals it.
So the same $\delta$ wins the round $\eps$ for $g$, and $\lim_{x \to a} g(x) = K - L$.
::::

::::{exercise} A product and one of its factors
:label: exr-calc-limit-laws-product-part
:class: tier-b

Let $f$ and $g$ be defined at every point of an open interval containing $a$, except possibly
at $a$. True or false: if $\lim_{x \to a} f(x)$ and $\lim_{x \to a} f(x)\,g(x)$ both exist, then
$\lim_{x \to a} g(x)$ exists.

:::{admonition} Hint 1
:class: dropdown hint
Try the limit of [](#eg-calc-limit-laws-hypotheses), part (ii).
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-limit-laws-product-part
:label: sol-calc-limit-laws-product-part
:class: dropdown

False. Take $a = 0$, $f(x) = x$ and $g(x) = \frac{1}{x}$ for $x \ne 0$. Both are defined at every
$x \ne 0$. By part (a) of [](#thm-calc-limit-laws), $\lim_{x \to 0} f(x) = 0$. The product is
$f(x)\,g(x) = 1$ at every $x \ne 0$, so every $\delta > 0$ wins every round, and its limit is
$1$. But $g$ has no limit at $0$: if $\lim_{x \to 0} g(x) = M$, the product law would give
$\lim_{x \to 0} f(x)\,g(x) = 0 \cdot M = 0$, and [uniqueness of limits](#thm-calc-limit-unique)
would give $0 = 1$.

Dividing does not rescue the claim: $g = \frac{fg}{f}$, but the quotient law needs
$\lim f(x) \ne 0$, and here it is $0$.
::::

::::{exercise} A square root with limit $0$
:label: exr-calc-limit-laws-root-zero
:class: tier-b

Find $\displaystyle \lim_{x \to 0} \sqrt{x^2 + x^4}$, and check the hypotheses of the law you
use.

:::{admonition} Hint 1
:class: dropdown hint
The limit under the root is $0$. Which extra hypothesis does part (f) of
[](#thm-calc-limit-laws) need then?
:::

:::{admonition} Answer
:class: dropdown answer
$0$
:::
::::

::::{solution} exr-calc-limit-laws-root-zero
:label: sol-calc-limit-laws-root-zero
:class: dropdown

By [](#cor-calc-direct-substitution), $\lim_{x \to 0} (x^2 + x^4) = 0$. The square-root law
with $L = 0$ needs $x^2 + x^4 \ge 0$ near $0$. For every real $x$,
$x^2 + x^4 = x^2(1 + x^2)$, with $x^2 \ge 0$ and $1 + x^2 \ge 1 > 0$. Multiplying
$0 \le x^2$ by the positive number $1 + x^2$ keeps the inequality, so
$0 \le x^2(1 + x^2)$. So the hypothesis holds with any $r > 0$, and
part (f) of [](#thm-calc-limit-laws) gives
$$
\lim_{x \to 0} \sqrt{x^2 + x^4} = 0 .
$$
::::

::::{exercise} When is the square root defined near the point?
:label: exr-calc-limit-laws-root-domain
:class: tier-c

For which real numbers $c$ is $\sqrt{cx - x^2}$ defined at every point of some open interval
containing $2$, except possibly at $2$? Give the set of all such $c$, and show that for each
of them $\lim_{x \to 2} \sqrt{cx - x^2} = \sqrt{2c - 4}$.

:::{admonition} Hint 1
:class: dropdown hint
$cx - x^2 = x(c - x)$. For $x$ near $2$, the factor $x$ is positive. What is the sign of
$c - x$?
:::

:::{admonition} Hint 2
:class: dropdown hint
If $c \le 2$, look at the points just to the right of $2$.
:::

:::{admonition} Answer
:class: dropdown answer set
$(2, \infty)$
:::
::::

::::{solution} exr-calc-limit-laws-root-domain
:label: sol-calc-limit-laws-root-domain
:class: dropdown

The square root is defined exactly where $cx - x^2 = x(c - x) \ge 0$.

**If $c > 2$.** The open interval $(1, c)$ contains $2$. At every $x$ in it, $x > 0$ and
$c - x > 0$, so $x(c - x) > 0$ (a product of two positive numbers), and the square root is
defined. By [](#cor-calc-direct-substitution), $\lim_{x \to 2} (cx - x^2) = 2c - 4$, which is
positive since $c > 2$. So part (f) of [](#thm-calc-limit-laws) gives
$\lim_{x \to 2} \sqrt{cx - x^2} = \sqrt{2c - 4}$.

**If $c \le 2$.** Every open interval containing $2$ contains numbers $x$ with $2 < x < 3$:
by [the definition of an interval](#def-calc-interval), it contains every number between $2$
and its right endpoint, or every number greater than $2$ if it has no right endpoint; take $x$
halfway between $2$ and the smaller of $3$ and that endpoint, or $x = \frac{5}{2}$ if there is
none. At such an $x$, $x > 0$ and $c - x < c - 2 \le 0$, so
$x(c - x) < 0$ (a product of a positive and a negative number), and the square root is
undefined. So no open interval containing $2$ works.

The set is $(2, \infty)$, and for those $c$ the limit is $\sqrt{2c - 4}$. For $c = 2$ the
limit under the root is $0$, but the sign condition of part (f) fails to the right of $2$.
::::

::::{exercise} The constant multiple law from the definition
:label: exr-calc-limit-laws-constant-multiple
:class: tier-c rigor

Suppose that $\lim_{x \to a} f(x) = L$, and let $c$ be a real number. Prove from
[the definition of a limit](#def-calc-limit), without the product law, that
$\lim_{x \to a} c\,f(x) = cL$.

:::{admonition} Hint 1
:class: dropdown hint
Treat $c = 0$ separately. For $c \ne 0$, which tolerance should you demand from $f$?
:::

:::{admonition} Answer
:class: dropdown answer manual
For $c \ne 0$, a $\delta$ that works for $f$ with the tolerance $\eps / \abs{c}$ works.
:::
::::

::::{solution} exr-calc-limit-laws-constant-multiple
:label: sol-calc-limit-laws-constant-multiple
:class: dropdown

The function $cf$ is defined wherever $f$ is.

**If $c = 0$.** Then $c\,f(x) = 0$ wherever $f(x)$ is defined, and $cL = 0$. Let $\eps > 0$. The
definition of $\lim_{x \to a} f(x) = L$, with any tolerance, say $1$, gives a $\delta > 0$ such
that $f$ is defined at every $x$ with $0 < \abs{x - a} < \delta$; there
$\abs{c\,f(x) - cL} = 0 < \eps$.

**If $c \ne 0$.** Then $\abs{c} > 0$, by
[property 1 of the absolute value](#rem-calc-absolute-value-properties). Let $\eps > 0$. Since
$\frac{\eps}{\abs{c}} > 0$, there is a $\delta > 0$ such that $f$ is defined and
$\abs{f(x) - L} < \frac{\eps}{\abs{c}}$ at every $x$ with $0 < \abs{x - a} < \delta$. For such
$x$, by [property 4 of the absolute value](#rem-calc-absolute-value-properties), and
multiplying the last inequality by the positive number $\abs{c}$, which keeps it strict,
$$
\abs{c\,f(x) - cL} = \abs{c}\,\abs{f(x) - L} < \abs{c} \cdot \frac{\eps}{\abs{c}} = \eps .
$$
In both cases $cf$ is defined on the window, which by
[part (e) of the proposition on distance inequalities](#prop-calc-abs-interval) is an open
interval around $a$ with $a$ removed, and $\delta$ wins the round $\eps$. So
$\lim_{x \to a} c\,f(x) = cL$.
::::

::::{exercise} The limit of an absolute value
:label: exr-calc-limit-laws-absolute-value
:class: tier-c rigor

Suppose that $\lim_{x \to a} f(x) = L$. Prove that $\lim_{x \to a} \abs{f(x)} = \abs{L}$.

:::{admonition} Hint 1
:class: dropdown hint
One part of [the triangle inequality](#thm-calc-triangle-inequality) compares
$\abs{\abs{u} - \abs{v}}$ with $\abs{u - v}$.
:::

:::{admonition} Answer
:class: dropdown answer manual
The $\delta$ that works for $f$ with the tolerance $\eps$ works.
:::
::::

::::{solution} exr-calc-limit-laws-absolute-value
:label: sol-calc-limit-laws-absolute-value
:class: dropdown

The function $\abs{f}$ is defined wherever $f$ is. Let $\eps > 0$. There is a $\delta > 0$ such
that $f$ is defined and $\abs{f(x) - L} < \eps$ at every $x$ with $0 < \abs{x - a} < \delta$.
For such $x$, $\abs{f(x)}$ is defined, and by
[part (c) of the triangle inequality](#thm-calc-triangle-inequality), applied to the numbers
$f(x)$ and $L$,
$$
\abs{\abs{f(x)} - \abs{L}} \le \abs{f(x) - L} < \eps .
$$
So $\delta$ wins the round $\eps$ for $\abs{f}$, on a window that is an open interval around $a$
with $a$ removed ([part (e) of the proposition on distance
inequalities](#prop-calc-abs-interval)). Hence $\lim_{x \to a} \abs{f(x)} = \abs{L}$.
::::

## Where this leads

:::{where-this-leads}
:::

From here on, limits are computed with the laws, and the definition of a limit is needed only
to prove new laws. The next pages extend the toolkit: rewriting "$\frac{0}{0}$" forms, the
squeeze theorem, and limits at infinity.
