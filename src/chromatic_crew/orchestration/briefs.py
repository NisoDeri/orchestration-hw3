"""Architect-authored prompt builders: turn a SectionSpec into precise briefs.

This is where the Senior Architect's planning is captured as deterministic prompt
construction. The global deadpan style contract plus per-section slot instructions
constrain a small local model to produce on-spec output. English is always drafted
first (the model's strongest language); Hebrew is produced by the translator agent
and finalized by the architect/editor.
"""

from chromatic_crew.orchestration.outline import SectionSpec, Slot

STYLE_CONTRACT = (
    "You are writing for a peer-reviewed journal in a strictly DEADPAN CLINICAL register.\n"
    "Rules:\n"
    "- Absolute seriousness. No jokes, no slang, no winking. The humour exists ONLY in treating an\n"
    "  absurd subject with total rigour.\n"
    "- SUBJECT: human STOOL / faeces (excreta), NOT urine. Dietary pigments colour the STOOL.\n"
    "  Parameters of interest: faecal colour (CIEDE2000), stool consistency (Bristol Stool Scale),\n"
    "  faecal pH, and luminal transit. Where 'beeturia' appears it denotes FAECAL pigmentation here.\n"
    "- Use precise clinical/colorimetric terminology (betalain, chromophore, luminal transit,\n"
    "  spectrophotometric, pharmacokinetic, Bristol Stool Scale, faecal pH).\n"
    "- Hedge like a scientist ('our model suggests', 'under the simplifying assumption').\n"
    "- Output GitHub-flavoured Markdown. Use $...$ and $$...$$ for math. Do NOT invent sections,\n"
    "  headers, or content beyond what is requested.\n"
)

_LANG_NOTE = {
    "en": "Write in English.",
    "he": "Write in clear English; it will be professionally translated to Hebrew afterwards.",
    "bilingual": "Write in English; a Hebrew translation will be appended after it.",
}


def _slot_lines(slots: list[Slot]) -> str:
    lines: list[str] = []
    for s in slots:
        if s.kind == "formula" and s.name != "none":
            lines.append(f"- Include formula [{s.name}] as display math, kept correct: {s.spec}")
        elif s.kind == "figure":
            lines.append(
                f"- Reference figure {s.name} via marker [[FIGURE:{s.name}]] with a caption; do not draw it."
            )
        elif s.kind == "table":
            lines.append(f"- Include a Markdown table [{s.name}] with columns: {s.spec}")
        elif s.kind == "diagram":
            lines.append(
                f"- Reference diagram {s.name} via marker [[DIAGRAM:{s.name}]] with a caption."
            )
        elif s.kind == "citation":
            lines.append(f"- Cite via marker [[CITE:{s.name}]] where relevant.")
        elif s.kind == "bidi":
            lines.append(f"- Keep these English terms in Latin script within Hebrew: {s.spec}")
    return "\n".join(lines) if lines else "- (no special slots)"


def writer_brief(section: SectionSpec) -> str:
    """Detailed drafting brief for one section."""
    points = "\n".join(f"  - {p}" for p in section.key_points)
    return (
        f"{STYLE_CONTRACT}\n"
        f"SECTION: {section.title_en} (id={section.id}). {_LANG_NOTE[section.language]} "
        f"TARGET LENGTH: ~{section.target_words} words.\n"
        f"PURPOSE: {section.purpose}\n"
        f"KEY POINTS TO COVER:\n{points}\n"
        f"SLOT INSTRUCTIONS:\n{_slot_lines(section.slots)}\n"
        f"Write only this section's body. Begin with the heading '## {section.title_en}'."
    )


def translator_brief(english_md: str) -> str:
    """Brief to render an English section into BiDi-safe academic Hebrew."""
    return (
        "Translate the following scientific section into natural ACADEMIC HEBREW.\n"
        "OUTPUT RULES (critical):\n"
        "- Output ONLY the Hebrew translation. Do NOT include the English original.\n"
        "- Do NOT repeat yourself; translate the whole text exactly once, then stop.\n"
        "- No commentary, no notes, and no language other than Hebrew (Latin-script terms aside).\n"
        "- Wrap English technical terms in Latin script as \\textenglish{...} for correct BiDi.\n"
        "- Keep numbers, units, math ($...$), and [[...]] markers verbatim; keep the '## ' heading (translate its text).\n\n"
        "TEXT TO TRANSLATE:\n"
        f"{english_md}"
    )


def figure_brief(name: str, spec: str) -> str:
    """Brief for a self-contained matplotlib snippet."""
    return (
        "Write a SELF-CONTAINED matplotlib snippet (Python only, no prose, no code fences).\n"
        f"FIGURE {name}: {spec}\n"
        "Requirements: use only the pre-imported `plt` (matplotlib.pyplot) and `np` (numpy). "
        "Generate plausible synthetic data. Label axes, add a title and legend where useful. "
        "Save exactly one PNG via plt.savefig(out_path, dpi=150, bbox_inches='tight')."
    )


def tikz_brief(name: str, spec: str) -> str:
    """Brief for a compilable TikZ diagram."""
    return (
        "Output ONLY a compilable LaTeX tikzpicture environment (no prose, no fences).\n"
        f"DIAGRAM {name}: {spec}\n"
        "Use \\begin{tikzpicture}...\\end{tikzpicture} with libraries arrows.meta and positioning. "
        "Stay within \\textwidth; use rounded-corner nodes and -{Stealth} arrows."
    )
