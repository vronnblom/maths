// The mathematics of function-plot (docs/plan/05 §5.8, 06 §6.2): sampling the graph, the value
// at a hole, the table of values, number formatting, and the semantic checks of a config. Pure:
// no DOM and no JSXGraph. `f` is any function x → number (NaN where undefined), in practice
// the JessieCode function from expression.mjs. widgets/_tests/ checks all of it against values
// that SymPy precomputed.

/**
 * Sample f at n + 1 equally spaced points of [a, b], for drawing. Returns {xs, ys}, where
 * NaN in ys means "no curve here": f is undefined there, the point is excluded (a hole), or
 * the graph jumps (a pole or a jump discontinuity). A jump is detected by bisection: between
 * two samples whose values differ by more than `jump`, a continuous function's difference
 * shrinks as the interval does; a discontinuous one's does not.
 */
export function sample(f, a, b, { n = 400, exclude = [], jump = Infinity } = {}) {
  const xs = [];
  const ys = [];
  const tol = 1e-9 * (b - a);
  const value = (x) => (exclude.some((e) => Math.abs(x - e) <= tol) ? NaN : f(x));
  let prev = null;
  for (let i = 0; i <= n; i++) {
    const x = i === n ? b : a + ((b - a) * i) / n;
    const y = value(x);
    if (prev && Number.isFinite(prev.y) && Number.isFinite(y) && Math.abs(y - prev.y) > jump) {
      const at = discontinuity(value, prev.x, prev.y, x, y, jump);
      if (at !== null) {
        xs.push(at);
        ys.push(NaN);
      }
    }
    xs.push(x);
    ys.push(y);
    prev = { x, y };
  }
  return { xs, ys };
}

/** Where f jumps by more than `jump` between x0 and x1, or null if it is continuous there. */
export function discontinuity(f, x0, y0, x1, y1, jump, steps = 40) {
  for (let k = 0; k < steps; k++) {
    const xm = (x0 + x1) / 2;
    const ym = f(xm);
    if (!Number.isFinite(ym)) return xm;
    if (Math.abs(ym - y0) >= Math.abs(y1 - ym)) [x1, y1] = [xm, ym];
    else [x0, y0] = [xm, ym];
    if (Math.abs(y1 - y0) <= jump / 4) return null; // the gap closes: continuous, just steep
  }
  return (x0 + x1) / 2;
}

/**
 * The value that f approaches at x0 (the y of a hole), from both sides. `scale` is a length
 * on the x-axis (the width of the plot): the estimate uses points within scale·1e-3 of x0.
 * Each side is extrapolated (Richardson) from two step sizes, at two scales; the estimates
 * must settle (else f has no finite limit there: a pole, an oscillation) and the two sides
 * must agree (else it jumps). Throws a RangeError otherwise.
 */
export function holeValue(f, x0, scale = 1) {
  const h = 1e-3 * scale;
  const side = (s, k) => 2 * f(x0 + (s * k) / 2) - f(x0 + s * k);
  const settled = (a, b) => Math.abs(a - b) <= 1e-3 * Math.max(1, Math.abs(a), Math.abs(b));
  const sides = [-1, 1].map((s) => [side(s, h), side(s, h / 8)]);
  if (sides.flat().some((v) => !Number.isFinite(v)) || !sides.every(([a, b]) => settled(a, b))) {
    throw new RangeError(`f has no finite value to approach at x = ${x0}: give hole.y`);
  }
  const [left, right] = sides.map(([, b]) => b);
  if (Math.abs(left - right) > 1e-4 * Math.max(1, Math.abs(left), Math.abs(right))) {
    throw new RangeError(`f approaches different values from the left (${left}) and the right (${right}) of x = ${x0}: give hole.y`);
  }
  // Symmetric average: the odd terms of the expansion cancel, then one Richardson step.
  const g = (k) => (f(x0 - k) + f(x0 + k)) / 2;
  const y = (4 * g(h / 2) - g(h)) / 3;
  return Number.isFinite(y) ? y : (left + right) / 2;
}

/** The rows of the table of values: [{x, y}], y NaN where f is undefined (or at the hole). */
export function tableRows(f, points, { holeX = null } = {}) {
  return points.map((x) => ({ x, y: holeX !== null && x === holeX ? NaN : f(x) }));
}

const SUPERSCRIPT = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };

/**
 * A number for display: `digits` significant digits, trailing zeros dropped, a real minus
 * sign, "×10ⁿ" instead of e-notation, and "undefined" for NaN.
 */
export function formatNumber(v, digits = 6) {
  if (!Number.isFinite(v)) return "undefined";
  if (v === 0) return "0";
  let s = v.toPrecision(digits);
  let exp = "";
  const k = s.indexOf("e");
  if (k >= 0) {
    exp = s.slice(k + 1).replace("+", "");
    s = s.slice(0, k);
  }
  if (s.includes(".")) s = s.replace(/0+$/, "").replace(/\.$/, "");
  if (exp) s += "×10" + [...exp].map((c) => SUPERSCRIPT[c]).join("");
  return s.replace("-", "−");
}

/** Parse a number displayed by formatNumber back (for tests of the rendered table). */
export function parseDisplayed(s) {
  if (s === "undefined") return NaN;
  const m = /^(.*?)(?:×10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+))?$/.exec(s.trim().replace("−", "-"));
  const inv = Object.fromEntries(Object.entries(SUPERSCRIPT).map(([k, v]) => [v, k]));
  const exp = m[2] ? [...m[2]].map((c) => inv[c]).join("") : "0";
  return Number(m[1]) * 10 ** Number(exp);
}

/**
 * The semantic rules that JSON Schema cannot express (scripts/check_widgets.py applies the same
 * rules in CI; widgets/_tests/fixtures/function-plot-invalid.json keeps the two in step).
 * Returns a list of messages, empty if the config is fine.
 */
export function configProblems(config) {
  const problems = [];
  const variable = config.variable ?? "x";
  const range = (key) => {
    const r = config[key];
    if (Array.isArray(r) && r.length === 2 && !(r[0] < r[1])) problems.push(`${key}: the first number must be smaller than the second`);
  };
  range("xRange");
  range("yRange");
  const [x0, x1] = config.xRange ?? [-Infinity, Infinity];
  const inside = (x) => x >= x0 && x <= x1;
  for (const [name, p] of Object.entries(config.parameters ?? {})) {
    if (name === variable) problems.push(`parameters.${name}: a parameter cannot have the name of the variable`);
    if (!(p.min < p.max)) problems.push(`parameters.${name}: min must be smaller than max`);
    else if (!(p.value >= p.min && p.value <= p.max)) problems.push(`parameters.${name}: value must lie between min and max`);
  }
  for (const x of config.table?.points ?? []) {
    if (!inside(x)) problems.push(`table.points: ${x} lies outside xRange`);
  }
  if (config.hole && !inside(config.hole.x)) problems.push(`hole.x: ${config.hole.x} lies outside xRange`);
  if (config.trace && !inside(config.trace.x)) problems.push(`trace.x: ${config.trace.x} lies outside xRange`);
  return problems;
}
