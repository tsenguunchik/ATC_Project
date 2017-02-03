import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import subprocess


output_filename = 'Atena_Opensees.pdf'
Atena_files = [
    'Atena_Result/drift_UnPunched_8story_Dmax_ELF_barBucklingModel.txt',
    'Atena_Result/drift_UnPunched_8story_Dmax_MRSA_barBucklingModel.txt',
    'Atena_Result/load_UnPunched_8story_Dmax_ELF_barBucklingModel.txt',
    'Atena_Result/load_UnPunched_8story_Dmax_MRSA_barBucklingModel.txt',
]

OpenSees_files = [
    'Output/nodeDisp_regular.txt',
    'Output/node1R_regular.txt',
        ]

pp = PdfPages(output_filename)

fig = plt.figure()
figure = fig.add_subplot(111)

Atena_ELF_x = np.loadtxt(Atena_files[0])
Atena_ELF_y = np.loadtxt(Atena_files[2])

Atena_MERSA_x = np.loadtxt(Atena_files[1])
Atena_MERSA_y = np.loadtxt(Atena_files[3])



# Atena
plt.plot(Atena_ELF_x, Atena_ELF_y * 2, lw=2, label='Atena ELF')


# OpenSeeS
eff_height = 72 #ft
OpenSees_x = np.loadtxt(OpenSees_files[0])
OpenSees_y = np.loadtxt(OpenSees_files[1])
plt.plot(((OpenSees_x[:, 16] - OpenSees_x[:, 13]) / 13.0 * 5.0 / 12.0 + OpenSees_x[:, 13]) / eff_height / 12 * 100, -OpenSees_y[:, 1] / 1000.0, lw=1, label='Opensees ELF - 0.2 fracture')

plt.xlim(0, 5)
# plt.ylim(-800, 800)
plt.legend(loc=0, shadow=True, numpoints=1)
plt.xlabel("Effective Height Drift [%]")
plt.ylabel("Base Shear [kips]")
plt.minorticks_on()
plt.grid(b=True, which='major', alpha=1)
# plt.grid(b=True, which='minor', alpha=0.2)
plt.tight_layout()
pp.savefig(fig)

plt.legend(loc=0, shadow=True, numpoints=1)
plt.xlabel("Effective Height Drift [%]")
plt.ylabel("Base Shear [kips]")
plt.minorticks_on()
plt.grid(b=True, which='major', alpha=1)
# plt.grid(b=True, which='minor', alpha=0.2)
plt.tight_layout()
pp.savefig(fig)
pp.close()
subprocess.Popen([output_filename], shell=True)
