import matplotlib.pyplot as plt


def get_conversion_coef_m_to_px(magnification=1e6):
    return 100/27.66 * 1e8 * (magnification / 1e6)
    # return 100/27.66 * 1e9 * (magnification / 1e6)

def load_spectrum_from_file(path, channel, magnification=1e6, unit='m', params_path=r"C:\Users\mojmir.michalek\PycharmProjects\interferenceSimulation\_parameters.json", show=True):
    import sys
    module_path_1 = r"C:\Users\mojmir.michalek\PycharmProjects\measurementDataPostProcessing\scripts"  # Nahraď skutečnou cestou
    module_path_2 = r"C:\Users\mojmir.michalek\PycharmProjects\measurementDataPostProcessing\scripts"  # Nahraď skutečnou cestou
    module_paths = [module_path_1, module_path_2]
    for module_path in module_paths:
        if module_path not in sys.path:
            sys.path.append(module_path)
    from DataClass import DataObject
    import module_dewetron_processing

    parameters_file = module_dewetron_processing.load_parameters(params_path)
    params = module_dewetron_processing.fill_plot_parameters_2(parameters_file, testtype="spectra", sensor="X")

    data_obj = DataObject(path, params)
    if unit == 'm':
        y_name = f'AI {channel}/Double integral/AmplFFT'
    elif unit == 'm/s':
        y_name = f'AI {channel}/Integral/AmplFFT'
    elif unit == 'm/s2':
        y_name = f'AI {channel}/AmplFFT'
    # y_names = ['AI 5/AmplFFT', 'AI 6/AmplFFT']
    chosen_dataset = [dataset for dataset in data_obj.dataSets if dataset.yName == y_name][0]
    spectrum = [chosen_dataset.x, chosen_dataset.y * get_conversion_coef_m_to_px(magnification=magnification)]

    if show:
        fig, ax1 = plt.subplots()
        ax1.plot(*spectrum, label="spectrum")
        ax1.legend()
        ax1.grid()
        plt.show()

    return spectrum

def denoise_spectrum(spectrum, show=True, min_freq=15, scale=1):
    from lmfit.models import ExponentialModel, Model
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.spatial import ConvexHull
    def hyperbola(x, x_offset, y_offset, scale):
        return scale / ((x - x_offset) ** 2) + y_offset

    index = np.argmax(spectrum[0] > min_freq)
    spectrum = [spectrum[0][index:], spectrum[1][index:]]

    # # model = ExponentialModel()
    # model = Model(hyperbola)
    # params = model.make_params(x_offset=0, y_offset=0, scale=1)
    #
    # # params['x_offset'].min =
    # # params['y_offset'].min = 0

    # Body spektra (frekvence, amplituda)
    points = np.column_stack((spectrum[0], spectrum[1]))
    i = 3
    # Výpočet konvexní obálky
    hull = ConvexHull(points)
    hull_freqs, hull_amps =  points[hull.vertices[i:], 0], points[hull.vertices[i:], 1]
    hull_amps_mod = hull_amps - min(hull_amps)
    hull_amps_interp = np.interp(spectrum[0], hull_freqs, hull_amps_mod)
    # result = model.fit(hull_amps, params, x=hull_freqs)
    subctracted_spectrum = spectrum[1]-hull_amps_interp
    scaled_spectrum = scale * subctracted_spectrum
    if show:
        fig, ax = plt.subplots()
        ax.plot(spectrum[0], spectrum[1], label='raw data')
        # ax.plot(hull_freqs, result.best_fit, label='best fit')
        ax.plot(hull_freqs, hull_amps, 'r', alpha=0.3, label="Konvexní obálka")
        ax.plot(hull_freqs, hull_amps_mod, 'b', alpha=0.7, label="Konvexní obálka mod")
        ax.plot(spectrum[0], subctracted_spectrum, label='subctracted_spectrum')
        ax.plot(spectrum[0], scaled_spectrum, label='scaled_spectrum')
        ax.legend()
        ax.grid()
        plt.show()
    return [spectrum[0], scaled_spectrum]



