"""Load the document outline (sections + content slots) from config.

The outline is the machine-readable form of ``docs/BLUEPRINT.md``: it is what the
Planner/Writer agents consume so the small model fills predefined slots rather
than inventing structure.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

from chromatic_crew.shared.exceptions import ConfigError


@dataclass(frozen=True)
class Slot:
    """A fillable content slot within a section (figure, table, formula, ...)."""

    kind: str
    name: str
    spec: str


@dataclass
class SectionSpec:
    """The drafting brief for one section of the paper."""

    id: str
    title_en: str
    title_he: str
    language: str
    target_words: int
    purpose: str
    key_points: list[str] = field(default_factory=list)
    slots: list[Slot] = field(default_factory=list)


def load_outline(config_dir: Path) -> list[SectionSpec]:
    """Parse ``config/outline.json`` into ordered :class:`SectionSpec` objects."""
    path = Path(config_dir) / "outline.json"
    if not path.exists():
        raise ConfigError(f"missing outline: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    sections: list[SectionSpec] = []
    for raw in data["sections"]:
        slots = [Slot(**s) for s in raw.get("slots", [])]
        sections.append(
            SectionSpec(
                id=raw["id"],
                title_en=raw["title_en"],
                title_he=raw["title_he"],
                language=raw["language"],
                target_words=int(raw["target_words"]),
                purpose=raw["purpose"],
                key_points=list(raw.get("key_points", [])),
                slots=slots,
            )
        )
    return sections
