---
title: Trigonometric Functions
label: calc-trig-functions
description: >-
  Angles measured in radians, sine and cosine defined on the unit circle, the Pythagorean
  identity and the addition formulas, the comparison of sine, angle and tangent that later
  limits rest on, and graphs with amplitude, period and phase.
tags: [preliminaries, trigonometry]
maths:
  kind: topic
  subject: calc
  status: reviewed
  level: core
  difficulty: 2
  est_minutes: 50
  prerequisites: [calc-functions]
  objectives:
    - Work in radians.
    - Define sin and cos on the unit circle.
    - Use the core identities.
    - Graph trigonometric functions with amplitude, period and phase.
  verify: verify/calculus/preliminaries/test_trigonometric_functions.py
  widgets: [function-plot]
  reviewed_by: [vronnblom]
  manual_checked:
    exr-calc-trig-functions-cos-decreasing: vronnblom
    exr-calc-trig-functions-tan-period: vronnblom
    exr-calc-trig-functions-sin-over-theta: vronnblom
  sources: []
---

:::{topic-header}
:::

## Why this matters

A Ferris wheel of radius 20 metres turns at a steady speed, once every 10 minutes, and its
centre is 22 metres above the ground. You board at the bottom. How high are you after 100
seconds? After 25 minutes?

Your height goes up and down between 2 and 42 metres and repeats every 10 minutes. To describe
it we need two functions that say where a point is after it has turned some way round a
circle: how far it is across, and how high. They are the **cosine** and the **sine**. The same
two functions describe everything that turns or swings back and forth: wheels and pendulums,
tides, sound waves and alternating current. We answer the question about the wheel in
[](#eg-calc-trig-functions-ferris-wheel).

Calculus adds one requirement: an angle is measured by a *length*, the length of an arc of a
circle of radius $1$. This unit, the radian, is what makes the formulas of calculus for sine
and cosine simple, and this page builds everything on it.

:::{admonition} Looking ahead
:class: looking-ahead
The inequality $\sin\theta < \theta < \tan\theta$ for $0 < \theta < \frac{\pi}{2}$, proved below
by comparing three areas ([](#lem-calc-sin-bounds)), is the key to the limit of
$\frac{\sin x}{x}$ as $x \to 0$ on the page The Squeeze Theorem, and through it to the
derivatives of sine and cosine on the page Derivatives of Trigonometric Functions.
:::

## Angles in radians

Everything on this page rests on a few facts of plane geometry that you know from school: they
are the starting point, not something this course proves. They are used directly in these
places, and through them by every example and exercise:

- the definitions of the radian ([](#def-calc-radian)) and of sine and cosine
  ([](#def-calc-sin-cos)), and the arc $r\theta$ and the sector $\frac12 r^2\theta$ on a circle
  of radius $r$ after them;
- the reasons for the properties in [](#rem-calc-trig-functions-circle-properties), and the
  "In words" of [](#def-calc-tan-sec-csc-cot) (the line through $O$ and $P(t)$);
- the proofs of [](#thm-calc-pythagorean-identity), [](#thm-calc-addition-formulas),
  [](#lem-calc-sin-bounds) and [](#prop-calc-pi-bounds), and the figure of the lemma;
- the Values bullet of Graphs: period, amplitude and phase;
- the worked examples on a wheel ([](#eg-calc-trig-functions-radians)) and on the Ferris wheel
  ([](#eg-calc-trig-functions-ferris-wheel));
- the exercises on a pendulum ([](#exr-calc-trig-functions-arc-length)), on solving
  $\sin t = -\frac12$ ([](#exr-calc-trig-functions-solve-sine), its hint and solution) and on
  the Ferris wheel ([](#exr-calc-trig-functions-ferris-times), its solution).

They use only the facts in the box below.

:::{proof:remark} Facts from school used on this page
:label: rem-calc-trig-functions-school-facts

We write $O = (0, 0)$ for the origin and $A = (1, 0)$.

- **Distance.** By Pythagoras' theorem, the distance between the points $(x_1, y_1)$ and
  $(x_2, y_2)$ is $\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$. So the **unit circle**, the circle of
  radius $1$ about $O$, is the set of points $(x, y)$ with $x^2 + y^2 = 1$, and the **unit
  disc** is the set of points with $x^2 + y^2 \le 1$. The disc contains, with any two of its
  points, the segment between them.
- **Length of arcs.** Every arc of the unit circle has a length. An arc cut into two arcs at a
  point has the sum of their lengths. The whole circle has length $2\pi$: this is the
  definition of the number $\pi$.
- **Journeys along the circle.** From any point of the circle, travelling a distance $d \ge 0$
  along it anticlockwise, or clockwise, ends at exactly one point; anticlockwise is the
  direction in which a journey from $A$ sets off towards $(0, 1)$. Counting clockwise
  distances as negative, a journey of $s$ followed by a journey of $t$ ends where a journey of
  $s + t$ does. Every point of the circle is reached from $A$ by an anticlockwise journey of
  exactly one length in $[0, 2\pi)$.
- **Journeys and arcs.** An anticlockwise journey of length $d$, where $0 < d \le 2\pi$, runs
  along an arc of the circle from its starting point to its end point, and that arc has length
  $d$. (For $d = 2\pi$ the arc is the whole circle.)
- **Rotations and reflections.** For every point $Q$ of the unit circle there is a rotation
  about $O$ that maps $A$ to $Q$. A rotation about $O$, and a reflection in a line through
  $O$, map the unit circle onto itself and keep the distances between points and the lengths
  of arcs. So they map a journey along the circle to a journey of the same length; a rotation
  keeps its direction, and a reflection reverses it.
- **Circles of other radii.** A circle of radius $r > 0$ is the unit circle scaled by $r$
  (and moved): lengths of arcs are multiplied by $r$, and areas by $r^2$.
- **Sectors.** Take an arc of the unit circle of length $\theta$, where $0 < \theta \le 2\pi$.
  The **region between the radii** at its ends is the set of points $\lambda X$ with
  $\lambda \ge 0$ and $X$ on the arc, and the **sector** of the arc is the part of this region
  that lies in the unit disc. If $\theta < \pi$, the region contains, with any two of its
  points, the segment between them; and if $Q$ and $R$ are points other than $O$ on the two rays
  from $O$ through the ends of the arc, the triangle $OQR$ is the part of the region that lies
  on the same side of the line $QR$ as $O$, or on that line. Every point of that triangle lies
  on a segment from $O$ to a point of its side $QR$.
- **Area.** A triangle with base $b$ and height $h$ has area $\frac12 bh$. A sector whose arc
  has length $\theta$, where $0 < \theta \le 2\pi$, has area $\frac{\theta}{2}$. For
  $\theta = 2\pi$ this says that the unit disc has area $\pi$: that is Archimedes' theorem, not
  the definition of $\pi$, which is the length of the circle. A region that lies inside another
  has at most the other's area.

No page of this course proves these facts. They are proved in Real Analysis (`ana`), outside
this course.
:::

:::{admonition} Looking ahead
:class: looking-ahead
Two of these facts hide a limit: the length of a curved arc, and the area of a region with a
curved edge. The Integrals chapter makes area precise, as a limit of sums (the pages Area and
Riemann Sums and The Definite Integral), and the page Arc Length and Surface Area defines the
length of a curve. Those pages may not
recover the arc length of the circle or the area of a sector with the derivatives of sine and
cosine: the derivatives rest on [](#lem-calc-sin-bounds) of this page, so that would argue in
a circle. Real Analysis (`ana`), which does not exist yet, constructs sine and cosine without
any geometry, from power series or from an integral, and proves the facts in the box.
:::

To measure an angle at the centre of the unit circle, walk along the circle, inside the angle,
from one arm to the other and measure how far you went. The larger the angle, the longer the
walk.

:::{proof:definition} Radian
:label: def-calc-radian

Let an angle have its vertex at the centre $O$ of the unit circle. Its two arms meet the circle
at two points, which cut the circle into two arcs. The angle's **measure in radians** is the
length of the one of these arcs that lies inside the angle. (For an angle smaller than a
straight angle, this is the shorter arc.) A full turn, whose arms coincide, has the whole
circle as its arc: $2\pi$.
:::

**In words.** An angle of $\theta$ radians is the angle you turn through while you walk a
distance $\theta$ along the unit circle. Radians are lengths divided by the radius, so the unit
is usually left out: "an angle of $2$" means $2$ radians.

**Example.** A full turn is the whole circle, $2\pi$ radians. A straight angle is half of it,
$\pi$, and a right angle is a quarter, $\frac{\pi}{2}$ (property 1 of
[](#rem-calc-trig-functions-circle-properties) shows that the quarter circles have equal
lengths). A full turn is also $360$ degrees, so $1$ degree is $\frac{2\pi}{360} = \frac{\pi}{180}$
radians: $60$ degrees is $\frac{60\pi}{180} = \frac{\pi}{3}$ radians, and an angle of $\theta$
radians is $\frac{180\theta}{\pi}$ degrees.

**Non-example.** An angle of $1$ radian is not $1$ degree. It is the angle whose arc is exactly
as long as the radius, $\frac{180}{\pi} \approx 57.3$ degrees.

On a circle of radius $r$, an angle of $\theta$ radians at the centre, with
$0 < \theta \le 2\pi$, cuts off an arc of length $r\theta$ and a sector of area
$\frac12 r^2 \theta$, by the facts on circles of other radii and on areas. For $\theta = 2\pi$
these are the circumference $2\pi r$ and the area $\pi r^2$ of the whole disc.

## Sine and cosine

Now let the angle grow beyond a full turn, and let it turn the other way too. Start at
$A = (1, 0)$ and walk along the unit circle; after a distance $t$ you are at a point $P(t)$. Its
coordinates are the cosine and the sine of $t$.

:::{proof:definition} Sine and cosine
:label: def-calc-sin-cos

For a real number $t$, let $P(t)$ be the point of the unit circle that is reached from
$A = (1, 0)$ by travelling along the circle a distance $t$ anticlockwise if $t \ge 0$, or a
distance $-t$ clockwise if $t < 0$. The **cosine** and the **sine** of $t$ are the coordinates
of $P(t)$:
$$
P(t) = (\cos t, \sin t).
$$
This defines functions $\cos$ and $\sin$ with domain $\R$. We write $\sin^2 t$ for
$(\sin t)^2$, and likewise for other powers.
:::

:::{figure} ./img/unit-circle.svg
:label: fig-calc-trig-functions-unit-circle
:alt: The unit circle about the origin O, with the x- and y-axes. The x-axis is marked −1 on the left, where the circle crosses it, and A on the right; the y-axis is marked 1 and −1. A thick arc runs anticlockwise along the circle from the point A = (1, 0) to a point P(t) = (cos t, sin t) in the first quadrant and is labelled "arc length t". A radius joins O to P(t). A thick segment on the x-axis from O to the foot of P(t) is labelled cos t, and a dashed vertical segment from there up to P(t) is labelled sin t.

The point $P(t)$ is reached from $A = (1, 0)$ by walking a distance $t$ along the unit circle.
Its $x$-coordinate is $\cos t$ and its $y$-coordinate is $\sin t$.
:::

**In words.** $\cos t$ is how far across, and $\sin t$ how high, you are after walking a
distance $t$ round the unit circle from $A$. For $0 < t < \frac{\pi}{2}$ they are the two legs
of the right-angled triangle with hypotenuse $OP(t)$ in
[](#fig-calc-trig-functions-unit-circle), which is the definition from school ("adjacent over
hypotenuse" and "opposite over hypotenuse", with hypotenuse $1$). The unit circle extends it to
every real number $t$, and $t$ is always in radians.

**Example.** $P(0) = A = (1, 0)$, so $\cos 0 = 1$ and $\sin 0 = 0$. After a quarter of the
circle, $P\bigl(\frac{\pi}{2}\bigr) = (0, 1)$, so $\cos\frac{\pi}{2} = 0$ and
$\sin\frac{\pi}{2} = 1$ (property 1 below).

**Non-example.** $\sin 30$ is not $\frac12$. The number $30$ is a distance along the unit
circle, almost five full turns, and $\sin 30 \approx -0.988$. The angle of $30$ degrees is
$\frac{\pi}{6}$ radians, and $\sin\frac{\pi}{6} = \frac12$
([](#eg-calc-trig-functions-special-values)).

Reflecting and rotating the circle moves $P(t)$ to other points $P(\ldots)$ in a predictable
way. These properties do most of the work on this page.

:::{proof:remark} Properties of the point $P(t)$
:label: rem-calc-trig-functions-circle-properties

Let $t$ and $\alpha$ be real numbers and $k$ an integer.

1. $P(0) = (1, 0)$, $P\bigl(\frac{\pi}{2}\bigr) = (0, 1)$, $P(\pi) = ({-1}, 0)$ and
   $P\bigl(\frac{3\pi}{2}\bigr) = (0, {-1})$.
2. A rotation about $O$ that maps $A$ to $P(\alpha)$ maps $P(t)$ to $P(t + \alpha)$.
3. $P(t + 2k\pi) = P(t)$. Conversely, if $P(s) = P(t)$ for real numbers $s$ and $t$, then
   $s - t = 2k\pi$ for some integer $k$.
4. $\cos(-t) = \cos t$ and $\sin(-t) = -\sin t$.
5. $\cos(\pi - t) = -\cos t$ and $\sin(\pi - t) = \sin t$.
6. $\cos\bigl(\frac{\pi}{2} - t\bigr) = \sin t$ and $\sin\bigl(\frac{\pi}{2} - t\bigr) = \cos t$.
7. $\cos(t + \pi) = -\cos t$ and $\sin(t + \pi) = -\sin t$.
8. If $0 < t < \frac{\pi}{2}$, then $\cos t > 0$ and $\sin t > 0$. If $0 < t < \pi$, then
   $\sin t > 0$.

*Reasons*, from the facts from school above.

1. The axes cut the circle into four arcs, one in each quadrant. The reflection in the
   $y$-axis maps the arc in the first quadrant onto the one in the second, and the reflection
   in the $x$-axis maps these two onto the arcs in the fourth and third quadrants. Reflections
   keep lengths, so the four arcs have the same length, and as the lengths add up to $2\pi$,
   each has length $\frac{\pi}{2}$. Walking anticlockwise from $A$ we reach $(0, 1)$, $({-1}, 0)$
   and $(0, {-1})$ after $\frac{\pi}{2}$, $\pi$ and $\frac{3\pi}{2}$.
2. $P(t)$ is reached from $A$ by a journey of $t$. The rotation keeps the length and the
   direction of that journey, so the image of $P(t)$ is reached from the image of $A$, which is
   $P(\alpha)$, by a journey of $t$. Since $P(\alpha)$ is reached from $A$ by a journey of
   $\alpha$, the image is reached from $A$ by a journey of $\alpha + t$: it is $P(t + \alpha)$.
3. A journey of $2\pi$ goes once round the circle and ends where it started, so
   $P(t + 2\pi) = P(t)$; repeating this $k$ times (with $t - 2\pi$ in place of $t$ when
   $k < 0$) gives $P(t + 2k\pi) = P(t)$. Conversely, let $P(s) = P(t)$. By
   [the remark on the integer part of a real number](#rem-calc-integer-part) in Real Numbers and
   Intervals, there is an integer $k$ with $k \le \frac{s - t}{2\pi} < k + 1$. Multiplying by the
   positive number $2\pi$ keeps both inequalities, and subtracting $2k\pi$ keeps them too
   ([properties 5 and 3 of the order rules](#rem-calc-order-rules) of Real Numbers and
   Intervals), so $u = s - t - 2k\pi$ satisfies $0 \le u < 2\pi$. Then
   $P(s) = P(t + u + 2k\pi) = P(t + u)$. A rotation that maps $A$ to
   $P(-t)$ maps $P(t)$ to $P(0) = A$ and $P(t + u)$ to $P(u)$, by property 2. As
   $P(t + u) = P(t)$, it follows that $P(u) = A = P(0)$. Only one length in $[0, 2\pi)$ leads
   from $A$ to $A$, so $u = 0$ and $s - t = 2k\pi$.
4. The reflection in the $x$-axis maps $(x, y)$ to $(x, -y)$, fixes $A$ and reverses
   directions. It maps the journey of $t$ from $A$ to a journey of $-t$ from $A$, so it maps
   $P(t)$ to $P(-t)$. Hence $(\cos(-t), \sin(-t)) = (\cos t, -\sin t)$.
5. The reflection in the $y$-axis maps $(x, y)$ to $(-x, y)$, maps $A$ to $P(\pi) = ({-1}, 0)$
   and reverses directions. It maps the journey of $t$ from $A$ to a journey of $-t$ from
   $P(\pi)$, which ends at $P(\pi - t)$. Hence $(\cos(\pi - t), \sin(\pi - t)) = (-\cos t, \sin t)$.
6. The reflection in the line $y = x$ maps $(x, y)$ to $(y, x)$, maps $A$ to
   $P\bigl(\frac{\pi}{2}\bigr) = (0, 1)$ and reverses directions, so as in 5 it maps $P(t)$ to
   $P\bigl(\frac{\pi}{2} - t\bigr)$. Hence
   $\bigl(\cos\bigl(\frac{\pi}{2} - t\bigr), \sin\bigl(\frac{\pi}{2} - t\bigr)\bigr) = (\sin t, \cos t)$.
7. $t + \pi = \pi - (-t)$, so by 5 and then 4, $\cos(t + \pi) = -\cos(-t) = -\cos t$ and
   $\sin(t + \pi) = \sin(-t) = -\sin t$.
8. A journey of $t$ with $0 < t < \frac{\pi}{2}$ ends on the arc in the first quadrant, but at
   neither of its ends $(1, 0)$ and $(0, 1)$, by 1; there $x > 0$ and $y > 0$. A journey of $t$
   with $0 < t < \pi$ ends on the upper half of the circle, from $(1, 0)$ to $({-1}, 0)$, at
   neither end; there $y > 0$.
:::

Property 4 says that $\cos$ is [even](#def-calc-even-odd) and $\sin$ is odd: their common
domain $\R$ is symmetric about $0$. Properties 5–7 move any $t$ into the first quadrant, so
the values there decide all the others.

Two more pairs of functions are built from $\sin$ and $\cos$.

:::{proof:definition} Tangent, secant, cosecant and cotangent
:label: def-calc-tan-sec-csc-cot

For every real number $t$ with $\cos t \ne 0$,
$$
\tan t = \frac{\sin t}{\cos t}, \qquad \sec t = \frac{1}{\cos t},
$$
and for every real number $t$ with $\sin t \ne 0$,
$$
\cot t = \frac{\cos t}{\sin t}, \qquad \csc t = \frac{1}{\sin t}.
$$
These are the **tangent**, **secant**, **cotangent** and **cosecant**; each is defined exactly
for those $t$, its natural domain.
:::

**In words.** $\tan t$ is the slope of the line through $O$ and $P(t)$: the rise $\sin t$
divided by the run $\cos t$. When $\cos t \ne 0$, that line meets the vertical line $x = 1$ at
the point $(1, \tan t)$, which is $P(t)$ with both coordinates multiplied by
$\frac{1}{\cos t}$. The other three are reciprocals: $\sec t = \frac{1}{\cos t}$,
$\csc t = \frac{1}{\sin t}$, and $\cot t = \frac{1}{\tan t}$ wherever both are defined.
[](#rem-calc-trig-functions-zeros) finds the $t$ where $\cos t$ or $\sin t$ is
$0$.

**Example.** $P(0) = (1, 0)$ gives $\tan 0 = \frac{0}{1} = 0$ and $\sec 0 = 1$.

**Non-example.** $\tan\frac{\pi}{2}$ is not a number, and not "infinity" either: by property 1,
$\cos\frac{\pi}{2} = 0$, so $\frac{\pi}{2}$ is not in the domain of $\tan$. Likewise $\cot 0$
and $\csc 0$ are undefined, because $\sin 0 = 0$.

## Main results

### Identities and values

Since $P(t)$ lies on the unit circle, its coordinates satisfy the equation of the circle. This
is the most used identity of trigonometry.

:::{proof:theorem} Pythagorean identity
:label: thm-calc-pythagorean-identity

For every real number $t$,
$$
\cos^2 t + \sin^2 t = 1 .
$$
:::

:::{proof:proof}
:enumerated: false
We use that $P(t)$ is a point of the unit circle. By [](#def-calc-sin-cos),
$P(t) = (\cos t, \sin t)$ is a point of the unit circle, and the unit circle is the set of points
$(x, y)$ with $x^2 + y^2 = 1$ (the facts from school). With $x = \cos t$ and $y = \sin t$, this
says $\cos^2 t + \sin^2 t = 1$.
:::

Where $\cos t \ne 0$, the number $\cos^2 t$ is positive, and dividing the identity by it gives
$1 + \tan^2 t = \sec^2 t$.

The next three facts are the ones that the page The Limit of a Function uses about $\sin$, with
$t$ in radians.

:::{proof:proposition} Sine and cosine lie between $-1$ and $1$
:label: prop-calc-sin-bounded

For every real number $t$:

(a) $-1 \le \sin t \le 1$;

(b) $-1 \le \cos t \le 1$.
:::

:::{proof:proof}
:enumerated: false
We show that $\sin^2 t \le 1$, and then that a number whose square is at most $1$ lies between
$-1$ and $1$.

(a) A square is never negative, so $\cos^2 t \ge 0$. Adding $1 - \cos^2 t$ to both sides keeps
the inequality ([property 3 of the order rules](#rem-calc-order-rules)), so, by
[](#thm-calc-pythagorean-identity), $\sin^2 t = 1 - \cos^2 t \le 1$. Suppose $\sin t > 1$.
Both $\sin t$ and $1$ are then non-negative, and by the order part of
[the square-root remark](#rem-calc-square-roots) (for non-negative $u$ and $v$, $u < v$ exactly
when $u^2 < v^2$), $1 < \sin t$ gives $1 < \sin^2 t$, which is impossible. Suppose
$\sin t < -1$. Multiplying by the negative number ${-1}$ reverses the inequality
([property 5(c) of the order rules](#rem-calc-order-rules)), so $-\sin t > 1$, and in the same
way $1 < (-\sin t)^2 = \sin^2 t$, which is impossible. So $-1 \le \sin t \le 1$ (property 7 of the order rules, negation).

(b) The same argument with $\cos$ and $\sin$ exchanged, using
$\cos^2 t = 1 - \sin^2 t \le 1$.
:::

:::{proof:proposition} Sine is zero at the multiples of $\pi$
:label: prop-calc-sin-multiples-of-pi

For every integer $k$, $\sin(k\pi) = 0$.
:::

:::{proof:proof}
:enumerated: false
We use the period $2\pi$ to move $k\pi$ to $0$ or to $\pi$, where we know the point $P$. Every
integer $k$ is even or odd: $k = 2m$ or $k = 2m + 1$ for an integer $m$.

- If $k = 2m$, then $P(k\pi) = P(0 + 2m\pi) = P(0) = (1, 0)$, by properties 3 and 1 of
  [](#rem-calc-trig-functions-circle-properties).
- If $k = 2m + 1$, then $P(k\pi) = P(\pi + 2m\pi) = P(\pi) = ({-1}, 0)$, by the same
  properties.

In both cases the second coordinate of $P(k\pi)$, which is $\sin(k\pi)$ by
[](#def-calc-sin-cos), is $0$.
:::

:::{proof:proposition} Sine is $1$ at $\frac{\pi}{2}$ plus multiples of $2\pi$
:label: prop-calc-sin-maxima

For every integer $k$, $\sin\bigl(\frac{\pi}{2} + 2k\pi\bigr) = 1$.
:::

:::{proof:proof}
:enumerated: false
We move $\frac{\pi}{2} + 2k\pi$ back to $\frac{\pi}{2}$ with the period $2\pi$. By property 3 of
[](#rem-calc-trig-functions-circle-properties), with $t = \frac{\pi}{2}$,
$P\bigl(\frac{\pi}{2} + 2k\pi\bigr) = P\bigl(\frac{\pi}{2}\bigr)$, and by property 1 this point is
$(0, 1)$. Its second coordinate, $\sin\bigl(\frac{\pi}{2} + 2k\pi\bigr)$, is $1$.
:::

By [](#prop-calc-sin-bounded), $1$ is the largest value of $\sin$, so these are maxima of
$\sin$. The converse of [](#prop-calc-sin-multiples-of-pi) holds too: $\sin$ is zero *only* at
the multiples of $\pi$.

:::{proof:remark} Where sine and cosine are zero
:label: rem-calc-trig-functions-zeros

Let $t$ be a real number.

1. $\sin t = 0$ exactly when $t = k\pi$ for an integer $k$.
2. $\cos t = 0$ exactly when $t = \frac{\pi}{2} + k\pi$ for an integer $k$.

So the natural domain of $\tan$ and $\sec$ is the set of all real numbers except
$\frac{\pi}{2} + k\pi$, $k \in \Z$, and that of $\cot$ and $\csc$ is the set of all real numbers
except $k\pi$, $k \in \Z$.

*Reason.* 1. If $t = k\pi$, then $\sin t = 0$ by [](#prop-calc-sin-multiples-of-pi).
Conversely, let $\sin t = 0$. Then $\cos^2 t = 1$ by [](#thm-calc-pythagorean-identity). If
$\cos t \ge 0$, then $\cos t$ is the non-negative square root of $1$, which is $1$
([the square-root remark](#rem-calc-square-roots)); if $\cos t < 0$, then $-\cos t > 0$
(multiplying by the negative number ${-1}$ reverses the inequality, by
[property 5(c) of the order rules](#rem-calc-order-rules)), and in the same way $-\cos t = 1$. So $P(t) = (1, 0) = P(0)$ or
$P(t) = ({-1}, 0) = P(\pi)$, by property 1 of
[](#rem-calc-trig-functions-circle-properties). By the converse in property 3, $t = 2m\pi$ or
$t = \pi + 2m\pi$ for an integer $m$: in both cases $t$ is an integer multiple of $\pi$.

2. By property 6, $\cos t = \sin\bigl(\frac{\pi}{2} - t\bigr)$. By 1, this is $0$ exactly when
$\frac{\pi}{2} - t = j\pi$ for an integer $j$, that is, when $t = \frac{\pi}{2} + k\pi$ with
$k = -j$.
:::

### The addition formulas

How do $\sin$ and $\cos$ of a sum depend on the summands? Not by adding: $\sin(s + t)$ is not
$\sin s + \sin t$ (for $s = t = \frac{\pi}{2}$ the left side is $\sin\pi = 0$ and the right
side is $2$). The answer mixes sines and cosines.

:::{proof:theorem} Addition formulas
:label: thm-calc-addition-formulas

For all real numbers $s$ and $t$:

(a) $\cos(s - t) = \cos s \cos t + \sin s \sin t$;

(b) $\cos(s + t) = \cos s \cos t - \sin s \sin t$;

(c) $\sin(s + t) = \sin s \cos t + \cos s \sin t$;

(d) $\sin(s - t) = \sin s \cos t - \cos s \sin t$;

(e) $\sin 2t = 2 \sin t \cos t$;

(f) $\cos 2t = \cos^2 t - \sin^2 t = 2\cos^2 t - 1 = 1 - 2\sin^2 t$.
:::

:::{proof:proof} Rigorous track
:label: prf-calc-addition-formulas
:enumerated: false
:class: dropdown
We compute the distance between $P(s)$ and $P(t)$ in two ways: directly, and after a rotation
that moves $P(t)$ to $A$. This gives (a), and the others follow from (a) and the properties of
$P(t)$.

(a) By property 2 of [](#rem-calc-trig-functions-circle-properties) with $\alpha = -t$, a
rotation about $O$ that maps $A$ to $P(-t)$ maps $P(t)$ to $P(0) = A$ and $P(s)$ to $P(s - t)$.
A rotation keeps distances (the facts from school), so the distance from $P(s)$ to $P(t)$
equals the distance from $P(s - t)$ to $A$, and so do their squares. By the distance formula
and [](#thm-calc-pythagorean-identity), the first squared distance is
$$
\begin{aligned}
&(\cos s - \cos t)^2 + (\sin s - \sin t)^2 \\
&= \cos^2 s + \sin^2 s + \cos^2 t + \sin^2 t \\
&\quad - 2\cos s \cos t - 2\sin s \sin t \\
&= 2 - 2(\cos s \cos t + \sin s \sin t),
\end{aligned}
$$
and the second is
$$
\begin{aligned}
&\bigl(\cos(s - t) - 1\bigr)^2 + \sin^2(s - t) \\
&= \cos^2(s - t) + \sin^2(s - t) \\
&\quad - 2\cos(s - t) + 1 \\
&= 2 - 2\cos(s - t).
\end{aligned}
$$
Setting them equal and solving for $\cos(s - t)$ gives (a).

(b) Apply (a) to $s$ and $-t$; by property 4, $\cos(-t) = \cos t$ and $\sin(-t) = -\sin t$,
so $\cos(s + t) = \cos s \cos(-t) + \sin s \sin(-t) = \cos s \cos t - \sin s \sin t$.

(c) By property 6, $\sin(s + t) = \cos\bigl(\frac{\pi}{2} - (s + t)\bigr)
= \cos\bigl(\bigl(\frac{\pi}{2} - s\bigr) - t\bigr)$. By (a), and property 6 again
($\cos\bigl(\frac{\pi}{2} - s\bigr) = \sin s$ and $\sin\bigl(\frac{\pi}{2} - s\bigr) = \cos s$),
$$
\begin{aligned}
\sin(s + t) &= \cos\Bigl(\frac{\pi}{2} - s\Bigr)\cos t \\
  &\quad + \sin\Bigl(\frac{\pi}{2} - s\Bigr)\sin t \\
  &= \sin s \cos t + \cos s \sin t .
\end{aligned}
$$

(d) Apply (c) to $s$ and $-t$, and use property 4 as in (b).

(e) and (f): put $s = t$ in (c) and (b). The other two forms of (f) follow from
[](#thm-calc-pythagorean-identity): $\cos^2 t - \sin^2 t = \cos^2 t - (1 - \cos^2 t) = 2\cos^2 t - 1$,
and in the same way $= 1 - 2\sin^2 t$.
:::

Parts (e) and (f) are the **double-angle formulas**. With the values of the next section they
give exact values such as $\cos\frac{\pi}{12}$ ([](#eg-calc-trig-functions-addition)).

### Sine, angle and tangent

For a small positive angle $\theta$, the height $\sin\theta$ of $P(\theta)$, the arc $\theta$
and the height $\tan\theta$ of the point where the line $OP(\theta)$ meets the line $x = 1$ are
three lengths that are almost equal. The next lemma puts them in order. It is the one fact
about sine on which the limit of $\frac{\sin x}{x}$, and so all of the calculus of sine and
cosine, will rest, so its proof uses no derivatives and no limits: only areas.

:::{figure} ./img/sin-bounds-areas.svg
:label: fig-calc-trig-functions-sin-bounds-areas
:alt: A quarter of the unit circle about the origin O, with A = (1, 0) on the x-axis, the point P = (cos θ, sin θ) on the circle at angle θ, and T = (1, tan θ) directly above A on the line through O and P. Three nested regions are shaded: the triangle OAP with a dashed side AP, inside it the height sin θ of P drawn dotted; the sector OAP bounded by the arc from A to P; and the large triangle OAT, whose vertical side AT has length tan θ.

For $0 < \theta < \frac{\pi}{2}$: the triangle $OAP$ (area $\frac12\sin\theta$) lies inside
the sector $OAP$ (area $\frac{\theta}{2}$), which lies inside the triangle $OAT$ (area
$\frac12\tan\theta$).
:::

:::{proof:lemma} Sine, angle and tangent
:label: lem-calc-sin-bounds

For every real number $\theta$ with $0 < \theta < \frac{\pi}{2}$,
$$
\sin\theta < \theta < \tan\theta .
$$
:::

:::{proof:proof}
:enumerated: false
We compare the areas of three regions that lie inside one another, which gives the inequalities
with $\le$; applying them to $\frac{\theta}{2}$ with the double-angle formulas then makes them
strict.

**Step 1: the inequalities with $\le$.** Let $0 < \theta < \frac{\pi}{2}$, let
$P = P(\theta) = (\cos\theta, \sin\theta)$, and let $T = (1, \tan\theta)$. By property 8 of
[](#rem-calc-trig-functions-circle-properties), $\cos\theta > 0$ and $\sin\theta > 0$, so
$\tan\theta = \frac{\sin\theta}{\cos\theta}$ is defined and positive
([](#def-calc-tan-sec-csc-cot)). Consider the three regions of
[](#fig-calc-trig-functions-sin-bounds-areas).

- The **triangle $OAP$** has base $OA$ of length $1$ on the $x$-axis and height $\sin\theta$,
  the height of $P$ above that axis. Its area is $\frac12\sin\theta$.
- The **sector $OAP$** is the sector of the arc traced by the anticlockwise journey of length
  $\theta$ from $A$, which ends at $P(\theta)$; that arc has length $\theta$ (journeys and arcs,
  in the facts from school). So the sector is the part of the unit disc between the radii $OA$
  and $OP$, and its area is $\frac{\theta}{2}$.
- The **triangle $OAT$** has base $OA$ of length $1$ and height $\tan\theta$, because $T$ lies
  directly above $A$ at height $\tan\theta > 0$. Its area is $\frac12\tan\theta$.

They lie inside one another.

- *The triangle $OAP$ lies in the sector.* Every point of the triangle lies on a segment from
  $O$ to a point $Q$ of its side $AP$ (the facts from school, sectors). The disc contains $A$
  and $P$, so it contains the segment $AP$ and with it $Q$, and then the whole segment $OQ$ (the facts from school, distance). The
  region between the radii $OA$ and $OP$ contains $O$, $A$ and $P$ (take $\lambda = 0$ or
  $\lambda = 1$), and, since $\theta < \frac{\pi}{2} < \pi$, with any two of its points the
  segment between them (the facts from school, sectors); so it contains $Q$ and then the
  segment $OQ$. That segment therefore lies in the part of the region in the disc, which is
  the sector.
- *The sector lies in the triangle $OAT$.* The point $T = \frac{1}{\cos\theta}\,P$ lies on the
  ray from $O$ through $P$, because $\frac{1}{\cos\theta} > 0$. So the triangle $OAT$ is the part
  of the region between the radii $OA$ and $OP$ that lies on the same side of the line $AT$
  (the line $x = 1$) as $O$, or on it: the part with $x \le 1$ (the facts from school,
  sectors). Every point $(x, y)$ of the disc has $x \le 1$. Indeed, $y^2 \ge 0$, so adding
  $x^2$ keeps the inequality and $x^2 \le x^2 + y^2 \le 1$
  ([properties 3 and 2 of the order rules](#rem-calc-order-rules)).
  If $x > 1$, then $x > 1 \ge 0$, and the order part of
  [the square-root remark](#rem-calc-square-roots) would give $x^2 > 1$, which is impossible. So
  the sector, the part of that region in the disc, lies in the triangle $OAT$.

A region that lies inside another has at most its area (the facts from school), so
$\frac12\sin\theta \le \frac{\theta}{2} \le \frac12\tan\theta$. Multiplying by the positive
number $2$ keeps both inequalities ([property 5(b) of the order rules](#rem-calc-order-rules)). So, for every $\theta$ with
$0 < \theta < \frac{\pi}{2}$,
$$
\sin\theta \le \theta \le \tan\theta .
$$

**Step 2: the inequalities are strict.** Let $0 < \theta < \frac{\pi}{2}$ again, and let
$s = \sin\frac{\theta}{2}$ and $c = \cos\frac{\theta}{2}$. Multiplying
$0 < \theta < \frac{\pi}{2}$ by the positive number $\frac12$ keeps both inequalities
([property 5(a) of the order rules](#rem-calc-order-rules)), so
$0 < \frac{\theta}{2} < \frac{\pi}{4} < \frac{\pi}{2}$. Property 8 then gives $s > 0$ and
$c > 0$, and step 1, applied to $\frac{\theta}{2}$, gives $s \le \frac{\theta}{2}$ and
$\frac{\theta}{2} \le \tan\frac{\theta}{2} = \frac{s}{c}$.
Also $c < 1$: $s^2 > 0$, and adding $1 - s^2$ to both sides of $0 < s^2$ gives
$1 - s^2 < 1$ ([property 3 of the order rules](#rem-calc-order-rules)), so $c^2 = 1 - s^2 < 1$ by
[](#thm-calc-pythagorean-identity); and $c \ge 1$ would give $c^2 \ge 1$, by the order part of
[the square-root remark](#rem-calc-square-roots).

- *Sine.* By part (e) of [](#thm-calc-addition-formulas), $\sin\theta = 2sc$. Multiplying
  $c < 1$ by the positive number $2s$ keeps the strict inequality, and multiplying
  $s \le \frac{\theta}{2}$ by the positive number $2$ keeps that one
  ([properties 5(a) and 5(b) of the order rules](#rem-calc-order-rules)), so
  $$
  \sin\theta = 2sc < 2s \le 2 \cdot \frac{\theta}{2} = \theta .
  $$
- *Tangent.* By part (f) of [](#thm-calc-addition-formulas), $\cos\theta = c^2 - s^2$, and
  $\cos\theta > 0$ by property 8. Adding $c^2 - s^2$ to both sides of $0 < s^2$ gives
  $c^2 - s^2 < c^2$ ([property 3 of the order rules](#rem-calc-order-rules)), so $0 < c^2 - s^2 < c^2$. Multiplying
  $c^2 - s^2 < c^2$ by the positive number $\frac{2sc}{(c^2 - s^2)\,c^2}$ keeps the strict
  inequality and gives $\frac{2sc}{c^2} < \frac{2sc}{c^2 - s^2}$. Multiplying
  $\frac{\theta}{2} \le \frac{s}{c}$ by the positive number $2$ keeps it:
  $2 \cdot \frac{s}{c} \ge 2 \cdot \frac{\theta}{2}$
  ([properties 5(a) and 5(b) of the order rules](#rem-calc-order-rules)). Hence
  $$
  \begin{aligned}
  \tan\theta = \frac{\sin\theta}{\cos\theta} &= \frac{2sc}{c^2 - s^2} \\
    &> \frac{2sc}{c^2} = 2\cdot\frac{s}{c} \\
    &\ge 2 \cdot \frac{\theta}{2} = \theta .
  \end{aligned}
  $$

So $\sin\theta < \theta < \tan\theta$.
:::

The proof used no derivatives and no limits. It rests directly on these facts from school:

- the equation of the unit circle and of the disc, and that the disc contains the segment
  between any two of its points;
- journeys and arcs: the arc from $A$ to $P(\theta)$ traced by the journey has length
  $\theta$;
- that the region between two radii whose arc is shorter than half the circle contains the
  segment between any two of its points, and that the triangle $OAT$ is the part of that region
  with $x \le 1$;
- that every point of the triangle $OAP$ lies on a segment from $O$ to a point $Q$ of its side
  $AP$;
- the area $\frac12 bh$ of a triangle, and the area $\frac{\theta}{2}$ of a sector (so the
  unit disc has area $\pi$, Archimedes' theorem);
- that a region inside another has at most its area.

Through property 8, the Pythagorean identity and parts (e) and (f), it also rests on the rest of
the box: the lengths of arcs, journeys along the circle, reflections and rotations. This course
proves none of these facts (Real Analysis does). Two of them hide a limit: the length of an arc
and the area of a sector.

:::{proof:remark} Why $0 < \theta < \frac{\pi}{2}$
:label: rem-calc-trig-functions-sin-bounds-hypothesis

Each part of the hypothesis is needed.

- At $\theta = 0$ all three numbers are $0$, so the strict inequalities fail.
- At $\theta = \frac{\pi}{2}$, $\tan\theta$ is undefined, and beyond it the second inequality can
  fail: at $\theta = \pi$, $\tan\pi = \frac{\sin\pi}{\cos\pi} = \frac{0}{-1} = 0 < \pi$, by
  property 1 of [](#rem-calc-trig-functions-circle-properties).
- For $-\frac{\pi}{2} < \theta < 0$ the inequalities reverse: $\phi = -\theta$ satisfies the
  lemma, and by property 4 $\sin\theta = -\sin\phi$ and $\tan\theta = -\tan\phi$, so multiplying
  $\sin\phi < \phi < \tan\phi$ by the negative number ${-1}$, which reverses both inequalities
  ([property 5(c) of the order rules](#rem-calc-order-rules)), gives
  $\sin\theta > \theta > \tan\theta$.
:::

At $\theta = \frac{\pi}{4}$ the lemma gives a first bound on the number $\pi$ itself, with no
decimals.

:::{proof:proposition} Bounds on $\pi$
:label: prop-calc-pi-bounds

$$
2\sqrt{2} < \pi < 4 .
$$
:::

:::{proof:proof}
:enumerated: false
We find $\sin\frac{\pi}{4}$ and $\tan\frac{\pi}{4}$ exactly and apply [](#lem-calc-sin-bounds)
at $\theta = \frac{\pi}{4}$.

**Step 1: $\frac{\pi}{4}$ lies in the range of the lemma.** The point $A$ of the circle is
reached from $A$ by an anticlockwise journey of some length $d$ with $0 \le d < 2\pi$ (the facts
from school, journeys along the circle), so $0 < 2\pi$
([property 2 of the order rules](#rem-calc-order-rules)). The number $\frac18$ is positive,
because $8 > 0$ ([property 6 of the order rules](#rem-calc-order-rules)), so multiplying
$0 < 2\pi$ by $\frac18$ keeps the inequality
([property 5(a) of the order rules](#rem-calc-order-rules)): $0 < \frac{\pi}{4}$. Adding
$\frac{\pi}{4}$ to both sides ([property 3 of the order rules](#rem-calc-order-rules)) gives
$\frac{\pi}{4} < \frac{\pi}{2}$. So $0 < \frac{\pi}{4} < \frac{\pi}{2}$.

**Step 2: $\sin\frac{\pi}{4} = \frac{1}{\sqrt{2}}$ and $\tan\frac{\pi}{4} = 1$.** Let
$s = \sin\frac{\pi}{4}$. By property 6 of [](#rem-calc-trig-functions-circle-properties) with
$t = \frac{\pi}{4}$, $\cos\frac{\pi}{4} = \cos\bigl(\frac{\pi}{2} - \frac{\pi}{4}\bigr) = s$.
By [](#thm-calc-pythagorean-identity) with $t = \frac{\pi}{4}$, $s^2 + s^2 = 1$, so
$s^2 = \frac12$. By property 8, $s > 0$, since $0 < \frac{\pi}{4} < \frac{\pi}{2}$ (step 1). By
[the square-root remark](#rem-calc-square-roots), exactly one number $u \ge 0$ has
$u^2 = \frac12$, and $s$ is one. The number $\frac{1}{\sqrt{2}}$ is another: $\sqrt{2} \ge 0$,
and $\sqrt{2} \ne 0$ because $0^2 = 0 \ne 2$, so $\sqrt{2} > 0$ and $\frac{1}{\sqrt{2}} > 0$
([property 6 of the order rules](#rem-calc-order-rules)); and
$\bigl(\frac{1}{\sqrt{2}}\bigr)^2 = \frac{1}{2}$. So $s = \frac{1}{\sqrt{2}}$. As
$\cos\frac{\pi}{4} = s \ne 0$, $\tan\frac{\pi}{4} = \frac{s}{s} = 1$
([](#def-calc-tan-sec-csc-cot)).

**Step 3: the bounds.** By step 1, [](#lem-calc-sin-bounds) applies at
$\theta = \frac{\pi}{4}$: $\sin\frac{\pi}{4} < \frac{\pi}{4} < \tan\frac{\pi}{4}$, that is, by
step 2,
$$
\frac{1}{\sqrt{2}} < \frac{\pi}{4} < 1 .
$$
Multiplying by the positive number $4$ keeps both inequalities
([property 5(a) of the order rules](#rem-calc-order-rules)), and
$\frac{4}{\sqrt{2}} = \frac{2\sqrt{2}\,\sqrt{2}}{\sqrt{2}} = 2\sqrt{2}$, because
$(\sqrt{2})^2 = 2$ ([the square-root remark](#rem-calc-square-roots)) and $\sqrt{2} \ne 0$
(step 2). So $2\sqrt{2} < \pi < 4$.
:::

**In words.** Doubling gives $4\sqrt{2} < 2\pi < 8$: the circle, of length $2\pi$, is longer
than the square inscribed in it, whose perimeter is $4\sqrt{2}$, and shorter than the square
drawn around it, whose perimeter is $8$; so $\pi$ lies between $2\sqrt{2} \approx 2.83$ and $4$.

### Graphs: period, amplitude and phase

As $t$ grows, $P(t)$ goes round and round the circle, and $\sin t$ and $\cos t$ repeat.

:::{proof:definition} Period
:label: def-calc-period

Let $f$ be a function. A number $p > 0$ is a **period** of $f$ if, for every $x \in \dom f$,
also $x + p \in \dom f$ and $f(x + p) = f(x)$. A function with a period is **periodic**. If $f$
has a period $p_0$ such that no number $p$ with $0 < p < p_0$ is a period of $f$, then $p_0$ is
called **the period** of $f$.
:::

- **Period $2\pi$.** By property 3 of [](#rem-calc-trig-functions-circle-properties),
  $2\pi$ is a period of $\sin$ and of $\cos$ ([](#def-calc-period)). No smaller $p > 0$ is a
  period of $\sin$: if $\sin\bigl(\frac{\pi}{2} + p\bigr) = \sin\frac{\pi}{2} = 1$, then
  $\cos\bigl(\frac{\pi}{2} + p\bigr) = 0$ by [](#thm-calc-pythagorean-identity), so
  $P\bigl(\frac{\pi}{2} + p\bigr) = (0, 1) = P\bigl(\frac{\pi}{2}\bigr)$, and $p = 2k\pi$ for an
  integer $k$ by the converse in property 3. Multiplying $2k\pi = p > 0$ by the positive number
  $\frac{1}{2\pi}$ gives $k > 0$ ([properties 6 and 5(a) of the order
  rules](#rem-calc-order-rules)), so $k \ge 1$, as $k$ is an integer; and multiplying $k \ge 1$
  by the positive number $2\pi$ gives $p \ge 2\pi$
  ([property 5(b) of the order rules](#rem-calc-order-rules)). The same argument at $t = 0$ shows it for $\cos$. So $2\pi$ is the period of
  $\sin$ and of $\cos$.
- **Values.** The values of $\sin$ and $\cos$ fill the interval $[-1, 1]$: they lie in it by
  [](#prop-calc-sin-bounded), and every $y \in [-1, 1]$ is a value of $\sin$. Indeed $y^2 \le 1$
  (for $y \ge 0$ by the order part of [the square-root remark](#rem-calc-square-roots), and for
  $y < 0$ by the same applied to $-y$, which lies in $(0, 1]$ because multiplying
  $-1 \le y < 0$ by the negative number ${-1}$ reverses both inequalities,
  [property 5(c) of the order rules](#rem-calc-order-rules)), so $1 - y^2 \ge 0$ (adding $-y^2$, [property 3 of the order rules](#rem-calc-order-rules)) and
  the point $\bigl(\sqrt{1 - y^2}, y\bigr)$ lies on the unit circle. By the facts from school
  (journeys along the circle) it is $P(t)$ for some $t$; then $\sin t = y$. In the same way, the
  point $\bigl(y, \sqrt{1 - y^2}\bigr)$ shows that $y$ is a value of $\cos$.
- **Shape.** On $[0, 2\pi]$ the graph of $\sin$ takes the values $0$, $1$, $0$, ${-1}$ and $0$ at
  $0$, $\frac{\pi}{2}$, $\pi$, $\frac{3\pi}{2}$ and $2\pi$ (property 1), and then repeats; in between,
  the widget below shows a smooth wave. By property 6, $\cos t = \sin\bigl(t + \frac{\pi}{2}\bigr)$ (apply 6 to
  $-t$ and use 4: $\sin\bigl(\frac{\pi}{2} - (-t)\bigr) = \cos(-t) = \cos t$), so the graph of
  $\cos$ is the graph of $\sin$ shifted $\frac{\pi}{2}$ to the left.

Stretching and shifting the graph of $\sin$ gives every wave of the same shape. For numbers
$a > 0$, $b > 0$, $c$ and $d$, the function
$$
f(x) = a \sin\bigl(b(x - c)\bigr) + d
$$
has

- **amplitude** $a$: its values fill $[d - a, d + a]$, because those of $\sin$ fill $[-1, 1]$,
  and multiplying $-1 \le u \le 1$ by the positive number $a$ and then adding $d$ keeps both
  inequalities ([properties 5(b) and 3 of the order rules](#rem-calc-order-rules));
- **period** $\frac{2\pi}{b}$: shifting $x$ by $p$ shifts $b(x - c)$ by $bp$, and as
  $b(x - c)$ runs through all real numbers when $x$ does, $p$ is a period of $f$ exactly when
  $bp$ is a period of $\sin$; the smallest such $bp$ is $2\pi$;
- **phase shift** $c$: its graph is that of $a\sin(bx) + d$ shifted $c$ to the right;
- **midline** $y = d$: the wave swings between $d - a$ and $d + a$, about the line $y = d$.

::::{figure}
:label: wdg-calc-trig-functions-wave

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "a*sin(b*(x - c)) + d",
  "xRange": [-7, 7],
  "yRange": [-5.5, 5.5],
  "parameters": {
    "a": { "value": 1, "min": 0.5, "max": 3, "step": 0.5 },
    "b": { "value": 1, "min": 0.5, "max": 4, "step": 0.5 },
    "c": { "value": 0, "min": -3, "max": 3, "step": 0.25 },
    "d": { "value": 0, "min": -2, "max": 2, "step": 0.5 }
  }
}
```

Graph of $y = a\sin\bigl(b(x - c)\bigr) + d$ for $-7 \le x \le 7$, with four sliders: $a$
from $0.5$ to $3$ in steps of $0.5$, $b$ from $0.5$ to $4$ in steps of $0.5$, $c$ from ${-3}$ to
$3$ in steps of $0.25$, and $d$ from ${-2}$ to $2$ in steps of $0.5$. It starts at $a = 1$,
$b = 1$, $c = 0$ and $d = 0$, with the graph of $y = \sin x$: a wave between ${-1}$ and $1$
that crosses the $x$-axis at the multiples of $\pi \approx 3.14$ and repeats every
$2\pi \approx 6.28$. Increasing $a$ stretches the wave vertically, increasing $b$ squeezes it
horizontally, increasing $c$ shifts it to the right, and increasing $d$ shifts it up.
::::

**Try this:**

1. Set $b = 2$. How many complete waves fit between $0$ and $2\pi \approx 6.28$ now? What is
   the period?
2. Set $b = 1$ again and move $c$ to ${-1.5}$, the slider's closest value to
   $-\frac{\pi}{2} \approx -1.571$. The graph is now $y = \sin(x + 1.5)$. Which function from
   this page does it almost match, and which value of $c$, not on the slider, would match it
   exactly? (Look at the shape bullet above.)
3. Set $c = 0$, $a = 3$ and $d = 2$. Between which heights does the wave swing, and where is its
   midline?

## Worked examples

:::{proof:example} Degrees, arcs and sectors on a wheel
:label: eg-calc-trig-functions-radians

A wheel of radius $0.3$ metres turns through $150$ degrees. Find the angle in radians, the
distance travelled by a point on the rim, and the area swept out by a spoke.

1. **Radians.** A full turn is $360$ degrees and $2\pi$ radians, so $1$ degree is
   $\frac{\pi}{180}$ radians, and
   $$
   150 \cdot \frac{\pi}{180} = \frac{5\pi}{6} .
   $$
2. **Arc.** On a circle of radius $r$, an angle of $\theta$ radians cuts off an arc of length
   $r\theta$ ([Radian](#def-calc-radian) and the facts on circles of other radii). Here
   $0.3 \cdot \frac{5\pi}{6} = \frac{\pi}{4}$, in metres.
3. **Sector.** The sector has area $\frac12 r^2\theta = \frac12 \cdot 0.09 \cdot \frac{5\pi}{6}
   = \frac{3\pi}{80}$, in square metres.

$$
\boxed{
\begin{aligned}
\theta &= \frac{5\pi}{6}, \\
r\theta &= \frac{\pi}{4} \approx 0.785, \\
\tfrac12 r^2\theta &= \frac{3\pi}{80} \approx 0.118
\end{aligned}
}
$$

The arc is in metres and the area in square metres.

**Check.** $150$ degrees is $\frac{150}{360} = \frac{5}{12}$ of a full turn. The circumference
is $2\pi \cdot 0.3 = 0.6\pi$, and $\frac{5}{12} \cdot 0.6\pi = \frac{\pi}{4}$ ✓. The disc has
area $\pi \cdot 0.09$, and $\frac{5}{12} \cdot 0.09\pi = 0.0375\pi = \frac{3\pi}{80}$ ✓.
:::

:::{proof:example} Exact values at $\frac{\pi}{4}$, $\frac{\pi}{3}$ and $\frac{\pi}{6}$
:label: eg-calc-trig-functions-special-values

Find $\cos t$ and $\sin t$ exactly for $t = \frac{\pi}{4}$, $\frac{\pi}{3}$ and $\frac{\pi}{6}$.

1. **At $\frac{\pi}{4}$.** By property 6 of [](#rem-calc-trig-functions-circle-properties)
   with $t = \frac{\pi}{4}$, $\cos\frac{\pi}{4} = \sin\bigl(\frac{\pi}{2} - \frac{\pi}{4}\bigr)$,
   which is $\sin\frac{\pi}{4}$; call this common value $c$. By
   [](#thm-calc-pythagorean-identity), $c^2 + c^2 = 1$, so $c^2 = \frac12$. By property 8,
   $c > 0$, so $c$ is the non-negative square root of $\frac12$
   ([the square-root remark](#rem-calc-square-roots)). Since $\frac{\sqrt{2}}{2} \ge 0$ and
   $\bigl(\frac{\sqrt{2}}{2}\bigr)^2 = \frac{2}{4} = \frac12$, that root is $\frac{\sqrt{2}}{2}$.
2. **At $\frac{\pi}{3}$.** Let $c = \cos\frac{\pi}{3}$. Part (f) of
   [](#thm-calc-addition-formulas) gives $\cos\frac{2\pi}{3} = 2c^2 - 1$, and property 5 gives
   $\cos\frac{2\pi}{3} = \cos\bigl(\pi - \frac{\pi}{3}\bigr) = -c$. So $2c^2 - 1 = -c$, that is,
   $2c^2 + c - 1 = 0$, which factors as $(2c - 1)(c + 1) = 0$. By property 8, $c > 0$,
   so adding $1$ gives $c + 1 > 1 > 0$
   ([properties 3 and 2 of the order rules](#rem-calc-order-rules); $1 > 0$ because
   multiplying $0 < \frac{1}{c}$ by $c > 0$ gives $0 < 1$, by properties 6 and 5(a)), and
   therefore $2c - 1 = 0$: $c = \frac12$. Then
   $\sin^2\frac{\pi}{3} = 1 - \frac14 = \frac34$, and $\sin\frac{\pi}{3} > 0$, so, as in step 1,
   $\sin\frac{\pi}{3} = \frac{\sqrt{3}}{2}$.
3. **At $\frac{\pi}{6}$.** Since $\frac{\pi}{6} = \frac{\pi}{2} - \frac{\pi}{3}$, property 6 with
   $t = \frac{\pi}{3}$ gives $\cos\frac{\pi}{6} = \sin\frac{\pi}{3} = \frac{\sqrt{3}}{2}$ and
   $\sin\frac{\pi}{6} = \cos\frac{\pi}{3} = \frac12$.

So:

- $\cos\frac{\pi}{6} = \frac{\sqrt{3}}{2}$ and $\sin\frac{\pi}{6} = \frac12$;
- $\cos\frac{\pi}{4} = \sin\frac{\pi}{4} = \frac{\sqrt{2}}{2}$;
- $\cos\frac{\pi}{3} = \frac12$ and $\sin\frac{\pi}{3} = \frac{\sqrt{3}}{2}$.

Dividing, $\tan\frac{\pi}{6} = \frac{1}{\sqrt{3}} = \frac{\sqrt{3}}{3}$, $\tan\frac{\pi}{4} = 1$ and
$\tan\frac{\pi}{3} = \sqrt{3}$.

**Check.** With a calculator in radian mode, $\frac{\pi}{3} \approx 1.047198$ gives
$\cos 1.047198 \approx 0.500000$ ✓, and $\frac{\pi}{4} \approx 0.785398$ gives
$\sin 0.785398 \approx 0.707107 \approx \frac{1.414214}{2}$ ✓. Each pair satisfies
$\cos^2 t + \sin^2 t = 1$: for example $\frac14 + \frac34 = 1$ ✓.
:::

:::{proof:example} Angles outside the first quadrant
:label: eg-calc-trig-functions-other-angles

Find $\sin\frac{5\pi}{6}$, $\cos\frac{4\pi}{3}$, $\tan\bigl(-\frac{\pi}{4}\bigr)$ and
$\sin\frac{17\pi}{6}$.

The properties of [](#rem-calc-trig-functions-circle-properties) move each number to the first
quadrant, where [](#eg-calc-trig-functions-special-values) gives the values.

1. $\frac{5\pi}{6} = \pi - \frac{\pi}{6}$, so by property 5,
   $\sin\frac{5\pi}{6} = \sin\frac{\pi}{6} = \frac12$.
2. $\frac{4\pi}{3} = \frac{\pi}{3} + \pi$, so by property 7,
   $\cos\frac{4\pi}{3} = -\cos\frac{\pi}{3} = -\frac12$.
3. By property 4, $\sin\bigl(-\frac{\pi}{4}\bigr) = -\sin\frac{\pi}{4}$ and
   $\cos\bigl(-\frac{\pi}{4}\bigr) = \cos\frac{\pi}{4} \ne 0$, so
   $\tan\bigl(-\frac{\pi}{4}\bigr) = \frac{-\sin(\pi/4)}{\cos(\pi/4)} = -\tan\frac{\pi}{4} = -1$.
4. $\frac{17\pi}{6} = \frac{5\pi}{6} + 2\pi$, so by property 3 and step 1,
   $\sin\frac{17\pi}{6} = \sin\frac{5\pi}{6} = \frac12$.

$$
\boxed{
\begin{aligned}
\sin\frac{5\pi}{6} &= \frac12, \\
\cos\frac{4\pi}{3} &= -\frac12, \\
\tan\Bigl(-\frac{\pi}{4}\Bigr) &= -1, \\
\sin\frac{17\pi}{6} &= \frac12
\end{aligned}
}
$$

**Check.** The signs agree with the quadrants: $P\bigl(\frac{5\pi}{6}\bigr)$ is in the second
quadrant, where $y > 0$; $P\bigl(\frac{4\pi}{3}\bigr)$ in the third, where $x < 0$;
$P\bigl(-\frac{\pi}{4}\bigr)$ in the fourth, where $x$ and $y$ have opposite signs ✓. With a
calculator in radian mode, $\sin 8.901179 \approx 0.500000$, and $\frac{17\pi}{6} \approx 8.901179$ ✓.
:::

:::{proof:example} The cosine from the sine, and the sign
:label: eg-calc-trig-functions-sign

Given that $\sin t = \frac35$ and $\frac{\pi}{2} < t < \pi$, find $\cos t$ and $\tan t$.

1. **The square.** By [](#thm-calc-pythagorean-identity),
   $\cos^2 t = 1 - \frac{9}{25} = \frac{16}{25}$.
2. **The sign.** Let $u = \pi - t$. Multiplying $\frac{\pi}{2} < t < \pi$ by the negative number
   ${-1}$ reverses both inequalities, and adding $\pi$ keeps them
   ([properties 5(c) and 3 of the order rules](#rem-calc-order-rules)): $0 < u < \frac{\pi}{2}$. By
   property 5 of [](#rem-calc-trig-functions-circle-properties),
   $\cos t = \cos(\pi - u) = -\cos u$, and $\cos u > 0$ by property 8. So $\cos t < 0$.
3. **The value.** So $-\cos t$ is the non-negative number whose square is $\frac{16}{25}$, which
   is $\frac45$ ([the square-root remark](#rem-calc-square-roots)): $\cos t = -\frac45$.
4. **The tangent.** $\tan t = \dfrac{3/5}{-4/5} = -\dfrac34$.

$$
\boxed{\cos t = -\frac45, \qquad \tan t = -\frac34}
$$

**Check.** $\bigl(\frac35\bigr)^2 + \bigl(-\frac45\bigr)^2 = \frac{9 + 16}{25} = 1$ ✓. With a
calculator in radian mode, $t = 2.498092$ lies between $\frac{\pi}{2}$ and $\pi$ and gives
$\sin t \approx 0.600000$ and $\cos t \approx -0.800000$ ✓.
:::

:::{proof:example} An exact value from the addition formulas
:label: eg-calc-trig-functions-addition

Find $\cos\frac{\pi}{12}$ exactly.

1. **Write the angle as a difference of known ones.**
   $\frac{\pi}{3} - \frac{\pi}{4} = \frac{4\pi}{12} - \frac{3\pi}{12} = \frac{\pi}{12}$.
2. **Apply part (a) of [](#thm-calc-addition-formulas)**, with the values of
   [](#eg-calc-trig-functions-special-values):
   $$
   \begin{aligned}
   \cos\frac{\pi}{12}
     &= \cos\frac{\pi}{3}\cos\frac{\pi}{4} \\
     &\quad + \sin\frac{\pi}{3}\sin\frac{\pi}{4} \\
     &= \frac12 \cdot \frac{\sqrt{2}}{2} + \frac{\sqrt{3}}{2} \cdot \frac{\sqrt{2}}{2} \\
     &= \frac{\sqrt{2} + \sqrt{6}}{4},
   \end{aligned}
   $$
   since $\sqrt{3}\,\sqrt{2} = \sqrt{6}$ (both sides are non-negative and square to $6$).

$$
\boxed{\cos\frac{\pi}{12} = \frac{\sqrt{2} + \sqrt{6}}{4}}
$$

**Check.** $\frac{1.414214 + 2.449490}{4} \approx 0.965926$, and with a calculator in radian
mode $\cos 0.261799 \approx 0.965926$, where $\frac{\pi}{12} \approx 0.261799$ ✓.
:::

:::{proof:example} The Ferris wheel
:label: eg-calc-trig-functions-ferris-wheel

The Ferris wheel of [Why this matters](#calc-trig-functions) has radius $20$ metres and its
centre $22$ metres above the ground, turns anticlockwise as we look at it, once every $10$
minutes, and you board at the bottom at time $0$. Find your height $h(t)$, in metres, after $t$
minutes, its amplitude, period, phase shift and midline, and your height after $100$ seconds and
after $25$ minutes.

1. **The angle.** The wheel turns $2\pi$ radians in $10$ minutes at a steady speed, so after
   $t$ minutes it has turned through $\frac{2\pi t}{10} = \frac{\pi t}{5}$ radians.
2. **The position.** The wheel is the unit circle scaled by $20$ and moved to the centre (the
   facts on circles of other radii). You start at the bottom, which corresponds to
   $P\bigl(-\frac{\pi}{2}\bigr) = (0, {-1})$ (properties 4 and 1 of
   [](#rem-calc-trig-functions-circle-properties)). Turning through $\theta$ is a rotation
   that maps $A$ to $P(\theta)$, so by property 2 it takes you to the point corresponding to
   $P\bigl(\theta - \frac{\pi}{2}\bigr)$, at height $20\sin\bigl(\theta - \frac{\pi}{2}\bigr)$
   above the centre.
3. **Simplify.** By property 4 and then property 6,
   $\sin\bigl(\theta - \frac{\pi}{2}\bigr) = -\sin\bigl(\frac{\pi}{2} - \theta\bigr) = -\cos\theta$.
   With $\theta = \frac{\pi t}{5}$:
   $$
   h(t) = 22 - 20\cos\frac{\pi t}{5} .
   $$
4. **Amplitude, period, phase shift, midline.** Step 3 also says that
   $-\cos\theta = \sin\bigl(\theta - \frac{\pi}{2}\bigr)$, and
   $\frac{\pi t}{5} - \frac{\pi}{2} = \frac{\pi}{5}\bigl(t - \frac52\bigr)$, so
   $h(t) = 20\sin\bigl(\frac{\pi}{5}\bigl(t - \frac52\bigr)\bigr) + 22$: amplitude $20$, period
   $\frac{2\pi}{\pi/5} = 10$, phase shift $\frac52$ and midline $h = 22$. The heights fill
   $[22 - 20, 22 + 20] = [2, 42]$.
5. **The two times.** $100$ seconds is $\frac53$ minutes, and $\frac{\pi}{5}\cdot\frac53 =
   \frac{\pi}{3}$, so $h\bigl(\frac53\bigr) = 22 - 20 \cdot \frac12 = 12$
   ([](#eg-calc-trig-functions-special-values)). After $25$ minutes,
   $\cos(5\pi) = \cos(\pi + 4\pi) = \cos\pi = -1$ (properties 3 and 1), so
   $h(25) = 22 + 20 = 42$: you are at the top.

$$
\boxed{
\begin{aligned}
h(t) &= 22 - 20\cos\frac{\pi t}{5}, \\
h\Bigl(\frac53\Bigr) &= 12, \qquad h(25) = 42
\end{aligned}
}
$$

The heights are in metres and the times in minutes.

**Check.** $h(0) = 22 - 20 = 2$: you board at the bottom ✓. $h(10) = 22 - 20\cos 2\pi = 2$: one
turn later you are back ✓. Halfway round, $h(5) = 22 - 20\cos\pi = 42$, the top ✓.
:::

## Common mistakes

:::{warning} Reading $t$ in degrees
✗ **Wrong:** "$\sin 30 = \frac12$", or a calculator left in degree mode.

**Why:** in $\sin t$, the number $t$ is a distance along the unit circle, in radians. The angle
of $30$ degrees is $\frac{\pi}{6}$ radians; the number $30$ is almost five full turns, and
$\sin 30 \approx -0.988$.

✓ **Right:** $\sin\frac{\pi}{6} = \frac12$. Convert degrees to radians first (multiply by
$\frac{\pi}{180}$), and set your calculator to radians. Every formula of calculus for $\sin$ and
$\cos$ assumes radians.
:::

:::{warning} "Sine of a sum is the sum of the sines"
✗ **Wrong:** "$\sin(s + t) = \sin s + \sin t$", or "$\cos 2t = 2\cos t$".

**Why:** one counterexample settles it: for $s = t = \frac{\pi}{2}$ the left side is
$\sin\pi = 0$ and the right side is $1 + 1 = 2$. And $\cos(2 \cdot 0) = 1$, but $2\cos 0 = 2$.

✓ **Right:** use [](#thm-calc-addition-formulas):
$\sin(s + t) = \sin s\cos t + \cos s\sin t$ and $\cos 2t = 2\cos^2 t - 1$.
:::

:::{warning} Forgetting the sign of a square root
✗ **Wrong:** "$\sin t = \frac35$, so $\cos t = \sqrt{1 - \sin^2 t} = \frac45$."

**Why:** $\cos^2 t = 1 - \sin^2 t$ fixes $\cos t$ only up to its sign. The square root
$\sqrt{1 - \sin^2 t}$ is never negative, but $\cos t$ is negative in the second and third
quadrants.

✓ **Right:** find the sign from where $P(t)$ is, then take the root: for
$\frac{\pi}{2} < t < \pi$, $\cos t = -\frac45$ ([](#eg-calc-trig-functions-sign)).
:::

:::{warning} Getting the period backwards
✗ **Wrong:** "$\sin 2x$ is stretched by $2$, so its period is $4\pi$."

**Why:** the factor $2$ inside makes the argument $2x$ run twice as fast, so the wave repeats
*sooner*: $\sin\bigl(2(x + \pi)\bigr) = \sin(2x + 2\pi) = \sin 2x$, by property 3 of
[](#rem-calc-trig-functions-circle-properties).

✓ **Right:** $a\sin\bigl(b(x - c)\bigr) + d$ has period $\frac{2\pi}{b}$, so $\sin 2x$ has period
$\pi$. In the [widget](#wdg-calc-trig-functions-wave), $b = 2$ shows two waves on $[0, 2\pi]$.
:::

## Rigorous track

::::{admonition} Why radians, and not degrees?
:class: dropdown rigor
In degrees, the angle that cuts off an arc of length $\theta$ is $\frac{180\theta}{\pi}$, so the
"sine in degrees" is $s(x) = \sin\frac{\pi x}{180}$. Then [](#lem-calc-sin-bounds) would read
$s(x) < \frac{\pi x}{180} < \tan\frac{\pi x}{180}$ for $0 < x < 90$: the sine is no longer
compared with the angle $x$ itself, but with $\frac{\pi}{180}$ times it. In the same way, with
$\theta = \frac{\pi x}{180}$,
$$
\frac{s(x)}{x} = \frac{\pi}{180} \cdot \frac{\sin\theta}{\theta},
$$
so every statement about $\frac{\sin\theta}{\theta}$ carries the factor $\frac{\pi}{180}$ when
it is written in degrees. Radians are the unit in which the length of the arc *is* the angle,
and no such factor appears.

:::{admonition} Looking ahead
:class: looking-ahead
The page The Squeeze Theorem finds the limit of $\frac{\sin\theta}{\theta}$ as $\theta \to 0$
from [](#lem-calc-sin-bounds). In degrees that limit, and every derivative of a trigonometric
function, would carry the factor $\frac{\pi}{180}$; that is why calculus uses no unit but
radians.
:::
::::

:::{admonition} Defining sine without pictures
:class: dropdown rigor
[](#def-calc-sin-cos) rests on the length of an arc, and [](#lem-calc-sin-bounds) on the area of
a sector. Both are limits in disguise (the length of a curve is a limit of the lengths of
inscribed polygons), so a fully rigorous treatment must define them first. There are two
standard ways round this. One defines $\sin$ and $\cos$ by power series and proves every
property on this page from the series; the number $\pi$ is then defined as twice the smallest
positive zero of $\cos$. The other defines the area of a sector as an integral and the angle
from it. Either way, the facts from school become theorems. The course takes them as known
here, and the order of the pages makes sure that they are never "proved" by a result that rests
on them; that construction belongs to Real Analysis (`ana`).
:::

## Summary

- An angle in **radians** is the length of the arc it cuts off on the unit circle: a full turn
  is $2\pi$, and $180$ degrees is $\pi$. On a circle of radius $r$, the arc is $r\theta$ and the
  sector $\frac12 r^2\theta$.
- $P(t) = (\cos t, \sin t)$ is the point reached by walking a distance $t$ from $(1, 0)$ round
  the unit circle, anticlockwise for $t > 0$ ([](#def-calc-sin-cos)); $\tan t = \frac{\sin t}{\cos t}$.
- Reflections and rotations of the circle give the symmetries
  ([](#rem-calc-trig-functions-circle-properties)): period $2\pi$, $\cos$ even, $\sin$ odd, and
  values in any quadrant from values in the first.
- $\cos^2 t + \sin^2 t = 1$; $-1 \le \sin t \le 1$; $\sin(k\pi) = 0$ and
  $\sin\bigl(\frac{\pi}{2} + 2k\pi\bigr) = 1$ for every integer $k$.
- Addition formulas: $\sin(s + t) = \sin s\cos t + \cos s\sin t$ and
  $\cos(s + t) = \cos s\cos t - \sin s\sin t$.
- For $0 < \theta < \frac{\pi}{2}$: $\sin\theta < \theta < \tan\theta$, by comparing areas, with
  no derivatives ([](#lem-calc-sin-bounds)).
- $a\sin\bigl(b(x - c)\bigr) + d$ (with $a, b > 0$) has amplitude $a$, period $\frac{2\pi}{b}$,
  phase shift $c$ and midline $y = d$.

## Exercises

::::{exercise} Degrees and radians
:label: exr-calc-trig-functions-degrees-to-radians
:class: tier-a

(a) Write $210$ degrees in radians. (b) Write $\frac{3\pi}{4}$ radians in degrees.

:::{admonition} Hint 1
:class: dropdown hint
A full turn is $360$ degrees and $2\pi$ radians, so $180$ degrees is $\pi$ radians.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $\frac{7\pi}{6}$ (b) $135$
:::
::::

::::{solution} exr-calc-trig-functions-degrees-to-radians
:label: sol-calc-trig-functions-degrees-to-radians
:class: dropdown
Since $180$ degrees is $\pi$ radians, $1$ degree is $\frac{\pi}{180}$ radians and $1$ radian is
$\frac{180}{\pi}$ degrees.

(a) $210 \cdot \frac{\pi}{180} = \frac{21\pi}{18} = \frac{7\pi}{6}$ radians.

(b) $\frac{3\pi}{4} \cdot \frac{180}{\pi} = \frac{540}{4} = 135$ degrees.
::::

::::{exercise} The swing of a pendulum
:label: exr-calc-trig-functions-arc-length
:class: tier-a applied

A pendulum $0.8$ metres long swings through an angle of $0.3$ radians from one side to the
other. How far does its tip travel during one swing, in metres?

:::{admonition} Hint 1
:class: dropdown hint
The tip moves along an arc of a circle of radius $0.8$ metres. How long is the arc that an angle
of $\theta$ radians cuts off on a circle of radius $r$?
:::

:::{admonition} Answer
:class: dropdown answer
$0.24$
:::
::::

::::{solution} exr-calc-trig-functions-arc-length
:label: sol-calc-trig-functions-arc-length
:class: dropdown
The tip moves along a circle of radius $r = 0.8$ about the point where the pendulum hangs, and
the angle at the centre is $\theta = 0.3$ radians. On a circle of radius $r$ an angle of
$\theta$ radians cuts off an arc of length $r\theta$ ([Radian](#def-calc-radian) and the facts
on circles of other radii), so the tip travels $0.8 \cdot 0.3 = 0.24$ metres.
::::

::::{exercise} Sine at multiples of $\pi$
:label: exr-calc-trig-functions-multiples-of-pi
:class: tier-a

Find (a) $\sin(2026\pi)$, (b) $\sin\bigl(-\frac{7\pi}{2}\bigr)$, (c) $\cos(5\pi)$.

:::{admonition} Hint 1
:class: dropdown hint
For (b), write $-\frac{7\pi}{2} = \frac{\pi}{2} + 2k\pi$ for a suitable integer $k$.
:::

:::{admonition} Hint 2
:class: dropdown hint
For (c), use the period $2\pi$ to move $5\pi$ to a number between $0$ and $2\pi$.
:::

:::{admonition} Answer
:class: dropdown answer
(a) $0$ (b) $1$ (c) $-1$
:::
::::

::::{solution} exr-calc-trig-functions-multiples-of-pi
:label: sol-calc-trig-functions-multiples-of-pi
:class: dropdown
(a) $2026$ is an integer, so $\sin(2026\pi) = 0$ by [](#prop-calc-sin-multiples-of-pi).

(b) $-\frac{7\pi}{2} = \frac{\pi}{2} - 4\pi = \frac{\pi}{2} + 2 \cdot (-2)\pi$, so
$\sin\bigl(-\frac{7\pi}{2}\bigr) = 1$ by [](#prop-calc-sin-maxima) with $k = -2$.

(c) $5\pi = \pi + 2 \cdot 2\pi$, so by properties 3 and 1 of
[](#rem-calc-trig-functions-circle-properties), $P(5\pi) = P(\pi) = ({-1}, 0)$, and
$\cos(5\pi) = -1$.
::::

::::{exercise} Exact values
:label: exr-calc-trig-functions-exact-values
:class: tier-a

Find exactly (a) $\cos\frac{5\pi}{6}$, (b) $\sin\frac{5\pi}{4}$, (c) $\tan\frac{2\pi}{3}$.

:::{admonition} Hint 1
:class: dropdown hint
Write each angle as $\pi - t$ or $t + \pi$ with $t$ in the first quadrant, as in
[](#eg-calc-trig-functions-other-angles).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $-\frac{\sqrt{3}}{2}$ (b) $-\frac{\sqrt{2}}{2}$ (c) $-\sqrt{3}$
:::
::::

::::{solution} exr-calc-trig-functions-exact-values
:label: sol-calc-trig-functions-exact-values
:class: dropdown
We use the properties of [](#rem-calc-trig-functions-circle-properties) and the values of
[](#eg-calc-trig-functions-special-values).

(a) $\frac{5\pi}{6} = \pi - \frac{\pi}{6}$, so by property 5,
$\cos\frac{5\pi}{6} = -\cos\frac{\pi}{6} = -\frac{\sqrt{3}}{2}$.

(b) $\frac{5\pi}{4} = \frac{\pi}{4} + \pi$, so by property 7,
$\sin\frac{5\pi}{4} = -\sin\frac{\pi}{4} = -\frac{\sqrt{2}}{2}$.

(c) $\frac{2\pi}{3} = \pi - \frac{\pi}{3}$, so by property 5,
$\sin\frac{2\pi}{3} = \sin\frac{\pi}{3} = \frac{\sqrt{3}}{2}$ and
$\cos\frac{2\pi}{3} = -\cos\frac{\pi}{3} = -\frac12$. Hence
$\tan\frac{2\pi}{3} = \dfrac{\sqrt{3}/2}{-1/2} = -\sqrt{3}$.
::::

::::{exercise} Sine and tangent from the cosine
:label: exr-calc-trig-functions-from-cosine
:class: tier-b

Given that $\cos t = -\frac{5}{13}$ and $\pi < t < \frac{3\pi}{2}$, find (a) $\sin t$ and
(b) $\tan t$.

:::{admonition} Hint 1
:class: dropdown hint
[](#thm-calc-pythagorean-identity) gives $\sin^2 t$. In which quadrant is $P(t)$, and what is
the sign of $\sin t$ there?
:::

:::{admonition} Hint 2
:class: dropdown hint
Write $t = u + \pi$ and use property 7 of [](#rem-calc-trig-functions-circle-properties).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $-\frac{12}{13}$ (b) $\frac{12}{5}$
:::
::::

::::{solution} exr-calc-trig-functions-from-cosine
:label: sol-calc-trig-functions-from-cosine
:class: dropdown
We follow [](#eg-calc-trig-functions-sign).

(a) By [](#thm-calc-pythagorean-identity), $\sin^2 t = 1 - \frac{25}{169} = \frac{144}{169}$.
For the sign, let $u = t - \pi$; subtracting $\pi$ from $\pi < t < \frac{3\pi}{2}$ keeps both
inequalities ([property 3 of the order rules](#rem-calc-order-rules)) and gives
$0 < u < \frac{\pi}{2}$. By property 7 of [](#rem-calc-trig-functions-circle-properties),
$\sin t = \sin(u + \pi) = -\sin u$, and $\sin u > 0$ by property 8. So $\sin t < 0$, and
$-\sin t$ is the non-negative number whose square is $\frac{144}{169}$, namely $\frac{12}{13}$
([the square-root remark](#rem-calc-square-roots)). So $\sin t = -\frac{12}{13}$.

(b) $\tan t = \dfrac{-12/13}{-5/13} = \dfrac{12}{5}$.
::::

::::{exercise} An exact value of sine
:label: exr-calc-trig-functions-addition
:class: tier-b

Find $\sin\frac{5\pi}{12}$ exactly.

:::{admonition} Hint 1
:class: dropdown hint
$\frac{5\pi}{12} = \frac{\pi}{4} + \frac{\pi}{6}$.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{\sqrt{6} + \sqrt{2}}{4}$
:::
::::

::::{solution} exr-calc-trig-functions-addition
:label: sol-calc-trig-functions-addition
:class: dropdown
Since $\frac{\pi}{4} + \frac{\pi}{6} = \frac{3\pi}{12} + \frac{2\pi}{12} = \frac{5\pi}{12}$,
part (c) of [](#thm-calc-addition-formulas) and the values of
[](#eg-calc-trig-functions-special-values) give
$$
\begin{aligned}
\sin\frac{5\pi}{12}
  &= \sin\frac{\pi}{4}\cos\frac{\pi}{6} \\
  &\quad + \cos\frac{\pi}{4}\sin\frac{\pi}{6} \\
  &= \frac{\sqrt{2}}{2}\cdot\frac{\sqrt{3}}{2} + \frac{\sqrt{2}}{2}\cdot\frac12 \\
  &= \frac{\sqrt{6} + \sqrt{2}}{4} .
\end{aligned}
$$
This is the value of $\cos\frac{\pi}{12}$ found in [](#eg-calc-trig-functions-addition), as it
must be: by property 6 of [](#rem-calc-trig-functions-circle-properties),
$\sin\frac{5\pi}{12} = \cos\bigl(\frac{\pi}{2} - \frac{5\pi}{12}\bigr) = \cos\frac{\pi}{12}$.
::::

::::{exercise} Solving an equation on one turn
:label: exr-calc-trig-functions-solve-sine
:class: tier-b

Find all $t$ in $[0, 2\pi)$ with $\sin t = -\frac12$.

:::{admonition} Hint 1
:class: dropdown hint
Which points $(x, y)$ of the unit circle have $y = -\frac12$?
:::

:::{admonition} Hint 2
:class: dropdown hint
Each point of the circle is $P(t)$ for exactly one $t$ in $[0, 2\pi)$ (the facts from school).
Use properties 4, 7 and 3 of [](#rem-calc-trig-functions-circle-properties) to find that $t$
for each point.
:::

:::{admonition} Answer
:class: dropdown answer set
$\frac{7\pi}{6}, \frac{11\pi}{6}$
:::
::::

::::{solution} exr-calc-trig-functions-solve-sine
:label: sol-calc-trig-functions-solve-sine
:class: dropdown
$\sin t = -\frac12$ means that $P(t)$ is a point of the unit circle with $y = -\frac12$. For such
a point, $x^2 = 1 - \frac14 = \frac34$, so $x = \frac{\sqrt{3}}{2}$ or $x = -\frac{\sqrt{3}}{2}$
([the square-root remark](#rem-calc-square-roots)). So there are exactly two such points, and
each is $P(t)$ for exactly one $t$ in $[0, 2\pi)$ (the facts from school). We find those $t$
with [](#rem-calc-trig-functions-circle-properties) and
[](#eg-calc-trig-functions-special-values):

- $\bigl(-\frac{\sqrt{3}}{2}, -\frac12\bigr)$: by property 7,
  $P\bigl(\frac{\pi}{6} + \pi\bigr) = \bigl(-\cos\frac{\pi}{6}, -\sin\frac{\pi}{6}\bigr)$, which
  is this point, and $\frac{7\pi}{6}$ lies in $[0, 2\pi)$.
- $\bigl(\frac{\sqrt{3}}{2}, -\frac12\bigr)$: by property 4,
  $P\bigl(-\frac{\pi}{6}\bigr) = \bigl(\cos\frac{\pi}{6}, -\sin\frac{\pi}{6}\bigr)$, which is this
  point, and by property 3 it is also $P\bigl(-\frac{\pi}{6} + 2\pi\bigr) = P\bigl(\frac{11\pi}{6}\bigr)$,
  with $\frac{11\pi}{6}$ in $[0, 2\pi)$.

So the solutions in $[0, 2\pi)$ are $t = \frac{7\pi}{6}$ and $t = \frac{11\pi}{6}$.
::::

::::{exercise} Reading a wave
:label: exr-calc-trig-functions-widget-wave
:class: tier-b widget

Let $f(x) = 2\sin 3x + 1$. Set the sliders of [the widget](#wdg-calc-trig-functions-wave) to
$a = 2$, $b = 3$, $c = 0$ and $d = 1$, and read off the largest value of $f$ and the length of
one wave. Then find exactly (a) the largest value of $f$ and (b) its period.

:::{admonition} Hint 1
:class: dropdown hint
Compare $f$ with $a\sin\bigl(b(x - c)\bigr) + d$ in Graphs: period, amplitude and phase.
:::

:::{admonition} Hint 2
:class: dropdown hint
For (a), where is $\sin 3x = 1$?
:::

:::{admonition} Answer
:class: dropdown answer
(a) $3$ (b) $\frac{2\pi}{3}$
:::
::::

::::{solution} exr-calc-trig-functions-widget-wave
:label: sol-calc-trig-functions-widget-wave
:class: dropdown
The function is $a\sin\bigl(b(x - c)\bigr) + d$ with $a = 2$, $b = 3$, $c = 0$ and $d = 1$. In the
widget, the wave swings between ${-1}$ and $3$, and about three waves fit between $0$ and
$2\pi \approx 6.28$.

(a) By [part (a) of the bounds on sine](#prop-calc-sin-bounded), $\sin 3x \le 1$.
Multiplying by the positive number $2$ and adding $1$ keep the inequality
([properties 5(b) and 3 of the order rules](#rem-calc-order-rules)), so $f(x) \le 2 + 1 = 3$ for every $x$. The value $3$ is taken: at $x = \frac{\pi}{6}$,
$\sin\frac{\pi}{2} = 1$ by property 1 of [](#rem-calc-trig-functions-circle-properties), so
$f\bigl(\frac{\pi}{6}\bigr) = 3$. The largest value is $3$.

(b) The period of $a\sin\bigl(b(x - c)\bigr) + d$ is $\frac{2\pi}{b}$ (Graphs: period,
amplitude and phase), here $\frac{2\pi}{3} \approx 2.09$: three waves on $[0, 2\pi]$, as in the
widget.
::::

::::{exercise} When is the seat 32 metres up?
:label: exr-calc-trig-functions-ferris-times
:class: tier-b applied

On the Ferris wheel of [](#eg-calc-trig-functions-ferris-wheel), your height after $t$ minutes
is $h(t) = 22 - 20\cos\frac{\pi t}{5}$ metres. At which two times $t$ in $[0, 10)$ are you $32$
metres above the ground? Give (a) the earlier and (b) the later time, in minutes.

:::{admonition} Hint 1
:class: dropdown hint
Solve $h(t) = 32$ for $\cos\frac{\pi t}{5}$, and put $u = \frac{\pi t}{5}$. Which interval does
$u$ run through when $t$ runs through $[0, 10)$?
:::

:::{admonition} Hint 2
:class: dropdown hint
Find the points of the unit circle with $x = -\frac12$, as in
[](#exr-calc-trig-functions-solve-sine).
:::

:::{admonition} Answer
:class: dropdown answer
(a) $\frac{10}{3}$ (b) $\frac{20}{3}$
:::
::::

::::{solution} exr-calc-trig-functions-ferris-times
:label: sol-calc-trig-functions-ferris-times
:class: dropdown
$h(t) = 32$ means $20\cos\frac{\pi t}{5} = -10$, that is, $\cos u = -\frac12$ with
$u = \frac{\pi t}{5}$. Multiplying $0 \le t < 10$ by the positive number $\frac{\pi}{5}$ keeps
both inequalities, and dividing by it (multiplying by $\frac{5}{\pi}$, which is positive) does
too ([properties 5 and 6 of the order rules](#rem-calc-order-rules)), so as $t$ runs through $[0, 10)$, $u$ runs through $[0, 2\pi)$.

The points of the unit circle with $x = -\frac12$ have $y^2 = 1 - \frac14 = \frac34$, so they are
$\bigl(-\frac12, \frac{\sqrt{3}}{2}\bigr)$ and $\bigl(-\frac12, -\frac{\sqrt{3}}{2}\bigr)$
([the square-root remark](#rem-calc-square-roots)). Each is $P(u)$ for exactly one $u$ in
$[0, 2\pi)$ (the facts from school). With the values of
[](#eg-calc-trig-functions-special-values):

- property 5 of [](#rem-calc-trig-functions-circle-properties) gives
  $P\bigl(\pi - \frac{\pi}{3}\bigr) = \bigl(-\frac12, \frac{\sqrt{3}}{2}\bigr)$, so $u = \frac{2\pi}{3}$;
- property 7 gives $P\bigl(\frac{\pi}{3} + \pi\bigr) = \bigl(-\frac12, -\frac{\sqrt{3}}{2}\bigr)$, so
  $u = \frac{4\pi}{3}$.

Then $t = \frac{5u}{\pi}$ gives $t = \frac{10}{3}$ and $t = \frac{20}{3}$: after
$3\frac13$ minutes on the way up and after $6\frac23$ minutes on the way down.
::::

::::{exercise} Cosine decreases on $[0, \pi]$
:label: exr-calc-trig-functions-cos-decreasing
:class: tier-c rigor

Show from [](#def-calc-monotone) that $\cos$ is strictly decreasing on $[0, \pi]$.

:::{admonition} Hint 1
:class: dropdown hint
For $0 \le v < u \le \pi$, write $v = m - d$ and $u = m + d$ with $m = \frac{u + v}{2}$ and
$d = \frac{u - v}{2}$.
:::

:::{admonition} Hint 2
:class: dropdown hint
Subtract part (b) of [](#thm-calc-addition-formulas) from part (a):
$\cos(m - d) - \cos(m + d) = 2\sin m \sin d$. What are the signs of $\sin m$ and $\sin d$?
:::

:::{admonition} Answer
:class: dropdown answer manual
For $0 \le v < u \le \pi$, $\cos v - \cos u = 2\sin\frac{u + v}{2}\sin\frac{u - v}{2} > 0$.
:::
::::

::::{solution} exr-calc-trig-functions-cos-decreasing
:label: sol-calc-trig-functions-cos-decreasing
:class: dropdown
We write the difference $\cos v - \cos u$ as a product with the addition formulas and show that
both factors are positive.

Let $v, u \in [0, \pi]$ with $v < u$. We must show $\cos v > \cos u$. Let $m = \frac{u + v}{2}$
and $d = \frac{u - v}{2}$, so that $v = m - d$ and $u = m + d$. By parts (a) and (b) of
[](#thm-calc-addition-formulas),
$$
\begin{aligned}
&\cos v - \cos u \\
&= \cos(m - d) - \cos(m + d) \\
&= \cos m\cos d + \sin m\sin d \\
&\quad - (\cos m\cos d - \sin m\sin d) \\
&= 2\sin m\sin d .
\end{aligned}
$$
Now $0 \le v < u \le \pi$ gives $0 < u + v < 2\pi$: adding $0 \le v$ and $0 < u$ gives
$0 < u + v$, and adding $v < \pi$ and $u \le \pi$ gives $u + v < 2\pi$ ([property 4 of the order
rules](#rem-calc-order-rules): adding two inequalities, one of them strict, gives a strict one).
Multiplying by the positive number $\frac12$ keeps both inequalities (property 5(a) of the
order rules), so $0 < m < \pi$. Also,
subtracting $v$ keeps $v < u$ and $u \le \pi$ (property 3 of the order rules), so $0 < u - v$
and $u - v \le \pi - v$; and $\pi - v \le \pi$, because multiplying $0 \le v$ by ${-1}$ gives
$-v \le 0$ (property 5(c)) and adding $\pi$ keeps that (property 3). So $0 < u - v \le \pi$;
multiplying by the positive number $\frac12$ gives $0 < d \le \frac{\pi}{2} < \pi$. By property 8 of
[](#rem-calc-trig-functions-circle-properties), $\sin m > 0$ and $\sin d > 0$. So
$\cos v - \cos u = 2\sin m\sin d > 0$, that is, $\cos v > \cos u$. As $v < u$ in $[0, \pi]$ were
arbitrary, $\cos$ is strictly decreasing on $[0, \pi]$.
::::

::::{exercise} The period of the tangent
:label: exr-calc-trig-functions-tan-period
:class: tier-c

Show that $\pi$ is a period of $\tan$, and that no number $p$ with $0 < p < \pi$ is.

:::{admonition} Hint 1
:class: dropdown hint
For the first part, use property 7 of [](#rem-calc-trig-functions-circle-properties). Check the
domain condition in [](#def-calc-period) too.
:::

:::{admonition} Hint 2
:class: dropdown hint
For the second part, suppose $p$ is a period and put $x = 0$. Then use
[](#rem-calc-trig-functions-zeros).
:::

:::{admonition} Answer
:class: dropdown answer manual
$\tan(t + \pi) = \frac{-\sin t}{-\cos t} = \tan t$; and a period $p$ has $\tan p = \tan 0 = 0$, so
$\sin p = 0$ and $p$ is a positive multiple of $\pi$.
:::
::::

::::{solution} exr-calc-trig-functions-tan-period
:label: sol-calc-trig-functions-tan-period
:class: dropdown
*$\pi$ is a period.* Let $t \in \dom \tan$, so $\cos t \ne 0$. By property 7 of
[](#rem-calc-trig-functions-circle-properties), $\cos(t + \pi) = -\cos t \ne 0$, so
$t + \pi \in \dom\tan$, and
$\tan(t + \pi) = \frac{\sin(t + \pi)}{\cos(t + \pi)} = \frac{-\sin t}{-\cos t} = \tan t$.

*No smaller period.* Let $p > 0$ be a period of $\tan$. Since $0 \in \dom\tan$ ($\cos 0 = 1$),
[](#def-calc-period) gives $p = 0 + p \in \dom\tan$ and $\tan p = \tan 0 = 0$. So
$\frac{\sin p}{\cos p} = 0$, and multiplying by $\cos p \ne 0$ gives $\sin p = 0$. By
[](#rem-calc-trig-functions-zeros), $p = k\pi$ for an integer $k$. Multiplying $k\pi = p > 0$
by the positive number $\frac{1}{\pi}$ gives $k > 0$
([properties 6 and 5(a) of the order rules](#rem-calc-order-rules)), so $k \ge 1$, as $k$ is an
integer. Multiplying $k \ge 1$ by the positive number $\pi$ gives $p \ge \pi$
([property 5(b) of the order rules](#rem-calc-order-rules)). So $\pi$ is the period of $\tan$ ([](#def-calc-period)).
::::

::::{exercise} Squeezing $\frac{\sin\theta}{\theta}$
:label: exr-calc-trig-functions-sin-over-theta
:class: tier-c rigor

Use [](#lem-calc-sin-bounds) to show that
$$
\cos\theta < \frac{\sin\theta}{\theta} < 1
$$
for every $\theta$ with $0 < \theta < \frac{\pi}{2}$, and then for every $\theta$ with
$-\frac{\pi}{2} < \theta < 0$.

:::{admonition} Hint 1
:class: dropdown hint
Divide $\sin\theta < \theta$ by $\theta$, and multiply $\theta < \tan\theta$ by $\cos\theta$.
What are the signs of $\theta$ and $\cos\theta$?
:::

:::{admonition} Hint 2
:class: dropdown hint
For $\theta < 0$, put $\phi = -\theta$ and use property 4 of
[](#rem-calc-trig-functions-circle-properties).
:::

:::{admonition} Answer
:class: dropdown answer manual
From $\sin\theta < \theta < \frac{\sin\theta}{\cos\theta}$, multiplying by the positive numbers
$\frac{1}{\theta}$ and $\frac{\cos\theta}{\theta}$; for $\theta < 0$, both sides are unchanged when
$\theta$ is replaced by $-\theta$.
:::
::::

::::{solution} exr-calc-trig-functions-sin-over-theta
:label: sol-calc-trig-functions-sin-over-theta
:class: dropdown
Let $0 < \theta < \frac{\pi}{2}$. By [](#lem-calc-sin-bounds), $\sin\theta < \theta$ and
$\theta < \tan\theta = \frac{\sin\theta}{\cos\theta}$, where $\cos\theta > 0$ by property 8 of
[](#rem-calc-trig-functions-circle-properties).

- Multiplying $\sin\theta < \theta$ by the positive number $\frac{1}{\theta}$ keeps the strict
  inequality ([property 5(a) of the order rules](#rem-calc-order-rules)):
  $\frac{\sin\theta}{\theta} < 1$.
- Multiplying $\theta < \frac{\sin\theta}{\cos\theta}$ by the positive number
  $\frac{\cos\theta}{\theta}$ keeps it too: $\cos\theta < \frac{\sin\theta}{\theta}$.

Now let $-\frac{\pi}{2} < \theta < 0$, and $\phi = -\theta$, so that $0 < \phi < \frac{\pi}{2}$.
By property 4, $\cos\theta = \cos\phi$ and $\sin\theta = -\sin\phi$, so
$\frac{\sin\theta}{\theta} = \frac{-\sin\phi}{-\phi} = \frac{\sin\phi}{\phi}$. The first part,
for $\phi$, gives $\cos\phi < \frac{\sin\phi}{\phi} < 1$, which is the claim for $\theta$.
::::

## Where this leads

:::{where-this-leads}
:::

The page The Squeeze Theorem traps $\frac{\sin x}{x}$ between $\cos x$ and $1$, as in
[](#exr-calc-trig-functions-sin-over-theta), and finds its limit at $0$; from it come the
derivatives of all six trigonometric functions.
