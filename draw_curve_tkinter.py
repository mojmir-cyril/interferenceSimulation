import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Vytvoření Tkinter okna
root = tk.Tk()
root.title("Interaktivní Graf v Tkinter")

# Vytvoření figure a axis pro Matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(-1.5, 1.5)
ax.grid(True)

# Inicializace seznamu bodů
points = {}

# Pomocné proměnné pro posouvání grafu a kreslení
is_dragging = False
is_drawing = False  # Proměnná pro detekci kreslení

# Funkce pro vykreslení bodů
def draw_points():
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True)
    if points:
        x_vals, y_vals = zip(*sorted(points.items()))
        ax.plot(x_vals, y_vals, "ro-")
    canvas.draw()

# Funkce pro reakci na události myši
def on_mouse_event(event):
    global is_dragging, is_drawing
    if event.name == "button_press_event":
        if event.button == 1 and event.xdata is not None and event.ydata is not None:
            is_drawing = True  # Povolit kreslení
            add_or_update_point(event.xdata, event.ydata)
        elif event.button == 3:
            is_dragging = True
            canvas.get_tk_widget().config(cursor="fleur")
    elif event.name == "button_release_event":
        if event.button == 1:
            is_drawing = False  # Zakázat kreslení po uvolnění levého tlačítka
        elif event.button == 3:
            is_dragging = False
            canvas.get_tk_widget().config(cursor="")

def add_or_update_point(x, y):
    x = round(x)
    if 0 <= x <= 100:
        points[x] = y
        draw_points()

def on_motion(event):
    global previous_mouse_position
    if is_dragging and event.xdata is not None and event.ydata is not None:
        # Logika pro posouvání
        dx = previous_mouse_position[0] - event.xdata if previous_mouse_position[0] else 0
        dy = previous_mouse_position[1] - event.ydata if previous_mouse_position[1] else 0
        ax.set_xlim(ax.get_xlim()[0] + dx, ax.get_xlim()[1] + dx)
        ax.set_ylim(ax.get_ylim()[0] + dy, ax.get_ylim()[1] + dy)
        previous_mouse_position = (event.xdata, event.ydata)
        draw_points()
    elif is_drawing and event.xdata is not None and event.ydata is not None:
        # Přidání bodů při tažení s aktivním kreslením
        add_or_update_point(event.xdata, event.ydata)

def on_scroll(event):
    # Logika pro zoomování
    if event.button == 'up':
        scale_factor = 1.1
    else:  # down
        scale_factor = 1 / 1.1
    ax.set_xlim([lim * scale_factor for lim in ax.get_xlim()])
    ax.set_ylim([lim * scale_factor for lim in ax.get_ylim()])
    draw_points()

# Přidání grafu do Tkinter okna
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Připojení událostí
canvas.mpl_connect('button_press_event', on_mouse_event)
canvas.mpl_connect('button_release_event', on_mouse_event)
canvas.mpl_connect('motion_notify_event', on_motion)
canvas.mpl_connect('scroll_event', on_scroll)

root.mainloop()
