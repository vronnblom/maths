"""graph.py on the real curriculum: the import from docs/plan/08, ready, closure, mermaid."""

from __future__ import annotations

import graph
from project import REPO, Project

ROOT = REPO / "content"


def test_curriculum_counts_match_08():
    """docs/plan/08 §8.1: 11 chapters, 82 topic pages, 5 of them extension pages."""
    cur = Project(ROOT).curriculum_for_subject("calc")
    assert len(cur.chapters) == 11
    assert len(cur.topics) == 82
    assert sum(t.level == "extension" for t in cur.topics.values()) == 5


def _plan_only(tmp_path) -> Project:
    """The real curriculum with no pages written: what these tests assert must not change when
    Phase 1a writes the first topics."""
    import shutil

    (tmp_path / "content" / "calculus").mkdir(parents=True)
    shutil.copy(ROOT / "calculus" / "curriculum.yml", tmp_path / "content" / "calculus")
    (tmp_path / "content" / "myst.yml").write_text("version: 1\nproject:\n  toc:\n    - file: index.md\n")
    return Project(tmp_path / "content")


def test_ready_lists_topics_without_unmet_prerequisites(tmp_path):
    rows = graph.ready(_plan_only(tmp_path), "calc")
    labels = [r[0] for r in rows]
    assert "calc-real-numbers" in labels
    assert "calc-limit" not in labels  # its prerequisites are not written yet


def test_closure():
    g = graph.Graph(Project(ROOT))
    mvt = g.closure("calc-mean-value-theorem")
    assert {"calc-extreme-values", "calc-evt", "calc-continuity", "calc-limit", "calc-real-numbers"} <= mvt
    assert "calc-mean-value-theorem" not in mvt and "calc-lhopital" not in mvt
    # The subject index is read after all its topics, and after the chapter index pages that exist.
    topics = {label for label in g.nodes if g.nodes[label].kind == "topic"}
    chapters = {label for label in g.nodes if g.nodes[label].kind == "chapter"}
    assert len(topics) == 82 and "calc-limits-chapter" in chapters
    assert g.closure("calc-subject") == topics | chapters


def test_closure_cli(capsys):
    assert graph.main(["closure", "calc-limit"]) == 0
    assert capsys.readouterr().out.split() == ["calc-absolute-value-inequalities", "calc-functions", "calc-real-numbers"]
    assert graph.main(["closure", "calc-no-such-topic"]) == 2


def test_mermaid_lists_every_topic(tmp_path):
    text = graph.mermaid(_plan_only(tmp_path), "calc", base_url="/maths")
    assert text.count("```{mermaid}") == 12  # the chapter overview, then one per chapter
    for label in Project(ROOT).curriculum_for_subject("calc").topics:
        assert f'  {label.replace("-", "_")}["' in text
    assert "class calc_real_numbers planned" in text


def test_mermaid_links_written_pages_with_base_url(tmp_path):
    import shutil

    shutil.copytree(REPO / "tests" / "fixtures" / "clean", tmp_path / "clean")
    text = graph.mermaid(Project(tmp_path / "clean" / "content"), "calc", base_url="/maths")
    assert 'click calc_limit "/maths/calculus/limits/limit-of-a-function"' in text
    assert "class calc_limit draft" in text


def _project(tmp_path, depends_on, calc_pre):
    (tmp_path / "content" / "calculus").mkdir(parents=True)
    (tmp_path / "content" / "linear-algebra").mkdir(parents=True)
    (tmp_path / "content" / "myst.yml").write_text("version: 1\nproject:\n  toc:\n    - file: calculus/index.md\n")
    (tmp_path / "content" / "calculus" / "index.md").write_text(
        "---\ntitle: Calculus\nlabel: calc-subject\ndescription: x\nmaths:\n  kind: subject\n  subject: calc\n"
        f"  status: draft\n  depends_on: {depends_on}\n---\n")
    topic = "      - {{label: {l}, file: ch/{l}.md, title: T, level: core, prerequisites: {p}, objectives: [A., B.], results: []}}\n"
    (tmp_path / "content" / "calculus" / "curriculum.yml").write_text(
        "subject: calc\nchapters:\n  - slug: ch\n    title: Ch\n    topics:\n"
        + topic.format(l="calc-a", p="[]") + topic.format(l="calc-b", p="[calc-a]") + topic.format(l="calc-c", p=calc_pre))
    (tmp_path / "content" / "linear-algebra" / "curriculum.yml").write_text(
        "subject: linalg\nchapters:\n  - slug: ch\n    title: Ch\n    topics:\n" + topic.format(l="linalg-v", p="[]"))
    return Project(tmp_path / "content")


def _check(project):
    from project import Reporter

    rep = Reporter(quiet=True)
    graph.check(project, rep)
    return rep


def test_cross_subject_edges_need_depends_on(tmp_path):
    rep = _check(_project(tmp_path, "[]", "[calc-b, linalg-v]"))
    assert [d.message for d in rep.errors] == [
        "calc-c: prerequisite linalg-v is in subject linalg, which calc-subject does not list in maths.depends_on"]
    rep = _check(_project(tmp_path / "ok", "[linalg]", "[calc-b, linalg-v]"))
    assert not rep.diagnostics


def test_redundant_transitive_edge_is_a_warning(tmp_path):
    rep = _check(_project(tmp_path, "[]", "[calc-a, calc-b]"))
    assert not rep.errors
    assert [d.message for d in rep.warnings] == [
        "calc-c: prerequisite calc-a is already implied by calc-b; list direct prerequisites only"]
