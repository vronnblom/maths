// Shared by the widget tests: the fixtures, and JSXGraph from the npm devDependency. That is
// the same file, at the same exact version, that widgets load from jsDelivr inside render()
// (modules.test.mjs checks the versions), so the tests run the browser's JessieCode. The
// package's `exports` map hides distrib/, hence the relative file path.
import { readFileSync } from "node:fs";

export const { default: JXG } = await import(new URL("../../node_modules/jsxgraph/distrib/jsxgraphcore.mjs", import.meta.url));

export const fixtures = JSON.parse(readFileSync(new URL("./fixtures/function-plot.json", import.meta.url), "utf8"));
export const invalid = JSON.parse(readFileSync(new URL("./fixtures/function-plot-invalid.json", import.meta.url), "utf8"));

/** |actual − expected| ≤ rel·max(1, |expected|); null in a fixture means "undefined" (NaN). */
export function close(actual, expected, rel = 1e-9) {
  if (expected === null) return Number.isNaN(actual);
  return Math.abs(actual - expected) <= rel * Math.max(1, Math.abs(expected));
}
