"""Test configuration for the Palmate project.

Pytest collects tests from the ``tests`` directory which means the
repository root is not guaranteed to be on ``sys.path`` during module
discovery.  The coverage report tests import helpers from the ``scripts``
package, so we proactively insert the project root into ``sys.path`` to
mirror the environment used when running the tools directly from the
command line.
"""

from __future__ import annotations

import sys
from pathlib import Path


def pytest_configure() -> None:
    project_root = Path(__file__).resolve().parents[1]
    root_str = str(project_root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
