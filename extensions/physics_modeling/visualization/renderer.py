"""Renderer protocol for the visualization backend system.

This module defines the :class:`Renderer` protocol that all visualization
backends must satisfy. Simulations interact only with this interface,
enabling swappable backends (matplotlib, Plotly, PyVista) without coupling
physics code to any particular rendering library.

Classes
-------
Renderer
    Protocol defining the common visualization interface.
"""

from __future__ import annotations

from typing import Any, Callable, Protocol

from physics_modeling.core.protocols import State

__all__ = ["Renderer"]


class Renderer(Protocol):
    """Common interface for all visualization backends.

    Any class implementing these four methods satisfies the protocol and
    can be used interchangeably by :class:`~physics_modeling.core.runner.SimulationRunner`
    or directly by individual simulations.

    Methods
    -------
    setup(config)
        Initialize the display surface (figure, canvas, window).
    draw(state, t)
        Render the current simulation state at time *t*.
    add_slider(name, min_val, max_val, initial, callback)
        Add an interactive parameter slider to the display.
    close()
        Release display resources and close any open windows.
    """

    def setup(self, config: dict[str, Any]) -> None:
        """Initialize the display surface.

        Parameters
        ----------
        config : dict[str, Any]
            Backend-specific configuration. Common keys include:
            - ``"title"`` (str): window/figure title
            - ``"xlim"`` (tuple[float, float]): x-axis range
            - ``"ylim"`` (tuple[float, float]): y-axis range
            - ``"zlim"`` (tuple[float, float]): z-axis range (3D only)
            - ``"xlabel"`` (str): x-axis label
            - ``"ylabel"`` (str): y-axis label
            - ``"zlabel"`` (str): z-axis label (3D only)
        """
        ...

    def draw(self, state: State, t: float) -> None:
        """Render the current simulation state.

        Parameters
        ----------
        state : State
            Current simulation state vector (1-D float64 NumPy array).
        t : float
            Current simulation time in seconds.
        """
        ...

    def add_slider(
        self,
        name: str,
        min_val: float,
        max_val: float,
        initial: float,
        callback: Callable[[float], None],
    ) -> None:
        """Add an interactive parameter slider.

        Parameters
        ----------
        name : str
            Human-readable label for the slider.
        min_val : float
            Minimum slider value.
        max_val : float
            Maximum slider value.
        initial : float
            Initial slider position.
        callback : Callable[[float], None]
            Function invoked with the new value whenever the slider changes.
        """
        ...

    def close(self) -> None:
        """Release display resources and close any open windows."""
        ...
