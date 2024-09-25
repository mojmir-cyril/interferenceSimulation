import numpy as np

from interference_simulation_single_frame import get_interfered_image
# blurs = np.arange(0, 20, 2)
blurs = [5]
# noises = np.arange(0, 80, 5)
noises = [0]
input_image_path = r"S:\Finalizace\FinalizaceS8000\124-0048, JAR\images\RT_port11\RT_nastrel\TMP_cat-4_Heavy_dumper\02_09_2024\RT_AD_01_1000_Heavy_dump-1.png"

for noise in noises:
    for blur in blurs:
        # amps = np.linspace(0,3,10).round(2)
        amps = [0]
        freq = 50
        # blur = 10
        # noise = 10
        width = 1024
        scan_speed_num = 4
        use_synch_50 = False
        save_image = True

        for amp in amps:
            amplitude_X = amp
            amplitude_Y = amp
            get_interfered_image(input_image_path, freq, amplitude_X, amplitude_Y, blur, noise, scan_speed_num, use_synch_50, save_image=save_image)
