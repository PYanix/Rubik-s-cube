from cube_model import Cube

class Algorithms(Cube):
    def pif_paf_right(self): # правый пифпаф
        self.rotate_R()
        self.rotate_U()
        self.rotate_R_streak()
        self.rotate_U_streak()

    def pif_paf_left(self):  # левый пифпаф
        self.rotate_L_streak()
        self.rotate_U_streak()
        self.rotate_L()
        self.rotate_U()

    def first_down_cross(self): # дописать
        z0 = -1
        for (x0, y0) in ((-1,0), (1,0), (0, -1), (0,1)):
            colors = cube.get_colors(x0,y0,z0)
            solved_colors = solved_cube.get_colors(x0, y0, z0)
            x1, y1, z1 = 0, 0, 0

            if colors != solved_colors:
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        for z in range(-1, 2):
                            if x*y*z != 0:
                                continue
                            if set(cube.get_colors(x, y, z).values())==set(solved_colors.values()):
                                x1, y1, z1 = x, y, z
                                break
                print(x1, y1, z1, solved_colors)
                print((x0,y0,z0),(x1,y1,z1))
                pass
    def F1L(self): # сборка первого слоя
        z0 = -1
        x0, y0 = 1, 1
        for _ in range(4):
            colors = cube.get_colors(x0, y0, z0)
            solved_colors = solved_cube.get_colors(x0, y0, z0)
            print(set(colors.values()) == set(solved_colors.values()), set(colors.values()), set(solved_colors.values()))
            if set(colors.values()) == set(solved_colors.values()): # кубик стоит на месте, но цвета необходимо перевернуть
                    while cube.get_colors(x0, y0, z0) != solved_colors:
                        Algorithms.pif_paf_right(cube)
            elif set(colors.values()) != set(solved_colors.values()):

                # найти нужный кубик:
                x1, y1, z1, = 0, 0, 0
                for x in (-1, 1):
                    for y in (-1, 1):
                        for z in (-1, 1):
                            if set(cube.get_colors(x, y, z).values()) == set(solved_colors.values()):
                                x1, y1, z1, = x, y, z
                print((x1,y1,z1), (x0,y0,z0))
                # перевести нужный кубик на верхнюю грань над нужным положением:
                if z1 == -1:
                    if (x1, y1) == (1, -1):
                        Algorithms.pif_paf_left(cube)
                        cube.rotate_U_streak()
                        print(1)
                    elif (x1, y1) == (-1, -1):
                        cube.rotate_cube_U_streak()
                        Algorithms.pif_paf_left(cube)
                        cube.rotate_cube_U()
                        for _ in range(2):
                            cube.rotate_U()
                        print(2)
                    else:
                        cube.rotate_cube_U()
                        Algorithms.pif_paf_right(cube)
                        cube.rotate_cube_U_streak()
                        cube.rotate_U()
                        print(3)
                # поставить кубик на место:
                if cube.get_colors(x0, y0, 1)['R']==cube.get_colors(0, 0, -1)['D']:
                    Algorithms.pif_paf_right(cube)
                    print(4)
                elif cube.get_colors(x0, y0, 1)['U']==cube.get_colors(0, 0, -1)['D']:
                    print(5)
                    for _ in range(3):
                        Algorithms.pif_paf_right(cube)
                else:
                    print(6)
                    cube.rotate_cube_U()
                    Algorithms.pif_paf_left(cube)
                    cube.rotate_cube_U_streak()  # важно повернуть собранный куб тоже
            cube.rotate_cube_U()
            solved_cube.rotate_cube_U()


cube = Cube(3)
solved_cube = Cube(3) #всегда ориентировать собранный куб как и обычный куб !!!
Algorithms.pif_paf_right(cube)
Algorithms.F1L(cube)
cube.show_cube()