"""SDK entry point: orchestrate the full paper build.

All business logic is reachable only through :func:`build_paper`. The build has two
phases, intentionally separable: (1) **generate** — the crew drafts English content,
figures, and TikZ diagrams; (2) **assemble** — content files are converted to LaTeX
and compiled. Splitting them lets the architect/editor inject the Hebrew translation
(local models are unreliable at Hebrew) between phases, then re-assemble with
``generate=False``.
"""

from dataclasses import dataclass, field
from pathlib import Path

from chromatic_crew.agents.factory import build_all_agents
from chromatic_crew.orchestration import crew_run
from chromatic_crew.orchestration.outline import SectionSpec, load_outline
from chromatic_crew.services import latex_service
from chromatic_crew.services.markdown_to_latex import convert
from chromatic_crew.shared.config import AppConfig, ConfigLoader
from chromatic_crew.shared.logger import get_logger

logger = get_logger()


@dataclass
class PaperResult:
    """Outcome of a build: where the PDF is, what ran, warnings, and cost."""

    pdf_path: Path | None
    section_order: list[str] = field(default_factory=list)
    warnings: dict = field(default_factory=dict)
    cost_report: dict = field(default_factory=dict)


def generate_content(project: Path, cfg: AppConfig, sections: list[SectionSpec]) -> dict:
    """Run the crew to write per-section English Markdown + figures + TikZ files."""
    gatekeeper = ConfigLoader.build_gatekeeper(cfg)
    agents = build_all_agents(project / "config", cfg)
    content_dir = project / "content"
    diagrams_dir = project / "latex" / "diagrams"
    content_dir.mkdir(parents=True, exist_ok=True)
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    for sec in sections:
        logger.info("generating section: %s", sec.id)
        markdown = crew_run.generate_section(sec, agents, gatekeeper, cfg.hebrew_strategy)
        (content_dir / f"{sec.id}.md").write_text(markdown, encoding="utf-8")
        crew_run.generate_figures(sec, agents, gatekeeper, project / "assets")
        for name, tikz in crew_run.generate_diagrams(sec, agents, gatekeeper).items():
            (diagrams_dir / f"{name}.tex").write_text(tikz, encoding="utf-8")
    return gatekeeper.cost_report


def assemble(project: Path, sections: list[SectionSpec]) -> list[str]:
    """Read content files (+ saved TikZ), convert to LaTeX, write ``body.tex``."""
    content_dir = project / "content"
    diagrams_dir = project / "latex" / "diagrams"
    fragments: dict[str, str] = {}
    order: list[str] = []
    for sec in sections:
        md_file = content_dir / f"{sec.id}.md"
        if not md_file.exists():
            continue
        tikz_map = {}
        for slot in sec.slots:
            if slot.kind == "diagram":
                df = diagrams_dir / f"{slot.name}.tex"
                if df.exists():
                    tikz_map[slot.name] = df.read_text(encoding="utf-8")
        fragments[sec.id] = convert(md_file.read_text(encoding="utf-8"), tikz_map, sec.language)
        order.append(sec.id)
    latex_service.assemble_body(fragments, order, project / "latex")
    return order


def build_paper(project_dir: Path, generate: bool = True, compile_pdf: bool = True) -> PaperResult:
    """Build the article. ``generate`` runs the crew; otherwise reuse content files."""
    project = Path(project_dir)
    cfg = ConfigLoader(project / "config").load()
    sections = load_outline(project / "config")
    cost = generate_content(project, cfg, sections) if generate else {}
    order = assemble(project, sections)
    pdf_path = None
    warnings: dict = {}
    if compile_pdf:
        pdf_path = latex_service.compile_pdf(project / "latex")
        warnings = latex_service.scan_warnings(latex_service.read_log(project / "latex"))
    return PaperResult(pdf_path=pdf_path, section_order=order, warnings=warnings, cost_report=cost)
