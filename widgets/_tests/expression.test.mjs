// widgets/_lib/expression.mjs: the allowlist in front of JessieCode, and JessieCode's values
// against SymPy (fixtures/function-plot.json, "expressions").
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { CONSTANTS, ExpressionError, FUNCTIONS, checkExpression, compileExpression, tokenize } from "../_lib/expression.mjs";
import { JXG, close, fixtures } from "./helpers.mjs";

const schema = JSON.parse(readFileSync(new URL("../../schema/widgets/function-plot.schema.json", import.meta.url), "utf8"));

test("the allowlists equal the schema's $defs (scripts/check_widgets.py reads those)", () => {
  assert.deepEqual(FUNCTIONS, schema.$defs.functions.enum);
  assert.deepEqual(Object.keys(CONSTANTS), schema.$defs.constants.enum);
});

for (const c of fixtures.expressions) {
  test(`JessieCode agrees with SymPy: ${c.f}`, () => {
    const f = compileExpression(JXG, c.f, c.variable, Object.keys(c.params));
    c.points.forEach((x, i) => {
      const y = f(x, c.params);
      assert.ok(close(y, c.values[i]), `${c.f} at ${c.variable} = ${x}: got ${y}, SymPy ${c.values[i]}`);
    });
  });
}

test("tokens keep their positions", () => {
  assert.deepEqual(tokenize(" 2*x^-1.5e3"), [
    { type: "num", value: "2", pos: 1 },
    { type: "op", value: "*", pos: 2 },
    { type: "name", value: "x", pos: 3 },
    { type: "op", value: "^", pos: 4 },
    { type: "op", value: "-", pos: 5 },
    { type: "num", value: "1.5e3", pos: 6 },
  ]);
});

test("pi and e are translated for JessieCode, everything else passes through", () => {
  assert.equal(checkExpression("e^(pi*x)", ["x"]), "EULER ^ ( PI * x )");
});

test("what JessieCode alone would accept silently is rejected before it", () => {
  // JessieCode returns its argument for an unknown function (sec(x) is x), undefined for an
  // unknown name, and compiles `2x` to a no-op; each of these must be an error instead.
  for (const [src, message] of [
    ["sec(x)", /unknown name sec/],
    ["a*x", /unknown name a/],
    ["2x", /missing \* after 2/],
    ["x;1", /unexpected character ";"/],
    ["X(1)", /unknown name X/],
    ["window", /unknown name window/],
    ["", /empty/],
  ]) {
    assert.throws(() => compileExpression(JXG, src, "x"), (e) => e instanceof ExpressionError && message.test(e.message), src);
  }
});

test("values that are not finite numbers become NaN", () => {
  const f = compileExpression(JXG, "1/x + sqrt(x)", "x");
  assert.ok(Number.isNaN(f(0)));
  assert.ok(Number.isNaN(f(-1)));
  assert.equal(f(1), 2);
});

test("parameters are passed by name", () => {
  const f = compileExpression(JXG, "a*x + b", "x", ["a", "b"]);
  assert.equal(f(2, { a: 3, b: -1 }), 5);
  assert.equal(f(2, { b: -1, a: 3 }), 5);
});
