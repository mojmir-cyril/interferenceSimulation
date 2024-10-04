import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import os

class InterferedImage():
    def __init__(self,
                 input_image_path,
                 method,
                 blur,
                 noise,
                 scan_speed_num,
                 synch_freq,
                 dwell_time=None,
                 out_folder=None,
                 crop_to_RT_size=True,
                 show=True,
                 frequency: float=None,
                 amplitude_X: float=None,
                 amplitude_Y: float=None,
                 frequencies: list[float]=None,
                 amplitudes_X:list[float]=None,
                 amplitudes_Y:list[float]=None,
                 spectrum_X=None,
                 spectrum_Y=None,
                 use_amp_phase=False,
                 phases_X=None,
                 phases_Y=None,
                 use_random_phase=False):
        # Nastavte cestu k obrázku a cestu pro výstup
        # input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
        # input_image_path = r"S:\Finalizace\FinalizaceS8000\124-0048, JAR\images\RT_port11\RT_nastrel\TMP_cat-4_Heavy_dumper\02_09_2024\RT_AD_01_1000_Heavy_dump-1.png"
        # scan_speed = 32e-6  # rychlost skenování v sec/pixel
        self.frequency = frequency
        self.amplitude_X = amplitude_X
        self.amplitude_Y = amplitude_Y

        self.frequencies = frequencies
        self.amplitudes_X = amplitudes_X
        self.amplitudes_Y = amplitudes_Y

        self.spectrum_X = spectrum_X
        self.spectrum_Y = spectrum_Y
        self.use_amp_phase = use_amp_phase
        self.phases_X = phases_X
        self.phases_Y = phases_Y
        self.use_random_phase = use_random_phase

        self.image_path = input_image_path
        self.show = show
        self.method = method
        self.blur = blur
        self.noise = noise
        self.scan_speed_num = scan_speed_num
        self.synch_freq = synch_freq
        if dwell_time is not None:
            self.dwell_time = dwell_time
        else:
            scan_speeds_time_per_px = [100e-9, 320e-9, 1e-6, 3.2e-6, 10e-6, 32e-6, 100e-6, 320e-6, 1e-3,
                                       3.2e-3]  # rychlost skenování v sec/pixel
            self.dwell_time = scan_speeds_time_per_px[scan_speed_num - 1]
            scan_speed_time_per_px = scan_speeds_time_per_px[scan_speed_num - 1]
        self.out_folder = out_folder
        self.crop_to_RT_size = crop_to_RT_size
        self.show = show
        self.grayscale_image = self.load_image()
        self.initial_grayscale_image = self.grayscale_image
        self.height, self.width = self.grayscale_image.shape
        self.background = self.create_uniform_color_image(intensity=0)
        self.times = self.generate_times(self.width, self.height, self.dwell_time, flyback_time=0, synch_freq=0)
        # Slovník funkcí
        self.functions = {
            'single_frequency': self.generate_single_freq_signal,
            'multiple_frequency': self.generate_multiple_freq_signal,
            'spectra': self.generate_signal_spectra
        }

        self.output_image_name = f"interfered_image_blur_{self.blur}_noise_{self.noise}_ss{self.scan_speed_num}.png"
        if self.out_folder is not None:
            self.create_folder_if_not_exist(self.out_folder)
            self.output_image_path = os.path.join(out_folder, self.output_image_name)
        else:
            self.output_image_path = None
        self.times = self.generate_times(self.width, self.height, self.dwell_time, flyback_time=0, synch_freq=0)
        self.interfered_image = self.add_interference_to_image()
        self.show_grayscale_image(self.interfered_image)

    def convert_to_grayscale_image(self, image):
        # Manual conversion to grayscale using luminance formula
        image = np.dot(image[..., :3], [0.299, 0.587, 0.114])

        # Scale and clip the values to the range [0, 255]
        image = (np.clip(image, 0, 255) * 255).astype(int)
        return image
    def convert_acc_spectrum_to_disp(self, acc_spectrum): #TODO
        freqs = acc_spectrum[0]
        omegas = 2 * np.pi * freqs
        return acc_spectrum[1] / omegas ** 2
    def create_time_dependent_oscilation(self, displacement_spectrum, fs): #TODO
        l = len(displacement_spectrum)
        time = np.linspace(0, 1/fs * l, l) # zkontrolovat
        displacement_time = np.fft.ifft(displacement_spectrum) # jak zarucit, aby byl output skutecne v jednotkach delky se spravnym scale?
        return np.array([time, displacement_time])
    def interpolate_time_value(): # TODO
        pass
    # def add_interference_to_image(self, image_path, scan_speed_time_per_px, frequency, amplitude_X, amplitude_Y, use_synch_50, blur=0, noise=0, crop_to_RT_size=True):
    #     # Načtení obrázku
    #     image = plt.imread(image_path) #bere jen prvni tri RGB kanaly, alfu zahodi
    #     # Kontrola tvaru
    #     if len(image.shape) == 2:
    #         grayscale_image = (np.clip(image, 0, 255) * 255).astype(int)
    #         print("Obrázek je černobílý.")
    #     elif len(image.shape) == 3:# and image.shape[2] == 3:
    #         grayscale_image = self.convert_to_grayscale_image(image)
    #         print("Obrázek je barevný (RGB).")
    #     # showGrayscaleImage(grayscale_image)
    #     if crop_to_RT_size:
    #         width = grayscale_image.shape[1]
    #         height = 768
    #         grayscale_image = grayscale_image[:height, :width]
    #     background = self.create_uniform_color_image(grayscale_image, intensity=0)
    #
    #     if blur > 0:
    #         grayscale_image = self.apply_blur_matplotlib(grayscale_image, blur_radius=blur)
    #         # showGrayscaleImage(grayscale_image)
    #
    #
    #     interfered_image = self.apply_interference(grayscale_image, background, scan_speed_time_per_px, frequency, amplitude_X, amplitude_Y, use_synch_50)
    #     if noise > 0:
    #         interfered_image = self.add_gaussian_noise(interfered_image, std=noise)
    #         # showGrayscaleImage(grayscale_image)
    #     return interfered_image
    def generate_times(self, width: int, height: int, dwell_time: float, flyback_time: float=0, synch_freq: float=0):
        times = []
        time = 0
        for i in range(height):
            for j in range(width):
                times.append(time)
                time += dwell_time
            if synch_freq != 0:
                time += 1/synch_freq - (time % (1 / synch_freq))
            time += flyback_time
        return np.array(times)
    def generate_single_freq_signal(self, frequency=None, amplitude_X=None, amplitude_Y=None):
        if frequency is None:
            frequency = self.frequency
            amplitude_X = self.amplitude_X
            amplitude_Y = self.amplitude_Y
        omega = 2 * np.pi * frequency
        displacement_X = amplitude_X * np.sin(omega * self.times)  # v pixelech
        displacement_Y = amplitude_Y * np.sin(omega * self.times)  # v pixelech
        return displacement_X, displacement_Y
    def generate_multiple_freq_signal(self):
        if not len(self.frequencies) == len(self.amplitudes_X) == len(self.amplitudes_Y):
            raise Exception("Frequencies and both amplitudes lists must have same length.")
        tot_displacement_X = np.zeros(self.width * self.height)
        tot_displacement_Y = np.zeros(self.width * self.height)
        for freq, amp_x, amp_y in zip(self.frequencies, self.amplitudes_X, self.amplitudes_Y):
            displacement_X, displacement_Y = self.generate_single_freq_signal(freq, amp_x, amp_y)
            tot_displacement_X += displacement_X
            tot_displacement_Y += displacement_Y
        return tot_displacement_X, tot_displacement_Y
    def generate_signal_spectra(self, show=True):
        if self.spectrum_X is None:
            displacement_X = np.zeros(len(self.times))
        else:
            displacement_X = np.interp(self.times, *self.spectrum_to_time_signal(self.spectrum_X, use_random_phase=self.use_random_phase, phases=self.phases_X), left=0, right=0)

        if self.spectrum_Y is None:
            displacement_Y = np.zeros(len(self.times))
        else:
            displacement_Y = np.interp(self.times, *self.spectrum_to_time_signal(self.spectrum_Y, use_random_phase=self.use_random_phase, phases=self.phases_Y), left=0, right=0)

        if show:
            fig, ax = plt.subplots()
            ax.plot(self.times, displacement_X, label='displacement_X')
            ax.plot(self.times, displacement_Y, label='displacement_Y')
            ax.legend()
            ax.grid()
            plt.show()
        return displacement_X, displacement_Y

    def spectrum_to_time_signal(self, spectrum, type="left", phases=None, use_random_phase=False):
        """types: 'left', 'symmetric' """
        orig_freqs = spectrum[0]
        orig_amps = spectrum[1]
        orig_phases = phases if phases is not None else None
        n_orig_samples = len(orig_amps)
        # Časový krok a délka signálu
        reserve_coef = 2 # coeficient to ensure that the signal is long enough after inclusion of freq. synchronization or flybacktime
        n_samples = int(((self.width * self.height * reserve_coef) // 2) * 2) + 1 # Celkový počet vzorků
        delka_signalu = (n_samples - 2) * self.dwell_time   # Celková délka signálu v sekundách

        # Vzorkovací frekvence
        f_s = 1 / self.dwell_time  # Vzorkovací frekvence v Hz



        # Vytvoření komplexního spektra
        spectrum = np.zeros(n_samples - 2, dtype=complex) # nulty clen uberu na obou stranach, proto -2
        # Vytvoření frekvenční osy
        interp_frequencies = np.linspace(0, f_s / 2, n_samples // 2)  # Frekvence od 0 do Nyquistovy frekvence
        frequencies = np.linspace(0, f_s / 2, n_samples // 2 + 1)  # Frekvence od 0 do Nyquistovy frekvence
        # Interpolace amplitud na nové frekvenční body
        interpolated_amplitudes = np.interp(interp_frequencies, orig_freqs, orig_amps, left=0, right=0)

        if type == 'left':
            # # Přiřazení interpolovaných amplitud k frekvencím
            # spectrum[:n_samples // 2] = interpolated_amplitudes + 1j * np.zeros(n_samples // 2)   # Pouze reálná část
            #
            # # Pokud je potřeba, můžeme spektrum symetricky doplnit pro IFFT
            # spectrum[n_samples // 2:] = np.conjugate(spectrum[:n_samples // 2][::-1])  # Symetrie pro reálný časový signál
            if self.use_amp_phase == True:
                if use_random_phase:
                    random_phase = np.random.random(n_samples // 2 - 1) * 2 * np.pi
                    complex_spectrum = interpolated_amplitudes[1:] * (np.cos(random_phase) + 1j * np.sin(random_phase))

                else:
                    interpolated_phases = np.interp(interp_frequencies, orig_freqs, orig_phases, left=0, right=0)
                    complex_spectrum = interpolated_amplitudes[1:] * (np.cos(interpolated_phases[1:]) + 1j * np.sin(interpolated_phases[1:]))

            else:
                complex_spectrum = interpolated_amplitudes[1:] + (1j * np.zeros(n_samples // 2 - 1))

            spectrum[0] = 0
            spectrum[1:(n_samples) // 2] = complex_spectrum
            spectrum[(n_samples) // 2:] = np.conjugate(
                complex_spectrum[::-1])  # Zrcadlení pro získání reálného signálu v časové doméně
        elif type == 'symmetric':
            # TODO
            pass

        # fig, ax = plt.subplots()
        # ax.plot(frequencies, spectrum[:n_samples//2 +1])
        # ax.set_title("Spectrum")
        # plt.show()
        #
        # fig, ax = plt.subplots()
        # ax.plot(spectrum)
        # ax.set_title("Full spectrum")
        # plt.show()

        time_vector = np.arange(0, delka_signalu, self.dwell_time)

        # Provedení IFFT
        window = np.hamming(n_samples)
        time_signal = np.real(np.fft.ifft(spectrum) * (n_samples / 2))
        shortened_time_vector = time_vector[:-2*(n_samples//10)-1]
        shortened_time_signal = time_signal[n_samples//10:-n_samples//10]

        return shortened_time_vector, shortened_time_signal


    def spectrum_to_time_signal_2(self, spectrum, type="left", phases=None, use_random_phase=False):
        """types: 'left', 'symmetric' """
        orig_freqs = spectrum[0]
        orig_amps = spectrum[1][1:]
        orig_phases = phases[1:] if phases is not None else None
        n_orig_samples = len(orig_amps)
        # Časový krok a délka signálu
        reserve_coef = 2 # coeficient to ensure that the signal is long enough after inclusion of freq. synchronization or flybacktime
        n_samples = int(((self.width * self.height * reserve_coef) // 2) * 2) # Celkový počet vzorků
        delka_signalu = n_orig_samples * 1/orig_freqs[-1]   # Celková délka signálu v sekundách


        # Vzorkovací frekvence
        f_s = 1 / self.dwell_time  # Vzorkovací frekvence v Hz



        # Vytvoření komplexního spektra
        spectrum = np.zeros(n_orig_samples * 2 + 1, dtype=complex)
        # # Vytvoření frekvenční osy
        # frequencies = np.linspace(0, f_s / 2, n_samples // 2)  # Frekvence od 0 do Nyquistovy frekvence
        # # Interpolace amplitud na nové frekvenční body
        # interpolated_amplitudes = np.interp(frequencies, orig_freqs, orig_amps, left=0, right=0)

        if type == 'left':
            # # Přiřazení interpolovaných amplitud k frekvencím
            # spectrum[:n_samples // 2] = interpolated_amplitudes + 1j * np.zeros(n_samples // 2)   # Pouze reálná část
            #
            # # Pokud je potřeba, můžeme spektrum symetricky doplnit pro IFFT
            # spectrum[n_samples // 2:] = np.conjugate(spectrum[:n_samples // 2][::-1])  # Symetrie pro reálný časový signál
            if self.use_amp_phase == True:
                if use_random_phase:
                    random_phase = np.random.random(n_orig_samples) * 2 * np.pi
                    complex_spectrum = (orig_amps * (np.cos(random_phase) + 1j * np.sin(random_phase)))
                    spectrum[0] = 0
                    spectrum[1:n_orig_samples+1] = complex_spectrum
                    spectrum[n_orig_samples+1:] = np.conjugate(complex_spectrum[::-1])  # Zrcadlení pro získání reálného signálu v časové doméně

                else:
                    complex_spectrum = orig_amps * (np.cos(orig_phases) + 1j * np.sin(orig_phases))
                    spectrum[:n_orig_samples] = complex_spectrum
                    spectrum[n_orig_samples+1:] = np.conjugate(
                        spectrum[:n_orig_samples][::-1])  # Zrcadlení pro získání reálného signálu v časové doméně
            else:
                spectrum[:n_orig_samples] = orig_amps + (1j * np.zeros(n_orig_samples))
                spectrum[n_orig_samples+1:] = np.conjugate(spectrum[:n_orig_samples][::-1])  # Zrcadlení pro získání reálného signálu v časové doméně

        elif type == 'symmetric':
            # TODO
            pass

        fig, ax = plt.subplots()
        ax.plot(orig_freqs[:n_orig_samples], spectrum[:n_orig_samples])
        ax.set_title("Spectrum")
        plt.show()

        fig, ax = plt.subplots()
        ax.plot(spectrum)
        ax.set_title("Full spectrum")
        plt.show()

        time_vector = np.arange(0, delka_signalu * 2 + 1/orig_freqs[-1], 1/orig_freqs[-1])

        # Provedení IFFT
        window = np.hamming(n_samples)
        time_signal = np.real(np.fft.ifft(spectrum ) * n_orig_samples)
        # shortened_time_vector = time_vector[:-2*(n_orig_samples//10)-1]
        # shortened_time_signal = time_signal[n_orig_samples//10:-n_orig_samples//10]
        shortened_time_vector = time_vector
        shortened_time_signal = time_signal

        return shortened_time_vector, shortened_time_signal

    # Funkce pro volání správné funkce na základě parametru
    def generate_signal(self, func_name, **kwargs):
        func = self.functions.get(func_name)
        if func:
            return func(**kwargs)
        else:
            raise ValueError(f"Function {func_name} not found")

    # # Příklad použití
    # print(generate_signal('single_frequency'))  # Výstup: 6
    # print(generate_signal('multiple_frequency', x=2, y=3))  # Výstup: 6
    # print(generate_signal('spectra', x=1, y=2, z=3))  # Výstup: 6

    def load_image(self):
        # Načtení obrázku
        image = plt.imread(self.image_path)  # bere jen prvni tri RGB kanaly, alfu zahodi
        # Kontrola tvaru
        if len(image.shape) == 2:
            grayscale_image = (np.clip(image, 0, 255) * 255).astype(int)
            print("Obrázek je černobílý.")
        elif len(image.shape) == 3:  # and image.shape[2] == 3:
            grayscale_image = self.convert_to_grayscale_image(image)
            print("Obrázek je barevný (RGB).")
        # showGrayscaleImage(grayscale_image)
        if self.crop_to_RT_size:
            width = grayscale_image.shape[1]
            height = 768
            grayscale_image = grayscale_image[:height, :width]
        return grayscale_image
    def add_interference_to_image(self):
        image = self.grayscale_image
        self.time_displacements_X, self.time_displacements_Y = self.generate_signal(func_name=self.method)
        if self.method == "sing":
            pass
        if self.blur > 0:
            image = self.apply_blur_matplotlib(image, blur_radius=self.blur)
        interfered_image = self.apply_interference(image, self.time_displacements_X, self.time_displacements_Y)
        if self.noise > 0:
            interfered_image = self.add_gaussian_noise(interfered_image, std=self.noise)
        return interfered_image


        # Zobrazení a uložení změněného obrázku
    def apply_interference(self, image, time_displacements_X: np.ndarray, time_displacements_Y: np.ndarray):
        # if self.blur > 0:
        #     image = self.blurred_image
        # else:
        #     image = self.grayscale_image
        height, width = image.shape
        interfered_image = self.background
        n_pixels = width * height
        if n_pixels != len(time_displacements_X) or n_pixels != len(time_displacements_Y):
            raise Exception("Num of pixels and length of times, time_displacements_X and time_displacements_Y array must be the same.")
        k = 0
        # skenovani pixel po pixelu
        for i in range(height):
            for j in range(width):
                displacement_X = time_displacements_X[k] # v pixelech
                displacement_Y = time_displacements_Y[k] # v pixelech
                # print(displacement)

                displaced_location_i = i + round(displacement_Y) # index vychylene pozice na radku
                displaced_location_j = j + round(displacement_X) # index vychylene pozice v sloupci
                if displaced_location_i > height-1 or displaced_location_j > width-1: # kdyz jsem mimo obraz, necham cerne pozadi
                    pass
                else:
                    interfered_image[i, j] = image[displaced_location_i, displaced_location_j] # prirazeni jasu vychyleneho mista na skenovany pixel
                k += 1

        return interfered_image
    def show_grayscale_image(self, image):
        fig, ax = plt.subplots(figsize=(self.width/100, self.height/100), dpi=100)
        ax.imshow(image, cmap="gray",vmin=0, vmax=255)
        plt.axis('off')
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)
        plt.margins(0, 0)
        if self.output_image_path != None:
            plt.savefig(self.output_image_path)
        if self.output_image_name != None:
            fig.canvas.manager.set_window_title(self.output_image_name)
        if self.show:
            plt.show()
        else:
            plt.close(fig)
        return fig, ax
    def create_uniform_color_image(self, intensity):
        # Vytvoření černého obrázku
        uniform_color_image = np.ones((self.height, self.width)) * intensity
        # Zobrazení a uložení černého obrázku
        # showGrayscaleImage(uniform_color_image)

        return uniform_color_image

    def apply_blur_matplotlib(self, input_image, blur_radius):
        # Vytvoření transformace s Gaussovským rozmazáním
        from scipy.ndimage import gaussian_filter

        transform = Affine2D().scale(blur_radius, blur_radius)
        blurred_image = gaussian_filter(input_image, sigma=blur_radius)
        # Uložení výsledného obrázku
        return blurred_image

    def add_gaussian_noise(self, image, std, mean=0):
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

    def create_folder_if_not_exist(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

