import pytest

import chromatic_crew.services.latex_service as ls
from chromatic_crew.shared.exceptions import LatexCompileError


def test_assemble_body_orders_fragments(tmp_path):
    path = ls.assemble_body({"a": "AA", "b": "BB"}, ["b", "a"], tmp_path)
    text = path.read_text(encoding="utf-8")
    assert text.index("BB") < text.index("AA")


def test_scan_warnings_counts():
    log = "Overfull \\hbox (1.0pt too wide)\n?? undefined\n?? again"
    w = ls.scan_warnings(log)
    assert w["overfull_hbox"] == 1
    assert w["unresolved_refs"] == 2


def test_read_log_absent(tmp_path):
    assert ls.read_log(tmp_path) == ""


def test_compile_pdf_missing_output_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(ls.subprocess, "run", lambda *a, **k: None)
    with pytest.raises(LatexCompileError):
        ls.compile_pdf(tmp_path)


def test_compile_pdf_returns_pdf_when_present(tmp_path, monkeypatch):
    (tmp_path / "main.pdf").write_bytes(b"%PDF-1.5")
    monkeypatch.setattr(ls.subprocess, "run", lambda *a, **k: None)
    assert ls.compile_pdf(tmp_path).name == "main.pdf"
