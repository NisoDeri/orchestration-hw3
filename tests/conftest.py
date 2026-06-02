"""Shared test fixtures."""

from pathlib import Path

import pytest

PROJECT = Path(__file__).parents[1]


@pytest.fixture
def project_dir() -> Path:
    """The hw3 project root (holds config/, latex/, src/)."""
    return PROJECT


@pytest.fixture
def config_dir() -> Path:
    """The real config directory, used for load/parse tests."""
    return PROJECT / "config"
