import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Use the controller from your real_system.py
from real_system import calculate_fan_speed


# -----------------------------
# Configuration
# -----------------------------

N = 10_000
RANDOM_SEED = 42

OUTPUT_DIR = Path("test_figures")
OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------
# Generate test dataset
# -----------------------------

rng = np.random.default_rng(RANDOM_SEED)

temperatures = rng.uniform(0, 100, N)
cpu_usages = rng.uniform(0, 100, N)

fan_speeds = np.array([
    calculate_fan_speed(temp, cpu)
    for temp, cpu in zip(temperatures, cpu_usages)
])


# -----------------------------
# Save dataset
# -----------------------------

data = np.column_stack((
    temperatures,
    cpu_usages,
    fan_speeds
))

np.savetxt(
    OUTPUT_DIR / "controller_test_dataset.csv",
    data,
    delimiter=",",
    header="temperature,cpu_usage,recommended_fan_speed",
    comments="",
    fmt="%.6f"
)


# -----------------------------
# Figure 1:
# Distribution of outputs
# -----------------------------

plt.figure(figsize=(8, 5))

plt.hist(fan_speeds, bins=40)

plt.xlabel("Recommended Fan Speed (%)")
plt.ylabel("Number of Test Cases")
plt.title("Distribution of Recommended Fan Speeds")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "fan_speed_distribution.png",
    dpi=150
)
plt.close()


# -----------------------------
# Figure 2:
# Fan speed vs temperature
# -----------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    temperatures,
    fan_speeds,
    s=4,
    alpha=0.25
)

plt.xlabel("CPU Temperature (°C)")
plt.ylabel("Recommended Fan Speed (%)")
plt.title("Recommended Fan Speed vs CPU Temperature")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "fan_speed_vs_temperature.png",
    dpi=150
)
plt.close()


# -----------------------------
# Figure 3:
# Fan speed vs CPU usage
# -----------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    cpu_usages,
    fan_speeds,
    s=4,
    alpha=0.25
)

plt.xlabel("CPU Utilization (%)")
plt.ylabel("Recommended Fan Speed (%)")
plt.title("Recommended Fan Speed vs CPU Utilization")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "fan_speed_vs_cpu_usage.png",
    dpi=150
)
plt.close()


# -----------------------------
# Figure 4:
# Complete controller response
# -----------------------------

temperatures_grid = np.arange(0, 101)
cpu_grid = np.arange(0, 101)

response = np.zeros(
    (len(cpu_grid), len(temperatures_grid))
)

for i, temp in enumerate(temperatures_grid):
    for j, cpu in enumerate(cpu_grid):
        response[j, i] = calculate_fan_speed(
            temp,
            cpu
        )


plt.figure(figsize=(9, 7))

plt.imshow(
    response,
    origin="lower",
    extent=[0, 100, 0, 100],
    aspect="auto"
)

plt.colorbar(
    label="Recommended Fan Speed (%)"
)

plt.xlabel("CPU Temperature (°C)")
plt.ylabel("CPU Utilization (%)")
plt.title("Fuzzy Controller Response Surface")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "controller_response_surface.png",
    dpi=150
)
plt.close()


# -----------------------------
# Test statistics
# -----------------------------

print(f"Generated {N:,} test cases.")

print(
    f"Minimum fan recommendation: "
    f"{fan_speeds.min():.2f}%"
)

print(
    f"Maximum fan recommendation: "
    f"{fan_speeds.max():.2f}%"
)

print(
    f"Mean fan recommendation: "
    f"{fan_speeds.mean():.2f}%"
)

print()
print("Figures saved in:", OUTPUT_DIR)
print(
    "Dataset saved in:",
    OUTPUT_DIR / "controller_test_dataset.csv"
)
