"""Configuration loading + validation.

Every tunable value in the system originates from `config/*.json` (rubric: zero
hardcoding). This module loads those files, validates their versions against the
code, and builds the typed objects the rest of the system consumes — including a
ready-to-use gatekeeper.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from chromatic_crew.shared.cost import CostTracker
from chromatic_crew.shared.exceptions import ConfigError
from chromatic_crew.shared.gatekeeper import Gatekeeper, ServiceLimits
from chromatic_crew.shared.version import validate_config_version


@dataclass(frozen=True)
class AgentModel:
    """Resolved model + sampling settings for one agent role."""

    model: str
    temperature: float


@dataclass(frozen=True)
class AppConfig:
    setup: dict
    models: dict[str, AgentModel]
    provider: str
    ollama_base_url: str
    hebrew_strategy: str
    limits: dict[str, ServiceLimits]
    max_cost_usd: float


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise ConfigError(f"missing config file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in {path}: {exc}") from exc


class ConfigLoader:
    """Loads and validates the three config files into an `AppConfig`."""

    def __init__(self, config_dir: Path):
        self._dir = Path(config_dir)

    def load(self) -> AppConfig:
        setup = _load_json(self._dir / "setup.json")
        models = _load_json(self._dir / "models.json")
        rates = _load_json(self._dir / "rate_limits.json")
        for cfg, name in (
            (setup, "setup.json"),
            (models, "models.json"),
            (rates, "rate_limits.json"),
        ):
            validate_config_version(cfg.get("version", ""), name)

        agent_models = {
            name: AgentModel(spec["model"], float(spec.get("temperature", 0.0)))
            for name, spec in models["agents"].items()
        }
        limits = {
            svc: ServiceLimits(
                requests_per_minute=int(s["requests_per_minute"]),
                concurrent_max=int(s["concurrent_max"]),
                retry_after_seconds=float(s["retry_after_seconds"]),
                max_retries=int(s["max_retries"]),
            )
            for svc, s in rates["services"].items()
        }
        return AppConfig(
            setup=setup,
            models=agent_models,
            provider=models.get("provider", "ollama"),
            ollama_base_url=models.get("ollama_base_url", "http://localhost:11434"),
            hebrew_strategy=models.get("hebrew_strategy", "editor"),
            limits=limits,
            max_cost_usd=float(rates["cost"]["max_cost_usd_per_run"]),
        )

    @staticmethod
    def build_gatekeeper(cfg: AppConfig) -> Gatekeeper:
        """Construct a gatekeeper wired to the config's limits and cost cap."""
        return Gatekeeper(cfg.limits, CostTracker(cfg.max_cost_usd))
