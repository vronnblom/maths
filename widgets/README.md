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
key, so existing configs stay valid. The squeeze band (g, f and h drawn at once) was requested
by vronnblom/maths#26 for `calc-squeeze-theorem`; until it is built, that page's figure
switches between g, f and h with a parameter slider.

### `epsilon-delta`

The ε–δ game for $\lim_{x \to a} f(x) = L$: the graph of f near a, the band $|y - L| < ε$
(translucent, dashed edges), the window $0 < |x - a| < δ$ (translucent, solid edges; the dotted
line $x = a$ is left out, and the curve has a gap there), and an open circle at $(a, L)$.
Schema: `schema/widgets/epsilon-delta.schema.json`.

- An **ε slider**. For each ε the widget searches for the largest δ on the left and on the
  right (δ₋, δ₊) and states what it found, one of three outcomes per side:
  - **a δ found**: "the largest δ the widget found is 0.0248456 (checked at 1,954 points)",
    however small (5×10⁻⁸ is shown as such), marked with a dotted tick across the band; if
    nothing fails up to the edge of the x-range, it says so ("out to the edge of the view");
  - **no δ observed**: f leaves the band (or is undefined) at the points closest to a, down to
    10⁻¹² of the reach: "f(x) leaves the band at points within 2×10⁻¹² of 0", then the
    mathematics conditionally: "If no δ works for this ε, then 1 is not the limit …" (a jump
    with ε below the gap, sin(1/x) at 0 with ε < 1, an unbounded f, a wrong L);
  - **could not settle it**: the re-checks ran out, or the window is too small for the doubles
    near a; it keeps what it saw: "f(x) leaves the band at x ≈ 0.708583, so a δ that works is
    at most 0.708584".
  Then, if both sides found a δ, "the largest δ the widget found for both sides" is the smaller.
- A **δ slider** for the reader's own δ, and a **Set δ to the largest on the slider** button: it
  sets the largest value on the slider's grid that is ≤ the δ found, and says so ("δ is now
  0.024, the largest δ on the slider that the widget found to work (the largest δ it found is
  0.0248456)"); if the δ found is below the slider's first step, it says that the slider can't
  show it. The native value, `aria-valuetext`, the readout and the δ in the verdict are always
  the same number (the widget reads it back from the input). Points of the graph inside the
  window but outside the band are marked with crosses (a shape, not only a colour), and a
  sentence says "Your δ = … works: every x the widget checked with 0 < |x − a| < δ has …", or
  "fails: at x ≈ …, f(x) ≈ …, which is not within ε of L", or "fails: f is undefined at x ≈ …,
  in the window"; a point where f is undefined has no graph point, so it is not marked, and
  the sentence says so.
- Zoom in / Zoom out (about (a, L)) / Reset view. Both sentences are `aria-live`, so a screen
  reader hears each new verdict; the sliders are native range inputs.

**What the widget may say.** It is read by students learning the definition of a limit, so it
never states as mathematical fact something it only observed numerically: a δ is "the largest
δ the widget found (checked at N points)", never "the largest δ", and nothing claims that every
smaller δ works; "no δ observed" says what was seen and states the mathematics only as an "if";
it never gives "the limit is L" or "the limit is not L" as a verdict.
`_tests/epsdelta-text.test.mjs` checks every sentence against these rules.

**Where f is undefined** (√x left of 0, 1/x at 0) the condition fails: a δ works only if f is
defined, and within ε of L, on the whole punctured window. This is the first-year definition
(`calc-limit` assumes f is defined on an open interval around a, except possibly at a). f is
never evaluated at x = a itself.

| Key | Required | Meaning |
|---|---|---|
| `f` | ✔ | the function of `x`, in the expression language of `function-plot` above |
| `a` | ✔ | the point x approaches; strictly inside `xRange` |
| `L` | ✔ | the claimed limit, the centre of the band; inside `yRange`. A wrong L is allowed: the widget then observes no δ for small ε |
| `eps` | ✔ | the starting ε (> 0), inside `epsRange` and on the ε slider's grid, `epsRange[0]` + k·`epsStep`, up to floating-point rounding (a range input would snap any other value, and the widget would not start at the ε the caption names; 0.500000005 is off the grid) |
| `epsRange` | ✔ | `[min, max]` of the ε slider, both > 0 |
| `epsStep` | | the ε slider's step (default: the `epsRange` width / 100). Put the values a **Try this:** names on the grid: `"epsRange": [0.05, 1.5], "epsStep": 0.05` reaches 0.1 |
| `delta` | | the starting δ (default: half the distance from a to the nearer end of `xRange`, which is the δ slider's maximum; its step is a thousandth of that, and `delta` must be a whole number of steps) |
| `xRange`, `yRange` | ✔ | `[min, max]` of the view at first. The widget searches for δ up to the ends of `xRange` |

**How the δ is searched for** (`_lib/epsdelta.mjs`, where the method is documented in full).
On each side, δ₊ = sup{t : f is defined and |f(x) − L| < ε for all x with 0 < x − a < t} (and
δ₋ likewise). Every point is a real coordinate: the widget computes the double x = a ± u,
drops it if it rounds onto a, and tests 0 < |x − a| < δ on that x (at a = 100 the offset 0.003
lands at 99.997, 0.0030000000000001137 from a). The widget samples (0, reach]: 1000 equally
spaced points, 480 points going geometrically down to 10⁻¹² × reach, and 480 closing in on the
far end. It finds the failing sample closest to a and bisects between it and the passing one
before (or a itself, so a δ of any size is found), **rounds down** to 6 significant digits (an
exact boundary such as δ = ε/2 = 0.05 shows as 0.05: the window is open), and re-checks the
result on the reader's-check sample of its window. If a point fails there, it is closer to a,
and the search retreats below it; after 8 failed re-checks it stops and says it could not
settle the question, with the closest failure as the bound.

- **It never over-reports on what it evaluated**: a δ found is below every point where f was
  seen to fail, and passed at every point checked in its window. It may under-report by up to
  about 10⁻⁵ (relative), or by the gap between the doubles near a.
- **It is not a proof.** Sampling cannot see a violation narrower than the gaps between samples
  (`1-sign(abs(x-0.49901)-1e-8)+1+sign(x-0.4998)` has a pocket of width 2 × 10⁻⁸ inside the δ it
  finds; `epsdelta.test.mjs` keeps it as a known limitation). That is why the wording says what
  was checked. Configure functions whose behaviour near a is visible at the scale of the figure.
- `widgets/_tests/epsdelta.test.mjs` checks every case against SymPy's exact δ: the reported δ
  is ≤ the exact one and within 2 × 10⁻⁵ of it, "no δ observed" agrees with SymPy's "no δ",
  the reported δ passes the reader's check, and a δ 0.1 % or 10⁻⁶ larger fails. The cases
  include every `epsilon-delta` figure on the site, at its starting ε and at both ends of its
  slider, and every case again translated to a = 10⁵. `make_fixtures.py` does not trust
  `solveset` (1.14 gets |x| at 1/2 wrong): it computes each δ from the complement of the band
  and from the band inequality without `abs`, splitting the window where `abs`, `sign`, `floor`
  or `ceil` change formula, requires the two to agree and the boundary to satisfy |f − L| = ε
  (or f to stop being defined there), probes a capped δ near its end, certifies "no δ" for
  sin(1/x) by points of f = −1 accumulating at a, and refuses any case it cannot certify.
