// widgets/_lib/plot.mjs against SymPy (fixtures/function-plot.json): the table of values of
// every function-plot figure on the site, the value at a hole, and sampling with breaks at poles
// and jumps; plus the number format and the semantic config rules.
import { test } from "node:test";
import assert from "node:assert/strict";

import { checkExpression, compileExpression } from "../_lib/expression.mjs";
import { configProblems, formatNumber, holeValue, parseDisplayed, sample, tableRows } from "../_lib/plot.mjs";
import { JXG, close, fixtures, invalid } from "./helpers.mjs";

for (const c of fixtures.tables) {
  test(`table of values matches SymPy: ${c.source} (${c.setting})`, () => {
    const g = compileExpression(JXG, c.f, c.variable, Object.keys(c.params));
    const rows = tableRows((x) => g(x, c.params), c.points, { holeX: c.holeX });
    rows.forEach((r, i) => {
      assert.equal(r.x, c.points[i]);
      assert.ok(close(r.y, c.values[i]), `${c.f} at ${r.x}: got ${r.y}, SymPy ${c.values[i]}`);
    });
  });
}

for (const c of fixtures.holes) {
  test(`hole: ${c.f} at ${c.variable} = ${c.x}`, () => {
    const g = compileExpression(JXG, c.f, c.variable);
    if (c.error) {
      assert.throws(() => holeValue(g, c.x, c.scale), RangeError, `SymPy: ${c.sympy}`);
    } else {
      const y = holeValue(g, c.x, c.scale);
      assert.ok(close(y, c.y, 1e-7), `got ${y}, SymPy ${c.y}`);
    }
  });
}

for (const c of fixtures.samples) {
  test(`sampling ${c.f} on [${c.a}, ${c.b}]: grid values and breaks`, () => {
    const g = compileExpression(JXG, c.f, "x");
    const { xs, ys } = sample(g, c.a, c.b, { n: c.n, jump: c.jump });
    const step = (c.b - c.a) / c.n;
    const gridX = (k) => (k === c.n ? c.b : c.a + ((c.b - c.a) * k) / c.n); // as sample() computes it
    const grid = [];
    const inserted = [];
    xs.forEach((x, i) => {
      if (grid.length <= c.n && x === gridX(grid.length)) grid.push(ys[i]);
      else inserted.push({ x, y: ys[i] });
    });
    assert.equal(grid.length, c.n + 1, "every grid point is sampled, in order");
    grid.forEach((y, k) => assert.ok(close(y, c.values[k]), `${c.f} at grid point ${k}: got ${y}, SymPy ${c.values[k]}`));
    for (const p of inserted) {
      assert.ok(Number.isNaN(p.y), "an inserted point is a break");
      assert.ok(c.breaks.some((b) => Math.abs(b - p.x) <= step), `a break at ${p.x}, where SymPy finds f continuous`);
    }
    // Every discontinuity SymPy finds cuts the curve: a NaN within one step of it.
    for (const b of c.breaks) {
      assert.ok(xs.some((x, i) => Number.isNaN(ys[i]) && Math.abs(x - b) <= step), `no break near ${b}`);
    }
  });
}

test("sampling leaves out an excluded point (a hole)", () => {
  const { xs, ys } = sample((x) => x, -1, 1, { n: 4, exclude: [0] });
  assert.deepEqual(xs, [-1, -0.5, 0, 0.5, 1]);
  assert.ok(Number.isNaN(ys[2]));
});

test("the table leaves the hole undefined", () => {
  const rows = tableRows((x) => x + 1, [0, 1], { holeX: 0 });
  assert.ok(Number.isNaN(rows[0].y));
  assert.equal(rows[1].y, 2);
});

test("number format", () => {
  const cases = [
    [0, "0"], [10, "10"], [10.005, "10.005"], [0.479425538604203, "0.479426"], [-0.5, "−0.5"],
    [9.995000000000001, "9.995"], [1234567, "1.23457×10⁶"], [-0.0000012, "−0.0000012"], [1.2e-8, "1.2×10⁻⁸"],
    [NaN, "undefined"],
  ];
  for (const [v, s] of cases) {
    assert.equal(formatNumber(v), s, String(v));
    if (Number.isFinite(v)) assert.ok(close(parseDisplayed(s), v, 1e-5), s);
  }
  assert.ok(Number.isNaN(parseDisplayed("undefined")));
});

function allProblems(config) {
  const params = Object.keys(config.parameters ?? {});
  const problems = configProblems(config);
  try {
    checkExpression(config.f, [config.variable ?? "x", ...params]);
  } catch (e) {
    problems.push(`f: ${e.message}`);
  }
  return problems;
}

for (const c of invalid.cases) {
  test(`config rule (shared with check_widgets.py): ${c.problem ?? "a valid config"}`, () => {
    const problems = allProblems(c.config);
    if (c.problem === null) assert.deepEqual(problems, []);
    else assert.ok(problems.some((p) => p.includes(c.problem)), `expected ${JSON.stringify(c.problem)}, got ${JSON.stringify(problems)}`);
  });
}
