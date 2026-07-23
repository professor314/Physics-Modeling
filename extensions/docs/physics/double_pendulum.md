# Double Pendulum Physics

## Overview

The double pendulum consists of two pendulum arms connected end-to-end. Despite its simple construction, it exhibits chaotic behavior — extreme sensitivity to initial conditions that makes long-term prediction impossible.

## System Description

- **Arm 1**: length $L_1$, mass $m_1$ at its end, angle $\theta_1$ from vertical
- **Arm 2**: length $L_2$, mass $m_2$ at its end, angle $\theta_2$ from vertical

The pivot of arm 2 is at the end of arm 1.

## Lagrangian Mechanics

For the double pendulum, Newtonian force analysis becomes unwieldy due to constraint forces. The **Lagrangian** approach eliminates constraints naturally.

### Positions

$$
x_1 = L_1 \sin\theta_1, \quad y_1 = -L_1 \cos\theta_1
$$

$$
x_2 = L_1 \sin\theta_1 + L_2 \sin\theta_2, \quad y_2 = -L_1 \cos\theta_1 - L_2 \cos\theta_2
$$

### Kinetic Energy

$$
T = \frac{1}{2} m_1 (\dot{x}_1^2 + \dot{y}_1^2) + \frac{1}{2} m_2 (\dot{x}_2^2 + \dot{y}_2^2)
$$

Expanding:

$$
T = \frac{1}{2}(m_1 + m_2) L_1^2 \dot{\theta}_1^2 + \frac{1}{2} m_2 L_2^2 \dot{\theta}_2^2 + m_2 L_1 L_2 \dot{\theta}_1 \dot{\theta}_2 \cos(\theta_1 - \theta_2)
$$

### Potential Energy

$$
U = -(m_1 + m_2) g L_1 \cos\theta_1 - m_2 g L_2 \cos\theta_2
$$

### The Lagrangian

$$
\mathcal{L} = T - U
$$

### Euler-Lagrange Equations

For each generalized coordinate $q_i$:

$$
\frac{d}{dt}\frac{\partial \mathcal{L}}{\partial \dot{q}_i} - \frac{\partial \mathcal{L}}{\partial q_i} = 0
$$

## Equations of Motion

Applying the Euler-Lagrange equations gives two coupled second-order ODEs:

### Angular Acceleration of Arm 1

$$
\ddot{\theta}_1 = \frac{-g(2m_1 + m_2)\sin\theta_1 - m_2 g \sin(\theta_1 - 2\theta_2) - 2\sin(\theta_1 - \theta_2)\,m_2\left[\dot{\theta}_2^2 L_2 + \dot{\theta}_1^2 L_1 \cos(\theta_1 - \theta_2)\right]}{L_1\left[2m_1 + m_2 - m_2\cos(2\theta_1 - 2\theta_2)\right]}
$$

### Angular Acceleration of Arm 2

$$
\ddot{\theta}_2 = \frac{2\sin(\theta_1 - \theta_2)\left[\dot{\theta}_1^2 L_1(m_1 + m_2) + g(m_1 + m_2)\cos\theta_1 + \dot{\theta}_2^2 L_2 m_2 \cos(\theta_1 - \theta_2)\right]}{L_2\left[2m_1 + m_2 - m_2\cos(2\theta_1 - 2\theta_2)\right]}
$$

## State Vector

The system has 4 degrees of freedom: $[\theta_1, \theta_2, \dot{\theta}_1, \dot{\theta}_2]$.

The derivatives are:

$$
\frac{d}{dt}\begin{pmatrix} \theta_1 \\ \theta_2 \\ \dot{\theta}_1 \\ \dot{\theta}_2 \end{pmatrix} = \begin{pmatrix} \dot{\theta}_1 \\ \dot{\theta}_2 \\ \ddot{\theta}_1(\theta_1, \theta_2, \dot{\theta}_1, \dot{\theta}_2) \\ \ddot{\theta}_2(\theta_1, \theta_2, \dot{\theta}_1, \dot{\theta}_2) \end{pmatrix}
$$

## Energy Conservation

Total energy (Hamiltonian) is conserved:

$$
E = T + U = \text{constant}
$$

This serves as the primary numerical accuracy diagnostic.

## Chaos

### Sensitivity to Initial Conditions

Two trajectories starting with angular difference $\delta\theta \sim 10^{-10}$ will diverge exponentially:

$$
|\Delta\theta(t)| \sim |\Delta\theta(0)| \, e^{\lambda t}
$$

where $\lambda > 0$ is the largest **Lyapunov exponent**.

### Practical Implications

- Prediction horizon: $t_{\text{max}} \sim \frac{1}{\lambda} \ln\left(\frac{\Delta\theta_{\text{max}}}{\Delta\theta_0}\right)$
- For typical parameters: prediction valid for ~5-10 oscillation periods
- Beyond this, behavior is statistically predictable but not deterministically

### Phase Space Structure

The phase space is 4-dimensional. Poincaré sections (2D slices) reveal:
- **Regular motion** at low energies (near-integrable, KAM tori)
- **Chaotic seas** at high energies
- **Islands of stability** embedded within chaotic regions

## Small-Angle Approximation

For small oscillations ($\theta_1, \theta_2 \ll 1$), the system linearizes to coupled harmonic oscillators with two normal modes:

**In-phase mode:** Both arms swing together
$$
\omega_-^2 \approx \frac{g}{L_1 + L_2}
$$

**Anti-phase mode:** Arms swing opposite
$$
\omega_+^2 \approx \frac{g(m_1 + m_2)}{m_2 L_1}
$$

## Numerical Considerations

- Use **RK4** for short-time accuracy (energy conservation to ~$10^{-10}$ per period)
- Use **symplectic integrators** for long-time statistics
- Monitor energy conservation: $|E(t) - E(0)| / |E(0)| < 10^{-8}$ indicates good integration
- Time step: $\Delta t \leq 0.01 \sqrt{L/g}$ for stability at high energies
