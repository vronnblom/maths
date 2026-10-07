# 1. Vision and scope

## 1.1 What this repository is

`vronnblom/maths` is an **open, interactive, verified reference-and-course for university
mathematics**, published as a static website. Each subject (Calculus first) is:

- a **course**: a recommended reading order through topic pages, with worked examples and
  exercises, that a first-year student can follow from start to finish;
- a **reference**: every definition, theorem, example and exercise has a permanent address
  (a *label*) that can be linked, hovered and cited from any other page or subject;
- a **knowledge graph**: topics declare their prerequisites, so the site can show what you
  need before a page and what a page unlocks.

## 1.2 What it is not

| Not this | Why / what we do instead |
|---|---|
| A replacement for a full textbook | We aim for complete coverage of the standard syllabus, but we leave out long historical digressions, exhaustive exercise banks (hundreds per section) and printed layout. Each page links "further reading" to open textbooks. |
| A formal-proof library (Lean/Mathlib) | Proofs are written for human readers. Correctness comes from review checklists plus computer-checked computations (see [06](06-quality-assurance.md)), not from formal verification. Linking Lean statements later is an open question ([12](12-risks-and-open-questions.md)). |
| A PDF/print product | We chose website only. MyST could export PDF later, but nothing is designed or tested for print. |
| A homework-answer site | Exercises are for learning. Hints come before answers, and answers come before full solutions. |
| A research-level or graduate resource | The scope is the undergraduate curriculum (years 1–3). |
| A video course | Short animations and widgets are welcome. Video is out of scope. |

## 1.3 Audience

The site uses **layered rigor**, so one text serves two audiences:

| Reader | What they read | What they skip |
|---|---|---|
| First-year engineering / science student (primary) | Core text: motivation, definitions, statements, core proofs, examples, tier A/B exercises | "Rigorous track" dropdowns, tier C ε–δ exercises |
| Mathematics major / honours student (secondary) | Everything, including the ε–δ proofs in dropdowns and the tier C exercises | – |
| Teacher / TA | Reference pages, exercise banks, cross-links | – |
| Self-learner returning to maths | Prerequisite chains ("Before you start") and the preliminaries chapter | – |

Assumed background for Calculus: upper-secondary school mathematics (algebra, basic
functions and trigonometry). Anything beyond that is in the *Preliminaries* chapter.

## 1.4 Guiding principles

1. **Correctness first.** No page is marked *verified* until every computation is checked by
   code and every proof has passed the review checklist. A shorter correct page beats a
   longer page with an error.
2. **Intuition before formalism, but never instead of it.** Each concept starts with a
   picture, an example or an interactive widget, then gives the precise definition. The
   precise version is always on the page, even when parts of it are in a dropdown.
3. **One concept, one home.** Each definition and theorem is stated once, on one page, under
   one label. Everything else links to it, and hover previews make the link cheap for the
   reader.
4. **Stable addresses.** Labels and URLs are permanent. Content can move, but its address
   does not break.
5. **Explicit prerequisites.** Every topic page lists what it builds on. A proof may only
   cite results from its prerequisites or from earlier on the same page; CI warns about
   forward references.
6. **Active learning.** Every topic ends with tiered exercises. Interactive widgets are for
   *exploring* an idea (drag ε, watch δ), not for decoration.
7. **Boring, durable tooling.** Plain-text Markdown, few dependencies, pinned versions,
   a static site on free hosting. Content must outlive any single tool, so we avoid
   proprietary syntax wherever a standard MyST construct exists.
8. **Uniformity at scale.** Every subject uses the same folder layout, templates, label
   scheme and checks. Adding Linear Algebra means adding a folder.

## 1.5 Layered rigor model

Each theorem in the curriculum ([08](08-calculus-curriculum.md)) gets a **proof policy**:

| Code | Meaning | Rendering |
|---|---|---|
| **F** | Full proof in the core text | `{proof}` directive, expanded |
| **R** | Proof in the rigorous track | `{proof}` with `:class: dropdown`, titled "Rigorous proof" |
| **S** | Sketch or idea only | "Proof idea" paragraph or `{proof}` titled "Proof sketch" |
| **D** | Deferred to another subject (usually Real Analysis) | Statement + "Proof: see [link]". Until the target exists, a remark explains what is needed (e.g. completeness of ℝ). |

Definitions are layered the same way. The *intuitive* definition of a limit is core, and the
*precise* (ε–δ) definition is **also stated in the core**, with a widget and one worked
example. ε–δ proofs of limit laws go in the rigorous track.

## 1.6 Success criteria

**Calculus 1.0** is reached when:
- all topic pages in [08](08-calculus-curriculum.md) exist with `status: verified`;
- every page has at least 6 exercises across at least 2 tiers, all with answers and solutions;
- every computational claim on a page is covered by a passing verification test;
- every page has at least one interactive widget where the curriculum asks for one;
- the site builds with zero warnings (other than the whitelisted one) and zero broken links;
- an outside reader (a student) has gone through the Limits and Derivatives chapters and
  their feedback has been addressed.
