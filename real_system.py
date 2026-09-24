import psutil
from cpu_fan import *
import wmi

def calculate_fan_speed(x,y):
    temp_membership = fuzzify(temperature,x)
    cpu_membership= fuzzify(utilization,y)

    ruleStrength = implementFuzzyRules(fuzzy_rules,temp_membership,cpu_membership)
    aggregated = aggregate_result(speed,ruleStrength)
    fan_speed = deffuzify(aggregated)
    return fan_speed
def get_cpu_temperature():
    w = wmi.WMI(namespace="root\\LibreHardwareMonitor")

    for sensor in w.Sensor():
        if sensor.SensorType == "Temperature" and sensor.Name == "CPU Package":
            return float(sensor.Value)

    return None

if __name__ =="__main__":
    temp = get_cpu_temperature()
    cpu = psutil.cpu_percent(interval=1)

    fan_speed = calculate_fan_speed(temp, cpu)

    print(f"Temperature: {temp}°C")
    print(f"CPU Usage: {cpu}%")
    print(f"Recommended Fan Speed: {fan_speed:.2f}%")