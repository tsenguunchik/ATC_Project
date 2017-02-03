import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import subprocess
import PyPDF2


output_filename = 'CS5.pdf'
files = [
    'experimental/CS5',
    # 'Output/Node2',
    'Output/StressStrain_Confined_3',
    'Output/StressStrain_Confined_3',
    'experimental/CS5_Envelope',
    'Output/StressStrainSteel',
        ]
titles = [
    'OBE',
    'OpenSees',
]

cover = 5./8.+3./8.+0.5*5./8.0
A_total = 15.0 * 8.0
# A_conf = (15.0 - 2.0*cover)*(8.0 - 2.0*cover)
A_conf = 79.18
A_unConf = 15.0*8.0 - (15.0 - 2.0*cover)*(8.0 - 2.0*cover)
print A_conf, A_unConf
pp = PdfPages(output_filename)
print '****************'
for i in range(0, len(files), 5):
    print i
    fig = plt.figure()
    figure = fig.add_subplot(111)

    d0 = np.loadtxt(files[i] + '.txt')
    d1 = np.loadtxt(files[i+1] + '.txt')
    d2 = np.loadtxt(files[i+2] + '.txt')
    d3 = np.loadtxt(files[i+3] + '.txt')
    d4 = np.loadtxt(files[i+4] + '.txt')

    # plt.plot(d0[:, 0], d0[:, 1], lw=1, label='monotonic (' + files[i] + ')')
    # plt.plot(-d1[:, 1]*100.0, (d1[:, 0]-abs((d2[:, 1])*3.1))/1000., lw=2, label='OpenSees')
    plt.plot(-d1[:, 2] * 100.0, -(d1[:, 1] * A_conf) / 1000., lw=2, label='OpenSees') # total area of concrete
    # plt.plot(-d1[:, 2] * 100.0, -(d1[:, 1] * (A_conf-3.1)) / 1000., lw=2, label='OpenSees') #A_eff
    # plt.plot(d3[:, 0], d3[:, 1], lw=1, label='measured')
    plt.plot(d3[:, 0], d3[:, 2], lw=1, label='measured')

    # plt.text(2, 255, 'max = ' + str(-min((d1[:, 1] * (A_conf-3.1) + d2[:, 1] * A_unConf) / 1000.)))
    # plt.text(2, 200, 'max = ' + str(max(d3[:, 2])))

    plt.axhline(c='grey'), plt.axvline(c='grey')
    # plt.title('Specimen ' + files[i] + ' Concrete only ($A_\mathrm{eff}$)')
    # plt.title('Specimen ' + files[i] + ' Concrete only')
    plt.title('Specimen ' + files[i] + ' Total')
    # plt.title('Specimen ' + files[i] + ' steel')
    # plt.xlim(-5, 5)
    # plt.xticks(xrange(-5, 6))
    # plt.ylim(-800, 800)
    plt.legend(loc=1, shadow=True, numpoints=1)
    plt.xlabel("Normalized axial displacement ($\Delta/h_w$), %")
    plt.ylabel("Axial force, kips")
    plt.minorticks_on()
    plt.grid(b=True, which='major', alpha=1, picker=4)
    # plt.grid(b=True, which='minor', alpha=0.2)
    plt.tight_layout()

    pp.savefig(fig)

fig = plt.figure()
figure = fig.add_subplot(111)
# plt.plot(d4[:, 2], d4[:, 1], lw=2, label='steel')
plt.plot(d3[:, 0], (d3[:, 1]-d3[:, 2])/(3.1), lw=1, label='measured')
plt.axhline(c='grey'), plt.axvline(c='grey')
# plt.ylim(-800, 800)
# plt.legend(loc=1, shadow=True, numpoints=1)
plt.xlabel("Avg. Strain, %")
plt.ylabel("Stress, ksi")
plt.minorticks_on()
plt.grid(b=True, which='major', alpha=1, picker=4)
# plt.grid(b=True, which='minor', alpha=0.2)
plt.tight_layout()
pp.savefig(fig)

fig = plt.figure()
figure = fig.add_subplot(111)
plt.plot(d4[:, 2], d4[:, 1]*3.1, lw=2, label='steel')
# plt.plot(d3[:, 0], (d3[:, 1]-d3[:, 2])/(3.1), lw=1, label='measured')
plt.axhline(c='grey'), plt.axvline(c='grey')
# plt.ylim(-800, 800)
# plt.legend(loc=1, shadow=True, numpoints=1)
# plt.xlabel("Avg. Strain, %")
# plt.ylabel("Stress, ksi")
plt.minorticks_on()
plt.grid(b=True, which='major', alpha=1, picker=4)
# plt.grid(b=True, which='minor', alpha=0.2)
plt.tight_layout()
pp.savefig(fig)

fig = plt.figure()
figure = fig.add_subplot(111)
# plt.plot(d4[:, 2], d4[:, 1], lw=2, label='steel')
plt.plot(d3[:, 0], d3[:, 1], lw=1, label='measured')
plt.plot(d3[:, 0], d3[:, 2], lw=1, label='measured')
plt.axhline(c='grey'), plt.axvline(c='grey')
# plt.ylim(-800, 800)
# plt.legend(loc=1, shadow=True, numpoints=1)
plt.xlabel("Normalized axial displacement ($\Delta/h_w$), %")
plt.ylabel("Axial force, kips")
plt.minorticks_on()
plt.grid(b=True, which='major', alpha=1, picker=4)
# plt.grid(b=True, which='minor', alpha=0.2)
plt.tight_layout()
pp.savefig(fig)

pp.close()
subprocess.Popen([output_filename], shell=True)
