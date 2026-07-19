"""Riemann sum computation for numerical integration visualization.

This module provides a pure-computation Riemann sum function supporting
left, right, midpoint, and trapezoidal methods. Results include the
rectangle data needed for visualization and a reference integral for
error calculation.

Classes
-------
RiemannResult
    Dataclass holding the computed sum, rectangle geometry, reference
    integral, and relative error.

Functions
---------
riemann_sum
    Compute a Riemann sum for a given function, interval, and method.

Examples
--------
>>> from physics_modeling.calculus.riemann import riemann_sum
>>> result = riemann_sum(lambda x: x**2, 0.0, 1.0, 100, "midpoint")
>>> abs(result.sum_value - 1/3) < 0.001
True
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np
from numpy.typing import NDArray

__all__ = ["RiemannResult", "riemann_sum"]


@dataclass
class RiemannResult:
    """Result of a Riemann sum computation.

    Parameters
    ----------
    sum_value : float
        The computed Riemann sum approximation.
    rectangles : NDArray[np.float64]
        Array of shape ``(n, 4)`` where each row is
        ``[x_left, width, height, x_sample]``. For trapezoid method,
        height represents the average of left and right function values.
    reference_integral : float
        High-precision reference integral computed with n=100,000
        using the midpoint rule.
    relative_error : float
        Relative error: ``|sum_value - reference| / |reference|``.
        Set to 0.0 if the reference integral is zero.
    """

    sum_value: float
    rectangles: NDArray[np.float64]
    reference_integral: float
    relative_error: float


def _compute_reference_integral(
    f: Callable[[float], float], a: float, b: float
) -> float:
    """Compute a high-precision reference integral using midpoint rule.

    Parameters
    ----------
    f : Callable[[float], float]
        The function to integrate.
    a : float
        Left endpoint of the interval.
    b : float
        Right endpoint of the interval.

    Returns
    -------
    float
        Approximate integral using 100,000 subdivisions.
    """
    n_ref = 100_000
    dx = (b - a) / n_ref
    midpoints = np.linspace(a + dx / 2.0, b - dx / 2.0, n_ref)
    # Vectorized evaluation
    values = np.array([f(x) for x in midpoints], dtype=np.float64)
    return float(np.sum(values) * dx)


def riemann_sum(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int,
    method: Literal["left", "right", "midpoint", "trapezoid"] = "midpoint",
) -> RiemannResult:
    """Compute a Riemann sum approximation of the integral of *f* on [a, b].

    Parameters
    ----------
    f : Callable[[float], float]
        The function to integrate. Must accept a single float argument.
    a : float
        Left endpoint of the integration interval.
    b : float
        Right endpoint of the integration interval.
    n : int
        Number of subdivisions (rectangles/trapezoids). Must be >= 1.
    method : {'left', 'right', 'midpoint', 'trapezoid'}
        The Riemann sum method to use:

        - ``"left"``: sample at left edge of each subinterval
        - ``"right"``: sample at right edge of each subinterval
        - ``"midpoint"``: sample at center of each subinterval
        - ``"trapezoid"``: average of left and right samples

    Returns
    -------
    RiemannResult
        Dataclass with the computed sum, rectangle data, reference
        integral, and relative error.

    Raises
    ------
    ValueError
        If *n* < 1 or *a* >= *b*, or *method* is invalid.

    Examples
    --------
    >>> result = riemann_sum(lambda x: x**2, 0.0, 1.0, 10, "left")
    >>> result.sum_value  # doctest: +SKIP
    0.285
    >>> result.rectangles.shape
    (10, 4)
    >>> result = riemann_sum(lambda x: x**2, 0.0, 1.0, 1000, "midpoint")
    >>> abs(result.sum_value - 1/3) < 1e-5
    True
    """
    if n < 1:
        raise ValueError(f"Number of subdivisions n must be >= 1, got {n}")
    if a >= b:
        raise ValueError(
            f"Left endpoint a must be less than b, got a={a}, b={b}"
        )
    valid_methods = ("left", "right", "midpoint", "trapezoid")
    if method not in valid_methods:
        raise ValueError(
            f"Invalid method '{method}'. Must be one of {valid_methods}"
        )

    dx = (b - a) / n
    rectangles = np.zeros((n, 4), dtype=np.float64)

    total = 0.0

    for i in range(n):
        x_left = a + i * dx

        if method == "left":
            x_sample = x_left
            height = f(x_sample)
        elif method == "right":
            x_sample = x_left + dx
            height = f(x_sample)
        elif method == "midpoint":
            x_sample = x_left + dx / 2.0
            height = f(x_sample)
        else:  # trapezoid
            x_sample = x_left + dx / 2.0
            height = (f(x_left) + f(x_left + dx)) / 2.0

        rectangles[i] = [x_left, dx, height, x_sample]
        total += height * dx

    # Compute reference integral
    reference = _compute_reference_integral(f, a, b)

    # Compute relative error
    if abs(reference) > 1e-15:
        relative_error = abs(total - reference) / abs(reference)
    else:
        relative_error = 0.0

    return RiemannResult(
        sum_value=total,
        rectangles=rectangles,
        reference_integral=reference,
        relative_error=relative_error,
    )
