import pytest

from chromatic_crew.services.figure_service import render_figure
from chromatic_crew.shared.exceptions import AgentOutputError


def test_render_saves_png(tmp_path):
    code = "plt.figure(); plt.plot([0,1,2],[0,1,4]); plt.title('t'); plt.savefig(out_path, dpi=80)"
    out = render_figure(code, tmp_path / "f.png")
    assert out.exists()


def test_missing_savefig_raises(tmp_path):
    with pytest.raises(AgentOutputError):
        render_figure("x = 1 + 1", tmp_path / "f.png")


def test_broken_code_raises(tmp_path):
    with pytest.raises(AgentOutputError):
        render_figure("raise ValueError('nope')", tmp_path / "f.png")
