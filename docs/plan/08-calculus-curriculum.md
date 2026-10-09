# 8. Calculus curriculum (first implementation)

## 8.1 Scope decisions

- **Calculus (`calc`) = single-variable calculus**, plus sequences and series and an
  introduction to ordinary differential equations. This matches a typical first-year
  sequence (e.g. US Calculus I + II, Swedish *Envariabelanalys 1–2*).
- **Multivariable calculus is a separate subject (`mvc`)** that depends on `calc` and `linalg`
  (§8.5). Keeping it separate keeps chapters manageable, lets `mvc` reuse linear algebra
  properly (Jacobians, gradients as vectors), and matches how most universities split courses.
- **Preliminaries are in `calc`** (not a separate pre-calculus subject), because they are
  written *for* calculus and kept short. Logic, sets and proof techniques will form the
  `found` subject later; until then, the rigorous track explains the bits it needs (see 12).
- **Parametric and polar curves** are a backlog extension chapter (§8.4), decided at Phase 6.
- **Order of exponential/log development**: an *early transcendentals* approach. Exponentials
  and logarithms are introduced in the preliminaries (as functions students know), their
  derivatives are derived in the derivatives chapter from one stated fact about $e$, and the
  extension page `calc-ln-integral` constructs $\ln$ rigorously as an integral and proves that
  fact, closing the loop without circularity (§8.3).

Totals: **11 chapters, 82 topic pages** (of which 5 are `level: extension`), about
45–55 hours of reading.

## 8.2 Proof policy legend

**F** full proof in core · **R** proof in the rigorous track (dropdown) · **S** sketch/idea ·
**D** deferred (to a later page or another subject; target named). Definitions are listed
with `def-` labels; results with `thm-`/`lem-`/`cor-`/`prop-` labels.

> **`content/calculus/curriculum.yml` is now the machine-readable source.** Phase 0 stage 2
> imported the list below into it with a one-off script (11 chapters, 82 topics, 5 extension,
> 194 results), and `scripts/graph.py` reads only that file. Change the curriculum there first
> (in its own PR), then this page. The list below stays as the readable commentary: each topic
> starts with a bold label line and has `Prereqs:`, `Objectives:`, `Results:` and optional
> `Widgets:` lines.

---

## Chapter 1 — Preliminaries (`preliminaries/`)

*Purpose: make the course self-contained for students from upper-secondary school. Short
pages, many exercises, few proofs.*

**`calc-real-numbers`** · Real Numbers and Intervals · `real-numbers-and-intervals.md`
- Prereqs: —
- Objectives: use interval and set-builder notation; distinguish ℕ, ℤ, ℚ, ℝ; state what "bounded above" and "supremum" mean (rigorous track).
- Results: `def-calc-interval`; `ax-calc-completeness` completeness axiom (stated, rigorous track) **S**; `thm-calc-sqrt2-irrational` **F**.

**`calc-absolute-value-inequalities`** · Absolute Value and Inequalities · `absolute-value-and-inequalities.md`
- Prereqs: `calc-real-numbers`
- Objectives: solve linear, quadratic and absolute-value inequalities; translate $\lvert x-a\rvert<\delta$ into an interval; apply the triangle inequality.
- Results: `def-calc-absolute-value`; `thm-calc-triangle-inequality` **F**; `prop-calc-abs-interval` ($\lvert x-a\rvert<\delta \iff a-\delta<x<a+\delta$) **F**.

**`calc-functions`** · Functions and Their Graphs · `functions.md`
- Prereqs: `calc-real-numbers`
- Objectives: determine the natural domain and the range; read and sketch graphs; recognise even/odd and increasing/decreasing functions; model a situation with a function.
- Results: `def-calc-function`, `def-calc-domain-range`, `def-calc-even-odd`, `def-calc-monotone`.

**`calc-function-operations`** · Combining and Transforming Functions · `combining-and-transforming-functions.md`
- Prereqs: `calc-functions`
- Objectives: form compositions and find their domains; decompose a function into a composition; predict the effect of shifts, stretches and reflections on a graph.
- Results: `def-calc-composition`; `prop-calc-graph-transformations` **F**.
- Widgets: `function-plot` (sliders for $a f(b(x-c))+d$)

**`calc-inverse-functions`** · Inverse Functions · `inverse-functions.md`
- Prereqs: `calc-function-operations`
- Objectives: test injectivity; find inverse functions and their domains; relate the graphs of $f$ and $f^{-1}$; restrict domains to obtain invertibility.
- Results: `def-calc-injective`, `def-calc-inverse-function`; `prop-calc-strictly-monotone-injective` **F**; `prop-calc-inverse-graph-reflection` **F**.

**`calc-polynomial-rational`** · Polynomial and Rational Functions · `polynomial-and-rational-functions.md`
- Prereqs: `calc-functions`
- Objectives: factor polynomials using known roots; perform polynomial division; find domains, zeros and the sign of rational functions.
- Results: `thm-calc-factor-theorem` **F**; `thm-calc-polynomial-division` **S**; `thm-calc-polynomial-roots-bound` (at most $n$ roots) **F**; `prop-calc-sign-rules` (signs of products and quotients, the zero-product rule, the sign of $x - t$; from trichotomy and the order rules) **F**; `prop-calc-rational-domain` (the domain of $p/q$ leaves out at most $\deg q$ points; the zeros are the roots of $p$ in the domain) **F**; `prop-calc-rational-sign` (a factored rational function has constant sign on an open interval free of its linear-factor points; no continuity used) **F**; `cor-calc-polynomial-identity` (two polynomials of degree at most $n$ that agree at $n + 1$ points have the same coefficients) **F**; `prop-calc-polynomial-degree-product` (degree and leading coefficient of a product: degree $m + k$, leading coefficient $ab$) **F**.

**`calc-exponential-functions`** · Exponential Functions and the Number e · `exponential-functions.md`
- Prereqs: `calc-function-operations`
- Objectives: apply the laws of exponents; graph $a^x$ for different bases; model growth and decay; describe $e$ via continuous compounding.
- Results: `def-calc-exponential-function` (rational exponents, extension to real exponents **S**, rigorous construction **D** → `calc-ln-integral`); `prop-calc-exponent-laws` (stated) **S**; `def-calc-e` (informal: $\lim_{n\to\infty}(1+1/n)^n$, made precise **D** → `calc-ln-integral`).

**`calc-logarithms`** · Logarithms · `logarithms.md`
- Prereqs: `calc-exponential-functions`, `calc-inverse-functions`
- Objectives: define $\log_b$ as the inverse of $b^x$; use the logarithm laws and change of base; solve exponential equations.
- Results: `def-calc-logarithm`, `def-calc-ln`; `thm-calc-log-laws` **F** (from exponent laws); `prop-calc-change-of-base` **F**.

**`calc-trig-functions`** · Trigonometric Functions · `trigonometric-functions.md`
- Prereqs: `calc-functions`
- Objectives: work in radians; define sin and cos on the unit circle; use the core identities; graph trigonometric functions with amplitude, period and phase.
- Results: `def-calc-radian`, `def-calc-sin-cos`, `def-calc-tan-sec-csc-cot`; `thm-calc-pythagorean-identity` **F**; `prop-calc-sin-bounded` ($-1\le\sin t\le 1$ for real $t$, from the Pythagorean identity) **F**; `prop-calc-sin-multiples-of-pi` ($\sin(k\pi)=0$ for every integer $k$) **F**; `prop-calc-sin-maxima` ($\sin(\pi/2+2k\pi)=1$ for every integer $k$) **F**, the three facts `calc-limit` takes from school; `thm-calc-addition-formulas` **R** (geometric proof); `lem-calc-sin-bounds` ($\sin\theta<\theta<\tan\theta$ for $0<\theta<\pi/2$, by comparing areas) **F**; `def-calc-period`.
- Widgets: `function-plot` (unit circle ↔ graph)

**`calc-inverse-trig`** · Inverse Trigonometric Functions · `inverse-trigonometric-functions.md`
- Prereqs: `calc-trig-functions`, `calc-inverse-functions`
- Objectives: define arcsin, arccos and arctan with their principal ranges; evaluate and simplify expressions like $\cos(\arcsin x)$; avoid the $\sin^{-1}$ ambiguity.
- Results: `def-calc-arcsin`, `def-calc-arccos`, `def-calc-arctan`; `prop-calc-arcsin-arccos-sum` **F**.

**`calc-hyperbolic-functions`** · Hyperbolic Functions *(extension)* · `hyperbolic-functions.md`
- Prereqs: `calc-exponential-functions`
- Objectives: define sinh, cosh and tanh; prove $\cosh^2-\sinh^2=1$; relate them to the hyperbola.
- Results: `def-calc-hyperbolic`; `thm-calc-hyperbolic-identity` **F**.

**`calc-complex-numbers`** · Complex Numbers *(extension)* · `complex-numbers.md`
- Prereqs: `calc-trig-functions`, `calc-polynomial-rational`
- Objectives: compute in rectangular and polar form; use $e^{i\theta}=\cos\theta+i\sin\theta$ as notation (justified by `calc-taylor-series`); solve quadratics with complex roots.
- Results: `def-calc-complex-number`, `def-calc-complex-polar`; `thm-calc-de-moivre` **F**; `def-calc-euler-formula` (definition here, consistency with series **D** → `calc-taylor-series`).

## Chapter 2 — Limits (`limits/`) ⭐ exemplar chapter

**`calc-limit`** · The Limit of a Function · `limit-of-a-function.md` · ⭐ **gold-standard page**
- Prereqs: `calc-functions`, `calc-absolute-value-inequalities`
- Objectives: estimate limits from tables and graphs and explain how this can mislead; state the precise (ε–δ) definition and interpret it as an ε–δ game; prove limits of linear and quadratic functions from the definition; recognise when a limit does not exist.
- Results: `def-calc-limit` (precise definition, in core with intuitive unpacking); `thm-calc-limit-unique` **R**; `eg-calc-limit-linear-eps-delta` **F** (worked ε–δ proof in core); `eg-calc-limit-quadratic-eps-delta` **R**; `eg-calc-limit-sin-1-over-x` (non-existence).
- Widgets: `epsilon-delta` (signature widget), `function-plot` (table of values, zoom)

**`calc-one-sided-limits`** · One-Sided Limits · `one-sided-limits.md`
- Prereqs: `calc-limit`
- Objectives: compute left and right limits, including for piecewise functions; decide existence of a limit from the one-sided limits.
- Results: `def-calc-one-sided-limit`; `thm-calc-limit-iff-one-sided` **R**; `cor-calc-one-sided-limits-differ` (different one-sided limits at $a$: the limit at $a$ does not exist) **F**.
- Widgets: `epsilon-delta` (the left and right half-windows reported separately)

**`calc-limit-laws`** · Limit Laws · `limit-laws.md`
- Prereqs: `calc-limit`
- Objectives: evaluate limits with the sum, product, quotient, power and root laws; justify direct substitution for polynomials and rational functions; identify when the laws do not apply.
- Results: `thm-calc-limit-laws` (sum **F** as the model ε/2 proof; product, quotient **R**; power, root **S**); `cor-calc-direct-substitution` **F**.

**`calc-computing-limits`** · Computing Limits Algebraically · `computing-limits.md`
- Prereqs: `calc-limit-laws`, `calc-polynomial-rational`
- Objectives: resolve 0/0 forms by factoring, rationalising and simplifying; justify each step with the "agree except at a point" lemma.
- Results: `lem-calc-limit-agree-except-point` **F**.

**`calc-squeeze-theorem`** · The Squeeze Theorem · `squeeze-theorem.md`
- Prereqs: `calc-limit-laws`, `calc-trig-functions`
- Objectives: apply the squeeze theorem, including to oscillating factors; prove $\lim_{x\to0}\frac{\sin x}{x}=1$ geometrically; use it for related trigonometric limits.
- Results: `thm-calc-squeeze` **R**; `thm-calc-sin-x-over-x` **F** (geometric, via `lem-calc-sin-bounds`; *must not* use derivatives or L'Hôpital); `cor-calc-one-minus-cos-over-x` **F**.
- Widgets: `function-plot` (squeeze band)

**`calc-infinite-limits`** · Infinite Limits and Vertical Asymptotes · `infinite-limits.md`
- Prereqs: `calc-one-sided-limits`, `calc-polynomial-rational`
- Objectives: determine infinite one-sided limits via sign analysis; locate vertical asymptotes; explain why "$=\infty$" means the limit does not exist in ℝ.
- Results: `def-calc-infinite-limit` (precise version in rigorous track); `def-calc-vertical-asymptote`; `prop-calc-reciprocal-power-limits` **F**.

**`calc-limits-at-infinity`** · Limits at Infinity and Horizontal Asymptotes · `limits-at-infinity.md`
- Prereqs: `calc-limit-laws`, `calc-infinite-limits`
- Objectives: compute limits at ±∞ of rational and root expressions; find horizontal asymptotes; compare growth informally.
- Results: `def-calc-limit-at-infinity` (precise: ε–M); `thm-calc-limit-laws-at-infinity` **S**; `prop-calc-rational-at-infinity` **F**.

## Chapter 3 — Continuity (`continuity/`)

**`calc-continuity`** · Continuity · `continuity.md`
- Prereqs: `calc-limit-laws`, `calc-one-sided-limits`
- Objectives: test continuity at a point and on an interval; classify discontinuities (removable, jump, infinite, oscillating); build continuous functions from known ones.
- Results: `def-calc-continuity`, `def-calc-continuity-interval`; `thm-calc-continuity-algebra` **F** (from the limit laws).

**`calc-continuity-elementary`** · Continuity of Elementary Functions · `continuity-of-elementary-functions.md`
- Prereqs: `calc-continuity`, `calc-squeeze-theorem`, `calc-logarithms`, `calc-inverse-trig`
- Objectives: justify continuity of polynomial, rational, root, trigonometric, exponential and logarithmic functions on their domains; evaluate limits of compositions.
- Results: `thm-calc-limit-of-composition` **R**; `thm-calc-composition-continuous` **F** (given the previous); `prop-calc-sin-cos-continuous` **F** (via squeeze); `prop-calc-exp-log-continuous` **S** (**D** → `calc-ln-integral`); `thm-calc-inverse-continuous` **S** (**D** → `ana`).

**`calc-ivt`** · The Intermediate Value Theorem · `intermediate-value-theorem.md`
- Prereqs: `calc-continuity`
- Objectives: apply the IVT to prove existence of roots and solutions; locate roots by bisection; explain why continuity is needed.
- Results: `thm-calc-ivt` **S** in core (picture), **R** full proof by bisection plus `ax-calc-completeness`; `cor-calc-root-existence` **F**.
- Widgets: `function-plot` (bisection mode)

**`calc-evt`** · The Extreme Value Theorem · `extreme-value-theorem.md`
- Prereqs: `calc-continuity`
- Objectives: state the EVT and check its hypotheses; give counterexamples when a hypothesis fails.
- Results: `thm-calc-evt` **S**, full proof **D** → `ana` (Bolzano–Weierstrass); `eg-calc-evt-hypotheses-needed` **F** (counterexamples).

## Chapter 4 — Derivatives (`derivatives/`)

**`calc-tangents-rates`** · Tangent Lines and Rates of Change · `tangent-lines-and-rates.md`
- Prereqs: `calc-limit`
- Objectives: compute slopes of secant lines and average rates; obtain tangent slopes and instantaneous velocity as limits.
- Results: `def-calc-average-rate`, `def-calc-tangent-line`.
- Widgets: `secant-tangent`

**`calc-derivative`** · The Derivative · `the-derivative.md`
- Prereqs: `calc-tangents-rates`, `calc-continuity`
- Objectives: compute derivatives from the definition; interpret $f'$ as a function and sketch it from the graph of $f$; recognise non-differentiability (corner, cusp, vertical tangent, discontinuity).
- Results: `def-calc-derivative`, `def-calc-differentiable`; `thm-calc-differentiable-implies-continuous` **F**; `eg-calc-derivative-abs-not-differentiable` **F**.
- Widgets: `zoom-to-linear`, `function-plot` (f and f′ linked)

**`calc-differentiation-rules`** · Basic Differentiation Rules · `differentiation-rules.md`
- Prereqs: `calc-derivative`
- Objectives: differentiate polynomials and rational functions with the constant, power (integer), sum, product and quotient rules; find tangent lines.
- Results: `thm-calc-power-rule-integer` **F**; `thm-calc-sum-rule` **F**; `thm-calc-product-rule` **F**; `thm-calc-quotient-rule` **F**.

**`calc-derivatives-trig`** · Derivatives of Trigonometric Functions · `derivatives-of-trigonometric-functions.md`
- Prereqs: `calc-differentiation-rules`, `calc-squeeze-theorem`
- Objectives: derive $(\sin x)'=\cos x$ from the fundamental trigonometric limits; differentiate all six trigonometric functions.
- Results: `thm-calc-derivative-sin-cos` **F**; `cor-calc-derivative-tan-etc` **F**.

**`calc-chain-rule`** · The Chain Rule · `chain-rule.md`
- Prereqs: `calc-differentiation-rules`
- Objectives: differentiate compositions in prime and Leibniz notation; recognise the composition structure of expressions.
- Results: `thm-calc-chain-rule` **F** (via the Carathéodory/"linear approximation" formulation, which avoids the $\Delta u = 0$ gap of the classic proof; a remark explains the gap).

**`calc-implicit-differentiation`** · Implicit Differentiation · `implicit-differentiation.md`
- Prereqs: `calc-chain-rule`
- Objectives: differentiate implicitly defined curves; find tangent lines to curves such as circles and the folium; explain when implicit differentiation is justified (implicit function theorem **D** → `mvc`).
- Results: `rem-calc-implicit-function-theorem` (statement **D** → `mvc`).

**`calc-inverse-function-derivatives`** · Derivatives of Inverse Functions · `derivatives-of-inverse-functions.md`
- Prereqs: `calc-chain-rule`, `calc-continuity-elementary`, `calc-derivatives-trig`
- Objectives: apply $(f^{-1})'(y)=1/f'(f^{-1}(y))$; derive the derivatives of arcsin, arccos and arctan.
- Results: `thm-calc-inverse-function-derivative` **S** in core (formula from the chain rule *assuming* differentiability), **R** full proof; `cor-calc-derivative-inverse-trig` **F**.

**`calc-derivatives-exp-log`** · Derivatives of Exponential and Logarithmic Functions · `derivatives-of-exponential-and-logarithmic-functions.md`
- Prereqs: `calc-inverse-function-derivatives`
- Objectives: differentiate $e^x$, $a^x$, $\ln x$, $\log_b x$ and $x^r$ for real $r$; use logarithmic differentiation.
- Results: `lem-calc-exp-limit` ($\lim_{h\to0}\frac{e^h-1}{h}=1$; stated as a fact characterising $e$, **D** → `calc-ln-integral`); `thm-calc-derivative-exp` **F** (given the lemma); `thm-calc-derivative-ln` **F**; `thm-calc-general-power-rule` **F**.

**`calc-higher-derivatives`** · Higher Derivatives · `higher-derivatives.md`
- Prereqs: `calc-derivatives-trig`
- Objectives: compute second and $n$-th derivatives; interpret acceleration; find patterns (e.g. $(\sin x)^{(n)}$).
- Results: `def-calc-higher-derivative`; `prop-calc-leibniz-product-rule` **R** (by induction).

**`calc-related-rates`** · Related Rates · `related-rates.md`
- Prereqs: `calc-implicit-differentiation`, `calc-derivatives-trig`
- Objectives: model a related-rates problem; differentiate the relation with respect to time; interpret the result with units.
- Results: none (method page); ≥ 5 worked examples.

## Chapter 5 — Applications of Derivatives (`derivative-applications/`)

**`calc-extreme-values`** · Extreme Values and Critical Points · `extreme-values.md`
- Prereqs: `calc-differentiation-rules`, `calc-evt`
- Objectives: distinguish local and global extrema; find critical points; apply the closed interval method.
- Results: `def-calc-local-extremum`, `def-calc-critical-point`; `thm-calc-fermat` **F**.

**`calc-mean-value-theorem`** · Rolle's Theorem and the Mean Value Theorem · `mean-value-theorem.md`
- Prereqs: `calc-extreme-values`
- Objectives: state and apply Rolle's theorem and the MVT; use the MVT to prove inequalities and uniqueness of roots.
- Results: `thm-calc-rolle` **F**; `thm-calc-mvt` **F**; `cor-calc-zero-derivative-constant` **F**; `cor-calc-same-derivative` **F**.
- Widgets: `secant-tangent` (MVT mode)

**`calc-monotonicity`** · Monotonicity and the First Derivative Test · `monotonicity.md`
- Prereqs: `calc-mean-value-theorem`
- Objectives: determine intervals of increase and decrease from the sign of $f'$; classify critical points with the first derivative test.
- Results: `thm-calc-monotonicity-test` **F** (from the MVT); `thm-calc-first-derivative-test` **F**.

**`calc-concavity`** · Concavity and the Second Derivative Test · `concavity.md`
- Prereqs: `calc-monotonicity`, `calc-higher-derivatives`
- Objectives: determine concavity and inflection points; apply the second derivative test and know when it is inconclusive.
- Results: `def-calc-concave` (via increasing $f'$); `thm-calc-concavity-test` **F**; `thm-calc-second-derivative-test` **F**.

**`calc-curve-sketching`** · Curve Sketching · `curve-sketching.md`
- Prereqs: `calc-concavity`, `calc-limits-at-infinity`
- Objectives: produce a complete sketch (domain, symmetry, intercepts, asymptotes including oblique, monotonicity, extrema, concavity); check it against a plot.
- Results: `def-calc-oblique-asymptote`; method page.
- Widgets: `function-plot` (reveal features step by step)

**`calc-optimisation`** · Optimisation Problems · `optimisation.md`
- Prereqs: `calc-monotonicity`
- Objectives: translate a word problem into an objective function with constraints; justify that a critical point is a global optimum.
- Results: `prop-calc-single-critical-point` (a unique local extremum on an interval is global) **F**.

**`calc-lhopital`** · Indeterminate Forms and L'Hôpital's Rule · `lhopital.md`
- Prereqs: `calc-mean-value-theorem`, `calc-derivatives-exp-log`, `calc-limits-at-infinity`
- Objectives: identify indeterminate forms; apply L'Hôpital's rule correctly (checking hypotheses); convert $0\cdot\infty$, $\infty-\infty$, $1^\infty$, $0^0$, $\infty^0$.
- Results: `thm-calc-cauchy-mvt` **R**; `thm-calc-lhopital` (0/0, finite $a$) **R**; `thm-calc-lhopital-general` (the ∞/∞ and $a=\pm\infty$ versions) **S**; `rem-calc-lhopital-misuse` (examples where it fails or is circular).

**`calc-linearisation`** · Linear Approximation and Differentials · `linear-approximation.md`
- Prereqs: `calc-differentiation-rules`
- Objectives: build the linearisation; estimate values and errors; use differentials for error propagation.
- Results: `def-calc-linearisation`, `def-calc-differential`; `prop-calc-linearisation-error-little-o` **F**.
- Widgets: `zoom-to-linear`

**`calc-newtons-method`** · Newton's Method · `newtons-method.md`
- Prereqs: `calc-linearisation`, `calc-ivt`
- Objectives: derive and run Newton's iteration; recognise failure modes (bad start, cycles, $f'=0$).
- Results: `thm-calc-newton-convergence` (quadratic convergence near a simple root) **S**, **D** → beyond scope (numerical analysis).
- Widgets: `newton-method`

**`calc-taylor-polynomials`** · Taylor Polynomials and Taylor's Theorem · `taylor-polynomials.md`
- Prereqs: `calc-linearisation`, `calc-mean-value-theorem`, `calc-higher-derivatives`
- Objectives: compute Taylor polynomials; bound the error with the Lagrange remainder; use Taylor polynomials for approximation and limits.
- Results: `def-calc-taylor-polynomial`; `thm-calc-taylor-lagrange` **R** (repeated Rolle / Cauchy MVT); `cor-calc-taylor-error-bound` **F**; `prop-calc-ordo-arithmetic` (big-O rules) **F**.
- Widgets: `taylor`

## Chapter 6 — Integrals (`integrals/`)

**`calc-antiderivatives`** · Antiderivatives · `antiderivatives.md`
- Prereqs: `calc-mean-value-theorem`, `calc-derivatives-exp-log`
- Objectives: find antiderivatives from a table of basic forms; explain the $+C$ (on an interval) using the MVT; solve simple initial value problems.
- Results: `def-calc-antiderivative`; `thm-calc-antiderivatives-differ-by-constant` **F** (from `cor-calc-same-derivative`).

**`calc-sigma-notation`** · Sums and Sigma Notation · `sigma-notation.md`
- Prereqs: `calc-real-numbers`
- Objectives: read and manipulate sigma notation; use the formulas for $\sum k$, $\sum k^2$, $\sum k^3$; recognise telescoping sums.
- Results: `thm-calc-power-sums` **F** (by induction, with a short induction primer); `prop-calc-telescoping-sum` **F**.

**`calc-area-riemann-sums`** · Area and Riemann Sums · `area-and-riemann-sums.md`
- Prereqs: `calc-sigma-notation`, `calc-limits-at-infinity`
- Objectives: approximate areas with left, right and midpoint sums; compute exact areas as limits for polynomials.
- Results: `def-calc-riemann-sum`.
- Widgets: `riemann-sum`

**`calc-definite-integral`** · The Definite Integral · `definite-integral.md`
- Prereqs: `calc-area-riemann-sums`, `calc-continuity`
- Objectives: define the integral as a limit of Riemann sums; interpret it as signed area; apply linearity, additivity and comparison properties.
- Results: `def-calc-definite-integral` (upper/lower Darboux sums in the rigorous track); `thm-calc-continuous-integrable` **S**, **D** → `ana`; `thm-calc-integral-properties` **S** (linearity, additivity, comparison; **R** for comparison).

**`calc-ftc`** · The Fundamental Theorem of Calculus · `fundamental-theorem.md`
- Prereqs: `calc-definite-integral`, `calc-antiderivatives`
- Objectives: differentiate accumulation functions $\int_a^x f$; evaluate definite integrals with antiderivatives; explain why differentiation and integration are inverse processes.
- Results: `thm-calc-mvt-integrals` **F**; `thm-calc-ftc-1` **F**; `thm-calc-ftc-2` **F**.
- Widgets: `area-accumulation`

**`calc-substitution`** · Integration by Substitution · `substitution.md`
- Prereqs: `calc-ftc`
- Objectives: choose a substitution; change limits in definite integrals; recognise symmetry ($\int_{-a}^a$ of odd/even functions).
- Results: `thm-calc-substitution-rule` **F** (indefinite and definite); `prop-calc-odd-even-integrals` **F**.

**`calc-ln-integral`** · The Logarithm Defined as an Integral *(extension)* · `logarithm-as-integral.md`
- Prereqs: `calc-ftc`, `calc-ivt`
- Objectives: define $\ln x=\int_1^x \frac{dt}{t}$ and derive all log laws; define $\exp$ as its inverse and $e=\exp(1)$; prove `lem-calc-exp-limit` and the compound-interest limit, closing the loop from chapters 1 and 4.
- Results: `def-calc-ln-integral`; `thm-calc-ln-integral-properties` **F**; `thm-calc-exp-as-inverse` **R**; `thm-calc-e-compound-interest` **F**; `thm-calc-definitions-agree` **F**.

## Chapter 7 — Integration Techniques (`integration-techniques/`)

**`calc-integration-by-parts`** · Integration by Parts · `integration-by-parts.md`
- Prereqs: `calc-substitution`
- Objectives: apply integration by parts (including repeated application and the "solve for the integral" trick); choose $u$ and $\mathrm{d}v$ well.
- Results: `thm-calc-integration-by-parts` **F** (indefinite and definite).

**`calc-trig-integrals`** · Trigonometric Integrals · `trigonometric-integrals.md`
- Prereqs: `calc-substitution`
- Objectives: integrate products of powers of sin/cos and tan/sec; use power-reduction identities.
- Results: method page; `prop-calc-power-reduction` **F**.

**`calc-trig-substitution`** · Trigonometric Substitution · `trigonometric-substitution.md`
- Prereqs: `calc-trig-integrals`
- Objectives: use $x=a\sin\theta$, $a\tan\theta$, $a\sec\theta$ for $\sqrt{a^2-x^2}$ and similar; convert back to $x$ with a reference triangle.
- Results: method page.

**`calc-partial-fractions`** · Partial Fractions · `partial-fractions.md`
- Prereqs: `calc-substitution`
- Objectives: decompose rational functions (distinct, repeated, irreducible quadratic factors); integrate them.
- Results: `thm-calc-partial-fraction-decomposition` (existence) **S**, **D** → `linalg` (algebra).

**`calc-integration-strategy`** · Strategy for Integration · `integration-strategy.md`
- Prereqs: `calc-integration-by-parts`, `calc-trig-substitution`, `calc-partial-fractions`
- Objectives: choose a method for an unfamiliar integral; use tables and CAS responsibly; recognise that some integrals (e.g. $\int e^{-x^2}\mathrm{d}x$) are not elementary.
- Results: `rem-calc-nonelementary-integrals` (statement, Liouville **D** → beyond scope).

**`calc-numerical-integration`** · Numerical Integration · `numerical-integration.md`
- Prereqs: `calc-definite-integral`, `calc-taylor-polynomials`
- Objectives: apply the midpoint, trapezoid and Simpson rules; use error bounds to choose $n$.
- Results: `thm-calc-trapezoid-error` **R**; `thm-calc-simpson-error` **S**.
- Widgets: `riemann-sum` (trapezoid/Simpson modes)

## Chapter 8 — Applications of Integrals (`integral-applications/`)

**`calc-area-between-curves`** · Area Between Curves · `area-between-curves.md`
- Prereqs: `calc-substitution`
- Objectives: set up area integrals with respect to $x$ or $y$; find intersection points; split at crossings.
- Results: method page.

**`calc-volumes-slicing`** · Volumes by Slicing · `volumes-by-slicing.md`
- Prereqs: `calc-area-between-curves`
- Objectives: compute volumes from cross-sectional areas; use disks and washers for solids of revolution.
- Results: `def-calc-volume-by-slicing` (justified by Riemann sums).
- Widgets: `solid-of-revolution`

**`calc-volumes-shells`** · Volumes by Cylindrical Shells · `volumes-by-shells.md`
- Prereqs: `calc-volumes-slicing`, `calc-integration-by-parts`
- Objectives: set up shell integrals; choose between washers and shells.
- Results: method page; `rem-calc-shells-washers-agree` **S**.

**`calc-arc-length`** · Arc Length and Surface Area · `arc-length.md`
- Prereqs: `calc-substitution`
- Objectives: derive and apply the arc-length formula (via the MVT on polygonal approximations); compute areas of surfaces of revolution.
- Results: `def-calc-arc-length` (derivation **F**); `def-calc-surface-area` (derivation **S**).

**`calc-average-value`** · Average Value of a Function · `average-value.md`
- Prereqs: `calc-ftc`
- Objectives: compute averages of functions; interpret the MVT for integrals.
- Results: `def-calc-average-value`; uses `thm-calc-mvt-integrals`.

**`calc-physics-applications`** · Work, Mass and Centre of Mass · `work-mass-centre-of-mass.md`
- Prereqs: `calc-area-between-curves`
- Objectives: set up integrals for work (springs, pumping), mass from density, and centroids of plane regions; keep track of units.
- Results: method page.

## Chapter 9 — Improper Integrals (`improper-integrals/`)

**`calc-improper-integrals`** · Improper Integrals · `improper-integrals.md`
- Prereqs: `calc-ftc`, `calc-lhopital`
- Objectives: evaluate type I (infinite interval) and type II (unbounded integrand) integrals; decide convergence of $p$-integrals.
- Results: `def-calc-improper-integral`; `thm-calc-p-integrals` **F**.

**`calc-improper-comparison`** · Comparison Tests for Improper Integrals · `comparison-tests-for-integrals.md`
- Prereqs: `calc-improper-integrals`
- Objectives: decide convergence without evaluating, using direct and limit comparison; choose a comparison function from the dominant behaviour of the integrand.
- Results: `thm-calc-improper-comparison` **R** (needs monotone bounded ⇒ convergent, from `ax-calc-completeness`); `thm-calc-improper-limit-comparison` **F** (given comparison); `thm-calc-absolute-convergence-integrals` **F**.

**`calc-probability-densities`** · Probability Density Functions *(extension)* · `probability-densities.md`
- Prereqs: `calc-improper-integrals`, `calc-integration-by-parts`
- Objectives: check that a density is valid; compute probabilities, means and variances of exponential and normal-type densities.
- Results: `def-calc-pdf`; `prop-calc-gaussian-integral` (value stated, proof **D** → `mvc`).

## Chapter 10 — Sequences and Series (`sequences-series/`)

**`calc-sequences`** · Sequences · `sequences.md`
- Prereqs: `calc-lhopital`
- Objectives: compute limits of sequences; use the function-limit connection and the squeeze theorem; prove simple limits from the definition (rigorous track).
- Results: `def-calc-sequence-limit` (precise: ε–N); `thm-calc-sequence-limit-laws` **S**; `thm-calc-sequence-from-function` **F**; `thm-calc-sequence-squeeze` **F**.

**`calc-monotone-sequences`** · Monotone and Bounded Sequences · `monotone-sequences.md`
- Prereqs: `calc-sequences`
- Objectives: prove monotonicity and boundedness; apply the monotone convergence theorem, including to recursive sequences.
- Results: `thm-calc-convergent-bounded` **F**; `thm-calc-monotone-convergence` **R** (from `ax-calc-completeness`).

**`calc-series`** · Infinite Series · `series.md`
- Prereqs: `calc-sequences`, `calc-sigma-notation`
- Objectives: define convergence via partial sums; sum geometric and telescoping series; apply the divergence test.
- Results: `def-calc-series-convergence`; `thm-calc-geometric-series` **F**; `thm-calc-divergence-test` **F**; `prop-calc-series-linearity` **F**.
- Widgets: `partial-sums`

**`calc-integral-test`** · The Integral Test and p-Series · `integral-test.md`
- Prereqs: `calc-series`, `calc-monotone-sequences`, `calc-improper-integrals`
- Objectives: apply the integral test; state the $p$-series result; estimate remainders.
- Results: `thm-calc-integral-test` **F**; `cor-calc-p-series` **F**; `thm-calc-integral-test-remainder` **F**.

**`calc-comparison-tests`** · Comparison Tests for Series · `comparison-tests.md`
- Prereqs: `calc-integral-test`
- Objectives: choose a comparison series; apply direct and limit comparison.
- Results: `thm-calc-series-comparison` **F** (via monotone convergence of partial sums); `thm-calc-series-limit-comparison` **F**.

**`calc-alternating-series`** · Alternating Series · `alternating-series.md`
- Prereqs: `calc-series`, `calc-monotone-sequences`
- Objectives: apply the alternating series test; bound the error of a partial sum.
- Results: `thm-calc-alternating-series-test` **F**; `thm-calc-alternating-error-bound` **F**.

**`calc-absolute-convergence`** · Absolute Convergence, Ratio and Root Tests · `absolute-convergence.md`
- Prereqs: `calc-comparison-tests`, `calc-alternating-series`
- Objectives: distinguish absolute and conditional convergence; apply the ratio and root tests; choose a test strategically.
- Results: `thm-calc-absolute-implies-convergence` **F**; `thm-calc-ratio-test` **F**; `thm-calc-root-test` **R**; `rem-calc-riemann-rearrangement` **S**, **D** → `ana`.

**`calc-power-series`** · Power Series · `power-series.md`
- Prereqs: `calc-absolute-convergence`
- Objectives: find the radius of convergence with the ratio or root test; determine the interval of convergence, checking each endpoint separately.
- Results: `def-calc-power-series`; `thm-calc-radius-of-convergence` **R**.

**`calc-power-series-calculus`** · Calculus with Power Series · `calculus-with-power-series.md`
- Prereqs: `calc-power-series`
- Objectives: differentiate and integrate power series term by term; build series for $\frac{1}{1-x}$, $\ln(1+x)$ and $\arctan x$.
- Results: `thm-calc-term-by-term` (stated) **S**, **D** → `ana` (uniform convergence).

**`calc-taylor-series`** · Taylor and Maclaurin Series · `taylor-series.md`
- Prereqs: `calc-power-series-calculus`, `calc-taylor-polynomials`, `calc-complex-numbers`
- Objectives: compute Taylor series; prove convergence to the function via the remainder for $e^x$, $\sin x$ and $\cos x$; state the standard series; explain why not every smooth function equals its Taylor series.
- Results: `thm-calc-taylor-series-convergence` **F** (for $e^x$, $\sin$, $\cos$); `eg-calc-taylor-series-smooth-not-analytic` ($e^{-1/x^2}$) **R**; `thm-calc-euler-formula-series` **F** (closes `def-calc-euler-formula`).
- Widgets: `taylor` (series mode)

**`calc-taylor-applications`** · Applications of Taylor Series *(extension)* · `taylor-series-applications.md`
- Prereqs: `calc-taylor-series`
- Objectives: use series to evaluate limits and integrals and to approximate with a guaranteed error; use the binomial series.
- Results: `thm-calc-binomial-series` **S**.

## Chapter 11 — Introduction to Differential Equations (`differential-equations/`)

*The `ode` subject will extend this chapter later. These pages remain the introduction that
`ode` lists as prerequisites.*

**`calc-ode-intro`** · Differential Equations and Slope Fields · `differential-equations-intro.md`
- Prereqs: `calc-antiderivatives`
- Objectives: verify solutions; read slope fields; distinguish general and particular solutions; explain what an existence-uniqueness theorem guarantees.
- Results: `def-calc-ode`, `def-calc-ivp`; `thm-calc-picard-lindelof` (stated) **D** → `ode`.
- Widgets: `slope-field`

**`calc-separable-equations`** · Separable Equations · `separable-equations.md`
- Prereqs: `calc-ode-intro`, `calc-partial-fractions`
- Objectives: solve separable equations, including lost constant solutions; handle the absolute value from $\ln\lvert y\rvert$ correctly.
- Results: `thm-calc-separation-of-variables` **F** (justified via the chain rule, not "multiplying by $\mathrm{d}x$").

**`calc-first-order-linear`** · First-Order Linear Equations · `first-order-linear-equations.md`
- Prereqs: `calc-ode-intro`, `calc-integration-by-parts`
- Objectives: solve $y'+p(x)y=q(x)$ with an integrating factor; solve IVPs.
- Results: `thm-calc-integrating-factor` **F** (including that all solutions have this form).

**`calc-ode-models`** · Modelling with First-Order Equations · `modelling-with-differential-equations.md`
- Prereqs: `calc-separable-equations`, `calc-first-order-linear`
- Objectives: build and solve models of growth/decay, Newton cooling, mixing and logistic growth; interpret equilibria.
- Results: `prop-calc-logistic-solution` **F**.

**`calc-eulers-method`** · Euler's Method · `eulers-method.md`
- Prereqs: `calc-ode-intro`, `calc-linearisation`
- Objectives: run Euler's method by hand and in code; observe first-order error behaviour.
- Results: `thm-calc-euler-error-order` **S**, **D** → `ode`.
- Widgets: `slope-field` (Euler overlay)

**`calc-second-order-linear`** · Second-Order Linear Equations with Constant Coefficients · `second-order-linear-equations.md`
- Prereqs: `calc-first-order-linear`, `calc-complex-numbers`
- Objectives: solve $ay''+by'+cy=0$ in the three root cases; find particular solutions with undetermined coefficients for polynomial, exponential and trigonometric right-hand sides; model oscillators.
- Results: `thm-calc-superposition` **F**; `thm-calc-characteristic-equation-solutions` **F** (these are solutions) + all solutions **D** → `ode`.

## 8.3 Circularity map (how the foundations hang together)

```
completeness axiom (ax-calc-completeness, stated)
   ├── IVT (R), monotone convergence (R), improper comparison (R)
   └── EVT, continuity ⇒ integrable, inverse continuity   ── deferred to `ana`
EVT ── Fermat ── Rolle ── MVT ── monotonicity, ± const antiderivatives, L'Hôpital, Taylor
sin θ < θ < tan θ (area argument) ── sin x/x → 1 ── (sin)' = cos
"(e^h − 1)/h → 1" (fact) ── (e^x)' = e^x ── (ln x)' = 1/x  …  all proven independently in calc-ln-integral
FTC ── substitution, parts ── all of ch. 7–9
```
Every arrow goes forward in the prerequisite graph except the deliberate "fact now, proof
later" items, which are listed in the table below so reviewers can check them.

The Integrals pages can't prove the unit-circle facts of `calc-trig-functions` (the last row):
arc length and sector area as integrals need the derivative of $\sin$, which rests on
$\sin\theta < \theta < \tan\theta$ and so on these very facts, which would be circular.

| Stated early | Where | Proved in |
|---|---|---|
| Real exponents $a^x$ well-defined and continuous | `calc-exponential-functions`, `calc-continuity-elementary` | `calc-ln-integral` |
| $\lim_{h\to0}(e^h-1)/h=1$ | `calc-derivatives-exp-log` | `calc-ln-integral` |
| $e=\lim(1+1/n)^n$ | `calc-exponential-functions` | `calc-ln-integral` |
| $e^{i\theta}=\cos\theta+i\sin\theta$ | `calc-complex-numbers` (definition) | `calc-taylor-series` (consistency) |
| EVT, continuous ⇒ integrable, inverse continuity, term-by-term differentiation | various | `ana` (future subject) |
| Geometry of the unit circle: the journey along the circle defines arc length; a rotation taking $A$ to $P(\alpha)$ exists; the region between two radii is convex when its arc is shorter than half the circle ($\theta < \pi$); the sector of angle $\theta$ has area $\theta/2$ (so the disc has area $\pi$: Archimedes' theorem) | `calc-trig-functions` | `ana` (future subject) |

## 8.4 Backlog (not in Calculus 1.0 unless decided at Phase 6)
- **Parametric and polar curves** (chapter `parametric-polar/`): parametric curves and
  derivatives, arc length, polar coordinates and area. Default: add as an extension chapter in
  Phase 6 if time allows, otherwise move it to `mvc`.
- Hyperbolic substitution, Wallis/Stirling products, Fourier-series teaser (→ `ode`).

## 8.5 Outline of `mvc` (separate subject, for orientation only)

`mvc` depends on `calc` and `linalg`. Chapters: vectors and geometry of space (uses
`linalg`), vector-valued functions, partial derivatives (limits, continuity,
differentiability, chain rule, gradient, implicit function theorem), optimisation (critical
points, Hessian via `linalg`, Lagrange multipliers), multiple integrals (double/triple,
change of variables with the Jacobian determinant from `linalg`), vector calculus (line and
surface integrals, Green, Stokes, divergence). Detailed curriculum: a Phase 8+ deliverable.

## 8.6 Suggested reading paths (shown on the subject page)

| Path | Chapters | Notes |
|---|---|---|
| Engineering Calculus I | 1–6 | skip the rigorous track; the tier C `rigor` exercises are optional |
| Engineering Calculus II | 7–11 | |
| Mathematics major, single-variable | all, including the rigorous track and extension pages | pair with `ana` when it exists |
| Quick review for multivariable | 2, 4, 5 (MVT, Taylor), 6, 10 (Taylor series) | |
