// Compile widget expressions with the browser's compiler (review of PR 10, F7): the allowlist in
// widgets/_lib/expression.mjs, then JSXGraph's JessieCode from the pinned npm devDependency
// (the same file, at the same version, that widgets load from jsDelivr). scripts/check_widgets.py
// runs this for every expression it accepts, so `npm run check` rejects what the widget could
// not compile (`sin()`, `x+`) instead of re-implementing JessieCode's grammar in Python.
//
//   echo '[{"f": "sin()", "variable": "x", "params": []}]' | node scripts/compile_expressions.mjs
//
// prints a JSON list with, for each expression, null (it compiles) or the error message.
import { readFileSync } from "node:fs";

import { compileExpression } from "../widgets/_lib/expression.mjs";

const { default: JXG } = await import(new URL("../node_modules/jsxgraph/distrib/jsxgraphcore.mjs", import.meta.url));

// JessieCode logs its warnings (with the code it failed to eval) to the console: keep stdout
// for the JSON answer.
console.log = console.info = console.warn = (...args) => process.stderr.write(`${args.join(" ")}\n`);

const items = JSON.parse(readFileSync(0, "utf8"));
const results = items.map(({ f, variable = "x", params = [] }) => {
  try {
    compileExpression(JXG, f, variable, params);
    return null;
  } catch (err) {
    return err.message;
  }
});
process.stdout.write(`${JSON.stringify(results)}\n`);
