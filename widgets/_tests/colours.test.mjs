// widgets/_lib/colours.mjs (docs/plan/12 R12): every colour that carries meaning has enough
// contrast with its background, in the light and the dark scheme.
import { test } from "node:test";
import assert from "node:assert/strict";

import { CONTRAST_RULES, PALETTES, contrastRatio, currentScheme } from "../_lib/colours.mjs";

test("contrast ratio (WCAG 2)", () => {
  assert.equal(contrastRatio("#000000", "#ffffff"), 21);
  assert.equal(contrastRatio("#777777", "#777777"), 1);
});

for (const [scheme, palette] of Object.entries(PALETTES)) {
  for (const [role, minimum] of Object.entries(CONTRAST_RULES)) {
    test(`${scheme}: ${role} has contrast ≥ ${minimum}:1 with the background`, () => {
      const r = contrastRatio(palette[role], palette.background);
      assert.ok(r >= minimum, `${palette[role]} on ${palette.background}: ${r.toFixed(2)}:1`);
    });
  }
}

test("both schemes define the same colours", () => {
  assert.deepEqual(Object.keys(PALETTES.light).sort(), Object.keys(PALETTES.dark).sort());
});

test("the scheme follows the theme's class on <html>, then the system preference", () => {
  const doc = (classes, prefersDark) => ({
    documentElement: { classList: { contains: (c) => classes.includes(c) } },
    defaultView: { matchMedia: () => ({ matches: prefersDark }) },
  });
  assert.equal(currentScheme(doc(["dark"], false)), "dark");
  assert.equal(currentScheme(doc(["light"], true)), "light");
  assert.equal(currentScheme(doc([], true)), "dark");
  assert.equal(currentScheme(doc([], false)), "light");
});
