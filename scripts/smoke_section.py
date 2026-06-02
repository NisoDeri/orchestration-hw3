"""Dev smoke test: generate ONE section live through the crew (Ollama).

Validates the real integration path (config -> agents -> CrewAI kickoff -> Ollama)
before committing to a full multi-section build. Not part of the package.

Usage: uv run python scripts/smoke_section.py [section_id]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from chromatic_crew.agents.factory import build_all_agents  # noqa: E402
from chromatic_crew.orchestration import crew_run  # noqa: E402
from chromatic_crew.orchestration.outline import load_outline  # noqa: E402
from chromatic_crew.shared.config import ConfigLoader  # noqa: E402

proj = Path(__file__).parents[1]
cfg = ConfigLoader(proj / "config").load()
gk = ConfigLoader.build_gatekeeper(cfg)
agents = build_all_agents(proj / "config", cfg)
sections = load_outline(proj / "config")

sid = sys.argv[1] if len(sys.argv) > 1 else "conclusion"
sec = next(s for s in sections if s.id == sid)
print(f"--- generating '{sid}' (language={sec.language}) ---", flush=True)
md = crew_run.generate_section(sec, agents, gk)
print(md)
print("--- cost/effort ---", gk.cost_report)
