"""End-to-end SDK test with the live crew + compiler mocked out.

Exercises `build_paper` wiring (config -> outline -> per-section generation ->
markdown->latex -> assemble) against a temp copy of the project so the real
repo's content/ and latex/body.tex are untouched.
"""

import shutil

import chromatic_crew.sdk.sdk as sdkmod
from chromatic_crew.sdk import build_paper


def test_build_paper_no_compile(project_dir, monkeypatch, tmp_path):
    shutil.copytree(project_dir / "config", tmp_path / "config")
    (tmp_path / "latex").mkdir()

    monkeypatch.setattr(sdkmod, "build_all_agents", lambda cd, cfg: {})
    monkeypatch.setattr(
        sdkmod.crew_run,
        "generate_section",
        lambda sec, agents, gk, strategy="editor": (
            f"## {sec.title_en}\nBody text [[CITE:beeturia]]"
        ),
    )
    monkeypatch.setattr(sdkmod.crew_run, "generate_figures", lambda *a, **k: {})
    monkeypatch.setattr(sdkmod.crew_run, "generate_diagrams", lambda *a, **k: {})

    result = build_paper(tmp_path, compile_pdf=False)

    assert result.pdf_path is None
    assert "abstract" in result.section_order
    body = (tmp_path / "latex" / "body.tex").read_text(encoding="utf-8")
    assert "\\section{" in body
    assert "\\cite{beeturia}" in body
    assert (tmp_path / "content" / "model.md").exists()
