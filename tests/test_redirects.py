"""write_redirects.py: redirect pages for maths.aliases, BASE_URL-aware, failing on collisions."""

from __future__ import annotations

import write_redirects
from project import REPO

FIXTURES = REPO / "tests" / "fixtures"


def run(name, html, monkeypatch, base_url=""):
    monkeypatch.setenv("BASE_URL", base_url)
    return write_redirects.main([str(html), "--root", str(FIXTURES / name / "content")])


def test_writes_redirect_pages(tmp_path, monkeypatch):
    html = tmp_path / "html"
    (html / "about" / "notation").mkdir(parents=True)
    (html / "about" / "notation" / "index.html").write_text("live page")
    assert run("redirects", html, monkeypatch, base_url="/maths") == 0
    for old in ("about/symbols", "notation"):
        page = (html / old / "index.html").read_text()
        assert '<meta http-equiv="refresh" content="0; url=/maths/about/notation">' in page
        assert '<link rel="canonical" href="/maths/about/notation">' in page
    assert (html / "about" / "notation" / "index.html").read_text() == "live page"


def test_without_base_url(tmp_path, monkeypatch):
    html = tmp_path / "html"
    html.mkdir()
    assert run("redirects", html, monkeypatch) == 0
    assert 'url=/about/notation"' in (html / "notation" / "index.html").read_text()


def test_collision_with_a_live_page_fails(tmp_path, monkeypatch, capsys):
    html = tmp_path / "html"
    html.mkdir()
    assert run("redirect-collision", html, monkeypatch) == 1
    out = capsys.readouterr()
    assert "alias /about/notation collides with the live page about/notation.md" in out.out
    assert list(html.iterdir()) == []  # nothing written


def test_collision_with_a_built_file_fails(tmp_path, monkeypatch, capsys):
    html = tmp_path / "html"
    (html / "notation").mkdir(parents=True)
    (html / "notation" / "index.html").write_text("something the build wrote")
    assert run("redirects", html, monkeypatch) == 1
    assert "alias /notation collides with" in capsys.readouterr().out
    assert not (html / "about" / "symbols").exists()
