import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import subprocess

ip = np.zeros(5)
ip[0] = 1.0 / 20.0
ip[1] = 49.0 / 180.0
ip[2] = 1.0 / 20.0
ip[3] = 49.0 / 180.0
ip[4] = 1.0 / 20.0
output_filename = 'Moment_Rotation.pdf'
phi_Mn = np.zeros(8)
phi_Mn[0] = 87147.0
phi_Mn[1] = 87147.0
phi_Mn[2] = 60315.0
phi_Mn[3] = 60315.0
phi_Mn[4] = 60315.0
phi_Mn[5] = 23545.0
phi_Mn[6] = 23545.0
phi_Mn[7] = 23545.0
#Conversion
phi_Mn = phi_Mn * 12000.0

pp = PdfPages(output_filename)
fig = plt.figure()
figure = fig.add_subplot(111)
story = 6
# Story loop
for i in range(story, story + 1):
    for j in range(1, 6):
        OpenSees_files = [
            'Output/SectionCurvature' + str(i) + '_regular' + str(j) + '.txt',
            'Output/SectionMoment' + str(i) + '_regular' + str(j) + '.txt',
                ]
        # OpenSeeS
        OpenSees_x = np.loadtxt(OpenSees_files[0])
        OpenSees_y = np.loadtxt(OpenSees_files[1])
        if i == 1:
            plt.plot(-OpenSees_x[:, 2] * ip[j - 1] * 15 * 12, -OpenSees_y[:, 2] / phi_Mn[i - 1], lw=1, label='Section - ' + str(j))
        else:
            plt.plot(-OpenSees_x[:, 2] * ip[j - 1] * 13 * 12, -OpenSees_y[:, 2] / phi_Mn[i - 1], lw=1,
                     label='Section - ' + str(j))





# plt.xlim(0, 9)
# plt.ylim(-800, 800)
plt.legend(loc=0, shadow=True, numpoints=1)
plt.xlabel("Rotation")
plt.ylabel(r"Nomalized Moment $M/M_n$")
plt.minorticks_on()
plt.grid(b=True, which='major', alpha=1)
# plt.grid(b=True, which='minor', alpha=0.2)
plt.tight_layout()
pp.savefig(fig)


pp.close()
subprocess.Popen([output_filename], shell=True)
