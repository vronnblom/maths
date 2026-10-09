---
title: The Squeeze Theorem
label: calc-squeeze-theorem
description: >-
  Trapping a function between two others that approach the same limit: the squeeze theorem,
  oscillating factors, and the proof from areas that sin x / x approaches 1, the limit on
  which the calculus of sine and cosine rests.
tags: [limits, trigonometry, proofs]
maths:
  kind: topic
  subject: calc
  status: draft
  level: core
  difficulty: 3
  est_minutes: 45
  prerequisites: [calc-limit-laws, calc-trig-functions]
  objectives:
    - Apply the squeeze theorem, including to oscillating factors.
    - Prove $\lim_{x\to0}\frac{\sin x}{x}=1$ geometrically.
    - Use it for related trigonometric limits.
  verify: verify/calculus/limits/test_squeeze_theorem.py
  widgets: [function-plot]
  reviewed_by: []
  sources: []
---

:::{topic-header}
:::

## Why this matters

How does $\sin x$ compare with $x$ when $x$ is small? A calculator set to radians gives
$\sin 0.1 \approx 0.0998334$, $\sin 0.01 \approx 0.00999983$ and
$\sin 0.001 \approx 0.000999999833$: each is almost exactly $x$. Physicists use this all the
time. For a pendulum that swings through small angles they replace $\sin\theta$ by $\theta$,
which turns an equation they cannot solve into one they can. Why does that work, and how good
is the replacement?

The precise question is about the ratio $\frac{\sin x}{x}$. Its values at the same points are

| $x$ | $0.1$ | $0.01$ | $0.001$ |
|---|---|---|---|
| $\frac{\sin x}{x}$ | $0.998334$ | $0.999983$ | $0.9999998$ |

(to the digits shown, and the same at $-0.1$, $-0.01$, $-0.001$). Does the ratio approach $1$
as $x \to 0$? The limit laws cannot tell us. At $x = 0$ the ratio is "$\frac{0}{0}$", where the
quotient law says nothing ([When the laws do not apply](#sec-calc-limit-laws-not-apply)), and
$\sin x$ is not a polynomial, so there is nothing to factor or cancel.

What we do have is a comparison. [The lemma on sine, angle and tangent](#lem-calc-sin-bounds)
says that $\sin\theta < \theta < \tan\theta$ for $0 < \theta < \frac{\pi}{2}$, and we will see
that this traps $\frac{\sin x}{x}$ between $\cos x$ and $1$. If both of these approach $1$, the
trapped function has nowhere else to go. This page makes that idea a theorem, the **squeeze
theorem**, and uses it to prove that $\frac{\sin x}{x}$ approaches $1$.

:::{admonition} Looking ahead
:class: looking-ahead
The limit of $\frac{\sin x}{x}$ is the key to the derivatives of sine and cosine, on the page
Derivatives of Trigonometric Functions. That is why its proof here may use neither
derivatives nor anything built on them, such as L'Hôpital's rule (the page Indeterminate
Forms and L'Hôpital's Rule): that would argue in a circle.
:::

## Trapping a function

Suppose that, near a point $a$, a function $f$ lies between two functions $g$ and $h$, and
that $g(x)$ and $h(x)$ both approach the same number $L$ as $x \to a$. Then $f(x)$, which is
caught between them, must approach $L$ too: the two bounds close in on $L$ and leave $f$ no
room. This works even when $f$ itself is hard to handle, as long as the bounds are easy.

Here is a function that is hard to handle. As $x$ approaches $0$, the factor $\sin(1/x)$ swings
between ${-1}$ and $1$ faster and faster, and $x \sin(1/x)$ swings with it. But the factor $x$
shrinks the swings: by [part (a) of the proposition on the bounds of sine and
cosine](#prop-calc-sin-bounded), $-1 \le \sin(1/x) \le 1$, so the values of $x\sin(1/x)$ stay
between $-\abs{x}$ and $\abs{x}$.

::::{figure}
:label: wdg-calc-squeeze-theorem-band

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "k*abs(x) + (1 - abs(k))*x*sin(1/x)",
  "xRange": [-0.5, 0.5],
  "yRange": [-0.5, 0.5],
  "parameters": { "k": { "value": 0, "min": -1, "max": 1, "step": 1 } },
  "table": { "points": [0.1, 0.01, 0.001, -0.001, -0.01, -0.1] },
  "hole": { "x": 0, "y": 0 },
  "trace": { "x": 0.25 }
}
```

Graph, for $-0.5 \le x \le 0.5$ and $x \ne 0$, of one of three functions, chosen by a slider
for $k$, which takes the values ${-1}$, $0$ and $1$ and starts at $0$. At $k = -1$ it is the
lower bound $g(x) = -\abs{x}$, at $k = 0$ the function $f(x) = x \sin(1/x)$, and at $k = 1$ the
upper bound $h(x) = \abs{x}$ (the widget plots $k\abs{x} + (1 - \abs{k})\,x\sin(1/x)$). The
graphs of $g$ and $h$ are the edges of a band shaped like a bow tie, which narrows to the
origin. The graph of $f$ swings up and down inside the band and touches its edges again and
again, faster and faster as $x$ approaches $0$; close to $0$ the drawing is a jumble of lines,
because the plotted curve joins finitely many computed points. An open circle marks the
origin, where the formula is undefined. A table lists the values at
$x = 0.1, 0.01, 0.001, -0.001, -0.01, -0.1$. For $k = 0$ they are $-0.0544021$,
$-0.00506366$, $0.00082688$, $0.00082688$, $-0.00506366$, $-0.0544021$; for $k = -1$ they are
$-\abs{x}$, and for $k = 1$ they are $\abs{x}$. At each of these six points the value of $f$
lies between those of $g$ and $h$. A second slider moves a point along the graph, starting at
$x = 0.25$, with a readout of $x$ and the value there.
::::

**Try this:** with $k = 0$, look at the table: do the values of $f$ settle as $x$ gets closer to
$0$? Now set $k = -1$ and $k = 1$ and compare the three tables row by row. How wide is the band
at $x = 0.001$, and what does that say about $f(0.001)$? Then move the traced point towards
$0$ and switch $k$ between ${-1}$, $0$ and $1$ at each position.

The table of $f$ alone looks irregular: its values change sign, and their sizes do not shrink
at a steady rate. What the widget shows, at every point it computed, is that $f$ stays inside a
band whose width $2\abs{x}$ shrinks to $0$. A picture and a table only check finitely many
points; the squeeze theorem turns the band into a proof that $x\sin(1/x)$ approaches $0$
([](#eg-calc-squeeze-theorem-oscillating)).

## Main results

### The squeeze theorem

:::{proof:theorem} Squeeze theorem
:label: thm-calc-squeeze

Let $a$ and $L$ be real numbers, let $r > 0$, and let $f$, $g$ and $h$ be functions that are
defined at every $x$ with $0 < \abs{x - a} < r$, such that, for every such $x$,
$$
g(x) \le f(x) \le h(x) .
$$
If $\lim_{x \to a} g(x) = L$ and $\lim_{x \to a} h(x) = L$, then $\lim_{x \to a} f(x) = L$.
:::

:::{proof:proof} Rigorous track
:label: prf-calc-squeeze
:enumerated: false
:class: dropdown
We play the ε–δ game of [the definition of a limit](#def-calc-limit) for $g$ and $h$ with the
same tolerance $\eps$: near $a$, both $g(x)$ and $h(x)$ lie strictly between $L - \eps$ and
$L + \eps$, and $f(x)$, caught between them, lies there too.

Let $\eps > 0$. Since $\lim_{x \to a} g(x) = L$, there is a $\delta_1 > 0$ such that $g$ is
defined and $\abs{g(x) - L} < \eps$ at every $x$ with $0 < \abs{x - a} < \delta_1$. Since
$\lim_{x \to a} h(x) = L$, there is a $\delta_2 > 0$ such that $h$ is defined and
$\abs{h(x) - L} < \eps$ at every $x$ with $0 < \abs{x - a} < \delta_2$.

Let $\delta = \min(\delta_1, \delta_2, r)$, which is positive, and let
$0 < \abs{x - a} < \delta$. Since $\delta$ is at most each of $\delta_1$, $\delta_2$ and $r$,
also $\abs{x - a} < \delta_1$, $\abs{x - a} < \delta_2$ and $\abs{x - a} < r$
([property 2 of the order rules](#rem-calc-order-rules), transitivity). So $x$ lies in both
windows and in the punctured interval of the hypothesis: $f(x)$, $g(x)$ and $h(x)$ are
defined, $g(x) \le f(x) \le h(x)$, $\abs{g(x) - L} < \eps$ and $\abs{h(x) - L} < \eps$. By
[part (a) of the proposition on distance inequalities](#prop-calc-abs-interval), applied to
the number $g(x)$ with centre $L$ and radius $\eps$, the inequality $\abs{g(x) - L} < \eps$
says $L - \eps < g(x) < L + \eps$; in the same way, $L - \eps < h(x) < L + \eps$. Hence
$$
L - \eps < g(x) \le f(x) \le h(x) < L + \eps .
$$
By transitivity (property 2 of the order rules: $u < v \le w$ implies $u < w$, and
$u \le v < w$ implies $u < w$), $L - \eps < f(x)$ and $f(x) < L + \eps$. By part (a) of the
proposition on distance inequalities again, this says $\abs{f(x) - L} < \eps$.

So $f$ is defined at every $x$ with $0 < \abs{x - a} < r$, which by [part (e) of the
proposition on distance inequalities](#prop-calc-abs-interval) is the open interval
$(a - r, a + r)$ with $a$ removed; the definition of a limit applies to $f$, and $\delta$ wins
the round $\eps$. Since $\eps > 0$ was arbitrary, $\lim_{x \to a} f(x) = L$.
:::

**In words.** If, near $a$ (but not necessarily at $a$), $f$ lies between a lower bound $g$ and
an upper bound $h$ that approach the *same* number $L$, then $f$ approaches $L$ too. The bounds
need to hold only on some punctured interval around $a$, however small, and they say nothing
about $f(a)$, which may be undefined. The theorem is also called the *sandwich theorem* or the
*pinching theorem*.

**Example.** Let $f(x) = x\abs{x}$. By [the definition of the absolute
value](#def-calc-absolute-value), $f(x) = x^2$ for $x \ge 0$ and $f(x) = -x^2$ for $x < 0$. Since
$x^2 \ge 0$, also $-x^2 \le 0 \le x^2$, so in both cases
$$
-x^2 \le f(x) \le x^2
$$
for every real $x$. The bounds are polynomials, so by [direct
substitution](#cor-calc-direct-substitution) both approach $0$ as $x \to 0$, and the theorem
(with any $r$, say $r = 1$) gives $\lim_{x \to 0} x\abs{x} = 0$. The function $f$ is given by
two formulas, and the bounds are single polynomials: the theorem is useful exactly when $f$ is
the hard part and the bounds are easy.

**Non-example.** For $x \ne 0$, $-1 \le \sin(1/x) \le 1$, but the bounds ${-1}$ and $1$
approach *different* numbers, so the theorem says nothing about $\lim_{x \to 0} \sin(1/x)$. In
fact that limit does not exist: the bounds leave room for the values to swing between them.

The hypotheses are all needed: [](#rem-calc-squeeze-theorem-hypotheses) gives a counterexample
for each. First, a form of the theorem that is often quicker to use. Most squeezes bound the
*distance* from $f(x)$ to $L$.

:::{proof:remark} Squeezing the distance
:label: rem-calc-squeeze-theorem-distance

Let $a$ and $L$ be real numbers, let $r > 0$, and let $f$ and $b$ be functions that are defined
at every $x$ with $0 < \abs{x - a} < r$, such that $\abs{f(x) - L} \le b(x)$ for every such
$x$. If $\lim_{x \to a} b(x) = 0$, then $\lim_{x \to a} f(x) = L$.

*Reason.* Let $0 < \abs{x - a} < r$. By [part (b) of the proposition on distance
inequalities](#prop-calc-abs-interval), applied to the number $f(x)$ with centre $L$ and radius
$b(x)$, the inequality $\abs{f(x) - L} \le b(x)$ says
$$
L - b(x) \le f(x) \le L + b(x) .
$$
By [part (a) of the limit laws](#thm-calc-limit-laws), $\lim_{x \to a} L = L$, and $b$ is
defined on the open interval $(a - r, a + r)$ except possibly at $a$, so the difference and
sum laws, part (b), give $\lim_{x \to a} \bigl(L - b(x)\bigr) = L - 0 = L$ and
$\lim_{x \to a} \bigl(L + b(x)\bigr) = L + 0 = L$. Both are defined wherever $b$ is. The
[squeeze theorem](#thm-calc-squeeze), with $g(x) = L - b(x)$ and $h(x) = L + b(x)$, gives
$\lim_{x \to a} f(x) = L$.
:::

With $g = h$, the squeeze theorem also says that two functions that are *equal* on a punctured
interval around $a$ have the same limit at $a$: if $f(x) = g(x)$ for every $x$ with
$0 < \abs{x - a} < r$, then $g(x) \le f(x) \le g(x)$ there, and $\lim_{x \to a} g(x) = L$ gives
$\lim_{x \to a} f(x) = L$. We use this when two formulas agree near $a$ but not everywhere.

:::{proof:remark} Each hypothesis is needed
:label: rem-calc-squeeze-theorem-hypotheses

The three counterexamples use one function: $s(x) = \dfrac{\abs{x}}{x}$ for $x \ne 0$. By
[the definition of the absolute value](#def-calc-absolute-value), $\abs{x} = x$ for $x > 0$ and
$\abs{x} = -x$ for $x < 0$, so $s(x) = 1$ for $x > 0$ and $s(x) = -1$ for $x < 0$.

**$s$ has no limit at $0$.** Let $L$ be any real number, and suppose that some $\delta > 0$
wins the round $\eps = 1$ of [the definition of a limit](#def-calc-limit). The points
$x = \frac{\delta}{2}$ and $x = -\frac{\delta}{2}$ satisfy $0 < \abs{x} = \frac{\delta}{2} < \delta$,
so they lie in the window, and $\abs{1 - L} < 1$ and $\abs{-1 - L} < 1$. Also
$\abs{L - (-1)} = \abs{-1 - L}$, by [property 2 of the absolute
value](#rem-calc-absolute-value-properties). By [part (b) of the triangle
inequality](#thm-calc-triangle-inequality), with $x = 1$, $y = -1$ and $z = L$,
$$
2 = \abs{1 - (-1)} \le \abs{1 - L} + \abs{L - (-1)} < 1 + 1 = 2,
$$
which is impossible. So no $\delta$ wins the round $\eps = 1$, and $L$ is not the limit. Since
$L$ was arbitrary, $s$ has no limit at $0$.

1. **The bounds must approach the same number.** Let $g(x) = -1$ and $h(x) = 1$. Then
   $g(x) \le s(x) \le h(x)$ for every $x \ne 0$, $\lim_{x \to 0} g(x) = -1$ and
   $\lim_{x \to 0} h(x) = 1$, by [part (a) of the limit laws](#thm-calc-limit-laws), and $s$
   has no limit at $0$. Bounds with different limits leave room between them.
2. **The inequalities must hold on both sides of $a$.** Let $g(x) = h(x) = 1$. Then
   $g(x) \le s(x) \le h(x)$ holds for every $x > 0$, but for no $x < 0$, where $s(x) = -1 < 1$.
   Both bounds have the limit $1$, and $s$ has no limit at $0$. The theorem needs the
   inequalities at every point of a punctured interval $0 < \abs{x - a} < r$, which reaches
   both sides of $a$.
3. **One bound is not enough.** Let $g(x) = -1$. Then $g(x) \le s(x)$ for every $x \ne 0$ and
   $\lim_{x \to 0} g(x) = -1$, but $s$ has no limit at $0$: a lower bound alone does not stop
   $f$ from moving up and down above it. In the same way, the upper bound $h(x) = 1$ alone is
   not enough.

What the theorem does *not* need: the inequalities at $a$ itself, a value $f(a)$, or strict
inequalities. And its conclusion is no stronger than its hypotheses: if $g(x) < f(x) < h(x)$,
the limit is still only $L$, with no strict inequality left.
:::

### Sine and cosine near 0

To use the squeeze theorem for $\frac{\sin x}{x}$, we need bounds for $\sin x$ and $\cos x$
near $0$, and their limits there. Everything rests on [the lemma on sine, angle and
tangent](#lem-calc-sin-bounds) of Trigonometric Functions, which compares areas and uses no
limits, and on the properties of $\sin$ and $\cos$ proved on that page. The lemma is about
$0 < \theta < \frac{\pi}{2}$ only. For negative numbers we use the symmetries of
[property 4 of the point $P(t)$](#rem-calc-trig-functions-circle-properties):
$\cos(-t) = \cos t$ and $\sin(-t) = -\sin t$.

:::{proof:lemma} Sine and cosine near 0
:label: lem-calc-sin-cos-near-zero

For every real number $x$ with $0 < \abs{x} < \frac{\pi}{2}$:

(a) $\abs{\sin x} < \abs{x}$;

(b) $1 - \dfrac{x^2}{2} < \cos x < 1$;

(c) $\cos x < \dfrac{\sin x}{x} < 1$.
:::

:::{proof:proof}
:enumerated: false
We reduce a negative $x$ to the positive number $t = \abs{x}$ with the symmetries of sine and
cosine, apply [the lemma on sine, angle and tangent](#lem-calc-sin-bounds) to $t$, and get (b)
from (a) with the double-angle formula for the cosine.

**Step 1: from $x$ to $t = \abs{x}$.** Let $y$ be a real number with
$0 < \abs{y} < \frac{\pi}{2}$, and let $t = \abs{y}$, so that $0 < t < \frac{\pi}{2}$. By
[the definition of the absolute value](#def-calc-absolute-value), $y = t$ if $y > 0$, and
$y = -t$ if $y < 0$. In the second case, by [property 4 of the point
$P(t)$](#rem-calc-trig-functions-circle-properties), $\sin y = \sin(-t) = -\sin t$ and
$\cos y = \cos(-t) = \cos t$, and so $\frac{\sin y}{y} = \frac{-\sin t}{-t} = \frac{\sin t}{t}$.
So in both cases
$$
\cos y = \cos t \quad\text{and}\quad \frac{\sin y}{y} = \frac{\sin t}{t},
$$
and $\sin y$ is $\sin t$ or $-\sin t$. By [property 8 of the point
$P(t)$](#rem-calc-trig-functions-circle-properties), $\sin t > 0$ and $\cos t > 0$, since
$0 < t < \frac{\pi}{2}$. So $\abs{\sin y} = \abs{\sin t} = \sin t > 0$, by [property 2 of the
absolute value](#rem-calc-absolute-value-properties) and the definition of the absolute value.

Now let $0 < \abs{x} < \frac{\pi}{2}$, and apply step 1 with $y = x$ and $t = \abs{x}$. By
[the lemma on sine, angle and tangent](#lem-calc-sin-bounds),
$$
\sin t < t < \tan t .
$$

**(a)** $\abs{\sin x} = \sin t < t = \abs{x}$.

**(c)** The number $\frac{1}{t}$ is positive, because $t > 0$ ([property 6 of the order
rules](#rem-calc-order-rules)). Multiplying $\sin t < t$ by it keeps the strict inequality
([property 5(a) of the order rules](#rem-calc-order-rules)) and gives $\frac{\sin t}{t} < 1$.
Next, $\cos t \ne 0$, so $\tan t = \frac{\sin t}{\cos t}$, by [the definition of the
tangent](#def-calc-tan-sec-csc-cot). The number $\frac{\cos t}{t}$ is positive: multiplying
$0 < \cos t$ by the positive number $\frac{1}{t}$ keeps the inequality (property 5(a)).
Multiplying $t < \frac{\sin t}{\cos t}$ by $\frac{\cos t}{t}$ keeps the strict inequality
(property 5(a)) and gives $\cos t < \frac{\sin t}{t}$. By step 1,
$$
\cos x = \cos t < \frac{\sin t}{t} = \frac{\sin x}{x} < 1 .
$$

**(b)** Let $s = \frac{x}{2}$, so that $x = 2s$. By [property 4 of the absolute
value](#rem-calc-absolute-value-properties), $\abs{s} = \frac{\abs{x}}{2}$, and multiplying
$0 < \abs{x} < \frac{\pi}{2}$ by the positive number $\frac12$ (property 5(a) of the order
rules) gives $0 < \abs{s} < \frac{\pi}{4}$; and $\frac{\pi}{4} < \frac{\pi}{2}$. So $s$ satisfies
the hypothesis of the lemma, and (a), applied to $s$, gives $\abs{\sin s} < \abs{s}$. Both sides
are non-negative ([property 1 of the absolute value](#rem-calc-absolute-value-properties)), so
squaring keeps the strict inequality ([property 6 of the absolute
value](#rem-calc-absolute-value-properties)), and by property 5 of the absolute value,
$\abs{y}^2 = y^2$:
$$
\sin^2 s = \abs{\sin s}^2 < \abs{s}^2 = s^2 = \frac{x^2}{4} .
$$
Multiplying by the positive number $2$ keeps it (property 5(a) of the order rules):
$2\sin^2 s < \frac{x^2}{2}$. By [part (f) of the addition formulas](#thm-calc-addition-formulas),
with $t = s$,
$$
\cos x = \cos 2s = 1 - 2\sin^2 s .
$$
Adding $1 - 2\sin^2 s - \frac{x^2}{2}$ to both sides of $2\sin^2 s < \frac{x^2}{2}$ keeps it
([property 3 of the order rules](#rem-calc-order-rules)) and gives
$1 - \frac{x^2}{2} < 1 - 2\sin^2 s = \cos x$. For the other inequality, step 1 with $y = s$
gives $\abs{\sin s} > 0$; multiplying $0 < \abs{\sin s}$ by the positive number $\abs{\sin s}$
(property 5(a)) gives $0 < \abs{\sin s}^2 = \sin^2 s$, and multiplying by $2$ gives
$0 < 2\sin^2 s$. Adding $1 - 2\sin^2 s$ to both sides (property 3) gives
$\cos x = 1 - 2\sin^2 s < 1$.
:::

The inequalities of the lemma are what the squeeze theorem needs. With them we get the limits
of $\sin$ and $\cos$ at $0$, without knowing that $\sin$ and $\cos$ are continuous.

:::{proof:lemma} Limits at 0
:label: lem-calc-sin-cos-limits-at-zero

(a) $\displaystyle \lim_{x \to 0} \abs{x} = 0$;

(b) $\displaystyle \lim_{x \to 0} \sin x = 0$;

(c) $\displaystyle \lim_{x \to 0} \cos x = 1$.
:::

:::{proof:proof}
:enumerated: false
We prove (a) from the definition, and then squeeze $\sin x$ and $\cos x$ with the bounds of
[](#lem-calc-sin-cos-near-zero).

**(a)** The function $\abs{x}$ is defined for every real $x$. Let $\eps > 0$ and take
$\delta = \eps$. For every real $x$, $\abs{x} \ge 0$ ([property 1 of the absolute
value](#rem-calc-absolute-value-properties)), so
$\bigl\lvert \abs{x} - 0 \bigr\rvert = \bigl\lvert \abs{x} \bigr\rvert = \abs{x}$, by
[the definition of the absolute value](#def-calc-absolute-value). So if
$0 < \abs{x - 0} < \delta$, then $\bigl\lvert \abs{x} - 0 \bigr\rvert = \abs{x} < \eps$. Hence
$\lim_{x \to 0} \abs{x} = 0$.

**(b)** The functions $\sin x$ and $\abs{x}$ are defined for every real $x$. For every $x$ with
$0 < \abs{x} < \frac{\pi}{2}$, [part (a) of the lemma](#lem-calc-sin-cos-near-zero) gives
$\abs{\sin x - 0} = \abs{\sin x} < \abs{x}$, so in particular $\abs{\sin x - 0} \le \abs{x}$. By
(a), $\lim_{x \to 0} \abs{x} = 0$. So [](#rem-calc-squeeze-theorem-distance), with $a = 0$,
$L = 0$, $r = \frac{\pi}{2}$, $f(x) = \sin x$ and $b(x) = \abs{x}$, gives
$\lim_{x \to 0} \sin x = 0$.

**(c)** For every $x$ with $0 < \abs{x} < \frac{\pi}{2}$, [part (b) of the
lemma](#lem-calc-sin-cos-near-zero) gives
$$
1 - \frac{x^2}{2} \le \cos x \le 1 .
$$
The lower bound is a polynomial, so by [direct substitution](#cor-calc-direct-substitution),
part (a), $\lim_{x \to 0} \bigl(1 - \frac{x^2}{2}\bigr) = 1 - \frac{0^2}{2} = 1$. The upper bound
is the constant $1$, and $\lim_{x \to 0} 1 = 1$ by [part (a) of the limit
laws](#thm-calc-limit-laws). All three functions are defined for every real $x$. The
[squeeze theorem](#thm-calc-squeeze), with $a = 0$, $L = 1$, $r = \frac{\pi}{2}$,
$g(x) = 1 - \frac{x^2}{2}$, $f(x) = \cos x$ and $h(x) = 1$, gives $\lim_{x \to 0} \cos x = 1$.
:::

So the limits of $\sin$ and $\cos$ at $0$ are their values there, $\sin 0 = 0$ and
$\cos 0 = 1$. That is no surprise, but it needed a proof: neither function is a polynomial, so
[direct substitution](#cor-calc-direct-substitution) does not apply to them.

:::{admonition} Looking ahead
:class: looking-ahead
With the addition formulas, these two limits at $0$ give the limits of $\sin$ and $\cos$ at
every point, that is, their continuity: the page Continuity of Elementary Functions proves it
that way. So continuity cannot be used here: it comes *from* this page.
:::

### The limit of sine x over x

:::{proof:theorem} The limit of $\frac{\sin x}{x}$ at $0$
:label: thm-calc-sin-x-over-x

With $x$ in radians,
$$
\lim_{x \to 0} \frac{\sin x}{x} = 1 .
$$
:::

:::{proof:proof}
:enumerated: false
We squeeze $\frac{\sin x}{x}$ between $\cos x$ and $1$, which both approach $1$; the bounds
come from comparing areas, through [the lemma on sine, angle and
tangent](#lem-calc-sin-bounds), and use no derivatives and no continuity of $\sin$ or $\cos$.

The function $\frac{\sin x}{x}$ is defined at every $x \ne 0$, and $\cos x$ and the constant $1$
at every real $x$. For every $x$ with $0 < \abs{x} < \frac{\pi}{2}$, [part (c) of
the lemma on sine and cosine near 0](#lem-calc-sin-cos-near-zero) gives
$\cos x < \frac{\sin x}{x} < 1$, and so
$$
\cos x \le \frac{\sin x}{x} \le 1 .
$$
By [part (c) of the lemma on limits at 0](#lem-calc-sin-cos-limits-at-zero),
$\lim_{x \to 0} \cos x = 1$, and $\lim_{x \to 0} 1 = 1$ by [part (a) of the limit
laws](#thm-calc-limit-laws). The [squeeze theorem](#thm-calc-squeeze), with $a = 0$, $L = 1$,
$r = \frac{\pi}{2}$, $g(x) = \cos x$, $f(x) = \frac{\sin x}{x}$ and $h(x) = 1$, gives
$\lim_{x \to 0} \frac{\sin x}{x} = 1$.
:::

The chain of reasoning, from the start: areas of a triangle, a sector and a larger triangle
give $\sin\theta < \theta < \tan\theta$ ([](#lem-calc-sin-bounds)); dividing by $\theta$ and
using the symmetries of $\sin$ and $\cos$ traps $\frac{\sin x}{x}$ between $\cos x$ and $1$
([](#lem-calc-sin-cos-near-zero)); the double-angle formula squeezes $\cos x$ to $1$
([](#lem-calc-sin-cos-limits-at-zero)); and the squeeze theorem finishes. No step uses a
derivative, a series, or the continuity of $\sin$ or $\cos$.

**Why radians.** The lemma compares $\sin\theta$ with $\theta$, the *length* of an arc of the
unit circle, and that length is the measure of the angle in radians ([](#def-calc-radian)). In
degrees the ratio does not approach $1$: an angle of $x$ degrees is $\frac{\pi x}{180}$ radians,
and at $x = 0.01$ the ratio $\sin\bigl(\frac{\pi \cdot 0.01}{180}\bigr) / 0.01$ is about
$0.0174533$, close to $\frac{\pi}{180} \approx 0.0174533$ rather than to $1$.

### A related limit

:::{proof:corollary} The limit of $\frac{1 - \cos x}{x}$ at $0$
:label: cor-calc-one-minus-cos-over-x

This follows from [](#thm-calc-sin-x-over-x). With $x$ in radians,
$$
\lim_{x \to 0} \frac{1 - \cos x}{x} = 0 .
$$
:::

:::{proof:proof}
:enumerated: false
We multiply numerator and denominator by $1 + \cos x$, which turns $1 - \cos x$ into
$\sin^2 x$, write the result as a product of $\frac{\sin x}{x}$ and a quotient, and apply the
limit laws.

**Rewriting.** Let $0 < \abs{x} < \frac{\pi}{2}$. Then $\cos x = \cos\abs{x}$: for $x > 0$
because $\abs{x} = x$, and for $x < 0$ because $\abs{x} = -x$ and $\cos(-x) = \cos x$, by
[property 4 of the point $P(t)$](#rem-calc-trig-functions-circle-properties). Since
$0 < \abs{x} < \frac{\pi}{2}$, property 8 gives $\cos\abs{x} > 0$. So $\cos x > 0$,
$1 + \cos x > 1 > 0$ ([property 3 of the order rules](#rem-calc-order-rules)) and
$1 + \cos x \ne 0$. Multiplying numerator and denominator by $1 + \cos x$, and using
[the Pythagorean identity](#thm-calc-pythagorean-identity), $1 - \cos^2 x = \sin^2 x$,
$$
\begin{aligned}
\frac{1 - \cos x}{x}
  &= \frac{(1 - \cos x)(1 + \cos x)}{x\,(1 + \cos x)} = \frac{\sin^2 x}{x\,(1 + \cos x)} \\
  &= \frac{\sin x}{x} \cdot \frac{\sin x}{1 + \cos x} .
\end{aligned}
$$
Call the last product $F(x)$. It is defined at every $x$ with $0 < \abs{x} < \frac{\pi}{2}$,
and equal to $\frac{1 - \cos x}{x}$ there.

**The limits of the parts.** By [the lemma on limits at 0](#lem-calc-sin-cos-limits-at-zero),
$\lim_{x \to 0} \sin x = 0$ and $\lim_{x \to 0} \cos x = 1$; with
$\lim_{x \to 0} 1 = 1$ ([part (a) of the limit laws](#thm-calc-limit-laws)), the sum law,
part (b), gives $\lim_{x \to 0} (1 + \cos x) = 2$. These functions are defined for every real
$x$. Since $2 \ne 0$, the quotient law, [part (d) of the limit laws](#thm-calc-limit-laws),
applies with $f(x) = \sin x$, $g(x) = 1 + \cos x$, $L = 0$ and $M = 2$, and gives
$$
\lim_{x \to 0} \frac{\sin x}{1 + \cos x} = \frac{0}{2} = 0 ,
$$
and it says that this quotient is defined on an open interval around $0$. By
[](#thm-calc-sin-x-over-x), $\lim_{x \to 0} \frac{\sin x}{x} = 1$, and $\frac{\sin x}{x}$ is
defined at every $x \ne 0$. So the product law, [part (c) of the limit
laws](#thm-calc-limit-laws), gives $\lim_{x \to 0} F(x) = 1 \cdot 0 = 0$.

**Back to the original function.** $\frac{1 - \cos x}{x}$ is defined at every $x \ne 0$, and
for $0 < \abs{x} < \frac{\pi}{2}$ it equals $F(x)$, so $F(x) \le \frac{1 - \cos x}{x} \le F(x)$
there. The [squeeze theorem](#thm-calc-squeeze), with $g = h = F$, $L = 0$ and
$r = \frac{\pi}{2}$, gives $\lim_{x \to 0} \frac{1 - \cos x}{x} = 0$.
:::

The only law used with a quotient was the quotient law with $M = 2$. The original quotient
$\frac{1 - \cos x}{x}$ has $M = 0$ in its denominator, so the quotient law cannot be applied to
it directly; the rewriting moves the "$\frac{0}{0}$" into $\frac{\sin x}{x}$, whose limit we
know.

:::{admonition} Looking ahead
:class: looking-ahead
[](#thm-calc-sin-x-over-x) and [](#cor-calc-one-minus-cos-over-x) are exactly the two limits
that the page Derivatives of Trigonometric Functions needs to find the derivatives of $\sin$
and $\cos$ from the definition of the derivative and the addition formulas.
:::

## Worked examples

:::{proof:example} An oscillating factor: $\lim_{x \to 0} x \sin(1/x)$
:label: eg-calc-squeeze-theorem-oscillating

Find $\displaystyle \lim_{x \to 0} x\sin\Bigl(\frac{1}{x}\Bigr)$, the function of
[the squeeze-band figure](#wdg-calc-squeeze-theorem-band).

1. **Why the laws fail.** The product law would need a limit of $\sin(1/x)$ at $0$, and the
   bound $-1 \le \sin(1/x) \le 1$ gives none. We bound the distance to the guess $0$ instead.
2. **The bound.** Let $x \ne 0$. By [part (a) of the proposition on the bounds of sine and
   cosine](#prop-calc-sin-bounded), with $t = \frac{1}{x}$, $-1 \le \sin(1/x) \le 1$, which by
   [part (b) of the proposition on distance inequalities](#prop-calc-abs-interval) (centre
   $0$, radius $1$) says $\abs{\sin(1/x)} \le 1$. By [property 4 of the absolute
   value](#rem-calc-absolute-value-properties), and multiplying $\abs{\sin(1/x)} \le 1$ by the
   number $\abs{x} \ge 0$, which gives only $\le$ ([property 5(b) of the order
   rules](#rem-calc-order-rules)),
   $$
   \Bigl\lvert x\sin\Bigl(\frac{1}{x}\Bigr) - 0\Bigr\rvert
   = \abs{x}\,\Bigl\lvert\sin\Bigl(\frac{1}{x}\Bigr)\Bigr\rvert \le \abs{x} .
   $$
3. **Squeeze.** Both $x\sin(1/x)$ and $\abs{x}$ are defined at every $x \ne 0$, and
   $\lim_{x \to 0} \abs{x} = 0$ by [part (a) of the lemma on limits at
   0](#lem-calc-sin-cos-limits-at-zero). By [](#rem-calc-squeeze-theorem-distance), with
   $a = 0$, $L = 0$, $r = 1$ and $b(x) = \abs{x}$, the limit is $0$.

$$
\boxed{\lim_{x \to 0} x\sin\Bigl(\frac{1}{x}\Bigr) = 0}
$$

**Check.** The table of the figure, at $k = 0$: $\abs{-0.0544021} \le 0.1$,
$\abs{-0.00506366} \le 0.01$ and $0.00082688 \le 0.001$. ✓ At $x = \frac{1}{\pi}$, where
$\sin(1/x) = \sin\pi = 0$, the value is $0$; at $x = \frac{2}{\pi}$, where
$\sin\frac{\pi}{2} = 1$, the value is $\frac{2}{\pi}$, on the upper edge of the band: the bound
cannot be improved in general. ✓
:::

:::{proof:example} A related trigonometric limit: $\lim_{x \to 0} \frac{\sin 3x}{x}$
:label: eg-calc-squeeze-theorem-sin-3x

Find $\displaystyle \lim_{x \to 0} \frac{\sin 3x}{x}$.

1. **Strategy.** Substituting $x = 0$ gives "$\frac{0}{0}$". The argument of the sine is $3x$,
   not $x$, so [](#thm-calc-sin-x-over-x) does not apply as it stands. We write $\sin 3x$ in
   terms of $\sin x$ and $\cos x$ with the addition formulas, so that $\frac{\sin x}{x}$
   appears.
2. **Rewrite $\sin 3x$.** For every real $x$, by [parts (c), (e) and (f) of the addition
   formulas](#thm-calc-addition-formulas), with $s = 2x$ and $t = x$ in (c), and then
   [the Pythagorean identity](#thm-calc-pythagorean-identity), $\cos^2 x = 1 - \sin^2 x$:
   $$
   \begin{aligned}
   \sin 3x &= \sin 2x \cos x + \cos 2x \sin x \\
     &= 2\sin x \cos^2 x + (1 - 2\sin^2 x)\sin x \\
     &= 2\sin x\,(1 - \sin^2 x) + \sin x - 2\sin^3 x \\
     &= 3\sin x - 4\sin^3 x .
   \end{aligned}
   $$
3. **Divide by $x$.** For every $x \ne 0$,
   $$
   \frac{\sin 3x}{x} = \frac{\sin x}{x}\,\bigl(3 - 4\sin^2 x\bigr) .
   $$
   Both sides are defined at exactly the $x \ne 0$, so they are the same function.
4. **The limits of the factors.** By [](#thm-calc-sin-x-over-x), the first factor approaches
   $1$. By [part (b) of the lemma on limits at 0](#lem-calc-sin-cos-limits-at-zero),
   $\lim_{x \to 0} \sin x = 0$, so the power law, [part (e) of the limit
   laws](#thm-calc-limit-laws) with $n = 2$, gives $\lim_{x \to 0} \sin^2 x = 0$; the "in
   particular" of part (c), with $c = 4$, gives $\lim_{x \to 0} 4\sin^2 x = 0$; and part (a)
   and the difference law, part (b), give $\lim_{x \to 0} (3 - 4\sin^2 x) = 3 - 0 = 3$. All
   these functions are defined for every real $x$.
5. **Combine.** By the product law, part (c),
   $\lim_{x \to 0} \frac{\sin 3x}{x} = 1 \cdot 3 = 3$.

$$
\boxed{\lim_{x \to 0} \frac{\sin 3x}{x} = 3}
$$

**Check.** At $x = 0.01$: $\frac{\sin 0.03}{0.01} \approx 2.99955$, close to $3$. ✓ The
identity of step 2 at $x = \frac{\pi}{2}$: $\sin\frac{3\pi}{2} = -1$, and
$3\sin\frac{\pi}{2} - 4\sin^3\frac{\pi}{2} = 3 - 4 = -1$. ✓
:::

:::{proof:example} How small is a small angle?
:label: eg-calc-squeeze-theorem-small-angle

A model of a pendulum replaces $\sin\theta$ by $\theta$, where $\theta$ is the angle of the
pendulum from the vertical, in radians. The *relative error* of this replacement is
$\frac{\theta - \sin\theta}{\theta} = 1 - \frac{\sin\theta}{\theta}$, for $\theta \ne 0$. For
which angles do the bounds on this page guarantee a relative error below $1\,\%$, that is,
below $0.01$?

1. **A bound for the error.** Let $0 < \abs{\theta} < \frac{\pi}{2}$. By [parts (b) and (c) of
   the lemma on sine and cosine near 0](#lem-calc-sin-cos-near-zero),
   $$
   1 - \frac{\theta^2}{2} < \cos\theta < \frac{\sin\theta}{\theta} < 1 .
   $$
   By transitivity ([property 2 of the order rules](#rem-calc-order-rules)),
   $1 - \frac{\theta^2}{2} < \frac{\sin\theta}{\theta} < 1$. Adding
   $\frac{\theta^2}{2} - \frac{\sin\theta}{\theta}$ to the first inequality and
   $-\frac{\sin\theta}{\theta}$ to the second keeps them ([property 3 of the order
   rules](#rem-calc-order-rules)):
   $$
   0 < 1 - \frac{\sin\theta}{\theta} < \frac{\theta^2}{2} .
   $$
   So the replacement always overestimates, by a relative error less than $\frac{\theta^2}{2}$.
2. **When is the bound at most $0.01$?** $\frac{\theta^2}{2} \le 0.01$ exactly when
   $\theta^2 \le 0.02$ (multiplying by the positive number $2$, or by $\frac12$, keeps
   inequalities, [property 5(b) of the order rules](#rem-calc-order-rules)). By [property 5 of
   the absolute value](#rem-calc-absolute-value-properties), $\theta^2 = \abs{\theta}^2$, and
   $0.02 = \bigl(\sqrt{0.02}\bigr)^2$ ([the square-root remark](#rem-calc-square-roots)). Both
   $\abs{\theta}$ and $\sqrt{0.02}$ are non-negative, so by [property 6 of the absolute
   value](#rem-calc-absolute-value-properties) this holds exactly when
   $\abs{\theta} \le \sqrt{0.02} \approx 0.141421$.
3. **Conclusion.** Since $\sqrt{0.02} \approx 0.141$ is less than $\frac{\pi}{2} \approx 1.571$,
   step 1 applies to every $\theta$ with $0 < \abs{\theta} \le \sqrt{0.02}$, and then
   $1 - \frac{\sin\theta}{\theta} < \frac{\theta^2}{2} \le 0.01$ (transitivity). In degrees,
   $\sqrt{0.02}$ radians is $\frac{180\sqrt{0.02}}{\pi} \approx 8.10$ degrees, since a full turn
   is $2\pi$ radians ([](#def-calc-radian)) and $360$ degrees.

$$
\boxed{\abs{\theta} \le \sqrt{0.02} \approx 0.141}
$$

in radians, about $8.1$ degrees: for such angles, replacing $\sin\theta$ by $\theta$ makes a
relative error of less than $1\,\%$.

**Check.** At $\theta = 0.14$: $\sin 0.14 \approx 0.139543$, so
$1 - \frac{\sin 0.14}{0.14} \approx 0.00326$, less than $\frac{0.14^2}{2} = 0.0098$, which is
less than $0.01$. ✓ Units: the angle is in radians, the relative error has no unit. ✓ The bound
is not sharp: at $\theta = \sqrt{0.02}$ the relative error is about $0.00333$, a third of
$0.01$. The bounds guarantee $1\,\%$; they do not say where the error reaches it.
:::

:::{admonition} Looking ahead
:class: looking-ahead
The page Taylor Polynomials and Taylor's Theorem shows that the relative error
$1 - \frac{\sin\theta}{\theta}$ is close to $\frac{\theta^2}{6}$ for small $\theta$, a third of
the bound found here, which explains the factor in the last check.
:::

## Common mistakes

:::{warning} Using the product law with a bounded factor
✗ **Wrong:** "$\lim_{x \to 0} x\sin(1/x) = \lim_{x \to 0} x \cdot \lim_{x \to 0} \sin(1/x)
= 0$, because $\lim_{x \to 0} x = 0$ and $\sin(1/x)$ is between ${-1}$ and $1$."

**Why:** the product law, [part (c) of the limit laws](#thm-calc-limit-laws), needs both
factors to have limits, as real numbers. "Between ${-1}$ and $1$" is a bound, not a limit, and
$\sin(1/x)$ has no limit at $0$ (the page The Limit of a Function shows this). So
$\lim_{x \to 0} \sin(1/x)$ cannot be written down at all.

✓ **Right:** squeeze. Since $\bigl\lvert x\sin(1/x)\bigr\rvert \le \abs{x}$ for $x \ne 0$, and
$\abs{x} \to 0$, the limit is $0$ ([](#eg-calc-squeeze-theorem-oscillating)). The bound is
used, but through the squeeze theorem, not the product law.
:::

:::{warning} Squeezing between bounds with different limits
✗ **Wrong:** "$-1 \le \sin(1/x) \le 1$ for $x \ne 0$, so by the squeeze theorem
$\lim_{x \to 0} \sin(1/x)$ exists and lies between ${-1}$ and $1$."

**Why:** the [squeeze theorem](#thm-calc-squeeze) needs both bounds to approach the *same*
number $L$. Bounds with different limits leave room for $f$ to move between them, and $f$ need
not have a limit at all ([](#rem-calc-squeeze-theorem-hypotheses), counterexample 1).

✓ **Right:** first find bounds that close in on one number, as $-\abs{x}$ and $\abs{x}$ do for
$x\sin(1/x)$. If no such bounds exist, the squeeze theorem is the wrong tool.
:::

:::{warning} "$\frac{\sin(\text{anything})}{\text{anything}}$" with two different anythings
✗ **Wrong:** "$\displaystyle \lim_{x \to 0} \frac{\sin 3x}{x} = 1$, by the limit of
$\frac{\sin x}{x}$."

**Why:** [](#thm-calc-sin-x-over-x) is about $\frac{\sin x}{x}$, with the same $x$ in the
sine and in the denominator. In $\frac{\sin 3x}{x}$ they differ, and the values tell: at
$x = 0.01$ the quotient is about $2.99955$, not close to $1$.

✓ **Right:** rewrite until $\frac{\sin x}{x}$ appears, then use the limit laws:
$\frac{\sin 3x}{x} = \frac{\sin x}{x}\,(3 - 4\sin^2 x) \to 1 \cdot 3 = 3$
([](#eg-calc-squeeze-theorem-sin-3x)).
:::

:::{warning} Working in degrees
✗ **Wrong:** "With my calculator, $\frac{\sin 0.01}{0.01} \approx 0.0174533$, so the limit of
$\frac{\sin x}{x}$ is not $1$."

**Why:** the calculator was set to degrees. On this site $\sin x$ always takes $x$ in radians,
and [](#thm-calc-sin-x-over-x) rests on comparing $\sin\theta$ with the arc length $\theta$,
which is the angle in radians. In degrees the ratio approaches $\frac{\pi}{180}$ instead.

✓ **Right:** set the calculator to radians: $\frac{\sin 0.01}{0.01} \approx 0.999983$.
:::

## Rigorous track

The proof of the [squeeze theorem](#thm-calc-squeeze) is in the dropdown under its statement.
Two more remarks for readers who want the details.

:::{admonition} Why not just use "$\sin$ is continuous"?
:class: dropdown rigor
A tempting proof of [](#lem-calc-sin-cos-limits-at-zero) is: "$\sin$ and $\cos$ are
continuous, so their limits at $0$ are their values there." That is true, but on this site it
is circular. Continuity of $\sin$ and $\cos$ is proved *from* these two limits at $0$ (with the
addition formulas), so it cannot be used to prove them. The same goes for any argument through
the derivative of $\sin$, or through a power series for $\sin$: the derivative is computed from
[](#thm-calc-sin-x-over-x), and this course defines $\sin$ by the unit circle, not by a series.
The only facts about $\sin$ and $\cos$ used on this page are the statements of Trigonometric
Functions: the lemma on sine, angle and tangent, the properties of the point $P(t)$, the
Pythagorean identity, the addition formulas, and the bounds $-1 \le \sin t, \cos t \le 1$.
:::

:::{admonition} The squeeze theorem with "eventually" bounds
:class: dropdown rigor
The theorem asks for the inequalities $g(x) \le f(x) \le h(x)$ only on *some* punctured
interval $0 < \abs{x - a} < r$; what happens farther from $a$ does not matter. For example,
$\abs{\sin x} < \abs{x}$ was proved only for $0 < \abs{x} < \frac{\pi}{2}$, and that was enough
for $\lim_{x \to 0} \sin x = 0$. In quantifiers, the hypothesis reads
$$
\exists r > 0 \ \ \forall x \colon \quad
0 < \abs{x - a} < r \implies g(x) \le f(x) \le h(x),
$$
and the proof chooses $\delta = \min(\delta_1, \delta_2, r)$ so that the window lies inside the
interval where the inequalities hold.
:::

## Summary

- **Squeeze theorem** ([](#thm-calc-squeeze)): if $g(x) \le f(x) \le h(x)$ on a punctured
  interval around $a$, and $g$ and $h$ both approach $L$, then
  $$
  \boxed{\lim_{x \to a} f(x) = L .}
  $$
  Both bounds must approach the *same* $L$, and the inequalities must hold on both sides of $a$
  ([](#rem-calc-squeeze-theorem-hypotheses)).
- To show $f(x) \to L$, it is often enough to bound the distance: $\abs{f(x) - L} \le b(x)$
  with $b(x) \to 0$ ([](#rem-calc-squeeze-theorem-distance)).
- A bounded factor times a factor that approaches $0$ approaches $0$, as in
  $x\sin(1/x) \to 0$; the product law does not apply there, the squeeze theorem does.
- Near $0$, $\abs{\sin x} < \abs{x}$ and $1 - \frac{x^2}{2} < \cos x < 1$, so $\sin x \to 0$ and
  $\cos x \to 1$ ([](#lem-calc-sin-cos-near-zero), [](#lem-calc-sin-cos-limits-at-zero)).
- In radians, $\displaystyle \lim_{x \to 0} \frac{\sin x}{x} = 1$
  ([](#thm-calc-sin-x-over-x)) and $\displaystyle \lim_{x \to 0} \frac{1 - \cos x}{x} = 0$
  ([](#cor-calc-one-minus-cos-over-x)), proved from areas and the squeeze theorem, without
  derivatives.
- Other trigonometric limits: rewrite until $\frac{\sin x}{x}$ appears, then use the limit
  laws.

## Exercises

::::{exercise} A double angle
:label: exr-calc-squeeze-theorem-sin-2x
:class: tier-a

Find $\displaystyle \lim_{x \to 0} \frac{\sin 2x}{x}$.

:::{admonition} Hint 1
:class: dropdown hint
Use the double-angle formula for $\sin 2x$ to make $\frac{\sin x}{x}$ appear.
:::

:::{admonition} Answer
:class: dropdown answer
$2$
:::
::::

::::{solution} exr-calc-squeeze-theorem-sin-2x
:label: sol-calc-squeeze-theorem-sin-2x
:class: dropdown

By [part (e) of the addition formulas](#thm-calc-addition-formulas), $\sin 2x = 2\sin x\cos x$
for every real $x$, so for every $x \ne 0$
$$
\frac{\sin 2x}{x} = 2\cos x \cdot \frac{\sin x}{x} ,
$$
and both sides are defined at exactly the $x \ne 0$. By [part (c) of the lemma on limits at
0](#lem-calc-sin-cos-limits-at-zero) and the "in particular" of [part (c) of the limit
laws](#thm-calc-limit-laws), $\lim_{x \to 0} 2\cos x = 2 \cdot 1 = 2$. By
[](#thm-calc-sin-x-over-x), $\lim_{x \to 0} \frac{\sin x}{x} = 1$. The product law, part (c),
gives $\lim_{x \to 0} \frac{\sin 2x}{x} = 2 \cdot 1 = 2$.
::::

::::{exercise} Another oscillating factor
:label: exr-calc-squeeze-theorem-x2-cos
:class: tier-a

Find $\displaystyle \lim_{x \to 0} x^2 \cos\Bigl(\frac{1}{x}\Bigr)$, and justify your answer
with the squeeze theorem.

:::{admonition} Hint 1
:class: dropdown hint
How large can $\abs{\cos(1/x)}$ be? Bound $\bigl\lvert x^2\cos(1/x)\bigr\rvert$ as in
[](#eg-calc-squeeze-theorem-oscillating).
:::

:::{admonition} Answer
:class: dropdown answer
$0$
:::
::::

::::{solution} exr-calc-squeeze-theorem-x2-cos
:label: sol-calc-squeeze-theorem-x2-cos
:class: dropdown

Let $x \ne 0$. By [part (b) of the proposition on the bounds of sine and
cosine](#prop-calc-sin-bounded), $-1 \le \cos(1/x) \le 1$, which says
$\abs{\cos(1/x)} \le 1$ ([part (b) of the proposition on distance
inequalities](#prop-calc-abs-interval)). By [properties 4 and 5 of the absolute
value](#rem-calc-absolute-value-properties), $\abs{x^2} = \abs{x}^2 = x^2$, and multiplying
$\abs{\cos(1/x)} \le 1$ by the number $x^2 \ge 0$ gives only $\le$ ([property 5(b) of the order
rules](#rem-calc-order-rules)):
$$
\Bigl\lvert x^2\cos\Bigl(\frac{1}{x}\Bigr) - 0\Bigr\rvert
= x^2\,\Bigl\lvert\cos\Bigl(\frac{1}{x}\Bigr)\Bigr\rvert \le x^2 .
$$
By [direct substitution](#cor-calc-direct-substitution), $\lim_{x \to 0} x^2 = 0$. By
[](#rem-calc-squeeze-theorem-distance), with $a = 0$, $L = 0$, $r = 1$ and $b(x) = x^2$, the
limit is $0$.
::::

::::{exercise} Tangent over x
:label: exr-calc-squeeze-theorem-tan
:class: tier-a

Find $\displaystyle \lim_{x \to 0} \frac{\tan x}{x}$.

:::{admonition} Hint 1
:class: dropdown hint
Write $\tan x = \frac{\sin x}{\cos x}$. Which law handles the division by $\cos x$, and what
does it need?
:::

:::{admonition} Answer
:class: dropdown answer
$1$
:::
::::

::::{solution} exr-calc-squeeze-theorem-tan
:label: sol-calc-squeeze-theorem-tan
:class: dropdown

By [the definition of the tangent](#def-calc-tan-sec-csc-cot), $\tan x = \frac{\sin x}{\cos x}$
wherever $\cos x \ne 0$. So at every $x$ with $x \ne 0$ and $\cos x \ne 0$,
$$
\frac{\tan x}{x} = \frac{\sin x}{x\cos x} = \frac{\;\frac{\sin x}{x}\;}{\cos x} ,
$$
and both sides are defined at exactly these $x$. By [](#thm-calc-sin-x-over-x), the numerator
$\frac{\sin x}{x}$ approaches $1$; it is defined at every $x \ne 0$. By [part (c) of the lemma
on limits at 0](#lem-calc-sin-cos-limits-at-zero), $\cos x$ approaches $M = 1$, and
$\cos$ is defined for every real $x$. Since $M = 1 \ne 0$, the quotient law, [part (d) of the
limit laws](#thm-calc-limit-laws), gives
$$
\lim_{x \to 0} \frac{\tan x}{x} = \frac{1}{1} = 1 .
$$
::::

::::{exercise} One minus cosine over x squared
:label: exr-calc-squeeze-theorem-one-minus-cos-x2
:class: tier-b

Find $\displaystyle \lim_{x \to 0} \frac{1 - \cos x}{x^2}$.

:::{admonition} Hint 1
:class: dropdown hint
Multiply numerator and denominator by $1 + \cos x$, as in the proof of
[](#cor-calc-one-minus-cos-over-x).
:::

:::{admonition} Hint 2
:class: dropdown hint
The result is $\bigl(\frac{\sin x}{x}\bigr)^2 \cdot \frac{1}{1 + \cos x}$ near $0$. Which laws
apply to each factor?
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{2}$
:::
::::

::::{solution} exr-calc-squeeze-theorem-one-minus-cos-x2
:label: sol-calc-squeeze-theorem-one-minus-cos-x2
:class: dropdown

Let $0 < \abs{x} < \frac{\pi}{2}$. By [properties 4 and 8 of the point
$P(t)$](#rem-calc-trig-functions-circle-properties), $\cos x = \cos\abs{x} > 0$, and adding $1$
([property 3 of the order rules](#rem-calc-order-rules)) gives $1 + \cos x > 1 > 0$. With
[the Pythagorean identity](#thm-calc-pythagorean-identity),
$$
\begin{aligned}
\frac{1 - \cos x}{x^2}
  &= \frac{(1 - \cos x)(1 + \cos x)}{x^2\,(1 + \cos x)} = \frac{\sin^2 x}{x^2\,(1 + \cos x)} \\
  &= \Bigl(\frac{\sin x}{x}\Bigr)^2 \cdot \frac{1}{1 + \cos x} .
\end{aligned}
$$
Call the last product $G(x)$. By [](#thm-calc-sin-x-over-x) and the power law,
[part (e) of the limit laws](#thm-calc-limit-laws) with $n = 2$,
$\bigl(\frac{\sin x}{x}\bigr)^2 \to 1^2 = 1$. By [part (c) of the lemma on limits at
0](#lem-calc-sin-cos-limits-at-zero) and the sum law, part (b), $1 + \cos x \to 2$, and since
$2 \ne 0$ the quotient law, part (d), with numerator $1$ (part (a)), gives
$\frac{1}{1 + \cos x} \to \frac12$. The product law, part (c), gives
$G(x) \to 1 \cdot \frac12 = \frac12$.

The function $\frac{1 - \cos x}{x^2}$ is defined at every $x \ne 0$ and equals $G(x)$ for
$0 < \abs{x} < \frac{\pi}{2}$. The [squeeze theorem](#thm-calc-squeeze) with $g = h = G$ gives
$\lim_{x \to 0} \frac{1 - \cos x}{x^2} = \frac12$.
::::

::::{exercise} A square root and an oscillation
:label: exr-calc-squeeze-theorem-sqrt-sin
:class: tier-b

Find $\displaystyle \lim_{x \to 0} \sqrt{\abs{x}}\,\sin\Bigl(\frac{1}{x}\Bigr)$.

:::{admonition} Hint 1
:class: dropdown hint
Bound the distance from $0$ by $\sqrt{\abs{x}}$. What is $\lim_{x \to 0} \sqrt{\abs{x}}$, and
which law gives it?
:::

:::{admonition} Answer
:class: dropdown answer
$0$
:::
::::

::::{solution} exr-calc-squeeze-theorem-sqrt-sin
:label: sol-calc-squeeze-theorem-sqrt-sin
:class: dropdown

Let $x \ne 0$. As in [](#eg-calc-squeeze-theorem-oscillating), $\abs{\sin(1/x)} \le 1$, by
[part (a) of the proposition on the bounds of sine and cosine](#prop-calc-sin-bounded). The
number $\sqrt{\abs{x}}$ is defined and non-negative ([the square-root
remark](#rem-calc-square-roots)), so $\bigl\lvert\sqrt{\abs{x}}\bigr\rvert = \sqrt{\abs{x}}$,
and by [property 4 of the absolute value](#rem-calc-absolute-value-properties) and
[property 5(b) of the order rules](#rem-calc-order-rules) (multiplying by
$\sqrt{\abs{x}} \ge 0$),
$$
\Bigl\lvert \sqrt{\abs{x}}\,\sin\Bigl(\frac{1}{x}\Bigr) - 0 \Bigr\rvert
= \sqrt{\abs{x}}\,\Bigl\lvert\sin\Bigl(\frac{1}{x}\Bigr)\Bigr\rvert \le \sqrt{\abs{x}} .
$$
By [part (a) of the lemma on limits at 0](#lem-calc-sin-cos-limits-at-zero),
$\lim_{x \to 0} \abs{x} = 0$, and $\abs{x} \ge 0$ for every $x$. So the square-root law,
[part (f) of the limit laws](#thm-calc-limit-laws) with $L = 0$, gives
$\lim_{x \to 0} \sqrt{\abs{x}} = 0$. By [](#rem-calc-squeeze-theorem-distance), with $a = 0$,
$L = 0$, $r = 1$ and $b(x) = \sqrt{\abs{x}}$, the limit is $0$.
::::

::::{exercise} A tighter tolerance for the pendulum
:label: exr-calc-squeeze-theorem-pendulum
:class: tier-b applied

In [](#eg-calc-squeeze-theorem-small-angle), the relative error of replacing $\sin\theta$ by
$\theta$ satisfies $0 < 1 - \frac{\sin\theta}{\theta} < \frac{\theta^2}{2}$ for
$0 < \abs{\theta} < \frac{\pi}{2}$. A more accurate model needs a relative error below
$0.005$, half a percent. Find the largest $r > 0$ such that $\frac{\theta^2}{2} \le 0.005$ for
every $\theta$ with $0 < \abs{\theta} < r$. Give $r$ in radians, and convert it to degrees in
your solution.

:::{admonition} Hint 1
:class: dropdown hint
Solve $\frac{\theta^2}{2} \le 0.005$ for $\abs{\theta}$, as in step 2 of the example.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{10}$
:::
::::

::::{solution} exr-calc-squeeze-theorem-pendulum
:label: sol-calc-squeeze-theorem-pendulum
:class: dropdown

Multiplying by the positive number $2$, or by $\frac12$, keeps inequalities
([property 5(b) of the order rules](#rem-calc-order-rules)), so $\frac{\theta^2}{2} \le 0.005$
exactly when $\theta^2 \le 0.01$. Now $\theta^2 = \abs{\theta}^2$ ([property 5 of the absolute
value](#rem-calc-absolute-value-properties)) and $0.01 = 0.1^2$, and $\abs{\theta}$ and $0.1$
are non-negative, so by [property 6 of the absolute
value](#rem-calc-absolute-value-properties) this holds exactly when $\abs{\theta} \le 0.1$.

So $r = 0.1$ works: every $\theta$ with $0 < \abs{\theta} < 0.1$ has $\abs{\theta} \le 0.1$.
No larger $r$ works: if $r > 0.1$, the number $\theta = \frac{0.1 + r}{2}$ satisfies
$0.1 < \theta < r$, and then $\abs{\theta} = \theta > 0.1$, so $\frac{\theta^2}{2} > 0.005$ by
the equivalence just shown. Hence $r = 0.1 = \frac{1}{10}$
radians. As $0.1 < \frac{\pi}{2} \approx 1.571$, the bound of the example applies to all these
$\theta$, and then the relative error is less than $\frac{\theta^2}{2} \le 0.005$.

In degrees, $0.1$ radians is $\frac{180 \cdot 0.1}{\pi} = \frac{18}{\pi} \approx 5.73$
degrees. Halving the tolerance shrank the guaranteed range by the factor
$\frac{0.1}{\sqrt{0.02}} = \frac{1}{\sqrt{2}}$, because the bound is quadratic in $\theta$.
::::

::::{exercise} Bounds with different limits
:label: exr-calc-squeeze-theorem-different-limits
:class: tier-b

True or false: if $f$ is defined at every $x \ne 0$ and $-1 \le f(x) \le 1$ for every
$x \ne 0$, then $\displaystyle \lim_{x \to 0} f(x)$ exists.

:::{admonition} Hint 1
:class: dropdown hint
Which hypothesis of the [squeeze theorem](#thm-calc-squeeze) fails? Look for a function that
jumps.
:::

:::{admonition} Answer
:class: dropdown answer bool
False
:::
::::

::::{solution} exr-calc-squeeze-theorem-different-limits
:label: sol-calc-squeeze-theorem-different-limits
:class: dropdown

False. The function $s(x) = \frac{\abs{x}}{x}$ of [](#rem-calc-squeeze-theorem-hypotheses) is
defined at every $x \ne 0$ and takes only the values $1$ and ${-1}$, so $-1 \le s(x) \le 1$ for
every $x \ne 0$. That remark shows that $s$ has no limit at $0$. The squeeze theorem does not
apply, because the bounds ${-1}$ and $1$ approach different numbers.
::::

::::{exercise} The corollary by a direct squeeze
:label: exr-calc-squeeze-theorem-direct-cor
:class: tier-c rigor

Prove [](#cor-calc-one-minus-cos-over-x), $\lim_{x \to 0} \frac{1 - \cos x}{x} = 0$, without
[](#thm-calc-sin-x-over-x): use [part (b) of the lemma on sine and cosine near
0](#lem-calc-sin-cos-near-zero) and [](#rem-calc-squeeze-theorem-distance).

:::{admonition} Hint 1
:class: dropdown hint
Part (b) gives $0 < 1 - \cos x < \frac{x^2}{2}$ for $0 < \abs{x} < \frac{\pi}{2}$. Divide by
$\abs{x}$.
:::

:::{admonition} Answer
:class: dropdown answer manual
For $0 < \abs{x} < \frac{\pi}{2}$, $\Bigl\lvert \frac{1 - \cos x}{x} \Bigr\rvert < \frac{\abs{x}}{2}$, and $\frac{\abs{x}}{2} \to 0$.
:::
::::

::::{solution} exr-calc-squeeze-theorem-direct-cor
:label: sol-calc-squeeze-theorem-direct-cor
:class: dropdown

Let $0 < \abs{x} < \frac{\pi}{2}$. By [part (b) of the lemma on sine and cosine near
0](#lem-calc-sin-cos-near-zero), $1 - \frac{x^2}{2} < \cos x < 1$. Adding
$\frac{x^2}{2} - \cos x$ to the first inequality, and $-\cos x$ to the second, keeps them
([property 3 of the order rules](#rem-calc-order-rules)):
$0 < 1 - \cos x < \frac{x^2}{2}$. So $\abs{1 - \cos x} = 1 - \cos x$, by
[the definition of the absolute value](#def-calc-absolute-value). By [properties 4 and 5 of the
absolute value](#rem-calc-absolute-value-properties),
$$
\Bigl\lvert \frac{1 - \cos x}{x} - 0 \Bigr\rvert = \frac{1 - \cos x}{\abs{x}}
< \frac{x^2}{2\abs{x}} = \frac{\abs{x}^2}{2\abs{x}} = \frac{\abs{x}}{2} ;
$$
the $<$ multiplies $1 - \cos x < \frac{x^2}{2}$ by the positive number $\frac{1}{\abs{x}}$
([properties 6 and 5(a) of the order rules](#rem-calc-order-rules)). In particular
$\bigl\lvert \frac{1 - \cos x}{x} - 0 \bigr\rvert \le \frac{\abs{x}}{2}$.

By [part (a) of the lemma on limits at 0](#lem-calc-sin-cos-limits-at-zero) and the "in
particular" of [part (c) of the limit laws](#thm-calc-limit-laws), with $c = \frac12$,
$\lim_{x \to 0} \frac{\abs{x}}{2} = \frac12 \cdot 0 = 0$. Both $\frac{1 - \cos x}{x}$ and
$\frac{\abs{x}}{2}$ are defined at every $x \ne 0$. By [](#rem-calc-squeeze-theorem-distance),
with $a = 0$, $L = 0$, $r = \frac{\pi}{2}$ and $b(x) = \frac{\abs{x}}{2}$,
$\lim_{x \to 0} \frac{1 - \cos x}{x} = 0$.
::::

::::{exercise} A function squeezed by a parabola
:label: exr-calc-squeeze-theorem-parabola
:class: tier-c rigor

Let $f$ be a function defined for every real $x$, with $\abs{f(x)} \le x^2$ for every real
$x$. Prove that $f(0) = 0$ and that $\displaystyle \lim_{x \to 0} \frac{f(x)}{x} = 0$.

:::{admonition} Hint 1
:class: dropdown hint
For $f(0)$, put $x = 0$ in the inequality. For the limit, bound
$\bigl\lvert \frac{f(x)}{x} \bigr\rvert$ for $x \ne 0$.
:::

:::{admonition} Answer
:class: dropdown answer manual
$\abs{f(0)} \le 0$ gives $f(0) = 0$; and $\Bigl\lvert \frac{f(x)}{x} \Bigr\rvert \le \abs{x}$ for $x \ne 0$, with $\abs{x} \to 0$.
:::
::::

::::{solution} exr-calc-squeeze-theorem-parabola
:label: sol-calc-squeeze-theorem-parabola
:class: dropdown

**$f(0) = 0$.** At $x = 0$ the hypothesis says $\abs{f(0)} \le 0^2 = 0$. Also
$\abs{f(0)} \ge 0$, by [property 1 of the absolute
value](#rem-calc-absolute-value-properties), so $\abs{f(0)} = 0$, and by the same property
$f(0) = 0$.

**The limit.** Let $x \ne 0$. Then $\abs{x} > 0$ (property 1 of the absolute value), and by
[properties 4 and 5 of the absolute value](#rem-calc-absolute-value-properties),
$$
\Bigl\lvert \frac{f(x)}{x} - 0 \Bigr\rvert = \frac{\abs{f(x)}}{\abs{x}}
\le \frac{x^2}{\abs{x}} = \frac{\abs{x}^2}{\abs{x}} = \abs{x} ,
$$
where the $\le$ multiplies $\abs{f(x)} \le x^2$ by the positive number $\frac{1}{\abs{x}}$
([properties 6 and 5(b) of the order rules](#rem-calc-order-rules)). The function
$\frac{f(x)}{x}$ is defined at every $x \ne 0$, and $\lim_{x \to 0} \abs{x} = 0$ by [part (a)
of the lemma on limits at 0](#lem-calc-sin-cos-limits-at-zero). By
[](#rem-calc-squeeze-theorem-distance), with $a = 0$, $L = 0$, $r = 1$ and $b(x) = \abs{x}$,
$\lim_{x \to 0} \frac{f(x)}{x} = 0$.

For example, $f(x) = x^2\cos(1/x)$ for $x \ne 0$ and $f(0) = 0$ satisfies the hypothesis:
$\abs{\cos(1/x)} \le 1$ by [part (b) of the proposition on the bounds of sine and
cosine](#prop-calc-sin-bounded), and multiplying by $x^2 \ge 0$ gives
$\bigl\lvert x^2\cos(1/x)\bigr\rvert \le x^2$.
::::

## Where this leads

:::{where-this-leads}
:::

The squeeze theorem is the tool for limits that the laws cannot reach: oscillating factors,
and the limits of $\sin$ and $\cos$, on which the calculus of the trigonometric functions rests.
