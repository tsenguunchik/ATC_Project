import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import subprocess


output_filename = 'Moment_Height_NOT_Regularized.pdf'

phi_Mn = np.zeros(8)
phi_Mn[0] = 87147.0
phi_Mn[1] = 87147.0
phi_Mn[2] = 60315.0
phi_Mn[3] = 60315.0
phi_Mn[4] = 60315.0
phi_Mn[5] = 23545.0
phi_Mn[6] = 23545.0
phi_Mn[7] = 23545.0
# Conversion
phi_Mn = phi_Mn * 12000.0

pp = PdfPages(output_filename)
fig = plt.figure()
figure = fig.add_subplot(111)
time_step = 10.0
height = np.zeros(9)
height[0] = 0
height[1] = 15
height[2] = 28
height[3] = 41
height[4] = 54
height[5] = 67
height[6] = 80
height[7] = 93
height[8] = 106
moment_index = range(3, 46, 6)

OpenSees_files = [
    'Output/WallForces_regular.txt',
    'Output/nodeDisp_regular.txt',
    ]
OpenSees_x = np.loadtxt(OpenSees_files[0])
OpenSees_disp = np.loadtxt(OpenSees_files[1])

# plt.plot(OpenSees_x[:, 0], -OpenSees_x[:, 3] / phi_Mn[0], lw=1, label='Section')

max_moment_index = np.argmax(abs(OpenSees_x[:, 3]))

max_drift_index = np.argmax(abs(OpenSees_disp[:, 22]))

value = np.append(OpenSees_x[max_drift_index, moment_index], 0.0)

plt.plot(value / 12000.0, height, lw=1, label='At maximum drift')

value = np.append(OpenSees_x[max_moment_index, moment_index], 0.0)

plt.plot(value / 12000.0, height, lw=1, label='At maximum base Moment')

# Story loop

# plt.xlim(0, 9)
# plt.ylim(-800, 800)
plt.legend(loc=0, shadow=True, numpoints=1)
plt.xlabel(r"Moment [kip-ft]")
plt.ylabel(r"Building Height [ft]")
plt.minorticks_on()
plt.grid(b=True, which='major', alpha=1)
# plt.grid(b=True, which='minor', alpha=0.2)
plt.tight_layout()
pp.savefig(fig)
plt.close()
pp.close()
subprocess.Popen([output_filename], shell=True)