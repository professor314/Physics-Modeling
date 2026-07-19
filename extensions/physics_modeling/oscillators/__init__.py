"""Oscillator simulations: spring pendulum, double pendulum, Lissajous."""

from physics_modeling.oscillators.double_pendulum import (
    DoublePendulum,
    DoublePendulumConfig,
)
from physics_modeling.oscillators.double_pendulum_viz import run_double_pendulum_2d
from physics_modeling.oscillators.lissajous import (
    LissajousConfig,
    generate_lissajous,
)
from physics_modeling.oscillators.lissajous_viz import run_lissajous_3d
from physics_modeling.oscillators.spring_pendulum import (
    SpringPendulum,
    SpringPendulumConfig,
)
from physics_modeling.oscillators.spring_pendulum_viz import run_spring_pendulum_3d

__all__: list[str] = [
    "DoublePendulum",
    "DoublePendulumConfig",
    "LissajousConfig",
    "SpringPendulum",
    "SpringPendulumConfig",
    "generate_lissajous",
    "run_double_pendulum_2d",
    "run_lissajous_3d",
    "run_spring_pendulum_3d",
]
