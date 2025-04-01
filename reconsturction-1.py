import numpy as np 
import matplotlib.pyplot as plt 

N = 1000
sampling_freq = 12.0 # all frequncies are angular frequncies
start_time = 0.0
end_time = 100.0 

time_window = end_time - start_time 
time = np.linspace(start_time, end_time, int(1e5))

def input_signal(t):
    return 5 * np.sin(10 * t) * np.sin(15 * t) + 0.5 * np.sin(15 * t) * np.sin(20 * t) + 10 * np.sin(5 * t) * np.sin(10 * t) + 6 * np.sin(25 * t) * np.sin(10 * t)
reconstructed_signal = np.zeros_like(time)

def compute_coeff(k):
    def f(t):
        return input_signal(k / sampling_freq - t) * sampling_freq * np.sinc(sampling_freq * (t))
    N_lim = 1e3
    a = -N_lim
    b = N_lim
    h = (b - a) / N_lim  
    s = 0.5 * (f(a) + f(b))  

    x0 = a + h
    for i in range(1, int(N_lim)):
        s += f(x0)
        x0 += h

    return h * s
    
for k in range(-N, N+1):
    #reconstructed_signal += (sampling_freq / 2) * input_signal(k / sampling_freq) * np.sinc(k / 2) * np.sinc(sampling_freq * (time - k / sampling_freq))
    #reconstructed_signal += input_signal(k / sampling_freq) * np.sinc(sampling_freq * (time - k / sampling_freq))
    
    #reconstructed_signal += compute_coeff(k) * np.sinc(sampling_freq * (time - k / sampling_freq)) / (2 * sampling_freq) # works good, scaling factor ambiguous, not that useful since we need to know the input function for convolution (compute_coeff) computation 
    reconstructed_signal+= input_signal(k / sampling_freq) * np.sinc(sampling_freq * (time - k / sampling_freq))

fig, ax = plt.subplots(2, 1, figsize=(10, 8))
input_signal_values = input_signal(time)
ax[0].plot(time, input_signal_values, label="input signal")
ax[0].plot(time, reconstructed_signal, label="reconstruction attempt")
ax[0].legend(loc='best')
ax[1].plot(time, np.abs(input_signal_values - reconstructed_signal), label="absolute local error")
ax[1].legend()
plt.tight_layout()
plt.title("Sampling Freuency ")
plt.show()
