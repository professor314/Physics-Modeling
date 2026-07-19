"""Protocols and type aliases for the physics-modeling core engine.

This module defines the foundational types and protocols used throughout the
package. All integrators and simulations rely on these definitions.
"""

from __future__ import annotations

from typing import Callable, Protocol

import numpy as np
from numpy.typing import NDArray

__all__ = ["State", "DerivativeFn", "Integrator"]

State = NDArray[np.float64]
"""Type alias for a simulation state vector — a 1-D float64 NumPy array."""

DerivativeFn = Callable[[State, float], State]
"""Type alias for a derivative function: (state, t) -> d(state)/dt."""


class Integrator(Protocol):
    """Protocol for numerical integrators.

    Any class that implements a compatible ``step`` method satisfies this
    protocol and can be used interchangeably within the simulation engine.

    Methods
    -------
    step(state, t, dt, derivatives)
        Advance *state* forward by one time step *dt*.
    """

    def step(
        self,
        state: State,
        t: float,
        dt: float,
        derivatives: DerivativeFn,
    ) -> State:
        """Advance the state by one time step.

        Parameters
        ----------
        state : State
            Current state vector (1-D float64 array).
        t : float
            Current simulation time.
        dt : float
            Time step size.
        derivatives : DerivativeFn
            Function computing the time derivative of the state.

        Returns
        -------
        State
            New state vector after advancing by *dt*.
        """
        ...
