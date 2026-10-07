// A MyST plugin (MIT; docs/plan/03 §3.6) with three directives, rendered from front matter:
//
//   {topic-header}      prerequisites (links; "coming soon" for planned topics without a page),
//                       objectives, time, difficulty, a status badge, and the draft banner
//                       (topic and chapter pages)
//   {where-this-leads}  the topics that list this one as a prerequisite (reverse edges), then
//                       a link that reports an error on the page (the erratum form, pre-filled)
//   {chapter-topics}    a chapter page's table of its topics, from curriculum.yml
//
// Registered in content/myst.yml under project.plugins. This file reads the files; what to
// render is decided by the pure functions in ./_lib/header.mjs (tested in plugins/_tests/).
// The pages come from the toc in myst.yml, never from a glob, which would also find the stale
// copies under content/_build/ (docs/plan/06 §6.4). The index of pages and curricula is built
// once per build and cached; `myst start` rebuilds it when one of those files changes.

import { existsSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import YAML from "yaml";

import { HeaderError, buildIndex, chapterTopics, topicHeader, whereThisLeads } from "./_lib/header.mjs";

/** The front matter of a Markdown file, parsed (null if it has none). */
export function readFrontmatter(file) {
  const src = readFileSync(file, "utf8");
  const m = /^---\r?\n([\s\S]*?)\r?\n---\s*(\r?\n|$)/.exec(src);
  if (!m) return null;
  try {
    return YAML.parse(m[1]);
  } catch (err) {
    throw new HeaderError(`${file}: front matter is not valid YAML: ${err.message.split("\n")[0]}`);
  }
}

/** The folder with myst.yml above `file`. */
export function projectRoot(file) {
  for (let dir = path.dirname(path.resolve(file)); ; dir = path.dirname(dir)) {
    if (existsSync(path.join(dir, "myst.yml"))) return dir;
    if (path.dirname(dir) === dir) throw new HeaderError(`${file}: no myst.yml above this file`);
  }
}

/** The .md files of the toc of root/myst.yml, in toc order (paths relative to root). */
export function tocFiles(config) {
  const out = [];
  const walk = (items) => {
    for (const item of items ?? []) {
      if (typeof item?.file === "string" && item.file.endsWith(".md")) out.push(item.file);
      if (Array.isArray(item?.children)) walk(item.children);
    }
  };
  walk(config?.project?.toc);
  return [...new Set(out)];
}

/** Everything the directives need about the project at `root`: read from disk. */
export function loadProject(root) {
  const config = YAML.parse(readFileSync(path.join(root, "myst.yml"), "utf8"));
  const files = tocFiles(config).filter((f) => existsSync(path.join(root, f)));
  const pages = files.map((rel) => ({ rel, fm: readFrontmatter(path.join(root, rel)) }));
  // A subject's curriculum sits in its folder; the folders are those of the toc's pages.
  const folders = [...new Set(files.filter((f) => f.includes("/")).map((f) => f.split("/")[0]))];
  const curricula = folders
    .filter((folder) => existsSync(path.join(root, folder, "curriculum.yml")))
    .map((folder) => ({ folder, data: YAML.parse(readFileSync(path.join(root, folder, "curriculum.yml"), "utf8")) }));
  return { config, files, curricula, index: buildIndex({ pages, curricula }) };
}

const cache = new Map(); // root → {stamp, project}

function stamp(root, project) {
  const files = ["myst.yml", ...(project?.files ?? []), ...(project?.curricula ?? []).map((c) => `${c.folder}/curriculum.yml`)];
  return files.map((f) => {
    try {
      return `${f}:${statSync(path.join(root, f)).mtimeMs}`;
    } catch {
      return `${f}:-`;
    }
  }).join("|");
}

function project(file) {
  const root = projectRoot(file);
  const hit = cache.get(root);
  if (hit && hit.stamp === stamp(root, hit.project)) return { root, ...hit.project };
  const loaded = loadProject(root);
  cache.set(root, { stamp: stamp(root, loaded), project: loaded });
  return { root, ...loaded };
}

/** Run `render` for the page of `vfile`; on a HeaderError, a fatal build message and a visible error. */
function directive(name, doc, render) {
  return {
    name,
    doc,
    run(data, vfile, ctx) {
      try {
        const p = project(vfile.path);
        const rel = path.relative(p.root, vfile.path).split(path.sep).join("/");
        const fm = readFrontmatter(vfile.path);
        return render({ fm, rel, index: p.index, config: p.config, ctx });
      } catch (err) {
        if (!(err instanceof HeaderError)) throw err;
        const message = vfile.message(`{${name}}: ${err.message}`, data.node, `maths:${name}`);
        message.fatal = true;
        return [{
          type: "admonition", kind: "danger",
          children: [{ type: "admonitionTitle", children: [{ type: "text", value: `{${name}} could not be rendered` }] },
            { type: "paragraph", children: [{ type: "text", value: err.message }] }],
        }];
      }
    },
  };
}

/** Objectives may contain Markdown and $math$: parse them with MyST, keep the inline nodes. */
function inlineParser(ctx) {
  return (markdown) => {
    const tree = ctx?.parseMyst?.(markdown);
    const first = tree?.children?.[0];
    return first?.type === "paragraph" ? first.children : [{ type: "text", value: markdown }];
  };
}

const plugin = {
  name: "Topic header",
  directives: [
    directive("topic-header", "Prerequisites, objectives, time, difficulty and status, from the front matter (docs/plan/03 §3.6).",
      ({ fm, rel, index, config, ctx }) => topicHeader(fm, rel, index, { parseInline: inlineParser(ctx), github: config?.project?.github ?? null })),
    directive("where-this-leads", "The topics that build on this one (reverse prerequisite edges, from the toc and curriculum.yml).",
      ({ fm, rel, index, config }) => whereThisLeads(fm, rel, index, { github: config?.project?.github ?? null })),
    directive("chapter-topics", "A chapter page's table of topics: title, time, difficulty, status (from curriculum.yml and front matter).",
      ({ fm, rel, index }) => chapterTopics(fm, rel, index)),
  ],
};

export default plugin;
