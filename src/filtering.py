import numpy as np
from scipy.signal import savgol_filter

def savgol_filtering(signal, window_length=101, polyorder=5, mode='interp'):
    """
    runs savgol filtering on signal (savgol is a polynomial filter which tries to map a
    polynomial of degree polyorder to your data)
    :param signal: The signal to be filtered
    :param window_length: the width of window when solving a best fit polynomial
    :param polyorder: the degree of polynomial used to solve.
    :param mode: How to connect the multiple polynomials
    :return: filtered signal
    """
    return savgol_filter(signal, window_length, polyorder, mode=mode)


def window_smoothing(signal, window_width=31):
    """
    moves across signal and takes average centered around each point,
    pads input signal with value at ends uses np.conv

    :param signal: signal to be smoothed
    :param window_width: window to use when calculating average
    :return: smoothed signal
    """
    window = np.ones(window_width) * 1./window_width
    padded = np.hstack((np.ones(window_width//2)*signal[0], signal, np.ones(window_width//2)*signal[-1]))
    return np.convolve(padded, window, 'valid')

def peak_detect(signals, threshold=0.0, min_length=20):
    """
    returns np.array which is signals like but with 1s where the signal is active and 0 else
    :param signals: the signals to find a peak in
    :param threshold: The threshold for what values are considered active
    :param min_length: The minimum length of a peak. This helps remove noise with small jump peaks
    :return: list(pairs) [(start_1,stop_1),(start_2,stop_2)...] where inbetween the start and stops the value is 1
    """
    bin_signals = (signals > threshold).astype(int)
    peak_segments = []
    for bin_signal in bin_signals:
        bounded = np.hstack(([0], bin_signal, [0]))
        diff = np.diff(bounded)
        run_starts, = np.where(diff > 0)
        run_ends, = np.where(diff < 0)
        lengths = run_ends-run_starts
        where,  = np.where(lengths >= min_length)
        good_starts = run_starts[where]
        good_ends = run_ends[where]-1
        peak_segments.append(zip(good_starts, good_ends))
    return peak_segments

def burst_detect(signal, w1=51, w2=101, threshold=0.0, min_length=20):
    signal = signal - signal.min()
    signal/=signal.max()
    s1_sample = savgol_filtering(signal, w1)
    s2_sample = window_smoothing(signal, w2)
    feature = (s1_sample - s2_sample)/s2_sample
    peak_segments = peak_detect(feature[np.newaxis, :], threshold=threshold, min_length=min_length)[0]


    return feature, peak_segments