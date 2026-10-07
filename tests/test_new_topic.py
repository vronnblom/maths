"""scripts/new_topic.py, the scaffolder behind /new-topic: a scaffold passes every check, in
curriculum order in the toc, and the script refuses what it must."""

from __future__ import annotations

import random
import shutil

import check_all
import new_topic
from project import REPO, Project, Reporter


def _repo(tmp_path):
    """A copy of the content and labels.lock (widgets/ linked), so the scaffold can be written."""
    shutil.copytree(REPO / "content", tmp_path / "content", ignore=shutil.ignore_patterns("_build", "_generated"))
    shutil.copy(REPO / "labels.lock", tmp_path / "labels.lock")
    (tmp_path / "widgets").symlink_to(REPO / "widgets")
    return tmp_path / "content"


def _unwritten(root):
    p = Project(root)
    return [label for label in p.planned if label not in p.page_by_label]


def _check(root):
    rep = Reporter(quiet=True)
    check_all.run(Project(root), rep)
    return [str(d) for d in rep.diagnostics]


def test_every_topic_scaffolds_cleanly_in_any_order(tmp_path):
    root = _repo(tmp_path)
    labels = _unwritten(root)
    random.Random(0).shuffle(labels)  # every way of inserting into the toc
    project = Project(root)  # scaffold() reads the toc and the files from disk, so one load will do
    for label in labels:
        new_topic.scaffold(project, label)
    assert new_topic.main(["--root", str(root), "--stubs", labels[0]]) == 0
    import check_labels
    assert check_labels.main(["--root", str(root), "--update-lock"]) == 0
    assert _check(root) == []
    p = Project(root)
    cur = p.curriculum_for_subject("calc")
    toc = [e.file for e in p.toc if e.file and e.file.startswith("calculus/") and not e.file.endswith("index.md")]
    assert toc == [cur.topics[label].file for _s, _t, ls, _l in cur.chapters for label in ls]


def test_scaffold_refuses_unknown_labels_and_existing_pages(tmp_path, capsys):
    root = _repo(tmp_path)
    label = _unwritten(root)[0]
    assert new_topic.main(["--root", str(root), "calc-no-such-topic"]) == 2
    assert "not a topic in any curriculum.yml" in capsys.readouterr().err
    assert new_topic.main(["--root", str(root), label]) == 0
    before = (root / "myst.yml").read_text()
    assert new_topic.main(["--root", str(root), label]) == 2
    assert "already exists" in capsys.readouterr().err
    assert (root / "myst.yml").read_text() == before


def test_stubs_cover_every_example_and_exercise(tmp_path):
    root = _repo(tmp_path)
    label = _unwritten(root)[0]
    assert new_topic.main(["--root", str(root), label]) == 0
    topic = Project(root).planned[label]
    page = root / topic.file
    slug = label  # eg-<topic label>-…, as check_labels.py requires
    page.write_text(page.read_text().replace("## Common mistakes", f"""\
:::{{proof:example}} An example
:label: eg-{slug}-first
Text.
:::

## Common mistakes""").replace("## Where this leads", f"""\
::::{{exercise}} An exercise
:label: exr-{slug}-first
:class: tier-a
Compute $1 + 1$.

:::{{admonition}} Answer
:class: dropdown answer
$2$
:::
::::

::::{{solution}} exr-{slug}-first
:label: sol-{slug}-first
:class: dropdown
$1 + 1 = 2$.
::::

## Where this leads"""))
    assert new_topic.add_stubs(Project(root), label) == [f"eg-{slug}-first", f"exr-{slug}-first"]
    assert new_topic.add_stubs(Project(root), label) == []
    test = (tmp_path / new_topic._verify_path(topic.file)).read_text()
    assert test.count("@covers(") == 2 and f"def test_eg_{slug.replace('-', '_')}_first()" in test
    compile(test, "test", "exec")
