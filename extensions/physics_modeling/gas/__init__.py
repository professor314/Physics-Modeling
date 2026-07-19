"""Gas simulations: hard sphere ideal gas with thermodynamic measurements.

Classes
-------
GasConfig
    Configuration dataclass for the hard sphere gas simulation.
HardSphereGas
    N-particle hard sphere gas in a bounded container.

Functions
---------
run_gas_3d
    Animated 3D visualization with velocity-coloured particles and
    live speed histogram.
"""

from physics_modeling.gas.gas_viz import run_gas_3d
from physics_modeling.gas.hard_sphere import GasConfig, HardSphereGas

__all__: list[str] = [
    "GasConfig",
    "HardSphereGas",
    "run_gas_3d",
]
