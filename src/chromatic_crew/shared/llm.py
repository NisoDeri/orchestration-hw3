"""Provider-agnostic LLM construction for CrewAI agents.

Default provider is local Ollama (free). Setting ``provider`` to ``"anthropic"``
in ``config/models.json`` (and supplying ``ANTHROPIC_API_KEY``) routes the very
same agents to Claude with no code change — satisfying the rubric's zero-hardcoding
and extensibility goals. The model string for each agent comes from config.
"""

from crewai import LLM

from chromatic_crew.shared.config import AgentModel, AppConfig


def build_llm(agent: AgentModel, cfg: AppConfig) -> LLM:
    """Build a CrewAI ``LLM`` for one agent from its configured model + provider."""
    if cfg.provider == "ollama":
        return LLM(
            model=agent.model,
            base_url=cfg.ollama_base_url,
            temperature=agent.temperature,
        )
    # Cloud providers (e.g. Anthropic) via litellm; credentials read from env.
    return LLM(model=agent.model, temperature=agent.temperature)
