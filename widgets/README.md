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
  writes `_tests/fixtures/function-plot.json`, and `tests/test_widget_checks.py` fails if it
  is stale. Never type an expected value by hand.
- The theme renders a widget inside a shadow root and may call `render()` more than once while
  the page hydrates. `render()` replaces the element's content, gives up if the element was
  detached while JSXGraph loaded, and returns a cleanup function.
- Accessibility (docs/plan/12 R12): controls are native `<input type="range">` and
  `<button>` elements (keyboard-operable, labelled, announced with their values); tables are
  real `<table>`s; colours come from `colours.mjs`, whose tests check the contrast in both
  schemes; no information is carried by colour alone.
- A new widget needs: the module, a schema (`additionalProperties: false`), a section below,
  tests, and a `tooling` PR.

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

**Modes to come** (docs/plan/08, `content/calculus/curriculum.yml`): unit circle ↔ graph,
squeeze band, bisection, f and f′ linked, reveal step by step. Each will be a new optional
key, so existing configs stay valid.
