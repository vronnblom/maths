---
title: Polynomial and Rational Functions
label: calc-polynomial-rational
description: >-
  Polynomials and quotients of polynomials: the factor theorem, division of polynomials, why a
  polynomial has no more roots than its degree, and how to find the domain, the zeros and the
  sign of a rational function.
tags: [preliminaries, proofs, inequalities]
maths:
  kind: topic
  subject: calc
  status: reviewed
  level: core
  difficulty: 2
  est_minutes: 45
  prerequisites: [calc-functions]
  objectives:
    - Factor polynomials using known roots.
    - Perform polynomial division.
    - Find domains, zeros and the sign of rational functions.
  verify: verify/calculus/preliminaries/test_polynomial_and_rational_functions.py
  widgets: [function-plot]
  reviewed_by: [vronnblom]
  manual_checked:
    exr-calc-polynomial-rational-integer-root: vronnblom
  sources: []
---

:::{topic-header}
:::

## Why this matters

A metal cube is heated and expands. When its side is $x$ centimetres, its volume is $x^3$ cubic
centimetres. As the side grows from $2$ to $x$, the volume grows by $x^3 - 8$, so on average
the volume grows by
$$
\frac{x^3 - 8}{x - 2}
$$
cubic centimetres per centimetre of side. How fast does the volume grow when the side is
exactly $2$? Putting $x = 2$ into the formula gives $\frac{0}{0}$, which is not a number. But
the numerator factors:
$$
x^3 - 8 = (x - 2)\,(x^2 + 2x + 4),
$$
as multiplying out the right-hand side confirms. So for every $x \ne 2$ we may cancel the
non-zero number $x - 2$: the average rate is $x^2 + 2x + 4$, a formula that makes sense at
every $x$, and for $x$ close to $2$ it is close to $2^2 + 2 \cdot 2 + 4 = 12$.

Why does $x^3 - 8$ have the factor $x - 2$? Because $2^3 - 8 = 0$. The **factor theorem** of
this page says that this always happens: for every polynomial $p$ and every number $a$, the
difference $p(x) - p(a)$ has the factor $x - a$. Limits and derivatives of polynomials rest on
exactly this.

The page also answers two questions that recur throughout calculus. How many solutions can an
equation $p(x) = 0$ have? At most the degree of $p$. And for which $x$ is a quotient of
polynomials, such as $\frac{x^2 - 1}{x^2 - x - 6}$, positive? Its factors decide, as soon as we
know the signs of products and quotients.

:::{admonition} Looking ahead
:class: looking-ahead
The page Computing Limits Algebraically turns "for $x$ close to $2$ it is close to $12$" into a
limit, by cancelling the factor $x - a$ as above. The page Tangent Lines and Rates of Change
calls the number $12$ the rate of change of the volume at $x = 2$.
:::

## Polynomials and rational functions

A polynomial is built from the variable $x$ and constants by adding, subtracting and
multiplying, finitely many times. Collecting equal powers of $x$ brings it to a standard form.

:::{proof:definition} Polynomial, degree, root
:label: def-calc-polynomial

A **polynomial** is a function $p\colon \R \to \R$ of the form
$$
p(x) = c_n x^n + \dots + c_1 x + c_0 ,
$$
where $n \in \N$ and the **coefficients** $c_0, c_1, \dots, c_n$ are real numbers.

- If $c_n \ne 0$, then $p$ has **degree** $n$; $c_n$ is its **leading coefficient**, $c_n x^n$
  its **leading term** and $c_0$ its **constant term**.
- If every coefficient is $0$, then $p$ is the **zero polynomial**, which has no degree.

A **root** (or **zero**) of $p$ is a real number $r$ with $p(r) = 0$.
:::

**In words.** The degree is the highest power of $x$ that really occurs. Polynomials of degree
$0$ are the non-zero constants; those of degree $1$, $2$ and $3$ are called **linear**,
**quadratic** and **cubic**. A polynomial is defined at every real number: its domain is $\R$.
Any polynomial other than the zero polynomial can be written with $c_n \ne 0$, by leaving out
the terms with coefficient $0$ at the top. Could one function have two such forms, with
different degrees? No: [](#cor-calc-polynomial-identity) below shows that the values of a
polynomial determine its coefficients, so its degree is well defined.

**Example.** $p(x) = 3x^4 - x + 7$ has degree $4$, leading coefficient $3$ and constant term
$7$. The polynomial $(x - 1)(x + 2) = x^2 + x - 2$ has degree $2$, and its roots are $1$ and
${-2}$. The polynomial $x^2 - 2$ has the roots $\sqrt{2}$ and ${-\sqrt{2}}$, because both square
to $2$ ([the remark on square roots](#rem-calc-square-roots)).

**Non-example.** $f(x) = \dfrac{1}{x}$ is not a polynomial. Its
[natural domain](#def-calc-domain-range) leaves out $0$, while every polynomial is defined at
$0$. In the same way $\sqrt{x}$, whose natural domain is $[0, \infty)$, is not a polynomial.

Dividing one polynomial by another gives the next class of functions.

:::{proof:definition} Rational function
:label: def-calc-rational-function

A **rational function** is a function $f$ given by
$$
f(x) = \frac{p(x)}{q(x)} ,
$$
where $p$ and $q$ are polynomials and $q$ is not the zero polynomial. Its domain is its
[natural domain](#def-calc-domain-range),
$$
\dom f = \{x \in \R : q(x) \ne 0\}.
$$
:::

**In words.** A rational function is a quotient of two polynomials. The formula
$\frac{p(x)}{q(x)}$ is a real number exactly when the denominator $q(x)$ is not $0$, so the
domain is $\R$ without the roots of $q$. Every polynomial $p$ is a rational function, with
$q(x) = 1$.

**Example.** $f(x) = \dfrac{x + 1}{x^2 - 4}$ is a rational function. An exercise on
[Functions and Their Graphs](#calc-functions) asks for its natural domain; now we can also say
why the denominator is $0$ only at $\pm 2$. It is $x^2 - 4 = (x - 2)(x + 2)$, which is $0$
exactly when $x = 2$ or $x = -2$ ([part (a) of the sign rules](#prop-calc-sign-rules) below), so
$\dom f = (-\infty, -2) \cup (-2, 2) \cup (2, \infty)$.

**Non-example.** $g(x) = \dfrac{\sqrt{x}}{x + 1}$ is not a rational function. Its natural domain
is $[0, \infty)$, while the domain of a rational function leaves out only finitely many numbers
([part (a) of the proposition on the domain](#prop-calc-rational-domain) below).

## Main results

### Signs of products and quotients

To find where a rational function is positive, we need the signs of products and quotients.
[The order rules](#rem-calc-order-rules), on Real Numbers and Intervals, speak of inequalities,
not of signs; the proposition below derives from them the facts about signs that we use.

:::{proof:proposition} Sign rules
:label: prop-calc-sign-rules

Let $u$ and $v$ be real numbers.

(a) $uv = 0$ exactly when $u = 0$ or $v = 0$. If $v \ne 0$, then $\frac{u}{v} = 0$ exactly when
$u = 0$.

(b) For real numbers $x$ and $t$, the number $x - t$ is negative if $x < t$, zero if $x = t$,
and positive if $x > t$.

(c) If $u \ne 0$ and $v \ne 0$, then $uv$ and $\frac{u}{v}$ are positive when $u$ and $v$ have
the same sign, and negative when their signs differ. In particular $\frac{1}{v}$ has the same
sign as $v$, $u^2 > 0$ for $u \ne 0$, so $u^2 \ge 0$ for every real $u$, and $1 > 0$.

(d) A product of finitely many non-zero numbers, or a quotient of two such products, is positive
if an even number of all its factors (in the numerator and the denominator together) are
negative, and negative if an odd number are.
:::

:::{proof:proof}
:enumerated: false
Parts (a) and (b) are short computations, (c) applies the rules for multiplying an inequality
to $0 < v$ or $v < 0$, and for (d) we multiply in the factors one at a time and follow the sign
with (c).

(a) If $u = 0$ or $v = 0$, then $uv = 0$. Conversely, let $uv = 0$. If $u \ne 0$, then
$v = \frac{1}{u} \cdot (uv) = \frac{1}{u} \cdot 0 = 0$. So $u = 0$ or $v = 0$. Now let $v \ne 0$.
Then $\frac{1}{v} \ne 0$, because $v \cdot \frac{1}{v} = 1 \ne 0$, and
$\frac{u}{v} = u \cdot \frac{1}{v}$. By what we have just proved, this is $0$ exactly when
$u = 0$.

(b) By [property 3 of the order rules](#rem-calc-order-rules), adding $-t$ to both sides keeps an
inequality: $x < t$ gives $x - t < 0$, and $x > t$ gives $x - t > 0$. If $x = t$, then
$x - t = 0$.

(c) First the product. If $v > 0$, multiplying $0 < v$ by $u$ gives $0 = u \cdot 0 < uv$ when
$u > 0$ ([property 5(a) of the order rules](#rem-calc-order-rules)), and multiplying $u < 0$
by $v > 0$ gives $uv < 0 \cdot v = 0$ when $u < 0$ (property 5(a) again). If $v < 0$,
multiplying $u < 0$ by $v$ reverses it, $uv > 0 \cdot v = 0$, when $u < 0$
([property 5(c)](#rem-calc-order-rules)), and multiplying $0 < u$ by $v$ gives $0 > uv$ when
$u > 0$ (property 5(c) again). So $uv > 0$ when the signs agree and $uv < 0$ when they differ.

Next, $\frac{1}{v}$ has the sign of $v$. If $v > 0$, then $\frac{1}{v} > 0$
([property 6 of the order rules](#rem-calc-order-rules)). If $v < 0$, adding $-v$ to both sides
gives $0 < -v$ ([property 3](#rem-calc-order-rules)), so $\frac{1}{-v} > 0$ by property 6, and
adding $\frac{1}{v}$ to both sides (property 3) gives $\frac{1}{v} < \frac{1}{-v} + \frac{1}{v}
= 0$. Since $\frac{u}{v} = u \cdot \frac{1}{v}$ and $\frac{1}{v}$ has the sign of $v$, the rule
for products gives the rule for quotients.

In particular, $u \cdot u$ has two factors of the same sign, so $u^2 > 0$ for $u \ne 0$; with
$0^2 = 0$ this gives $u^2 \ge 0$ for every real $u$. And $1 = 1^2 > 0$, as $1 \ne 0$.

(d) Start from $1$, which is positive by (c), and multiply in the factors one at a time. Each
partial product is non-zero, by (a). By (c), multiplying a non-zero number by a positive factor
keeps its sign, and multiplying it by a negative factor changes its sign. So the sign changes
once for each negative factor, and the product is positive after an even number of changes and
negative after an odd number. A quotient $\frac{N}{D}$ of two such products is, by (c) again,
positive exactly when $N$ and $D$ have the same sign, that is, exactly when $N \cdot D$ is
positive. Since $N \cdot D$ is the
product of all the factors, the count for the product decides the sign of the quotient.
:::

**In words.** "Minus times minus is plus": only the number of negative factors matters, and a
quotient behaves like a product. Part (b) says that the factor $x - t$ is negative to the left
of $t$ and positive to the right of it.

### Degree of a product

The first use of the sign rules is the degree of a product of polynomials, on which the division
of polynomials below rests.

:::{proof:proposition} Degree of a product
:label: prop-calc-polynomial-degree-product

Let $f$ be a polynomial of degree $m$ with leading coefficient $a$, and $g$ a polynomial of
degree $k$ with leading coefficient $b$. Then $f(x)\, g(x)$ is a polynomial of degree $m + k$,
with leading coefficient $ab$. In particular, a product of two polynomials that are not the zero
polynomial is not the zero polynomial.
:::

:::{proof:proof}
:enumerated: false
We multiply out and find the highest power of $x$ that occurs.

Write $f(x) = a_m x^m + \dots + a_1 x + a_0$ with $a_m = a$, and
$g(x) = b_k x^k + \dots + b_1 x + b_0$ with $b_k = b$. Multiplying out, $f(x)\, g(x)$ is the sum
of the terms $a_i b_j\, x^{i + j}$ for $i = 0, 1, \dots, m$ and $j = 0, 1, \dots, k$, and
collecting equal powers of $x$ writes it in the form of [](#def-calc-polynomial): it is a
polynomial. Since $i \le m$ and $j \le k$, every power that occurs has $i + j \le m + k$, and if
$i < m$ or $j < k$, then $i + j < m + k$ ([property 4 of the order rules](#rem-calc-order-rules)).
So only the term with $i = m$ and $j = k$ has the power $x^{m + k}$, and its coefficient is
$ab$. Since $a \ne 0$ and $b \ne 0$, [part (a) of the sign rules](#prop-calc-sign-rules) gives
$ab \ne 0$. So the product has degree $m + k$ and leading coefficient $ab$; having a degree, it
is not the zero polynomial.
:::

**In words.** Multiplying polynomials adds their degrees and multiplies their leading
coefficients. For example, $(3x^2 + 1)(x - 5)$ has degree $2 + 1 = 3$ and leading coefficient
$3 \cdot 1 = 3$.

### Factors and roots

:::{proof:theorem} Factor theorem
:label: thm-calc-factor-theorem

Let $p$ be a polynomial and $a$ a real number.

(a) There is a polynomial $q$ such that, for every real $x$,
$$
p(x) - p(a) = (x - a)\, q(x) ,
$$
and so, for every real $x \ne a$,
$$
\frac{p(x) - p(a)}{x - a} = q(x) .
$$
If $p$ has degree $n \ge 1$, then $q$ has degree $n - 1$ and the same leading coefficient as
$p$.

(b) If $p(a) = 0$, then $p(x) = (x - a)\, q(x)$ for every real $x$, with $q$ as in (a).
Conversely, if $p(x) = (x - a)\, q(x)$ for every real $x$, for some polynomial $q$, then
$p(a) = 0$. So $a$ is a root of $p$ exactly when $x - a$ is a **factor** of $p$.
:::

:::{proof:proof}
:enumerated: false
We write $p(x) - p(a)$ as a sum of multiples of $x^k - a^k$ and take the factor $x - a$ out of
each of them.

Write $p(x) = c_n x^n + \dots + c_1 x + c_0$ with $n \ge 1$ (a constant polynomial can be
written so too, with $c_n = \dots = c_1 = 0$). The constant terms cancel in the difference:
$$
\begin{aligned}
&p(x) - p(a) \\
&\quad = c_n (x^n - a^n) + \dots \\
&\qquad + c_2 (x^2 - a^2) + c_1 (x - a).
\end{aligned}
$$
For each integer $k \ge 1$, let
$$
\begin{aligned}
q_k(x) &= x^{k-1} + x^{k-2} a + \dots \\
&\quad + x a^{k-2} + a^{k-1},
\end{aligned}
$$
the sum of the $k$ terms $x^{j} a^{k - 1 - j}$ for $j = 0, 1, \dots, k - 1$. Here, as in the
constant term $c_0 = c_0 x^0$ of a polynomial, $x^0$ and $a^0$ mean $1$, also when $x = 0$ or
$a = 0$: we read $0^0$ as $1$. For $k = 1$, $q_1$ is the constant $1$.

Then $x^k - a^k = (x - a)\, q_k(x)$. Indeed, multiplying $q_k(x)$ by $x$ gives
$x^k + x^{k-1} a + \dots + x a^{k-1}$, multiplying it by $-a$ gives
$-x^{k-1} a - \dots - x a^{k-1} - a^k$, and in the sum of the two every term cancels except
$x^k$ and $-a^k$.

Hence $p(x) - p(a) = (x - a)\, q(x)$ for every real $x$, with
$$
q(x) = c_n\, q_n(x) + \dots + c_1\, q_1(x).
$$
Since $a$ is a fixed number, each $q_k$ is a polynomial in $x$ whose highest power is
$x^{k-1}$, with coefficient $1$. So $q$ is a polynomial, no power higher than $x^{n-1}$ occurs in
it, and $x^{n-1}$ occurs only in $c_n\, q_n(x)$, with coefficient $c_n$. If $p$ has degree
$n \ge 1$, then $c_n \ne 0$, so $q$ has degree $n - 1$ and leading coefficient $c_n$. Finally,
for $x \ne a$ the number $x - a$ is not $0$, so we may divide both sides of
$p(x) - p(a) = (x - a)\, q(x)$ by it, which gives the quotient form. This proves (a).

(b) If $p(a) = 0$, the identity of (a) reads $p(x) = (x - a)\, q(x)$. Conversely, if
$p(x) = (x - a)\, q(x)$ for every real $x$, then at $x = a$ it gives
$p(a) = 0 \cdot q(a) = 0$.
:::

**In words.** Every root $a$ splits off a linear factor $x - a$, and what is left has degree one
less. The quotient $\frac{p(x) - p(a)}{x - a}$ of part (a) is undefined at $x = a$, but it agrees
with the polynomial $q$ at every other point. This is the form in which the Limits and
Derivatives chapters use the theorem. The proof also gives a way to compute $q$: replace each
$x^k - a^k$ by $(x - a)\, q_k(x)$ ([](#eg-calc-polynomial-rational-difference-quotient)).

**Example.** For $p(x) = x^3$ and $a = 2$, the proof gives $q(x) = q_3(x) = x^2 + 2x + 4$, the
factorisation of $x^3 - 8$ in Why this matters.

Each root splits off a factor, and the degree drops by one each time, so a polynomial cannot
have more roots than its degree.

:::{proof:theorem} A polynomial of degree $n$ has at most $n$ roots
:label: thm-calc-polynomial-roots-bound

Let $p$ be a polynomial of degree $n$. Then $p$ has at most $n$ roots: there are at most $n$
different real numbers $r$ with $p(r) = 0$.
:::

:::{proof:proof}
:enumerated: false
A root $r$ splits off the factor $x - r$, and every other root is a root of the quotient, which
has degree $n - 1$. We turn this into a proof by looking at a smallest counterexample.

A polynomial of degree $0$ is a non-zero constant, so it has no roots, and the theorem holds for
it. Suppose the theorem fails for some degree. Then the degrees $n$ of the polynomials of degree
$n$ with more than $n$ roots form a non-empty set of positive integers, and by
[the well-ordering principle](#rem-calc-well-ordering) it has a smallest element
$n \ge 1$. Let $p$ be a polynomial of degree $n$ with more than $n$ roots, and let $r$ be one of
them.

By [](#thm-calc-factor-theorem) (b), $p(x) = (x - r)\, q(x)$ for every real $x$, where $q$ is
the polynomial of part (a), of degree $n - 1$. Let $s$ be a root of $p$ with $s \ne r$. Then
$$
0 = p(s) = (s - r)\, q(s),
$$
and $s - r \ne 0$, so $q(s) = 0$ by [part (a) of the sign rules](#prop-calc-sign-rules). So
each of the roots of $p$ other than $r$, of which there are more than $n - 1$, is a root of
$q$. Then $q$ is a polynomial of degree $n - 1$ with more than $n - 1$ roots. If $n - 1 = 0$,
this contradicts the first paragraph; if $n - 1 \ge 1$, it contradicts the choice of $n$ as the
smallest degree with a counterexample. So the theorem holds for every degree.
:::

The theorem says nothing about the zero polynomial, which has no degree: every real number is
a root of it. For any other polynomial, it gives a test for equality.

:::{proof:corollary} Polynomials that agree at many points
:label: cor-calc-polynomial-identity

Let $n \in \N$, and let
$$
\begin{aligned}
p(x) &= c_n x^n + \dots + c_1 x + c_0, \\
\tilde{p}(x) &= d_n x^n + \dots + d_1 x + d_0
\end{aligned}
$$
be polynomials, written with the same $n$ (some coefficients may be $0$). If
$p(x) = \tilde{p}(x)$ at $n + 1$ different real numbers $x$, then $c_k = d_k$ for every
$k = 0, 1, \dots, n$, and so $p(x) = \tilde{p}(x)$ for every real $x$.

In particular, a polynomial can be written in the form of [](#def-calc-polynomial) in only one
way, apart from terms with coefficient $0$: its coefficients, and its degree, are determined by
its values.
:::

:::{proof:proof}
:enumerated: false
The difference $p - \tilde{p}$ has $n + 1$ roots, which is too many for any polynomial of degree
at most $n$.

Let $D(x) = p(x) - \tilde{p}(x) = (c_n - d_n)x^n + \dots + (c_1 - d_1)x + (c_0 - d_0)$. Suppose
that $c_k \ne d_k$ for some $k$, and let $m$ be the largest such $k$. Then $D$ has degree $m$,
with leading coefficient $c_m - d_m$, and $m \le n$. Every number at which $p$ and $\tilde{p}$
agree is a root of $D$, so $D$ has at least $n + 1 > m$ roots, which contradicts
[](#thm-calc-polynomial-roots-bound). So $c_k = d_k$ for every $k$, and then $p$ and $\tilde{p}$
are the same formula, so they agree at every real $x$.

For the last statement, suppose one function is given by two such formulas. Writing the shorter
one with extra terms $0 \cdot x^k$, both have the same $n$, and they agree at every real number,
in particular at $n + 1$ of them. So their coefficients are equal.
:::

**In words.** Two polynomials of degree at most $n$ that agree at $n + 1$ points agree
everywhere, and have the same coefficients. So we may **compare coefficients**: if
$ax^2 + bx + c = 2x^2 - 5$ for every $x$, then $a = 2$, $b = 0$ and $c = -5$.

::::{figure}
:label: wdg-calc-polynomial-rational-cubic-roots

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "x^3 - 3*x + c",
  "xRange": [-3, 3],
  "yRange": [-6, 6],
  "parameters": { "c": { "value": 0, "min": -4, "max": 4, "step": 0.5 } }
}
```

Graph of $y = x^3 - 3x + c$ for $-3 \le x \le 3$, with a slider for $c$ from ${-4}$ to $4$ in
steps of $0.5$, starting at $c = 0$. At $c = 0$ the graph crosses the $x$-axis at
$x = -\sqrt{3}$, $x = 0$ and $x = \sqrt{3}$, the roots of $x^3 - 3x = x(x^2 - 3)$. At $c = 2$
it meets the $x$-axis only at $x = {-2}$ and $x = 1$, the roots of
$x^3 - 3x + 2 = (x - 1)^2 (x + 2)$; at $x = 1$ it touches the axis without crossing it. For
every $c$ the polynomial has degree $3$, so it has at most three roots.
::::

**Try this:** move $c$ through its whole range. For which values of $c$ on the slider does the
graph meet the $x$-axis three times, and for which only once? Can you find a $c$ for which it
meets the axis four times? [](#thm-calc-polynomial-roots-bound) says why not, for every real
$c$, not only those on the slider.

### Division of polynomials

Integers can be divided with a remainder: $17 = 5 \cdot 3 + 2$, with a remainder $2$ smaller
than the divisor $3$. Polynomials can be divided in the same way, with "smaller" measured by the
degree.

:::{proof:theorem} Division of polynomials
:label: thm-calc-polynomial-division

Let $f$ and $g$ be polynomials, where $g$ is not the zero polynomial. Then there are polynomials
$q$ and $r$ such that, for every real $x$,
$$
f(x) = g(x)\, q(x) + r(x),
$$
and $r$ is the zero polynomial or has smaller degree than $g$. The polynomials $q$ and $r$ are
unique; they are called the **quotient** and the **remainder** of $f$ divided by $g$.
:::

:::{proof:proof} Sketch
:enumerated: false
Long division removes the leading term of $f$, one term at a time. If $f$ is the zero
polynomial or has smaller degree than $g$, then $q = 0$ and $r = f$ work. Otherwise let
$a x^k$ be the leading term of $f$ and $b x^m$ that of $g$, with $k \ge m$. Subtracting
$\frac{a}{b} x^{k - m} g(x)$, whose leading term is $a x^k$
([](#prop-calc-polynomial-degree-product)), from $f(x)$ cancels the leading
term of $f$ and leaves a polynomial $f_1$ that is zero or has degree less than $k$. Repeat with
$f_1$ in place of $f$. The degree drops at every step, so after at most $k - m + 1$ steps what is
left is zero or has degree less than $m$: that is $r$, and $q$ is the sum of the terms
$\frac{a}{b} x^{k - m}$ that were subtracted. The first worked example below shows the steps.

*This sketch leaves out the induction on the degree of $f$ that makes "repeat" into a proof.
Uniqueness is proved in the rigorous track below, from
[](#cor-calc-polynomial-identity).*
:::

**In words.** The remainder is what is left when no more multiples of $g$ can be subtracted
without raising the degree. When $r$ is the zero polynomial, $g$ is a factor of $f$:
$f(x) = g(x)\, q(x)$. Dividing by $g(x) = x - a$, part (a) of [](#thm-calc-factor-theorem)
gives the quotient and the remainder at once: $p(x) = (x - a)\, q(x) + p(a)$, and the
remainder is the constant $p(a)$ ([](#exr-calc-polynomial-rational-remainder)).

### Domain, zeros and sign of a rational function

:::{proof:proposition} Domain and zeros of a rational function
:label: prop-calc-rational-domain

Let $f(x) = \frac{p(x)}{q(x)}$ be a rational function, where $q$ has degree $m$.

(a) $\dom f$ is $\R$ without the roots of $q$, and $q$ has at most $m$ roots. So $\dom f$ leaves
out at most $m$ real numbers.

(b) For every real number $a$ there is an open interval $(\alpha, \beta)$ containing $a$ such
that $f$ is defined at every point of $(\alpha, \beta)$, except possibly at $a$. If
$q(a) \ne 0$, then $f$ is defined at every point of $(\alpha, \beta)$.

(c) For $x \in \dom f$, $f(x) = 0$ exactly when $p(x) = 0$. So the zeros of $f$ are the roots of
$p$ that are not roots of $q$.
:::

:::{proof:proof}
:enumerated: false
Parts (a) and (c) come straight from the definition of a rational function, with the bound on
the number of roots and the sign rules; for (b) we choose an interval around $a$ that no other
root of $q$ reaches.

(a) By [](#def-calc-rational-function), $\dom f = \{x \in \R : q(x) \ne 0\}$, which is $\R$
without the roots of $q$. Since $q$ is not the zero polynomial, it has a degree $m$, and by
[](#thm-calc-polynomial-roots-bound) it has at most $m$ roots.

(b) We squeeze an interval around $a$ between the roots of $q$ nearest to $a$. By (a), the roots
of $q$ other than $a$ are finitely many. If some of them are less than $a$, let $\alpha$ be the
largest of these; otherwise let $\alpha = a - 1$. If some are greater than $a$, let $\beta$ be the
smallest of these; otherwise let $\beta = a + 1$. Then $\alpha < a < \beta$, so $a$ lies in
$(\alpha, \beta)$. No root of $q$ other than $a$ lies in $(\alpha, \beta)$: a root less than $a$
is at most $\alpha$, and a root greater than $a$ is at least $\beta$. So every $x$ in
$(\alpha, \beta)$ with $x \ne a$ has $q(x) \ne 0$, that is, $x \in \dom f$. If moreover
$q(a) \ne 0$, then $a \in \dom f$ as well.

(c) For $x \in \dom f$ we have $q(x) \ne 0$, so by
[part (a) of the sign rules](#prop-calc-sign-rules), $\frac{p(x)}{q(x)} = 0$ exactly when
$p(x) = 0$.
:::

**In words.** A rational function is defined everywhere except at finitely many points, the
roots of the denominator, and around each point $a$ it is defined on a whole open interval,
except perhaps at $a$ itself. It is zero exactly where the numerator is zero and the denominator
is not.

Its sign can be read off its factors. A polynomial such as $x^2 + 1$ is positive at every real
number: $x^2 \ge 0$ and $1 > 0$ by [part (c) of the sign rules](#prop-calc-sign-rules), adding
$1$ to both sides gives $x^2 + 1 \ge 1$ ([property 3 of the order rules](#rem-calc-order-rules)),
and so $x^2 + 1 > 0$ (property 2).

:::{proof:proposition} Sign of a factored rational function
:label: prop-calc-rational-sign

Let
$$
f(x) = \frac{K\, N(x)\, P(x)}{D(x)\, Q(x)} ,
$$
where:

- $K \ne 0$ is a constant;
- $N(x) = (x - r_1) \cdots (x - r_k)$ and $D(x) = (x - s_1) \cdots (x - s_m)$ are products of
  linear factors, with $k, m \in \N$ and real numbers $r_1, \dots, r_k$, $s_1, \dots, s_m$, not
  necessarily different (for $k = 0$ or $m = 0$ the empty product is read as $1$);
- $P$ and $Q$ are polynomials with $P(x) > 0$ and $Q(x) > 0$ for every real $x$ (either may be
  the constant $1$).

Let $I$ be an open interval that contains none of the numbers $r_1, \dots, r_k$,
$s_1, \dots, s_m$. Then:

- $f$ is defined at every point of $I$, and is not zero there;
- $f$ has the same sign at every point of $I$: positive if, at one point $x$ of $I$, an even
  number of the numbers $K$, $x - r_1, \dots, x - r_k$, $x - s_1, \dots, x - s_m$ are negative,
  and negative if an odd number are.
:::

:::{proof:proof}
:enumerated: false
On $I$ each factor keeps one sign, and then [part (d) of the sign rules](#prop-calc-sign-rules)
decides the sign of $f$.

Let $t$ be one of the numbers $r_i$ or $s_j$. We show that $x - t$ is non-zero and has the same
sign at every $x \in I$. By [](#def-calc-interval), the open interval $I$ is one of
$(\alpha, \beta)$, $(\alpha, \infty)$, $(-\infty, \beta)$ and $\R$, for real $\alpha < \beta$. It
is not $\R$, which contains $t$.

- If $I = (\alpha, \beta) = \{x \in \R : \alpha < x < \beta\}$, then $t \notin I$ means that
  $\alpha < t < \beta$ fails, so $t \le \alpha$ or $t \ge \beta$
  ([property 7 of the order rules](#rem-calc-order-rules)). If $t \le \alpha$, every
  $x \in I$ satisfies $t \le \alpha < x$, so $x > t$ by transitivity (property 2), and
  $x - t > 0$ by [part (b) of the sign rules](#prop-calc-sign-rules). If $t \ge \beta$, every
  $x \in I$ satisfies $x < \beta \le t$, so $x - t < 0$.
- If $I = (\alpha, \infty)$, then $t \notin I$ means $t \le \alpha$, and every $x \in I$ has
  $x - t > 0$, as in the first case above. If $I = (-\infty, \beta)$, then $t \ge \beta$, and
  every $x \in I$ has $x - t < 0$.

So at every $x \in I$, each factor $x - r_i$ and $x - s_j$ is non-zero, with the same sign at
every point of $I$; $P(x)$ and $Q(x)$ are positive; and $K \ne 0$. The denominator is a product
of non-zero numbers, so it is not $0$, by part (a) of the sign rules (applied to one factor
after another), and $x \in \dom f$. By part (d) of the sign rules, $f(x)$ is positive if an even
number of the factors are negative and negative if an odd number are; $P(x)$ and $Q(x)$ are
positive, so they do not change the count. In particular $f(x) \ne 0$. Since every factor has
the same sign at every point of $I$, the count, and with it the sign of $f$, is the same at
every point of $I$.
:::

**In words: the sign chart.** To find the sign of a rational function:

1. Factor the numerator and the denominator into a constant, linear factors $x - t$, and
   factors that are positive everywhere, such as $x^2 + 1$.
2. Mark every number $t$ of a linear factor on the number line. They cut it into open
   intervals, and on each of them $f$ has one sign ([](#prop-calc-rational-sign)).
3. On each interval, count the negative factors at one point of it (or compute $f$ there).
4. At the marked numbers themselves, $f$ is $0$ where the numerator is $0$ and the denominator
   is not, and undefined where the denominator is $0$ ([](#prop-calc-rational-domain)).

## Worked examples

### Dividing and factoring

:::{proof:example} Divide $2x^3 - 3x^2 + 4x - 1$ by $x^2 + 1$
:label: eg-calc-polynomial-rational-division

**Goal.** Find the quotient $q$ and the remainder $r$ of
[](#thm-calc-polynomial-division) for $f(x) = 2x^3 - 3x^2 + 4x - 1$ and $g(x) = x^2 + 1$, of
degree $2$.

1. **Cancel $2x^3$.** The leading terms give $\frac{2x^3}{x^2} = 2x$. Subtracting
   $2x \cdot g(x) = 2x^3 + 2x$ from $f(x)$ leaves $-3x^2 + 2x - 1$.
2. **Cancel $-3x^2$.** Now $\frac{-3x^2}{x^2} = -3$. Subtracting $-3 \cdot g(x) = -3x^2 - 3$
   from $-3x^2 + 2x - 1$ leaves $2x + 2$.
3. **Stop.** $2x + 2$ has degree $1$, less than the degree $2$ of $g$. The quotient is the sum
   of the multipliers, $2x - 3$, and the remainder is $2x + 2$.

$$
\boxed{
\begin{aligned}
q(x) &= 2x - 3, \\
r(x) &= 2x + 2
\end{aligned}
}
$$

That is, $2x^3 - 3x^2 + 4x - 1 = (x^2 + 1)(2x - 3) + (2x + 2)$ for every real $x$.

**Check.** At $x = 1$: the left-hand side is $2 - 3 + 4 - 1 = 2$, and the right-hand side is
$2 \cdot ({-1}) + 4 = 2$. ✓ At $x = 0$: ${-1}$ on the left and $1 \cdot ({-3}) + 2 = -1$ on the
right. ✓ Multiplying out, $(x^2 + 1)(2x - 3) = 2x^3 - 3x^2 + 2x - 3$, and adding $2x + 2$
gives $f(x)$. ✓
:::

:::{proof:example} Factor $x^3 - 2x^2 - 5x + 6$ completely
:label: eg-calc-polynomial-rational-factor-cubic

**Goal.** Write $p(x) = x^3 - 2x^2 - 5x + 6$ as a product of linear factors, and find all its
roots.

1. **Find one root.** We try small integers
   ([](#exr-calc-polynomial-rational-integer-root) shows why the divisors of the constant term
   $6$ are the only integers worth trying): $p(1) = 1 - 2 - 5 + 6 = 0$. So, by
   [](#thm-calc-factor-theorem) (b), $x - 1$ is a factor.
2. **Divide by $x - 1$**, as in [](#eg-calc-polynomial-rational-division). Each step cancels
   the leading term of what is left:
   - subtracting $x^2 (x - 1)$ from $p(x)$ leaves $-x^2 - 5x + 6$;
   - subtracting $-x\,(x - 1)$ from that leaves $-6x + 6$;
   - subtracting $-6\,(x - 1)$ from that leaves $0$.

   The remainder is $0$, and the quotient is $x^2 - x - 6$: $p(x) = (x - 1)(x^2 - x - 6)$. The
   quotient has degree $2$ and leading coefficient $1$, as part (a) of the factor theorem says.
3. **Factor the quadratic.** Two numbers with product ${-6}$ and sum ${-1}$ are ${-3}$ and $2$,
   so $x^2 - x - 6 = (x - 3)(x + 2)$.
4. **The roots.** By [part (a) of the sign rules](#prop-calc-sign-rules), applied twice,
   $p(x) = 0$ exactly when one of the factors is $0$: at $x = 1$, $3$ or ${-2}$. These are all
   the roots, as [](#thm-calc-polynomial-roots-bound) also confirms: a cubic has at most three.

$$
\boxed{p(x) = (x - 1)(x - 3)(x + 2)}
$$

**Check.** $p(3) = 27 - 18 - 15 + 6 = 0$ ✓ and $p(-2) = -8 - 8 + 10 + 6 = 0$. ✓ The constant
term of the product is $({-1})({-3})(2) = 6$. ✓
:::

:::{proof:example} The factor $x - 1$ of $p(x) - p(1)$
:label: eg-calc-polynomial-rational-difference-quotient

**Goal.** For $p(x) = 2x^3 - 5x + 1$, find the polynomial $q$ of [](#thm-calc-factor-theorem)
(a) with $p(x) - p(1) = (x - 1)\, q(x)$, and simplify $\frac{p(x) - p(1)}{x - 1}$ for $x \ne 1$.

1. **The difference.** $p(1) = 2 - 5 + 1 = -2$, so $p(x) - p(1) = 2x^3 - 5x + 3$, which is
   $2(x^3 - 1) - 5(x - 1)$.
2. **Take out $x - 1$**, as in the proof of the factor theorem. Since
   $x^3 - 1 = (x - 1)(x^2 + x + 1)$, the difference is
   $2(x - 1)(x^2 + x + 1) - 5(x - 1)$, and taking out the common factor $x - 1$ gives
   $p(x) - p(1) = (x - 1)(2x^2 + 2x - 3)$. So $q(x) = 2x^2 + 2x - 3$: degree $2$ and leading coefficient $2$, as part (a) says.
3. **Simplify.** For $x \ne 1$ the number $x - 1$ is not $0$, so we may divide by it:
   $\frac{p(x) - p(1)}{x - 1} = 2x^2 + 2x - 3$. The polynomial on the right is also defined at
   $x = 1$, where it is $2 + 2 - 3 = 1$.

$$
\boxed{q(x) = 2x^2 + 2x - 3}
$$

and $\frac{p(x) - p(1)}{x - 1} = q(x)$ for every $x \ne 1$.

**Check.** At $x = 0$: $p(0) - p(1) = 1 + 2 = 3$, and $(0 - 1)(0 + 0 - 3) = 3$. ✓ At $x = 2$:
$p(2) = 16 - 10 + 1 = 7$, so $p(2) - p(1) = 9$, and $(2 - 1)(8 + 4 - 3) = 9$. ✓
:::

:::{admonition} Looking ahead
:class: looking-ahead
The number $q(1) = 1$ is the slope of the tangent line to the graph of $p$ at $x = 1$. The page
Tangent Lines and Rates of Change explains why, and the Derivatives chapter computes such slopes
with rules instead of division.
:::

### Domain, zeros and sign

:::{proof:example} The sign of $\frac{x^2 - 1}{x^2 - x - 6}$
:label: eg-calc-polynomial-rational-sign-chart

**Goal.** For $f(x) = \dfrac{x^2 - 1}{x^2 - x - 6}$, find the domain, the zeros, and the
intervals where $f$ is positive or negative.

1. **Factor.** $x^2 - 1 = (x - 1)(x + 1)$ and $x^2 - x - 6 = (x - 3)(x + 2)$, so
   $$
   f(x) = \frac{(x - 1)(x + 1)}{(x - 3)(x + 2)} .
   $$
2. **Domain.** By [part (a) of the sign rules](#prop-calc-sign-rules), the denominator is $0$
   exactly when $x = 3$ or $x = -2$. So
   $\dom f = (-\infty, -2) \cup (-2, 3) \cup (3, \infty)$.
3. **Zeros.** By [](#prop-calc-rational-domain) (c), the zeros are the roots of the numerator
   that lie in the domain: $x = 1$ and $x = -1$.
4. **Sign.** The numbers ${-2}$, ${-1}$, $1$ and $3$ cut $\R$ into five open intervals, and on
   each of them $f$ has one sign, by [](#prop-calc-rational-sign) (here $K = 1$ and
   $P = Q = 1$). We count the negative factors, using
   [part (b) of the sign rules](#prop-calc-sign-rules): a factor $x - t$ is negative exactly to
   the left of $t$.

   | Interval | $x + 2$ | $x + 1$ | $x - 1$ | $x - 3$ | $f(x)$ |
   |---|---|---|---|---|---|
   | $(-\infty, -2)$ | $-$ | $-$ | $-$ | $-$ | $+$ |
   | $(-2, -1)$ | $+$ | $-$ | $-$ | $-$ | $-$ |
   | $(-1, 1)$ | $+$ | $+$ | $-$ | $-$ | $+$ |
   | $(1, 3)$ | $+$ | $+$ | $+$ | $-$ | $-$ |
   | $(3, \infty)$ | $+$ | $+$ | $+$ | $+$ | $+$ |

   Four, two and zero negative factors give $+$; three and one give $-$.

**Result.**

- $f(x) > 0$ on $(-\infty, -2)$, on $(-1, 1)$ and on $(3, \infty)$;
- $f(x) < 0$ on $(-2, -1)$ and on $(1, 3)$;
- $f(x) = 0$ at $x = -1$ and $x = 1$, and $f$ is undefined at $x = -2$ and $x = 3$.

**Check.** $f(0) = \frac{-1}{-6} = \frac{1}{6} > 0$, and $0$ lies in $(-1, 1)$. ✓
$f(2) = \frac{3}{-4} < 0$, and $2$ lies in $(1, 3)$. ✓ $f(4) = \frac{15}{6} > 0$. ✓
:::

::::{figure}
:label: wdg-calc-polynomial-rational-sign-chart

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "(x^2 - 1)/(x^2 - x - 6)",
  "xRange": [-5, 6],
  "yRange": [-5, 5],
  "table": { "points": [-3, -1.5, 0, 2, 4] }
}
```

Graph of $y = \frac{x^2 - 1}{x^2 - x - 6}$ for $-5 \le x \le 6$. It has gaps at $x = {-2}$ and
$x = 3$, where the function is undefined, and next to them it is steep and leaves the view. It
meets the $x$-axis at $x = {-1}$ and $x = 1$. A table lists the values at $x = {-3}$, ${-1.5}$,
$0$, $2$ and $4$, one point in each interval of the sign chart. The exact values are
$\frac{4}{3}$, ${-\frac{5}{9}}$, $\frac{1}{6}$, ${-\frac{3}{4}}$ and $\frac{5}{2}$: positive,
negative, positive, negative, positive, as the sign chart of
[](#eg-calc-polynomial-rational-sign-chart) predicts.
::::

**Try this:** before you look at the table, predict from the factors whether the graph lies above
or below the $x$-axis on each of the five intervals. Then compare with the graph. The graph and the
table show finitely many points; the sign chart, by [](#prop-calc-rational-sign), covers every
point of each interval.

:::{proof:example} The least material for a box
:label: eg-calc-polynomial-rational-box

**Goal.** An open box (no lid) has a square base of side $x$ metres and a volume of $4$ cubic
metres. Show that it needs at least $12$ square metres of material, and find the only box that
needs exactly $12$.

1. **Model.** Let $h$ be the height in metres. The volume is $x^2 h = 4$, so $h = \frac{4}{x^2}$.
   The base has area $x^2$ and each of the four sides $xh = \frac{4}{x}$, so the area of
   material, in square metres, is
   $$
   S(x) = x^2 + \frac{16}{x} .
   $$
   A box needs $x > 0$, so the domain is $(0, \infty)$, from the situation.
2. **Compare with $12$.** Over a common denominator,
   $$
   S(x) - 12 = \frac{x^3 - 12x + 16}{x} .
   $$
3. **Factor the numerator.** At $x = 2$ it is $8 - 24 + 16 = 0$, so $x - 2$ is a factor
   ([](#thm-calc-factor-theorem) (b)). Dividing by $x - 2$:
   - subtracting $x^2 (x - 2)$ from $x^3 - 12x + 16$ leaves $2x^2 - 12x + 16$;
   - subtracting $2x\,(x - 2)$ from that leaves $-8x + 16$;
   - subtracting $-8\,(x - 2)$ from that leaves $0$.

   So $x^3 - 12x + 16 = (x - 2)(x^2 + 2x - 8)$, and $x^2 + 2x - 8 = (x - 2)(x + 4)$.
4. **Sign on $(0, \infty)$.** By step 3, $S(x) - 12$ is
   $$
   \frac{(x - 2)(x - 2)(x + 4)}{x} .
   $$
   For $x > 0$, the factors $x$ and $x + 4$ are positive ($x > 0 > -4$, and
   [part (b) of the sign rules](#prop-calc-sign-rules)). On $(0, 2)$ both factors $x - 2$ are
   negative, and on $(2, \infty)$ both are positive. So on each of these intervals an even
   number of factors is negative, and $S(x) - 12 > 0$ there, by
   [](#prop-calc-rational-sign). At $x = 2$ the numerator is $0$, so $S(2) = 12$.

$$
\boxed{S(x) \ge 12}
$$

for every $x > 0$, with $S(x) = 12$ only at $x = 2$. So every such box needs at least $12$ square metres of material, and the only box that needs
exactly $12$ has a base of side $2$ metres and a height of $h = \frac{4}{2^2} = 1$ metre.

**Check.** $S(1) = 1 + 16 = 17$, $S(2) = 4 + 8 = 12$ and $S(4) = 16 + 4 = 20$: all at least
$12$. ✓ The box with $x = 2$ and $h = 1$ has volume $2^2 \cdot 1 = 4$. ✓ Units: the area is a
sum of products of two lengths in metres, so it is in square metres. ✓
:::

## Common mistakes

:::{warning} Multiplying an inequality by a factor of unknown sign
✗ **Wrong:** "$\dfrac{x + 3}{x - 1} < 2$. Multiplying by $x - 1$ gives $x + 3 < 2x - 2$, so
$x > 5$."

**Why:** multiplying by $x - 1$ keeps the inequality only where $x - 1 > 0$. For $x < 1$ the
factor is negative and reverses it
([property 5(a) and (c) of the order rules](#rem-calc-order-rules)).
The answer $x > 5$ misses, for example, $x = 0$, where $\frac{0 + 3}{0 - 1} = -3 < 2$.

✓ **Right:** subtract $2$ and use one fraction:
$\frac{x + 3}{x - 1} - 2 = \frac{5 - x}{x - 1} = \frac{(-1)(x - 5)}{x - 1}$. Its sign chart
([](#prop-calc-rational-sign), with $K = -1$) gives $\frac{5 - x}{x - 1} < 0$ exactly on
$(-\infty, 1) \cup (5, \infty)$.
:::

:::{warning} "The sign changes at every zero"
✗ **Wrong:** "$p(x) = (x - 1)^2 (x + 2)$ is positive on $(-2, 1)$, so it is negative on
$(1, \infty)$."

**Why:** the factor $x - 1$ occurs twice. Passing $x = 1$, both copies change sign, so the
number of negative factors changes by two, and the sign of $p$ does not change.

✓ **Right:** count the negative factors on each interval: on $(1, \infty)$ there are none, so
$p(x) > 0$ there. Indeed $p(2) = 1 \cdot 4 = 4 > 0$.
:::

:::{warning} "Degree $n$ means $n$ roots"
✗ **Wrong:** "$x^2 + 1$ has degree $2$, so it has two roots."

**Why:** [](#thm-calc-polynomial-roots-bound) says *at most* $n$. The polynomial $x^2 + 1$ is
at least $1$ at every real number, so it has no roots at all, and $(x - 1)^2$ has only the root
$1$.

✓ **Right:** a polynomial of degree $n$ has at most $n$ roots; it may have fewer.
:::

:::{warning} "The zeros of the numerator are the zeros of the function"
✗ **Wrong:** "$f(x) = \dfrac{x^2 - 4}{x^2 - 3x + 2}$ has the zeros $2$ and ${-2}$."

**Why:** the denominator $x^2 - 3x + 2 = (x - 1)(x - 2)$ is $0$ at $x = 2$, so $2 \notin \dom f$:
$f(2)$ is not a number at all, let alone $0$.

✓ **Right:** the zeros are the roots of the numerator that lie in the domain
([](#prop-calc-rational-domain) (c)): here only ${-2}$, where
$f(-2) = \frac{0}{12} = 0$.
:::

## Rigorous track

:::{admonition} Why the quotient and the remainder are unique
:class: dropdown rigor
This is the part of [](#thm-calc-polynomial-division) that its sketch leaves to this section.
We subtract two divisions of $f$ by $g$ from each other and compare the coefficients of the
highest power of $x$ on the two sides.

Let $g$ have degree $m$ and leading coefficient $b$, and suppose that
$$
\begin{aligned}
f(x) &= g(x)\, q_1(x) + r_1(x) \\
&= g(x)\, q_2(x) + r_2(x)
\end{aligned}
$$
for every real $x$, where each of $r_1$ and $r_2$ is the zero polynomial or has degree less than
$m$. Then, for every real $x$,
$$
\begin{aligned}
&g(x)\,\bigl(q_1(x) - q_2(x)\bigr) \\
&\quad = r_2(x) - r_1(x).
\end{aligned}
$$
On the right is a polynomial in which no power $x^j$ with $j \ge m$ has a non-zero coefficient.
Suppose $q_1 - q_2$ were not the zero polynomial, say of degree $k$ with leading coefficient
$e \ne 0$. Then the left-hand side would be a polynomial of degree $m + k$, with leading
coefficient $be \ne 0$, by [](#prop-calc-polynomial-degree-product). The two sides agree at
every real number, so by [](#cor-calc-polynomial-identity) they have the same coefficients.
But the coefficient of $x^{m + k}$, where $m + k \ge m$, is $be \ne 0$ on the left
and $0$ on the right. So $q_1 - q_2$ is the zero polynomial: $q_1(x) = q_2(x)$ for every $x$,
and then $r_1(x) = r_2(x)$ for every $x$ as well.
:::

:::{admonition} The degree of the zero polynomial
:class: dropdown rigor
The zero polynomial has no highest power with a non-zero coefficient, so it has no degree.
Some books give it the degree ${-\infty}$, with the convention $-\infty + n = -\infty$, so that
"the degree of a product is the sum of the degrees" holds for every pair of polynomials. We
avoid the convention and state the zero polynomial separately instead. It is the one polynomial
that [](#thm-calc-polynomial-roots-bound) must leave out: every real number is a root of it.
:::

:::{admonition} Looking ahead
:class: looking-ahead
The sign chart needs a factorisation. For a polynomial we cannot factor by hand, such as
$x^3 - 3x + 1$, it is still true that the sign does not change between consecutive roots, but
the proof needs the intermediate value theorem, on the page The Intermediate Value Theorem. And
not every polynomial splits into linear factors over $\R$: $x^2 + 1$ has no real roots. The
page Complex Numbers finds the roots of such quadratics among the complex numbers.
:::

## Summary

- A polynomial $c_n x^n + \dots + c_1 x + c_0$ with $c_n \ne 0$ has degree $n$; its values
  determine its coefficients ([](#cor-calc-polynomial-identity)). The degree of a product is
  the sum of the degrees ([](#prop-calc-polynomial-degree-product)). A rational function
  $\frac{p(x)}{q(x)}$ is defined exactly where $q(x) \ne 0$.
- **Factor theorem** ([](#thm-calc-factor-theorem)): $p(x) - p(a) = (x - a)\, q(x)$ for a
  polynomial $q$ of degree one less, so
  $$
  \frac{p(x) - p(a)}{x - a} = q(x) \quad (x \ne a),
  $$
  and $a$ is a root of $p$ exactly when $x - a$ is a factor.
- A polynomial of degree $n$ has at most $n$ roots ([](#thm-calc-polynomial-roots-bound)).
- Division: $f = gq + r$ with $r$ zero or of smaller degree than $g$
  ([](#thm-calc-polynomial-division)); subtract multiples of $g$ to cancel leading terms.
- Signs: only the number of negative factors matters ([](#prop-calc-sign-rules)). A factored
  rational function has one sign on each interval between the numbers of its linear factors
  ([](#prop-calc-rational-sign)). Never multiply an inequality by a factor of unknown sign.

## Exercises

::::{exercise} Degree and leading coefficient
:label: exr-calc-polynomial-rational-degree
:class: tier-a

Find (a) the degree and (b) the leading coefficient of the polynomial
$p(x) = (2x - 1)(x^2 + 3) - 2x^3$.

:::{admonition} Hint 1
:class: dropdown hint
Multiply out first. What happens to the terms in $x^3$?
:::

:::{admonition} Answer
:class: dropdown answer
(a) $2$ (b) $-1$
:::
::::

::::{solution} exr-calc-polynomial-rational-degree
:label: sol-calc-polynomial-rational-degree
:class: dropdown
Multiplying out, $(2x - 1)(x^2 + 3) = 2x^3 - x^2 + 6x - 3$. Subtracting $2x^3$ cancels the
$x^3$ term, so
$$
p(x) = -x^2 + 6x - 3 .
$$
The highest power with a non-zero coefficient is $x^2$, with coefficient ${-1}$. So (a) the degree
is $2$ and (b) the leading coefficient is ${-1}$. The product alone has degree $3$, but
subtracting $2x^3$ cancels its leading term.
::::

::::{exercise} A factor or not?
:label: exr-calc-polynomial-rational-factor-check
:class: tier-a

True or false: $x - 2$ is a factor of $p(x) = x^4 - 3x^3 + x + 6$.

:::{admonition} Hint 1
:class: dropdown hint
Use [](#thm-calc-factor-theorem) (b): compute $p(2)$.
:::

:::{admonition} Answer
:class: dropdown answer bool
True
:::
::::

::::{solution} exr-calc-polynomial-rational-factor-check
:label: sol-calc-polynomial-rational-factor-check
:class: dropdown
$p(2) = 16 - 24 + 2 + 6 = 0$, so $2$ is a root of $p$, and by [](#thm-calc-factor-theorem) (b),
$x - 2$ is a factor of $p$. Dividing gives $p(x) = (x - 2)(x^3 - x^2 - 2x - 3)$, as multiplying
out confirms.
::::

::::{exercise} The domain of a rational function
:label: exr-calc-polynomial-rational-domain
:class: tier-a

Find the domain of the rational function $f(x) = \dfrac{x + 3}{x^2 + x - 6}$.

:::{admonition} Hint 1
:class: dropdown hint
Factor the denominator. Does a common factor with the numerator change the domain?
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, -3), (-3, 2), (2, \infty)$ (the union of these three intervals)
:::
::::

::::{solution} exr-calc-polynomial-rational-domain
:label: sol-calc-polynomial-rational-domain
:class: dropdown
The denominator is $x^2 + x - 6 = (x + 3)(x - 2)$. By
[part (a) of the sign rules](#prop-calc-sign-rules) it is $0$ exactly when $x = -3$ or $x = 2$,
and by [](#def-calc-rational-function) these two numbers are left out of the domain:
$\dom f = (-\infty, -3) \cup (-3, 2) \cup (2, \infty)$. The numerator is also $0$ at $x = -3$, but that does not help: the formula gives $\frac{0}{0}$
there, which is not a number. For $x$ in the domain, $f(x) = \frac{1}{x - 2}$, but the function
$\frac{1}{x - 2}$ has a larger domain, so it is a different function.
::::

::::{exercise} The zeros of a rational function
:label: exr-calc-polynomial-rational-zeros
:class: tier-a

Find all the zeros of $f(x) = \dfrac{x^2 - 9}{x^2 + 2x - 3}$.

:::{admonition} Hint 1
:class: dropdown hint
Find the domain first. Which roots of the numerator lie in it?
:::

:::{admonition} Answer
:class: dropdown answer set
$3$
:::
::::

::::{solution} exr-calc-polynomial-rational-zeros
:label: sol-calc-polynomial-rational-zeros
:class: dropdown
The denominator is $x^2 + 2x - 3 = (x + 3)(x - 1)$, which is $0$ at $x = -3$ and $x = 1$, so
these are not in the domain. The numerator is $x^2 - 9 = (x - 3)(x + 3)$, with roots $3$ and
${-3}$. By [](#prop-calc-rational-domain) (c), the zeros of $f$ are the roots of the numerator
that lie in the domain: only $3$. Indeed $f(3) = \frac{0}{12} = 0$, while $f(-3)$ is
undefined.
::::

::::{exercise} Long division
:label: exr-calc-polynomial-rational-division
:class: tier-b

Divide $f(x) = x^4 + 2x^2 - x + 3$ by $g(x) = x^2 - x + 1$: find (a) the quotient and (b) the
remainder.

:::{admonition} Hint 1
:class: dropdown hint
Follow [](#eg-calc-polynomial-rational-division). The first step subtracts $x^2 \cdot g(x)$.
:::

:::{admonition} Hint 2
:class: dropdown hint
$f$ has no $x^3$ term: its coefficient is $0$.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $x^2 + x + 2$ (b) $1$
:::
::::

::::{solution} exr-calc-polynomial-rational-division
:label: sol-calc-polynomial-rational-division
:class: dropdown
Each step cancels the leading term of what is left:

- subtracting $x^2\, g(x) = x^4 - x^3 + x^2$ from $f(x)$ leaves $x^3 + x^2 - x + 3$;
- subtracting $x\, g(x) = x^3 - x^2 + x$ from that leaves $2x^2 - 2x + 3$;
- subtracting $2\, g(x) = 2x^2 - 2x + 2$ from that leaves $1$.

What is left has degree $0$, less than the degree $2$ of $g$, so we stop. The quotient is the
sum of the multipliers, $x^2 + x + 2$, and the remainder is $1$: for every real $x$,
$x^4 + 2x^2 - x + 3 = (x^2 - x + 1)(x^2 + x + 2) + 1$. At $x = 1$: $f(1) = 5$, and
$1 \cdot 4 + 1 = 5$.
::::

::::{exercise} Factoring with a known root
:label: exr-calc-polynomial-rational-factor-cubic
:class: tier-b

Let $p(x) = 2x^3 - 3x^2 - 11x + 6$. Check that $p(3) = 0$, and write $p(x)$ as a product of
linear factors.

:::{admonition} Hint 1
:class: dropdown hint
Divide by $x - 3$, as in [](#eg-calc-polynomial-rational-factor-cubic).
:::

:::{admonition} Hint 2
:class: dropdown hint
The quotient is a quadratic with leading coefficient $2$. Look for a factorisation
$(2x + u)(x + v)$.
:::

:::{admonition} Answer
:class: dropdown answer
$(x - 3)(2x - 1)(x + 2)$
:::
::::

::::{solution} exr-calc-polynomial-rational-factor-cubic
:label: sol-calc-polynomial-rational-factor-cubic
:class: dropdown
$p(3) = 54 - 27 - 33 + 6 = 0$, so by [](#thm-calc-factor-theorem) (b), $x - 3$ is a factor.
Dividing by $x - 3$:

- subtracting $2x^2 (x - 3)$ from $p(x)$ leaves $3x^2 - 11x + 6$;
- subtracting $3x\,(x - 3)$ from that leaves $-2x + 6$;
- subtracting $-2\,(x - 3)$ from that leaves $0$.

So $p(x) = (x - 3)(2x^2 + 3x - 2)$. The quadratic factors as
$2x^2 + 3x - 2 = (2x - 1)(x + 2)$, as multiplying out confirms. So
$$
p(x) = (x - 3)(2x - 1)(x + 2),
$$
with the roots $3$, $\frac{1}{2}$ and ${-2}$.
::::

::::{exercise} The factor $x + 1$ of $p(x) - p(-1)$
:label: exr-calc-polynomial-rational-difference-quotient
:class: tier-b

Let $p(x) = x^3 - 2x$. Find (a) the polynomial $q$ with $p(x) - p(-1) = (x + 1)\, q(x)$ for
every real $x$, and (b) the value $q(-1)$.

:::{admonition} Hint 1
:class: dropdown hint
$x + 1 = x - (-1)$. Use [](#thm-calc-factor-theorem) (a) with $a = -1$, as in
[](#eg-calc-polynomial-rational-difference-quotient).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $x^2 - x - 1$ (b) $1$
:::
::::

::::{solution} exr-calc-polynomial-rational-difference-quotient
:label: sol-calc-polynomial-rational-difference-quotient
:class: dropdown
(a) $p(-1) = -1 + 2 = 1$, so $p(x) - p(-1) = x^3 - 2x - 1$. As in the proof of the factor
theorem, with $a = -1$, we write this as $\bigl(x^3 - (-1)^3\bigr) - 2\bigl(x - (-1)\bigr)$.
Since $x^3 - (-1)^3 = x^3 + 1 = (x + 1)(x^2 - x + 1)$, it is
$(x + 1)(x^2 - x + 1) - 2(x + 1)$, and taking out the common factor $x + 1$ gives
$p(x) - p(-1) = (x + 1)(x^2 - x - 1)$. So $q(x) = x^2 - x - 1$, of degree $2$ and leading coefficient $1$, as part (a) of the theorem
says.

(b) $q(-1) = 1 + 1 - 1 = 1$.
::::

::::{exercise} A remainder without dividing
:label: exr-calc-polynomial-rational-remainder
:class: tier-b

Find the remainder when $p(x) = x^{100} - 2x + 1$ is divided by $x - 1$.

:::{admonition} Hint 1
:class: dropdown hint
Part (a) of [](#thm-calc-factor-theorem) with $a = 1$ gives
$p(x) = (x - 1)\, q(x) + p(1)$. Is $p(1)$ the zero polynomial or a polynomial of degree $0$?
Compare with the degree of $x - 1$.
:::

:::{admonition} Answer
:class: dropdown answer
$0$
:::
::::

::::{solution} exr-calc-polynomial-rational-remainder
:label: sol-calc-polynomial-rational-remainder
:class: dropdown
By [](#thm-calc-factor-theorem) (a) with $a = 1$, there is a polynomial $q$ with
$p(x) = (x - 1)\, q(x) + p(1)$ for every real $x$. The constant $p(1)$ is the zero polynomial
or has degree $0$, less than the degree $1$ of $x - 1$, so by the uniqueness in
[](#thm-calc-polynomial-division) it is the remainder. Here $p(1) = 1 - 2 + 1 = 0$: the remainder
is $0$, and $x - 1$ is a factor of $p$.
::::

::::{exercise} A rational inequality
:label: exr-calc-polynomial-rational-inequality
:class: tier-b

Find all real numbers $x$ with $\dfrac{2x - 1}{x + 1} < 1$. Give the answer as an interval or a
union of intervals.

:::{admonition} Hint 1
:class: dropdown hint
Do not multiply by $x + 1$: its sign depends on $x$ (see Common mistakes).
:::

:::{admonition} Hint 2
:class: dropdown hint
Subtract $1$ from both sides and write the left-hand side as one fraction.
:::

:::{admonition} Answer
:class: dropdown answer set
$(-1, 2)$
:::
::::

::::{solution} exr-calc-polynomial-rational-inequality
:label: sol-calc-polynomial-rational-inequality
:class: dropdown
The left-hand side is defined for $x \ne -1$. Adding ${-1}$ to both sides keeps the inequality,
and so does adding $1$ back ([property 3 of the order rules](#rem-calc-order-rules)), so for
$x \ne -1$ the inequality holds exactly when
$\frac{2x - 1}{x + 1} - 1 < 0$. Over the common denominator $x + 1$, the numerator is
$2x - 1 - (x + 1) = x - 2$, so this says
$$
\frac{x - 2}{x + 1} < 0 .
$$
The numbers ${-1}$ and $2$ cut $\R$ into three open intervals, and by
[](#prop-calc-rational-sign) the quotient has one sign on each:

- on $(-\infty, -1)$ both factors are negative, so it is positive;
- on $(-1, 2)$ only $x - 2$ is negative, so it is negative;
- on $(2, \infty)$ neither is negative, so it is positive.

At $x = 2$ it is $0$, which is not less than $0$, and $x = -1$ is not in the domain. So the
inequality holds exactly on $(-1, 2)$. For example $x = 0$ gives $-1 < 1$, while $x = -2$ gives
$\frac{-5}{-1} = 5$, which is not less than $1$.
::::

::::{exercise} When is the dose effective?
:label: exr-calc-polynomial-rational-concentration
:class: tier-b applied

After a dose of a medicine, its concentration in the blood is
$$
c(t) = \frac{5t}{t^2 + 4}
$$
milligrams per litre, $t$ hours later ($t \ge 0$). The medicine works while the concentration is
above $1$ milligram per litre. For which times $t$ is that? Give the answer as an interval, in
hours.

:::{admonition} Hint 1
:class: dropdown hint
The denominator $t^2 + 4$ is positive for every $t$, so you may multiply by it.
:::

:::{admonition} Hint 2
:class: dropdown hint
You should reach $t^2 - 5t + 4 < 0$. Factor it.
:::

:::{admonition} Answer
:class: dropdown answer set
$(1, 4)$
:::
::::

::::{solution} exr-calc-polynomial-rational-concentration
:label: sol-calc-polynomial-rational-concentration
:class: dropdown
For every real $t$, $t^2 \ge 0$ ([part (c) of the sign rules](#prop-calc-sign-rules)), so
adding $4$ to both sides gives $t^2 + 4 \ge 4 > 0$
([property 3 of the order rules](#rem-calc-order-rules)). Multiplying by the positive number
$t^2 + 4$ keeps an inequality (property 5(a)), and multiplying by its reciprocal, also positive
(property 6), takes us back.
So $c(t) > 1$ holds exactly when
$$
5t > t^2 + 4 ,
$$
that is, after adding $-5t$ to both sides (property 3; adding $5t$ takes us back), when
$t^2 - 5t + 4 < 0$. Now
$t^2 - 5t + 4 = (t - 1)(t - 4)$. By [](#prop-calc-rational-sign) (with $K = 1$ and no
denominator): on $(-\infty, 1)$ both factors are negative and the product is positive; on
$(1, 4)$ only $t - 4$ is negative and the product is negative; on $(4, \infty)$ it is positive;
and at $t = 1$ and $t = 4$ it is $0$. So $c(t) > 1$ exactly for $1 < t < 4$, all of which
satisfy $t \ge 0$: the medicine works from $1$ hour to $4$ hours after the dose.

At $t = 2$, $c(2) = \frac{10}{8} = 1.25 > 1$; at $t = 1$, $c(1) = \frac{5}{5} = 1$, which is not
above $1$.
::::

::::{exercise} A polynomial from its roots
:label: exr-calc-polynomial-rational-from-roots
:class: tier-c

A polynomial $p$ of degree $3$ has the roots ${-1}$, $1$ and $2$, and $p(0) = 4$. Find $p(x)$.

:::{admonition} Hint 1
:class: dropdown hint
Use [](#thm-calc-factor-theorem) three times. Each time the degree of what is left drops by one.
:::

:::{admonition} Hint 2
:class: dropdown hint
After three factors, what is left has degree $0$: it is a non-zero constant $K$. Use $p(0) = 4$
to find $K$.
:::

:::{admonition} Answer
:class: dropdown answer
$2(x + 1)(x - 1)(x - 2)$
:::
::::

::::{solution} exr-calc-polynomial-rational-from-roots
:label: sol-calc-polynomial-rational-from-roots
:class: dropdown
Since $p(-1) = 0$, [](#thm-calc-factor-theorem) gives $p(x) = (x + 1)\, q_1(x)$ for every real
$x$, where $q_1$ has degree $2$ and the same leading coefficient as $p$. At $x = 1$:
$0 = p(1) = 2\, q_1(1)$, so $q_1(1) = 0$ by [part (a) of the sign rules](#prop-calc-sign-rules).
So, by the factor theorem again, $q_1(x) = (x - 1)\, q_2(x)$, where $q_2$ has degree $1$. At
$x = 2$: $0 = p(2) = 3 \cdot 1 \cdot q_2(2)$, so $q_2(2) = 0$, and $q_2(x) = (x - 2)\, K$, where
$K$ is a polynomial of degree $0$: a non-zero constant, the leading coefficient of $p$. Hence, for every real $x$,
$$
p(x) = K\,(x + 1)(x - 1)(x - 2) .
$$
At $x = 0$ this gives $4 = K \cdot 1 \cdot ({-1}) \cdot ({-2}) = 2K$, so $K = 2$, and
$p(x) = 2(x + 1)(x - 1)(x - 2)$.
::::

::::{exercise} A harder rational inequality
:label: exr-calc-polynomial-rational-inequality-hard
:class: tier-c

Find all real numbers $x$ with
$$
\frac{x}{x - 1} \ge \frac{2}{x + 1} .
$$
Give the answer as a union of intervals.

:::{admonition} Hint 1
:class: dropdown hint
Bring everything to one side over the common denominator $(x - 1)(x + 1)$.
:::

:::{admonition} Hint 2
:class: dropdown hint
The numerator $x^2 - x + 2$ has no real roots. Complete the square to see its sign.
:::

:::{admonition} Answer
:class: dropdown answer set
$(-\infty, -1), (1, \infty)$ (the union of these two intervals)
:::
::::

::::{solution} exr-calc-polynomial-rational-inequality-hard
:label: sol-calc-polynomial-rational-inequality-hard
:class: dropdown
Both sides are defined for $x \ne 1$ and $x \ne -1$. Subtracting the right-hand side from both
sides keeps the inequality, and adding it back returns to it
([property 3 of the order rules](#rem-calc-order-rules)), so for these $x$ it holds exactly
when $\frac{x}{x - 1} - \frac{2}{x + 1} \ge 0$.
Over the common denominator $(x - 1)(x + 1)$, the numerator is
$x(x + 1) - 2(x - 1) = x^2 - x + 2$, so this says
$$
\frac{x^2 - x + 2}{(x - 1)(x + 1)} \ge 0 .
$$
Completing the square, $x^2 - x + 2 = \bigl(x - \frac{1}{2}\bigr)^2 + \frac{7}{4}$. The square is
$\ge 0$ ([part (c) of the sign rules](#prop-calc-sign-rules)), so, adding $\frac{7}{4}$ to both
sides ([property 3 of the order rules](#rem-calc-order-rules)), the numerator is at least $\frac{7}{4}$, positive at every real $x$.
By [](#prop-calc-rational-sign), with
$P(x) = x^2 - x + 2$, the quotient has one sign on each of $(-\infty, -1)$, $(-1, 1)$ and
$(1, \infty)$, and it is never $0$:

- on $(-\infty, -1)$ both $x - 1$ and $x + 1$ are negative, so it is positive;
- on $(-1, 1)$ only $x - 1$ is negative, so it is negative;
- on $(1, \infty)$ neither is negative, so it is positive.

So the inequality holds exactly on $(-\infty, -1) \cup (1, \infty)$. For example $x = 2$ gives
$2 \ge \frac{2}{3}$, while $x = 0$ gives $0 \ge 2$, which is false.
::::

::::{exercise} Integer roots divide the constant term
:label: exr-calc-polynomial-rational-integer-root
:class: tier-c rigor

Let $p(x) = c_n x^n + \dots + c_1 x + c_0$ be a polynomial whose coefficients are integers, and
let $r$ be an integer with $p(r) = 0$. Show that $r$ divides $c_0$: there is an integer $k$ with
$c_0 = rk$. Use this to find all the integer roots of $x^3 + x^2 - 7x + 2$.

:::{admonition} Hint 1
:class: dropdown hint
Move $c_0$ to one side of $p(r) = 0$ and take out a factor $r$ from the other side.
:::

:::{admonition} Hint 2
:class: dropdown hint
The integers that divide $2$ are $\pm 1$ and $\pm 2$. Test each of them.
:::

:::{admonition} Answer
:class: dropdown answer manual
$c_0 = r \cdot \bigl(-(c_n r^{n-1} + \dots + c_1)\bigr)$, and the bracket is an integer. The only
integer root of $x^3 + x^2 - 7x + 2$ is $2$.
:::
::::

::::{solution} exr-calc-polynomial-rational-integer-root
:label: sol-calc-polynomial-rational-integer-root
:class: dropdown
**The proof.** From $p(r) = 0$ we get $c_0 = -\bigl(c_n r^n + \dots + c_1 r\bigr)$. Every term
in the bracket has the factor $r$, so $c_0 = r \cdot k$ with
$$
k = -\bigl(c_n r^{n-1} + \dots + c_1\bigr).
$$
The number $k$ is built from the integers $c_1, \dots, c_n$ and $r$ by adding and multiplying, so
it is an integer, and $r$ divides $c_0$. (If $n = 0$, then $p$ is the constant $c_0$, and
$p(r) = 0$ says $c_0 = 0 = r \cdot 0$.)

**The example.** For $x^3 + x^2 - 7x + 2$ the constant term is $2$, so an integer root must be one
of the integers that divide $2$. These are $1$, ${-1}$, $2$ and ${-2}$. Indeed, let $2 = rk$ with
integers $r$ and $k$. Then $r \ne 0$ and $k \ne 0$, since otherwise $rk = 0$. If $r \ge 3$, then
multiplying by the positive number $r$ ([property 5(b) of the order rules](#rem-calc-order-rules))
turns $k \ge 1$ into $rk \ge r$, and $k \le -1$ into $rk \le -r$. Since $r \ge 3$, and so
$-r \le -3$ (multiplying by ${-1}$ reverses it, by property 5(c)), this gives $rk \ge 3$ or
$rk \le -3$; neither is $2$. If $r \le -3$, the same argument applies to $2 = (-r)(-k)$, with
$-r \ge 3$. So $r$ is one of $1$, ${-1}$, $2$ and ${-2}$, and each of them divides $2$. Testing
them, with $p$ now this polynomial:

- $p(1) = 1 + 1 - 7 + 2 = -3$;
- $p(-1) = -1 + 1 + 7 + 2 = 9$;
- $p(2) = 8 + 4 - 14 + 2 = 0$;
- $p(-2) = -8 + 4 + 14 + 2 = 12$.

So $2$ is the only integer root.
::::

## Where this leads

:::{where-this-leads}
:::

:::{admonition} Looking ahead
:class: looking-ahead
The page Computing Limits Algebraically cancels the factor $x - a$ of part (a) of the factor
theorem to compute limits of the form $\frac{0}{0}$, and uses the proposition on the domain of a
rational function to know where such a function is defined. The page Partial Fractions divides
polynomials and compares coefficients, as [](#cor-calc-polynomial-identity) allows.
:::
