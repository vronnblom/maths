"""The build gate (scripts/myst_gate.sh, used by build_site.sh) on minimal fixture projects.

The `checks` job has no theme, so these run `myst build <page> --md --force` through the gate
instead of `--html`. That export runs mystmd's same parse and reference resolution and logs the
same ⛔️/⚠️ lines, without a theme and in about a second; a bare `myst build` or `--site`
without a site config reports the unknown directive but not the broken reference. The full
`--html` gate runs in the `build` job on the real site.
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
