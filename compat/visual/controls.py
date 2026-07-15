"""
Compatibility stub for legacy `from visual.controls import *` imports.

The `visual.controls` module provided UI widgets (buttons, sliders, toggles)
in legacy VPython. Modern vpython handles UI differently through its own
widget system. This stub provides no-op classes that warn but don't crash,
allowing legacy code to import without errors.
"""

import warnings

_controls_warning_shown = False


def _warn_once():
    global _controls_warning_shown
    if not _controls_warning_shown:
        warnings.warn(
            "visual.controls is not available in modern vpython. "
            "UI controls will not be displayed. Programs will continue "
            "running but interactive controls will be non-functional.",
            stacklevel=3,
        )
        _controls_warning_shown = True


class controls:
    """Stub for the legacy controls window."""

    def __init__(self, *args, **kwargs):
        _warn_once()

    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class button:
    """Stub for legacy button control."""

    def __init__(self, *args, **kwargs):
        _warn_once()


class slider:
    """Stub for legacy slider control."""

    def __init__(self, *args, **kwargs):
        _warn_once()

    @property
    def value(self):
        return 0

    @value.setter
    def value(self, v):
        pass


class toggle:
    """Stub for legacy toggle control."""

    def __init__(self, *args, **kwargs):
        _warn_once()

    @property
    def value(self):
        return False

    @value.setter
    def value(self, v):
        pass


class menu:
    """Stub for legacy menu control."""

    def __init__(self, *args, **kwargs):
        _warn_once()

    @property
    def value(self):
        return 0

    @value.setter
    def value(self, v):
        pass


__all__ = ['controls', 'button', 'slider', 'toggle', 'menu']
