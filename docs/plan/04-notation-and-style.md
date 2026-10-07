# 4. Notation, conventions and writing style

This document becomes the published page `content/about/notation.md` in Phase 0. Notation is
**site-wide**: every subject uses the same symbols for the same things. Where conventions
differ internationally (e.g. Swedish/French interval brackets), the alternative is mentioned
once on the notation page, never mixed into content.

## 4.1 KaTeX macros (defined once in `content/myst.yml`)

Macros make notation consistent and globally changeable. Authors **must** use them where
one exists.

```yaml
project:
  math:
    '\R': '\mathbb{R}'
    '\N': '\mathbb{N}'
    '\Z': '\mathbb{Z}'
    '\Q': '\mathbb{Q}'
    '\C': '\mathbb{C}'
    '\dd': '\,\mathrm{d}'              # integrals:  \int_0^1 x^2 \dd x
    '\dv': '\frac{\mathrm{d} #1}{\mathrm{d} #2}'   # \dv{y}{x}   → dy/dx
    '\dvn': '\frac{\mathrm{d}^{#1} #2}{\mathrm{d} #3^{#1}}'  # \dvn{2}{y}{x}
    '\pdv': '\frac{\partial #1}{\partial #2}'      # (multivariable, reserved now)
    '\abs': '\left\lvert #1 \right\rvert'
    '\norm': '\left\lVert #1 \right\rVert'
    '\vb': '\mathbf{#1}'               # vectors: \vb{v}
    '\eps': '\varepsilon'
    '\sgn': '\operatorname{sgn}'
    '\arsinh': '\operatorname{arsinh}'
    '\dom': '\operatorname{dom}'
    '\ran': '\operatorname{ran}'
```

> Macros with arguments (`#1`) are supported by KaTeX. Before Phase 1 closes, every macro is
> exercised on `content/about/notation.md` itself, which serves as the render test.

## 4.2 Notation table

| Topic | We write | We do **not** write | Notes |
|---|---|---|---|
| Natural numbers | $\N = \{0, 1, 2, \dots\}$, positive integers $\Z_{>0}$ or "$n \ge 1$" | $\N$ meaning $\{1,2,\dots\}$ | ISO 80000-2 and Swedish convention. In statements prefer an explicit range ("for $n \ge 1$"). |
| Intervals | $[a,b]$, $(a,b)$, $[a,b)$, $(a,\infty)$ | $]a,b[$, $]a,b]$ | The reversed-bracket convention is mentioned on the notation page only. |
| Natural log | $\ln x$ | $\log x$ for natural log | |
| Other logs | $\log_{10} x$, $\log_2 x$, $\log_b x$ | bare $\log x$ | A bare `\log` fails the CI notation lint. |
| Exponential | $e^{x}$, $\exp(x)$ for large exponents | $\mathrm{e}^x$ | Italic $e$ (matches the major calculus texts); the macro set allows a global switch later. |
| Inverse trig | $\arcsin x$, $\arccos x$, $\arctan x$ | $\sin^{-1}x$ (except on the inverse-trig page, where it is mentioned as an alternative and the $1/\sin x$ ambiguity is explained) | |
| Powers of trig | $\sin^2 x = (\sin x)^2$ | $\sin x^2$ when $(\sin x)^2$ is meant | |
| Reciprocal trig | $\sec, \csc, \cot$ defined once in preliminaries | | |
| Angles | radians always | degrees in calculus statements | |
| Derivative | $f'(x)$, $\dv{y}{x}$, $\dv{}{x}\bigl(f(x)\bigr)$; higher: $f''$, $f^{(n)}$ | $\dot y$ (reserved for time derivatives in the ODE chapter, introduced there) | Use Leibniz notation for the chain rule and related rates, prime notation for rules about functions. |
| Differentials | $\dd x$ in integrals via `\dd` | `dx` written raw | A thin space plus upright d. |
| Integrals | $\int_a^b f(x) \dd x$; antiderivative $\int f(x)\dd x = F(x) + C$ | omitting $+C$ | $C$ always stated as "$C \in \R$ arbitrary" once per page. |
| Limits | $\lim_{x \to a} f(x)$; one-sided $x \to a^{+}$, $x \to a^{-}$; $\lim_{n\to\infty} a_n$ | $\lim_{x \to a+}$ | |
| Infinite limits | "$\lim f = \infty$" with the remark that the limit *does not exist* as a real number | | Stated explicitly in `calc-infinite-limits`. |
| Functions | $f\colon A \to B$, $x \mapsto x^2$; "the function $f$" vs "the value $f(x)$" | "the function $f(x)$" in definitions | Allowed informally in examples. |
| Composition / inverse | $f \circ g$; $f^{-1}$ (inverse function); $1/f$ or $f(x)^{-1}$ for reciprocal | | |
| Definitions | $:=$ when defining in a display; "is called" in prose | $\equiv$ | |
| Approximately | $\approx$ with stated precision ("to 4 decimals") | | |
| Sequences | $(a_n)_{n \ge 1}$ or $(a_n)$; terms $a_n$ | $\{a_n\}$ (set braces) | |
| Series | $\sum_{k=1}^{\infty} a_k$; partial sums $s_n = \sum_{k=1}^{n} a_k$ | | Summation index $k$, sequence index $n$. |
| Vectors (later subjects) | $\vb{v}$ (bold upright), components $(v_1, \dots, v_n)$; column vectors in linear algebra | $\vec v$ | Reserved now so `mvc`/`linalg` agree. |
| Absolute value / norm | $\abs{x}$, $\norm{\vb{v}}$ | `\|x\|` raw in large displays (sizing) | Raw `\|x\|` is fine inline. |
| Logic | "if and only if", "implies" in prose; $\implies$, $\iff$ in displays | "iff" | |
| Quantifiers | prose ("for every $\eps > 0$ there exists $\delta > 0$") in core; symbols $\forall\,\exists$ only in the rigorous track | | |
| Decimal mark | point: $3.14$ | comma | Changes in a future Swedish edition. |
| Set-builder | $\{x \in \R : x > 0\}$ | $\{x \mid x>0\}$ | |

## 4.3 Answer LaTeX subset (machine-checked)

Exercise answers are parsed by SymPy (see [06](06-quality-assurance.md)), so answers in
`Answer` dropdowns must use this subset. SymPy 1.14's `antlr` backend reads all of it, but
returns `\pi` and `e` as plain symbols, drops list items after the first comma, and reads a
command it doesn't know as a variable of that name (`\approx 0.69` "parses"). So
`parse_answer` normalises its input, **refuses every command outside this list**, and
post-processes the output (06 §6.1). Its golden tests cover every item below:

- numbers (a decimal is read exactly: `0.69` is $\tfrac{69}{100}$), `\frac{}{}`, `\sqrt{}`,
  `\sqrt[n]{}`, `^{}`, `\pi`, `e`, `\infty`, `-\infty`; `\cdot` or `\times` for a product;
  variables are single letters or Greek letters, optionally with a subscript (`x_1`)
- `\sin \cos \tan \arcsin \arccos \arctan \ln \log_{b}` (a bare `\log` is refused), `\abs{}` / `|x|`
- `+C` for antiderivatives (the checker differentiates instead of comparing)
- several answers as a comma-separated list (each element is checked); intervals as
  `(a, b)` / `[a, b]` with the `set` answer type (see 07); without it, `(a, b)` is a point
- **not** `\mathrm{e}` and not `\dfrac` (normalised by the checker, but avoid them anyway); the
  project macros are expanded from `content/myst.yml`, and `\left`/`\right` and spacing
  commands are dropped
- an answer is a value, not an equation: `2`, not `x = 2`

Answers that are not expressions (proofs, sketches, "does not exist") use
`:class: dropdown answer manual` and are reviewed by hand.

## 4.4 Writing style

- **Language**: English (international, en-GB spelling: *normalise*, *behaviour*). One
  spelling only. codespell enforces it with a curated US→GB dictionary
  (`.codespell-en-gb.txt`, see 05 §5.5), because its built-in dictionaries accept US spellings.
- **Voice**: "we" for shared reasoning ("we now show"), "you" for instructions to the reader
  ("try dragging ε"). Present tense.
- **The notation lint** (`scripts/notation_lint.py`, run by `npm run check`) rejects, in math,
  a bare `\log`, `\sin^{-1}` (and the other inverse-trig powers), a raw `dx` or
  `\mathrm{d}x` in an integral, reversed-bracket intervals `]a, b[`, `\mathrm{e}`, and on
  calculus pages degrees (`°`, `^\circ`); in prose, "clearly", "obviously" and "trivially"
  (a quoted mention is fine). A page that must *show* a rejected form, such as the notation
  guide or the inverse-trig page, wraps that part in `% notation-lint: off (reason)` …
  `% notation-lint: on`.
- **Sentences**: short. One idea per sentence in definitions and theorem statements.
- **Bold** only for terms being defined. *Italics* for emphasis, sparingly.
- **Headings**: sentence case ("Common mistakes", not "Common Mistakes"). Page titles are
  Title Case.
- **Math in prose**: punctuate displayed equations as part of the sentence (comma or full
  stop inside the display).
- **No forward references** in proofs. A "looking ahead" admonition may mention later topics.
- **Units**: applied examples state units, and the final answer has units.
- **Accessibility**: every figure has alt text, and every widget has a one-paragraph text
  description of what it shows, as the caption of its `{figure}` (05 §5.8). Because the
  caption is static HTML, it is the fallback when JavaScript is off or the widget fails to
  load, and screen readers always reach it. Colour is never the only carrier of meaning
  (use colour plus dash style plus labels).
- **i18n readiness**: no wordplay or idioms in core text; labels and file names never
  depend on English grammar beyond being English nouns; no text baked into images (SVG
  text or captions instead).
