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

:::{proof}
:label: prf-calc-mvt
We apply [Rolle's theorem](#thm-calc-rolle) to $f$ minus its secant line. Define …
:::
```

## Proof in the rigorous track (policy R)

```markdown
:::{proof} Rigorous proof
:label: prf-calc-squeeze
:class: dropdown
Let $\eps > 0$. Since $\lim_{x\to a} g(x) = L$, there is $\delta_1 > 0$ such that …
:::
```

## Proof sketch / deferred proof (policies S and D)

```markdown
:::{proof} Proof sketch
Bisect $[a,b]$ repeatedly, keeping the half on which $f$ changes sign. The nested intervals
shrink to a point $c$ by the [completeness axiom](#ax-calc-completeness), and continuity
forces $f(c) = 0$.
*A complete proof needs more about the real numbers; it is given in Real Analysis.*
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
Tier classes on the exercise: `tier-a` · `tier-b` · `tier-c`, plus optional `rigor`, `applied`, `widget`.

## Widget

````markdown
```{anywidget} ../../../widgets/secant-tangent.mjs
{
  "id": "wdg-calc-tangents-rates-secant",
  "f": "x^3 - x",
  "a": 1,
  "h": 0.5, "hRange": [-1, 1],
  "xRange": [-2, 2], "yRange": [-2, 3],
  "description": "Graph of y = x³ − x with a secant line through x = 1 and x = 1 + h. As h approaches 0 the secant approaches the tangent of slope 2."
}
```

**Try this:** …
````

The path is relative to the page (`../../../widgets/` from `content/<subject>/<chapter>/`).
The JSON must validate against `schema/widgets/<widget>.schema.json`; `description` is required.

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
$$ (eq-calc-linearization)

…as in [](#eq-calc-linearization).
```

## Cross-references

```markdown
Same page:      [](#thm-calc-squeeze)                → "Theorem 2"
Other page:     [the squeeze theorem](#thm-calc-squeeze)   (always name it)
Title only:     [{name}](#thm-calc-squeeze)
Whole page:     [](#calc-squeeze-theorem)
```
