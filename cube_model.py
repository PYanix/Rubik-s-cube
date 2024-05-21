from copy import deepcopy


class Cube:
    def __init__(self, dim: int):
        self.dim = dim
        colors = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        def set_colors(color):
            c = color
            return [['1' + f'{c}', '2' + f'{c}', '3' + f'{c}'], ['4' + f'{c}', '5' + f'{c}', '6' + f'{c}'],
                    ['7' + f'{c}', '8' + f'{c}', '9' + f'{c}']]

        # colors = [['1'+f'{c}', '2'+f'{c}', '3'+f'{c}'], ['4'+f'{c}', '5'+f'{c}', '6'+f'{c}'], ['7'+f'{c}', '8'+f'{c}', '9'+f'{c}']]

        self.R_colors = set_colors('R')
        self.L_colors = set_colors('L')
        self.U_colors = set_colors('U')
        self.D_colors = set_colors('D')
        self.F_colors = set_colors('F')
        self.B_colors = set_colors('B')

        """
        self.R_colors = [['b' for _ in range(self.dim)] for _ in range(self.dim)]  # R - right face of the cube
        self.L_colors = [['g' for _ in range(self.dim)] for _ in range(self.dim)]  # L - left face of the cube
        self.U_colors = [['w' for _ in range(self.dim)] for _ in range(self.dim)]  # U - upper face of the cube
        self.D_colors = [['y' for _ in range(self.dim)] for _ in range(self.dim)]  # D - down face of the cube
        self.F_colors = [['r' for _ in range(self.dim)] for _ in range(self.dim)]  # F - front face of the cube
        self.B_colors = [['o' for _ in range(self.dim)] for _ in range(self.dim)]  # B - back face of the cube
        """

    def __repr__(self) -> str:
        return f'''       {' '.join(map(str, self.U_colors))}'''

    def show_cube(self):
        for i in self.U_colors:
            print('  ' * 3, '', *i, ' ' * 3)
        print()
        for i in range(3):
            print(*self.L_colors[i], ' ', *self.F_colors[i], ' ', *self.R_colors[i])
        print()
        for i in self.D_colors:
            print('  ' * 3, '', *i, ' ' * 3)
        print()
        for i in self.B_colors:
            print('  ' * 3, '', *i, ' ' * 3)

    def rotate_R(self):
        matrixU = [self.U_colors[i][2] for i in range(3)]
        for i in range(3):
            self.U_colors[i][2] = self.F_colors[i][2]
            self.F_colors[i][2] = self.D_colors[i][2]
            self.D_colors[i][2] = self.B_colors[i][2]
            self.B_colors[i][2] = matrixU[i]
        self.R_colors = [[self.R_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]

    def rotate_R_streak(self):
        for _ in range(3):
            self.rotate_R()

    def rotate_L(self):
        matrixU = [self.U_colors[i][0] for i in range(3)]
        for i in range(self.dim):
            self.U_colors[i][0] = self.B_colors[i][0]
            self.B_colors[i][0] = self.D_colors[i][0]
            self.D_colors[i][0] = self.F_colors[i][0]
            self.F_colors[i][0] = matrixU[i]
        self.L_colors = [[self.L_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]

    def rotate_L_streak(self):
        for _ in range(3):
            self.rotate_L()

    def rotate_U(self):
        matrixL = deepcopy(self.L_colors[0])
        for i in range(3):
            self.L_colors[0][i] = self.F_colors[0][i]
            self.F_colors[0][i] = self.R_colors[0][i]
            self.R_colors[0][i] = self.B_colors[2][self.dim - i - 1]
            self.B_colors[2][self.dim - i - 1] = matrixL[i]
        self.U_colors = [[self.U_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]

    def rotate_U_streak(self):
        for _ in range(3):
            self.rotate_U()

    def rotate_F(self):
        matrixR = deepcopy(self.R_colors)
        matrixL = deepcopy(self.L_colors)
        matrixU = deepcopy(self.U_colors)
        matrixD = deepcopy(self.D_colors)
        for i in range(3):
            self.L_colors[i][2] = matrixD[0][i]
            self.D_colors[0][i] = matrixR[self.dim - i - 1][0]
            self.R_colors[i][0] = matrixU[2][i]
            self.U_colors[2][self.dim - i - 1] = matrixL[i][2]
        self.F_colors = [[self.F_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]

    def rotate_F_streak(self):
        for _ in range(3):
            self.rotate_F()

    def rotate_B(self):
        matrixR = deepcopy(self.R_colors)
        matrixL = deepcopy(self.L_colors)
        matrixU = deepcopy(self.U_colors)
        matrixD = deepcopy(self.D_colors)
        for i in range(3):
            self.L_colors[2-i][0] = matrixU[0][i]
            self.D_colors[2][i] = matrixL[i][0]
            self.R_colors[2-i][2] = matrixD[2][i]
            self.U_colors[0][i] = matrixR[i][2]
        self.B_colors = [[self.B_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]


    def rotate_B_streak(self):
        for _ in range(3):
            self.rotate_B()

    def rotate_D(self):
        matrixR = deepcopy(self.R_colors)
        matrixL = deepcopy(self.L_colors)
        matrixF = deepcopy(self.F_colors)
        matrixB = deepcopy(self.B_colors)
        for i in range(3):
            self.R_colors[2][i] = matrixF[2][i]
            self.F_colors[2][i] = matrixL[2][i]
            self.L_colors[2][2-i] = matrixB[0][i]
            self.B_colors[0][2-i] = matrixR[2][i]
        self.D_colors = [[self.D_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]

    def rotate_D_streak(self):
        for _ in range(3):
            self.rotate_D()

    def rotate_cube_U(self):
        matrixR = deepcopy(self.R_colors)
        matrixL = deepcopy(self.L_colors)
        matrixU = deepcopy(self.U_colors)
        matrixD = deepcopy(self.D_colors)
        matrixF = deepcopy(self.F_colors)
        matrixB = deepcopy(self.B_colors)
        self.F_colors = matrixR
        self.R_colors = [[matrixB[j][i] for i in range(2, -1, -1)] for j in range(2, -1, -1)]
        self.L_colors = matrixF
        self.B_colors = [[matrixL[j][i] for i in range(2, -1, -1)] for j in range(2, -1, -1)]
        self.U_colors = [[matrixU[2 - j][i] for j in range(3)] for i in range(3)]
        self.D_colors = [[matrixD[i][j] for i in range(3)] for j in range(2, -1, -1)]

    def rotate_cube_U_streak(self):
        for _ in range(3):
            self.rotate_cube_U()

    def get_colors(self, x, y, z):
        colors = {}
        # x=1
        if x == 1 and y == 1 and z == 1:
            colors['F'] = self.F_colors[0][2]
            colors['U'] = self.U_colors[2][2]
            colors['R'] = self.R_colors[0][0]
        elif x == 1 and y == 1 and z == 0:
            colors['F'] = self.F_colors[1][2]
            colors['R'] = self.R_colors[1][0]
        elif x == 1 and y == 1 and z == -1:
            colors['F'] = self.F_colors[2][2]
            colors['D'] = self.D_colors[0][2]
            colors['R'] = self.R_colors[2][0]
        elif x == 1 and y == 0 and z == 1:
            colors['F'] = self.F_colors[0][1]
            colors['U'] = self.U_colors[2][1]
        elif x == 1 and y == 0 and z == 0:
            colors['F'] = self.F_colors[1][1]
        elif x == 1 and y == 0 and z == -1:
            colors['F'] = self.F_colors[2][1]
            colors['D'] = self.D_colors[0][1]
        elif x == 1 and y == -1 and z == 1:
            colors['F'] = self.F_colors[0][0]
            colors['L'] = self.L_colors[0][2]
            colors['U'] = self.U_colors[2][0]
        elif x == 1 and y == -1 and z == 0:
            colors['F'] = self.F_colors[1][0]
            colors['L'] = self.L_colors[1][2]
        elif x == 1 and y == -1 and z == -1:
            colors['F'] = self.F_colors[2][0]
            colors['L'] = self.L_colors[2][2]
            colors['D'] = self.D_colors[0][0]
        # x=0:
        elif x == 0 and y == 1 and z == 1:
            colors['U'] = self.U_colors[1][2]
            colors['R'] = self.R_colors[0][1]
        elif x == 0 and y == 1 and z == 0:
            colors['R'] = self.R_colors[1][1]
        elif x == 0 and y == 1 and z == -1:
            colors['R'] = self.R_colors[2][1]
            colors['D'] = self.D_colors[1][2]
        elif x == 0 and y == 0 and z == 1:
            colors['U'] = self.U_colors[1][1]
        elif x == 0 and y == 0 and z == -1:
            colors['D'] = self.D_colors[1][1]
        elif x == 0 and y == -1 and z == 1:
            colors['U'] = self.U_colors[1][0]
            colors['L'] = self.L_colors[0][1]
        elif x == 0 and y == -1 and z == 0:
            colors['L'] = self.L_colors[1][1]
        elif x == 0 and y == -1 and z == -1:
            colors['L'] = self.L_colors[2][1]
            colors['D'] = self.D_colors[1][0]
        #x=-1
        elif x == -1 and y == 1 and z == 1:
            colors['U'] = self.U_colors[0][2]
            colors['R'] = self.R_colors[0][2]
            colors['B'] = self.B_colors[2][2]
        elif x == -1 and y == 1 and z == 0:
            colors['R'] = self.R_colors[1][2]
            colors['B'] = self.B_colors[1][2]
        elif x == -1 and y == 1 and z == -1:
            colors['R'] = self.R_colors[2][2]
            colors['B'] = self.B_colors[0][2]
            colors['D'] = self.D_colors[2][2]
        elif x == -1 and y == 0 and z == 1:
            colors['U'] = self.U_colors[0][1]
            colors['B'] = self.B_colors[2][1]
        elif x == -1 and y == 0 and z == 0:
            colors['B'] = self.B_colors[1][1]
        elif x == -1 and y == 0 and z == -1:
            colors['B'] = self.B_colors[0][1]
            colors['D'] = self.D_colors[2][1]
        elif x == -1 and y == -1 and z == 1:
            colors['U'] = self.U_colors[0][0]
            colors['B'] = self.B_colors[2][0]
            colors['L'] = self.L_colors[0][0]
        elif x == -1 and y == -1 and z == 0:
            colors['B'] = self.B_colors[1][0]
            colors['L'] = self.L_colors[1][0]
        elif x == -1 and y == -1 and z == -1:
            colors['B'] = self.B_colors[0][0]
            colors['L'] = self.L_colors[2][0]
            colors['D'] = self.D_colors[2][0]
        return colors