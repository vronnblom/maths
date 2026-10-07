"""The files in .github/ that copy or depend on something else: the PR template's proof
checklist is 06 §6.3's, and the erratum form has the fields the page links pre-fill."""

from __future__ import annotations

import re

import yaml

from project import REPO

CHECKBOX = re.compile(r"^- \[ \] (.*(?:\n {2,}(?!- \[).*)*)", re.M)


def _items(text: str) -> list[str]:
    """The checklist items, whitespace collapsed, with the template's substitutions undone."""
    out = []
    for m in CHECKBOX.finditer(text):
        item = " ".join(m.group(1).split())
        item = item.replace(r"\varepsilon", r"\eps").replace("`docs/plan/07`", "[07](07-exercises.md)")
        out.append(item.replace("`docs/plan/04`", "[04](04-notation-and-style.md)"))
    return out


def test_pr_template_carries_the_proof_checklist():
    plan = (REPO / "docs/plan/06-quality-assurance.md").read_text(encoding="utf-8")
    checklist = _items(plan[plan.index("## 6.3"):plan.index("## 6.4")])
    template = (REPO / ".github/pull_request_template.md").read_text(encoding="utf-8")
    section = template[template.index("## Proof checklist"):template.index("## Widgets")]
    assert len(checklist) == 19
    assert _items(section) == checklist


def test_issue_forms_have_unique_ids_and_the_prefilled_fields():
    forms = {p.name: yaml.safe_load(p.read_text(encoding="utf-8"))
             for p in (REPO / ".github/ISSUE_TEMPLATE").glob("*.yml") if p.name != "config.yml"}
    assert set(forms) == {"erratum.yml", "new-topic.yml", "widget.yml"}
    for name, form in forms.items():
        ids = [f["id"] for f in form["body"] if "id" in f]
        assert len(ids) == len(set(ids)), name
    erratum = {f["id"]: f for f in forms["erratum.yml"]["body"] if "id" in f}
    assert {"page", "block", "type", "problem"} <= set(erratum)  # plugins/_lib/header.mjs fills `page`
    myst = (REPO / "content/myst.yml").read_text(encoding="utf-8")
    assert "/issues/new?template=erratum.yml" in myst
