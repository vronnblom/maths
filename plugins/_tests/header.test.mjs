// plugins/topic-header.mjs and its pure logic, plugins/_lib/header.mjs (docs/plan/03 §3.6).
// tests/test_plugin_build.py builds the templates with the plugin through mystmd and checks
// the resolved AST; these tests check the decisions directly.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

import { HeaderError, buildIndex, chapterTopics, topicHeader, whereThisLeads } from "../_lib/header.mjs";
import plugin, { loadProject, readFrontmatter, tocFiles } from "../topic-header.mjs";

const fm = (label, maths, title = label) => ({ title, label, maths });
const topic = (label, prerequisites, extra = {}) =>
  fm(label, { kind: "topic", subject: "calc", status: "draft", est_minutes: 30, difficulty: 2, prerequisites, objectives: ["State it.", "Use it."], ...extra });

const curriculum = {
  folder: "calculus",
  data: {
    subject: "calc",
    chapters: [
      { slug: "preliminaries", title: "Preliminaries", topics: [
        { label: "calc-functions", title: "Functions and Their Graphs", level: "core", prerequisites: [] },
        { label: "calc-absolute-value-inequalities", title: "Absolute Value and Inequalities", level: "core", prerequisites: [] },
      ] },
      { slug: "limits", title: "Limits", topics: [
        { label: "calc-limit", title: "The Limit of a Function", level: "core", prerequisites: ["calc-functions", "calc-absolute-value-inequalities"] },
        { label: "calc-one-sided-limits", title: "One-Sided Limits", level: "core", prerequisites: ["calc-limit"] },
        { label: "calc-limit-laws", title: "Limit Laws", level: "core", prerequisites: ["calc-limit"] },
        { label: "calc-epsilon-extra", title: "An Extension", level: "extension", prerequisites: ["calc-limit"] },
      ] },
      { slug: "continuity", title: "Continuity", topics: [
        { label: "calc-continuity", title: "Continuity", level: "core", prerequisites: ["calc-limit-laws"] },
      ] },
    ],
  },
};

const pages = [
  { rel: "calculus/preliminaries/functions.md", fm: topic("calc-functions", []) },
  { rel: "calculus/limits/index.md", fm: fm("calc-limits-chapter", { kind: "chapter", subject: "calc", status: "draft", prerequisites: ["calc-functions"], objectives: ["Explain limits."] }, "Limits") },
  { rel: "calculus/limits/limit-of-a-function.md", fm: topic("calc-limit", ["calc-functions", "calc-absolute-value-inequalities"], { est_minutes: 40 }) },
  { rel: "calculus/limits/limit-laws.md", fm: topic("calc-limit-laws", ["calc-limit"], { status: "reviewed", difficulty: 3 }) },
];
const index = buildIndex({ pages, curricula: [curriculum] });
const page = (label) => pages.find((p) => p.fm.label === label);

/** Every node of a tree, depth first. */
function* walk(node) {
  if (Array.isArray(node)) {
    for (const n of node) yield* walk(n);
    return;
  }
  yield node;
  yield* walk(node.children ?? []);
}
const textOf = (nodes) => [...walk(nodes)].filter((n) => n.type === "text").map((n) => n.value).join("");
const refs = (nodes) => [...walk(nodes)].filter((n) => n.type === "crossReference").map((n) => n.identifier);
const byClass = (nodes, cls) => [...walk(nodes)].filter((n) => (n.class ?? "").split(" ").includes(cls));

test("the index: written pages, planned topics, reverse edges from front matter and curriculum", () => {
  assert.deepEqual([...index.written.keys()], ["calc-functions", "calc-limits-chapter", "calc-limit", "calc-limit-laws"]);
  assert.equal(index.planned.size, 7);
  assert.deepEqual([...index.dependants.get("calc-limit")].sort(), ["calc-epsilon-extra", "calc-limit-laws", "calc-one-sided-limits"]);
  assert.deepEqual([...index.dependants.get("calc-limit-laws")], ["calc-continuity"]);
  assert.ok(!index.dependants.has("calc-limits-chapter"), "a chapter page is nobody's prerequisite");
});

test("{topic-header} on a draft topic: banner, badge, time, difficulty, prerequisites, objectives", () => {
  const nodes = topicHeader(page("calc-limit").fm, "calculus/limits/limit-of-a-function.md", index);
  assert.equal(nodes.length, 2);
  assert.equal(nodes[0].kind, "warning");
  assert.match(textOf(nodes[0]), /^Draft — may contain errors/);
  const header = nodes[1];
  assert.equal(header.class, "maths-topic-header");
  assert.equal(byClass(header, "maths-badge")[0].class, "maths-badge maths-status-draft");
  assert.match(textOf(header), /About 40 minutes · Difficulty ●●○○○ \(2 of 5\)/);
  assert.deepEqual(refs(header), ["calc-functions"], "a written prerequisite is a crossReference");
  assert.match(textOf(header), /You should know: , Absolute Value and Inequalities \(coming soon\)/, "a planned one is its title, coming soon");
  const list = [...walk(header)].find((n) => n.type === "list");
  assert.deepEqual(list.children.map((li) => textOf(li)), ["State it.", "Use it."]);
});

test("objectives go through the inline parser (MyST's, in the plugin), so $math$ renders", () => {
  const parseInline = (s) => [{ type: "inlineMath", value: s }];
  const nodes = topicHeader(page("calc-limit").fm, "x.md", index, { parseInline });
  assert.equal([...walk(nodes)].filter((n) => n.type === "inlineMath").length, 2);
});

test("a reviewed page has no banner; a verified one links its badge to the test file", () => {
  const reviewed = topicHeader(page("calc-limit-laws").fm, "calculus/limits/limit-laws.md", index);
  assert.equal(reviewed.length, 1);
  assert.equal(byClass(reviewed, "maths-badge")[0].class, "maths-badge maths-status-reviewed");
  const v = topic("calc-limit-laws", ["calc-limit"], { status: "verified", verify: "verify/calculus/limits/test_limit_laws.py" });
  const verified = topicHeader(v, "calculus/limits/limit-laws.md", index, { github: "https://github.com/vronnblom/maths" });
  const link = [...walk(verified)].find((n) => n.type === "link");
  assert.equal(link.url, "https://github.com/vronnblom/maths/blob/main/verify/calculus/limits/test_limit_laws.py");
  assert.equal(link.children[0].class, "maths-badge maths-status-verified");
});

test("{topic-header} on a chapter page: no time or difficulty", () => {
  const nodes = topicHeader(page("calc-limits-chapter").fm, "calculus/limits/index.md", index);
  const header = nodes.at(-1);
  assert.match(textOf(header), /^About this chapterDraftThis chapter builds on: /);
  assert.doesNotMatch(textOf(header), /minutes|Difficulty/);
  assert.deepEqual(refs(header), ["calc-functions"]);
});

test("{where-this-leads}: written dependants as links, then planned ones, coming soon", () => {
  const nodes = whereThisLeads(page("calc-limit").fm, "calculus/limits/limit-of-a-function.md", index);
  assert.deepEqual(refs(nodes), ["calc-limit-laws"]);
  assert.match(textOf(nodes), /One-Sided Limits \(coming soon\).*An Extension \(coming soon\)/);
  const none = whereThisLeads(topic("calc-functions", []), "calculus/preliminaries/functions.md", buildIndex({ pages: [], curricula: [] }));
  assert.equal(textOf(none), "Nothing builds on this topic yet.");
});

test("{where-this-leads} on a chapter page: dependants outside the chapter", () => {
  const nodes = whereThisLeads(page("calc-limits-chapter").fm, "calculus/limits/index.md", index);
  assert.equal(textOf(nodes), "These topics build on this chapter:Continuity (coming soon)");
});

test("{chapter-topics}: the chapter's topics from the curriculum, with front matter where written", () => {
  const [table] = chapterTopics(page("calc-limits-chapter").fm, "calculus/limits/index.md", index);
  assert.equal(table.type, "table");
  const rows = table.children.map((r) => r.children.map((c) => textOf(c)));
  assert.deepEqual(rows, [
    ["Topic", "Time", "Difficulty", "Status"],
    ["", "40 min", "●●○○○ (2 of 5)", "Draft"],
    ["One-Sided Limits", "–", "–", "coming soon"],
    ["", "30 min", "●●●○○ (3 of 5)", "Reviewed"],
    ["An Extension (extension)", "–", "–", "coming soon"],
  ]);
  assert.deepEqual(refs(table), ["calc-limit", "calc-limit-laws"]);
  assert.ok(table.children[0].children.every((c) => c.header === true));
});

test("malformed front matter is an error, never an empty header", () => {
  const cases = [
    [null, /no front matter/],
    [{ title: "x", label: "calc-limit" }, /no maths: block/],
    [fm("site-home", { kind: "meta", status: "draft" }), /maths.kind is "meta"/],
    [topic("calc-limit", ["calc-functions"], { status: "done" }), /maths.status must be one of/],
    [topic("calc-limit", ["calc-functions"], { difficulty: 7 }), /difficulty must be a whole number from 1 to 5/],
    [topic("calc-limit", ["calc-functions"], { est_minutes: "40" }), /est_minutes/],
    [topic("calc-limit", "calc-functions"), /prerequisites must be a list/],
    [topic("calc-limit", ["calc-functions"], { objectives: [] }), /objectives must be a non-empty list/],
    [topic("calc-limit", ["calc-no-such-topic"]), /calc-no-such-topic is neither a page in the toc nor a topic/],
  ];
  for (const [front, message] of cases) {
    assert.throws(() => topicHeader(front, "p.md", index), (e) => e instanceof HeaderError && message.test(e.message), String(message));
  }
  assert.throws(() => chapterTopics(page("calc-limit").fm, "calculus/limits/limit-of-a-function.md", index), /this directive is for chapter pages/);
  const orphan = fm("calc-nowhere-chapter", { kind: "chapter", subject: "calc", status: "draft", objectives: ["Do."] });
  assert.throws(() => chapterTopics(orphan, "calculus/nowhere/index.md", index), /found no chapter calculus\/nowhere/);
});

test("loadProject reads the toc's pages and the curricula of their folders, never _build/", () => {
  const root = mkdtempSync(path.join(tmpdir(), "maths-plugin-"));
  try {
    const write = (rel, content) => {
      mkdirSync(path.dirname(path.join(root, rel)), { recursive: true });
      writeFileSync(path.join(root, rel), content);
    };
    write("myst.yml", "version: 1\nproject:\n  toc:\n    - file: index.md\n    - title: Calculus\n      children:\n        - file: calculus/limits/limit-of-a-function.md\n");
    write("index.md", "---\ntitle: Home\nlabel: site-home\nmaths: {kind: meta, status: draft}\n---\n");
    write("calculus/limits/limit-of-a-function.md", "---\ntitle: The Limit of a Function\nlabel: calc-limit\nmaths:\n  kind: topic\n  prerequisites: [calc-functions]\n---\nBody\n");
    write("calculus/curriculum.yml", "subject: calc\nchapters:\n  - slug: limits\n    title: Limits\n    topics:\n      - {label: calc-limit, title: The Limit of a Function, prerequisites: []}\n");
    write("_build/site/calculus/limits/stale.md", "---\ntitle: Stale\nlabel: calc-stale\nmaths: {kind: topic, prerequisites: [calc-functions]}\n---\n");
    const p = loadProject(root);
    assert.deepEqual(p.files, ["index.md", "calculus/limits/limit-of-a-function.md"]);
    assert.deepEqual([...p.index.written.keys()], ["site-home", "calc-limit"]);
    assert.deepEqual(p.curricula.map((c) => c.folder), ["calculus"]);
    assert.deepEqual([...p.index.dependants.get("calc-functions")], ["calc-limit"]);
    assert.deepEqual(readFrontmatter(path.join(root, "index.md")).maths, { kind: "meta", status: "draft" });
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("tocFiles: .md files, nested, in order, without duplicates", () => {
  const config = { project: { toc: [{ file: "a.md" }, { title: "T", file: "b/index.md", children: [{ file: "b/c.md" }, { file: "a.md" }] }, { url: "https://x" }] } };
  assert.deepEqual(tocFiles(config), ["a.md", "b/index.md", "b/c.md"]);
});

test("the plugin registers the three directives", () => {
  assert.deepEqual(plugin.directives.map((d) => d.name), ["topic-header", "where-this-leads", "chapter-topics"]);
  for (const d of plugin.directives) assert.equal(typeof d.run, "function");
});
