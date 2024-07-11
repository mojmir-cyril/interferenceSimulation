import pickle
import numpy as np
import matplotlib.pyplot as plt

def namer(name, sufix):
    i = 0
    import os
    format = "02d"
    while os.path.exists(f"{name}_{i:02d}.{sufix}"):
        i += 1
    return f"{name}_{i:02d}.{sufix}"
# Funkce pro vykreslení bodů
def draw_points():
    global n_pix
    ax.clear()
    ax.set_xlim(0, n_pix)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True)
    if points:  # Kontrola, zda existují nějaké body k vykreslení
        x_vals, y_vals = zip(*sorted(points.items()))
        ax.plot(x_vals, y_vals, "ro-")  # Vykreslí body červenými kruhy a spojí čarou

# Funkce pro reakci na události myši
def on_mouse_event(event):
    if event.button == 1:  # Pouze při stisknutém levém tlačítku myši
        if event.xdata is not None and event.ydata is not None:
            x = round(event.xdata)
            y = event.ydata
            global n_pix
            if 0 <= x <= n_pix:  # Omezení x na celá čísla od 0 do n_pix
                points[x] = y  # Přidání nebo aktualizace bodu
                draw_points()
                fig.canvas.draw()
def on_scroll(event):
    ax.set_xlim([lim * (1.1 if event.button == 'up' else 0.9) for lim in ax.get_xlim()])
    ax.set_ylim([lim * (1.1 if event.button == 'up' else 0.9) for lim in ax.get_ylim()])
    draw_points()
    fig.canvas.draw()

# Inicializace seznamu bodů
n_pix = 160
points = {}

# Inicializace grafu Matplotlib
fig, ax = plt.subplots()
ax.set_xlim(0, n_pix)
ax.set_ylim(-1.5, 1.5)  # Přizpůsobte dle potřeby
ax.grid(True)

# Připojení událostí kliknutí a tažení myši
fig.canvas.mpl_connect('button_press_event', on_mouse_event)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_event)
fig.canvas.mpl_connect('scroll_event', on_scroll)

plt.show()


x_vals, y_vals = zip(*sorted(points.items()))
print(f"points: {x_vals, y_vals}")

path = namer(fr"curves\curve_periods=2_Npx={n_pix}", "p")
# Po zavření grafu provádí lineární interpolaci
if points:  # Kontrola, zda existují nějaké body pro interpolaci
    x_vals, y_vals = zip(*sorted(points.items()))
    x_new = np.arange(0, n_pix)  # Cílové hodnoty x pro interpolaci
    y_new = np.interp(x_new, x_vals, y_vals)  # Lineární interpolace
    interpolated_points = zip(x_new, y_new)
    # Vrácení interpolovaných hodnot
    print("Interpolované hodnoty:")
    print("x_vals:", x_new)
    print("y_vals:", y_new)
    pickle.dump(interpolated_points, open(path, "wb"))
    np.savetxt(path[:-2]+".txt", list(interpolated_points))