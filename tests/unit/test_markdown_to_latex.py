from chromatic_crew.services.markdown_to_latex import convert


def test_heading():
    assert "\\section{Intro}" in convert("## Intro", {}, "en")


def test_subsection():
    assert "\\subsection{Sub}" in convert("### Sub", {}, "en")


def test_bold_percent_and_asterisks():
    out = convert("**b** and 15% and L*a*b*", {}, "en")
    assert "\\textbf{b}" in out
    assert "15\\%" in out
    assert "L*a*b*" in out  # asterisks preserved, not treated as italic


def test_citation_marker():
    assert "\\cite{ref}" in convert("see [[CITE:ref]]", {}, "en")


def test_figure_marker():
    out = convert("[[FIGURE:F2|My caption]]", {}, "en")
    assert "includegraphics" in out
    assert "../assets/F2.png" in out
    assert "My caption" in out


def test_diagram_marker_inlines_tikz():
    out = convert("[[DIAGRAM:D1|Flow]]", {"D1": "\\begin{tikzpicture}\\end{tikzpicture}"}, "en")
    assert "tikzpicture" in out
    assert "Flow" in out


def test_table_conversion():
    md = "| A | B |\n| --- | --- |\n| 1 | 2 |"
    out = convert(md, {}, "en")
    assert "\\toprule" in out
    assert "A & B" in out
    assert "1 & 2" in out


def test_hebrew_paragraph_wrapped():
    out = convert("שלום world", {}, "he")
    assert "\\begin{hebrew}" in out
