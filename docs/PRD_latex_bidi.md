# PRD — LaTeX BiDi Rendering Pipeline

## Purpose
Render the generated content into a polished PDF with correct Hebrew↔English
bidirectional typesetting, real math, figures, TikZ diagrams, tables, and resolved
clickable citations.

## Engine & packages
- **LuaLaTeX** (best Hebrew shaping; chosen over XeLaTeX/pdfLaTeX) via MiKTeX.
- **polyglossia** with `\setdefaultlanguage{english}` + `\setotherlanguage{hebrew}`;
  Hebrew via `\newfontfamily\hebrewfont[Script=Hebrew]{David}` (Windows system font).
- **amsmath/mathtools** (formulas), **booktabs** (tables), **tikz** (`arrows.meta`,
  `positioning`), **biblatex + biber** (citations), **hyperref** (clickable refs),
  **fancyhdr** (headers/footers), **geometry** (margins).

## BiDi strategy
- Hebrew paragraphs are wrapped in `\begin{hebrew}...\end{hebrew}`; English technical
  terms inside Hebrew are wrapped `\textenglish{...}` so numbers/units/Latin terms flow
  correctly. LuaLaTeX's luabidi (via polyglossia) handles the reordering.

## Assembly & conversion
- `markdown_to_latex.convert` maps the controlled Markdown subset → LaTeX: headings,
  booktabs tables, slot markers (`[[FIGURE:NAME|cap]]`, `[[DIAGRAM:NAME|cap]]`,
  `[[CITE:key]]`), inline emphasis, math passthrough, Hebrew wrapping.
- `latex_service.assemble_body` concatenates fragments in outline order into `body.tex`;
  `main.tex` provides cover/TOC/headers/bibliography and `\input{body}`.

## Compilation
Four passes: `lualatex → biber → lualatex → lualatex` so `\ref`/`\cite` resolve.
`scan_warnings` counts `Overfull \hbox` and unresolved `??` for the QA loop. A missing
output PDF is a hard error.

## Acceptance
PDF compiles; no table exceeds the margin; BiDi is not garbled; every `\cite`/`\ref`
is clickable and resolved; formulas render as real math (not flat text).
