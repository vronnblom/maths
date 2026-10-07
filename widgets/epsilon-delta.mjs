// epsilon-delta: the ε–δ game for lim_{x→a} f(x) = L (docs/plan/05 §5.8; config:
// schema/widgets/epsilon-delta.schema.json; catalogue entry: widgets/README.md). The graph of f
// near a, the band |y − L| < ε, the window 0 < |x − a| < δ with x = a itself left out, an ε
// slider with the largest δ on each side, and a δ slider for the reader's own choice with a
// verdict. An anywidget module: mystmd publishes this file with a content hash, and `./_lib/`
// next to it through `project.static_files`.
//
// All the mathematics (the largest δ, the reader's check, the config rules) is in
// ./_lib/epsdelta.mjs, which widgets/_tests/ checks against SymPy. This file only draws.

import { JSXGRAPH_URL } from "./_lib/jsxgraph.mjs";
import { compileExpression } from "./_lib/expression.mjs";
import { formatNumber, sample } from "./_lib/plot.mjs";
import { METHOD, checkDelta, configProblems, largestDelta, spread } from "./_lib/epsdelta.mjs";
import { PALETTES, currentScheme, watchScheme } from "./_lib/colours.mjs";
import { STYLES, button, el, slider } from "./_lib/controls.mjs";
import { createBoard, freeBoard, visibleRange, zoomAbout } from "./_lib/board.mjs";

export const KEYS = ["f", "a", "L", "eps", "epsRange", "epsStep", "delta", "xRange", "yRange"];

/** The config from the anywidget model (the JSON body of the {anywidget} directive). */
export function readConfig(model) {
  const config = {};
  for (const key of KEYS) {
    const v = model.get(key);
    if (v !== undefined) config[key] = v;
  }
  return config;
}

// Failing points drawn as crosses, at most, on each side: one per 20 px of board, up to 40.
const marksPerSide = (width) => Math.max(8, Math.min(40, Math.round(width / 20)));
const CROSS_PX = 4; // half the size of a cross, in pixels

// A reported δ is rounded down to METHOD.digits significant digits; show all of them (one more
// than formatNumber's default could round up).
const showDelta = (d) => formatNumber(d, METHOD.digits + 1);

async function render({ model, el: host }) {
  const doc = host.ownerDocument;
  const root = el(doc, "div", { class: "mp-widget" }, [el(doc, "style", { text: STYLES })]);
  host.replaceChildren(root);
  const say = (text) => root.append(el(doc, "p", { class: "mp-message", role: "status", text }));

  const config = readConfig(model);
  const problems = configProblems(config);
  if (problems.length) {
    say(`This figure could not be drawn (${problems.join("; ")}). The caption describes it.`);
    return undefined;
  }

  let JXG;
  try {
    ({ default: JXG } = await import(JSXGRAPH_URL));
  } catch (err) {
    console.error("epsilon-delta: could not load JSXGraph", err);
    say("The interactive figure could not be loaded. The caption describes it.");
    return undefined;
  }
  // The theme may unmount this element while JSXGraph loads; it then never calls our cleanup.
  if (!host.isConnected) return undefined;

  let compiled;
  try {
    compiled = compileExpression(JXG, config.f, "x");
  } catch (err) {
    say(`This figure could not be drawn (${err.message}). The caption describes it.`);
    return undefined;
  }
  const f = (x) => compiled(x);
  const { a, L } = config;
  const [x0, x1] = config.xRange;
  const [y0, y1] = config.yRange;
  const reach = [a - x0, x1 - a];
  const maxDelta = Math.min(...reach);
  const n = formatNumber;

  let eps = config.eps;
  let delta = config.delta ?? maxDelta / 2;
  let result = null; // largestDelta(): the largest δ on each side for this ε
  let check = null; // checkDelta(): the reader's δ
  let marks = []; // failing points to draw as crosses

  // ── Layout: board, legend, controls, the two verdicts ──
  const boardBox = el(doc, "div", { class: "mp-board" });
  const legend = el(doc, "p", {
    class: "mp-view",
    text:
      `Band (dashed edges): ${n(L)} − ε < y < ${n(L)} + ε. Window (solid edges): 0 < |x − ${n(a)}| < δ; ` +
      `the dotted line x = ${n(a)} is left out. Dotted ticks: the largest δ on each side. ` +
      "Crosses: points of the graph in the window but outside the band.",
  });
  const controls = el(doc, "div", { class: "mp-controls" });
  const largest = el(doc, "p", { class: "mp-readout", "aria-live": "polite" });
  const verdict = el(doc, "p", { class: "mp-readout", "aria-live": "polite" });
  root.append(boardBox, legend, controls, largest, verdict);

  const sideText = (side, name) => {
    if (side.none) return `on the ${name}, no δ works (f(x) leaves the band even within ${n(METHOD.noDelta * (x1 - x0), 2)} of ${n(a)})`;
    if (side.capped) return `on the ${name}, the largest δ is at least ${n(side.delta)} (the graph stays in the band to the edge of the view)`;
    return `on the ${name}, the largest δ is ${showDelta(side.delta)}`;
  };
  const showLargest = () => {
    const head = `For ε = ${n(eps)}: ${sideText(result.left, "left")}; ${sideText(result.right, "right")}. `;
    largest.textContent = result.none
      ? `${head}So no δ works for this ε, which shows that the limit of f(x) as x → ${n(a)} is not ${n(L)}: it is another number, or there is no limit.`
      : `${head}So δ = ${showDelta(result.delta)}, or any smaller δ, works on both sides.`;
  };
  const showVerdict = () => {
    const head = `Your δ = ${n(delta)}`;
    if (check.works) {
      verdict.textContent = `${head} works: every x the widget checked with 0 < |x − ${n(a)}| < ${n(delta)} has |f(x) − ${n(L)}| < ${n(eps)}.`;
      return;
    }
    const w = check.witness;
    const where = Number.isFinite(w.y)
      ? `at x ≈ ${n(w.x)}, f(x) ≈ ${n(w.y)}, which is not within ${n(eps)} of ${n(L)}`
      : `f is undefined at x ≈ ${n(w.x)}`;
    const count = check.left.length + check.right.length;
    verdict.textContent = `${head} fails: ${where}. ${count === 1 ? "That point is" : "Such points are"} marked with crosses.`;
  };

  const compute = () => {
    result = largestDelta(f, { a, L, eps, reach, width: x1 - x0 });
  };
  const judge = () => {
    check = checkDelta(f, { a, L, eps, delta });
    const finite = (ps) => ps.filter((p) => Number.isFinite(p.y));
    const most = marksPerSide(boardBox.clientWidth || 320);
    marks = [...spread(finite(check.left), most), ...spread(finite(check.right), most)];
  };

  // ── The board (rebuilt when the colour scheme changes, keeping the view) ──
  let board = null;
  let view = null;
  const draw = () => {
    if (board) {
      view = board.getBoundingBox();
      freeBoard(JXG, board);
    }
    const palette = PALETTES[currentScheme(doc)];
    boardBox.style.background = palette.background;
    const width = Math.max(boardBox.clientWidth || host.clientWidth || 320, 200);
    boardBox.style.height = `${Math.round(Math.max(Math.min(width * 0.62, 420), 220))}px`;
    board = createBoard(JXG, boardBox, {
      xRange: [x0, x1],
      yRange: [y0, y1],
      palette,
      label: `Graph of y = f(x), where f(x) = ${config.f}, near x = ${n(a)}, with the band of half-width ε around y = ${n(L)} and the window of half-width δ around x = ${n(a)}. The text below the graph states the largest δ and whether your δ works.`,
    });
    if (view) board.setBoundingBox(view, false);
    const fixed = { fixed: true, highlight: false, withLabel: false, showInfobox: false };
    // A filled rectangle that follows the view: [left, right, bottom, top] of user coordinates.
    const rect = (bounds, colour) => {
      const c = board.create("curve", [[], []], { ...fixed, strokeWidth: 0, strokeOpacity: 0, fillColor: colour, fillOpacity: 0.14 });
      c.updateDataArray = function () {
        const [l, r, b, t] = bounds();
        this.dataX = [l, r, r, l, l];
        this.dataY = [b, b, t, t, b];
      };
    };
    const far = () => {
      const [l, r, b, t] = visibleRange(board);
      return { l: l - (r - l), r: r + (r - l), b: b - (t - b), t: t + (t - b) };
    };
    rect(() => [far().l, far().r, L - eps, L + eps], palette.band);
    rect(() => [a - delta, a + delta, far().b, far().t], palette.window);
    const hline = (y) => board.create("line", [[0, y], [1, y]], { ...fixed, strokeColor: palette.band, strokeWidth: 1.5, dash: 2 });
    hline(() => L - eps);
    hline(() => L + eps);
    const vline = (x, style) => board.create("line", [[x, 0], [x, 1]], { ...fixed, ...style });
    vline(() => a - delta, { strokeColor: palette.window, strokeWidth: 1.5 });
    vline(() => a + delta, { strokeColor: palette.window, strokeWidth: 1.5 });
    vline(a, { strokeColor: palette.axis, strokeWidth: 1, dash: 1 });
    // The largest δ on each side: dotted ticks across the band (hidden when there is none).
    for (const [side, key] of [[-1, "left"], [1, "right"]]) {
      const x = () => (result[key].none ? NaN : a + side * result[key].delta);
      board.create("segment", [[x, () => L - eps], [x, () => L + eps]], {
        ...fixed, strokeColor: palette.window, strokeWidth: 3, dash: 1,
      });
    }
    const curve = board.create("curve", [[], []], { ...fixed, strokeColor: palette.curve, strokeWidth: 2.5 });
    curve.updateDataArray = function () {
      const [l, r, b, t] = visibleRange(board);
      const s = sample(f, l, r, { n: 600, exclude: [a], jump: 2 * (t - b) });
      this.dataX = s.xs;
      this.dataY = s.ys;
    };
    // (a, L): an open circle, the point the graph should approach.
    board.create("point", [a, L], { ...fixed, size: 4, strokeWidth: 2, strokeColor: palette.point, fillColor: palette.background, fillOpacity: 1 });
    // Failing points: crosses (a shape, not only a colour).
    const crosses = board.create("curve", [[], []], { ...fixed, strokeColor: palette.bad, strokeWidth: 2 });
    crosses.updateDataArray = function () {
      const dx = CROSS_PX / board.unitX;
      const dy = CROSS_PX / board.unitY;
      const xs = [];
      const ys = [];
      for (const p of marks) {
        xs.push(p.x - dx, p.x + dx, NaN, p.x - dx, p.x + dx, NaN);
        ys.push(p.y - dy, p.y + dy, NaN, p.y + dy, p.y - dy, NaN);
      }
      this.dataX = xs;
      this.dataY = ys;
    };
    board.update();
  };

  // ── Controls ──
  const epsStep = config.epsStep ?? (config.epsRange[1] - config.epsRange[0]) / 100;
  const epsSlider = slider(doc, {
    name: "ε", min: config.epsRange[0], max: config.epsRange[1], step: epsStep, value: eps,
    onInput: (v) => {
      eps = v;
      compute();
      judge();
      showLargest();
      showVerdict();
      board?.update();
    },
  });
  const deltaStep = maxDelta / 1000;
  const deltaSlider = slider(doc, {
    name: "δ", min: deltaStep, max: maxDelta, step: deltaStep, value: delta,
    onInput: (v) => {
      delta = v;
      judge();
      showVerdict();
      board?.update();
    },
  });
  // The browser snaps a value that is off the slider's grid; start from what it shows.
  eps = Number(epsSlider.input.value) || eps;
  epsSlider.set(eps);
  delta = Number(deltaSlider.input.value) || delta;
  deltaSlider.set(delta);
  const useLargest = button(doc, "Set δ to the largest", () => {
    if (result.none) return;
    delta = Math.min(result.delta, maxDelta);
    deltaSlider.set(delta);
    judge();
    showVerdict();
    board?.update();
  });
  const centre = () => [a, L];
  controls.append(
    epsSlider.element,
    deltaSlider.element,
    el(doc, "div", { class: "mp-buttons", role: "group", "aria-label": "δ and zoom" }, [
      useLargest,
      button(doc, "Zoom in", () => zoomAbout(board, 2, ...centre())),
      button(doc, "Zoom out", () => zoomAbout(board, 0.5, ...centre())),
      button(doc, "Reset view", () => board.setBoundingBox([x0, y1, x1, y0], false)),
    ]),
  );
  const refreshButton = () => {
    useLargest.disabled = result.none;
  };

  compute();
  judge();
  draw();
  showLargest();
  showVerdict();
  refreshButton();
  epsSlider.input.addEventListener("input", refreshButton);

  const stopWatching = watchScheme(draw, doc);
  let lastWidth = boardBox.clientWidth;
  const resize = new doc.defaultView.ResizeObserver(() => {
    if (Math.abs(boardBox.clientWidth - lastWidth) > 4) {
      lastWidth = boardBox.clientWidth;
      judge(); // the number of crosses follows the width
      draw();
    }
  });
  resize.observe(boardBox);

  return () => {
    stopWatching();
    resize.disconnect();
    freeBoard(JXG, board);
  };
}

export default { render };
