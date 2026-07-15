"""
Compatibility shim for legacy `from visual.graph import *` imports.

In VPython circa 2004, graph-related objects lived in a separate
`visual.graph` submodule. Modern vpython includes them in the top-level
namespace. This module re-exports the relevant graph objects so that
legacy code like:

    from visual.graph import *
    graph1 = gdisplay(x=0, y=0, width=600, height=600,
                      title='Motion', xtitle='t', ytitle='y',
                      xmax=10., xmin=-1., ymax=1000, ymin=-1)
    yplot = gcurve(color=color.red)
    yplot.plot(pos=(t, y))

continues to work without modification.
"""

import warnings

from vpython import graph, gcurve, gdots, gvbars, ghbars, series, color  # noqa: F401

# --- gdisplay alias ---

_gdisplay_warning_shown = False


def gdisplay(*args, **kwargs):
    """
    Alias for legacy `gdisplay` which maps to vpython's `graph`.

    Legacy parameters like `x`, `y` (pixel positioning) are accepted but
    ignored. Core parameters like `title`, `xtitle`, `ytitle`, `xmin`,
    `xmax`, `ymin`, `ymax`, `width`, `height` still work.
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


__all__ = [
    'graph',
    'gcurve',
    'gdots',
    'gvbars',
    'ghbars',
    'series',
    'gdisplay',
    'color',
]
