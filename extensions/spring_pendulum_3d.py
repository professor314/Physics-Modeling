"""
Spring Pendulum — 3D Animated Demo
====================================
Same physics as the original spring.py but rendered in 3D with matplotlib.
The pendulum swings in 3D space (the original gave it a z-velocity push).

You can rotate the view by clicking and dragging. Scroll to zoom.

Run: py extensions/spring_pendulum_3d.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# --- Physics Parameters ---
mass = 1.0
k = 10.0
damping = 0.05
rest_length = 2.0
g = np.array([0.0, -9.8, 0.0])
air_resistance = 0.01

# --- Initial Conditions ---
theta = 7 * np.pi / 8
length = 2.0

pos = np.array([
    length * np.sin(theta),
    -length * np.cos(theta),
    0.0
])
vel = np.array([0.0, 0.0, 0.5])  # push in z-direction for 3D motion

# --- Simulation ---
dt = 1.0 / 32
sub_steps = 100
sub_dt = dt / sub_steps

trail = []  # list of (x, y, z) positions


def simulate_step():
    """Advance physics by one frame."""
    global pos, vel

    for _ in range(sub_steps):
        r = np.linalg.norm(pos)
        S = r - rest_length
        phat = pos / r if r > 1e-10 else np.array([0, -1, 0])

        F_spring = -k * S * phat
        F_damp = np.dot(-damping * vel, phat) * phat
        F_air = -air_resistance * vel
        F_gravity = mass * g

        F_net = F_spring + F_damp + F_air + F_gravity
        acc = F_net / mass
        vel = vel + acc * sub_dt
        pos = pos + vel * sub_dt

    trail.append(pos.copy())
    if len(trail) > 600:
        trail.pop(0)


def generate_helix(start, end, n_coils=10, radius=0.08):
    """Generate 3D helix points between start and end for spring visual."""
    direction = end - start
    length = np.linalg.norm(direction)
    if length < 1e-10:
        return np.array([[0, 0, 0]])

    # Build local coordinate frame
    z_axis = direction / length

    # Find a vector not parallel to z_axis
    if abs(z_axis[0]) < 0.9:
        ref = np.array([1, 0, 0])
    else:
        ref = np.array([0, 1, 0])

    x_axis = np.cross(z_axis, ref)
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)

    n_points = n_coils * 20
    t = np.linspace(0, 1, n_points)
    theta = np.linspace(0, n_coils * 2 * np.pi, n_points)

    points = np.zeros((n_points, 3))
    for i in range(n_points):
        center = start + t[i] * direction
        offset = radius * (np.cos(theta[i]) * x_axis + np.sin(theta[i]) * y_axis)
        points[i] = center + offset

    return points


# --- 3D Visualization ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(-3, 3)
ax.set_ylim(-4, 1)
ax.set_zlim(-3, 3)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Spring Pendulum — 3D\n(drag to rotate, scroll to zoom)')

# Plot elements
spring_line, = ax.plot([], [], [], 'b-', linewidth=1.2)
bob_dot, = ax.plot([], [], [], 'ro', markersize=12)
trail_line, = ax.plot([], [], [], 'c-', linewidth=0.8, alpha=0.5)
pivot_dot, = ax.plot([0], [0], [0], 'ks', markersize=8)


def animate(frame):
    """Animation frame callback."""
    simulate_step()

    # Spring helix from origin to bob
    origin = np.array([0.0, 0.0, 0.0])
    helix = generate_helix(origin, pos)
    spring_line.set_data(helix[:, 0], helix[:, 1])
    spring_line.set_3d_properties(helix[:, 2])

    # Bob
    bob_dot.set_data([pos[0]], [pos[1]])
    bob_dot.set_3d_properties([pos[2]])

    # Trail
    if trail:
        t_arr = np.array(trail)
        trail_line.set_data(t_arr[:, 0], t_arr[:, 1])
        trail_line.set_3d_properties(t_arr[:, 2])

    return spring_line, bob_dot, trail_line


ani = animation.FuncAnimation(
    fig, animate, interval=int(dt * 1000), blit=False, cache_frame_data=False
)

plt.tight_layout()
plt.show()
