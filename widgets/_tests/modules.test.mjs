// The module rules of docs/plan/05 §5.8: no static https: import anywhere (Node refuses them,
// so the tests could not import the widget); the maths modules in _lib/ touch neither the DOM
// nor a global JSXGraph; one exact JSXGraph version everywhere; every widget has a schema and
// a catalogue entry; and a widget module imports in Node and exports render().
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";

import { JSXGRAPH_URL, JSXGRAPH_VERSION } from "../_lib/jsxgraph.mjs";
import { JXG } from "./helpers.mjs";

const read = (rel) => readFileSync(new URL(rel, import.meta.url), "utf8");
const strip = (src) => src.replace(/\/\*[\s\S]*?\*\//g, "").replace(/(^|[^:])\/\/.*$/gm, "$1");
const modules = (dir) => readdirSync(new URL(dir, import.meta.url)).filter((f) => f.endsWith(".mjs")).map((f) => dir + f);
const ALL = [...modules("../"), ...modules("../_lib/"), ...modules("../../plugins/"), ...modules("../../plugins/_lib/")];
const PURE = ["../_lib/expression.mjs", "../_lib/plot.mjs", "../_lib/epsdelta.mjs", "../_lib/jsxgraph.mjs"];
const widgets = modules("../").map((f) => f.slice(3, -4));

test("no module imports an https: URL statically", () => {
  for (const file of ALL) {
    const src = strip(read(file));
    assert.doesNotMatch(src, /^\s*import\b[^;]*?["']https?:/m, file);
    assert.doesNotMatch(src, /^\s*export\b[^;]*?\bfrom\s*["']https?:/m, file);
  }
});

test("JSXGraph is loaded only by a dynamic import of JSXGRAPH_URL, inside a widget's render()", () => {
  for (const file of ALL) {
    const src = strip(read(file));
    const isWidget = /^\.\.\/[\w-]+\.mjs$/.test(file);
    for (const d of src.match(/\bimport\([^)]*\)/g) ?? []) {
      assert.ok(isWidget && d === "import(JSXGRAPH_URL)", `${file}: ${d}`);
    }
    if (file !== "../_lib/jsxgraph.mjs") assert.doesNotMatch(src, /https?:\/\/(cdn\.jsdelivr|unpkg)/, file);
  }
});

test("the maths modules in _lib/ are pure: no DOM, no global JSXGraph, no imports from outside _lib/", () => {
  for (const file of PURE) {
    const src = strip(read(file));
    assert.doesNotMatch(src, /\b(document|window|globalThis|navigator|localStorage)\b/, file);
    assert.doesNotMatch(src, /\bimport\(/, file);
    for (const m of src.matchAll(/^\s*import\b[^;]*?from\s*["']([^"']+)["']/gm)) assert.match(m[1], /^\.\/[\w-]+\.mjs$/, file);
  }
});

test("one exact JSXGraph version: the CDN URL and the devDependency the tests use", () => {
  const pkg = JSON.parse(read("../../package.json"));
  assert.equal(pkg.devDependencies.jsxgraph, JSXGRAPH_VERSION, "exact, no ^ or ~");
  assert.ok(JSXGRAPH_URL.includes(`jsxgraph@${JSXGRAPH_VERSION}/`));
  assert.equal(JXG.version, JSXGRAPH_VERSION, "node_modules has the pinned version (run npm ci)");
});

test("every widget has a schema and an entry in widgets/README.md", () => {
  const readme = read("../README.md");
  for (const w of widgets) {
    assert.doesNotThrow(() => read(`../../schema/widgets/${w}.schema.json`), `schema/widgets/${w}.schema.json`);
    assert.match(readme, new RegExp(`^### \`${w}\``, "m"), `widgets/README.md has no ### \`${w}\``);
  }
});

for (const w of widgets) {
  test(`${w}.mjs imports in Node and has the anywidget contract`, async () => {
    const mod = await import(`../${w}.mjs`);
    assert.equal(typeof mod.default.render, "function");
  });
}

for (const w of widgets) {
  test(`${w} reads every key of its schema from the model`, async () => {
    const { KEYS, readConfig } = await import(`../${w}.mjs`);
    const schema = JSON.parse(read(`../../schema/widgets/${w}.schema.json`));
    assert.deepEqual([...KEYS].sort(), Object.keys(schema.properties).sort());
    const config = { f: "x", xRange: [0, 1], yRange: [0, 1] };
    const model = { get: (k) => config[k] };
    assert.deepEqual(readConfig(model), config);
  });
}

test("every widget schema allows the same functions and constants (expression.mjs has one list)", () => {
  const defs = (w) => JSON.parse(read(`../../schema/widgets/${w}.schema.json`)).$defs;
  for (const w of widgets) {
    assert.deepEqual(defs(w).functions.enum, defs("function-plot").functions.enum, w);
    assert.deepEqual(defs(w).constants.enum, defs("function-plot").constants.enum, w);
  }
});
