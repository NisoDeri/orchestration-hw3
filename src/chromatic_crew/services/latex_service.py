"""Assemble ``body.tex`` from per-section LaTeX fragments and compile the PDF.

Compilation runs the four-pass sequence (lualatex -> biber -> lualatex -> lualatex)
so cross-references and biber citations resolve. Compilation warnings (overfull
boxes, etc.) do not abort the build; they are surfaced via :func:`read_log` for
the QA agent. A missing output PDF is treated as a hard failure.
"""

import subprocess
from pathlib import Path

from chromatic_crew.constants import BIB_ENGINE, LATEX_ENGINE, LOG_OVERFULL, LOG_UNRESOLVED
from chromatic_crew.shared.exceptions import LatexCompileError


def assemble_body(fragments: dict[str, str], order: list[str], latex_dir: Path) -> Path:
    """Concatenate section fragments (in ``order``) into ``body.tex``."""
    parts = [fragments[sid] for sid in order if sid in fragments]
    out = Path(latex_dir) / "body.tex"
    out.write_text("\n\n".join(parts), encoding="utf-8")
    return out


def _passes(jobname: str) -> list[list[str]]:
    tex = [LATEX_ENGINE, "-interaction=nonstopmode", f"{jobname}.tex"]
    return [tex, [BIB_ENGINE, jobname], tex, tex]


def compile_pdf(latex_dir: Path, jobname: str = "main") -> Path:
    """Run the 4-pass compile in ``latex_dir``; return the produced PDF path."""
    latex_dir = Path(latex_dir)
    for cmd in _passes(jobname):
        subprocess.run(cmd, cwd=str(latex_dir), capture_output=True, text=True, check=False)
    pdf = latex_dir / f"{jobname}.pdf"
    if not pdf.exists():
        log = read_log(latex_dir, jobname)
        raise LatexCompileError(f"{jobname}.pdf not produced. Log tail:\n{log[-1500:]}")
    return pdf


def read_log(latex_dir: Path, jobname: str = "main") -> str:
    """Return the LaTeX log text (empty string if absent)."""
    log = Path(latex_dir) / f"{jobname}.log"
    return log.read_text(encoding="utf-8", errors="replace") if log.exists() else ""


def scan_warnings(log_text: str) -> dict[str, int]:
    """Count the warning classes the QA agent cares about."""
    return {
        "overfull_hbox": log_text.count(LOG_OVERFULL),
        "unresolved_refs": log_text.count(LOG_UNRESOLVED),
    }
