# SIR / SEIR Epidemic Models

## Overview

Compartmental models divide a population into distinct groups (compartments) based on disease status. The SIR model is the simplest useful epidemic model; SEIR adds a latent period.

## SIR Model

### Compartments

| Symbol | Meaning |
|--------|---------|
| $S$ | **Susceptible** — individuals who can catch the disease |
| $I$ | **Infected** — currently infectious individuals |
| $R$ | **Recovered** — immune or removed individuals |

### Flow Diagram

$$
S \xrightarrow{\beta S I} I \xrightarrow{\gamma I} R
$$

### Differential Equations

$$
\frac{dS}{dt} = -\beta S I
$$

$$
\frac{dI}{dt} = \beta S I - \gamma I
$$

$$
\frac{dR}{dt} = \gamma I
$$

### Parameters

| Parameter | Meaning | Typical Range |
|-----------|---------|---------------|
| $\beta$ | Transmission rate | $10^{-5}$ to $10^{-3}$ (pre-normalized) |
| $\gamma$ | Recovery rate | $1/14$ to $1/3$ day$^{-1}$ |
| $N = S + I + R$ | Total population | Conserved quantity |

### Conservation Law

Adding all three equations:

$$
\frac{d}{dt}(S + I + R) = 0
$$

Total population $N$ is always conserved — this serves as a numerical invariant check.

## Basic Reproduction Number $R_0$

$$
R_0 = \frac{\beta N}{\gamma}
$$

**Interpretation:** The average number of secondary infections produced by one infected individual in a fully susceptible population.

- $R_0 > 1$: epidemic grows exponentially initially
- $R_0 < 1$: epidemic dies out
- $R_0 = 1$: threshold between growth and decline

### Epidemic Peak Condition

The infected population peaks when $dI/dt = 0$:

$$
\beta S I - \gamma I = 0 \implies S_{\text{peak}} = \frac{\gamma}{\beta} = \frac{N}{R_0}
$$

### Herd Immunity Threshold

The fraction of the population that must be immune to prevent epidemic growth:

$$
p_c = 1 - \frac{1}{R_0}
$$

## Final Size Relation

The total fraction of the population ever infected (the "attack rate") satisfies the transcendental equation:

$$
\ln\left(\frac{S_\infty}{S_0}\right) = -R_0 \left(1 - \frac{S_\infty}{N}\right)
$$

where $S_\infty$ is the susceptible population as $t \to \infty$.

## SEIR Model

### Additional Compartment

| Symbol | Meaning |
|--------|---------|
| $E$ | **Exposed** — infected but not yet infectious (latent period) |

### Flow Diagram

$$
S \xrightarrow{\beta S I} E \xrightarrow{\sigma E} I \xrightarrow{\gamma I} R
$$

### Differential Equations

$$
\frac{dS}{dt} = -\beta S I
$$

$$
\frac{dE}{dt} = \beta S I - \sigma E
$$

$$
\frac{dI}{dt} = \sigma E - \gamma I
$$

$$
\frac{dR}{dt} = \gamma I
$$

### Parameters

| Parameter | Meaning |
|-----------|---------|
| $\sigma$ | Rate of progression from exposed to infectious |
| $1/\sigma$ | Average incubation (latent) period |

### $R_0$ for SEIR

The basic reproduction number is unchanged from SIR:

$$
R_0 = \frac{\beta N}{\gamma}
$$

The incubation period delays the epidemic but does not change $R_0$ because $E$ individuals eventually become $I$.

## Numerical Considerations

- **Population conservation** ($S + I + R = N$ or $S + E + I + R = N$) should be monitored as a numerical health check
- **Non-negativity**: Compartments should never go negative; large time steps with Euler can violate this
- **Stiff systems**: When $\beta N \gg \gamma$, the system can become stiff — RK4 handles this better than Euler
- Typical time step: $\Delta t = 0.1$ days for most parameter regimes

## Extensions

- **SIS**: No immunity (recovered return to susceptible)
- **SIRS**: Temporary immunity (R → S after waning)
- **SEIRS**: Combines exposed compartment with waning immunity
- **Age-structured**: Different parameters for age groups
- **Spatial**: Multiple connected populations (metapopulation models)
