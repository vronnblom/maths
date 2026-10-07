// Shared widget controls (docs/plan/05 §5.8, 12 R12): native HTML range inputs and buttons,
// which are keyboard-operable as they are (Tab to focus; arrow keys, Page Up/Down, Home/End),
// labelled, and announced with their value. Widgets render inside the theme's shadow root, so
// the page's CSS does not reach them; STYLES is put into the widget with a <style> element.
// Colours come from the inherited text colour or from colours.mjs, so both themes work.

import { formatNumber } from "./plot.mjs";

export const STYLES = `
.mp-widget { font: inherit; color: inherit; }
.mp-board { width: 100%; border-radius: 4px; touch-action: pan-y; }
.mp-board:focus-visible, .mp-widget input:focus-visible, .mp-widget button:focus-visible {
  outline: 2px solid currentColor; outline-offset: 2px;
}
.mp-controls { display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; align-items: center; margin: 0.5rem 0; }
.mp-slider { display: flex; align-items: center; gap: 0.5rem; }
.mp-slider label { font-style: italic; min-width: 1.5em; }
.mp-slider input { width: 9rem; accent-color: currentColor; }
.mp-slider output { font-variant-numeric: tabular-nums; min-width: 4.5em; }
.mp-buttons { display: flex; gap: 0.5rem; }
.mp-widget button {
  font: inherit; font-size: 0.875em; color: inherit; background: transparent;
  border: 1px solid currentColor; border-radius: 4px; padding: 0.15em 0.6em; cursor: pointer;
}
.mp-readout, .mp-view { margin: 0.25rem 0; font-variant-numeric: tabular-nums; }
.mp-view { font-size: 0.875em; }
.mp-table { border-collapse: collapse; margin: 0.5rem 0; font-variant-numeric: tabular-nums; }
.mp-table caption { text-align: left; font-size: 0.875em; padding-bottom: 0.25rem; }
.mp-table th, .mp-table td { border: 1px solid currentColor; padding: 0.15em 0.75em; text-align: right; }
.mp-table th { font-weight: 600; font-style: italic; }
.mp-message { margin: 0.5rem 0; font-size: 0.875em; }
@media (max-width: 30rem) { .mp-slider input { width: 7rem; } }
`;

let counter = 0;

function el(doc, tag, props = {}, children = []) {
  const node = doc.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else node.setAttribute(k, v);
  }
  for (const c of children) node.append(c);
  return node;
}

/**
 * A labelled slider for `name` (rendered in italics, like a variable). Calls onInput(value)
 * as it moves. Returns {element, input, set(value)}.
 */
export function slider(doc, { name, min, max, step, value, onInput, describe = (v) => `${name} = ${formatNumber(v)}` }) {
  const id = `mp-slider-${++counter}`;
  const input = el(doc, "input", { id, type: "range", min, max, step, value });
  const output = el(doc, "output", { for: id, text: formatNumber(value) });
  const element = el(doc, "div", { class: "mp-slider" }, [el(doc, "label", { for: id, text: name }), input, output]);
  const show = (v) => {
    output.textContent = formatNumber(v);
    input.setAttribute("aria-valuetext", describe(v));
  };
  show(value);
  input.addEventListener("input", () => {
    const v = Number(input.value);
    show(v);
    onInput(v);
  });
  return {
    element,
    input,
    set(v) {
      input.value = String(v);
      show(v);
    },
  };
}

export function button(doc, label, onClick) {
  const b = el(doc, "button", { type: "button", text: label });
  b.addEventListener("click", onClick);
  return b;
}

/** A real <table> of values with a caption and column headers. Returns {element, update(rows)}. */
export function valueTable(doc, { caption, xName, yName }) {
  const body = el(doc, "tbody");
  const head = el(doc, "thead", {}, [
    el(doc, "tr", {}, [el(doc, "th", { scope: "col", text: xName }), el(doc, "th", { scope: "col", text: yName })]),
  ]);
  const element = el(doc, "table", { class: "mp-table" }, [el(doc, "caption", { text: caption }), head, body]);
  return {
    element,
    update(rows) {
      body.replaceChildren(
        ...rows.map((r) => el(doc, "tr", {}, [el(doc, "td", { text: formatNumber(r.x) }), el(doc, "td", { text: formatNumber(r.y) })])),
      );
    },
  };
}

export { el };
