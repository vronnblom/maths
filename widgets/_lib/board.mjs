// JSXGraph board helpers shared by the widgets (docs/plan/05 §5.8). JSXGraph itself is passed
// in by the widget, which loads it inside render() (jsxgraph.mjs); nothing here imports it.

/**
 * A board in `container` showing [x0, x1] × [y0, y1], with axes in the palette's colours. Wheel
 * zoom is off (it would hijack page scrolling); the widget offers zoom buttons instead. Panning
 * needs two fingers on touch screens, so one finger still scrolls the page.
 */
export function createBoard(JXG, container, { xRange, yRange, palette, label }) {
  const axis = {
    strokeColor: palette.axis,
    highlight: false,
    ticks: {
      strokeColor: palette.axis,
      label: { strokeColor: palette.text, highlight: false, fontSize: 12 },
      majorHeight: 8,
      minorTicks: 0,
    },
  };
  const board = JXG.JSXGraph.initBoard(container, {
    boundingbox: [xRange[0], yRange[1], xRange[1], yRange[0]],
    keepAspectRatio: false,
    axis: true,
    defaultAxes: { x: axis, y: axis },
    grid: { strokeColor: palette.grid, strokeOpacity: 1, majorStep: "auto", minorElements: 0 },
    showCopyright: false,
    showNavigation: false,
    showInfobox: false,
    zoom: { wheel: false, needShift: false, pinch: true, min: 1e-4, max: 1e4 },
    pan: { enabled: true, needShift: false, needTwoFingers: true },
    // The widget redraws the board when its width changes; JSXGraph's own resize observer
    // would then fire on the freed board.
    resize: { enabled: false },
    title: label,
    description: label,
  });
  container.setAttribute("role", "img");
  container.setAttribute("aria-label", label);
  return board;
}

/** [x0, x1, y0, y1] of what the board currently shows. */
export function visibleRange(board) {
  const [x0, y1, x1, y0] = board.getBoundingBox();
  return [x0, x1, y0, y1];
}

/** Zoom by `factor` (> 1 zooms in) about the point (cx, cy), keeping it where it is on screen. */
export function zoomAbout(board, factor, cx, cy) {
  const [x0, x1, y0, y1] = visibleRange(board);
  const sx = (x) => cx + (x - cx) / factor;
  const sy = (y) => cy + (y - cy) / factor;
  board.setBoundingBox([sx(x0), sy(y1), sx(x1), sy(y0)], false);
}

export function freeBoard(JXG, board) {
  if (board) JXG.JSXGraph.freeBoard(board);
}
