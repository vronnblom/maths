"""schema/page.schema.json accepts every template and existing page, and its conditional rules."""

from __future__ import annotations

import copy
import json

import jsonschema
import pytest
import yaml

from project import REPO, read_page

SCHEMA = json.loads((REPO / "schema" / "page.schema.json").read_text(encoding="utf-8"))
V = jsonschema.Draft202012Validator(SCHEMA)


def fm(path):
    return read_page(path.parent, path.name).fm


@pytest.mark.parametrize("name", ["topic.md", "chapter-index.md", "subject-index.md"])
def test_templates_validate(name):
    assert not list(V.iter_errors(fm(REPO / "templates" / name)))


def errors(data):
    return [e.message for e in V.iter_errors(data)]


TOPIC = fm(REPO / "templates" / "topic.md")


def test_reviewed_needs_reviewers_and_verify():
    d = copy.deepcopy(TOPIC)
    d["maths"]["status"] = "reviewed"
    del d["maths"]["verify"]
    msgs = errors(d)
    assert any("'verify' is a required property" in m for m in msgs)
    assert any("should be non-empty" in m or "is too short" in m for m in msgs)


@pytest.mark.parametrize(
    "path, value, fragment",
    [
        (("label",), "calc-limits-chapter", "should not be valid"),
        (("label",), "site-limit", "should not be valid"),
        (("maths", "objectives", 0), "Understand limits.", "does not match"),
        (("maths", "est_minutes"), 120, "greater than the maximum"),
        (("maths", "depends_on"), ["linalg"], "is not one of"),
        (("maths", "subject"), "maths", "is not one of"),
        (("title",), "A" * 61, "is too long"),
    ],
)
def test_topic_rules(path, value, fragment):
    d = copy.deepcopy(TOPIC)
    node = d
    for k in path[:-1]:
        node = node[k]
    node[path[-1]] = value
    assert any(fragment in m for m in errors(d)), errors(d)


def test_meta_page_has_no_subject():
    d = {"title": "Notation", "label": "site-notation", "description": "x", "maths": {"kind": "meta", "status": "draft", "subject": "calc"}}
    assert errors(d)
    del d["maths"]["subject"]
    assert not errors(d)


def test_tags_vocabulary_covers_the_templates():
    tags = yaml.safe_load((REPO / "content" / "tags.yml").read_text(encoding="utf-8"))["tags"]
    assert set(TOPIC["tags"]) <= set(tags)
