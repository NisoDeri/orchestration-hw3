import pytest

from chromatic_crew.shared.exceptions import VersionMismatchError
from chromatic_crew.shared.version import CODE_VERSION, validate_config_version


def test_matching_version_ok():
    validate_config_version(CODE_VERSION, "setup.json")


def test_mismatched_version_raises():
    with pytest.raises(VersionMismatchError):
        validate_config_version("9.99", "setup.json")
