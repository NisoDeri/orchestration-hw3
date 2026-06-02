import pytest

from chromatic_crew.shared.config import ConfigLoader
from chromatic_crew.shared.exceptions import ConfigError


def test_load_real_config(config_dir):
    cfg = ConfigLoader(config_dir).load()
    assert cfg.provider == "ollama"
    assert "writer" in cfg.models
    assert cfg.models["writer"].model.startswith("ollama/")
    assert cfg.max_cost_usd > 0
    assert "default" in cfg.limits


def test_build_gatekeeper(config_dir):
    cfg = ConfigLoader(config_dir).load()
    gk = ConfigLoader.build_gatekeeper(cfg)
    assert gk.execute(lambda: 7) == 7


def test_missing_config_dir_raises(tmp_path):
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load()


def test_invalid_json_raises(tmp_path):
    (tmp_path / "setup.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load()
