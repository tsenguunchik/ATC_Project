import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import subprocess


output_filename = 'Stress_Strain_1.pdf'


OpenSees_files = [
    'Output/story1_SS_EC_Comp1.txt',
    'Output/story1_SS_CC_Comp1.txt',
    'Output/story1_SS_ES_Comp1.txt',
    'Output/story1_SS_EC_Ten1.txt',
    'Output/story1_SS_CC_Ten1.txt',
    'Output/story1_SS_ES_Ten1.txt',
        ]

pp = PdfPages(output_filename)

fig = plt.figure()
count = 1
for file_name in OpenSees_files:
    figure = fig.add_subplot(3, 2, count)
    count = count + 1
    OpenSees = np.loadtxt(file_name)
    plt.minorticks_on()
    plt.grid(b=True, which='major', alpha=1)
    plt.tight_layout()
    plt.plot(OpenSees[:, 2], OpenSees[:, 1], lw=1, label='Fiber 1')



# plt.xlim(-5, 5)
# plt.ylim(-800, 800)
# plt.legend(loc=0, shadow=True, numpoints=1)
# plt.xlabel("Normalized axial displacement ($\Delta/h_w$), %")
# plt.ylabel(r"Normalized Axial Core Stress, $P_c / (A_\mathrm{core} \, f'_c)$")

# plt.grid(b=True, which='minor', alpha=0.2)


pp.savefig(fig)

pp.close()
subprocess.Popen([output_filename], shell=True)
