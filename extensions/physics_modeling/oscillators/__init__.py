"""Oscillator simulations: spring pendulum, double pendulum, Lissajous."""

from physics_modeling.oscillators.spring_pendulum import (
    SpringPendulum,
    SpringPendulumConfig,
)
from physics_modeling.oscillators.spring_pendulum_viz import run_spring_pendulum_3d

__all__: list[str] = [
    "SpringPendulum",
    "SpringPendulumConfig",
    "run_spring_pendulum_3d",
]
