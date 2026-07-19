"""Epidemic models: SIR and SEIR compartmental simulations."""

from physics_modeling.epidemics.sir import SIRConfig, SIRSimulation
from physics_modeling.epidemics.sir_viz import run_sir_2d

__all__: list[str] = [
    "SIRConfig",
    "SIRSimulation",
    "run_sir_2d",
]
