import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import os


def convert_to_grayscale_image(image):
    # Manual conversion to grayscale using luminance formula
    image = np.dot(image[..., :3], [0.299, 0.587, 0.114])

    # Scale and clip the values to the range [0, 255]
    image = (np.clip(image, 0, 255) * 255).astype(int)
    return image
def convert_acc_spectrum_to_disp(acc_spectrum): #TODO
    freqs = acc_spectrum[0]
    omegas = 2 * np.pi * freqs
    return acc_spectrum[1] / omegas ** 2
def create_time_dependent_oscilation(displacement_spectrum, fs): #TODO
    l = len(displacement_spectrum)
    time = np.linspace(0, 1/fs * l, l) # zkontrolovat
    displacement_time = np.fft.ifft(displacement_spectrum) # jak zarucit, aby byl output skutecne v jednotkach delky se spravnym scale?
    return np.array([time, displacement_time])
def interpolate_time_value(): # TODO
    pass
def add_interference_to_image(image_path, output_path, scan_speed, frequency, amplitude, blur=0, noise=0):
    # Načtení obrázku
    image = plt.imread(image_path)[:, :, :3] #bere jen prvni tri RGB kanaly, alfu zahodi
    grayscale_image = convert_to_grayscale_image(image)
    # showGrayscaleImage(grayscale_image)
    background = create_uniform_color_image(grayscale_image, intensity=0)

    if blur > 0:
        grayscale_image = apply_blur_matplotlib(grayscale_image, blur_radius=blur)
        # showGrayscaleImage(grayscale_image)


    interfered_image = apply_interference(grayscale_image, background, scan_speed, frequency, amplitude)
    if noise > 0:
        interfered_image = add_gaussian_noise(interfered_image, std=noise)
        # showGrayscaleImage(grayscale_image)
    show_grayscale_image(interfered_image, outPath=output_path, show=False, name=name)
    return interfered_image


    # Zobrazení a uložení změněného obrázku
def apply_interference(image, background, scan_speed, frequency, amplitude):
    height, width = image.shape
    interfered_image = background

    # skenovani pixel po pixelu
    time = 0
    for i in range(height):
        for j in range(width):
            omega = 2 * np.pi * frequency
            displacement = amplitude * np.sin(omega * time) # v pixelech, zatim pro oba smery stejna vychylka
            # print(displacement)

            displaced_location_i = i + int(displacement) # index vychylene pozice na radku
            displaced_location_j = j + int(displacement) # index vychylene pozice v sloupci
            if displaced_location_i > height-1 or displaced_location_j > width-1: # kdyz jsem mimo obraz, necham cerne pozadi
                pass
            else:
                interfered_image[i, j] = image[displaced_location_i, displaced_location_j] # prirazeni jasu vychyleneho mista na skenovany pixel
            time += scan_speed
    return interfered_image
def show_grayscale_image(image, outPath=None, show=True, name=None):
    height, width = image.shape
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.imshow(image, cmap="gray",vmin=0, vmax=255)
    plt.axis('off')
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    plt.margins(0, 0)
    if outPath != None:
        plt.savefig(outPath)
    if name != None:
        fig.canvas.manager.set_window_title(name)
    if show:
        plt.show()
    else:
        plt.close(fig)
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
def update_image(frame_number):
    ax2.imshow(list_images[frame_number], cmap="gray", vmin=0, vmax=255)
    # ax2.title.set_text(f'{np.round(freq,2)} Hz')
    ax2.set_title(f'{np.round(list_freqs[frame_number],2)} Hz')
    text.set(text=f'{np.round(list_freqs[frame_number], 2)} Hz')
    print(f"{frame_number} of {num_of_samples}")

def create_folder_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Nastavte cestu k obrázku a cestu pro výstup
input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
# scan_speed = 32e-6  # rychlost skenování v sec/pixel
scan_speeds = [100e-9, 320e-9, 1e-6, 3.2e-6, 10e-6, 32e-6, 100e-6, 320e-6, 1e-3, 3.2e-3]   # rychlost skenování v sec/pixel
scan_speed_num = range(1,11)   # rychlost skenování v sec/pixel

# frequency = 13  # frekvence pohybu vzorku Hz
amplitude = 6  # amplituda pohybu vzorku v pixelech
blur = 5
noise = 20

start_freq = 0
end_freq = 300
num_of_samples = 100

for scan_speed, scan_speed_num in zip(scan_speeds, scan_speed_num):
    output_image_name = f"interfered_image_blur_{blur}_noise_{noise}_XYAmp_{amplitude}_ss{scan_speed_num}"

    # Volání funkce pro změnu barev obrázku
    dict_interfered_images = {}
    # n_row = 6
    # n_col = 10
    freqs = np.linspace(start_freq,end_freq,num_of_samples)
    for freq in freqs:
        name = f"{output_image_name}_freq={np.round(freq,2)} Hz"
        out_folder = rf"ss{scan_speed_num}\blur_{blur}_noise_{noise}_XYAmp_{amplitude}_ss{scan_speed_num}_freqs_np.linspace({start_freq},{end_freq},{num_of_samples})"
        create_folder_if_not_exist(out_folder)
        out_path = rf"{out_folder}\{name}.png"
        interfered_image = add_interference_to_image(input_image_path, out_path, scan_speed, freq, amplitude, blur=blur, noise=noise)
        dict_interfered_images[freq] = interfered_image


    # fig, axs = plt.subplots(n_row, n_col, figsize=(12, 12),sharex='all',sharey='all')
    # axs = axs.flatten()
    #
    # for img, ax, freq in zip(dict_interfered_images.values(), axs, freqs):
    #     ax.imshow(img, cmap="gray",vmin=0, vmax=255)
    #     ax.title.set_text(f'{np.round(freq,2)} Hz')
    # plt.show()


    list_images = list(dict_interfered_images.values())
    list_freqs = list(dict_interfered_images.keys())


    input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
    image = plt.imread(input_image_path)[:, :, :3] #bere jen prvni tri RGB kanaly, alfu zahodi
    grayscale_image = convert_to_grayscale_image(image)
    height, width = grayscale_image.shape
    fig2, ax2 = plt.subplots(figsize=(width/100, height/100), dpi=100)
    fig2.subplots_adjust(top=1.0, bottom=0, right=1.0, left=0, hspace=0, wspace=0)
    plt.axis('off')
    # plt.gca().set_axis_off()
    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
    #                     hspace=0, wspace=0)
    # plt.margins(0, 0)

    print("start animating")
    text = ax2.text(512, 100, "", size=20, color="white",
             horizontalalignment="center")

    ani = animation.FuncAnimation(fig=fig2, func=update_image, frames=num_of_samples, interval=100)
    print("start saving")
    ani.save(filename=rf"{out_folder}\{output_image_name}.gif", writer="pillow")
    # plt.show()