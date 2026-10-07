// function-plot: the graph of y = f(x) with parameter sliders, a table of values, a hole, a
// traced point and zoom (docs/plan/05 §5.8; config: schema/widgets/function-plot.schema.json;
// catalogue entry: widgets/README.md). An anywidget module: mystmd publishes this file with a
// content hash, and `./_lib/` next to it through `project.static_files`.
//
// All the mathematics (compiling f, sampling, the hole, the table) is in ./_lib/expression.mjs
// and ./_lib/plot.mjs, which widgets/_tests/ check against SymPy. This file only draws.

import { JSXGRAPH_URL } from "./_lib/jsxgraph.mjs";
import { compileExpression } from "./_lib/expression.mjs";
import { configProblems, formatNumber, holeValue, sample, tableRows } from "./_lib/plot.mjs";
import { PALETTES, currentScheme, watchScheme } from "./_lib/colours.mjs";
import { STYLES, button, el, slider, valueTable } from "./_lib/controls.mjs";
import { createBoard, freeBoard, visibleRange, zoomAbout } from "./_lib/board.mjs";

export const KEYS = ["f", "variable", "xRange", "yRange", "parameters", "table", "hole", "trace", "zoom"];

/** The config from the anywidget model (the JSON body of the {anywidget} directive). */
export function readConfig(model) {
  const config = {};
  for (const key of KEYS) {
    const v = model.get(key);
    if (v !== undefined) config[key] = v;
  }
  return config;
}

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
    console.error("function-plot: could not load JSXGraph", err);
    say("The interactive figure could not be loaded. The caption describes it.");
    return undefined;
  }
  // The theme may unmount this element while JSXGraph loads; it then never calls our cleanup.
  if (!host.isConnected) return undefined;

  const variable = config.variable ?? "x";
  const paramSpecs = Object.entries(config.parameters ?? {});
  const params = Object.fromEntries(paramSpecs.map(([name, p]) => [name, p.value]));
  let compiled;
  try {
    compiled = compileExpression(JXG, config.f, variable, paramSpecs.map(([name]) => name));
  } catch (err) {
    say(`This figure could not be drawn (${err.message}). The caption describes it.`);
    return undefined;
  }
  const f = (x) => compiled(x, params);
  // f with the hole punched out: undefined at hole.x, as in the table and on the curve.
  const value = (x) => (config.hole && x === config.hole.x ? NaN : f(x));
  const [x0, x1] = config.xRange;
  const [y0, y1] = config.yRange;
  const fx = `f(${variable})`;

  // ── Layout: board, controls, readout, table ──
  const boardBox = el(doc, "div", { class: "mp-board" });
  const controls = el(doc, "div", { class: "mp-controls" });
  root.append(boardBox, controls);

  const holeY = () => (config.hole.y !== undefined ? config.hole.y : holeValue(f, config.hole.x, x1 - x0));
  let hole = null; // {x, y} or null when f has no finite limit there
  const updateHole = () => {
    if (!config.hole) return;
    try {
      hole = { x: config.hole.x, y: holeY() };
    } catch {
      hole = null;
    }
  };
  updateHole();

  let trace = config.trace ? config.trace.x : null;
  const readout = config.trace ? el(doc, "p", { class: "mp-readout", "aria-live": "polite" }) : null;
  const showReadout = () => {
    if (!readout) return;
    const y = value(trace);
    readout.textContent = Number.isFinite(y)
      ? `${variable} = ${formatNumber(trace)}, ${fx} = ${formatNumber(y)}`
      : `${variable} = ${formatNumber(trace)}: ${fx} is undefined`;
  };

  // The visible range, in words: the axes leave the view when a reader zooms in away from
  // them, and the text also tells a screen reader what the zoom did.
  const viewText = config.zoom !== false ? el(doc, "p", { class: "mp-view", "aria-live": "polite" }) : null;
  const showView = () => {
    if (!viewText || !board) return;
    const [a, b, c, d] = visibleRange(board).map((v) => formatNumber(v, 3));
    viewText.textContent = `Showing ${variable} from ${a} to ${b} and y from ${c} to ${d}.`;
  };

  const table = config.table
    ? valueTable(doc, { caption: `Values of ${fx}`, xName: variable, yName: fx })
    : null;
  const showTable = () => table?.update(tableRows(f, config.table.points, { holeX: config.hole?.x ?? null }));

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
      label: `Graph of y = ${fx}, where ${fx} = ${config.f}. The caption below describes it.`,
    });
    if (view) board.setBoundingBox(view, false);
    board.on("boundingbox", showView); // panning (the zoom buttons call showView themselves)
    const curve = board.create("curve", [[], []], { strokeColor: palette.curve, strokeWidth: 2.5, highlight: false });
    curve.updateDataArray = function () {
      const [a, b, c, d] = visibleRange(board);
      const s = sample(f, a, b, { n: 600, exclude: hole ? [hole.x] : [], jump: 2 * (d - c) });
      this.dataX = s.xs;
      this.dataY = s.ys;
    };
    if (config.hole) {
      board.create("point", [() => hole?.x ?? NaN, () => hole?.y ?? NaN], {
        name: "", fixed: true, highlight: false, size: 4, strokeWidth: 2,
        strokeColor: palette.curve, fillColor: palette.background, fillOpacity: 1, showInfobox: false,
      });
    }
    if (config.trace) {
      board.create("point", [() => trace, () => value(trace)], {
        name: "", fixed: true, highlight: false, size: 4, strokeColor: palette.point, fillColor: palette.point,
        showInfobox: false,
      });
    }
    board.update();
  };

  const refresh = () => {
    updateHole();
    showReadout();
    showTable();
    board?.update();
  };

  // ── Controls ──
  for (const [name, p] of paramSpecs) {
    controls.append(
      slider(doc, {
        name, min: p.min, max: p.max, step: p.step ?? (p.max - p.min) / 100, value: p.value,
        onInput: (v) => {
          params[name] = v;
          refresh();
        },
      }).element,
    );
  }
  if (config.trace) {
    controls.append(
      slider(doc, {
        name: variable, min: x0, max: x1, step: config.trace.step ?? (x1 - x0) / 200, value: trace,
        describe: (v) => `${variable} = ${formatNumber(v)}`,
        onInput: (v) => {
          trace = v;
          showReadout();
          board?.update();
        },
      }).element,
    );
  }
  if (config.zoom !== false) {
    const centre = () => {
      if (hole) return [hole.x, hole.y];
      if (config.trace && Number.isFinite(value(trace))) return [trace, value(trace)];
      const [a, b, c, d] = visibleRange(board);
      return [(a + b) / 2, (c + d) / 2];
    };
    controls.append(
      el(doc, "div", { class: "mp-buttons", role: "group", "aria-label": "Zoom" }, [
        button(doc, "Zoom in", () => (zoomAbout(board, 2, ...centre()), showView())),
        button(doc, "Zoom out", () => (zoomAbout(board, 0.5, ...centre()), showView())),
        button(doc, "Reset view", () => (board.setBoundingBox([x0, y1, x1, y0], false), showView())),
      ]),
    );
  }
  if (viewText) root.append(viewText);
  if (readout) root.append(readout);
  if (table) root.append(table.element);

  draw();
  showView();
  showReadout();
  showTable();

  const stopWatching = watchScheme(draw, doc);
  let lastWidth = boardBox.clientWidth;
  const resize = new doc.defaultView.ResizeObserver(() => {
    if (Math.abs(boardBox.clientWidth - lastWidth) > 4) {
      lastWidth = boardBox.clientWidth;
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
