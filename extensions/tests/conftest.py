"""Shared pytest configuration and Hypothesis strategies for physics-modeling tests."""

from hypothesis import settings, HealthCheck, Phase

# --- Hypothesis settings profiles ---

# Default profile: reasonable limits for local development
settings.register_profile(
    "default",
    max_examples=50,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)

# CI profile: more thorough testing, no deadline for slow runners
settings.register_profile(
    "ci",
    max_examples=100,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
    phases=[Phase.explicit, Phase.reuse, Phase.generate, Phase.shrink],
)

# Load the default profile; CI overrides via --hypothesis-profile=ci
settings.load_profile("default")


# --- Shared fixtures ---
# TODO: Add shared fixtures for common simulation setups as needed.
# For example:
#   - A fixture providing a simple harmonic oscillator simulation
#   - A fixture providing a configured RK4 integrator
#   - Hypothesis strategies for generating valid state vectors
