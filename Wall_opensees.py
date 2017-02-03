import os
import subprocess
import math
import Pinching4_newTension as p4


class Moment_capacity:
    ''' ********* '''
    def __init__(self,
                 Wall_geometry,
                 Layer1,
                 Layer2,
                 Layer3,
                 cover,
                 ties,
                 Steel,
                 Concrete,
                 file_name,
                 Building,
                 Opensees
                 ):



        self.Wall_geometry = Wall_geometry
        self.Layer1 = Layer1
        self.Layer2 = Layer2
        self.Layer3 = Layer3
        self.cover = cover
        self.ties = ties
        self.Steel = Steel
        self.Concrete = Concrete
        self.file_name = file_name
        self.Building = Building
        self.Opensees = Opensees

        # Giving variables names

        L = Wall_geometry[0]
        w = Wall_geometry[1]
        Height1 = Wall_geometry[2]  # height of the first story
        HeightR = Wall_geometry[3]  # height of the rest of the story

        # Transverse Steel Layout
        num_ties_y = ties[0]
        num_ties_x = ties[1]
        s = ties[2]
        As_trans = ties[3]

        # Longitudinal Steel Layout
        b_d1 = Layer1[0]
        b_count1 = Layer1[1]
        b_count1_row = Layer1[2]
        A_b1 = Layer1[3]
        W_count1 = Layer1[4]
        A_w1 = Layer1[5]

        b_d2 = Layer2[0]
        b_count2 = Layer2[1]
        b_count2_row = Layer2[2]
        A_b2 = Layer2[3]
        W_count2 = Layer2[4]
        A_w2 = Layer2[5]

        b_d3 = Layer3[0]
        b_count3 = Layer3[1]
        b_count3_row = Layer3[2]
        A_b3 = Layer3[3]
        W_count3 = Layer3[4]
        A_w3 = Layer3[5]

        # Steel Properties
        f_y = Steel[0]  # yield stress
        f_u = Steel[1]  # ultimate stress
        e_u = Steel[2]  # rupture strain
        regularized = Steel[3] # Regularize tension steel or not

        # Concrete Properties
        f_c = Concrete[0]
        f_cc = Concrete[1]
        E_c = Concrete[2]
        res_u = Concrete[3]
        res_c = Concrete[4]
        # e_0c = Concrete[5] changes
        e_0cc = Concrete[6]

        # Building Dimensions
        f_load = Building[0]  # psf floor load
        r_load = Building[1]  # psf roof load
        story = Building[2]
        t_area = Building[3]  # ft^2 tributary area
        b_area = Building[4]  # ft^2 half of building area

        # Opensees Constants
        elemTol = Opensees[0]
        globalTol = Opensees[1]
        iterations = Opensees[2]
        percent_drift = Opensees[3]

        elf = [
            38,
            72,
            105,
            138,
            172,
            205,
            238,
            211]
        # Calculation
        # Concrete
        e_0c = 2 * f_c / E_c
        E_cc = 57000 * math.sqrt(-f_cc)
        lyambda = 0.1
        Gfu = -f_c * 0.078
        ku = 1.0
        fpu = ku * f_c
        Gfc = 1.7 * Gfu
        kc = 1.2
        fpc = f_cc

        # Shear softening
        A_cv = L * w * 5 / 6
        G_agg = 0.4 * E_c * 0.1  # change for walls
        G_agg2 = 0.4 * E_c * 0.5  # change for walls
        K_shear = G_agg * A_cv
        K_shear2 = G_agg2 * A_cv

        # Tensile Strength
        G_atina = 4.044e-1
        L_t = math.sqrt(3 ** 2 + 3 ** 2)
        f_tU = 4 * math.sqrt(-f_c)
        delta_e = 2 * G_atina / f_tU / L_t
        Ets = f_tU / delta_e  # tension softening stiffness
        f_tUc = 4 * math.sqrt(-f_cc)  # tensile strength
        delta_e = 2 * G_atina / f_tUc / L_t
        Etsc = f_tUc / delta_e  # tension softening stiffness

        # Mesh size
        delta = 1  # in increment fiber mesh

        # Steel Property
        E = 29000000
        e_y = f_y / E
        # b = (f_u - f_y) / (0.2 - e_y) / E
        b = (f_u - f_y) / (0.2 - e_y) / E

        # Integration point
        ip1 = 1.0 / 20.0
        ip2 = 49.0 / 180.0
        ip3 = 32.0 / 90.0


        # Create Tickle File for analysis ########################################################
        infile = open(file_name, 'w')  # writing the script
        infile.write('puts "------------------ 8 Story Wall -------------------"\n')
        infile.write('# Create ModelBuilder (with two-dimensions and 3 DOF/node)\n')
        infile.write('wipe\n')
        infile.write('model basic -ndm 2 -ndf 3\n')
        infile.write('file mkdir Output\n')
        infile.write('# Create nodes\n')
        infile.write('# ------------\n')
        infile.write('# Create nodes\n')
        infile.write('#  tag  X    Y \n')
        # Walls
        infile.write('node 1 0.0 0.0 \n\n')
        infile.write('node 2   0.0    ' + str(Height1 * 12) + ' \n')
        infile.write('node 3   0.0		' + str((Height1 + HeightR * 1.0) * 12) + '\n')
        infile.write('node 4   0.0		' + str((Height1 + HeightR * 2.0) * 12) + '\n')
        infile.write('node 5   0.0		' + str((Height1 + HeightR * 3.0) * 12) + '\n')
        infile.write('node 6   0.0		' + str((Height1 + HeightR * 4.0) * 12) + '\n')
        infile.write('node 7   0.0		' + str((Height1 + HeightR * 5.0) * 12) + '\n')
        infile.write('node 8   0.0		' + str((Height1 + HeightR * 6.0) * 12) + '\n')
        infile.write('node 9   0.0		' + str((Height1 + HeightR * 7.0) * 12) + '\n')

        infile.write('fix 1 1 1 1\n')

        infile.write('# Define materials\n')
        infile.write('# ------------------------------------------\n')
        infile.write('# CONCRETE         tag  f''c  ec0  f''cu    ecu\n')

        # Unconfined concrete
        infile.write('uniaxialMaterial Concrete02 11 ' + str(f_c) + ' ' + str(e_0c) + ' ' +
                     str(res_u * f_c) + '   ' +
                     str(Gfu / (0.6 * fpu * Height1 * 12 / 20.0) - 0.8 * fpu / E_c + e_0c) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tU) + ' ' + str(Ets) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 12 ' + str(f_c) + ' ' + str(e_0c) + '  ' +
                     str(res_u * f_c) + '   ' +
                     str(Gfu / (0.6 * fpu * Height1 * 12 * 49. / 180.) - 0.8 * fpu / E_c + e_0c) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tU) + ' ' + str(Ets) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 13 ' + str(f_c) + ' ' + str(e_0c) + '  ' +
                     str(res_u * f_c) + '   ' +
                     str(Gfu / (0.6 * fpu * Height1 * 12 * 32. / 90.0) - 0.8 * fpu / E_c + e_0c) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tU) + ' ' + str(Ets) +
                     '\n')

        infile.write('uniaxialMaterial Concrete02 21 ' + str(f_c) + ' ' + str(e_0c) + ' ' +
                     str(res_u * f_c) + '   ' +
                     str(Gfu / (0.6 * fpu * HeightR * 12 / 20.0) - 0.8 * fpu / E_c + e_0c) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tU) + ' ' + str(Ets) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 22 ' + str(f_c) + ' ' + str(e_0c) + '  ' +
                     str(res_u * f_c) + '   ' +
                     str(Gfu / (0.6 * fpu * HeightR * 12 * 49. / 180.) - 0.8 * fpu / E_c + e_0c) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tU) + ' ' + str(Ets) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 23 ' + str(f_c) + ' ' + str(e_0c) + '  ' +
                     str(res_u * f_c) + '   ' +
                     str(Gfu / (0.6 * fpu * HeightR * 12 * 32. / 90.0) - 0.8 * fpu / E_c + e_0c) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tU) + ' ' + str(Ets) +
                     '\n')

        # Confined concrete
        infile.write('uniaxialMaterial Concrete02 31 ' + str(f_cc) + ' ' + str(e_0cc) + '  ' +
                     str(res_c * f_cc) + '   ' +
                     str(Gfc / (0.6 * fpc * Height1 * 12 / 20.0) - 0.8 * fpc / E_cc + e_0cc) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tUc) + ' ' + str(Etsc) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 32 ' + str(f_cc) + ' ' + str(e_0cc) + '  ' +
                     str(res_c * f_cc) + '   ' +
                     str(Gfc / (0.6 * fpc * Height1 * 12 * 49. / 180.) - 0.8 * fpc / E_cc + e_0cc) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tUc) + ' ' + str(Etsc) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 33 ' + str(f_cc) + ' ' + str(e_0cc) + '  ' +
                     str(res_c * f_cc) + '   ' +
                     str(Gfc / (0.6 * fpc * Height1 * 12 * 32. / 90.0) - 0.8 * fpc / E_cc + e_0cc) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tUc) + ' ' + str(Etsc) +
                     '\n')

        infile.write('uniaxialMaterial Concrete02 41 ' + str(f_cc) + ' ' + str(e_0cc) + '  ' +
                     str(res_c * f_cc) + '   ' +
                     str(Gfc / (0.6 * fpc * HeightR * 12 / 20.0) - 0.8 * fpc / E_cc + e_0cc) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tUc) + ' ' + str(Etsc) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 42 ' + str(f_cc) + ' ' + str(e_0cc) + '  ' +
                     str(res_c * f_cc) + '   ' +
                     str(Gfc / (0.6 * fpc * HeightR * 12 * 49. / 180.) - 0.8 * fpc / E_cc + e_0cc) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tUc) + ' ' + str(Etsc) +
                     '\n')
        infile.write('uniaxialMaterial Concrete02 43 ' + str(f_cc) + ' ' + str(e_0cc) + '  ' +
                     str(res_c * f_cc) + '   ' +
                     str(Gfc / (0.6 * fpc * HeightR * 12 * 32. / 90.0) - 0.8 * fpc / E_cc + e_0cc) + ' ' +
                     str(lyambda) + ' ' +
                     str(f_tUc) + ' ' + str(Etsc) +
                     '\n')

        # STEEL
        infile.write('uniaxialMaterial SteelMPF  1  '+ str(f_y) + ' '+ str(f_y) + ' '+ str(E) + ' ' + str(b) +
                 ' '+ str(b)+ ' 20 0.925 0.15 \n')
        if regularized == 1:
            e_y = f_y / E
            infile.write('uniaxialMaterial MinMax   1011  1 -min ' +
                         str(Gfu / (0.6 * f_c * Height1 * 12 * ip1) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip1 * Height1 * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1012  1 -min ' +
                         str(Gfu / (0.6 * f_c * Height1 * 12 * ip2) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip2 * Height1 * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1013  1 -min ' +
                         str(Gfu / (0.6 * f_c * Height1 * 12 * ip3) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip3 * Height1 * 12) + '\n')

            infile.write('uniaxialMaterial MinMax   1021  1 -min ' +
                         str(Gfu / (0.6 * f_c * HeightR * 12 * ip1) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip1 * HeightR * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1022  1 -min ' +
                         str(Gfu / (0.6 * f_c * HeightR * 12 * ip2) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip2 * HeightR * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1023  1 -min ' +
                         str(Gfu / (0.6 * f_c * HeightR * 12 * ip3) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip3 * HeightR * 12) + '\n')

            infile.write('uniaxialMaterial MinMax   1031  1 -min ' +
                         str(Gfc / (0.6 * f_cc * Height1 * 12 * ip1) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip1 * Height1 * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1032  1 -min ' +
                         str(Gfc / (0.6 * f_cc * Height1 * 12 * ip2) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip2 * Height1 * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1033  1 -min ' +
                         str(Gfc / (0.6 * f_cc * Height1 * 12 * ip3) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip3 * Height1 * 12) + '\n')

            infile.write('uniaxialMaterial MinMax   1041  1 -min ' +
                         str(Gfc / (0.6 * f_cc * HeightR * 12 * ip1) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip1 * HeightR * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1042  1 -min ' +
                         str(Gfc / (0.6 * f_cc * HeightR * 12 * ip2) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip2 * HeightR * 12) + '\n')
            infile.write('uniaxialMaterial MinMax   1043  1 -min ' +
                         str(Gfc / (0.6 * f_cc * HeightR * 12 * ip3) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(
                e_y + 8 * (0.2 - e_y) / ip3 * HeightR * 12) + '\n')
        else:
            infile.write('uniaxialMaterial MinMax   1011  1 -min ' +
                         str(Gfu / (0.6 * f_c * Height1 * 12 * ip1) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1012  1 -min ' +
                         str(Gfu / (0.6 * f_c * Height1 * 12 * ip2) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1013  1 -min ' +
                         str(Gfu / (0.6 * f_c * Height1 * 12 * ip3) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(e_u) + '\n')

            infile.write('uniaxialMaterial MinMax   1021  1 -min ' +
                         str(Gfu / (0.6 * f_c * HeightR * 12 * ip1) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1022  1 -min ' +
                         str(Gfu / (0.6 * f_c * HeightR * 12 * ip2) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1023  1 -min ' +
                         str(Gfu / (0.6 * f_c * HeightR * 12 * ip3) - 0.8 * f_c / E_c + e_0c) + ' -max ' + str(e_u) + '\n')

            infile.write('uniaxialMaterial MinMax   1031  1 -min ' +
                         str(Gfc / (0.6 * f_cc * Height1 * 12 * ip1) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1032  1 -min ' +
                         str(Gfc / (0.6 * f_cc * Height1 * 12 * ip2) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1033  1 -min ' +
                         str(Gfc / (0.6 * f_cc * Height1 * 12 * ip3) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(e_u) + '\n')

            infile.write('uniaxialMaterial MinMax   1041  1 -min ' +
                         str(Gfc / (0.6 * f_cc * HeightR * 12 * ip1) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1042  1 -min ' +
                         str(Gfc / (0.6 * f_cc * HeightR * 12 * ip2) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(e_u) + '\n')
            infile.write('uniaxialMaterial MinMax   1043  1 -min ' +
                         str(Gfc / (0.6 * f_cc * HeightR * 12 * ip3) - 0.8 * f_cc / E_cc + e_0cc) + ' -max ' + str(e_u) + '\n')

        infile.write('uniaxialMaterial Steel01 90 50.00 ' + str(K_shear) + ' 1.0000\n')
        infile.write('uniaxialMaterial Steel01 91 50.00 ' + str(K_shear2) + ' 1.0000\n')

        infile.write('set AsBE  ' + str(A_b1) + '\n')
        infile.write('set AsBE1  ' + str(A_b2) + '\n')
        infile.write('set AsWeb  ' + str(A_w1) + '\n')

        y1 = L / 2
        z1 = w / 2
        # From story 1 - 2

        infile.write('section Fiber 1 {\n')
        # Create BE fibers\n
        infile.write(
            'patch rect 31 ' + str(int(b_d1 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 31 ' + str(int(b_d1 / delta)) + ' 1 ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + '   ' + str(z1 - cover) + '\n')

        # Create the concrete cover fibers(top, bottom, left, right)\n ')
        infile.write(
            'patch rect 11 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + ' ' + str(z1 - cover) + ' ' + str(y1) + ' ' +
            str(z1) + '\n')
        infile.write('patch rect 11 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + ' ' + str(-z1) + ' ' + str(y1) + ' ' +
                     str(cover - z1) + '\n')
        infile.write('patch rect 11 1 1 ' + str(-y1) + ' ' + str(cover - z1) + ' ' + str(cover - y1) + ' ' +
                     str(z1 - cover) + '\n')
        infile.write('patch rect 11 1 1 ' + str(y1 - cover) + ' ' + str(cover - z1) + ' ' + str(y1) + ' ' +
                     str(z1 - cover) + '\n')
        infile.write(
            'patch rect 11 ' + str(int((L - 2 * b_d1) / delta)) + ' 1 ' + str(-y1 + b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - b_d1) + ' ' + str(z1 - cover) + '\n')

        # Create the reinforcing fibers(left, middle, right)\n ')
        # boundary elements
        infile.write(
            'layer straight 1031 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1031 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1031 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1031 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1031 2 $AsBE ' + str(y1 - b_d1) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1031 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d1) + ' 0\n')

        # creating web elements
        infile.write('layer straight 1011 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1011 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(cover - z1) + '\n')

        infile.write('}  \n')

        infile.write('section Fiber 2 {\n')

        # Create BE fibers\n')
        infile.write(
            'patch rect 32 ' + str(int(b_d1 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 32 ' + str(int(b_d1 / delta)) + ' 1 ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')

        # Create the concrete cover fibers(top, bottom, left, right)\n ')
        infile.write(
            'patch rect 12 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 12 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 12 1 1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 12 1 1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 12 ' + str(int((L - 2 * b_d1) / delta)) + ' 1 ' + str(-y1 + b_d1) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + '\n')

        # Create boundary steel
        infile.write(
            'layer straight 1032 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1032 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1032 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1032 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1032 2 $AsBE ' + str(y1 - b_d1) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1032 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d1) + ' 0\n')

        # creating web elements
        infile.write('layer straight 1012 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1012 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(cover - z1) + '\n')

        infile.write('} \n')

        infile.write('section Fiber 3 {\n')

        # Create BE fibers\n ')
        infile.write(
            'patch rect 33 ' + str(int(b_d1 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 33 ' + str(int(b_d1 / delta)) + ' 1 ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')

        # Create the concrete cover fibers(top, bottom, left, right)\n ')
        infile.write(
            'patch rect 13 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 13 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 13 1  1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 13 1 1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 13 ' + str(int((L - 2 * b_d1) / delta)) + ' 1 ' + str(-y1 + b_d1) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + '\n')

        # Create boundary steel
        infile.write(
            'layer straight 1033 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1033 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1033 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1033 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1033 2 $AsBE ' + str(y1 - b_d1) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1033 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d1) + ' 0\n')

        infile.write('layer straight 1013 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1013 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(cover - z1) + '\n')

        infile.write('} \n')

        # Story 2 - 3

        infile.write('section Fiber 4 {\n')
        infile.write(
            'patch rect 41 ' + str(int(b_d1 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 41 ' + str(int(b_d1 / delta)) + ' 1 ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 21 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 21 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 21 1  1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 21 1  1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 21 ' + str(int((L - 2 * b_d1) / delta)) + ' 1 ' + str(-y1 + b_d1) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + '\n')

        infile.write(
            'layer straight 1041 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1041 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1041 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1041 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1041 2 $AsBE ' + str(y1 - b_d1) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1041 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d1) + ' 0\n')

        infile.write('layer straight 1021 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1021 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(cover - z1) + '\n')

        infile.write('}  \n')

        infile.write('section Fiber 5 {\n')

        infile.write(
            'patch rect 42 ' + str(int(b_d1 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 42 ' + str(int(b_d1 / delta)) + ' 1 ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 22 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 22 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 22 1  1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 22 1  1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 22 ' + str(int((L - 2 * b_d1) / delta)) + ' 1 ' + str(-y1 + b_d1) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + '\n')

        # Create the reinforcing fibers(left, middle, right)\n')
        # boundary elements
        infile.write(
            'layer straight 1042 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1042 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1042 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1042 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1042 2 $AsBE ' + str(y1 - b_d1) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1042 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d1) + ' 0\n')

        infile.write('layer straight 1022 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1022 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(cover - z1) + '\n')
        infile.write('}\n')

        infile.write('section Fiber 6 {\n')

        infile.write(
            'patch rect 43 ' + str(int(b_d1 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 43 ' + str(int(b_d1 / delta)) + ' 1 ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')

        infile.write(
            'patch rect 23 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 23 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 23 1  1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 23 1  1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 23 ' + str(int((L - 2 * b_d1) / delta)) + ' 1 ' + str(-y1 + b_d1) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + '\n')

        # boundary elements
        infile.write(
            'layer straight 1043 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1043 ' + str(b_count1) + ' $AsBE ' + str(y1 - b_d1) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1043 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d1) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1043 ' + str(b_count1) + ' $AsBE ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d1) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1043 2 $AsBE ' + str(y1 - b_d1) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1043 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d1) + ' 0\n')

        # creating web elements
        infile.write('layer straight 1023 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1023 ' + str(W_count1) + ' $AsWeb ' + str(-y1 + b_d1 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d1 - 2 * cover) + ' ' + str(cover - z1) + '\n')
        infile.write('}\n')

        # From story 3 - 5
        infile.write('section Fiber 7 {\n')

        infile.write(
            'patch rect 41 ' + str(int(b_d2 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d2) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 41 ' + str(int(b_d2 / delta)) + ' 1 ' + str(y1 - b_d2) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')

        infile.write(
            'patch rect 21 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 21 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 21 1  1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 21 1  1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 21 ' + str(int((L - 2 * b_d2) / delta)) + ' 1 ' + str(-y1 + b_d2) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d2) + ' ' + str(z1 - cover) + '\n')

        # Create the reinforcing fibers(left, middle, right)\n ')
        #  boundary elements
        infile.write(
            'layer straight 1041 ' + str(b_count2) + ' $AsBE1 ' + str(y1 - b_d2) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1041 ' + str(b_count2) + ' $AsBE1 ' + str(y1 - b_d2) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1041 ' + str(b_count2) + ' $AsBE1 ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d2) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1041 ' + str(b_count2) + ' $AsBE1 ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d2) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1041 2 $AsBE ' + str(y1 - b_d2) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1041 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d2) + ' 0\n')

        # creating web elements
        infile.write('layer straight 1021 ' + str(W_count2) + ' $AsWeb ' + str(-y1 + b_d2 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d2 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1021 ' + str(W_count2) + ' $AsWeb ' + str(-y1 + b_d2 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d2 - 2 * cover) + ' ' + str(cover - z1) + '\n')

        infile.write('}  \n')

        infile.write('section Fiber 8 {\n')

        infile.write(
            'patch rect 42 ' + str(int(b_d2 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d2) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 42 ' + str(int(b_d2 / delta)) + ' 1 ' + str(y1 - b_d2) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')

        infile.write(
            'patch rect 22 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 22 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 22 1  1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 22 1  1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 22 ' + str(int((L - 2 * b_d2) / delta)) + ' 1 ' + str(-y1 + b_d2) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d2) + ' ' + str(z1 - cover) + '\n')

        infile.write(
            'layer straight 1042 ' + str(b_count2) + ' $AsBE1 ' + str(y1 - b_d2) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1042 ' + str(b_count2) + ' $AsBE1 ' + str(y1 - b_d2) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1042 ' + str(b_count2) + ' $AsBE1 ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d2) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1042 ' + str(b_count2) + ' $AsBE1 ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d2) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1042 2 $AsBE ' + str(y1 - b_d2) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1042 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d2) + ' 0\n')

        # creating web elements
        infile.write('layer straight 1022 ' + str(W_count2) + ' $AsWeb ' + str(-y1 + b_d2 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d2 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1022 ' + str(W_count2) + ' $AsWeb ' + str(-y1 + b_d2 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d2 - 2 * cover) + ' ' + str(cover - z1) + '\n')
        infile.write('}\n')

        infile.write('section Fiber 9 {\n')

        infile.write(
            'patch rect 43 ' + str(int(b_d2 / delta)) + ' 1 ' + str(cover - y1) + '  ' + str(cover - z1) + ' ' +
            str(-y1 + b_d2) + ' ' + str(z1 - cover) + '\n')
        infile.write('patch rect 43 ' + str(int(b_d2 / delta)) + ' 1 ' + str(y1 - b_d2) + ' ' + str(cover - z1) + ' ' +
                     str(y1 - cover) + '   ' + str(z1 - cover) + '\n')

        infile.write(
            'patch rect 23 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(z1 - cover) + ' ' +
            str(y1) + '         ' + str(z1) + '\n')
        infile.write('patch rect 23 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + '      ' + str(-z1) + '    ' +
                     str(y1) + '         ' + str(cover - z1) + '\n')
        infile.write(
            'patch rect 23 1  1 ' + str(-y1) + '      ' + str(cover - z1) + ' ' + str(cover - y1) + '  ' +
            str(z1 - cover) + '\n')
        infile.write('patch rect 23 1  1 ' + str(y1 - cover) + '   ' + str(cover - z1) + ' ' + str(y1) +
                     '         ' + str(z1 - cover) + '\n')
        infile.write(
            'patch rect 23 ' + str(int((L - 2 * b_d2) / delta)) + ' 1 ' + str(-y1 + b_d2) + ' ' + str(cover - z1) +
            ' ' + str(y1 - b_d2) + ' ' + str(z1 - cover) + '\n')

        infile.write(
            'layer straight 1043 ' + str(b_count2) + ' $AsBE1 ' + str(y1 - b_d2) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1043 ' + str(b_count2) + ' $AsBE1 ' + str(y1 - b_d2) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write(
            'layer straight 1043 ' + str(b_count2) + ' $AsBE1 ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(-y1 + b_d2) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1043 ' + str(b_count2) + ' $AsBE1 ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(-y1 + b_d2) + ' ' + str(cover - z1) + '\n')
        infile.write('layer straight 1043 2 $AsBE ' + str(y1 - b_d2) + ' 0 ' + str(y1 - cover) + ' 0\n')
        infile.write('layer straight 1043 2 $AsBE ' + str(-y1 + cover) + ' 0 ' + str(-y1 + b_d2) + ' 0\n')
        # creating web elements
        infile.write('layer straight 1023 ' + str(W_count2) + ' $AsWeb ' + str(-y1 + b_d2 + 2 * cover) + ' ' +
                     str(z1 - cover) + ' ' + str(y1 - b_d2 - 2 * cover) + ' ' + str(z1 - cover) + '\n')
        infile.write('layer straight 1023 ' + str(W_count2) + ' $AsWeb ' + str(-y1 + b_d2 + 2 * cover) + ' ' +
                     str(cover - z1) + ' ' + str(y1 - b_d2 - 2 * cover) + ' ' + str(cover - z1) + '\n')
        infile.write('}\n')

        # From  story  6 - 8
        infile.write('section Fiber 10 {\n')

        infile.write(
            'patch rect 21 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + ' ' + str(-z1) + ' ' + str(y1) + ' ' +
            str(z1) + '\n')

        infile.write(
            'layer straight 1021 ' + str(W_count3) + ' $AsWeb ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1021 ' + str(W_count3) + ' $AsWeb ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')

        infile.write('}  \n')

        infile.write('section Fiber 11 {\n')

        infile.write(
            'patch rect 22 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + ' ' + str(-z1) + ' ' + str(y1) + ' ' +
            str(z1) + '\n')

        infile.write(
            'layer straight 1022 ' + str(W_count3) + ' $AsWeb ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1022 ' + str(W_count3) + ' $AsWeb ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write('}\n')

        infile.write('section Fiber 12 {\n')

        infile.write(
            'patch rect 23 ' + str(int(L / delta)) + ' 1 ' + str(-y1) + ' ' + str(-z1) + ' ' + str(y1) + ' ' +
            str(z1) + '\n')

        infile.write(
            'layer straight 1023 ' + str(W_count3) + ' $AsWeb ' + str(-y1 + cover) + ' ' + str(z1 - cover) + ' ' +
            str(y1 - cover) + ' ' + str(z1 - cover) + '\n')
        infile.write(
            'layer straight 1023 ' + str(W_count3) + ' $AsWeb ' + str(-y1 + cover) + ' ' + str(cover - z1) + ' ' +
            str(y1 - cover) + ' ' + str(cover - z1) + '\n')
        infile.write('}\n')

        infile.write('geomTransf Corotational 1\n')
        infile.write('section Aggregator 101 90 Vy -section 1\n')
        infile.write('section Aggregator 102 90 Vy -section 2\n')
        infile.write('section Aggregator 103 90 Vy -section 3\n')

        infile.write('section Aggregator 104 91 Vy -section 4\n')
        infile.write('section Aggregator 105 91 Vy -section 5\n')
        infile.write('section Aggregator 106 91 Vy -section 6\n')

        infile.write('section Aggregator 107 91 Vy -section 7\n')
        infile.write('section Aggregator 108 91 Vy -section 8\n')
        infile.write('section Aggregator 109 91 Vy -section 9\n')

        infile.write('section Aggregator 1010 91 Vy -section 10\n')
        infile.write('section Aggregator 1011 91 Vy -section 11\n')
        infile.write('section Aggregator 1012 91 Vy -section 12\n')

        # infile.write('#set locations {-1 -0.65465367 0. 0.65465367 1.0}\n')
        infile.write('set locations {0.0 0.172673165 0.5 0.827326835 1.0}\n')
        # infile.write('set weights   {0.1 0.54444444 0.711111111 0.54444444 0.1}\n')
        infile.write('set weights  {0.05 0.27222222 0.3555555555 0.27222222 0.05}\n')
        infile.write('set secTags1  {101 102 103 102 101}\n')
        infile.write('set secTags2  {104 105 106 105 104}\n')
        infile.write('set secTags3  {107 108 109 108 107}\n')
        infile.write('set secTags4  {1010 1011 1012 1011 1010}\n')
        infile.write('set elemTol ' + str(elemTol) + ' \n')
        infile.write('element forceBeamColumn 1 1 2 1 UserDefined 5 $secTags1 $locations $weights -iter 10 $elemTol\n')
        infile.write('element forceBeamColumn 2 2 3 1 UserDefined 5 $secTags2 $locations $weights -iter 10 $elemTol\n')
        infile.write('element forceBeamColumn 3 3 4 1 UserDefined 5 $secTags3 $locations $weights -iter 10 $elemTol\n')
        infile.write('element forceBeamColumn 4 4 5 1 UserDefined 5 $secTags3 $locations $weights -iter 10 $elemTol\n')
        infile.write('element forceBeamColumn 5 5 6 1 UserDefined 5 $secTags3 $locations $weights -iter 10 $elemTol\n')
        infile.write('element forceBeamColumn 6 6 7 1 UserDefined 5 $secTags4 $locations $weights -iter 10 $elemTol\n')
        infile.write('element forceBeamColumn 7 7 8 1 UserDefined 5 $secTags4 $locations $weights -iter 10 $elemTol\n')
        infile.write('element forceBeamColumn 8 8 9 1 UserDefined 5 $secTags4 $locations $weights -iter 10 $elemTol\n')
        # ------------------------------
        # Create recorders
        # ------------------------------
        # Stress Strain of Fiber 1 only
        for j in range(1, 4):  # number of fibers
            for i in range(1, 9):  # number of stories
                # ------------------------Compression Side
                if i == 1:
                    # Extreme Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_EC_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2) + ' 0.0 1' + str(j) + ' stressStrain\n')
                    # Confined Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_CC_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2 + cover + delta) +
                        ' 0.0 3' + str(j) + ' stressStrain\n')
                    # Extreme Steel
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_ES_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2 + cover) + ' ' +
                        str(w / 2 - cover) + ' 103' + str(j) + ' stressStrain\n')

                    # ------------------------Tension Side

                    # Extreme Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_EC_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2) + ' 0.0 1' + str(j) + ' stressStrain\n')
                    # Confined Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_CC_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2 - cover - delta) +
                        ' 0.0 3' + str(j) + ' stressStrain\n')
                    # Extreme Steel
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_ES_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2 - cover) + ' ' +
                        str(w / 2 - cover) + ' 103' + str(j) + ' stressStrain\n')
                elif i > 5:  # Story 6 - 8
                    # This section has no confinement
                    # Extreme Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_EC_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2) + ' 0.0 2' + str(j) + ' stressStrain\n')
                    # Extreme Steel
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_ES_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2 + cover) + ' ' +
                        str(w / 2 - cover) + ' 102' + str(j) + ' stressStrain\n')
                    # ------------------------Tension Side
                    # Extreme Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_EC_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2) + ' 0.0 2' + str(j) + ' stressStrain\n')
                    # Extreme Steel
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_ES_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2 - cover) + ' ' +
                        str(w / 2 - cover) + ' 102' + str(j) + ' stressStrain\n')
                else:  # Story 2 - 5
                    # Extreme Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_EC_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2) + ' 0.0 2' + str(j) + ' stressStrain\n')
                    # Confined Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_CC_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2 + cover + delta) +
                        ' 0.0 4' + str(j) + ' stressStrain\n')
                    # Extreme Steel
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_ES_Comp'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(-L / 2 + cover) + ' ' +
                        str(w / 2 - cover) + ' 104' + str(j) + ' stressStrain\n')

                    # ------------------------Tension Side

                    # Extreme Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_EC_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2) + ' 0.0 2' + str(j) + ' stressStrain\n')
                    # Confined Concrete
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_CC_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2 - cover - delta) +
                        ' 0.0 4' + str(j) + ' stressStrain\n')
                    # Extreme Steel
                    infile.write(
                        'recorder Element -file Output/story' + str(i) + '_SS_ES_Ten'+ str(j) +'.txt -time -ele ' + str(i) +
                        ' section ' + str(j) + ' fiber ' + str(L / 2 - cover) + ' ' +
                        str(w / 2 - cover) + ' 104' + str(j) + ' stressStrain\n')

        infile.write('recorder Node  -file Output/node1R_regular.txt -time -node 1 -dof 1 2 3 reaction\n')
        infile.write('recorder Node  -file Output/nodeDisp_regular.txt -time -node 2 3 4 5 6 7 8 9 -dof 1 2 3 disp\n')
        infile.write('recorder Element -file Output/WallForces_regular.txt -time -ele 1 2 3 4 5 6 7 8 globalForce\n')

        for j in range(1,9):
            infile.write(
                'recorder Element -file Output/SectionCurvature' + str(j) + '_regular1.txt -time -ele ' + str(j) +
                ' section 1 deformation\n')
            infile.write('recorder Element -file Output/SectionMoment' + str(j) + '_regular1.txt -time -ele ' + str(j) +
                         ' section 1 force\n')
            infile.write(
                'recorder Element -file Output/SectionCurvature' + str(j) + '_regular2.txt -time -ele ' + str(j) +
                ' section 2 deformation\n')
            infile.write('recorder Element -file Output/SectionMoment' + str(j) + '_regular2.txt -time -ele ' + str(j) +
                         ' section 2 force\n')
            infile.write(
                'recorder Element -file Output/SectionCurvature' + str(j) + '_regular3.txt -time -ele ' + str(j) +
                ' section 3 deformation\n')
            infile.write('recorder Element -file Output/SectionMoment' + str(j) + '_regular3.txt -time -ele ' + str(j) +
                         ' section 3 force\n')
            infile.write(
                'recorder Element -file Output/SectionCurvature' + str(j) + '_regular4.txt -time -ele ' + str(j) +
                ' section 4 deformation\n')
            infile.write('recorder Element -file Output/SectionMoment' + str(j) + '_regular4.txt -time -ele ' + str(j) +
                         ' section 4 force\n')
            infile.write(
                'recorder Element -file Output/SectionCurvature' + str(j) + '_regular5.txt -time -ele ' + str(j) +
                ' section 5 deformation\n')
            infile.write('recorder Element -file Output/SectionMoment' + str(j) + '_regular5.txt -time -ele ' + str(j) +
                         ' section 5 force\n')

        infile.write('# ------------------------------\n')
        infile.write('# End of model generation\n')
        infile.write('# ------------------------------\n')

        infile.write('# ------------------------------\n')
        infile.write('# Start of analysis\n')
        infile.write('# ------------------------------\n')

        infile.write('# Define gravity loads\n')
        infile.write('# --------------------\n')
        infile.write('# Set a parameter for the axial load\n')

        # Create a Plain load pattern with a Linear TimeSeries\n')
        infile.write('pattern Plain 1 "Linear" {\n')
        # Create nodal loads at all floors with half load applied to roof\n')
        # nd FX FY MZ \n ')

        infile.write('	load 2  0.0 ' + str(-t_area * f_load) + '  0.0\n')
        infile.write('	load 3  0.0 ' + str(-t_area * f_load) + '  0.0\n')
        infile.write('	load 4  0.0 ' + str(-t_area * f_load) + '  0.0\n')
        infile.write('	load 5  0.0 ' + str(-t_area * f_load) + '  0.0\n')
        infile.write('	load 6  0.0 ' + str(-t_area * f_load) + '  0.0\n')
        infile.write('	load 7  0.0 ' + str(-t_area * f_load) + '  0.0\n')
        infile.write('	load 8  0.0 ' + str(-t_area * f_load) + '  0.0\n')
        infile.write('	load 9  0.0 ' + str(-t_area * r_load) + '  0.0\n')

        infile.write('}\n')
        # Gravity analysis - - load - controlled static analysis\n ')

        infile.write('set Tol 1.0e-8;						# convergence tolerance for test\n')

        infile.write('constraints Plain;   				# how it handles boundary conditions\n')
        infile.write('numberer Plain;	# renumber dof''s to minimize band-width (optimization) + if you want to\n')
        infile.write('system BandGeneral;					# how to store and solve the system of equations in the analysis\n')
        infile.write('test NormDispIncr $Tol 10; 		# determine if convergence has been achieved at the end of an iteration step\n')
        infile.write('algorithm Newton;					# use Newton''s solution algorithm: updates tangent stiffness at every iteration\n')
        infile.write('set NstepGravity 10; 				# apply gravity in 10 steps\n')
        infile.write('set DGravity [expr 1./$NstepGravity]; 	# first load increment\n')
        infile.write('integrator LoadControl $DGravity;	# determine the next time step for an analysis\n')
        infile.write('analysis Static;					# define type of analysis static or transient\n')
        infile.write('analyze $NstepGravity	;			# apply gravity\n')
        infile.write(
            '# ------------------------------------------------- maintain constant gravity loads and reset time to zero\n')
        infile.write('loadConst -time 0.0;\n')

        # STATIC PUSHOVER ANALYSIS - -------------------------------------------------------------------------------------------------\n ')
        # create load pattern for lateral pushover load\n')
        # single pointload  at story six.NOte that  true effective height is 72 ft height of  story 6 is 67 ft.\n ')

        # ELF load distribution\n ')
        infile.write('pattern Plain 12 Linear {				# define load pattern -- generalized\n')
        infile.write('	load 9 [expr ' + str(elf[7]) + './1534.] 0.0 0.0 \n')
        infile.write('	load 8 [expr ' + str(elf[6]) + './1534.] 0.0 0.0 \n')
        infile.write('	load 7 [expr ' + str(elf[5]) + './1534.] 0.0 0.0 \n')
        infile.write('	load 6 [expr ' + str(elf[4]) + './1534.] 0.0 0.0 \n')
        infile.write('	load 5 [expr ' + str(elf[3]) + './1534.] 0.0 0.0 \n')
        infile.write('	load 4 [expr ' + str(elf[2]) + './1534.] 0.0 0.0 \n')
        infile.write('	load 3 [expr ' + str(elf[1]) + './1534.] 0.0 0.0 \n')
        infile.write('	load 2 [expr ' + str(elf[0]) + './1534.] 0.0 0.0 \n')
        infile.write('}\n')
        infile.write('set globalTol ' + str(globalTol) + ' ;\n')
        infile.write('constraints Transformation;\n')
        infile.write('numberer RCM;\n')
        infile.write('system ProfileSPD;\n')
        infile.write('set globalSolutionTol $globalTol;\n')
        infile.write('set numIter	35;\n')
        infile.write('set printFlagStatic 0;\n')
        infile.write('test NormUnbalance $globalSolutionTol $numIter $printFlagStatic;\n')
        infile.write('algorithm Newton;\n')


        infile.write('set nodeTag 9;					# node where displacement is read for displacement control\n')
        infile.write(
            'set dofTag 1;					# degree of freedom of displacement read for displacement contro\n')

        # maximum displacement of pushover.push to 10  # drift.
        infile.write('set Dmax [expr 0.0' + str(percent_drift) + '*[expr (15.0 + 13.0*7.0)*12.0]];\n')
        infile.write('set Dincr [expr 0.01*$Dmax];		# displacement increment for pushover. you want this to be very small + but not too small to slow down the analysis\n')
        infile.write('set minDu [expr 0.00001*$Dincr];\n')
        infile.write('set maxDu $Dincr;\n')
        infile.write('set dU1 $Dincr;\n')

        infile.write('integrator DisplacementControl $nodeTag $dofTag $dU1 4 $minDu $maxDu;\n')
        infile.write('analysis Static;\n')
        infile.write('set nSteps [expr int($Dmax/$dU1)];\n')

        infile.write('# --- Set initial variables ---\n')
        infile.write('set uDemand 0; set duDemand 0;\n')
        infile.write('set ok 0; set linearFlag 0; set stepCount 0; set stepKill ' + str(iterations) + ';\n')

        infile.write('# ---------------------------------  perform Static Pushover Analysis;\n')
        infile.write('# set Nsteps [expr int($Dmax/$Dincr)];    # number of pushover analysis steps;\n')
        infile.write(
            '# set ok [analyze $Nsteps];        # this will return zero if no convergence problems were encountered;\n')

        infile.write('puts "Model Built"\n')

        infile.write('#\n')
        infile.write(
            '# Perform Analysis -----------------------------------------------------------------------------------\n')
        infile.write('while {$ok == 0 && $uDemand < $Dmax && $stepCount < $stepKill } {\n')
        infile.write('	set ok [analyze 1 $dU1];	\n')
        infile.write('	set duDemand [nodeDisp $nodeTag $dofTag];\n')

        infile.write('	# if the analysis fails try some other stuff\n')
        infile.write('	if {$ok != 0} {\n')
        infile.write('			puts "***that didn''t work - try Modified Newton"\n')
        infile.write('			integrator DisplacementControl $nodeTag $dofTag 0 1 $minDu $minDu\n')
        infile.write('			algorithm Newton -initial\n')
        infile.write('			set ok [analyze 1 $dU1];\n')
        infile.write('			set duDemand [nodeDisp $nodeTag $dofTag];\n')
        infile.write('      if {$ok != 0} {\n')
        infile.write('        puts "***that didn''t work - try Newton-Line Search"\n')
        infile.write('        algorithm NewtonLineSearch	0.8\n')
        infile.write('        set ok [analyze 1 $dU1];\n')
        infile.write('        set duDemand [nodeDisp $nodeTag $dofTag];\n')
        infile.write('        if {$ok != 0} {\n')
        infile.write('            puts "***that didn''t work - take large step"\n')
        infile.write(
            '            integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu*20] [expr $maxDu*20]\n')
        infile.write('            test NormDispIncr 1e-3 [expr $numIter] 2\n')
        infile.write('            algorithm Newton\n')
        infile.write('            set ok [analyze 1 [expr $minDu*5.]];\n')
        infile.write('            set duDemand [nodeDisp $nodeTag $dofTag];\n')
        infile.write('          if {$ok != 0} {\n')
        infile.write('            puts "***that didn''t work - take large step"\n')
        infile.write(
            '            integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu*20] [expr $maxDu*20]\n')
        infile.write('            test NormDispIncr 1e-3 [expr $numIter] 2\n')
        infile.write('            algorithm Newton\n')
        infile.write('            set ok [analyze 1 [expr $minDu*5.]];\n')
        infile.write('            set duDemand [nodeDisp $nodeTag $dofTag];\n')
        infile.write('            if {$ok != 0} {\n')
        infile.write('              puts "***that didn''t work - take small step"\n')
        infile.write(
            '              integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu/100] [expr $maxDu/100]\n')
        infile.write('              test NormDispIncr 1e-3 [expr $numIter] 2\n')
        infile.write('              set ok [analyze 1 [expr $minDu/100.]];\n')
        infile.write('              set duDemand [nodeDisp $nodeTag $dofTag];\n')
        infile.write('              if {$ok != 0} {\n')
        infile.write('                puts "***that didn''t work - take linear step"\n')
        infile.write('                set linearFlag 1;\n')
        infile.write('                test NormDispIncr 1e-3 [expr $numIter*2] 2\n')
        infile.write('                algorithm Linear\n')
        infile.write('                set ok [analyze 1 $minDu];\n')
        infile.write('                set duDemand [nodeDisp $nodeTag $dofTag];\n')
        infile.write('              }\n')
        infile.write('            }\n')
        infile.write('          }\n')
        infile.write('}\n')
        infile.write('      }\n')

        infile.write('		if {$ok == 0} {\n')
        infile.write('			puts "***... back to regular Newton"\n')
        infile.write(
            '			integrator DisplacementControl $nodeTag $dofTag 0 4 [expr $minDu] [expr $maxDu]\n')
        infile.write('			test NormDispIncr [expr $globalSolutionTol] $numIter $printFlagStatic\n')
        infile.write('			algorithm Newton\n')
        infile.write('		}\n')
        infile.write('	}\n')
        infile.write('	set uDemand [expr $duDemand];				# update new Ui\n')
        infile.write('	set stepCount [expr $stepCount + 1];		# update the step number\n')
        infile.write('	puts "stepCount $stepCount"\n')
        infile.write('}\n')
        infile.write(
            '# Window Outputs -----------------------------------------------------------------------------------------------------\n')
        infile.write('puts " "\n')
        infile.write('puts "=================================================================================="\n')
        infile.write('puts "================================= Analysis Ended ================================="\n')
        infile.write('puts "=================================================================================="\n')
        infile.write('puts " "\n')
        infile.write('if {$ok != 0} {\n')
        infile.write('	puts "target displacement NOT achieved"\n')
        infile.write('} elseif {$linearFlag == 1} {\n')
        infile.write('	puts "target displacement achieved but required linear steps"\n')
        infile.write('} else {\n')
        infile.write('	puts "target displacement achieved successfully"\n')
        infile.write('}\n')
        infile.write('wipe\n')
        infile.close()
        #############################################################################################################

        # Run OpenSEES file
        cmd = ['OpenSees', file_name] # runFile2D.tcl is the main file
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()


    