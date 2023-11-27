# import matplotlib.pyplot as plt
# import numpy as np
#
# def create_noisy_scanned_image(input_image_path, scan_speed, frequency, amplitude, output_path):
#     # Načtení existujícího obrázku
#     image = plt.imread(input_image_path)
#
#     # Získání šířky a výšky obrázku
#     height, width, _ = image.shape
#
#     fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
#     ax.set_xlim(0, width)
#     ax.set_ylim(0, height)
#     ax.set_aspect('equal', adjustable='box')
#     ax.set_facecolor('black')  # nastavení černého pozadí pro osu
#
#     # Simulace rušení pohybem vzorku
#     for i in image:
#         for j in i:
#
#             displacement = amplitude * np.sin(2 * np.pi * frequency * i / amplitude)
#             displaced_pixel = np.roll(image[i, :, :], int(displacement * width))
#             ax.plot(displaced_row, color='white', linewidth=1)
#
#     plt.axis('off')
#     plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='black')
#     plt.show()
#
# # Nastavte parametry podle potřeby
# input_image_path = "random_circles_image_matplotlib.png"
# scan_speed = 1  # rychlost skenování v pixelech na řádek
# frequency = 0.05  # frekvence pohybu vzorku
# amplitude = 0.5  # amplituda pohybu vzorku
# output_path = "noisy_scanned_image.png"
#
# create_noisy_scanned_image(input_image_path, scan_speed, frequency, amplitude, output_path)
# print(f"Obrázek byl vytvořen a uložen do souboru: {output_path}")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D


def modify_image_colors(image_path, output_path, scan_speed, frequency, amplitude):
    # Načtení obrázku
    image = plt.imread(image_path)[:, :, :3] #bere jen prvni tri RGB kanaly, alfu zahodi
    interfered_image = create_black_image_like(input_image_path, output_image_path)

    # Získání šířky a výšky obrázku
    height, width, _ = image.shape

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
            print(displacement)
            # Přiřazení změněné barvy zpět do obrázku
            displaced_location_i = i + int(displacement)
            displaced_location_j = j + int(displacement)
            if displaced_location_i > height-1 or displaced_location_j > width-1:
                pass
            else:
                interfered_image[displaced_location_i, displaced_location_j, :] = modified_color
            time += scan_speed

    # Zobrazení a uložení změněného obrázku
    blurred_image = apply_blur_matplotlib(interfered_image, blur_radius=2)
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.imshow(blurred_image)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='black')
    plt.show()



def create_black_image_like(input_image_path, output_path):
    # Načtení rozměrů vstupního obrázku
    input_image = plt.imread(input_image_path)
    height, width, _ = input_image.shape

    # Vytvoření černého obrázku
    black_image = np.zeros((height, width, 3))
    return black_image

    # # Zobrazení a uložení černého obrázku
    # fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    # ax.imshow(black_image)
    # plt.axis('off')
    # plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='black')
    # plt.show()

def apply_blur_matplotlib(input_image, blur_radius=2):
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
modify_image_colors(input_image_path, output_image_path, scan_speed, frequency, amplitude)
print(f"Obrázek byl změněn a uložen do souboru: {output_image_path}")
