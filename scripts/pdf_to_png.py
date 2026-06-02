"""Render a PDF to per-page PNGs under logs/ for visual QA. Not part of the package."""

import sys
from pathlib import Path

import fitz  # PyMuPDF

root = Path(__file__).parents[1]
pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "latex" / "main.pdf"
out = root / "logs"
out.mkdir(exist_ok=True)

doc = fitz.open(str(pdf))
print("pages:", doc.page_count)
for i in range(doc.page_count):
    doc[i].get_pixmap(dpi=110).save(str(out / f"pg-{i + 1:02d}.png"))
print("rendered", doc.page_count, "pages to logs/")
