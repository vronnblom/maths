// The logic of plugins/topic-header.mjs (docs/plan/03 §3.6): from front matter, the toc and the
// curricula to the MyST AST nodes that {topic-header}, {where-this-leads} and {chapter-topics}
// emit. Pure functions over plain data, with no file access and no mystmd, so that
// plugins/_tests/ can run them with `node --test`. Malformed input raises HeaderError, which the
// plugin turns into a build error: a header is never silently empty.

export class HeaderError extends Error {}

const STATUSES = ["draft", "reviewed", "verified"];
const STATUS_TEXT = { draft: "Draft", reviewed: "Reviewed", verified: "Verified" };

// ── Nodes ────────────────────────────────────────────────────────────────────

export const text = (value) => ({ type: "text", value });
const strong = (value) => ({ type: "strong", children: [text(value)] });
const paragraph = (...children) => ({ type: "paragraph", children });
const span = (cls, children) => ({ type: "span", class: cls, children });

/** A reference to a page or block label; MyST resolves it to the target's title and URL. */
export const crossReference = (label) => ({ type: "crossReference", identifier: label, label, children: [] });

export function badge(status) {
  return span(`maths-badge maths-status-${status}`, [text(STATUS_TEXT[status])]);
}

export function dots(difficulty) {
  const marks = `${"●".repeat(difficulty)}${"○".repeat(5 - difficulty)}`;
  return span("maths-difficulty", [span("maths-dots", [text(marks)]), text(` (${difficulty} of 5)`)]);
}

function comingSoon(title) {
  return [text(title), span("maths-coming-soon", [text(" (coming soon)")])];
}

function admonition(kind, cls, title, children) {
  return { type: "admonition", kind, class: cls, children: [{ type: "admonitionTitle", children: [text(title)] }, ...children] };
}

function joined(parts, sep = ", ") {
  return parts.flatMap((p, i) => (i ? [text(sep), ...p] : p));
}

// ── Front matter ─────────────────────────────────────────────────────────────

const isInt = (v) => Number.isInteger(v);

/**
 * The `maths` block of a page that uses {topic-header}, checked. `rel` is the page's path in
 * the project (for messages). Throws HeaderError on anything the header could not render.
 */
export function readMaths(fm, rel, kinds = ["topic", "chapter"]) {
  if (!fm || typeof fm !== "object") throw new HeaderError(`${rel}: no front matter`);
  const m = fm.maths;
  if (!m || typeof m !== "object" || Array.isArray(m)) throw new HeaderError(`${rel}: front matter has no maths: block (docs/plan/03 §3.3)`);
  if (!kinds.includes(m.kind)) throw new HeaderError(`${rel}: maths.kind is ${JSON.stringify(m.kind)}; this directive is for ${kinds.join(" and ")} pages`);
  if (!STATUSES.includes(m.status)) throw new HeaderError(`${rel}: maths.status must be one of ${STATUSES.join(", ")}, not ${JSON.stringify(m.status)}`);
  if (typeof fm.label !== "string" || !fm.label) throw new HeaderError(`${rel}: front matter has no label`);
  const pre = m.prerequisites ?? [];
  if (!Array.isArray(pre) || pre.some((p) => typeof p !== "string" || !p)) throw new HeaderError(`${rel}: maths.prerequisites must be a list of topic labels`);
  const obj = m.objectives;
  if (!Array.isArray(obj) || obj.length === 0 || obj.some((o) => typeof o !== "string" || !o.trim())) {
    throw new HeaderError(`${rel}: maths.objectives must be a non-empty list of sentences`);
  }
  if (m.kind === "topic") {
    if (!isInt(m.est_minutes) || m.est_minutes < 1) throw new HeaderError(`${rel}: maths.est_minutes must be a whole number of minutes`);
    if (!isInt(m.difficulty) || m.difficulty < 1 || m.difficulty > 5) throw new HeaderError(`${rel}: maths.difficulty must be a whole number from 1 to 5`);
  }
  return { ...m, label: fm.label, title: fm.title, prerequisites: pre };
}

// ── The index: written pages, planned topics, reverse edges ──────────────────

/**
 * pages: [{rel, fm}] in toc order (only pages in the toc; never a glob, docs/plan/06 §6.4).
 * curricula: [{folder, data}] (data = a parsed curriculum.yml).
 */
export function buildIndex({ pages, curricula }) {
  const written = new Map();
  pages.forEach(({ rel, fm }, order) => {
    if (fm && typeof fm.label === "string") written.set(fm.label, { label: fm.label, title: fm.title, rel, maths: fm.maths ?? {}, order });
  });
  const planned = new Map();
  const chapters = new Map();
  let order = 0;
  for (const { folder, data } of curricula) {
    for (const ch of data?.chapters ?? []) {
      const labels = [];
      for (const t of ch.topics ?? []) {
        if (typeof t?.label !== "string") continue;
        planned.set(t.label, { label: t.label, title: t.title, level: t.level, prerequisites: t.prerequisites ?? [], chapter: `${folder}/${ch.slug}`, order: order++ });
        labels.push(t.label);
      }
      chapters.set(`${folder}/${ch.slug}`, { title: ch.title, topics: labels });
    }
  }
  // Reverse edges. A written page's own front matter is the truth (03 §3.3); a planned topic
  // without a page contributes its curriculum prerequisites.
  const dependants = new Map();
  const add = (pre, label) => {
    if (!dependants.has(pre)) dependants.set(pre, new Set());
    dependants.get(pre).add(label);
  };
  for (const p of written.values()) {
    const pre = Array.isArray(p.maths.prerequisites) ? p.maths.prerequisites : [];
    if (p.maths.kind === "topic") pre.forEach((x) => add(x, p.label));
  }
  for (const t of planned.values()) {
    if (!written.has(t.label)) t.prerequisites.forEach((x) => add(x, t.label));
  }
  return { written, planned, chapters, dependants };
}

/** [nodes] for a topic label: a link if its page is written, else its title "(coming soon)". */
function topicRef(label, index, rel) {
  if (index.written.has(label)) return [crossReference(label)];
  const t = index.planned.get(label);
  if (t) return comingSoon(t.title);
  throw new HeaderError(`${rel}: ${label} is neither a page in the toc nor a topic in a curriculum.yml`);
}

function sortTopics(labels, index) {
  const key = (l) => (index.written.has(l) ? [0, index.written.get(l).order] : [1, index.planned.get(l)?.order ?? 0]);
  return [...labels].sort((a, b) => {
    const [ka, kb] = [key(a), key(b)];
    return ka[0] - kb[0] || ka[1] - kb[1];
  });
}

/** The chapter (folder/slug) of a chapter page, from its path. */
export function chapterOf(rel) {
  const parts = rel.split("/");
  return parts.length === 3 && parts[2] === "index.md" ? `${parts[0]}/${parts[1]}` : null;
}

// ── {topic-header} ───────────────────────────────────────────────────────────

/**
 * The nodes of {topic-header}. `parseInline(markdown)` turns an objective into inline nodes
 * (the plugin passes MyST's parser, so $math$ renders); `github` is project.github.
 */
export function topicHeader(fm, rel, index, { parseInline = (s) => [text(s)], github = null } = {}) {
  const m = readMaths(fm, rel);
  const nodes = [];
  if (m.status === "draft") {
    nodes.push(admonition("warning", "maths-draft-banner", "Draft — may contain errors", [
      paragraph(text("This page has not been reviewed yet. Read it critically, and please report anything that looks wrong.")),
    ]));
  }
  let status = badge(m.status);
  if (m.status === "verified" && github && typeof m.verify === "string") {
    status = { type: "link", url: `${github}/blob/main/${m.verify}`, children: [status] };
  }
  const facts = [status];
  if (m.kind === "topic") facts.push(text(` · About ${m.est_minutes} minutes · Difficulty `), dots(m.difficulty));

  const pre = m.prerequisites.map((p) => topicRef(p, index, rel));
  const children = [
    paragraph(...facts),
    paragraph(
      strong(m.kind === "topic" ? "You should know: " : "This chapter builds on: "),
      ...(pre.length ? joined(pre) : [text("nothing beyond school mathematics.")]),
    ),
    paragraph(strong(m.kind === "topic" ? "After this page you should be able to:" : "After this chapter you should be able to:")),
    { type: "list", ordered: false, spread: false, children: m.objectives.map((o) => ({ type: "listItem", spread: false, children: [paragraph(...parseInline(o))] })) },
  ];
  nodes.push(admonition("note", "maths-topic-header", m.kind === "topic" ? "Before you start" : "About this chapter", children));
  return nodes;
}

// ── {where-this-leads} ───────────────────────────────────────────────────────

export function whereThisLeads(fm, rel, index) {
  const m = readMaths(fm, rel);
  let labels;
  if (m.kind === "topic") {
    labels = [...(index.dependants.get(m.label) ?? [])];
  } else {
    const ch = index.chapters.get(chapterOf(rel));
    if (!ch) throw new HeaderError(`${rel}: no chapter ${chapterOf(rel)} in curriculum.yml`);
    const own = new Set(ch.topics);
    labels = [...new Set(ch.topics.flatMap((t) => [...(index.dependants.get(t) ?? [])]))].filter((l) => !own.has(l));
  }
  if (!labels.length) return [paragraph(text(`Nothing builds on this ${m.kind} yet.`))];
  return [
    paragraph(text(m.kind === "topic" ? "These topics build on this one:" : "These topics build on this chapter:")),
    {
      type: "list", ordered: false, spread: false,
      children: sortTopics(labels, index).map((l) => ({ type: "listItem", spread: false, children: [paragraph(...topicRef(l, index, rel))] })),
    },
  ];
}

// ── {chapter-topics} ─────────────────────────────────────────────────────────

const cell = (children, header = false) => ({ type: "tableCell", ...(header ? { header: true } : {}), children });
const row = (cells) => ({ type: "tableRow", children: cells });

export function chapterTopics(fm, rel, index) {
  readMaths(fm, rel, ["chapter"]);
  const key = chapterOf(rel);
  const ch = index.chapters.get(key);
  if (!ch) throw new HeaderError(`${rel}: {chapter-topics} found no chapter ${key} in a curriculum.yml`);
  const rows = [row(["Topic", "Time", "Difficulty", "Status"].map((h) => cell([text(h)], true)))];
  for (const label of ch.topics) {
    const t = index.planned.get(label);
    const ext = t.level === "extension" ? [text(" (extension)")] : [];
    const page = index.written.get(label);
    if (page) {
      const m = readMaths({ ...page, maths: page.maths }, page.rel, ["topic"]);
      rows.push(row([cell([crossReference(label), ...ext]), cell([text(`${m.est_minutes} min`)]), cell([dots(m.difficulty)]), cell([badge(m.status)])]));
    } else {
      rows.push(row([cell([text(t.title), ...ext]), cell([text("–")]), cell([text("–")]), cell([span("maths-coming-soon", [text("coming soon")])])]));
    }
  }
  return [{ type: "table", class: "maths-chapter-topics", children: rows }];
}
