import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

A1, A2, A3 = 5, 6, 8
f1, f2, f3, f4, f5, f6 = 5, 25, 10, 30, 15, 20
sampling_frequency = 100
duration = 5  

true_time_range = np.linspace(0, duration, 100000)  
sampled_time_range = np.arange(0, duration, 1 / sampling_frequency)  

def target_function_0(x, A1, A2, A3, f1, f2, f3, f4, f5, f6):
    return (A1 * np.sin(2 * np.pi * f1 * x) * np.sin(2 * np.pi * f2 * x)) + \
           (A2 * np.sin(2 * np.pi * f3 * x) * np.sin(2 * np.pi * f4 * x)) + \
           (A3 * np.sin(2 * np.pi * f5 * x) * np.sin(2 * np.pi * f6 * x))

# Compute Initial Signals
true_signal = target_function_0(true_time_range, A1, A2, A3, f1, f2, f3, f4, f5, f6)
sampled_signal = target_function_0(sampled_time_range, A1, A2, A3, f1, f2, f3, f4, f5, f6)

dft_result = np.fft.fft(sampled_signal)
frequencies = np.fft.fftfreq(len(sampled_signal), d=1/sampling_frequency)
dft_magnitude = np.abs(dft_result)

# Shorter impulse response for deconvolution
sampling_function = np.array([1e7 for x in range(200)])

# Convert DFT to real for deconvolution
dft_result_real = np.real(dft_result)

# Perform deconvolution
quotient, remainder = signal.deconvolve(dft_result, sampling_function)

# Create a new time axis matching quotient length
deconv_time_range = np.linspace(0, duration, len(quotient))

fig, ax = plt.subplots(3, 1, figsize=(10, 6))

ax[0].plot(true_time_range, true_signal, label="Original Function", alpha=0.7)
ax[0].plot(sampled_time_range, sampled_signal, 'ro', label="Sampled Points", markersize=3)
ax[0].legend()
ax[0].set_title("Time-Domain Signal")

ax[1].plot(frequencies, dft_magnitude, 'bo', markersize=3)  
ax[1].vlines(frequencies, 0, dft_magnitude, colors='blue')  
ax[1].set_title("Frequency Spectrum (DFT)")
ax[1].set_xlabel("Frequency (Hz)")

ax[2].plot(deconv_time_range, quotient, 'bo', markersize=3)  
ax[2].vlines(deconv_time_range, 0, quotient, colors='blue')  
ax[2].set_title("Deconvolved Signal")

plt.tight_layout()
plt.show()

