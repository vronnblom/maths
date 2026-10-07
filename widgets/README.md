# Widgets

Interactive figures for the site (docs/plan/05 §5.8). Each widget is one
[anywidget](https://anywidget.dev) ES module here, configured by the JSON body of an
`{anywidget}` directive, so authors never write JavaScript. The catalogue below lists the
widgets that exist; the plan (05 §5.8) lists the ones to come, each built when a curriculum
page needs it.

## Using a widget on a page

A widget sits alone in a `{figure}`. The figure carries the `wdg-` label, and its caption is
the widget's text description: it is static HTML, so readers get it when JavaScript is off,
when the JSXGraph CDN is down, or when the widget fails. Follow the figure with a
**Try this:** prompt.

`````markdown
::::{figure}
:label: wdg-calc-limit-average-speed

```{anywidget} ../../../widgets/function-plot.mjs
{
  "f": "(5*(1+h)^2 - 5)/h",
  "variable": "h",
  "xRange": [-1, 1],
  "yRange": [5, 15],
  "table": { "points": [0.1, 0.01, 0.001, -0.001, -0.01, -0.1] },
  "hole": { "x": 0 },
  "trace": { "x": 0.5 }
}
```

Graph of the average speed … (the text description).
::::

**Try this:** …
`````

The path is relative to the page: `../../../widgets/` from `content/<subject>/<chapter>/`,
`../../widgets/` from `content/about/`. List the widget's id in the page's `maths.widgets`.
`npm run check` (`scripts/check_widgets.py`) enforces all of this and validates the JSON
against `schema/widgets/<widget>.schema.json`.

## Layout and rules

```
widgets/<name>.mjs            a widget: `export default { render({ model, el }) }`
widgets/_lib/jsxgraph.mjs     the pinned JSXGraph URL (one exact version)
widgets/_lib/expression.mjs   expressions → JessieCode, behind an allowlist   (pure)
widgets/_lib/plot.mjs         sampling, holes, tables, number format, config rules (pure)
widgets/_lib/epsdelta.mjs     the largest δ, the reader's δ check, epsilon-delta's config rules (pure)
widgets/_lib/colours.mjs      light and dark palettes, contrast, scheme changes
widgets/_lib/controls.mjs     sliders, buttons, the value table, the widget CSS
widgets/_lib/board.mjs        JSXGraph board creation and zoom
widgets/_tests/               node --test, against SymPy fixtures (npm run test:widgets)
```

- mystmd publishes only the module named in `{anywidget}` (renamed with a content hash);
  `_lib/` is published next to it by `project.static_files` in `content/myst.yml`, so
  `./_lib/…` imports resolve.
- JSXGraph is loaded **inside `render()`** with `await import(JSXGRAPH_URL)`. No module has a
  static `https:` import: Node refuses them, and the tests import every widget.
- The mathematics a widget computes lives in pure `_lib/` modules (no DOM, no JSXGraph import),
  tested against values that SymPy computes: `uv run python widgets/_tests/make_fixtures.py`
  writes `_tests/fixtures/function-plot.json` and `epsilon-delta.json`, and
  `tests/test_widget_checks.py` fails if either is stale. Never type an expected value by hand.
- The theme renders a widget inside a shadow root and may call `render()` more than once while
  the page hydrates. `render()` replaces the element's content, gives up if the element was
  detached while JSXGraph loaded, and returns a cleanup function.
- Accessibility (docs/plan/12 R12): controls are native `<input type="range">` and
  `<button>` elements (keyboard-operable, labelled, announced with their values); tables are
  real `<table>`s; colours come from `colours.mjs`, whose tests check the contrast in both
  schemes; no information is carried by colour alone.
- A new widget needs: the module, a schema (`additionalProperties: false`), a section below,
  tests, and a `widget` PR (docs/plan/10 §10.2).

## Catalogue

### `function-plot`

The graph of $y = f(x)$, with optional parameter sliders, a table of values, a hole, a point
traced along the graph, and zoom. Schema: `schema/widgets/function-plot.schema.json`.

| Key | Required | Meaning |
|---|---|---|
| `f` | ✔ | the function, in the expression language below |
| `variable` | | its variable, one letter (default `x`; not `e`) |
| `xRange`, `yRange` | ✔ | `[min, max]` of the view at first |
| `parameters` | | up to 6 sliders: `{"a": {"value": 1, "min": -2, "max": 2, "step": 0.5}}` (`step` defaults to (max − min)/100) |
| `table` | | `{"points": [...]}`: a table of values of f at these points (1–12, inside `xRange`) |
| `hole` | | `{"x": 0}`: an open circle at x where f is undefined; its height is the limit of f there, estimated from both sides, or `"y"` if given. The hole's x is left out of the curve, the table and the trace |
| `trace` | | `{"x": 0.5}`: a slider for the variable that moves a point along the graph, with a readout of x and f(x) (`step` defaults to the `xRange` width / 200) |
| `zoom` | | `false` hides the Zoom in / Zoom out / Reset view buttons and the line that states the visible range (default `true`). Zooming centres on the hole, else the traced point; the range line keeps the scale readable when the axes leave the view |

**Expressions.** Numbers (`2`, `0.5`, `1e-3`), the variable, the parameters, `+ - * / ^`
(power, right-associative: `2^3^2` is $2^9$) and parentheses, the constants `pi` and `e`,
and the functions `sin cos tan asin acos atan sinh cosh tanh exp ln sqrt cbrt abs floor ceil
sign`. Multiplication is always written: `2*x`, `a*(x - c)`. `ln` is the natural logarithm;
`log` is rejected (docs/plan/04 §4.2). `cbrt` is the real cube root; `x^(1/3)` is undefined
for negative x. JSXGraph's JessieCode compiles the expression, but only after the allowlist
in `_lib/expression.mjs` has accepted it, because JessieCode on its own returns the argument
of an unknown function (`sec(x)` would be x) and accepts statements and property access.
JessieCode builds the function by running `eval` on the code it generates, so the guarantee
is the allowlist: no statement, property access, string or unknown name reaches it (tested
in `_tests/expression.test.mjs`). The allowlist does not check the grammar, so `npm run check`
also compiles every expression with JessieCode (`scripts/compile_expressions.mjs`, run by
`check_widgets.py`): `sin()` and `x+` are errors there, as in the browser.

**Modes to come** (docs/plan/08, `content/calculus/curriculum.yml`): unit circle ↔ graph,
squeeze band, bisection, f and f′ linked, reveal step by step. Each will be a new optional
key, so existing configs stay valid.

### `epsilon-delta`

The ε–δ game for $\lim_{x \to a} f(x) = L$: the graph of f near a, the band $|y - L| < ε$
(translucent, dashed edges), the window $0 < |x - a| < δ$ (translucent, solid edges; the dotted
line $x = a$ is left out, and the curve has a gap there), and an open circle at $(a, L)$.
Schema: `schema/widgets/epsilon-delta.schema.json`.

- An **ε slider**. For each ε the widget states the largest δ on the left and on the right
  (δ₋, δ₊) and δ = min(δ₋, δ₊), and marks them with dotted ticks across the band. When no δ
  works (a jump with ε below the gap, sin(1/x) at 0 with ε < 1, an unbounded f, a wrong L) it
  says so, and says that this shows L is not the limit; it never shows a tiny δ instead. When
  the graph stays in the band up to the edge of the x-range, it says "at least" that distance.
- A **δ slider** for the reader's own δ, and a **Set δ to the largest** button. Points of the
  graph inside the window but outside the band are marked with crosses (a shape, not only a
  colour), and a sentence says "Your δ = … works" or "fails: at x ≈ …, f(x) ≈ …, which is not
  within ε of L" (or "f is undefined at x ≈ …").
- Zoom in / Zoom out (about (a, L)) / Reset view. Both sentences are `aria-live`, so a screen
  reader hears each new verdict; the sliders are native range inputs.

| Key | Required | Meaning |
|---|---|---|
| `f` | ✔ | the function of `x`, in the expression language of `function-plot` above |
| `a` | ✔ | the point x approaches; strictly inside `xRange` |
| `L` | ✔ | the claimed limit, the centre of the band; inside `yRange`. A wrong L is allowed: the widget then finds no δ for small ε |
| `eps` | ✔ | the starting ε (> 0), inside `epsRange` and on the ε slider's grid, `epsRange[0]` + k·`epsStep` (a range input would snap any other value, and the widget would not start at the ε the caption names) |
| `epsRange` | ✔ | `[min, max]` of the ε slider, both > 0 |
| `epsStep` | | the ε slider's step (default: the `epsRange` width / 100). Put the values a **Try this:** names on the grid: `"epsRange": [0.05, 1.5], "epsStep": 0.05` reaches 0.1 |
| `delta` | | the starting δ (default: half the distance from a to the nearer end of `xRange`, which is the δ slider's maximum; its step is a thousandth of that, and `delta` must be a whole number of steps) |
| `xRange`, `yRange` | ✔ | `[min, max]` of the view at first. The largest δ is searched up to the ends of `xRange` |

**How the largest δ is computed** (`_lib/epsdelta.mjs`, where the method is documented in
full). On each side, with $u = |x - a|$, δ₊ = sup{t : |f(a + u) − L| < ε for all 0 < u < t}
(and δ₋ likewise; where f is undefined the condition fails). The widget samples u in
(0, reach]: 1000 equally spaced points, 480 points going geometrically down to 10⁻¹² × reach
(so an oscillation or a jump at a is seen however close it starts), and 480 closing in on
the far end. It finds the failing sample closest to a, bisects between it and the sample
before, **rounds down** to 6 significant digits (to a decimal no larger than the failing
point, so that an exact boundary such as δ = ε/2 = 0.05 shows as 0.05: the window is open),
and re-checks the result on the reader's-check sample, retreating if anything fails there.

- **It never over-reports on what it sampled**: the reported δ is below every point where the
  condition was seen to fail, and passes at every point evaluated in (0, δ). It may
  under-report by up to about 10⁻⁵ (relative).
- **No δ** is reported when f leaves the band within 10⁻⁶ × the `xRange` width of a. A genuine
  δ smaller than that is reported as none.
- Sampling cannot see a violation narrower than the gaps between samples (a spike of width
  10⁻⁹ in the middle of the window). Configure functions whose behaviour near a is visible at
  the scale of the figure.
- `widgets/_tests/epsdelta.test.mjs` checks every case against SymPy's exact δ (it solves
  |f(x) − L| < ε; for sin(1/x) the one-sided limit's accumulation bounds decide that no δ
  exists; `make_fixtures.py` checks each interval SymPy returns, because `solveset` is
  sometimes wrong, and refuses a case that does not check out): the reported δ is ≤ the exact
  one and within 2 × 10⁻⁵ of it, "no δ" agrees, the reported δ passes the reader's check, and
  a δ 0.1 % or 10⁻⁶ larger fails. The cases include
  every `epsilon-delta` figure on the site, at its starting ε and at both ends of its slider.
