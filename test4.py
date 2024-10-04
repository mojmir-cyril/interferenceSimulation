import numpy as np
import matplotlib.pyplot as plt

# Zadané hodnoty
freq = 36
frekvence = np.arange(0,50,1)       # Frekvence v Hz
vychylky = [0,] * len(frekvence)
vychylky[freq] = 1
vychylky = np.array(vychylky) # Amplitudy


# Časový krok a délka signálu
casovy_krok = 1e-5  # 10 mikrosekund
pocet_vzorku = 1024 * 768  # Celkový počet vzorků
delka_signalu = pocet_vzorku * casovy_krok  # Celková délka signálu v sekundách

# Vzorkovací frekvence
f_s = 1 / casovy_krok  # Vzorkovací frekvence v Hz

# Vytvoření komplexního spektra
N = pocet_vzorku  # Počet frekvenčních bodů, měl by být alespoň maximálně stejný jako počet frekvencí
spectrum = np.zeros(N, dtype=complex)

# Vytvoření frekvenční osy
frequencies = np.linspace(0, f_s/2, N//2)  # Frekvence od 0 do Nyquistovy frekvence

# Interpolace amplitud na nové frekvenční body
interpolated_amplitudes = np.interp(frequencies, frekvence, vychylky, left=0, right=0)

# Přiřazení interpolovaných amplitud k frekvencím
spectrum[:N//2] = interpolated_amplitudes + 1j * np.zeros(N//2)  # Pouze reálná část

# Pokud je potřeba, můžeme spektrum symetricky doplnit pro IFFT
spectrum[N//2:] = np.conjugate(spectrum[:N//2][::-1])  # Symetrie pro reálný časový signál


# Provedení IFFT
window = np.hamming(pocet_vzorku)
time_signal = np.fft.ifft(window * spectrum) * N
time_signal_nowindow = np.fft.ifft(spectrum) * N

# Vytvoření časového vektoru

time_vector = np.arange(0, delka_signalu, casovy_krok)
print(f"delka signalu = {delka_signalu}")

# Vykreslení výsledného časového signálu
plt.figure(figsize=(10, 6))
plt.plot(time_vector, np.real(time_signal), label="Časový signál")
plt.plot(time_vector, np.real(time_signal_nowindow), label="Časový signál okenkovany")
plt.title("Časový signál po IFFT")
plt.xlabel("Čas (s)")
plt.ylabel("Amplituda")
# plt.xlim(0, 0.1)  # Zobrazit pouze první 0.1 sekundy
plt.grid()
plt.legend()
plt.show()


fft = np.abs(np.fft.fft(time_signal))[:len(time_signal) // 2] / N
freqs = np.linspace(0, f_s / 2, N // 2)

plt.figure(figsize=(10, 6))
plt.plot(freqs, fft, label="spektrum")
plt.title("opetovne FFT signálu po IFFT")
plt.xlabel("Freq (Hz)")
plt.ylabel("Amplituda")
# plt.xlim(0, 0.1)  # Zobrazit pouze první 0.1 sekundy
plt.grid()
plt.legend()
plt.show()


from scipy.signal import butter, lfilter

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='highpass', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Parametry filtru
cutoff_frequency = 5  # Například 50 Hz
order = 5

# Použití filtru na časový signál
filtered_signal = lowpass_filter(np.real(time_signal), cutoff_frequency, f_s, order)

# Vykreslení filtrového signálu
plt.figure(figsize=(10, 6))
plt.plot(time_vector, filtered_signal, label="Filtrováný časový signál")
plt.title("Filtrováný časový signál po IFFT")
plt.xlabel("Čas (s)")
plt.ylabel("Amplituda")
plt.grid()
plt.legend()
plt.show()