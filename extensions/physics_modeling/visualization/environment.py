"""Execution environment detection for renderer selection.

This module provides :func:`detect_environment` which determines whether
code is running inside a Jupyter notebook, a standalone desktop session,
or a headless server. The visualization system uses this to pick the
appropriate default backend automatically.

Functions
---------
detect_environment
    Detect the current execution environment.
"""

from __future__ import annotations

import os
import sys
from typing import Literal

__all__ = ["detect_environment"]


def detect_environment() -> Literal["notebook", "standalone", "headless"]:
    """Detect the current execution environment.

    The detection logic follows this priority order:

    1. If an IPython kernel is active (Jupyter notebook/lab), return
       ``"notebook"``.
    2. If a graphical display is available (``DISPLAY`` env var on Linux/macOS,
       or running on Windows/macOS which always have a display), return
       ``"standalone"``.
    3. Otherwise return ``"headless"`` (e.g., CI servers, Docker containers
       without X11 forwarding).

    Returns
    -------
    Literal["notebook", "standalone", "headless"]
        One of three environment identifiers.

    Examples
    --------
    >>> env = detect_environment()
    >>> env in ("notebook", "standalone", "headless")
    True
    """
    # Check for Jupyter/IPython kernel
    try:
        from IPython import get_ipython  # type: ignore[import-untyped]

        shell = get_ipython()
        if shell is not None and "IPKernelApp" in shell.config:
            return "notebook"
    except (ImportError, AttributeError):
        pass

    # Check for graphical display availability
    if sys.platform in ("win32", "darwin"):
        # Windows and macOS always have a display manager
        return "standalone"

    # On Linux/Unix, check DISPLAY or WAYLAND_DISPLAY
    if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        return "standalone"

    return "headless"
