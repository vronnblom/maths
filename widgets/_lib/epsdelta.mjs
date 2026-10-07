// The mathematics of epsilon-delta (docs/plan/05 §5.8, 06 §6.2): the largest δ on each side of
// a that the widget can find, the check of a reader's δ, and the semantic checks of a config.
// Pure: no DOM and no JSXGraph. `f` is any function x → number (NaN where undefined), in
// practice the JessieCode function from expression.mjs. widgets/_tests/epsdelta.test.mjs checks
// it against the exact δ that SymPy computes (fixtures/epsilon-delta.json).
//
// For ε > 0 the largest δ on the right of a is
//     δ₊ = sup{t > 0 : f is defined and |f(x) − L| < ε for every x with 0 < x − a < t},
// and δ₋ likewise on the left; δ = min(δ₋, δ₊) is the largest δ that works on both sides.
// **A point where f is undefined counts as a failure**: a δ works only if f is defined, and
// within ε of L, on the whole punctured window. This is the first-year definition (f defined on
// an open interval around a, except possibly at a). f is never evaluated at x = a itself.
// Each side is searched up to its `reach` (the distance from a to the end of the x-range).
//
// Every point is a real coordinate: x = a ± u is rounded to a double, so the method keeps the
// x it will evaluate, drops it if it rounds onto a (or past it), and measures the window
// condition 0 < |x − a| < δ on that x, never on the u it started from. Points are deduplicated
// by x.
//
// The method, for one side:
//  1. Sample (0, reach]: METHOD.uniform equally spaced offsets; METHOD.geometric offsets
//     reach·10^(−12k/480), 40 per decade down to reach·10⁻¹², so that an oscillation or a jump
//     at a itself is seen, however close to a it starts; and as many offsets
//     reach·(1 − 10^(−12k/480)) closing in on the far end, where a monotone f leaves the band
//     (this is what lets the reader's check see that a δ just 0.1 % too large fails).
//     If no sample fails, the side is `capped`: the widget found δ = reach and looked no further.
//  2. Bisect between the failing sample closest to a (`hi`) and the passing one before it (or a
//     itself, never evaluated), until the two are neighbouring doubles or the gap is below
//     2⁻⁴⁰ of the distance; from a itself this descends as far as doubles go, so a δ of any size
//     is found. Every point evaluated closer to a than the final `hi` passed.
//  3. Round |hi − a| down to METHOD.digits significant digits: the window is open, so that
//     distance itself is a candidate when everything closer passes, and an exact boundary such
//     as δ = ε/2 = 0.05 is reported as 0.05. That is only when the last passing point `lo` is
//     within 2⁻³⁰ (relative) of the rounded value; otherwise the doubles near a are too coarse to
//     say where between lo and hi the boundary is, and |lo − a| is rounded down instead.
//  4. Re-check the candidate on the reader's-check sample of its window (`windowPoints`). If
//     every point passes, the δ is **found**. If one fails, it is closer to a than the
//     candidate, so the search retreats strictly: bisect again between it and the passing point
//     before it. At most METHOD.rechecks re-checks are made.
// Three outcomes per side (`status`):
//  - "found": a δ that passed its re-check at `checked` points, however small it is. It never
//    exceeds a point where f was seen to fail (`at`), but it is what the widget found, not a
//    proof: sampling cannot see a violation narrower than the gaps between samples (a spike of
//    width 10⁻⁹ in mid-window), and no numerical method can without knowing more about f.
//  - "none" (no δ observed): no δ was found, and f was seen to fail within `near` of a, where
//    near = max(reach·METHOD.noDelta, 2|a|·2⁻⁵²): as close to a as the samples go, down to
//    the first doubles next to a (a jump, sin(1/x), an unbounded f, a wrong L). That is an
//    observation, not a proof that no δ exists.
//  - "indeterminate": no δ was found and the failures seen are farther from a than that: the
//    re-checks ran out (`reason: "rechecks"`), or the next candidate's window holds fewer than
//    METHOD.minPoints doubles (`reason: "resolution"`). `bound` keeps what was observed: f fails
//    at distance `bound` from a, so no δ above it works.

export const METHOD = {
  uniform: 1000,
  geometric: 480,
  depth: 1e-12,
  noDelta: 1e-12,
  minPoints: 100,
  digits: 6,
  bisections: 1100,
  rechecks: 8,
};

/** The offsets u in (0, reach] at which a side is sampled (step 1), increasing, without repeats. */
export function offsets(reach, { uniform = METHOD.uniform, geometric = METHOD.geometric, depth = METHOD.depth } = {}) {
  const us = [];
  for (let j = 1; j <= uniform; j++) us.push(j === uniform ? reach : (reach * j) / uniform);
  const ratio = depth ** (1 / geometric);
  for (let k = 1; k <= geometric; k++) {
    us.push(reach * ratio ** k);
    us.push(reach * (1 - ratio ** k));
  }
  us.sort((p, q) => p - q);
  return us.filter((u, i) => u > 0 && u !== us[i - 1]);
}

/**
 * v rounded down to `digits` significant digits: the double nearest to the decimal n·10^e (so
 * 0.05 is the double 0.05, as SymPy's 1/20 is), stepped down while it exceeds v. 0 for v ≤ 0,
 * and below 10⁻²⁹⁰, where doubles no longer carry `digits` digits.
 */
export function floorSignificant(v, digits = METHOD.digits) {
  if (!(v >= 1e-290) || !Number.isFinite(v)) return 0;
  const e = Math.floor(Math.log10(v)) - (digits - 1);
  const decimal = (n) => Number(`${n}e${e}`); // parsed: correctly rounded
  const [mantissa, exponent] = v.toExponential().split("e"); // v = mantissa·10^exponent, shortest
  let n = Math.floor(Number(`${mantissa}e${Number(exponent) - e}`));
  while (n > 0 && decimal(n) > v) n -= 1;
  if (decimal(n + 1) <= v) n += 1; // n is off by at most one either way
  return decimal(n);
}

/** v rounded up to `digits` significant digits (for "at most" bounds); v itself if v ≤ 0. */
export function ceilSignificant(v, digits = METHOD.digits) {
  const down = floorSignificant(v, digits);
  if (!(v > 0) || down >= v) return down || v;
  const e = Math.floor(Math.log10(down)) - (digits - 1);
  return Number(`${Math.round(down / 10 ** e) + 1}e${e}`);
}

const inBand = (y, L, eps) => Math.abs(y - L) < eps; // false for NaN: undefined fails

/** The distance of x from a on `side` (−1 left, +1 right), measured on the double x: > 0 inside. */
const distance = (a, side, x) => side * (x - a);

/**
 * The points of the side's window 0 < |x − a| < delta that the reader's check (and the
 * re-check) evaluate: [{x, d}], d = |x − a| of the double x, closest to a first, each x once,
 * never a itself. `inclusive` keeps d = delta too (the search over (0, reach]).
 */
export function windowPoints(a, side, delta, { inclusive = false, ...opts } = {}) {
  const pts = [];
  let last = NaN;
  for (const u of offsets(delta, opts)) {
    const x = a + side * u;
    const d = distance(a, side, x);
    if (!(d > 0) || x === last) continue;
    if (d > delta || (d === delta && !inclusive)) continue; // the window is open
    pts.push({ x, d });
    last = x;
  }
  pts.sort((p, q) => p.d - q.d);
  return pts.filter((p, i) => i === 0 || p.x !== pts[i - 1].x);
}

/**
 * The points of 0 < |x − a| < delta on one side where f is undefined or |f(x) − L| < ε fails,
 * closest to a first: [{x, y, u}] (u = |x − a| of the double x; y NaN where f is undefined).
 */
export function failures(f, { a, L, eps, side, delta, ...opts }) {
  const bad = [];
  for (const { x, d } of windowPoints(a, side, delta, opts)) {
    const y = f(x);
    if (!inBand(y, L, eps)) bad.push({ x, y, u: d });
  }
  return bad;
}

/**
 * The largest δ that the widget finds on one side: {status, delta, capped, at, bound,
 * undefinedAt, near, checked, rechecks, reason}. status is "found", "none" or "indeterminate"
 * (see the header). delta: the δ found (0 unless found); capped: nothing failed up to the
 * reach, and delta is the reach; at: the x of the failing point closest to a that was seen
 * (null if none was); bound: its distance |at − a| (no δ above it works); undefinedAt: f is
 * undefined at `at` (else it is outside the band there); near: how close to a a failure must be
 * seen for "none"; checked: how many points the found δ passed; rechecks: how many re-checks
 * failed; reason ("rechecks" or "resolution"): why an indeterminate side stopped.
 */
export function sideDelta(f, { a, L, eps, side, reach }) {
  const dist = (x) => distance(a, side, x);
  const good = (x) => inBand(f(x), L, eps);
  const near = Math.max(reach * METHOD.noDelta, 2 * Math.abs(a) * Number.EPSILON);
  let at = null; // the failing point closest to a that was seen
  const failed = (x) => {
    if (at === null || dist(x) < dist(at)) at = x;
  };
  const result = (status, extra) => ({
    status, delta: 0, capped: false, at, bound: at === null ? null : dist(at),
    undefinedAt: at !== null && Number.isNaN(f(at)), near, checked: 0, rechecks, reason: null, ...extra,
  });

  // 1. The first failing sample of (0, reach], and the passing sample before it (or a).
  const samples = windowPoints(a, side, reach, { inclusive: true });
  const first = samples.findIndex((p) => !good(p.x));
  let rechecks = 0;
  if (first < 0) return result("found", { delta: reach, capped: true, checked: samples.length });
  let lo = first > 0 ? samples[first - 1].x : a; // passes (or is a, never evaluated)
  let hi = samples[first].x; // fails
  failed(hi);
  let reason = "rechecks";
  for (;;) {
    // 2. Bisect on the doubles between lo and hi.
    for (let k = 0; k < METHOD.bisections; k++) {
      const mid = lo + (hi - lo) / 2;
      if (mid === lo || mid === hi || mid === a) break;
      if (good(mid)) lo = mid;
      else {
        hi = mid;
        failed(hi);
      }
      if (lo !== a && dist(hi) - dist(lo) <= dist(hi) * 2 ** -40) break;
    }
    // 3. The candidate, rounded down: from the failing point's own distance when the last
    // passing point is next to it, else from the passing point's (where the doubles near a are
    // coarse, the boundary may lie anywhere between the two).
    const close = floorSignificant(dist(hi)) - (lo === a ? 0 : dist(lo)) <= dist(hi) * 2 ** -30;
    const delta = floorSignificant(close ? dist(hi) : dist(lo));
    const pts = delta > 0 ? windowPoints(a, side, delta) : [];
    if (pts.length < METHOD.minPoints) {
      reason = "resolution";
      break;
    }
    // 4. The re-check.
    const j = pts.findIndex((p) => !good(p.x));
    if (j < 0) return result("found", { delta, checked: pts.length });
    failed(pts[j].x);
    rechecks += 1;
    if (rechecks >= METHOD.rechecks) break;
    // Retreat: strictly closer to a than the candidate, so strictly closer than hi.
    lo = j > 0 ? pts[j - 1].x : a;
    hi = pts[j].x;
  }
  if (dist(at) <= near) return result("none");
  return result("indeterminate", { reason });
}

/**
 * The largest δ the widget finds on both sides of a: {left, right, status, delta}. `reach` is
 * [left, right], the distances from a to the ends of the x-range. status is "none" if either
 * side is, else "indeterminate" if either side is, else "found" with delta = min(δ₋, δ₊).
 */
export function largestDelta(f, { a, L, eps, reach }) {
  const left = sideDelta(f, { a, L, eps, side: -1, reach: reach[0] });
  const right = sideDelta(f, { a, L, eps, side: 1, reach: reach[1] });
  const statuses = [left.status, right.status];
  const status = statuses.includes("none") ? "none" : statuses.includes("indeterminate") ? "indeterminate" : "found";
  return { left, right, status, delta: status === "found" ? Math.min(left.delta, right.delta) : 0 };
}

/**
 * Whether a reader's δ works at the points the widget checks: {works, left, right, witness,
 * checked}. left and right are the failing points of each side ([{x, y, u}], closest to a
 * first); `witness` is one failing point to name in the verdict (null if δ works): the worst
 * one, |f(x) − L| largest, among those not extremely close to a, else the farthest failing
 * point; `checked` is the number of points evaluated.
 */
export function checkDelta(f, { a, L, eps, delta }) {
  const left = failures(f, { a, L, eps, side: -1, delta });
  const right = failures(f, { a, L, eps, side: 1, delta });
  const checked = windowPoints(a, -1, delta).length + windowPoints(a, 1, delta).length;
  const all = [...left, ...right];
  if (!all.length) return { works: true, left, right, witness: null, checked };
  const visible = all.filter((p) => p.u >= delta * 1e-3 && Number.isFinite(p.y));
  const witness = visible.length
    ? visible.reduce((w, p) => (Math.abs(p.y - L) > Math.abs(w.y - L) ? p : w))
    : all.reduce((w, p) => (p.u > w.u ? p : w));
  return { works: false, left, right, witness, checked };
}

/** At most n items of a list, evenly spread (for drawing failing points). */
export function spread(items, n) {
  if (items.length <= n) return items;
  return Array.from({ length: n }, (_, i) => items[Math.round((i * (items.length - 1)) / (n - 1))]);
}

/**
 * The steps of the two sliders: ε from epsRange[0] in steps of epsStep (default: a hundredth of
 * epsRange), and δ in steps of a thousandth of the distance from a to the nearer end of xRange.
 */
export function sliderSteps(config) {
  const [e0, e1] = config.epsRange;
  return { eps: config.epsStep ?? (e1 - e0) / 100, delta: Math.min(config.a - config.xRange[0], config.xRange[1] - config.a) / 1000 };
}

// Whether v is start + k·step for a whole k ≥ 0 (up to rounding): a range input snaps any other
// value, so the widget would not start where the caption says.
const onGrid = (v, start, step) => {
  const k = (v - start) / step;
  return k > -1e-6 && Math.abs(k - Math.round(k)) <= 1e-6;
};

/**
 * The semantic rules that JSON Schema cannot express (scripts/check_widgets.py applies the same
 * rules in CI; widgets/_tests/fixtures/epsilon-delta-invalid.json keeps the two in step).
 * Returns a list of messages, empty if the config is fine.
 */
export function configProblems(config) {
  const problems = [];
  const increasing = (key) => {
    const r = config[key];
    const ok = !(Array.isArray(r) && r.length === 2) || r[0] < r[1];
    if (!ok) problems.push(`${key}: the first number must be smaller than the second`);
    return ok && Array.isArray(r);
  };
  const xOk = increasing("xRange");
  const yOk = increasing("yRange");
  const epsOk = increasing("epsRange");
  const [x0, x1] = config.xRange ?? [];
  if (xOk && !(config.a > x0 && config.a < x1)) problems.push("a: must lie strictly inside xRange, so that both sides of a show");
  if (yOk && !(config.L >= config.yRange[0] && config.L <= config.yRange[1])) problems.push("L: must lie inside yRange");
  if (epsOk && !(config.eps >= config.epsRange[0] && config.eps <= config.epsRange[1])) problems.push("eps: must lie inside epsRange");
  if (epsOk && config.epsStep !== undefined && !(config.epsStep <= config.epsRange[1] - config.epsRange[0])) {
    problems.push("epsStep: must be at most the width of epsRange");
  }
  if (xOk && config.delta !== undefined && !(config.delta <= Math.min(config.a - x0, x1 - config.a))) {
    problems.push("delta: must be at most the distance from a to the nearer end of xRange");
  }
  if (!problems.length) {
    const step = sliderSteps(config);
    if (!onGrid(config.eps, config.epsRange[0], step.eps)) {
      problems.push("eps: must be on the ε slider's grid, epsRange[0] + k·epsStep (epsStep defaults to a hundredth of epsRange)");
    }
    if (config.delta !== undefined && !(config.delta >= step.delta && onGrid(config.delta, 0, step.delta))) {
      problems.push("delta: must be on the δ slider's grid, k thousandths of the distance from a to the nearer end of xRange");
    }
  }
  return problems;
}
