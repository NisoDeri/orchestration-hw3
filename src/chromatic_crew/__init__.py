"""chromatic-crew — a CrewAI multi-agent system that authors a BiDi LaTeX article.

Public surface is intentionally tiny: consumers import the SDK entry point.
"""

from chromatic_crew.shared.version import CODE_VERSION

__version__ = CODE_VERSION
__all__ = ["__version__"]
