"""Gravity simulations: bouncing objects and N-body gravitational systems."""

from physics_modeling.gravity.bouncing import (
    BouncingSimulation,
    GravityConfig,
    create_fountain_config,
)
from physics_modeling.gravity.bouncing_viz import run_bouncing_3d
from physics_modeling.gravity.nbody import NBodyConfig, NBodySimulation
from physics_modeling.gravity.nbody_viz import run_nbody_3d

__all__ = [
    "BouncingSimulation",
    "GravityConfig",
    "NBodyConfig",
    "NBodySimulation",
    "create_fountain_config",
    "run_bouncing_3d",
    "run_nbody_3d",
]
