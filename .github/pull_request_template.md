<!--
The fixed PR description (docs/plan/10 §10.4, 11 §11.5). Keep the sections that apply to your
PR type and delete the rest. Run `npm run all` before pushing: it is exactly what CI runs.
-->

## Type

<!-- One of the PR types in docs/plan/10 §10.2, with its branch name. One topic per PR. -->
- [ ] `topic` (`topic/<label>`): one topic page, its verify test and widget configs
- [ ] `chapter-index` (`chapter/<label>`)
- [ ] `widget` (`widget/<name>`)
- [ ] `curriculum` (`curriculum/…`): `curriculum.yml` and 08, approved by the maintainer
- [ ] `tooling` (`tooling/…`): scripts, CI, plugin, templates
- [ ] `erratum` (`erratum/<issue>`): fixes #<!-- issue number -->, with a regression test

## Summary

<!-- Topic and chapter PRs: the mathematics in a few sentences: what is defined, what is
proved and how, which examples and exercises. Other PRs: what changes and why. -->

## Results and proof policies

<!-- Topic PRs: every result of the curriculum entry, with the policy from curriculum.yml
(F full proof in core, R rigorous track, S sketch, D deferred, or a combination) and where
the proof is. -->

| Label | Statement (short) | Policy | Notes |
|---|---|---|---|
| `thm-…` | | F | |

## Verification coverage

<!-- Paste what `check_coverage.py` printed at the end of `npm run verify`. A draft at 0 %
is expected until the Verifier has written the tests (/verify-topic). -->

```text
Verification coverage (eg-/exr- labels covered by passing tests, or manual with a reviewer's note):
  …
```

Disagreements between the page and SymPy (label, the page's claim, the test's result,
evidence), or "none":

## Proof checklist (topic and chapter PRs)

<!-- docs/plan/06 §6.3, copied here (tests/test_github_templates.py keeps the two in step). The
Author ticks what they checked; the Reviewer (/review-math) and the owner go through it again. -->

**Statements**
- [ ] Every hypothesis is stated, and the statement is false without each one (a remark or the
  rigorous track gives a counterexample for the non-obvious ones).
- [ ] Domains are explicit: "for all $x$ in $I$", "$a < b$", "$f$ continuous on $[a,b]$ and
  differentiable on $(a,b)$".
- [ ] Quantifier order is correct ($\forall \varepsilon\, \exists \delta$, not $\exists \delta\, \forall \varepsilon$).
- [ ] The statement matches the standard literature version, or the difference is remarked on.

**Proofs**
- [ ] The strategy is stated in the first sentence.
- [ ] Every hypothesis is used (an unused one means either the statement is weaker than it
  could be, or the proof is wrong).
- [ ] Every cited result is on the same page earlier, or in the page's prerequisite closure
  (also checked by CI's forward-reference check). On the same page, a proof may cite
  only results stated before the result it proves (02 §2.5).
- [ ] **No circularity**. Known traps in calculus:
  - $\lim_{x\to 0} \frac{\sin x}{x} = 1$ must not use L'Hôpital or $(\sin x)' = \cos x$
    (the derivative of sine is derived *from* this limit). Use the geometric squeeze argument.
  - The derivative of $e^x$ must follow from how $e$ / $\exp$ was *defined* on the
    preliminaries page. That definition choice is fixed in 08 and must be used consistently.
  - The MVT proof uses Rolle, which uses the EVT and Fermat. None of them may use the MVT.
  - Taylor's theorem must not assume the Taylor series converges.
- [ ] Edge cases: division by zero, $h \to 0$ with $h$ negative, $\Delta u = 0$ in the chain
  rule (the classic flawed proof), endpoints of intervals, empty sets.
- [ ] Inequalities: the direction is preserved when multiplying (sign of the factor stated).
- [ ] "Choose $\delta = \min(\dots)$" proofs: verify the final inequality chain with that δ.
- [ ] The proof matches its declared policy (F/R/S/D in 08).

**Examples and exercises**
- [ ] Each step is covered by a verification test or annotated as reviewed prose.
- [ ] The answer is in simplest conventional form (rationalised denominators, $\ln$ combined).
- [ ] The difficulty tier fits (`docs/plan/07`).
- [ ] The solution uses only methods available at this point in the graph.

**Pedagogy**
- [ ] Intuition comes before formalism; at least one picture or widget per main concept.
- [ ] Common mistakes reflect real student errors.
- [ ] Notation follows `docs/plan/04` (`check_all.py` lints the mechanical part:
  bare `\log`, `\sin^{-1}`, raw `dx` in integrals, `]a, b[`, `\mathrm{e}`, degrees,
  "clearly"/"obviously"; 04 §4.4).

## Widgets

<!-- New or changed widgets: a screenshot of each on the built site (the `site` artifact of
the CI build, served with `npx serve`), and what you tried with the keyboard. -->

## Checks

- [ ] `npm run all` is green locally.
- [ ] Labels: no label renamed or removed; new labels are in `labels.lock`.
- [ ] Status: still `draft`, unless the owner changes it (authors and agents never set
  `reviewed`/`verified`, `reviewed_by` or `maths.manual_checked`).
- [ ] Sources and licence: I have not copied from incompatible sources (anything NC or
  proprietary, docs/plan/07 §7.4); every adapted CC BY / CC BY-SA source is listed in
  `maths.sources`.
