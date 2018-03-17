# https://pyspice.fabrice-salvaire.fr/examples/diode/rectification.html
import os

import matplotlib.pyplot as plt


import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)


figure1 = plt.figure(1, (20, 10))

circuit = Circuit('115/230V Rectifier')
circuit.include(spice_library['1N4148'])
on_115 = True # switch to select 115 or 230V
if on_115:
    node_230 = circuit.gnd
    node_115 = 'node_115'
    amplitude = 115@u_V
else:
    node_230 = 'node_230'
    node_115 = circuit.gnd
    amplitude = 230@u_V
source = circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=amplitude, frequency=50) # Fixme: rms
circuit.X('D1', '1N4148', 'in', 'output_plus')
circuit.X('D3', '1N4148', node_230, 'output_plus')
circuit.X('D2', '1N4148', 'output_minus', node_230)
circuit.X('D4', '1N4148', 'output_minus', 'in')
circuit.C('1', 'output_plus', node_115, 1@u_mF)
circuit.C('2', node_115, 'output_minus', 1@u_mF)
circuit.R('load', 'output_plus', 'output_minus', 10@u_Ω)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
if on_115:
    simulator.initial_condition(node_115=0)
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)

figure2 = plt.figure(1, (20, 10))
axe = plt.subplot(111)
plt.title('115/230V Rectifier')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.grid()
plot(analysis['in'], axis=axe)
plot(analysis.output_plus - analysis.output_minus, axis=axe)
plt.legend(('input', 'output'), loc=(.05,.1))
# plt.ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

plt.tight_layout()

plt.show()