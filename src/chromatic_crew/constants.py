"""Immutable project constants.

Only true constants live here — physical/structural facts about the project that
are not user-tunable. Anything a user might change belongs in `config/` instead.
"""

from enum import StrEnum

# Slot markers the Writer leaves in Markdown for downstream agents to fill.
SLOT_FORMULA = "[[FORMULA:{name}]]"
SLOT_FIGURE = "[[FIGURE:{name}]]"
SLOT_TABLE = "[[TABLE:{name}]]"
SLOT_DIAGRAM = "[[DIAGRAM:{name}]]"

# Number of LaTeX passes required for cross-refs + biber citations to resolve.
LATEX_PASSES = 4
LATEX_ENGINE = "lualatex"
BIB_ENGINE = "biber"

# Log markers the QA agent scans for.
LOG_OVERFULL = "Overfull \\hbox"
LOG_UNRESOLVED = "??"


class Language(StrEnum):
    """Per-section language directive."""

    EN = "en"
    HE = "he"
    BILINGUAL = "bilingual"


class Slot(StrEnum):
    """Kinds of fillable content slots."""

    FORMULA = "formula"
    FIGURE = "figure"
    TABLE = "table"
    DIAGRAM = "diagram"
