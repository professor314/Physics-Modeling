"""
Compatibility shim for legacy VPython imports.

This module allows code written for the legacy `visual` module (circa 2004)
to run against modern `vpython` without modifying the original source files.

Usage:
    Add the `compat/` directory to your Python path, then legacy imports like
    `from visual import *` will resolve through this shim.

    Example:
        PYTHONPATH=./compat python original/assignments/springsim.py

Known limitations:
    - `frame` objects are stubbed (tracks pos/axis but doesn't group objects)
    - `display()` maps to `canvas()` but pixel-positioning params are ignored
    - `gdisplay` maps to `graph` with a slightly different API
    - Programs using `visual.controls` need the separate controls.py stub
"""

import warnings

# One-time notice on import
print("Note: Using compatibility shim for legacy VPython imports")

# Re-export everything from vpython so `from visual import *` works
from vpython import *  # noqa: F401, F403

# Alias `display` to `canvas` (the modern vpython equivalent)
display = canvas  # noqa: F811

# Re-export `arange` from numpy (legacy VPython bundled this)
from numpy import arange  # noqa: F401

# --- frame class stub ---

_frame_warning_shown = False


class frame:
    """
    Stub for the legacy VPython `frame` object.

    In legacy VPython, `frame` grouped objects so they could be moved/rotated
    together. Modern vpython removed `frame` in favor of `compound()` or
    manual transforms. This stub accepts common parameters and tracks
    position/axis without actually grouping child objects.
    """

    def __init__(self, pos=None, axis=None, **kwargs):
        global _frame_warning_shown
        if not _frame_warning_shown:
            warnings.warn(
                "frame has limited support in modern vpython. "
                "Objects will not be grouped — position and axis are tracked "
                "but child objects must be positioned manually.",
                stacklevel=2,
            )
            _frame_warning_shown = True

        if pos is None:
            pos = vector(0, 0, 0)
        if axis is None:
            axis = vector(1, 0, 0)

        self.pos = pos
        self.axis = axis

        # Absorb any other kwargs silently so legacy code doesn't crash
        for key, value in kwargs.items():
            setattr(self, key, value)


# --- gdisplay alias ---

_gdisplay_warning_shown = False


def gdisplay(*args, **kwargs):
    """
    Alias for legacy `gdisplay` which maps to vpython's `graph`.

    Note: The API has changed. Legacy parameters like `x`, `y` (pixel position)
    are accepted but ignored. Core parameters like `title`, `xtitle`, `ytitle`,
    `xmin`, `xmax`, `ymin`, `ymax` still work.
    """
    global _gdisplay_warning_shown
    if not _gdisplay_warning_shown:
        warnings.warn(
            "gdisplay is deprecated. Using vpython's `graph` instead. "
            "Some parameters (pixel positioning) may be ignored.",
            stacklevel=2,
        )
        _gdisplay_warning_shown = True

    return graph(*args, **kwargs)


# Ensure `arange`, `display`, `frame`, `gdisplay` are all available via `from visual import *`
__all__ = [name for name in dir() if not name.startswith('_')]
