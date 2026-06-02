"""Execute Figure-agent matplotlib code to produce one PNG per figure.

The Figure agent emits a self-contained snippet that draws a chart and saves it to
the provided ``out_path``. We run it with a non-interactive backend and a fixed
seed so figures are reproducible. Execution is local and trusted-for-coursework;
the snippet is constrained to the matplotlib/numpy namespace we inject.
"""

from pathlib import Path

from chromatic_crew.shared.exceptions import AgentOutputError
from chromatic_crew.shared.seeding import set_global_seed


def render_figure(code: str, out_path: Path, seed: int = 42) -> Path:
    """Run ``code`` (which must save a PNG to ``out_path``) and return the path."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    set_global_seed(seed)

    # Models often ignore `out_path` and call plt.savefig('their_name.png'). Force
    # every savefig to our path so the figure always lands where the pipeline expects.
    original_savefig = plt.savefig

    def forced_savefig(*_args, **kwargs):
        kwargs.setdefault("dpi", 150)
        kwargs.setdefault("bbox_inches", "tight")
        return original_savefig(str(out_path), **kwargs)

    plt.savefig = forced_savefig
    namespace = {"plt": plt, "np": np, "numpy": np, "out_path": str(out_path)}
    try:
        exec(code, namespace)  # noqa: S102 - generated figure code, local use
        # Fallback: if the model never called savefig, persist the current figure.
        if not out_path.exists() and plt.get_fignums():
            original_savefig(str(out_path), dpi=150, bbox_inches="tight")
    except Exception as exc:  # noqa: BLE001 - surface any drawing failure uniformly
        raise AgentOutputError(f"figure code failed: {exc}") from exc
    finally:
        plt.savefig = original_savefig
        plt.close("all")
    if not out_path.exists():
        raise AgentOutputError(f"figure code did not write {out_path.name}")
    return out_path
