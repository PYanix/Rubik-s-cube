from copy import deepcopy


class Cube:
    def __init__(self, dim: int):
        self.dim = dim
        colors = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        def colors(color):
            c = color
            return [['1' + f'{c}', '2' + f'{c}', '3' + f'{c}'], ['4' + f'{c}', '5' + f'{c}', '6' + f'{c}'],
                    ['7' + f'{c}', '8' + f'{c}', '9' + f'{c}']]

        # colors = [['1'+f'{c}', '2'+f'{c}', '3'+f'{c}'], ['4'+f'{c}', '5'+f'{c}', '6'+f'{c}'], ['7'+f'{c}', '8'+f'{c}', '9'+f'{c}']]

        self.R_colors = colors('R')
        self.L_colors = colors('L')
        self.U_colors = colors('U')
        self.D_colors = colors('D')
        self.F_colors = colors('F')
        self.B_colors = colors('B')

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

    def rotate_L(self):
        matrixU = [self.U_colors[i][0] for i in range(3)]
        for i in range(self.dim):
            self.U_colors[i][0] = self.B_colors[i][0]
            self.B_colors[i][0] = self.D_colors[i][0]
            self.D_colors[i][0] = self.F_colors[i][0]
            self.F_colors[i][0] = matrixU[i]
        self.L_colors = [[self.L_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]

    def rotate_U(self):
        matrixL = deepcopy(self.L_colors[0])
        for i in range(3):
            self.L_colors[0][i] = self.F_colors[0][i]
            self.F_colors[0][i] = self.R_colors[0][i]
            self.R_colors[0][i] = self.B_colors[2][self.dim - i - 1]
            self.B_colors[2][self.dim - i - 1] = matrixL[i]
        self.U_colors = [[self.U_colors[self.dim - j - 1][i] for j in range(self.dim)] for i in range(self.dim)]
