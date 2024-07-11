import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import os

def get_interfered_image(freq, amplitude_X, amplitude_Y, blur, noise, width, scan_speed_num, use_synch_50, save_image=False):
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
    def add_interference_to_image(image_path, output_path, scan_speed_time_per_px, frequency, amplitude_X, amplitude_Y, use_synch_50, blur=0, noise=0):
        # Načtení obrázku
        image = plt.imread(image_path)[:, :, :3] #bere jen prvni tri RGB kanaly, alfu zahodi
        grayscale_image = convert_to_grayscale_image(image)
        # showGrayscaleImage(grayscale_image)
        background = create_uniform_color_image(grayscale_image, intensity=0)

        if blur > 0:
            grayscale_image = apply_blur_matplotlib(grayscale_image, blur_radius=blur)
            # showGrayscaleImage(grayscale_image)


        interfered_image = apply_interference(grayscale_image, background, scan_speed_time_per_px, frequency, amplitude_X, amplitude_Y, use_synch_50)
        if noise > 0:
            interfered_image = add_gaussian_noise(interfered_image, std=noise)
            # showGrayscaleImage(grayscale_image)
        show_grayscale_image(interfered_image, outPath=None, show=False, name=None)
        return interfered_image


        # Zobrazení a uložení změněného obrázku
    def apply_interference(image, background, scan_speed_time_per_px, frequency, amplitude_X, amplitude_Y, use_synch_50):
        height, width = image.shape
        interfered_image = background

        # skenovani pixel po pixelu
        time = np.float32(0)
        for i in range(height):
            for j in range(width):
                omega = 2 * np.pi * frequency
                displacement_X = amplitude_X * np.sin(omega * time) # v pixelech
                displacement_Y = amplitude_Y * np.sin(omega * time) # v pixelech
                # print(displacement)

                displaced_location_i = i + round(displacement_Y) # index vychylene pozice na radku
                displaced_location_j = j + round(displacement_X) # index vychylene pozice v sloupci
                if displaced_location_i > height-1 or displaced_location_j > width-1: # kdyz jsem mimo obraz, necham cerne pozadi
                    pass
                else:
                    interfered_image[i, j] = image[displaced_location_i, displaced_location_j] # prirazeni jasu vychyleneho mista na skenovany pixel
                time += scan_speed_time_per_px
            if use_synch_50:
                time += 0.02 - (time % np.float32(0.02))
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
        return fig, ax
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

    def create_folder_if_not_exist(path):
        if not os.path.exists(path):
            os.makedirs(path)

    # Nastavte cestu k obrázku a cestu pro výstup
    input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
    # scan_speed = 32e-6  # rychlost skenování v sec/pixel
    scan_speeds_time_per_px = [100e-9, 320e-9, 1e-6, 3.2e-6, 10e-6, 32e-6, 100e-6, 320e-6, 1e-3, 3.2e-3]   # rychlost skenování v sec/pixel


    scan_speed_time_per_px = scan_speeds_time_per_px[scan_speed_num-1]


    if save_image:
        output_image_name = f"interfered_image_blur_{blur}_noise_{noise}_XAmp_{amplitude_X}_YAmp_{amplitude_Y}_ss{scan_speed_num}"
        name = f"{output_image_name}_freq={np.round(freq,2)} Hz"
        out_folder = rf"ss{scan_speed_num}\blur_{blur}_noise_{noise}_XAmp_{amplitude_X}_YAmp_{amplitude_Y}_ss{scan_speed_num}"
        create_folder_if_not_exist(out_folder)
        out_path = rf"{out_folder}\{name}.png"
    else:
        out_path = None

    interfered_image = add_interference_to_image(input_image_path, out_path, scan_speed_time_per_px, freq, amplitude_X, amplitude_Y, use_synch_50=use_synch_50, blur=blur, noise=noise)

    return show_grayscale_image(interfered_image, show=False)