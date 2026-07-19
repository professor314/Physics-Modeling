"""Matplotlib-based visualization backends.

This module provides two concrete :class:`~physics_modeling.visualization.renderer.Renderer`
implementations backed by matplotlib:

- :class:`Matplotlib2DRenderer` — real-time 2D line plots (time series,
  phase diagrams, histograms).
- :class:`Matplotlib3DRenderer` — animated 3D scatter/line plots using
  ``mpl_toolkits.mplot3d`` and :class:`~matplotlib.animation.FuncAnimation`.

Both renderers support interactive sliders via
:class:`matplotlib.widgets.Slider`.

Classes
-------
Matplotlib2DRenderer
    2D real-time plotting renderer.
Matplotlib3DRenderer
    3D animated plotting renderer with FuncAnimation support.
"""

from __future__ import annotations

from typing import Any, Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers 3D projection
from numpy.typing import NDArray

from physics_modeling.core.protocols import State

__all__ = ["Matplotlib2DRenderer", "Matplotlib3DRenderer"]


class Matplotlib2DRenderer:
    """Real-time 2D matplotlib renderer for time-series data.

    Creates a matplotlib figure that updates its line plot each time
    :meth:`draw` is called, appending data points over time.

    Attributes
    ----------
    _fig : Figure | None
        The matplotlib figure instance.
    _ax : Axes | None
        The primary axes for plotting.
    _lines : list
        Line2D objects managed by this renderer.
    _t_data : list[float]
        Accumulated time values.
    _y_data : list[list[float]]
        Accumulated state component values (one list per line).
    _sliders : list[Slider]
        Active slider widgets (kept alive to prevent garbage collection).
    _slider_axes : list[Axes]
        Axes reserved for slider widgets.
    """

    def __init__(self) -> None:
        self._fig: Figure | None = None
        self._ax: Axes | None = None
        self._lines: list[Any] = []
        self._t_data: list[float] = []
        self._y_data: list[list[float]] = []
        self._sliders: list[Slider] = []
        self._slider_axes: list[Axes] = []
        self._config: dict[str, Any] = {}

    def setup(self, config: dict[str, Any]) -> None:
        """Initialize the 2D figure and axes.

        Parameters
        ----------
        config : dict[str, Any]
            Configuration dictionary. Supported keys:

            - ``"title"`` (str): figure/axes title
            - ``"xlabel"`` (str): x-axis label (default ``"Time (s)"``)
            - ``"ylabel"`` (str): y-axis label (default ``"Value"``)
            - ``"xlim"`` (tuple[float, float]): fixed x-axis limits
            - ``"ylim"`` (tuple[float, float]): fixed y-axis limits
            - ``"labels"`` (list[str]): legend labels for each state component
            - ``"num_lines"`` (int): number of lines to plot (default 1)
        """
        self._config = config
        plt.ion()

        self._fig, self._ax = plt.subplots()
        assert self._ax is not None

        self._ax.set_title(config.get("title", "Simulation"))
        self._ax.set_xlabel(config.get("xlabel", "Time (s)"))
        self._ax.set_ylabel(config.get("ylabel", "Value"))

        if "xlim" in config:
            self._ax.set_xlim(config["xlim"])
        if "ylim" in config:
            self._ax.set_ylim(config["ylim"])

        num_lines: int = config.get("num_lines", 1)
        labels: list[str] = config.get("labels", [f"y{i}" for i in range(num_lines)])

        self._t_data = []
        self._y_data = [[] for _ in range(num_lines)]
        self._lines = []

        for i in range(num_lines):
            (line,) = self._ax.plot([], [], label=labels[i])
            self._lines.append(line)

        if num_lines > 1:
            self._ax.legend()

        self._fig.tight_layout()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

    def draw(self, state: State, t: float) -> None:
        """Append the current state to the plot and refresh.

        Parameters
        ----------
        state : State
            Current state vector. Each component is plotted as a
            separate line (up to the number configured in :meth:`setup`).
        t : float
            Current simulation time in seconds.
        """
        if self._fig is None or self._ax is None:
            return

        self._t_data.append(t)
        num_lines = len(self._lines)

        for i in range(min(num_lines, len(state))):
            self._y_data[i].append(float(state[i]))
            self._lines[i].set_data(self._t_data, self._y_data[i])

        # Auto-scale axes if no fixed limits were specified
        if "xlim" not in self._config:
            self._ax.set_xlim(0, max(t, 0.1))
        if "ylim" not in self._config:
            self._ax.relim()
            self._ax.autoscale_view(scalex=False)

        self._fig.canvas.draw_idle()
        self._fig.canvas.flush_events()

    def add_slider(
        self,
        name: str,
        min_val: float,
        max_val: float,
        initial: float,
        callback: Callable[[float], None],
    ) -> None:
        """Add an interactive slider below the plot.

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
            Function invoked with the new value on slider change.
        """
        if self._fig is None:
            return

        # Make room at the bottom for a new slider
        n_sliders = len(self._sliders)
        bottom_margin = 0.15 + n_sliders * 0.05
        self._fig.subplots_adjust(bottom=bottom_margin + 0.05)

        ax_slider = self._fig.add_axes([0.2, 0.02 + n_sliders * 0.05, 0.6, 0.03])
        slider = Slider(ax_slider, name, min_val, max_val, valinit=initial)
        slider.on_changed(callback)

        self._slider_axes.append(ax_slider)
        self._sliders.append(slider)

    def close(self) -> None:
        """Close the figure and release resources."""
        if self._fig is not None:
            plt.close(self._fig)
            self._fig = None
            self._ax = None
            self._lines = []
            self._t_data = []
            self._y_data = []
            self._sliders = []
            self._slider_axes = []


class Matplotlib3DRenderer:
    """Animated 3D matplotlib renderer using FuncAnimation.

    Creates a 3D figure with :mod:`mpl_toolkits.mplot3d` that can render
    scatter points, trajectory lines, and supports interactive sliders.

    Attributes
    ----------
    _fig : Figure | None
        The matplotlib figure instance.
    _ax : Axes3D | None
        The 3D axes for plotting.
    _scatter : object | None
        The 3D scatter plot object for current positions.
    _trail_line : object | None
        A Line3D object for the trajectory trail.
    _trail_data : list[NDArray]
        History of positions for trail rendering.
    _sliders : list[Slider]
        Active slider widgets.
    _slider_axes : list[Axes]
        Axes reserved for sliders.
    """

    def __init__(self) -> None:
        self._fig: Figure | None = None
        self._ax: Any = None  # Axes3D
        self._scatter: Any = None
        self._trail_line: Any = None
        self._trail_data: list[NDArray[np.float64]] = []
        self._sliders: list[Slider] = []
        self._slider_axes: list[Axes] = []
        self._config: dict[str, Any] = {}

    def setup(self, config: dict[str, Any]) -> None:
        """Initialize the 3D figure and axes with limits.

        Parameters
        ----------
        config : dict[str, Any]
            Configuration dictionary. Supported keys:

            - ``"title"`` (str): figure/axes title
            - ``"xlim"`` (tuple[float, float]): x-axis limits
            - ``"ylim"`` (tuple[float, float]): y-axis limits
            - ``"zlim"`` (tuple[float, float]): z-axis limits
            - ``"xlabel"`` (str): x-axis label (default ``"X"``)
            - ``"ylabel"`` (str): y-axis label (default ``"Y"``)
            - ``"zlabel"`` (str): z-axis label (default ``"Z"``)
            - ``"trail"`` (bool): whether to draw a trajectory trail
            - ``"trail_length"`` (int): max trail points (default 200)
        """
        self._config = config
        plt.ion()

        self._fig = plt.figure(figsize=(8, 6))
        self._ax = self._fig.add_subplot(111, projection="3d")

        self._ax.set_title(config.get("title", "3D Simulation"))
        self._ax.set_xlabel(config.get("xlabel", "X"))
        self._ax.set_ylabel(config.get("ylabel", "Y"))
        self._ax.set_zlabel(config.get("zlabel", "Z"))

        if "xlim" in config:
            self._ax.set_xlim(config["xlim"])
        if "ylim" in config:
            self._ax.set_ylim(config["ylim"])
        if "zlim" in config:
            self._ax.set_zlim(config["zlim"])

        # Initialize empty scatter for current positions
        self._scatter = self._ax.scatter([], [], [], s=50, c="blue")

        # Initialize trail line if requested
        if config.get("trail", False):
            (self._trail_line,) = self._ax.plot([], [], [], "b-", alpha=0.4, linewidth=1)

        self._trail_data = []
        self._fig.tight_layout()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

    def draw(self, state: State, t: float) -> None:
        """Update the 3D plot with current state.

        The state is interpreted as position data. For a single body the
        state should contain ``[x, y, z, ...]`` (first 3 elements are
        position). For multiple bodies, reshape appropriately before
        calling.

        Parameters
        ----------
        state : State
            Current state vector. The first 3 elements (or groups of 3
            for multi-body) are used as 3D coordinates.
        t : float
            Current simulation time in seconds.
        """
        if self._fig is None or self._ax is None:
            return

        # Extract 3D positions from state
        # For a single body: state = [x, y, z, vx, vy, vz, ...]
        # For N bodies: state = [x1,y1,z1,...,xN,yN,zN, vx1,...]
        positions = self._extract_positions(state)

        # Update scatter positions
        if self._scatter is not None:
            self._scatter._offsets3d = (
                positions[:, 0],
                positions[:, 1],
                positions[:, 2],
            )

        # Update trail
        trail_length = self._config.get("trail_length", 200)
        if self._config.get("trail", False) and self._trail_line is not None:
            # For trail, use only the first body position
            self._trail_data.append(positions[0].copy())
            if len(self._trail_data) > trail_length:
                self._trail_data = self._trail_data[-trail_length:]

            trail_arr = np.array(self._trail_data)
            self._trail_line.set_data(trail_arr[:, 0], trail_arr[:, 1])
            self._trail_line.set_3d_properties(trail_arr[:, 2])

        self._fig.canvas.draw_idle()
        self._fig.canvas.flush_events()

    def add_slider(
        self,
        name: str,
        min_val: float,
        max_val: float,
        initial: float,
        callback: Callable[[float], None],
    ) -> None:
        """Add a matplotlib slider below the 3D plot.

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
            Function invoked with the new value on slider change.
        """
        if self._fig is None:
            return

        n_sliders = len(self._sliders)
        bottom_margin = 0.15 + n_sliders * 0.05
        self._fig.subplots_adjust(bottom=bottom_margin + 0.05)

        ax_slider = self._fig.add_axes([0.2, 0.02 + n_sliders * 0.05, 0.6, 0.03])
        slider = Slider(ax_slider, name, min_val, max_val, valinit=initial)
        slider.on_changed(callback)

        self._slider_axes.append(ax_slider)
        self._sliders.append(slider)

    def close(self) -> None:
        """Close the figure and release resources."""
        if self._fig is not None:
            plt.close(self._fig)
            self._fig = None
            self._ax = None
            self._scatter = None
            self._trail_line = None
            self._trail_data = []
            self._sliders = []
            self._slider_axes = []

    @staticmethod
    def run_animation(
        simulation: Any,
        draw_callback: Callable[[State, float], None],
        dt: float = 0.01,
        interval: int = 16,
    ) -> None:
        """Set up a FuncAnimation loop and display it.

        This is a convenience method that creates a
        :class:`~matplotlib.animation.FuncAnimation` driving a
        simulation step-render loop and calls ``plt.show()`` to block
        until the window is closed.

        Parameters
        ----------
        simulation : Simulation
            A simulation instance with ``step(dt)`` and ``state``/``t``
            attributes.
        draw_callback : Callable[[State, float], None]
            Function called each frame with ``(state, t)`` to update the
            display. Typically the renderer's :meth:`draw` method.
        dt : float
            Time step per animation frame (default 0.01 s).
        interval : int
            Milliseconds between frames (default 16 ms ≈ 60 fps).

        Notes
        -----
        This method calls ``plt.show()`` which blocks until the user
        closes the figure window. It is intended for standalone mode.
        """

        def _update(frame: int) -> None:
            simulation.step(dt)
            draw_callback(simulation.state, simulation.t)

        fig = plt.gcf()
        _ = FuncAnimation(fig, _update, interval=interval, cache_frame_data=False)
        plt.show()

    def _extract_positions(self, state: State) -> NDArray[np.float64]:
        """Extract 3D position coordinates from a state vector.

        Parameters
        ----------
        state : State
            Flat state vector.

        Returns
        -------
        NDArray[np.float64]
            Array of shape ``(N, 3)`` containing position coordinates.
        """
        # If state has 6 elements: single body [x, y, z, vx, vy, vz]
        if len(state) == 6:
            return np.array([[state[0], state[1], state[2]]])

        # If state length is divisible by 6: N bodies with [pos, vel] each
        if len(state) % 6 == 0:
            n_bodies = len(state) // 6
            positions = np.zeros((n_bodies, 3))
            for i in range(n_bodies):
                positions[i] = state[i * 3 : i * 3 + 3]
            return positions

        # N-body format: first half positions, second half velocities
        if len(state) % 2 == 0:
            half = len(state) // 2
            if half % 3 == 0:
                n_bodies = half // 3
                return state[:half].reshape(n_bodies, 3)

        # Fallback: take first 3 elements as single position
        return np.array([[state[0], state[1], state[2] if len(state) > 2 else 0.0]])
