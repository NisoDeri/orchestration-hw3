"""Regenerate ONLY the figures (all figure slots) using the fixed figure_service.

Lets us refill assets/ without re-running text generation. Not part of the package.
Usage: uv run python scripts/regen_figures.py
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

for sec in load_outline(proj / "config"):
    figs = crew_run.generate_figures(sec, agents, gk, proj / "assets")
    for name in figs:
        print(f"OK  {sec.id}: {name}", flush=True)
print("cost/effort:", gk.cost_report)
