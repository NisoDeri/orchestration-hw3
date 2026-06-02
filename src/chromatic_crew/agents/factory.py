"""Factory that builds CrewAI agents from config (personas + per-agent model).

Keeping personas in ``config/agents.json`` and models in ``config/models.json``
means new agents or model swaps require no code change (zero hardcoding).
"""

import json
from pathlib import Path

from crewai import Agent

from chromatic_crew.shared.config import AppConfig
from chromatic_crew.shared.exceptions import ConfigError
from chromatic_crew.shared.llm import build_llm


def load_agent_specs(config_dir: Path) -> dict[str, dict]:
    """Load agent persona specs (role/goal/backstory) from ``agents.json``."""
    path = Path(config_dir) / "agents.json"
    if not path.exists():
        raise ConfigError(f"missing agent config: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["agents"]


def build_agent(name: str, specs: dict[str, dict], cfg: AppConfig) -> Agent:
    """Construct one CrewAI ``Agent`` by name from its persona + configured model."""
    if name not in specs:
        raise ConfigError(f"unknown agent persona: {name!r}")
    if name not in cfg.models:
        raise ConfigError(f"no model configured for agent: {name!r}")
    spec = specs[name]
    return Agent(
        role=spec["role"],
        goal=spec["goal"],
        backstory=spec["backstory"],
        llm=build_llm(cfg.models[name], cfg),
        allow_delegation=False,
        verbose=True,
    )


def build_all_agents(config_dir: Path, cfg: AppConfig) -> dict[str, Agent]:
    """Build every configured agent, keyed by name."""
    specs = load_agent_specs(config_dir)
    return {name: build_agent(name, specs, cfg) for name in specs}
