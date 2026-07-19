"""Visualization backends: matplotlib, Plotly, PyVista, and widget controls.

This sub-package provides a unified :class:`Renderer` protocol and concrete
backend implementations for displaying simulation state in both standalone
and notebook environments.

Exported Names
--------------
Renderer
    Protocol defining the common visualization interface.
Matplotlib2DRenderer
    Real-time 2D line-plot renderer backed by matplotlib.
Matplotlib3DRenderer
    Animated 3D renderer backed by matplotlib and mpl_toolkits.mplot3d.
detect_environment
    Function that detects whether code is running in a notebook, standalone,
    or headless environment.
"""

from physics_modeling.visualization.environment import detect_environment
from physics_modeling.visualization.matplotlib_backend import (
    Matplotlib2DRenderer,
    Matplotlib3DRenderer,
)
from physics_modeling.visualization.renderer import Renderer

__all__ = [
    "Renderer",
    "Matplotlib2DRenderer",
    "Matplotlib3DRenderer",
    "detect_environment",
]
