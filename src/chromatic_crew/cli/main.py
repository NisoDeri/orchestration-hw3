"""CLI — a thin shell over the SDK. No business logic lives here.

Usage:
    uv run python -m chromatic_crew              # generate + compile the PDF
    uv run python -m chromatic_crew --no-compile # generate + assemble only
"""

import argparse
from pathlib import Path

from chromatic_crew import __version__
from chromatic_crew.sdk import build_paper


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="chromatic-crew",
        description="Generate the bilingual (Hebrew/English) LaTeX article via a CrewAI team.",
    )
    parser.add_argument(
        "--project", default=str(Path.cwd()), help="Project root (holds config/, latex/)."
    )
    parser.add_argument(
        "--no-compile", action="store_true", help="Generate + assemble but skip PDF compilation."
    )
    parser.add_argument(
        "--no-generate",
        action="store_true",
        help="Skip the crew; reuse existing content/ files (assemble + compile only).",
    )
    parser.add_argument("--version", action="version", version=f"chromatic-crew {__version__}")
    args = parser.parse_args(argv)

    result = build_paper(
        Path(args.project), generate=not args.no_generate, compile_pdf=not args.no_compile
    )
    print("sections:", ", ".join(result.section_order))
    print("pdf:", result.pdf_path)
    print("warnings:", result.warnings)
    print("cost:", result.cost_report)
    return 0
