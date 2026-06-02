import pytest

from chromatic_crew.shared.cost import CostTracker, Usage
from chromatic_crew.shared.gatekeeper import Gatekeeper, ServiceLimits, _SlidingWindow


def _gk(rpm=100, conc=2, retry=0.01, retries=2):
    limits = {"default": ServiceLimits(rpm, conc, retry, retries)}
    return Gatekeeper(limits, CostTracker(100.0))


def test_execute_returns_result():
    assert _gk().execute(lambda: 42) == 42


def test_retry_then_succeed():
    gk = _gk()
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("transient")
        return "ok"

    assert gk.execute(flaky) == "ok"
    assert calls["n"] == 2


def test_retry_exhausted_raises():
    gk = _gk(retries=1)

    def always():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        gk.execute(always)


def test_unknown_service_falls_back_to_default():
    assert _gk().execute(lambda: 1, service="nonexistent") == 1


def test_usage_is_recorded():
    gk = _gk()
    gk.execute(lambda: "x", usage_of=lambda r: Usage(10, 5, "ollama"))
    assert gk.cost_report["default"]["calls"] == 1


def test_sliding_window_blocks_when_full():
    window = _SlidingWindow(1)
    assert window.time_until_slot() == 0.0
    assert window.time_until_slot() > 0.0
