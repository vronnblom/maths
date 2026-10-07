// The mathematics of epsilon-delta (docs/plan/05 §5.8, 06 §6.2): the largest admissible δ on
// each side of a, the check of a reader's δ, and the semantic checks of a config. Pure: no DOM
// and no JSXGraph. `f` is any function x → number (NaN where undefined), in practice the
// JessieCode function from expression.mjs. widgets/_tests/epsdelta.test.mjs checks it against
// the exact δ that SymPy computes (fixtures/epsilon-delta.json).
//
// For ε > 0 the largest δ on the right of a is
//     δ₊ = sup{t > 0 : |f(x) − L| < ε for every x in (a, a + t)},
// and δ₋ likewise on the left; δ = min(δ₋, δ₊) is the largest δ that works on both sides.
// Where f is undefined, |f(x) − L| < ε fails. Each side is searched up to its `reach` (the
// distance from a to the end of the x-range); if nothing fails before that, δ is "at least the
// reach" (`capped`).
//
// The method, for one side (u = |x − a|):
//  1. Sample u in (0, reach]: METHOD.uniform equally spaced points; METHOD.geometric points
//     reach·10^(−12k/480), 40 per decade down to reach·10⁻¹², so that an oscillation or a jump
//     at a itself is seen, however close to a it starts; and as many points
//     reach·(1 − 10^(−12k/480)) closing in on the far end, where a monotone f leaves the band
//     (this is what lets the reader's check see that a δ just 0.1 % too large fails).
//  2. Find the sample closest to a where the condition fails. If it lies within
//     METHOD.noDelta·width of a (width: the x-range), there is no δ: f leaves the band that close
//     to a (a jump with ε below the gap, sin(1/x) with ε < 1, an unbounded f, a wrong L).
//  3. Otherwise bisect between it (`hi`, failing) and the sample before it (passing), down to
//     a few units in the last place; every point evaluated below the final `hi` passed.
//  4. Round the failing point's distance |x − a| down to METHOD.digits significant digits. The
//     window 0 < |x − a| < δ is open, so that distance itself works when everything closer
//     passes; rounding down keeps δ at or below the failing point, and an exact boundary such
//     as δ = ε/2 = 0.05 is reported as 0.05.
//  5. Re-check the result on a fresh sample of (0, δ) (the reader's check, `failures`); if a
//     point fails there, retreat below it and repeat.
// So a reported δ never exceeds a point where the condition was seen to fail, and passes at
// every point the method evaluated in (0, δ): it never over-reports on what was sampled. It
// under-reports by at most about 10⁻⁵ relative (the rounding), or reports "no δ" for a
// genuine δ smaller than METHOD.noDelta·width. Sampling cannot see a violation narrower than
// the gaps between samples (a spike of width 10⁻⁹ in the middle of the window); no numerical
// method can without knowing more about f.

export const METHOD = {
  uniform: 1000,
  geometric: 480,
  depth: 1e-12,
  noDelta: 1e-6,
  digits: 6,
  bisections: 80,
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

/** v rounded down to `digits` significant digits (0 for v ≤ 0). */
export function floorSignificant(v, digits = METHOD.digits) {
  if (!(v > 0) || !Number.isFinite(v)) return 0;
  const scale = 10 ** (digits - 1 - Math.floor(Math.log10(v)));
  let n = Math.floor(v * scale);
  while (n > 0 && n / scale > v) n -= 1; // v·scale may round up in binary
  return n / scale;
}

const inBand = (y, L, eps) => Math.abs(y - L) < eps; // false for NaN: undefined fails

/**
 * The points of 0 < |x − a| < delta on one side (side = −1 left, +1 right) where
 * |f(x) − L| < ε fails, closest to a first: [{x, y, u}] (u = |x − a|; y NaN where f is
 * undefined).
 */
export function failures(f, { a, L, eps, side, delta, ...opts }) {
  const bad = [];
  for (const u of offsets(delta, opts)) {
    if (u >= delta) continue; // the window is open
    const x = a + side * u;
    const y = f(x);
    if (!inBand(y, L, eps)) bad.push({ x, y, u });
  }
  return bad;
}

/**
 * The largest δ on one side: {delta, capped, none, at}. `capped`: nothing fails up to the
 * reach, and delta is the reach. `none`: f leaves the band within METHOD.noDelta·width of a,
 * and delta is 0. `at` is the x of a failing point just beyond delta (null when capped).
 */
export function sideDelta(f, { a, L, eps, side, reach, width }) {
  const point = (u) => a + side * u;
  const good = (u) => inBand(f(point(u)), L, eps);
  const tooClose = METHOD.noDelta * width;
  const none = (u) => ({ delta: 0, capped: false, none: true, at: point(u) });
  // The first failing sample of (0, r] and the sample before it, or null if none fails.
  const bracket = (r) => {
    const us = offsets(r);
    const i = us.findIndex((u) => !good(u));
    return i < 0 ? null : { lo: i > 0 ? us[i - 1] : 0, hi: us[i] };
  };
  let b = bracket(reach);
  if (!b) return { delta: reach, capped: true, none: false, at: null };
  for (let round = 0; round <= METHOD.rechecks; round++) {
    if (b.hi <= tooClose) return none(b.hi);
    let { lo, hi } = b;
    for (let k = 0; k < METHOD.bisections && hi - lo > 4 * Number.EPSILON * hi; k++) {
      const mid = (lo + hi) / 2;
      if (good(mid)) lo = mid;
      else hi = mid;
    }
    // The failing point's own distance from a: x = a ± u is rounded, and 3 − 0.2499…9 is 2.75.
    const delta = floorSignificant(Math.abs(point(hi) - a));
    if (!(delta > tooClose)) return none(hi);
    if (!failures(f, { a, L, eps, side, delta }).length) return { delta, capped: false, none: false, at: point(hi) };
    // The re-check found a point that the first sample missed: start again below it.
    b = bracket(delta);
  }
  return none(b.hi);
}

/**
 * The largest δ on both sides of a: {left, right, delta, none}. `reach` is [left, right], the
 * distances from a to the ends of the x-range, and `width` the width of the x-range.
 */
export function largestDelta(f, { a, L, eps, reach, width }) {
  const left = sideDelta(f, { a, L, eps, side: -1, reach: reach[0], width });
  const right = sideDelta(f, { a, L, eps, side: 1, reach: reach[1], width });
  const none = left.none || right.none;
  return { left, right, none, delta: none ? 0 : Math.min(left.delta, right.delta) };
}

/**
 * Whether a reader's δ works: {works, left, right, witness}. left and right are the failing
 * points of each side ([{x, y}], closest to a first); `witness` is one failing point to name in
 * the verdict (null if δ works): the worst one, |f(x) − L| largest, among those not
 * extremely close to a, else the farthest failing point.
 */
export function checkDelta(f, { a, L, eps, delta }) {
  const left = failures(f, { a, L, eps, side: -1, delta });
  const right = failures(f, { a, L, eps, side: 1, delta });
  const all = [...left, ...right];
  if (!all.length) return { works: true, left, right, witness: null };
  const visible = all.filter((p) => p.u >= delta * 1e-3 && Number.isFinite(p.y));
  const witness = visible.length
    ? visible.reduce((w, p) => (Math.abs(p.y - L) > Math.abs(w.y - L) ? p : w))
    : all.reduce((w, p) => (p.u > w.u ? p : w));
  return { works: false, left, right, witness };
}

/** At most n items of a list, evenly spread (for drawing failing points). */
export function spread(items, n) {
  if (items.length <= n) return items;
  return Array.from({ length: n }, (_, i) => items[Math.round((i * (items.length - 1)) / (n - 1))]);
}

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
  return problems;
}
