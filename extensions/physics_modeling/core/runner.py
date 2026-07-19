"""Simulation runner that orchestrates stepping and rendering.

The :class:`SimulationRunner` couples a :class:`~physics_modeling.core.simulation.Simulation`
with a renderer, executing a step-render loop at a target frame rate.
"""

from __future__ import annotations

from typing import Any

from physics_modeling.core.simulation import Simulation

__all__ = ["SimulationRunner"]


class SimulationRunner:
    """Orchestrates simulation stepping and rendering.

    Couples a simulation with a renderer to produce animated output.
    The runner advances the simulation by ``dt`` each frame and calls
    the renderer's ``draw`` method with the updated state.

    Parameters
    ----------
    simulation : Simulation
        The simulation instance to advance.
    renderer : Any
        An object implementing a ``draw(state, t)`` method. Typed as
        ``Any`` until the Renderer protocol is implemented.
    dt : float
        Time step per simulation frame (seconds).
    fps : int
        Target frames per second for the render loop.

    Examples
    --------
    >>> runner = SimulationRunner(sim, renderer, dt=0.01, fps=60)
    >>> runner.start()  # blocks until runner.stop() is called
    """

    def __init__(
        self,
        simulation: Simulation,
        renderer: Any,
        dt: float = 0.01,
        fps: int = 60,
    ) -> None:
        self._sim: Simulation = simulation
        self._renderer: Any = renderer
        self._dt: float = dt
        self._fps: int = fps
        self._running: bool = False

    @property
    def running(self) -> bool:
        """Whether the runner loop is currently active."""
        return self._running

    def start(self) -> None:
        """Begin the step-render loop.

        Blocks until :meth:`stop` is called (e.g., from a callback or
        another thread). Each iteration advances the simulation by one
        time step and passes the state to the renderer.
        """
        self._running = True
        while self._running:
            self._sim.step(self._dt)
            self._renderer.draw(self._sim.state, self._sim.t)

    def stop(self) -> None:
        """Stop the step-render loop.

        Sets the internal running flag to ``False``, causing the loop
        in :meth:`start` to exit on its next iteration.
        """
        self._running = False
