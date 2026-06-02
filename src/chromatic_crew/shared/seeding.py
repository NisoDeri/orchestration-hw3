"""Deterministic seeding so generated figure data is reproducible across runs."""

import random


def set_global_seed(seed: int) -> None:
    """Seed Python's RNG (and numpy if present) for reproducible synthetic data."""
    random.seed(seed)
    try:
        import numpy as np
    except ImportError:
        return
    np.random.seed(seed)
