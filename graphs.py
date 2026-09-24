# this below specific file is vibe-coded
from cpu_fan import *
import os
import matplotlib.pyplot as plt


FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)


def plot_temperature_memberships():
    x_values = range(0, 101)

    plt.figure(figsize=(10, 6))

    for name, params in temperature.items():
        y_values = [
            triangular(x, params) if len(params) == 3
            else trapezoid(x, params)
            for x in x_values
        ]
        plt.plot(x_values, y_values, label=name.upper())

    plt.title("Temperature Membership Functions")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Membership Degree")
    plt.xlim(0, 100)
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "temperature_memberships.png"), dpi=300)
    plt.close()


def plot_cpu_memberships():
    x_values = range(0, 101)

    plt.figure(figsize=(10, 6))

    for name, params in utilization.items():
        y_values = [
            triangular(x, params) if len(params) == 3
            else trapezoid(x, params)
            for x in x_values
        ]
        plt.plot(x_values, y_values, label=name.upper())

    plt.title("CPU Utilization Membership Functions")
    plt.xlabel("CPU Utilization (%)")
    plt.ylabel("Membership Degree")
    plt.xlim(0, 100)
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "cpu_memberships.png"), dpi=300)
    plt.close()


def plot_fan_speed_memberships():
    x_values = range(0, 101)

    plt.figure(figsize=(10, 6))

    for name, params in speed.items():
        y_values = [
            triangular(x, params) if len(params) == 3
            else trapezoid(x, params)
            for x in x_values
        ]
        plt.plot(x_values, y_values, label=name.upper())

    plt.title("Fan Speed Membership Functions")
    plt.xlabel("Fan Speed (%)")
    plt.ylabel("Membership Degree")
    plt.xlim(0, 100)
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fan_speed_memberships.png"), dpi=300)
    plt.close()


def calculate_fan_speed(temp, cpu):
    temp_membership = fuzzify(temperature, temp)
    cpu_membership = fuzzify(utilization, cpu)

    rule_strength = implementFuzzyRules(
        fuzzy_rules,
        temp_membership,
        cpu_membership
    )

    aggregated = aggregate_result(speed, rule_strength)

    return deffuzify(aggregated)


def plot_fan_vs_temperature():
    temperatures = list(range(0, 101))

    # Fixed CPU utilization for this experiment
    fixed_cpu = 50

    fan_speeds = [
        calculate_fan_speed(temp, fixed_cpu)
        for temp in temperatures
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(temperatures, fan_speeds)

    plt.title(f"Fan Speed vs Temperature (CPU = {fixed_cpu}%)")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Recommended Fan Speed (%)")
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fan_speed_vs_temperature.png"), dpi=300)
    plt.close()


def plot_fan_vs_cpu():
    cpu_values = list(range(0, 101))

    # Fixed temperature for this experiment
    fixed_temperature = 70

    fan_speeds = [
        calculate_fan_speed(fixed_temperature, cpu)
        for cpu in cpu_values
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(cpu_values, fan_speeds)

    plt.title(f"Fan Speed vs CPU Utilization (Temperature = {fixed_temperature}°C)")
    plt.xlabel("CPU Utilization (%)")
    plt.ylabel("Recommended Fan Speed (%)")
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "fan_speed_vs_cpu.png"), dpi=300)
    plt.close()


if __name__ == "__main__":
    plot_temperature_memberships()
    plot_cpu_memberships()
    plot_fan_speed_memberships()
    plot_fan_vs_temperature()
    plot_fan_vs_cpu()

    print("Phase 12 graphs generated successfully.")
    print(f"Saved inside: {FIGURES_DIR}/")
