import pytest

from chromatic_crew.orchestration.outline import load_outline
from chromatic_crew.shared.exceptions import ConfigError


def test_load_outline_has_expected_sections(config_dir):
    sections = load_outline(config_dir)
    ids = {s.id for s in sections}
    assert {"abstract", "model", "methodology", "conclusion"} <= ids


def test_model_section_has_formula_and_language(config_dir):
    model = next(s for s in load_outline(config_dir) if s.id == "model")
    assert model.language == "he"  # full-Hebrew document
    assert any(slot.kind == "formula" for slot in model.slots)


def test_hebrew_sections_present(config_dir):
    he = [s for s in load_outline(config_dir) if s.language == "he"]
    assert {"methodology", "results", "discussion", "implications"} <= {s.id for s in he}


def test_missing_outline_raises(tmp_path):
    with pytest.raises(ConfigError):
        load_outline(tmp_path)
