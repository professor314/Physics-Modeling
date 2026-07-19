"""Lissajous Figures — Parametric Curve Generation.

Generates 3D Lissajous curves defined by:

    x(t) = A * cos(a*t + δ)
    y(t) = B * sin(b*t)
    z(t) = C * sin(c*t)

These are not ODE-based simulations but direct parametric evaluations.

Run the visualization::

    py -m physics_modeling.oscillators.lissajous_viz

Or generate curve data programmatically::

    from physics_modeling.oscillators.lissajous import (
        LissajousConfig,
        generate_lissajous,
    )
    config = LissajousConfig(a=3, b=2, delta=np.pi / 2)
    points = generate_lissajous(config)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

__all__ = ["LissajousConfig", "generate_lissajous", "is_closed"]


@dataclass
class LissajousConfig:
    """Configuration for a 3D Lissajous curve.

    Parameters
    ----------
    a : float
        Frequency parameter for the x-axis.
    b : float
        Frequency parameter for the y-axis.
    c : float
        Frequency parameter for the z-axis.
    A : float
        Amplitude for the x-axis.
    B : float
        Amplitude for the y-axis.
    C : float
        Amplitude for the z-axis.
    delta : float
        Phase offset applied to the x-component (radians).
    n_points : int
        Number of sample points along the curve.
    """

    a: float = 1.0
    b: float = 1.0
    c: float = 1.0
    A: float = 1.0
    B: float = 1.0
    C: float = 1.0
    delta: float = 0.0
    n_points: int = 1000


def _lcm_period(a: float, b: float, c: float) -> float:
    """Compute the least common period for three frequency parameters.

    For rational frequency ratios the curve closes after t spans
    ``2π * lcm(1/a, 1/b, 1/c)``.  For irrational ratios we fall back
    to a reasonable default of ``2π``.

    Parameters
    ----------
    a : float
        First frequency.
    b : float
        Second frequency.
    c : float
        Third frequency.

    Returns
    -------
    float
        Number of full ``2π`` cycles needed to close the curve.
    """
    def _to_fraction(x: float, tol: float = 1e-9, max_denom: int = 10000) -> tuple[int, int]:
        """Convert a float to an approximate integer fraction (num, denom)."""
        if abs(x) < tol:
            return (0, 1)
        sign = 1 if x > 0 else -1
        x = abs(x)
        # Use continued fraction expansion
        num_prev, den_prev = 0, 1
        num_curr, den_curr = 1, 0
        val = x
        for _ in range(100):
            floor_val = int(math.floor(val))
            num_prev, num_curr = num_curr, floor_val * num_curr + num_prev
            den_prev, den_curr = den_curr, floor_val * den_curr + den_prev
            if den_curr > max_denom:
                # Revert to previous convergent
                num_curr, den_curr = num_prev, den_prev
                break
            if abs(x - num_curr / den_curr) < tol:
                break
            remainder = val - floor_val
            if abs(remainder) < tol:
                break
            val = 1.0 / remainder
        return (sign * num_curr, den_curr)

    def _lcm_int(x: int, y: int) -> int:
        return abs(x * y) // math.gcd(x, y) if x and y else 0

    # Convert each frequency to a fraction: a = num_a / den_a
    num_a, den_a = _to_fraction(a)
    num_b, den_b = _to_fraction(b)
    num_c, den_c = _to_fraction(c)

    if num_a == 0 or num_b == 0 or num_c == 0:
        return 1.0

    # Period of each component is 2π / freq.
    # Period_a = 2π * den_a / num_a  (since freq a = num_a/den_a)
    # LCM of periods = 2π * lcm(den_a/num_a, den_b/num_b, den_c/num_c)
    # = 2π * lcm(den_a, den_b, den_c) / gcd(num_a, num_b, num_c)?
    # Actually: lcm(p/q, r/s) = lcm(p,r) / gcd(q,s)
    # For our periods: T_a = den_a / |num_a|, etc. (in units of 2π)
    abs_num_a = abs(num_a)
    abs_num_b = abs(num_b)
    abs_num_c = abs(num_c)

    # LCM of three rationals: lcm(den_a/abs_num_a, den_b/abs_num_b, den_c/abs_num_c)
    # = lcm(den_a, den_b, den_c) / gcd(abs_num_a, abs_num_b, abs_num_c)
    # Actually the correct formula for lcm of fractions a/b is:
    # lcm(a1/b1, a2/b2) = lcm(a1,a2) / gcd(b1,b2)
    lcm_dens = _lcm_int(_lcm_int(den_a, den_b), den_c)
    gcd_nums = math.gcd(math.gcd(abs_num_a, abs_num_b), abs_num_c)

    return lcm_dens / gcd_nums


def is_closed(a: float, b: float, c: float, tol: float = 1e-9) -> bool:
    """Determine whether a Lissajous curve with given frequencies is closed.

    A curve is closed when all pairwise frequency ratios are rational numbers.

    Parameters
    ----------
    a : float
        Frequency parameter for x.
    b : float
        Frequency parameter for y.
    c : float
        Frequency parameter for z.
    tol : float
        Tolerance for rationality check.

    Returns
    -------
    bool
        ``True`` if the frequency ratios a:b, a:c, b:c are all rational.

    Examples
    --------
    >>> is_closed(1.0, 2.0, 3.0)
    True
    >>> is_closed(1.0, math.sqrt(2), 1.0)
    False
    """
    def _is_rational(x: float, max_denom: int = 10000) -> bool:
        """Check if x is close to a rational number with small denominator."""
        if abs(x) < tol:
            return True
        for denom in range(1, max_denom + 1):
            nearest_num = round(x * denom)
            if abs(x * denom - nearest_num) < tol * denom:
                return True
        return False

    # Check all pairwise ratios
    if abs(a) < tol or abs(b) < tol or abs(c) < tol:
        # Degenerate: zero frequency means the component is constant
        return True

    return _is_rational(a / b) and _is_rational(a / c) and _is_rational(b / c)


def generate_lissajous(config: LissajousConfig) -> NDArray[np.float64]:
    """Generate a 3D Lissajous curve from the given configuration.

    Evaluates the parametric equations:

        x(t) = A * cos(a*t + δ)
        y(t) = B * sin(b*t)
        z(t) = C * sin(c*t)

    over a time span that covers one full period (for closed curves) or
    a reasonable default of 2π (for non-closed curves).

    Parameters
    ----------
    config : LissajousConfig
        Curve parameters including frequencies, amplitudes, phase, and
        sample count.

    Returns
    -------
    NDArray[np.float64]
        Array of shape ``(n_points, 3)`` containing [x, y, z] coordinates.

    Examples
    --------
    >>> cfg = LissajousConfig(a=1, b=2, A=2.0, n_points=500)
    >>> pts = generate_lissajous(cfg)
    >>> pts.shape
    (500, 3)
    """
    period = _lcm_period(config.a, config.b, config.c)
    t: NDArray[np.float64] = np.linspace(
        0.0, 2.0 * np.pi * period, config.n_points, dtype=np.float64
    )

    x: NDArray[np.float64] = config.A * np.cos(config.a * t + config.delta)
    y: NDArray[np.float64] = config.B * np.sin(config.b * t)
    z: NDArray[np.float64] = config.C * np.sin(config.c * t)

    return np.column_stack([x, y, z])
