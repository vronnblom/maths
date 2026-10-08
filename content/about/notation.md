---
title: Notation
label: site-notation
description: >-
  The symbols and conventions used on every page of the site, and the house style for
  writing mathematics here.
maths:
  kind: meta
  status: draft
---

Notation is the same across the whole site: every subject uses the same symbol for the same
thing. Where conventions differ between countries, the alternative is mentioned once on this
page and never mixed into the content.

## Shorthand used throughout

These commands are defined once for the whole site. If you write for the site, use them
wherever they apply, so that the notation stays consistent.

| Meaning | Typed as | Renders as |
|---|---|---|
| real numbers | `\R` | $\R$ |
| natural numbers $\{0, 1, 2, \dots\}$ | `\N` | $\N$ |
| integers | `\Z` | $\Z$ |
| rational numbers | `\Q` | $\Q$ |
| complex numbers | `\C` | $\C$ |
| the differential in an integral | `\int_0^1 x^2 \dd x` | $\int_0^1 x^2 \dd x$ |
| a derivative in Leibniz notation | `\dv{y}{x}` | $\dv{y}{x}$ |
| a higher derivative | `\dvn{2}{y}{x}` | $\dvn{2}{y}{x}$ |
| a partial derivative (multivariable subjects) | `\pdv{f}{x}` | $\pdv{f}{x}$ |
| absolute value | `\abs{x - a}` | $\abs{x - a}$ |
| norm of a vector | `\norm{\vb{v}}` | $\norm{\vb{v}}$ |
| a vector | `\vb{v}` | $\vb{v}$ |
| epsilon (as in ε–δ) | `\eps` | $\eps$ |
| sign function | `\sgn x` | $\sgn x$ |
| inverse hyperbolic sine | `\arsinh x` | $\arsinh x$ |
| domain and range of a function | `\dom f`, `\ran f` | $\dom f$, $\ran f$ |

The same commands in displayed formulas, where their sizes adapt to what they contain:

$$
\dv{}{x}\bigl(x^3\bigr) = 3x^2,
\qquad
\dvn{2}{}{x}\bigl(\sin x\bigr) = -\sin x,
\qquad
\pdv{}{x}\bigl(x^2 y\bigr) = 2xy,
$$

$$
\abs{\frac{x^2 - 4}{x - 2} - 4} = \abs{x - 2} < \eps
\quad\text{whenever}\quad
0 < \abs{x - 2} < \eps,
\qquad
\norm{\vb{u} + \vb{v}} \le \norm{\vb{u}} + \norm{\vb{v}},
$$

$$
\int_1^{e} \frac{1}{x} \dd x = 1,
\qquad
\sgn x = \frac{x}{\abs{x}} \text{ for } x \ne 0,
\qquad
\arsinh x = \ln\Bigl(x + \sqrt{x^2 + 1}\Bigr),
$$

$$
\N \subset \Z \subset \Q \subset \R \subset \C,
\qquad
f\colon \dom f \to \R,
\qquad
\ran f = \{f(x) : x \in \dom f\}.
$$

## Notation table

% notation-lint: off (the "We do not write" column shows what the lint rejects)

| Topic | We write | We do **not** write | Notes |
|---|---|---|---|
| Natural numbers | $\N = \{0, 1, 2, \dots\}$; positive integers $\Z_{>0}$ or "$n \ge 1$" | $\N$ meaning $\{1, 2, \dots\}$ | This follows ISO 80000-2. In statements we prefer an explicit range ("for $n \ge 1$"). |
| Intervals | $[a, b]$, $(a, b)$, $[a, b)$, $(a, \infty)$ | $]a, b[$, $]a, b]$ | See the note on other countries below. |
| Natural logarithm | $\ln x$ | $\log x$ for the natural logarithm | |
| Other logarithms | $\log_{10} x$, $\log_2 x$, $\log_b x$ | a bare $\log x$ | The base is always written. |
| Exponential | $e^{x}$, or $\exp(x)$ for large exponents | $\mathrm{e}^x$ | An italic $e$, as in the major calculus textbooks. |
| Inverse trigonometric functions | $\arcsin x$, $\arccos x$, $\arctan x$ | $\sin^{-1} x$ | The page on inverse trigonometric functions mentions $\sin^{-1} x$ as an alternative and explains why it can be confused with $1/\sin x$. |
| Powers of trigonometric functions | $\sin^2 x = (\sin x)^2$ | $\sin x^2$ when $(\sin x)^2$ is meant | |
| Reciprocal trigonometric functions | $\sec x$, $\csc x$, $\cot x$ | | Defined once, in the preliminaries. |
| Angles | radians | degrees in calculus statements | |
| Derivatives | $f'(x)$, $\dv{y}{x}$, $\dv{}{x}\bigl(f(x)\bigr)$; higher derivatives $f''$, $f^{(n)}$ | $\dot y$ | $\dot y$ is reserved for time derivatives and is introduced in the chapter on differential equations. Leibniz notation is used for the chain rule and related rates, prime notation for rules about functions. |
| Differentials | $\dd x$ in integrals | an italic $dx$ | A thin space and an upright d. |
| Integrals | $\int_a^b f(x) \dd x$; an antiderivative $\int f(x) \dd x = F(x) + C$ | leaving out $+ C$ | Each page says once that $C \in \R$ is an arbitrary constant. |
| Limits | $\lim_{x \to a} f(x)$; one-sided $x \to a^{+}$, $x \to a^{-}$; $\lim_{n \to \infty} a_n$ | $\lim_{x \to a+}$ | |
| Infinite limits | "$\lim_{x \to a} f(x) = \infty$", with the remark that the limit *does not exist* as a real number | | |
| Functions | $f\colon A \to B$, $x \mapsto x^2$; "the function $f$" and "the value $f(x)$" | "the function $f(x)$" in definitions | Allowed informally in examples. |
| Composition and inverse | $f \circ g$; $f^{-1}$ for the inverse function; $1/f$ or $f(x)^{-1}$ for the reciprocal | | |
| Monotone functions | increasing: $x_1 < x_2$ implies $f(x_1) \le f(x_2)$; strictly increasing: $x_1 < x_2$ implies $f(x_1) < f(x_2)$; likewise decreasing ($\ge$) and strictly decreasing ($>$) | "non-decreasing" for increasing, or "increasing" when strictly increasing is meant | "Increasing" allows the function to stay level; a result that needs $<$ says "strictly". Defined in [Functions and Their Graphs](#def-calc-monotone). |
| Definitions | $:=$ when defining in a display; "is called" in prose | $\equiv$ | |
| Approximation | $\approx$, with the precision stated ("to 4 decimal places") | | |
| Sequences | $(a_n)_{n \ge 1}$ or $(a_n)$; terms $a_n$ | $\{a_n\}$ | Set braces would suggest a set, which forgets order and repetition. |
| Series | $\sum_{k=1}^{\infty} a_k$; partial sums $s_n = \sum_{k=1}^{n} a_k$ | | The summation index is $k$, the sequence index $n$. |
| Vectors (later subjects) | $\vb{v}$ (bold upright), components $(v_1, \dots, v_n)$; column vectors in linear algebra | $\vec{v}$ | Fixed now so that linear algebra and multivariable calculus agree. |
| Absolute value and norm | $\abs{x}$, $\norm{\vb{v}}$ | plain vertical bars around tall expressions in displays | Plain bars do not grow with their contents; they are fine inline. |
| Logic | "if and only if" and "implies" in prose; $\implies$, $\iff$ in displays | "iff" | |
| Quantifiers | words in the core text ("for every $\eps > 0$ there exists $\delta > 0$"); the symbols $\forall$, $\exists$ only in the rigorous track | | |
| Decimal mark | a point: $3.14$ | a comma | |
| Set-builder notation | $\{x \in \R : x > 0\}$ | $\{x \mid x > 0\}$ | |

% notation-lint: on

### Intervals in other countries

% notation-lint: off (this paragraph names the reversed-bracket convention)

In some countries, for example France and Sweden, an open interval is written with reversed
brackets: $]a, b[$ for what we write as $(a, b)$, and $]a, b]$ for $(a, b]$. This site always
uses round brackets, which can be confused with an ordered pair $(a, b)$; the context makes
clear which is meant.

% notation-lint: on

## For contributors

### Answers to exercises

Exercise answers are checked automatically against the computer algebra system, so the final
answer of an exercise is written in this subset of LaTeX:

- numbers, `\frac{}{}`, `\sqrt{}`, `\sqrt[n]{}`, powers `^{}`, `\pi`, `e`, `\infty`, `-\infty`;
- `\sin`, `\cos`, `\tan`, `\arcsin`, `\arccos`, `\arctan`, `\ln`, `\log_{b}`, and `\abs{}`;
- `+C` for an antiderivative (the checker differentiates the answer instead of comparing it);
- several answers as a comma-separated list; intervals as `(a, b)` or `[a, b]` when the
  exercise asks for a set (otherwise `(a, b)` is a point);
- not `\mathrm{e}` and not `\dfrac`.

Answers that are not expressions (proofs, sketches, "does not exist") are marked as manual
and are checked by a person.

### Writing style

- **Spelling**: British English (*normalise*, *behaviour*), one spelling throughout.
- **Voice**: "we" for reasoning that we do together ("we now show"), "you" for instructions
  ("try dragging $\eps$"). Present tense.
- **Sentences**: short, with one idea per sentence in definitions and statements of results.
- **Emphasis**: **bold** only for a term being defined; *italics* for emphasis, sparingly.
- **Headings**: sentence case ("Common mistakes"); page titles in title case.
- **Displayed formulas** are punctuated as part of the sentence.
- **No forward references in proofs.** A "looking ahead" note may mention later topics.
- **No "clearly" or "obviously".** If a step is easy, a short reason costs nothing.
- **Units**: applied examples state their units, and the final answer has units.
- **Accessibility**: every figure has a text alternative, and every interactive figure has a
  caption describing what it shows. Colour is never the only carrier of meaning.
- **Translation**: no wordplay or idioms in the core text, and no text inside images.
