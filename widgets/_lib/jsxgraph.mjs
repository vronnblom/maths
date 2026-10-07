// The one place that pins JSXGraph (docs/plan/05 §5.4, §5.8). Widgets load it inside render()
// with `await import(JSXGRAPH_URL)`; no module imports an https: URL statically, because Node
// refuses those and the widget tests could not import the module. The devDependency `jsxgraph`
// in package.json has the same exact version (a test checks it), so the tests run the same
// JessieCode as the browser.
export const JSXGRAPH_VERSION = "1.14.0";
export const JSXGRAPH_URL = `https://cdn.jsdelivr.net/npm/jsxgraph@${JSXGRAPH_VERSION}/distrib/jsxgraphcore.mjs`;
