# Tests for the repository checks

`npm run check` runs `uv run pytest tests -q` after `check_all.py` and codespell; CI runs it in
the `checks` job. These tests check the *checkers* (docs/plan/06 §6.4, "Checker tests"): each one
must fail on a fixture with exactly one deliberate defect, with the intended message, and pass on
the clean fixture and on the real tree. The mathematics is tested in `verify/`, whose harness
has its own tests in `verify/test_mathcheck.py`.

## Fixtures

Each folder in `fixtures/` is a tiny repository: `content/myst.yml` with a toc, a few pages,
often `content/calculus/curriculum.yml`, a `labels.lock`, and sometimes a `verify/` file.

| Fixture | Defect | Caught by |
|---|---|---|
| `clean` | none: `templates/topic.md` verbatim (a test keeps them identical), plus a lock with a tombstone | – |
| `bad-label` | `def-calc-Limit` | `check_labels.py` |
| `duplicate-label` | `def-calc-limit` on two pages | `check_labels.py` |
| `label-missing-from-lock` | a label that `labels.lock` lacks | `check_labels.py` |
| `removed-label-without-tombstone` | a locked label that left the content | `check_labels.py` |
| `kind-prefix-mismatch` | `thm-` on a `{proof:lemma}` | `check_labels.py` |
| `exercise-without-solution` | no `{solution}` | `check_labels.py` |
| `exercise-without-answer` | no Answer admonition | `check_labels.py` |
| `orphan-proof` | a proof after prose, without a `prf-` label | `check_labels.py` |
| `forward-reference-outside-closure` | a verified page cites a page outside its closure | `check_labels.py --forward-refs` |
| `forward-citation-in-proof` | a rigorous-track proof cites a lemma stated after its theorem | `check_labels.py --forward-refs` |
| `prerequisite-cycle` | `calc-functions` ↔ `calc-limit` in the curriculum | `graph.py check` |
| `unknown-prerequisite` | `calc-no-such-topic` | `graph.py check` |
| `reviewed-with-draft-prerequisite` | a reviewed page needs a draft one | `check_frontmatter.py` |
| `schema-violation` | `difficulty: 7` | `check_frontmatter.py` |
| `toc-mismatch` | a page that is not in the toc | `check_toc.py` |
| `lint-*` | one hit for each notation-lint rule | `check_all.py` (`notation_lint.py`) |
| `us-spelling` | "behavior" | codespell |
| `redirect-collision` | an alias that is a live page | `write_redirects.py` |
| `redirects` | none: two aliases, to show that redirects are written | – |
| `gate-*` | a broken reference, an unknown directive (and a clean page) | `scripts/myst_gate.sh` |
| `gate-katex-*` | an unknown macro, a command KaTeX doesn't support, a project macro missing an argument, an unclosed `\frac{1}{` | `scripts/myst_gate.sh` (mystmd's build-time KaTeX) |
| `widget-schema-violation` | a typo in the widget JSON (`tabel`) | `check_widgets.py` (schema) |
| `widget-missing-file` | `{anywidget}` names `widgets/no-such-widget.mjs` | `check_widgets.py` |
| `widget-figure-without-caption` | a widget figure with no caption (its text description) | `check_widgets.py` |
| `widget-unknown-id` | `maths.widgets` lists `no-such-widget` | `check_widgets.py` |
| `widget-epsilon-delta-out-of-range` | an `epsilon-delta` figure whose `eps` lies outside its `epsRange` | `check_widgets.py` (a rule the schema cannot express) |

`test_widget_checks.py` covers the rest of the widget rules on edited copies of `clean` (a widget
outside a figure, a non-`wdg-` label, wrong paths, invalid JSON, typos in nested keys, the rules
that JSON Schema cannot express, for `function-plot` and for `epsilon-delta`), runs
`widgets/_tests/fixtures/function-plot-invalid.json` and `epsilon-delta-invalid.json` through the
Python rules (the widget tests run the same tables through `widgets/_lib/`), and fails if
`widgets/_tests/fixtures/function-plot.json` or `epsilon-delta.json` is not what
`widgets/_tests/make_fixtures.py` writes now.

`test_plugin_build.py` assembles a project from `templates/topic.md` and
`templates/chapter-index.md` with the real `curriculum.yml`, builds it with
`plugins/topic-header.mjs` through the gate (`myst build --site` with a stub site template, so
no theme or network), and checks the resolved AST: prerequisite links, "coming soon" for
planned topics, the reverse links, the chapter table, and a build error for malformed front
matter. `uv run python tests/test_plugin_build.py <dir> [<theme URL>]` writes the project out to
look at it.

`test_checkers.py` also checks `maths.verify` (the page's own test path) and the reviewer's
notes in `maths.manual_checked` on edited copies of `clean`.

`test_verify_pipeline.py` runs the verification pipeline as `npm run verify` does
(`myst build --site` → `extract_answers.py` → `pytest` with `verify/conftest.py` →
`check_coverage.py`) on the project of `test_plugin_build.py`, with `templates/verify_test.py`
as its test, both verbatim: the template must pass and report 2 of 3 covered. Each verification
defect is that project with one edit (the `DEFECTS` table there): a `@covers` stub on a verified
page, an example test without a mathcheck assertion, an exercise test that never calls
`answer()`, a failing test, a reviewed page below 50 %, an answer outside the subset, a wrongly
rounded `numeric-5e-3` answer, an exercise without an Answer or with two, an unknown answer
type, a manual answer without the reviewer's note, an xfailed test, an `@covers` typo and a
stale AST; plus a stale or missing `_answers.json`, a stale `_coverage.json`, and a test outside
the page's `maths.verify` file.

`test_check_verified_edits.py` runs the verified-page edit guard on temporary git repositories:
an edited verified page fails, and passes when its test changed too, when its status is
lowered, or with the `typo-only` label; a draft page and prose outside blocks are free to change.

`fixtures/ast/topic.json` is mystmd's AST of `templates/topic.md`; `test_parser.py` compares it
with what `scripts/myst_source.py` reads. Regenerate it with `tests/make_ast_fixture.py` after
changing the template or upgrading mystmd.

A new check gets a new fixture with exactly one defect, and an entry in `DEFECTS` in
`test_checkers.py`, which also asserts that `check_all.py` reports nothing else on it.
