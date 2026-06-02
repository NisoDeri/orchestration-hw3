import pytest

from chromatic_crew.agents.factory import build_agent, build_all_agents, load_agent_specs
from chromatic_crew.shared.config import ConfigLoader
from chromatic_crew.shared.exceptions import ConfigError


def test_load_agent_specs(config_dir):
    specs = load_agent_specs(config_dir)
    assert "writer" in specs
    assert "role" in specs["writer"]


def test_build_single_agent(config_dir):
    cfg = ConfigLoader(config_dir).load()
    specs = load_agent_specs(config_dir)
    agent = build_agent("writer", specs, cfg)
    assert agent.role


def test_build_unknown_agent_raises(config_dir):
    cfg = ConfigLoader(config_dir).load()
    specs = load_agent_specs(config_dir)
    with pytest.raises(ConfigError):
        build_agent("does-not-exist", specs, cfg)


def test_build_all_agents(config_dir):
    cfg = ConfigLoader(config_dir).load()
    agents = build_all_agents(config_dir, cfg)
    assert {"planner", "writer", "translator", "qa"} <= set(agents)
