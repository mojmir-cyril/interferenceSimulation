import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from interference_simulation_single_frame import get_interfered_image

# Hlavní okno aplikace
root = tk.Tk()
root.title("Image Control GUI with Multiple Amplitude Options and Previous Controls")
canvas_interfered_widget = None
fig_interfered = None


def update_image():
    # Přidání grafu do Tkinter okna
    amplitude_X, amplitude_Y, freq, blur, noise, scan_speed_num, dwell_time, flyback_time, use_synch_50 = get_current_values()
    scan_speed_num = int(scan_speed_num)
    width = 1024
    height = 768
    global canvas_interfered_widget, fig_interfered
    if canvas_interfered_widget is not None:
        canvas_interfered_widget.pack_forget()
    fig_interfered, _ = get_interfered_image(freq=freq, amplitude_X=amplitude_X, amplitude_Y=amplitude_Y, blur=blur, noise=noise, width=width, scan_speed_num=scan_speed_num, use_synch_50=use_synch_50)
    canvas_interfered = FigureCanvasTkAgg(fig_interfered, master=image_frame)
    canvas_interfered_widget = canvas_interfered.get_tk_widget()
    canvas_interfered_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def save_image():
    global fig_interfered
    if fig_interfered is not None:
        # Otevření dialogu pro výběr souboru
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if filepath:
            # Uložení obrázku do zvolené cesty
            fig_interfered.savefig(filepath)

# Funkce pro aktualizaci hodnoty posuvníku z textového pole
def update_slider_from_entry(slider, entry):
    value = entry.get()
    try:
        slider.set(float(value))
    except ValueError:
        pass  # Neplatná hodnota zůstane ignorována

# Funkce pro aktualizaci hodnoty textového pole z posuvníku
def update_entry_from_slider(slider, entry):
    entry.delete(0, tk.END)
    entry.insert(0, str(slider.get()))

# Funkce pro procházení souborů
def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

# Skrytí nebo zobrazení prvků pro různé metody zadávání amplitud
def show_frame(frame):
    for f in amplitude_frames.values():
        f.pack_forget()
    frame.pack()


# Přepínání mezi různými možnostmi zadávání amplitud
def on_amplitude_option_change():
    option = amplitude_option_var.get()
    show_frame(amplitude_frames[option])

# Vytvoření rámců
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

control_frame = ttk.LabelFrame(main_frame, text="Controls")
control_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

image_frame = ttk.LabelFrame(main_frame, text="Image")
image_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)



# Rámce pro různé metody zadávání amplitud
single_frequency_frame = ttk.Frame(control_frame)
import_spectrum_frame = ttk.Frame(control_frame)
draw_spectrum_frame = ttk.Frame(control_frame)

amplitude_frames = {
    "single_frequency": single_frequency_frame,
    "import_spectrum": import_spectrum_frame,
    "draw_spectrum": draw_spectrum_frame
}

# # Single frequency - posuvníky a textová pole pro zadávání hodnot
# for i, name in enumerate(["X AMP", "Y AMP", "Frequency"]):
#     ttk.Label(single_frequency_frame, text=name).pack()
#     slider = ttk.Scale(single_frequency_frame, from_=0, to=100 if name != "Frequency" else 1000, orient="horizontal")
#     slider.pack()
#     entry = ttk.Entry(single_frequency_frame, width=6)
#     entry.pack()
#     slider.bind("<Motion>", lambda event, s=slider, e=entry: update_entry_from_slider(s, e))
#     entry.bind("<Return>", lambda event, s=slider, e=entry: update_slider_from_entry(s, e))

# Seznam proměnných pro uchování hodnot posuvníků
slider_values_single_freq = [tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()]

# Seznam pro uchování vstupních polí
entry_widgets = []

for i, (name, min_max_val) in enumerate({"X AMP": (0, 100), "Y AMP": (0, 100), "Frequency": (1, 10000)}.items()):
    ttk.Label(single_frequency_frame, text=name).pack()
    slider = ttk.Scale(single_frequency_frame, from_=min_max_val[0], to=min_max_val[1], orient="horizontal", variable=slider_values_single_freq[i])
    slider.pack()
    entry = ttk.Entry(single_frequency_frame, width=6, textvariable=slider_values_single_freq[i])
    entry.pack()
    entry_widgets.append(entry)
    slider.bind("<Motion>", lambda event, s=slider, e=entry: update_entry_from_slider(s, e))
    entry.bind("<Return>", lambda event, s=slider, e=entry: update_slider_from_entry(s, e))

# Funkce pro získání aktuálních hodnot
def get_current_values():
    amplitude_X, amplitude_Y, freq = [var.get() for var in slider_values_single_freq]
    blur, noise = [var.get() for var in slider_values_blur_noise]
    scan_speed_num = slider_value_scanning_speed_num.get()
    dwell_time = dwell_time_var.get()
    flyback_time = flyback_time_var.get()
    use_synch_50 = use_synch_50_var.get()
    return amplitude_X, amplitude_Y, freq, blur, noise, scan_speed_num, dwell_time, flyback_time, use_synch_50

def set_default_values():
    [var.set(0) for var in slider_values_single_freq]
    [var.set(0) for var in slider_values_blur_noise]
    slider_value_scanning_speed_num.set(6)
    dwell_time_var.set(0)
    flyback_time_var.set(0)
    use_synch_50_var.set(False)


# Import spectrum - vstupní pole a tlačítka pro procházení
for axis in ["X", "Y"]:
    ttk.Label(import_spectrum_frame, text=f"{axis} Spectrum File").pack()
    entry = ttk.Entry(import_spectrum_frame)
    entry.pack()
    browse_button = ttk.Button(import_spectrum_frame, text="Browse", command=lambda e=entry: browse_file(e))
    browse_button.pack()

# Radio buttons pro výběr metody zadávání amplitud
amplitude_option_var = tk.StringVar(value="single_frequency")
ttk.Radiobutton(control_frame, text="Single Frequency", variable=amplitude_option_var, value="single_frequency", command=on_amplitude_option_change).pack(anchor=tk.W)
ttk.Radiobutton(control_frame, text="Import Spectrum", variable=amplitude_option_var, value="import_spectrum", command=on_amplitude_option_change).pack(anchor=tk.W)
ttk.Radiobutton(control_frame, text="Draw Spectrum", variable=amplitude_option_var, value="draw_spectrum", command=on_amplitude_option_change).pack(anchor=tk.W)

def update_slider(slider, entry):
    slider.set(entry.get())

def update_entry(slider, entry):
    entry.delete(0, tk.END)
    entry.insert(0, slider.get())

# Funkce pro ovládání stavu rozšířených možností
def toggle_advanced():
    if advanced_var.get():
        for widget in advanced_widgets:
            widget['state'] = 'normal'

    else:
        for widget in advanced_widgets:
            widget['state'] = 'disabled'




main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

control_frame = ttk.LabelFrame(main_frame, text="Controls")
control_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

slider_values_blur_noise = [tk.DoubleVar(), tk.DoubleVar()]

# Posuvníky a názvy
sliders = {}
entries = {}
for i, (name, max_val) in enumerate({"BLUR": 40, "NOISE": 100}.items()):
    ttk.Label(control_frame, text=name).grid(row=i*2, column=0, sticky="W")
    slider = ttk.Scale(control_frame, from_=0, to=max_val, orient="horizontal", variable=slider_values_blur_noise[i])
    slider.grid(row=i*2+1, column=0, sticky="EW")
    entry = ttk.Entry(control_frame, width=4, textvariable=slider_values_blur_noise[i])
    entry.grid(row=i*2+1, column=1)
    slider.bind("<Motion>", lambda event, s=slider, e=entry: update_entry(s, e))
    entry.bind("<Return>", lambda event, s=slider, e=entry: update_slider(s, e))
    sliders[name] = slider
    entries[name] = entry

slider_value_scanning_speed_num =  tk.DoubleVar()
for i, (name, max_val) in enumerate({"Scanning Speed": (1, 10)}.items()):
    i=2
    def round_to_integer(value):
        return round(float(value))
    ttk.Label(control_frame, text=name).grid(row=i*2, column=0, sticky="W")
    slider = ttk.Scale(control_frame, from_=max_val[0], to=max_val[1], orient="horizontal", command=lambda val: slider_value_scanning_speed_num.set(round_to_integer(val)), variable=slider_value_scanning_speed_num)
    # Funkce pro zaokrouhlení hodnoty na nejbližší celé číslo

    # Připojte funkci k slideru, která zaokrouhlí hodnotu na celé číslo
    # slider.configure(command=lambda val: scan_speed_var.set(int(float(val))))
    slider.grid(row=i*2+1, column=0, sticky="EW")
    entry = ttk.Entry(control_frame, width=4, textvariable=slider_value_scanning_speed_num)
    entry.grid(row=i*2+1, column=1)
    slider.bind("<Motion>", lambda event, s=slider, e=entry: update_entry(s, e))
    entry.bind("<Return>", lambda event, s=slider, e=entry: update_slider(s, e))
    sliders[name] = slider
    entries[name] = entry

interfere_button = ttk.Button(root, text="Interfere", command=update_image)
interfere_button.pack()
# interfere_button.pack(anchor=tk.W)
#
# # Radio buttons pro scan speed
# scan_speed_var = tk.IntVar()
# scan_speed_buttons = {}
# for i in range(1, 11):
#     radio = ttk.Radiobutton(control_frame, text=str(i), variable=scan_speed_var, value=i)
#     radio.grid(row=i+8, column=0, sticky="W")
#     scan_speed_buttons[i] = radio

# use synch 50 button
use_synch_50_var = tk.BooleanVar()
check_synch_50 = ttk.Checkbutton(control_frame, text="Use 50 Hz synch", variable=use_synch_50_var, command=toggle_advanced)
check_synch_50.grid(row=18, column=0, sticky="W")

# Check button pro advanced setup
advanced_var = tk.BooleanVar()
check = ttk.Checkbutton(control_frame, text="Advanced setup", variable=advanced_var, command=toggle_advanced)
check.grid(row=19, column=0, sticky="W")


dwell_time_var =  tk.StringVar()
flyback_time_var =  tk.StringVar()
# Rozšířené nastavení
advanced_widgets = []
dwell_label = ttk.Label(control_frame, text="Dwell Time:")
dwell_label.grid(row=20, column=0, sticky="W")
dwell_time = ttk.Entry(control_frame, width=7, state='disabled', textvariable=dwell_time_var)
dwell_time.grid(row=20, column=1, sticky="W")
advanced_widgets.append(dwell_time)

flyback_label = ttk.Label(control_frame, text="Flyback Time:")
flyback_label.grid(row=21, column=0, sticky="W")
flyback_time = ttk.Entry(control_frame, width=7, state='disabled', textvariable=flyback_time_var)
flyback_time.grid(row=21, column=1, sticky="W")
advanced_widgets.append(flyback_time)



import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


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
canvas = FigureCanvasTkAgg(fig, master=draw_spectrum_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



# Připojení událostí
canvas.mpl_connect('button_press_event', on_mouse_event)
canvas.mpl_connect('button_release_event', on_mouse_event)
canvas.mpl_connect('motion_notify_event', on_motion)
canvas.mpl_connect('scroll_event', on_scroll)

# # Zobrazení výchozí metody zadávání amplitud
on_amplitude_option_change()

# Přidání tlačítka pro uložení obrázku
save_button = ttk.Button(root, text="Uložit obrázek", command=save_image)
save_button.pack(side=tk.RIGHT, padx=5, pady=5)

set_default_values()
# initaial reference image
fig_interfered, _ = get_interfered_image(freq=0, amplitude_X=0, amplitude_Y=0, blur=0,
                                         noise=0, width=0, scan_speed_num=1, use_synch_50=False)
canvas_interfered = FigureCanvasTkAgg(fig_interfered, master=image_frame)
canvas_interfered_widget = canvas_interfered.get_tk_widget()
canvas_interfered_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()
