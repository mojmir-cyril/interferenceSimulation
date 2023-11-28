import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors

def convert_to_grayscale_image(image):
    # Manual conversion to grayscale using luminance formula
    image = np.dot(image[..., :3], [0.299, 0.587, 0.114])

    # Scale and clip the values to the range [0, 255]
    image = (np.clip(image, 0, 255) * 255).astype(int)
    return image
def add_interference_to_image(image_path, output_path, scan_speed, frequency, amplitude, blur=0, noise=0):
    # Načtení obrázku
    image = plt.imread(image_path)[:, :, :3] #bere jen prvni tri RGB kanaly, alfu zahodi
    grayscale_image = convert_to_grayscale_image(image)
    # showGrayscaleImage(grayscale_image)
    background = create_uniform_color_image(grayscale_image, intensity=0)

    if blur > 0:
        grayscale_image = apply_blur_matplotlib(grayscale_image, blur_radius=blur)
        # showGrayscaleImage(grayscale_image)

    if noise > 0:
        grayscale_image = add_gaussian_noise(grayscale_image, std=noise)
        # showGrayscaleImage(grayscale_image)


    interfered_image = applyInterference(grayscale_image, background)
    showGrayscaleImage(interfered_image, outPath="outImage1")


    # Zobrazení a uložení změněného obrázku
def applyInterference(image, background):
    # Procházení pixelů a změna barvy
    height, width = image.shape
    time = 0
    interfered_image = background
    for i in range(height):
        for j in range(width):
            # Získání původní barvy pixelu
            original_color = image[i, j]

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
                interfered_image[i, displaced_location_j] = modified_color
            time += scan_speed
    return interfered_image
def showGrayscaleImage(image, outPath=None):
    height, width = image.shape
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.imshow(image, cmap="gray",vmin=0, vmax=255)
    plt.axis('off')
    if outPath != None:
        plt.savefig(outPath)
    plt.show()
def create_uniform_color_image(image, intensity):
    # Načtení rozměrů vstupního obrázku
    height, width = image.shape
    # Vytvoření černého obrázku
    uniform_color_image = np.ones((height, width)) * intensity
    # Zobrazení a uložení černého obrázku
    # showGrayscaleImage(uniform_color_image)

    return uniform_color_image

def apply_blur_matplotlib(input_image, blur_radius):
    # Vytvoření transformace s Gaussovským rozmazáním
    from scipy.ndimage import gaussian_filter

    transform = Affine2D().scale(blur_radius, blur_radius)
    blurred_image = gaussian_filter(input_image, sigma=blur_radius)
    # Uložení výsledného obrázku
    return blurred_image

def add_gaussian_noise(image, std, mean=0):
    """
    Adds Gaussian noise to an image.

    Parameters:
    - image: NumPy array representing the image
    - mean: Mean of the Gaussian distribution (default: 0)
    - std: Standard deviation of the Gaussian distribution (default: 25)

    Returns:
    - Noisy image as a NumPy array
    """
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = image + noise
    noisy_image = np.clip(noisy_image, 0, 255)  # Ensure values are in the valid range [0, 255]
    return noisy_image

# Nastavte cestu k obrázku a cestu pro výstup
input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
output_image_path = "outImage.png"
scan_speed = 32e-6  # rychlost skenování v sec/pixel
frequency = 13  # frekvence pohybu vzorku Hz
amplitude = 10  # amplituda pohybu vzorku v pixelech

# Volání funkce pro změnu barev obrázku
add_interference_to_image(input_image_path, output_image_path, scan_speed, frequency, amplitude, blur=5, noise=100)
print(f"Obrázek byl změněn a uložen do souboru: {output_image_path}")
