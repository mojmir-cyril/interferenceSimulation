from interference_simulation_single_frame import get_interfered_image

input_image_path = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace\AMBER\MD (SE), 15kV\122-0130 S8251G, CN.png"
out_folder = r"C:\Users\mojmir.michalek\OneDrive - TESCAN ORSAY HOLDING, a.s\Documents\Measurements\ruseni_kategorizace"
freq = 79
amplitude_X = 1
amplitude_Y = 0.6
blur = 0
noise = 0
scan_speed_num = 5
use_synch_50 = True
save_image = True
get_interfered_image(input_image_path, freq, amplitude_X, amplitude_Y, blur, noise, scan_speed_num, use_synch_50,
                     save_image=save_image, out_folder=out_folder)
