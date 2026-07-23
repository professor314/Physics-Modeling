# N-Body Gravitational Physics

## Overview

The N-body problem describes the motion of $N$ point masses interacting under mutual Newtonian gravity. It is one of the oldest problems in physics and remains computationally challenging for large $N$.

## Newton's Law of Universal Gravitation

The gravitational force between two masses $m_i$ and $m_j$ separated by distance $r$:

$$
\mathbf{F}_{ij} = \frac{G \, m_i \, m_j}{|\mathbf{r}_j - \mathbf{r}_i|^2} \, \hat{\mathbf{r}}_{ij}
$$

where $G = 6.674 \times 10^{-11}$ N⋅m²/kg² is the gravitational constant and $\hat{\mathbf{r}}_{ij}$ is the unit vector from $i$ to $j$.

## Equations of Motion

The acceleration on body $i$ due to all other bodies:

$$
\mathbf{a}_i = \sum_{j \neq i} \frac{G \, m_j \, (\mathbf{r}_j - \mathbf{r}_i)}{|\mathbf{r}_j - \mathbf{r}_i|^3}
$$

This gives $3N$ coupled second-order ODEs (or $6N$ first-order).

## Gravitational Softening

When two bodies approach closely, the force diverges as $1/r^2$. Numerically this causes:
- Extremely large accelerations
- Required time step shrinks to zero
- Loss of energy conservation

The standard fix is a **softening length** $\varepsilon$:

$$
\mathbf{a}_i = \sum_{j \neq i} \frac{G \, m_j \, (\mathbf{r}_j - \mathbf{r}_i)}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2)^{3/2}}
$$

Physical interpretation: each point mass is "smeared" into a Plummer sphere of radius $\varepsilon$. For $r \gg \varepsilon$, the force is essentially Newtonian.

## Energy Conservation

### Kinetic Energy

$$
T = \sum_{i=1}^{N} \frac{1}{2} m_i |\mathbf{v}_i|^2
$$

### Potential Energy

$$
U = -\sum_{i=1}^{N} \sum_{j>i} \frac{G \, m_i \, m_j}{\sqrt{|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2}}
$$

### Total Energy

$$
E = T + U = \text{constant (for conservative system)}
$$

Energy conservation is the primary diagnostic for integration accuracy.

### Virial Theorem

For a gravitationally bound system in equilibrium:

$$
2\langle T \rangle + \langle U \rangle = 0
$$

## Angular Momentum Conservation

Total angular momentum is also conserved:

$$
\mathbf{L} = \sum_{i=1}^{N} m_i \, \mathbf{r}_i \times \mathbf{v}_i = \text{constant}
$$

## Two-Body Problem (Kepler Orbits)

For $N = 2$, the problem reduces to a single effective body in a central force. The solutions are conic sections:

| Eccentricity $e$ | Orbit Type |
|------------------|------------|
| $e = 0$ | Circle |
| $0 < e < 1$ | Ellipse |
| $e = 1$ | Parabola |
| $e > 1$ | Hyperbola |

The orbital period (Kepler's third law):

$$
T^2 = \frac{4\pi^2}{G(m_1 + m_2)} a^3
$$

where $a$ is the semi-major axis.

### Circular Orbit Velocity

For equal masses $M$ in circular orbit with separation $d$:

$$
v = \sqrt{\frac{G M}{4 r}} \quad \text{where } r = d/2
$$

## Three-Body Problem

For $N \geq 3$, the system is generically **chaotic**:
- Sensitivity to initial conditions
- No general closed-form solution
- Lyapunov exponents are positive
- Long-term prediction is fundamentally limited

Special solutions exist (Lagrange points, figure-8 orbit) but are typically unstable.

## Computational Complexity

| Method | Complexity | Use Case |
|--------|-----------|----------|
| Direct summation | $O(N^2)$ | $N < 10^4$ |
| Barnes-Hut tree | $O(N \log N)$ | $10^4 < N < 10^6$ |
| Fast Multipole Method | $O(N)$ | $N > 10^6$ |
| Particle-Mesh | $O(N + M \log M)$ | Cosmological simulations |

## Numerical Integration

### Why Symplectic Integrators?

Non-symplectic methods (Euler, RK4) cause systematic energy drift:
- Euler: energy grows monotonically (system "heats up")
- RK4: slow energy drift, excellent for short integrations

Symplectic methods (Verlet, leapfrog) conserve a "shadow Hamiltonian" close to the true Hamiltonian:
- Energy oscillates but does not drift
- Phase space volume is preserved
- Ideal for long-term orbital dynamics

### Velocity Verlet Algorithm

$$
\mathbf{r}(t + \Delta t) = \mathbf{r}(t) + \mathbf{v}(t) \, \Delta t + \frac{1}{2} \mathbf{a}(t) \, \Delta t^2
$$

$$
\mathbf{v}(t + \Delta t) = \mathbf{v}(t) + \frac{1}{2} [\mathbf{a}(t) + \mathbf{a}(t + \Delta t)] \, \Delta t
$$

This is second-order accurate and time-reversible.

### Adaptive Time Stepping

For systems with close encounters, a global fixed time step is wasteful. Common approaches:
- Individual time steps per particle
- Block time stepping (powers of 2)
- Regularization for close binaries
