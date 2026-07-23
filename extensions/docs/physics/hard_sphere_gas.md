# Hard Sphere Gas Physics

## Overview

The hard sphere gas model treats gas molecules as rigid spheres that undergo perfectly elastic collisions. This is the simplest model that captures the statistical mechanics of an ideal gas, including the emergence of the Maxwell-Boltzmann velocity distribution and the relationship between microscopic motion and macroscopic temperature.

## Kinetic Theory of Gases

### Assumptions

1. Gas consists of $N$ identical spheres of radius $r$ and mass $m$
2. Spheres move in straight lines between collisions (no inter-particle forces except at contact)
3. Collisions are perfectly elastic (kinetic energy is conserved)
4. The container walls are perfectly rigid

### Microscopic to Macroscopic

The bridge between molecular motion and thermodynamics:

$$
\frac{3}{2} k_B T = \frac{1}{2} m \langle v^2 \rangle
$$

where $k_B = 1.38 \times 10^{-23}$ J/K is Boltzmann's constant and $\langle v^2 \rangle$ is the mean squared speed.

## Maxwell-Boltzmann Distribution

At thermal equilibrium, the probability of a molecule having speed $v$ is:

### Speed Distribution (3D)

$$
f(v) = 4\pi \left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2 \exp\left(-\frac{mv^2}{2k_B T}\right)
$$

### Characteristic Speeds

| Speed | Formula | Meaning |
|-------|---------|---------|
| Most probable | $v_p = \sqrt{2k_B T / m}$ | Peak of $f(v)$ |
| Mean | $\langle v \rangle = \sqrt{8k_B T / (\pi m)}$ | Average speed |
| RMS | $v_{\text{rms}} = \sqrt{3k_B T / m}$ | Root mean square |

Relation: $v_p < \langle v \rangle < v_{\text{rms}}$

### Velocity Component Distribution

Each velocity component follows a Gaussian:

$$
f(v_x) = \sqrt{\frac{m}{2\pi k_B T}} \exp\left(-\frac{mv_x^2}{2k_B T}\right)
$$

## Temperature

Temperature emerges as the average kinetic energy per degree of freedom:

$$
T = \frac{2}{3 k_B} \cdot \frac{1}{N} \sum_{i=1}^{N} \frac{1}{2} m |\mathbf{v}_i|^2
$$

In 2D simulations:

$$
T_{2D} = \frac{1}{k_B} \cdot \frac{1}{N} \sum_{i=1}^{N} \frac{1}{2} m |\mathbf{v}_i|^2
$$

(2 degrees of freedom instead of 3)

## Elastic Collision Physics

### Sphere-Sphere Collision

When two spheres $i$ and $j$ collide (surfaces touch):

**Collision normal:**
$$
\hat{\mathbf{n}} = \frac{\mathbf{r}_j - \mathbf{r}_i}{|\mathbf{r}_j - \mathbf{r}_i|}
$$

**Relative velocity along normal:**
$$
v_{\text{rel}} = (\mathbf{v}_i - \mathbf{v}_j) \cdot \hat{\mathbf{n}}
$$

**Velocity updates (equal masses):**
$$
\mathbf{v}_i' = \mathbf{v}_i - v_{\text{rel}} \, \hat{\mathbf{n}}
$$
$$
\mathbf{v}_j' = \mathbf{v}_j + v_{\text{rel}} \, \hat{\mathbf{n}}
$$

For unequal masses:
$$
\Delta v_i = -\frac{2 m_j}{m_i + m_j} v_{\text{rel}} \, \hat{\mathbf{n}}
$$
$$
\Delta v_j = +\frac{2 m_i}{m_i + m_j} v_{\text{rel}} \, \hat{\mathbf{n}}
$$

### Wall Collision

For a wall with inward normal $\hat{\mathbf{n}}_w$:

$$
\mathbf{v}' = \mathbf{v} - 2(\mathbf{v} \cdot \hat{\mathbf{n}}_w)\,\hat{\mathbf{n}}_w
$$

This reflects the velocity component perpendicular to the wall.

## Conservation Laws

Each collision conserves:

**Momentum:**
$$
m_i \mathbf{v}_i + m_j \mathbf{v}_j = m_i \mathbf{v}_i' + m_j \mathbf{v}_j'
$$

**Kinetic Energy:**
$$
\frac{1}{2}m_i |\mathbf{v}_i|^2 + \frac{1}{2}m_j |\mathbf{v}_j|^2 = \frac{1}{2}m_i |\mathbf{v}_i'|^2 + \frac{1}{2}m_j |\mathbf{v}_j'|^2
$$

These serve as numerical invariants to verify simulation correctness.

## Pressure

Pressure arises from momentum transfer to walls:

$$
P = \frac{N k_B T}{V}
$$

This is the ideal gas law. In simulation, pressure can be measured by accumulating momentum transferred to walls per unit area per unit time.

## Mean Free Path

The average distance a molecule travels between collisions:

$$
\ell = \frac{1}{n \sigma}
$$

where:
- $n = N/V$ is the number density
- $\sigma = \pi (2r)^2$ is the collision cross-section (for identical spheres of radius $r$)

More precisely (accounting for relative motion):

$$
\ell = \frac{1}{\sqrt{2} \, n \sigma}
$$

## Approach to Equilibrium

### Boltzmann H-theorem

The quantity:

$$
H = \int f(\mathbf{v}) \ln f(\mathbf{v}) \, d^3v
$$

decreases monotonically until equilibrium is reached (Maxwell-Boltzmann distribution). This is related to entropy: $S = -k_B H$.

### Relaxation Time

The time for the system to reach equilibrium scales as:

$$
\tau \sim \frac{\ell}{\langle v \rangle}
$$

## Simulation Algorithm

### Event-Driven Approach

1. Predict the time of the next collision for all pairs
2. Advance to the earliest collision
3. Resolve the collision (update velocities)
4. Recompute affected collision times
5. Repeat

### Time-Stepping Approach (simpler)

1. Move all particles: $\mathbf{r}_i \leftarrow \mathbf{r}_i + \mathbf{v}_i \Delta t$
2. Detect overlaps (distance < $2r$)
3. Resolve overlaps: separate particles and apply collision response
4. Check wall boundaries
5. Repeat

### Numerical Considerations

- **Energy conservation**: total KE should remain constant (no potential energy)
- **Overlap resolution**: must handle multiple simultaneous collisions
- **Time step**: $\Delta t < r / v_{\text{max}}$ to prevent tunneling through partners
- **Boundary conditions**: reflecting walls or periodic boundaries
