# Spring Pendulum Physics

## Overview

A spring pendulum is a point mass attached to a spring that can both oscillate radially (stretch/compress) and swing angularly under gravity. This creates a coupled nonlinear system with rich dynamics including energy transfer between radial and angular modes.

## Hooke's Law

A spring exerts a restoring force proportional to its displacement from equilibrium:

$$
F_{\text{spring}} = -k \, \Delta x
$$

where:
- $k$ is the spring constant (N/m) — stiffness of the spring
- $\Delta x = |\mathbf{r}| - L_0$ is the extension beyond the natural length $L_0$

## Equations of Motion

For a 3D spring pendulum with pivot at the origin, the bob at position $\mathbf{r}$ with velocity $\mathbf{v}$ experiences:

### Spring Restoring Force

$$
\mathbf{F}_{\text{spring}} = -k \, (|\mathbf{r}| - L_0) \, \hat{\mathbf{r}}
$$

where $\hat{\mathbf{r}} = \mathbf{r} / |\mathbf{r}|$ is the unit vector from pivot to bob.

### Spring Damping

Opposes the radial component of velocity (energy loss along the spring axis):

$$
\mathbf{F}_{\text{damp}} = -b \, (\mathbf{v} \cdot \hat{\mathbf{r}}) \, \hat{\mathbf{r}}
$$

### Air Resistance

Linear drag opposing all motion:

$$
\mathbf{F}_{\text{air}} = -c \, \mathbf{v}
$$

### Gravity

$$
\mathbf{F}_{\text{gravity}} = -m g \, \hat{\mathbf{y}}
$$

### Net Acceleration

$$
\mathbf{a} = \frac{\mathbf{F}_{\text{spring}} + \mathbf{F}_{\text{damp}} + \mathbf{F}_{\text{air}} + \mathbf{F}_{\text{gravity}}}{m}
$$

## Simple Harmonic Motion (Undamped, 1D)

In the absence of gravity and damping, a mass on a spring oscillates as:

$$
x(t) = A \cos(\omega t + \phi)
$$

with angular frequency:

$$
\omega = \sqrt{\frac{k}{m}}
$$

and period:

$$
T = \frac{2\pi}{\omega} = 2\pi \sqrt{\frac{m}{k}}
$$

## Damped Oscillation

With damping coefficient $b$, the motion becomes:

$$
x(t) = A \, e^{-\gamma t} \cos(\omega_d t + \phi)
$$

where:
- $\gamma = b / (2m)$ is the damping rate
- $\omega_d = \sqrt{\omega_0^2 - \gamma^2}$ is the damped frequency

### Damping Regimes

| Condition | Regime | Behavior |
|-----------|--------|----------|
| $\gamma < \omega_0$ | Underdamped | Oscillates with decaying amplitude |
| $\gamma = \omega_0$ | Critically damped | Returns to equilibrium fastest without oscillating |
| $\gamma > \omega_0$ | Overdamped | Slow exponential return, no oscillation |

## Energy

For the conservative (undamped) system:

$$
E = \frac{1}{2} m |\mathbf{v}|^2 + \frac{1}{2} k (|\mathbf{r}| - L_0)^2 + m g y
$$

Energy is conserved when $b = 0$ and $c = 0$. With damping, energy decreases monotonically:

$$
\frac{dE}{dt} = -b (\mathbf{v} \cdot \hat{\mathbf{r}})^2 - c |\mathbf{v}|^2 \leq 0
$$

## Resonance

When driven by an external periodic force $F_0 \cos(\omega_d t)$, the system exhibits resonance when the driving frequency matches the natural frequency. The steady-state amplitude is:

$$
A(\omega_d) = \frac{F_0 / m}{\sqrt{(\omega_0^2 - \omega_d^2)^2 + (2\gamma\omega_d)^2}}
$$

Maximum response occurs near $\omega_d = \omega_0$ (shifted slightly by damping).

## Numerical Considerations

- **Euler method** introduces artificial energy gain/loss — visible as amplitude drift
- **RK4** maintains energy well for moderate time steps
- **Verlet** (symplectic) is ideal for long-term energy conservation
- Time step should satisfy $\Delta t \ll T / 10$ for stability
