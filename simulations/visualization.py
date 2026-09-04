import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------------------------------
# Physics setup
# -------------------------------
g = 9.81               # gravity (m/s²)
rho = 1.225            # air density (kg/m³)
mass = 0.5             # kite mass (kg)
area = 1.2             # kite surface area (m²)
CL = 0.8               # lift coefficient
CD = 0.3               # drag coefficient
wind_speed = 8.0       # constant wind (m/s)

# Initial conditions
x, y = 0.0, 1.5        # position (m)
vx, vy = 0.0, 0.0      # velocity (m/s)
dt = 0.02              # time step (s)
t_max = 15.0           # simulation duration (s)

# Store trajectory
trail_x, trail_y = [], []

# -------------------------------
# Physics update function
# -------------------------------
def update_kite():
    global x, y, vx, vy, trail_x, trail_y

    # Relative wind (wind pushes kite horizontally)
    vx_rel = wind_speed - vx
    vy_rel = -vy
    V_rel = np.sqrt(vx_rel**2 + vy_rel**2)

    if V_rel < 0.01:
        return

    # Dynamic pressure
    q = 0.5 * rho * V_rel**2 * area

    # Lift and drag forces (perpendicular & parallel to relative wind)
    L = q * CL
    D = q * CD

    # Force components in world coordinates
    angle = np.arctan2(vy_rel, vx_rel)
    Fx = L * np.sin(angle) - D * np.cos(angle)
    Fy = L * np.cos(angle) + D * np.sin(angle) - mass * g

    # Update velocities and positions
    vx += (Fx / mass) * dt
    vy += (Fy / mass) * dt
    x += vx * dt
    y += vy * dt

    # Ground collision (bounce / stop)
    if y < 0.3:
        y = 0.3
        vy = abs(vy) * 0.4
        vx *= 0.95

    # Keep within view (optional soft boundary)
    if x > 35:
        x = 35
        vx *= -0.5

    trail_x.append(x)
    trail_y.append(y)

    # Keep trail length manageable
    if len(trail_x) > 150:
        trail_x.pop(0)
        trail_y.pop(0)

# -------------------------------
# Animation setup
# -------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-2, 40)
ax.set_ylim(0, 18)
ax.set_xlabel("Horizontal distance (m)")
ax.set_ylabel("Height (m)")
ax.set_title("🪁 Kite Flight Simulation with Wind & Physics")
ax.grid(True, linestyle='--', alpha=0.5)

# Kite as a triangle + tail
kite_patch = plt.Polygon([[0, 0], [0.4, 0.6], [-0.4, 0.6]], 
                         closed=True, color='red', ec='darkred')
tail_line, = ax.plot([], [], 'b--', linewidth=1.5, alpha=0.6)
trail_line, = ax.plot([], [], 'orange', linewidth=2, alpha=0.5)

# Wind arrow
wind_arrow = ax.quiver(0, 16, 1, 0, scale=20, color='gray', alpha=0.5,
                       angles='xy', scale_units='xy')
ax.text(2, 16.2, f'Wind → {wind_speed} m/s', fontsize=9, color='gray')

# Info text (will be updated)
info_text = ax.text(0.5, 0.95, '', transform=ax.transAxes,
                    fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle="round", facecolor='white', alpha=0.7))

# Add kite patch to plot
ax.add_patch(kite_patch)

# -------------------------------
# Animation function
# -------------------------------
def animate(frame):
    global kite_patch, trail_line, info_text

    # Run physics for a few steps per frame for smoother motion
    for _ in range(3):
        update_kite()

    # Update kite position
    kite_patch.set_xy([[x - 0.4, y - 0.2],
                       [x, y + 0.5],
                       [x + 0.4, y - 0.2]])

    # Update tail (simple trailing line)
    tail_x = [x - 0.2, x - 0.6, x - 1.0, x - 1.4]
    tail_y = [y - 0.3, y - 0.6, y - 0.9, y - 1.1]
    tail_line.set_data(tail_x, tail_y)

    # Update trail
    if len(trail_x) > 1:
        trail_line.set_data(trail_x, trail_y)

    # Update info text
    V = np.sqrt(vx**2 + vy**2)
    info_text.set_text(f'Height: {y:.1f} m  |  Speed: {V:.1f} m/s  |  Time: {frame*dt*3:.1f}s')

    return kite_patch, tail_line, trail_line, info_text

# -------------------------------
# Run animation
# -------------------------------
ani = animation.FuncAnimation(fig, animate, frames=int(t_max/dt/3),
                              interval=30, blit=True, repeat=True)

plt.tight_layout()
plt.show()
