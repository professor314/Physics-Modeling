"""
Spring Pendulum — Animated Demo
================================
A modernized version of the original spring.py / springsim.py simulation.
Uses matplotlib animation instead of the legacy VPython visual module.

Physics: A mass on a spring swinging under gravity with damping.
Method: Euler's method (same as the original).

Run: py extensions/spring_pendulum_demo.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Physics Parameters (same as original springsim.py) ---
mass = 1.0
k = 10.0              # spring constant
damping = 0.05        # spring damping
rest_length = 2.0     # natural length of spring
g = np.array([0, -9.8, 0])
air_resistance = 0.01

# --- Initial Conditions (same as original) ---
theta = 7 * np.pi / 8   # angle from vertical
length = 2.0             # initial extension

# Initial position (spherical to cartesian)
pos = np.array([
    length * np.sin(theta),
    -length * np.cos(theta),
    0.0
])

# Initial velocity (small push in z — we'll use y-component for 2D view)
vel = np.array([0.0, 0.0, 0.5])

# --- Simulation ---
dt = 1.0 / 32       # time step for animation frames
sub_steps = 100      # Euler steps per frame (same as original pend.steps=100)
sub_dt = dt / sub_steps

# Store trail
trail_x = []
trail_y = []


def simulate_step():
    """Advance physics by one animation frame (sub_steps of Euler's method)."""
    global pos, vel

    for _ in range(sub_steps):
        # Extension of spring beyond rest length
        r = np.linalg.norm(pos)
        S = r - rest_length
        phat = pos / r if r > 1e-10 else np.array([0, -1, 0])

        # Forces (same formula as original spring.py)
        F_spring = -k * S * phat
        F_damp = np.dot(-damping * vel, phat) * phat
        F_air = -air_resistance * vel
        F_gravity = mass * g

        F_net = F_spring + F_damp + F_air + F_gravity
        acc = F_net / mass

        vel = vel + acc * sub_dt
        pos = pos + vel * sub_dt

    trail_x.append(pos[0])
    trail_y.append(pos[1])

    # Keep trail to last 500 points
    if len(trail_x) > 500:
        trail_x.pop(0)
        trail_y.pop(0)


# --- Visualization ---
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 2)
ax.set_aspect('equal')
ax.set_title('Spring Pendulum Simulation')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')

# Drawing elements
spring_line, = ax.plot([], [], 'b-', linewidth=1.5, label='Spring')
bob_dot, = ax.plot([], [], 'ro', markersize=15)
trail_line, = ax.plot([], [], 'c-', linewidth=0.5, alpha=0.6, label='Trail')
pivot_dot, = ax.plot([0], [0], 'ks', markersize=8)
ax.legend(loc='upper right')


def draw_spring_coil(start, end, n_coils=12, width=0.15):
    """Generate points for a zigzag spring between start and end."""
    direction = end - start
    length = np.linalg.norm(direction)
    if length < 1e-10:
        return [start[0]], [start[1]]

    unit = direction / length
    perp = np.array([-unit[1], unit[0]])  # perpendicular in 2D

    points_x = [start[0]]
    points_y = [start[1]]

    # Straight lead-in
    lead = 0.1 * length
    p = start + lead * unit
    points_x.append(p[0])
    points_y.append(p[1])

    # Coils
    coil_length = length - 2 * lead
    for i in range(n_coils * 2):
        t = lead + coil_length * (i + 1) / (n_coils * 2 + 1)
        side = width * (1 if i % 2 == 0 else -1)
        p = start + t * unit + side * perp
        points_x.append(p[0])
        points_y.append(p[1])

    # Straight lead-out
    p = end - lead * unit
    points_x.append(p[0])
    points_y.append(p[1])
    points_x.append(end[0])
    points_y.append(end[1])

    return points_x, points_y


def animate(frame):
    """Animation callback — advance physics and update drawing."""
    simulate_step()

    # Draw spring coil from origin to bob
    pivot = np.array([0.0, 0.0])
    bob_pos = np.array([pos[0], pos[1]])
    sx, sy = draw_spring_coil(pivot, bob_pos)
    spring_line.set_data(sx, sy)

    # Draw bob
    bob_dot.set_data([pos[0]], [pos[1]])

    # Draw trail
    trail_line.set_data(trail_x, trail_y)

    return spring_line, bob_dot, trail_line


# Run animation
ani = animation.FuncAnimation(
    fig, animate, interval=int(dt * 1000), blit=True, cache_frame_data=False
)

plt.tight_layout()
plt.show()
