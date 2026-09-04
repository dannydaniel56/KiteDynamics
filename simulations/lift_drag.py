import numpy as np
import matplotlib.pyplot as plt

# Calculate lift for a kite
def calculate_lift(density, velocity, area, lift_coefficient):
    return 0.5 * density * velocity**2 * area * lift_coefficient

# Example values
density = 1.225  # kg/m³ (air at sea level)
velocity = 10     # m/s (wind speed)
area = 1.5        # m² (kite surface)
lift_coefficient = 0.8  # typical for a kite

lift = calculate_lift(density, velocity, area, lift_coefficient)
print(f"Lift force: {lift:.2f} N")

# Plot lift vs wind speed
velocities = np.linspace(0, 20, 100)
lifts = calculate_lift(density, velocities, area, lift_coefficient)

plt.plot(velocities, lifts)
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Lift Force (N)')
plt.title('Kite Lift vs Wind Speed')
plt.grid()
plt.show()
