import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

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

# Compute Initial Fourier Transform
dft_result = np.fft.fft(sampled_signal)
frequencies = np.fft.fftfreq(len(sampled_signal), d=1/sampling_frequency)  

fig, ax = plt.subplots(2, 1, figsize=(10, 6))
plt.subplots_adjust(left=0.25, bottom=0.35)  # Adjust layout for sliders

ax[0].plot(true_time_range, true_signal, label="Original Function", alpha=0.7)
sampled_plot, = ax[0].plot(sampled_time_range, sampled_signal, 'ro', label="Sampled Points", markersize=3)
ax[0].legend()
ax[0].set_title("Time-Domain Signal")

# Initial Frequency Spectrum
dft_magnitude = np.abs(dft_result)

stem_plot, = ax[1].plot(frequencies, dft_magnitude, 'bo', markersize=3)  
stem_lines = ax[1].vlines(frequencies, 0, dft_magnitude, colors='blue')  
ax[1].set_title("Frequency Spectrum (DFT)")
ax[1].set_xlabel("Frequency (Hz)")

# Slider Positions (Two Columns)
slider_positions = [
    (0.1, 0.25, "A1", 0, 10, A1),
    (0.1, 0.20, "A2", 0, 10, A2),
    (0.1, 0.15, "A3", 0, 10, A3),
    (0.1, 0.10, "f1", 0, 100, f1),
    (0.1, 0.05, "f2", 0, 100, f2),
    (0.5, 0.25, "f3", 0, 100, f3),
    (0.5, 0.20, "f4", 0, 100, f4),
    (0.5, 0.15, "f5", 0, 100, f5),
    (0.5, 0.10, "f6", 0, 100, f6),
    (0.5, 0.05, "SF", 10, 1000, sampling_frequency),
]

# Create Sliders
sliders = {}
for x_pos, y_pos, label, min_val, max_val, init_val in slider_positions:
    ax_slider = plt.axes([x_pos, y_pos, 0.35, 0.03])
    sliders[label] = Slider(ax_slider, label, min_val, max_val, valinit=init_val)

def update(val):
    A1, A2, A3 = sliders["A1"].val, sliders["A2"].val, sliders["A3"].val
    f1, f2, f3, f4, f5, f6 = sliders["f1"].val, sliders["f2"].val, sliders["f3"].val, sliders["f4"].val, sliders["f5"].val, sliders["f6"].val
    sample_frequency = sliders["SF"].val

    sampled_time_range = np.arange(0, duration, 1 / sample_frequency)
    
    updated_sampled_signal = target_function_0(sampled_time_range, A1, A2, A3, f1, f2, f3, f4, f5, f6)
    sampled_plot.set_xdata(sampled_time_range)
    sampled_plot.set_ydata(updated_sampled_signal)

    updated_dft = np.fft.fft(updated_sampled_signal)
    updated_frequencies = np.fft.fftfreq(len(updated_sampled_signal), d=1/sample_frequency)  
    updated_magnitude = np.abs(updated_dft[:len(updated_dft)])  

    # Update frequency spectrum plot
    stem_plot.set_data(updated_frequencies, updated_magnitude)  # Update points

    # FIX: Remove old lines and update with new ones
    global stem_lines
    segments = [[[x, 0], [x, y]] for x, y in zip(updated_frequencies, updated_magnitude)]
    stem_lines.set_segments(segments)  # Efficiently update the vlines
    
    fig.canvas.draw_idle()  # Redraw the figure

# Link Sliders to Update Function
for slider in sliders.values():
    slider.on_changed(update)

plt.show()
