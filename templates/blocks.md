# Block snippets

Copy-paste snippets for every block type. Rules: `docs/plan/03-content-model.md` §3.4.
Label grammar: `<kind>-<subj>-<slug>` with only `[a-z0-9-]` (see `docs/plan/02-information-architecture.md` §2.4).
Nesting: the **outer** directive needs more colons than the inner ones (`::::` around `:::`).

## Definition

```markdown
:::{proof:definition} Continuity at a point
:label: def-calc-continuity

A function $f$ is **continuous at $a$** if $f$ is defined at $a$ and
$$
\lim_{x \to a} f(x) = f(a).
$$
:::

**In words.** …  **Example.** …  **Non-example.** …
```

## Theorem with a core proof (policy F)

```markdown
:::{proof:theorem} Mean value theorem
:label: thm-calc-mvt

Let $f$ be continuous on $[a, b]$ and differentiable on $(a, b)$, where $a < b$. Then there is
a $c \in (a, b)$ with
$$
f'(c) = \frac{f(b) - f(a)}{b - a}.
$$
:::

:::{proof:proof}
:label: prf-calc-mvt
:enumerated: false
We apply [Rolle's theorem](#thm-calc-rolle) to $f$ minus its secant line. Define …
:::
```

Always `{proof:proof}` with `:enumerated: false`: it renders "Proof". A bare `{proof}` has no
kind, and the theme heads it with just a number.

## Proof in the rigorous track (policy R)

```markdown
:::{proof:proof} Rigorous track
:label: prf-calc-squeeze
:enumerated: false
:class: dropdown
Let $\eps > 0$. Since $\lim_{x\to a} g(x) = L$, there is $\delta_1 > 0$ such that …
:::
```

## Proof sketch (policy S)

A sketch says what it leaves out. If the full proof is on the same page (policy "S in core,
R in the rigorous track", as for the IVT), point to it.

```markdown
:::{proof:proof} Sketch
:enumerated: false
Bisect $[a,b]$ repeatedly, keeping the half on which $f$ changes sign. The nested intervals
shrink to a point $c$, and continuity forces $f(c) = 0$.
*Why the intervals shrink to a point of $[a,b]$ needs the [completeness axiom](#ax-calc-completeness);
the full proof is in the rigorous track below.*
:::
```

## Deferred proof (policy D)

A deferred proof names where the proof lives. Until the target subject exists, say what it
needs.

```markdown
:::{proof:proof} Sketch
:enumerated: false
A continuous $f$ on $[a,b]$ is bounded, and its supremum is approached by values $f(x_n)$; a
convergent subsequence of $(x_n)$ gives a point where the supremum is attained.
*The complete proof needs the Bolzano–Weierstrass theorem; it belongs to Real Analysis
(`ana`), which does not exist yet.*
:::
```

## Lemma, corollary, proposition, axiom

```markdown
:::{proof:lemma} Limits ignore a single point
:label: lem-calc-limit-agree-except-point
…
:::

:::{proof:corollary} Zero derivative means constant
:label: cor-calc-zero-derivative-constant
This follows from the [mean value theorem](#thm-calc-mvt). …
:::

:::{proof:axiom} Completeness of $\R$
:label: ax-calc-completeness
Every non-empty subset of $\R$ that is bounded above has a least upper bound.
:::
```

## Worked example

```markdown
:::{proof:example} Find $\lim_{x \to 3} \frac{x^2 - 9}{x - 3}$
:label: eg-calc-computing-limits-factor

1. Direct substitution gives $\frac{0}{0}$, so we simplify first.
2. For $x \ne 3$: $\dfrac{x^2-9}{x-3} = \dfrac{(x-3)(x+3)}{x-3} = x + 3$.
3. By [the lemma](#lem-calc-limit-agree-except-point), the limits agree:
   $\lim_{x\to3}(x+3) = 6$.

$$\boxed{6}$$

**Check.** $x = 3.001$: $\frac{3.001^2 - 9}{0.001} = 6.001$. ✓
:::
```

## Remark

```markdown
:::{proof:remark} Why the hypothesis "on an interval" matters
:label: rem-calc-antiderivative-interval
On $\R\setminus\{0\}$, both $\ln\abs{x}$ and $\ln\abs{x} + \sgn(x)$ have derivative $1/x$. …
:::
```

## Common mistake

```markdown
:::{warning} Cancelling before checking the domain
✗ **Wrong:** "$\frac{x^2-9}{x-3} = x+3$, so the function is continuous at $3$."

**Why:** the left-hand side is undefined at $x = 3$; the equality only holds for $x \ne 3$.

✓ **Right:** the *limits* agree, but $f$ has a removable discontinuity at $3$.
:::
```

## Rigorous aside (not a proof)

```markdown
:::{admonition} Each hypothesis of the EVT is needed
:class: dropdown rigor
- Not closed: $f(x) = x$ on $(0, 1)$ has no maximum.
- Not continuous: …
:::
```

## Looking ahead (allowed forward reference)

```markdown
:::{admonition} Looking ahead
:class: looking-ahead
This fact is proved in [The Logarithm Defined as an Integral](#calc-ln-integral).
:::
```

## Facts from school (only by the owner's ruling)

A page may use a few elementary facts that are proved on a page **outside its prerequisite
closure** only when the owner has ruled so in the PR (the other way out is a `curriculum` PR
that adds the prerequisite). A `looking-ahead` admonition is not enough when a proof rests on
the facts. The box:

- sits just before the first use, and the sentence before it names **every** place on the page
  that uses the facts (figures, examples, common mistakes, exercises with their hints and
  solutions);
- lists **exactly** the facts used, as a bulleted list (a display would scroll sideways on a
  phone), and nothing that goes beyond them: check each use against the list, and reword any
  sentence that needs more (for example "runs through all values between −1 and 1" needs more
  than $-1 \le \sin t \le 1$);
- is a `{proof:remark}` with the label `rem-<subj>-<topic slug>-school-facts`, so that later
  uses link to it. Not an `{admonition}`: the theme renders no anchor for a labelled
  admonition, so a link to one goes nowhere (found on `calc-limit`'s box after it merged);
- names the page that proves the facts in plain text (it is outside the closure, so no link).
  That page's `curriculum.yml` entry must list each fact as a result (a `curriculum` PR, as
  vronnblom/maths#14 did for `calc-trig-functions`), so that the promise rests on the plan;
- or, for facts proved **outside this course**, names the subject that proves them ("proved in
  Real Analysis"), and the circularity table of `docs/plan/08-calculus-curriculum.md` §8.3 has
  a matching row (stated early in this page, proved in that subject), so that the promise rests
  on the plan there instead; no curriculum entry lists them (the geometry of the unit circle in
  `calc-trig-functions` is the case in point).

The verifier tests each fact, and each use as an instance of one. A function that the closure
could replace is replaced instead: `calc-limit` swapped $(2^x - 1)/x$ for
$(\sqrt{1 + x} - 1)/x$.

```markdown
The sine function appears in the next figure, the worked example on $\sin(1/x)$, the common
mistake "Checking one $\eps$, or a few points", and the exercise on $\sin(\pi/x)$ (its
statement, hints and solution). They use only the facts about it in the box below.

:::{proof:remark} Facts from school used on this page
:label: rem-calc-limit-school-facts

With $t$ in radians:

- $\sin(k\pi) = 0$ for every integer $k$;
- $\sin\bigl(\frac{\pi}{2} + 2k\pi\bigr) = 1$ for every integer $k$;
- $-1 \le \sin t \le 1$ for every real number $t$.

These are the only facts about $\sin$ that this page uses. The page Trigonometric Functions, in
the Preliminaries chapter, defines $\sin$ and proves them.
:::
```

Later uses cite it: `by [the facts from school](#rem-calc-limit-school-facts)`.

For facts proved outside the course, the last paragraph of the box names the subject instead:

```markdown
These are the only facts about the unit circle that this page uses. They are proved in Real
Analysis, from a construction of $\sin$ and $\cos$ that does not rest on them.
```

## Steps that say what they rest on

Every step of a proof, an example or a solution names the hypothesis, the definition clause or
the result it uses, and cites parts and properties exactly: the letter of a theorem's part, the
number of a remark's property, and only what that statement says (a fact inside another page's
proof or an unlabelled dropdown is not citable; ask for it to be stated). Before multiplying or
dividing an inequality, state the sign of the factor and name the order rule
([Absolute Value and Inequalities](#calc-absolute-value-inequalities), "Working with
inequalities"): a positive factor keeps a strict inequality, a negative one reverses it, and
one that may be $0$ gives only $\le$.

```markdown
Since $\delta \le 1$, step 2 gives $\abs{x + 2} < 5$. Multiplying this by the positive number
$\abs{x - 2}$ (positive because $0 < \abs{x - 2}$) keeps the strict inequality, and
$\abs{x - 2} < \delta \le \frac{\eps}{5}$:
$$
\abs{x^2 - 4} = \abs{x - 2}\,\abs{x + 2} < 5\abs{x - 2} < 5 \cdot \frac{\eps}{5} = \eps .
$$
The first of these says also that $\abs{L - f(x)} < \eps$, because
$\abs{L - f(x)} = \abs{f(x) - L}$ by
[property 2 of the absolute value](#rem-calc-absolute-value-properties). By
[part (b) of the triangle inequality](#thm-calc-triangle-inequality), with $u = L$, $v = M$
and $w = f(x)$, …
```

## Displays on a phone

At 375 px a display wider than the screen scrolls sideways inside its box, and the reader may
not see that it goes on. Keep units and words in the sentence, not inside the display, and split
a long chain over lines with `aligned`, one relation per line:

```markdown
Its average speed is
$$
\frac{s(1 + h) - s(1)}{h} = \frac{5(1+h)^2 - 5}{h},
$$
in metres per second.

$$
\begin{aligned}
\bigl(\sqrt{4.1} + \sqrt{3.9}\bigr)^2
  &= 4.1 + 2\sqrt{4.1}\,\sqrt{3.9} + 3.9 \\
  &< 8 + 2 \cdot 4 = 16 = 4^2 .
\end{aligned}
$$
```

In inline maths, a negative number alone is written `${-1}$`: mystmd turns number-only inline
maths into plain text, and `$-1$` then shows a hyphen instead of a minus sign.

## Drafting ahead: `% TODO link`

A page drafted before a prerequisite is merged (10 §10.4) names the result in plain text and
leaves a MyST comment, which the PR body lists (`grep -n TODO` prints exactly these lines):

```markdown
By the Archimedean property, there is an integer $n \ge 1$ with $n > \frac{1}{2\pi\delta}$.
% TODO link: rem-calc-naturals-unbounded once vronnblom/maths#8 is merged
```

After the prerequisite merges: merge `main` into the branch, replace every `% TODO link` with a
named link (`By [the Archimedean property](#rem-calc-naturals-unbounded), …`), and check that
the target's **statement**, as merged, says what the step uses (not its proof, nor an example
on that page). `grep -n TODO <page>` prints nothing before the page leaves draft.

## Exercise with hints, answer and solution

```markdown
::::{exercise} Rationalising the numerator
:label: exr-calc-computing-limits-conjugate
:class: tier-b

Compute $\displaystyle\lim_{x \to 0} \frac{\sqrt{x+1} - 1}{x}$.

:::{admonition} Hint 1
:class: dropdown hint
Direct substitution gives $\tfrac{0}{0}$.
:::

:::{admonition} Hint 2
:class: dropdown hint
Multiply by the conjugate $\sqrt{x+1} + 1$.
:::

:::{admonition} Answer
:class: dropdown answer
$\frac{1}{2}$
:::
::::

::::{solution} exr-calc-computing-limits-conjugate
:label: sol-calc-computing-limits-conjugate
:class: dropdown
For $x \ne 0$, …
::::
```

Answer classes (add after `dropdown answer`):
`antiderivative` · `set` · `bool` · `numeric-<tol>` (e.g. `numeric-1e-4`) · `manual`.
One Answer, one type: if a question needs two different types (a limit and a True/False,
say), rephrase it so that one part is the Answer and the other is a "show that …" that the
solution checks.
Tier classes on the exercise: `tier-a` · `tier-b` · `tier-c`, plus optional `rigor`, `applied`, `widget`.

## Widget

````markdown
::::{figure}
:label: wdg-calc-tangents-rates-secant

```{anywidget} ../../../widgets/secant-tangent.mjs
{
  "f": "x^3 - x",
  "a": 1,
  "h": 0.5, "hRange": [-1, 1],
  "xRange": [-1.5, 2.5], "yRange": [-2, 7]
}
```

Graph of $y = x^3 - x$ with a secant line through the points at $x = 1$ and $x = 1 + h$. As
$h$ approaches $0$ the secant approaches the tangent of slope $2$.
::::

**Try this:** …
````

- The widget sits **alone in a `{figure}`**. The figure carries the `wdg-` label (the JSON can't:
  mystmd ignores ids there), and its **caption is the text description**. The caption is
  static HTML, so readers get it even when JavaScript is off or the widget fails to load.
  Required, and checked by CI.
- The path is relative to the page (`../../../widgets/` from `content/<subject>/<chapter>/`).
- The JSON must validate against `schema/widgets/<widget>.schema.json`. Use only widgets that
  exist: `widgets/README.md` is the catalogue (`secant-tangent`, shown here, comes in Phase 3).
- Choose `xRange`/`yRange` so that every point the sliders can move stays in view. Here
  $f(1+h)$ ranges over about $[-0.4, 6]$ for $h \in [-1, 1]$.

## Figure

```markdown
:::{figure} ./img/squeeze-sin-1-over-x.svg
:label: fig-calc-squeeze-oscillation
:alt: The graph of x·sin(1/x) oscillating between the lines y = x and y = −x, which squeeze it to 0 at the origin.

$x \sin(1/x)$ is squeezed between $-\abs{x}$ and $\abs{x}$.
:::
```

## Labelled equation

```markdown
$$
f(x) \approx f(a) + f'(a)(x - a)
$$ (eq-calc-linearisation)

…as in [](#eq-calc-linearisation).
```

## Cross-references

```markdown
Same page:      [](#thm-calc-squeeze)                → "Theorem 2"
Other page:     [the squeeze theorem](#thm-calc-squeeze)   (always name it)
Title only:     [{name}](#thm-calc-squeeze)
Whole page:     [](#calc-squeeze-theorem)
```
