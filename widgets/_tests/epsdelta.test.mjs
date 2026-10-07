// widgets/_lib/epsdelta.mjs against SymPy (fixtures/epsilon-delta.json): the largest δ found on
// each side never exceeds the exact value and is within the fixture's tolerance of it; "no δ
// observed" is reported exactly where SymPy finds none, and every other case is "found"; the
// reported δ passes the reader's check and a slightly larger one fails. Then the regressions of
// the review of PR 10 (F1–F4: a tiny δ, the real coordinate, x = a, the re-check budget, thin
// pockets), the rounding, and the config rules shared with scripts/check_widgets.py.
import { test } from "node:test";
import assert from "node:assert/strict";

import { checkExpression, compileExpression } from "../_lib/expression.mjs";
import { METHOD, ceilSignificant, checkDelta, configProblems, floorSignificant, largestDelta, offsets, sideDelta, spread, windowPoints } from "../_lib/epsdelta.mjs";
import { JXG, epsilonDelta, epsilonDeltaInvalid } from "./helpers.mjs";

const { tolerance } = epsilonDelta;

for (const c of epsilonDelta.cases) {
  const g = compileExpression(JXG, c.f, "x");
  // f is never evaluated at a itself (review F2), in any case.
  const f = (x) => {
    assert.notEqual(x, c.a, `f evaluated at x = a = ${c.a}`);
    return g(x);
  };
  const [x0, x1] = c.xRange;
  const reach = [c.a - x0, x1 - c.a];
  let computed = null; // computed inside the tests, so that a failure is the test's, not the file's
  const largest = () => (computed ??= largestDelta(f, { a: c.a, L: c.L, eps: c.eps, reach }));
  const spacing = Math.abs(c.a) * Number.EPSILON; // at least the gap between neighbouring doubles near a

  test(`largest δ matches SymPy: ${c.f} at a = ${c.a}, L = ${c.L}, ε = ${c.eps} (${c.case})`, () => {
    const result = largest();
    for (const [name, exact, got] of [["left", c.left, result.left], ["right", c.right, result.right]]) {
      const where = `${name}: got ${JSON.stringify(got)}, SymPy ${JSON.stringify(exact)}`;
      assert.equal(got.status, exact.none ? "none" : "found", `the outcome disagrees, ${where}`);
      if (exact.none) {
        assert.ok(got.bound <= got.near, `"no δ observed" needs a failure within ${got.near} of a, ${where}`);
        continue;
      }
      assert.ok(got.delta <= exact.delta, `over-reported, ${where}`);
      if (!got.capped) assert.ok(got.delta <= got.bound, `above a point seen to fail, ${where}`);
      // The tolerance, plus the gap between the doubles near a: below it there is nothing to evaluate.
      assert.ok(got.delta >= exact.delta * (1 - tolerance) - 2 * spacing, `more than ${tolerance} below, ${where}`);
      assert.equal(got.capped, exact.capped, `capped disagrees, ${where}`);
    }
    assert.equal(result.status, c.left.none || c.right.none ? "none" : "found");
    if (result.status === "found") assert.equal(result.delta, Math.min(result.left.delta, result.right.delta));
  });

  test(`the reader's check agrees: ${c.f} at a = ${c.a}, L = ${c.L}, ε = ${c.eps}`, () => {
    const result = largest();
    const check = (delta) => checkDelta(f, { a: c.a, L: c.L, eps: c.eps, delta });
    if (result.status === "found") assert.ok(check(result.delta).works, `the reported δ = ${result.delta} fails`);
    // A δ just too large fails: by 0.1 % (one step of a slider) and by 10⁻⁶ (relative).
    for (const [name, side] of [["left", c.left], ["right", c.right]]) {
      // (Larger by at least four doubles near a: a smaller step has no double inside it.)
      const deltas = side.none
        ? [Math.min(...reach) / 2]
        : [side.delta * 1.001, side.delta * (1 + 1e-6)].map((d) => Math.max(d, side.delta + 4 * spacing));
      for (const delta of deltas) {
        if (side.capped || delta > reach[name === "left" ? 0 : 1]) continue;
        const verdict = check(delta);
        assert.ok(!verdict.works && verdict[name].length > 0, `δ = ${delta} should fail on the ${name}`);
        assert.ok(verdict.witness, "a failing point is named");
        assert.ok(!(Math.abs(verdict.witness.y - c.L) < c.eps), "the named point is outside the band");
      }
    }
  });
}

test("the fixtures cover the cases the widget must get right", () => {
  const has = (f, pred) => epsilonDelta.cases.some((c) => c.f === f && pred(c));
  assert.ok(has("2*x - 1", (c) => !c.left.none));
  assert.ok(has("x^2", (c) => c.L === 4 && c.eps === 0.1 && c.left.delta !== c.right.delta));
  assert.ok(has("sqrt(x)", (c) => c.left.delta < c.right.delta));
  assert.ok(has("1/x", (c) => !c.left.none));
  assert.ok(has("x + sign(x)", (c) => c.left.none && !c.right.none));
  assert.ok(has("sin(1/x)", (c) => c.eps < 1 && c.left.none && c.right.none));
  assert.ok(has("1/x^2", (c) => c.left.none));
  assert.ok(has("x^2", (c) => c.L === 4.5 && c.left.none));
  assert.ok(has("1e7*x", (c) => c.left.delta === 5e-8), "a δ far below 10⁻⁶ of the width (review F1)");
  assert.ok(epsilonDelta.cases.filter((c) => c.a >= 100000).length >= 20, "the cases translated to a large a (review F2)");
  assert.ok(epsilonDelta.cases.some((c) => c.source.startsWith("templates/topic.md:")), "the template's figure");
});

test("offsets: increasing, in (0, reach], reaching down to reach·10⁻¹²", () => {
  const us = offsets(2);
  assert.ok(us.every((u, i) => u > 0 && u <= 2 && (i === 0 || u > us[i - 1])));
  assert.equal(us[us.length - 1], 2);
  assert.ok(us[0] <= 2e-12 * 1.0001);
});

test("floorSignificant rounds down to 6 significant digits", () => {
  const cases = [[0.024845673131659, 0.0248456], [0.04, 0.04], [1, 1], [123.4567891, 123.456], [2.5e-7, 2.5e-7], [0, 0], [-1, 0],
    [5.00000000000291e-8, 5e-8], [5.0000000000008205e-21, 5e-21], [5e-324, 0]];
  for (const [v, r] of cases) assert.equal(floorSignificant(v), r, String(v));
  for (let k = 0; k < 2000; k++) {
    const v = Math.exp(30 * Math.random() - 15);
    const r = floorSignificant(v);
    assert.ok(r <= v && r >= v * (1 - 1e-5), `${v} → ${r}`);
  }
});

test("spread keeps the ends and at most n items", () => {
  const items = Array.from({ length: 100 }, (_, i) => i);
  const s = spread(items, 5);
  assert.deepEqual(s, [0, 25, 50, 74, 99]);
  assert.deepEqual(spread([1, 2], 5), [1, 2]);
});

function allProblems(config) {
  const problems = configProblems(config);
  try {
    checkExpression(config.f, ["x"]);
  } catch (e) {
    problems.push(`f: ${e.message}`);
  }
  return problems;
}

for (const c of epsilonDeltaInvalid.cases) {
  test(`epsilon-delta config rule (shared with check_widgets.py): ${c.problem ?? "a valid config"}`, () => {
    const problems = allProblems(c.config);
    if (c.problem === null) assert.deepEqual(problems, []);
    else assert.ok(problems.some((p) => p.includes(c.problem)), `expected ${JSON.stringify(c.problem)}, got ${JSON.stringify(problems)}`);
  });
}

// ── Regressions from the review of PR 10 ─────────────────────────────────────

const compiled = (src) => {
  const g = compileExpression(JXG, src, "x");
  return (x) => g(x);
};

test("F1: a δ far below 10⁻⁶ of the width is found, never rounded to 'none'", () => {
  for (const [src, exact] of [["1e7*x", 5e-8], ["1e20*x", 5e-21]]) {
    const r = largestDelta(compiled(src), { a: 0, L: 0, eps: 0.5, reach: [1, 1] });
    assert.equal(r.status, "found", src);
    assert.ok(r.delta <= exact && r.delta >= exact * (1 - tolerance), `${src}: ${r.delta}`);
    assert.ok(checkDelta(compiled(src), { a: 0, L: 0, eps: 0.5, delta: r.delta }).works);
  }
});

test("F2: the window is measured on the double x, not on the offset u (10*(x-100) at a = 100)", () => {
  const f = compiled("10*(x-100)");
  const c = { a: 100, L: 0, eps: 0.03 };
  const r = largestDelta(f, { ...c, reach: [1, 1] });
  assert.equal(r.status, "found");
  assert.equal(r.left.delta, 0.003);
  assert.equal(r.right.delta, 0.003);
  // The point 99.997 is 0.0030000000000001137 from a: outside the open window of δ = 0.003.
  assert.ok(checkDelta(f, { ...c, delta: 0.003 }).works);
  for (const side of [-1, 1]) {
    for (const p of windowPoints(c.a, side, 0.003)) assert.ok(p.d > 0 && p.d < 0.003 && p.d === side * (p.x - c.a));
  }
});

test("F2: f is never evaluated at x = a ((x-100000)/(x-100000) at a = 100000)", () => {
  const seen = [];
  const g = compiled("(x-100000)/(x-100000)");
  const f = (x) => {
    seen.push(x);
    return g(x);
  };
  const c = { a: 100000, L: 1, eps: 0.5 };
  const r = largestDelta(f, { ...c, reach: [1, 1] });
  assert.equal(r.status, "found");
  assert.ok(r.left.capped && r.right.capped);
  assert.ok(checkDelta(f, { ...c, delta: 0.5 }).works);
  assert.ok(seen.length > 1000 && !seen.includes(c.a));
  // Every point is a distinct double on its own side.
  for (const side of [-1, 1]) {
    const xs = windowPoints(c.a, side, 1e-9).map((p) => p.x);
    assert.equal(new Set(xs).size, xs.length);
    assert.ok(xs.every((x) => side * (x - c.a) > 0));
  }
});

test("F3: the reviewer's nine pockets: never 'none', and a re-check failure is never mistaken for one", () => {
  const cs = [0.8595, 0.8294165350000001, 0.819463008, 0.783405672, 0.75833604, 0.74923498, 0.731252384, 0.7085831880000001, 0.6766967649999999];
  const f = (x) => (x >= 0.9 || cs.some((c) => Math.abs(x - c) <= c * 1e-7) ? 2 : 0);
  const r = sideDelta(f, { a: 0, L: 0, eps: 1, side: 1, reach: 1 });
  const exact = Math.min(...cs.map((c) => c * (1 - 1e-7)));
  assert.notEqual(r.status, "none");
  assert.ok(r.rechecks <= METHOD.rechecks);
  if (r.status === "found") assert.ok(r.delta <= r.bound);
  else assert.ok(r.bound >= exact, "the bound is a point where f fails");
});

// An adversary that defeats every re-check: each new pocket is a single point of the re-check
// sample of the δ found so far. With k pockets the search needs k + 1 re-checks; it must find a
// δ while k < METHOD.rechecks and stop as "indeterminate" (not "none") when they run out. At
// the small scale the failures are still far from a (bound 10⁻⁴ ≫ near 10⁻¹²): a threshold
// that called them "none" would be wrong.
for (const scale of [1, 1e-4]) {
  test(`F3: the re-check budget is exactly METHOD.rechecks, and running out is 'indeterminate' (scale ${scale})`, () => {
    const pockets = new Set();
    const f = (x) => (x >= 0.9 * scale || pockets.has(x) ? 2 : 0);
    const opts = { a: 0, L: 0, eps: 1, side: 1, reach: 1 };
    for (let k = 0; k <= METHOD.rechecks; k++) {
      const r = sideDelta(f, opts);
      if (k < METHOD.rechecks) {
        assert.equal(r.status, "found", `${k} pockets`);
        assert.equal(r.rechecks, k, `${k} pockets need ${k + 1} re-checks`);
        assert.ok(r.delta <= 0.9 * scale && [...pockets].every((p) => r.delta <= p), "below every pocket");
        assert.ok(checkDelta(f, { a: 0, L: 0, eps: 1, delta: r.delta }).works);
        const pts = windowPoints(0, 1, r.delta);
        pockets.add(pts[pts.length - 1].x); // the re-check point closest to δ
      } else {
        assert.equal(r.status, "indeterminate", `${k} pockets`);
        assert.equal(r.reason, "rechecks");
        assert.equal(r.rechecks, METHOD.rechecks);
        assert.equal(r.bound, Math.min(...pockets), "the bound is the closest failure seen");
        assert.ok(r.bound > r.near);
      }
    }
  });
}

test("F4 (known limitation): a pocket thinner than the samples is missed, and the result says only what was checked", () => {
  // f = 2 on |x − 0.49901| < 10⁻⁸ and for x ≥ 0.4998: the pocket lies inside the window of
  // the δ found. Sampling cannot see it; widgets/epsilon-delta.mjs words the result as "the
  // largest δ the widget found (checked at N points)" and never says that smaller δ work.
  const f = compiled("1-sign(abs(x-0.49901)-1e-8)+1+sign(x-0.4998)");
  const r = largestDelta(f, { a: 0, L: 0, eps: 1, reach: [1, 1] });
  assert.equal(r.status, "found");
  assert.equal(r.right.delta, 0.4998);
  assert.equal(f(0.49901), 2, "f fails inside the window");
  assert.ok(r.right.checked > 1000);
});

test("undefined points count as failures (sqrt(x) at a = 0.04: undefined for x < 0)", () => {
  const f = compiled("sqrt(x)");
  const r = sideDelta(f, { a: 0.04, L: 0.2, eps: 0.3, side: -1, reach: 0.14 });
  assert.equal(r.status, "found");
  assert.equal(r.delta, 0.04);
  const v = checkDelta(f, { a: 0.04, L: 0.2, eps: 0.3, delta: 0.07 });
  assert.ok(!v.works && v.left.length && v.left.every((p) => Number.isNaN(p.y)));
});

test("too few doubles in the window is 'indeterminate', with the failure seen as the bound", () => {
  // At a = 10¹⁵ the doubles are 0.125 apart: a boundary at distance 10 leaves 80 of them, fewer
  // than METHOD.minPoints, and the points closest to a pass, so it is not "none" either.
  const r = sideDelta((x) => (x - 1e15 < 10 ? 0 : 2), { a: 1e15, L: 0, eps: 1, side: 1, reach: 1000 });
  assert.equal(r.status, "indeterminate");
  assert.equal(r.reason, "resolution");
  assert.ok(r.bound >= 10 && r.bound <= 10.125);
});

test("ceilSignificant rounds up, for 'at most' bounds", () => {
  for (const [v, r] of [[0.7085831880000001, 0.708584], [0.05, 0.05], [1e-12, 1e-12], [2.220446049250313e-12, 2.3e-12]]) {
    assert.equal(ceilSignificant(v, r === 2.3e-12 ? 2 : 6), r, String(v));
  }
  for (let k = 0; k < 2000; k++) {
    const v = Math.exp(30 * Math.random() - 15);
    const r = ceilSignificant(v);
    assert.ok(r >= v && r <= v * (1 + 1e-5), `${v} → ${r}`);
  }
});
