// Theme-aware colours for widgets (docs/plan/05 §5.8, 12 R12). The book-theme switches the
// colour scheme with a `dark` (or `light`) class on <html>; its backgrounds are #ffffff and
// #1c1917 (stone-900, measured on the pinned theme commit). widgets/_tests/colours.test.mjs
// checks every colour that carries meaning against its background: at least 3:1 for lines and
// points (WCAG 1.4.11), 4.5:1 for text. Meaning never rests on colour alone: the hole is an
// open circle, the traced point a filled one, the ε-band has dashed edges and the δ-window
// solid ones, a failing point is a cross, and every value is also in text.

export const PALETTES = {
  light: {
    background: "#ffffff",
    text: "#44403c", // the theme's body text
    axis: "#57534e",
    grid: "#e7e5e4", // decorative: exempt from the contrast rule
    curve: "#0b5cad",
    point: "#9a3412",
    band: "#0f766e", // the ε-band around L (its edges; the fill is translucent)
    window: "#6d28d9", // the δ-window around a
    bad: "#b91c1c", // points in the window but outside the band
  },
  dark: {
    background: "#1c1917",
    text: "#d6d3d1",
    axis: "#a8a29e",
    grid: "#3a3532",
    curve: "#54aeff",
    point: "#fb8f44",
    band: "#2dd4bf",
    window: "#b39dfa",
    bad: "#ff7b72",
  },
};

/** The colours that must contrast with the background, and the ratio each needs. */
export const CONTRAST_RULES = { text: 4.5, axis: 3, curve: 3, point: 3, band: 3, window: 3, bad: 3 };

function luminance(hex) {
  const n = parseInt(hex.slice(1), 16);
  const lin = (c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * lin((n >> 16) & 255) + 0.7152 * lin((n >> 8) & 255) + 0.0722 * lin(n & 255);
}

/** The WCAG 2 contrast ratio of two #rrggbb colours. */
export function contrastRatio(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

/** "dark" or "light": the theme's class on <html>, else the system preference. */
export function currentScheme(doc = globalThis.document) {
  const cls = doc.documentElement.classList;
  if (cls.contains("dark")) return "dark";
  if (cls.contains("light")) return "light";
  return doc.defaultView?.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

/** Call `onChange(scheme)` whenever the colour scheme changes. Returns a function that stops. */
export function watchScheme(onChange, doc = globalThis.document) {
  let scheme = currentScheme(doc);
  const check = () => {
    const now = currentScheme(doc);
    if (now !== scheme) {
      scheme = now;
      onChange(now);
    }
  };
  const observer = new doc.defaultView.MutationObserver(check);
  observer.observe(doc.documentElement, { attributes: true, attributeFilter: ["class"] });
  const media = doc.defaultView.matchMedia?.("(prefers-color-scheme: dark)");
  media?.addEventListener?.("change", check);
  return () => {
    observer.disconnect();
    media?.removeEventListener?.("change", check);
  };
}
