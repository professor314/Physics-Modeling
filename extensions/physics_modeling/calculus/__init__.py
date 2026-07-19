"""Calculus tools: logistic equation, Riemann sums, and numerical methods.

This subpackage provides:

- :class:`LogisticConfig` / :class:`LogisticSimulation` — Logistic growth ODE
  with analytical solution and multi-step-count comparison.
- :class:`RiemannResult` / :func:`riemann_sum` — Riemann sum computation for
  left, right, midpoint, and trapezoidal methods.
- :func:`run_logistic_2d` — Interactive 2D logistic growth visualization.
- :func:`run_riemann_2d` — Interactive 2D Riemann sum visualization.
"""

from physics_modeling.calculus.logistic import LogisticConfig, LogisticSimulation
from physics_modeling.calculus.logistic_viz import run_logistic_2d
from physics_modeling.calculus.riemann import RiemannResult, riemann_sum
from physics_modeling.calculus.riemann_viz import run_riemann_2d

__all__ = [
    "LogisticConfig",
    "LogisticSimulation",
    "RiemannResult",
    "riemann_sum",
    "run_logistic_2d",
    "run_riemann_2d",
]
