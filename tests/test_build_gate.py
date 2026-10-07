"""The build gate (scripts/myst_gate.sh, used by build_site.sh) on minimal fixture projects.

The `checks` job has no theme, so these run `myst build <page> --md --force` through the gate
instead of `--html`. That export runs mystmd's same parse and reference resolution and logs the
same ⛔️/⚠️ lines, without a theme and in about a second; a bare `myst build` or `--site`
without a site config reports the unknown directive but not the broken reference. The full
`--html` gate runs in the `build` job on the real site.

The `gate-katex-*` fixtures settle docs/plan/05 §5.3's question with evidence: mystmd renders
every formula with its bundled KaTeX at build time, and each kind of KaTeX error (an unknown
macro, a command KaTeX doesn't support, a project macro missing an argument, an unclosed
`\\frac`) is a ⛔️ error that fails the gate, in `--md` here and in `--html` (checked when this
was written). So there is no separate KaTeX check (06 §6.4).
"""

from __future__ import annotations

import os
import shutil
import subprocess

import pytest

from project import REPO

FIXTURES = REPO / "tests" / "fixtures"
MYST_BIN = REPO / "node_modules" / ".bin"


def gate(name, tmp_path):
    if not (MYST_BIN / "myst").exists():
        pytest.fail("mystmd is not installed: run npm ci (the checks job does)")
    shutil.copytree(FIXTURES / name, tmp_path / name)
    env = {**os.environ, "PATH": f"{MYST_BIN}{os.pathsep}{os.environ.get('PATH', '')}"}
    return subprocess.run(
        ["bash", str(REPO / "scripts" / "myst_gate.sh"), "index.md", "--md", "--force"],
        cwd=tmp_path / name / "content", env=env, capture_output=True, text=True, timeout=120,
    )


def test_clean_page_passes_with_the_whitelisted_warning(tmp_path):
    r = gate("gate-clean", tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "extra key ignored: maths" in r.stdout


def test_broken_reference_fails(tmp_path):
    r = gate("gate-broken-reference", tmp_path)
    assert r.returncode == 1
    assert 'No target for internal reference "#thm-calc-squeeze"' in r.stdout
    assert "::error::MyST build produced errors or warnings" in r.stdout


def test_unknown_directive_fails(tmp_path):
    r = gate("gate-unknown-directive", tmp_path)
    assert r.returncode == 1
    assert "unknown directive: nosuchdirective" in r.stdout


KATEX = {
    "gate-katex-unknown-macro": "Undefined control sequence: \\foo",
    "gate-katex-unsupported-command": "Undefined control sequence: \\bbox",
    "gate-katex-macro-missing-argument": "Unexpected end of input in a macro argument, expected '}' at end of input: \\dv{f}",
    "gate-katex-unclosed-frac": "Unexpected end of input in a macro argument, expected '}' at end of input: \\frac{1}{",
}


@pytest.mark.parametrize("name", sorted(KATEX))
def test_katex_error_fails(name, tmp_path):
    r = gate(name, tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert f"⛔️ index.md:10 {KATEX[name]}" in r.stdout
    assert "::error::MyST build produced errors or warnings" in r.stdout


def test_katex_fixture_uses_the_real_macro():
    """The missing-argument fixture defines \\dv exactly as content/myst.yml does."""
    import yaml

    real = yaml.safe_load((REPO / "content" / "myst.yml").read_text(encoding="utf-8"))["project"]["math"]
    fixture = yaml.safe_load((FIXTURES / "gate-katex-macro-missing-argument" / "content" / "myst.yml").read_text(encoding="utf-8"))
    assert fixture["project"]["math"] == {"\\dv": real["\\dv"]}
