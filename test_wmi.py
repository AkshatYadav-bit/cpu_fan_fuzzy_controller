import wmi

w = wmi.WMI(namespace="root\\LibreHardwareMonitor")

for sensor in w.Sensor():
    print(sensor.SensorType, "|", sensor.Name, "|", sensor.Value)