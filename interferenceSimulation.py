import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors


def add_interference_to_image(image_path, output_path, scan_speed, frequency, amplitude, blur=0):
    # Načtení obrázku
    image = plt.imread(image_path)[:, :, :3] #bere jen prvni tri RGB kanaly, alfu zahodi
    interfered_image = create_uniform_color_image(image, color_rgb=(0,0,0))
    # maxInt = max([max(sum(i)) for i in image])
    # print(maxInt)
    # Získání šířky a výšky obrázku
    height, width, _ = image.shape
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)

    # Procházení pixelů a změna barvy
    time = 0
    for i in range(height):
        for j in range(width):
            # Získání původní barvy pixelu
            original_color = image[i, j, :]

            # Zde můžete provádět různé úpravy barev, například inverzi barvy
            modified_color = original_color
            omega = 2 * np.pi * frequency
            displacement = amplitude * np.sin(omega * time)
            # print(displacement)
            # Přiřazení změněné barvy zpět do obrázku
            displaced_location_i = i + int(displacement)
            displaced_location_j = j + int(displacement)
            if displaced_location_i > height-1 or displaced_location_j > width-1:
                pass
            else:
                interfered_image[displaced_location_i, displaced_location_j, :] = modified_color
            time += scan_speed

    # Zobrazení a uložení změněného obrázku
    if blur > 0:
        interfered_image = apply_blur_matplotlib(interfered_image, blur_radius=blur)

    ax.imshow(interfered_image)
    plt.axis('off')
    plt.savefig(output_path)
    plt.show()


def hex_to_rgb(hex_color):
    return tuple(round(val * 255) for val in mcolors.to_rgb(hex_color))
def create_uniform_color_image(image, color_rgb):
    # Načtení rozměrů vstupního obrázku
    height, width, _ = image.shape
    # color_rgb = hex_to_rgb(hex_color)
    # Vytvoření černého obrázku
    uniform_color_image = np.ones((height, width, 3)) * color_rgb
    # uniform_color_image = np.zeros((height, width, 3))
    # # Zobrazení a uložení černého obrázku
    # fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    # ax.imshow(uniform_color_image)
    # plt.axis('off')
    # # plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='black')
    # plt.show()
    return uniform_color_image

def apply_blur_matplotlib(input_image, blur_radius):
    # Vytvoření transformace s Gaussovským rozmazáním
    from scipy.ndimage import gaussian_filter

    transform = Affine2D().scale(blur_radius, blur_radius)
    blurred_image = gaussian_filter(input_image, sigma=blur_radius)
    # Uložení výsledného obrázku
    return blurred_image

# Nastavte cestu k obrázku a cestu pro výstup
input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
output_image_path = "outImage.png"
scan_speed = 32e-6  # rychlost skenování v sec/pixel
frequency = 100  # frekvence pohybu vzorku Hz
amplitude = 5  # amplituda pohybu vzorku v pixelech

# Volání funkce pro změnu barev obrázku
add_interference_to_image(input_image_path, output_image_path, scan_speed, frequency, amplitude, blur=0)
print(f"Obrázek byl změněn a uložen do souboru: {output_image_path}")
