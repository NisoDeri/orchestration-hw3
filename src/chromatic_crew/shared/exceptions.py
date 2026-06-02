"""Project exception hierarchy.

A single base (`ChromaticCrewError`) lets callers catch everything from this
project with one `except`, while specific subclasses carry precise meaning.
"""


class ChromaticCrewError(Exception):
    """Base class for all project-specific errors."""


class ConfigError(ChromaticCrewError):
    """A configuration file is missing, malformed, or internally inconsistent."""


class VersionMismatchError(ConfigError):
    """A config file's declared version disagrees with the code version."""


class RateLimitExceededError(ChromaticCrewError):
    """The gatekeeper's configured rate limit was exceeded and could not recover."""


class CostCapExceededError(ChromaticCrewError):
    """Cumulative spend for a run exceeded the configured cap (cloud engines only)."""


class LatexCompileError(ChromaticCrewError):
    """A LaTeX compilation pass failed; inspect the captured log for details."""


class AgentOutputError(ChromaticCrewError):
    """An agent returned output that failed validation against its contract."""
