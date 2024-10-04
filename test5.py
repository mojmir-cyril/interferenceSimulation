# Znovu načteme potřebné knihovny a spustíme skript
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy.interpolate import interp1d


# Definice funkce spectrum_to_time_signal_fixed
def spectrum_to_time_signal_fixed(frekvence, amplitudy, dt, duration, imaginary_part=False):
    # Výpočet parametrů signálu
    f_s = 1 / dt  # Vzorkovací frekvence
    N = int(duration / dt)  # Počet vzorků signálu

    # Frekvenční osa
    freqs_fft = np.fft.fftfreq(N, d=dt)
    freqs_pos = freqs_fft[:N // 2 + 1]

    # Interpolace spektra na frekvenční osy
    interpolator = interp1d(frekvence, amplitudy, bounds_error=False, fill_value=0)
    interpolated_amplitudes = interpolator(freqs_pos)

    # Vytvoření komplexního spektra (symetrického) pro IFFT
    spectrum = np.zeros(N, dtype=complex)
    spectrum[:N // 2 + 1] = interpolated_amplitudes + (
        1j * np.random.random(N // 2 + 1) if imaginary_part else 1j * np.zeros(N // 2 + 1))

    spectrum[N // 2 + 1:] = np.conjugate(
        spectrum[1:N // 2][::-1])  # Zrcadlení pro získání reálného signálu v časové doméně

    # Inverse FFT a vytvoření časového signálu
    time_signal = np.fft.ifft(spectrum).real * N

    # Časový vektor
    time_vector = np.arange(0, duration, dt)

    return time_signal, time_vector


# Spektrum s reálnými složkami
frekvence_real = np.array([50, 150, 300, 450, 600, 800, 950])
amplitudy_real = np.array([1.0, 0.5, 1.2, 0.7, 0.9, 1.1, 0.8])

# Parametry časového signálu
dt = 1e-5
duration = 1024 * 768 * dt

# Vytvoření časových signálů pro obě varianty (s a bez imaginární složky)
time_signal_real, time_vector_real = spectrum_to_time_signal_fixed(frekvence_real, amplitudy_real, dt, duration,
                                                                   imaginary_part=False)
time_signal_imaginary, time_vector_imaginary = spectrum_to_time_signal_fixed(frekvence_real, amplitudy_real, dt,
                                                                             duration, imaginary_part=True)

# Vykreslení obou signálů
plt.figure(figsize=(10, 6))

# Časový signál s reálnými složkami
plt.subplot(2, 1, 1)
plt.plot(time_vector_real, time_signal_real, label="Reálné složky", color='blue')
plt.title("Časový signál s reálnými složkami")
plt.xlabel("Čas (s)")
plt.ylabel("Amplituda")
plt.grid()

# Časový signál s náhodnými imaginárními složkami
plt.subplot(2, 1, 2)
plt.plot(time_vector_imaginary, time_signal_imaginary, label="Náhodné imaginární složky", color='orange')
plt.title("Časový signál s náhodnými imaginárními složkami")
plt.xlabel("Čas (s)")
plt.ylabel("Amplituda")
plt.grid()

plt.tight_layout()
plt.show()
