import matplotlib.pyplot as plt
import numpy as np

percieved_freq = 100
sampling_freq = 500
n = np.arange(1,10,1)
var1 = n * sampling_freq - percieved_freq
var2 = n * sampling_freq + percieved_freq
real_freqs = np.sort(np.concatenate((var1, var2)))
print(real_freqs)

# real_freq = 600
# period = 1/sampling_freq
# times = np.arange(0,1,period)
# omega = 2 * np.pi * real_freq
# ys = np.sin(omega * times)
#
# freqs = np.fft.fftfreq(len(times), period)
# mask = freqs >= 0
# freqs_nyq = freqs[mask]
# ys_fft = abs(np.fft.fft(ys)[mask])
#
# fig, ax = plt.subplots()
# ax.plot(freqs_nyq , ys_fft, label="FFT")
# ax.grid()
# ax.legend()
# plt.show()


