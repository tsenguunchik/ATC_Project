import math
import matplotlib.pyplot as plt

def Pinching4_newTension(f_y, E, f_u, e_max_tension, Gf_comp_concrete, ec0, f_p, G_bs, Height, IP, b, plotting, regularized):
    e_y = f_y / E
    E_c = 57000 * math.sqrt(-f_p)
    e_max_comp = Gf_comp_concrete / (0.6 * f_p * Height * IP) - 0.8 * f_p / E_c + ec0
    L_IP = Height * IP
    # calcs
    e_1t = e_y
    if regularized == 1:
        e_3t = e_1t + 8 * (e_max_tension - e_1t) / L_IP
    else:
        e_3t = e_max_tension

    s_1t = f_y
    s_3t = s_1t + b * (e_3t - e_1t) * E
    e_2t = (e_1t + e_3t) / 2.0
    s_4t = 0.001 * f_y
    e_4t = (s_3t + 10 * E * e_3t - 0.001 * f_y) / (10 * E)
    s_2t = (s_1t + s_3t) / 2.0

    e_1c = -e_y
    s_1c = -f_y
    e_3c = e_max_comp
    s_3c = s_1c + b * E * (e_3c - e_1c)
    e_2c = (e_3c - e_1c) / 2 + e_1c
    s_2c = (s_3c - s_1c) / 2 + s_1c
    s_4c = 0.5 * s_1c
    e_4c = -2 * G_bs / (L_IP * (1.5 * f_y + b * E * (abs(e_max_comp) - e_y))) + e_3c

    points = [
    s_1t, e_1t,
    s_2t, e_2t,
    s_3t, e_3t,
    s_4t, e_4t,
    s_1c, e_1c,
    s_2c, e_2c,
    s_3c, e_3c,
    s_4c, e_4c]

    print points
    e_t = [0, e_1t, e_2t, e_3t, e_4t, 0.3]
    s_t = [0, s_1t, s_2t, s_3t, s_4t, s_4t]
    plt.plot(e_t, s_t)


    e_c = [0, e_1c, e_2c, e_3c, e_4c, -0.3]
    s_c = [0, s_1c, s_2c, s_3c, s_4c, s_4c]

    plt.plot(e_c, s_c)
    if plotting == 'Yes':
        plt.show()

    return points
