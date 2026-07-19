"""Collision simulations: elastic sphere collisions in 2D and 3D.

This subpackage provides elastic collision detection and resolution for
spherical objects, along with animated visualization.

Modules
-------
elastic
    Core collision simulation with detection and elastic resolution.
collisions_viz
    Animated 3D visualization for collision simulations.
"""

from physics_modeling.collisions.elastic import (
    CollisionConfig,
    CollisionSimulation,
    detect_collisions,
    resolve_collision,
)

__all__ = [
    "CollisionConfig",
    "CollisionSimulation",
    "detect_collisions",
    "resolve_collision",
]
