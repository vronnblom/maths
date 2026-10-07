// The sentences of widgets/epsilon-delta.mjs (review of PR 10, F1, F4, F8): every one must be
// true for every config that check_widgets.py accepts. So a δ is "the largest δ the widget
// found (checked at N points)", never "the largest δ", and nothing says that every smaller δ
// works; "no δ observed" says what was seen, and the mathematics only conditionally; the widget
// never gives "the limit is (not) L" as a verdict; it never promises crosses it cannot draw.
import { test } from "node:test";
import assert from "node:assert/strict";

import { compileExpression } from "../_lib/expression.mjs";
import { checkDelta, largestDelta, sideDelta } from "../_lib/epsdelta.mjs";
import { largestText, verdictText } from "../epsilon-delta.mjs";
import { JXG, epsilonDelta } from "./helpers.mjs";

const compiled = (src) => {
  const g = compileExpression(JXG, src, "x");
  return (x) => g(x);
};

// What no sentence may say.
const FORBIDDEN = [
  [/(every|any|all) smaller δ/, "claims that smaller δ work"],
  [/the largest δ is\b/, "states the largest δ as a fact"],
  [/(?<!then \S+ )is not the limit|the limit (of f\(x\) as x → \S+ )?is\b/, "a verdict on the limit"],
  [/no δ works for this ε, which/, "states that no δ exists"],
  [/\bclearly\b|\bobviously\b/i, "house style"],
];

function allowed(text) {
  for (const [re, why] of FORBIDDEN) assert.doesNotMatch(text, re, `${why}: ${text}`);
  if (/is not the limit/.test(text)) assert.match(text, /If no δ works for this ε, then \S+ is not the limit/, text);
}

for (const c of epsilonDelta.cases) {
  test(`the sentences are allowed: ${c.f} at a = ${c.a}, ε = ${c.eps}`, () => {
    const f = compiled(c.f);
    const reach = [c.a - c.xRange[0], c.xRange[1] - c.a];
    const result = largestDelta(f, { a: c.a, L: c.L, eps: c.eps, reach });
    const text = largestText(result, { eps: c.eps, a: c.a, L: c.L });
    allowed(text);
    for (const side of [result.left, result.right]) {
      if (side.status === "found" && !side.capped) assert.match(text, /the largest δ the widget found is \S+ \(checked at [\d,]+ points\)/);
      if (side.status === "none") assert.match(text, /no δ observed: f(\(x\) leaves the band| is undefined) at points within/);
    }
    if (result.status === "none") assert.match(text, /If no δ works for this ε, then \S+ is not the limit/);
    for (const delta of [result.delta, Math.min(...reach) / 2].filter((d) => d > 0)) {
      allowed(verdictText(checkDelta(f, { a: c.a, L: c.L, eps: c.eps, delta }), { delta, eps: c.eps, a: c.a, L: c.L }));
    }
  });
}

test("F1: a tiny δ is shown as found, in scientific notation, with no claim about the limit", () => {
  const result = largestDelta(compiled("1e7*x"), { a: 0, L: 0, eps: 0.5, reach: [1, 1] });
  const text = largestText(result, { eps: 0.5, a: 0, L: 0 });
  assert.match(text, /the largest δ the widget found for both sides is 5×10⁻⁸\./);
  assert.doesNotMatch(text, /no δ|not the limit/);
});

test("F4: a δ that misses a thin pocket is only 'the largest δ the widget found (checked at N points)'", () => {
  const f = compiled("1-sign(abs(x-0.49901)-1e-8)+1+sign(x-0.4998)");
  const result = largestDelta(f, { a: 0, L: 0, eps: 1, reach: [1, 1] });
  const text = largestText(result, { eps: 1, a: 0, L: 0 });
  allowed(text);
  assert.match(text, /on the right, the largest δ the widget found is 0\.4998 \(checked at [\d,]+ points\)/);
  const v = verdictText(checkDelta(f, { a: 0, L: 0, eps: 1, delta: 0.4998 }), { delta: 0.4998, eps: 1, a: 0, L: 0 });
  assert.match(v, /works: every x the widget checked with 0 < \|x − 0\| < 0\.4998/);
});

test("no δ observed: what was seen, then the mathematics conditionally", () => {
  const text = largestText(largestDelta(compiled("x + sign(x)"), { a: 0, L: 1, eps: 0.5, reach: [2, 2] }), { eps: 0.5, a: 0, L: 1 });
  assert.match(text, /on the left, no δ observed: f\(x\) leaves the band at points within 2×10⁻¹² of 0/);
  assert.match(text, /So the widget observed no δ that works for this ε\. If no δ works for this ε, then 1 is not the limit of f\(x\) as x → 0\.$/);
  // Owner decision 1: where f is undefined, the text says so.
  const sqrt = largestText(largestDelta(compiled("sqrt(x)"), { a: 0, L: 0, eps: 0.5, reach: [1, 1] }), { eps: 0.5, a: 0, L: 0 });
  assert.match(sqrt, /on the left, no δ observed: f is undefined at points within 1×10⁻¹² of 0/);
});

test("indeterminate: the observed bound, rounded up, and no verdict", () => {
  const cs = [0.8595, 0.8294165350000001, 0.819463008, 0.783405672, 0.75833604, 0.74923498, 0.731252384, 0.7085831880000001, 0.6766967649999999];
  const f = (x) => (x >= 0.9 || cs.some((c) => Math.abs(x - c) <= c * 1e-7) ? 2 : 0);
  const result = largestDelta(f, { a: 0, L: 0, eps: 1, reach: [1, 1] });
  assert.equal(result.status, "indeterminate");
  const text = largestText(result, { eps: 1, a: 0, L: 0 });
  allowed(text);
  assert.match(text, /on the right, the widget could not settle the largest δ: f\(x\) leaves the band at x ≈ \S+, so a δ that works is at most (\S+), but each smaller δ the widget tried failed its re-check/);
  const shown = Number(/at most (\S+),/.exec(text)[1]);
  assert.ok(shown >= result.right.bound, "an 'at most' bound is rounded up");
  assert.match(text, /So the widget could not settle the largest δ for this ε\.$/);
  const r = sideDelta((x) => (x - 1e15 < 10 ? 0 : 2), { a: 1e15, L: 0, eps: 1, side: 1, reach: 1000 });
  allowed(largestText({ left: r, right: r, status: "indeterminate" }, { eps: 1, a: 1e15, L: 0 }));
});

test("F8: no crosses are promised where f is undefined (sqrt(x) at a = 0.04, δ = 0.07)", () => {
  const c = { a: 0.04, L: 0.2, eps: 0.3, delta: 0.07 };
  const check = checkDelta(compiled("sqrt(x)"), c);
  const text = verdictText(check, c);
  assert.match(text, /^Your δ = 0\.07 fails: f is undefined at x ≈ −0\.0\d+, in the window\. A point where f is undefined counts as a failure; the graph has no point there to mark\.$/);
  assert.doesNotMatch(text, /cross/);
  // Finite failures are marked, and the text says so.
  const x2 = { a: 2, L: 4, eps: 0.1, delta: 1.5 };
  assert.match(verdictText(checkDelta(compiled("x^2"), x2), x2), /fails: at x ≈ \S+, f\(x\) ≈ \S+, which is not within 0\.1 of 4\. Points of the graph in the window but outside the band are marked with crosses\.$/);
  // Both: crosses for the graph, and the undefined points said in words.
  const both = { a: 0.04, L: 0.2, eps: 0.1, delta: 0.07 };
  const t = verdictText(checkDelta(compiled("sqrt(x)"), both), both);
  assert.match(t, /marked with crosses\. f is also undefined at some x in the window\. A point where f is undefined counts as a failure/);
});
