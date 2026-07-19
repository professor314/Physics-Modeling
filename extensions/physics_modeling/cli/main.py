"""CLI entry point for the physics-modeling package.

Provides subcommands to launch standalone simulations from the terminal.

Usage::

    physics-modeling spring-pendulum
    physics-modeling gravity
    physics-modeling sir
    physics-modeling list
"""

from __future__ import annotations

import argparse
import sys


SIMULATIONS = {
    "spring-pendulum": "3D spring pendulum with interactive sliders",
    "gravity": "3D bouncing objects under gravity (fountain mode)",
    "bouncing": "Alias for 'gravity'",
    "sir": "2D SIR epidemic model with parameter sliders",
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


def _run_bouncing() -> None:
    """Launch the bouncing gravity 3D visualization."""
    from physics_modeling.gravity.bouncing_viz import run_bouncing_3d

    run_bouncing_3d()


def _run_sir() -> None:
    """Launch the SIR epidemic 2D visualization."""
    from physics_modeling.epidemics.sir_viz import run_sir_2d

    run_sir_2d()


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
        "gravity",
        help="Launch 3D bouncing objects under gravity (fountain mode)",
    )

    subparsers.add_parser(
        "bouncing",
        help="Alias for 'gravity' — bouncing objects simulation",
    )

    subparsers.add_parser(
        "sir",
        help="Launch 2D SIR epidemic model with parameter sliders",
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

    if args.command == "spring-pendulum":
        _run_spring_pendulum()
    elif args.command in ("gravity", "bouncing"):
        _run_bouncing()
    elif args.command == "sir":
        _run_sir()


if __name__ == "__main__":
    main()
