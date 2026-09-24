import tkinter as tk
import psutil
import threading
import pythoncom
import time
from collections import deque

from real_system import get_cpu_temperature, calculate_fan_speed

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- GRAPH DATA ----------------

time_data = deque(maxlen=60)
temperature_data = deque(maxlen=60)
cpu_data = deque(maxlen=60)
fan_data = deque(maxlen=60)

start_time = time.time()

graph_window = None
canvas = None


# ---------------- SYSTEM READING ----------------

def read_system():
    pythoncom.CoInitialize()

    try:
        temp = get_cpu_temperature()
        cpu = psutil.cpu_percent(interval=0.2)

        if temp is not None:
            fan_speed = calculate_fan_speed(temp, cpu)

            root.after(
                0,
                update_labels,
                temp,
                cpu,
                fan_speed
            )

    finally:
        pythoncom.CoUninitialize()

    root.after(1000, start_reading)


def start_reading():
    threading.Thread(
        target=read_system,
        daemon=True
    ).start()


# ---------------- GUI UPDATE ----------------

def update_labels(temp, cpu, fan_speed):

    temp_label.config(
        text=f"{temp:.2f} °C"
    )

    cpu_label.config(
        text=f"{cpu:.2f} %"
    )

    fan_label.config(
        text=f"{fan_speed:.2f} %"
    )

    # Store data for graph
    elapsed = time.time() - start_time

    time_data.append(elapsed)
    temperature_data.append(temp)
    cpu_data.append(cpu)
    fan_data.append(fan_speed)

    update_graph()


# ---------------- LIVE GRAPH ----------------

def open_graph():

    global graph_window, canvas

    # Don't create multiple graph windows
    if graph_window is not None and graph_window.winfo_exists():
        graph_window.lift()
        return

    graph_window = tk.Toplevel(root)

    graph_window.title("Live System Graph")
    graph_window.geometry("900x700")

    figure = Figure(
        figsize=(8, 6),
        dpi=100
    )

    ax1 = figure.add_subplot(311)
    ax2 = figure.add_subplot(312)
    ax3 = figure.add_subplot(313)

    canvas = FigureCanvasTkAgg(
        figure,
        master=graph_window
    )

    canvas.get_tk_widget().pack(
        fill=tk.BOTH,
        expand=True
    )

    # Store axes and figure
    graph_window.figure = figure
    graph_window.ax1 = ax1
    graph_window.ax2 = ax2
    graph_window.ax3 = ax3

    update_graph()


def update_graph():

    if graph_window is None:
        return

    if not graph_window.winfo_exists():
        return

    ax1 = graph_window.ax1
    ax2 = graph_window.ax2
    ax3 = graph_window.ax3

    # Temperature
    ax1.clear()
    ax1.plot(
        time_data,
        temperature_data
    )

    ax1.set_title("CPU Temperature")
    ax1.set_ylabel("Temperature (°C)")
    ax1.grid(True)

    # CPU utilization
    ax2.clear()
    ax2.plot(
        time_data,
        cpu_data
    )

    ax2.set_title("CPU Utilization")
    ax2.set_ylabel("CPU (%)")
    ax2.grid(True)

    # Fan speed
    ax3.clear()
    ax3.plot(
        time_data,
        fan_data
    )

    ax3.set_title("Recommended Fan Speed")
    ax3.set_ylabel("Fan Speed (%)")
    ax3.set_xlabel("Time (seconds)")
    ax3.grid(True)

    graph_window.figure.tight_layout()

    canvas.draw_idle()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Fuzzy CPU Fan Controller")
root.geometry("500x350")


tk.Label(
    root,
    text="Fuzzy CPU Fan Controller",
    font=("Arial", 20)
).pack(pady=20)


tk.Label(
    root,
    text="CPU Temperature"
).pack()

temp_label = tk.Label(
    root,
    text="-- °C",
    font=("Arial", 16)
)

temp_label.pack()


tk.Label(
    root,
    text="CPU Utilization"
).pack()

cpu_label = tk.Label(
    root,
    text="-- %",
    font=("Arial", 16)
)

cpu_label.pack()


tk.Label(
    root,
    text="Recommended Fan Speed"
).pack()

fan_label = tk.Label(
    root,
    text="-- %",
    font=("Arial", 16)
)

fan_label.pack()


# ---------------- GRAPH BUTTON ----------------

tk.Button(
    root,
    text="Live Graph",
    command=open_graph,
    font=("Arial", 12)
).pack(pady=20)


# Initialize psutil measurement
psutil.cpu_percent(interval=None)

# Start background worker
start_reading()

root.mainloop()