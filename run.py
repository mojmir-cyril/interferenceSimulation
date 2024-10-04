from interfere_image_class import InterferedImage

# input_image_path = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace\AMBER\MD (SE), 15kV\122-0130 S8251G, CN.png"
input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
out_folder = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace"
freq = 79
amplitude_X = 0.5
amplitude_Y = 0
blur = 0
noise = 0
scan_speed_num = 5
synch_freq = 0

InterferedImage(input_image_path=input_image_path,
                frequency=freq,
                amplitude_X=amplitude_X,
                amplitude_Y=amplitude_Y,
                blur=blur,
                noise=noise,
                scan_speed_num=scan_speed_num,
                synch_freq=synch_freq,
                out_folder=out_folder,
                method="single_frequency",
                use_subpixel_precision=True,
                show=True)

# Multiple Freqs
# from interfere_image_class import InterferedImage
#
# input_image_path = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace\AMBER\MD (SE), 15kV\122-0130 S8251G, CN.png"
# out_folder = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace"
# freqs = [30, 50, 79, 180]
# amplitudes_X = [2, 2, 1, 1.5]
# amplitudes_Y = [1, 1, 1, 0]
# blur = 0
# noise = 0
# scan_speed_num = 5
# synch_freq = 0
#
# InterferedImage(input_image_path=input_image_path,
#                 frequencies=freqs,
#                 amplitudes_X=amplitudes_X,
#                 amplitudes_Y=amplitudes_Y,
#                 blur=blur,
#                 noise=noise,
#                 scan_speed_num=scan_speed_num,
#                 synch_freq=synch_freq,
#                 out_folder=out_folder,
#                 method="multiple_frequency")


# Input from spectra
# from interfere_image_class import InterferedImage
#
# input_image_path = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace\AMBER\MD (SE), 15kV\122-0130 S8251G, CN.png"
# input_image_path = r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\random_circles_image_matplotlib_reference.png"
# out_folder = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace"
# # freqs = [10, 20, 30, 40, 50]
# # spectrum_X = np.array([0, 0, 1, 0, 0])
# # spectrum_Y = np.array([0, 0, 0, 0, 0])
# blur = 4
# noise = 30
# scan_speed_num = 9
# synch_freq = 0
# scale = 2
# min_freq = 45
# show = False
#

# Umele generovane spectrum
# # Zadané hodnoty
# freq = 50
# frekvence = np.arange(0,100,0.1)       # Frekvence v Hz
# vychylky = [0,] * len(frekvence)
# vychylky[freq*10] = 5
# vychylky = np.array(vychylky) # Amplitudy
# spectrum_X = [frekvence, vychylky]
#

# Spectrum nactene z mereni akcelerometrem
# # path = r'C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\AMBER_116-0024\nedotazene vs dotazene krizove lozisko 3\00_AMBER_116-0024_chamber234_stage567_hodnePovoleneKrizLozisko_spectra_XYZ_0000.txt'
# # path = r'C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\MAGNA 117-0086\2023_06_16_agilentVsPfeifferTMP\spectra\04_MAGNA_117-0086_agilent_poVikendu_spectra_XYZ_0000.txt'
# path = r'C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\SOLARIS 116-0089\2023_10_12_galvanicIsolation\00_SOLARIS_116-0089_galvIsol_chamberTMP_stage_spectra_XYZ_0000.txt'
#
# spectrum_X = read_measurement_file.load_spectrum_from_file(path=path, channel=5, show=show, unit="m")
# spectrum_Y = read_measurement_file.load_spectrum_from_file(path=path, channel=6, show=show, unit="m")
# denoised_spectrum_X = read_measurement_file.denoise_spectrum(spectrum_X, show=show, min_freq=min_freq, scale=scale)
# denoised_spectrum_Y = read_measurement_file.denoise_spectrum(spectrum_Y, show=show, min_freq=min_freq, scale=scale)
#
# # time_signal = np.real(np.fft.ifft(denoised_spectrum_X[1]))
# # fig, ax = plt.subplots()
# # ax.plot(time_signal)
# # ax.grid()
# # ax.set_title("raw ifft")
# # plt.show()
#
# InterferedImage(input_image_path=input_image_path,
#                 spectrum_X=denoised_spectrum_X,
#                 spectrum_Y=denoised_spectrum_Y,
#                 blur=blur,
#                 noise=noise,
#                 scan_speed_num=scan_speed_num,
#                 synch_freq=synch_freq,
#                 out_folder=out_folder,
#                 method="spectra",
#                 use_amp_phase=True,
#                 use_random_phase=True)