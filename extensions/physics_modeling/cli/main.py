"""CLI entry point for the physics-modeling package.

Provides subcommands to launch standalone simulations from the terminal.

Usage::

    physics-modeling spring-pendulum
    physics-modeling gravity
    physics-modeling double-pendulum
    physics-modeling nbody
    physics-modeling sir
    physics-modeling seir
    physics-modeling logistic
    physics-modeling lissajous
    physics-modeling riemann
    physics-modeling collisions
    physics-modeling gas
    physics-modeling list
"""

from __future__ import annotations

import argparse
import sys


SIMULATIONS: dict[str, str] = {
    "spring-pendulum": "3D spring pendulum with interactive sliders",
    "double-pendulum": "2D double pendulum with chaotic motion + trail",
    "gravity": "3D bouncing objects under gravity (fountain mode)",
    "bouncing": "Alias for 'gravity'",
    "nbody": "3D N-body gravitational simulation (binary star + particle)",
    "sir": "2D SIR epidemic model with parameter sliders",
    "seir": "2D SEIR epidemic model with parameter sliders",
    "logistic": "2D logistic growth equation visualization",
    "lissajous": "3D Lissajous figure visualization",
    "riemann": "2D Riemann sum visualization with interactive controls",
    "collisions": "Elastic collision simulation visualization",
    "gas": "Ideal gas hard-sphere simulation visualization",
}


def _check_display() -> bool:
    """Return True if matplotlib can display a window."""
    try:
        import matplotlib

        backend = matplotlib.get_backend()
        # Non-interactive backends that can't show windows
        headless_backends = {"agg", "pdf", "svg", "ps", "cairo", "template"}
        return backend.lower() not in headless_backends
    except ImportError:
        return False


def _run_spring_pendulum() -> None:
    """Launch the spring pendulum 3D visualization."""
    from physics_modeling.oscillators.spring_pendulum_viz import run_spring_pendulum_3d

    run_spring_pendulum_3d()


def _run_double_pendulum() -> None:
    """Launch the double pendulum 2D visualization."""
    from physics_modeling.oscillators.double_pendulum_viz import run_double_pendulum_2d

    run_double_pendulum_2d()


def _run_bouncing() -> None:
    """Launch the bouncing gravity 3D visualization."""
    from physics_modeling.gravity.bouncing_viz import run_bouncing_3d

    run_bouncing_3d()


def _run_nbody() -> None:
    """Launch the N-body gravitational 3D visualization."""
    from physics_modeling.gravity.nbody_viz import run_nbody_3d

    run_nbody_3d()


def _run_sir() -> None:
    """Launch the SIR epidemic 2D visualization."""
    from physics_modeling.epidemics.sir_viz import run_sir_2d

    run_sir_2d()


def _run_seir() -> None:
    """Launch the SEIR epidemic 2D visualization."""
    from physics_modeling.epidemics.seir_viz import run_seir_2d

    run_seir_2d()


def _run_logistic() -> None:
    """Launch the logistic equation 2D visualization."""
    from physics_modeling.calculus.logistic_viz import run_logistic_2d

    run_logistic_2d()


def _run_lissajous() -> None:
    """Launch the Lissajous figure 3D visualization."""
    from physics_modeling.oscillators.lissajous_viz import run_lissajous_3d

    run_lissajous_3d()


def _run_riemann() -> None:
    """Launch the Riemann sum 2D visualization."""
    from physics_modeling.calculus.riemann_viz import run_riemann_2d

    run_riemann_2d()


def _run_collisions() -> None:
    """Launch the elastic collisions visualization."""
    from physics_modeling.collisions.collisions_viz import run_collisions_2d

    run_collisions_2d()


def _run_gas() -> None:
    """Launch the ideal gas simulation visualization."""
    from physics_modeling.gas.gas_viz import run_gas_2d

    run_gas_2d()


def _list_simulations() -> None:
    """Print available simulations to stdout."""
    print("Available simulations:\n")
    for name, description in SIMULATIONS.items():
        print(f"  {name:<20} {description}")
    print("\nRun with: physics-modeling <simulation>")


def main() -> None:
    """Parse CLI arguments and dispatch to the appropriate simulation."""
    parser = argparse.ArgumentParser(
        prog="physics-modeling",
        description="Launch physics simulations from the command line.",
    )

    subparsers = parser.add_subparsers(dest="command", help="simulation to run")

    subparsers.add_parser(
        "spring-pendulum",
        help="Launch 3D spring pendulum with interactive sliders",
    )

    subparsers.add_parser(
        "double-pendulum",
        help="Launch 2D double pendulum with chaotic motion and trail",
    )

    subparsers.add_parser(
        "gravity",
        help="Launch 3D bouncing objects under gravity (fountain mode)",
    )

    subparsers.add_parser(
        "bouncing",
        help="Alias for 'gravity' — bouncing objects simulation",
    )

    subparsers.add_parser(
        "nbody",
        help="Launch 3D N-body gravitational simulation",
    )

    subparsers.add_parser(
        "sir",
        help="Launch 2D SIR epidemic model with parameter sliders",
    )

    subparsers.add_parser(
        "seir",
        help="Launch 2D SEIR epidemic model with parameter sliders",
    )

    subparsers.add_parser(
        "logistic",
        help="Launch 2D logistic growth equation visualization",
    )

    subparsers.add_parser(
        "lissajous",
        help="Launch 3D Lissajous figure visualization",
    )

    subparsers.add_parser(
        "riemann",
        help="Launch 2D Riemann sum visualization",
    )

    subparsers.add_parser(
        "collisions",
        help="Launch elastic collision simulation visualization",
    )

    subparsers.add_parser(
        "gas",
        help="Launch ideal gas hard-sphere simulation visualization",
    )

    subparsers.add_parser(
        "list",
        help="List all available simulations",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "list":
        _list_simulations()
        return

    # Check display availability for visualization commands
    if not _check_display():
        print(
            "No display available. Cannot open a visualization window.\n"
            "Run in an environment with a display, or use the Python API\n"
            "in a Jupyter notebook for inline rendering.",
            file=sys.stderr,
        )
        sys.exit(1)

    dispatch: dict[str, callable] = {  # type: ignore[type-arg]
        "spring-pendulum": _run_spring_pendulum,
        "double-pendulum": _run_double_pendulum,
        "gravity": _run_bouncing,
        "bouncing": _run_bouncing,
        "nbody": _run_nbody,
        "sir": _run_sir,
        "seir": _run_seir,
        "logistic": _run_logistic,
        "lissajous": _run_lissajous,
        "riemann": _run_riemann,
        "collisions": _run_collisions,
        "gas": _run_gas,
    }

    handler = dispatch.get(args.command)
    if handler is not None:
        handler()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
