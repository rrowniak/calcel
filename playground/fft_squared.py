# https://pyspice.fabrice-salvaire.fr/examples/data-analysis/fft.html

import numpy as np

from scipy import signal
from scipy.fftpack import fft

import matplotlib.pyplot as plt

N = 1000 # number of sample points
dt = 1. / 1000 # sample spacing

frequency = 5.

t = np.linspace(.0, N*dt, N)
y = signal.square(2*np.pi*frequency*t)

figure2 = plt.figure(2, (20, 10))

plt.subplot(211)
plt.plot(t, y)
y_sum = None
for n in range(1, 20, 2):
    yn = 4/(np.pi*n)*np.sin((2*np.pi*n*frequency*t))
    if y_sum is None:
        y_sum = yn
    else:
        y_sum += yn
    if n in (1, 3, 5):
        plt.plot(t, y_sum)
plt.plot(t, y_sum)
plt.xlim(0, 2/frequency)
plt.ylim(-1.5, 1.5)

yf = fft(y)
tf = np.linspace(.0, 1./(2.*dt), N/2)
spectrum = 2./N * np.abs(yf[0:N//2])

plt.subplot(212)
plt.plot(tf, spectrum)
n = np.arange(1, 20, 2)
plt.plot(n*frequency, 4/(np.pi*n), 'o', color='red')
plt.grid()
plt.title('Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')

plt.show()