"""Run the crew to generate per-section content + assets (live LLM calls).

Every model call is routed through the gatekeeper. English is drafted first, then
Hebrew sections are translated; figures are produced by executing the Figure
agent's matplotlib code. This module is excluded from coverage because it requires
a live engine; its pure helpers (e.g. fence stripping) are unit-tested separately.
"""

from pathlib import Path

from crewai import Crew, Task

from chromatic_crew.orchestration import briefs
from chromatic_crew.orchestration.outline import SectionSpec
from chromatic_crew.services.figure_service import render_figure
from chromatic_crew.shared.gatekeeper import Gatekeeper
from chromatic_crew.shared.logger import get_logger

logger = get_logger("chromatic_crew.crew_run")


def strip_code_fences(text: str) -> str:
    """Remove leading/trailing Markdown code fences from a model response."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _run(agent, prompt: str, gatekeeper: Gatekeeper, service: str = "ollama") -> str:
    task = Task(description=prompt, expected_output="The requested content only.", agent=agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    return gatekeeper.execute(lambda: str(crew.kickoff()), service=service)


def generate_section(
    section: SectionSpec, agents: dict, gatekeeper: Gatekeeper, strategy: str = "editor"
) -> str:
    """Draft a section in English; optionally translate via the local agent.

    With the default ``editor`` strategy the crew produces English only, and Hebrew
    sections are translated by the architect/editor afterwards — local models proved
    unreliable at Hebrew (repetition loops, language leakage). Set ``strategy='agent'``
    to use the local translator instead.
    """
    english = _run(agents["writer"], briefs.writer_brief(section), gatekeeper)
    if strategy != "agent":
        return english
    if section.language == "he":
        return _run(agents["translator"], briefs.translator_brief(english), gatekeeper)
    if section.language == "bilingual":
        hebrew = _run(agents["translator"], briefs.translator_brief(english), gatekeeper)
        return f"{english}\n\n{hebrew}"
    return english


def generate_figures(
    section: SectionSpec, agents: dict, gatekeeper: Gatekeeper, assets_dir: Path
) -> dict:
    """Produce a PNG for every figure slot in the section."""
    produced: dict[str, Path] = {}
    for slot in section.slots:
        if slot.kind != "figure":
            continue
        try:
            code = strip_code_fences(
                _run(agents["figure"], briefs.figure_brief(slot.name, slot.spec), gatekeeper)
            )
            produced[slot.name] = render_figure(code, Path(assets_dir) / f"{slot.name}.png")
        except Exception as exc:  # noqa: BLE001 - one bad figure must not abort the run
            logger.warning("figure %s failed, skipping: %s", slot.name, exc)
    return produced


def generate_diagrams(section: SectionSpec, agents: dict, gatekeeper: Gatekeeper) -> dict:
    """Produce TikZ source for every diagram slot in the section."""
    produced: dict[str, str] = {}
    for slot in section.slots:
        if slot.kind != "diagram":
            continue
        try:
            produced[slot.name] = strip_code_fences(
                _run(agents["tikz"], briefs.tikz_brief(slot.name, slot.spec), gatekeeper)
            )
        except Exception as exc:  # noqa: BLE001 - one bad diagram must not abort the run
            logger.warning("diagram %s failed, skipping: %s", slot.name, exc)
    return produced
