import pytest

from chromatic_crew.shared.cost import CostTracker, Usage
from chromatic_crew.shared.exceptions import CostCapExceededError


def test_local_engine_is_free():
    tracker = CostTracker(1.0)
    tracker.record("ollama", Usage(1000, 1000, "ollama"), 0.5)
    assert tracker.total_usd() == 0.0
    assert tracker.report()["ollama"]["calls"] == 1


def test_cloud_model_is_priced():
    tracker = CostTracker(100.0)
    tracker.record("svc", Usage(1_000_000, 0, "claude-sonnet-4-6"), 0.1)
    assert tracker.total_usd() == pytest.approx(3.0)


def test_usage_total():
    assert Usage(3, 4).total == 7


def test_cap_enforced():
    tracker = CostTracker(0.001)
    with pytest.raises(CostCapExceededError):
        tracker.record("svc", Usage(1_000_000, 1_000_000, "claude-opus-4-8"), 0.1)
