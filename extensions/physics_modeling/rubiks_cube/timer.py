"""Rubik's cube solve timer.

Provides a ``CubeTimer`` class for timing solves with split tracking,
suitable for speedcubing practice sessions.
"""

from __future__ import annotations

import time


class CubeTimer:
    """Timer for Rubik's cube solves with split support.

    Tracks elapsed time between start and stop, and allows recording
    intermediate split times (e.g., for cross, F2L, OLL, PLL phases).

    Examples
    --------
    >>> timer = CubeTimer()
    >>> timer.is_running
    False
    >>> timer.start()
    >>> timer.is_running
    True
    >>> # ... solve the cube ...
    >>> elapsed = timer.stop()
    >>> elapsed > 0
    True
    """

    def __init__(self) -> None:
        self._start_time: float | None = None
        self._stop_time: float | None = None
        self._splits: list[float] = []

    @property
    def is_running(self) -> bool:
        """Whether the timer is currently active.

        Returns
        -------
        bool
            True if the timer has been started and not yet stopped.
        """
        return self._start_time is not None and self._stop_time is None

    @property
    def elapsed(self) -> float:
        """Current or final elapsed time.

        If the timer is running, returns the time elapsed since start.
        If the timer has been stopped, returns the final elapsed time.
        If the timer has never been started, returns 0.0.

        Returns
        -------
        float
            Elapsed time in seconds.
        """
        if self._start_time is None:
            return 0.0
        if self._stop_time is not None:
            return self._stop_time - self._start_time
        return time.perf_counter() - self._start_time

    @property
    def splits(self) -> list[float]:
        """Recorded split times (elapsed seconds at each split point).

        Returns
        -------
        list[float]
            List of elapsed times at which splits were recorded.
        """
        return list(self._splits)

    def start(self) -> None:
        """Start the timer.

        Records the current time as the start point. If the timer was
        previously used, it is automatically reset before starting.

        Raises
        ------
        RuntimeError
            If the timer is already running.
        """
        if self.is_running:
            raise RuntimeError("Timer is already running. Call stop() first.")
        self._start_time = time.perf_counter()
        self._stop_time = None
        self._splits = []

    def stop(self) -> float:
        """Stop the timer and return the elapsed time.

        Returns
        -------
        float
            Total elapsed time in seconds.

        Raises
        ------
        RuntimeError
            If the timer is not currently running.
        """
        if not self.is_running:
            raise RuntimeError("Timer is not running. Call start() first.")
        self._stop_time = time.perf_counter()
        return self.elapsed

    def reset(self) -> None:
        """Reset the timer, clearing all recorded times and splits."""
        self._start_time = None
        self._stop_time = None
        self._splits = []

    def split(self) -> float:
        """Record a split time.

        Records the current elapsed time as a split point, useful for
        tracking phase times (cross, F2L, OLL, PLL).

        Returns
        -------
        float
            The elapsed time at the moment of the split.

        Raises
        ------
        RuntimeError
            If the timer is not currently running.
        """
        if not self.is_running:
            raise RuntimeError("Timer is not running. Cannot record split.")
        current_elapsed = self.elapsed
        self._splits.append(current_elapsed)
        return current_elapsed
