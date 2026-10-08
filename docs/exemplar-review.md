# Exemplar review: `calc-limit`, The Limit of a Function

This is the [09 §9.1](plan/09-roadmap.md#91-exemplar-rubric-used-in-phase-1a-then-for-every-subjects-exemplar)
rubric applied to the gold-standard page of Phase 1a,
[`content/calculus/limits/limit-of-a-function.md`](../content/calculus/limits/limit-of-a-function.md)
([live page](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/)), as merged in
vronnblom/maths#11 (`d057b7c`). Every later subject's exemplar is judged by the same rubric, and
every topic page aims at the same bar: this document is what "as good as `calc-limit`" means.

**Short answer.** Items 1–11 are met, with evidence below (item 10 with one dead anchor,
found by this review, now a template rule and a follow-up). Item 12 is met on the measurements
(Lighthouse accessibility **95** on mobile and **100** on desktop), with mobile findings that
this freeze turns into rules and theme issues left as follow-ups. The **reader test** is the
owner's and is still to do (the placeholder below). The page is `reviewed`, with 17/17 (100 %)
coverage; it goes to `verified` after the reader test.

## Sources of the evidence

| Source | Link |
|---|---|
| The PR and its rubric self-check | vronnblom/maths#11 |
| Verifier report (tests `4865db9`) | <https://github.com/vronnblom/maths/pull/11#issuecomment-6053843922> |
| Review 1, "at exemplar strictness" (F1–F12) | <https://github.com/vronnblom/maths/pull/11#pullrequestreview-5452874391> |
| The Author's list of changes for the re-check | <https://github.com/vronnblom/maths/pull/11#issuecomment-6058633739> |
| Second pass, verifier and reviewer (N1–N4, tests `aeddec3`) | <https://github.com/vronnblom/maths/pull/11#pullrequestreview-5456282872> |
| N1–N3 fixed; Lighthouse, Playwright at 375 px, axe | <https://github.com/vronnblom/maths/pull/11#issuecomment-6060490139> |
| The trig facts made results of `calc-trig-functions` (second pass N4) | vronnblom/maths#14 |
| The widget and its wording rule | vronnblom/maths#10 |
| The three prerequisite pages | vronnblom/maths#7, #8, #9 |

Links to the page below go to the live site; line numbers refer to the page at `d057b7c`.

## The rubric, item by item

| # | Criterion | Mark | Evidence |
|---|---|---|---|
| 1 | Follows the page structure exactly; the topic header renders prerequisites, objectives, time and status | ✔ | The sections of `templates/topic.md`, in order: [Why this matters](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#why-this-matters) → [What a limit is](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#what-a-limit-is) → [Main results](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#main-results) → [Worked examples](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#worked-examples) → [Common mistakes](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#common-mistakes) → [Rigorous track](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#rigorous-track) → Summary → [Exercises](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#exercises) → Where this leads. `{topic-header}` renders both prerequisites, the four objectives, 45 minutes and the status from the front matter. `check_all.py` reports 0 errors and 0 warnings. Both reviews mark it ✔. |
| 2 | Opens with a concrete question; the first formula appears only after motivation | ✔ | "You drop a stone from a bridge. How fast is it falling exactly one second later?" (L38) comes before $s(t) = 5t^2$ (L43). Both reviews: ✔. |
| 3 | Every definition has an "in words" unpacking, an example and a non-example | ✔ | [`def-calc-limit`](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#def-calc-limit): **In words** (the ε–δ game, with three points to notice), **Example** $\lim_{x\to a} x = a$, **Non-example** $\lim_{x \to 1} x \ne 1.5$ with a winning $\eps = 0.25$. The remark [`rem-calc-limit-value-irrelevant`](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#rem-calc-limit-value-irrelevant) has its own example ($g$) and non-example ($h$). |
| 4 | Every theorem: hypotheses justified (counterexamples for the subtle ones), proof per policy, strategy sentence | ✔ | `thm-calc-limit-unique` (policy R): a `{proof:proof} Rigorous track` dropdown, [`prf-calc-limit-unique`](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#prf-calc-limit-unique), `:enumerated: false`, opening with its strategy. The theorem adds no hypothesis ("Let $f$ and $a$ be as in the definition"); the proof rests on the definition's **domain clause**, and the rigorous-track aside "Why $f$ must be defined near $a$" shows uniqueness fails without it ($\sqrt{x}$ at $-1$). Review 1's F2 corrected which hypothesis the counterexample justifies ([thread](https://github.com/vronnblom/maths/pull/11#discussion_r4215926471)). |
| 5 | ≥ 3 worked examples covering the typical, the edge case, and an applied case; each ends with a **Check** | ✔ | Six, each ending with **Check**: typical, [linear ε–δ](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#eg-calc-limit-linear-eps-delta) (F) and [quadratic ε–δ](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#eg-calc-limit-quadratic-eps-delta) (R, with "Why the 1?"); edge cases, the [jump](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#eg-calc-limit-jump), oscillation ($\sin(1/x)$) and [unbounded values](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#eg-calc-limit-unbounded); applied, [the stone's speed](https://vronnblom.github.io/maths/calculus/limits/limit-of-a-function/#eg-calc-limit-average-speed), with units and a tolerance in m/s. |
| 6 | Widgets: ≥ 1, each with a "Try this", a text description, and keyboard operability | ✔ | Three figures, each a `{figure}` whose caption is the text description, followed by **Try this**: `wdg-calc-limit-average-speed` (`function-plot`, table and hole), `wdg-calc-limit-misleading-table` (the $\sin(\pi/x)$ table that misleads), `wdg-calc-limit-eps-delta` (the signature `epsilon-delta` widget, with a four-step guided game). Keyboard: Tab order, arrows, PageDown, Home/End and Enter/Space on every control, with a 2 px focus ring, in light and dark ([Playwright run](https://github.com/vronnblom/maths/pull/11#issuecomment-6060490139)); the reviewers did not repeat it. Every number in the captions and the Try this steps is tested against SymPy. The widget and the prose report what the widget observed, never a verdict on the limit (#10's rule; review 1, item 5). |
| 7 | Common mistakes are drawn from real student errors (≥ 2) | ✔ | Four: "The limit is just $f(a)$", "Letting $\delta$ depend on $x$", "Checking one $\eps$, or a few points", "Reading $\frac{0}{0}$ as the value of a limit", each ✗ / Why / ✓. |
| 8 | Exercises: ≥ 10, all tiers, hints/answer/solution complete, ≥ 1 `rigor` and ≥ 1 `applied` | ✔ | Eleven: 4 tier A, 4 tier B, 3 tier C, as 09 asks; 2 `rigor` (quadratic and square-root ε–δ proofs), 1 `applied` (the stone at $t = 2$), 1 `widget`. Each has at least one hint, exactly one Answer and a collapsed solution. The owner kept the linear ε–δ proof in tier B, because it imitates the worked example (F11, [ruling](https://github.com/vronnblom/maths/pull/11#discussion_r4218185209)). |
| 9 | 100 % verification coverage; every displayed step in examples checked or annotated | ✔ | `check_coverage.py` on this branch: `calculus/limits/limit-of-a-function.md [reviewed] 17/17 (100%): examples 6/6, exercises 11/11 (3 manual)`. The 14 computable labels are covered by passing tests; the 3 `manual` proofs were found correct and complete by both reviews and carry the owner's `maths.manual_checked` notes. The tests assert every displayed step, check each δ symbolically on each branch of a `min`, and test each implication on exact rational $(\eps, x)$ pairs up to the edge of the window; the "Facts from school" box has its own test. Disagreements: none, in both verifications. |
| 10 | All cross-references named; prerequisites linked; "where this leads" non-empty | ✔, one dead anchor | Every cross-page link is named and cites the part or property it uses: triangle inequality (b) ×3, `prop-calc-abs-interval` (a) and (e), properties 2, 4, 5 and 6 of the absolute value, the order part of the square-root remark, the Archimedean property, `def-calc-interval`, `def-calc-domain-range`. No `TODO link` is left (second pass). `{where-this-leads}` lists the dependent pages, with a hand-written sentence after it. **Found in this review:** the box is a labelled `{admonition}`, and the theme renders no `id` for it (checked in the server HTML and after hydration in headless Chromium), so the link "the facts from school" in `eg-calc-limit-sin-1-over-x` goes nowhere. The label still satisfies the checks. Follow-up: make the box a `{proof:remark}`, which does get an anchor; `templates/blocks.md` now says so. |
| 11 | Notation lint clean; reads well aloud (no undefined symbols, no "clearly") | ✔ | The notation lint and codespell are clean. $\sin$ is introduced by the labelled "Facts from school used on this page" box (`rem-calc-limit-school-facts`, in Why this matters) (F1, the owner's ruling) and $\pi$ comes from `calc-real-numbers`; there are no exponentials or logarithms. "Reads well aloud" is for the reader test below. |
| 12 | Renders well on mobile and in dark mode; accessibility ≥ 95 | ✔, with follow-ups | Lighthouse accessibility **95 on mobile, 100 on desktop** (was 91 and 96 before the contrast fix in `aa287ee`). No horizontal page scroll at 375 px in light or dark mode, all 42 dropdowns open by tap, no console errors. The findings below became rules of this freeze (displays) or follow-ups (theme). |

## Accessibility (item 12)

Measured by the Author with Lighthouse 12.8.2 and the preinstalled Chromium 141 against the
local build ([comment](https://github.com/vronnblom/maths/pull/11#issuecomment-6060490139)):

| Run | Before `aa287ee` | After |
|---|---|---|
| mobile (default preset, 412 px) | 91 | **95** |
| desktop (`--preset=desktop`) | 96 | **100** |

- **Fixed in vronnblom/maths#11** (`aa287ee`, `content/_static/custom.css`, site-wide): in light
  mode the theme's tinted header colours failed AA contrast (3.15, 4.41, 3.07, 3.35); they now
  use the Tailwind 700 shades (4.79, 4.84, 5.91, 4.88). Dark mode already passed (≥ 6.4).
- **Theme follow-ups, not fixable in our content:**
  - `button-name`: at narrow widths the search button (`.myst-search-bar`) has no accessible
    name. It is the only audit left failing on mobile.
  - The link "Solution to *Exercise N*" in a solution's header bar jumps to the exercise and
    leaves the solution closed (tapping the rest of the bar opens it), and logs a
    passive-listener error.
  - axe-core 4.10.3: `nested-interactive` (13: dropdown summaries that contain a link),
    `label-content-name-mismatch` on anchor links (weight 0), and a hover-only link contrast
    of 3.51.

## Mobile and dark mode (item 12)

Playwright at 375 px with touch, in light and dark mode
([comment](https://github.com/vronnblom/maths/pull/11#issuecomment-6060490139)):

- **No horizontal page scroll**, with every dropdown closed and with every dropdown open
  (`scrollWidth` = 375).
- **Seventeen displays and one table are wider than 375 px** and scroll sideways inside their
  own box. The widest are the two quantifier lines of the rigorous track (361 and 344 px
  hidden), the $(\sqrt{4.1} + \sqrt{3.9})^2$ line (255 px) and the uniqueness chain (182 px).
  In the first display, only "met" of "metres per second" shows until the reader scrolls.
  The page itself is left as merged (changing it is a content PR, guarded once the page is
  `verified`); the rule for every page from now on is in `CLAUDE.md`, "Displays on a phone":
  units in the sentence, long chains split with `aligned`, lists as bulleted lists.
- The "Facts from school" box began as a display equation, which was cut off at 375 px; it
  became a bulleted list.
- **Dark mode**: the theme follows the colour scheme; widgets redraw; the static SVGs of the
  prerequisite pages have white backgrounds so that they read in dark mode.
- **Dropdowns**: 42/42 open in both modes (2 proofs, 3 admonitions, 15 hints, 11 answers, 11
  solutions), apart from the solution-header link above.
- **Widgets by keyboard**: both widget types work in both modes; the misleading-table figure
  (`zoom: false`) has no controls, and Tab passes over it.

## Reader test (owner)

> **PLACEHOLDER: to be filled in by the owner.** 09 Phase 1a asks for the page to be "tested
> by a real reader (a student or colleague), and their feedback addressed". Not done yet.
>
> - Reader (role, not name): …
> - Date, and what they read (desktop / phone, light / dark): …
> - Did they reach the ε–δ definition from the question in Why this matters? Did the game make
>   sense? Which exercises did they try? …
> - Where they got stuck or misread something, and what was changed (PR links): …
> - Rubric item 11, "reads well aloud": …

## What the reviews found, and where it went

Neither review found wrong mathematics on the page. What they did find, here and on the three
prerequisite pages, is the evidence for the template freeze (the `tooling` PR that adds this
document lists each change and the comment behind it):

- the sign of each factor and the order rule before multiplying an inequality (#7, #8, #9);
- which hypothesis or definition clause a step rests on (#11 F2, F3, F8; #8);
- citing theorem parts and remark properties exactly, and only what a statement says (#11 F3,
  F4, F12, the TODO-link targets; #7 N2; #8 N1);
- the "Facts from school" box: the owner's ruling, its form, its label, the list of uses, and
  the proving page's curriculum entry (#11 F1, N1, N2, N4; #14);
- drafting ahead with `% TODO link` and resolving it after the prerequisite merges (#7, #9,
  #11);
- widget wording (#10 F1, F3, F4, F8; #11 F6, F7);
- displays on a phone (#11, above);
- the owner's sign-off, in a PR with CI green first (#12 and #11 merged with a red `checks`
  job; `calc-functions` was signed off directly on `main`).

## Still to do before `verified`

- [ ] The "Facts from school" box as a `{proof:remark}`, so that its link works (item 10); a
      wording-only content PR on the page.

- [ ] The reader test above, and its feedback addressed.
- [ ] The owner's sign-off of the proof checklist (09: "signed by the owner and the reviewer
      agent"; the reviewer sessions' checklists are in the two reviews above).
- [ ] Then, in a PR with CI green first: `status: verified` (coverage is already 17/17, every
      prerequisite is `reviewed`, and `check_labels.py --forward-refs` is clean).
