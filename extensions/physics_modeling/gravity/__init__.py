"""Gravity simulations: bouncing objects and N-body gravitational systems."""

from physics_modeling.gravity.bouncing import (
    BouncingSimulation,
    GravityConfig,
    create_fountain_config,
)
from physics_modeling.gravity.bouncing_viz import run_bouncing_3d

__all__ = [
    "BouncingSimulation",
    "GravityConfig",
    "create_fountain_config",
    "run_bouncing_3d",
]
