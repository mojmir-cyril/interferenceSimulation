import numpy as np
from scipy.signal import correlate
import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm

path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\curves\curve_periods=2_Npx=160_03.p"
interpolated_points = pickle.load(open(path, "rb"))
interpolated_points = list(interpolated_points)
xs = [i[0] for i in interpolated_points]
ys = [i[1] for i in interpolated_points]
print(interpolated_points)

fig, ax = plt.subplots()
ax.plot(xs, ys)
plt.show()
def apply_noise(carrier_signal, noise_std):
    if noise_std != 0:
        # Parametry šumu
        noise_mean = 0  # střední hodnota (průměr) šumu
        noise_std = noise_std  # standardní odchylka šumu
        noise_length = len(carrier_signal)  # délka šumu odpovídá délce nosného signálu

        # Generování Gaussovského šumu
        noise = np.random.normal(noise_mean, noise_std, noise_length)

        # Přidání šumu k nosnému signálu
        return carrier_signal + noise
    else:
        return carrier_signal

def get_shifted_array(array : np.ndarray, length : int, shift: int):
    shift = int(shift)
    orig_length = len(array)
    max_amp = (orig_length - length) // 2
    if max_amp < shift:
       raise Exception("Amplitude exceeds bounds given by original array.")
    else:
        center_ind = (orig_length // 2 - 1)
        lower_ind = center_ind - (length // 2 - 1)
        upper_ind = center_ind + (length // 2 - 1)
        return array[lower_ind + shift : upper_ind + shift]

fs = 5000
freq = 100
times = np.arange(0, 10, 1/fs)
amp = 10
shifts = amp * np.sin(2 * np.pi * freq * times)

# fig2, ax2 = plt.subplots()
# ax2.plot(times, shifts)
# plt.show()

img_arrays = []
n_pix = 100
for time, shift in zip(times, shifts):
    img_arrays.append(get_shifted_array(ys, n_pix, shift))

noise_std = 1

fig = plt.figure()
hann = np.hanning(len(img_arrays[0]))
ref_img_array = apply_noise(img_arrays[0], noise_std=noise_std)
ref_img_array_norm = (ref_img_array - np.mean(ref_img_array)) / np.std(ref_img_array)
ref_img_array_norm = ref_img_array_norm * hann

normalize = mcolors.Normalize(vmin=times.min(), vmax=times.max())
colormap = cm.jet
plt.plot(ref_img_array_norm, label="reference curve")
# calculates optimal shift to reference curve for each of the curves
n_curves_to_plot = 15
di = len(times) // n_curves_to_plot
optimal_shifts = []
for i, time, img_array in zip(range(len(times)), times, img_arrays):
    img_array = apply_noise(img_array, noise_std=noise_std)
    img_array_norm = (img_array - np.mean(img_array)) / np.std(img_array)
    img_array_norm = img_array_norm * hann
    correlations = correlate(ref_img_array_norm, img_array_norm, method="direct")
    optimal_shift = np.argmax(correlations) - len(ref_img_array_norm) + 1
    optimal_shifts.append(optimal_shift)
    if i % di == 0:
        plt.plot(img_array_norm, label=f"time = {np.round(time, 2)} [s]", color=colormap(normalize(time)), alpha=0.3)

scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(times)
cbar = plt.colorbar(scalarmappaple)
cbar.set_label('time [s]', rotation=270, labelpad=20)
plt.xlabel("X position [px]")
plt.ylabel("normalized intensity [-]")
# plt.title(f"Line size = {line_size} [nm], pixel size = {pixel_size} [nm]")
plt.legend()
plt.grid()
# plt.savefig(namer(f"{directory}\profiles_colorbar_{name_common_part}", "png"))
plt.show()
plt.close()

plt.figure()
plt.plot(times, optimal_shifts)
plt.show()

length = len(optimal_shifts)
fft_half_length = len(optimal_shifts) // 2
fft = np.abs(np.fft.fft(optimal_shifts)[:fft_half_length]) / length * 2  # Normalizace amplitud
freqs = np.linspace(0, fs // 2, fft_half_length)
df = freqs[1] - freqs[0]
begining = 10
plt.figure("FFT", figsize=(20, 10))
plt.plot(freqs[begining:len(freqs) // 5],
         fft[begining:len(freqs) // 5])  # omezeni na rozsah s relevantni amplitudou
# Adjust the indices to the original array
plt.grid()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [px]")
# plt.ylim(0, 10)
plt.title(f"df = {df}")
plt.show()
