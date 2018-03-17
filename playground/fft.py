# https://pyspice.fabrice-salvaire.fr/examples/data-analysis/fft.html

import numpy as np

from scipy import signal
from scipy.fftpack import fft

import matplotlib.pyplot as plt

N = 1000 # number of sample points
dt = 1. / 500 # sample spacing

frequency1 = 50.
frequency2 = 80.

t = np.linspace(0.0, N*dt, N)
y = np.sin(2*np.pi * frequency1 * t) + .5 * np.sin(2*np.pi * frequency2 * t)

yf = fft(y)
tf = np.linspace(.0, 1./(2.*dt), N/2)
spectrum = 2./N * np.abs(yf[0:N//2])

figure1 = plt.figure(1, (20, 10))
plt.plot(tf, spectrum, 'o-')
plt.grid()
for frequency in frequency1, frequency2:
    plt.axvline(x=frequency, color='red')
plt.title('Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')

plt.show()
