import Wall_opensees
from math import sqrt

bar_size = {"No.2": (0.250, 0.05),  # 1st is diameter of the bar and then the area
                    "No.3": (0.375, 0.11),
                    "No.4": (0.500, 0.20),
                    "No.5": (0.625, 0.31),
                    "No.6": (0.750, 0.44),
                    "No.7": (0.875, 0.60),
                    "No.8": (1.000, 0.79),
                    "No.9": (1.128, 1.00),
                    "No.10": (1.27, 1.27),
                    "No.11": (1.41, 1.56),
                    "No.14": (1.693, 2.25),
                    "No.18": (2.257, 4.00),
                    "No.18J": (2.337, 4.29),
                    }
# Wall Geometry
L = 360.0
w = 24.0
height1 = 15 # height of the first story in [ft]
heightR = 13 # height of the rest of the story in [ft]
Wall_geometry = [L, w, height1, heightR]

# Vertical Steel Layout
# [Boundary Length, Boundary columns, Boundary_rows, Boundary Area, Web columns, Web Area]
Layer1 = [72, 14, 3, 1.27, 33, 0.2] # story 1-2
Layer2 = [36, 6, 3, 1.128, 44, 0.2] # story 3-5
Layer3 = [0, 0, 0, 0, 55, 0.2] # story 6-8
cover = 3

# Transverse Steel Layout
num_ties_y = 2.0
num_ties_x = 3.0
s = 3.5
As_trans = 0.20
ties = [num_ties_y, num_ties_x, s, As_trans]

# Steel Properties
f_y = 70.2e3 # yield stress
f_u = 105.0e3 # ultimate stress
e_u = 0.2 # rupture strain
regularized = 0 # Tension Steel Regularization
Steel = [f_y, f_u, e_u, regularized]

# Concrete Properties
f_c = -6500.0
f_cc = -10272.0
E_c = 57000 * sqrt(-f_c)
res_u = 0.1
res_c = 0.2
e_0c = -0.002 # changes
e_0cc = -0.004
Concrete = [f_c, f_cc, E_c, res_u, res_c, e_0c, e_0cc]

# FileName
file_name = '8story_opensees.tcl'
# Calling the function

# Building Properties
B_length = 120 # ft building length
B_width = 120 # ft building width
f_load = 199.5 # psf floor load
r_load = 154.9 # psf roof load
story = 8
t_area = 30 * 44 # ft^2 tributary area
b_area = B_length * B_width / 2 # ft^2 half of building area
Building = [f_load, r_load, story, t_area, b_area]

# Opensees Constants
elemTol = 1e-6
globalTol = 1e-4
iterations = 2000
percent_drift = 5
Opensees_constant = [elemTol, globalTol, iterations, percent_drift]

# Modelling Approaches
approach = 1 # New Buckling model with ultimate strain 0.2
# approach = 2 # New Buckling model with ultimate strain 0.2 * 0.33
# approach = 3 # New Buckling model with regularized tension steel
MRSA = 0 # 0 means ELF design, 1 means MRSA design

# Changin parameters based on approaches
if approach == 1:
    pass
elif approach == 2:
    e_u = 0.2 * 0.33
    Steel = [f_y, f_u, e_u, regularized]
elif approach == 3:
    regularized = 1
    Steel = [f_y, f_u, e_u, regularized]
if MRSA == 1:
    pass
else:
    Layer1 = [72, 16, 3, 1.27, 33, 0.2]  # story 1-2
    Layer2 = [36, 8, 3, 1.27, 44, 0.2]  # story 3-5

my_class = Wall_opensees.Moment_capacity(Wall_geometry, Layer1, Layer2, Layer3, cover, ties, Steel, Concrete, file_name, Building, Opensees_constant)
