// Expressions in widget configs ("f": "a*sin(b*(x - c)) + d"), compiled by JSXGraph's JessieCode
// (docs/plan/05 §5.8). Pure: no DOM, and JSXGraph is passed in, never imported, so `node --test`
// can run this with the npm copy of the same JSXGraph version that the browser loads.
//
// JessieCode alone is too forgiving for author input: an unknown function returns its argument
// (`sec(x)` is x), an unknown name is undefined, `2x` compiles to a no-op, and it accepts `;`,
// `==`, `?:` and property access. So every expression first passes a strict tokenizer with an
// allowlist (the same lists as `$defs` in schema/widgets/function-plot.schema.json, which
// scripts/check_widgets.py applies in CI): numbers, the variable and parameters, + - * / ^,
// parentheses, pi, e and 17 functions, so no statement, property access or string reaches
// JessieCode (expression.test.mjs tests the injections). Only then is it handed to JessieCode,
// which parses it and builds a JavaScript function from the code it generates **with eval**:
// this module calls neither eval nor new Function itself, but the allowlisted expression is
// compiled through JessieCode's eval. The allowlist does not check the grammar (`sin()`, `x+`
// pass it); JessieCode rejects those, and scripts/compile_expressions.mjs runs this compiler on
// every expression in the content for `npm run check` (check_widgets.py).

// Function names an expression may call, and the constants it may use. `e` and `pi` are
// written as in the answer subset (docs/plan/04 §4.3) and translated for JessieCode. `log` is
// not allowed: write `ln` (docs/plan/04 §4.2).
export const FUNCTIONS = [
  "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh",
  "exp", "ln", "sqrt", "cbrt", "abs", "floor", "ceil", "sign",
];
export const CONSTANTS = { pi: "PI", e: "EULER" };

export class ExpressionError extends Error {}

const TOKEN = /\s*(?:(\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|([-+*/^()]))/y;

/** Split an expression into tokens {type: "num"|"name"|"op", value, pos}. */
export function tokenize(src) {
  if (typeof src !== "string" || !src.trim()) throw new ExpressionError("the expression is empty");
  const tokens = [];
  TOKEN.lastIndex = 0;
  let pos = 0;
  while (pos < src.length) {
    if (!src.slice(pos).trim()) break;
    TOKEN.lastIndex = pos;
    const m = TOKEN.exec(src);
    if (!m) {
      const at = pos + (src.slice(pos).length - src.slice(pos).trimStart().length);
      throw new ExpressionError(`unexpected character ${JSON.stringify(src[at])} at position ${at + 1}`);
    }
    const start = m.index + m[0].length - (m[1] ?? m[2] ?? m[3]).length;
    if (m[1] !== undefined) tokens.push({ type: "num", value: m[1], pos: start });
    else if (m[2] !== undefined) tokens.push({ type: "name", value: m[2], pos: start });
    else tokens.push({ type: "op", value: m[3], pos: start });
    pos = TOKEN.lastIndex;
  }
  return tokens;
}

/**
 * Check `src` against the expression rules and return it in JessieCode syntax.
 * `names` are the variable and the parameters, e.g. ["x", "a", "b"].
 */
export function checkExpression(src, names) {
  const tokens = tokenize(src);
  const known = new Set(names);
  let depth = 0;
  const out = [];
  const startsOperand = (t) => t && (t.type === "num" || t.type === "name" || t.value === "(");
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    const next = tokens[i + 1];
    const where = `at position ${t.pos + 1}`;
    if (t.type === "name") {
      if (FUNCTIONS.includes(t.value)) {
        if (!next || next.value !== "(") throw new ExpressionError(`${t.value} needs parentheses: ${t.value}(…) (${where})`);
        out.push(t.value);
        continue;
      }
      if (t.value === "log") throw new ExpressionError(`write ln for the natural logarithm, not log (${where})`);
      let value;
      if (known.has(t.value)) value = t.value;
      else if (Object.hasOwn(CONSTANTS, t.value)) value = CONSTANTS[t.value];
      else throw new ExpressionError(`unknown name ${t.value} (${where}): use the variable, a parameter, pi, e, or one of ${FUNCTIONS.join(", ")}`);
      if (next && next.value === "(") throw new ExpressionError(`${t.value} is not a function: write ${t.value}*(…) (${where})`);
      if (startsOperand(next)) throw new ExpressionError(`missing * after ${t.value} (${where})`);
      out.push(value);
    } else if (t.type === "num") {
      if (startsOperand(next)) throw new ExpressionError(`missing * after ${t.value}: write ${t.value}*${next.value} (${where})`);
      out.push(t.value);
    } else {
      if (t.value === "(") depth++;
      if (t.value === ")") {
        depth--;
        if (depth < 0) throw new ExpressionError(`unmatched ) (${where})`);
        if (startsOperand(next)) throw new ExpressionError(`missing * after ) (${where})`);
      }
      out.push(t.value);
    }
  }
  if (depth > 0) throw new ExpressionError("unmatched (");
  return out.join(" ");
}

// One headless JessieCode board per JSXGraph instance (a NoRenderer board needs no DOM).
const parsers = new WeakMap();

function parser(JXG) {
  let board = parsers.get(JXG);
  if (!board) {
    const attr = JXG.copyAttributes({}, JXG.Options, "board");
    // No events: in a browser a board would otherwise listen for window resizes and scrolls,
    // and this one has no container to measure.
    for (const k of Object.keys(attr.registerevents)) attr.registerevents[k] = false;
    attr.resize = { ...attr.resize, enabled: false };
    board = new JXG.Board("maths-expression-parser", new JXG.NoRenderer(), "maths-expression-parser", [0, 0], 1, 1, 1, 1, 1, 1, attr);
    parsers.set(JXG, board);
  }
  return board.jc;
}

/**
 * Compile `src` with JessieCode. Returns f(x, params) → number, where params maps each
 * parameter name to its value; any value that is not a finite number becomes NaN.
 */
export function compileExpression(JXG, src, variable = "x", paramNames = []) {
  const names = [variable, ...paramNames];
  const code = checkExpression(src, names);
  let fn;
  try {
    fn = parser(JXG).snippet(code, true, names.join(", "), false);
  } catch (err) {
    // Its own message names its internal grammar ('NULL', 'MAP'), so say what to look for.
    throw new ExpressionError(`JessieCode cannot parse ${JSON.stringify(src)}: is an operand missing, as in "x+" or "sin()"?`);
  }
  const f = (x, params = {}) => {
    const y = fn(x, ...paramNames.map((p) => params[p]));
    return typeof y === "number" && Number.isFinite(y) ? y : NaN;
  };
  // JessieCode turns some syntax errors into a no-op function instead of throwing.
  const probe = fn(0.5, ...paramNames.map(() => 0.5));
  if (typeof probe !== "number") throw new ExpressionError(`JessieCode cannot compile ${JSON.stringify(src)}`);
  return f;
}
