"""Deterministic Markdown -> LaTeX conversion for the controlled subset the crew
emits: headings, booktabs tables, figure/diagram/citation slot markers, inline
emphasis, math passthrough, and BiDi Hebrew wrapping.

Slot marker formats (the Writer is instructed to use these):
  [[FIGURE:NAME|caption]]   [[DIAGRAM:NAME|caption]]   [[CITE:bibkey]]
"""

import re

_HEB = re.compile(r"[֐-׿]")
_FIG = re.compile(r"\[\[FIGURE:([^\]|]+)(?:\|([^\]]*))?\]\]")
_DIAG = re.compile(r"\[\[DIAGRAM:([^\]|]+)(?:\|([^\]]*))?\]\]")
_CITE = re.compile(r"\[\[CITE:([^\]]+)\]\]")


def _inline(text: str) -> str:
    # Bold only. '*' is deliberately left alone: it appears in scientific notation
    # (e.g. CIELAB L*a*b*) and inside math, where treating it as italic corrupts output.
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\\)%", r"\\%", text)
    text = re.sub(r"(?<!\\)#", r"\\#", text)
    return _CITE.sub(r"\\cite{\1}", text)


def _wrap_he(text: str) -> str:
    """Wrap Hebrew-containing heading/caption text so polyglossia applies RTL + font."""
    return f"\\texthebrew{{{text}}}" if _HEB.search(text) else text


def _table(block: list[str]) -> str:
    rows = [r.strip().strip("|").split("|") for r in block]
    header, body = rows[0], rows[2:]
    ncol = len(header)
    out = [
        "\\begin{table}[h]\\centering\\small",
        "\\setlength{\\tabcolsep}{4pt}",
        "\\begin{tabular}{" + "l" * ncol + "}",
        "\\toprule",
    ]
    out.append(" & ".join(_inline(c.strip()) for c in header) + r" \\")
    out.append("\\midrule")
    for r in body:
        out.append(" & ".join(_inline(c.strip()) for c in r) + r" \\")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}"]
    return "\n".join(out)


def _figure(name: str, caption: str) -> str:
    return (
        "\\begin{figure}[h]\\centering\n"
        f"\\includegraphics[width=0.8\\textwidth]{{../assets/{name}.png}}\n"
        f"\\caption{{{_wrap_he(_inline(caption))}}}\n\\end{{figure}}"
    )


def _diagram(tikz: str, caption: str) -> str:
    cap = _wrap_he(_inline(caption))
    return f"\\begin{{figure}}[h]\\centering\n{tikz}\n\\caption{{{cap}}}\n\\end{{figure}}"


def _is_table_start(lines: list[str], i: int) -> bool:
    return (
        lines[i].strip().startswith("|")
        and i + 1 < len(lines)
        and set(lines[i + 1].strip()) <= set("|-: ")
        and "-" in lines[i + 1]
    )


def convert(md: str, tikz_map: dict[str, str], language: str) -> str:
    """Convert one section's Markdown to a LaTeX fragment."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            out.append("\\section{" + _wrap_he(_inline(line[3:].strip())) + "}")
        elif line.startswith("### "):
            out.append("\\subsection{" + _wrap_he(_inline(line[4:].strip())) + "}")
        elif _is_table_start(lines, i):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(_table(block))
            continue
        elif _FIG.search(line) or _DIAG.search(line):
            # Markers may be inline within a sentence: emit the surrounding prose
            # (marker removed) AND the float, so the paragraph text is preserved.
            floats: list[str] = [
                _figure(m.group(1), m.group(2) or m.group(1)) for m in _FIG.finditer(line)
            ]
            floats += [
                _diagram(tikz_map.get(m.group(1), ""), m.group(2) or m.group(1))
                for m in _DIAG.finditer(line)
            ]
            text = _DIAG.sub("", _FIG.sub("", line))
            text = re.sub(r"\((?:Figure|Diagram|איור|תרשים)\s*\)", "", text).strip(" .")
            if text:
                if language in ("he", "bilingual") and _HEB.search(text):
                    out.append("\\begin{hebrew}" + _inline(text) + "\\end{hebrew}")
                else:
                    out.append(_inline(text))
            out.extend(floats)
        elif line.strip() == "":
            out.append("")
        elif language in ("he", "bilingual") and _HEB.search(line):
            out.append("\\begin{hebrew}" + _inline(line) + "\\end{hebrew}")
        else:
            out.append(_inline(line))
        i += 1
    return "\n".join(out)
