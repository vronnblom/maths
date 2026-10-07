// widgets/_lib/epsdelta.mjs against SymPy (fixtures/epsilon-delta.json): the largest δ on each
// side never exceeds the exact value and is within the fixture's tolerance of it; "no δ" is
// reported exactly where SymPy finds none; the reported δ passes the reader's check and a
// slightly larger one fails; plus the rounding and the config rules shared with
// scripts/check_widgets.py.
import { test } from "node:test";
import assert from "node:assert/strict";

import { checkExpression, compileExpression } from "../_lib/expression.mjs";
import { checkDelta, configProblems, floorSignificant, largestDelta, offsets, spread } from "../_lib/epsdelta.mjs";
import { JXG, epsilonDelta, epsilonDeltaInvalid } from "./helpers.mjs";

const { tolerance } = epsilonDelta;

for (const c of epsilonDelta.cases) {
  const g = compileExpression(JXG, c.f, "x");
  const f = (x) => g(x);
  const [x0, x1] = c.xRange;
  const reach = [c.a - x0, x1 - c.a];
  const result = largestDelta(f, { a: c.a, L: c.L, eps: c.eps, reach, width: x1 - x0 });

  test(`largest δ matches SymPy: ${c.f} at a = ${c.a}, L = ${c.L}, ε = ${c.eps} (${c.case})`, () => {
    for (const [name, exact, got] of [["left", c.left, result.left], ["right", c.right, result.right]]) {
      const where = `${name}: got ${JSON.stringify(got)}, SymPy ${JSON.stringify(exact)}`;
      assert.equal(got.none, exact.none, `"no δ" disagrees, ${where}`);
      if (exact.none) continue;
      assert.ok(got.delta <= exact.delta, `over-reported, ${where}`);
      assert.ok(got.delta >= exact.delta * (1 - tolerance), `more than ${tolerance} below, ${where}`);
      assert.equal(got.capped, exact.capped, `capped disagrees, ${where}`);
    }
    assert.equal(result.none, c.left.none || c.right.none);
    if (!result.none) assert.equal(result.delta, Math.min(result.left.delta, result.right.delta));
  });

  test(`the reader's check agrees: ${c.f} at a = ${c.a}, L = ${c.L}, ε = ${c.eps}`, () => {
    const check = (delta) => checkDelta(f, { a: c.a, L: c.L, eps: c.eps, delta });
    if (!result.none) assert.ok(check(result.delta).works, `the reported δ = ${result.delta} fails`);
    // A δ just too large fails: by 0.1 % (one step of a slider) and by 10⁻⁶ (relative).
    for (const [name, side] of [["left", c.left], ["right", c.right]]) {
      const deltas = side.none ? [Math.min(...reach) / 2] : [side.delta * 1.001, side.delta * (1 + 1e-6)];
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
  assert.ok(epsilonDelta.cases.some((c) => c.source.startsWith("templates/topic.md:")), "the template's figure");
});

test("offsets: increasing, in (0, reach], reaching down to reach·10⁻¹²", () => {
  const us = offsets(2);
  assert.ok(us.every((u, i) => u > 0 && u <= 2 && (i === 0 || u > us[i - 1])));
  assert.equal(us[us.length - 1], 2);
  assert.ok(us[0] <= 2e-12 * 1.0001);
});

test("floorSignificant rounds down to 6 significant digits", () => {
  const cases = [[0.024845673131659, 0.0248456], [0.04, 0.04], [1, 1], [123.4567891, 123.456], [2.5e-7, 2.5e-7], [0, 0], [-1, 0]];
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
